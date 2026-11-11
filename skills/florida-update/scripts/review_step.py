#!/usr/bin/env python3
"""Run one review step with checked exit status, full logs and atomic next state."""
import argparse
from datetime import datetime, timezone
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def repair_budget(run, packet, action, note):
    """Count consecutive failed validations, not failed advancement after commit."""
    failed=[]
    for folder in sorted((run/'agent-steps').glob('*')):
        meta=folder/(action+'.json')
        if not meta.is_file():continue
        saved=json.loads(meta.read_text());argv=saved.get('argv',[])
        if '--packet' not in argv or str(packet)!=argv[argv.index('--packet')+1]:continue
        if saved['exit_code']==0:failed=[];continue
        stderr=(folder/(action+'.stderr')).read_text()
        if 'submission is saved' in stderr:continue
        if (folder/'attempt.json').is_file() and json.loads((folder/'attempt.json').read_text()).get('repair_note_sha256'):
            failed=[]
        failed.append(folder.name)
    if len(failed)<2:return None
    if not note:raise ValueError('Two draft validations failed for this packet. Preserve evidence and provide --repair-note JSON with packet_sha256, failed_attempts, change_in_approach and evidence_paths; do not vary wording to bypass validation.')
    path=within(note,run);value=json.loads(path.read_text());body=json.loads(packet.read_text())
    identity=body.get('packet_sha256') or hashlib.sha256(packet.read_bytes()).hexdigest()
    if (set(value)!={'packet_sha256','failed_attempts','change_in_approach','evidence_paths'}
            or value['packet_sha256']!=identity or value['failed_attempts']!=failed[-2:]
            or not isinstance(value['change_in_approach'],str) or not value['change_in_approach'].strip()
            or not isinstance(value['evidence_paths'],list) or not value['evidence_paths']
            or any(not within(p,run).is_file() for p in value['evidence_paths'])):
        raise ValueError('Repair note must bind this packet, the last two failed attempts, a changed approach and existing acquired evidence paths')
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def save_bytes(path, raw):
    """Durably save model input before invoking any accepting coordinator action."""
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout',type=Path)
    parser.add_argument('--python',type=Path,help='Explicit launcher interpreter override for development/CI')
    parser.add_argument('action',choices=['next','reply','retry','submit','revise','answer'])
    parser.add_argument('--run-dir',required=True,type=Path)
    parser.add_argument('--packet',type=Path)
    parser.add_argument('--receipt',type=Path)
    parser.add_argument('--answer',type=Path)
    parser.add_argument('--task',help='Code-issued handle for reply; the JSON answer is read from stdin.')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--predecessor')
    parser.add_argument('--reason')
    parser.add_argument('--repair-note',type=Path,help='Evidence-bound checkpoint after two failed draft validations')
    args=parser.parse_args(argv)
    run=args.run_dir.expanduser().resolve()
    if not run.is_dir():parser.error('Run directory must already exist')
    try:
        output=within(args.output or run/'agent-next-task.json',run)
        if output.parent!=run or output.name not in ('agent-next-task.json','last-next-task.json'):
            parser.error('Output must be agent-next-task.json or last-next-task.json at the run root')
        if args.action in ('submit','revise'):
            if not args.packet or not args.receipt:parser.error('submit/revise requires --packet and --receipt')
            if args.action=='revise' and (not args.predecessor or not args.reason or not args.reason.strip()):
                parser.error('revise requires the returned --predecessor and --reason')
            packet=within(args.packet,run);receipt=within(args.receipt,run)
            if not packet.is_file() or not receipt.is_file():parser.error('Packet and receipt must exist')
            if output in (packet,receipt):parser.error('Next state cannot overwrite a packet or receipt')
            repair_digest=repair_budget(run,packet,args.action,args.repair_note)
        elif args.action=='answer':
            if not args.packet or not args.answer:parser.error('answer requires --packet and --answer')
            packet=within(args.packet,run);answer=within(args.answer,run)
            if not packet.is_file() or not answer.is_file():parser.error('Packet and answer must exist')
            if output in (packet,answer):parser.error('Next state cannot overwrite a packet or answer')
            # Do not run repair_budget for answer; the coordinator owns answer_rejected
            # records and the automatic unresolved checkpoint after two validations.
        elif args.action=='reply':
            if not args.task:parser.error('reply requires --task and a JSON answer on stdin')
            if args.packet or args.answer or args.receipt:
                parser.error('reply uses the issued task handle and stdin, not model-written file paths')
        elif args.action=='retry':
            if not args.packet:parser.error('retry requires the returned current --packet checkpoint')
            packet=within(args.packet,run)
            if not packet.is_file():parser.error('Preserved publication packet must exist')
        logs=within(run/'agent-steps',run);logs.mkdir(exist_ok=True)
        folder=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S-'),dir=logs))
        if args.action in ('submit','revise'):
            (folder/'packet.json').write_bytes(packet.read_bytes())
            (folder/'receipt.json').write_bytes(receipt.read_bytes())
            (folder/'attempt.json').write_text(json.dumps(dict(action=args.action,
                packet_sha256=json.loads(packet.read_text()).get('packet_sha256') or hashlib.sha256(packet.read_bytes()).hexdigest(),
                packet_file_sha256=hashlib.sha256(packet.read_bytes()).hexdigest(),
                receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest(),
                repair_note_sha256=repair_digest),indent=2)+'\n')
            if repair_digest:(folder/'repair-note.json').write_bytes(within(args.repair_note,run).read_bytes())
        elif args.action=='answer':
            (folder/'packet.json').write_bytes(packet.read_bytes())
            (folder/'answer.json').write_bytes(answer.read_bytes())
            (folder/'attempt.json').write_text(json.dumps(dict(action='answer',
                packet_sha256=json.loads(packet.read_text()).get('packet_sha256') or hashlib.sha256(packet.read_bytes()).hexdigest(),
                packet_file_sha256=hashlib.sha256(packet.read_bytes()).hexdigest(),
                answer_sha256=hashlib.sha256(answer.read_bytes()).hexdigest()),indent=2)+'\n')
        elif args.action=='reply':
            incoming=getattr(sys.stdin,'buffer',sys.stdin).read()
            raw_answer=incoming.encode('utf-8') if isinstance(incoming,str) else incoming
            answer=folder/'answer.json'
            save_bytes(answer,raw_answer)
            save_bytes(folder/'attempt.json',(json.dumps(dict(action='reply',task_handle=args.task,
                answer_sha256=hashlib.sha256(raw_answer).hexdigest()),indent=2)+'\n').encode('utf-8'))
    except (ValueError,OSError) as exc:parser.error(str(exc))
    launcher=[sys.executable,str(Path(__file__).with_name('flwu.py'))]
    if args.checkout:launcher+=['--checkout',str(args.checkout.expanduser().resolve())]
    if args.python:launcher+=['--python',str(args.python.expanduser().absolute())]
    try:
        if args.action in ('submit','revise'):
            command=launcher+['workflow',args.action,'--advance','--run-dir',str(run),'--packet',str(packet),'--receipt',str(receipt)]
            if args.action=='revise':command+=['--predecessor',args.predecessor,'--reason',args.reason]
            raw=execute(command,folder,args.action)
        elif args.action in ('answer','reply'):
            command=(launcher+['workflow','reply','--run-dir',str(run),'--task',args.task,'--answer',str(answer)]
                     if args.action=='reply' else
                     launcher+['workflow','answer','--advance','--run-dir',str(run),'--packet',str(packet),'--answer',str(answer)])
            # Inline execute: the per-attempt answer input occupies 'answer.json',
            # so command metadata (argv, exit_code) is recorded in attempt.json instead.
            result=subprocess.run(command,capture_output=True,text=True)
            (folder/'answer.stdout').write_text(result.stdout)
            (folder/'answer.stderr').write_text(result.stderr)
            meta=json.loads((folder/'attempt.json').read_text())
            meta['argv']=command;meta['exit_code']=result.returncode
            (folder/'attempt.json').write_text(json.dumps(meta,indent=2)+'\n')
            if result.returncode:
                print(result.stderr or result.stdout,file=sys.stderr)
                raise subprocess.CalledProcessError(result.returncode,command)
            raw=result.stdout
        elif args.action=='retry':
            raw=execute(launcher+['workflow','retry-publication','--run-dir',str(run),'--packet',str(packet)],folder,'retry')
        else:
            raw=execute(launcher+['workflow','model-next','--run-dir',str(run)],folder,'next')
        state=json.loads(raw)
        if not isinstance(state,dict) or 'phase' not in state or type(state.get('complete')) is not bool:
            raise ValueError('Next-task returned an invalid state; previous pointer preserved')
        if state.get('review_mode')=='inline_answer':
            card=state.get('review_card')
            token=state.get('task_handle','')
            if (not isinstance(card,dict) or not {'question','evidence','answer'}<=set(card)
                    or not isinstance(card['evidence'],list) or not isinstance(card['answer'],dict)
                    or not isinstance(token,str) or not 24<=len(token)<=32
                    or any(ch not in '0123456789abcdef' for ch in token)
                    or not isinstance(state.get('command'),str) or not state['command']
                    or not isinstance(state.get('review_progress'),dict)):
                raise ValueError('Inline task returned an incomplete card or binding; previous pointer preserved')
        output.parent.mkdir(parents=True,exist_ok=True)
        fd,temporary=tempfile.mkstemp(prefix='.next-',dir=output.parent)
        try:
            with os.fdopen(fd,'w') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            os.replace(temporary,output)
        finally:
            if os.path.exists(temporary):os.unlink(temporary)
        # The routine view already contains its complete card and one checked
        # action. Detailed execution paths remain in the private attempt logs.
        visible=(state if state.get('review_mode')=='inline_answer' else
                 dict(state,next_state=str(output),logs=str(folder)))
        print(json.dumps(visible,indent=2,ensure_ascii=False))
        return 0
    except subprocess.CalledProcessError as exc:
        print('Step failed; previous next-state pointer preserved. Logs: '+str(folder),file=sys.stderr)
        return exc.returncode
    except (ValueError,OSError) as exc:
        print(str(exc)+'; previous next-state pointer preserved. Logs: '+str(folder),file=sys.stderr)
        return 1


if __name__=='__main__':raise SystemExit(main())
