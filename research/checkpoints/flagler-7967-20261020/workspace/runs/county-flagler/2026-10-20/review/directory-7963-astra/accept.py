import json,copy,shutil
from pathlib import Path
from flwu.county_directory import public_metadata,validate_supplement
from flwu.publication import digest
from flwu.history import now
r=Path('runs/county-flagler/2026-10-20/review/directory-7963-astra');run=r.parent.parent
d=json.loads((r/'draft.json').read_text());validate_supplement(d,preview=True)
def result(n):return json.loads((r/n).read_text().split('### Result\n')[1].split('\n### Ran')[0])
m=result('browser-matrix.txt');assert len(m)==8
for x in m:
 assert x['status']==200 and not x['overflow'] and x['rows']==(0 if 'from=' in x['query'] else 63 if 'circuit_seventh' in x['query'] else 3)
 if 'from=' in x['query']:assert x['historical']
l=result('browser-links.txt');assert l['focus']=='Skip to content' and l['skip']==dict(hash='#report',focus='report');expected=set()
for person in d['people']:
 if 'county_flagler' in person['court_ids']:
  expected.update(u for u in [person['profile_url'],person['procedure_url']] if u);expected.update(row['href'] for rows in person['contacts'].values() for row in rows if row.get('href'))
assert set(l['links'])==expected
p=json.loads(Path('output/county-review/flagler-7965/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']};audit=json.loads((r/'field-audit.json').read_text());count=0
for person in d['people']:
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=facts[person['id']]
   for key in row['fact_path'].split('.'):v=v[key]
   value=v if isinstance(v,list) else [v]
   for repair in audit[person['id']]['address_spacing_repairs']:
    if repair['fact_path']==row['fact_path']:
     assert repair['original_lines']==value;value=repair['display_lines']
   assert row['lines']==value,(person['id'],row);count+=1
assert count==43
for file in ['flagler-desktop.png','flagler-mobile-clerk.png']:shutil.copyfile(Path('output/playwright')/file,r/file)
stamp=now();d=public_metadata(d);d.update(review_status='reviewed',review=dict(reviewed_by='Astra',reviewed_at=stamp,attestation='Pinned7965 contact values and explicit county/circuit memberships reviewed;165artifacts readback. Combined1280/390 filters/no-overflow, county links, keyboard skip and visual clerk layout checked. Actual July1issue excludes supplement. Documented source/contact gaps retained.'))
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d);(r/'reviewed-supplement.json').write_text(json.dumps(d,indent=2)+'\n')
p=json.loads((run/'draft/checkpoint-013.json').read_text());p['run_id']='flagler-acceptance-astra-20261020';p['payload']['contract']['created_at']=stamp
f=next(f for f in p['payload']['findings'] if f['key']=='flagler-county-review');f['facts'].update(basis_capture=7965,reviewed_by='Astra',reviewed_at=stamp,research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(directory_people=9,county_rows=3,combined_circuit_rows=63,verified_contact_rows=count),validation=dict(viewports=[390,1280],overflow=False,historical_rows=0,historical_issue_selected=True,reviewed_supplement_digest=d['content_sha256']),next_action='Production build/tests, merge and deployed verification; then next population-order county.')
(r/'reviewed-packet.json').write_text(json.dumps(p,indent=2)+'\n')
s=Path('runs/county-sumter/2026-10-20/review/directory-7935-astra/save.py').read_text().replace('county-sumter','county-flagler').replace('directory-7935-astra','directory-7963-astra').replace('==7935','==7965').replace('then Flagler.','then next population-order county.');(r/'save.py').write_text(s);shutil.copyfile(__file__,r/'accept.py');print('Accepted pending publication;43 contact rows verified')
