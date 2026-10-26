"""Current workflow command behavior against isolated official-shaped fixtures."""
import copy
import json
from pathlib import Path
import pytest
from flwu import history as h, source_gate as g, update, workflow as w
from flwu import workflow_report as report, workflow_directory as directory, workflow_release as release
from tests.test_opinion_discovery import Server, opinion, pdf_bytes


def environment(tmp_path, *, fail=False, directories=(), profile=None):
    database=tmp_path/'db.sqlite';run=tmp_path/'run'
    with h.database(database) as conn:
        h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},run_id='initial',
                 payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[]),artifacts={})
    registry={'schema_version':1,'stream':'weekly','review_protocol':g.PROTOCOL,
              'sources':[{'id':g.source_id('https://court.gov/profile'),'url':'https://court.gov/profile'}]}
    registry_path=tmp_path/'registry.json';w.write(registry_path,registry)
    w.initialize(run,database,registry_path,'trial',start='2026-10-15',end='2026-10-22',directories=directories)
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
def test_directory_alias_projection_preserves_other_people_and_evidence(tmp_path,supplement,update_assignment):
    supplement['review_status']='reviewed'
    supplement['review']=dict(reviewed_by='Prior fixture editor',reviewed_at='2026-10-17T13:00:00Z',attestation='Reviewed fixture.')
    seal(supplement)
    current=tmp_path/'broward.json';w.write(current,supplement)
    text=b'Judge Example Judge serves Broward civil court. Chambers phone: 954-555-0200.'
    run,db,_,_=environment(tmp_path,directories=[current],profile=text)
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
    with pytest.raises(ValueError,match='Prepared artifact changed'):
        directory.refresh(run)


def test_publish_mode_advances_to_export_handoff_without_deployment(tmp_path):
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
