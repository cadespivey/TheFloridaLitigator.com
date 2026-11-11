"""Routine short-answer execution and durable unresolved technical checkpoints."""
from pathlib import Path
import shlex
import sys
from flwu import history as h, workflow as w, compact_review as compact


def checked_command(config, action, *, packet=None, answer=None):
    """One ordinary entry point, pinned to this checkout and interpreter."""
    args = [sys.executable, str(w.ROOT/'skills/florida-update/scripts/review_step.py'),
            '--checkout', str(w.ROOT), '--python', sys.executable,
            action, '--run-dir', config['run_dir']]
    if packet is not None:
        args += ['--packet', str(packet)]
    if answer is not None:
        args += ['--answer', str(answer)]
    return shlex.join(map(str, args))


def present(conn, config, queue, decisions, state):
    """Expose literal counts at every post-acquisition stage, without extra work."""
    counts = progress(conn, config, queue, decisions)
    result = dict(state, review_progress=counts)
    if state['phase'] in ('source_review', 'opinion_review'):
        return result
    if state['complete']:
        phase = f"Authorized workflow complete: {state['phase']}."
    elif state['phase'] in ('review_exceptions','publication_exceptions'):
        phase = 'Review checkpoint; update incomplete. Finalization/publication blocked.'
    else:
        phase = f"Update incomplete; next required stage: {state['phase']}."
    result['handoff_text'] = '\n'.join([
        '- ' + phase,
        (f"- Sources: {counts['total_sources']} total; {counts['reviewed_sources']} reviewed; "
         f"{counts['machine_reused_sources']} reused; {counts['pending_sources']} pending."),
        (f"- Saved review decisions: {counts['saved_review_decisions']}; "
         f"opinion reviews remaining: {counts['remaining_opinion_reviews']}."),
        (f"- Unresolved checkpoints: {counts['checkpointed_reviews']}; "
         f"rejected short answers: {counts['failed_short_answers']}."),
        '- Logs: agent-steps/; checkpoint details: agent-next-task.json in the run directory.',
    ])
    result['handoff_instructions'] = ('When the user-authorized scope permits stopping, return handoff_text verbatim as the entire final response, '
                                    'without an introduction, postscript or repeated explanation, unless the user requests detail. '
                                    'Otherwise continue the returned stage. Do not inspect directories or '
                                    'reconstruct counts; a checkpoint is not workflow completion.')
    return result


def _within(path, config):
    path=Path(path).resolve()
    if not path.is_relative_to(Path(config['run_dir']).resolve()):
        raise ValueError('Review inputs must stay inside this run')
    return path


def unresolved(conn, config):
    pending={}
    for event in w.events(conn,config):
        if event['kind']=='review_exception': pending[event['packet_sha256']]=event
        elif event['kind']=='review_exception_resolved': pending.pop(event['packet_sha256'],None)
    return pending


def progress(conn, config, queue, decisions):
    """Literal code-owned counts, including checkpoints hidden behind other work."""
    sources={(t['source_id'],(t.get('observation') or {}).get('capture_id')) for t in queue['source_reviews']['tasks']}
    opinions={(t['opinion']['id'],t['signature']) for t in queue['opinion_reviews']['tasks']}
    active=[]
    checkpoints=unresolved(conn,config)
    from flwu.publication_driver import KINDS
    publication_packets=({t['packet_sha256'] for t in w.tasks(conn,config,queue) if t['kind'] in KINDS}
                         if any(e['task_kind'] in KINDS for e in checkpoints.values()) else set())
    for entry in checkpoints.values():
        if entry['task_kind']=='source_review' and (entry['identity'],entry['observation_capture_id']) in sources:active.append(entry)
        elif entry['task_kind']=='opinion_review' and (entry['identity'],entry.get('task',{}).get('inputs',{}).get('signature')) in opinions:active.append(entry)
        elif entry['packet_sha256'] in publication_packets and entry['packet_sha256'] not in decisions:active.append(entry)
    pending_ids={source_id for source_id,_ in sources}
    reused=queue['source_reviews'].get('reused_reviews',[])
    reused_ids={item['source_id'] for item in reused}-pending_ids
    reused_pairs={(item['source_id'],item.get('sha256')) for item in reused if item.get('sha256')}
    reviewed_ids=set()
    for event in decisions.values():
        task=event['task']
        observed=task.get('inputs',{}).get('observation') or {}
        if (task['kind']=='source_review' and observed.get('sha256')
                and (task.get('identity'),observed['sha256']) in reused_pairs):
            reviewed_ids.add(task['identity'])
    reviewed_ids &= reused_ids
    return dict(total_sources=len(pending_ids|reused_ids),
                reviewed_sources=len(reviewed_ids),
                machine_reused_sources=len(reused_ids-reviewed_ids),
                pending_sources=len(pending_ids),
                saved_review_decisions=sum(e['task']['kind'] in ('source_review','opinion_review') for e in decisions.values()),
                remaining_source_reviews=len(queue['source_reviews']['tasks']),
                remaining_opinion_reviews=len(queue['opinion_reviews']['tasks']),
                checkpointed_reviews=len(active),
                failed_short_answers=sum(e['kind']=='answer_rejected' for e in w.events(conn,config)))


def checkpoint(conn, config, task, reason, category):
    old=unresolved(conn,config).get(task['packet_sha256'])
    if old and old['reason']==reason:return old
    event=dict(kind='review_exception',packet_sha256=task['packet_sha256'],
               identity=task['identity'],task_kind=task['kind'],category=category,reason=reason,
               packet=task['packet_path'],task=task,projection_hashes=w.projection_hashes([task['packet_path']]),observation_capture_id=(task['inputs'].get('observation') or task['inputs'].get('source_observation') or {}).get('capture_id'))
    w.record(conn,config,event)
    return event


def exception_view(config, task, reason, category):
    return dict(identity=task['identity'],kind=task['kind'],packet=task['packet_path'],
                category=category,reason=reason,
                maintenance_command=w.command(config,'workflow','maintenance-task','--run-dir',config['run_dir'],'--packet',task['packet_path']))


def view(conn, config, task, *, emit):
    """Return ordinary task or unresolved descriptor; never a benign verdict."""
    flagged=unresolved(conn,config).get(task['packet_sha256'])
    bundle=compact.prepare(conn,task)
    if flagged or bundle['exception']:
        reason=flagged['reason'] if flagged else bundle['exception']
        category=flagged['category'] if flagged else 'technical_or_extended_evidence'
        if emit:
            compact.project(conn,config,task)
            checkpoint(conn,config,task,reason,category)
        return None,exception_view(config,task,reason,category)
    state=dict(phase=task['kind'],complete=False,review_mode='short_answer')
    if emit:
        state.update(compact.project(conn,config,task))
        # Kept for existing API clients. These are maintenance-only, not reading
        # instructions; no legacy guide or schema is in the ordinary task view.
        template=Path(task['packet_path']).with_name('receipt-template.json')
        w.write(template,task['receipt_template'],immutable=True)
        state.update(receipt_template=str(template),save_receipt=task['receipt_path'])
    else:state.update(identity=task['identity'],next_command=checked_command(config,'next'))
    return state,None


def _rejected(config, task, answer, error, answer_path=None):
    with w.locked(config),h.database(config['database']) as conn:
        number=1+sum(e['kind']=='answer_rejected' and e.get('packet_sha256')==task['packet_sha256'] for e in w.events(conn,config))
        event=dict(kind='answer_rejected',packet_sha256=task['packet_sha256'],attempt=number,
                   answer=answer,error=str(error))
        if answer_path is not None and Path(answer_path).is_file():
            from flwu.derived_cache import write_bytes
            raw=Path(answer_path).read_bytes()
            frozen=Path(task['packet_path']).with_name('rejected-answer-'+h.sha(raw)+'.bin')
            if frozen.exists() and frozen.read_bytes()!=raw:raise ValueError('Rejected answer snapshot is corrupt')
            write_bytes(frozen,raw)
            event['projection_hashes']=w.projection_hashes([frozen])
        w.record(conn,config,event)
        if number>=2:
            checkpoint(conn,config,task,'Two short answers rejected. Latest validator error: '+str(error),'answer_validation')
            return event
    raise ValueError('Short answer rejected: '+str(error)+'. Correct the short answer only; evidence and error are saved.') from error


def _continue_after_failure(run_dir, task, failure):
    # Full input/error/provenance stays in database/logs. The next model needs
    # only the exact error and permission to follow the newly returned task.
    note=dict(source=task['identity'],attempt=failure['attempt'],error=failure['error'],
              next_action='Previous task is checkpointed unresolved. Continue this returned task; do not retry the previous packet automatically.')
    return dict(w.inspect(run_dir,emit=True),answer_failure=note,unresolved_checkpoint=True)


def answer(run_dir, packet_path, answer_path, *, advance=False):
    config=w.load(run_dir)
    packet_path=_within(packet_path,config);answer_path=_within(answer_path,config)
    if packet_path==answer_path:raise ValueError('Answer cannot overwrite its packet')
    supplied=w.read(packet_path)
    with w.locked(config),h.database(config['database']) as conn:
        queue=w.latest_queue(conn,config,refresh=True)
        if queue is None:raise ValueError('Complete acquisition first')
        previous=w.accepted(conn,config).get(supplied.get('packet_sha256'))
        current=(previous['task'] if previous else next((t for t in w.tasks(conn,config,queue) if t['packet_sha256']==supplied.get('packet_sha256')),None))
        if current is None:
            current=next((e['task'] for e in reversed(w.events(conn,config)) if e['kind']=='submission' and e['task']==supplied),None)
        if current is None or current!=supplied:raise ValueError('Task packet is stale or modified; request next-task')
        correction=w.source_correction(conn,config,queue,emit=False)
        if correction and current['kind']=='source_review' and correction['identity']==current['identity']:
            raise ValueError('This source requires its explicit predecessor-bound correction, not a new short review')
        from flwu.publication_driver import KINDS
        if current['kind'] not in ('source_review','opinion_review') and current['kind'] not in KINDS:
            raise ValueError('This stage uses its existing explicit review command')
        bundle=compact.prepare(conn,current)
        # Refuse edited cards/bindings rather than trusting projections supplied by
        # the caller. Rebuild only from packet-bound acquired SQLite evidence.
        compact.project(conn,config,current)
    try:
        value=w.read(answer_path)
    except (ValueError,OSError,UnicodeError) as exc:
        failure=_rejected(config,current,dict(answer_path=str(answer_path),unreadable_answer=True),exc,answer_path)
        return _continue_after_failure(run_dir,current,failure)
    try:
        receipt=compact.compile_answer(current,bundle,value)
        if receipt is not None and '_person_scope' in receipt:
            scope_reason=receipt['_reason']
            from flwu.publication_driver import mapping
            with h.database(config['database']) as conn:
                receipt=mapping(conn,config,current,supplied=dict(scope=receipt['_person_scope']))
            if receipt is None:raise ValueError('Explicit supported personnel scope is required')
            receipt['reason']=scope_reason
    except (ValueError,KeyError,TypeError) as exc:
        failure=_rejected(config,current,value,exc,answer_path)
        return _continue_after_failure(run_dir,current,failure)
    if receipt is None:
        with w.locked(config),h.database(config['database']) as conn:
            checkpoint(conn,config,current,value.get('summary') or value.get('reason'),'model_uncertainty')
        return dict(w.inspect(run_dir,emit=True),unresolved_checkpoint=True)
    if '_opinion_corrections' in receipt:
        from flwu.publication_driver import correct_opinions
        correct_opinions(run_dir,current,bundle,receipt,value)
        return w.inspect(run_dir,emit=True)
    if current['kind']=='publication_acceptance':
        from flwu.publication_driver import artifact_checks
        with w.locked(config),h.database(config['database']) as conn:
            proof=artifact_checks(conn,current)
            w.record(conn,config,dict(kind='publication_artifact_checked',**proof))
    compiled=Path(current['packet_path']).with_name('compiled-answer-'+h.sha(receipt)+'.json')
    w.write(compiled,receipt,immutable=True)
    with w.locked(config),h.database(config['database']) as conn:
        w.record(conn,config,dict(kind='answer_compiled',packet_sha256=current['packet_sha256'],answer=value,
                                 receipt_path=str(compiled),receipt_sha256=h.sha(receipt),
                                 projection_hashes=w.projection_hashes([compiled])))
    try:
        result=w.submit(run_dir,packet_path,compiled)
    except (ValueError,KeyError,TypeError) as exc:
        failure=_rejected(config,current,value,exc,answer_path)
        return _continue_after_failure(run_dir,current,failure)
    with w.locked(config),h.database(config['database']) as conn:
        if current['packet_sha256'] in unresolved(conn,config):
            w.record(conn,config,dict(kind='review_exception_resolved',packet_sha256=current['packet_sha256'],validation=result))
    if not advance:return result
    try:return w.inspect(run_dir,emit=True)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        raise ValueError('Short answer submission is saved, but advancement failed: '+str(exc)+'. Retry next-task or the exact answer; do not rewrite it.') from exc


def maintenance(run_dir, packet_path):
    """Explicit compatibility route for technical/extended reviews, not normal UI."""
    config=w.load(run_dir);path=_within(packet_path,config);supplied=w.read(path)
    with w.locked(config),h.database(config['database']) as conn:
        queue=w.latest_queue(conn,config,refresh=True)
        if queue is None:raise ValueError('Complete acquisition first')
        current=next((t for t in w.tasks(conn,config,queue) if t['packet_sha256']==supplied.get('packet_sha256')),None)
        if current is None or current!=supplied:raise ValueError('Maintenance packet is stale or modified')
        return dict(w.materialize(config,current,conn),review_mode='explicit_maintenance',complete=False,
                    explanation='Legacy technical/extended review. It cannot be completed from a short no-change answer.')


def public_state(state):
    """Hide maintenance-only compatibility pointers in the actual model CLI."""
    if state.get('review_mode')!='short_answer':return state
    return {k:v for k,v in state.items() if k not in ('receipt_template','save_receipt','answer_binding','exception')}
