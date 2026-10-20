"""One-time Bay acceptance; do not rerun after acknowledgement."""
import copy, hashlib, json, sqlite3, tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.county_directory import public_metadata, validate_supplement
from flwu.publication import digest
from flwu.history import now
root=Path.cwd(); run=Path('runs/county-bay/2026-10-20'); review=run/'review/directory-7765-cloud'; receipt=review/'acceptance-ack.json'
assert not receipt.exists()
def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
draft=read(review/'draft.json'); validate_supplement(draft,preview=True)
actual=json.loads((review/'browser-links-keyboard.txt').read_text().splitlines()[1]); browser=json.loads((review/'browser-circuit-history.txt').read_text().splitlines()[1])
assert all(actual[str(w)]==dict(rows=6,overflow=False) for w in (390,1280))
assert actual['focus']=='Skip to content' and browser['skip']==dict(hash='#report',focus='report')
assert all(browser['circuit'][str(w)]==dict(rows=22,overflow=False) for w in (390,1280)) and browser['historical']==0
expected=[]
for p in draft['people']:
 if 'county_bay' in p['court_ids']:
  expected += [u for u in (p['profile_url'],p['procedure_url']) if u]
  expected += [r['href'] for rows in p['contacts'].values() for r in rows if r.get('href')]
# Renderer deduplicates identical hrefs within a person's contact groups.
assert set(x['href'] for x in actual['links'])==set(expected)
assert 'Holmes office phone' in browser['roberts'] and 'Bay chambers — procedure manual' in browser['roberts']
stamp=now(); reviewed=public_metadata(copy.deepcopy(draft)); reviewed['review_status']='reviewed'
reviewed['review']={'reviewed_by':'Astra','reviewed_at':stamp,'attestation':'Source/field, role and court-membership review; combined desktop/mobile, rendered-link, keyboard skip-link and historical-isolation checks. Gaps and source conflicts retained without controlling-authority resolution.'}
reviewed['coverage_note']='Seventeen active judges, one senior judge, three judicial officers and the clerk reviewed. Source-specific contact, assignment and procedure gaps remain explicit; noncivil review is limited to basic operations.'
reviewed['content_sha256']=digest({k:v for k,v in reviewed.items() if k!='content_sha256'}); validate_supplement(reviewed);write(review/'reviewed-supplement.json',reviewed)
write(review/'browser-review.json',dict(reviewed_at=stamp,runtime='Installed Chromium 1247; headless with Chromium sandbox enabled',county_rows=6,circuit_rows=22,historical_county_rows=0,viewports=[390,1280],horizontal_overflow=False,skip_link='Keyboard Tab then Enter focused report',rendered_county_links='Matched saved draft targets',visual_screenshots=['bay-7765-desktop.png','bay-7765-mobile.png','bay-7765-roberts-mobile.png'],prior_browser_failures='Default Chrome absent; Firefox startup failed; Safari CUA unavailable. Resolved with installed sandboxed Chromium, no install or inference changes.'))
packet=read(run/'draft/checkpoint-027.json');packet['run_id']='bay-bounded-acceptance-astra-20261020';packet['payload']['contract'].update(created_at=stamp,execution='Astra-only; no local workers. Earlier collected evidence preserved and reviewed.')
for folder in (review,Path('output/county-review/bay-7765-b')):
 for p in sorted(folder.rglob('*')):
  if p.is_file():packet['artifacts'][hashlib.sha256(p.read_bytes()).hexdigest()]=str(p)
for name in ['bay-7765-desktop.png','bay-7765-mobile.png','bay-7765-roberts-mobile.png']:
 p=Path('output/playwright')/name;packet['artifacts'][hashlib.sha256(p.read_bytes()).hexdigest()]=str(p)
ref=next(f for f in packet['payload']['findings'] if f['key']=='bay-directory-refinement')
packet['payload']['findings'].append(dict(key='bay-county-review',kind='county_review',citations=copy.deepcopy(ref['citations']),facts=dict(basis_capture=7765,reviewed_at=stamp,reviewed_by='Astra',research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(active_judges=17,senior_judges=1,judicial_officers=3,clerk=1,people=22),validation=dict(repeat_export_identical_files=168,cited_artifact_hashes_verified=137,export_entities=28,county_rows=6,circuit_rows=22,historical_county_rows=0,tests='542 passed before release integration',reviewed_supplement_digest=reviewed['content_sha256']),next_action='Integrate and validate publication, preserving five historical reports.')))
packet['payload']['checks']=[dict(id='county-roster',status='verified',checked_at=stamp,hashes=[hashlib.sha256((review/'projection-check.json').read_bytes()).hexdigest()],scope='22 reviewed people; bounded source gaps preserved'),dict(id='county-publication',status='incomplete')]
path=run/'draft/checkpoint-028.json';write(path,packet);db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(packet['stream'],)).fetchone()[0]==7765
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==packet['payload']
 for sha,p in packet['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(sha,)).fetchone()[0]==Path(p).read_bytes()
 for f in packet['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
write(receipt,dict(ack,artifacts_readback=len(packet['artifacts']),findings_readback=len(packet['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5));print(receipt.read_text())
