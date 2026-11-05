"""Queue filtering must not reload opinion history for every omitted URL."""
import copy
import sqlite3

import pytest

from flwu import evidence_binding, update


@pytest.mark.parametrize("omitted_count", [0, 40])
@pytest.mark.parametrize("failed_source", [False, True])
@pytest.mark.parametrize("unavailable_opinion", [False, True])
def test_refresh_reuses_history_without_hiding_source_or_opinion_failures(
    tmp_path, monkeypatch, omitted_count, failed_source, unavailable_opinion
):
    old_pdf = "https://court.example/opinion.pdf?version=1"
    new_pdf = "https://court.example/opinion.pdf?version=2"
    missing_pdf = "https://court.example/unavailable.pdf"
    omitted = [f"https://court.example/procedure/{n}" for n in range(omitted_count)]
    history = [
        {"run_id": "one", "checkpoint": "entries", "entries": [{"pdf_url": old_pdf}]},
        {"run_id": "one", "checkpoint": "entries", "entries": [{"pdf_url": new_pdf}]},
        {"run_id": "one", "checkpoint": "entries", "entries": [{"pdf_url": missing_pdf}]},
        {"run_id": "one", "checkpoint": "update-result", "queue_sha256": "prior"},
    ]
    reads = []

    def events(conn, stream):
        reads.append(stream)
        return copy.deepcopy(history)

    source_tasks = [
        {"source_id": update.gate.source_id(old_pdf), "url": old_pdf, "reason": "changed"},
        {"source_id": update.gate.source_id(new_pdf), "url": new_pdf, "reason": "changed"},
    ]
    if unavailable_opinion:
        source_tasks.append({"source_id": update.gate.source_id(missing_pdf), "url": missing_pdf,
                             "reason": "retrieval_failed"})
    if failed_source:
        source_tasks.append({"source_id": update.gate.source_id("https://court.example/profile"),
                             "url": "https://court.example/profile",
                             "reason": "retrieval_failed"})
    source_queue = {"tasks": source_tasks, "unregistered_previous_sources":
                    [old_pdf, new_pdf, missing_pdf, *omitted]}
    # A missing PDF still has saved status evidence and a pending opinion task.
    opinion_queue = {"tasks": ([{
        "opinion": {"id": "missing", "pdf_url": missing_pdf,
                    "status_source": {"sha256": "raw", "text_sha256": "text"}},
        "reasons": ["opinion_download_unavailable"],
        "source_observation": None, "prior_review": None,
    }] if unavailable_opinion else [])}

    class Index:
        source_observations = {}
        detail_events = {}

        def __init__(self, conn, stream):
            pass

        def reviewed_supplement(self, queue, url):
            return None

    monkeypatch.setattr(update.gate, "write_queue", lambda *a, **kw: copy.deepcopy(source_queue))
    monkeypatch.setattr(update.gate, "blob", lambda conn, digest: b"saved status evidence")
    monkeypatch.setattr(update.opinions, "review_queue", lambda *a: copy.deepcopy(opinion_queue))
    monkeypatch.setattr(update.opinions, "events", events)
    monkeypatch.setattr(update.opinions, "save", lambda *a, **kw: None)
    monkeypatch.setattr(evidence_binding, "AcquisitionIndex", Index)
    result = update.refresh_queue(sqlite3.connect(':memory:'), {"stream": "weekly"}, "one", tmp_path,
                                  {"start": "2026-10-23", "end": "2026-10-25"},
                                  {"complete": True})

    assert reads == ["weekly", "weekly"]
    assert result["source_reviews"]["unregistered_previous_sources"] == omitted
    assert result["source_reviews"]["tasks"] == (source_tasks[-1:] if failed_source else [])
    if unavailable_opinion:
        candidate = result["opinion_reviews"]["tasks"][0]
        assert candidate["opinion"]["pdf_url"] == missing_pdf
        assert candidate["reasons"] == ["opinion_download_unavailable"]
        assert candidate["document_files"] == source_tasks[2]
    else:
        assert not result["opinion_reviews"]["tasks"]
    expected_complete = not (omitted_count or failed_source or unavailable_opinion)
    assert result["acquisition_complete"] is expected_complete
    assert set(result["unregistered_source_evidence"]) == set(omitted)
    assert not result["reviewed_supplements"]
    assert not result["publication_performed"]
