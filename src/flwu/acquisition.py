"""Process-wide CLI acquisition exclusion and bounded, flushed progress output."""
from contextlib import contextmanager
from pathlib import Path
import fcntl
import json
import os
import sys
import threading
import time
from flwu import history

_local = threading.local()


def progress(phase, **fields):
    reporter = getattr(_local, 'reporter', None)
    if reporter:
        reporter(phase, **fields)


@contextmanager
def acquisition(database, run_id, command, *, heartbeat_seconds=30):
    """One CLI acquisition per canonical DB path; OS releases lock on process exit.

    Never unlink the sidecar: doing so could create independent locked inodes.
    Metadata is diagnostic only, never evidence that a lock is still held.
    """
    db = Path(database or history.default_database()).expanduser().resolve()
    db.parent.mkdir(parents=True, exist_ok=True)
    lock = Path(str(db) + '.acquisition.lock')
    with lock.open('a+') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            handle.seek(0)
            try:
                owner = json.load(handle)
                detail = f"PID {owner.get('pid')}, run {owner.get('run_id')}"
            except (ValueError, OSError):
                detail = 'owner metadata unavailable'
            raise ValueError(f'Acquisition already running for this database ({detail}). Wait for it to exit; do not launch another run or delete the lock file.') from None
        started = time.monotonic()
        state = {'phase': 'starting'}
        mutex = threading.Lock()
        stop = threading.Event()
        def emit(phase, **fields):
            with mutex:
                state.clear()
                state.update(phase=phase, **fields)
                print(json.dumps(dict(event='acquisition_progress', run_id=run_id,
                                      elapsed_seconds=round(time.monotonic()-started, 1), **state)), file=sys.stderr, flush=True)
        def heartbeat():
            while not stop.wait(heartbeat_seconds):
                with mutex:
                    print(json.dumps(dict(event='acquisition_heartbeat', run_id=run_id,
                                          elapsed_seconds=round(time.monotonic()-started, 1), **state)), file=sys.stderr, flush=True)
        previous = getattr(_local, 'reporter', None)
        thread = threading.Thread(target=heartbeat, daemon=True)
        try:
            handle.seek(0); handle.truncate()
            json.dump(dict(pid=os.getpid(), run_id=run_id, command=command,
                           database=str(db), started_at=history.now()), handle)
            handle.flush()
            _local.reporter = emit
            emit('starting')
            thread.start()
            yield
            emit('completed')
        except BaseException:
            emit('interrupted_or_failed')
            raise
        finally:
            stop.set()
            if thread.is_alive():
                thread.join()
            _local.reporter = previous
            fcntl.flock(handle, fcntl.LOCK_UN)
