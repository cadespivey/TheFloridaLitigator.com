import json,copy,shutil
from pathlib import Path
from flwu.county_directory import public_metadata,validate_supplement
from flwu.publication import digest
from flwu.history import now
r=Path(__file__).parent;run=r.parent.parent;d=json.loads((r/'draft.json').read_text());validate_supplement(d,preview=True)
def result(n):return json.loads((r/n).read_text().split('### Result\n')[1].split('\n### Ran')[0])
m=result('browser-matrix.txt');assert len(m)==8
for x in m:assert not x['overflow'] and x['rows']==(0 if 'from=' in x['query'] else 71 if 'circuit_fifth' in x['query'] else 9 if 'county_martin' in x['query'] else 3)
l=result('browser-links.txt');assert '1 update for 2026-07-01' in l['historical'];assert l['focus']=='Skip to content' and l['skip']==dict(hash='#report',focus='report');expected=set()
for person in d['people']:
 if 'county_sumter' in person['court_ids']:
  expected.update(u for u in [person['profile_url'],person['procedure_url']] if u);expected.update(row['href'] for rows in person['contacts'].values() for row in rows if row.get('href'))
assert set(l['links'])==expected
p=json.loads(Path('output/county-review/sumter-7935/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']};count=0
for person in d['people']:
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=facts[person['id']]
   for key in row['fact_path'].split('.'):v=v[key]
   assert row['lines']==(v if isinstance(v,list) else [v]),(person['id'],row);count+=1
for file in ['sumter-desktop.png','sumter-mobile-clerk.png']:shutil.copyfile(Path('output/playwright')/file,r/file)
stamp=now();d=public_metadata(d);d.update(review_status='reviewed',review=dict(reviewed_by='Astra',reviewed_at=stamp,attestation='Pinned7935 contacts and court membership reviewed;212artifacts readback. Combined1280/390 filters/no-overflow, rendered county links, keyboard skip and visual clerk-contact layout checked. Actual July1issue excludes supplement. Source discrepancies and explicit historical senior/traffic/contact gaps retained.'))
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d);(r/'reviewed-supplement.json').write_text(json.dumps(d,indent=2)+'\n')
p=json.loads((run/'draft/checkpoint-013.json').read_text());p['run_id']='sumter-acceptance-astra-20261020';p['payload']['contract']['created_at']=stamp;p['payload']['findings'].append(dict(key='sumter-county-review',kind='county_review',facts=dict(basis_capture=7935,reviewed_by='Astra',reviewed_at=stamp,research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(directory_people=9,county_rows=3,combined_circuit_rows=71,verified_contact_rows=count),validation=dict(viewports=[390,1280],overflow=False,historical_rows=0,historical_issue_selected=True,reviewed_supplement_digest=d['content_sha256']),gaps='Older senior/traffic current-service leads unresolved and original URLs404; individual contact gaps and source conflicts preserved. No exhaustive noncivil review.',next_action='Production build/tests, merge and deployed verification; then Flagler.'),citations=copy.deepcopy(p['payload']['findings'][0]['citations'])));(r/'reviewed-packet.json').write_text(json.dumps(p,indent=2)+'\n')
s=Path('runs/county-martin/2026-10-20/review/directory-7905-astra/save.py').read_text().replace('county-martin','county-sumter').replace('directory-7905-astra','directory-7935-astra').replace('checkpoint-025','checkpoint-014').replace('==7905','==7935').replace('then Sumter.','then Flagler.').replace('Reconcile officers/clerk/chief/senior and county assignments/shared rules before publication.','Retain documented source/contact gaps; verify production and historical isolation before publication.');(r/'save.py').write_text(s);print('Accepted pending publication; contact rows verified',count)
