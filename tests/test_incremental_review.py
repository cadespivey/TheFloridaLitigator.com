"""Fast paths must produce the same work and never supply a model verdict."""
import json
from pathlib import Path

import pytest
from flwu import derived_cache as d, history as h, source_gate as g
from flwu import workflow as w, update, raw_comparison
from tests.test_source_gate import env, acquire, receipt
from tests.test_workflow import environment, answer


def test_identical_bytes_skip_extraction_but_save_fresh_observations(env, monkeypatch):
    c, registry, _ = env
    original = g.extract
    calls = []
    monkeypatch.setattr(g, 'extract', lambda *a: (calls.append(a[1]['url']) or original(*a)))
    acquire(env, 'one')
    first = g.observations(c, registry['stream'])
    acquire(env, 'two')
    second = g.observations(c, registry['stream'])[-2:]
    assert len(calls) == 2
    assert all(a['sha256'] == b['sha256'] and a['text_sha256'] == b['text_sha256']
               and a['capture_id'] != b['capture_id'] and b['run_id'] == 'two'
               for a,b in zip(first, second))
    assert len(g.queue(c, registry)['tasks']) == 2  # Parsing reuse is not review.


def test_extraction_policy_change_and_unavailable_extraction_retry(env, monkeypatch):
    c, r, _ = env
    calls = []
    monkeypatch.setattr(g, 'extract', lambda *a: (calls.append(1) or ('', 'unavailable', [])))
    acquire(env, 'one'); acquire(env, 'two')
    assert len(calls) == 4
    original_policy = d.policy()
    monkeypatch.setattr(g, 'extract', lambda *a: (calls.append(1) or ('Readable', 'utf8', [])))
    acquire(env, 'three'); acquire(env, 'four')
    assert len(calls) == 6
    monkeypatch.setattr(d, 'policy', lambda: original_policy+'changed')
    acquire(env, 'five')
    assert len(calls) == 8


@pytest.mark.parametrize('field,value', [('content_type','text/html'), ('resolved_url','https://court.gov/new-base/')])
def test_identical_bytes_changed_metadata_requires_extraction(env, monkeypatch, field, value):
    c, r, _ = env
    acquire(env, 'one')
    original = g.extract; calls = []
    monkeypatch.setattr(g, 'extract', lambda *a: (calls.append(1) or original(*a)))
    def fetch(url):
        meta = dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,
                    http_status=200,content_type='text/plain')
        meta[field] = value
        return meta, b'Profile' if url == r['sources'][0]['url'] else b'Procedure'
    g.run(c, r, 'two', fetch=fetch)
    assert len(calls) == 2


def test_acquisition_reads_history_constant_times_not_per_source(env, monkeypatch):
    c, r, _ = env
    r['sources'] += [dict(id=g.source_id(u),url=u) for u in
                     [f'https://court.gov/judge/{n}' for n in range(12)]]
    original = g.observations; calls = []
    monkeypatch.setattr(g, 'observations', lambda *a: (calls.append(1) or original(*a)))
    def fetch(url):
        return dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,
                    http_status=200,content_type='text/plain'), b'Operating instructions'
    g.run(c, r, 'one', fetch=fetch)
    assert len(calls) == 2  # Acquisition index and final queue, regardless of N.


def test_persistent_comparison_cache_corruption_policy_and_missing_original(env, monkeypatch):
    c, r, folder = env
    acquire(env, 'one'); acquire(env, 'two', page=b'Updated profile')
    o = g.observations(c, r['stream'])[-2]
    before, after = o['previous_sha256'], o['sha256']
    original = raw_comparison.compare; calls = []
    monkeypatch.setattr(raw_comparison, 'compare', lambda *a: (calls.append(1) or original(*a)))
    one = g.cached_comparison(c, before, after, 'text/plain')
    # A fresh connection/process-level cache instance can reuse the result.
    with h.database(folder/'history.sqlite') as fresh:
        assert g.cached_comparison(fresh, before, after, 'text/plain') == one
    assert len(calls) == 1
    path = d.Cache(c).path('raw-comparison', dict(before=before,after=after,content_type='text/plain'))
    path.write_text('{partial')
    assert g.cached_comparison(c, before, after, 'text/plain') == one
    assert len(calls) == 2
    old_policy = d.policy(); monkeypatch.setattr(d,'policy',lambda: old_policy+'changed')
    assert g.cached_comparison(c, before, after, 'text/plain') == one
    assert len(calls) == 3
    c.execute('DELETE FROM artifacts WHERE sha256=?',(before,)); c.commit()
    with pytest.raises(ValueError,match='Missing or corrupt'):
        g.cached_comparison(c, before, after, 'text/plain')


def test_disabled_unwritable_and_tampered_caches_recompute(env, monkeypatch):
    c, _, folder = env
    cache = d.Cache(c); key = dict(test=True)
    cache.put('test', key, dict(value=1))
    path = cache.path('test',key)
    record = json.loads(path.read_text()); record['result']['value'] = 99
    path.write_text(json.dumps(record))
    assert cache.memo('test',key,lambda: dict(value=2)) == dict(value=2)
    cache.root = folder/'not-directory'; cache.root.write_text('preserve')
    assert cache.memo('test',key,lambda: dict(value=3)) == dict(value=3)
    monkeypatch.setenv('FLWU_DISABLE_DERIVED_CACHE','1')
    assert d.Cache(c).memo('test',key,lambda: dict(value=4)) == dict(value=4)


def test_queue_cache_equivalence_and_only_dependent_source_exports(env, monkeypatch):
    c, r, folder = env
    first, _ = acquire(env, 'one')
    output = folder/'queue'
    exported = g.write_queue(c,r,output,start='2026-10-01',end='2026-11-30')
    originals = {p:p.stat().st_mtime_ns for p in output.rglob('*') if p.is_file()}
    exports = []; original = g.export_task
    monkeypatch.setattr(g, 'export_task', lambda *a,**kw: (exports.append(a[1]['source_id']) or original(*a,**kw)))
    assert g.write_queue(c,r,output,start='2026-10-01',end='2026-11-30') == exported
    assert not exports and all(p.stat().st_mtime_ns == stamp for p,stamp in originals.items())
    g.accept(c,r,receipt(first['tasks'][0],r,c))
    cached = g.write_queue(c,r,output,start='2026-10-01',end='2026-11-30')
    assert not exports and len(cached['tasks']) == 1
    monkeypatch.setenv('FLWU_DISABLE_DERIVED_CACHE','1')
    assert g.write_queue(c,r,output,start='2026-10-01',end='2026-11-30') == cached


def test_unchanged_next_task_does_not_rebuild_queue_and_repairs_emitted_files(tmp_path, monkeypatch):
    run, db, r, server = environment(tmp_path)
    first = w.inspect(run,emit=True)
    packet = w.read(first['packet']); path = Path(packet['inputs']['current_path'])
    expected = path.read_bytes(); path.write_bytes(b'corrupt local projection')
    calls = len(server.calls)
    monkeypatch.setattr(update,'refresh_queue',lambda *a,**kw: pytest.fail('unchanged queue rebuilt'))
    assert w.inspect(run,emit=True)['packet'] == first['packet']
    assert path.read_bytes() == expected and len(server.calls) == calls


def test_submission_invalidates_queue_and_combined_advance_recovers(tmp_path, monkeypatch):
    run, db, r, _ = environment(tmp_path)
    task = w.inspect(run,emit=True)
    answer(run, db, task)  # Accepted exact receipt; simulate interruption before advancement.
    original = update.refresh_queue; calls = []
    monkeypatch.setattr(update,'refresh_queue',lambda *a,**kw: (calls.append(1) or original(*a,**kw)))
    state = w.submit_and_next(run,task['packet'],task['save_receipt'])
    assert state['packet'] != task['packet'] and len(calls) == 0
    assert w.submit_and_next(run,task['packet'],task['save_receipt'])['packet'] == state['packet']
    assert len(calls) == 0
    with h.database(db) as c:
        cached = w.latest_queue(c,w.load(run),refresh=True)
        monkeypatch.setenv('FLWU_DISABLE_DERIVED_CACHE','1')
        assert w.latest_queue(c,w.load(run),refresh=True) == cached


def test_failed_advance_reports_saved_receipt_and_preserves_replay(tmp_path, monkeypatch):
    run, db, r, _ = environment(tmp_path)
    task = w.inspect(run,emit=True); answer(run,db,task)
    original = w.inspect
    monkeypatch.setattr(w,'inspect',lambda *a,**kw: (_ for _ in ()).throw(ValueError('projection interrupted')))
    with pytest.raises(ValueError,match='submission is saved.*projection interrupted'):
        w.submit_and_next(run,task['packet'],task['save_receipt'])
    monkeypatch.setattr(w,'inspect',original)
    assert w.submit_and_next(run,task['packet'],task['save_receipt'])['packet'] != task['packet']


def test_opinion_status_event_invalidates_queue_with_identical_pdf(tmp_path, monkeypatch):
    run, db, r, _ = environment(tmp_path)
    w.inspect(run,emit=True)  # Warm snapshot.
    from flwu import opinion_discovery as opinions
    with h.database(db) as c:
        item = next(iter(opinions.known(c,r['stream']).values()))
        before = next(o for o in g.observations(c,r['stream']) if o['url']==item['pdf_url'])['sha256']
        item['metadata']['note'] = 'Opinion withdrawn.'
        raw = h.canonical(item['metadata']).encode()
        item['state_sha256'] = h.sha(raw)
        item['status_source']['text_sha256'] = h.sha(raw)
        opinions.save(c,r['stream'],'status-correction','detail',dict(kind='detail',id=item['id'],complete=True,entries=[item]))
    config = w.load(run)
    with h.database(db) as c:
        queue = w.latest_queue(c,config,refresh=True)
        task = queue['opinion_reviews']['tasks'][0]
        assert task['source_observation']['sha256'] == before
        assert task['opinion']['metadata']['note'] == 'Opinion withdrawn.'
        monkeypatch.setenv('FLWU_DISABLE_DERIVED_CACHE','1')
        assert w.latest_queue(c,config,refresh=True) == queue


def test_new_observation_invalidates_warm_queue(tmp_path, monkeypatch):
    run, db, r, _ = environment(tmp_path)
    w.inspect(run,emit=True)
    with h.database(db) as c:
        def fetch(url):
            return dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,
                        http_status=200,content_type='text/plain'), b'Updated chambers telephone: 555-0200'
        g.run(c,r,'new-observation',fetch=fetch)
    new = w.inspect(run,emit=True)
    assert w.read(new['packet'])['inputs']['observation']['run_id'] == 'new-observation'


def test_concurrent_acquisition_during_queue_refresh_is_not_cached(tmp_path,monkeypatch):
    run, db, r, _ = environment(tmp_path)
    original = update.refresh_queue
    def race(conn,*args,**kwargs):
        result = original(conn,*args,**kwargs)
        from flwu import opinion_discovery as opinions
        opinions.save(conn,r['stream'],'external','new-listing',dict(kind='listing',complete=False,entries=[]))
        return result
    monkeypatch.setattr(update,'refresh_queue',race)
    with pytest.raises(ValueError,match='inputs changed during queue refresh'):
        w.inspect(run,emit=True)
    monkeypatch.setattr(update,'refresh_queue',original)
    assert w.inspect(run,emit=True)['phase'] == 'source_review'


def test_protocol_change_never_reuses_old_export_template(env):
    c, r, folder = env
    acquire(env,'one'); old = g.write_queue(c,r,folder/'queue')
    r['review_protocol'] = 'different-review-contract'
    new = g.write_queue(c,r,folder/'queue')
    assert old['tasks'][0]['review_template']['review_protocol'] != new['tasks'][0]['review_template']['review_protocol']
    assert new['tasks'][0]['review_template']['review_protocol'] == r['review_protocol']


def test_baseline_state_invalidates_without_a_new_capture(env):
    c, r, _ = env
    before = d.dependencies(c,[r['stream']])
    row = c.execute('SELECT seq FROM captures ORDER BY seq LIMIT 1').fetchone()
    data=b'Fixture finalized report'
    c.execute('INSERT INTO artifacts VALUES(?,?)',(h.sha(data),data))
    c.execute('INSERT INTO finalized_reports(stream,capture_seq,report_sha256,finalized_at,review) VALUES(?,?,?,?,?)',
              (r['stream'],row['seq'],h.sha(data),h.now(),'Fixture editor'))
    c.commit()
    after = d.dependencies(c,[r['stream']])
    assert before['streams'] == after['streams'] and before != after


def test_source_delta_does_not_refresh_other_courts(env,monkeypatch):
    c, r, folder = env
    r['sources'][1] = dict(id=g.source_id('https://other-court.gov/profile'),url='https://other-court.gov/profile')
    first,_ = acquire(env,'one')
    g.write_queue(c,r,folder/'queue')
    g.accept(c,r,receipt(first['tasks'][0],r,c))
    from flwu import content_fingerprint
    original=content_fingerprint.ReviewIndex.reuse; calls=[]
    def reuse(self,current):
        calls.append(current['url']); return original(self,current)
    monkeypatch.setattr(content_fingerprint.ReviewIndex,'reuse',reuse)
    g.queue(c,r)
    assert 'https://other-court.gov/profile' not in calls


def test_real_cli_combined_submission_returns_next_state(tmp_path,monkeypatch,capsys):
    from flwu.cli import main
    run,db,r,_=environment(tmp_path)
    task=w.inspect(run,emit=True);answer(run,db,task)
    assert main(['workflow','submit','--advance','--run-dir',str(run),
                 '--packet',task['packet'],'--receipt',task['save_receipt']])==0
    state=json.loads(capsys.readouterr().out)
    assert state['complete'] is False and state['packet']!=task['packet']
