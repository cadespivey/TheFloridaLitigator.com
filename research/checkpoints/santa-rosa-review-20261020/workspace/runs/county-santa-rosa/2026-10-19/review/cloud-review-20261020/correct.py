"""One-time append-only review correction; never rerun after successful save."""
import copy, hashlib, json, sqlite3, tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now

root=Path.cwd(); run=Path('runs/county-santa-rosa/2026-10-19'); review=run/'review/cloud-review-20261020'
state=json.loads((run/'state.json').read_text()); db=Path(state['database_save']['database'])
assert state['database_save']['seq']==7699
p11=json.loads((run/'draft/checkpoint-011.json').read_text())
p12=json.loads((run/'draft/checkpoint-012.json').read_text())
p13=json.loads((run/'draft/checkpoint-013.json').read_text())
p=copy.deepcopy(p13);p['run_id']='santa-rosa-cloud-review-corrections-20261020'
p['payload']['contract']['execution']='Cloud review of local-runner and orchestration work, authorized by user October 20'
p['payload']['contract']['created_at']=now()
p['payload']['checks']=[{'id':'county-roster','status':'incomplete'},{'id':'senior-contact-review','status':'incomplete'},{'id':'material-access-review','status':'incomplete'}]
p['payload']['findings']=copy.deepcopy(p11['payload']['findings'])
scope,_,shared=p['payload']['findings']
scope['facts'].update(finding='The official county roster lists eight active judges. The officer index has no Santa Rosa section; absence is not evidence that no officers serve the county. AO 2026-28 affirmatively assigns Senior Judge Jan Shackelford to the courts of the First Judicial Circuit from August 17 through December 31, 2026. Circuit-wide assignment must remain in scope; no individual Santa Rosa case assignment is inferred.', senior_judges='Jan Shackelford: circuit-wide senior assignment established by AO 2026-28, issued August 18, 2026; stated service period August 17–December 31, 2026. Personal contact/procedure review remains pending.', limitations='Eight is the active-judge roster count, not a complete personnel count. SRCAD2019-03 distribution names Magistrate Michelle Inere historically; it does not establish current service. Bounded current-status screening remains open.')
scope['facts']['review_correction']='Supersedes capture7695 complete-personnel wording and unsupported exclusion of the circuit-wide senior judge.'
scope['citations'].append(copy.deepcopy(shared['citations'][1]))
ao=shared['facts']['ao_2024_25'];ao['scope']='Circuit-wide civil actions, except actions within a Rule 1.200 exception (paragraph 1).'
ao['key_requirements']=['For cases subject to the order, the presiding judge assigns a case-management track within 120 days of commencement; complex cases proceed under Rule 1.201.','Plaintiff or counsel files the Notice of Final Service within five days of service on the last-named defendant and serves the assigned judicial assistant; clerk filing alone is insufficient.','A stipulated amended case-management order must meet the stated time/form requirements and be submitted for final approval by the presiding judge; stipulation alone does not amend the order.']
ao['review_scope']='General applicability and office routing in paragraphs 1–7; stated effective/issuance dates retained. No case-specific deadline calculation or exhaustive motion analysis.'
ad=shared['facts']['srcad_2019_03'];ad['scope']='Directive states applicability to parties in civil, probate and family proceedings in Santa Rosa; practical order-submission rules only.'
ad['key_requirements']=['Attorneys use the Portal Proposed Order function except as otherwise directed by the presiding judge case by case or specified by statute, rule or Supreme Court administrative order.','Attorneys excused under Rule 2.516 may use paper with a certificate of service, conforming copies and addressed stamped envelopes. Unregistered pro se litigants may submit Word by email or paper with copies/envelopes; only paper submissions include a certificate of service.','The directive states specific attorney-service and certificate-of-compliance duties in cases with one pro se party; its required notice qualifies the five-business-day service duty by the pro se party lacking Portal access/registration. See paragraphs 2–3 for wording; do not generalize to every pro se party.','Paragraph 4 states that electronic proposed orders no longer include a certificate of service effective October 1, 2019.']
ad['review_scope']='Pages 1–2 general submission rules and qualifications; historical distribution list reviewed solely as a lead, not current appointment evidence.'
shared['facts']['review_correction']='Restores exceptions and final judicial approval omitted at capture7695. Records source statements without deciding controlling authority.'
# Replace title-only/one-paragraph pinpoints with operative support.
shared['citations'][0]['quote']='The proposed order should be \nsubmitted for final approval by the presiding judge.'
shared['citations'][0]['locator']='PDF pages 1–2, paragraphs 1–7 (especially 1 and 6); page 3 dates'
shared['citations'][1]['quote']='Except as otherwise directed by the presiding judge on a case by case basis, or'
shared['citations'][1]['locator']='PDF pages 1–2, paragraphs 1–4 and historical distribution list'
clerk=copy.deepcopy(p12['payload']['findings'][0])
clerk['facts']['contact_notes']=['The clerk directs court-related correspondence to 4025 Avalon Blvd, Milton, FL 32583; other correspondence goes to 6495 Caroline Street, Milton, FL 32570. The footer separately gives Suite A at Caroline Street.','The main phone/fax are the clerk information line, not personal chambers contacts.']
clerk['facts']['review_scope']='Contact table and footer read against the original HTML; civil, administration and public-records routes checked. No separate clerk operational procedure review is asserted.'
clerk['citations'][0]['quote']='Circuit Civil 981-5667 983-4627 Civil@santarosaclerk.com'
clerk['citations'][0]['locator']='Contact Us department table, correspondence directions and footer; area code 850 stated above table'
p['payload']['findings'][1]=clerk
accept=copy.deepcopy(p13['payload']['findings'][0]);accept['facts'].update(basis_capture=7699,research_review_status='reopened_after_independent_review',publication_status='not_published',reviewed_at=now(),reviewed_by='Cloud independent review, user requested October 20',next_action='Complete bounded senior-contact/current officer lead and material shared-access review; regenerate the county review and acceptance before publication.')
accept['facts']['gaps']=['Eight active judges and the clerk are supported; circuit-wide Senior Judge Jan Shackelford has a collected assignment order but no completed personal contact/procedure review.','Magistrate Michelle Inere appears in a 2019 distribution list only; current status requires a bounded official-source screen, not automatic inclusion.','No separate clerk operational or shared courthouse-access review/reuse attestation was located in the new packets; judge-specific ADA text does not by itself prove completion of that county step.','Original judge-profile discrepancies remain preserved; no authority conflict is resolved.']
accept['facts']['validation']['review_correction']='Earlier counts describe a Santa-Rosa-only preview, not the full 27-supplement production site. The issue identified as July actually reports July 2–August 1. Production acceptance not established by those checks.'
accept['facts']['validation']['sequence_diagnosis']='Sequence gaps do not establish deleted rows. captures uses AUTOINCREMENT with INSERT OR IGNORE; exact replay can advance sqlite_sequence without adding a capture. No deletion is inferred.'
p['payload']['findings'].append(accept)
p['artifacts']={**p11['artifacts'],**p12['artifacts'],**p13['artifacts']}
script=Path(__file__);raw=script.read_bytes();h=hashlib.sha256(raw).hexdigest();p['artifacts'][h]=str(script.relative_to(root))
packet=run/'draft/checkpoint-014.json';packet.write_text(json.dumps(p,indent=2)+'\n')
with tempfile.TemporaryDirectory() as td:save_checkpoint(root,packet,Path(td)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7699
 before=c.execute('select * from finalized_reports order by seq').fetchall()
ack=save_checkpoint(root,packet,db);assert ack==save_checkpoint(root,packet,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,f in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(f).read_bytes()
 for f in p['payload']['findings']:
  v=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(v[0])==f['facts']
state['database_save']=dict(ack,database=str(db));state['execution_status']='review_complete_research_paused';state['acceptance_checkpoint']['status']='superseded_by_review_correction';state['acceptance_checkpoint']['seq_note']='Superseded: gaps do not prove deletion. INSERT OR IGNORE on AUTOINCREMENT can advance the allocator during replay.'
state['next_actions']=['Complete bounded Jan Shackelford senior contact/procedure review and current-status screen of historical Michelle Inere lead.','Record shared access/clerk operational review or reuse evidence, then regenerate county export and acceptance.','Validate a combined production preview with all reviewed supplements; obtain publication review before merge.','After Santa Rosa, Bay is Fourteenth Judicial Circuit (14), not First; verify https://jud14.flcourts.org/ before creating scope/stream.']
(run/'state.json').write_text(json.dumps(state,indent=2)+'\n')
(review/'correction-ack.json').write_text(json.dumps(dict(ack,artifacts_readback=len(p['artifacts']),facts_readback=len(p['payload']['findings']),finalized_reports_unchanged=len(before),replay_verified=True),indent=2)+'\n')
print(json.dumps(ack))
