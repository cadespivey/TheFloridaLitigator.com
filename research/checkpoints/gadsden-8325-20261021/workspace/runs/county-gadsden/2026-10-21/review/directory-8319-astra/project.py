import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-gadsden/2026-10-21/review/directory-8319-astra');p=json.loads(Path('output/county-review/gadsden-8319/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[dict(category='Circuit Courts',group_id='circuit_second',label='Second Judicial Circuit',url='https://2ndcircuit.leoncountyfl.gov/'),dict(category='County Courts',group_id='county_gadsden',label='Gadsden',url='https://2ndcircuit.leoncountyfl.gov/gadsden.php',resources=[dict(label='Official Records',url='http://www.gadsdenclerk.com/PublicInquiry/Search.aspx?Type=Name'),dict(label='Court Records',url='https://www.gadsdenclerk.com/CourtScribePublicInquiry'),dict(label='Tax Assessor',url='http://www.qpublic.net/gadsden/')])]
notes={}
for k in ['gadsden-francis-allman','gadsden-acelo-pedroso']:
 f=facts[k];notes[k]=dict(expected_conflicts_sha256=digest(f['conflicts']),notes=[dict(conflict_index=i,title='Source difference',text=v['summary'] if isinstance(v,dict) else v) for i,v in enumerate(f['conflicts'])])
d,a=make_supplement(p,courts,contact_notes=notes);assert len(d['people'])==8
for person in d['people']:
 k=person['id'];f=facts[k];audit=a[k];person['court_ids']=['county_gadsden'] if k=='gadsden-kathy-garner' else ['circuit_second']
 if k=='gadsden-nicholas-thomas':person['court_ids']=['county_gadsden','circuit_second']
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
   value=v['value'];person['contacts']['office'].append(dict(label=key.replace('_',' ').capitalize(),lines=value.splitlines() if isinstance(value,str) else value,type='address' if 'address' in key else 'note',fact_path=path))
 for rows in person['contacts'].values():
  for row in rows:
   if 'fax' in row['fact_path']:row.pop('href',None)
 person['dates']=f.get('stated_dates')
 audit['explicit_court_membership_reviewed']=True
d['coverage_note']='Gadsden: three regular judges, two shared officers, the chief judge and clerk, plus David Frank with a documented assignment discrepancy. Individual procedure gaps and published address/fax differences remain qualified. Chief and shared-officer contacts are not regular county trial assignments.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
for person in d['people']:print(person['id'],person['contacts'],person['contact_notes'])
