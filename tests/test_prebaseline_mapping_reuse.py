"""The reporting boundary is code; interpretation and change screening stay reviewed."""
import copy
import json
from pathlib import Path

import pytest

from flwu import history as h, workflow as w, workflow_report as report
from flwu import workflow_directory as directory, workflow_release as release
from flwu import update, opinion_discovery as opinions
from flwu.evidence_binding import AcquisitionIndex
from tests.test_workflow import environment, answer


def baseline_and_next(tmp_path, *, start='2026-10-23', mutate=None, legacy=False):
    run, db, registry, server = environment(tmp_path)
    while True:
        task = w.inspect(run, emit=True)
        if task['kind'] == 'publication_mapping':
            packet = w.read(task['packet']); receipt = copy.deepcopy(packet['receipt_template'])
            receipt.update(decision='exclude', candidate=None,
                reason='Fixture opinion retained as comparison context; not news in the fixture baseline.')
            w.write(task['save_receipt'], receipt); w.submit(run,task['packet'],task['save_receipt'])
            break
        answer(run,db,task)
    prepared=report.prepare(run);directory.refresh(run);release.build(run)
    answer(run,db,w.inspect(run,emit=True))
    with h.database(db) as conn:
        baseline_id=prepared['capture_id']
        if legacy:
            from flwu import publication_acceptance
            payload=json.loads(conn.execute('SELECT payload FROM captures WHERE capture_id=?',
                                            (baseline_id,)).fetchone()[0])
            payload.pop('workflow_report')
            manifest=json.loads(conn.execute('SELECT manifest FROM publication_acceptances WHERE capture_id=?',
                                             (baseline_id,)).fetchone()[0])
            saved=h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},
                           run_id='legacy-format-baseline',payload=payload,artifacts={})
            baseline_id=saved['capture_id'];manifest['capture_id']=baseline_id
            publication_acceptance.accept(conn,manifest,Path(prepared['report']))
        h.finalize(conn,baseline_id,Path(prepared['report']),'Fixture baseline')
        before = h.latest_finalized(conn,'weekly')['capture_id']
    if mutate:mutate(db,registry,server)
    second=tmp_path/'next'
    w.initialize(second,db,tmp_path/'registry.json','next',start=start,end='2026-10-29')
    with h.database(db) as conn:
        update.run(conn,registry,'next',second,start=start,end='2026-10-29',fetch=server)
    return second,db,registry,server,before


@pytest.mark.parametrize('legacy',[False,True])
def test_unchanged_prebaseline_excluded_opinion_maps_without_new_model_review(tmp_path,legacy):
    run,db,_,server,baseline=baseline_and_next(tmp_path,legacy=legacy)
    calls=list(server.calls)
    phase=w.inspect(run,emit=True)
    assert phase['phase']=='prepare_report'
    config=w.load(run)
    with h.database(db) as conn:
        events=list(w.accepted(conn,config).values())
        reused=[e for e in events if e.get('reuse',{}).get('policy')=='unchanged_prebaseline_opinion_outside_period']
        assert len(reused)==1
        event=reused[0]
        assert event['receipt']['decision']=='exclude' and event['receipt']['candidate'] is None
        assert event['reuse']['baseline_capture']==baseline
        assert event['reuse']['review_receipt_sha256']==event['task']['inputs']['version']
        assert event['reuse']['opinion_signature']
        assert conn.execute('SELECT 1 FROM captures WHERE capture_id=?',
                            (event['reuse']['current_acquisition_capture_id'],)).fetchone()
        assert h.latest_finalized(conn,'weekly')['capture_id']==baseline
        before=w.events(conn,config)
    assert w.inspect(run)['phase']=='prepare_report'
    with h.database(db) as conn:assert w.events(conn,config)==before
    assert server.calls==calls


@pytest.mark.parametrize('start',['2026-10-19','2026-10-20'])
def test_in_window_and_boundary_dates_still_require_mapping(tmp_path,start):
    run,db,_,_,_=baseline_and_next(tmp_path,start=start)
    assert w.inspect(run,emit=True)['phase']=='publication_mapping'
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


@pytest.mark.parametrize('change',['status','pdf'])
def test_status_and_original_changes_still_require_review(tmp_path,change):
    def mutate(db,registry,server):
        if change=='pdf':
            from tests.test_opinion_discovery import pdf_bytes
            server.pdf=pdf_bytes('Changed holding. Affirmed. Author Example.')
        else:server.entries[0]['content']['fields']['note']='Withdrawn'
    run,db,_,_,_=baseline_and_next(tmp_path,mutate=mutate)
    task=w.inspect(run,emit=True)
    assert task['phase']=='opinion_review'
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


def test_later_editorial_revision_cannot_reuse_old_interpretation(tmp_path):
    def mutate(db,registry,server):
        with h.database(db) as conn:
            previous=next(r for row in reversed(opinions.g.rows(conn,registry['stream']))
                if (r:=json.loads(row['payload']).get('opinion_review')))
            keys={'id','signature','reviewer','relevance','summary','holding','disposition','authors','citations'}
            receipt={k:copy.deepcopy(previous[k]) for k in keys}
            receipt.update(predecessor_version=previous['receipt_sha256'],reason='Fixture editorial correction.',
                review_protocol=registry['review_protocol'],pdf_sha256=previous['pdf_sha256'],
                state_sha256=previous['state_sha256'],summary='Corrected commercial opinion.')
            citation=receipt['citations'][0]
            citation.update(quote=opinions.g.blob(conn,citation['text_sha256']).decode(),
                            locator='Entire fixture opinion including author')
            opinions.revise_review(conn,registry,receipt)
    run,db,_,_,_=baseline_and_next(tmp_path,mutate=mutate)
    assert w.inspect(run,emit=True)['phase']=='publication_mapping'
    with h.database(db) as conn:assert not w.accepted(conn,w.load(run))


def test_late_discovered_old_date_requires_new_review(tmp_path):
    from tests.test_opinion_discovery import opinion
    def mutate(db,registry,server):
        server.entries.append(opinion(2,day='2026-10-19'))
    run,db,_,_,_=baseline_and_next(tmp_path,mutate=mutate)
    task=w.inspect(run,emit=True)
    assert task['phase']=='opinion_review'
    assert 'new_or_unreviewed_opinion' in w.read(task['packet'])['inputs']['reasons']
    with h.database(db) as conn:
        decisions=w.accepted(conn,w.load(run))
        assert all(e['task']['identity']!='opinion:'+opinions.document_id('1dca','content:2')
                   for e in decisions.values())


@pytest.mark.parametrize('defect',['not_reused','late_review','date_mismatch','invalid_date',
    'missing_date','missing_citation_status','signature_mismatch','unavailable','wrong_pdf'])
def test_proof_gaps_never_generate_a_scope_exclusion(tmp_path,defect):
    run,db,_,_,_=baseline_and_next(tmp_path)
    config=w.load(run)
    with h.database(db) as conn:
        queue=w.latest_queue(conn,config);task=next(t for t in report.tasks(conn,config,queue)
            if t['kind']=='publication_mapping')
        baseline=conn.execute('SELECT seq FROM captures WHERE capture_id=?',(config['baseline_capture'],)).fetchone()
        index=AcquisitionIndex(conn,config['registry']['stream']);known=opinions.known(conn,config['registry']['stream'])
        identity=task['inputs']['finding']['facts']['id']
        assert report.prebaseline_opinion_exclusion(conn,config,queue,task,baseline,index,known)
        if defect=='not_reused':queue['opinion_reviews']['reused_reviews']=[]
        elif defect=='late_review':task['inputs']['capture_seq']=baseline['seq']+1
        elif defect=='date_mismatch':task['inputs']['finding']['facts']['published_date']='2026-10-19'
        elif defect=='invalid_date':task['inputs']['finding']['facts']['published_date']='2026-99-01'
        elif defect=='missing_date':task['inputs']['finding']['facts']['published_date']=None
        elif defect=='missing_citation_status':
            for cite in task['inputs']['finding']['citations']:cite.pop('http_status',None)
        elif defect=='signature_mismatch':config['registry']['review_protocol']='unreviewed-protocol'
        elif defect=='unavailable':index.source_observations[known[identity]['pdf_url']]['success']=False
        else:index.source_observations[known[identity]['pdf_url']]['sha256']='changed-original'
        assert report.prebaseline_opinion_exclusion(conn,config,queue,task,baseline,index,known) is None
