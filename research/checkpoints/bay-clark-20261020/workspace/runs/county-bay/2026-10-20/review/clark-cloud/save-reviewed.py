"""Append Clark's bounded review once. Do not rerun after acknowledgement."""
import hashlib,json,sqlite3,tempfile,copy
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd(); run=Path('runs/county-bay/2026-10-20'); review=run/'review/clark-cloud'; local=run/'review/clark-local'
receipt=review/'checkpoint-ack.json'; assert not receipt.exists()
db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
packet=copy.deepcopy(json.loads((run/'draft/checkpoint-001.json').read_text()))
person=json.loads((review/'reviewed-person.json').read_text())
meta=json.loads((local/'admin-order-2025-00-01-meta.json').read_text())
ao=json.loads((review/'ao-visual-review.json').read_text())
excerpt=review/'ao-reviewed-transcription-excerpts.txt'
cite={k:meta[k] for k in ('url','http_status','retrieved_at','sha256')}
cite.update(resolved_url=meta['final_url'],text_sha256=hashlib.sha256(excerpt.read_bytes()).hexdigest(),quote='The case management procedures set forth in this Order must be followed in all civil actions unless the action falls within an exception set forth in Rule 1.200(a).',locator='Page 1 paragraph 1; explicitly labeled manual visual transcription, not full extraction',authority='official',synthetic=False)
assert cite['quote'] in excerpt.read_text()
shared=dict(ao,county='bay',circuit=14,status='bounded_shared_source_review',title='Shared circuit civil case-management order',summary='The order states Rule 1.200(a) exceptions and preserves pre-January 1, 2025 case-management orders. Paragraph 3 requires service of the appropriate standing order with initial process and pleadings, subject to paragraph 1 scope. Its stated effective date precedes its signing date; both are retained without deciding legal effect.',individual_attribution='No Goodman-named form is attributed to Clark. Attachments are collected, not reviewed.')
packet['payload']['findings'] += [dict(key='bay-judge-brantley-s-clark-jr',kind='person',facts=person['facts'],citations=person['citations']),dict(key='bay-shared-civil-case-management-2025-00-01',kind='source_review',facts=shared,citations=[cite])]
packet['run_id']='bay-clark-reviewed-20261020'; packet['payload']['contract']['created_at']=now()
for folder in (local,review):
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix in {'.json','.html','.txt','.pdf','.png','.py'}:
            packet['artifacts'][hashlib.sha256(path.read_bytes()).hexdigest()]=str(path)
for finding in packet['payload']['findings']:
    for citation in finding['citations']:
        original=Path(packet['artifacts'][citation['sha256']]); text=Path(packet['artifacts'][citation['text_sha256']])
        assert hashlib.sha256(original.read_bytes()).hexdigest()==citation['sha256']
        assert citation['quote'] in text.read_text()
path=run/'draft/checkpoint-002.json'; path.write_text(json.dumps(packet,indent=2)+'\n')
with tempfile.TemporaryDirectory() as tmp: save_checkpoint(root,path,Path(tmp)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
    assert conn.execute('select max(seq) from captures where stream=?',(packet['stream'],)).fetchone()[0]==7713
    before=conn.execute('select * from finalized_reports order by seq').fetchall(); assert len(before)==5
ack=save_checkpoint(root,path,db)
assert save_checkpoint(root,path,db)==ack
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
    assert before==conn.execute('select * from finalized_reports order by seq').fetchall()
    assert json.loads(conn.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==packet['payload']
    for h,p in packet['artifacts'].items(): assert conn.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(p).read_bytes()
    for f in packet['payload']['findings']:
        row=conn.execute('select v.facts from finding_versions v join finding_observations o using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone()
        assert json.loads(row[0])==f['facts']
receipt.write_text(json.dumps(dict(ack,artifacts_readback=len(packet['artifacts']),findings_readback=len(packet['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5),indent=2)+'\n')
print(receipt.read_text())
