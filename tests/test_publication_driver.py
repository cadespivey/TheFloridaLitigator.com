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
    assert state['phase']=='publication_acceptance'
    assert state['review_mode']=='inline_answer' and isinstance(state['review_card'],dict)
    return run,db,registry,server,state,phases


def approve(state,tmp_path):
    result=invoke(state,dict(decision='approve',reason='Reviewed current publication text; approved without new legal interpretation.',corrections=[],reviewer='Fixture content reviewer'),tmp_path)
    assert result.returncode==0,result.stderr.decode()
    return json.loads(result.stdout)


def test_checked_route_runs_all_local_stages_with_one_small_content_approval(tmp_path):
    run,db,_,server,state,phases=reach_approval(tmp_path)
    calls=list(server.calls)
    assert not set(phases)&driver.KINDS
    assert set(state['review_card']['answer'])=={'decision','reason','corrections'}
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
    result=invoke(state,dict(decision='unresolved',reason='A substantive qualification needs correction before publication.',corrections=[]),tmp_path)
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
    result=invoke(state,dict(decision='approve',reason='Content approved.',corrections=[]),tmp_path)
    assert result.returncode!=0
    with h.database(db) as conn:
        assert not conn.execute('SELECT 1 FROM publication_acceptances').fetchone() if conn.execute("SELECT 1 FROM sqlite_master WHERE name='publication_acceptances'").fetchone() else True
        assert h.latest_finalized(conn,'weekly') is None


def test_small_correction_appends_revision_and_rebuilds_before_new_approval(tmp_path):
    run,db,_,server,state,_=reach_approval(tmp_path,summary='Overbroad draft needing a record qualification.')
    old_handle=state['task_handle'];entry=state['review_card']['entries'][0]['ref'];calls=list(server.calls)
    fixed='On this record, the court affirmed the commercial holding.'
    value=dict(decision='correct',reason='Retain the express record limit.',corrections=[dict(entry=entry,summary=fixed,reason='The prior summary omitted the record limitation.')],reviewer='Fixture content reviewer')
    result=invoke(state,value,tmp_path);assert result.returncode==0,result.stderr.decode()
    updated=json.loads(result.stdout)
    assert updated['phase']=='publication_acceptance' and updated['task_handle']!=old_handle
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


def test_reviewed_person_and_roster_project_without_directory_or_roster_model_task(tmp_path,supplement):
    supplement['review_status']='reviewed';supplement['review']=dict(reviewed_by='Prior fixture editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Reviewed fixture.')
    supplement['people'][0]['legacy_person_id']='person-example-judge';seal(supplement)
    path=tmp_path/'broward.json';w.write(path,supplement);before=path.read_bytes()
    text=b'Judge Example Judge serves Broward civil court. Chambers phone: 954-555-0200.'
    run,db,registry,_=environment(tmp_path,directories=[path],profile=text)
    # Establish reviewed source facts with an explicit named inventory; this is
    # the substantive boundary. Subsequent mechanics must not ask the model again.
    for _ in range(30):
        state=w.inspect(run,emit=True)
        if state['phase'] not in ('source_review','opinion_review'):break
        task=w.read(state['packet'])
        if task['kind']=='source_review' and task['inputs']['url']=='https://court.gov/profile':
            obs=task['inputs']['observation'];ci={k:obs[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')};ci.update(quote=text.decode(),locator='Fixture profile')
            person=dict(key='person-example-judge',kind='judge',facts=dict(name='Example Judge',fields={'chambers_phone':dict(value='954-555-0200',status='verified',citation=ci)}),citations=[ci],expected_version=None)
            inventory=dict(key='roster-test',kind='source_inventory',facts=dict(entities=[dict(id='example-judge',name='Example Judge',type='judge',counties=['Broward'],citation=ci)]),citations=[ci],expected_version=None)
            rec=copy.deepcopy(task['receipt_template']);rec.update(reviewer='Fixture source reviewer',summary='Updated chambers phone.',review_scope='One named person',outcome='updated_findings',findings=[person,inventory],support=dict(reason='Current source states this phone.',current=[{k:ci[k] for k in ('sha256','text_sha256','quote','locator')}],previous=[]))
            w.write(state['save_receipt'],rec);w.submit(run,state['packet'],state['save_receipt'])
        else:legacy_answer(run,db,state)
    state=transport.next_task(run)
    assert state['phase']=='publication_acceptance'
    changes=state['review_card']['directory_changes'];assert len(changes)==1
    after=changes[0]['after'];assert '954-555-0200' in json.dumps(after['contacts'])
    assert '954-555-0100' not in json.dumps(after['contacts'])
    assert '100 Court Street' in json.dumps(after['contacts'])
    assert after['assignment']==supplement['people'][0]['assignment']
    with h.database(db) as conn:
        ds=w.accepted(conn,w.load(run));rosters=[d for d in ds.values() if d['task']['kind']=='roster_review'];assert len(rosters)==1
    assert path.read_bytes()==before
    assert approve(state,tmp_path)['phase']=='preview_complete'
    assert path.read_bytes()==before


def test_new_person_missing_scope_returns_small_semantic_card_not_inferred_membership(tmp_path):
    run,db,_,_=environment(tmp_path,profile=b'Clerk Jane Smith. Phone: 555-0101.')
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
    result=invoke(state,dict(decision='include_directory',reason='Reviewed clerk scope.',scope=dict(counties=[],court_ids=['dca_fifth'])),tmp_path)
    assert result.returncode==0,result.stderr.decode();state=json.loads(result.stdout)
    assert state['phase']=='publication_acceptance'
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
    assert next_state['phase']=='publication_acceptance'
    assert next_state['review_card']['entries']==[]
    assert next_state['review_progress']['remaining_opinion_reviews']==0
    assert w.load(second)['baseline_capture']==prepared['capture_id']
    assert list(server.calls)==calls
    assert approve(next_state,tmp_path)['phase']=='preview_complete'


def test_unresolved_publication_can_retry_same_checkpoint_with_corrected_answer(tmp_path):
    import shlex,subprocess,os
    run,db,_,_,state,_=reach_approval(tmp_path)
    value=dict(decision='unresolved',reason='Content approval withheld pending clarification.',corrections=[])
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
    assert resumed['phase']=='publication_acceptance'
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
    entry=state['review_card']['entries'][0]['ref'];value=dict(decision='correct',reason='Qualify the rule.',corrections=[dict(entry=entry,summary='On this record, the commercial holding is affirmed.',reason='Retain record limit.')])
    # In-process reply lets the injected interruption cross the same domain path.
    folder=run/'agent-steps'/'correction-recovery';folder.mkdir(parents=True);path=folder/'answer.json';w.write(path,value)
    with pytest.raises(OSError,match='interrupted'):transport.reply(run,state['task_handle'],path)
    monkeypatch.setattr(w,'record',actual)
    resumed=transport.reply(run,state['task_handle'],path)
    assert resumed['phase']=='publication_acceptance'
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
    assert state['phase']=='publication_acceptance'
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
        assert next_state['phase']=='publication_acceptance'
        entries=next_state['review_card']['entries'];assert len(entries)==count
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
    assert next_state['phase']=='publication_acceptance'
    assert len(next_state['review_card']['entries'])==1
    assert next_state['review_card']['entries'][0]['summary']=='Reviewed civil holding.'


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
