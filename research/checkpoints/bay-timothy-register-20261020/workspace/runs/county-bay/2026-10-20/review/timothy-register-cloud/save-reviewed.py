"""One-time Timothy Register append; never rerun after acknowledgement."""
import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd(); run=Path('runs/county-bay/2026-10-20'); review=run/'review/timothy-register-cloud'; receipt=review/'checkpoint-ack.json'; assert not receipt.exists()
db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
packet=json.loads((run/'draft/checkpoint-009.json').read_text()); person=json.loads((review/'reviewed-person.json').read_text())
finding=dict(key='bay-judge-timothy-register',kind='person',facts=person['facts'],citations=person['citations']); packet['payload']['findings'].append(finding); packet['run_id']='bay-timothy-register-reviewed-20261020'; packet['payload']['contract']['created_at']=now()
for folder in [review,run/'review/timothy-register-local']:
 for p in folder.rglob("*"):
  if p.is_file() and p.suffix in {'.json','.html','.pdf','.png','.txt','.py','.md'}: packet['artifacts'][hashlib.sha256(p.read_bytes()).hexdigest()]=str(p)
for f in packet['payload']['findings']:
 for c in f['citations']:
  assert c['quote'] in Path(packet['artifacts'][c['text_sha256']]).read_text()
path=run/'draft/checkpoint-010.json'; path.write_text(json.dumps(packet,indent=2)+'\n')
with tempfile.TemporaryDirectory() as tmp: save_checkpoint(root,path,Path(tmp)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
 assert conn.execute('select max(seq) from captures where stream=?',(packet['stream'],)).fetchone()[0]==7729
 before=conn.execute('select * from finalized_reports order by seq').fetchall(); assert len(before)==5
ack=save_checkpoint(root,path,db); assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
 assert before==conn.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(conn.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==packet['payload']
 for h,p in packet['artifacts'].items(): assert conn.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(p).read_bytes()
 for f in packet['payload']['findings']:
  row=conn.execute('select v.facts from finding_versions v join finding_observations o using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone(); assert json.loads(row[0])==f['facts']
receipt.write_text(json.dumps(dict(ack,artifacts_readback=len(packet['artifacts']),findings_readback=len(packet['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5),indent=2)+'\n'); print(receipt.read_text())
