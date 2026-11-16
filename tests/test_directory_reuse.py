"""Reviewed placement is reusable evidence, never a name-only identity guess."""
import copy
from pathlib import Path

import pytest

from flwu import directory_reuse as reuse, history as h, workflow as w
from tests.test_county_directory import supplement, seal


@pytest.fixture
def reviewed(supplement):
    supplement['review_status']='reviewed'
    supplement['review']=dict(reviewed_by='Fixture editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Reviewed fixture.')
    return seal(supplement)


def finding(**facts):
    return dict(key='source-specific-person',kind='judge',facts=dict(name='Example Judge',**facts),
                citations=[dict(url='https://court.example/judge',quote='EXAMPLE\nJUDGE')])


@pytest.mark.parametrize('stable',[False,True])
def test_proof_preserves_review_and_source_provenance_without_mutating_inputs(reviewed,stable):
    person=finding()
    if stable:
        person['key']=reviewed['people'][0]['id'];person['citations']=[]
    before=copy.deepcopy((person,reviewed))
    proof=reuse.basis(person,{'saved.json':reviewed})
    assert proof['scope']==dict(counties=['Broward'],court_ids=['clerk_broward'])
    match=proof['matches'][0]
    assert match['match']==('stable_id' if stable else 'exact_name_and_official_url')
    assert match['review']==reviewed['review'] and match['directory_sha256']==h.sha(reviewed)
    assert match['person']['sources']==reviewed['people'][0]['sources']
    assert match['person']['source_observation']==reviewed['people'][0]['source_observation']
    assert (person,reviewed)==before


@pytest.mark.parametrize('defect',['name_only','scheme','name','pending','contact','role','level','county','court','duplicate','conflicting_role'])
def test_insufficient_or_conflicting_identity_is_not_reused(reviewed,defect):
    person=finding()
    if defect=='name_only':person['citations']=[]
    elif defect=='scheme':person['citations'][0]['url']='http://court.example/judge'
    elif defect=='name':person['facts']['name']='Example J. Judge'
    elif defect=='pending':reviewed['review_status']='pending_review'
    elif defect=='contact':reviewed['people'][0]['contact_status']='not_verified'
    elif defect=='role':person['facts']['role']='General magistrate'
    elif defect=='level':person['facts']['role']='Circuit judge'
    elif defect=='county':person['facts']['fields']={'county':dict(status='verified',value='Orange')}
    elif defect=='court':person['facts']['court_ids']=['circuit_seventeenth']
    elif defect=='duplicate':reviewed['people'].append(copy.deepcopy(reviewed['people'][0]))
    elif defect=='conflicting_role':person['facts'].update(role='Judge',fields={'role':dict(status='verified',value='Clerk')})
    assert reuse.basis(person,{'saved.json':reviewed}) is None


def test_structured_official_url_and_configured_court_category_support_reuse(reviewed):
    person=finding(role='County court judge',fields={'profile_url':dict(status='verified',value='https://court.example/judge/')})
    person['citations']=[]
    assert reuse.basis(person,{'saved.json':reviewed})['scope']['court_ids']==['clerk_broward']
    person['facts']['fields']['profile_url']['status']='not_verified'
    assert reuse.basis(person,{'saved.json':reviewed}) is None


def test_distinct_ids_require_explicit_stable_identity_for_each_county_copy(reviewed):
    other=copy.deepcopy(reviewed)
    other['people'][0].update(id='second-county-copy',counties=['Baker'])
    values={'one.json':reviewed,'two.json':other}
    assert reuse.basis(finding(),values) is None
    for value in values.values():value['people'][0]['legacy_person_id']='source-specific-person'
    proof=reuse.basis(finding(),values)
    assert proof['scope']['counties']==['Baker','Broward']
    assert len(proof['matches'])==2


def test_changed_reviewed_evidence_invalidates_bound_task(reviewed,tmp_path,monkeypatch):
    path=str(tmp_path/'directory.json');w.write(path,reviewed)
    monkeypatch.setattr(w,'events',lambda *a,**k:[])
    config=dict(directories=[path]);person=finding()
    task=dict(kind='publication_mapping',inputs=dict(finding=person,directory_reuse=reuse.basis(person,{path:reviewed})))
    assert reuse.verify(None,config,task)==task['inputs']['directory_reuse']
    reviewed['people'][0]['assignment']='Changed assignment';seal(reviewed);w.write(path,reviewed)
    with pytest.raises(ValueError,match='reuse evidence changed'):reuse.verify(None,config,task)


def test_exact_integrated_bytes_restore_original_basis_but_later_edits_do_not(reviewed,tmp_path,monkeypatch):
    path=str(tmp_path/'directory.json');after=copy.deepcopy(reviewed)
    after['people'][0]['assignment']='Integrated assignment';seal(after);w.write(path,after)
    intent=dict(files=[dict(destination=path,sha256=h.sha(Path(path).read_bytes()))],directory_inputs={path:reviewed})
    monkeypatch.setattr(w,'events',lambda *a,**k:[intent])
    assert reuse.supplements(None,dict(directories=[path]))[path]==reviewed
    after['people'][0]['assignment']='Later edit';seal(after);w.write(path,after)
    assert reuse.supplements(None,dict(directories=[path]))[path]==after


def test_binding_preserves_previously_accepted_original_task(reviewed,tmp_path):
    config=dict(run_dir=str(tmp_path),database='fixture.sqlite')
    task=w.packet(config,'publication_mapping','person',dict(finding=finding()),dict(decision='',candidate=None),'Fixture instructions')
    proof=reuse.basis(finding(),{'saved.json':reviewed})
    assert reuse.bind(config,task,{task['packet_sha256']:{}},proof) is task
    bound=reuse.bind(config,task,{},proof)
    assert bound['packet_sha256']!=task['packet_sha256']
    assert bound['inputs']['directory_reuse']==proof
    assert bound['receipt_template']==task['receipt_template']
    assert reuse.bind(config,task,{},None) is task
