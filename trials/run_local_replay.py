"""Run five independent local Codex contexts, preserving exact prompts and events."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from datetime import datetime, timezone


def run(root):
    root=root.resolve()
    plan=json.loads((root/'plan.json').read_text())
    if plan['provider']!='http://127.0.0.1:8000/v1':raise ValueError('Only the pinned local provider is permitted')
    work=root/'workspace'
    args=['codex','--no-daemon','exec','--ignore-user-config','-m',plan['model'],
          '-c','model_provider="trial_omlx"',
          '-c','model_providers.trial_omlx.name="Local oMLX trial"',
          '-c','model_providers.trial_omlx.base_url="http://127.0.0.1:8000/v1"',
          '-c','model_providers.trial_omlx.wire_api="responses"',
          '-c','model_providers.trial_omlx.requires_openai_auth=false',
          '-c','model_catalog_json="/Users/cadespivey/.codex/omlx-models.json"',
          '-c','model_reasoning_effort="none"','-c','model_reasoning_summary="none"',
          '-c','approval_policy="never"','--ephemeral','--sandbox','workspace-write',
          '--skip-git-repo-check','-C',str(work),'--json']
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    # Credential variables are unnecessary for the keyless loopback server.
    for key in list(env):
        if any(word in key.upper() for word in ('API_KEY','TOKEN','SECRET','PASSWORD')):env.pop(key)
    (root/'invocation.json').write_text(json.dumps({'argv':args,'environment':'inherited except secret-like variables; PYTHONDONTWRITEBYTECODE=1','native_auto_compaction':False},indent=2))
    summaries=[]
    for phase in range(1,6):
        if phase==5:
            (work/'state/control.json').write_text(json.dumps({'restored':True}))
            (root/'restoration-event.json').write_text(json.dumps({'at':datetime.now(timezone.utc).isoformat(),'restored':['circuits/orders','procedures/casey-morgan']},indent=2))
        started=time.time()
        print(f'Starting phase {phase}',flush=True)
        with (root/f'phase-{phase}.events.jsonl').open('x') as out, (root/f'phase-{phase}.stderr.txt').open('x') as err, (root/f'phase-{phase}.prompt.txt').open() as prompt:
            result=subprocess.run(args+['-o',str(root/f'phase-{phase}.final.txt'),'-'],stdin=prompt,stdout=out,stderr=err,env=env,timeout=3600)
        snapshot=root/f'phase-{phase}-artifacts'
        snapshot.mkdir()
        for p in (work/'work').rglob('*'):
            if p.is_file() and p.suffix in ('.json','.jsonl','.html','.txt'):
                target=snapshot/p.relative_to(work/'work')
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(p,target)
        counts={'input_tokens':0,'cached_input_tokens':0,'output_tokens':0,'reasoning_output_tokens':0}
        tool_calls=0
        for line in (root/f'phase-{phase}.events.jsonl').read_text().splitlines():
            try:event=json.loads(line)
            except json.JSONDecodeError:continue
            if event.get('type')=='turn.completed':
                for key in counts:counts[key]+=event.get('usage',{}).get(key,0)
            if event.get('type')=='item.completed' and event.get('item',{}).get('type')=='command_execution':tool_calls+=1
        summary={'phase':phase,'exit_code':result.returncode,'seconds':round(time.time()-started,2),'usage':counts,'tool_calls':tool_calls,
                 'handoff_sha256':hashlib.sha256((work/'work/HANDOFF.json').read_bytes()).hexdigest() if (work/'work/HANDOFF.json').exists() else None}
        summaries.append(summary)
        (root/'execution.json').write_text(json.dumps(summaries,indent=2))
        print(json.dumps(summary),flush=True)
        if result.returncode:
            print('Runtime failed; retaining evidence and stopping dependent phases.',flush=True)
            return result.returncode
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path)
    raise SystemExit(run(p.parse_args().root))
