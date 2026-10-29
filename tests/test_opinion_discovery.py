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


def pdf_bytes(text='Commercial holding. Affirmed. Author Example.'):
    import io
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
    writer = PdfWriter(); page = writer.add_blank_page(width=612, height=792)
    font = DictionaryObject({NameObject('/Type'):NameObject('/Font'),
                             NameObject('/Subtype'):NameObject('/Type1'),
                             NameObject('/BaseFont'):NameObject('/Helvetica')})
    page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'):
        DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
    stream = DecodedStreamObject()
    stream.set_data(('BT /F1 12 Tf 72 720 Td ('+text+') Tj ET').encode())
    page[NameObject('/Contents')] = writer._add_object(stream)
    out = io.BytesIO(); writer.write(out); return out.getvalue()


class Server:
    def __init__(self, entries):
        self.entries = entries
        self.calls = []
        self.pdf = pdf_bytes()
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
    server.pdf = pdf_bytes('Corrected commercial holding. Reversed.')
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


@pytest.mark.parametrize('covered_end', ['2026-10-22', '2026-10-25'])
def test_default_window_uses_covered_period_not_later_publication_and_ignores_partial_runs(env, covered_end):
    c, r, _ = env
    result = h.record(c, stream='weekly', mode='manual_research', scope=g.target(c, 'weekly'),
                      run_id='finalized-report-fixture', payload=dict(status='ready_for_review',
                      contract={'window_start':'2026-10-16','window_end':covered_end},
                      findings=[], checks=[], drafts=[]), artifacts={h.sha(b'report-fixture'):b'report-fixture'})
    c.execute('UPDATE captures SET recorded_at=? WHERE seq=?', ('2026-10-29T13:30:00+00:00', result['seq']))
    c.execute('INSERT INTO finalized_reports(stream,capture_seq,report_sha256,finalized_at,review) VALUES(?,?,?,?,?)',
              ('weekly',result['seq'],h.sha(b'report-fixture'),'2026-10-29T13:40:00+00:00','Fixture'))
    c.commit()
    if covered_end == '2026-10-25':
        with pytest.raises(ValueError, match='No new reporting interval'):
            d.window(c, 'weekly', end='2026-10-25')
        return
    before = d.window(c, 'weekly', end='2026-10-25')
    assert before['start'] == '2026-10-23' and before['discovery_start'] == '2026-09-23'
    assert before['finalized_baseline_capture'] == result['capture_id']
    h.record(c, stream='weekly', mode='manual_research', scope=g.target(c, 'weekly'), run_id='partial-later',
             payload=dict(status='incomplete',contract={},findings=[],checks=[],drafts=[]),artifacts={})
    assert d.window(c, 'weekly', end='2026-10-25') == before
    assert d.window(c, 'weekly', start='2026-10-20', end='2026-10-25')['start'] == '2026-10-20'


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


def test_standard_update_status_evidence_has_actual_transport_binding(env):
    from flwu.evidence_binding import AcquisitionIndex
    c, r, _ = env
    result = run(env, Server([opinion()]))
    item = result['opinion_reviews']['tasks'][0]['opinion']
    ref = dict(item['status_source'], quote='Company v. Business', locator='official metadata case_style')
    assert ref['http_status'] == 200 and ref['success'] is True
    AcquisitionIndex(c, r['stream']).validate(ref)
    ref['http_status'] = 201
    with pytest.raises(ValueError, match='does not match'):
        AcquisitionIndex(c, r['stream']).validate(ref)


def test_extensionless_opinion_login_response_is_preserved_but_failed(env):
    entry = opinion()
    entry['content']['fields']['opinion']['uri'] = '/content/download/1/123?version=5'
    server = Server([entry]); server.pdf = b'<html><input type="password">Login</html>'
    result = run(env, server)
    task = result['opinion_reviews']['tasks'][0]
    assert not result['acquisition_complete']
    assert 'opinion_download_unavailable' in task['reasons']
    observation = task['source_observation']
    assert not observation['success'] and observation['http_status'] == 200
    assert observation['url'].endswith('/123?version=5')
    assert g.blob(env[0], observation['sha256']) == server.pdf
    rec = task['review_template'] | {'reviewer':'Reviewer', 'summary':'Unavailable login response'}
    with pytest.raises(ValueError, match='download unavailable'):
        d.accept_review(env[0], env[1], rec)


@pytest.mark.parametrize('body', [b'%PDF-malformed', pdf_bytes('')])
def test_malformed_or_unextracted_pdf_cannot_complete_review(env, body):
    server = Server([opinion()]); server.pdf = body
    result = run(env, server)
    task = result['opinion_reviews']['tasks'][0]
    assert not result['acquisition_complete']
    assert task['document_error']
    for relevance in ('relevant', 'not_relevant', 'uncertain'):
        rec = task['review_template'] | {'reviewer':'Reviewer','summary':'No finding',
                                         'relevance':relevance}
        with pytest.raises(ValueError, match='Opinion'):
            d.accept_review(env[0], env[1], rec)
    assert not result['opinion_reviews']['reused_reviews']


def test_legacy_login_review_is_not_reused_or_accepted(env, monkeypatch):
    c, registry, tmp = env
    result = run(env, Server([opinion()]))
    item = result['opinion_reviews']['tasks'][0]['opinion']
    url = item['pdf_url']
    legacy = dict(registry, sources=[{'id':g.source_id(url), 'url':url}])
    # Reproduce old saved acquisition behavior: HTTP200 HTML accepted as transport success.
    g.run(c, legacy, 'legacy-login', fetch=lambda u: ({'url':u,'retrieved_at':h.now(),
        'success':True,'http_status':200,'content_type':'text/html'},b'<html>Home Login Username Password</html>'))
    with monkeypatch.context() as m:
        m.setattr(d, 'document_error', lambda *args: None)
        task = d.review_queue(c, registry)['tasks'][0];o=task['source_observation']
        rec = task['review_template'] | {'reviewer':'Legacy reviewer', 'relevance':'relevant',
            'summary':'Citation opinion', 'holding':'Citation', 'disposition':'Affirmed',
            'citations':[{'sha256':o['sha256'],'text_sha256':o['text_sha256'],
                          'quote':'Home Login Username Password','locator':'saved login'}]}
        old = d.accept_review(c, registry, rec)
    queue = d.review_queue(c, registry)
    assert not queue['reused_reviews']
    assert 'opinion_download_unavailable' in queue['tasks'][0]['reasons']
    assert c.execute('SELECT 1 FROM captures WHERE capture_id=?',(old['capture_id'],)).fetchone()
    changed = dict(rec, summary='Another unsupported summary')
    with pytest.raises(ValueError, match='not a PDF'):
        d.accept_review(c, registry, changed)

    with pytest.raises(ValueError, match='cannot be replayed'):
        d.accept_review(c, registry, rec)


def test_review_protocol_correction_preserves_old_evidence_and_replays(env):
    from flwu import publication_acceptance as pa
    c, registry, tmp = env
    result = run(env, Server([opinion()]))
    accept(env, result)
    before = c.execute('SELECT capture_id,payload FROM captures WHERE stream=? ORDER BY seq DESC',
                       (registry['stream'],)).fetchone()
    corrected_registry = dict(registry, review_protocol='practical-civil-correction-v2')
    task = d.review_queue(c, corrected_registry)['tasks'][0]
    original = task['source_observation']
    assert task['reasons'] == ['unfinished_or_protocol_changed_review']
    rec = task['review_template'] | {'reviewer':'Correcting reviewer', 'relevance':'relevant',
        'summary':'Corrected source-based summary.', 'holding':'Commercial holding.',
        'disposition':'Affirmed.', 'authors':['Example'], 'citations':[
            {'quote':'Commercial holding.', 'locator':'page 1', 'sha256':original['sha256'],
             'text_sha256':original['text_sha256']}]}
    saved = d.accept_review(c, corrected_registry, rec)
    row = c.execute('SELECT * FROM captures WHERE capture_id=?',(saved['capture_id'],)).fetchone()
    payload = json.loads(row['payload'])
    citation = payload['findings'][0]['citations'][0]
    assert citation['url'] == original['url']
    assert citation['retrieved_at'] == original['retrieved_at']
    assert citation['http_status'] == original['http_status']
    assert citation['sha256'] == original['sha256']
    assert c.execute('SELECT payload FROM captures WHERE capture_id=?',(before['capture_id'],)).fetchone()[0] == before['payload']
    assert pa.requirements(c,row)['opinion:'+rec['id']]['summary'] == rec['summary']
    replay = d.accept_review(c, corrected_registry, rec)
    assert replay['replayed'] and replay['capture_id'] == saved['capture_id']
    assert d.review_queue(c, corrected_registry)['reused_reviews'] == [rec['id']]


def test_resume_pins_registry_despite_later_opinion_url_revision(env):
    c, r, tmp = env
    server = Server([opinion(1)])
    run(env, server)
    original = json.loads((tmp/'one'/'expanded-registry.json').read_text())
    item = copy.deepcopy(next(iter(d.known(c, r['stream']).values())))
    item['pdf_url'] += '?version=2'
    d.save(c, r['stream'], 'later-review', 'revision',
           {'entries': [item], 'complete': True})
    server.calls.clear()
    resumed = run(env, server)
    assert not server.calls
    assert len(resumed['opinion_reviews']['tasks']) == 1
    assert 'opinion_download_unavailable' in resumed['opinion_reviews']['tasks'][0]['reasons']
    assert not any('/content/download/' in task['url'] for task in resumed['source_reviews']['tasks'])
    assert json.loads((tmp/'one'/'expanded-registry.json').read_text()) == original
    assert next(iter(d.known(c, r['stream']).values()))['pdf_url'].endswith('?version=2')


def test_legacy_registry_recovery_requires_exact_acquisition_hash(env):
    c, r, _ = env
    original = copy.deepcopy(r)
    url = 'https://court.gov/old.pdf'
    original['sources'].append({'id': g.source_id(url), 'url': url})
    g.run(c, original, 'legacy', fetch=Server([]))
    changed = copy.deepcopy(original)
    changed['sources'][-1] = {'id': g.source_id(url+'?version=2'), 'url': url+'?version=2'}
    recovered = update.pinned_registry(c, r, 'legacy', changed)
    assert recovered == original
    checkpoint = next(e for e in d.events(c, r['stream']) if e['checkpoint'] == 'update-registry')
    assert checkpoint['registry_sha256'] == h.sha(original)


def test_incomplete_legacy_registry_cannot_be_guessed(env):
    c, r, _ = env
    original = copy.deepcopy(r)
    url = 'https://court.gov/not-yet-fetched'
    original['sources'].append({'id': g.source_id(url), 'url': url})
    server = Server([])
    def interrupted(url):
        if url.endswith('not-yet-fetched'):
            raise RuntimeError('interrupted')
        return server(url)
    with pytest.raises(RuntimeError):
        g.run(c, original, 'partial-legacy', fetch=interrupted)
    with pytest.raises(ValueError, match='Cannot recover original'):
        update.pinned_registry(c, r, 'partial-legacy', r)
    assert not any(e['checkpoint'] == 'update-registry' for e in d.events(c, r['stream']))
