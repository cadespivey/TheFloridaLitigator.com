"""Observed GitHub release and live current-data checkpoints."""
from __future__ import annotations
import base64
import json
from pathlib import Path
import re
import subprocess
import shlex
import urllib.request
from flwu import workflow as w, history as h


def github(config,*args):
    result=subprocess.run(['gh',*args],cwd=config['checkout'],capture_output=True,text=True,timeout=90)
    if result.returncode:raise ValueError('GitHub verification failed: '+result.stderr.strip())
    return json.loads(result.stdout)


def fetch_json(url):
    request=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'FloridaLitigator-publication-verification'})
    with urllib.request.urlopen(request,timeout=45) as response:
        raw=response.read(32*1024*1024+1)
    if len(raw)>32*1024*1024:raise ValueError('Live publication response exceeds verification limit')
    return json.loads(raw)


def plan(run_dir):
    """Persist a release branch and exact file list before external Git steps."""
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        integrated=next((e for e in reversed(w.events(conn,config)) if e['kind']=='publication_integrated'),None)
        if not integrated:raise ValueError('Integrate the publication before preparing its Git release')
        saved=next((e for e in reversed(w.events(conn,config)) if e['kind']=='git_release_plan' and e['identity']==integrated['identity']),None)
        if saved:return saved
        root=Path(config['checkout']);paths=[]
        for item in integrated['files']:
            path=Path(item['destination']).resolve()
            if h.sha(path.read_bytes())!=item['sha256']:raise ValueError('Integrated publication file changed')
            try:paths.append(str(path.relative_to(root)))
            except ValueError:raise ValueError('Publication files must reside in the selected release checkout') from None
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
        branch='publish/flwu-'+integrated['identity'][:16]
        event=dict(kind='git_release_plan',identity=integrated['identity'],checkout=str(root),base_commit=head,
                   branch=branch,files=paths,
                   commands=[shlex.join(['git','switch','-c',branch]),shlex.join(['git','add','--',*paths]),
                             shlex.join([__import__('sys').executable,'scripts/check_public_credentials.py']),
                             shlex.join(['git','commit','--only','-m','Publish reviewed Florida Litigator update','--',*paths]),
                             shlex.join(['git','push','-u','origin',branch]),
                             shlex.join(['gh','pr','list','--head',branch,'--state','all','--json','number,url,state'])],
                   recovery='On retry inspect the recorded branch, Git status/log and remote PR before repeating a mutation. Reuse an existing branch, commit or PR; never reset unrelated edits. After PR creation run workflow verify-deployment --pr NUMBER. Merge only under existing release authorization.')
        w.record(conn,config,event)
        return event


def verify(run_dir,pr_number,run_id=None):
    if not isinstance(pr_number,int) or pr_number<=0:raise ValueError('A positive --pr number is required')
    from flwu.workflow_release import export
    export(run_dir)
    config=w.load(run_dir)
    if config['mode']!='publish':raise ValueError('Deployment verification requires publish mode')
    with w.locked(config),h.database(config['database']) as conn:
        integrated=next((e for e in reversed(w.events(conn,config)) if e['kind']=='publication_integrated'),None)
        if integrated is None:raise ValueError('Integrate the accepted publication bundle first')
        repo=github(config,'repo','view','--json','nameWithOwner')['nameWithOwner']
        pr=github(config,'pr','view',str(pr_number),'--json','number,state,url,headRefOid,mergeCommit,baseRefName')
        if pr['baseRefName']!='main':raise ValueError('Release PR must target main')
        commit=pr['mergeCommit']['oid'] if pr.get('mergeCommit') else pr['headRefOid']
        for item in integrated['files']:
            path=Path(item['destination']).resolve()
            try:relative=str(path.relative_to(Path(config['checkout']).resolve()))
            except ValueError:raise ValueError('Integrated publication destination is outside the release checkout') from None
            data=github(config,'api',f'repos/{repo}/contents/{relative}?ref={commit}')
            if data.get('encoding')!='base64' or h.sha(base64.b64decode(data['content']))!=item['sha256']:
                raise ValueError('Release commit does not contain the exact integrated publication files')
        observation=dict(kind='release_observed',identity=integrated['identity'],repository=repo,
                         pr=pr_number,url=pr['url'],state=pr['state'],commit=commit)
        w.record(conn,config,observation)
        if pr['state']!='MERGED':
            return dict(phase='merge_required',complete=False,publication_performed=False,pr=pr['url'])
        if run_id is None:
            return dict(phase='deployment_verification',complete=False,publication_performed=False,
                        next_instruction='Supply the successful main GitHub Pages workflow run using --deployment-run.')
        run=github(config,'run','view',str(run_id),'--json','databaseId,headSha,headBranch,event,status,conclusion,workflowName,url,jobs')
        if (run['headSha']!=commit or run['headBranch']!='main' or run['workflowName']!='GitHub Pages'
            or run['event'] not in ('push','workflow_dispatch') or run['status']!='completed'
            or run['conclusion']!='success' or not any(j['name']=='deploy' and j['conclusion']=='success' for j in run['jobs'])):
            raise ValueError('Expected a successful GitHub Pages deployment of the exact merged release commit')
        origin='https://thefloridalitigator.com/'
        pointer=fetch_json(origin+'assets/current-archive.json')
        name=pointer.get('archive','')
        if not re.fullmatch(r'archive-[0-9a-f]{16}\.json',name):raise ValueError('Invalid live archive pointer')
        live=fetch_json(origin+'assets/'+name)
        if live.get('preview') is not False:raise ValueError('Live site is not a production archive')
        for item in integrated['files']:
            expected=w.read(item['source'])
            if 'sections' in expected:
                matches=[v for v in live.get('issues',[]) if v.get('id')==expected['id']]
            else:
                matches=[v for v in live.get('county_directories',[]) if
                         (v.get('county'),v.get('court_scope'))==(expected.get('county'),expected.get('court_scope'))]
            if len(matches)!=1 or matches[0]!=expected:raise ValueError('Live current publication data does not match the released bundle')
        event=dict(kind='deployment_verified',identity=integrated['identity'],repository=repo,pr=pr_number,
                   commit=commit,run_id=run_id,run_url=run['url'],site=origin,archive=name,
                   live_data_sha256=h.sha(live),verified_at=h.now())
        w.record(conn,config,event)
        return dict(phase='publication_complete',complete=True,publication_performed=True,**{k:event[k] for k in ('commit','run_url','site')})
