import copy
import json
import pytest
from flwu import history as h
from flwu import source_limitations as sl


def fixture(conn, status=403, body=b'Forbidden', success=False, target='report'):
    obs = dict(url='https://court.example/required', sha256=h.sha(body), text_sha256=h.sha(body),
               retrieved_at='2026-10-22T12:00:00Z', http_status=status, success=success)
    saved = h.record(conn, stream='sources', mode='manual_research', scope={'target_stream':target},
                     run_id='observation', payload={'status':'incomplete','checks':[],'findings':[],
                                                  'drafts':[],'source_gate':obs}, artifacts={h.sha(body):body})
    task = dict(id='S01', kind='source', url=obs['url'])
    limitation = dict(task_id='S01', observation_capture_id=saved['capture_id'],
                      **{k:obs[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')},
                      category='invalid_content' if success else 'retrieval_failed', reviewer='Reviewer',
                      reason='Saved source could not supply official content.', reviewed_scope='Required landing page.',
                      pending_work=[], invalid_content_quote=body.decode() if success else None, alternatives=[])
    return task, limitation, saved


@pytest.mark.parametrize('status', [403, 404])
def test_exact_failed_source_remains_a_limitation(tmp_path, status):
    with h.database(tmp_path/'db') as c:
        task, limit, _ = fixture(c, status=status)
        assert sl.validate(c,'report',task,limit) == h.sha(limit)


@pytest.mark.parametrize('key,value', [('url','https://court.example/substitute'), ('http_status',200),
    ('retrieved_at','2026-10-23T12:00:00Z'), ('sha256','0'*64), ('text_sha256','0'*64),
    ('observation_capture_id','invented'), ('category','extraction_incomplete'),
    ('pending_work',['Unread linked page']), ('reviewer','')])
def test_limitation_rejects_forgery_and_unfinished_work(tmp_path,key,value):
    with h.database(tmp_path/'db') as c:
        task, limit, _ = fixture(c);limit[key]=value
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)


def test_invalid_http200_needs_actual_invalid_content_quote(tmp_path):
    with h.database(tmp_path/'db') as c:
        task, limit, _ = fixture(c, status=200, body=b'This domain is for sale.', success=True)
        sl.validate(c,'report',task,limit)
        limit['invalid_content_quote']='Invented domain for sale'
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)


def test_valid_official_content_cannot_be_called_a_failure(tmp_path):
    with h.database(tmp_path/'db') as c:
        task, limit, _ = fixture(c,status=200,body=b'Official civil procedure requirements.',success=True)
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)
        limit.update(category='retrieval_failed',invalid_content_quote=None)
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)


def test_official_http200_not_found_body_is_not_successful_coverage(tmp_path):
    with h.database(tmp_path/'db') as c:
        task, limit, _ = fixture(c,status=200,success=True,
                                body=b"Court title\nWe're sorry, the page you have requested cannot be found.\nFooter")
        assert sl.validate(c,'report',task,limit) == h.sha(limit)
        limit['invalid_content_quote'] = 'the page you have requested cannot be found'
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)
        limit.update(category='retrieval_failed',invalid_content_quote=None)
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)


def test_limitation_cannot_excuse_roster_or_use_other_stream(tmp_path):
    with h.database(tmp_path/'db') as c:
        task, limit, saved = fixture(c)
        with pytest.raises(ValueError):sl.validate(c,'elsewhere',task,limit)
        with pytest.raises(ValueError):sl.validate(c,'report',dict(task,kind='roster'),limit)
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit,through_seq=saved['seq']-1)


def test_receipt_capture_preserves_limitation_without_success_or_no_change(tmp_path):
    from flwu.research import inspect_run, digest
    from flwu.history_capture import stream_for
    contract = dict(mode='manual_research', profile='test', counties=[], circuits=[],
                    cutoff_utc='2026-10-22T00:00:00+00:00', window_start='2026-10-16',window_end='2026-10-22',
                    tasks=[dict(id='S01',kind='source',group='statutes',url='https://court.example/required')])
    target = stream_for(contract)[0];db=tmp_path/'db';root=tmp_path/'run';(root/'receipts').mkdir(parents=True)
    with h.database(db) as c:_, limit, _=fixture(c,target=target)
    (root/'contract.json').write_text(json.dumps(contract));(root/'contract.sha256').write_text(digest(contract))
    receipt=dict(task_id='S01',status=sl.STATUS,checked_at='2026-10-22T13:00:00Z',errors=[],
                 pages=[],pages_complete=False,reviewed_pages_complete=True,candidates=[],entities=[],source_limitation=limit)
    (root/'receipts/S01.json').write_text(json.dumps(receipt))
    status=inspect_run(root,history_db=db)
    assert status['status']=='ready_for_review' and status['evidence_valid']==0
    assert status['reviewed_source_limitations']==1
    with h.database(db) as c:
        row=c.execute('SELECT payload FROM captures WHERE stream=? ORDER BY seq DESC',(target,)).fetchone()
        payload=json.loads(row[0]);assert payload['checks'][0]['status']==sl.STATUS
        assert payload['checks'][0]['limitation']==limit and not payload['findings']
        assert h.compare(c,target)['assessment']=='insufficient_coverage'
        assert h.latest_finalized(c,target) is None


@pytest.mark.parametrize('linked', [False, True])
def test_limitation_needs_explicit_acceptance_and_survives_export(tmp_path, linked):
    from tests.test_publication_evidence_gates import report_fixture
    from flwu import publication_acceptance as pa
    from flwu.publication import export_capture
    db=tmp_path/'db'
    with h.database(db) as c:
        task,limit,_=linked_fixture(c) if linked else fixture(c)
        task['group']='statutes'
        cap,report,manifest,_=report_fixture(c,tmp_path)
        payload=json.loads(c.execute('SELECT payload FROM captures WHERE capture_id=?',(cap['capture_id'],)).fetchone()[0])
        payload['contract']['tasks']=[task]
        payload['checks'].append(dict(id=task['id'],status=sl.STATUS,limitation=limit,hashes=[],checked_at=None))
        revised=h.record(c,stream='report',mode='manual_research',scope={},run_id='with-limitation',payload=payload,artifacts={})
        manifest['capture_id']=revised['capture_id']
        with pytest.raises(ValueError,match='acknowledgment'):pa.accept(c,manifest,report)
        assert h.latest_finalized(c,'report') is None
        manifest['source_limitations']=[dict(task_id=task['id'],sha256=h.sha(limit),acknowledged=False,reason='Reviewed saved failure.')]
        with pytest.raises(ValueError,match='acknowledgment'):pa.accept(c,manifest,report)
        manifest['source_limitations'][0]['acknowledged']=True
        pa.accept(c,manifest,report)
        h.finalize(c,revised['capture_id'],report,'Separate legal and visual review completed.')
    output=export_capture(db,revised['capture_id'],tmp_path/'archive')
    issue=json.loads(output.read_text());public=issue['provenance']['source_limitations'][0]
    assert public['url']==limit['url'] and public['http_status']==403
    assert public['category']=='retrieval_failed' and public['sha256']==limit['sha256']
    assert 'path' not in public and 'alternatives' not in public
    if linked:
        assert public['required_url'] == task['url']
        assert public['discovery_observations'][0]['target_url'] == limit['url']
        assert public['discovery_observations'][0]['http_status'] == 200
    assert issue['sections']['statutes']['status']=='incomplete'
    assert issue['sections']['case_law']['status']=='reviewed'
    from flwu.publication import validate_issue, digest
    changed=copy.deepcopy(issue);changed['sections']['statutes']['status']='reviewed'
    changed['content_sha256']=digest({k:v for k,v in changed.items() if k!='content_sha256'})
    with pytest.raises(ValueError,match='fully reviewed'):validate_issue(changed)
    changed=copy.deepcopy(issue);del changed['provenance']['source_limitations']
    changed['content_sha256']=digest({k:v for k,v in changed.items() if k!='content_sha256'})
    with pytest.raises(ValueError,match='Incomplete section'):validate_issue(changed)


def linked_fixture(conn):
    task, limit, failed = fixture(conn)
    task = dict(task, url='https://court.example/')
    body=b'<a href="/required">Court information</a>'
    obs=dict(url=task['url'],sha256=h.sha(body),text_sha256=None,
             retrieved_at='2026-10-22T11:00:00Z',http_status=200,success=True)
    saved=h.record(conn,stream='sources',mode='manual_research',scope={'target_stream':'report'},
                   run_id='parent',payload={'status':'incomplete','checks':[],'findings':[],
                   'drafts':[],'source_gate':obs},artifacts={h.sha(body):body})
    hop={k:obs[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')}
    hop.update(observation_capture_id=saved['capture_id'],reference='/required',target_url=limit['url'])
    limit['discovery_path']=[hop]
    return task,limit,saved


def test_linked_failure_preserves_parent_and_failed_endpoint(tmp_path):
    with h.database(tmp_path/'db') as c:
        task,limit,saved=linked_fixture(c)
        assert sl.validate(c,'report',task,limit)==h.sha(limit)
        assert limit['http_status']==403 and limit['discovery_path'][0]['http_status']==200
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit,through_seq=saved['seq']-1)
        limit.pop('discovery_path')
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)


@pytest.mark.parametrize('field,value', [('url','https://court.example/other'),
    ('reference','/unrelated'),('reference','/require'),('target_url','https://other.example/required'),
    ('sha256','0'*64),('http_status',403),('retrieved_at','invented'),('observation_capture_id','missing')])
def test_linked_failure_rejects_unproven_or_forged_path(tmp_path,field,value):
    with h.database(tmp_path/'db') as c:
        task,limit,_=linked_fixture(c);limit['discovery_path'][0][field]=value
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)


def test_linked_failure_cannot_excuse_unread_or_unrelated_material(tmp_path):
    with h.database(tmp_path/'db') as c:
        task,limit,_=linked_fixture(c)
        for path in [[],limit['discovery_path']*2]:
            bad=copy.deepcopy(limit);bad['discovery_path']=path
            with pytest.raises(ValueError):sl.validate(c,'report',task,bad)
        limit['pending_work']=['Available unread rule document']
        with pytest.raises(ValueError):sl.validate(c,'report',task,limit)
