import copy
import json
from pathlib import Path

import pytest

from flwu import editorial as e, publication as pub
from flwu.site import build_site
from tests.test_publication import example_issue,archive,seal
from tests.test_source_gate import env,acquire


def test_material_rule_analysis_requires_a_changed_requirement_effect_and_acquired_quote():
    candidate=dict(section='procedural_rules',summary='Responses must now be served on all parties.',change_analysis=dict(
        material=True,previous_requirement='Only the request was described.',current_requirement='The response must be served on all parties.',
        practical_effect='Serve the response on each party.',basis_quote='Responses must be served on all parties.'))
    cites=[dict(quote='(4) Responses must be served on all parties.')]
    e.validate_change(candidate,cites)
    for field in candidate['change_analysis']:
        bad=copy.deepcopy(candidate);bad['change_analysis'][field]=False if field=='material' else ''
        with pytest.raises(ValueError):e.validate_change(bad,cites)
    bad=copy.deepcopy(candidate);bad['change_analysis']['previous_requirement']=bad['change_analysis']['current_requirement']
    with pytest.raises(ValueError,match='unchanged'):e.validate_change(bad,cites)
    with pytest.raises(ValueError,match='exact quotation'):e.validate_change(candidate,[dict(quote='Unrelated source text')])
    with pytest.raises(ValueError):e.validate_change(dict(section='local_rules',summary='Only source hashes differ.'),cites)


@pytest.mark.parametrize('summary',[
    'Research is incomplete; missing findings do not establish no changes.',
    'This is a documented difference between official-source compilations.',
    'Both statements are retained without deciding which source controls.',
])
def test_new_public_rule_summaries_reject_research_process_notices(summary):
    with pytest.raises(ValueError,match='keep research-process notes internal'):
        pub.candidate_summary(dict(summary=summary),'procedural_rules')


def test_exact_issue_exclusion_keeps_original_report_and_dates(tmp_path):
    issue=example_issue();item=copy.deepcopy(issue['sections']['case_law']['items'][0]);item['id']='comparison-only'
    item['summary']='Internal comparison bookkeeping.';issue['sections']['procedural_rules']['items']=[item]
    issue=seal(issue);source=archive(tmp_path,issue);original=(source/(issue['id']+'.json')).read_bytes()
    folder=source/'editorial';folder.mkdir();record=dict(issue_id=issue['id'],content_sha256=issue['content_sha256'],
        reviewer='Fixture editor',reviewed_at='2026-11-04T12:00:00Z',excluded_items=[dict(id=item['id'],reason='No supported material rule change')])
    (folder/'exclusion.json').write_text(json.dumps(record))
    built=build_site(source,tmp_path/'site',preview=True);data=json.loads(next((built/'assets').glob('archive-*.json')).read_text());projected=data['issues'][0]
    assert projected['sections']['procedural_rules']['items']==[]
    assert len(projected['sections']['case_law']['items'])==1
    assert projected['published_at']==issue['published_at'] and projected['provenance']==issue['provenance']
    assert projected['content_sha256']!=issue['content_sha256']
    pub.validate_issue(projected,preview=True)
    assert (source/(issue['id']+'.json')).read_bytes()==original
    assert 'No supported material rule change' not in json.dumps(data)
    for text in ('Research is incomplete','No items included in this reviewed section','missing findings do not establish'):
        assert text not in (built/'assets/search.js').read_text()
    record['content_sha256']='0'*64;(folder/'exclusion.json').write_text(json.dumps(record))
    with pytest.raises(ValueError,match='exact issue'):build_site(source,tmp_path/'bad',preview=True)


def test_review_html_never_inserts_completion_notices_or_empty_section_boilerplate():
    from flwu.workflow_report import render
    html=render({},dict(bounds=dict(start='2026-10-26',end='2026-11-01'),acquisition_complete=False)).decode()
    assert '<h2>Procedural Rules</h2>' in html
    assert 'incomplete' not in html.lower() and 'limitations' not in html.lower()


def test_mapping_validator_enforces_materiality_with_real_acquired_citation(env):
    from flwu import source_gate as gate,workflow_report as report
    conn,registry,_=env;result,_=acquire(env,'materiality',page=b'New requirement: serve the response on every party.')
    observation=result['tasks'][0]['observation']
    cite={k:observation[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')}
    cite.update(quote='New requirement: serve the response on every party.',locator='Fixture requirement')
    finding=dict(key='rule',kind='court_rule',facts={},citations=[cite])
    requirement=dict(finding=finding,version='version',sha256=observation['sha256'],summary=None)
    receipt=report.mapping_template('source:rule',requirement)
    receipt.update(decision='include',reason='Fixture rule has a changed service requirement.',candidate=dict(
        section='procedural_rules',title='Response service',summary='Serve the response on every party.'))
    task=dict(kind='publication_mapping',identity='source:rule',inputs=requirement,receipt_template=copy.deepcopy(receipt))
    with pytest.raises(ValueError,match='change_analysis'):
        report.validate_decision(conn,dict(registry=registry),task,receipt)
    receipt['candidate']['change_analysis']=dict(material=True,previous_requirement='Only requests were specified.',
        current_requirement='Responses must also be served.',practical_effect='Serve the response on every party.',
        basis_quote='serve the response on every party.')
    assert report.validate_decision(conn,dict(registry=registry),task,receipt)['validated']=='publication_mapping'
    receipt['candidate']['change_analysis']['material']=False
    with pytest.raises(ValueError,match='change_analysis'):
        report.validate_decision(conn,dict(registry=registry),task,receipt)
