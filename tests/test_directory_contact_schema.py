"""Convert internal display metadata without weakening directory row validation."""
import copy

import pytest

from flwu import workflow_directory as directory
from flwu.directory_display import load_formats


@pytest.mark.parametrize('kind', [None, 'phone', 'email', 'name', 'address', 'note'])
def test_display_type_conversion_preserves_contact_values_and_source(kind, monkeypatch):
    row = dict(label='Contact', lines=['Published value'], href='https://court.example/contact')
    if kind is not None:
        row['type'] = kind
    displayed = dict(office=[row], assistant=[])
    before = copy.deepcopy(displayed)
    monkeypatch.setattr(directory, 'format_contacts', lambda *args: copy.deepcopy(displayed))
    person = dict(id='fixture-person', name='Fixture Person', details={})
    result = directory.contacts(person)['office'][0]
    assert result['lines'] == row['lines'] and result['href'] == row['href']
    assert result.get('type') == (kind if kind in ('address', 'note') else None)
    assert result['label'] == 'Contact'
    assert result['fact_path'] == 'reviewed_person_details'
    assert displayed == before


def test_unknown_display_type_is_rejected_before_a_review_packet(monkeypatch):
    monkeypatch.setattr(directory, 'format_contacts', lambda *args: dict(
        office=[dict(label='Contact', lines=['Published value'], type='unknown-type')], assistant=[]))
    with pytest.raises(ValueError, match='Unsupported directory contact type.*fixture-person.*Contact'):
        directory.contacts(dict(id='fixture-person', name='Fixture Person', details={}))


def test_replacement_after_rows_use_the_same_export_types_without_changing_before_rows(monkeypatch):
    before = dict(label='Old email', lines=['ja@court.example'], href='mailto:ja@court.example')
    after = dict(label='Email', lines=['ja@court.example'], href='mailto:ja@court.example', type='email')
    formats = dict(contact_replacements={'fixture-person': [dict(
        side='assistant', before=[before], after=[after], reason='Explicit reviewed label change.')]})
    snapshot = copy.deepcopy(formats)
    monkeypatch.setattr(directory, 'load_formats', lambda: formats)
    rules = directory.contact_replacements('fixture-person')
    expected = {key: value for key, value in after.items() if key != 'type'}
    assert rules[0]['before'] == [before] and rules[0]['after'] == [expected]
    merged = directory.merge_contacts(dict(office=[], assistant=[before]),
                                      dict(office=[], assistant=[expected]), rules)
    assert merged['assistant'] == [expected]
    assert formats == snapshot


@pytest.mark.parametrize('person_id', [
    'person-clerk-1d4e51176b4e4369', 'person-clerk-da9db5cf75d14d04',
    'person-judge-2f4f9c8357724a55',
])
def test_current_reviewed_rules_emit_only_exportable_row_types(person_id):
    formats = load_formats()
    fields = formats['person_fields'][person_id]
    person = dict(id=person_id, name='Fixture display adapter',
                  details={key: value['value'] for key, value in fields.items()})
    for rows in directory.contacts(person).values():
        assert all(row.get('type') in (None, 'address', 'note') for row in rows)
    for rule in directory.contact_replacements(person_id):
        assert all(row.get('type') in (None, 'address', 'note') for row in rule['after'])
