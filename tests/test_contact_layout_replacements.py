"""Explicit presentation replacements must not become broad contact deletion."""
import copy
import pytest
from flwu import workflow_directory as d


def example():
    old={'office':[
        {'label':'Phone','lines':['Yulee: (904) 548-4600']},
        {'label':'Phone','lines':['Fernandina Beach: (904) 491-6430']},
        {'label':'Contact','lines':['Public records requests: publicrecordsreq@nassauclerk.com']},
        {'label':'Contact','lines':['Office telephone: (904) 548-4600']},
        {'label':'Address','lines':['Yulee Office (Full Service)','76347 Veterans Way','Yulee, FL 32097',
                                  'Fernandina Beach Office','416 Centre Street','Fernandina Beach, FL 32034'],'type':'address'}],
         'assistant':[]}
    new={'office':[
        {'label':'Yulee phone','lines':['(904) 548-4600'],'type':'phone','href':'tel:9045484600'},
        {'label':'Fernandina beach phone','lines':['(904) 491-6430'],'type':'phone','href':'tel:9044916430'},
        {'label':'Public records email','lines':['publicrecordsreq@nassauclerk.com'],'type':'email','href':'mailto:publicrecordsreq@nassauclerk.com'},
        {'label':'Yulee address','lines':old['office'][4]['lines'][:3],'type':'address'},
        {'label':'Fernandina beach address','lines':old['office'][4]['lines'][3:],'type':'address'}],
         'assistant':[]}
    rule=dict(side='office',before=copy.deepcopy(old['office']),after=copy.deepcopy(new['office']),
              reason='Split both offices and label the published records email without repeating values.')
    return old,new,rule


def test_explicit_relabel_fixes_duplicate_rows_preserving_unmatched_contacts():
    old,new,rule=example();before=copy.deepcopy(old)
    assert len(d.merge_contacts(old,new)['office'])==10  # Reproduces the defect.
    fax={'label':'Fax','lines':['(904) 555-0100']}
    assistant={'label':'Name','lines':['Published assistant']}
    old['office'].append(fax);old['assistant'].append(assistant)
    result=d.merge_contacts(old,new,[rule])
    assert result=={'office':[fax]+new['office'],'assistant':[assistant]}
    assert str(result).count('(904) 548-4600')==1
    assert old['office'][:-1]==before['office']  # Inputs are immutable.
    assert rule['before']==before['office']


@pytest.mark.parametrize('changed',['before','after','href','extra_metadata'])
def test_rule_does_not_follow_changed_old_or_proposed_values(changed):
    old,new,rule=example()
    if changed=='before':old['office'][0]['lines']=['Different office: (904) 555-0200']
    elif changed=='after':new['office'][0]['lines']=['(904) 555-0200']
    elif changed=='href':new['office'][0]['href']='tel:9045550200'
    else:old['office'][0]['purpose']='New independent qualification'
    assert d.merge_contacts(old,new,[rule])==d.merge_contacts(old,new)


def test_only_fact_path_metadata_is_ignored_and_replay_is_idempotent():
    old,new,rule=example()
    for row in old['office']:row['fact_path']='old-source-path'
    for row in new['office']:row['fact_path']='new-source-path'
    result=d.merge_contacts(old,new,[rule])
    assert result==new
    assert d.merge_contacts(result,new,[rule])==result


def test_rules_are_scoped_to_canonical_person(monkeypatch):
    _,_,rule=example()
    monkeypatch.setattr(d,'load_formats',lambda:{'contact_replacements':{'person-clerk-example':[rule]}})
    assert d.contact_replacements('other-person')==[]
    selected=d.contact_replacements('person-clerk-example')
    expected=copy.deepcopy(rule)
    for row in expected['after'][:3]:del row['type']  # Two phones and one email export as ordinary rows.
    assert selected==[expected]
    assert rule['after'][0]['type']=='phone'  # The display configuration remains unchanged.
    selected[0]['before'].clear()
    assert d.contact_replacements('person-clerk-example')[0]['before']


@pytest.mark.parametrize('change',[{'before':[]},{'after':[]},{'reason':''},{'side':'all'},{'extra':True}])
def test_invalid_rule_cannot_wipe_a_contact_side(change):
    old,new,rule=example();rule.update(change)
    with pytest.raises(ValueError,match='Contact replacement'):
        d.merge_contacts(old,new,[rule])
