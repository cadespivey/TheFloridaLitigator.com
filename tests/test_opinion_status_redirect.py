"""PDF redirects require independent, exact-identity official status evidence."""
import json
from urllib.parse import parse_qs, urlparse

import pytest
from flwu import opinion_discovery as d, history as h
from tests.test_opinion_discovery import Server, opinion, env, run, accept


class RedirectServer(Server):
    def __init__(self, entries):
        super().__init__(entries)
        self.inactive = set()
        self.bad = None
        self.api_calls = 0
        self.interrupt_api_offset = None
        self.detail_blocked = False

    def __call__(self, url):
        q = parse_qs(urlparse(url).query)
        if '_search/opinions/' not in url:
            if '/opinion/' in url and '/content/download/' not in url:
                self.calls.append(url)
                if self.detail_blocked:
                    return {'url': url, 'retrieved_at': h.now(), 'success': False,
                            'http_status': 403}, b'Forbidden'
                return {'url': url, 'resolved_url': 'https://flcourts-media.flcourts.gov/file.pdf',
                        'retrieved_at': h.now(), 'success': True, 'http_status': 200,
                        'content_type': 'application/pdf'}, self.pdf
            return super().__call__(url)
        self.calls.append(url)
        court = next(c for c in d.COURTS if c['siteaccess'] == q['siteaccess'][0])
        offset = int(q['offset'][0]); inactive = q.get('nonactive_only') == ['1']
        api = 'startdate' not in q
        if api:
            self.api_calls += 1
            if self.interrupt_api_offset == offset:
                self.interrupt_api_offset = None
                raise RuntimeError('interrupted API')
        meta = {'url': url, 'resolved_url': url, 'retrieved_at': h.now(),
                'success': True, 'http_status': 200, 'content_type': 'application/json'}
        if api and self.bad == 'blocked':
            return dict(meta, success=False, http_status=403), b'Forbidden'
        entries = [e for e in self.entries if urlparse(e['content']['url']).hostname == urlparse(court['listing_page']).hostname]
        if inactive:
            entries = [e for e in entries if e['content']['id'] in self.inactive]
        if api:
            entries = [e for e in entries if q['query'][0] in e['content']['fields']['case_number']]
            if self.bad == 'missing':
                entries = []
        else:
            entries = [e for e in entries if q['startdate'][0] <= e['content']['fields']['disposition_date']['date']['date'][:10] < q['enddate'][0]]
        page = entries[offset:offset+self.clamp]
        if api and self.bad == 'duplicate' and offset and page:
            page = entries[:1]
        params = {'query': q.get('query', [''])[0], 'siteaccess': court['siteaccess'],
                  'scopes': q['scopes[]'], 'offset': offset, 'startDate': q.get('startdate', [None])[0],
                  'endDate': q.get('enddate', [None])[0], 'nonActiveOnly': inactive,
                  'activeOnly': False, 'types': ['Written', 'PCA', 'Citation'],
                  'opinionsSearchFields': ['case_number']}
        if api and self.bad == 'wrong_filter':
            params['activeOnly'] = True
        if api and self.bad == 'wrong_court':
            params['siteaccess'] = 'other'
        return meta, json.dumps({'searchParams': params, 'totalCount': len(entries), 'searchResults': page}).encode()


def seed(env, entry):
    c, r, _ = env
    court = next(c for c in d.COURTS if urlparse(c['listing_page']).hostname == urlparse(entry['content']['url']).hostname)
    x = entry['content']; item = d.normalized(court, x['id'], x['fields'], x['url'])
    raw = json.dumps(entry).encode()
    meta = {'url': court['endpoint'], 'retrieved_at': h.now(), 'http_status': 200, 'success': True}
    d.save(c, r['stream'], 'tracked-seed', 'seed:'+item['id'],
           {'kind': 'seed', 'complete': True, 'entries': d.bind_status([item], meta, raw)}, raw)
    return item


@pytest.mark.parametrize('blocked', [False, True])
def test_all_seven_redirects_use_complete_listings_and_preserve_originals(env, blocked):
    server = RedirectServer([opinion(n+100, court=c) for n, c in enumerate(d.COURTS)])
    server.detail_blocked = blocked
    result = run(env, server)
    assert result['acquisition_complete']
    assert len(result['opinion_reviews']['tasks']) == 7 and server.api_calls == 0
    events = d.events(env[0], 'weekly')
    legacy = [e for e in events if e.get('checkpoint', '').startswith('detail:')]
    recovered = [e for e in events if e.get('checkpoint', '').startswith('detail-v2:')]
    assert len(legacy) == len(recovered) == 7
    assert all(not e['complete'] and e['sha256'] for e in legacy)
    assert all(e['complete'] and e['route'] == 'completed_current_listing_channels' for e in recovered)
    accept(env, result)
    server.calls.clear()
    second = run(env, server, 'two')
    assert not second['opinion_reviews']['tasks']
    assert len(second['opinion_reviews']['reused_reviews']) == 7
    assert len({parse_qs(urlparse(u).query)['siteaccess'][0] for u in server.calls if '_search/opinions/' in u}) == 7


def test_redirect_status_only_change_and_revised_pdf_are_separate(env):
    server = RedirectServer([opinion(1)])
    first = run(env, server); accept(env, first)
    server.inactive.add(1)
    server.entries[0]['content']['fields']['note'] = 'Withdrawn; substituted opinion to follow.'
    second = run(env, server, 'two'); task = second['opinion_reviews']['tasks'][0]
    assert second['acquisition_complete']
    assert 'official_status_metadata_changed' in task['reasons']
    assert 'new_or_changed_pdf' not in task['reasons']
    assert task['opinion']['metadata']['listed_in_inactive_feed'] is True
    accept(env, second)
    from tests.test_opinion_discovery import pdf_bytes
    server.pdf = pdf_bytes('Corrected commercial holding. Reversed.')
    third = run(env, server, 'three')
    assert 'new_or_changed_pdf' in third['opinion_reviews']['tasks'][0]['reasons']


@pytest.mark.parametrize('blocked', [False, True])
def test_outside_window_api_paginates_and_matches_id_not_case_number(env, blocked):
    a, b = opinion(1, '2026-01-01'), opinion(2, '2026-01-02')
    b['content']['fields']['case_number'] = a['content']['fields']['case_number']
    seed(env, b)
    server = RedirectServer([a, b]); server.inactive.add(2)
    server.detail_blocked = blocked
    result = run(env, server)
    assert result['acquisition_complete'] and server.api_calls == 3
    task = result['opinion_reviews']['tasks'][0]
    assert task['opinion']['content_id'] == 2
    assert task['opinion']['metadata']['listed_in_inactive_feed'] is True
    assert len(result['opinion_reviews']['tasks']) == 1  # incidental lookup records aren't new discovery


@pytest.mark.parametrize('bad', ['blocked', 'missing', 'duplicate', 'wrong_filter', 'wrong_court'])
def test_unverified_api_never_becomes_no_change(env, bad):
    a, b = opinion(1, '2026-01-01'), opinion(2, '2026-01-02')
    b['content']['fields']['case_number'] = a['content']['fields']['case_number']
    seed(env, b); server = RedirectServer([a, b]); server.bad = bad
    result = run(env, server)
    assert not result['acquisition_complete']
    assert result['discovery']['detail_failures']
    assert 'official_status_source_unavailable' in result['opinion_reviews']['tasks'][0]['reasons']
    assert not result['opinion_reviews']['reused_reviews']


def test_interrupted_recovery_reuses_pages_and_preserves_failed_detail(env):
    a, b = opinion(1, '2026-01-01'), opinion(2, '2026-01-02')
    b['content']['fields']['case_number'] = a['content']['fields']['case_number']
    seed(env, b); server = RedirectServer([a, b]); server.interrupt_api_offset = 1
    with pytest.raises(RuntimeError, match='interrupted API'):
        run(env, server)
    before = [e for e in d.events(env[0], 'weekly') if e['checkpoint'].startswith('detail:')]
    server.calls.clear(); result = run(env, server)
    assert result['acquisition_complete']
    assert not any('/opinion/' in u and '/content/download/' not in u for u in server.calls)
    assert not any('_search/opinions/' in u and 'startdate=' in u for u in server.calls)
    assert not any('_search/opinions/' in u and 'offset=0' in u and 'nonactive_only' not in u for u in server.calls)
    after = [e for e in d.events(env[0], 'weekly') if e['checkpoint'].startswith('detail:')]
    assert before == after and len(after) == 1
    server.calls.clear(); replay = run(env, server)
    assert replay['acquisition_complete'] and not server.calls


def test_failed_html_event_from_old_adapter_is_recovered_without_refetch(env, monkeypatch):
    server = RedirectServer([opinion(1)])
    original = d._pdf_status
    def stop(*args, **kwargs):
        raise RuntimeError('before new recovery')
    monkeypatch.setattr(d, '_pdf_status', stop)
    with pytest.raises(RuntimeError):
        run(env, server)
    monkeypatch.setattr(d, '_pdf_status', original); server.calls.clear()
    result = run(env, server)
    assert result['acquisition_complete']
    assert not any('_search/opinions/' in u or '/opinion/1' in u for u in server.calls)
