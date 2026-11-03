"""Provenance-path changes alone must not consume another personnel review."""
import copy
import pytest
from flwu.workflow_directory import same_person_display


@pytest.fixture
def unchanged_display():
    contacts={'office':[dict(label='Phone',lines=['954-555-0100'],href='tel:9545550100',fact_path='contact.phone'),
                        dict(label='Location',lines=['Room 1'],type='note',fact_path='contact.room')],
              'assistant':[dict(label='Email',lines=['ja@example.org'],href='mailto:ja@example.org',fact_path='contact.email')]}
    old=dict(name='Example Person',profile_url='https://court.gov/profile',procedure_url='https://court.gov/guide',contacts=contacts)
    person={k:old[k] for k in ('name','profile_url','procedure_url')}
    proposal=copy.deepcopy(contacts)
    for rows in proposal.values():
        for row in rows:row['fact_path']='reviewed_person_details'
    return old,person,proposal


def test_only_internal_provenance_changes_are_ignored_without_mutation(unchanged_display):
    old,person,proposal=unchanged_display
    before=copy.deepcopy((old,person,proposal))
    assert same_person_display(old,person,proposal,[])
    assert (old,person,proposal)==before


@pytest.mark.parametrize('field',['name','profile_url','procedure_url'])
def test_changed_identity_or_official_link_still_needs_review(unchanged_display,field):
    old,person,proposal=unchanged_display
    person[field]+='-changed'
    assert not same_person_display(old,person,proposal,[])


@pytest.mark.parametrize('change',['value','label','href','type','order','duplicate','other_metadata'])
def test_reader_facing_or_unknown_contact_changes_still_need_review(unchanged_display,change):
    old,person,proposal=unchanged_display
    row=proposal['office'][0]
    if change=='value':row['lines']=['954-555-0200']
    elif change=='label':row['label']='Fax'
    elif change=='href':row['href']='tel:9545550200'
    elif change=='type':row['type']='note'
    elif change=='order':proposal['office'].reverse()
    elif change=='duplicate':proposal['office'].append(copy.deepcopy(row))
    else:row['unrecognized_metadata']='changed'
    assert not same_person_display(old,person,proposal,[])
