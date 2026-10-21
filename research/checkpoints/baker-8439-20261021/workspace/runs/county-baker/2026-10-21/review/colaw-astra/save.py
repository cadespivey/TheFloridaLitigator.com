import json,hashlib,sqlite3,tempfile,sys
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
run=Path('runs/county-baker/2026-10-21');r=run/'review'/sys.argv[1];prev=int(sys.argv[2]);n=int(sys.argv[3]);receipt=r/'ack.json';assert not receipt.exists();p=json.loads((run/f'draft/checkpoint-{n-1:03}.json').read_text());f=json.loads((r/'reviewed-person.json').read_text());p['payload']['findings'].append(f);p['run_id']='baker-'+sys.argv[1]+'-20261021';p['payload']['contract']['created_at']=now();db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite');refs=set()
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('sha256','text_sha256'):refs.add(v)
   walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(f)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 for h in refs-set(p['artifacts']):
  data=c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0];assert hashlib.sha256(data).hexdigest()==h;(r/h).write_bytes(data)
for file in r.iterdir():
 if file.is_file():p['artifacts'][hashlib.sha256(file.read_bytes()).hexdigest()]=str(file)
path=run/f'draft/checkpoint-{n:03}.json';path.write_text(json.dumps(p,indent=2)+'\n')
with tempfile.TemporaryDirectory() as t:save_checkpoint(Path.cwd(),path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==prev
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(Path.cwd(),path,db);assert ack==save_checkpoint(Path.cwd(),path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f0 in p['payload']['findings']:assert json.loads(c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f0['key'])).fetchone()[0])==f0['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n');s=json.loads((run/'state.json').read_text());s['database_save']=ack;s['completed_people'].append(f['facts'].get('name',f['key']));s['pending_people']=[x for x in s['pending_people'] if x!=f['facts'].get('name')];s['next_actions']=['Next saved pending person; finish each before next. Shared roster/procedures,clerk and publication remain.'];(run/'state.json').write_text(json.dumps(s,indent=2)+'\n');print(ack)
