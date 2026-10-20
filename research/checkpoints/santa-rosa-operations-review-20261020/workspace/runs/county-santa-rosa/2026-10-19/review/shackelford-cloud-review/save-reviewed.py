"""One-time reviewed append; do not rerun after successful acknowledgement."""
import copy, hashlib, json, sqlite3, tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd(); run=Path('runs/county-santa-rosa/2026-10-19'); review=run/'review/shackelford-cloud-review'; worker=run/'review/shackelford-repair'
assert not (review/'checkpoint-ack.json').exists()
state=json.loads((run/'state.json').read_text()); db=Path(state['database_save']['database'])
assert state['database_save']['seq']==7701
p=copy.deepcopy(json.loads((run/'draft/checkpoint-014.json').read_text()))
p['run_id']='santa-rosa-shackelford-reviewed-20261020';p['payload']['contract']['created_at']=now();p['payload']['contract']['execution']='Qwen3.8 bounded collection followed by cloud evidence review and corrected persistence'
for check in p['payload']['checks']:
 if check['id']=='senior-contact-review':check.update(status='verified', checked_at=now(), hashes=[hashlib.sha256((review/'item_45-tool-evidence.json').read_bytes()).hexdigest()], scope='Bounded search reviewed with explicit missing-contact gaps; not verification of contact availability')
# Preserve original worker outputs, including statements rejected by review.
for path in sorted(worker.iterdir()):
 if path.is_file() and path.name not in {'worker-events.jsonl','worker-errors.log'}:
  p['artifacts'][hashlib.sha256(path.read_bytes()).hexdigest()]=str(path)
for path in sorted(review.glob('*')):
 if path.is_file():p['artifacts'][hashlib.sha256(path.read_bytes()).hexdigest()]=str(path)
# Verify worker hashes against actual evidence bytes.
for name,meta in json.loads((worker/'manifests.json').read_text()).items():
 b=(worker/name).read_bytes();assert len(b)==meta['byte_length'];assert hashlib.sha256(b).hexdigest()==meta['sha256']
scope=p['payload']['findings'][0]
ao=copy.deepcopy(scope['citations'][1])
ao['quote']='Judge Jan Shackelford';ao['locator']='PDF page 1, ORDERED paragraph and issuance date'
fields={k:{'value':None,'status':'not_found_in_bounded_search','note':'Three official-domain searches, rendered judges roster and old profile URL reviewed; no personal value located. This is not proof that the court publishes no such information.'} for k in ['chambers_phone','chambers_email','chambers_address','assistant_name','assistant_phone','assistant_email','fax']}
facts={'task_id':'person-santa-rosa-jan-shackelford','judge_key':'santa-rosa-jan-shackelford','entity_type':'judge','name':'Jan Shackelford','role':'Senior Judge','county':'santa_rosa','circuit':1,'status':'complete_with_documented_gaps','reviewed_at':now(),'assignment':'AO2026-28 assigns service in the courts of the First Judicial Circuit from August 17 through December 31, 2026. Issued August 18, 2026. Circuit-wide scope includes Santa Rosa; no individual county case assignment or subject-matter division is inferred.','profile_url':None,'procedure_url':None,'fields':fields,'procedures':{'status':'not_found_in_bounded_search','summary':'No judge-specific operating procedures located in the bounded review. No other judge’s requirements substituted.'},'review_scope':'Existing assignment order plus three official-domain searches, rendered current roster and HTTP404 old profile check. Contacts, assignment and practical procedure discovery only.','source_review':{'old_profile_url':'https://www.firstjudicialcircuit.org/legal-professionals/judges/jan-shackelford/','old_profile_http_status':404,'browser_snapshot_at':'2026-10-20T16:06:25.430Z','timestamp_basis':'Timestamp of browser snapshot path in item_48, not an independently recorded HTTP response retrieval timestamp.','roster_observation':'Jan Shackelford was not listed in the preserved rendered roster snapshot. No general court policy about senior listings is inferred.','evidence_manifest':str(review/'evidence-manifest.json'),'retrieval_limitations':'Worker supplied timestamps for search summaries and browser notes are not independently established. Preserve terminal event evidence and original response metadata separately.','worker_corrections':['Replaced universal absence statements with bounded not-found findings.','Removed unsupported general senior-listing policy inference.','Omitted unverified general procedure links.','Retained original worker drafts as unaccepted evidence, superseded by these reviewed facts.']},'limitations':['Personal contacts, assistant and judge-specific procedures remain unlocated.','Circuit-wide service is not proof of a current individual Santa Rosa case assignment.']}
p['payload']['findings'].append({'key':'santa-rosa-jan-shackelford','kind':'judge','facts':facts,'citations':[ao]})
scope['facts']['senior_judges']='Jan Shackelford: circuit-wide assignment AO2026-28 reviewed; bounded personal contact/procedure search completed with explicit not-found gaps. No individual Santa Rosa case assignment inferred.'
scope['facts']['limitations']='Eight is the active roster count. Senior Jan Shackelford retained separately with documented contact/procedure gaps. Historical Michelle Inere lead and shared operations review remain pending.'
scope['facts']['review_correction']='Supersedes the pending senior personal review statement at7701; county acceptance remains reopened.'
accept=p['payload']['findings'][3]['facts'];accept['next_action']='Bounded current-status screening of historical Michelle Inere lead, then shared-access/clerk operations review and county validation.'
accept['gaps'][0]='Eight active judges, clerk and circuit-wide senior assignment reviewed. Jan Shackelford personal contacts and procedures were not found in a bounded official-source search; no unsupported county case assignment inferred.'
packet=run/'draft/checkpoint-015.json';packet.write_text(json.dumps(p,indent=2)+'\n')
with tempfile.TemporaryDirectory() as td: save_checkpoint(root,packet,Path(td)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7701
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,packet,db)
assert ack==save_checkpoint(root,packet,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,path in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(path).read_bytes()
 for f in p['payload']['findings']:
  v=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(v[0])==f['facts']
receipt=dict(ack,artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5)
(review/'checkpoint-ack.json').write_text(json.dumps(receipt,indent=2)+'\n')
state['database_save']=dict(ack,database=str(db));state['execution_status']='senior_review_saved_county_pending'
state['active_assignment']['status']='terminal_exit0_reviewed_and_saved';state['active_assignment']['reviewed_capture']=ack['seq']
state['next_actions']=['Bounded current-status screen of historical Magistrate Michelle Inere lead.','Shared courthouse-access/clerk operational review or explicit prior-source reuse.','Regenerate reviewed directory including circuit-wide senior with documented gaps; validate before county acceptance/publication.','Next county Bay is Fourteenth Judicial Circuit.']
(run/'state.json').write_text(json.dumps(state,indent=2)+'\n')
resume=run/'RESUME.txt';resume.write_text(f"CURRENT: reviewed Jan Shackelford saved at {ack['seq']} / packet015. Worker72083 terminal exit0; do not restart. Contacts/procedures not found in bounded search; assignment circuit-wide. County pending. Next historical Michelle Inere current-status screen, then shared operations. Do not rerun save-reviewed.py.\n\n"+resume.read_text())
print(json.dumps(receipt))
