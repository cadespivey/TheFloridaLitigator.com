import json
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-baker/2026-10-21/review/directory-8437-astra');r.mkdir(exist_ok=True)
p=json.load(open('output/county-review/baker-8437/packet.json'));facts={e['entity_key']:e['facts'] for e in p['entities']};courts=[dict(category='Circuit Courts',group_id='circuit_eighth',label='Eighth Judicial Circuit',url='https://circuit8.org/'),dict(category='County Courts',group_id='county_baker',label='Baker',url='https://circuit8.org/courts-judges/baker-county/',resources=facts['baker-shared-civil-access-baseline']['county_resource_links'])]
notes={}
for k,indices in [('baker-samuel-stafford',[0])]:
 f=facts[k];notes[k]=dict(expected_conflicts_sha256=digest(f['conflicts']),notes=[dict(conflict_index=i,title='Source-specific contact',text=f['conflicts'][i]) for i in indices])
d,a=make_supplement(p,courts,contact_notes=notes);assert len(d['people'])==12
for person in d['people']:
 k=person['id'];f=facts[k];audit=a[k];person['court_ids']=['county_baker'] if k=='baker-julie-johnson' else ['circuit_eighth']
 if k=='baker-stacie-harvey':person['court_ids']=['county_baker','circuit_eighth']
 for path in list(audit['omitted_contact_fields']):
  parts=path.split('.');v=f
  for part in parts:v=v[part]
  key=parts[-1]
  if v is None:continue
  lines=v if isinstance(v,list) else str(v).splitlines()
  existing=next((row for rows in person['contacts'].values() for row in rows if row['lines']==lines),None)
  if existing:audit['omission_reasons'][path]='Exact same value displayed at '+existing['fact_path'];continue
  row=dict(label=key.replace('_',' ').capitalize(),lines=lines,fact_path=path,type='address' if 'address' in key else 'note')
  person['contacts']['assistant' if 'assistant' in key else 'office'].append(row);audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 for rows in person['contacts'].values():
  for row in rows:
   if 'fax' in row['fact_path']:row.pop('href',None)
 audit['explicit_court_membership_reviewed']=True;person['dates']=f.get('stated_dates')
d['coverage_note']='Baker: five regular judges, shared judicial officers and circuit administrators, and clerk. Shared subject-specific roles do not imply regular Baker civil assignments. Clerk contact evidence was observed October 11; the October 21 refresh was blocked.'
legacy=json.load(open('website/updates/update-a2af444acf5630d9bf71.json'))['directory']
identity={}
for person in d['people']:
 matches=[x for x in legacy if x['name']==person['name'] and 'Baker' in x.get('counties',[])]
 if matches:
  assert len(matches)==1
  original=person['id'];person['id']=matches[0]['id'];identity[person['id']]=original
(r/'identity-review.json').write_text(json.dumps(identity,indent=2)+'\n')
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');(r/'project.py').write_text(Path('/tmp/project-baker.py').read_text())
for x in d['people']:print(x['id'],x['kind'],a[identity.get(x['id'],x['id'])]['omitted_contact_fields'])
