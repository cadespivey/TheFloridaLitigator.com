"""Opt-in, task-bound Python timings. No evidence or answer bodies are recorded."""
from collections import Counter
from contextlib import contextmanager
from contextvars import ContextVar
import os
from pathlib import Path
import time

metrics = ContextVar('review_metrics', default=None)


@contextmanager
def capture(run_dir, action, handle=None):
    if os.environ.get('FLWU_REVIEW_PROFILE') != '1':
        yield
        return
    import cProfile
    import pstats
    from flwu import workflow

    profile = cProfile.Profile()
    counters = Counter()
    token = metrics.set(counters)
    started = time.monotonic_ns()
    status = 'failed'
    try:
        profile.enable()
        yield
        status = 'returned'
    finally:
        profile.disable()
        elapsed = time.monotonic_ns() - started
        metrics.reset(token)
        spans = []
        for (path, _, name), (_, calls, own, total, _) in pstats.Stats(profile).stats.items():
            if Path(path).parent != Path(__file__).parent:
                continue
            spans.append(dict(module=Path(path).stem, function=name, calls=calls,
                              exclusive_seconds=own, inclusive_seconds=total))
        # The run and issued handle identify the measured transition. 'returned'
        # includes checked rejection and unresolved states.
        config = workflow.load(run_dir)
        bounded_handle = handle if isinstance(handle,str) and len(handle)==24 and all(c in '0123456789abcdef' for c in handle) else None
        folder = Path(config['run_dir'])/'workflow'/'profiles'
        workflow.write(folder/f'{started}-{os.getpid()}.json',
                       dict(run_id=config['run_id'], action=action, handle=bounded_handle,
                            outcome=status, elapsed_ns=elapsed, counters=dict(counters),
                            spans=sorted(spans, key=lambda s:-s['inclusive_seconds'])))
