import json,copy,shutil
from pathlib import Path
from flwu.county_directory import public_metadata,validate_supplement
from flwu.publication import digest
from flwu.history import now
r=Path(__file__).parent;run=r.parent.parent;d=json.loads((r/'draft.json').read_text());validate_supplement(d,preview=True)
def result(name):return json.loads((r/name).read_text().split('### Result\n')[1].split('\n### Ran')[0])
m=result('browser-matrix.txt');assert len(m)==8
for x in m:assert not x['overflow'] and x['rows']==(0 if 'from=' in x['query'] else 54 if 'circuit_nineteenth' in x['query'] else 4 if 'citrus' in x['query'] else 9)
l=result('browser-links.txt');assert '1 update for 2026-07-01' in l['historical'];expected=set()
for person in d['people']:
 if 'county_martin' in person['court_ids']:
  expected.update(x for x in [person['profile_url'],person['procedure_url']] if x);expected.update(row['href'] for rows in person['contacts'].values() for row in rows if row.get('href'))
assert set(l['links'])==expected
k=result('browser-status-keyboard.txt');assert k['focus']=='Skip to content' and k['skip']==dict(hash='#report',focus='report');assert 'assumption date' in k['status'] and 'new judicial-office contacts are unconfirmed' in k['status']
p=json.loads(Path('output/county-review/martin-7905/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']}
for person in d['people']:
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=facts[person['id']]
   for key in row['fact_path'].split('.'):v=v[key]
   assert row['lines']==(v if isinstance(v,list) else [v]),(person['id'],row)
for file in ['martin-desktop-viewport.png','martin-mobile-status.png']:shutil.copyfile(Path('output/playwright')/file,r/file)
stamp=now();d=public_metadata(d);d.update(review_status='reviewed',review=dict(reviewed_by='Astra',reviewed_at=stamp,attestation='Pinned7905 contact/source/court membership review;205original artifact readback; combined desktop/mobile filters and overflow; rendered county links; keyboard skip and expanded successor-gap notes; actual saved July1issue excludes supplement. Source conflicts and explicit contact/senior gaps retained.'))
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d);(r/'reviewed-supplement.json').write_text(json.dumps(d,indent=2)+'\n')
p=json.loads((run/'draft/checkpoint-024.json').read_text());p['run_id']='martin-acceptance-astra-20261020';p['payload']['contract']['created_at']=stamp;p['payload']['findings'].append(dict(key='martin-county-review',kind='county_review',facts=dict(basis_capture=7905,reviewed_by='Astra',reviewed_at=stamp,research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(directory_people=19,county_rows=9,combined_circuit_rows=54),validation=dict(viewports=[390,1280],overflow=False,historical_rows=0,historical_issue_selected=True,reviewed_supplement_digest=d['content_sha256']),gaps='Successor current-service/allocation/contact gaps; no current named senior established; four traffic-officer personal contacts absent; source conflicts retained. No exhaustive noncivil review.',next_action='Production build/tests, merge and deployed verification; then Sumter.'),citations=copy.deepcopy(p['payload']['findings'][0]['citations'])));(r/'reviewed-packet.json').write_text(json.dumps(p,indent=2)+'\n')
s=Path('runs/county-citrus/2026-10-20/review/directory-7853-astra/save.py').read_text().replace('county-citrus','county-martin').replace('directory-7853-astra','directory-7905-astra').replace('checkpoint-018','checkpoint-025').replace('==7853','==7905').replace('Integrate and test production supplement; publish and verify site, then Martin.','Integrate and test production supplement; publish and verify site, then Sumter.');(r/'save.py').write_text(s);print('Acceptance checks passed;19people, all concrete contact rows match pinned facts.')
