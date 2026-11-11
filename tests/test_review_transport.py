"""Binding and failure-path tests for code-owned inline review transport."""
import json
from pathlib import Path

import pytest

from flwu import compact_review, history as h, review_transport as transport, workflow as w
from tests.test_workflow import environment

ROOT=Path(__file__).resolve().parents[1]


def answer_file(run, raw, name='input'):
    folder=run/'agent-steps'/name;folder.mkdir(parents=True,exist_ok=True)
    path=folder/'answer.json';path.write_bytes(raw);return path


def answer():
    return dict(decision='no_material_change',summary='No material change in the acquired fixture.',evidence=['C1'],people=[])


@pytest.mark.parametrize('target',['card','packet','manifest','contract','wrapper'])
def test_modified_artifact_rejected_without_acceptance(tmp_path,monkeypatch,target):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path)
    current=transport.next_task(run);raw=w.inspect(run,emit=True)
    paths={'card':Path(raw['review_card']),'packet':Path(raw['packet']),
           'manifest':run/'workflow/inline-tasks'/f"{current['task_handle']}.json",
           'contract':run/'workflow/contract.json','wrapper':run/'review'}
    path=paths[target];original=path.read_bytes();path.write_bytes(original+b'\n')
    if target=='contract':
        value=json.loads(original);value['end']='2026-10-23';path.write_text(json.dumps(value))
    with pytest.raises(ValueError):transport.reply(run,current['task_handle'],answer_file(run,json.dumps(answer()).encode()))
    if target=='contract':path.write_bytes(original)  # Readback requires the original contract, never a new one.
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


@pytest.mark.parametrize('handle',['../escape','x'*24,'a'*23,'a'*25,'0'*24])
def test_unknown_or_malformed_handle_fails_closed(tmp_path,monkeypatch,handle):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);transport.next_task(run)
    with pytest.raises(ValueError):transport.reply(run,handle,answer_file(run,b'{}'))
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


def test_foreign_run_handle_and_outside_input_rejected(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    one=tmp_path/'one';one.mkdir();two=tmp_path/'two';two.mkdir()
    run,db,_,_=environment(one);other,_,_,_=environment(two)
    current=transport.next_task(run);foreign=transport.next_task(other)
    with pytest.raises(ValueError):transport.reply(run,foreign['task_handle'],answer_file(run,b'{}'))
    outside=tmp_path/'outside.json';outside.write_text('{}')
    with pytest.raises(ValueError):transport.reply(run,current['task_handle'],outside)
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


@pytest.mark.parametrize('raw',[b'null',b'[]',b'{bad json',b'\xff'])
def test_malformed_input_preserved_replayed_once_and_correctable(tmp_path,monkeypatch,raw):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);current=transport.next_task(run)
    path=answer_file(run,raw)
    failed=transport.reply(run,current['task_handle'],path)
    assert failed['review_progress']['failed_short_answers']==1
    assert path.read_bytes()==raw and failed['task_handle']==current['task_handle']
    replay=transport.reply(run,current['task_handle'],answer_file(run,raw,'retry'))
    assert replay['review_progress']['failed_short_answers']==1
    fixed=transport.reply(run,current['task_handle'],answer_file(run,json.dumps(answer()).encode(),'corrected'))
    assert fixed['task_handle']!=current['task_handle']
    with h.database(db) as conn:assert len(w.accepted(conn,w.load(run)))==1


def test_inline_card_and_semantic_instructions_identical_to_original_compiler(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);state=transport.next_task(run);legacy=w.inspect(run,emit=True)
    with h.database(db) as conn:
        expected=compact_review.prepare(conn,w.read(legacy['packet']))['card']
    assert state['review_card']==expected
    assert not set(state)&{'packet','answer_binding','answer_template','receipt_template','save_answer','save_receipt'}
    assert len(state['command'])<len(legacy['command'])


def test_uncertainty_retry_stays_unresolved_without_duplicate_checkpoint(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);state=transport.next_task(run)
    raw=json.dumps(dict(decision='insufficient_evidence',summary='Assignment is unresolved in this fixture.',evidence=[],people=[])).encode()
    first=transport.reply(run,state['task_handle'],answer_file(run,raw))
    replay=transport.reply(run,state['task_handle'],answer_file(run,raw,'retry'))
    assert first['task_handle']==replay['task_handle'] and first['task_handle']!=state['task_handle']
    assert replay['review_progress']['checkpointed_reviews']==1
    with h.database(db) as conn:
        assert not w.accepted(conn,w.load(run))
        assert len([e for e in w.events(conn,w.load(run)) if e['kind']=='review_exception'])==1


def test_reply_validates_immutable_input_even_if_callers_file_changes(tmp_path,monkeypatch):
    from flwu import workflow_short
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);state=transport.next_task(run)
    raw=json.dumps(answer()).encode();path=answer_file(run,raw)
    original=workflow_short.answer
    def caller_edit(*args,**kwargs):
        path.write_text('{"summary":"unsubmitted replacement"}')
        return original(*args,**kwargs)
    monkeypatch.setattr(workflow_short,'answer',caller_edit)
    following=transport.reply(run,state['task_handle'],path)
    assert following['task_handle']!=state['task_handle']
    with h.database(db) as conn:
        saved=next(iter(w.accepted(conn,w.load(run)).values()))
        assert saved['receipt']['summary']==answer()['summary']
        from flwu import source_gate
        assert source_gate.blob(conn,h.sha(raw))==raw


def test_accepted_replay_cannot_bypass_source_withdrawal_gate(tmp_path,monkeypatch):
    from flwu.review_withdrawal import withdraw
    monkeypatch.setattr(w,'ROOT',ROOT)
    run,db,_,_=environment(tmp_path);state=transport.next_task(run)
    path=answer_file(run,json.dumps(answer()).encode())
    transport.reply(run,state['task_handle'],path)
    with h.database(db) as conn:
        accepted=next(iter(w.accepted(conn,w.load(run)).values()))
        withdraw(conn,'weekly',h.sha(accepted['receipt']),'Fixture editor','This review needs explicit correction.')
    with pytest.raises(ValueError):transport.reply(run,state['task_handle'],path)
    with h.database(db) as conn:
        assert len(w.accepted(conn,w.load(run)))==1
        assert conn.execute('SELECT count(*) FROM finalized_reports').fetchone()[0]==0
