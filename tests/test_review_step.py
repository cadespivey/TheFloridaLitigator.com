"""The skill runner must not mask failures or erase the last good next-task state."""
import importlib.util
import json
import sys
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
        return SimpleNamespace(returncode=0,stdout=json.dumps(state),stderr='')
    monkeypatch.setattr(step.subprocess,'run',response)
    assert step.main(['--checkout',str(run.parent),'submit','--run-dir',str(run),
                      '--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')])==0
    assert len(calls)==1 and 'submit' in calls[0] and '--advance' in calls[0]
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


def test_real_launcher_next_task_preserves_the_coordinators_state(step,tmp_path,monkeypatch):
    from flwu import history as h, workflow as w, source_gate as gate
    # CI tests the installed wheel; the real launcher deliberately imports this
    # checkout. Bind the fixture to that selected checkout just as the CLI does.
    monkeypatch.setattr(w,'ROOT',Path(__file__).parents[1])
    database=tmp_path/'history.sqlite';registry=tmp_path/'registry.json';run=tmp_path/'run'
    with h.database(database) as conn:
        h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},run_id='initial',
                 payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[]),artifacts={})
    w.write(registry,dict(schema_version=1,stream='weekly',review_protocol=gate.PROTOCOL,sources=[]))
    w.initialize(run,database,registry,'run',start='2026-10-26',end='2026-11-01')
    assert step.main(['--checkout',str(Path(__file__).parents[1]),'--python',sys.executable,'next','--run-dir',str(run)])==0
    actual=json.loads((run/'agent-next-task.json').read_text())
    assert actual['phase']=='acquisition' and actual['complete'] is False
    attempt=next((run/'agent-steps').iterdir())
    assert json.loads((attempt/'next.stdout').read_text())==actual
    assert json.loads((attempt/'next.json').read_text())['exit_code']==0


def test_correction_uses_exact_predecessor_then_requests_next_task(step,run,monkeypatch):
    calls=[]
    def response(argv,**kwargs):
        calls.append(argv)
        return SimpleNamespace(returncode=0,stdout='{"phase":"source_review","complete":false}',stderr='')
    monkeypatch.setattr(step.subprocess,'run',response)
    assert step.main(['revise','--run-dir',str(run),'--packet',str(run/'packet.json'),
        '--receipt',str(run/'receipt.json'),'--predecessor','exact-digest','--reason','Supported correction'])==0
    assert calls[0][-4:]==['--predecessor','exact-digest','--reason','Supported correction']
    assert len(calls)==1 and 'revise' in calls[0] and '--advance' in calls[0]


def test_failed_correction_preserves_pointer_without_requesting_next(step,run,monkeypatch):
    calls=[];old=(run/'agent-next-task.json').read_bytes()
    def failure(argv,**kwargs):
        calls.append(argv);return SimpleNamespace(returncode=4,stdout='',stderr='Stale predecessor')
    monkeypatch.setattr(step.subprocess,'run',failure)
    assert step.main(['revise','--run-dir',str(run),'--packet',str(run/'packet.json'),
        '--receipt',str(run/'receipt.json'),'--predecessor','stale','--reason','Correction'])==4
    assert len(calls)==1 and (run/'agent-next-task.json').read_bytes()==old


def test_interpreter_override_preserves_virtual_environment_path(step,run,monkeypatch):
    calls=[];interpreter=run/'venv/bin/python'
    interpreter.parent.mkdir(parents=True)
    interpreter.symlink_to(Path(sys.executable).resolve())
    def response(argv,**kwargs):
        calls.append(argv);return SimpleNamespace(returncode=0,stdout='{"phase":"source_review","complete":false}',stderr='')
    monkeypatch.setattr(step.subprocess,'run',response)
    assert step.main(['--python',str(interpreter),'next','--run-dir',str(run)])==0
    assert calls[0][calls[0].index('--python')+1]==str(interpreter)


def test_two_failed_drafts_require_evidence_bound_repair_note(step,run,monkeypatch):
    calls=[]
    def failure(argv,**kwargs):
        calls.append(argv);return SimpleNamespace(returncode=1,stdout='',stderr='Workflow error: Citation mismatch')
    monkeypatch.setattr(step.subprocess,'run',failure)
    argv=['submit','--run-dir',str(run),'--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')]
    assert step.main(argv)==1 and step.main(argv)==1
    with pytest.raises(SystemExit):step.main(argv)
    assert len(calls)==2
    import hashlib
    folders=sorted((run/'agent-steps').iterdir())
    for folder in folders:
        assert (folder/'receipt.json').read_bytes()==(run/'receipt.json').read_bytes()
        assert (folder/'packet.json').read_bytes()==(run/'packet.json').read_bytes()
    note=run/'repair.json'
    note.write_text(json.dumps(dict(packet_sha256=hashlib.sha256((run/'packet.json').read_bytes()).hexdigest(),
        failed_attempts=[p.name for p in folders[-2:]],change_in_approach='Inspect the exact acquired pair instead of rewording.',
        evidence_paths=[str(run/'packet.json')])))
    assert step.main(argv+['--repair-note',str(note)])==1
    assert len(calls)==3


def test_saved_submission_advance_failure_does_not_consume_draft_budget(step,run,monkeypatch):
    def failure(argv,**kwargs):return SimpleNamespace(returncode=1,stdout='',stderr='Review submission is saved (capture), but advancement failed')
    monkeypatch.setattr(step.subprocess,'run',failure)
    argv=['submit','--run-dir',str(run),'--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')]
    for _ in range(3):assert step.main(argv)==1


# --- answer action tests ---

def test_answer_argv_construction(step,run,monkeypatch):
    """The answer action must invoke workflow answer --advance with --packet and --answer."""
    answer=run/'answer.json'
    answer.write_text('{"decision":"no_material_change","summary":"ok","evidence":[],"people":[]}')
    calls=[]
    def response(argv,**kwargs):
        calls.append(argv)
        return SimpleNamespace(returncode=0,stdout='{"phase":"source_review","complete":false}',stderr='')
    monkeypatch.setattr(step.subprocess,'run',response)
    rc=step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(answer)])
    assert rc==0
    assert len(calls)==1
    cmd=calls[0]
    # Must contain 'answer' subcommand and --advance
    assert 'answer' in cmd
    assert '--advance' in cmd
    # Must pass --packet and --answer with resolved paths
    assert '--packet' in cmd
    assert str(run/'packet.json') in cmd
    assert '--answer' in cmd
    assert str(answer) in cmd
    # Must NOT pass --receipt
    assert '--receipt' not in cmd


def test_answer_saves_copied_original_bytes_and_hashes(step,run,monkeypatch):
    """Per-attempt packet.json and answer.json must preserve exact original bytes; attempt.json has both hashes."""
    import hashlib
    answer=run/'answer.json'
    answer_bytes=b'{"decision":"material_change","summary":"statute change","evidence":["ev1"],"people":[]}'
    answer.write_bytes(answer_bytes)
    packet_bytes=(run/'packet.json').read_bytes()
    monkeypatch.setattr(step.subprocess,'run',
        lambda argv,**kw:SimpleNamespace(returncode=0,stdout='{"phase":"source_review","complete":false}',stderr=''))
    rc=step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(answer)])
    assert rc==0
    attempt=next((run/'agent-steps').iterdir())
    # Copied bytes must match originals exactly
    assert (attempt/'packet.json').read_bytes()==packet_bytes
    assert (attempt/'answer.json').read_bytes()==answer_bytes
    # attempt.json must have correct hashes
    meta=json.loads((attempt/'attempt.json').read_text())
    assert meta['action']=='answer'
    assert meta['packet_file_sha256']==hashlib.sha256(packet_bytes).hexdigest()
    assert meta['answer_sha256']==hashlib.sha256(answer_bytes).hexdigest()
    # Must NOT have receipt_sha256 or repair_note_sha256
    assert 'receipt_sha256' not in meta
    assert 'repair_note_sha256' not in meta


def test_answer_failure_preserves_previous_pointer(step,run,monkeypatch):
    """A failed answer must preserve the existing next-state pointer and return the coordinator exit code."""
    answer=run/'answer.json'
    answer.write_text('{"decision":"material_change","summary":"x","evidence":[],"people":[]}')
    old=(run/'agent-next-task.json').read_bytes()
    monkeypatch.setattr(step.subprocess,'run',
        lambda argv,**kw:SimpleNamespace(returncode=5,stdout='',stderr='Validator rejected: missing evidence ID'))
    rc=step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(answer)])
    assert rc==5
    assert (run/'agent-next-task.json').read_bytes()==old


def test_answer_outside_run_rejected(step,run,monkeypatch):
    """Answer and packet paths outside the run directory must be rejected before execution."""
    outside_answer=run.parent/'outside-answer.json'
    outside_answer.write_text('{}')
    monkeypatch.setattr(step.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):
        step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(outside_answer)])


def test_answer_cannot_alias_next_state_output(step,run,monkeypatch):
    """The answer file must not be the same as the next-state output path."""
    output=run/'agent-next-task.json'
    monkeypatch.setattr(step.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):
        step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(output)])


def test_answer_requires_both_packet_and_answer(step,run,monkeypatch):
    """Answer without --packet or without --answer must produce a parser error."""
    answer=run/'answer.json'
    answer.write_text('{}')
    monkeypatch.setattr(step.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):
        step.main(['answer','--run-dir',str(run),'--answer',str(answer)])
    with pytest.raises(SystemExit):
        step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json')])


def test_answer_accepts_review_exceptions_state(step,run,monkeypatch):
    """A successful answer that returns review_exceptions with complete:false is a valid coordinator result."""
    answer=run/'answer.json'
    answer.write_text('{"decision":"insufficient_evidence","summary":"unclear","evidence":[],"people":[]}')
    state=dict(phase='review_exceptions',complete=False,exceptions=[{'source':'s1','cause':'raw_change_unresolved'}])
    def response(argv,**kwargs):
        return SimpleNamespace(returncode=0,stdout=json.dumps(state),stderr='')
    monkeypatch.setattr(step.subprocess,'run',response)
    rc=step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(answer)])
    assert rc==0
    assert json.loads((run/'agent-next-task.json').read_text())==state
    # The pointer is saved because the coordinator succeeded (exit 0)
    attempt=next((run/'agent-steps').iterdir())
    assert json.loads((attempt/'answer.json').read_text())==json.loads(answer.read_text())


def test_answer_preserves_exact_stderr_on_failure(step,run,monkeypatch):
    """The exact stderr from the coordinator must be preserved in the attempt log."""
    answer=run/'answer.json'
    answer.write_text('{}')
    exact_stderr='Workflow error: version mismatch packet=abc expected=def'
    monkeypatch.setattr(step.subprocess,'run',
        lambda argv,**kw:SimpleNamespace(returncode=2,stdout='',stderr=exact_stderr))
    rc=step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(answer)])
    assert rc==2
    attempt=next((run/'agent-steps').iterdir())
    assert (attempt/'answer.stderr').read_text()==exact_stderr
    assert json.loads((attempt/"attempt.json").read_text())["exit_code"]==2


def test_old_actions_unaffected_by_answer_addition(step,run,monkeypatch):
    """Adding answer must not break existing next, submit, or revise behavior."""
    # next
    monkeypatch.setattr(step.subprocess,'run',
        lambda argv,**kw:SimpleNamespace(returncode=0,stdout='{"phase":"acquisition","complete":false}',stderr=''))
    assert step.main(['next','--run-dir',str(run)])==0
    # submit
    monkeypatch.setattr(step.subprocess,'run',
        lambda argv,**kw:SimpleNamespace(returncode=0,stdout='{"phase":"source_review","complete":false}',stderr=''))
    assert step.main(['submit','--run-dir',str(run),'--packet',str(run/'packet.json'),'--receipt',str(run/'receipt.json')])==0
    # revise
    monkeypatch.setattr(step.subprocess,'run',
        lambda argv,**kw:SimpleNamespace(returncode=0,stdout='{"phase":"source_review","complete":false}',stderr=''))
    assert step.main(['revise','--run-dir',str(run),'--packet',str(run/'packet.json'),
        '--receipt',str(run/'receipt.json'),'--predecessor','abc','--reason','Fix'])==0


def test_answer_does_not_run_repair_budget(step,run,monkeypatch):
    """Answer must not invoke repair_budget even after two failures; coordinator owns that logic."""
    import hashlib
    answer=run/'answer.json'
    answer.write_text('{"decision":"material_change","summary":"x","evidence":[],"people":[]}')
    calls=[]
    def failure(argv,**kwargs):
        calls.append(argv)
        return SimpleNamespace(returncode=1,stdout='',stderr='Rejected: bad evidence')
    monkeypatch.setattr(step.subprocess,'run',failure)
    argv=['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(answer)]
    # Two failures should NOT trigger the repair_budget error (unlike submit)
    assert step.main(argv)==1
    assert step.main(argv)==1
    # A third attempt is also allowed (no SystemExit from repair_budget)
    assert step.main(argv)==1
    assert len(calls)==3
    # None of the attempts should have a repair-note in the attempt metadata
    for folder in (run/'agent-steps').iterdir():
        meta=json.loads((folder/'attempt.json').read_text())
        assert 'repair_note_sha256' not in meta


def test_answer_missing_file_rejected(step,run,monkeypatch):
    """A non-existent answer file must be rejected before command execution."""
    monkeypatch.setattr(step.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):
        step.main(['answer','--run-dir',str(run),'--packet',str(run/'packet.json'),'--answer',str(run/'nonexistent.json')])
