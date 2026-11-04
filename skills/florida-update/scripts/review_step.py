#!/usr/bin/env python3
"""Run one review step with checked exit status, full logs and atomic next state."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def within(path,run):
    path=Path(path).expanduser().resolve()
    if not path.is_relative_to(run):raise ValueError('Step paths must stay inside the run directory')
    return path


def execute(argv,folder,name):
    result=subprocess.run(argv,capture_output=True,text=True)
    (folder/(name+'.stdout')).write_text(result.stdout)
    (folder/(name+'.stderr')).write_text(result.stderr)
    (folder/(name+'.json')).write_text(json.dumps(dict(argv=argv,exit_code=result.returncode),indent=2)+'\n')
    if result.returncode:
        print(result.stderr or result.stdout,file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode,argv)
    return result.stdout


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout',type=Path)
    parser.add_argument('action',choices=['next','submit'])
    parser.add_argument('--run-dir',required=True,type=Path)
    parser.add_argument('--packet',type=Path)
    parser.add_argument('--receipt',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    run=args.run_dir.expanduser().resolve()
    if not run.is_dir():parser.error('Run directory must already exist')
    try:
        output=within(args.output or run/'agent-next-task.json',run)
        if output.parent!=run or output.name not in ('agent-next-task.json','last-next-task.json'):
            parser.error('Output must be agent-next-task.json or last-next-task.json at the run root')
        if args.action=='submit':
            if not args.packet or not args.receipt:parser.error('submit requires --packet and --receipt')
            packet=within(args.packet,run);receipt=within(args.receipt,run)
            if not packet.is_file() or not receipt.is_file():parser.error('Packet and receipt must exist')
            if output in (packet,receipt):parser.error('Next state cannot overwrite a packet or receipt')
        logs=within(run/'agent-steps',run);logs.mkdir(exist_ok=True)
        folder=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S-'),dir=logs))
    except (ValueError,OSError) as exc:parser.error(str(exc))
    launcher=[sys.executable,str(Path(__file__).with_name('flwu.py'))]
    if args.checkout:launcher+=['--checkout',str(args.checkout.expanduser().resolve())]
    try:
        if args.action=='submit':
            execute(launcher+['workflow','submit','--run-dir',str(run),'--packet',str(packet),'--receipt',str(receipt)],folder,'submit')
        raw=execute(launcher+['workflow','next-task','--run-dir',str(run)],folder,'next')
        state=json.loads(raw)
        if not isinstance(state,dict) or 'phase' not in state or type(state.get('complete')) is not bool:
            raise ValueError('Next-task returned an invalid state; previous pointer preserved')
        output.parent.mkdir(parents=True,exist_ok=True)
        fd,temporary=tempfile.mkstemp(prefix='.next-',dir=output.parent)
        try:
            with os.fdopen(fd,'w') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            os.replace(temporary,output)
        finally:
            if os.path.exists(temporary):os.unlink(temporary)
        print(json.dumps(dict(state,next_state=str(output),logs=str(folder)),indent=2))
        return 0
    except subprocess.CalledProcessError as exc:
        print('Step failed; previous next-state pointer preserved. Logs: '+str(folder),file=sys.stderr)
        return exc.returncode
    except (ValueError,OSError) as exc:
        print(str(exc)+'; previous next-state pointer preserved. Logs: '+str(folder),file=sys.stderr)
        return 1


if __name__=='__main__':raise SystemExit(main())
