"""Explicit source row dates queue review without interpreting which date controls."""
import pytest

from flwu import history as h


@pytest.fixture
def dated_history(tmp_path):
    with h.database(tmp_path / "history.sqlite") as conn:
        def seed(facts):
            raw = b"Same preserved assignment order"
            for day in (1, 2):
                when = f"2026-12-0{day}T12:00:00+00:00"
                h.record(conn, stream="dates", mode="synthetic_replay", scope={"profile": "row-dates"},
                         run_id=str(day), recorded_at=when,
                         payload={"status": "ready_for_review", "contract": {}, "drafts": [],
                                  "checks": [{"id": "order", "status": "verified",
                                              "checked_at": when, "hashes": [h.sha(raw)]}],
                                  "findings": [{"key": "assignments", "kind": "court_administration",
                                                "facts": facts,
                                                "citations": [{"url": "https://replay.invalid/order",
                                                               "sha256": h.sha(raw), "quote": raw.decode(),
                                                               "retrieved_at": when}]}]},
                         artifacts={h.sha(raw): raw})
        yield conn, seed


@pytest.mark.parametrize("day,expected", [("01", 1), ("04", 1), ("05", 1), ("02", 0)])
def test_general_and_distinct_row_dates_remain_independent_review_events(dated_history, day, expected):
    conn, seed = dated_history
    facts = {"effective_date": "2027-01-04", "issued_date": "2027-01-02",
             "rows": [{"judge": "First", "row_effective_date": "2027-01-01"},
                      {"judge": "Second", "row_effective_date": "2027-01-05"}],
             "date_discrepancy": "Preserve each source statement; no controlling-date conclusion."}
    seed(facts)
    counts = conn.execute("SELECT count(*) FROM captures").fetchone()[0]
    result = h.compare(conn, "dates", start=f"2027-01-{day}", end=f"2027-01-{day}")
    assert len(result["events"]) == expected
    if expected:
        event = result["events"][0]
        assert (event["type"], event["effective_date"], event["requires_review"]) == (
            "effective_date_reached", f"2027-01-{day}", True)
        assert event["after"]["facts"] == facts
    assert result["current_findings"]["assignments"]["facts"] == facts
    assert conn.execute("SELECT count(*) FROM captures").fetchone()[0] == counts
    assert conn.execute("SELECT count(*) FROM finding_versions").fetchone()[0] == 1
    assert conn.execute("SELECT count(*) FROM finalized_reports").fetchone()[0] == 0


def test_same_date_in_general_and_row_fields_is_not_duplicated(dated_history):
    conn, seed = dated_history
    seed({"effective_date": "2027-01-01", "rows": [{"row_effective_date": "2027-01-01"}]})
    assert len(h.compare(conn, "dates", start="2027-01-01", end="2027-01-01")["events"]) == 1


def test_withdrawn_row_and_empty_dates_do_not_create_clock_events(dated_history):
    conn, seed = dated_history
    seed({"rows": [{"row_effective_date": "2027-01-01", "legal_status": "withdrawn"},
                   {"row_effective_date": None}]})
    assert not h.compare(conn, "dates", start="2027-01-01", end="2027-01-01")["events"]


def test_unparseable_row_date_stays_unresolved(dated_history):
    conn, seed = dated_history
    seed({"rows": [{"row_effective_date": "date uncertain"}]})
    events = h.compare(conn, "dates", start="2027-01-01", end="2027-01-01")["events"]
    assert len(events) == 1
    assert events[0]["type"] == "unresolved_effective_date"
    assert events[0]["requires_review"] is True
