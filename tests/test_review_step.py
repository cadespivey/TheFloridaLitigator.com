"""The skill runner must not mask failures or erase the last good next-task state."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

@pytest.fixture
def step():
    path=Path(__file__).parents[1]/'skills/florida-update/scripts/review_step.py'
    spec=importlib.util.spec_from_file_location('review_step',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

@pytest.fixture
def run(tmp_path):
    folder=tmp_path/'run';folder.mkdir()
    for name in ('packet.json','receipt.json','agent-next-task.json'):
        (folder/name).write_text('{"previous":"preserve me"}\n')
    return folder

def test_failed_submission_keeps_state_and_does_not_request_another_task(step,run,monkeypatch):
    calls=[];before={p.name:p.read_bytes() for p in run.iterdir()}
    def failed(argv,**kwargs):
        calls.append(argv);return SimpleNamespace(returncode=7,stdout='Partial stdout',stderr='Actual validation failure')
    monkeypatch.setattr(step.subprocess,'run',failed)
    assert step.main(['submit','--run-dir',str(run),'--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')])==7
    assert len(calls)==1 and 'submit' in calls[0]
    assert all((run/name).read_bytes()==value for name,value in before.items())
    attempt=next((run/'agent-steps').iterdir())
    assert (attempt/'submit.stderr').read_text()=='Actual validation failure'
    assert json.loads((attempt/'submit.json').read_text())['exit_code']==7

@pytest.mark.parametrize('failure', ['command','invalid_json','invalid_state'])
def test_next_failure_never_truncates_previous_pointer(step,run,monkeypatch,failure):
    old=(run/'agent-next-task.json').read_bytes()
    def response(argv,**kwargs):
        return SimpleNamespace(returncode=3 if failure=='command' else 0,
            stdout='not JSON' if failure=='invalid_json' else '{}',stderr='Failure')
    monkeypatch.setattr(step.subprocess,'run',response)
    assert step.main(['next','--run-dir',str(run)])!=0
    assert (run/'agent-next-task.json').read_bytes()==old

def test_success_submits_exact_paths_then_atomically_saves_actual_next_state(step,run,monkeypatch):
    state=dict(phase='source_review',complete=False,packet='next packet');calls=[]
    def response(argv,**kwargs):
        calls.append(argv)
        return SimpleNamespace(returncode=0,stdout=json.dumps(state) if 'next-task' in argv else '{"capture_id":"saved"}',stderr='')
    monkeypatch.setattr(step.subprocess,'run',response)
    assert step.main(['--checkout',str(run.parent),'submit','--run-dir',str(run),
                      '--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')])==0
    assert len(calls)==2 and 'submit' in calls[0] and 'next-task' in calls[1]
    assert calls[0][-4:]==['--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')]
    assert json.loads((run/'agent-next-task.json').read_text())==state
    assert not list(run.glob('.next-*'))

def test_paths_outside_run_are_rejected_before_command_execution(step,run,monkeypatch):
    monkeypatch.setattr(step.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):step.main(['next','--run-dir',str(run),'--output',str(run.parent/'outside.json')])

@pytest.mark.parametrize('name',['registry.json','workflow/contract.json'])
def test_next_output_cannot_overwrite_run_inputs(step,run,monkeypatch,name):
    monkeypatch.setattr(step.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):step.main(['next','--run-dir',str(run),'--output',str(run/name)])


def test_real_launcher_next_task_preserves_the_coordinators_state(step,tmp_path):
    from flwu import history as h, workflow as w, source_gate as gate
    database=tmp_path/'history.sqlite';registry=tmp_path/'registry.json';run=tmp_path/'run'
    with h.database(database) as conn:
        h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},run_id='initial',
                 payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[]),artifacts={})
    w.write(registry,dict(schema_version=1,stream='weekly',review_protocol=gate.PROTOCOL,sources=[]))
    w.initialize(run,database,registry,'run',start='2026-10-26',end='2026-11-01')
    assert step.main(['--checkout',str(Path(__file__).parents[1]),'next','--run-dir',str(run)])==0
    actual=json.loads((run/'agent-next-task.json').read_text())
    assert actual['phase']=='acquisition' and actual['complete'] is False
    attempt=next((run/'agent-steps').iterdir())
    assert json.loads((attempt/'next.stdout').read_text())==actual
    assert json.loads((attempt/'next.json').read_text())['exit_code']==0
