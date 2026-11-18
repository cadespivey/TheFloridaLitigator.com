"""Count substantive handoffs when a finalized fixture reappears in an overlapping window."""
import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from flwu import history, review_transport as transport, update, workflow
from tests.test_inline_review_integration import source_answer
from tests.test_workflow import environment


def review(run):
    state = transport.next_task(run)
    phases = []
    while state['phase'] != 'preview_complete':
        phase = state['phase']
        phases.append(phase)
        if phase == 'source_review':
            value = source_answer()
        elif phase == 'opinion_review':
            value = dict(relevance='relevant', summary='Reviewed civil holding.',
                         holding='Commercial holding.', disposition='Affirmed.', authors=['Example'], evidence=['C1'])
        elif phase == 'publication_acceptance':
            value = dict(decision='approve', reason='Checked the assembled fixture against the source.', corrections=[])
        elif phase == 'publication_verification':
            value = dict(decision='verify', reason='Checked the final text against the source.', corrections=[],
                         results=[dict(item=row['ref'], reason='The cited evidence supports the published holding.')
                                  for row in state['review_card']['evidence']])
        else:
            raise ValueError(phase)
        path = run/'agent-steps'/state['task_handle']/'answer.json'
        workflow.write(path, value)
        state = transport.reply(run, state['task_handle'], path)
        if state.get('answer_failure'):
            raise RuntimeError(state['answer_failure'])
        assert len(phases) <= 24
    return phases


def run_trial(directory):
    run, db, registry, server = environment(directory)
    first = review(run)
    with history.database(db) as conn:
        prepared = next(e for e in reversed(workflow.events(conn, workflow.load(run))) if e['kind']=='report_prepared')
        history.finalize(conn, prepared['capture_id'], Path(prepared['report']), 'Approved fixture baseline.')
    following = directory/'following'
    workflow.initialize(following, db, directory/'registry.json', 'explicit-range', start='2026-10-15', end='2026-10-29')
    with history.database(db) as conn:
        update.run(conn, registry, 'explicit-range', following, start='2026-10-15', end='2026-10-29', fetch=server)
    second = review(following)
    with history.database(db) as conn:
        prepared = next(e for e in reversed(workflow.events(conn, workflow.load(following))) if e['kind']=='report_prepared')
        issue = workflow.read(prepared['public_preview'])
    entries = issue['sections']['case_law']['items']
    assert len(entries) == 1 and 'Reviewed civil holding.' in entries[0]['summary']
    visible = {k:entries[0][k] for k in ('title','summary','publication_date','legal_status','citations')}
    return dict(first_window_cards=first, following_window_cards=second, public_entry=visible,
                human_nudges=0, model_calls=0, final_phase='preview_complete')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    with TemporaryDirectory() as folder:
        result = run_trial(Path(folder))
    args.output.write_text(json.dumps(result, indent=2)+'\n')
