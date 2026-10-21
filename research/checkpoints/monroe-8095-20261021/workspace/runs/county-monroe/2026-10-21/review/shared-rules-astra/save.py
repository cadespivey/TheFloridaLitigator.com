import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.history import now
from flwu.baseline_capture import save_checkpoint
root=Path.cwd();run=Path('runs/county-monroe/2026-10-21');r=run/'review/shared-rules-astra';assert not (r/'ack.json').exists()
f=json.loads((r/'reviewed-finding.json').read_text())
p=json.loads((run/'draft/checkpoint-012.json').read_text());p['run_id']='monroe-shared-civil-rules-astra-20261021';p['payload']['contract']['created_at']=now();p['payload']['findings'].append(f)
for file in r.iterdir():
 if file.is_file():p['artifacts'][hashlib.sha256(file.read_bytes()).hexdigest()]=str(file)
for f in p['payload']['findings']:
 for cite in f['citations']:assert cite['quote'] in Path(p['artifacts'][cite['text_sha256']]).read_text()
path=run/'draft/checkpoint-013.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
 assert conn.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8093
 before=conn.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
 assert before==conn.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(conn.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert conn.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f in p['payload']['findings']:
  row=conn.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);(r/'ack.json').write_text(json.dumps(ack,indent=2)+'\n')
s=json.loads((run/'state.json').read_text());s.update(database_save=ack,next_actions=['Complete bounded senior applicability and shared civil filing/access rules, Tax Assessor link.','Reconcile and publish county supplement; preserve historical reports.']);(run/'state.json').write_text(json.dumps(s,indent=2)+'\n');print(ack)
