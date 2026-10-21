import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-highlands/2026-10-20');review=run/'review/daly-astra';receipt=review/'ack.json';assert not receipt.exists()
p=json.loads((run/'draft/checkpoint-009.json').read_text());p['run_id']='flagler-daly-astra-20261020';p['payload']['contract']['created_at']=now();p['payload']['findings'].append(json.loads((review/'reviewed-person.json').read_text()))
for extra in (run/'review/reconciliation-astra').iterdir():
 if extra.is_file():p['artifacts'][hashlib.sha256(extra.read_bytes()).hexdigest()]=str(extra)
for f in review.iterdir():
 if f.is_file():p['artifacts'][hashlib.sha256(f.read_bytes()).hexdigest()]=str(f)
for f in p['payload']['findings']:
 for c in f['citations']:assert c['quote'] in Path(p['artifacts'][c['text_sha256']]).read_text()
path=run/'draft/checkpoint-010.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7987
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n')
s=json.loads((run/'state.json').read_text());s.update(database_save=ack,completed_people=s['completed_people']+['Christine Daly'],pending_people=[name for name in s['pending_people'] if name!='Christine Daly'],next_actions=['Review Donald Frenette next, then remaining named circuit officers one at a time; shared rules and county acceptance remain pending.','Reconcile officers, clerk, chief and shared rules before county acceptance.']);(run/'state.json').write_text(json.dumps(s,indent=2)+'\n');print(receipt.read_text())
