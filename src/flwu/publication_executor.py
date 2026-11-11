"""Explicit, resumable ordinary Git/PR release. No model-authored shell plans."""
from contextlib import contextmanager,ExitStack
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tempfile

from flwu import workflow as w,history as h,workflow_deployment as deployment

NOREPLY='259985078+cadespivey@users.noreply.github.com'


def command(config,args,*,allowed=(0,)):
    env=dict(os.environ,GIT_AUTHOR_EMAIL=NOREPLY,GIT_COMMITTER_EMAIL=NOREPLY,
             GH_PROMPT_DISABLED='1',GIT_TERMINAL_PROMPT='0')
    result=subprocess.run(args,cwd=config['checkout'],capture_output=True,text=True,timeout=120,env=env)
    if result.returncode not in allowed:
        # Preserve exact diagnostics privately without dumping credentials or
        # private identity into the model-facing checkpoint or public files.
        parent=Path(config['run_dir'])/'workflow/release-errors';parent.mkdir(parents=True,exist_ok=True)
        folder=Path(tempfile.mkdtemp(prefix='failed-',dir=parent))
        (folder/'stdout.txt').write_text(result.stdout);(folder/'stderr.txt').write_text(result.stderr)
        (folder/'command.json').write_text(json.dumps(dict(argv=args,exit_code=result.returncode),indent=2)+'\n')
        raise ValueError('Release command failed: '+args[0]+' '+(args[1] if len(args)>1 else '')+
                         ' (exit '+str(result.returncode)+'); exact private diagnostics: '+str(folder))
    return result


def json_command(config,args,*,allowed=(0,)):
    result=command(config,args,allowed=allowed)
    try:return json.loads(result.stdout)
    except ValueError:raise ValueError('Release command returned invalid JSON: '+args[0]) from None


def event(config,body):
    with w.locked(config),h.database(config['database']) as conn:
        if body not in w.events(conn,config):w.record(conn,config,body)


@contextmanager
def locked(config):
    # Different runs/worktrees can share a Git repository. Serialize the entire
    # branch/index/remote operation sequence, not just one run's bookkeeping.
    common=Path(command(config,['git','rev-parse','--git-common-dir']).stdout.strip())
    if not common.is_absolute():common=Path(config['checkout'])/common
    paths=[Path(config['run_dir'])/'workflow/release-executor.lock',common.resolve()/'flwu-publication.lock']
    with ExitStack() as stack:
        for path in paths:
            handle=stack.enter_context(path.open('a+'))
            try:fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise ValueError('A release executor for this run/repository is active; wait for its existing process') from None
        yield


def _pr(config,branch):
    values=json_command(config,['gh','pr','list','--head',branch,'--base','main','--state','all','--json','number,state,url,headRefOid,mergeCommit,baseRefName'])
    if len(values)>1:raise ValueError('Multiple PRs for the recorded release branch; resolve the ambiguity explicitly')
    if values and values[0]['state']=='CLOSED':raise ValueError('Recorded release PR was closed without merge; do not create a duplicate')
    return values[0] if values else None


def _publish_branch(config,plan):
    files=plan['files'];branch=plan['branch']
    with h.database(config['database']) as conn:
        integrated=next(e for e in reversed(w.events(conn,config)) if e['kind']=='publication_integrated' and e['identity']==plan['identity'])
    for item in integrated['files']:
        if h.sha(Path(item['destination']).read_bytes())!=item['sha256']:
            raise ValueError('Release file changed before staging')
    # Implementation/renderer changes need their own reviewed code release; never
    # mix them silently into a data-only commit or deploy with an unreviewed build.
    changed=command(config,['git','status','--porcelain','--untracked-files=all','--','src','pyproject.toml','.github/workflows/pages.yml']).stdout
    if changed.strip():raise ValueError('Commit/release maintained implementation changes separately before the data-only website release')
    staged=command(config,['git','diff','--cached','--name-only','-z']).stdout.split('\0')
    if set(filter(None,staged))-set(files):raise ValueError('Unrelated staged changes are present; preserve them and resolve staging before release')
    current=command(config,['git','branch','--show-current']).stdout.strip()
    if current!=branch:
        exists=command(config,['git','show-ref','--verify','--quiet','refs/heads/'+branch],allowed=(0,1)).returncode==0
        command(config,['git','switch',branch] if exists else ['git','switch','-c',branch,plan['base_commit']])
    # Stage only the pinned bundle. Already committed bytes do not create a new
    # commit; a crash before push can safely execute this same sequence again.
    command(config,['git','add','--',*files])
    command(config,[sys.executable,'scripts/check_public_credentials.py'])
    for item in integrated['files']:
        relative=str(Path(item['destination']).relative_to(Path(config['checkout'])))
        raw=subprocess.run(['git','show',':'+relative],cwd=config['checkout'],capture_output=True,timeout=90)
        if raw.returncode or h.sha(raw.stdout)!=item['sha256']:raise ValueError('Staged release bytes differ from the pinned publication')
    changed=command(config,['git','diff','--cached','--quiet','--',*files],allowed=(0,1)).returncode==1
    if changed:
        email=command(config,['git','config','--get','user.email'],allowed=(0,1)).stdout.strip()
        if email!=NOREPLY:command(config,['git','config','user.email',NOREPLY])
        name=command(config,['git','config','--get','user.name'],allowed=(0,1)).stdout.strip()
        if not name:command(config,['git','config','user.name','Cade Spivey'])
        for variable in ('GIT_AUTHOR_IDENT','GIT_COMMITTER_IDENT'):
            identity=command(config,['git','var',variable]).stdout
            if '<'+NOREPLY+'>' not in identity:raise ValueError('Effective Git identity must use the required no-reply email')
        command(config,['git','commit','--only','-m','Publish reviewed Florida Litigator update','--',*files])
    commit=command(config,['git','rev-parse','HEAD']).stdout.strip()
    # Re-read pinned file bytes before an external mutation; do not push a stale
    # or concurrently edited bundle merely because an earlier build passed.
    for item in integrated['files']:
        if h.sha(Path(item['destination']).read_bytes())!=item['sha256']:raise ValueError('Release file changed before push')
        relative=str(Path(item['destination']).relative_to(Path(config['checkout'])))
        raw=subprocess.run(['git','show',commit+':'+relative],cwd=config['checkout'],capture_output=True,timeout=90)
        if raw.returncode or h.sha(raw.stdout)!=item['sha256']:raise ValueError('Recorded commit does not contain the exact publication bundle')
    command(config,['git','push','-u','origin',branch])
    event(config,dict(kind='release_branch_pushed',identity=plan['identity'],branch=branch,commit=commit))
    return commit


def _once(config,plan,merge):
    pr=_pr(config,plan['branch'])
    if not pr:
        _publish_branch(config,plan)
        # Recover a create that succeeded before its local event was saved.
        pr=_pr(config,plan['branch'])
        if not pr:
            body=Path(config['run_dir'])/'workflow/release-pr-body.txt'
            body.write_text('Publish the approved current Florida Litigator report and directory projections.\n\nValidation: source-bound findings, named membership, exact report/build and publication approval verified by the workflow. No historical reports were re-reviewed.\n')
            command(config,['gh','pr','create','--base','main','--head',plan['branch'],'--title','Publish reviewed Florida Litigator update','--body-file',str(body)])
            pr=_pr(config,plan['branch'])
            if pr is None:raise ValueError('Created release PR could not be located; preserve the branch and inspect the remote before retrying')
    # Existing verifier proves the exact remote bytes before any merge decision.
    state=deployment.verify(config['run_dir'],pr['number'])
    if pr['state']!='MERGED':
        changed=json_command(config,['gh','pr','view',str(pr['number']),'--json','files'])
        if {f['path'] for f in changed['files']}-set(plan['files']):
            raise ValueError('Release PR contains files outside its pinned publication plan')
        checks=json_command(config,['gh','pr','checks',str(pr['number']),'--json','name,bucket,workflow,link'],allowed=(0,1,8))
        if any(c['bucket'] in ('fail','cancel') for c in checks):
            return dict(phase='release_failed',complete=False,publication_performed=False,pr=pr['url'],reason='CI failed or was cancelled; preserve this PR and accepted evidence.')
        pages=[c for c in checks if c.get('workflow')=='GitHub Pages' and c.get('name')=='build']
        if not pages or any(c['bucket']=='pending' for c in checks) or not all(c['bucket']=='pass' for c in pages):
            return dict(phase='awaiting_ci',complete=False,publication_performed=False,pr=pr['url'])
        if not merge:return dict(state,reason='Checks passed; merge requires the explicit --merge execution option under publication authorization.')
        command(config,['gh','pr','merge',str(pr['number']),'--squash','--match-head-commit',pr['headRefOid'],'--author-email',NOREPLY])
        # A merge queue may defer actual merge. Never infer MERGED from exit 0.
        pr=_pr(config,plan['branch'])
        if pr is None or pr['state']!='MERGED':return dict(phase='awaiting_merge',complete=False,publication_performed=False,pr=pr['url'] if pr else None)
        state=deployment.verify(config['run_dir'],pr['number'])
    commit=pr['mergeCommit']['oid']
    runs=json_command(config,['gh','run','list','--branch','main','--commit',commit,'--workflow','pages.yml','--limit','20','--json','databaseId,status,conclusion,headSha,event,url'])
    if not runs:return dict(state,reason='No Pages deployment is visible for the exact merged commit yet.')
    applicable=[r for r in runs if r['headSha']==commit and r['event'] in ('push','workflow_dispatch')]
    # Newest attempt governs. A stale success must not hide a failed rerun.
    if not applicable:return dict(state,reason='No matching main deployment attempt yet.')
    run=applicable[0]
    if run['status']!='completed':return dict(state,reason='The exact main deployment is still running.')
    if run['conclusion']!='success':return dict(phase='release_failed',complete=False,publication_performed=False,pr=pr['url'],reason='Pages deployment failed; do not restart research or create another release.')
    try:return deployment.verify(config['run_dir'],pr['number'],run['databaseId'])
    except ValueError as exc:
        if str(exc).startswith('Live current publication'):
            return dict(phase='awaiting_live_verification',complete=False,publication_performed=False,pr=pr['url'],reason=str(exc))
        raise


def execute(run_dir,*,perform=False,merge=False,wait=False,timeout=1800):
    config=w.load(run_dir)
    if config['mode']!='publish':raise ValueError('Release execution requires an approved publish-mode workflow')
    if not perform:return deployment.plan(run_dir)
    if not isinstance(timeout,int) or not 1<=timeout<=7200:raise ValueError('Release wait timeout must be 1–7200 seconds')
    from flwu.publication_driver import advance
    state=advance(run_dir)
    if state['phase']=='publication_complete':return state
    if state['phase'] not in ('release_required','merge_required','deployment_verification'):
        raise ValueError('Complete substantive publication approval and integration before executing release')
    with locked(config):
        plan=deployment.plan(run_dir);deadline=time.monotonic()+timeout
        event(config,dict(kind='release_execution_authorized',identity=plan['identity'],merge=merge))
        while True:
            try:result=_once(config,plan,merge)
            except (ValueError,OSError,subprocess.SubprocessError) as exc:
                result=dict(phase='release_failed',complete=False,publication_performed=False,reason=str(exc))
            if wait and not result['complete'] and result['phase'] not in ('release_failed','merge_required') and time.monotonic()>=deadline:
                result=dict(result,wait_expired=True,next_instruction='Resume the same workflow release command only after the reported condition changes; do not create a new run.')
            event(config,dict(kind='release_execution_checkpoint',identity=plan['identity'],result=result))
            if not wait or result['complete'] or result['phase'] in ('release_failed','merge_required') or result.get('wait_expired'):return result
            print(json.dumps(dict(status='release_wait',phase=result['phase'],pr=result.get('pr'))),file=sys.stderr,flush=True)
            time.sleep(min(30,max(0,deadline-time.monotonic())))
