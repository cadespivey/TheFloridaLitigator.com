import json,copy,re
from pathlib import Path
from flwu.county_review import export_review
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
if not Path('output/county-review/jackson-8185').exists():export_review('/Users/cadespivey/.local/share/flwu/research-history.sqlite','manual_research:county-baseline-v1:d6c7d5e70f60',8185,'output/county-review/jackson-8185')
r=Path('runs/county-jackson/2026-10-21/review/directory-8185-astra');r.mkdir(exist_ok=True);p=json.loads(Path('output/county-review/jackson-8185/packet.json').read_text());before=copy.deepcopy(p);facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[dict(category='Circuit Courts',group_id='circuit_fourteenth',label='Fourteenth Judicial Circuit',url='https://jud14.flcourts.org/'),dict(category='County Courts',group_id='county_jackson',label='Jackson',url='https://jud14.flcourts.org/court-locations/jackson-county',resources=facts['jackson-shared-civil-access-baseline']['county_resource_links'])]
d,a=make_supplement(p,courts);assert p==before;assert len(d['people'])==6
(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n')
labels=dict(contact_note='Contact scope',profile_office_phone='Calhoun office phone — profile',profile_fax='Calhoun fax — directory',procedure_assistant_name='Assistant — procedure PDF',procedure_assistant_email='Assistant email — procedure PDF',small_claims_fax='Small claims fax',hours='Office hours')
for person in d['people']:
 k=person['id'];f=facts[k];c=f['contact'];audit=a[k];person['court_ids']=['county_jackson'] if f['role']=='County Judge' else ['circuit_fourteenth']
 if person['kind']=='Clerk':person['court_ids']=['county_jackson','circuit_fourteenth']
 for path in list(audit['omitted_contact_fields']):
  key=path.split('.',1)[1];value=c[key]
  if value is None or value==[]:continue
  lines=value if isinstance(value,list) else [value];existing=next((row for rows in person['contacts'].values() for row in rows if row['lines']==lines),None)
  if existing:
   audit['omission_reasons'][path]='Exact same value displayed at '+existing['fact_path'];continue
  row=dict(label=labels.get(key,key.replace('_',' ').capitalize()),lines=lines,fact_path=path)
  if 'address' in key:row['type']='address'
  if key=='contact_note':row['type']='note'
  if isinstance(value,str) and '@' in value and ' ' not in value:row['href']='mailto:'+value
  person['contacts']['assistant' if 'assistant' in key else 'office'].append(row);audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 for rows in person['contacts'].values():
  for row in rows:
   key=row['fact_path'].split('.')[-1]
   if key in labels:row['label']=labels[key]
   if k=='jackson-brandon-young' and key in ['office_phone','fax']:row['label']='Jackson '+('phone' if key=='office_phone' else 'fax')+' — directory'
   if len(row['lines'])==1 and re.fullmatch(r'[\d ()-]+',row['lines'][0]):row['href']='tel:'+re.sub(r'\D','',row['lines'][0])
 for n,conflict in enumerate(f.get('conflicts',[])):
  if isinstance(conflict,dict) and conflict.get('summary'):person['contact_notes'].append(dict(title='Source difference',text=conflict['summary'],fact_path=f'conflicts.{n}'))
 audit['explicit_court_membership_reviewed']=True
d['coverage_note']='Jackson: three judges, two court officers and the clerk. Individual missing contacts/procedures and source discrepancies remain qualified. Current named Jackson senior assignment not established in bounded review. Appraiser destination is official-clerk-linked but returned403.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True);(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print([(x['id'],sum(len(v) for v in x['contacts'].values())) for x in d['people']]);print({k:v['omission_reasons'] for k,v in a.items()})
