"""One-time bounded filing followup append; never rerun after acknowledgement."""
import copy,hashlib,json,sqlite3,tempfile
from pathlib import Path
from bs4 import BeautifulSoup
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-santa-rosa/2026-10-19');review=run/'review/filing-cloud-review';worker=run/'review/filing-followup-local'
assert not (review/'checkpoint-ack.json').exists()
state=json.loads((run/'state.json').read_text());db=Path(state['database_save']['database']);assert state['database_save']['seq']==7707
p=copy.deepcopy(json.loads((run/'draft/checkpoint-017.json').read_text()));p['run_id']='santa-rosa-filing-followup-reviewed-20261020';p['payload']['contract']['created_at']=now()
manifest=json.loads((worker/'manifests.json').read_text())
for name,meta in manifest.items():
 b=(worker/name).read_bytes();assert len(b)==meta['byte_length'] and hashlib.sha256(b).hexdigest()==meta['sha256']
fetch=json.loads((worker/'fetch-metadata.json').read_text());citations=[]
for name,quote in [('pro-se-page','Pro Se filings are accepted'),('contact-page','For court related correspondence:')]:
 meta=fetch[name];raw=worker/meta['raw_file'];soup=BeautifulSoup(raw.read_bytes(),'html.parser')
 for tag in soup(['script','style']):tag.decompose()
 text=soup.get_text(' ',strip=True);assert quote in text;path=review/(name+'-original-extracted.txt');path.write_text(text)
 citations.append({'url':meta['url'],'resolved_url':meta['final_url'],'http_status':meta['status'],'retrieved_at':meta['retrieved_utc'],'sha256':meta['sha256'],'text_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'quote':quote,'locator':'Original HTML substantive page body; footer office location/correspondence not treated as filing authorization.','authority':'official','synthetic':False})
for folder in [worker,review]:
 for path in sorted(folder.iterdir()):
  if path.is_file() and path.name not in {'worker-events.jsonl','worker-errors.log'}:p['artifacts'][hashlib.sha256(path.read_bytes()).hexdigest()]=str(path)
facts={'county':'santa_rosa','circuit':1,'reviewed_at':now(),'review_status':'bounded_followup_complete_with_gaps','pages_reviewed':[x['url'] for x in citations],'finding':'The Pro Se Information page says pro se filings are accepted for its listed matters but does not specify a physical, mail or electronic submission channel. Its definition of pro se includes in person in the sense of self-representation; that wording plus an office-address footer is not evidence of a physical filing route. The contact page gives correspondence routing and departmental contact details, not filing permission.','scope':'Only the specified official Pro Se Information page and its linked contact page. Basic channel discovery; no substantive family-law review, forms, manuals or merits.','gaps':{'in_person_filing':'not_found_in_two_page_review','mail_filing':'not_found_in_two_page_review','e_filing_requirements':'not_found_in_two_page_review','filing_window_hours':'not_found_in_two_page_review','policy_effective_date':'not_stated'},'disposition':'Retain these explicit bounded evidence gaps for future comparison. This review does not assert that any filing route is unavailable. No further broad source search required to accept this bounded baseline.','corrections':['Worker circuit2replaced with established county circuit1; scope/stream unchanged.','Rejected inference that definition of pro se and office location confirm in-person filing.','Use exact acquisition metadata, not approximate17:16time in worker narrative.','Preserve original worker drafts as received, not accepted assertions. Browser snapshot transcriptions are secondary; original full HTML supports this finding.'],'validation':{'worker_manifest_entries_verified':len(manifest),'original_response_bodies_preserved':2,'county_acceptance':False}}
p['payload']['findings'].append({'key':'santa-rosa-filing-channel-followup','kind':'source_review','facts':facts,'citations':citations})
for check in p['payload']['checks']:
 if check['id']=='general-civil-filing-instructions':check.update(status='verified',checked_at=now(),hashes=[x['sha256'] for x in citations],scope='Bounded followup and explicit gap disposition verified; filing channels themselves are not verified.')
shared=p['payload']['findings'][-2]['facts'];shared['clerk_operations']['filing_channel_status']='not_found_after_two_page_targeted_followup';shared['clerk_operations']['next_bounded_source']='Observed Pro Se Information link and linked contact page now reviewed; explicit gaps retained.'
a=p['payload']['findings'][3]['facts'];a['next_action']='Reconcile saved personnel and gaps; produce pinned repeatable county export and pending website supplement; validate before county acceptance/publication.';a['gaps'][2]='Shared-access/ADA/clerk review and targeted filing followup completed with explicit filing-channel/window-hour gaps. No conflict resolution or universal filing availability claim.'
packet=run/'draft/checkpoint-018.json';packet.write_text(json.dumps(p,indent=2)+'\n')
with tempfile.TemporaryDirectory() as td:save_checkpoint(root,packet,Path(td)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7707
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,packet,db);assert ack==save_checkpoint(root,packet,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,path in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(path).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
receipt=dict(ack,artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);(review/'checkpoint-ack.json').write_text(json.dumps(receipt,indent=2)+'\n')
state['database_save']=dict(ack,database=str(db));state['execution_status']='bounded_research_saved_county_validation_pending';state['active_assignment']['status']='terminal_exit0_reviewed_and_saved';state['active_assignment']['reviewed_capture']=ack['seq'];state['next_actions']=['Reconcile pinned county roster and source dispositions, export twice and compare.','Prepare ten-person directory draft including senior with gaps; validate combined views and historical isolation before acceptance/publication.','Next county Bay, Fourteenth Judicial Circuit.'];(run/'state.json').write_text(json.dumps(state,indent=2)+'\n')
resume=run/'RESUME.txt';resume.write_text(f'CURRENT: filing-channel followup saved at{ack["seq"]}/packet018. Worker69181 terminal. Explicit channel gaps retained; circuit1and inference corrected. No further broad research needed before county reconciliation/export. Do not rerun saved scripts.\n\n'+resume.read_text());print(json.dumps(receipt))
