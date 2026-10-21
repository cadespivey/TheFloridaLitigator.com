import json
from pathlib import Path
from flwu.publication import digest
from flwu.county_directory import validate_supplement
r=Path('runs/county-hendry/2026-10-21/review/directory-8271-astra');d=json.loads((r/'draft.json').read_text());p=json.loads(Path('output/county-review/hendry-8271/packet.json').read_text());notes=[]
for x in d['people']:
 f=next(e['facts'] for e in p['entities'] if e['entity_key']==x['id']);rows=x['contacts']['office']
 if 'room' in f.get('contact',{}):rows.append(dict(label='Hearing room',lines=[f['contact']['room']],fact_path='contact.room'))
 if 'glades_mailing_address' in f.get('contact',{}):rows.append(dict(label='Glades mailing address',lines=f['contact']['glades_mailing_address'],type='address',fact_path='contact.glades_mailing_address'))
 if x['kind']=='Clerk':
  for i,a in enumerate(f['additional_contacts']):
   rows.append(dict(label=a['label']+' phone',lines=[a['phone']],fact_path=f'additional_contacts.{i}.phone',href='tel:'+a['phone'].replace('-','')))
   if a.get('address'):rows.append(dict(label=a['label']+' address',lines=a['address'],type='address',fact_path=f'additional_contacts.{i}.address'))
   if a.get('location'):rows.append(dict(label=a['label']+' location',lines=[a['location']],fact_path=f'additional_contacts.{i}.location'))
 for col in ['office','assistant']:
  for row in x['contacts'][col]:
   val=f
   for part in row['fact_path'].split('.'):val=val[int(part)] if isinstance(val,list) else val[part]
   if row['fact_path'].startswith('conflicts.'):continue
   assert row['lines']==(val if isinstance(val,list) else [val]),(x['id'],row,val)
 notes.append(dict(id=x['id'],source_facts_sha256=digest(f),contact_rows_verified=sum(len(v) for v in x['contacts'].values())))
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'presented-draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'contact-verification.json').write_text(json.dumps(notes,indent=2)+'\n');print(len(notes),'people',sum(n['contact_rows_verified'] for n in notes),'source-exact contact rows')
