import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import sha,now
root=Path.cwd();run=Path('runs/county-martin/2026-10-20');review=run/'review/initial-roster-astra';receipt=review/'ack.json';assert not receipt.exists()
scope=dict(profile='county-baseline-v1',county='martin',circuit=19);stream='manual_research:county-baseline-v1:'+sha(scope)[:12];stamp=now();cite=json.loads((review/'source-citation.json').read_text())
candidates=json.loads((review/'candidates.json').read_text());names=[x['name'] for x in candidates]
facts=dict(county='martin',circuit=19,title='Initial Martin official judiciary roster',reviewed_at=stamp,review_scope='Twelve filtered roster candidate identities and profile links only; not completed individual reviews or a verified current roster.',candidates=candidates,counts=dict(roster_cards=12,judge_cards=8,magistrate_cards=2,hearing_office_cards=2),reuse_leads=dict(prior_county='indian-river',capture=7821,scope='Fleming, Presley, vacant hearing office, chief and shared circuit rules may be reused after applicability/field verification.'),gaps=['June2026 Florida Bar JNC search lead identifies Roby retirement and Roberts resignation vacancies; current roster still lists them. Verify appointments/current service before acceptance, without deciding conflicting sources.','Chief/senior/clerk and traffic officer applicability require bounded reconciliation.'],next_person='Sherwood Bauer, Jr.')

packet=dict(scope=scope,stream=stream,run_id='martin-initial-roster-astra-20261020',payload=dict(status='incomplete',contract=dict(mode='manual_research',created_at=stamp,execution='Astra-only; no local workers',scope=scope,stream=stream,research_as_of='2026-10-20',sequence='Finish one person and save before next',priority='Practical civil/commercial; noncivil basic operations'),checks=[dict(id='county-roster-reconciliation',status='incomplete'),dict(id='individual-reviews',status='incomplete')],drafts=[],findings=[dict(key='martin-initial-roster',kind='source_review',facts=facts,citations=[cite])]),artifacts={})
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
 row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],'martin-initial-roster')).fetchone();assert json.loads(row[0])==facts
ack.update(artifacts_readback=len(packet['artifacts']),findings_readback=1,replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n')
(run/'state.json').write_text(json.dumps(dict(county='martin',circuit=19,database_save=ack,execution='Astra-only',active_worker=None,completed_people=[],pending_people=names,next_actions=['Review Sherwood Bauer contacts and bounded applicable procedures, then save before next person.','Reuse Nineteenth Circuit evidence after checking applicability; reconcile clerk/chief/senior coverage.']),indent=2)+'\n');print(receipt.read_text())
