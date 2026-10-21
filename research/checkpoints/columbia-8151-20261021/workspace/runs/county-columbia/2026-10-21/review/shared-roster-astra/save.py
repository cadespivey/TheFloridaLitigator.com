import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-columbia/2026-10-21');review=run/'review/shared-roster-astra';receipt=review/'ack.json';assert not receipt.exists()
p=json.loads((run/'draft/checkpoint-007.json').read_text());p['run_id']='columbia-current-assignment-astra-20261021';p['payload']['contract']['created_at']=now();html_url='https://thirdcircuitfl.org/orders/gao-2026-020/';assignment_citation={'url': 'https://thirdcircuitfl.org/orders/gao-2026-020/', 'retrieved_at': '2026-10-21T11:27:33.502Z', 'http_status': 200, 'sha256': '6931bf91a1e3631773bec6d380c05b8ac870e56d3c5fef54641f50f47aeaa2f5', 'text_sha256': 'b5f722ce7a85083aeff52697f66163386bb42d281e267dc72649c8a2cb724f2c', 'authority': 'official', 'synthetic': False, 'quote': 'Disqualifications and recusals to Judge Koberlein, then Judge Feagle', 'locator': 'Columbia civil assignment table'}

for finding in p['payload']['findings']:
 if finding['key']=='columbia-melissa-olin':
  finding['facts']['assignment']+=' Separately, GAO2026-020 (July–December2026) assigns Olin felonyDivisionB L–Z and Hill DivisionA A–K; profile difference retained.'
  finding['facts']['conflicts'].append({'summary':'Profile felonyDivisionA versus current-period order DivisionB; both preserved.','sources':[finding['facts']['profile_url'],html_url]})
  finding['citations'].append(assignment_citation)
 if finding['key']=='columbia-mark-feagle':
  finding['facts']['assignment']+=' GAO2026-020 expressly lists Feagle as subsequent successor for Columbia civil recusals, not a routine half-docket judge.'
  finding['citations'].append(assignment_citation)

p['payload']['findings'].append(json.loads((review/'reviewed-person.json').read_text()))
for f in review.iterdir():
 if f.is_file():p['artifacts'][hashlib.sha256(f.read_bytes()).hexdigest()]=str(f)
for f in p['payload']['findings']:
 for c in f['citations']:assert c['quote'] in Path(p['artifacts'][c['text_sha256']]).read_text()
path=run/'draft/checkpoint-008.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8149
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n')
s=json.loads((run/'state.json').read_text());s.update(database_save=ack,pending_people=['Christina N. Seifert','Steven P. Johnson','Thomas J. Kennon'],next_actions=['Review Seifert, then Johnson, then Kennon individually; clerk, senior/shared rules and publication pending.']);(run/'state.json').write_text(json.dumps(s,indent=2)+'\n');print(receipt.read_text())
