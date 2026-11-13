"""Inline cards and evidence-bound replies over the existing review protocol.

This layer changes transport only. Original bytes, drafting, domain validation,
corrections and finalization remain owned by the existing coordinator.
"""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re
import shlex
import sys
import tempfile

from flwu import compact_review as compact, history as h, workflow as w
from flwu import workflow_short as short

VERSION = 1
from flwu.publication_driver import KINDS
ORDINARY = ('source_review', 'opinion_review', *sorted(KINDS))
UNREADABLE = object()


def _within(path, root):
    path=Path(path).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError('Inline review artifacts must stay inside this run')
    return path


def _json_bytes(value):
    return (json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n').encode()


def _immutable_bytes(path, raw, mode=0o400):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=raw:raise ValueError('Immutable inline artifact changed: '+str(path))
        return path
    fd,name=tempfile.mkstemp(prefix='.inline-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(raw);stream.flush();os.fsync(stream.fileno());os.fchmod(stream.fileno(),mode)
        try:os.link(name,path)
        except FileExistsError:
            if path.read_bytes()!=raw:raise ValueError('Concurrent immutable inline artifact differs') from None
    finally:
        if os.path.exists(name):os.unlink(name)
    return path


def _wrapper(config):
    path=_within(Path(config['run_dir'])/'review',config['run_dir'])
    common=shlex.join([sys.executable,str(w.ROOT/'skills/florida-update/scripts/review_step.py'),
                       '--checkout',str(w.ROOT),'--python',sys.executable])
    run=shlex.quote(config['run_dir'])
    raw=("#!/bin/sh\nset -eu\n"
         "if [ \"$#\" -eq 0 ]; then\n"
         f"  exec {common} next --run-dir {run}\n"
         "elif [ \"$#\" -eq 1 ]; then\n"
         f"  exec {common} reply --run-dir {run} --task \"$1\"\n"
         "else\n  echo 'Use review with no arguments to refresh, or one issued task handle with JSON on stdin.' >&2\n  exit 2\nfi\n").encode()
    _immutable_bytes(path,raw,0o700)
    if not os.access(path,os.X_OK):raise ValueError('Pinned review executable is not executable')
    return path


def _binding(config, task, packet_path, card_path, bundle):
    return dict(version=VERSION,contract_sha256=h.sha(config),checkout=str(w.ROOT),
                python=sys.executable,packet_sha256=task['packet_sha256'],
                packet_path=str(packet_path),packet_file_sha256=h.sha(packet_path.read_bytes()),
                card_path=str(card_path),card_file_sha256=h.sha(card_path.read_bytes()),
                bundle_sha256=h.sha(bundle))


def model_state(run_dir, state):
    """Project only the routine UI; maintenance/downstream states retain their API."""
    if state.get('phase') not in ORDINARY or state.get('review_mode')!='short_answer':return state
    config=w.load(run_dir)
    live=w.inspect(run_dir,emit=False)
    packet_path=_within(state['packet'],config['run_dir'])
    card_path=_within(state['review_card'],config['run_dir'])
    task=w.read(packet_path)
    with w.locked(config),h.database(config['database']) as conn:
        queue=w.latest_queue(conn,config,refresh=True)
        current=next((t for t in w.tasks(conn,config,queue) if t['packet_sha256']==task['packet_sha256']),None)
        if (current!=task or live.get('phase')!=task['kind'] or live.get('identity')!=task['identity']
                or task['packet_sha256'] in w.accepted(conn,config)):
            raise ValueError('Task changed while projecting inline card; refresh checked next')
        bundle=compact.prepare(conn,task)
        if bundle['exception']:raise ValueError(bundle['exception'])
        if card_path.read_bytes()!=_json_bytes(bundle['card']):raise ValueError('Acquired inline card changed')
        wrapper=_wrapper(config)
        binding=_binding(config,task,packet_path,card_path,bundle)
        handle=h.sha(binding)[:24]
        manifest=_within(Path(config['run_dir'])/'workflow/inline-tasks'/f'{handle}.json',config['run_dir'])
        w.write(manifest,binding,immutable=True)
        private=w.write(Path(config['run_dir'])/'workflow/inline-states'/f'{h.sha(state)}.json',state,immutable=True)
        event=dict(kind='inline_task',handle=handle,binding=binding,
                   projection_hashes=w.projection_hashes([manifest,packet_path,card_path,wrapper,private]))
        if event not in w.events(conn,config):w.record(conn,config,event)
    result={k:state[k] for k in ('phase','complete','acquisition_complete','review_progress',
                                'answer_failure','unresolved_checkpoint') if k in state}
    result.update(review_mode='inline_answer',task_handle=handle,review_card=bundle['card'],
                  command=shlex.join([str(wrapper),handle]))
    return result


def next_task(run_dir):
    from flwu.publication_driver import advance
    return model_state(run_dir,advance(run_dir))


@contextmanager
def _reply_lock(config):
    path=_within(Path(config['run_dir'])/'workflow/inline-reply.lock',config['run_dir'])
    with path.open('a+') as stream:
        try:fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Inline review reply is active; wait for that command') from None
        try:yield
        finally:fcntl.flock(stream,fcntl.LOCK_UN)


def _issued(conn, config, handle):
    if not isinstance(handle,str) or not re.fullmatch(r'[0-9a-f]{24}',handle):
        raise ValueError('Invalid inline task handle; refresh checked next')
    issued=next((e for e in reversed(w.events(conn,config)) if e['kind']=='inline_task' and e['handle']==handle),None)
    if issued is None:raise ValueError('Unknown inline task handle for this run; refresh checked next')
    binding=issued['binding']
    if h.sha(binding)[:24]!=handle:raise ValueError('Inline task binding changed')
    for path in issued['projection_hashes']:_within(path,config['run_dir'])
    w.verify_projections(issued)
    manifest=_within(Path(config['run_dir'])/'workflow/inline-tasks'/f'{handle}.json',config['run_dir'])
    if w.read(manifest)!=binding:raise ValueError('Inline task manifest changed')
    packet_path=_within(binding['packet_path'],config['run_dir'])
    card_path=_within(binding['card_path'],config['run_dir'])
    task=w.read(packet_path)
    bundle=compact.prepare(conn,task)
    if (bundle['exception'] or _binding(config,task,packet_path,card_path,bundle)!=binding
            or card_path.read_bytes()!=_json_bytes(bundle['card'])):
        raise ValueError('Inline task evidence or execution binding changed; refresh checked next')
    return task,packet_path


def _rejection(events, task, request, value):
    if not request:return None
    start=events.index(request)
    for event in reversed(events[start+1:]):
        if event['kind']!='answer_rejected' or event.get('packet_sha256')!=task['packet_sha256']:continue
        if (value is not UNREADABLE and event['answer']==value) or (
                value is UNREADABLE and isinstance(event['answer'],dict) and event['answer'].get('unreadable_answer')
                and event['answer'].get('answer_path')==request['answer_path']):return event
    return None


def _retry(run_dir, task, failure):
    state=next_task(run_dir)
    state['answer_failure']=dict(source=task['identity'],attempt=failure['attempt'],error=failure['error'])
    return state


def reply(run_dir, task_handle, answer_path):
    """Save/validate via the existing protocol, then return the complete next card."""
    config=w.load(run_dir)
    answer_path=_within(answer_path,Path(config['run_dir'])/'agent-steps')
    raw=answer_path.read_bytes()
    digest=h.sha(raw)
    try:value=json.loads(raw)
    except (ValueError,UnicodeError):value=UNREADABLE
    with _reply_lock(config):
        # Never let a caller's subsequently edited file change the validated
        # request. The helper also retains its original per-invocation input.
        answer_path=_immutable_bytes(_within(Path(config['run_dir'])/'workflow/inline-inputs'/f'{digest}.json',
                                            config['run_dir']),raw)
        live=w.inspect(run_dir,emit=False)
        with w.locked(config),h.database(config['database']) as conn:
            task,packet_path=_issued(conn,config,task_handle)
            events=w.events(conn,config)
            request=next((e for e in events if e['kind']=='inline_request' and e['handle']==task_handle
                          and e['answer_sha256']==digest),None)
            done=w.accepted(conn,config).get(task['packet_sha256'])
            compiled=[e for e in events if e['kind']=='answer_compiled' and e['packet_sha256']==task['packet_sha256']
                      and e['answer']==value]
            if done:
                if not any(e['receipt_sha256']==h.sha(done['receipt']) for e in compiled):
                    raise ValueError('Accepted answer changed; use the explicit correction path')
            else:
                retry_submission=any(e['kind']=='submission' and e['task']==task
                                     and any(c['receipt_sha256']==h.sha(e['receipt']) for c in compiled) for e in events)
                queue=w.latest_queue(conn,config,refresh=True)
                current=next((t for t in w.tasks(conn,config,queue) if t['packet_sha256']==task['packet_sha256']),None)
                active=(current==task and live.get('phase')==task['kind'] and live.get('identity')==task['identity'])
                rejection=_rejection(events,task,request,value)
                checkpoint=short.unresolved(conn,config).get(task['packet_sha256'])
                if not active and not retry_submission and not (request and checkpoint):
                    raise ValueError('Inline task is stale or no longer current; refresh checked next')
                if rejection:
                    deferred_failure=rejection
                else:deferred_failure=None
                if request and checkpoint and not rejection:
                    # Replaying an uncertainty checkpoint cannot complete it.
                    deferred_uncertainty=True
                else:deferred_uncertainty=False
            if not request:
                request=dict(kind='inline_request',handle=task_handle,packet_sha256=task['packet_sha256'],
                             answer_sha256=digest,answer_path=str(answer_path),
                             projection_hashes=w.projection_hashes([answer_path]))
                w.record(conn,config,request)
        if not done and deferred_failure:return _retry(run_dir,task,deferred_failure)
        if not done and deferred_uncertainty:return next_task(run_dir)
        w.verify_projections(request)
        try:
            # next_task below owns advancement, including deterministic publication.
            # Do not prepare the next statewide state here only to discard it.
            saved=short.answer(run_dir,packet_path,answer_path,advance=False)
        except ValueError:
            with h.database(config['database']) as conn:
                failure=_rejection(w.events(conn,config),task,request,value)
            if failure:return _retry(run_dir,task,failure)
            raise  # A technical/advance/correction failure is not a semantic verdict.
        try:return next_task(run_dir)
        except (ValueError,OSError,KeyError,TypeError) as exc:
            if saved.get('packet_sha256')==task['packet_sha256']:
                raise ValueError('Short answer submission is saved, but advancement failed: '+str(exc)+
                    '. Retry next-task or the exact answer; do not rewrite it.') from exc
            raise
