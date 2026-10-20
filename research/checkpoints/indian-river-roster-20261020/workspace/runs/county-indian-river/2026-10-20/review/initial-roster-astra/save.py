import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import sha,now
root=Path.cwd();run=Path('runs/county-indian-river/2026-10-20');review=run/'review/initial-roster-astra';receipt=review/'ack.json';assert not receipt.exists()
scope=dict(profile='county-baseline-v1',county='indian_river',circuit=19);stream='manual_research:county-baseline-v1:'+sha(scope)[:12];stamp=now();cite=json.loads((review/'source-citation.json').read_text());links=[x['url'] for x in json.loads((review/'roster-links.json').read_text()) if x['text']=='Judge Page'];names=['Cynthia L. Cox','Victoria L. Griffin','Anastasia M. Norman','Rebecca White','Nicole Menz','Robyn E. Stone','Kathryn Hill','Adrienne Fleming','Vacant hearing-officer position','Kameisha Presley'];assert len(links)==10
facts=dict(county='indian_river',circuit=19,title='Initial Indian River filtered official roster',reviewed_at=stamp,review_scope='Roster identity and profile-link inventory only; individual contacts/procedures not yet reviewed for this county.',candidates=[dict(name=name,profile_url=url,role=('Circuit Judge' if i<4 else 'County Judge' if i<6 else 'Magistrate' if i<8 else 'Child Support Enforcement Hearing Officer'),status='vacant' if i==8 else 'named') for i,(name,url) in enumerate(zip(names,links))],counts=dict(active_judges=6,named_other_officers=3,vacant_positions=1),reuse_leads=dict(prior_county='st_lucie',capture=7337,workspace='/Users/cadespivey/florida-litigator-weekly-update/runs/county-st-lucie/2026-10-19',scope='Inspect saved shared circuit rules and Fleming/Presley/vacancy evidence for applicability before recollection; not yet accepted for Indian River.'),gaps=['Clerk, chief/senior applicability and county assignment reconciliation remain to review.','Direct HTTP returned403; actual browser response200 retained.'],next_person='Cynthia L. Cox')
packet=dict(scope=scope,stream=stream,run_id='indian-river-initial-roster-astra-20261020',payload=dict(status='incomplete',contract=dict(mode='manual_research',created_at=stamp,execution='Astra-only; no local workers',scope=scope,stream=stream,research_as_of='2026-10-20',sequence='Finish one person and save before next',priority='Practical civil/commercial; noncivil basic operations'),checks=[dict(id='county-roster-reconciliation',status='incomplete'),dict(id='individual-reviews',status='incomplete')],drafts=[],findings=[dict(key='indian-river-initial-roster',kind='source_review',facts=facts,citations=[cite])]),artifacts={})
for p in sorted(review.iterdir()):
 if p.is_file():packet['artifacts'][hashlib.sha256(p.read_bytes()).hexdigest()]=str(p)
path=run/'draft/checkpoint-001.json';path.write_text(json.dumps(packet,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select count(*) from captures where stream=?',(stream,)).fetchone()[0]==0
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==packet['payload']
 for h,p in packet['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(p).read_bytes()
 row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],'indian-river-initial-roster')).fetchone();assert json.loads(row[0])==facts
ack.update(artifacts_readback=len(packet['artifacts']),findings_readback=1,replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n')
(run/'state.json').write_text(json.dumps(dict(county='indian_river',circuit=19,database_save=ack,execution='Astra-only',active_worker=None,completed_people=[],pending_people=names,next_actions=['Review Cynthia L. Cox contacts and bounded applicable procedures, then save before next person.','Reuse St. Lucie circuit evidence after checking applicability; reconcile clerk/chief/senior coverage.']),indent=2)+'\n');print(receipt.read_text())
