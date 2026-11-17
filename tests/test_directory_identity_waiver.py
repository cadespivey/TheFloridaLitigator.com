"""A frozen user mapping waiver cannot waive source or publication integrity."""
import copy
import pytest
from flwu import history as h,workflow as w,workflow_directory as directory
from tests.test_directory_citation_index import directory_review,acquired

CONFIG={'registry':{'stream':'report'}}

def record_waiver(conn,task,receipt,**changes):
    event=dict(kind='directory_identity_verification_waiver',scope='alias_name_correspondence_only',
               authorized_by='user',user_instruction='Run these saved mappings without verification.',
               mappings=[dict(task_sha256=h.sha(task),receipt_sha256=h.sha(receipt),targets=copy.deepcopy(receipt['targets']))])
    event.update(changes)
    w.record(conn,CONFIG,event)
    return h.sha(event)

def alias(task):
    task['inputs']['exact_matches']=[]
    task['inputs']['person']['name']='Judge Person'

def test_waiver_is_explicit_frozen_and_honestly_reported(directory_review,tmp_path):
    path,task,receipt=directory_review;alias(task)
    with h.database(tmp_path/'history.sqlite') as conn:
        with pytest.raises(ValueError,match='quoted identity support'):
            directory.validate_decision(conn,CONFIG,task,receipt)
        digest=record_waiver(conn,task,receipt)
        result=directory.validate_decision(conn,CONFIG,task,receipt)
        assert result['identity_verification']=='waived_by_user'
        assert result['identity_waiver_sha256']==digest
        changed=copy.deepcopy(receipt);changed['reason']='Changed mapping receipt'
        with pytest.raises(ValueError,match='quoted identity support'):
            directory.validate_decision(conn,CONFIG,task,changed)
        changed_task=copy.deepcopy(task);changed_task['inputs']['person']['name']='Different Person'
        with pytest.raises(ValueError,match='quoted identity support'):
            directory.validate_decision(conn,CONFIG,changed_task,receipt)
        with pytest.raises(ValueError,match='quoted identity support'):
            directory.validate_decision(conn,{'registry':{'stream':'other'}},task,receipt)

@pytest.mark.parametrize('changes',[{'authorized_by':'code'},{'user_instruction':''},{'scope':'all_checks'}])
def test_generic_or_wrong_scope_event_is_not_a_waiver(directory_review,tmp_path,changes):
    _,task,receipt=directory_review;alias(task)
    with h.database(tmp_path/'history.sqlite') as conn:
        record_waiver(conn,task,receipt,**changes)
        with pytest.raises(ValueError,match='quoted identity support'):
            directory.validate_decision(conn,CONFIG,task,receipt)

@pytest.mark.parametrize('damage',['directory','target','scope','citation','assignment'])
def test_waiver_preserves_other_publication_checks(directory_review,tmp_path,damage):
    path,task,receipt=directory_review;alias(task)
    with h.database(tmp_path/'history.sqlite') as conn:
        if damage=='target':receipt['targets'][0]['id']='missing-target'
        elif damage=='scope':receipt['targets']=[]
        elif damage=='citation':
            cite=acquired(conn);cite['quote']='Invented evidence';receipt['identity_citations']=[cite]
        elif damage=='assignment':
            receipt['assignment_updates']=[dict(path=str(path),value='Unverified assignment',reason='Fixture',citations=[])]
        record_waiver(conn,task,receipt)
        if damage=='directory':w.write(path,{'people':[]})
        with pytest.raises(ValueError):directory.validate_decision(conn,CONFIG,task,receipt)
