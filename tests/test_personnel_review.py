import copy
import pytest

from flwu import personnel_review as p


@pytest.mark.parametrize('kind',['judge','clerk'])
def test_new_templates_have_directory_shape_but_no_invented_facts(kind):
    draft = p.new_template(kind)
    labels = (('chambers_phone','chambers_address','assistant_name','assistant_contact')
              if kind=='judge' else ('office_phone','office_address','office_contact'))
    assert draft['key']=='person-<stable-id>' and draft['kind']==kind
    assert draft['expected_version'] is None and draft['citations']==[]
    assert draft['facts']==dict(name='',fields={k:dict(value='',status='unreviewed',citation={}) for k in labels})
    with pytest.raises(ValueError, match='placeholders'): p.validate_finding(draft)
    draft.update(key='person-own-stable-id')
    with pytest.raises(ValueError, match='full name'): p.validate_finding(draft)
    draft['facts']['name'] = 'Supported Person'
    with pytest.raises(ValueError, match='contact citation'): p.validate_finding(draft)
    draft['facts']['fields'] = {}  # Explicitly omit unreviewed contacts, never fake absence.
    p.validate_finding(draft)  # No unsearched not_published contact defaults.
    assert p.new_template(kind)['facts']['name'] == ''
    assert p.new_template(kind)['facts']['fields'][labels[0]]['status'] == 'unreviewed'


def test_role_must_be_explicit_and_existing_template_is_full_deep_copy():
    with pytest.raises(ValueError, match='judge or clerk'): p.new_template('personnel_change')
    prior = dict(key='person-same',kind='judge',expected_version='v3',
                 facts={'name':'Same Person','procedure':{'documents':[{'title':'Keep'}]},
                        'fields':{'chambers_phone':{'value':'123','legacy':True}}},citations=[{'old':'binding'}])
    before = copy.deepcopy(prior)
    result = p.existing_template(prior)
    assert result['facts'] == prior['facts'] and result['expected_version'] == 'v3'
    assert result['key'] == prior['key'] and result['citations'] == []
    result['facts']['procedure']['documents'][0]['title'] = 'Changed'
    assert prior == before
    p.validate_finding(prior, prior=prior)  # Legacy nested fields are not rewritten.
    with pytest.raises(ValueError, match='judge or clerk'):
        p.existing_template(dict(prior,kind='source_inventory'))


@pytest.mark.parametrize('key',['person-<stable-id>','person-','clerk-new','person-has spaces'])
def test_bad_new_identity_rejected(key):
    with pytest.raises(ValueError, match='stable person-'):
        p.validate_finding(dict(key=key,kind='clerk',facts={'name':'Real Person'},citations=[]))


def person(field):
    return dict(key='person-supported',kind='clerk',expected_version=None,
                facts={'name':'Supported Person','fields':{'office_phone':field}},citations=[{'quote':'Bound by source-gate'}])


def test_verified_and_explicit_absence_require_acquired_citation_and_evidence():
    citation = {'quote':'Bound by source-gate'}
    p.validate_finding(person(dict(value='555-0100',status='verified',citation=citation)))
    p.validate_finding(person(dict(value='',status='not_published',citation=citation,
                                   search_log=[{'url':'https://court.gov','terms':['office phone']} ])))


@pytest.mark.parametrize('field',[
    'plain string', {}, {'value':'123','status':'verified'},
    {'value':'123','status':'verified','citation':{}},
    {'value':'123','status':'verified','citation':{'different':'unbound'}},
    {'value':'','status':'verified','citation':{'quote':'Bound by source-gate'}},
    {'value':'   ','status':'verified','citation':{'quote':'Bound by source-gate'}},
    {'status':'not_published','citation':{'quote':'Bound by source-gate'},'search_log':[]},
    {'status':'not_published','citation':{'quote':'Bound by source-gate'},'search_log':'guessed'},
    {'status':'not_published','citation':{'quote':'Bound by source-gate'},'search_log':[None]},
    {'status':'unreviewed','citation':{'quote':'Bound by source-gate'}},
])
def test_malformed_new_contacts_rejected(field):
    with pytest.raises(ValueError): p.validate_finding(person(field))


def test_bad_fields_container_and_named_event_alias_rejected_generic_news_allowed():
    draft = person({});draft['facts']['fields'] = []
    with pytest.raises(ValueError, match='named contact'): p.validate_finding(draft)
    with pytest.raises(ValueError, match='judge or clerk'):
        p.validate_finding(dict(key='event',kind='personnel_change',facts={'name':'Successor'}))
    p.validate_finding(dict(key='event',kind='personnel_change',facts={'summary':'Office announcement'}))
    p.validate_finding(dict(key='rule',kind='court_rule',facts={'name':'Rule title'}))
    p.validate_finding(dict(key='legacy',kind='judge',facts={},citations=[]),prior={'version':'old'})
