"""Gate acceptance tests use disposable SQLite databases and HTTP fixtures only."""
import copy
import json
from pathlib import Path

import httpx
import pytest

from flwu import history as h, source_gate as g
from flwu.cli import main


@pytest.fixture
def env(tmp_path):
    db = tmp_path/'history.sqlite'
    with h.database(db) as c:
        h.record(c, stream='research', mode='manual_research', scope={'profile': 'test'}, run_id='initial',
                 payload={'status': 'incomplete', 'contract': {}, 'findings': [], 'drafts': [], 'checks': []}, artifacts={})
        registry = {'schema_version': 1, 'stream': 'research', 'review_protocol': g.PROTOCOL,
                    'sources': [{'id': g.source_id(u), 'url': u} for u in
                                ['https://court.gov/judge', 'https://court.gov/procedure.pdf']]}
        yield c, registry, tmp_path


def fetcher(bodies, *, failures=()):
    calls = []
    def fetch(url):
        calls.append(url)
        return {'url': url, 'resolved_url': url, 'retrieved_at': h.now(), 'success': url not in failures,
                'http_status': 403 if url in failures else 200, 'content_type': 'text/plain'}, bodies[url]
    return fetch, calls


def acquire(env, run_id, *, page=b'Profile', pdf=b'Procedure', failures=()):
    c, registry, _ = env
    urls = [s['url'] for s in registry['sources']]
    fetch, calls = fetcher(dict(zip(urls, (page, pdf))), failures=failures)
    return g.run(c, registry, run_id, fetch=fetch), calls


def receipt(task, registry, c):
    o = task['observation']
    return {'source_id': o['source_id'], 'observation_capture_id': o['capture_id'], 'sha256': o['sha256'],
            'review_protocol': registry['review_protocol'], 'reviewer': 'Test reviewer',
            'summary': 'Bounded operating requirements reviewed.', 'review_scope': 'Entire fixture',
            'outcome': 'baseline_reviewed', 'findings': [],
            'support': {'reason': 'Reviewed the operating requirements in this source.',
                        'current': [{'sha256': o['sha256'], 'text_sha256': o.get('text_sha256'),
                                     'quote': g.blob(c, o['text_sha256']).decode() if o.get('text_sha256') else '',
                                     'locator': 'Fixture paragraph 1'}], 'previous': []}}


def test_unchanged_parent_still_fetches_changed_document_and_reuses_review(env):
    c, r, tmp = env
    first, _ = acquire(env, 'one')
    for task in first['tasks']:
        g.accept(c, r, receipt(task, r, c))
    second, calls = acquire(env, 'two', pdf=b'Changed procedure')
    assert calls == [s['url'] for s in r['sources']]
    assert len(second['reused_reviews']) == 1
    assert len(second['tasks']) == 1 and second['tasks'][0]['reason'] == 'changed'
    written = g.write_queue(c, r, tmp/'queue')
    task = written['tasks'][0]
    assert Path(task['previous_path']).read_bytes() == b'Procedure'
    assert Path(task['current_path']).read_bytes() == b'Changed procedure'
    assert '-Procedure' in Path(task['diff_path']).read_text()
    assert '+Changed procedure' in Path(task['diff_path']).read_text()
    assert c.execute('SELECT count(*) FROM finalized_reports').fetchone()[0] == 0


def test_identical_unreviewed_is_still_queued_and_resume_does_not_fetch(env):
    c, r, _ = env
    acquire(env, 'one')
    result, calls = acquire(env, 'one')
    assert not calls and len(result['tasks']) == 2
    result, calls = acquire(env, 'two')
    assert len(calls) == 2 and {t['reason'] for t in result['tasks']} == {'unreviewed'}
    assert not result['reused_reviews']
    changed_registry = copy.deepcopy(r); changed_registry['review_protocol'] = 'different'
    with pytest.raises(ValueError, match='different registry'):
        g.run(c, changed_registry, 'one', fetch=lambda u: pytest.fail('must not fetch'))


def test_failure_retains_last_success_and_blocks_review_reuse(env):
    c, r, _ = env
    first, _ = acquire(env, 'one')
    for task in first['tasks']:
        g.accept(c, r, receipt(task, r, c))
    failed, _ = acquire(env, 'two', page=b'Forbidden', failures=[r['sources'][0]['url']])
    task = failed['tasks'][0]
    assert task['reason'] == 'retrieval_failed'
    assert task['observation']['previous_sha256'] == h.sha(b'Profile')
    with pytest.raises(ValueError, match='latest successful'):
        g.accept(c, r, receipt(task, r, c))
    recovered, _ = acquire(env, 'three')
    assert not recovered['tasks'] and len(recovered['reused_reviews']) == 2
    assert g.blob(c, h.sha(b'Forbidden')) == b'Forbidden'


def test_stale_review_rejected_exact_replay_idempotent_and_protocol_change_requeues(env):
    c, r, _ = env
    first, _ = acquire(env, 'one')
    rec = receipt(first['tasks'][0], r, c)
    ack = g.accept(c, r, rec)
    count = c.execute('SELECT count(*) FROM captures').fetchone()[0]
    assert g.accept(c, r, rec)['capture_id'] == ack['capture_id']
    assert c.execute('SELECT count(*) FROM captures').fetchone()[0] == count
    stale = receipt(first['tasks'][1], r, c)
    acquire(env, 'two', pdf=b'Changed')
    with pytest.raises(ValueError, match='latest successful'):
        g.accept(c, r, stale)
    changed = copy.deepcopy(r); changed['review_protocol'] = 'revised-scope'
    assert len(g.queue(c, changed)['tasks']) == 2


def test_raw_hash_change_is_not_hidden_by_equal_extracted_text(env):
    c, r, _ = env
    r['sources'] = r['sources'][:1]
    url = r['sources'][0]['url']
    def get(body):
        return lambda u: ({'url': u, 'resolved_url': u, 'retrieved_at': h.now(), 'success': True,
                           'http_status': 200, 'content_type': 'text/html'}, body)
    one = g.run(c, r, 'one', fetch=get(b'<p>Same</p><script>nonce=1</script>'))
    g.accept(c, r, receipt(one['tasks'][0], r, c))
    two = g.run(c, r, 'two', fetch=get(b'<p>Same</p><script>nonce=2</script>'))
    assert two['tasks'][0]['reason'] == 'changed'
    o = two['tasks'][0]['observation']
    assert o['text_sha256'] == o['previous_text_sha256']


def test_findings_require_exact_bound_citations_and_expected_version(env):
    c, r, _ = env
    first, _ = acquire(env, 'one')
    task = first['tasks'][0]; o = task['observation']; rec = receipt(task, r, c)
    cite = {k: o[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at')}
    cite.update(quote='Profile', locator='fixture paragraph')
    rec.update(outcome='updated_findings', findings=[{'key': 'judge', 'kind': 'judge',
        'facts': {'name': 'Fixture'}, 'expected_version': None, 'citations': [cite]}])
    bad = copy.deepcopy(rec); bad['findings'][0]['citations'][0]['quote'] = 'Invented'
    before = c.execute('SELECT count(*) FROM captures').fetchone()[0]
    with pytest.raises(ValueError, match='absent'):
        g.accept(c, r, bad)
    assert c.execute('SELECT count(*) FROM captures').fetchone()[0] == before
    ack = g.accept(c, r, rec)
    stored = c.execute('SELECT v.facts FROM finding_observations o JOIN finding_versions v USING(version_id) WHERE o.capture_seq=?', (ack['seq'],)).fetchone()
    assert json.loads(stored[0]) == {'name': 'Fixture'}
    assert g.accept(c, r, rec)['replayed']
    wrong = copy.deepcopy(rec); wrong['summary'] = 'A different review'
    with pytest.raises(ValueError, match='Finding changed'):
        g.accept(c, r, wrong)


def test_effective_date_trigger_survives_unchanged_bytes(env):
    c, r, _ = env
    first, _ = acquire(env, 'one')
    for task in first['tasks']:
        g.accept(c, r, receipt(task, r, c))
    h.record(c, stream='research', mode='manual_research', scope={'profile': 'test'}, run_id='dated',
             payload={'status': 'incomplete', 'contract': {}, 'checks': [], 'drafts': [],
                      'findings': [{'key': 'rule', 'kind': 'rule', 'facts': {'effective_date': '2026-10-22'},
                                    'citations': [{'url': 'https://court.gov/rule'}]}]}, artifacts={})
    result = g.queue(c, r, start='2026-10-01', end='2026-10-31')
    assert not result['tasks']
    assert result['effective_date_tasks'][0]['type'] == 'effective_date_reached'
    assert not result['baseline_known']


def test_http_failures_redirect_bounds_and_pdf_error_pages():
    responses = {
        '/redirect': (302, {'location': '/file.pdf'}, b''),
        '/file.pdf': (200, {'content-type': 'application/pdf'}, b'%PDF-fixture'),
        '/error.pdf': (200, {'content-type': 'text/html'}, b'<h1>Forbidden</h1>'),
        '/blocked': (403, {'content-type': 'text/html'}, b'Forbidden'),
        '/loop': (302, {'location': '/loop'}, b'')}
    calls = []
    def handle(req):
        calls.append(str(req.url))
        status, headers, body = responses[req.url.path]
        return httpx.Response(status, headers=headers, content=body)
    transport = httpx.MockTransport(handle)
    meta, raw = g.retrieve('https://court.gov/redirect', transport=transport)
    assert meta['success'] and raw == b'%PDF-fixture' and meta['resolved_url'].endswith('/file.pdf')
    for path in ('error.pdf', 'blocked', 'loop'):
        meta, raw = g.retrieve('https://court.gov/'+path, transport=transport)
        assert not meta['success']
    assert calls.count('https://court.gov/loop') == 6


def test_registry_and_cli_validation(env):
    c, r, tmp = env
    path = tmp/'registry.json'; path.write_text(json.dumps(r))
    assert g.load_registry(path) == r
    bad = copy.deepcopy(r); bad['sources'].append(bad['sources'][0]); path.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match='Duplicate'):
        g.load_registry(path)
    assert main(['source-gate', 'run']) == 1
    path.write_text(json.dumps(r))
    assert main(['source-gate', 'queue', '--database', str(tmp/'history.sqlite'), '--registry', str(path), '--output', str(tmp/'queue')]) == 0
    assert len(json.loads((tmp/'queue/queue.json').read_text())['tasks']) == 2


def test_interrupted_run_keeps_first_source_and_resumes_only_remaining(env):
    c, r, _ = env
    calls = []
    def interrupted(url):
        calls.append(url)
        if len(calls) == 2:
            raise RuntimeError('simulated interruption')
        return {'url': url, 'resolved_url': url, 'retrieved_at': h.now(), 'success': True,
                'http_status': 200, 'content_type': 'text/plain'}, b'Profile'
    with pytest.raises(RuntimeError):
        g.run(c, r, 'resume-me', fetch=interrupted)
    assert len(g.observations(c, 'research')) == 1
    result, calls = acquire(env, 'resume-me')
    assert calls == [r['sources'][1]['url']]
    assert len(result['tasks']) == 2


def test_existing_baseline_hash_used_without_inventing_completed_review(env):
    c, r, tmp = env
    raw = b'Profile'; digest = h.sha(raw)
    ci = {'url': r['sources'][0]['url'], 'sha256': digest, 'text_sha256': digest,
          'retrieved_at': '2026-10-01T12:00:00+00:00'}
    h.record(c, stream='research', mode='manual_research', scope={'profile': 'test'}, run_id='legacy',
             payload={'status': 'incomplete', 'contract': {}, 'checks': [], 'drafts': [],
                      'findings': [{'key': 'legacy-judge', 'kind': 'judge', 'facts': {'phone': '555-0100'},
                                    'citations': [ci]}]}, artifacts={digest: raw})
    result, _ = acquire(env, 'one')
    task = result['tasks'][0]
    assert task['reason'] == 'unreviewed'
    assert task['observation']['change'] == 'unchanged'
    assert task['observation']['previous_sha256'] == digest
    written = g.write_queue(c, r, tmp/'queue')
    prior = written['tasks'][0]['prior_findings'][0]
    assert prior['key'] == 'legacy-judge' and prior['facts']['phone'] == '555-0100'
    generated = g.inventory(c, 'research')
    assert generated['sources'] == [r['sources'][0]]


def test_failed_oversized_response_never_gets_success_hash(monkeypatch):
    monkeypatch.setattr(g, 'MAX_BYTES', 3)
    transport = httpx.MockTransport(lambda req: httpx.Response(200, content=b'too big'))
    meta, raw = g.retrieve('https://court.gov/page', transport=transport)
    assert not meta['success'] and raw is None


def test_removed_registry_source_is_visible(env):
    c, r, _ = env
    acquire(env, 'one')
    reduced = copy.deepcopy(r); reduced['sources'] = reduced['sources'][:1]
    assert g.queue(c, reduced)['unregistered_previous_sources'] == [r['sources'][1]['url']]


def test_citation_cannot_mix_unrelated_raw_and_text(env):
    c, r, _ = env
    first, _ = acquire(env, 'one')
    task = first['tasks'][0]; o = task['observation']; rec = receipt(task, r, c)
    cite = {k: o[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at')}
    cite.update(text_sha256=first['tasks'][1]['observation']['text_sha256'], quote='Procedure', locator='wrong source')
    rec.update(outcome='updated_findings', findings=[{'key': 'judge', 'kind': 'judge',
               'facts': {'name': 'Fixture'}, 'expected_version': None, 'citations': [cite]}])
    with pytest.raises(ValueError, match='acquired source/text pair'):
        g.accept(c, r, rec)


def test_visual_extraction_preserves_original_and_binds_citation(env):
    c, r, _ = env
    first, _ = acquire(env, 'one')
    o = first['tasks'][0]['observation']
    extraction = {'source_id': o['source_id'], 'observation_capture_id': o['capture_id'],
                  'sha256': o['sha256'], 'method': 'selected visual transcription',
                  'reviewer': 'Fixture reviewer', 'scope': 'page 1, office contact only'}
    ack = g.attach_text(c, r, extraction, 'Telephone 555-0100')
    assert g.attach_text(c, r, extraction, 'Telephone 555-0100')['capture_id'] == ack['capture_id']
    task = g.queue(c, r)['tasks'][0]
    assert task['observation']['sha256'] == o['sha256']
    assert task['observation']['extraction_receipt'] == extraction
    assert g.blob(c, task['observation']['text_sha256']) == b'Telephone 555-0100'
    assert g.blob(c, o['sha256']) == b'Profile'


def test_negative_review_requires_real_current_and_previous_support(env):
    c, r, _ = env
    acquire(env, 'before')
    result, _ = acquire(env, 'after', page=b'New hearing notice requirement')
    task = result['tasks'][0]
    rec = receipt(task, r, c)
    rec['outcome'] = 'no_relevant_change'
    with pytest.raises(ValueError, match='previous and current'):
        g.accept(c, r, rec)
    o = task['observation']
    rec['support']['previous'] = [{'sha256': o['previous_sha256'],
        'text_sha256': o['previous_text_sha256'], 'quote': 'Profile', 'locator': 'paragraph 1'}]
    rec['support']['current'][0]['quote'] = 'Invented unchanged text'
    with pytest.raises(ValueError, match='quote absent'):
        g.accept(c, r, rec)
    rec['support']['current'][0]['quote'] = 'New hearing notice requirement'
    rec['support']['reason'] = 'This fixture exercises evidence binding, not legal correctness.'
    g.accept(c, r, rec)


def test_legacy_unsubstantiated_review_is_not_reused(env):
    c, r, _ = env
    first, _ = acquire(env, 'first')
    task = first['tasks'][0]
    old = receipt(task, r, c)
    del old['support']
    old['receipt_sha256'] = h.sha(old)
    h.record(c, stream=r['stream'], mode='manual_research', scope={'profile': 'test'},
             run_id='legacy-review', payload={'status':'incomplete', 'contract':{},
             'checks':[], 'findings':[], 'drafts':[], 'source_gate_review':old}, artifacts={})
    result, _ = acquire(env, 'repeat')
    assert not result['reused_reviews']
    assert len(result['tasks']) == 2


def test_empty_extraction_cannot_be_dismissed_as_irrelevant(env):
    c, r, _ = env
    result, _ = acquire(env, 'empty', page=b'\xff')
    rec = receipt(result['tasks'][0], r, c)
    rec['outcome'] = 'no_relevant_change'
    with pytest.raises(ValueError, match='Unavailable extraction'):
        g.accept(c, r, rec)


def test_no_change_cannot_cite_only_unchanged_heading_or_one_of_two_changes(env):
    c, r, tmp = env
    acquire(env, 'before', page=b'Court procedures\nOld hearing instruction\nOld contact')
    result, _ = acquire(env, 'after', page=b'Court procedures\nNew hearing instruction\nNew contact')
    task = result['tasks'][0]; o = task['observation']
    rec = receipt(task, r, c)
    rec['outcome'] = 'no_relevant_change'
    rec['support']['previous'] = [{'sha256':o['previous_sha256'], 'text_sha256':o['previous_text_sha256'],
                                  'quote':'Court procedures', 'locator':'heading'}]
    rec['support']['current'][0]['quote'] = 'Court procedures'
    with pytest.raises(ValueError, match='every changed text line'):
        g.accept(c, r, rec)
    rec['support']['previous'][0]['quote'] = 'Old hearing instruction'
    rec['support']['current'][0]['quote'] = 'New hearing instruction'
    with pytest.raises(ValueError, match='every changed text line'):
        g.accept(c, r, rec)
    queue = g.write_queue(c, r, tmp/'review')
    changes = queue['tasks'][0]['changed_text_lines']
    assert changes == {'previous':['Old hearing instruction','Old contact'],
                       'current':['New hearing instruction','New contact']}
    rec['support']['previous'][0]['quote'] = '\n'.join(changes['previous'])
    rec['support']['current'][0]['quote'] = '\n'.join(changes['current'])
    g.accept(c, r, rec)


def test_changed_source_cannot_bypass_comparison_as_baseline(env):
    c, r, _ = env
    acquire(env, 'before')
    result, _ = acquire(env, 'after', page=b'New requirements')
    with pytest.raises(ValueError, match='not baseline_reviewed'):
        g.accept(c, r, receipt(result['tasks'][0], r, c))


def test_queue_indexes_latest_prior_findings_once_for_all_sources(env):
    c,r,tmp=env
    raw=b'Profile';digest=h.sha(raw)
    for n in (0,1):
        cite={'url':r['sources'][n]['url'],'sha256':digest,'text_sha256':digest,
              'retrieved_at':f'2026-10-0{n+1}T12:00:00+00:00'}
        h.record(c,stream='research',mode='manual_research',scope={'profile':'test'},run_id='version-'+str(n),
                 payload={'status':'incomplete','contract':{},'checks':[],'drafts':[],
                          'findings':[{'key':'same-judge','kind':'judge','facts':{'phone':str(n)},'citations':[cite,cite]}]},
                 artifacts={digest:raw})
    acquire(env,'indexed')
    queries=[];c.set_trace_callback(queries.append)
    written=g.write_queue(c,r,tmp/'indexed-queue')
    c.set_trace_callback(None)
    assert len([q for q in queries if q.startswith('SELECT o.entity_key,o.version_id')])==1
    assert written['tasks'][0]['prior_findings']==[]
    prior=written['tasks'][1]['prior_findings']
    assert len(prior)==1 and prior[0]['facts']=={'phone':'1'}
    assert prior==g.prior_findings(c,'research',r['sources'][1]['url'])


def test_identical_extracted_text_skips_quadratic_line_matching(monkeypatch):
    def forbidden(*args,**kwargs):raise AssertionError('Identical text needs no sequence matching')
    monkeypatch.setattr(g.difflib,'SequenceMatcher',forbidden)
    text='Repeated statutory line\n'*10000
    assert g.changed_text_lines(text,text)=={'previous':[],'current':[]}
