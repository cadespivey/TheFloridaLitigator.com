import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-martin/2026-10-20');review=run/'review/steele-astra';receipt=review/'ack.json';assert not receipt.exists()
p=json.loads((run/'draft/checkpoint-007.json').read_text());p['run_id']='martin-steele-astra-20261020';p['payload']['contract']['created_at']=now();p['payload']['findings'].append(json.loads((review/'reviewed-person.json').read_text()))
for prior in p['payload']['findings']:
 if prior['key']=='martin-steven-levin':prior['facts']['stated_dates']={'profile_revision':None,'civil_guide_effective':'2025-12-10','basis':'Guide page1 expressly says Effective December10,2025; date is not inferred from filename.'}

for f in review.iterdir():
 if f.is_file():p['artifacts'][hashlib.sha256(f.read_bytes()).hexdigest()]=str(f)
for f in p['payload']['findings']:
 for c in f['citations']:assert c['quote'] in Path(p['artifacts'][c['text_sha256']]).read_text()
path=run/'draft/checkpoint-008.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7871
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n')
s=json.loads((run/'state.json').read_text());s.update(database_save=ack,completed_people=s['completed_people']+['Darren Steele'],pending_people=[name for name in s['pending_people'] if name!='Darren Steele'],next_actions=['Review Jennifer Alcorta Waters next; retain successor leads for county reconciliation.','Reconcile Roby/Roberts vacancy leads and remaining county personnel/shared rules before acceptance.']);(run/'state.json').write_text(json.dumps(s,indent=2)+'\n');print(receipt.read_text())
