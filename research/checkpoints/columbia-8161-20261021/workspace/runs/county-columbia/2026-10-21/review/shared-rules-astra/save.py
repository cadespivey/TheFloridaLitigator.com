import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-columbia/2026-10-21');review=run/'review/shared-rules-astra';receipt=review/'ack.json';assert not receipt.exists()
p=json.loads((run/'draft/checkpoint-012.json').read_text());p['run_id']='columbia-shared-rules-astra-20261021';p['payload']['contract']['created_at']=now();civil_citation={'url': 'https://thirdcircuitfl.org/civil-law/', 'retrieved_at': '2026-10-21T11:33:30.522Z', 'http_status': 200, 'sha256': '70213a13a097da4c99214c9e91c4217db979e60088e4fdb25c0847249f018a04', 'text_sha256': '968c60099ab2eb904e2c4be38862731c24fbeb095a8f258386b601ed8e39b948', 'authority': 'official', 'synthetic': False, 'quote': 'Megan Gutshall', 'locator': 'Columbia/Hamilton civil case manager contact block'}

for finding in p['payload']['findings']:
 if finding['key']=='columbia-christina-seifert':
  finding['facts']['contact'].update(civil_case_manager_name='Megan Gutshall',civil_case_manager_phone='386-719-7577',civil_case_manager_email='gutshall.megan@jud3.flcourts.org',civil_case_manager_address=['4424 NW American Lane, Suite 102','Lake City, FL 32055'])
  finding['facts']['contact']['contact_note']+=' Columbia foreclosure coordination: civil case manager Megan Gutshall, not judicial assistant.'
  finding['citations'].append(civil_citation)

p['payload']['findings'].append(json.loads((review/'reviewed-person.json').read_text()))
for f in review.iterdir():
 if f.is_file():p['artifacts'][hashlib.sha256(f.read_bytes()).hexdigest()]=str(f)
for f in p['payload']['findings']:
 for c in f['citations']:assert c['quote'] in Path(p['artifacts'][c['text_sha256']]).read_text()
path=run/'draft/checkpoint-013.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8159
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n')
s=json.loads((run/'state.json').read_text());s.update(database_save=ack,next_actions=['Pinned export, directory projection/contact audit, acceptance and publication.']);(run/'state.json').write_text(json.dumps(s,indent=2)+'\n');print(receipt.read_text())
