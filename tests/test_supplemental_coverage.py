"""Current supplement proof and coordinator recovery; disposable HTTP/DB fixtures."""
import copy
import json

import pytest

from flwu import history as h, source_gate as g, update, workflow as w
from flwu import opinion_discovery as opinions, publication_pending as pending
from flwu.evidence_binding import AcquisitionIndex
from tests.test_workflow import environment, complete_analysis
from tests.test_opinion_discovery import pdf_bytes
from tests.test_source_gate import receipt
from tests.test_content_fingerprint import page


URL = 'https://court.gov/supplement'


def supplement(db, registry, run_id='supplement', *, url=URL, body=b'Civil operating instructions.',
               success=True, reviewed=True, protocol=None, retrieved_at=None):
    reg = dict(registry, sources=[dict(id=g.source_id(url), url=url)],
               review_protocol=protocol or registry['review_protocol'])
    def fetch(address):
        return dict(url=address, resolved_url=address, retrieved_at=retrieved_at or h.now(),
                    success=success, http_status=200 if success else 403,
                    content_type='text/html' if body.startswith(b'<html') else 'text/plain'), body
    with h.database(db) as conn:
        result = g.run(conn, reg, run_id, fetch=fetch)
        if reviewed and success:
            task = result['tasks'][0]
            g.accept(conn, reg, receipt(task, reg, conn))
    return reg


def ready(tmp_path):
    run, db, reg, server = environment(tmp_path)
    assert complete_analysis(run, db)[0]['phase'] == 'prepare_report'
    return run, db, reg, server


def queue(run):
    return w.read(run/'update-queue.json')


def decision(q, url=URL):
    key = 'unregistered_source:'+h.sha({'url':url})
    return dict(task_id=key, decision='reviewed_supplement', reason='Fixture machine-proof request.', citations=[])


def validate(db, q, value):
    with h.database(db) as conn:
        return pending.validate_disposition(pending.pending(q), value,
                                           AcquisitionIndex(conn, 'weekly'), queue=q)


def test_current_review_auto_reconciles_without_another_model_receipt_or_baseline(tmp_path):
    run, db, reg, server = ready(tmp_path)
    supplement(db, reg, reviewed=False)
    assert w.inspect(run, emit=True)['kind'] == 'coverage_review'
    with pytest.raises(ValueError, match='completed matching review'):
        validate(db, queue(run), decision(queue(run)))
    with h.database(db) as conn:
        extra = dict(reg, sources=[dict(id=g.source_id(URL), url=URL)])
        task = g.queue(conn, extra)['tasks'][0]
        g.accept(conn, extra, receipt(task, extra, conn))
    assert w.inspect(run, emit=True)['phase'] == 'prepare_report'
    q = queue(run)
    assert q['acquisition_complete'] is True
    assert q['reviewed_supplements'][URL]['basis'] == 'raw_sha256'
    proof = validate(db, q, decision(q))
    assert proof['url'] == URL and proof['review_protocol'] == reg['review_protocol']
    with h.database(db) as conn:
        events = [e for e in w.events(conn, w.load(run)) if e.get('reuse', {}).get('policy') == 'reviewed_supplement']
        assert len(events) == 1 and events[0]['validation']['reviewed_supplement'] == proof
        assert events[0]['receipt']['citations'] == []  # No fabricated model quotation.
        before = conn.execute('SELECT count(*) FROM captures').fetchone()[0]
        assert h.latest_finalized(conn, 'weekly') is None
    w.inspect(run)
    with h.database(db) as conn:
        assert conn.execute('SELECT count(*) FROM captures').fetchone()[0] == before


@pytest.mark.parametrize('change', ['failed', 'changed', 'protocol', 'old_time', 'different_url', 'legacy_review'])
def test_stale_failed_changed_cross_url_and_unsubstantiated_reviews_stay_pending(tmp_path, change):
    run, db, reg, server = ready(tmp_path)
    if change == 'old_time':
        supplement(db, reg, retrieved_at='2000-01-01T00:00:00+00:00')
    elif change == 'different_url':
        supplement(db, reg, 'other-url-source', url=URL+'-other')
        supplement(db, reg, reviewed=False)
    elif change == 'protocol':
        supplement(db, reg, protocol='other-protocol')
    else:
        supplement(db, reg)
        if change in ('failed', 'changed'):
            supplement(db, reg, 'new-bytes', success=change != 'failed', reviewed=False,
                       body=b'Changed civil filing requirements.' if change == 'changed' else b'Forbidden')
        else:
            with h.database(db) as conn:
                row = conn.execute("SELECT seq,payload FROM captures WHERE json_extract(payload,'$.source_gate_review.source_id')=? ORDER BY seq DESC LIMIT 1", (g.source_id(URL),)).fetchone()
                payload = json.loads(row['payload']); payload['source_gate_review']['acceptance_version'] = 2
                conn.execute('UPDATE captures SET payload=? WHERE seq=?', (h.canonical(payload), row['seq']))
                conn.commit()
    phase = w.inspect(run, emit=True)
    q = queue(run)
    assert phase['kind'] == 'coverage_review'
    assert URL not in q['reviewed_supplements']
    with pytest.raises(ValueError, match='completed matching review'):
        validate(db, q, decision(q))


def test_supported_content_hash_reuse_preserves_changed_raw_bytes(tmp_path):
    run, db, reg, server = ready(tmp_path)
    url = 'https://5dca.flcourts.gov/Judges/Example'
    supplement(db, reg, url=url, body=page())
    supplement(db, reg, 'metadata-only', url=url, body=page(stamp='2026-10-21T12:00:00Z'), reviewed=False)
    assert w.inspect(run)['phase'] == 'prepare_report'
    proof = queue(run)['reviewed_supplements'][url]
    assert proof['basis'] == 'content_and_component_hashes'
    raw = proof['content_hash_reuse']
    assert raw['current_fingerprint']['original_sha256'] != raw['reviewed_fingerprint']['original_sha256']
    assert raw['current_fingerprint']['core_sha256'] == raw['reviewed_fingerprint']['core_sha256']


def test_changed_evidence_invalidates_completed_url_only_coverage_and_saved_snapshot_remains_valid(tmp_path):
    run, db, reg, server = ready(tmp_path)
    supplement(db, reg)
    assert w.inspect(run)['phase'] == 'prepare_report'
    old = queue(run)
    with h.database(db) as conn:
        bound = conn.execute('SELECT max(seq) FROM captures').fetchone()[0]
    supplement(db, reg, 'changed-again', body=b'New civil procedures.', reviewed=False)
    assert w.inspect(run, emit=True)['kind'] == 'coverage_review'
    with pytest.raises(ValueError, match='completed matching review'):
        validate(db, old, decision(old))
    with h.database(db) as conn:
        proof = pending.validate_disposition(pending.pending(old), decision(old),
                                             AcquisitionIndex(conn, 'weekly', through_seq=bound), queue=old)
        assert proof == old['reviewed_supplements'][URL]


def test_queue_proof_cannot_be_forged_or_applied_to_effective_date_or_listing_failure(tmp_path):
    run, db, reg, server = ready(tmp_path)
    supplement(db, reg)
    w.inspect(run)
    q = queue(run); forged = copy.deepcopy(q)
    forged['reviewed_supplements'][URL]['sha256'] = '0'*64
    with pytest.raises(ValueError, match='proof is stale'):
        validate(db, forged, decision(forged))
    for kind in ('effective_date', 'listing_failure'):
        key = kind+':fixture'
        with h.database(db) as conn, pytest.raises(ValueError, match='completed matching review'):
            pending.validate_disposition({key:dict(task={'url':URL}, unavailable=True, hashes=set())},
                                         dict(decision(q), task_id=key), AcquisitionIndex(conn, 'weekly'), queue=q)


def test_opinion_details_use_actual_completed_standard_monitor_without_html_rereview(tmp_path):
    run, db, reg, server = ready(tmp_path)
    url = server.entries[0]['content']['url']
    # A former generic HTML source is now independently monitored as opinion metadata.
    supplement(db, reg, url=url, body=server(url)[1], reviewed=False)
    assert w.inspect(run)['phase'] == 'prepare_report'
    q = queue(run); proof = q['reviewed_supplements'][url]
    assert proof['kind'] == 'opinion_monitor'
    assert proof['scope'] == 'official_opinion_metadata_and_pdf'
    with h.database(db) as conn:
        item = opinions.known(conn, 'weekly')[proof['opinion_id']]
        server.entries[0]['content']['fields']['note'] = 'Withdrawn'
        meta, raw = server(url)
        updated = opinions.detail(raw, opinions.COURTS[1], item)
        event = dict(kind='detail', id=item['id'], source=meta, sha256=h.sha(raw), complete=True,
                     entries=opinions.bind_status([updated], meta, raw))
        opinions.save(conn, 'weekly', 'trial', 'detail:'+item['id'], event, raw)
    phase = w.inspect(run, emit=True)
    assert phase['kind'] == 'opinion_review'  # Identical PDF cannot waive withdrawal screening.
    assert url not in queue(run)['reviewed_supplements']


def test_changed_pdf_cannot_reuse_completed_opinion_monitor(tmp_path):
    run, db, reg, server = ready(tmp_path)
    url = server.entries[0]['content']['url']
    supplement(db, reg, url=url, body=server(url)[1], reviewed=False)
    assert w.inspect(run)['phase'] == 'prepare_report'
    with h.database(db) as conn:
        item = next(i for i in opinions.known(conn, 'weekly').values() if i['detail_url'] == url)
    supplement(db, reg, 'revised-pdf', url=item['pdf_url'],
               body=pdf_bytes('Revised commercial holding.'), reviewed=False)
    phase = w.inspect(run, emit=True)
    assert phase['kind'] == 'opinion_review'
    assert url not in queue(run)['reviewed_supplements']


def test_interruption_after_machine_decision_recovers_projection_without_repeating_review(tmp_path, monkeypatch):
    run, db, reg, server = ready(tmp_path)
    supplement(db, reg)
    original = w.write
    def interrupted(path, *args, **kwargs):
        if '/workflow/accepted/' in str(path):
            raise RuntimeError('Interrupted after database decision')
        return original(path, *args, **kwargs)
    monkeypatch.setattr(w, 'write', interrupted)
    with pytest.raises(RuntimeError, match='after database decision'):
        w.inspect(run)
    monkeypatch.setattr(w, 'write', original)
    assert w.inspect(run)['phase'] == 'prepare_report'
    with h.database(db) as conn:
        events = [e for e in w.events(conn, w.load(run)) if e.get('reuse', {}).get('policy') == 'reviewed_supplement']
        assert len(events) == 1
        assert (run/'workflow/accepted'/(events[0]['packet_sha256']+'.json')).is_file()
