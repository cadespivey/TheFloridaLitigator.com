import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-wakulla/2026-10-21/review/directory-8373-astra');p=json.loads(Path('output/county-review/wakulla-8373/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[dict(category='Circuit Courts',group_id='circuit_second',label='Second Judicial Circuit',url='https://2ndcircuit.leoncountyfl.gov/'),dict(category='County Courts',group_id='county_wakulla',label='Wakulla',url='https://2ndcircuit.leoncountyfl.gov/wakulla.php',resources=[dict(label='Official Records',url='http://www.wakullaclerk.com/landmarkweb'),dict(label='Court Records',url='https://www.civitekflorida.com/ocrs/county/65/'),dict(label='Tax Assessor',url='http://www.qpublic.net/fl/wakullapa/search.html')])]
notes={}
for k in ['wakulla-francis-allman','wakulla-dina-foster']:
 f=facts[k];notes[k]=dict(expected_conflicts_sha256=digest(f['conflicts']),notes=[dict(conflict_index=i,title='Source difference',text=v['summary'] if isinstance(v,dict) else v) for i,v in enumerate(f['conflicts'])])
d,a=make_supplement(p,courts,contact_notes=notes);assert len(d['people'])==6
for person in d['people']:
 k=person['id'];f=facts[k];audit=a[k];person['court_ids']=['county_wakulla'] if k=='wakulla-brian-miller' else ['circuit_second']
 if k=='wakulla-greg-james':person['court_ids']=['county_wakulla','circuit_second']
 for path in list(audit['omitted_contact_fields']):
  container,key=path.split('.');value=f[container][key];lines=value if isinstance(value,list) else [value]
  existing=next((row for rows in person['contacts'].values() for row in rows if row['lines']==lines),None)
  if existing:audit['omission_reasons'][path]='Exact same value displayed at '+existing['fact_path'];continue
  row=dict(label=key.replace('_',' ').capitalize(),lines=lines,fact_path=path)
  if 'address' in key:row['type']='address'
  if 'note' in key:row['type']='note'
  person['contacts']['assistant' if 'assistant' in key else 'office'].append(row);audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 # Preserve additional role-specific contact statements outside the ordinary contact block.
 for i,o in enumerate(f.get('contact_observations',[])):
  person['contacts']['office'].append(dict(label='Published contact detail',lines=[o['statement']],type='note',fact_path=f'contact_observations.{i}.statement'))
 for key,v in f.get('fields',{}).items():
  path='fields.'+key+'.value'
  if not any(row['fact_path']==path for rows in person['contacts'].values() for row in rows):
   value=v['value'];person['contacts']['assistant' if 'assistant' in key else 'office'].append(dict(label=key.replace('_',' ').capitalize(),lines=value.splitlines() if isinstance(value,str) else value,type='address' if 'address' in key else 'note',fact_path=path))
 for rows in person['contacts'].values():
  for row in rows:
   if 'fax' in row['fact_path']:row.pop('href',None)
 for i,svc in enumerate(f.get('service_contacts',[])):
  for key in ['name','phone','email']:
   if svc.get(key):person['contacts']['office'].append(dict(label=svc['label']+' — '+key,lines=[svc[key]],fact_path=f'service_contacts.{i}.{key}'))
 person['dates']=f.get('stated_dates')
 audit['explicit_court_membership_reviewed']=True
d['coverage_note']='Wakulla: two regular judges, two shared officers, the chief judge and clerk. Source assistant/address/fax differences remain qualified. Shared officer and chief responsibilities do not imply regular county trial assignments.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
for person in d['people']:print(person['id'],person['contacts'],person['contact_notes'])
