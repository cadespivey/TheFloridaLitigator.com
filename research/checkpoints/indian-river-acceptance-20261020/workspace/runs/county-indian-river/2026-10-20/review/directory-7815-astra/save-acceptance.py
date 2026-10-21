"""One-time bounded acceptance; immutable checkpoint, not a historical report."""
import copy, hashlib, json, sqlite3, tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.county_directory import public_metadata, validate_supplement
from flwu.publication import digest
from flwu.history import now
root=Path.cwd();run=Path('runs/county-indian-river/2026-10-20');review=run/'review/directory-7815-astra';receipt=review/'acceptance-ack.json';assert not receipt.exists()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
draft=read(review/'draft.json');validate_supplement(draft,preview=True)
matrix=json.loads((review/'browser-matrix.txt').read_text().splitlines()[1]);links=json.loads((review/'browser-links-keyboard-final.txt').read_text().splitlines()[1])
assert len(matrix)==6
for x in matrix:
 expected=0 if '&from=' in x['q'] else 35 if 'circuit_nineteenth' in x['q'] else 7
 assert x['rows']==expected and not x['overflow']
assert links['focus']=='Skip to content' and links['skip']==dict(hash='#report',focus='report')
expected=set()
for p in draft['people']:
 if 'county_indian_river' in p['court_ids']:
  expected.update(u for u in (p['profile_url'],p['procedure_url']) if u)
  expected.update(r['href'] for rows in p['contacts'].values() for r in rows if r.get('href'))
assert {x['href'] for x in links['links']}==expected
stamp=now();reviewed=public_metadata(copy.deepcopy(draft));reviewed['review_status']='reviewed';reviewed['review']=dict(reviewed_by='Astra',reviewed_at=stamp,attestation='Pinned source/field and court-membership review; combined desktop/mobile, rendered links, keyboard skip-link and historical exclusion verified. Contact gaps, vacant office and conflicting county assignment remain explicit. Practical civil scope; noncivil basic operations only.')
reviewed['content_sha256']=digest({k:v for k,v in reviewed.items() if k!='content_sha256'});validate_supplement(reviewed);write(review/'reviewed-supplement.json',reviewed)
write(review/'review-validation.json',dict(reviewed_at=stamp,people=17,county_rows=7,combined_circuit_rows=35,historical_rows=0,viewports=[1280,390],overflow=False,visual_review='desktop-final and mobile-final screenshots inspected; readable aligned table and stacked mobile records',tests='67 directory/export tests passed',browser_attempt_note='An initial personnel.html URL was incorrect and timed out; final checks used directory.html after that command terminated.',resource_check='See resource-check.json and resource-browser.txt; no certificate checks disabled.',qualifications=['White profile3380/procedure3280','Meadows county conflict visible','vacant office distinct Indian River routing','shared county-court email','clerk administration versus civil fax','traffic court contact gaps']))
packet=read(run/'draft/checkpoint-023.json');packet['run_id']='indian-river-bounded-acceptance-astra-20261020';packet['payload']['contract'].update(created_at=stamp,execution='Astra-only; no local workers. Preserve earlier evidence and five finalized reports.')
for folder in [review,Path('output/county-review/indian-river-7815-b')]:
 for p in sorted(folder.rglob('*')):
  if p.is_file():packet['artifacts'][hashlib.sha256(p.read_bytes()).hexdigest()]=str(p)
for name in ['desktop-final','mobile-final']:
 p=Path(f'output/playwright/indian-river-7815-{name}.png');packet['artifacts'][hashlib.sha256(p.read_bytes()).hexdigest()]=str(p)
ref=next(f for f in packet['payload']['findings'] if f['citations'])
packet['payload']['findings'].append(dict(key='indian-river-county-review',kind='county_review',citations=copy.deepcopy(ref['citations']),facts=dict(basis_capture=7815,reviewed_at=stamp,reviewed_by='Astra',research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(local_judges=6,magistrates=2,child_support_offices=2,traffic_officers=4,clerk=1,circuit_chief=1,additional_conflicted_assignment=1,people=17),validation=dict(cited_artifacts_verified=96,export_entities=29,county_rows=7,circuit_rows=35,historical_rows=0,reviewed_supplement_digest=reviewed['content_sha256']),next_action='Integrate, test and publish reviewed supplement; preserve five historical reports.')))
packet['payload']['checks']=[dict(id='county-roster',status='verified',checked_at=stamp,hashes=[hashlib.sha256((review/'field-audit.json').read_bytes()).hexdigest()],scope='17 reviewed entries; bounded gaps and conflicts preserved'),dict(id='county-publication',status='incomplete')]
path=run/'draft/checkpoint-024.json';write(path,packet);db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(packet['stream'],)).fetchone()[0]==7815
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==packet['payload']
 for h,p in packet['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(p).read_bytes()
 for f in packet['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(packet['artifacts']),findings_readback=len(packet['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);write(receipt,ack)
s=read(run/'state.json');s.update(database_save=ack,next_actions=['Integrate and validate reviewed Indian River supplement; publish with historical isolation.','Then Citrus County, Astra-only one person at a time.']);write(run/'state.json',s);print(receipt.read_text())
