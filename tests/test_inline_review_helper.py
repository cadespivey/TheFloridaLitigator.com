"""Checked stdin transport, independent of the coordinator's semantic tests."""
import importlib.util
import io
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def helper():
    path=Path(__file__).parents[1]/'skills/florida-update/scripts/review_step.py'
    spec=importlib.util.spec_from_file_location('inline_checked_helper',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def state():
    return dict(phase='source_review',complete=False,review_mode='inline_answer',
                task_handle='a'*24,command='/run/review '+'a'*24,
                review_card={'question':'Review acquired text','evidence':[{'id':'C1','passage':'Exact\u00a0text'}],'answer':{}},
                review_progress={'saved_review_decisions':1})


def test_stdin_saved_exactly_before_execution_and_next_inline_card_returned(helper,tmp_path,monkeypatch,capsys):
    raw=b'{"summary":"Exact\xc2\xa0text\\nsecond line","people":[]}\n'
    monkeypatch.setattr(helper.sys,'stdin',io.TextIOWrapper(io.BytesIO(raw),encoding='utf-8'))
    nxt=state();calls=[]
    def execute(argv,**kwargs):
        calls.append(argv)
        answer=Path(argv[argv.index('--answer')+1])
        assert answer.read_bytes()==raw  # Input exists before any accepting subprocess.
        assert answer.parent.parent==tmp_path/'agent-steps'
        assert 'reply' in argv and '--task' in argv and '--packet' not in argv
        assert '--advance' not in argv  # Reply always advances through its own coordinator path.
        return SimpleNamespace(returncode=0,stdout=json.dumps(nxt),stderr='')
    monkeypatch.setattr(helper.subprocess,'run',execute)
    assert helper.main(['reply','--run-dir',str(tmp_path),'--task','b'*24])==0
    assert len(calls)==1
    assert json.loads(capsys.readouterr().out)==nxt
    assert json.loads((tmp_path/'agent-next-task.json').read_text())==nxt
    attempt=next((tmp_path/'agent-steps').iterdir())
    meta=json.loads((attempt/'attempt.json').read_text())
    import hashlib
    assert meta['answer_sha256']==hashlib.sha256(raw).hexdigest()
    assert meta['task_handle']=='b'*24 and meta['exit_code']==0
    assert json.loads((attempt/'answer.stdout').read_text())==nxt


@pytest.mark.parametrize('output',['not json','{}','{"phase":"source_review","complete":"false"}'])
def test_invalid_reply_result_preserves_pointer_and_input(helper,tmp_path,monkeypatch,output):
    pointer=tmp_path/'agent-next-task.json';pointer.write_text('{"old":true}')
    monkeypatch.setattr(helper.sys,'stdin',io.StringIO('{"summary":"preserve"}'))
    monkeypatch.setattr(helper.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0,stdout=output,stderr=''))
    assert helper.main(['reply','--run-dir',str(tmp_path),'--task','b'*24])==1
    assert pointer.read_text()=='{"old":true}'
    assert next((tmp_path/'agent-steps').glob('*/answer.json')).read_bytes()==b'{"summary":"preserve"}'


def test_failed_reply_retains_exact_error_and_previous_pointer(helper,tmp_path,monkeypatch):
    pointer=tmp_path/'agent-next-task.json';pointer.write_text('{"old":true}')
    monkeypatch.setattr(helper.sys,'stdin',io.StringIO('{"summary":"preserve"}'))
    monkeypatch.setattr(helper.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=3,stdout='',stderr='Stale task snapshot'))
    assert helper.main(['reply','--run-dir',str(tmp_path),'--task','b'*24])==3
    assert pointer.read_text()=='{"old":true}'
    assert next((tmp_path/'agent-steps').glob('*/answer.stderr')).read_text()=='Stale task snapshot'


@pytest.mark.parametrize('extra',[['--packet','packet.json'],['--answer','answer.json'],['--receipt','receipt.json']])
def test_reply_refuses_model_written_paths(helper,tmp_path,monkeypatch,extra):
    monkeypatch.setattr(helper.subprocess,'run',lambda *a,**k:pytest.fail('Must not execute'))
    with pytest.raises(SystemExit):
        helper.main(['reply','--run-dir',str(tmp_path),'--task','b'*24,*extra])


def test_next_requests_model_view_without_an_extra_command(helper,tmp_path,monkeypatch,capsys):
    calls=[];nxt=state()
    def execute(argv,**kwargs):
        calls.append(argv);return SimpleNamespace(returncode=0,stdout=json.dumps(nxt),stderr='')
    monkeypatch.setattr(helper.subprocess,'run',execute)
    assert helper.main(['next','--run-dir',str(tmp_path)])==0
    assert len(calls)==1 and 'model-next' in calls[0]
    assert json.loads(capsys.readouterr().out)==nxt


def test_pointer_write_interruption_keeps_saved_answer_for_exact_replay(helper,tmp_path,monkeypatch):
    pointer=tmp_path/'agent-next-task.json';pointer.write_text('{"old":true}')
    monkeypatch.setattr(helper.sys,'stdin',io.StringIO('{"summary":"accepted before pointer"}'))
    calls=[]
    def execute(argv,**kwargs):
        calls.append(argv);return SimpleNamespace(returncode=0,stdout=json.dumps(state()),stderr='')
    monkeypatch.setattr(helper.subprocess,'run',execute)
    def interrupted(*args):raise OSError('Simulated interrupted pointer replacement')
    monkeypatch.setattr(helper.os,'replace',interrupted)
    assert helper.main(['reply','--run-dir',str(tmp_path),'--task','b'*24])==1
    assert len(calls)==1 and pointer.read_text()=='{"old":true}'
    assert next((tmp_path/'agent-steps').glob('*/answer.json')).read_text()=='{"summary":"accepted before pointer"}'
    assert not list(tmp_path.glob('.next-*'))


def test_semantic_rejection_returns_exact_error_complete_card_and_counts(helper,tmp_path,monkeypatch,capsys):
    nxt=state();nxt['answer_failure']={'error':'New Clerk fields.office_address is unsupported','attempt':1}
    nxt['review_progress']['failed_short_answers']=1
    monkeypatch.setattr(helper.sys,'stdin',io.StringIO('{"summary":"bad address"}'))
    monkeypatch.setattr(helper.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0,stdout=json.dumps(nxt),stderr=''))
    assert helper.main(['reply','--run-dir',str(tmp_path),'--task','b'*24])==0
    actual=json.loads(capsys.readouterr().out)
    assert actual==nxt
    assert actual['review_card']['evidence'][0]['passage']=='Exact\u00a0text'


def test_incomplete_inline_card_cannot_replace_pointer(helper,tmp_path,monkeypatch):
    pointer=tmp_path/'agent-next-task.json';pointer.write_text('{"old":true}')
    broken=state();del broken['review_card']['evidence']
    monkeypatch.setattr(helper.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0,stdout=json.dumps(broken),stderr=''))
    assert helper.main(['next','--run-dir',str(tmp_path)])==1
    assert pointer.read_text()=='{"old":true}'
