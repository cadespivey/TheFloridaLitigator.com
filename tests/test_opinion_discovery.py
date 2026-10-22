"""Official-response-shaped replay; no live calls and no production report checks."""
import copy
import json
from urllib.parse import parse_qs, urlparse

import pytest
from flwu import history as h, opinion_discovery as d, source_gate as g, update
from flwu.cli import main


def opinion(n=1, day='2026-10-20', note='Affirmed', court=None):
    court = court or d.COURTS[1]
    return {'type': 'opinion', 'content': {'id': n, 'typeIdentifier': 'opinion',
        'url': court['listing_page'].replace('/Opinions', '/opinion/'+str(n)),
        'fields': {'case_number': '2026-'+str(n), 'case_style': 'Company v. Business',
                   'disposition': 'Affirmed', 'note': note, 'remote_id': 'official-'+str(n),
                   'disposition_date': {'date': {'date': day+' 00:00:00.000000', 'timezone': '+00:00'}, 'stringFormat': 'l d F Y'},
                   'type': {'selection': [0]},
                   'opinion': {'uri': '/content/download/'+str(n)+'/opinion/file.pdf'}}}}


class Server:
    def __init__(self, entries):
        self.entries = entries
        self.calls = []
        self.pdf = b'Commercial holding. Affirmed. Author Example.'
        self.block = set()
        self.interrupt_offset = None
        self.clamp = 1
        self.duplicate = False

    def __call__(self, url):
        self.calls.append(url)
        meta = {'url': url, 'resolved_url': url, 'retrieved_at': h.now(), 'success': True,
                'http_status': 200, 'content_type': 'text/plain'}
        q = parse_qs(urlparse(url).query)
        if '_search/opinions/' in url:
            site = q['siteaccess'][0]; offset = int(q['offset'][0]); inactive = q.get('nonactive_only') == ['1']
            if site in self.block:
                return dict(meta, success=False, http_status=403), b'Forbidden'
            if self.interrupt_offset == offset and site == '1dca' and not inactive:
                self.interrupt_offset = None
                raise RuntimeError('interrupted')
            entries = self.entries if site == '1dca' and not inactive else []
            entries = [x for x in entries if q['startdate'][0] <= x['content']['fields']['disposition_date']['date']['date'][:10] < q['enddate'][0]]
            page = entries[offset:offset+self.clamp]
            if self.duplicate and offset and page:
                page = entries[:1]
            body = {'searchParams': {'siteaccess': site, 'scopes': q['scopes[]'], 'offset': offset,
                                    'startDate': q['startdate'][0], 'endDate': q['enddate'][0], 'nonActiveOnly': inactive,
                                    'types': ['Written', 'PCA', 'Citation']},
                    'totalCount': len(entries), 'searchResults': page}
            return dict(meta, content_type='application/json'), json.dumps(body).encode()
        if '/opinion/' in url and '/content/download/' not in url:
            n = int(url.rsplit('/', 1)[1]); item = next(x for x in self.entries if x['content']['id'] == n);f = item['content']['fields']
            page = {'_contentInfo': {'id': n}, 'caseNumber': f['case_number'], 'caseStyle': f['case_style'],
                    'disposition': f['disposition'], 'dispositionDate': {'format': f['disposition_date']['date']['date'][:10]},
                    'note': f['note'], 'remoteId': f['remote_id'], 'opinion': f['opinion']}
            return dict(meta, content_type='text/html'), ('<script id="__NEXT_DATA__">'+json.dumps({'props': {'pageProps': {'pageData': page}}})+'</script>').encode()
        if '/content/download/' in url:
            return meta, self.pdf
        return meta, b'Court release notices.'


@pytest.fixture
def env(tmp_path):
    with h.database(tmp_path/'history.sqlite') as c:
        h.record(c, stream='weekly', mode='manual_research', scope={'profile': 'test'}, run_id='initial',
                 payload={'status': 'incomplete', 'contract': {}, 'checks': [], 'findings': [], 'drafts': []}, artifacts={})
        r = {'schema_version': 1, 'stream': 'weekly', 'review_protocol': g.PROTOCOL,
             'sources': [{'id': g.source_id('https://court.gov/profile'), 'url': 'https://court.gov/profile'}]}
        yield c, r, tmp_path


def run(env, server, run_id='one'):
    c, r, tmp = env
    return update.run(c, r, run_id, tmp/run_id, start='2026-10-15', end='2026-10-22', fetch=server)


def accept(env, result):
    c, r, tmp = env
    expanded = g.load_registry(tmp/result['run_id']/'expanded-registry.json')
    for task in result['opinion_reviews']['tasks']:
        rec = copy.deepcopy(task['review_template']); o = task['source_observation']
        rec.update(reviewer='Fixture reviewer', relevance='relevant', summary='Commercial opinion.',
                   holding='Commercial holding.', disposition='Affirmed.', authors=['Example'],
                   citations=[{'quote': 'Commercial holding.', 'locator': 'page 1', 'sha256': o['sha256'], 'text_sha256': o['text_sha256']}])
        d.accept_review(c, expanded, rec)


def test_standard_entry_fetches_all_seven_both_feeds_paginates_and_downloads(env):
    server = Server([opinion(1), opinion(2, '2026-10-19'), opinion(3, '2026-09-20')])
    result = run(env, server)
    assert result['acquisition_complete']
    assert len(result['discovery']['courts']) == 14
    assert len(result['opinion_reviews']['tasks']) == 3  # overlap catches older entry
    feeds = [parse_qs(urlparse(u).query) for u in server.calls if '_search/opinions/' in u]
    assert {q['siteaccess'][0] for q in feeds} == {c['siteaccess'] for c in d.COURTS}
    assert [q['offset'][0] for q in feeds if q['siteaccess'] == ['1dca'] and 'nonactive_only' not in q] == ['0', '1', '2']
    assert sum('/content/download/' in u for u in server.calls) == 3
    assert env[0].execute('SELECT count(*) FROM finalized_reports').fetchone()[0] == 0


def test_unchanged_reviews_reused_late_posting_and_revised_pdf_queued(env):
    server = Server([opinion(1)])
    first = run(env, server); accept(env, first)
    second = run(env, server, 'two')
    assert not second['opinion_reviews']['tasks']
    server.entries.append(opinion(2, '2026-09-30'))
    third = run(env, server, 'three')
    assert len(third['opinion_reviews']['tasks']) == 1
    assert third['opinion_reviews']['tasks'][0]['opinion']['content_id'] == 2
    accept(env, third)
    server.pdf = b'Corrected commercial holding. Reversed.'
    fourth = run(env, server, 'four')
    assert len(fourth['opinion_reviews']['tasks']) == 2
    assert all('new_or_changed_pdf' in t['reasons'] for t in fourth['opinion_reviews']['tasks'])


def test_withdrawal_note_creates_task_even_when_pdf_unchanged(env):
    server = Server([opinion(1)])
    first = run(env, server); accept(env, first)
    server.entries[0]['content']['fields']['note'] = 'Opinion withdrawn; substituted opinion to follow.'
    result = run(env, server, 'two')
    task = result['opinion_reviews']['tasks'][0]
    assert 'official_status_metadata_changed' in task['reasons']
    assert 'new_or_changed_pdf' not in task['reasons']
    assert task['source_observation']['change'] == 'unchanged'
    assert g.blob(env[0], task['opinion']['status_source']['text_sha256']).decode().find('withdrawn') >= 0


def test_blocked_court_does_not_stop_others_or_report_no_new_opinions(env):
    server = Server([opinion(1)]); server.block = {'1dca'}
    result = run(env, server)
    assert not result['acquisition_complete']
    assert len(result['discovery']['courts']) == 14
    assert sum(not c['complete'] for c in result['discovery']['courts']) == 2
    assert not result['opinion_reviews']['tasks']  # must not be interpreted as no opinions
    assert all(c['error'] for c in result['discovery']['courts'] if not c['complete'])


def test_duplicates_deduplicated_but_pagination_coverage_not_assumed(env):
    server = Server([opinion(1), opinion(2)]); server.duplicate = True
    result = run(env, server)
    assert not result['acquisition_complete']
    assert len(result['opinion_reviews']['tasks']) == 1
    assert any('Duplicate' in (c['error'] or '') for c in result['discovery']['courts'])


def test_interrupted_page_resumes_and_does_not_refetch_saved_pages(env):
    server = Server([opinion(1), opinion(2)]); server.interrupt_offset = 1
    with pytest.raises(RuntimeError):
        run(env, server)
    server.calls.clear()
    result = run(env, server)
    assert result['acquisition_complete'] and len(result['opinion_reviews']['tasks']) == 2
    assert not any('siteaccess=1dca' in u and 'offset=0' in u and 'nonactive_only' not in u for u in server.calls)
    server.calls.clear()
    resumed = run(env, server)
    assert not server.calls and len(resumed['opinion_reviews']['tasks']) == 2


def test_default_window_requires_finalized_report_and_partial_never_advances(env, tmp_path):
    c, r, _ = env
    with pytest.raises(ValueError, match='No finalized report'):
        d.window(c, 'weekly', end='2026-10-22')
    # Synthetic finalized marker only; no production report inspected.
    c.execute('INSERT INTO artifacts VALUES(?,?)', (h.sha(b'fixture'), b'fixture'))
    seq = c.execute('SELECT min(seq) FROM captures WHERE stream=?', ('weekly',)).fetchone()[0]
    c.execute('UPDATE captures SET recorded_at=? WHERE seq=?', ('2026-10-10T12:00:00+00:00', seq))
    c.execute('INSERT INTO finalized_reports(stream,capture_seq,report_sha256,finalized_at,review) VALUES(?,?,?,?,?)', ('weekly', seq, h.sha(b'fixture'), '2026-10-10T13:00:00+00:00', 'Fixture'))
    c.commit()
    before = d.window(c, 'weekly', end='2026-10-22')
    run(env, Server([opinion()]))
    assert d.window(c, 'weekly', end='2026-10-22') == before
    assert before['start'] == '2026-10-10' and before['discovery_start'] == '2026-09-10'


def test_listing_scope_and_date_mismatch_rejected():
    court = d.COURTS[1]; bounds = {'discovery_start': '2026-09-15', 'end': '2026-10-22', 'api_end_exclusive': '2026-10-23'}
    server = Server([opinion()]); meta, raw = server(d.query_url(court, bounds, 0, 50))
    body = json.loads(raw);body['searchParams']['scopes'] = ['supreme_court']
    with pytest.raises(ValueError, match='filters'):
        d.parse_page(json.dumps(body), court, bounds, 0)


def test_standard_cli_is_wired_to_discovery(env, monkeypatch):
    c, r, tmp = env
    path = tmp/'registry.json'; path.write_text(json.dumps(r))
    server = Server([opinion()])
    original = update.run
    monkeypatch.setattr(update, 'run', lambda *a, **kw: original(*a, **kw, fetch=server))
    assert main(['update', '--database', str(tmp/'history.sqlite'), '--registry', str(path), '--run-id', 'cli', '--output', str(tmp/'cli'), '--start', '2026-10-15', '--end', '2026-10-22']) == 0
    result = json.loads((tmp/'cli/update-queue.json').read_text())
    assert result['all_seven_courts_wired'] == [c['id'] for c in d.COURTS]
    assert len(result['discovery']['courts']) == 14


def test_consolidated_case_filename_spaces_are_url_encoded():
    court = d.COURTS[0]; item = opinion(10, court=court)
    item['content']['fields']['opinion']['uri'] = '/content/download/10/opinion/Opinion_SC2024-0251 & SC2024-1181.pdf'
    result = d.normalized(court, 10, item['content']['fields'], item['content']['url'])
    assert ' ' not in result['pdf_url'] and '%20' in result['pdf_url']


def test_status_detail_failure_keeps_completed_opinion_pending(env):
    server = Server([opinion(1)])
    first = run(env, server); accept(env, first)
    base = server
    def blocked_detail(url):
        if '/opinion/' in url and '/content/download/' not in url:
            return {'url': url, 'resolved_url': url, 'retrieved_at': h.now(), 'success': False,
                    'http_status': 403, 'content_type': 'text/plain'}, b'Forbidden'
        return base(url)
    result = run(env, blocked_detail, 'two')
    assert not result['acquisition_complete']
    assert 'official_status_source_unavailable' in result['opinion_reviews']['tasks'][0]['reasons']
    assert not result['opinion_reviews']['reused_reviews']


def test_tracked_legacy_opinion_outside_window_is_reconciled_by_exact_content_id(env):
    c, r, tmp = env
    legacy = opinion(31, '2026-01-01'); legacy['content']['fields']['opinion']['uri'] = '/content/download/31/opinion/Opinion_2026-31.pdf'
    url = 'https://flcourts-media.flcourts.gov'+legacy['content']['fields']['opinion']['uri']
    r['sources'].append({'id': g.source_id(url), 'url': url})
    regular = Server([legacy])
    def fetch(url):
        q = parse_qs(urlparse(url).query)
        if '_search/opinions/' in url and 'startdate' not in q:
            entries = [legacy] if q['siteaccess'] == ['1dca'] else []
            body = {'searchParams': {'query': '2026-31', 'scopes': q['scopes[]'], 'offset': int(q['offset'][0])},
                    'totalCount': len(entries), 'searchResults': entries}
            return {'url': url, 'resolved_url': url, 'retrieved_at': h.now(), 'success': True,
                    'http_status': 200, 'content_type': 'application/json'}, json.dumps(body).encode()
        return regular(url)
    result = run(env, fetch)
    assert result['acquisition_complete']
    assert len(result['opinion_reviews']['tasks']) == 1
    assert result['opinion_reviews']['tasks'][0]['opinion']['content_id'] == 31
    assert result['opinion_reviews']['tasks'][0]['opinion']['published_date'] == '2026-01-01'
