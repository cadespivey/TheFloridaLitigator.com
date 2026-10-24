"""Negative tests of the reviewed trial's failure paths; no live requests."""
import copy
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest

from flwu.research import initialize, inspect_run, write_json, _source, _person, _citation
from flwu.fixture_pipeline import run_fixture
from flwu.state import open_db, migrate, begin_run, begin_attempt, commit_acquisition, finalize_run
from flwu.fetch import _BoundedClient, FetchError
from flwu.registry import load_sources, validate_sources


def now():
    return datetime.now(timezone.utc).isoformat()


@pytest.fixture
def workspace(tmp_path):
    initialize(tmp_path, "2026-01-01", "2026-01-08")
    return tmp_path


def citation(root, url="https://example.invalid/source"):
    # Test-only replay bytes. Never used as live research evidence.
    data = b"No further pages. Example Judge. Example clerk. Prior rule. New rule."
    sha = hashlib.sha256(data).hexdigest()
    (root / "raw" / sha).write_bytes(data)
    (root / "text" / sha).write_bytes(data)
    ref = {"path": "raw/" + sha, "sha256": sha, "url": url,
            "retrieved_at": now(), "http_status": 200, "authority": "official", "synthetic": False,
            "text_path": "text/" + sha, "text_sha256": sha, "locator": "paragraph 1",
            "quote": "No further pages. Example Judge. Example clerk."}
    from flwu import history as h
    from flwu.history_capture import stream_for
    target = stream_for(json.loads((root/'contract.json').read_text()))[0]
    with h.database() as conn:
        h.record(conn, stream='test-acquisition', mode='manual_research',
                 scope={'target_stream':target}, run_id=ref['retrieved_at'],
                 payload={'status':'incomplete','contract':{},'checks':[], 'findings':[], 'drafts':[],
                          'source_gate':dict(ref, success=True)}, artifacts={sha:data})
    return ref


def receipt(root, task="S01-01"):
    task_url = next(t["url"] for t in contract(root)["tasks"] if t["id"] == task)
    ref = citation(root, task_url)
    return {"task_id": task, "status": "complete", "checked_at": now(),
            "pages": [ref], "pages_complete": True, "freshness_verified": True,
            "pagination": {"next": None, "stop_reason": "terminal index", "evidence": ref},
            "candidates": [], "entities": [], "errors": []}


def contract(root):
    return json.loads((root / "contract.json").read_text())


def test_new_workspace_incomplete_and_resumable(workspace):
    first = inspect_run(workspace)
    initialize(workspace, "2026-01-01", "2026-01-08")
    assert inspect_run(workspace) == first
    assert first["status"] == "incomplete" and first["publication_ready"] is False
    assert "S01-01" in (workspace / "RESUME.txt").read_text()
    assert {"putnam", "clay"} <= set(contract(workspace)["counties"])
    assert contract(workspace)["circuits"] == [4, 7, 8]
    with pytest.raises(ValueError, match="differs"):
        initialize(workspace, "2026-01-01", "2026-01-08", "statewide-circuits")


def test_statewide_profile_has_twenty_circuits(tmp_path):
    initialize(tmp_path, "2026-01-01", "2026-01-08", "statewide-circuits")
    data = contract(tmp_path)
    assert data["circuits"] == list(range(1, 21))
    assert len([t for t in data["tasks"] if t["id"].startswith("roster-circuit-")]) == 20


def test_contract_edit_rejected(workspace):
    data = contract(workspace)
    data["tasks"] = []
    write_json(workspace / "contract.json", data)
    with pytest.raises(ValueError, match="contract changed"):
        inspect_run(workspace)


@pytest.mark.parametrize("failure", ["pagination", "bytes", "quote", "future", "stale", "escape", "synthetic", "candidate"])
def test_bad_evidence_cannot_complete_task(workspace, failure):
    r = receipt(workspace)
    if failure == "pagination": r["pagination"]["next"] = "page-2"
    if failure == "bytes": (workspace / r["pages"][0]["path"]).write_text("tampered")
    if failure == "quote": r["pagination"]["evidence"]["quote"] = "invented statement"
    if failure == "future": r["checked_at"] = "2099-01-01T00:00:00Z"
    if failure == "stale": r["pages"][0]["retrieved_at"] = "2020-01-01T00:00:00Z"
    if failure == "escape": r["pages"][0]["path"] = "../outside"
    if failure == "synthetic": r["pages"][0]["synthetic"] = True
    if failure == "candidate": r["candidates"] = [{"id": "x", "decision": "pending"}]
    write_json(workspace / "receipts/S01-01.json", r)
    result = inspect_run(workspace)
    assert result["tasks"][0]["status"] == "incomplete"
    assert result["tasks"][0]["reason"]


def test_empty_source_requires_real_index_evidence(workspace):
    r = receipt(workspace)
    _source(workspace, contract(workspace), r, "source")
    r["pages"] = []
    with pytest.raises(ValueError, match="index"):
        _source(workspace, contract(workspace), r, "source")


def test_roster_expands_to_required_people(workspace):
    r = receipt(workspace, "roster-circuit-4")
    r.update(roster_reconciled=True, entities=[{"id": "example-judge", "type": "judge", "name": "Example Judge",
                    "counties": ["duval"], "citation": r["pages"][0]}])
    write_json(workspace / "receipts/roster-circuit-4.json", r)
    status = inspect_run(workspace)
    assert any(t["task_id"] == "person-example-judge" and t["status"] == "incomplete" for t in status["tasks"])


@pytest.mark.parametrize("failure", ["old", "effective", "change"])
def test_date_and_change_claims_rejected(workspace, failure):
    r = receipt(workspace)
    ref = r["pages"][0]
    candidate = {"id": "opinion", "decision": "include", "reason": "relevant", "citation": ref,
                 "publication_date": "2026-01-02", "effective_date": "2026-01-03", "effective_date_reviewed": True,
                 "legal_status": "operative", "claims": [{"statement": "new rule", "review": "supported", "citation": ref}]}
    if failure == "old": candidate["publication_date"] = "2025-01-01"
    if failure == "effective": candidate["effective_date"] = "2027-01-01"
    if failure == "change": candidate["claims"][0]["change"] = True
    r["candidates"] = [candidate]
    with pytest.raises((ValueError, KeyError)):
        _source(workspace, contract(workspace), r, "source")


def test_person_requires_specific_procedure(workspace):
    ref = citation(workspace)
    r = {"task_id": "person-example-judge", "entity_type": "judge", "fields": {key: {"status": "verified", "value": "example", "citation": ref}
         for key in ("chambers_phone", "chambers_address", "assistant_name", "assistant_contact")},
         "procedure": {"status": "blocked", "citation": ref}, "governing_rules": [{"citation": ref}]}
    with pytest.raises(ValueError, match="procedure"):
        _person(workspace, r, True)
    r["procedure"] = {"status": "verified", "citation": ref, "applies_to": "example-judge", "documents": [{"citation": ref, "applicability": "Example Judge division"}]}
    _person(workspace, r, True)


def test_repeated_same_state_and_date_filter(tmp_path):
    args = (Path("fixtures/synthetic-source.json"), tmp_path / "state", tmp_path / "output")
    kwargs = {"observed_at": "2026-10-11T10:00:00Z", "window_start": "2026-10-04", "window_end": "2026-10-10"}
    a = run_fixture(*args, **kwargs)
    b = run_fixture(*args, **kwargs)
    assert a["issue_id"] == b["issue_id"]
    assert all("2026-10-04" <= r["publication_date"] <= "2026-10-10" for group in b["categories"].values() for r in group)
    with sqlite3.connect(tmp_path / "state/flwu.db") as conn:
        assert conn.execute("SELECT count(*) FROM runs").fetchone()[0] == 2
        assert conn.execute("SELECT count(*) FROM runs WHERE status='running' OR finished_at IS NULL").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM source_attempts WHERE status!='complete' OR finished_at IS NULL").fetchone()[0] == 0
        revisions = conn.execute("SELECT count(*) FROM revisions").fetchone()[0]
        assert conn.execute("SELECT count(*) FROM observations").fetchone()[0] == 2 * revisions
        json.loads(conn.execute("SELECT revision_ids_json FROM source_snapshots LIMIT 1").fetchone()[0])


def test_issue_identity_across_hash_seeds(tmp_path):
    code = "from pathlib import Path; from flwu.fixture_pipeline import run_fixture; import sys; print(run_fixture(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), observed_at='2026-01-09T00:00:00Z')['issue_id'])"
    results = []
    for seed in ("1", "2"):
        results.append(subprocess.check_output([sys.executable, "-c", code, str(Path("fixtures/synthetic-source.json").resolve()), str(tmp_path / seed), str(tmp_path / (seed + "out"))], env={**os.environ, "PYTHONHASHSEED": seed, "PYTHONDONTWRITEBYTECODE": "1"}, text=True).strip())
    assert results[0] == results[1]


def test_acquisition_rolls_back_real_partial_write(tmp_path):
    conn = open_db(tmp_path / "test.db")
    migrate(conn)
    begin_run(conn, run_id="r", mode="fixture", window_start="2026-01-01", window_end="2026-01-08", created_at=now())
    begin_attempt(conn, attempt_id="a", run_id="r", source_id="s", started_at=now())
    rec = {"document_id": "d", "revision_id": "v", "content_sha256": "sha", "record_json": "{}", "document_key": "key", "canonical_url": "url"}
    kwargs = dict(attempt_id="a", source_id="s", watermark_utc=now(), profile_id="p", coverage={"complete": True, "pages_complete": True, "freshness_verified": True})
    with pytest.raises(sqlite3.IntegrityError):
        commit_acquisition(conn, records=[rec, rec], **kwargs)
    assert conn.execute("SELECT count(*) FROM documents").fetchone()[0] == 0
    assert conn.execute("SELECT count(*) FROM source_checkpoints").fetchone()[0] == 0
    commit_acquisition(conn, records=[rec], **kwargs)
    original = conn.execute("SELECT snapshot_id FROM source_checkpoints").fetchone()[0]
    begin_attempt(conn, attempt_id="b", run_id="r", source_id="s", started_at=now())
    with pytest.raises(sqlite3.IntegrityError):
        commit_acquisition(conn, records=[rec, rec], **{**kwargs, "attempt_id": "b"})
    assert conn.execute("SELECT snapshot_id FROM source_checkpoints").fetchone()[0] == original
    result = finalize_run(conn, run_id="r", required_source_ids=["s"], required_scope_ids=["duval"], scope_coverage=[{"source_id": "s", "complete": False}], profile_id="p", has_changes=False, finished_at=now())
    assert result == "incomplete"
    conn.close()


@pytest.mark.parametrize("status_codes,expected", [([429, 200], None), ([429, 429], "RETRY_EXHAUSTED")])
def test_http_retry(monkeypatch, status_codes, expected):
    calls, waits = [], []
    @contextmanager
    def stream(*args, **kwargs):
        calls.append(args)
        yield httpx.Response(status_codes[len(calls)-1], headers={"Retry-After": "0"}, content=b"ok", request=httpx.Request("GET", "https://example.invalid"))
    monkeypatch.setattr(httpx, "stream", stream)
    monkeypatch.setattr("flwu.fetch.time.sleep", waits.append)
    client = _BoundedClient(max_retries=1)
    if expected:
        with pytest.raises(FetchError, match=expected): client.fetch("https://example.invalid")
    else: assert client.fetch("https://example.invalid") == "ok"
    assert len(calls) == 2 and waits == [0]


def test_http_stream_budget(monkeypatch):
    @contextmanager
    def stream(*args, **kwargs):
        yield httpx.Response(200, content=b"too long", request=httpx.Request("GET", "https://example.invalid"))
    monkeypatch.setattr(httpx, "stream", stream)
    client = _BoundedClient(max_bytes=2, max_pages=1)
    with pytest.raises(FetchError, match="RESPONSE_TOO_LARGE"): client.fetch("https://example.invalid")
    with pytest.raises(FetchError, match="PAGE_LIMIT"): client.fetch("https://example.invalid")


def test_each_critical_source_required():
    sources = load_sources()
    for s in sources:
        if s["critical"]:
            with pytest.raises(ValueError): validate_sources([x for x in sources if x != s])


def test_config_applies_production_security(tmp_path):
    from flwu.config import load_config, ConfigError
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"mode": "production", "model": {"base_url": "http://localhost.evil.test"}}))
    with pytest.raises(ConfigError, match="MODEL_URL"): load_config(p)


def test_scope_doc_entry_point(tmp_path):
    from flwu.scope_docs import generate_all_scope_docs
    paths = generate_all_scope_docs(tmp_path)
    assert paths and all(p.exists() for p in paths)
    assert any("RUNBOOK" in p.read_text() for p in paths)


def test_complete_replay_ready_for_review_but_never_publication(workspace):
    """Full synthetic replay proves the positive path and then withholds a person."""
    for task in contract(workspace)["tasks"]:
        r = receipt(workspace, task["id"])
        if task["kind"] == "roster" or task["group"].startswith("clerk_"):
            types = ["judge"] if task["kind"] == "roster" else []
            if not task["group"].startswith("circuit-"): types.append("clerk")
            r.update(roster_reconciled=True, entities=[{
                "id": task["id"].lower() + "-" + kind, "name": "Example " + kind,
                "type": kind, "counties": ["duval"] if task["group"].startswith("circuit-") else [],
                "citation": r["pages"][0]} for kind in types])
        write_json(workspace / "receipts" / (task["id"] + ".json"), r)
    status = inspect_run(workspace)
    assert status["status"] == "incomplete"
    people = [r for r in status["tasks"] if r["task_id"].startswith("person-")]
    assert len(people) == 24  # ten court rosters + seven appellate and seven county clerks
    for person in people:
        path = workspace / "receipts" / (person["task_id"] + ".json")
        r = json.loads(path.read_text())
        ref = citation(workspace)
        r.update(status="complete", checked_at=now())
        for field in r["fields"].values(): field.update(status="verified", value="Example", citation=ref)
        r["procedure"].update(status="verified", citation=ref, documents=[{"citation": ref, "applicability": "Example division"}])
        r["governing_rules"] = [{"citation": ref}]
        write_json(path, r)
    status = inspect_run(workspace)
    assert status["status"] == "ready_for_review", status
    assert status["publication_ready"] is False
    withheld = workspace / "receipts" / (people[0]["task_id"] + ".json")
    withheld.unlink()
    assert inspect_run(workspace)["status"] == "incomplete"


def test_fixture_inclusive_boundaries(tmp_path):
    raw = json.loads(Path("fixtures/synthetic-source.json").read_text())
    base = raw["records"][0]
    raw["records"] = [{**base, "official_key": f"TEST-{n}", "publication_date": day}
                      for n, day in enumerate(["2026-01-01", "2026-01-02", "2026-01-08", "2026-01-09"])]
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(raw))
    issue = run_fixture(path, tmp_path / "state", tmp_path / "output", window_start="2026-01-02", window_end="2026-01-08")
    records = [r for rows in issue["categories"].values() for r in rows]
    assert sorted(r["publication_date"] for r in records) == ["2026-01-02", "2026-01-08"]


def test_preview_render_failure_terminalizes_run(tmp_path, monkeypatch):
    def fail(*args): raise RuntimeError("injected render failure")
    monkeypatch.setattr("flwu.fixture_pipeline._build_html_preview", fail)
    with pytest.raises(RuntimeError, match="injected"):
        run_fixture(Path("fixtures/synthetic-source.json"), tmp_path / "state", tmp_path / "out")
    with sqlite3.connect(tmp_path / "state/flwu.db") as conn:
        assert conn.execute("SELECT status, finished_at FROM runs").fetchone()[0] == "failed"
        assert conn.execute("SELECT count(*) FROM runs WHERE finished_at IS NULL").fetchone()[0] == 0


def test_required_source_cannot_be_made_optional():
    sources = copy.deepcopy(load_sources())
    sources[0]["critical"] = False
    with pytest.raises(ValueError, match="downgraded"): validate_sources(sources)


def test_acquired_same_host_page_cannot_replace_required_task(workspace):
    r = receipt(workspace)
    wrong = citation(workspace, r["pages"][0]["url"] + "?unrelated=1")
    r.update(pages=[wrong], checked_at=now())
    r["pagination"]["evidence"] = wrong
    write_json(workspace / "receipts/S01-01.json", r)
    result = inspect_run(workspace)
    assert result["tasks"][0]["status"] == "incomplete"
    assert "Required task URL" in result["tasks"][0]["reason"]


def test_inspection_reuses_marker_database_and_rejects_override(workspace, tmp_path):
    db = tmp_path / "pinned.sqlite"
    inspect_run(workspace, history_db=db)
    result = inspect_run(workspace)
    marker = json.loads((workspace / "history-capture.json").read_text())
    assert Path(marker["database"]) == db
    assert result["status"] == "incomplete"
    with pytest.raises(ValueError, match="database is pinned"):
        inspect_run(workspace, history_db=tmp_path / "other.sqlite")
    assert not (tmp_path / "other.sqlite").exists()


def test_person_receipt_cannot_change_roster_name(workspace):
    r = receipt(workspace, "roster-circuit-4")
    r.update(roster_reconciled=True, entities=[{"id":"example-judge", "type":"judge", "name":"Example Judge",
                 "counties":["duval"], "citation":r["pages"][0]}])
    write_json(workspace / "receipts/roster-circuit-4.json", r)
    inspect_run(workspace)
    path = workspace / "receipts/person-example-judge.json"
    person = json.loads(path.read_text())
    person.update(status="complete", checked_at=now(), name="Different Judge")
    write_json(path, person)
    status = inspect_run(workspace)
    result = next(t for t in status['tasks'] if t['task_id'] == 'person-example-judge')
    assert result['status'] == 'incomplete'
    assert 'name differs' in result['reason']
