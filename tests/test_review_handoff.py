"""The single ordinary command must persist logs/state, including section handoffs."""
import json
import os
import shlex
import subprocess
from pathlib import Path
import pytest

from flwu import history as h, workflow as w, workflow_short as short, source_gate as gate
from tests.test_workflow import environment
from tests import test_opinion_discovery as fixtures


@pytest.fixture(autouse=True)
def selected_checkout(monkeypatch):
    # The launcher intentionally imports the checkout even when CI tests a wheel.
    monkeypatch.setattr(w, 'ROOT', Path(__file__).resolve().parents[1])


def execute(state, outside):
    args = shlex.split(state['command'])
    assert Path(args[1]).name == 'review_step.py'
    assert '-m' not in args  # No competing raw CLI command in the ordinary view.
    result = subprocess.run(args, cwd=outside, capture_output=True, text=True,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    assert result.returncode == 0, result.stderr
    actual = json.loads(result.stdout)
    pointer = json.loads(Path(actual['next_state']).read_text())
    assert pointer == {k: v for k, v in actual.items() if k not in ('next_state', 'logs')}
    assert (Path(actual['logs'])/'answer.json').is_file()
    return actual


def test_returned_command_advances_real_pointer_and_preserves_complete_pca(tmp_path, monkeypatch):
    original = fixtures.pdf_bytes('PER CURIAM. Affirmed.')
    monkeypatch.setattr(fixtures, 'pdf_bytes', lambda: original)
    fixture = tmp_path/"case with ' spaces"; fixture.mkdir()
    run, db, _, server = environment(fixture)
    calls = list(server.calls)
    state = w.inspect(run, emit=True)
    source_total = state['review_progress']['total_sources']
    reviewed = 0
    while state['phase'] in ('source_review', 'opinion_review'):
        card = w.read(state['review_card'])
        if state['phase'] == 'source_review':
            answer = dict(decision='no_material_change', summary='Baseline operating notice reviewed.',
                          evidence=['C1'], people=[])
        else:
            assert 'PER CURIAM. Affirmed.' in card['evidence'][0]['passage']
            # A complete unexplained opinion needs no underlying-merits research.
            answer = dict(relevance='not_relevant', summary='Complete bare PCA; no substantive ruling stated.',
                          holding='', disposition='Affirmed.', authors=[], evidence=['C1'])
        assert 'handoff_text' not in state  # A progress view is not a stop signal.
        w.write(state['save_answer'], answer)
        state = execute(state, tmp_path)
        reviewed += 1
        assert reviewed <= source_total+1
    assert state['phase'] != 'review_exceptions' and not state['complete']
    progress = state['review_progress']
    assert progress['reviewed_sources'] == source_total
    assert progress['pending_sources'] == progress['remaining_opinion_reviews'] == 0
    assert progress['saved_review_decisions'] == reviewed
    assert state['handoff_text'].count('\n') == 4 and len(state['handoff_text'].split()) <= 120
    assert 'Update incomplete' in state['handoff_text']
    assert str(progress['saved_review_decisions']) in state['handoff_text']
    assert list(server.calls) == calls  # All review/summary steps use saved evidence only.
    with h.database(db) as c:
        opinions = [json.loads(row['payload'])['opinion_review'] for row in gate.rows(c, 'weekly')
                    if json.loads(row['payload']).get('opinion_review')]
        assert len(opinions) == 1 and opinions[0]['relevance'] == 'not_relevant'
        assert gate.blob(c, opinions[0]['pdf_sha256']) == original
        assert h.latest_finalized(c, 'weekly') is None


def test_uncertainty_handoff_keeps_exception_counts_and_blocks_completion(tmp_path):
    run, db, _, server = environment(tmp_path)
    state = w.inspect(run, emit=True)
    w.write(state['save_answer'], dict(decision='insufficient_evidence', summary='Assignment cannot be established.',
                                      evidence=[], people=[]))
    state = execute(state, tmp_path)
    for _ in range(24):
        if state['phase'] not in ('source_review', 'opinion_review'):
            break
        answer = (dict(decision='no_material_change', summary='Operating baseline reviewed.', evidence=['C1'], people=[])
                  if state['phase'] == 'source_review' else
                  dict(relevance='uncertain', summary='Substantive significance unresolved.', holding='',
                       disposition='', authors=[], evidence=['C1']))
        w.write(state['save_answer'], answer)
        state = execute(state, tmp_path)
    assert state['phase'] == 'review_exceptions' and state['complete'] is False
    counts = state['review_progress']
    assert counts['checkpointed_reviews'] == 2
    assert counts['pending_sources'] == counts['remaining_opinion_reviews'] == 1
    assert counts['failed_short_answers'] == 0
    assert 'Finalization/publication blocked' in state['handoff_text']
    assert f"Saved review decisions: {counts['saved_review_decisions']}" in state['handoff_text']
    assert len(state['handoff_text'].split()) <= 120
    with h.database(db) as c:
        assert h.latest_finalized(c, 'weekly') is None


def test_checked_command_quotes_paths_and_pins_checkout_and_python(tmp_path, monkeypatch):
    import sys
    root = tmp_path/"checkout with ' quotes"
    monkeypatch.setattr(w, 'ROOT', root)
    config = {'run_dir': str(tmp_path/"run with ' quotes")}
    packet = Path(config['run_dir'])/'packet.json'
    answer = Path(config['run_dir'])/'answer.json'
    args = shlex.split(short.checked_command(config, 'answer', packet=packet, answer=answer))
    assert args[0] == sys.executable
    assert args[args.index('--checkout')+1] == str(root)
    assert args[args.index('--python')+1] == sys.executable
    assert args[args.index('--packet')+1] == str(packet)
    assert args[args.index('--answer')+1] == str(answer)
