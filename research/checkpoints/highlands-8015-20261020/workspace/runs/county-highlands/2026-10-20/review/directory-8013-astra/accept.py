import json,shutil
from pathlib import Path
from flwu.county_directory import public_metadata,validate_supplement
from flwu.publication import digest
from flwu.history import now
r=Path(__file__).parent;run=r.parent.parent;d=json.loads((r/'draft.json').read_text());validate_supplement(d,preview=True)
def result(n):return json.loads((r/n).read_text().split('### Result\n')[1].split('\n### Ran')[0])
m=result('browser-matrix.txt');assert len(m)==8
for x in m:
 expected=0 if 'from=' in x['query'] else 65 if 'circuit_tenth' in x['query'] else 3 if 'county_flagler' in x['query'] else 5
 assert x['status']==200 and not x['overflow'] and x['rows']==expected
 if 'from=' in x['query']:assert x['historical']
l=result('browser-links.txt');assert l['focus']=='Skip to content' and l['skip']==dict(hash='#report',focus='report');expected=set()
for person in d['people']:
 if 'county_highlands' in person['court_ids']:
  expected.update(u for u in [person['profile_url'],person['procedure_url']] if u);expected.update(row['href'] for rows in person['contacts'].values() for row in rows if row.get('href'))
assert set(l['links'])==expected
packet=json.loads(Path('output/county-review/highlands-8013/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in packet['entities']};audit=json.loads((r/'field-audit.json').read_text());count=0
for person in d['people']:
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=facts[person['id']]
   for key in row['fact_path'].split('.'):v=v[key]
   value=v if isinstance(v,list) else [v]
   for repair in audit[person['id']].get('address_spacing_repairs',[]):
    if repair['fact_path']==row['fact_path']:assert repair['original_lines']==value;value=repair['display_lines']
   assert row['lines']==value,(person['id'],row);count+=1
for file in ['highlands-desktop.png','highlands-mobile-clerk.png']:shutil.copyfile(Path('output/playwright')/file,r/file)
stamp=now();d=public_metadata(d);d.update(review_status='reviewed',review=dict(reviewed_by='Astra',reviewed_at=stamp,attestation=f'Pinned8013: {count} contact rows and explicit memberships checked;299artifacts readback. Browser1280/390 county5/circuit65/priorFlagler3/historical0, actual July1issue, links and keyboard skip verified. Desktop/mobile screenshots inspected. Vacancy and November2 future appointee kept distinct; documented gaps retained.'))
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d);(r/'reviewed-supplement.json').write_text(json.dumps(d,indent=2)+'\n');(r/'contact-verification.json').write_text(json.dumps(dict(contact_rows=count,people=19,pinned_capture=8013,remaining_omissions='Duplicate shared office phone only'),indent=2)+'\n')
p=json.loads((run/'draft/checkpoint-022.json').read_text());p['run_id']='highlands-acceptance-astra-20261020';p['payload']['contract']['created_at']=stamp
f={'key':'highlands-county-review','kind':'county_review','facts':dict(basis_capture=8013,reviewed_by='Astra',reviewed_at=stamp,research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(directory_people=19,county_rows=5,combined_circuit_rows=65,verified_contact_rows=count),validation=dict(viewports=[390,1280],overflow=False,historical_rows=0,historical_issue_selected=True,reviewed_supplement_digest=d['content_sha256']),roster='Four locally listed circuit judges; vacancy and dated future appointee kept distinct; chief, clerk, nine appointed officers and two traffic officers. Ten circuit senior profiles reused; no routine Highlands assignment inferred.',shared_procedures='Submission/case-management/access sources reviewed for Highlands applicability. Polk-only county orders excluded. Historical local rule and mediation establishment screened; no litigation recipes.',limitations=['County vacancy/future appointee/elections-directory conflict preserved without choosing controlling authority.','Direct senior and traffic-officer contacts not established; family virtual policy county applicability unconfirmed.','Tax-assessor target certificate/timeout failures retained; official referring link preserved.','One official elections HTML original contains third-party embedded token and remains SQLite/local only; public recovery metadata records hash/storage exception.'],next_action='Production build/tests, merge and deployed verification; then Nassau.'),'citations':p['payload']['findings'][0]['citations']}
p['payload']['findings'].append(f);(r/'reviewed-packet.json').write_text(json.dumps(p,indent=2)+'\n')
s=Path('runs/county-flagler/2026-10-20/review/directory-7963-astra/save.py').read_text().replace('county-flagler','county-highlands').replace('directory-7963-astra','directory-8013-astra').replace('==7965','==8013').replace('checkpoint-014','checkpoint-023');(r/'save.py').write_text(s);print('Reviewed',count,'contact rows; pending production/publication')
