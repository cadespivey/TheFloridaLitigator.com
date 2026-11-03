"""Scope instructions reach every editorial task without rebinding evidence."""
import copy
from pathlib import Path

import pytest

from flwu import workflow as w


@pytest.mark.parametrize('kind', [
    'source_review', 'opinion_review', 'publication_mapping', 'directory_review',
    'directory_removal', 'coverage_review', 'roster_review', 'publication_acceptance',
])
def test_each_returned_guide_exposes_bounded_scope_without_changing_its_contract(tmp_path, kind):
    config = {'run_dir': str(tmp_path / 'run')}
    template = {'source_review': {'outcome': ''}, 'opinion_review': {'relevance': ''},
                'publication_mapping': {'decision': '', 'candidate': None},
                'coverage_review': {'decision': ''}}.get(kind, {})
    task = w.packet(config, kind, 'example', {}, template, 'Review the supplied evidence.')
    before = copy.deepcopy(task)
    returned = w.materialize(config, task)
    guide = w.read(returned['review_guide'])
    scope = guide['research_scope']
    assert scope['policy_path'] == 'docs/workflow/RESEARCH_SCOPE.md'
    assert all(category in scope['purpose'] for category in (
        'case law', 'statutes', 'bar rules', 'court procedural rules', 'personnel'))
    assert scope['task_instruction']
    assert guide['reading_order'][0].startswith('Read research_scope')
    assert task == before == w.read(returned['packet'])
    assert guide['output_contract'] == task['output_contract']
    assert w.read(guide['receipt_template']) == task['receipt_template']
    assert returned['command'] == task['submit_command']


def test_existing_guides_and_packet_are_preserved_when_scope_guide_is_added(tmp_path):
    config = {'run_dir': str(tmp_path / 'run')}
    task = w.packet(config, 'source_review', 'example', {}, {'outcome': ''}, 'Review source.')
    returned = w.materialize(config, task)
    folder = Path(returned['packet']).parent
    preserved = {name: (folder / name).read_bytes() for name in (
        'packet.json', 'review-guide.json', 'review-overview-v1.json',
        'review-overview-v2.json', 'receipt-template.json')}
    assert 'research_scope' not in w.read(folder / 'review-overview-v2.json')
    # Simulate a run predating v3: only the new view is absent, not its evidence.
    Path(returned['review_guide']).unlink()
    assert w.materialize(config, task) == returned
    assert all((folder / name).read_bytes() == raw for name, raw in preserved.items())
    guide = w.read(returned['review_guide'])
    assert guide['research_scope']['task_instruction'].endswith('invent a scope_excluded outcome.')
    assert guide['receipt_template_sha256'] == w.read(folder / 'review-overview-v2.json')['receipt_template_sha256']


def test_scope_guide_cannot_be_silently_replaced(tmp_path):
    config = {'run_dir': str(tmp_path / 'run')}
    task = w.packet(config, 'coverage_review', 'example', {}, {'decision': ''}, 'Review saved failure.')
    returned = w.materialize(config, task)
    Path(returned['review_guide']).write_text('{}')
    with pytest.raises(ValueError, match='Immutable workflow artifact differs: .*review-overview-v3.json'):
        w.materialize(config, task)
