import pytest
from flwu.research import validate_person_identity


@pytest.mark.parametrize('name', ['Chief Judge', 'Court Clerk', 'As Chief Judge',
                                  'Courthouse Locations Kim C. Hammond Justice Center', 'Unnamed'])
def test_placeholder_is_rejected_even_when_heading_is_in_source(name):
    with pytest.raises(ValueError, match='placeholder'):
        validate_person_identity({'name': name, 'citation': {'quote': name}})


def test_person_needs_name_in_cited_passage():
    with pytest.raises(ValueError, match='quote the actual'):
        validate_person_identity({'name': 'Matthew C. Lucas', 'citation': {'quote': 'Second District Court of Appeal'}})
    validate_person_identity({'name': 'Matthew C. Lucas',
                              'citation': {'quote': 'Judge Matthew C. Lucas serves on the court.'}})

from flwu import history as h
from flwu.evidence_binding import AcquisitionIndex


def acquired(conn):
    raw = b'Original bytes'; text = b'Judge Actual Person serves here.'
    observation = {'url': 'https://court.example/profile', 'sha256': h.sha(raw),
                   'text_sha256': h.sha(text), 'retrieved_at': '2026-10-22T12:00:00Z',
                   'http_status': 200, 'success': True}
    h.record(conn, stream='acquisition', mode='manual_research',
             scope={'target_stream':'report'}, run_id='fetch',
             payload={'status':'incomplete','contract':{},'checks':[], 'findings':[], 'drafts':[],
                      'source_gate':observation}, artifacts={h.sha(raw):raw,h.sha(text):text})
    return {k:v for k,v in observation.items() if k!='success'}


@pytest.mark.parametrize('field,value', [('url','https://court.example/another-page'),
    ('retrieved_at','2026-10-23T12:00:00Z'), ('http_status',201), ('text_sha256','0'*64)])
def test_report_rejects_reconstructed_acquisition_metadata(tmp_path, field, value):
    with h.database(tmp_path/'db') as conn:
        ref = acquired(conn)
        index = AcquisitionIndex(conn,'report')
        index.validate(ref)
        ref[field] = value
        with pytest.raises(ValueError, match='does not match'):
            index.validate(ref)


def test_report_cannot_use_another_stream_or_invent_quote(tmp_path):
    with h.database(tmp_path/'db') as conn:
        ref = acquired(conn)
        with pytest.raises(ValueError, match='does not match'):
            AcquisitionIndex(conn,'unrelated').validate(ref)
        ref.update(quote='Judge Imaginary Person',locator='paragraph 1')
        with pytest.raises(ValueError, match='quote absent'):
            AcquisitionIndex(conn,'report').validate(ref)

import json
from flwu import publication_acceptance as pa
from flwu.publication import export_capture


def report_fixture(conn, tmp_path):
    ref=acquired(conn)
    ref.update(quote='Judge Actual Person serves here.',locator='paragraph 1',synthetic=False)
    review={'id':'op1','relevance':'relevant','summary':'Supported holding.',
            'receipt_sha256':'a'*64,'pdf_sha256':ref['sha256']}
    h.record(conn,stream='report',mode='manual_research',scope={},run_id='screen',
             payload={'status':'incomplete','contract':{},'checks':[],'findings':[],'drafts':[],
                      'opinion_review':review},artifacts={})
    facts={'id':'op1','decision':'include','title':'Reviewed case','section':'case_law',
           'summary':'Supported holding.','publication_date':'2026-10-22','effective_date':None,'legal_status':'operative'}
    payload={'status':'ready_for_review','contract':{'window_start':'2026-10-16','window_end':'2026-10-22'},
             'checks':[{'id':'report','status':'verified','checked_at':h.now(),'hashes':[ref['sha256']]}],'drafts':[],
             'findings':[{'key':'case:op1','kind':'candidate','facts':facts,'citations':[ref]}]}
    from flwu import opinion_discovery as discovery
    bounds = {'start':'2026-10-16', 'end':'2026-10-22'}
    queue = {'run_id':'fixture-update','bounds':bounds,
             'source_reviews':{'tasks':[], 'effective_date_tasks':[], 'unregistered_previous_sources':[]},
             'opinion_reviews':{'tasks':[]},
             'discovery':{'courts':[], 'detail_failures':[], 'tracked_identity_failures':[]}}
    discovery.save(conn, 'report', 'fixture-update', 'update-result',
                   {'kind':'update-result','bounds':bounds,'complete':True,'queue_sha256':h.sha(queue)},
                   h.canonical(queue).encode())
    cap=h.record(conn,stream='report',mode='manual_research',scope={},run_id='report',payload=payload,artifacts={})
    report=tmp_path/'report.html';report.write_text('<h1>Reviewed case</h1><p>Supported holding.</p>')
    manifest=pa.template(conn,cap['capture_id'],report)
    manifest.update(reviewer='Fixture editor',legal_review='Checked fixture claim against source.',visual_review='Inspected fixture layout.')
    manifest['dispositions'][0].update(decision='include',candidate_key='case:op1',reason='Relevant procedural holding.')
    return cap,report,manifest,ref


def test_screening_cannot_finalize_but_separate_acceptance_can_publish(tmp_path):
    db=tmp_path/'db'
    with h.database(db) as conn:
        cap,report,manifest,_=report_fixture(conn,tmp_path)
        with pytest.raises(ValueError,match='Separate publication acceptance'):
            h.finalize(conn,cap['capture_id'],report,'Screened')
        assert not conn.execute('select 1 from finalized_reports').fetchone()
        pa.accept(conn,manifest,report)
        h.finalize(conn,cap['capture_id'],report,'Actual fixture editorial review')
    output=export_capture(db,cap['capture_id'],tmp_path/'archive')
    issue=json.loads(output.read_text())
    assert len(issue['sections']['case_law']['items'])==1
    assert issue['sections']['case_law']['items'][0]['summary']=='Supported holding.'


def test_omission_and_unsupported_exclusion_rejected(tmp_path):
    with h.database(tmp_path/'db') as conn:
        cap,report,manifest,ref=report_fixture(conn,tmp_path)
        missing=dict(manifest,dispositions=[])
        with pytest.raises(ValueError,match='Every relevant finding'):
            pa.accept(conn,missing,report)
        manifest['dispositions'][0].update(decision='exclude',candidate_key=None,citations=[])
        with pytest.raises(ValueError,match='Exclusion needs cited support'):
            pa.accept(conn,manifest,report)


def test_report_bytes_and_mapping_cannot_drift_after_acceptance(tmp_path):
    with h.database(tmp_path/'db') as conn:
        cap,report,manifest,_=report_fixture(conn,tmp_path)
        manifest['dispositions'][0]['candidate_key']='nonexistent'
        with pytest.raises(ValueError,match='actual candidate'):
            pa.accept(conn,manifest,report)
        manifest['dispositions'][0]['candidate_key']='case:op1'
        pa.accept(conn,manifest,report)
        report.write_text('An empty replacement report')
        with pytest.raises(ValueError,match='acceptance missing'):
            h.finalize(conn,cap['capture_id'],report,'Review')


def test_new_review_does_not_rewrite_accepted_snapshot_or_allow_stale_acceptance(tmp_path):
    """Future work cannot alter an accepted export or approve an obsolete report."""
    db = tmp_path/'db'
    with h.database(db) as conn:
        cap, report, manifest, ref = report_fixture(conn, tmp_path)
        pa.accept(conn, manifest, report)
        h.finalize(conn, cap['capture_id'], report, 'Fixture editor reviewed report')
        h.record(conn, stream='report', mode='manual_research', scope={}, run_id='next-review',
                 payload={'status':'incomplete','contract':{},'checks':[], 'findings':[], 'drafts':[],
                          'opinion_review':{'id':'op1','relevance':'relevant',
                              'summary':'A later corrected holding.', 'receipt_sha256':'b'*64,
                              'pdf_sha256':ref['sha256']}}, artifacts={})
        with pytest.raises(ValueError, match='latest report'):
            pa.accept(conn, manifest, report)
        with pytest.raises(ValueError, match='latest captured state'):
            h.finalize(conn, cap['capture_id'], report, 'Cannot advance stale baseline')
    output = export_capture(db, cap['capture_id'], tmp_path/'archive')
    issue = json.loads(output.read_text())
    assert issue['sections']['case_law']['items'][0]['summary'] == 'Supported holding.'


def test_acquisition_sequence_zero_does_not_expose_later_observations(tmp_path):
    with h.database(tmp_path/'db') as conn:
        ref = acquired(conn)
        with pytest.raises(ValueError, match='does not match'):
            AcquisitionIndex(conn, 'report', through_seq=0).validate(ref)


@pytest.mark.parametrize('operation', ['accept', 'finalize'])
def test_publication_holds_write_lock_during_validation(tmp_path, monkeypatch, operation):
    import sqlite3
    db = tmp_path/'db'
    with h.database(db) as conn, h.database(db) as competitor:
        cap, report, manifest, _ = report_fixture(conn, tmp_path)
        if operation == 'finalize':
            pa.accept(conn, manifest, report)
        competitor.execute('PRAGMA busy_timeout=0')
        original = pa.validate
        attempted = []

        def competing_validate(*args, **kwargs):
            # A real second SQLite connection attempts a write during validation.
            with pytest.raises(sqlite3.OperationalError, match='locked'):
                competitor.execute("INSERT INTO streams VALUES('concurrent','manual_research','{}')")
            competitor.rollback()
            attempted.append(True)
            return original(*args, **kwargs)

        monkeypatch.setattr(pa, 'validate', competing_validate)
        if operation == 'accept':
            pa.accept(conn, manifest, report)
        else:
            h.finalize(conn, cap['capture_id'], report, 'Fixture review')
        assert attempted == [True]
        assert not conn.in_transaction
        # Reservation is released after success, not retained indefinitely.
        competitor.execute("INSERT INTO streams VALUES('after','manual_research','{}')")
        competitor.commit()


def test_failed_acceptance_rolls_back_and_releases_reservation(tmp_path):
    with h.database(tmp_path/'db') as conn:
        cap, report, manifest, _ = report_fixture(conn, tmp_path)
        manifest['dispositions'] = []
        with pytest.raises(ValueError, match='Every relevant finding'):
            pa.accept(conn, manifest, report)
        assert not conn.in_transaction
        assert not conn.execute("SELECT 1 FROM sqlite_master WHERE name='publication_acceptances'").fetchone()
        assert not conn.execute('SELECT 1 FROM finalized_reports').fetchone()


@pytest.mark.parametrize('field,value', [('finding_id', []), ('candidate_key', {}), ('citations', 'not citations')])
def test_malformed_acceptance_returns_validation_error_without_persistence(tmp_path, field, value):
    with h.database(tmp_path/'db') as conn:
        _, report, manifest, _ = report_fixture(conn, tmp_path)
        manifest['dispositions'][0][field] = value
        with pytest.raises(ValueError):
            pa.accept(conn, manifest, report)
        assert not conn.in_transaction
        assert not conn.execute('SELECT 1 FROM finalized_reports').fetchone()


@pytest.mark.parametrize('failure', ['missing', 'wrong_name', 'wrong_role', 'unrostered', 'conflicting_id'])
def test_roster_and_personnel_records_must_reconcile(tmp_path, failure):
    with h.database(tmp_path/'db') as conn:
        cap, report, manifest, ref = report_fixture(conn, tmp_path)
        payload = json.loads(pa.report_row(conn, cap['capture_id'])['payload'])
        entity = {'id':'actual-person', 'name':'Actual Person', 'type':'judge', 'citation':ref}
        payload['findings'].extend([
            {'key':'roster-test', 'kind':'source_inventory', 'facts':{'entities':[entity]}, 'citations':[ref]},
            {'key':'person-actual-person', 'kind':'judge', 'facts':{'name':'Actual Person'}, 'citations':[ref]}])
        manifest['rosters'] = [{'inventory_key':'roster-test', 'people':[entity], 'reason':'Reviewed named roster'}]
        if failure == 'missing':
            payload['findings'].pop()
        elif failure == 'wrong_name':
            payload['findings'][-1]['facts']['name'] = 'Different Person'
        elif failure == 'wrong_role':
            payload['findings'][-1]['kind'] = 'clerk'
        elif failure == 'unrostered':
            payload['findings'].append({'key':'person-other', 'kind':'judge', 'facts':{'name':'Other Person'}, 'citations':[ref]})
        else:
            other = dict(entity, type='clerk')
            payload['findings'].append({'key':'roster-other', 'kind':'source_inventory', 'facts':{'entities':[other]}, 'citations':[ref]})
            manifest['rosters'].append({'inventory_key':'roster-other','people':[other],'reason':'Conflicting role'})
        updated = h.record(conn, stream='report', mode='manual_research', scope={}, run_id='roster-report', payload=payload, artifacts={})
        manifest['capture_id'] = updated['capture_id']
        with pytest.raises(ValueError, match='roster|Roster'):
            pa.accept(conn, manifest, report)
        assert not conn.execute('SELECT 1 FROM finalized_reports').fetchone()


def test_removed_roster_requires_supported_disposition_even_if_inventory_disappears(tmp_path):
    with h.database(tmp_path/'db') as conn:
        cap, report, manifest, ref = report_fixture(conn, tmp_path)
        payload = json.loads(pa.report_row(conn, cap['capture_id'])['payload'])
        person = {'id':'actual-person','name':'Actual Person','type':'judge','citation':ref}
        payload['findings'].extend([
            {'key':'roster-test','kind':'source_inventory','facts':{'entities':[person]},'citations':[ref]},
            {'key':'person-actual-person','kind':'judge','facts':{'name':'Actual Person'},'citations':[ref]}])
        first = h.record(conn,stream='report',mode='manual_research',scope={},run_id='first-roster',payload=payload,artifacts={})
        manifest['capture_id'] = first['capture_id']
        manifest['rosters'] = [{'inventory_key':'roster-test','people':[person],'reason':'Named official roster'}]
        pa.accept(conn,manifest,report)
        h.finalize(conn,first['capture_id'],report,'Fixture legal and visual review')
        notice = b'Judge Actual Person retired.'
        departure = dict(ref, sha256=h.sha(notice), text_sha256=h.sha(notice),
                         quote=notice.decode(), url='https://court.example/retirement')
        h.record(conn,stream='acquisition',mode='manual_research',scope={'target_stream':'report'},run_id='departure',
                 payload={'status':'incomplete','contract':{},'checks':[],'findings':[],'drafts':[],
                          'source_gate':dict(departure,success=True)},artifacts={h.sha(notice):notice})
        payload['findings'] = payload['findings'][:1]
        second = h.record(conn,stream='report',mode='manual_research',scope={},run_id='second-roster',payload=payload,artifacts={})
        fresh = pa.template(conn,second['capture_id'],report)
        assert fresh['rosters'][0]['removals'][0]['id'] == 'actual-person'
        fresh.update(reviewer=manifest['reviewer'],legal_review=manifest['legal_review'],visual_review=manifest['visual_review'],
                     dispositions=manifest['dispositions'])
        fresh['rosters'][0]['reason'] = 'Official retirement notice'
        with pytest.raises(ValueError,match='cited substantive'):
            pa.accept(conn,fresh,report)
        fresh['rosters'][0]['removals'][0].update(reason='Official notice states retirement.',citations=[departure])
        pa.accept(conn,fresh,report)
        h.finalize(conn,second['capture_id'],report,'Reviewed supported departure')
        assert conn.execute('SELECT count(*) FROM finalized_reports').fetchone()[0] == 2


def test_cli_template_accept_finalize_and_reject_modified_report(tmp_path, capsys):
    from flwu.cli import main
    db = tmp_path/'db'
    with h.database(db) as conn:
        cap, report, approved, _ = report_fixture(conn, tmp_path)
    receipt_path = tmp_path/'acceptance.json'
    assert main(['history','review-template','--database',str(db),'--capture-id',cap['capture_id'],
                 '--report',str(report),'--output',str(receipt_path)]) == 0
    generated = json.loads(receipt_path.read_text())
    assert generated['dispositions'][0]['finding_id'] == 'opinion:op1'
    assert generated['reviewer'] == ''
    assert main(['history','accept','--database',str(db),'--receipt',str(receipt_path),'--report',str(report)]) == 1
    receipt_path.write_text(json.dumps(approved))
    assert main(['history','accept','--database',str(db),'--receipt',str(receipt_path),'--report',str(report)]) == 0
    assert main(['history','finalize','--database',str(db),'--capture-id',cap['capture_id'],
                 '--report',str(report),'--review','Fixture editor checked content and rendering']) == 0
    report.write_text('Changed report without renewed review')
    assert main(['history','finalize','--database',str(db),'--capture-id',cap['capture_id'],
                 '--report',str(report),'--review','Unsupported reuse']) == 1
    with h.database(db) as conn:
        assert conn.execute('SELECT count(*) FROM finalized_reports').fetchone()[0] == 1


@pytest.mark.parametrize('failure', ['binding', 'artifact', 'wrong_dates'])
def test_report_requires_exact_saved_update_snapshot(tmp_path, failure):
    with h.database(tmp_path/'db') as conn:
        cap, report, manifest, _ = report_fixture(conn, tmp_path)
        if failure == 'binding':
            manifest['acquisition']['run_id'] = 'different-update'
        elif failure == 'artifact':
            with conn:
                conn.execute('UPDATE artifacts SET bytes=? WHERE sha256=?',
                             (b'corrupted',manifest['acquisition']['queue_sha256']))
        else:
            payload = json.loads(pa.report_row(conn,cap['capture_id'])['payload'])
            payload['contract']['window_start'] = '2026-10-01'
            cap = h.record(conn,stream='report',mode='manual_research',scope={},run_id='other-window',payload=payload,artifacts={})
            manifest['capture_id'] = cap['capture_id']
        with pytest.raises(ValueError,match='acquisition binding|queue artifact|standard update result'):
            pa.accept(conn,manifest,report)
        assert not conn.execute('SELECT 1 FROM finalized_reports').fetchone()


@pytest.mark.parametrize('mismatch', [None, 'url', 'retrieved_at', 'sha256'])
def test_legacy_status_transport_reused_only_from_exact_saved_parent(tmp_path, mismatch):
    from flwu import opinion_discovery as discovery
    with h.database(tmp_path/'db') as conn:
        raw = b'Official status response'
        metadata = {'status':'withdrawn'}
        ref = {'url':'https://court.example/status','retrieved_at':'2026-10-22T12:00:00Z',
               'sha256':h.sha(raw),'text_sha256':h.sha(metadata)}
        transport = {'url':ref['url'],'retrieved_at':ref['retrieved_at'],'http_status':200,'success':True}
        event = {'kind':'detail','complete':True,'sha256':ref['sha256'],'source':transport,
                 'entries':[{'metadata':metadata,'status_source':ref}]}
        if mismatch == 'sha256':
            event['sha256'] = '0'*64
        elif mismatch:
            transport[mismatch] = 'different'
        discovery.save(conn,'report','legacy','detail:test',event,raw)
        cite = dict(ref,http_status=200,quote='withdrawn',locator='status')
        index = AcquisitionIndex(conn,'report')
        if mismatch:
            with pytest.raises(ValueError,match='does not match'):
                index.validate(cite)
        else:
            index.validate(cite)


def test_pending_acquisition_tasks_cannot_disappear_or_be_called_unavailable(tmp_path):
    from flwu import publication_pending as pending
    with h.database(tmp_path/'db') as conn:
        ref = acquired(conn)
        ref.update(quote='Judge Actual Person serves here.',locator='paragraph 1')
        index = AcquisitionIndex(conn,'report')
        queue = {'source_reviews':{'tasks':[{'source_id':'source-1','reason':'changed','observation':ref}],
                    'effective_date_tasks':[], 'unregistered_previous_sources':[]},
                 'opinion_reviews':{'tasks':[]},
                 'discovery':{'courts':[], 'detail_failures':[], 'tracked_identity_failures':[]}}
        with pytest.raises(ValueError,match='Every pending'):
            pending.validate(queue,[],index)
        dispositions = pending.template(queue)
        dispositions[0].update(decision='unavailable',reason='Skipped')
        with pytest.raises(ValueError,match='Available unreviewed'):
            pending.validate(queue,dispositions,index)
        dispositions[0].update(decision='scope_excluded',reason='Fixture demonstrates supported scope disposition')
        with pytest.raises(ValueError,match='cited support'):
            pending.validate(queue,dispositions,index)
        dispositions[0]['citations'] = [ref]
        pending.validate(queue,dispositions,index)
        queue['source_reviews']['tasks'][0]['reason'] = 'retrieval_failed'
        dispositions = pending.template(queue)
        dispositions[0].update(decision='unavailable',reason='Saved retrieval failed; no no-change conclusion.')
        pending.validate(queue,dispositions,index)


def test_all_pending_categories_are_enumerated_and_unknown_queue_is_rejected():
    from flwu import publication_pending as pending
    queue = {'source_reviews':{'tasks':[], 'effective_date_tasks':[{'key':'rule'}],
                               'unregistered_previous_sources':['https://court.example/removed']},
             'opinion_reviews':{'tasks':[{'opinion':{'id':'case'},'reasons':['new_or_unreviewed_opinion']}]},
             'discovery':{'courts':[{'id':'first','complete':False}],
                          'detail_failures':[{'id':'case'}], 'tracked_identity_failures':[{'url':'missing'}]}}
    assert {key.split(':')[0] for key in pending.pending(queue)} == {
        'effective_date','unregistered_source','opinion','listing_failure','detail_failures','tracked_identity_failures'}
    with pytest.raises(ValueError,match='lacks'):
        pending.pending({})


@pytest.mark.parametrize('alter_contact', [False, True])
def test_reviewed_contact_finding_maps_to_directory_without_news_item(tmp_path, alter_contact):
    with h.database(tmp_path/'db') as conn:
        cap, report, _, ref = report_fixture(conn,tmp_path)
        facts = {'name':'Actual Person','fields':{'chambers_phone':{'value':'555-0100'}}}
        finding = {'key':'person-actual-person','kind':'judge','facts':facts,'citations':[ref]}
        h.record(conn,stream='report',mode='manual_research',scope={},run_id='contact-review',
                 payload={'status':'incomplete','contract':{},'checks':[],'drafts':[], 'findings':[finding],
                          'source_gate_review':{'acceptance_version':3,'sha256':ref['sha256']}},artifacts={})
        payload=json.loads(pa.report_row(conn,cap['capture_id'])['payload'])
        payload['findings'].extend([finding, {'key':'roster-test','kind':'source_inventory',
            'facts':{'entities':[{'id':'actual-person','name':'Actual Person','type':'judge','citation':ref}]},'citations':[ref]}])
        if alter_contact:
            payload['findings'][-2]['facts']['fields']['chambers_phone']['value']='555-9999'
        new=h.record(conn,stream='report',mode='manual_research',scope={},run_id='contact-report',payload=payload,artifacts={})
        report.write_text(report.read_text()+'<p>Actual Person: 555-0100</p>')
        manifest=pa.template(conn,new['capture_id'],report)
        manifest.update(reviewer='Editor',legal_review='Checked contact evidence',visual_review='Checked report and directory')
        manifest['rosters'][0]['reason']='Named official roster'
        for disposition in manifest['dispositions']:
            disposition.update(reason='Supported finding')
            if disposition['finding_id'].startswith('source:'):
                disposition.update(decision='include_directory',candidate_key='person-actual-person')
            else:
                disposition.update(decision='include',candidate_key='case:op1')
        if alter_contact:
            with pytest.raises(ValueError,match='retain the reviewed personnel facts'):
                pa.accept(conn,manifest,report)
        else:
            pa.accept(conn,manifest,report)
            h.finalize(conn,new['capture_id'],report,'Reviewed contact and opinion')


def test_explicit_invalidation_preserves_evidence_and_removes_baseline_eligibility(tmp_path):
    from flwu import opinion_discovery as discovery
    db=tmp_path/'db'
    with h.database(db) as conn:
        first, report, manifest, _ = report_fixture(conn,tmp_path)
        pa.accept(conn,manifest,report)
        h.finalize(conn,first['capture_id'],report,'Reviewed first fixture')
        second, report, manifest, _ = report_fixture(conn,tmp_path)
        assert second['capture_id'] != first['capture_id']
        pa.accept(conn,manifest,report)
        h.finalize(conn,second['capture_id'],report,'Reviewed second fixture')
        counts = [conn.execute('SELECT count(*) FROM '+table).fetchone()[0]
                  for table in ('captures','artifacts','finalized_reports')]
        assert h.latest_finalized(conn,'report')['capture_id'] == second['capture_id']
        result=h.invalidate_report(conn,second['capture_id'],'Editor','Erroneous current report')
        assert h.invalidate_report(conn,second['capture_id'],'Editor','Erroneous current report') == result
        with pytest.raises(ValueError,match='immutable'):
            h.invalidate_report(conn,second['capture_id'],'Editor','Different explanation')
        assert h.latest_finalized(conn,'report')['capture_id'] == first['capture_id']
        assert discovery.window(conn,'report',end='2099-01-01')['finalized_baseline_capture'] == first['capture_id']
        assert counts == [conn.execute('SELECT count(*) FROM '+table).fetchone()[0]
                          for table in ('captures','artifacts','finalized_reports')]
        with pytest.raises(ValueError,match='Invalidated'):
            h.finalize(conn,second['capture_id'],report,'Reapprove same report')
        with pytest.raises(ValueError,match='Invalidated'):
            pa.accept(conn,manifest,report)
    with pytest.raises(ValueError,match='Invalidated'):
        export_capture(db,second['capture_id'],tmp_path/'archive')


def test_invalidation_requires_existing_finalization_and_is_stream_specific(tmp_path):
    with h.database(tmp_path/'db') as conn:
        cap, report, manifest, _=report_fixture(conn,tmp_path)
        with pytest.raises(ValueError,match='existing finalized'):
            h.invalidate_report(conn,cap['capture_id'],'Editor','Not yet published')
        pa.accept(conn,manifest,report)
        h.finalize(conn,cap['capture_id'],report,'Reviewed fixture')
        h.invalidate_report(conn,cap['capture_id'],'Editor','Withdraw erroneous fixture')
        assert h.latest_finalized(conn,'report') is None
        assert h.latest_finalized(conn,'unrelated') is None
