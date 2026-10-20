import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.county_review import references
R=Path('runs/county-santa-rosa/2026-10-19');D=R/'review/warrick';s=json.loads((R/'state.json').read_text());assert s['database_save']['seq']==7689
p=json.loads((R/'draft/checkpoint-008.json').read_text());f=json.loads((D/'findings.json').read_text());p['payload']['findings'].extend(f);p['run_id']='santa-rosa-warrick-20261019'
for c in references([f,*[json.loads(x.read_text()) for x in D.glob('*-acquisition.json')]]):
 for h,k in [('sha256','path'),('text_sha256','text_path')]:p['artifacts'][c[h]]=c[k]
for file in [*D.glob('*.py'),*D.glob('*.json'),*D.glob('*.xml'),*D.glob('*.png')]:
 b=file.read_bytes();h=hashlib.sha256(b).hexdigest();dest=R/'raw'/(h+file.suffix);dest.write_bytes(b);p['artifacts'][h]=str(dest)
path=R/'draft/checkpoint-009.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path(s['database_save']['database'])
with tempfile.TemporaryDirectory() as t:save_checkpoint(Path.cwd(),path,Path(t)/'trial.sqlite')
with sqlite3.connect(db) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7689;before=c.execute('select * from finalized_reports order by seq').fetchall()
r=save_checkpoint(Path.cwd(),path,db);assert r==save_checkpoint(Path.cwd(),path,db)
with sqlite3.connect(db) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for finding in p['payload']['findings']:
  row=c.execute('select v.facts from finding_versions v join finding_observations o using(version_id) where o.capture_seq=? and o.entity_key=?',(r['seq'],finding['key'])).fetchone();assert json.loads(row[0])==finding['facts']
assert s['pending_people'][0]=='Steven Warrick';s['pending_people'].pop(0);s['completed_people'].append('Steven Warrick')
s.update(database_save=r,next_actions=['Next officer/senior roster and clerk/shared reconciliation; complete one person before the next.','Later officers, assignment/senior, clerk/shared source reconciliation and county validation.']);(R/'state.json').write_text(json.dumps(s,indent=2)+'\n');v=dict(result=r,artifacts_readback=len(p['artifacts']),facts_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=len(before),record_validation='Warrick contacts and brief office procedures reviewed; county incomplete');(D/'validation.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v,indent=2))
