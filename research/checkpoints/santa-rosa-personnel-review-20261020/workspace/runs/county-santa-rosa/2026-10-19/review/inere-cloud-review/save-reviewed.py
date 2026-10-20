"""One-time append of reviewed Inere historical lead. Never rerun after acknowledgement."""
import copy,hashlib,json,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-santa-rosa/2026-10-19');review=run/'review/inere-cloud-review';worker=run/'review/inere-local'
assert not (review/'checkpoint-ack.json').exists()
state=json.loads((run/'state.json').read_text());db=Path(state['database_save']['database']);assert state['database_save']['seq']==7703
p=copy.deepcopy(json.loads((run/'draft/checkpoint-015.json').read_text()));p['run_id']='santa-rosa-inere-status-reviewed-20261020';p['payload']['contract']['created_at']=now()
# Hash actual immutable files, never rely on the worker's self-referential manifest.
for folder in [worker,review]:
 for path in sorted(folder.iterdir()):
  if path.is_file() and path.name not in {'worker-events.jsonl','worker-errors.log','appointment-page.png'}:
   p['artifacts'][hashlib.sha256(path.read_bytes()).hexdigest()]=str(path)
fetches=json.loads((worker/'fetch-results.json').read_text());ao=next(x for x in fetches if x['id']=='ao_2014_41_pdf');text=worker/'ao_2014_41_pdf.txt'
for x in fetches:
 b=(worker/x['raw_file']).read_bytes();assert len(b)==x['raw_byte_length'];assert hashlib.sha256(b).hexdigest()==x['raw_sha256']
cite={'url':ao['source_url'],'resolved_url':ao['final_url'],'http_status':200,'retrieved_at':ao['retrieval_time_utc'],'sha256':ao['raw_sha256'],'text_sha256':hashlib.sha256(text.read_bytes()).hexdigest(),'quote':'Inere as Magistrate for the First Judicial Circuit effective September 2, 2014','locator':'PDF page1 appointment paragraph; issuance August29,2014; page visually reviewed','authority':'official','synthetic':False}
assert cite['quote'] in text.read_text()
facts={'name':'Michelle A. Inere','county':'santa_rosa','circuit':1,'status':'bounded_review_complete_current_service_unresolved','reviewed_at':now(),'historical_appointment':{'role':'Magistrate, First Judicial Circuit','issued':'2014-08-29','effective':'2014-09-02','source':ao['source_url']},'historical_lead':'SRCAD2019-03 separately names Magistrate Michelle Inere in its distribution list. This is a historical reference, not independent proof of current service.','current_service':None,'current_contact':None,'procedure_urls':[],'directory_decision':'Do not add a current personnel entry based only on historical evidence. Preserve unresolved current status for future comparison.','bounded_review':['Rendered official magistrates/hearing-officers index: four named magistrates and two hearing officers; Inere not listed in the observed page.','Official circuit site search for Michelle Inere: observed one result, AO2014-41.','Rendered judges-page text search: no Inere match.','Santa Rosa clerk site search: observed no results for Michelle Inere.'],'limitations':['These checks do not establish departure, retirement or absence of other sources.','No inference about restructuring or completeness of the magistrate program.','No substantive procedure review required without supported current service.'],'evidence_notes':{'originals':'Five HTTP bodies with actual source metadata retained; PDF page1 text and visual review confirm appointment/dates.','rendered_evidence':'Exact browser tool events retained under review/inere-cloud-review. Worker *_rendered.txt files are manually transcribed summaries, not verbatim DOM originals.','timestamp_scope':'HTTP acquisition timestamps come from fetch-results.json. Browser observation times not independently asserted.','path_correction':'Worker wrote19files in original checkout outside assigned integrated directory; copied without deletion/overwriting differing bytes and verified hashes via copy-receipt.json.','manifest_correction':'18of19 worker manifest entries match. Self-hash is stale; original preserved, actual bytes hashed independently in this checkpoint.','source_summary_correction':'Rejected only-official-reference claim because2019distribution reference also retained; rejected speculative reasons for roster omission.'}}
p['payload']['findings'].append({'key':'santa-rosa-michelle-inere-status','kind':'source_review','facts':facts,'citations':[cite]})
p['payload']['checks'].append({'id':'historical-inere-current-status-screen','status':'verified','checked_at':now(),'hashes':[cite['sha256']],'scope':'Bounded screening completed; current service remains unresolved, not verified absent.'})
scope=p['payload']['findings'][0]['facts'];scope['limitations']='Eight active judges plus clerk and circuit-wide senior reviewed. Michelle Inere historical appointment/2019reference retained; current service unresolved after bounded official-source screen. Shared operational review remains pending.'
accept=p['payload']['findings'][3]['facts'];accept['next_action']='Complete shared-access/clerk operational review, then county export, reconciliation and acceptance.';accept['gaps'][1]='Michelle Inere current status unresolved after bounded official-source screen; historical2014appointment and2019distribution reference retained. No current entry inferred.'
packet=run/'draft/checkpoint-016.json';packet.write_text(json.dumps(p,indent=2)+'\n')
with tempfile.TemporaryDirectory() as td:save_checkpoint(root,packet,Path(td)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7703
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,packet,db);assert ack==save_checkpoint(root,packet,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,path in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(path).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
receipt=dict(ack,artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5)
(review/'checkpoint-ack.json').write_text(json.dumps(receipt,indent=2)+'\n')
state['database_save']=dict(ack,database=str(db));state['execution_status']='personnel_screen_saved_shared_operations_pending';state['active_assignment']['status']='terminal_exit0_reviewed_and_saved';state['active_assignment']['reviewed_capture']=ack['seq'];state['next_actions']=['Shared courthouse-access/clerk operational review or explicit reusable source evidence.','County export/reconciliation including senior with gaps; validate before acceptance/publication.','Next county Bay, Fourteenth Judicial Circuit.']
(run/'state.json').write_text(json.dumps(state,indent=2)+'\n');resume=run/'RESUME.txt';resume.write_text(f'CURRENT: Inere historical-lead screen reviewed/saved at{ack["seq"]}/packet016. Worker18646 terminal exit0. Current service unresolved; no current entry inferred. Next shared operations review. Do not rerun successful save scripts.\n\n'+resume.read_text())
print(json.dumps(receipt))
