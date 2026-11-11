"""Independent end-to-end review transport checks using real disposable evidence."""
import json
from pathlib import Path
import shlex
import subprocess
import sys

import pytest

from flwu import history as h, source_gate as gate, workflow as w
from tests.test_workflow import environment

ROOT=Path(__file__).resolve().parents[1]
HELPER=ROOT/'skills/florida-update/scripts/review_step.py'


def source_answer():
    return dict(decision='no_material_change',summary='Reviewed the acquired fixture profile; no substantive change is established.',evidence=['C1'],people=[])


def checked_next(run,cwd):
    result=subprocess.run([sys.executable,str(HELPER),'--checkout',str(ROOT),'--python',sys.executable,
                           'next','--run-dir',str(run)],cwd=cwd,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    return json.loads(result.stdout)


def invoke(state,value,cwd):
    return subprocess.run(shlex.split(state['command']),input=json.dumps(value,ensure_ascii=False).encode(),
                          cwd=cwd,capture_output=True)


def test_real_pinned_wrapper_accepts_stdin_outside_checkout_and_replays(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    base=tmp_path/"court's run with spaces";base.mkdir()
    run,db,_,server=environment(base);calls=len(server.calls)
    current=checked_next(run,tmp_path)
    assert current['review_mode']=='inline_answer' and isinstance(current['review_card'],dict)
    assert not set(current)&{'packet','answer_template','receipt_template','save_answer','save_receipt','answer_binding','logs','next_state'}
    raw=w.inspect(run,emit=True)
    assert current['review_card']==w.read(raw['review_card'])
    answer=source_answer();saved=invoke(current,answer,tmp_path)
    assert saved.returncode==0,saved.stderr.decode()
    following=json.loads(saved.stdout)
    assert following['task_handle']!=current['task_handle']
    assert json.loads((run/'agent-next-task.json').read_text())==following
    replay=invoke(current,answer,tmp_path)
    assert replay.returncode==0,replay.stderr.decode()
    assert json.loads(replay.stdout)['task_handle']==following['task_handle']
    changed=invoke(current,dict(answer,summary='Different accepted answer'),tmp_path)
    assert changed.returncode!=0
    assert json.loads((run/'agent-next-task.json').read_text())==following
    with h.database(db) as conn:
        assert len(w.accepted(conn,w.load(run)))==1
        assert len(gate.reviews(conn,'weekly'))==1
        assert not list(conn.execute('PRAGMA foreign_key_check'))
    assert len(server.calls)==calls  # Review/refresh never reacquire.


def test_standard_continuation_command_enters_inline_route(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,_,_,_=environment(tmp_path)
    advertised=w.command(w.load(run),'workflow','next-task','--run-dir',str(run))
    result=subprocess.run(shlex.split(advertised),cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    actual=json.loads(result.stdout)
    assert actual['review_mode']=='inline_answer' and isinstance(actual['review_card'],dict)
    assert json.loads((run/'agent-next-task.json').read_text())==actual


def test_inline_reviews_derive_mappings_and_reach_compact_approval(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,server=environment(tmp_path);calls=len(server.calls)
    with h.database(db) as conn:
        expected=len(w.latest_queue(conn,w.load(run))['opinion_reviews']['tasks'])
    current=checked_next(run,tmp_path)
    observed=[]
    for _ in range(30):
        if current.get('phase') not in ('source_review','opinion_review'):break
        observed.append(current['phase'])
        answer=(source_answer() if current['phase']=='source_review' else
                dict(relevance='relevant',summary='Fixture commercial outcome.',holding='Commercial holding.',
                     disposition='Affirmed.',authors=['Example'],evidence=['C1']))
        result=invoke(current,answer,tmp_path)
        assert result.returncode==0,result.stderr.decode()
        current=json.loads(result.stdout)
    else:pytest.fail('Ordinary work did not finish')
    assert expected>=1 and observed.count('opinion_review')==expected and 'source_review' in observed
    assert current['phase']=='publication_acceptance' and not current['complete']
    assert current['review_mode']=='inline_answer'
    assert current['review_progress']['remaining_opinion_reviews']==0
    with h.database(db) as conn:
        for decision in w.accepted(conn,w.load(run)).values():
            receipt=decision['receipt']
            citations=(receipt['support']['current'] if decision['task']['kind']=='source_review' else
                       receipt.get('citations',[]))
            assert citations
            for ci in citations:
                assert ci['quote'] in gate.blob(conn,ci['text_sha256']).decode()
        assert conn.execute('SELECT count(*) FROM finalized_reports').fetchone()[0]==0
    assert len(server.calls)==calls


def test_domain_commit_before_workflow_decision_recovers_once(tmp_path,monkeypatch):
    from flwu import review_transport as transport
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path)
    current=transport.next_task(run)
    folder=run/'agent-steps'/'crash-fixture';folder.mkdir(parents=True)
    answer=folder/'answer.json';w.write(answer,source_answer())
    original=w.record
    def interrupted(conn,config,event):
        if event.get('kind')=='decision':raise RuntimeError('Stopped after domain commit')
        return original(conn,config,event)
    monkeypatch.setattr(w,'record',interrupted)
    with pytest.raises((RuntimeError,ValueError),match='Stopped after domain commit'):
        transport.reply(run,current['task_handle'],answer)
    with h.database(db) as conn:
        assert len(gate.reviews(conn,'weekly'))==1
        assert not w.accepted(conn,w.load(run))
    monkeypatch.setattr(w,'record',original)
    following=transport.reply(run,current['task_handle'],answer)
    assert following['task_handle']!=current['task_handle']
    with h.database(db) as conn:
        assert len(gate.reviews(conn,'weekly'))==1
        assert len(w.accepted(conn,w.load(run)))==1


def test_source_change_invalidates_old_handle_without_acceptance(tmp_path,monkeypatch):
    from flwu import review_transport as transport
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,registry,_=environment(tmp_path)
    current=transport.next_task(run)
    def fetch(url):
        return dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,
                    content_type='text/plain'),b'Now require ten days notice for civil hearings.'
    with h.database(db) as conn:gate.run(conn,registry,'new-observation',fetch=fetch)
    folder=run/'agent-steps'/'stale-fixture';folder.mkdir(parents=True)
    answer=folder/'answer.json';w.write(answer,source_answer())
    with pytest.raises(ValueError):transport.reply(run,current['task_handle'],answer)
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


def test_identical_invalid_retry_not_counted_but_second_distinct_failure_checkpoints(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path)
    current=checked_next(run,tmp_path)
    bad=dict(source_answer(),unexpected='first invalid value')
    first=invoke(current,bad,tmp_path)
    assert first.returncode==0,first.stderr.decode()
    retry=json.loads(first.stdout)
    assert retry['task_handle']==current['task_handle']
    assert retry['review_card']==current['review_card']
    assert retry['review_progress']['failed_short_answers']==1
    replay=invoke(current,bad,tmp_path)
    assert replay.returncode==0,replay.stderr.decode()
    assert json.loads(replay.stdout)['review_progress']['failed_short_answers']==1
    second=invoke(current,dict(bad,unexpected='second distinct invalid value'),tmp_path)
    assert second.returncode==0,second.stderr.decode()
    following=json.loads(second.stdout)
    assert following['task_handle']!=current['task_handle']
    assert following['review_progress']['failed_short_answers']==2
    assert following['review_progress']['checkpointed_reviews']==1
    with h.database(db) as conn:
        assert not w.accepted(conn,w.load(run))
        assert not gate.reviews(conn,'weekly')


def test_concurrent_reply_is_refused_and_lock_released(tmp_path,monkeypatch):
    import threading
    from flwu import review_transport as transport
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);current=transport.next_task(run)
    folder=run/'agent-steps'/'concurrency-fixture';folder.mkdir(parents=True)
    answer=folder/'answer.json';w.write(answer,source_answer())
    started=threading.Event();release=threading.Event();errors=[]
    original=w.submit
    def blocked(*args,**kwargs):
        started.set()
        if not release.wait(5):raise RuntimeError('Test failed to release submit')
        return original(*args,**kwargs)
    monkeypatch.setattr(w,'submit',blocked)
    def first():
        try:transport.reply(run,current['task_handle'],answer)
        except BaseException as exc:errors.append(exc)
    thread=threading.Thread(target=first);thread.start()
    try:
        assert started.wait(5)
        with pytest.raises(ValueError):transport.reply(run,current['task_handle'],answer)
    finally:
        release.set();thread.join(5)
    assert not thread.is_alive() and not errors
    # A completed caller must not leave the transport lock held.
    assert transport.reply(run,current['task_handle'],answer)['task_handle']!=current['task_handle']
    with h.database(db) as conn:assert len(w.accepted(conn,w.load(run)))==1
