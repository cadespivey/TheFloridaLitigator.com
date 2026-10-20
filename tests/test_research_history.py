"""Temporal memory tests use synthetic facts, never legal conclusions."""
import json
import sqlite3

import pytest

from flwu import history as h
from flwu.history_capture import capture
from flwu.research import initialize, inspect_run
from flwu.cli import main


def payload(value="A", *, checked="2026-01-01T12:00:00+00:00", blocked=False, effective=None):
    raw = value.encode()
    cite = {"sha256": h.sha(raw), "url": "https://replay.invalid/rule", "quote": value,
            "retrieved_at": checked}
    facts = {"text": value, "publication_date": "2025-12-01"}
    if effective:
        facts.update(effective_date=effective, legal_status="future_effective")
    return {"status": "incomplete" if blocked else "ready_for_review", "contract": {},
            "checks": [{"id": "source", "status": "incomplete" if blocked else "verified",
                        "checked_at": None if blocked else checked, "hashes": [] if blocked else [h.sha(raw)]}],
            "findings": [] if blocked else [{"key": "candidate:rule", "kind": "candidate", "facts": facts, "citations": [cite]}],
            "drafts": [{"unsupported": "B"}] if blocked else []}


def save(conn, p, *, at, run="run", stream="replay", mode="synthetic_replay"):
    artifacts = {h.sha(p["findings"][0]["facts"]["text"].encode()): p["findings"][0]["facts"]["text"].encode()} if p["findings"] else {}
    return h.record(conn, stream=stream, mode=mode, scope={"counties": ["duval"]},
                    run_id=run, payload=p, artifacts=artifacts, recorded_at=at)


def test_unchanged_has_new_observation_not_new_version_and_idempotent(tmp_path):
    with h.database(tmp_path / "history.sqlite") as conn:
        p = payload()
        first = save(conn, p, at="2026-01-01T13:00:00Z")
        assert save(conn, p, at="2026-01-01T14:00:00Z") == first
        p = payload(checked="2026-01-03T12:00:00Z")
        save(conn, p, at="2026-01-03T13:00:00Z", run="run2")
        assert conn.execute("SELECT count(*) FROM finding_versions").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM finding_observations").fetchone()[0] == 2
        assert conn.execute("SELECT count(*) FROM artifacts").fetchone()[0] == 1
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-04")
        assert result["events"] == []
        assert result["assessment"] == "no_observed_change"


def test_every_transition_including_reversal_and_source_bytes(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        for day, value in ((1, "A"), (3, "B"), (4, "A")):
            when = f"2026-01-0{day}T12:00:00Z"
            save(conn, payload(value, checked=when), at=when, run=str(day))
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-05")
        events = [e for e in result["events"] if e["type"] == "finding_changed"]
        assert [(e["before"]["facts"]["text"], e["after"]["facts"]["text"]) for e in events] == [("A", "B"), ("B", "A")]
        assert sum(e["type"] == "source_changed" for e in result["events"]) == 2


def test_blocked_and_absent_never_erase_prior_facts(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(), at="2026-01-01T13:00:00Z")
        save(conn, payload(blocked=True), at="2026-01-03T13:00:00Z", run="failed")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-04")
        assert result["current_findings"]["candidate:rule"]["facts"]["text"] == "A"
        assert result["coverage_gaps"] and not result["events"]
        assert result["assessment"] == "insufficient_coverage"
        save(conn, payload("B", checked="2026-01-04T12:00:00Z"), at="2026-01-04T13:00:00Z", run="restored")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-05")
        assert any(e["type"] == "source_changed" for e in result["events"])
        absent = payload(checked="2026-01-05T12:00:00Z")
        absent["findings"] = []
        save(conn, absent, at="2026-01-05T13:00:00Z", run="limited-window")
        assert h.compare(conn, "replay", start="2026-01-04", end="2026-01-06")["current_findings"]["candidate:rule"]["facts"]["text"] == "B"


def test_finalized_baseline_not_latest_research_and_partial_rejected(tmp_path, monkeypatch):
    with h.database(tmp_path / "h.sqlite") as conn:
        first = save(conn, payload(), at="2026-01-01T13:00:00Z")
        report = tmp_path / "report.html"; report.write_text("Reviewed synthetic report")
        monkeypatch.setattr(h, "now", lambda: "2026-01-02T13:00:00+00:00")
        h.finalize(conn, first["capture_id"], report, "Tester: legal and visual review of synthetic fixture complete")
        second = save(conn, payload("B", checked="2026-01-03T12:00:00Z"), at="2026-01-03T13:00:00Z", run="second")
        third = save(conn, payload(blocked=True), at="2026-01-04T13:00:00Z", run="third")
        result = h.compare(conn, "replay", end="2026-01-05")
        assert result["baseline_known"] and result["start_utc"] == first["recorded_at"]
        assert any(e["type"] == "finding_changed" for e in result["events"])
        with pytest.raises(ValueError, match="Incomplete"):
            h.finalize(conn, third["capture_id"], report, "review")
        with pytest.raises(ValueError, match="latest"):
            h.finalize(conn, second["capture_id"], report, "review")
        assert conn.execute("SELECT count(*) FROM finalized_reports").fetchone()[0] == 1


def test_effective_date_triggers_review_without_new_bytes(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(effective="2026-01-04"), at="2026-01-01T13:00:00Z")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-04")
        assert [e["type"] for e in result["events"]] == ["effective_date_reached"]
        assert result["not_rechecked_since_baseline"] == ["source"]


def test_unknown_baseline_and_old_publication_are_not_new_law(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(), at="2026-01-03T13:00:00Z")
        result = h.compare(conn, "replay", start="2026-01-01", end="2026-01-04")
        assert not result["baseline_known"]
        assert result["events"][0]["type"] == "first_observed"
        assert result["events"][0]["after"]["facts"]["publication_date"] == "2025-12-01"
        assert not h.compare(conn, "replay", end="2026-01-04")["baseline_known"]


def test_new_york_inclusive_dates_and_dst():
    assert h.boundary("2026-03-08") == "2026-03-08T05:00:00+00:00"
    assert h.boundary("2026-03-08", end=True) == "2026-03-09T04:00:00+00:00"
    with pytest.raises(ValueError, match="timezone"):
        h.boundary("2026-01-01T00:00:00")


def test_upper_bound_excludes_next_midnight_and_preserves_start(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(), at="2026-01-02T05:00:00Z", run="start")
        save(conn, payload("B"), at="2026-01-03T05:00:00Z", run="end")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-02")
        assert len(result["events"]) == 1
        assert result["current_findings"]["candidate:rule"]["facts"]["text"] == "A"


def test_modes_isolated_and_wrong_database_rejected(tmp_path):
    db = tmp_path / "h.sqlite"
    with h.database(db) as conn:
        save(conn, payload(), at="2026-01-01T13:00:00Z")
        with pytest.raises(ValueError, match="mode/scope"):
            save(conn, payload(), at="2026-01-01T13:00:00Z", mode="manual_research")
        assert not h.compare(conn, "live")["current_findings"]
    legacy = tmp_path / "legacy.sqlite"
    with sqlite3.connect(legacy) as conn:
        conn.execute("CREATE TABLE runs(id TEXT)")
    with pytest.raises(ValueError, match="legacy schema"):
        with h.database(legacy):
            pass


def test_failed_write_rolls_back_all_checkpoint_data(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        p = payload(); del p["findings"][0]["kind"]
        with pytest.raises(KeyError):
            save(conn, p, at="2026-01-01T13:00:00Z")
        assert conn.execute("SELECT count(*) FROM captures").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM artifacts").fetchone()[0] == 0


def test_manual_status_automatically_persists_and_cli_context(tmp_path, monkeypatch, capsys):
    root = tmp_path / "research"; db = tmp_path / "h.sqlite"
    monkeypatch.setenv("FLWU_HISTORY_DB", str(db))
    initialize(root, "2026-01-01", "2026-01-08")
    inspect_run(root)
    marker = json.loads((root / "history-capture.json").read_text())
    context = json.loads((root / "history-context.json").read_text())
    assert context["coverage_gaps"] and not context["baseline_known"]
    assert capture(root)["capture_id"] == marker["capture_id"]
    output = tmp_path / "comparison.json"
    assert main(["history", "changes", "--stream", marker["stream"], "--start", "2026-01-01", "--output", str(output)]) == 0
    assert json.loads(output.read_text())["assessment"] == "insufficient_coverage"
    assert main(["history", "finalize", "--capture-id", marker["capture_id"]]) == 1
    assert main(["history", "changes", "--stream", "typo"]) == 1


def test_artifact_export_survives_deleted_workspace(tmp_path):
    db = tmp_path / "h.sqlite"
    with h.database(db) as conn:
        save(conn, payload(), at="2026-01-01T13:00:00Z")
    exported = tmp_path / "retrieved.txt"
    assert main(["history", "artifact", "--database", str(db), "--sha256", h.sha(b"A"), "--output", str(exported)]) == 0
    assert exported.read_bytes() == b"A"


def test_pending_analysis_prevents_no_change_even_with_successful_fetches(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(), at="2026-01-01T13:00:00Z")
        pending = payload(checked="2026-01-03T12:00:00Z")
        pending.update(status="incomplete", findings=[], drafts=[{"analysis": "pending"}])
        save(conn, pending, at="2026-01-03T13:00:00Z", run="pending")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-04")
        assert not result["coverage_gaps"] and not result["events"]
        assert result["assessment"] == "insufficient_coverage"


def test_reinspection_of_old_download_does_not_count_as_recheck(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(), at="2026-01-01T13:00:00Z")
        save(conn, payload(), at="2026-01-03T13:00:00Z", run="new-review-old-bytes")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-04")
        assert result["assessment"] == "insufficient_coverage"
        assert result["not_rechecked_since_baseline"] == ["source"]


def test_missing_entity_is_unknown_not_unchanged(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload(), at="2026-01-01T13:00:00Z")
        save(conn, payload(checked="2026-01-03T12:00:00Z"), at="2026-01-03T13:00:00Z", run="new")
        result = h.compare(conn, "replay", start="2026-01-02", end="2026-01-04", entity="judge:unknown")
        assert result["unknown_entity"] and result["assessment"] == "insufficient_coverage"


def test_late_import_of_old_evidence_does_not_regress_current_state(tmp_path):
    with h.database(tmp_path / "h.sqlite") as conn:
        save(conn, payload("B", checked="2026-01-03T12:00:00Z"), at="2026-01-03T13:00:00Z", run="current")
        save(conn, payload("A"), at="2026-01-04T13:00:00Z", run="old-import")
        result = h.compare(conn, "replay", start="2026-01-04", end="2026-01-05")
        assert result["current_findings"]["candidate:rule"]["facts"]["text"] == "B"
        assert [e["type"] for e in result["events"]] == ["historical_observation"]
        assert result["source_checks"]["source"]["hashes"] == [h.sha(b"B")]


def nested_evidence_payload(checked):
    """Exercise the county adapter's legacy nested citation shape."""
    import copy
    p = payload(checked=checked)
    c = copy.deepcopy(p['findings'][0]['citations'][0])
    c.update(path='raw/first.pdf', text_path='text/first.txt',
             extracted_at=checked, effective_date='2025-12-01')
    p['findings'][0]['facts']['contacts'] = [
        {'phone': '555-0100', 'identity_citations': [c]}]
    return p


def test_nested_freshness_is_not_change_and_raw_history_is_preserved(tmp_path, monkeypatch):
    import copy
    with h.database(tmp_path / 'nested.sqlite') as conn:
        old = nested_evidence_payload('2026-01-01T12:00:00Z')
        first = save(conn, old, at='2026-01-01T13:00:00Z')
        report = tmp_path / 'report.html'
        report.write_text('Synthetic finalized baseline')
        monkeypatch.setattr(h, 'now', lambda: '2026-01-02T00:00:00+00:00')
        h.finalize(conn, first['capture_id'], report, 'Synthetic test reviewer')
        new = nested_evidence_payload('2026-01-03T12:00:00Z')
        cite = new['findings'][0]['facts']['contacts'][0]['identity_citations'][0]
        cite.update(path='raw/moved.pdf', text_path='text/moved.txt')
        snapshot = copy.deepcopy(new)
        save(conn, new, at='2026-01-03T13:00:00Z', run='refresh')
        before = [tuple(r) for r in conn.execute('SELECT * FROM captures ORDER BY seq')]
        for start in (None, '2026-01-02'):
            result = h.compare(conn, 'replay', start=start, end='2026-01-04')
            assert result['events'] == []
            assert result['assessment'] == 'no_observed_change'
            assert result['current_findings']['candidate:rule']['facts'] == new['findings'][0]['facts']
        assert new == snapshot
        assert [tuple(r) for r in conn.execute('SELECT * FROM captures ORDER BY seq')] == before
        # Preserve legacy raw versions instead of migrating or rewriting history.
        assert conn.execute('SELECT count(*) FROM finding_versions').fetchone()[0] == 2
        stored = json.loads(conn.execute('SELECT payload FROM captures ORDER BY seq LIMIT 1').fetchone()[0])
        assert stored['findings'][0]['facts'] == old['findings'][0]['facts']


@pytest.mark.parametrize('field,value', [
    ('phone', '555-0199'), ('quote', 'Different requirement'),
    ('url', 'https://replay.invalid/replacement'), ('sha256', 'new-source-hash'),
    ('effective_date', '2026-02-01'), ('revision_date', '2026-01-03'),
])
def test_nested_substantive_and_source_changes_still_require_review(tmp_path, field, value):
    with h.database(tmp_path / 'changes.sqlite') as conn:
        save(conn, nested_evidence_payload('2026-01-01T12:00:00Z'), at='2026-01-01T13:00:00Z')
        new = nested_evidence_payload('2026-01-03T12:00:00Z')
        contact = new['findings'][0]['facts']['contacts'][0]
        if field == 'phone':
            contact[field] = value
        else:
            contact['identity_citations'][0][field] = value
        save(conn, new, at='2026-01-03T13:00:00Z', run='changed')
        events = h.compare(conn, 'replay', start='2026-01-02', end='2026-01-04')['events']
        assert [e['type'] for e in events] == ['finding_changed']
        assert events[0]['requires_review'] is True


def test_non_evidence_timestamp_is_not_ignored(tmp_path):
    with h.database(tmp_path / 'ordinary.sqlite') as conn:
        for day in (1, 3):
            p = payload(checked=f'2026-01-0{day}T12:00:00Z')
            p['findings'][0]['facts']['retrieved_at'] = f'ordinary substantive value {day}'
            save(conn, p, at=f'2026-01-0{day}T13:00:00Z', run=str(day))
        assert [e['type'] for e in h.compare(conn, 'replay', start='2026-01-02', end='2026-01-04')['events']] == ['finding_changed']


@pytest.mark.parametrize('changed', [False, True])
def test_older_nested_observation_does_not_roll_back_current(tmp_path, changed):
    with h.database(tmp_path / 'older.sqlite') as conn:
        current = nested_evidence_payload('2026-01-03T12:00:00Z')
        save(conn, current, at='2026-01-03T13:00:00Z')
        older = nested_evidence_payload('2026-01-01T12:00:00Z')
        if changed:
            older['findings'][0]['facts']['contacts'][0]['phone'] = '555-0199'
        save(conn, older, at='2026-01-04T13:00:00Z', run='historical')
        result = h.compare(conn, 'replay', start='2026-01-04', end='2026-01-05')
        assert [e['type'] for e in result['events']] == (['historical_observation'] if changed else [])
        assert result['current_findings']['candidate:rule']['facts'] == current['findings'][0]['facts']


def test_exact_replay_can_skip_allocator_values_without_deleted_captures(tmp_path):
    """Resume logic must use returned identity, not predict max(seq) + 1."""
    with h.database(tmp_path / "allocator.sqlite") as conn:
        first = save(conn, payload(), at="2026-01-01T13:00:00Z")
        assert save(conn, payload(), at="2026-01-01T14:00:00Z") == first
        assert conn.execute("SELECT count(*) FROM captures").fetchone()[0] == 1
        assert conn.execute("SELECT seq FROM sqlite_sequence WHERE name='captures'").fetchone()[0] > first["seq"]
        second = save(conn, payload("B"), at="2026-01-02T13:00:00Z", run="next")
        assert second["seq"] > first["seq"] + 1
        assert [row[0] for row in conn.execute("SELECT capture_id FROM captures ORDER BY seq")] == [first["capture_id"], second["capture_id"]]
        assert conn.execute("SELECT count(*) FROM finding_observations").fetchone()[0] == 2
