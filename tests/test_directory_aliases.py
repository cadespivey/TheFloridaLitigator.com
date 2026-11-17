"""Explicit aliases preserve identities without automatic name equivalence."""
import copy
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from flwu import county_directory as cd
from flwu.site import build_site
from tests.test_county_directory import supplement, seal, identity_archive


@pytest.mark.parametrize('left,right,expected',[
    ('BAKER, MICHELLE VITT','Michelle Vitt Baker',True),
    ('BALLOU, TESHA','Tesha Scolaro Ballou',True),
    ('Adam Lee','Adam J. Lee',True),
    ('John L. Smith','John T. Smith',True),  # Candidate only; a person must decide.
    ('John Smith, Jr.','John Smith, Sr.',True),
    ('Jane Smith','John Smith',False),
    ('John Smith','John Jones',False),
    ('Judge','Other Judge',False),
])
def test_candidate_names_are_only_a_review_prompt(left,right,expected):
    assert cd.identity_candidate(left,right)==expected
    if expected and left!=right:assert cd.name_key(left)!=cd.name_key(right)


@pytest.mark.parametrize('damage',['canonical','missing_decision','duplicate','own_id'])
def test_invalid_alias_provenance_fails_supplement_validation(supplement,damage):
    person=supplement['people'][0]
    alias=dict(id='reviewed-source-person',name='JUDGE, EXAMPLE',canonical_name=person['name'],decision_sha256='a'*64)
    person['reviewed_aliases']=[alias]
    if damage=='canonical':alias['canonical_name']='Another Judge'
    if damage=='missing_decision':alias['decision_sha256']=''
    if damage=='duplicate':person['reviewed_aliases'].append(copy.deepcopy(alias))
    if damage=='own_id':alias['id']=person['id']
    with pytest.raises(ValueError,match='alias binding'):
        cd.validate_supplement(seal(supplement),preview=True)


@pytest.mark.parametrize('shared',[False,True])
def test_site_checks_explicit_alias_name_and_county(supplement,tmp_path,shared):
    archive,old=identity_archive(tmp_path,shared=shared)
    supplement['county']=old['counties'][0]
    for person in supplement['people']:person['counties']=[supplement['county']]
    person=supplement['people'][0]
    alias=dict(id=old['id'],name=old['name'],canonical_name=person['name'],decision_sha256='a'*64)
    person['reviewed_aliases']=[alias]
    path=tmp_path/'scoped.json'
    def write():path.write_text(json.dumps(seal(supplement)))
    write();build_site(archive,tmp_path/'valid',preview=True,county_directories=[path])
    alias['name']='Not the acquired source name'
    write()
    with pytest.raises(ValueError,match='legacy identity mapping'):
        build_site(archive,tmp_path/'wrong-source-name',preview=True,county_directories=[path])
    alias['name']=old['name'];supplement['county']='Broward'
    for row in supplement['people']:row['counties']=['Broward']
    write()
    with pytest.raises(ValueError,match='legacy identity mapping'):
        build_site(archive,tmp_path/'wrong-county',preview=True,county_directories=[path])


def test_multiple_source_aliases_do_not_duplicate_current_rows_or_change_history():
    node=shutil.which('node')
    if not node:pytest.skip('Node required for actual directory selection')
    script=r'''
const assert=require('node:assert/strict');
const {countyDirectoryView}=require(process.argv[1]);
const one={id:'source-one',name:'BAKER, MICHELLE VITT',counties:['Brevard'],court_ids:['county_brevard']};
const two={id:'source-two',name:'Michelle Vitt Baker',counties:['Brevard','Seminole'],court_ids:[]};
const person={id:'saved-baker',name:'Michelle Vitt Baker',kind:'Judge',counties:['Brevard'],court_ids:['county_brevard'],
 legacy_person_id:'source-one',reviewed_aliases:[{id:'source-one'},{id:'source-two'}],
 contacts:{office:['saved office']},sources:[],contact_notes:[],source_observation:{capture_seq:2}};
const snapshot={directory:[one,two]},savedContacts={'source-one':['old one'],'source-two':['old two']};
const supplement={county:'Brevard',people:[person]},before=JSON.stringify([snapshot,supplement,savedContacts]);
const current=countyDirectoryView(snapshot,'',[supplement],savedContacts);
assert.equal(current.entries.length,2);
assert(!current.entries.some(p=>p.id==='source-one'));
assert.deepEqual(current.entries.find(p=>p.id==='source-two').counties,['Seminole']);
assert.equal(current.entries.filter(p=>p.counties.includes('Brevard')).length,1);
assert.deepEqual(current.contacts['saved-baker'],person.contacts);
for(const query of ['?issue=old','?from=2026-01-01&to=2026-01-02']){
 const historical=countyDirectoryView(snapshot,query,[supplement],savedContacts);
 assert.deepEqual(historical.entries,[one,two]);assert.deepEqual(historical.contacts,savedContacts);
}
assert.equal(JSON.stringify([snapshot,supplement,savedContacts]),before);
'''
    subprocess.run([node,'-e',script,str(Path('src/flwu/data/web/search.js').resolve())],check=True,capture_output=True,text=True)
