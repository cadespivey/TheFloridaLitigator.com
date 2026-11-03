"""Finalized discovery inventories may be reused without claiming content review."""
import copy
import json
from pathlib import Path
import pytest
from flwu import history as h,source_gate as g,workflow as w,workflow_report as report
from flwu import workflow_directory as directory,workflow_release as release,update
from flwu.evidence_binding import AcquisitionIndex
from tests.test_workflow import environment,answer


def baseline_and_next(tmp_path,*,legacy=False,discovery_only=True,publication_ready=False,changed=False,failed=False):
    text=b'Official document catalog. Listed documents require separate content review.'
    run,db,registry,server=environment(tmp_path,profile=text)
    for _ in range(30):
        task=w.inspect(run,emit=True)
        if 'packet' not in task:break
        packet=w.read(task['packet']);receipt=copy.deepcopy(packet['receipt_template'])
        if packet['kind']=='source_review' and packet['inputs']['url']=='https://court.gov/profile':
            o=packet['inputs']['observation']
            cite={k:o[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')}
            cite.update(quote=text.decode(),locator='Fixture catalog')
            finding=dict(key='fixture-catalog',kind='statute',
                facts=dict(discovery_only=discovery_only,publication_ready=publication_ready,
                           summary='Catalog only; document contents not reviewed.',coverage_status='incomplete'),
                citations=[cite],expected_version=None)
            receipt.update(reviewer='Fixture source editor',summary='Catalog captured; contents unreviewed.',
                review_scope='Catalog identity only',outcome='updated_findings',findings=[finding],
                support=dict(reason='Baseline catalog observation.',current=[{k:cite[k] for k in ('sha256','text_sha256','quote','locator')}],previous=[]))
        elif packet['kind']=='publication_mapping' and packet['identity']=='source:fixture-catalog':
            receipt.update(decision='exclude',candidate=None,reason='Discovery-only catalog is not a substantive legal update.')
        else:
            answer(run,db,task);continue
        w.write(task['save_receipt'],receipt);w.submit(run,task['packet'],task['save_receipt'])
    assert task['phase']=='prepare_report'
    prepared=report.prepare(run);directory.refresh(run);release.build(run)
    answer(run,db,w.inspect(run,emit=True))
    with h.database(db) as conn:
        baseline=prepared['capture_id']
        if legacy:
            from flwu import publication_acceptance
            payload=json.loads(conn.execute('SELECT payload FROM captures WHERE capture_id=?',(baseline,)).fetchone()[0])
            payload.pop('workflow_report')
            manifest=json.loads(conn.execute('SELECT manifest FROM publication_acceptances WHERE capture_id=?',(baseline,)).fetchone()[0])
            saved=h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},
                run_id='legacy-catalog-baseline',payload=payload,artifacts={})
            baseline=saved['capture_id'];manifest['capture_id']=baseline
            publication_acceptance.accept(conn,manifest,Path(prepared['report']))
        h.finalize(conn,baseline,Path(prepared['report']),'Fixture finalized baseline')
    second=tmp_path/'next'
    w.initialize(second,db,tmp_path/'registry.json','next',start='2026-10-23',end='2026-10-29')
    def fetch(url):
        meta,raw=server(url)
        if failed and url=='https://court.gov/profile':return dict(meta,success=False,http_status=403),b'Forbidden'
        return meta,(text+b' Newly changed catalog content.' if changed else text) if url=='https://court.gov/profile' else raw
    with h.database(db) as conn:update.run(conn,registry,'next',second,start='2026-10-23',end='2026-10-29',fetch=fetch)
    return second,db,server,baseline


@pytest.mark.parametrize('legacy',[False,True])
def test_standard_command_reuses_exact_finalized_discovery_exclusion(tmp_path,legacy):
    run,db,server,baseline=baseline_and_next(tmp_path,legacy=legacy)
    calls=list(server.calls)
    assert w.inspect(run,emit=True)['phase']=='prepare_report'
    config=w.load(run)
    with h.database(db) as conn:
        events=w.accepted(conn,config)
        event=next(e for e in events.values() if e['task']['identity']=='source:fixture-catalog')
        assert event['reuse']['policy']=='unchanged_finalized_discovery_exclusion_v1'
        assert event['reuse']['baseline_capture']==baseline
        assert event['reuse']['finding_version']==event['task']['inputs']['version']
        assert event['receipt']['decision']=='exclude' and event['receipt']['candidate'] is None
        assert event['receipt']['personnel']==event['receipt']['inventories']==event['receipt']['removals']==[]
        assert 'not a new source review' in event['receipt']['reason']
        assert event['task']['inputs']['finding']['facts']['coverage_status']=='incomplete'
        index=AcquisitionIndex(conn,'weekly')
        for cite in event['receipt']['citations']:index.validate(cite)
        assert h.latest_finalized(conn,'weekly')['capture_id']==baseline
        before=w.events(conn,config)
    assert w.inspect(run)['phase']=='prepare_report'
    with h.database(db) as conn:assert w.events(conn,config)==before
    assert server.calls==calls


@pytest.mark.parametrize('discovery_only,publication_ready',[(False,False),(True,True),('true',False),(True,0)])
def test_missing_exact_boolean_classification_requires_mapping(tmp_path,discovery_only,publication_ready):
    run,_,_,_=baseline_and_next(tmp_path,discovery_only=discovery_only,publication_ready=publication_ready)
    task=w.inspect(run,emit=True)
    assert task['phase']=='publication_mapping' and task['identity']=='source:fixture-catalog'


def test_changed_source_still_requires_source_review_before_inventory_reuse(tmp_path):
    run,db,_,_=baseline_and_next(tmp_path,changed=True)
    assert w.inspect(run,emit=True)['phase']=='source_review'
    with h.database(db) as conn:
        assert all(e['task']['identity']!='source:fixture-catalog' for e in w.accepted(conn,w.load(run)).values())


def test_failed_retrieval_still_requires_coverage_disposition(tmp_path):
    run,db,_,baseline=baseline_and_next(tmp_path,failed=True)
    task=w.inspect(run,emit=True)
    assert task['phase']=='coverage_review'
    assert w.read(task['packet'])['inputs']['unavailable'] is True
    with h.database(db) as conn:
        cfg=w.load(run);queue=w.latest_queue(conn,cfg)
        assert queue['acquisition_complete'] is False
        assert any(t['reason']=='retrieval_failed' for t in queue['source_reviews']['tasks'])
        event=next(e for e in w.accepted(conn,cfg).values() if e['task']['identity']=='source:fixture-catalog')
        assert event['receipt']['decision']=='exclude'
        assert 'not a new source review' in event['receipt']['reason']
        assert h.latest_finalized(conn,'weekly')['capture_id']==baseline


@pytest.mark.parametrize('defect',['version','new_finding','raw_hash','unbound_citation','no_prior',
    'prior_include','candidate','date_trigger','pending_source','ordinary_rule','missing_flag','inconsistent_hash',
    'person_kind','candidate_kind','contradictory_disposition','empty_citations'])
def test_proof_gaps_do_not_generate_a_discovery_exclusion(tmp_path,defect):
    run,db,_,_=baseline_and_next(tmp_path)
    cfg=w.load(run)
    with h.database(db) as conn:
        queue=w.latest_queue(conn,cfg)
        task=next(t for t in report.tasks(conn,cfg,queue) if t['identity']=='source:fixture-catalog')
        baseline=conn.execute('SELECT seq FROM captures WHERE capture_id=?',(cfg['baseline_capture'],)).fetchone()
        manifest=json.loads(conn.execute('SELECT manifest FROM publication_acceptances WHERE capture_id=?',(cfg['baseline_capture'],)).fetchone()[0])
        index=AcquisitionIndex(conn,'weekly')
        assert report.finalized_discovery_exclusion(conn,cfg,queue,task,baseline,manifest,index)
        prior=next(x for x in manifest['dispositions'] if x['finding_id']==task['identity'])
        if defect=='version':prior['version']='different'
        elif defect=='new_finding':task['inputs']['capture_seq']=baseline['seq']+1
        elif defect=='raw_hash':task['inputs']['sha256']='different'
        elif defect=='unbound_citation':prior['citations'][0]['http_status']=404
        elif defect=='no_prior':manifest['dispositions']=[]
        elif defect=='prior_include':prior['decision']='include'
        elif defect=='candidate':prior['candidate_key']='candidate-unreviewed'
        elif defect=='date_trigger':queue['source_reviews']['effective_date_tasks']=[{'type':'effective_date_reached'}]
        elif defect=='pending_source':queue['source_reviews']['tasks']=[{'reason':'changed'}]
        elif defect=='ordinary_rule':task['inputs']['finding']['facts']['discovery_only']=False
        elif defect=='missing_flag':task['inputs']['finding']['facts'].pop('publication_ready')
        elif defect=='person_kind':task['inputs']['finding']['kind']='judge'
        elif defect=='candidate_kind':task['inputs']['finding']['kind']='candidate'
        elif defect=='contradictory_disposition':task['inputs']['finding']['facts']['disposition']='include'
        elif defect=='empty_citations':prior['citations']=[]
        else:task['inputs']['finding']['facts']['summary']='Unreviewed altered facts.'
        if defect in ('ordinary_rule','missing_flag','person_kind','candidate_kind','contradictory_disposition'):
            # Keep the hash bindings consistent to test the specific predicate,
            # rather than passing only because the generic hash guard rejects it.
            task['inputs']['version']=h.sha(task['inputs']['finding'])
            prior['version']=task['inputs']['version']
        assert report.finalized_discovery_exclusion(conn,cfg,queue,task,baseline,manifest,index) is None


def test_corrupt_baseline_acceptance_cannot_create_machine_receipts(tmp_path):
    run,db,_,baseline=baseline_and_next(tmp_path)
    # Deliberate corruption in an isolated fixture database, never production.
    with h.database(db) as conn:
        conn.execute('UPDATE publication_acceptances SET manifest_sha256=? WHERE capture_id=?',('corrupt',baseline))
        conn.commit()
        assert conn.execute('SELECT manifest_sha256 FROM publication_acceptances WHERE capture_id=?',(baseline,)).fetchone()[0]=='corrupt'
    with pytest.raises(ValueError,match='Baseline acceptance checksum'):
        w.inspect(run)


def test_interrupted_machine_receipt_projection_recovers_from_database(tmp_path,monkeypatch):
    run,db,server,_=baseline_and_next(tmp_path);cfg=w.load(run);calls=list(server.calls)
    real_write=w.write
    def interrupted(path,value,**kwargs):
        if (Path(path).parent.name=='accepted' and isinstance(value,dict)
            and value.get('reuse',{}).get('policy')=='unchanged_finalized_discovery_exclusion_v1'):
            raise OSError('Fixture interruption after machine decision commit')
        return real_write(path,value,**kwargs)
    monkeypatch.setattr(w,'write',interrupted)
    with pytest.raises(OSError,match='after machine decision commit'):w.inspect(run)
    with h.database(db) as conn:
        event=next(e for e in w.accepted(conn,cfg).values() if e['task']['identity']=='source:fixture-catalog')
    path=w.projection_folder(cfg,'accepted')/(event['packet_sha256']+'.json')
    assert not path.exists()
    monkeypatch.setattr(w,'write',real_write)
    assert w.inspect(run)['phase']=='prepare_report'
    assert w.read(path)==event
    with h.database(db) as conn:
        assert len([e for e in w.events(conn,cfg) if e['kind']=='decision'
                    and e['task']['identity']=='source:fixture-catalog'])==1
    assert server.calls==calls
