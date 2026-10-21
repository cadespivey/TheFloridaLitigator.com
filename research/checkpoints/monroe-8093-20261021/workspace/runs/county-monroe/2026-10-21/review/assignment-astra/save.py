import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.history import now
from flwu.baseline_capture import save_checkpoint
root=Path.cwd();run=Path('runs/county-monroe/2026-10-21');r=run/'review/assignment-astra';assert not (r/'ack.json').exists()
c=json.loads((r/'circuit.json').read_text());c.update(quote='Civil Division',locator='Pages1,4–5 civil/probate assignment and effective period; criminal/family names screened only')
k=json.loads((r/'county.json').read_text());k.update(quote='All new and pending small claims cases',locator='Pages1–3 county assignments and dates; ExhibitA individual cases not reviewed')
i=json.loads((r/'index.json').read_text());i.update(quote='Administrative Orders',locator='Official order index, assignment and shared civil/access titles')
(r/'visual-dates.txt').write_text('Astra visual review of rendered signature pages: circuit2.004/26-3 signed July28,2026; stated assignment period July1–December31,2026 or further order. County2.005/25-2 signed October15,2025; effective October20,2025. Automated extraction of handwritten dates unreliable; original PDFs and renders preserved.\n')
f={'key':'monroe-shared-assignments','kind':'procedure','facts':{'county':'monroe','circuit':16,'reviewed_by':'Astra','reviewed_at':now(),'review_status':'reviewed_with_gaps','title':'Dated circuit and county assignment statements','circuit_civil':'Lower Keys four-fifths Koenig/one-fifth Jones; Middle Keys Jones; Upper Keys Morgan. Order says allocations by filing courthouse, subject to incidental assignments.','county_civil':'Lower Keys small claims and county civil Kelley except new landlord/tenant actions split equally Wilson/Kelley; Middle Keys Lewis; Upper Keys Hamilton. Order disclaims conferring venue/jurisdiction rights.','probate_guardianship':'Lower Keys probate Koenig, mental-health/guardianship Helms; Middle Keys new cases Helms; Upper Keys split Koenig/Helms.','stated_dates':{'circuit_signed':'2026-07-28','circuit_period_start':'2026-07-01','circuit_period_end':'2026-12-31','county_signed':'2025-10-15','county_effective':'2025-10-20'},'review_scope':{'collected':'Official order index, circuit5page and county4page original PDFs, extracted text, page renders.','content_reviewed':'Civil/personnel assignments, official headquarters and effective-date/reassignment qualifications; noncivil headings screened for roster only.','not_reviewed':'Criminal case-specific ExhibitA, specialized family/criminal allocation mechanics.'},'conflicts':['Orders supply different/specific assignments compared with some undated profile descriptions; both retained without deciding authority.'],'gaps':['Senior applicability and practical shared filing/access rules still pending.']},'citations':[i,c,k]}
(r/'reviewed-finding.json').write_text(json.dumps(f,indent=2)+'\n')
p=json.loads((run/'draft/checkpoint-011.json').read_text());p['run_id']='monroe-shared-assignments-astra-20261021';p['payload']['contract']['created_at']=now();p['payload']['findings'].append(f)
assignments={
'monroe-timothy-koenig':('Lower Keys four-fifths circuit civil; Lower Keys probate; half Upper Keys probate/guardianship/mental health.',c),
'monroe-mark-jones':('Lower Keys one-fifth circuit civil and all Middle Keys circuit civil.',c),
'monroe-james-morgan':('Upper Keys circuit civil; official headquarters Plantation Key.',c),
'monroe-bonnie-helms':('Lower Keys mental health/guardianship; Middle Keys new probate/guardianship cases; half Upper Keys probate/guardianship/mental health.',c),
'monroe-derek-lewis':('Middle Keys county cases, including county civil and small claims; headquarters Marathon.',k),
'monroe-sharon-hamilton':('All Upper Keys county cases; headquarters Plantation Key.',k),
'monroe-albert-kelley':('Lower Keys county civil/small claims, except new landlord/tenant actions split equally with Wilson; headquarters Key West.',k),
'monroe-mark-wilson':('Half of new Lower Keys landlord/tenant actions; headquarters Key West. Civil allocation supplements primarily criminal profile.',k)}
for f in p['payload']['findings']:
 if f['key'] in assignments:
  summary,cite=assignments[f['key']];f['facts']['assignment_order_statement']={'summary':summary,'url':cite['url'],'retrieved_at':cite['retrieved_at'],'stated_effective_period':'July1–December31,2026 or further order' if cite==c else 'Effective October20,2025, subject to incidental reassignment','note':'Additional dated source statement; prior profile preserved, no authority resolution.'};f['citations'].append(cite)
for file in r.iterdir():
 if file.is_file():p['artifacts'][hashlib.sha256(file.read_bytes()).hexdigest()]=str(file)
for f in p['payload']['findings']:
 for cite in f['citations']:assert cite['quote'] in Path(p['artifacts'][cite['text_sha256']]).read_text()
path=run/'draft/checkpoint-012.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
 assert conn.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8091
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
