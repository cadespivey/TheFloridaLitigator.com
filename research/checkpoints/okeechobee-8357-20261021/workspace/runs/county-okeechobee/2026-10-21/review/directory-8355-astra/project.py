import json
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-okeechobee/2026-10-21/review/directory-8355-astra');p=json.loads(Path('output/county-review/okeechobee-8355/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']};resources=facts['okeechobee-public-resources']['resources'];courts=[dict(category='Circuit Courts',group_id='circuit_nineteenth',label='Nineteenth Judicial Circuit',url='https://www.circuit19.org/'),dict(category='County Courts',group_id='county_okeechobee',label='Okeechobee',url='https://www.circuit19.org/judges/?_location=okeechobee',resources=resources)]
notes={}
for k in ['okeechobee-william-wallace','okeechobee-kameisha-presley','okeechobee-rebecca-white','okeechobee-vacant-hearing-officer']:
 f=facts[k];v=f['conflicts'][0];notes[k]=dict(expected_conflicts_sha256=digest(f['conflicts']),notes=[dict(conflict_index=0,title='Source difference',text=v if isinstance(v,str) else v['summary'])])
d,a=make_supplement(p,courts,contact_notes=notes);assert len(d['people'])==14
for person in d['people']:
 k=person['id'];f=facts[k];audit=a[k];person['court_ids']=['county_okeechobee'] if k in ['okeechobee-william-wallace','okeechobee-jeffrey-battista','okeechobee-robert-goldman','okeechobee-ryan-grazi','okeechobee-jessica-sebag'] else ['circuit_nineteenth']
 if k=='okeechobee-jerald-bryant':person['court_ids']=['county_okeechobee','circuit_nineteenth']
 for path in list(audit['omitted_contact_fields']):
  container,key=path.split('.');value=f[container][key]
  if value is None:continue
  lines=value if isinstance(value,list) else [value];existing=next((row for rows in person['contacts'].values() for row in rows if row['lines']==lines),None)
  if existing:audit['omission_reasons'][path]='Exact same value displayed at '+existing['fact_path'];continue
  row=dict(label=key.replace('_',' ').capitalize(),lines=lines,fact_path=path)
  if 'address' in key:row['type']='address'
  if 'note' in key or 'procedure_phone' in key:row['type']='note'
  person['contacts']['assistant' if 'assistant' in key else 'office'].append(row);audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 for i,o in enumerate(f.get('contact_observations',[])):person['contacts']['office'].append(dict(label='Published contact detail',lines=[o],type='note',fact_path=f'contact_observations.{i}'))
 for rows in person['contacts'].values():
  for row in rows:
   if 'fax' in row['fact_path']:row.pop('href',None)
 audit['explicit_court_membership_reviewed']=True
 # Clerk services remain individually labeled, not personal chambers routes.
 for i,o in enumerate(f.get('service_contacts',[])):person['contacts']['office'].append(dict(label=o['label'],lines=[o['email']],fact_path=f'service_contacts.{i}.email',href='mailto:'+o['email']))
d['coverage_note']='Okeechobee regular judges, shared magistrates/hearing offices, chief, clerk, Early Childhood Court cross-assignment and four appointed traffic officers. Vacancy, unpublished traffic-officer contacts and source differences retained; shared offices are not dedicated county chambers.';d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True);(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
for person in d['people']:print(person['name'],person['contacts'])
