"""Real disposable Git plus fake GitHub boundaries; no production release."""
import copy
from pathlib import Path
import shutil
import subprocess
import os
from types import SimpleNamespace
import pytest
from flwu import history as h
from flwu import publication_executor as executor


@pytest.fixture
def git_release(tmp_path,monkeypatch):
    root=tmp_path/'repo';root.mkdir();remote=tmp_path/'remote.git'
    env=dict(os.environ,GIT_AUTHOR_EMAIL=executor.NOREPLY,GIT_COMMITTER_EMAIL=executor.NOREPLY)
    def git(*args):
        result=subprocess.run(['git',*args],cwd=root,capture_output=True,text=True,env=env)
        assert result.returncode==0,result.stderr
        return result.stdout.strip()
    git('init','-b','main');git('config','user.name','Fixture Creator');git('config','user.email',executor.NOREPLY)
    (root/'scripts').mkdir();shutil.copy2(Path(__file__).resolve().parents[1]/'scripts/check_public_credentials.py',root/'scripts/check_public_credentials.py')
    (root/'website').mkdir();target=root/'website/current.json';target.write_text('old public data\n')
    unrelated=root/'unrelated.txt';unrelated.write_text('original unrelated work\n');git('add','.');git('commit','-m','Initial fixture')
    subprocess.run(['git','init','--bare',str(remote)],check=True,capture_output=True)
    git('remote','add','origin',str(remote));base=git('rev-parse','HEAD')
    target.write_text('new reviewed public data\n');unrelated.write_text('preserve unrelated unstaged edits\n')
    db=tmp_path/'db.sqlite'
    with h.database(db):pass
    config=dict(checkout=str(root),database=str(db),run_dir=str(tmp_path/'run'),mode='publish')
    (Path(config['run_dir'])/'workflow').mkdir(parents=True)
    plan=dict(identity='fixture-release',branch='publish/flwu-fixture',base_commit=base,files=['website/current.json'])
    integrated=dict(kind='publication_integrated',identity=plan['identity'],files=[dict(destination=str(target),sha256=h.sha(target.read_bytes()))])
    events=[]
    monkeypatch.setattr(executor.w,'events',lambda conn,cfg:[integrated])
    monkeypatch.setattr(executor,'event',lambda cfg,e:events.append(e))
    return config,plan,git,target,unrelated,events


def test_real_git_only_commits_reviewed_files_and_resumes_push_without_new_commit(git_release):
    config,plan,git,target,unrelated,events=git_release
    first=executor._publish_branch(config,plan)
    assert git('show','HEAD:website/current.json')=='new reviewed public data'
    assert git('show','HEAD:unrelated.txt')=='original unrelated work'
    assert unrelated.read_text()=='preserve unrelated unstaged edits\n'
    assert git('show','-s','--format=%ae|%ce')==executor.NOREPLY+'|'+executor.NOREPLY
    count=git('rev-list','--count','HEAD')
    second=executor._publish_branch(config,plan)
    assert second==first and git('rev-list','--count','HEAD')==count
    assert all(e['kind']=='release_branch_pushed' for e in events)
    assert git('diff','--name-only')=='unrelated.txt'


def test_unrelated_staged_work_is_not_reset_or_committed(git_release):
    config,plan,git,target,unrelated,_=git_release
    git('add','unrelated.txt')
    before=git('rev-parse','HEAD')
    with pytest.raises(ValueError,match='Unrelated staged'):executor._publish_branch(config,plan)
    assert git('rev-parse','HEAD')==before
    assert git('diff','--cached','--name-only')=='unrelated.txt'
    assert unrelated.read_text()=='preserve unrelated unstaged edits\n'


def test_changed_bundle_refused_before_git_mutation(git_release):
    config,plan,git,target,_,_=git_release
    before=git('rev-parse','HEAD');target.write_text('concurrent edit')
    with pytest.raises(ValueError,match='before staging'):executor._publish_branch(config,plan)
    assert git('branch','--show-current')=='main' and git('rev-parse','HEAD')==before
    assert target.read_text()=='concurrent edit'


def fake_remote(monkeypatch,*,checks=None,merged=False,run_status='completed',run_conclusion='success'):
    config=dict(run_dir='fixture-run');plan=dict(branch='publish/flwu-fixture',files=['website/current.json'])
    pr=dict(number=7,state='MERGED' if merged else 'OPEN',url='https://github.com/example/repo/pull/7',headRefOid='a'*40,mergeCommit={'oid':'b'*40} if merged else None)
    calls=[]
    monkeypatch.setattr(executor,'_pr',lambda c,b:copy.deepcopy(pr))
    monkeypatch.setattr(executor,'_publish_branch',lambda *a:pytest.fail('Existing PR must not push or create a new commit'))
    def execute(c,args,**kwargs):
        calls.append(args)
        if args[:3]==['gh','pr','merge']:pr.update(state='MERGED',mergeCommit={'oid':'b'*40})
        return SimpleNamespace(returncode=0,stdout='')
    monkeypatch.setattr(executor,'command',execute)
    def json_call(c,args,**kwargs):
        calls.append(args)
        if args[:3]==['gh','pr','view']:return {'files':[{'path':'website/current.json'}]}
        if args[:3]==['gh','pr','checks']:
            return checks if checks is not None else [dict(name='build',workflow='GitHub Pages',bucket='pass'),dict(name='deploy',workflow='GitHub Pages',bucket='skipping')]
        if args[:3]==['gh','run','list']:
            return [dict(databaseId=13,status=run_status,conclusion=run_conclusion,headSha='b'*40,event='push',url='https://github.com/example/repo/actions/runs/13')]
        raise AssertionError(args)
    monkeypatch.setattr(executor,'json_command',json_call)
    def verify(run,number,run_id=None):
        calls.append(['verify',number,run_id])
        return dict(phase='publication_complete' if run_id else 'deployment_verification' if pr['state']=='MERGED' else 'merge_required',complete=bool(run_id),publication_performed=bool(run_id),pr=pr['url'])
    monkeypatch.setattr(executor.deployment,'verify',verify)
    return config,plan,calls


def test_ci_gate_allows_intentionally_skipped_pr_deploy_but_requires_successful_build(monkeypatch):
    config,plan,calls=fake_remote(monkeypatch)
    done=executor._once(config,plan,True)
    assert done['phase']=='publication_complete'
    merge=next(c for c in calls if c[:3]==['gh','pr','merge'])
    assert '--match-head-commit' in merge and '--author-email' in merge
    assert '--admin' not in merge and '--auto' not in merge
    assert ['verify',7,13] in calls


@pytest.mark.parametrize('bucket,phase',[('pending','awaiting_ci'),('fail','release_failed'),('cancel','release_failed')])
def test_unfinished_or_failed_ci_never_merges(monkeypatch,bucket,phase):
    config,plan,calls=fake_remote(monkeypatch,checks=[dict(name='build',workflow='GitHub Pages',bucket=bucket)])
    assert executor._once(config,plan,True)['phase']==phase
    assert not any(c[:3]==['gh','pr','merge'] for c in calls)


def test_merge_option_is_required_and_failed_deployment_is_not_success(monkeypatch):
    config,plan,calls=fake_remote(monkeypatch)
    assert executor._once(config,plan,False)['phase']=='merge_required'
    assert not any(c[:3]==['gh','pr','merge'] for c in calls)
    config,plan,calls=fake_remote(monkeypatch,merged=True,run_conclusion='failure')
    result=executor._once(config,plan,True)
    assert result['phase']=='release_failed' and not result['publication_performed']
    assert not any(c[:3]==['gh','pr','merge'] for c in calls)


def test_wait_loop_is_code_owned_bounded_and_resumable(tmp_path,monkeypatch):
    run=tmp_path/'run';(run/'workflow').mkdir(parents=True)
    common=tmp_path/'git-common';common.mkdir()
    config=dict(run_dir=str(run),mode='publish',checkout=str(tmp_path))
    monkeypatch.setattr(executor,'command',lambda *a,**k:SimpleNamespace(stdout=str(common),returncode=0))
    monkeypatch.setattr(executor.w,'load',lambda _:config)
    from flwu import publication_driver
    monkeypatch.setattr(publication_driver,'advance',lambda _:dict(phase='release_required',complete=False))
    monkeypatch.setattr(executor.deployment,'plan',lambda _:dict(identity='fixture'))
    events=[];monkeypatch.setattr(executor,'event',lambda c,e:events.append(e))
    clock=[0];monkeypatch.setattr(executor.time,'monotonic',lambda:clock[0]);monkeypatch.setattr(executor.time,'sleep',lambda sec:clock.__setitem__(0,clock[0]+sec))
    monkeypatch.setattr(executor,'_once',lambda *a:dict(phase='awaiting_ci',complete=False,publication_performed=False))
    result=executor.execute(run,perform=True,merge=True,wait=True,timeout=31)
    assert result['wait_expired'] and clock[0]==31
    assert any(e['kind']=='release_execution_checkpoint' for e in events)
    assert not result['publication_performed']
    monkeypatch.setattr(executor,'_once',lambda *a:dict(phase='publication_complete',complete=True,publication_performed=True))
    assert executor.execute(run,perform=True,merge=True,wait=True)['complete']


def test_repository_lock_serializes_distinct_runs_in_same_git_repository(git_release,tmp_path):
    config,_,_,_,_,_=git_release
    other=dict(config,run_dir=str(tmp_path/'another-run'));(Path(other['run_dir'])/'workflow').mkdir(parents=True)
    with executor.locked(config):
        with pytest.raises(ValueError,match='run/repository is active'):
            with executor.locked(other):pytest.fail('Concurrent releases must not enter')
    with executor.locked(other):pass


def test_failed_command_keeps_private_exact_diagnostics_out_of_checkpoint(tmp_path,monkeypatch):
    config=dict(checkout=str(tmp_path),run_dir=str(tmp_path/'run'))
    marker='private diagnostic fixture, do not put this in the checkpoint'
    monkeypatch.setattr(executor.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=1,stdout='',stderr=marker))
    with pytest.raises(ValueError) as caught:executor.command(config,['gh','pr','create'])
    assert marker not in str(caught.value)
    logs=list((Path(config['run_dir'])/'workflow/release-errors').glob('*/stderr.txt'))
    assert len(logs)==1 and logs[0].read_text()==marker
