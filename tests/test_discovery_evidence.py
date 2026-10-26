import copy
import json

import pytest

from flwu import history as h, opinion_discovery as d
from flwu.discovery_evidence import page_binding, validate_channel
from flwu.evidence_binding import AcquisitionIndex
from tests.test_opinion_discovery import Server, opinion


def saved(conn, entries=()):
    h.record(conn, stream='report', mode='manual_research', scope={}, run_id='initial',
             payload={'status':'incomplete','checks':[],'findings':[],'drafts':[]}, artifacts={})
    bounds = d.window(conn, 'report', start='2026-10-16', end='2026-10-22')
    contract = dict(bounds=bounds, courts=d.COURTS, page_size=50, max_pages=200)
    d.discover(conn, 'report', 'run', bounds, fetch=Server(list(entries)))
    rows = conn.execute('SELECT capture_id,payload FROM captures ORDER BY seq').fetchall()
    captures = [(r['capture_id'], json.loads(r['payload']).get('opinion_discovery', {})) for r in rows]
    return contract, captures


def test_empty_feed_is_bound_to_original_bytes_and_exact_capture(tmp_path):
    with h.database(tmp_path/'db') as conn:
        contract, captures = saved(conn)
        channel = d.COURTS[0]['id']+':inactive'
        refs = validate_channel(conn, captures, contract, channel)
        assert len(refs) == 1
        ref = refs[0]
        assert ref['sha256'] == ref['text_sha256']
        ref.update(quote='"totalCount": 0', locator='Original JSON totalCount')
        AcquisitionIndex(conn, 'report').validate(ref)
        for key, value in [('url', 'https://supremecourt.flcourts.gov/another'),
                           ('retrieved_at', '2000-01-01T00:00:00Z'),
                           ('http_status', 201), ('acquisition_capture_id', 'forged')]:
            with pytest.raises(ValueError, match='does not match'):
                AcquisitionIndex(conn, 'report').validate(dict(ref, **{key: value}))
        with pytest.raises(ValueError, match='does not match'):
            AcquisitionIndex(conn, 'another-report').validate(ref)


def test_channel_requires_every_page_and_rejects_duplicate_checkpoint(tmp_path):
    with h.database(tmp_path/'db') as conn:
        contract, captures = saved(conn, [opinion(1), opinion(2)])
        channel = d.COURTS[1]['id']+':listing'
        pages = [(cap, e) for cap, e in captures if e.get('kind') == 'page' and e['channel'] == channel]
        assert len(validate_channel(conn, pages, contract, channel)) == 2
        with pytest.raises(ValueError, match='missing page'):
            validate_channel(conn, pages[:1], contract, channel)
        with pytest.raises(ValueError, match='Duplicate discovery page'):
            validate_channel(conn, pages+pages[:1], contract, channel)


@pytest.mark.parametrize('mutation', ['missing_blob', 'invalid_json', 'wrong_court',
                                    'wrong_total', 'premature_empty', 'wrong_ids'])
def test_page_reparses_original_and_rejects_corruption(tmp_path, mutation):
    with h.database(tmp_path/'db') as conn:
        contract, captures = saved(conn)
        cap, original = next((cap, e) for cap, e in captures if e.get('kind') == 'page')
        event = copy.deepcopy(original)
        if mutation == 'missing_blob':
            event['sha256'] = '0'*64
        elif mutation == 'invalid_json':
            # Use a real existing non-JSON artifact, not a fabricated hash.
            raw = b'not JSON'
            h.record(conn, stream='auxiliary', mode='manual_research', scope={}, run_id='bad',
                     payload={'status':'incomplete','checks':[],'findings':[],'drafts':[]},
                     artifacts={h.sha(raw):raw})
            event['sha256'] = h.sha(raw)
        elif mutation == 'wrong_court':
            event['court'] = d.COURTS[1]['id']
        elif mutation == 'wrong_total':
            event['total'] = 99
        elif mutation == 'wrong_ids':
            event['page_ids'] = ['invented']
        else:
            raw = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (event['sha256'],)).fetchone()[0]
            body = json.loads(raw);body['totalCount'] = 1;raw = json.dumps(body).encode()
            h.record(conn, stream='auxiliary', mode='manual_research', scope={}, run_id='premature',
                     payload={'status':'incomplete','checks':[],'findings':[],'drafts':[]},
                     artifacts={h.sha(raw):raw})
            event.update(sha256=h.sha(raw), total=1)
        # Save the malformed event so the test exercises byte/metadata validation,
        # rather than failing only because an in-memory event differs from storage.
        stream, scope = d.stream_for('report')
        bad = h.record(conn, stream=stream, mode='manual_research', scope=scope,
                       run_id='malformed-'+mutation,
                       payload={'status':'incomplete','checks':[],'findings':[],'drafts':[],
                                'opinion_discovery':event}, artifacts={})
        with pytest.raises(ValueError):
            page_binding(conn, event, bad['capture_id'], contract)


@pytest.mark.parametrize('mutation', ['total_drift', 'repeated_identity'])
def test_channel_rejects_individually_valid_but_inconsistent_pages(tmp_path, mutation):
    with h.database(tmp_path/'db') as conn:
        contract, captures = saved(conn, [opinion(1), opinion(2)])
        court = d.COURTS[1];channel = court['id']+':listing'
        pages = [(cap, e) for cap, e in captures if e.get('kind') == 'page' and e['channel'] == channel]
        _, event = pages[1];event = copy.deepcopy(event)
        raw = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (event['sha256'],)).fetchone()[0]
        body = json.loads(raw)
        if mutation == 'total_drift':
            body['totalCount'] = 3
        else:
            body['searchResults'] = [opinion(1)]
        raw = json.dumps(body).encode()
        total, entries = d.parse_page(raw, court, contract['bounds'], 1)
        event.update(sha256=h.sha(raw), total=total, returned=len(entries),
                     page_ids=[e['id'] for e in entries], entries=d.bind_status(entries,event['source'],raw))
        stream, scope = d.stream_for('report')
        stored = h.record(conn, stream=stream, mode='manual_research', scope=scope, run_id='inconsistent',
                          payload={'status':'incomplete','checks':[],'findings':[],'drafts':[],
                                   'opinion_discovery':event}, artifacts={h.sha(raw):raw})
        pair = (stored['capture_id'], event)
        page_binding(conn, event, pair[0], contract)  # Individually valid.
        with pytest.raises(ValueError, match='total drift|Duplicate discovery identities'):
            validate_channel(conn, [pages[0],pair], contract, channel)
