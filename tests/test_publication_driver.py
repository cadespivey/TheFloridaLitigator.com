"""The standard checked route transfers reviewed data without model receipts."""
import copy
import json
from pathlib import Path
import pytest

from flwu import history as h, workflow as w, source_gate as gate
from flwu import publication_driver as driver, workflow_report as report, review_transport as transport
from tests.test_workflow import environment, answer as legacy_answer
from tests.test_inline_review_integration import checked_next, invoke, source_answer
from tests.test_county_directory import supplement, seal

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def pin(monkeypatch):monkeypatch.setattr(w,'ROOT',ROOT)


def reach_approval(tmp_path, *, summary='Reviewed civil holding.'):
    run,db,registry,server=environment(tmp_path)
    state=checked_next(run,tmp_path);phases=[]
    for _ in range(30):
        if state['phase'] not in ('source_review','opinion_review'):break
        phases.append(state['phase'])
        value=(source_answer() if state['phase']=='source_review' else
               dict(relevance='relevant',summary=summary,holding='Commercial holding.',disposition='Affirmed.',authors=['Example'],evidence=['C1']))
        result=invoke(state,value,tmp_path);assert result.returncode==0,result.stderr.decode()
        state=json.loads(result.stdout)
    assert state['phase']=='publication_verification'
    assert state['review_mode']=='inline_answer' and isinstance(state['review_card'],dict)
    return run,db,registry,server,state,phases


def approve(state,tmp_path):
    results = [dict(item=row['ref'], reason='The published fixture text matches the supplied evidence.')
               for row in state['review_card']['evidence']]
    result=invoke(state,dict(decision='verify',reason='Checked final fixture content.',results=results,corrections=[],reviewer='Fixture content reviewer'),tmp_path)
    assert result.returncode==0,result.stderr.decode()
    return json.loads(result.stdout)


def test_inventory_selects_multiline_name_without_rewriting_citation():
    from flwu.research import validate_person_identity
    unrelated=dict(quote='Court contact information',url='https://court.gov/contact')
    citation=dict(quote='Bio\nALBERTO\nRIBAS, JR.\nJudicial Assistant: Kenndrah Stonom',
                  url='https://court.gov/profile',sha256='original',text_sha256='extraction')
    person=dict(key='person-alberto-ribas-jr-source',kind='judge',
                facts=dict(name='Alberto Ribas, Jr.'),citations=[unrelated,citation])
    original=copy.deepcopy(person)
    result=driver._inventory(person,dict(counties=['Broward'],court_ids=['circuit_seventeenth']),{})
    entity=result[0]['facts']['entities'][0]
    assert entity['citation']==citation
    assert entity['name']=='Alberto Ribas, Jr.' and entity['counties']==['Broward']
    validate_person_identity(entity)
    assert person==original


def test_inventory_missing_full_name_fails_with_actionable_error():
    person=dict(key='person-alberto-ribas-jr-source',kind='judge',
                facts=dict(name='Alberto Ribas, Jr.'),
                citations=[dict(quote='Alberto Ribas. Judicial Assistant: Kenndrah Stonom')])
    with pytest.raises(ValueError,match='actual full person name'):
        driver._inventory(person,dict(counties=['Broward'],court_ids=['circuit_seventeenth']),{})


@pytest.mark.parametrize('fields,scope',[
    ({'county':dict(status='verified',value='Citrus')},dict(counties=['Citrus'],court_ids=[])),
    ({'counties':dict(status='verified',value=['Citrus','Marion'])},dict(counties=['Citrus','Marion'],court_ids=[])),
    ({'court_ids':dict(status='verified',value=['dca_first'])},dict(counties=[],court_ids=['dca_first'])),
    ({'county':dict(status='unverified',value='Citrus')},None),
    ({'county':dict(status='verified',value='Citrus'),'counties':dict(status='verified',value=['Marion'])},None),
    ({'counties':dict(status='verified',value='Citrus')},None),
    ({'court_ids':dict(status='verified',value=[''])},None),
])
def test_structured_scope_uses_only_explicit_verified_values(fields,scope):
    finding=dict(facts=dict(fields=fields));before=copy.deepcopy(finding)
    assert driver._reviewed_scope(finding)==scope
    assert finding==before


def test_structured_scope_does_not_override_conflicting_partial_top_level_scope():
    finding=dict(facts=dict(court_ids=['circuit_fifth'],fields={'county':dict(status='verified',value='Citrus')}))
    assert driver._reviewed_scope(finding) is None


@pytest.mark.parametrize('unavailable', [True, False])
def test_coverage_card_preserves_failure_and_support_without_historical_findings(unavailable):
    citation=dict(quote='The requested table failed to load.',url='https://court.gov/rules',
                  sha256='source-hash',text_sha256='text-hash',locator='Rendered page')
    observation=dict(http_status=200,success=False,transport_success=True,
                     error='Required table unavailable',
                     availability_evidence=dict(document_ready_state='complete',case_table_rows=0))
    task=dict(kind='coverage_review',packet_sha256='packet-hash',
              inputs=dict(unavailable=unavailable,task=dict(
                  source_id='source-rules',url='https://court.gov/rules',
                  observation=observation,citations=[citation],reason='retrieval_failed',
                  prior_findings=[dict(facts=dict(summary='Historical finding. '*20000))],
                  review_template=dict(outcome='baseline_reviewed'))),
              receipt_template=dict(task_id='source:source-rules',decision='',reason='',citations=[]))
    original=copy.deepcopy(task)
    bundle=driver.prepare_card(None,task)
    card=bundle['card']
    assert len(json.dumps(card))<5000
    assert card['failure']['unavailable'] is unavailable
    assert card['failure']['task']['observation']==observation
    assert card['evidence']==[dict(id='E1',passage=citation['quote'])]
    assert 'prior_findings' not in card['failure']['task']
    assert 'review_template' not in card['failure']['task']
    assert task==original
    receipt=driver.compile_card(task,bundle,dict(decision='unavailable',
        reason='The recorded browser failure leaves the required table unavailable.',evidence=['E1']))
    assert receipt['decision']=='unavailable' and receipt['citations']==[citation]
    assert receipt['task_id']=='source:source-rules'


def test_checked_route_runs_all_local_stages_with_one_small_content_approval(tmp_path):
    run,db,_,server,state,phases=reach_approval(tmp_path)
    calls=list(server.calls)
    assert not set(phases)&driver.KINDS
    assert set(state['review_card']['answer'])=={'decision','reason','results','corrections'}
    assert 'receipt_template' not in state and len(json.dumps(state['review_card']))<7000
    final=approve(state,tmp_path)
    assert final['phase']=='preview_complete' and final['complete'] and not final['publication_performed']
    assert list(server.calls)==calls
    with h.database(db) as conn:
        events=w.events(conn,w.load(run))
        assert any(e['kind']=='publication_derivation' for e in events)
        assert any(e['kind']=='publication_artifact_checked' for e in events)
        accepted=w.accepted(conn,w.load(run))
        assert any(e['task']['kind']=='publication_mapping' for e in accepted.values())
        assert conn.execute('SELECT count(*) FROM finalized_reports').fetchone()[0]==0
        assert not list(conn.execute('PRAGMA foreign_key_check'))
    replay=approve(state,tmp_path)
    assert replay['phase']=='preview_complete'


def test_content_not_approved_or_missing_source_cannot_finalize(tmp_path):
    run,db,_,_,state,_=reach_approval(tmp_path)
    result=invoke(state,dict(decision='unresolved',reason='A substantive qualification needs correction before publication.',results=[],corrections=[]),tmp_path)
    assert result.returncode==0,result.stderr.decode()
    stopped=json.loads(result.stdout)
    assert stopped['phase']=='publication_exceptions' and not stopped['complete']
    with h.database(db) as conn:
        assert not any(e['kind']=='decision' and e['task']['kind']=='publication_acceptance' for e in w.events(conn,w.load(run)))
        assert h.latest_finalized(conn,'weekly') is None
    assert transport.next_task(run)['phase']=='publication_exceptions'


def test_artifact_damage_blocks_approval_without_attestation(tmp_path):
    run,db,_,_,state,_=reach_approval(tmp_path)
    Path(state['review_card']['site'],'index.html').write_text('damaged site')
    result=invoke(state,dict(decision='approve',reason='Content approved.',results=[],corrections=[]),tmp_path)
    assert result.returncode!=0
    with h.database(db) as conn:
        assert not conn.execute('SELECT 1 FROM publication_acceptances').fetchone() if conn.execute("SELECT 1 FROM sqlite_master WHERE name='publication_acceptances'").fetchone() else True
        assert h.latest_finalized(conn,'weekly') is None


def test_small_correction_appends_revision_and_rebuilds_before_new_approval(tmp_path):
    run,db,_,server,state,_=reach_approval(tmp_path,summary='Overbroad draft needing a record qualification.')
    old_handle=state['task_handle'];entry=state['review_card']['entries'][0]['ref'];calls=list(server.calls)
    fixed='On this record, the court affirmed the commercial holding.'
    value=dict(decision='correct',reason='Retain the express record limit.',results=[],corrections=[dict(entry=entry,summary=fixed,reason='The prior summary omitted the record limitation.')],reviewer='Fixture content reviewer')
    result=invoke(state,value,tmp_path);assert result.returncode==0,result.stderr.decode()
    updated=json.loads(result.stdout)
    assert updated['phase']=='publication_verification' and updated['task_handle']!=old_handle
    assert updated['review_card']['entries'][0]['summary']==fixed
    assert list(server.calls)==calls
    with h.database(db) as conn:
        revisions=[json.loads(r['payload'])['opinion_review'] for r in gate.rows(conn,'weekly') if json.loads(r['payload']).get('opinion_review',{}).get('editorial_revision')]
        assert len(revisions)==1 and revisions[0]['summary']==fixed
        assert h.latest_finalized(conn,'weekly') is None
    assert approve(updated,tmp_path)['phase']=='preview_complete'
    # Exact old correction request can recover after its domain commit.
    replay=invoke(state,value,tmp_path)
    assert replay.returncode==0,replay.stderr.decode()
    assert json.loads(replay.stdout)['phase']=='preview_complete'


@pytest.mark.parametrize('identity',['stable','official_url','multiline','assignment_change','name_only','structured_scope','unsupported_scope','name_case','name_case_only','surname_first','shorter_name','unreviewed_alias','stable_name_change','distinct_middle'])
def test_reviewed_person_and_roster_project_without_directory_or_roster_model_task(tmp_path,supplement,identity):
    supplement['review_status']='reviewed';supplement['review']=dict(reviewed_by='Prior fixture editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Reviewed fixture.')
    if identity=='stable':supplement['people'][0]['legacy_person_id']='person-example-judge'
    if identity in ('shorter_name','unreviewed_alias','stable_name_change','distinct_middle'):supplement['people'][0]['name']='Example Middle Judge'
    if identity=='stable_name_change':supplement['people'][0]['legacy_person_id']='person-example-judge'
    if identity=='unreviewed_alias':supplement.update(review_status='pending',review=None)
    if identity=='surname_first':
        supplement['people'][0]['legacy_person_id']='earlier-source'
        supplement['people'][0]['reviewed_aliases']=[dict(id='earlier-source',name='Example Judge',canonical_name='Example Judge',decision_sha256='a'*64)]
    seal(supplement)
    path=tmp_path/'broward.json';w.write(path,supplement);before=path.read_bytes()
    text=b'Judge Example Judge serves Broward civil court. Chambers phone: 954-555-0200.'
    if identity in ('multiline','name_case','name_case_only'):text=b'Judge EXAMPLE\nJUDGE serves Broward civil court. Chambers phone: 954-555-0200.'
    if identity=='surname_first':text=b'JUDGE, EXAMPLE serves Broward civil court. Chambers phone: 954-555-0200.'
    if identity=='distinct_middle':text=b'Example Other Judge serves Broward civil court. Chambers phone: 954-555-0200.'
    if identity=='assignment_change':text+=b' Assignment: Criminal division.'
    if identity=='unsupported_scope':text+=b' County label: Broward County.'
    if identity in ('official_url','multiline','assignment_change','name_case'):text+=b' Official profile: https://court.example/judge'
    run,db,registry,server=environment(tmp_path,directories=[path],profile=text)
    # Establish reviewed source facts with an explicit named inventory; this is
    # the substantive boundary. Subsequent mechanics must not ask the model again.
    for _ in range(30):
        state=w.inspect(run,emit=True)
        if state['phase'] not in ('source_review','opinion_review'):break
        task=w.read(state['packet'])
        if task['kind']=='source_review' and task['inputs']['url']=='https://court.gov/profile':
            obs=task['inputs']['observation'];ci={k:obs[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')};ci.update(quote=text.decode(),locator='Fixture profile')
            person=dict(key='person-example-judge',kind='judge',facts=dict(name='Example Judge',fields={'chambers_phone':dict(value='954-555-0200',status='verified',citation=ci)}),citations=[ci],expected_version=None)
            if identity in ('official_url','multiline','assignment_change','name_case'):person['facts']['profile_url']='https://court.example/judge'
            if identity in ('name_case','name_case_only'):person['facts'].update(name='EXAMPLE JUDGE',counties=['Broward'],court_ids=['clerk_broward'])
            if identity=='surname_first':person['facts'].update(name='JUDGE, EXAMPLE',counties=['Broward'],court_ids=['clerk_broward'])
            if identity in ('shorter_name','unreviewed_alias','stable_name_change'):person['facts'].update(counties=['Broward'],court_ids=['clerk_broward'])
            if identity=='distinct_middle':person['facts'].update(name='Example Other Judge',counties=['Broward'],court_ids=['clerk_broward'])
            if identity=='assignment_change':person['facts']['assignment']='Criminal division'
            if identity=='structured_scope':person['facts']['fields']['county']=dict(value='Broward',status='verified',citation=ci)
            if identity=='unsupported_scope':person['facts']['fields']['county']=dict(value='Broward County',status='verified',citation=ci)
            if identity=='official_url':person['facts']['fields']['county']=dict(value='Broward',status='verified',citation=ci)
            inventory=dict(key='roster-test',kind='source_inventory',facts=dict(entities=[dict(id='example-judge',name='Example Judge',type='judge',counties=['Broward'],citation=ci)]),citations=[ci],expected_version=None)
            rec=copy.deepcopy(task['receipt_template']);rec.update(reviewer='Fixture source reviewer',summary='Updated chambers phone.',review_scope='One named person',outcome='updated_findings',findings=[person,inventory] if identity=='stable' else [person],support=dict(reason='Current source states this phone.',current=[{k:ci[k] for k in ('sha256','text_sha256','quote','locator')}],previous=[]))
            w.write(state['save_receipt'],rec);w.submit(run,state['packet'],state['save_receipt'])
        else:legacy_answer(run,db,state)
    calls=list(server.calls)
    if identity=='unreviewed_alias':
        with pytest.raises(ValueError,match='Pending county directory requires a preview build'):
            transport.next_task(run)
        assert path.read_bytes()==before and list(server.calls)==calls
        return
    state=transport.next_task(run)
    assert list(server.calls)==calls
    if identity in ('assignment_change','name_only','structured_scope','unsupported_scope','name_case_only','surname_first','shorter_name','stable_name_change','distinct_middle'):
        assert state['phase']==('publication_mapping' if identity in ('name_only','unsupported_scope') else 'directory_review')
        assert path.read_bytes()==before
        with h.database(db) as conn:assert h.latest_finalized(conn,'weekly') is None
        if identity=='distinct_middle':
            result=invoke(state,dict(decision='approve',reason='The different middle names identify distinct fixture people; retain the prior judge and create the reviewed new person.',
                targets=[dict(path=str(path),id=None)],assignment_updates=[]),tmp_path)
            assert result.returncode==0,result.stderr.decode()
            final=json.loads(result.stdout);assert final['phase']=='publication_verification'
            changes=final['review_card']['directory_changes'];assert len(changes)==1 and changes[0]['before'] is None
            assert changes[0]['after']['name']=='Example Other Judge' and 'reviewed_aliases' not in changes[0]['after']
            assert approve(final,tmp_path)['phase']=='preview_complete'
        if identity in ('surname_first','shorter_name','stable_name_change'):
            assert state['review_card']['reviewed_alias_candidates']
            wrong=invoke(state,dict(decision='approve',reason='This unsupported target must be rejected.',
                targets=[dict(path=str(path),id=supplement['people'][1]['id'])],assignment_updates=[]),tmp_path)
            assert b'quoted identity support for both source names' in wrong.stdout
            assert json.loads(wrong.stdout)['phase']!='publication_verification'
            result=invoke(state,dict(decision='approve',reason='Reviewed the acquired alias and prior reviewed identity; this is the same fixture judge.',
                targets=[dict(path=str(path),id=supplement['people'][0]['id'])],assignment_updates=[]),tmp_path)
            assert result.returncode==0,result.stderr.decode()
            final=json.loads(result.stdout);assert final['phase']=='publication_verification'
            changes=final['review_card']['directory_changes'];assert len(changes)==1
            after=changes[0]['after'];old=supplement['people'][0]
            assert after['id']==old['id'] and after['name']==old['name']
            assert after['assignment']==old['assignment'] and after['conflicts']==old['conflicts']
            assert '100 Court Street' in json.dumps(after['contacts'])
            assert all(source in after['sources'] for source in old['sources'])
            aliases={a['id']:a for a in after['reviewed_aliases']}
            assert aliases['person-example-judge']['name']==('JUDGE, EXAMPLE' if identity=='surname_first' else 'Example Judge')
            if identity=='surname_first':
                assert after['legacy_person_id']=='earlier-source'
                assert aliases['earlier-source']==old['reviewed_aliases'][0]
            assert approve(final,tmp_path)['phase']=='preview_complete'
            assert path.read_bytes()==before
        return
    assert state['phase']=='publication_verification'
    changes=state['review_card']['directory_changes'];assert len(changes)==1
    after=changes[0]['after'];assert '954-555-0200' in json.dumps(after['contacts'])
    assert '954-555-0100' not in json.dumps(after['contacts'])
    assert '100 Court Street' in json.dumps(after['contacts'])
    assert after['assignment']==supplement['people'][0]['assignment']
    assert after['id']==supplement['people'][0]['id']
    assert after['name']==supplement['people'][0]['name']
    assert all(source in after['sources'] for source in supplement['people'][0]['sources'])
    with h.database(db) as conn:
        ds=w.accepted(conn,w.load(run));rosters=[d for d in ds.values() if d['task']['kind']=='roster_review'];assert len(rosters)==1
        if identity!='stable':
            reused=[d for d in ds.values() if d['task']['inputs'].get('directory_reuse')]
            assert {d['task']['kind'] for d in reused}==({'directory_review'} if identity=='name_case' else {'publication_mapping','directory_review'})
            if identity!='name_case':
                mapping=next(d for d in reused if d['task']['kind']=='publication_mapping')
                assert mapping['receipt']['inventories'][0]['facts']['court_ids']==['clerk_broward']
    assert path.read_bytes()==before
    assert approve(state,tmp_path)['phase']=='preview_complete'
    assert path.read_bytes()==before


@pytest.mark.parametrize('scope', [dict(counties=[],court_ids=['dca_fifth']),
                                   dict(counties=['Broward'],court_ids=['clerk_broward'])])
@pytest.mark.parametrize('profile', [b'Clerk Jane Smith. Phone: 555-0101.',
                                     b'Clerk JANE\nSMITH. Phone: 555-0101.'])
def test_new_person_missing_scope_returns_small_semantic_card_not_inferred_membership(tmp_path,supplement,scope,profile):
    supplement['review_status']='reviewed'
    supplement['review']=dict(reviewed_by='Fixture editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Reviewed fixture.')
    seal(supplement)
    path=tmp_path/'broward.json';w.write(path,supplement)
    run,db,_,_=environment(tmp_path,directories=[path],profile=profile)
    state=transport.next_task(run)
    # Submit source form through actual checked wrapper.
    person=dict(person='new',name='Jane Smith',kind='clerk',evidence=['C1'],fields={'office_phone':dict(value='555-0101',evidence='C1')})
    result=invoke(state,dict(decision='material_change',summary='Current clerk is Jane Smith.',evidence=['C1'],people=[person]),tmp_path)
    assert result.returncode==0,result.stderr.decode()
    state=json.loads(result.stdout)
    for _ in range(20):
        if state['phase'] not in ('source_review','opinion_review'):break
        value=(source_answer() if state['phase']=='source_review' else dict(relevance='not_relevant',summary='Fixture excluded.',holding='',disposition='Affirmed.',authors=[],evidence=['C1']))
        result=invoke(state,value,tmp_path);assert result.returncode==0,result.stderr.decode();state=json.loads(result.stdout)
    assert state['phase']=='publication_mapping' and state['review_mode']=='inline_answer'
    assert set(state['review_card']['answer'])=={'decision','reason','scope'}
    choices=state['review_card']['scope_choices']
    assert 'Broward' in choices['counties'] and 'clerk_broward' in choices['court_ids']
    assert 'Unknown County' not in choices['counties']
    invalid=invoke(state,dict(decision='include_directory',reason='Invalid scope fixture.',scope=dict(counties=['Unknown County'],court_ids=[])),tmp_path)
    assert b'Choose only the supported county' in invalid.stdout
    assert json.loads(invalid.stdout)['phase']=='publication_mapping'
    result=invoke(state,dict(decision='include_directory',reason='Reviewed clerk scope.',scope=scope),tmp_path)
    assert result.returncode==0,result.stderr.decode();state=json.loads(result.stdout)
    assert state['phase']=='publication_verification'
    assert approve(state,tmp_path)['phase']=='preview_complete'


def test_next_reporting_period_reuses_finalized_baseline_without_republishing(tmp_path):
    from flwu import update
    run,db,registry,server,state,_=reach_approval(tmp_path)
    assert approve(state,tmp_path)['phase']=='preview_complete'
    config=w.load(run)
    with h.database(db) as conn:
        prepared=next(e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared')
        h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Fixture explicitly finalized baseline.')
    second=tmp_path/'following-week'
    w.initialize(second,db,tmp_path/'registry.json','next-week',start='2026-10-23',end='2026-10-29')
    with h.database(db) as conn:update.run(conn,registry,'next-week',second,start='2026-10-23',end='2026-10-29',fetch=server)
    calls=list(server.calls);next_state=transport.next_task(second)
    assert next_state['phase']=='preview_complete' and 'review_card' not in next_state
    assert next_state['review_progress']['remaining_opinion_reviews']==0
    assert w.load(second)['baseline_capture']==prepared['capture_id']
    assert list(server.calls)==calls


def test_unresolved_publication_can_retry_same_checkpoint_with_corrected_answer(tmp_path):
    import shlex,subprocess,os
    run,db,_,_,state,_=reach_approval(tmp_path)
    value=dict(decision='unresolved',reason='Content approval withheld pending clarification.',results=[],corrections=[])
    result=invoke(state,value,tmp_path);assert result.returncode==0,result.stderr.decode()
    stopped=json.loads(result.stdout)
    assert stopped['review_progress']['checkpointed_reviews']==1
    restored=subprocess.run(shlex.split(stopped['retry_command']),cwd=tmp_path,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    assert restored.returncode==0,restored.stderr
    restored=json.loads(restored.stdout)
    assert restored['task_handle']==state['task_handle']
    assert approve(restored,tmp_path)['phase']=='preview_complete'
    with h.database(db) as conn:
        assert not __import__('flwu.workflow_short',fromlist=['unresolved']).unresolved(conn,w.load(run))


def test_derived_decision_commit_recovers_missing_completion_without_duplication(tmp_path,monkeypatch):
    # Finish substantive review through compatibility API, then interrupt the
    # code-owned completion record after the validated mapping has committed.
    run,db,_,_=environment(tmp_path)
    for _ in range(30):
        state=w.inspect(run,emit=True)
        if state['phase'] not in ('source_review','opinion_review'):break
        legacy_answer(run,db,state)
    actual=w.record;crashed=[False]
    def interrupt(conn,config,event):
        if event['kind']=='publication_derivation' and not crashed[0]:
            crashed[0]=True;raise OSError('simulated crash after domain/decision commit')
        return actual(conn,config,event)
    monkeypatch.setattr(w,'record',interrupt)
    with pytest.raises(OSError,match='simulated crash'):transport.next_task(run)
    monkeypatch.setattr(w,'record',actual)
    resumed=transport.next_task(run)
    assert resumed['phase']=='publication_verification'
    with h.database(db) as conn:
        events=w.events(conn,w.load(run));decisions=w.accepted(conn,w.load(run))
        intents=[e for e in events if e['kind']=='publication_derivation_intent']
        completed=[e for e in events if e['kind']=='publication_derivation']
        assert len(intents)==len(completed)
        assert len([d for d in decisions.values() if d['task']['kind']=='publication_mapping'])==1


def test_correction_recovers_crash_after_domain_revision_without_duplicate_revision(tmp_path,monkeypatch):
    run,db,_,_,state,_=reach_approval(tmp_path,summary='Overbroad draft.')
    actual=w.record;crashed=[False]
    def interrupt(conn,config,event):
        if event['kind']=='publication_content_corrected' and not crashed[0]:
            crashed[0]=True;raise OSError('interrupted after opinion revision')
        return actual(conn,config,event)
    monkeypatch.setattr(w,'record',interrupt)
    entry=state['review_card']['entries'][0]['ref'];value=dict(decision='correct',reason='Qualify the rule.',results=[],corrections=[dict(entry=entry,summary='On this record, the commercial holding is affirmed.',reason='Retain record limit.')])
    # In-process reply lets the injected interruption cross the same domain path.
    folder=run/'agent-steps'/'correction-recovery';folder.mkdir(parents=True);path=folder/'answer.json';w.write(path,value)
    with pytest.raises(OSError,match='interrupted'):transport.reply(run,state['task_handle'],path)
    monkeypatch.setattr(w,'record',actual)
    resumed=transport.reply(run,state['task_handle'],path)
    assert resumed['phase']=='publication_verification'
    with h.database(db) as conn:
        revised=[json.loads(r['payload'])['opinion_review'] for r in gate.rows(conn,'weekly') if json.loads(r['payload']).get('opinion_review',{}).get('editorial_revision')]
        assert len(revised)==1
    assert approve(resumed,tmp_path)['phase']=='preview_complete'


def test_missing_legal_metadata_uses_small_card_and_validates_material_change(tmp_path):
    text=b'Prior notice period five days; current notice period ten days. Rule adopted October 18, 2026.'
    run,db,registry,server=environment(tmp_path,profile=text)
    state=transport.next_task(run)
    result=invoke(state,dict(decision='material_change',summary='Civil notice increased from five to ten days.',evidence=['C1'],people=[]),tmp_path)
    assert result.returncode==0,result.stderr.decode();state=json.loads(result.stdout)
    for _ in range(30):
        if state['phase'] not in ('source_review','opinion_review'):break
        value=(source_answer() if state['phase']=='source_review' else dict(relevance='not_relevant',summary='Fixture exclusion.',holding='',disposition='Affirmed.',authors=[],evidence=['C1']))
        result=invoke(state,value,tmp_path);assert result.returncode==0,result.stderr.decode();state=json.loads(result.stdout)
    assert state['phase']=='publication_mapping' and state['review_mode']=='inline_answer'
    candidate=dict(section='procedural_rules',title='Civil notice period',summary='Civil notice increased from five to ten days.',publication_date='2026-10-18',effective_date=None,legal_status='adopted',change_analysis=dict(material=True,previous_requirement='five days',current_requirement='ten days',practical_effect='Allow ten days notice.',basis_quote='current notice period ten days'))
    result=invoke(state,dict(decision='include',reason='Supported procedural change in reporting period.',candidate=candidate),tmp_path)
    assert result.returncode==0,result.stderr.decode();state=json.loads(result.stdout)
    assert state['phase']=='publication_verification'
    assert state['review_card']['entries'][0]['change_analysis']==candidate['change_analysis']
    assert approve(state,tmp_path)['phase']=='preview_complete'
    config=w.load(run)
    with h.database(db) as conn:
        prepared=next(e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared')
        h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Approved fixture baseline.')
    from flwu import update
    def unchanged(url):
        meta,body=server(url)
        return meta,text if url=='https://court.gov/profile' else body
    for ident,start,count in [('explicit-range','2026-10-15',1),('next-week','2026-10-23',0)]:
        following=tmp_path/ident
        w.initialize(following,db,tmp_path/'registry.json',ident,start=start,end='2026-10-29')
        with h.database(db) as conn:update.run(conn,registry,ident,following,start=start,end='2026-10-29',fetch=unchanged)
        # No second source interpretation or metadata drafting for unchanged law.
        next_state=transport.next_task(following)
        assert next_state['phase']=='preview_complete' and 'review_card' not in next_state
        with h.database(db) as conn:
            records = w.events(conn, w.load(following))
            prep = next(e for e in records if e['kind']=='report_prepared')
            payload=json.loads(conn.execute('SELECT payload FROM captures WHERE capture_id=?',(prep['capture_id'],)).fetchone()[0])
            entries=[f['facts'] for f in payload['findings'] if f['kind']=='candidate']
            assert len(entries)==count
            if entries:assert entries[0]['change_analysis']==candidate['change_analysis']


def test_explicit_interval_includes_reviewed_opinion_already_in_finalized_baseline(tmp_path):
    from flwu import update
    run,db,registry,server,state,_=reach_approval(tmp_path)
    approve(state,tmp_path)
    config=w.load(run)
    with h.database(db) as conn:
        prepared=next(e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared')
        h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Approved fixture baseline.')
    following=tmp_path/'explicit-interval'
    w.initialize(following,db,tmp_path/'registry.json','explicit-range',start='2026-10-15',end='2026-10-29')
    with h.database(db) as conn:update.run(conn,registry,'explicit-range',following,start='2026-10-15',end='2026-10-29',fetch=server)
    next_state=transport.next_task(following)
    assert next_state['phase']=='preview_complete' and 'review_card' not in next_state
    with h.database(db) as conn:
        saved = w.events(conn, w.load(following))
        decisions = [e for e in saved if e['kind']=='decision']
        assert not any(e['task']['kind']=='publication_verification' for e in decisions)
        aggregate=next(e for e in decisions if e['task']['kind']=='publication_acceptance')
        assert len(aggregate['task']['inputs']['campaign']['results'])==1
        prepared=next(e for e in saved if e['kind']=='report_prepared')
        issue=w.read(prepared['public_preview'])
        assert 'Reviewed civil holding.' in issue['sections']['case_law']['items'][0]['summary']


def test_current_only_review_preview_does_not_bind_unused_aliases_or_weaken_production(tmp_path,supplement):
    from flwu.site import build_site
    from tests.test_county_directory import identity_archive
    archive,old=identity_archive(tmp_path)
    person=supplement['people'][0];person['legacy_person_id']='outside-this-current-report'
    path=tmp_path/'county.json';w.write(path,seal(supplement))
    # Existing generic/production behavior is unchanged.
    with pytest.raises(ValueError,match='legacy identity mapping'):
        build_site(archive,tmp_path/'generic',preview=True,county_directories=[path])
    with pytest.raises(ValueError,match='restricted'):
        build_site(archive,tmp_path/'production',partial_directory_preview=True,county_directories=[path])
    build_site(archive,tmp_path/'current-preview',preview=True,county_directories=[path],partial_directory_preview=True)
    # An alias that actually participates must still identify the same person.
    person['legacy_person_id']=old['id'];person['name']='Unrelated identity';w.write(path,seal(supplement))
    with pytest.raises(ValueError,match='legacy identity mapping'):
        build_site(archive,tmp_path/'bad-preview',preview=True,county_directories=[path],partial_directory_preview=True)


def test_one_campaign_retains_sound_item_through_named_correction(tmp_path, monkeypatch):
    from tests.test_opinion_discovery import Server, opinion
    server = Server([opinion(1), opinion(2), opinion(3)])
    monkeypatch.setattr('tests.test_workflow.Server', lambda _: server)
    run, db, _, _, state, _ = reach_approval(tmp_path, summary='A broadly stated commercial holding.')
    entries = state['review_card']['entries']
    assert len(entries) == 3
    first, second, third = (entry['ref'] for entry in entries)
    value = dict(decision='verify', reason='Reviewed first item against its acquired text.',
                 results=[dict(item=first, reason='Supported commercial holding and disposition.')], corrections=[])
    result = invoke(state, value, tmp_path)
    assert result.returncode == 0, result.stderr
    remaining = json.loads(result.stdout)
    assert [row['id'] for row in remaining['review_card']['entries']] == [row['id'] for row in entries[1:]]
    retry = invoke(state, value, tmp_path)
    assert retry.returncode == 0 and json.loads(retry.stdout)['task_handle'] == remaining['task_handle']
    second, third = (row['ref'] for row in remaining['review_card']['entries'])
    correction = dict(decision='correct', reason='Narrow the third holding to the actual record.',
                      results=[dict(item=second, reason='The stated result matches the supplied opinion.')],
                      corrections=[dict(entry=third, summary='Commercial holding affirmed on this record.',
                                        reason='The acquired opinion supports this narrower result.')])
    result = invoke(remaining, correction, tmp_path)
    assert result.returncode == 0, result.stderr
    last = json.loads(result.stdout)
    assert len(last['review_card']['entries']) == 1 and last['review_card']['entries'][0]['id'] == entries[-1]['id']
    assert last['review_card']['entries'][0]['summary'] == correction['corrections'][0]['summary']
    assert approve(last,tmp_path)['phase'] == 'preview_complete'
    with h.database(db) as conn:
        events = w.events(conn, w.load(run))
        aggregates = [e for e in events if e['kind']=='decision' and e['task']['kind']=='publication_acceptance']
        assert len(aggregates) == 1 and len(aggregates[0]['task']['inputs']['campaign']['results']) == 3
        assert len([e for e in events if e['kind']=='verified_batch_items']) == 2


def test_rehearsal_reports_both_defects_and_writes_no_acceptance(tmp_path, monkeypatch):
    from tests.test_opinion_discovery import Server, opinion
    server = Server([opinion(1), opinion(2)])
    monkeypatch.setattr('tests.test_workflow.Server', lambda _: server)
    run, db, _, _ = environment(tmp_path)
    state = w.inspect(run, emit=True)
    while state['phase'] in ('source_review','opinion_review'):
        legacy_answer(run, db, state)
        state = w.inspect(run, emit=True)
    config = w.load(run)
    with h.database(db) as conn:
        before = w.events(conn, config)
        def broken(conn, config, task):
            raise ValueError('Malformed projection for '+task['identity'])
        monkeypatch.setattr(driver, 'mapping', broken)
        with pytest.raises(ValueError) as exc:
            driver.rehearse_mappings(conn, config, w.latest_queue(conn,config))
        assert str(exc.value).count('Malformed projection for') == 2
        assert w.events(conn, config) == before
        assert not conn.execute('SELECT 1 FROM finalized_reports').fetchone()


@pytest.mark.parametrize('boundary', ['submission', 'domain_acceptance', 'decision'])
@pytest.mark.parametrize('when', ['before', 'after'])
def test_restart_at_aggregate_boundary_reuses_item_results(tmp_path, monkeypatch, boundary, when):
    from flwu import publication_acceptance as acceptance

    run, db, _, _ = environment(tmp_path)
    state = transport.next_task(run)
    while state['phase'] in ('source_review', 'opinion_review'):
        value = source_answer() if state['phase'] == 'source_review' else dict(
            relevance='relevant', summary='Reviewed civil holding.', holding='Commercial holding.',
            disposition='Affirmed.', authors=['Example'], evidence=['C1'])
        path = run/'agent-steps'/state['task_handle']/'answer.json'
        w.write(path, value)
        state = transport.reply(run, state['task_handle'], path)

    assert state['phase'] == 'publication_verification'
    path = run/'agent-steps'/state['task_handle']/'answer.json'
    w.write(path, dict(decision='verify', reason='Checked final text against the fixture.',
                       results=[dict(item=row['ref'], reason='Supported by cited source.')
                                for row in state['review_card']['evidence']], corrections=[]))

    class Interrupted(Exception):
        pass

    def interrupt(operation):
        def wrapped(*args, **kwargs):
            aggregate = (boundary == 'domain_acceptance' or
                         (args[2].get('kind') == boundary and
                          args[2].get('task', {}).get('kind') == 'publication_acceptance'))
            if aggregate and when == 'before':
                raise Interrupted
            result = operation(*args, **kwargs)
            if aggregate and when == 'after':
                raise Interrupted
            return result
        return wrapped

    with monkeypatch.context() as patches:
        if boundary == 'domain_acceptance':
            patches.setattr(acceptance, 'accept', interrupt(acceptance.accept))
        else:
            patches.setattr(w, 'record', interrupt(w.record))
        with pytest.raises(Interrupted):
            transport.reply(run, state['task_handle'], path)

    assert transport.next_task(run)['phase'] == 'preview_complete'
    with h.database(db) as conn:
        events = w.events(conn, w.load(run))
        for kind in ('publication_verification', 'publication_acceptance'):
            assert sum(e['kind'] == 'decision' and e['task']['kind'] == kind for e in events) == 1
        assert conn.execute('SELECT COUNT(*) FROM publication_acceptances').fetchone()[0] == 1
