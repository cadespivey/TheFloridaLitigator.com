"""Append-only rebinding of an acquired, pre-report run after a checkout move.

Acquisition and domain reviews keep their identities. Coordinator contracts are
path-bound, so a new binding links to (rather than edits) the old event stream.
"""
from pathlib import Path
import json
import os
import tempfile

from flwu import history as h, workflow as w
from flwu.acquisition import acquisition


def rows(conn, config):
    return list(conn.execute('SELECT * FROM captures WHERE stream=? ORDER BY seq',
                             (w.stream(config),)))


def checked_events(records, config):
    result = []
    for row in records:
        payload = json.loads(row['payload'])
        event = payload['workflow']
        if (row['capture_id'] != h.sha([w.stream(config), row['run_id'], payload])
                or row['run_id'] != h.sha(event)):
            raise ValueError('Workflow relocation found a damaged database event')
        result.append(event)
    if not result or result[0] != dict(kind='initialized', config=config):
        raise ValueError('Workflow contract does not match its database record')
    return result


def validate_lineage(conn, config):
    """An active binding must have its original contract and durable predecessor."""
    lineage = config.get('relocated_from')
    if not lineage:
        return
    folder = Path(config['run_dir'])/'workflow'/'relocations'/lineage['contract_sha256']
    raw = (folder/'contract.json').read_bytes()
    previous = json.loads(raw)
    if h.sha(raw) != lineage['contract_file_sha256'] or h.sha(previous) != lineage['contract_sha256']:
        raise ValueError('Preserved relocation contract checksum mismatch')
    records = rows(conn, previous)
    events = checked_events(records, previous)
    marker = events[-1]
    if (w.stream(previous) != lineage['stream'] or marker.get('kind') != 'relocation_committed'
            or marker.get('config') != config or len(events)-1 != lineage['event_count']
            or records[-2]['capture_id'] != lineage['head_capture_id']):
        raise ValueError('Relocation predecessor does not match its durable binding')


def _preserve(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.relocation-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.read_bytes() != raw:
                raise ValueError('Preserved relocation contract differs') from None
    finally:
        os.unlink(temporary)


def _project(path, config):
    # w.write performs an fsynced, atomic replacement. Only the live binding is
    # replaced; the original contract bytes have already been preserved.
    w.write(path, config)


def relocate(run_dir, reason):
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError('relocate requires a specific --reason')
    run = Path(run_dir).resolve()
    contract_path = run/'workflow'/'contract.json'
    # Use the moved lock inode, never recreate the retired source directory.
    with w.locked(dict(run_dir=str(run))):
        raw = contract_path.read_bytes()
        previous = json.loads(raw)
        if previous.get('run_dir') == str(run) and previous.get('checkout') == str(w.ROOT):
            current = w.load(run)
            if not current.get('relocated_from'):
                raise ValueError('Workflow has not moved')
            return _result(current, replayed=True)
        if previous.get('schema_version') != w.VERSION or previous.get('trial'):
            raise ValueError('Only an acquired production-style workflow can be relocated')
        old_root = Path(previous['checkout'])
        old_run = Path(previous['run_dir'])
        if not old_root.is_absolute() or not old_run.is_absolute():
            raise ValueError('Original checkout and run must be absolute paths')
        if old_run.exists():
            raise ValueError('Original workflow still exists; move it rather than copying or linking it')
        if not old_run.is_relative_to(old_root) or run != w.ROOT/old_run.relative_to(old_root):
            raise ValueError('Relocation must preserve the run location within its checkout')
        if not Path(previous['database']).is_file():
            raise ValueError('Original research database is missing; relocation does not move databases')

        def moved(value):
            path = Path(value)
            if not path.is_absolute() or not path.is_relative_to(old_root):
                raise ValueError('Configured publication inputs must be inside the original checkout')
            return str(w.ROOT/path.relative_to(old_root))

        config = dict(previous, run_dir=str(run), checkout=str(w.ROOT),
                      archive=moved(previous['archive']) if previous['archive'] else None,
                      directories=[moved(p) for p in previous['directories']])
        if any(not Path(p).is_file() for p in config['directories']):
            raise ValueError('A configured directory supplement is missing after relocation')
        with acquisition(previous['database'], previous['run_id'], 'workflow relocate'), h.database(previous['database']) as conn:
            records = rows(conn, previous)
            events = checked_events(records, previous)
            # An interrupted relocation freezes the predecessor. Recover its
            # exact saved binding, even when a retry supplies different wording.
            marker = events[-1] if events[-1].get('kind') == 'relocation_committed' else None
            if marker:
                target = marker['config']
                expected = {k: v for k, v in target.items() if k != 'relocated_from'}
                candidate = {k: v for k, v in config.items() if k != 'relocated_from'}
                if expected != candidate or h.sha(raw) != target['relocated_from']['contract_file_sha256']:
                    raise ValueError('Interrupted relocation is bound to another location or contract')
                config = target
            else:
                if any(e['kind'] not in ('initialized', 'submission', 'decision') for e in events):
                    raise ValueError('Relocation is limited to research before report preparation')
                decisions = {e['packet_sha256']: e for e in events if e['kind'] == 'decision'}
                for event in events:
                    if event['kind'] == 'initialized':
                        continue
                    task = event['task']
                    if task['kind'] not in ('source_review', 'opinion_review', 'coverage_review'):
                        raise ValueError('Relocation cannot discard downstream editorial decisions')
                    if task['kind'] == 'coverage_review' and (
                            event.get('receipt', {}).get('decision') != 'reviewed_supplement'
                            or event.get('reuse', {}).get('policy') != 'reviewed_supplement'):
                        raise ValueError('Relocation cannot discard a model-authored coverage decision')
                    if event['kind'] == 'submission':
                        done = decisions.get(task['packet_sha256'])
                        if not done or done['receipt'] != event['receipt'] or done['task'] != task:
                            raise ValueError('Complete the interrupted submission before relocation')
                for stage in ('reports', 'directories', 'builds', 'release'):
                    path = run/'workflow'/stage
                    if path.exists() and any(path.iterdir()):
                        raise ValueError('Preserve and recover downstream stage before relocation')
                if w.latest_queue(conn, previous) is None:
                    raise ValueError('Complete the saved acquisition before relocation')
                config['relocated_from'] = dict(
                    contract_sha256=h.sha(previous), contract_file_sha256=h.sha(raw),
                    stream=w.stream(previous), head_capture_id=records[-1]['capture_id'],
                    event_count=len(events), reason=reason.strip())
                _preserve(run/'workflow'/'relocations'/h.sha(previous)/'contract.json', raw)
                # First freeze the old stream. A crash after either record is
                # recoverable using this marker, without another acquisition.
                w.record(conn, previous, dict(kind='relocation_committed', config=config))
            _preserve(run/'workflow'/'relocations'/config['relocated_from']['contract_sha256']/'contract.json', raw)
            w.record(conn, config, dict(kind='initialized', config=config))
            validate_lineage(conn, config)
            _project(contract_path, config)
            return _result(config, replayed=marker is not None)


def _result(config, *, replayed):
    return dict(run_dir=config['run_dir'], run_id=config['run_id'],
                contract_sha256=h.sha(config), relocated_from=config['relocated_from'],
                replayed=replayed, acquisition_repeated=False, publication_performed=False,
                next_command=w.command(config, 'workflow', 'next-task', '--run-dir', config['run_dir']))
