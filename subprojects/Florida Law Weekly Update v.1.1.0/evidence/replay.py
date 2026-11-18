"""Offline fixed-answer workload. Run with the selected checkout on PYTHONPATH."""
import argparse
from collections import Counter
import cProfile
import hashlib
import json
from pathlib import Path
from contextlib import contextmanager, ExitStack
import platform
import pstats
import resource
import subprocess
import tempfile
import time
from unittest.mock import patch

from flwu import derived_cache, history, review_transport, workflow
from tests.test_inline_review_integration import source_answer
from tests.test_opinion_discovery import Server, opinion, pdf_bytes
from tests.test_workflow import environment


# The PDF bodies, listing notes and answer stream are fixed across checkouts.
CASES = [
    ('qualified', 'Affirmed on this record only.', 'Affirmed'),
    ('qualified', 'Ordinarily notice is required unless waived.', 'Affirmed'),
    ('qualified', 'The panel assumed timeliness without deciding it.', 'Affirmed'),
    ('qualified', 'The panel affirmed only the award of fees.', 'Affirmed'),
    ('excluded', 'Criminal sentencing appeal. Affirmed.', 'Affirmed'),
    ('excluded', 'Affirmed without opinion.', 'Affirmed'),
    ('status', 'Substituted opinion. Earlier opinion withdrawn. Affirmed.', 'Substituted opinion'),
]


class FixtureServer(Server):
    def __init__(self, _):
        super().__init__([opinion(i, note=case[2]) for i, case in enumerate(CASES, 1)])
        self.clamp = len(CASES)
        self.pdfs = {i: pdf_bytes(case[1]) for i, case in enumerate(CASES, 1)}

    def __call__(self, url):
        meta, raw = super().__call__(url)
        if '/content/download/' in url:
            raw = self.pdfs[int(url.split('/content/download/')[1].split('/')[0])]
        meta['retrieved_at'] = '2026-10-22T12:00:00Z'
        return meta, raw


def answer_for(state):
    if state['phase'] == 'source_review':
        return 'source', source_answer()
    card = state['review_card']
    number = int(card['opinion']['case_number'].split('-')[-1])
    category, body, _ = CASES[number - 1]
    assert body in card['evidence'][0]['passage']
    included = category != 'excluded'
    return category, dict(relevance='relevant' if included else 'not_relevant',
                          summary=body, holding=body if included else '',
                          disposition='Affirmed.', authors=[], evidence=['C1'])


def workload(directory):
    started = time.perf_counter()
    with patch('tests.test_workflow.Server', FixtureServer):
        run, db, _, server = environment(directory)
    acquisition = time.perf_counter() - started
    calls = len(server.calls)
    started = time.perf_counter()
    state = review_transport.next_task(run)
    cold_issue = time.perf_counter() - started
    rows = []
    reminders = int(bool(state.get("scope_reminder")))
    for index in range(state['review_progress']['remaining_source_reviews'] + len(CASES)):
        category, answer = answer_for(state)
        started = time.perf_counter()
        path = run / 'agent-steps' / str(index) / 'input.json'
        path.parent.mkdir(parents=True)
        if index == 2:
            resumed = review_transport.next_task(run)
            assert resumed['task_handle'] == state['task_handle']
            reminders += int(bool(resumed.get('scope_reminder')))
        if index == 3:
            workflow.write(path, dict(answer, unexpected_field=True))
            failed = review_transport.reply(run, state['task_handle'], path)
            assert failed['task_handle'] == state['task_handle'] and failed['answer_failure']
            reminders += int(bool(failed.get('scope_reminder')))
        workflow.write(path, answer)
        state = review_transport.reply(run, state['task_handle'], path)
        reminders += int(bool(state.get('scope_reminder')))
        rows.append(dict(category=category, seconds=time.perf_counter() - started,
                         resumed=index == 2, repaired=index == 3))
    assert state['phase'] in ('publication_acceptance', 'publication_verification'), (state['phase'], state.get('review_progress'), rows)
    with history.database(db) as conn:
        decisions = list(workflow.accepted(conn, workflow.load(run)).values())
    accepted = [d for d in decisions if d['task']['kind'] in ('source_review', 'opinion_review')]
    assert len(accepted) == len(rows) and len(server.calls) == calls
    opinions = [d['receipt'] for d in accepted if d['task']['kind'] == 'opinion_review']
    assert Counter((r['summary'], r['relevance']) for r in opinions) == Counter(
        (body, 'not_relevant' if cat == 'excluded' else 'relevant') for cat, body, _ in CASES)
    return dict(acquisition_seconds=acquisition, first_issue_seconds=cold_issue, reviews=rows,
                scope_reminders=reminders, transport_calls=len(rows)+3, rejected_attempts=1, stale_tasks=0,
                bytes_on_disk=sum(p.stat().st_size for p in directory.rglob('*') if p.is_file()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--groups', type=int, default=3)
    parser.add_argument('--profile', action='store_true')
    args = parser.parse_args()
    results = []
    counters = Counter()
    lock = workflow.locked
    @contextmanager
    def timed_lock(*args, **kwargs):
        start = time.perf_counter_ns()
        with lock(*args, **kwargs):
            acquired = time.perf_counter_ns()
            counters['coordinator_lock_wait_ns'] += acquired - start
            try:yield
            finally:counters['coordinator_lock_hold_ns'] += time.perf_counter_ns() - acquired
    cache_get = derived_cache.Cache.get
    def counted_get(*args, **kwargs):
        result = cache_get(*args, **kwargs)
        counters['cache_hit' if result is not None else 'cache_miss'] += 1
        return result
    profiler = cProfile.Profile()
    started = time.perf_counter()
    cpu_start = time.process_time()
    initial_usage = resource.getrusage(resource.RUSAGE_SELF)
    with ExitStack() as stack:
        if args.profile:
            stack.enter_context(patch.object(workflow, 'locked', timed_lock))
            stack.enter_context(patch.object(derived_cache.Cache, 'get', counted_get))
            profiler.enable()
        for _ in range(args.groups):
            with tempfile.TemporaryDirectory() as directory:
                results.append(workload(Path(directory)))
    if args.profile:
        profiler.disable()
    stages = []
    if args.profile:
        for (path, line, name), (primitive, calls, own, total, _) in pstats.Stats(profiler).stats.items():
            if '/src/flwu/' in path and total >= 0.001:
                stages.append(dict(module=Path(path).stem, function=name, calls=calls,
                                   exclusive_seconds=own, inclusive_seconds=total))
    usage = resource.getrusage(resource.RUSAGE_SELF)
    output = dict(disk_input_blocks=usage.ru_inblock-initial_usage.ru_inblock,
                  disk_output_blocks=usage.ru_oublock-initial_usage.ru_oublock,
                  commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python=platform.python_version(), machine=platform.machine(), platform=platform.platform(),
                  implementation_sha256={name:hashlib.sha256((Path(workflow.__file__).parent/name).read_bytes()).hexdigest()
                                         for name in ('review_transport.py','workflow.py','workflow_short.py','publication_driver.py')},
                  cpu_seconds=time.process_time()-cpu_start, counters=counters,
                  groups=results, stages=sorted(stages,key=lambda row:-row['inclusive_seconds']),
                  elapsed=time.perf_counter()-started, peak_rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  human_interventions=0, model_calls=0, workload='fixed answers, in-process Python, fixture server')
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(f'{len(results)} groups, {sum(len(g["reviews"]) for g in results)} accepted reviews, {output["elapsed"]:.2f}s')


if __name__ == '__main__':
    main()
