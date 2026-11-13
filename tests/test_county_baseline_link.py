"""Pinned county evidence is comparison input, not an invented gate review."""
import copy
import json
from pathlib import Path

import pytest
from flwu import history as h, source_gate as gate, county_baseline_link as link
from flwu import county_directory, compact_review, workflow as w
from tests.test_source_gate import env, acquire, receipt
from tests.test_county_directory import seal


def county(conn, folder, *, raw=b'Profile', url='https://court.gov/judge', suffix='one', quote='Profile'):
    text, _, _ = gate.extract(raw, dict(url=url,content_type='text/plain'))
    cite=dict(url=url,sha256=h.sha(raw),text_sha256=h.sha(text.encode()),quote=quote,
              locator='Profile',retrieved_at='2026-10-01T12:00:00Z',http_status=200,authority='official',synthetic=False)
    facts=dict(name='Example Judge',role='County Judge',county='baker',profile_url=url,procedure_url=url,
               contact=dict(phone='555-0100'),procedure_checklist={'scheduling':{'status':'reviewed','summary':'Email chambers.'}})
    finding=dict(key='example',kind='county_judge_baseline',facts=facts,citations=[cite])
    stream='county-'+suffix
    saved=h.record(conn,stream=stream,mode='manual_research',scope=dict(profile='county-baseline-v1',county='baker'),
        run_id='old',recorded_at='2026-10-01T13:00:00Z',
        payload=dict(status='incomplete',contract={},findings=[finding],drafts=[],checks=[]),
        artifacts={h.sha(raw):raw,h.sha(text.encode()):text.encode()})
    observation=dict(capture_seq=saved['seq'],capture_id=saved['capture_id'],recorded_at=saved['recorded_at'])
    packet=dict(scope=dict(county='baker'),stream=stream,
        through_capture=dict(seq=saved['seq'],capture_id=saved['capture_id'],recorded_at=saved['recorded_at'],research_status='incomplete'),
        entities=[dict(entity_key='example',kind=finding['kind'],facts=facts,citations=[cite],observation=observation)])
    data,_=county_directory.make_supplement(packet,[dict(group_id='county_baker',category='County Courts',label='Baker County',url='https://court.gov/')])
    data.update(review_status='reviewed',review=dict(reviewed_by='Fixture reviewer',reviewed_at='2026-10-01T14:00:00Z',attestation='Reviewed saved contact and practical procedures.'))
    seal(data);path=folder/('county-'+suffix+'.json');path.write_text(json.dumps(data))
    return path,data,cite


def config(r, path, run_id='one'):
    return dict(registry=r,run_id=run_id,directories=[str(path)])


def test_identical_raw_preserves_bounded_review_without_fabricating_receipts(env):
    c,r,p=env;path,data,cite=county(c,p);acquire(env,'one')
    original=gate.observations(c,r['stream'])[0];before=gate.reviews(c,r['stream'])
    result=link.ensure(c,config(r,path));assert len(result['references'])==1
    q=gate.queue(c,r);proof=q['reused_reviews'][0]
    assert proof['reuse_basis']=='county_baseline_exact_bytes'
    assert proof['county_baseline_proof']['reference']['review']['finding_capture']==data['people'][0]['source_observation']
    assert gate.reviews(c,r['stream'])==before
    assert c.execute('SELECT count(*) FROM finalized_reports').fetchone()[0]==0
    saved=json.loads(c.execute('SELECT payload FROM captures WHERE capture_id=?',(original['capture_id'],)).fetchone()[0])['source_gate']
    assert saved['change']=='new' and saved['previous_sha256'] is None
    assert link.ensure(c,config(r,path))==result
    assert len(q['tasks'])==1 and q['tasks'][0]['url'].endswith('procedure.pdf')


def test_changed_source_gets_bound_previous_passage_and_actual_diff(env):
    c,r,p=env;path,_,_=county(c,p);acquire(env,'one',page=b'Profile\nNew deadline: ten days.')
    link.ensure(c,config(r,path));q=gate.write_queue(c,r,p/'queue')
    t=next(t for t in q['tasks'] if t['url'].endswith('judge'))
    assert t['reason']=='changed' and t['observation']['acquired_change']=='new'
    assert Path(t['previous_path']).read_bytes()==b'Profile'
    task=next(w.tasks(c,{'run_dir':str(p/'run')},{'source_reviews':q,'opinion_reviews':{'tasks':[]}}))
    card=compact_review.prepare(c,task)
    assert not card['exception'] and card['card']['source_context']['purpose']=='comparison'
    assert {e['side'] for e in card['card']['evidence']}=={'current','previous'}
    assert card['bindings']['P1']['retrieved_at']=='2026-10-01T12:00:00Z'


@pytest.mark.parametrize('damage',['raw','text','quote','capture','pending'])
def test_missing_or_unapproved_evidence_does_not_create_reuse(env,damage):
    c,r,p=env;path,data,cite=county(c,p,quote='Absent' if damage=='quote' else 'Profile');acquire(env,'one',page=b'Current')
    if damage in ('raw','text'):
        c.execute('DELETE FROM artifacts WHERE sha256=?',(cite['sha256' if damage=='raw' else 'text_sha256'],));c.commit()
    if damage=='capture':data['people'][0]['source_observation']['capture_id']='0'*64
    if damage=='pending':data.update(review_status='pending',review=None)
    if damage in ('capture','pending'):
        seal(data);path.write_text(json.dumps(data))
    if damage=='pending':
        with pytest.raises(ValueError):link.ensure(c,config(r,path))
    else:
        result=link.ensure(c,config(r,path));assert result['failures'] and not result['references']
    assert not gate.queue(c,r)['reused_reviews']


def test_existing_accepted_review_and_failed_current_source_are_preserved(env):
    c,r,p=env;path,_,_=county(c,p);q,_=acquire(env,'one')
    gate.accept(c,r,receipt(q['tasks'][0],r,c));assert not link.ensure(c,config(r,path))['references']
    acquire(env,'two',failures=[r['sources'][0]['url']])
    assert not link.ensure(c,config(r,path,'two'))['references']
    assert gate.queue(c,r)['tasks'][0]['reason']=='retrieval_failed'


def test_nonprimary_citation_does_not_bridge(env):
    c,r,p=env;path,data,_=county(c,p)
    data['people'][0]['profile_url']='https://court.gov/elsewhere';data['people'][0]['procedure_url']='https://court.gov/elsewhere'
    seal(data);path.write_text(json.dumps(data));acquire(env,'one')
    assert not link.ensure(c,config(r,path))['references']


def test_county_evidence_newer_than_current_capture_does_not_bridge(env):
    c,r,p=env;path,_,_=county(c,p)
    def fetch(url):
        return dict(url=url,resolved_url=url,retrieved_at='2026-09-01T12:00:00Z',
            success=True,http_status=200,content_type='text/plain'),b'Profile'
    gate.run(c,r,'early',fetch=fetch)
    assert not link.ensure(c,config(r,path))['references']
    assert not gate.queue(c,r)['reused_reviews']


def test_changed_redirect_cannot_reuse_county_review(env):
    c,r,p=env;path,_,_=county(c,p)
    def fetch(url):
        return dict(url=url,resolved_url='https://court.gov/replacement',retrieved_at=h.now(),
            success=True,http_status=200,content_type='text/plain'),b'Profile'
    gate.run(c,r,'redirect',fetch=fetch);link.ensure(c,config(r,path))
    assert not gate.queue(c,r)['reused_reviews']


def test_changed_bytes_equal_text_is_not_automatic_reuse(env):
    c,r,p=env
    path,_,_=county(c,p,raw=b'<html><body>Profile</body></html>')
    def fetch(url):
        return dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,content_type='text/html'),b'<html><body class="new">Profile</body></html>'
    gate.run(c,r,'one',fetch=fetch);link.ensure(c,config(r,path))
    q=gate.queue(c,r)
    assert not q['reused_reviews']
    assert q['tasks'][0]['raw_comparison_basis']


def test_standard_workflow_wires_bridge_before_source_review(tmp_path):
    from tests.test_workflow import environment
    with h.database(tmp_path/'db.sqlite') as c:
        path,_,_=county(c,tmp_path,url='https://court.gov/profile')
    run,db,r,_=environment(tmp_path,directories=[path],profile=b'Profile')
    state=w.inspect(run,emit=True)
    with h.database(db) as c:
        assert link.bindings(c,r['stream'])
        queue=w.latest_queue(c,w.load(run))
        assert any(x.get('reuse_basis')=='county_baseline_exact_bytes' for x in queue['source_reviews']['reused_reviews'])
        assert not gate.reviews(c,r['stream'])
    assert state['phase']!='publication_complete'


def test_hash_match_uses_saved_reviewed_extraction_without_reparsing(env,monkeypatch):
    c,r,p=env;path,_,_=county(c,p);acquire(env,'one')
    monkeypatch.setattr(gate,'extract',lambda *a:pytest.fail('Identical county bytes reparsed'))
    result=link.ensure(c,config(r,path))
    assert result['references'][0]['previous']['extraction']=='reviewed-county-extraction'
    assert gate.queue(c,r)['reused_reviews'][0]['reuse_basis']=='county_baseline_exact_bytes'


def test_distinct_person_stream_is_bound_by_capture_not_name(env):
    c,r,p=env;path,data,_=county(c,p)
    saved=h.record(c,stream='new-directory',mode='manual_research',scope={'profile':'test'},run_id='new',
        payload=dict(status='incomplete',contract={},findings=[],checks=[],drafts=[]),artifacts={})
    data['stream']='new-directory';data['through_capture']=dict(seq=saved['seq'],capture_id=saved['capture_id'],recorded_at=saved['recorded_at'],research_status='incomplete')
    seal(data);path.write_text(json.dumps(data));acquire(env,'one')
    ref=link.ensure(c,config(r,path))['references'][0]
    assert ref['review']['stream']=='county-one'
    assert ref['review']['finding_capture']==data['people'][0]['source_observation']


def test_dry_run_does_not_write_binding_or_derivatives(env):
    c,r,p=env;path,_,_=county(c,p);acquire(env,'one')
    before=c.total_changes
    result=link.ensure(c,config(r,path),dry_run=True)
    assert result['references'] and c.total_changes==before and not link.bindings(c,r['stream'])
