"""Durable, model-neutral coordination of the existing update/review components.

Database events are authoritative. Files are reproducible projections, never proof
that acquisition, review, acceptance, or deployment completed.
"""
from __future__ import annotations

from contextlib import contextmanager
import copy
import fcntl
import json
import os
from pathlib import Path
import shlex
import tempfile

from flwu import history as h, source_gate as gate, opinion_discovery as opinions, update

VERSION = 1
ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value, *, immutable=False):
    """Atomic projection; interrupted writes cannot masquerade as completed JSON."""
    path = Path(path)
    raw = (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    if immutable and path.exists():
        if path.read_bytes() != raw:
            raise ValueError('Immutable workflow artifact differs: ' + str(path))
        return path
    fd, temporary = tempfile.mkstemp(prefix='.'+path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if immutable:
            try:
                os.link(temporary, path)
            except FileExistsError:
                if path.read_bytes() != raw:
                    raise ValueError('Concurrent workflow artifact differs: ' + str(path)) from None
        else:
            os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path


def stream(config):
    return 'workflow:' + h.sha(config)


def events(conn, config):
    return [json.loads(r['payload'])['workflow'] for r in conn.execute(
        'SELECT payload FROM captures WHERE stream=? ORDER BY seq', (stream(config),))]


def record(conn, config, event):
    payload = dict(status='incomplete', contract={}, checks=[], findings=[], drafts=[], workflow=event)
    return h.record(conn, stream=stream(config), mode='manual_research',
                    scope={'workflow_contract':h.sha(config)}, run_id=h.sha(event),
                    payload=payload, artifacts={h.sha(event):h.canonical(event).encode()})


def initialize(run_dir, database, registry, run_id, *, start=None, end=None,
               directories=(), archive=None, mode='preview', trial=None):
    run_dir = Path(run_dir).resolve()
    if mode not in ('preview', 'publish'):
        raise ValueError('Workflow mode must be preview or publish')
    config = dict(schema_version=VERSION, run_dir=str(run_dir), database=str(Path(database).expanduser().resolve()),
                  registry=gate.load_registry(registry), run_id=run_id, start=start, end=end,
                  mode=mode, checkout=str(ROOT), archive=str(Path(archive).resolve()) if archive else None,
                  directories=sorted(str(Path(p).resolve()) for p in directories))
    if trial is not None:
        config['trial'] = trial
        if mode != 'preview':raise ValueError('Offline trials are preview-only')
    if not isinstance(run_id, str) or not run_id.strip() or not end:
        raise ValueError('An explicit run ID and resolved reporting cutoff are required')
    contract_path = run_dir/'workflow'/'contract.json'
    if contract_path.exists():
        pinned = read(contract_path)
        if {k:v for k,v in pinned.items() if k != 'baseline_capture'} != config:
            raise ValueError('Workflow inputs are pinned; use the original arguments or a new run directory')
        write(run_dir/'workflow'/'registry.json', pinned['registry'], immutable=True)
        return dict(run_dir=str(run_dir), contract_sha256=h.sha(pinned), mode=mode,
                    next_command=command(pinned, 'workflow', 'next-task', '--run-dir', str(run_dir)))
    with h.database(config['database']) as conn:
        gate.target(conn, config['registry']['stream'])
        # Recover a committed initialization whose file projection was interrupted.
        previous = [json.loads(r['payload']).get('workflow', {}) for r in conn.execute(
            "SELECT payload FROM captures WHERE stream LIKE 'workflow:%' ORDER BY seq")]
        recovered = next((e['config'] for e in previous if e.get('kind') == 'initialized'
                          and e['config'].get('run_dir') == str(run_dir)), None)
        if recovered is not None:
            if {k:v for k,v in recovered.items() if k != 'baseline_capture'} != config:
                raise ValueError('Database already pins different workflow inputs for this directory')
            write(contract_path, recovered, immutable=True)
            write(run_dir/'workflow'/'registry.json', recovered['registry'], immutable=True)
            return dict(run_dir=str(run_dir), contract_sha256=h.sha(recovered), mode=mode,
                        next_command=command(recovered, 'workflow', 'next-task', '--run-dir', str(run_dir)))
        # Validate reporting boundaries now, before creating any workflow state.
        opinions.window(conn, config['registry']['stream'], start, end, 30)
        baseline = h.latest_finalized(conn, config['registry']['stream'])
        config['baseline_capture'] = baseline['capture_id'] if baseline else None
        record(conn, config, dict(kind='initialized', config=config))
    write(contract_path, config, immutable=True)
    write(run_dir/'workflow'/'registry.json', config['registry'], immutable=True)
    return dict(run_dir=str(run_dir), contract_sha256=h.sha(config), mode=mode,
                next_command=command(config, 'workflow', 'next-task', '--run-dir', str(run_dir)))


def load(run_dir):
    path = Path(run_dir).resolve()/'workflow'/'contract.json'
    config = read(path)
    if config.get('schema_version') != VERSION or config.get('run_dir') != str(Path(run_dir).resolve()):
        raise ValueError('Invalid or relocated workflow contract')
    if config.get('checkout') != str(ROOT):
        raise ValueError('Use the pinned workflow checkout: ' + config.get('checkout', 'unknown'))
    with h.database(config['database']) as conn:
        saved = events(conn, config)
        if not saved or saved[0] != dict(kind='initialized', config=config):
            raise ValueError('Workflow contract does not match its database record')
    return config


def command(config, *args):
    """Commands bind interpreter and checkout, independent of editable installs."""
    import sys
    return shlex.join(['env', 'PYTHONDONTWRITEBYTECODE=1', 'PYTHONPATH='+str(ROOT/'src'),
                       sys.executable, '-m', 'flwu', *map(str, args)])


def acquisition_command(config):
    return command(config, 'workflow', 'acquire', '--run-dir', config['run_dir'])


def acquire(run_dir):
    config = load(run_dir)
    from flwu.acquisition import acquisition
    with locked(config), acquisition(config['database'],config['run_id'],'workflow acquire'), h.database(config['database']) as conn:
        pinned=any(e['run_id']==config['run_id'] and e['checkpoint']=='update-contract'
                   for e in opinions.events(conn,config['registry']['stream']))
        baseline=h.latest_finalized(conn,config['registry']['stream'])
        if not pinned and not config['start'] and (baseline['capture_id'] if baseline else None)!=config['baseline_capture']:
            raise ValueError('Finalized baseline changed before acquisition; initialize a new workflow')
        kwargs = {}
        if config.get('trial'):
            from flwu.workflow_trial import Transport
            kwargs['fetch'] = Transport(config)
        queue = update.run(conn, config['registry'], config['run_id'], config['run_dir'],
                           start=config['start'], end=config['end'], **kwargs)
        return dict(phase='acquired', acquisition_complete=queue['acquisition_complete'],
                    publication_performed=False, queue=str(Path(config['run_dir'])/'update-queue.json'),
                    next_command=command(config,'workflow','next-task','--run-dir',config['run_dir']))


@contextmanager
def locked(config):
    path = Path(config['run_dir'])/'workflow'/'coordinator.lock'
    with path.open('a+') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Workflow coordinator is active; wait for that command, do not restart it') from None
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def latest_queue(conn, config, *, refresh=False):
    registry = config['registry']
    saved = [e for e in opinions.events(conn, registry['stream']) if e['run_id']==config['run_id']]
    event = next((e for e in reversed(saved) if e['checkpoint']=='update-result'), None)
    if event is None:
        return None
    if refresh:
        return update.refresh(conn, registry, config['run_id'], config['run_dir'])
    raw = gate.blob(conn, event['queue_sha256'])
    if h.sha(raw) != event['queue_sha256']:
        raise ValueError('Saved standard queue checksum mismatch')
    queue = json.loads(raw)
    if queue['run_id'] != config['run_id'] or queue['bounds'] != event['bounds']:
        raise ValueError('Saved standard queue identity mismatch')
    return queue


def accepted(conn, config):
    return {e['packet_sha256']:e for e in events(conn, config) if e['kind']=='decision'}


def packet(config, kind, identity, inputs, template, instructions, *, checks=()):
    from flwu.workflow_contracts import contract
    body = dict(schema_version=VERSION, kind=kind, identity=identity, inputs=inputs,
                receipt_template=template, instructions=instructions, completion_checks=list(checks),
                output_contract=contract(kind,template))
    digest = h.sha(body)
    folder = Path(config['run_dir'])/'workflow'/'tasks'/digest
    body.update(packet_sha256=digest, packet_path=str(folder/'packet.json'),
                receipt_path=str(folder/'receipt.json'))
    body['submit_command'] = command(config, 'workflow', 'submit', '--run-dir', config['run_dir'],
                                     '--packet', body['packet_path'], '--receipt', body['receipt_path'])
    return body


def materialize(config, task):
    write(task['packet_path'], task, immutable=True)
    template = Path(task['packet_path']).with_name('receipt-template.json')
    write(template, task['receipt_template'], immutable=True)
    return dict(kind=task['kind'], identity=task['identity'], packet=task['packet_path'],
                receipt_template=str(template), save_receipt=task['receipt_path'],
                command=task['submit_command'], completion_checks=task['completion_checks'])


def tasks(conn, config, queue):
    """One saved source/opinion at a time; downstream assembly is a separate stage."""
    available=False
    for task in queue['source_reviews']['tasks']:
        if task['reason'] not in ('retrieval_failed', 'not_fetched'):
            available=True
            template = copy.deepcopy(task['review_template'])
            observed = task['observation']
            for side, prefix in (('current',''),('previous','previous_')):
                if observed.get(prefix+'sha256') and observed.get(prefix+'text_sha256'):
                    template['support'][side] = [dict(sha256=observed[prefix+'sha256'],
                        text_sha256=observed[prefix+'text_sha256'],quote='',locator='')]
            yield packet(config, 'source_review', task['source_id'], task, template,
                         'Read this source and its diff/prior findings. Fill the exact receipt. Code compares bytes; '
                         'you interpret civil/commercial relevance. Missing extraction remains unfinished.',
                         checks=('Exact acquisition and quoted support validated by source-gate review',))
    for task in queue['opinion_reviews']['tasks']:
        if not set(task['reasons']) & {'official_status_source_unavailable','opinion_download_unavailable'}:
            available=True
            template=copy.deepcopy(task['review_template'])
            observation=task['source_observation']
            template['citations']=[dict(sha256=observation['sha256'],text_sha256=observation['text_sha256'],quote='',locator='')]
            yield packet(config, 'opinion_review', task['opinion']['id'], task, template,
                         'Read the acquired opinion and status evidence. Screen relevance; for relevant opinions '
                         'provide supported summary, holding, disposition and author names.',
                         checks=('Exact opinion signature and citations validated by opinion-review',))
    if available:return
    from flwu.workflow_report import tasks as report_tasks
    yield from report_tasks(conn, config, queue)
    done = accepted(conn, config)
    if any(t['packet_sha256'] not in done for t in report_tasks(conn, config, queue)):
        return
    from flwu.workflow_report import assemble
    _, _, _, fingerprint = assemble(conn, config, queue)
    prepared = next((e for e in reversed(events(conn, config)) if e['kind']=='report_prepared' and e['fingerprint']==fingerprint), None)
    if prepared is None:
        return
    from flwu.workflow_directory import tasks as directory_tasks
    yield from directory_tasks(conn, config, prepared)
    if any(t['packet_sha256'] not in done for t in directory_tasks(conn, config, prepared)):
        return
    from flwu.workflow_directory import current as current_directories
    directories = current_directories(conn, config, prepared)
    if directories is not None:
        from flwu.workflow_release import tasks as release_tasks
        yield from release_tasks(conn, config, prepared, directories)


def inspect(run_dir, *, emit=False):
    config = load(run_dir)
    with locked(config), h.database(config['database']) as conn:
        queue = latest_queue(conn, config, refresh=True)
        if queue is None:
            return dict(phase='acquisition', complete=False, command=acquisition_command(config),
                        explanation='No completed standard acquisition result. Resume the exact command; wait if it is active.')
        decisions = accepted(conn, config)
        for task in tasks(conn, config, queue):
            if task['packet_sha256'] not in decisions:
                result = dict(phase=task['kind'], complete=False,
                              acquisition_complete=queue['acquisition_complete'])
                result.update(materialize(config, task) if emit else
                              dict(identity=task['identity'], next_command=command(config,'workflow','next-task','--run-dir',config['run_dir'])))
                return result
        from flwu.workflow_report import state
        return state(conn, config, queue, emit=emit)


def submit(run_dir, packet_path, receipt_path):
    config = load(run_dir)
    supplied = read(packet_path)
    receipt = read(receipt_path)
    with locked(config), h.database(config['database']) as conn:
        done = accepted(conn, config).get(supplied.get('packet_sha256'))
        if done:
            if supplied != done['task']:
                raise ValueError('Completed task packet was modified')
            if receipt != done['receipt']:
                raise ValueError('Completed task receipt changed; an explicit new review is required')
            return dict(replayed=True, packet_sha256=done['packet_sha256'])
        queue = latest_queue(conn, config, refresh=True)
        if queue is None:
            raise ValueError('Complete acquisition first')
        current = next((t for t in tasks(conn, config, queue)
                        if t['packet_sha256']==supplied.get('packet_sha256')), None)
        # The domain review may commit before our completion event. Only replay
        # a previously validated, durably saved submission of the exact receipt.
        retry = next((e for e in reversed(events(conn, config))
                      if e['kind']=='submission' and e['task']==supplied and e['receipt']==receipt), None)
        if current is None and retry and supplied['kind'] in ('source_review','opinion_review'):
            current = retry['task']
        if current is None or current != supplied:
            raise ValueError('Task packet is stale or modified; request next-task again')
        record(conn, config, dict(kind='submission', task=current, receipt=receipt))
        registry = gate.load_registry(Path(config['run_dir'])/'expanded-registry.json')
        if current['kind']=='source_review':
            result = gate.accept(conn, registry, receipt)
        elif current['kind']=='opinion_review':
            result = opinions.accept_review(conn, registry, receipt)
        elif current['kind'] in ('directory_review','directory_removal'):
            from flwu.workflow_directory import validate_decision
            result = validate_decision(conn, config, current, receipt)
        elif current['kind'] in ('roster_review','publication_acceptance'):
            from flwu.workflow_release import validate_decision
            result = validate_decision(conn, config, current, receipt)
        else:
            from flwu.workflow_report import validate_decision
            result = validate_decision(conn, config, current, receipt)
        event = dict(kind='decision', packet_sha256=current['packet_sha256'], task=current,
                     receipt=receipt, validation=result)
        saved = record(conn, config, event)
        write(Path(config['run_dir'])/'workflow'/'accepted'/(current['packet_sha256']+'.json'),event,immutable=True)
        return dict(capture_id=saved['capture_id'], packet_sha256=current['packet_sha256'],
                    next_command=command(config,'workflow','next-task','--run-dir',config['run_dir']))
