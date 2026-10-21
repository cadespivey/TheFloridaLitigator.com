import json,hashlib,sqlite3,tempfile,base64
from pathlib import Path
from flwu.history import now,sha
from flwu.baseline_capture import save_checkpoint
run=Path('runs/county-columbia/2026-10-21');r=run/'review/roster-astra';assert not (r/'ack.json').exists()
def result(name):return json.loads((r/name).read_text().split('### Result\n')[1].split('\n### Ran')[0])
docs=[result('roster-browser.txt'),*result('directory-county-browser.txt')];citations=[]
for name,d in zip(['roster','directory','county'],docs):
 b=base64.b64decode(d['original_base64']);t=d['text'];assert d['http_status']==200
 (r/(name+'.html')).write_bytes(b);(r/(name+'.txt')).write_text(t);(r/(name+'-links.json')).write_text(json.dumps(d['links'],indent=2)+'\n')
 m={k:d[k] for k in ['url','retrieved_at','http_status']};m.update(sha256=hashlib.sha256(b).hexdigest(),text_sha256=hashlib.sha256(t.encode()).hexdigest(),authority='official',synthetic=False);(r/(name+'.json')).write_text(json.dumps(m,indent=2)+'\n')
 quote='GARRETT HILL' if name=='directory' else 'Chief Judge Melissa G. Olin';assert quote in t;citations.append({**m,'quote':quote,'locator':'Columbia roster/directory grouping and navigation; individual review pending'})
scope=dict(profile='county-baseline-v1',county='columbia',circuit=3);stream='manual_research:county-baseline-v1:'+sha(scope)[:12];stamp=now()
names=['Melissa G. Olin','Frederick L. Koberlein Jr.','Sara J. Carter','Mark E. Feagle','Wesley R. Douglas','Garrett Hill']
f={'key':'columbia-initial-roster','kind':'source_review','facts':{'county':'columbia','circuit':3,'reviewed_by':'Astra','reviewed_at':stamp,'roster_candidates':[{'name':n,'role':'County Judge' if n in ['Sara J. Carter','Garrett Hill'] else 'Circuit Judge'} for n in names],'review_scope':'Initial official county-tag listing, county page and full directory. Four circuit and two county judge candidates; individual assignment verification remains pending.','conflicts':['County page and county-tag listing show five names, omitting Garrett Hill; full official directory expressly lists Hill under Columbia County Judge. Both originals retained; omission not interpreted as termination.'],'gaps':['Current assignment order, quasi-judicial officers and senior assignment screen pending.','Individual contact/procedure review, clerk, shared rules and publication pending.'],'next_action':'Chief Melissa G.Olin first; complete and save before next person.'},'citations':citations}
p={'scope':scope,'stream':stream,'run_id':'columbia-initial-roster-astra-20261021','payload':{'status':'incomplete','contract':{'mode':'manual_research','created_at':stamp,'execution':'Astra-only; no local workers','scope':scope,'stream':stream,'research_as_of':'2026-10-21','sequence':'Finish and save one person before next','priority':'Practical civil/commercial; noncivil basic operations'},'checks':[{'id':'county-roster-reconciliation','status':'incomplete'},{'id':'individual-reviews','status':'incomplete'}],'drafts':[],'findings':[f]},'artifacts':{}}
for file in r.iterdir():
 if file.is_file():p['artifacts'][hashlib.sha256(file.read_bytes()).hexdigest()]=str(file)
path=run/'draft/checkpoint-001.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as td:save_checkpoint(Path.cwd(),path,Path(td)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert not c.execute('select 1 from captures where stream=?',(stream,)).fetchall();before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(Path.cwd(),path,db);assert ack==save_checkpoint(Path.cwd(),path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 facts=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(facts[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=1,replay_verified=True,finalized_reports_unchanged=5);(r/'ack.json').write_text(json.dumps(ack,indent=2)+'\n');(run/'state.json').write_text(json.dumps(dict(scope=scope,stream=stream,database_save=ack,completed_people=[],pending_people=names,next_actions=['Olin first; one person at a time. Reconcile assignments/officers/seniors; clerk/shared operations/publication pending.']),indent=2)+'\n');print(ack)
