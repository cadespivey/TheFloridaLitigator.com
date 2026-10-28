"""Current workflow command behavior against isolated official-shaped fixtures."""
import copy
import json
from pathlib import Path
import pytest
from flwu import history as h, source_gate as g, update, workflow as w
from flwu import workflow_report as report, workflow_directory as directory, workflow_release as release
from tests.test_opinion_discovery import Server, opinion, pdf_bytes


def environment(tmp_path, *, fail=False, directories=(), profile=None,mode='preview'):
    database=tmp_path/'db.sqlite';run=tmp_path/'run'
    with h.database(database) as conn:
        h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},run_id='initial',
                 payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[]),artifacts={})
    registry={'schema_version':1,'stream':'weekly','review_protocol':g.PROTOCOL,
              'sources':[{'id':g.source_id('https://court.gov/profile'),'url':'https://court.gov/profile'}]}
    registry_path=tmp_path/'registry.json';w.write(registry_path,registry)
    w.initialize(run,database,registry_path,'trial',start='2026-10-15',end='2026-10-22',directories=directories,mode=mode,archive=tmp_path/'public' if mode=='publish' else None)
    server=Server([opinion()]);server.block={'2dca'} if fail else set()
    def fetch(url):
        meta,raw=server(url)
        return meta,profile if profile is not None and url=='https://court.gov/profile' else raw
    with h.database(database) as conn:update.run(conn,registry,'trial',run,start='2026-10-15',end='2026-10-22',fetch=fetch)
    return run,database,registry,server


def answer(run,database,task):
    t=w.read(task['packet']);r=copy.deepcopy(t['receipt_template'])
    if t['kind']=='source_review':
        o=t['inputs']['observation']
        with h.database(database) as c:text=g.blob(c,o['text_sha256']).decode()
        cite={k:o[k] for k in ('sha256','text_sha256')}
        cite.update(quote=text,locator='Fixture body')
        r.update(reviewer='Fixture reviewer',summary='Reviewed operating instructions.',review_scope='Fixture source only',
                 outcome='baseline_reviewed',support=dict(reason='No changed substantive requirement in this fixture.',current=[cite],previous=[]))
    elif t['kind']=='opinion_review':
        o=t['inputs']['source_observation']
        r.update(reviewer='Fixture reviewer',relevance='relevant',summary='Commercial opinion.',holding='Commercial holding.',
                 disposition='Affirmed.',authors=['Example'],citations=[dict(quote='Commercial holding.',locator='Page1',sha256=o['sha256'],text_sha256=o['text_sha256'])])
    elif t['kind']=='coverage_review':r.update(decision='unavailable',reason='This saved fixture endpoint was unavailable; no no-change conclusion.')
    elif t['kind']=='publication_mapping':r.update(decision='include',reason='Relevant commercial holding in the selected period.')
    elif t['kind']=='publication_acceptance':r.update(reviewer='Fixture editor',legal_review='Fixture claims checked.',visual_review='Fixture markup checked separately.')
    elif t['kind']=='roster_review':r.update(reason='Verified named fixture roster and cited identity.')
    else:raise AssertionError(t['kind'])
    w.write(task['save_receipt'],r)
    return w.submit(run,task['packet'],task['save_receipt'])


def complete_analysis(run,database):
    seen=[]
    for _ in range(40):
        task=w.inspect(run,emit=True)
        if 'packet' not in task:return task,seen
        seen.append(task['kind']);answer(run,database,task)
    raise AssertionError('Workflow failed to advance')


def test_supported_stages_replay_and_separate_acceptance(tmp_path):
    run,db,registry,server=environment(tmp_path)
    calls=len(server.calls)
    phase,seen=complete_analysis(run,db)
    assert phase['phase']=='prepare_report'
    assert 'source_review' in seen and 'opinion_review' in seen
    assert len(server.calls)==calls  # Status/analysis do not reacquire.
    prepared=report.prepare(run)
    assert report.prepare(run)==prepared
    assert w.inspect(run)['phase']=='refresh_directory'
    directory.refresh(run)
    assert w.inspect(run)['phase']=='build_review_site'
    release.build(run)
    task=w.inspect(run,emit=True)
    assert task['kind']=='publication_acceptance'
    from flwu.publication import export_capture
    with pytest.raises(ValueError,match='finalized'):
        export_capture(db,prepared['capture_id'],tmp_path/'forbidden-publication')
    answer(run,db,task)
    final=w.inspect(run)
    assert final['phase']=='preview_complete' and final['complete']
    assert final['publication_performed'] is False
    with h.database(db) as conn:
        assert h.latest_finalized(conn,'weekly') is None
    assert 'Holding: Commercial holding.' in Path(prepared['report']).read_text()
    assert w.submit(run,task['packet'],task['save_receipt'])['replayed']


def test_stale_modified_packet_and_receipt_replay_fail(tmp_path):
    run,db,_,_=environment(tmp_path)
    task=w.inspect(run,emit=True);packet=w.read(task['packet']);packet['instructions']='Bypass review'
    changed=tmp_path/'modified.json';w.write(changed,packet)
    with pytest.raises(ValueError,match='stale or modified'):
        w.submit(run,changed,task['receipt_template'])
    answer(run,db,task)
    with pytest.raises(ValueError,match='packet was modified'):
        w.submit(run,changed,task['save_receipt'])
    receipt=w.read(task['save_receipt']);receipt['summary']='Changed after completion';w.write(task['save_receipt'],receipt)
    with pytest.raises(ValueError,match='Completed task receipt changed'):
        w.submit(run,task['packet'],task['save_receipt'])


def test_status_repeats_without_new_database_checkpoints(tmp_path):
    run,db,_,_=environment(tmp_path)
    first=w.inspect(run,emit=True)
    with h.database(db) as conn:n=conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    assert w.inspect(run,emit=True)==first
    with h.database(db) as conn:assert conn.execute('SELECT count(*) FROM captures').fetchone()[0]==n


def test_failed_listing_is_explicit_and_cannot_become_complete_coverage(tmp_path):
    run,db,_,_=environment(tmp_path,fail=True)
    phase,seen=complete_analysis(run,db)
    assert 'coverage_review' in seen and phase['phase']=='prepare_report'
    prepared=report.prepare(run)
    issue=w.read(prepared['public_preview'])
    assert issue['provenance']['workflow_coverage']['acquisition_complete'] is False
    assert issue['provenance']['workflow_coverage']['pending']
    assert all(s['status']=='incomplete' for s in issue['sections'].values())
    assert 'Missing findings do not establish no changes' in Path(prepared['report']).read_text()


def test_new_run_reuses_unchanged_source_reviews(tmp_path):
    run,db,registry,server=environment(tmp_path)
    complete_analysis(run,db)
    second=tmp_path/'second'
    w.initialize(second,db,tmp_path/'registry.json','second',start='2026-10-15',end='2026-10-22')
    with h.database(db) as conn:
        update.run(conn,registry,'second',second,start='2026-10-15',end='2026-10-22',fetch=server)
    task=w.inspect(second,emit=True)
    assert task['phase']=='publication_mapping'
    queue=w.read(second/'update-queue.json')
    assert not queue['source_reviews']['tasks'] and not queue['opinion_reviews']['tasks']
    assert queue['source_reviews']['reused_reviews']


def test_interrupted_acquisition_next_command_resumes_saved_pages(tmp_path):
    run,db,registry,server=environment(tmp_path)
    second=tmp_path/'interrupted'
    w.initialize(second,db,tmp_path/'registry.json','interrupted',start='2026-10-15',end='2026-10-22')
    server=Server([opinion(1),opinion(2)]);server.interrupt_offset=1
    with h.database(db) as conn:
        with pytest.raises(RuntimeError,match='interrupted'):
            update.run(conn,registry,'interrupted',second,start='2026-10-15',end='2026-10-22',fetch=server)
    task=w.inspect(second,emit=True)
    assert task['phase']=='acquisition' and 'workflow acquire' in task['command'] and str(second) in task['command']
    first_pages=[u for u in server.calls if 'offset=0' in u]
    server.interrupt_offset=None;server.calls.clear()
    with h.database(db) as conn:
        update.run(conn,registry,'interrupted',second,start='2026-10-15',end='2026-10-22',fetch=server)
    assert not set(first_pages)&set(server.calls)
    assert w.inspect(second)['phase'] in ('source_review','opinion_review','publication_mapping')


def test_replay_recovers_domain_review_committed_before_coordinator(tmp_path, monkeypatch):
    run,db,_,_=environment(tmp_path)
    task=w.inspect(run,emit=True)
    real=w.record
    def fail(conn,config,event):
        if event['kind']=='decision':raise OSError('simulated coordinator interruption')
        return real(conn,config,event)
    monkeypatch.setattr(w,'record',fail)
    with pytest.raises(OSError,match='interruption'):answer(run,db,task)
    monkeypatch.setattr(w,'record',real)
    with h.database(db) as conn:before=len(g.reviews(conn,'weekly'))
    result=w.submit(run,task['packet'],task['save_receipt'])
    assert result['packet_sha256']
    with h.database(db) as conn:assert len(g.reviews(conn,'weekly'))==before
    assert w.submit(run,task['packet'],task['save_receipt'])['replayed']


def test_contact_projection_preserves_unsupplied_fields_and_scoped_assignments():
    old={'office':[{'label':'Phone','lines':['555-0100'],'fact_path':'contact.phone'},
                   {'label':'Address','lines':['Court','100 Main','City FL'],'fact_path':'address','type':'address'}],
         'assistant':[{'label':'Name','lines':['Jane Smith'],'fact_path':'assistant.name'}]}
    proposed={'office':[{'label':'Phone','lines':['555-0200'],'fact_path':'reviewed_person_details'}],'assistant':[]}
    merged=directory.merge_contacts(old,proposed)
    assert merged['assistant']==old['assistant']
    assert old['office'][1] in merged['office']
    assert old['office'][0] not in merged['office']
    assert proposed['office'][0] in merged['office']
    assert old['office'][0]['lines']==['555-0100']


from tests.test_county_directory import supplement, seal


@pytest.mark.parametrize('update_assignment',[False,True])
def test_directory_alias_projection_preserves_other_people_and_evidence(tmp_path,supplement,update_assignment,monkeypatch):
    supplement['review_status']='reviewed'
    supplement['review']=dict(reviewed_by='Prior fixture editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Reviewed fixture.')
    seal(supplement)
    current=tmp_path/'broward.json';w.write(current,supplement)
    text=b'Judge Example Judge serves Broward civil court. Chambers phone: 954-555-0200.'
    run,db,_,_=environment(tmp_path,directories=[current],profile=text,mode='publish')
    for _ in range(40):
        task=w.inspect(run,emit=True)
        if 'packet' not in task:break
        packet=w.read(task['packet']);receipt=copy.deepcopy(packet['receipt_template'])
        if packet['kind']=='source_review' and packet['inputs']['url']=='https://court.gov/profile':
            o=packet['inputs']['observation'];ref={k:o[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')}
            ref.update(quote=text.decode(),locator='Fixture profile')
            person=dict(key='person-example-judge',kind='judge',facts=dict(name='Example Judge',fields={'chambers_phone':{'value':'954-555-0200','citation':ref}}),citations=[ref],expected_version=None)
            roster=dict(key='roster-test',kind='source_inventory',facts={'entities':[dict(id='example-judge',name='Example Judge',type='judge',counties=['Broward'],citation=ref)]},citations=[ref],expected_version=None)
            receipt.update(reviewer='Fixture editor',summary='Updated chambers phone.',review_scope='One civil judge',outcome='updated_findings',findings=[person,roster],support=dict(reason='Current profile states phone.',current=[{k:ref[k] for k in ('sha256','text_sha256','quote','locator')}],previous=[]))
        elif packet['kind']=='publication_mapping' and packet['inputs']['finding']['kind']!='opinion':
            f=packet['inputs']['finding']
            receipt.update(decision='include_directory' if f['kind']=='judge' else 'exclude',candidate=None,reason='Personnel update belongs in directory, not legal news.')
            if f['kind']=='source_inventory':receipt['inventories']=[f]
        else:
            answer(run,db,task);continue
        w.write(task['save_receipt'],receipt);w.submit(run,task['packet'],task['save_receipt'])
    assert task['phase']=='prepare_report'
    prepared=report.prepare(run)
    task=w.inspect(run,emit=True);packet=w.read(task['packet'])
    assert task['kind']=='directory_review'
    receipt=packet['receipt_template']
    receipt.update(targets=[dict(path=str(current),id='example-judge')],reviewer='Fixture directory editor',reason='Same named judge, updated phone only.',identity_citations=[ref])
    if update_assignment:
        receipt['assignment_updates']=[dict(path=str(current),value='Broward civil court',reason='The source explicitly states this assignment.',citations=[ref])]
    w.write(task['save_receipt'],receipt);w.submit(run,task['packet'],task['save_receipt'])
    result=directory.refresh(run);out=w.read(result['directory_paths'][0])
    assert w.read(current)==supplement # No publication side effect.
    assert out['people'][1]==supplement['people'][1]
    assert out['people'][0]['assignment']==('Broward civil court' if update_assignment else supplement['people'][0]['assignment'])
    assert out['people'][0]['id']=='example-judge'
    assert out['people'][0]['legacy_person_id']=='person-example-judge'
    assert '954-555-0200' in json.dumps(out['people'][0]['contacts'])
    assert '954-555-0100' not in json.dumps(out['people'][0]['contacts'])
    assert '100 Court Street' in json.dumps(out['people'][0]['contacts'])
    assert len(out['people'][0]['sources'])>len(supplement['people'][0]['sources'])
    assert directory.refresh(run)==result
    assert release.build(run)==release.build(run)
    previous=w.decision(run,task['packet'])
    correction=copy.deepcopy(receipt);correction['reason']='Corrected explanation of the same cited identity match.'
    corrected_path=tmp_path/'directory-correction.json';w.write(corrected_path,correction)
    w.revise(run,task['packet'],corrected_path,previous['decision_sha256'],'Clarify identity rationale')
    assert w.inspect(run)['phase']=='refresh_directory'
    refreshed=directory.refresh(run)
    assert refreshed['decision_sha256']!=result['decision_sha256']
    assert refreshed['audit']!=result['audit']
    assert w.inspect(run)['phase']=='build_review_site'
    rebuilt=release.build(run)
    with h.database(db) as conn:
        with pytest.raises(ValueError,match='requires publication acceptance'):
            release.require_build_acceptance(conn,w.load(run),rebuilt)
    phase,_=complete_analysis(run,db)
    assert phase['phase']=='ready_for_publication'
    with h.database(db) as conn:h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Fixture publication')
    release.export(run)
    real_record=w.record
    def interrupt_completion(conn,config,event):
        if event['kind']=='publication_integrated':raise OSError('Interrupted after file installation')
        return real_record(conn,config,event)
    with monkeypatch.context() as interrupted:
        interrupted.setattr(w,'record',interrupt_completion)
        with pytest.raises(OSError,match='Interrupted after file installation'):release.integrate(run)
    release.integrate(run)
    assert w.inspect(run)['phase']=='release_required'
    assert release.integrate(run)['phase']=='release_required'
    assert '954-555-0200' in current.read_text()
    # A concurrent directory edit invalidates the prepared projection/build.
    changed=copy.deepcopy(supplement);changed['people'][0]['assignment']='New assignment';seal(changed);w.write(current,changed)
    with pytest.raises(ValueError,match='refresh current directories'):release.build(run)


def test_trial_cli_is_offline_resumable_and_rejects_live_boundaries(tmp_path,capsys):
    from flwu.cli import main
    from flwu.workflow_trial import Transport
    root=tmp_path/'trial';run=root/'interrupt'
    args=['workflow','trial-init','--trial-root',str(root),'--run-dir',str(run),'--scenario','interrupted']
    assert main(args)==0
    assert main(['workflow','acquire','--run-dir',str(run)])==1
    assert w.inspect(run)['phase']=='acquisition'
    assert main(['workflow','acquire','--run-dir',str(run)])==0
    calls=[json.loads(line)['url'] for line in (run/'fixture-requests.jsonl').read_text().splitlines()]
    first=[u for u in calls if 'siteaccess=1dca' in u and 'offset=0' in u and 'nonactive_only' not in u]
    assert len(first)==1
    config=w.load(run);config['database']=str(tmp_path/'live.sqlite')
    with pytest.raises(ValueError,match='boundary'):Transport(config)
    with pytest.raises(ValueError,match='publish workflow'):release.export(run)


def test_coordinator_acquire_obeys_database_lock(tmp_path):
    from flwu.acquisition import acquisition
    run,db,_,_=environment(tmp_path)
    with acquisition(db,'other-run','test',heartbeat_seconds=60):
        with pytest.raises(ValueError,match='already running'):w.acquire(run)


def test_unaccepted_report_cannot_finalize_and_build_tampering_blocks_acceptance(tmp_path):
    run,db,_,_=environment(tmp_path)
    complete_analysis(run,db);prepared=report.prepare(run);directory.refresh(run)
    build=release.build(run)
    with h.database(db) as conn:
        with pytest.raises(ValueError,match='acceptance'):
            h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Fixture editor')
    (Path(build['site'])/'index.html').write_text('tampered')
    with pytest.raises(ValueError,match='artifact missing or changed'):
        w.inspect(run)


def test_changed_prepared_preview_cannot_supply_directory_values(tmp_path):
    run,db,_,_=environment(tmp_path)
    complete_analysis(run,db);prepared=report.prepare(run)
    value=w.read(prepared['public_preview']);value['directory']=[{'name':'Invented Person'}]
    w.write(prepared['public_preview'],value)
    with pytest.raises(ValueError,match='projection missing or changed'):
        directory.refresh(run)


def test_projection_repair_restores_original_bytes_without_new_reviews(tmp_path):
    run,db,_,server=environment(tmp_path)
    complete_analysis(run,db);prepared=report.prepare(run);dirs=directory.refresh(run)
    paths=[Path(prepared['report']),Path(prepared['public_preview']),Path(prepared['acceptance_template']),Path(dirs['audit'])]
    expected={str(p):p.read_bytes() for p in paths}
    calls=len(server.calls)
    with h.database(db) as conn:before=w.accepted(conn,w.load(run))
    paths[0].write_bytes(b'corrupt report');paths[1].unlink()
    paths[2].write_bytes(b'corrupt template');paths[3].unlink()
    result=w.repair(run)
    assert len(result['repaired'])==4
    for p in paths:assert p.read_bytes()==expected[str(p)]
    damaged=[Path(item['damaged_copy']).read_bytes() for item in result['repaired'] if item['damaged_copy']]
    assert b'corrupt report' in damaged and b'corrupt template' in damaged
    assert not w.repair(run)['repaired']
    assert len(server.calls)==calls
    with h.database(db) as conn:assert w.accepted(conn,w.load(run))==before
    assert w.inspect(run)['phase']=='build_review_site'


def test_legacy_stage_regeneration_preserves_damaged_files(tmp_path,monkeypatch):
    run,db,_,server=environment(tmp_path)
    complete_analysis(run,db)
    with monkeypatch.context() as legacy:
        legacy.setattr(w,'projection_hashes',lambda paths:{})
        old=report.prepare(run);dirs=directory.refresh(run)
    original=Path(old['report']).read_bytes();calls=len(server.calls)
    Path(old['report']).write_bytes(b'damaged legacy report')
    Path(old['acceptance_template']).unlink()
    restored=report.prepare(run,repair=True)
    assert Path(restored['report']).read_bytes()==original
    backups=list(Path(old['report']).parent.parent.glob('*.preserved-*/report.html'))
    assert any(p.read_bytes()==b'damaged legacy report' for p in backups)
    Path(dirs['audit']).write_bytes(b'damaged audit')
    refreshed=directory.refresh(run,repair=True)
    assert w.read(refreshed['audit'])==[]
    assert any(p.read_bytes()==b'damaged audit' for p in Path(dirs['audit']).parent.parent.glob('*.preserved-*/field-audit.json'))
    assert len(server.calls)==calls
    assert w.inspect(run)['phase']=='build_review_site'


@pytest.mark.parametrize('damage', ['modified', 'missing', 'extra'])
def test_build_repair_preserves_damage_and_restores_exact_output(tmp_path, damage):
    run,db,_,server=environment(tmp_path)
    complete_analysis(run,db);report.prepare(run);directory.refresh(run)
    original=release.build(run)
    root=Path(original['site']);expected=(root/'index.html').read_bytes()
    if damage=='modified':(root/'index.html').write_text('damaged')
    elif damage=='missing':(root/'index.html').unlink()
    else:(root/'unexpected.html').write_text('unreviewed')
    calls=len(server.calls)
    with pytest.raises(ValueError,match='artifact missing or changed'):
        release.build(run)
    repaired=release.build(run,repair=True)
    assert repaired['site']!=original['site']
    assert (Path(repaired['site'])/'index.html').read_bytes()==expected
    assert len(server.calls)==calls
    if damage=='modified':assert (root/'index.html').read_text()=='damaged'
    elif damage=='missing':assert not (root/'index.html').exists()
    else:assert (root/'unexpected.html').read_text()=='unreviewed'
    assert release.build(run)==repaired
    assert w.inspect(run)['phase']=='publication_acceptance'


def test_mapping_correction_is_append_only_and_rebuilds_report(tmp_path):
    run,db,_,_=environment(tmp_path)
    complete_analysis(run,db);before=report.prepare(run);directory.refresh(run);release.build(run)
    config=w.load(run)
    with h.database(db) as conn:
        old=next(e for e in w.accepted(conn,config).values() if e['task']['kind']=='publication_mapping')
    task=old['task'];replacement=copy.deepcopy(old['receipt'])
    replacement.update(decision='exclude',candidate=None,reason='Corrected editorial scope: this fixture is excluded.')
    path=tmp_path/'correction.json';w.write(path,replacement)
    with pytest.raises(ValueError,match='Stale predecessor'):
        w.revise(run,task['packet_path'],path,'0'*64,'Scope correction')
    result=w.revise(run,task['packet_path'],path,h.sha(old),'Scope correction')
    assert w.revise(run,task['packet_path'],path,h.sha(old),'Scope correction')['replayed']
    assert w.inspect(run)['phase']=='prepare_report'
    after=report.prepare(run)
    assert after['capture_id']!=before['capture_id']
    assert 'Commercial holding.' in Path(before['report']).read_text()
    assert 'Commercial holding.' not in Path(after['report']).read_text()
    with h.database(db) as conn:
        revisions=[e for e in w.events(conn,config) if e['kind']=='decision' and e['packet_sha256']==task['packet_sha256']]
        assert revisions==[old,w.accepted(conn,config)[task['packet_sha256']]]
        assert h.sha(revisions[-1])==result['decision_sha256']


def test_finalized_workflow_rejects_mapping_correction_without_mutation(tmp_path):
    run,db,_,_=environment(tmp_path)
    complete_analysis(run,db)
    prepared=report.prepare(run);directory.refresh(run);release.build(run)
    answer(run,db,w.inspect(run,emit=True))
    config=w.load(run)
    with h.database(db) as conn:
        h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Fixture publication')
        before=w.events(conn,config)
        old=next(e for e in w.accepted(conn,config).values() if e['task']['kind']=='publication_mapping')
        baseline=h.latest_finalized(conn,'weekly')
    original=Path(prepared['report']).read_bytes()
    replacement=copy.deepcopy(old['receipt'])
    replacement.update(decision='exclude',candidate=None,reason='Attempted post-publication correction.')
    path=tmp_path/'correction.json';w.write(path,replacement)
    with pytest.raises(ValueError,match='Finalized workflow is immutable'):
        w.revise(run,old['task']['packet_path'],path,h.sha(old),'New editorial assessment')
    with h.database(db) as conn:
        assert w.events(conn,config)==before
        assert h.latest_finalized(conn,'weekly')==baseline
    assert Path(prepared['report']).read_bytes()==original


@pytest.mark.parametrize('start,end,expected_policy',[
    ('2026-10-15','2026-10-22','identical_reporting_period'),
    ('2026-10-23','2026-10-29','previously_published_unchanged_opinion'),
    ('2026-10-15','2026-10-29',None),
])
def test_finalized_mapping_reuse_respects_reporting_scope(tmp_path,start,end,expected_policy):
    run,db,registry,server=environment(tmp_path)
    complete_analysis(run,db);prepared=report.prepare(run);directory.refresh(run);release.build(run)
    answer(run,db,w.inspect(run,emit=True))
    with h.database(db) as conn:h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Fixture baseline')
    second=tmp_path/'next'
    w.initialize(second,db,tmp_path/'registry.json','next',start=start,end=end)
    with h.database(db) as conn:update.run(conn,registry,'next',second,start=start,end=end,fetch=server)
    phase=w.inspect(second,emit=True)
    with h.database(db) as conn:
        reused=[e for e in w.accepted(conn,w.load(second)).values() if 'reuse' in e]
    if expected_policy:
        assert phase['phase']=='prepare_report'
        assert reused and {e['reuse']['policy'] for e in reused}=={expected_policy}
        if expected_policy=='previously_published_unchanged_opinion':
            assert all(e['receipt']['decision']=='exclude' for e in reused)
        assert w.inspect(second)['phase']=='prepare_report'
    else:
        assert not reused
        assert phase['phase']=='publication_mapping'


def test_publish_mode_advances_to_export_handoff_without_deployment(tmp_path,monkeypatch):
    monkeypatch.setattr(w,'ROOT',tmp_path)
    run,db,registry,server=environment(tmp_path)
    second=tmp_path/'publish'
    w.initialize(second,db,tmp_path/'registry.json','publish',start='2026-10-15',end='2026-10-22',mode='publish',archive=tmp_path/'public')
    with h.database(db) as conn:update.run(conn,registry,'publish',second,start='2026-10-15',end='2026-10-22',fetch=server)
    complete_analysis(second,db);prepared=report.prepare(second);directory.refresh(second);release.build(second)
    answer(second,db,w.inspect(second,emit=True))
    assert w.inspect(second)['phase']=='ready_for_publication'
    with h.database(db) as conn:h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Fixture editor after actual fixture acceptance')
    assert w.inspect(second)['phase']=='export_publication'
    result=release.export(second)
    assert result==release.export(second)
    assert w.inspect(second)['phase']=='publication_handoff'
    assert not (tmp_path/'public').exists()
    assert result['complete'] is False and result['publication_performed'] is False
    manifest=w.read(result['manifest']);assert len(manifest['files'])==1
    assert Path(manifest['files'][0]['source']).is_file()
    bundle=Path(manifest['files'][0]['source']);bundle_bytes=bundle.read_bytes()
    bundle.write_bytes(b'damaged release bundle')
    repairs=w.repair(second)['repaired']
    assert bundle.read_bytes()==bundle_bytes
    assert any(Path(item['damaged_copy']).read_bytes()==b'damaged release bundle'
               for item in repairs if item['damaged_copy'])
    assert release.export(second)==result
    target=Path(manifest['files'][0]['destination'])
    target.parent.mkdir(parents=True);target.write_bytes(b'concurrent publication')
    with pytest.raises(ValueError,match='Concurrent publication edit'):
        release.integrate(second)
    assert target.read_bytes()==b'concurrent publication'
    target.unlink() # Remove this test's deliberate conflicting fixture.
    installed=release.integrate(second)
    assert installed==release.integrate(second)
    assert target.read_bytes()==Path(manifest['files'][0]['source']).read_bytes()
    assert w.inspect(second)['phase']=='release_required'
    assert w.inspect(second)['complete'] is False
    from flwu import workflow_deployment as deployment
    monkeypatch.setattr(deployment.subprocess,'check_output',lambda *a,**k:'b'*40+'\n')
    release_plan=deployment.plan(second)
    assert release_plan==deployment.plan(second)
    assert release_plan['files']==[str(target.relative_to(tmp_path))]
    assert '--only' in release_plan['commands'][3]
    import base64
    expected=w.read(manifest['files'][0]['source'])
    pr=dict(number=7,state='OPEN',url='https://github.com/example/repo/pull/7',headRefOid='a'*40,mergeCommit=None,baseRefName='main')
    job=dict(databaseId=9,headSha='a'*40,headBranch='main',event='push',status='completed',conclusion='success',workflowName='GitHub Pages',url='https://github.com/example/repo/actions/runs/9',jobs=[dict(name='deploy',conclusion='success')])
    live=dict(preview=False,issues=[expected],county_directories=[])
    def gh(config,*args):
        if args[0]=='repo':return {'nameWithOwner':'example/repo'}
        if args[0]=='pr':return pr
        if args[0]=='run':return job
        if args[0]=='api':return dict(encoding='base64',content=base64.b64encode(target.read_bytes()).decode())
        raise AssertionError(args)
    monkeypatch.setattr(deployment,'github',gh)
    monkeypatch.setattr(deployment,'fetch_json',lambda url: {'archive':'archive-'+'a'*16+'.json'} if url.endswith('current-archive.json') else live)
    assert deployment.verify(second,7)['phase']=='merge_required'
    pr.update(state='MERGED',mergeCommit={'oid':'a'*40})
    assert deployment.verify(second,7)['phase']=='deployment_verification'
    job['jobs'][0]['conclusion']='skipped'
    with pytest.raises(ValueError,match='successful GitHub Pages'):deployment.verify(second,7,9)
    job['jobs'][0]['conclusion']='success'
    live['issues']=[]
    with pytest.raises(ValueError,match='Live current publication'):deployment.verify(second,7,9)
    assert w.inspect(second)['complete'] is False
    live['issues']=[expected]
    assert deployment.verify(second,7,9)['complete'] is True
    assert w.inspect(second)['phase']=='publication_complete'


def test_explicit_directory_removal_requires_exact_review_and_preserves_others(tmp_path,supplement,monkeypatch):
    supplement['review_status']='reviewed'
    supplement['review']=dict(reviewed_by='Prior editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Fixture reviewed.')
    # Existing alias was already reconciled by a prior review.
    supplement['people'][0]['legacy_person_id']='person-example-judge';seal(supplement)
    path=tmp_path/'broward.json';w.write(path,supplement)
    run,db,_,_=environment(tmp_path,directories=[path])
    complete_analysis(run,db);prepared=report.prepare(run)
    config=w.load(run)
    with h.database(db) as conn:
        source=g.observations(conn,'weekly')[0]
        ref={k:source[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')}
        ref.update(quote='Court release notices.',locator='Fixture body')
    # Report assembly tests separately guard actual departure evidence. Here the
    # prepared source-bound decision isolates the directory projection contract.
    removal=dict(person_id='person-example-judge',reason='Fixture departure decision.',citations=[ref])
    monkeypatch.setattr(report,'decisions',lambda *args:([{'removals':[removal]}],[]))
    with h.database(db) as conn:
        task=next(directory.tasks(conn,config,prepared));receipt=copy.deepcopy(task['receipt_template'])
        assert task['kind']=='directory_removal'
        receipt.update(reviewer='Directory fixture editor',reason='Confirm explicit prior departure decision.')
        altered=copy.deepcopy(receipt);altered['targets'][0]['id']='example-senior'
        with pytest.raises(ValueError,match='explicit removal targets'):directory.validate_decision(conn,config,task,altered)
        result=directory.validate_decision(conn,config,task,receipt)
        w.record(conn,config,dict(kind='decision',packet_sha256=task['packet_sha256'],task=task,receipt=receipt,validation=result))
        original_assemble=report.assemble
        monkeypatch.setattr(report,'assemble',lambda *args:({},[],[],prepared['fingerprint']))
    output=directory.refresh(run);current=w.read(output['directory_paths'][0])
    assert current['people']==[supplement['people'][1]]
    assert w.read(path)==supplement
    assert w.read(output['audit'])[0]['after'] is None


def source_correction_fixture(tmp_path):
    run, db, registry, server = environment(tmp_path)
    complete_analysis(run, db)
    before = report.prepare(run)
    config = w.load(run)
    with h.database(db) as conn:
        old = next(e for e in w.accepted(conn, config).values() if e['task']['kind'] == 'source_review')
    receipt = copy.deepcopy(old['receipt'])
    receipt['summary'] = 'Corrected description: observed fixture text only.'
    path = tmp_path/'source-correction.json'
    w.write(path, receipt)
    return run, db, registry, server, config, old, receipt, path, before


def test_source_correction_preserves_history_and_invalidates_report(tmp_path):
    run, db, _, _, config, old, receipt, path, before = source_correction_fixture(tmp_path)
    # The accepted projection remains the original; corrections have their own files.
    original = run/'workflow'/'accepted'/(old['packet_sha256']+'.json')
    raw = original.read_bytes()
    with pytest.raises(ValueError, match='Stale predecessor'):
        w.revise(run, old['task']['packet_path'], path, '0'*64, 'Remove unsupported inference')
    result = w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Remove unsupported inference')
    assert w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Remove unsupported inference')['replayed']
    assert original.read_bytes() == raw
    with h.database(db) as conn:
        reviews = g.reviews(conn, 'weekly')
        assert reviews[-1]['receipt_sha256'] == h.sha(receipt)
        assert any(r['receipt_sha256'] == h.sha(old['receipt']) for r in reviews)
        current = w.accepted(conn, config)[old['packet_sha256']]
        assert current['supersedes'] == h.sha(old)
        assert current['receipt'] == receipt
        assert h.sha(current) == result['decision_sha256']
    assert w.inspect(run)['phase'] == 'prepare_report'
    assert report.prepare(run)['capture_id'] != before['capture_id']


def test_source_correction_recovers_domain_commit_before_coordinator_commit(tmp_path, monkeypatch):
    run, db, _, _, config, old, receipt, path, _ = source_correction_fixture(tmp_path)
    record = w.record
    def interrupted(conn, config, event):
        if event.get('supersedes'):
            raise RuntimeError('Simulated interruption after domain commit')
        return record(conn, config, event)
    monkeypatch.setattr(w, 'record', interrupted)
    with pytest.raises(RuntimeError, match='Simulated interruption'):
        w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Correct description')
    with h.database(db) as conn:
        assert g.reviews(conn, 'weekly')[-1]['receipt_sha256'] == h.sha(receipt)
        assert w.accepted(conn, config)[old['packet_sha256']] == old
        count = len(g.reviews(conn, 'weekly'))
    with pytest.raises(ValueError, match='Source review and coordinator decision disagree'):
        w.inspect(run)
    with pytest.raises(ValueError, match='Source review and coordinator decision disagree'):
        report.prepare(run)
    monkeypatch.setattr(w, 'record', record)
    w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Correct description')
    with h.database(db) as conn:
        assert len(g.reviews(conn, 'weekly')) == count
        assert w.accepted(conn, config)[old['packet_sha256']]['receipt'] == receipt


@pytest.mark.parametrize('failure', ['identity', 'quote', 'intervening'])
def test_source_correction_rejects_invalid_or_intervening_review(tmp_path, failure):
    run, db, registry, _, config, old, receipt, path, _ = source_correction_fixture(tmp_path)
    if failure == 'identity':
        receipt['sha256'] = '0'*64
        error = 'retain the accepted source evidence identity'
    elif failure == 'quote':
        receipt['support']['current'][0]['quote'] = 'Fabricated quote not in fixture'
        error = 'quote absent'
    else:
        other = copy.deepcopy(old['receipt']); other['summary'] = 'Independent newer domain review'
        with h.database(db) as conn:g.accept(conn, registry, other)
        error = 'changed outside this decision'
    w.write(path, receipt)
    with h.database(db) as conn:
        count = len(g.reviews(conn, 'weekly')); history = w.events(conn, config)
    with pytest.raises(ValueError, match=error):
        w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Correct description')
    with h.database(db) as conn:
        assert len(g.reviews(conn, 'weekly')) == count
        assert w.events(conn, config) == history


def test_source_correction_rejects_new_observation(tmp_path):
    run, db, registry, server, config, old, receipt, path, _ = source_correction_fixture(tmp_path)
    with h.database(db) as conn:
        update.run(conn, registry, 'later-observation', tmp_path/'later',
                   start='2026-10-15', end='2026-10-22', fetch=server)
        count = len(g.reviews(conn, 'weekly'))
    with pytest.raises(ValueError, match='observation is no longer current'):
        w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Correct description')
    with h.database(db) as conn:
        assert len(g.reviews(conn, 'weekly')) == count
        assert w.accepted(conn, config)[old['packet_sha256']] == old


def test_source_correction_rejects_finalized_run(tmp_path):
    run, db, _, _, config, old, receipt, path, prepared = source_correction_fixture(tmp_path)
    directory.refresh(run); release.build(run); answer(run, db, w.inspect(run, emit=True))
    with h.database(db) as conn:
        h.finalize(conn, prepared['capture_id'], Path(prepared['report']), 'Fixture publication')
        count = len(g.reviews(conn, 'weekly'))
        baseline = h.latest_finalized(conn, 'weekly')
    with pytest.raises(ValueError, match='Finalized workflow is immutable'):
        w.revise(run, old['task']['packet_path'], path, h.sha(old), 'Correct description')
    with h.database(db) as conn:
        assert len(g.reviews(conn, 'weekly')) == count
        assert h.latest_finalized(conn, 'weekly') == baseline
        assert w.accepted(conn, config)[old['packet_sha256']] == old
