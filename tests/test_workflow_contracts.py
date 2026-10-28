"""Task packets state the same bounded editorial choices as domain validation."""
import pytest
from flwu.workflow_contracts import contract


@pytest.mark.parametrize('kind,field,values', [
    ('source_review', 'outcome', ['baseline_reviewed', 'no_relevant_change', 'updated_findings']),
    ('opinion_review', 'relevance', ['relevant', 'not_relevant', 'uncertain']),
    ('publication_mapping', 'decision', ['include', 'include_directory', 'exclude']),
    ('coverage_review', 'decision', ['unavailable', 'scope_excluded']),
])
def test_packet_declares_allowed_choices(kind, field, values):
    template = {field: '', 'candidate': None} if kind == 'publication_mapping' else {field: ''}
    result = contract(kind, template)
    assert result['receipt_schema']['properties'][field]['enum'] == values
    assert result['receipt_schema']['additionalProperties'] is False
    assert template[field] == ''


def test_source_packet_explains_identity_and_template_use():
    notes = contract('source_review', {'outcome': ''})['field_guidance']
    assert any('Copy receipt_template' in note for note in notes)
    assert any('launcher/preflight' in note and 'rather than guessing' in note for note in notes)
