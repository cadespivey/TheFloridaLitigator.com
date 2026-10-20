"""Structural checkpoint tests: all evidence and databases here are disposable fixtures."""
import copy
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pytest
from flwu import baseline_capture as bc, history as h


@pytest.fixture
def packet(tmp_path, monkeypatch):
    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 10, 15, 20, tzinfo=timezone.utc)
    monkeypatch.setattr(bc, 'datetime', Clock)
    root = tmp_path / 'evidence'
    root.mkdir()
    raw, text = b'<p>Fixture division phone: 555-0100.</p>', b'Fixture division phone: 555-0100.'
    artifacts = {}
    for name, value in [('original.html', raw), ('extracted.txt', text)]:
        (root/name).write_bytes(value)
        artifacts[h.sha(value)] = name
    citation = dict(sha256=h.sha(raw), text_sha256=h.sha(text), quote='phone: 555-0100.',
                    locator='paragraph 1', url='https://www.17th.flcourts.org/fixture',
                    retrieved_at='2026-10-15T19:00:00+00:00', authority='official',
                    synthetic=False, http_status=200)
    scope = dict(profile='county-baseline-v1', county='broward', circuit=17)
    data = dict(stream='manual_research:county-baseline-v1:'+h.sha(scope)[:12], scope=scope,
                run_id='fixture-run', artifacts=artifacts,
                payload=dict(status='incomplete', contract={'mode':'manual_research'},
                    findings=[dict(key='fixture-judge', kind='judge', facts={'phone':'555-0100'}, citations=[citation])],
                    checks=[dict(id='reviewed', status='verified', checked_at='2026-10-15T19:00:00Z', hashes=list(artifacts)),
                            dict(id='remaining', status='incomplete')],
                    drafts=[{'kind':'review_receipt', 'receipt':{'fields':{'phone':{'citation':copy.deepcopy(citation)}}}}]))
    return root, tmp_path/'packet.json', tmp_path/'history.sqlite', data


def save(packet):
    root, path, db, data = packet
    path.write_text(json.dumps(data))
    return bc.save_checkpoint(root, path, db)


def rows(db):
    with sqlite3.connect(db) as conn:
        return {name:conn.execute('SELECT * FROM '+name+' ORDER BY rowid').fetchall()
                for name in ['streams','captures','artifacts','finding_versions','finding_observations','finalized_reports']}


def test_storage_replay_observations_and_versions(packet):
    root, path, db, data = packet
    first = save(packet)
    assert save(packet) == first
    before = rows(db)
    assert len(before['captures']) == len(before['finding_versions']) == 1
    assert {sha:raw for sha,raw in before['artifacts']} == {sha:(root/name).read_bytes() for sha,name in data['artifacts'].items()}
    # A changed retrieval observation survives even with the stable run ID.
    data['payload']['findings'][0]['citations'][0]['retrieved_at'] = '2026-10-15T19:30:00Z'
    second = save(packet)
    assert first['capture_id'] != second['capture_id']
    after = rows(db)
    assert len(after['captures']) == len(after['finding_observations']) == 2
    assert after['finding_versions'] == before['finding_versions']
    assert after['artifacts'] == before['artifacts']
    data['payload']['findings'][0]['facts']['phone'] = '555-0199'
    data['run_id'] = 'changed-facts'
    save(packet)
    after = rows(db)
    assert len(after['finding_versions']) == 2
    assert len(after['finding_observations']) == 3
    assert {json.loads(r[3])['phone'] for r in after['finding_versions']} == {'555-0100','555-0199'}
    assert after['finalized_reports'] == []
    assert first['status'] == 'incomplete' and first['finalized'] is False


@pytest.mark.parametrize('location', ['finding','nested_fact','nested_draft'])
@pytest.mark.parametrize('field,value', [
    ('quote','not in source'), ('locator',''), ('text_sha256','0'*64), ('sha256','0'*64),
    ('retrieved_at','2026-10-15T19:00:00'), ('retrieved_at','2026-10-15T20:00:01Z'),
    ('retrieved_at','not-a-date'), ('authority','third_party'), ('synthetic',True),
    ('synthetic',0), ('synthetic',None), ('http_status',404),
    ('url','http://localhost/'), ('resolved_url','http://127.0.0.1/private'),
])
def test_reject_invalid_citation_at_every_depth_before_db(packet, location, field, value):
    data=packet[3]
    cite=data['payload']['findings'][0]['citations'][0]
    if location=='nested_fact':
        cite=copy.deepcopy(cite);data['payload']['findings'][0]['facts']['nested']={'citation':cite}
    elif location=='nested_draft':
        cite=data['payload']['drafts'][0]['receipt']['fields']['phone']['citation']
    cite[field]=value
    with pytest.raises(bc.BaselineCaptureError):save(packet)
    assert not packet[2].exists()


@pytest.mark.parametrize('url', [
    'file:///tmp/evidence','http://[::1]/','http://10.0.0.1/', 'http://169.254.169.254/',
    'http://224.0.0.1/', 'http://2130706433/', 'http://127.1/', 'http://0x7f000001/',
    'http://host.local/', 'http://host.internal/', 'http://name.localhost/',
    'http://fixture.invalid/', 'https://user:SENSITIVE@example.com/',
    'https://example.com/?api_key=SENSITIVE','https://example.com/?accessToken=SENSITIVE',
    'https://example.com/?ACCESSTOKEN=SENSITIVE',
    'https://example.com:99999/', 'https://[invalid/',
])
def test_url_rejection_redacts_credentials(packet, url):
    packet[3]['payload']['findings'][0]['citations'][0]['url']=url
    with pytest.raises(bc.BaselineCaptureError) as error:save(packet)
    assert 'SENSITIVE' not in str(error.value)
    assert not packet[2].exists()


def test_artifact_checksum_mismatch(packet):
    (packet[0]/'original.html').write_bytes(b'changed')
    with pytest.raises(bc.BaselineCaptureError,match='mismatch'):save(packet)
    assert not packet[2].exists()


@pytest.mark.parametrize('kind',['absolute','parent','internal_link','external_link','parent_link'])
def test_artifact_path_rejections(packet,kind):
    root,path,db,data=packet
    raw_sha=next(iter(data['artifacts']))
    if kind=='absolute':replacement=str(root/'original.html')
    elif kind=='parent':replacement='../evidence/original.html'
    elif kind=='internal_link':
        (root/'link').symlink_to(root/'original.html');replacement='link'
    elif kind=='external_link':
        outside=root.parent/'outside';outside.write_bytes((root/'original.html').read_bytes())
        (root/'link').symlink_to(outside);replacement='link'
    else:
        (root/'dirlink').symlink_to(root,target_is_directory=True);replacement='dirlink/original.html'
    data['artifacts'][raw_sha]=replacement
    with pytest.raises(bc.BaselineCaptureError):save(packet)
    assert not db.exists()


@pytest.mark.parametrize('mutation', ['checked_future','checked_naive','verified_hash','no_open_check','scope','stream','mode','final_status','missing_marker','nested_empty','nested_hash','duplicate_finding','duplicate_check','extra_top'])
def test_packet_guards(packet,mutation):
    d=packet[3];p=d['payload']
    if mutation=='checked_future':p['checks'][0]['checked_at']='2026-10-15T20:00:01Z'
    elif mutation=='checked_naive':p['checks'][0]['checked_at']='2026-10-15T19:00:00'
    elif mutation=='verified_hash':p['checks'][0]['hashes']=['0'*64]
    elif mutation=='no_open_check':p['checks'].pop()
    elif mutation=='scope':d['scope']['circuit']=True
    elif mutation=='stream':d['stream']='legacy-stream'
    elif mutation=='mode':p['contract']['mode']='automatic'
    elif mutation=='final_status':p['status']='ready_for_review'
    elif mutation=='missing_marker':del p['findings'][0]['citations'][0]['synthetic']
    elif mutation=='nested_empty':p['drafts'].append({'nested':{'citation':{}}})
    elif mutation=='nested_hash':p['drafts'].append({'nested':{'sha256':'0'*64}})
    elif mutation=='duplicate_finding':p['findings'].append(copy.deepcopy(p['findings'][0]))
    elif mutation=='duplicate_check':p['checks'].append(copy.deepcopy(p['checks'][0]))
    elif mutation=='extra_top':d['unexpected']=True
    with pytest.raises(bc.BaselineCaptureError):save(packet)
    assert not packet[2].exists()


def test_inventory_failure_and_image_are_not_citations(packet):
    data=packet[3]
    data['payload']['drafts'].append({'kind':'acquisition_inventory','sources':{
        'failed':dict(sha256=next(iter(data['artifacts'])),http_status=404,url='https://example.org/missing'),
        'image':dict(sha256=next(iter(data['artifacts'])),http_status=200,url='https://example.org/seal.png')}})
    assert save(packet)['status']=='incomplete'


def test_invalid_packet_preserves_existing_database(packet):
    save(packet);before=rows(packet[2])
    packet[3]['payload']['drafts'][0]['receipt']['fields']['phone']['citation']['quote']='false quote'
    with pytest.raises(bc.BaselineCaptureError):save(packet)
    assert rows(packet[2])==before


def test_transaction_failure_rolls_back_existing_rows(packet):
    save(packet);before=rows(packet[2])
    with sqlite3.connect(packet[2]) as conn:
        conn.execute("CREATE TRIGGER fail_observation BEFORE INSERT ON finding_observations BEGIN SELECT RAISE(ABORT,'injected failure'); END")
    packet[3]['run_id']='new-run';packet[3]['payload']['findings'][0]['facts']['phone']='changed'
    with pytest.raises(sqlite3.IntegrityError,match='injected failure'):save(packet)
    assert rows(packet[2])==before


def test_existing_finalized_reports_and_unrelated_table_preserved(packet):
    root,path,db,data=packet
    with h.database(db) as conn:
        scope={'profile':'fixture-prior'};stream='synthetic_replay:fixture-prior'
        payload={'status':'ready_for_review','contract':{'mode':'synthetic_replay'},'checks':[{'id':'fixture','status':'verified','checked_at':'2026-01-01T00:00:00Z'}],'findings':[]}
        ack=h.record(conn,stream=stream,mode='synthetic_replay',scope=scope,run_id='fixture',payload=payload,artifacts={})
        report=root/'report.html';report.write_text('<p>Fixture report</p>')
        h.finalize(conn,ack['capture_id'],report,'Fixture review for persistence test')
        conn.execute('CREATE TABLE unrelated(value TEXT)');conn.execute("INSERT INTO unrelated VALUES('retain')");conn.commit()
    before=rows(db)
    save(packet)
    after=rows(db)
    assert after['finalized_reports']==before['finalized_reports']
    assert all(row in after['artifacts'] for row in before['artifacts'])
    assert all(row in after['captures'] for row in before['captures'])
    with sqlite3.connect(db) as conn:assert conn.execute('SELECT value FROM unrelated').fetchall()==[('retain',)]


def test_legacy_database_is_not_migrated(packet):
    with sqlite3.connect(packet[2]) as conn:conn.execute('CREATE TABLE legacy(value TEXT)')
    with pytest.raises(ValueError,match='legacy schema'):save(packet)
    with sqlite3.connect(packet[2]) as conn:
        assert conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()==[('legacy',)]


def test_explicit_synthetic_mode_separate_stream(packet):
    d=packet[3];d['payload']['contract']['mode']='synthetic_replay'
    d['stream']='synthetic_replay:county-baseline-v1:'+h.sha(d['scope'])[:12]
    for c in [d['payload']['findings'][0]['citations'][0],d['payload']['drafts'][0]['receipt']['fields']['phone']['citation']]:
        c['synthetic']=True;c['url']='https://fixture.invalid/document'
    assert save(packet)['mode']=='synthetic_replay'


def test_cli_ack_and_redacted_failure(packet,capsys):
    root,path,db,data=packet;path.write_text(json.dumps(data))
    args=['--root',str(root),'--packet',str(path),'--database',str(db)]
    assert bc.main(args)==0
    out=capsys.readouterr();assert json.loads(out.out)['finalized'] is False;assert out.err==''
    data['payload']['findings'][0]['citations'][0]['url']='https://user:SENSITIVE@example.com/'
    path.write_text(json.dumps(data));assert bc.main(args)==1
    out=capsys.readouterr();assert out.out=='' and 'SENSITIVE' not in out.err
    assert json.loads(out.err)['ok'] is False


def test_invalid_utf8_extraction_rejected_before_write(packet):
    root,path,db,data=packet
    bad=b'\xff\xfe';sha=h.sha(bad);(root/'bad.txt').write_bytes(bad);data['artifacts'][sha]='bad.txt'
    data['payload']['findings'][0]['citations'][0]['text_sha256']=sha
    with pytest.raises(bc.BaselineCaptureError,match='UTF-8'):save(packet)
    assert not db.exists()


def test_changed_source_bytes_preserve_stable_fact_version(packet):
    root,path,db,data=packet
    save(packet);before=rows(db)
    raw=b'<html><p>Fixture division phone: 555-0100.</p></html>'
    sha=h.sha(raw);(root/'refetched.html').write_bytes(raw);data['artifacts'][sha]='refetched.html'
    data['payload']['findings'][0]['citations'][0]['sha256']=sha
    save(packet);after=rows(db)
    assert len(after['captures'])==2 and len(after['finding_observations'])==2
    assert after['finding_versions']==before['finding_versions']
    assert len(after['artifacts'])==len(before['artifacts'])+1
    assert (sha,raw) in after['artifacts']


def browser_packet(packet):
    root, _, _, data = packet
    cite = data['payload']['findings'][0]['citations'][0]
    raw = b'<html><body>Division phone: 555-0100.</body></html>'
    (root/'browser.html').write_bytes(raw)
    data['artifacts'][h.sha(raw)] = 'browser.html'
    cite['sha256'] = h.sha(raw)
    cite['http_status'] = None
    receipt = dict(method='native_browser_save_page_source', content_reviewed=True,
                   page_url=cite['url'], original_sha256=cite['sha256'],
                   observed_at=cite['retrieved_at'], page_title='Official directory',
                   review_note='Rendered contact row matched saved source.')
    return cite, receipt


def attach_browser_receipt(packet, cite, receipt):
    raw = json.dumps(receipt).encode()
    (packet[0]/'browser-observation.json').write_bytes(raw)
    packet[3]['artifacts'][h.sha(raw)] = 'browser-observation.json'
    cite['browser_capture'] = {'observation_sha256': h.sha(raw)}


def test_browser_saved_source_preserves_unknown_status_and_replays(packet):
    cite, receipt = browser_packet(packet)
    attach_browser_receipt(packet, cite, receipt)
    result = save(packet)
    assert save(packet) == result
    assert cite['http_status'] is None
    assert rows(packet[2])['finalized_reports'] == []
    assert dict(rows(packet[2])['artifacts'])[cite['sha256']] == (packet[0]/'browser.html').read_bytes()


@pytest.mark.parametrize('field,value', [
    ('method', 'http_failure'), ('content_reviewed', False),
    ('page_url', 'https://www.17th.flcourts.org/other'),
    ('original_sha256', '0'*64), ('observed_at', '2026-10-15T18:00:00Z'),
    ('page_title', ''), ('review_note', ''),
])
def test_browser_receipt_mismatch_rejected_before_database(packet, field, value):
    cite, receipt = browser_packet(packet)
    receipt[field] = value
    attach_browser_receipt(packet, cite, receipt)
    with pytest.raises(bc.BaselineCaptureError):
        save(packet)
    assert not packet[2].exists()


@pytest.mark.parametrize('fault', ['missing_receipt', 'known_403', 'non_html'])
def test_browser_capture_cannot_override_failure_or_missing_original(packet, fault):
    cite, receipt = browser_packet(packet)
    if fault == 'non_html':
        raw = b'Access denied'
        (packet[0]/'denied.txt').write_bytes(raw)
        packet[3]['artifacts'][h.sha(raw)] = 'denied.txt'
        cite['sha256'] = receipt['original_sha256'] = h.sha(raw)
    attach_browser_receipt(packet, cite, receipt)
    if fault == 'known_403':
        cite['http_status'] = 403
    if fault == 'missing_receipt':
        cite['browser_capture']['observation_sha256'] = '0'*64
    with pytest.raises(bc.BaselineCaptureError):
        save(packet)
    assert not packet[2].exists()

@pytest.mark.parametrize('fault', [None, 'html', 'broken_pdf', 'known_403', 'wrong_hash'])
def test_browser_saved_pdf_requires_readable_original_and_matching_receipt(packet, fault):
    from io import BytesIO
    from pypdf import PdfWriter
    cite, receipt = browser_packet(packet)
    stream = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.write(stream)
    raw = stream.getvalue()
    if fault == 'html':
        raw = b'<html>Access denied</html>'
    elif fault == 'broken_pdf':
        raw = b'%PDF-1.7\nnot a PDF'
    (packet[0]/'browser.pdf').write_bytes(raw)
    packet[3]['artifacts'][h.sha(raw)] = 'browser.pdf'
    cite['sha256'] = receipt['original_sha256'] = h.sha(raw)
    receipt['method'] = 'native_browser_save_pdf'
    if fault == 'known_403':
        cite['http_status'] = 403
    elif fault == 'wrong_hash':
        receipt['original_sha256'] = '0'*64
    attach_browser_receipt(packet, cite, receipt)
    if fault:
        with pytest.raises(bc.BaselineCaptureError):
            save(packet)
        assert not packet[2].exists()
    else:
        result = save(packet)
        assert save(packet) == result
        assert dict(rows(packet[2])['artifacts'])[cite['sha256']] == raw
        assert rows(packet[2])['finalized_reports'] == []
