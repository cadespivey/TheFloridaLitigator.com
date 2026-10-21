import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
p=Path(__file__).parent;packet=json.loads(Path('output/county-review/indian-river-7815-a/packet.json').read_text());initial=json.loads((p/'initial-draft.json').read_text());draft,audit=make_supplement(packet,initial['courts']);facts={e['entity_key']:e['facts'] for e in packet['entities']}
for person in draft['people']:
 f=facts[person['id']];role=f['role'];c=f['contact'];a=audit[person['id']]
 person['court_ids']=['county_indian_river'] if role in ['County Judge','Civil Traffic Infraction Hearing Officer'] else ['circuit_nineteenth']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['circuit_nineteenth','county_indian_river']
 def add(field,label,kind=None):
  v=c[field];row=dict(label=label,lines=v if isinstance(v,list) else [v],fact_path='contact.'+field)
  if kind:row['type']=kind
  if 'email' in field:row['href']='mailto:'+v
  if 'phone' in field:row['href']='tel:'+re.sub(r'\D','',v)
  person['contacts']['office'].append(row)
  path='contact.'+field
  if path in a['omitted_contact_fields']:a['omitted_contact_fields'].remove(path);a['omission_reasons'].pop(path)
 for field,label,kind in [('county_email','Indian River office email',None),('county_phone','Indian River office phone',None),('procedure_phone','Phone — October 6 procedure guide',None),('civil_fax','Civil division fax',None),('civil_office_address','Civil department','address')]:
  if c.get(field):add(field,label,kind)
 if person['id'].endswith(('nicole-menz','robyn-stone')):
  for row in person['contacts']['assistant']:
   if row['fact_path']=='contact.assistant_email':row['label']='Shared county-court email'
 if person['id'].endswith('ryan-butler'):
  for row in person['contacts']['office']:
   if row['fact_path']=='contact.fax':row['label']='Administration fax'
  person['contacts']['office'].append(dict(label='Hours',lines=['Civil and family: 8 a.m.–5 p.m.'],fact_path='contact.contact_note',type='note'))
 if role=='Civil Traffic Infraction Hearing Officer':
  person['contacts']['office'].append(dict(label='Court contacts',lines=['Not established in reviewed court sources.'],fact_path='contact.contact_note',type='note'))
  person['contacts']['assistant'].append(dict(label='Assistant',lines=['Not identified in reviewed court sources.'],fact_path='contact.assistant_name',type='note'))
  person['contact_status']='not_verified'
  person['contacts']['office'].append(dict(label='Role',lines=['Civil traffic infraction hearing officer'],fact_path='role'))
 for i,conflict in enumerate(person['conflicts']):
  if conflict.get('subject') in ['Email spellings','Courtesy-copy email domain','Assistant first-name spelling']:
   person['contact_notes'].append(dict(title=conflict['subject'],text='; '.join(conflict['statements'])+'. Source differences retained.',fact_path=f'conflicts.{i}'))
 if person['id'].endswith('robert-meadows'):
  person['contacts']['office'].append(dict(label='County assignment',lines=['Conflicting official sources: profile says Indian River; roster and dated order say St. Lucie.'],fact_path='assignment'))
 if person['id'].endswith('rebecca-white'):
  for row in person['contacts']['assistant']:
   if row['fact_path']=='contact.assistant_phone':row['label']='Phone — profile'
 a['explicit_membership_reviewed']=True
 a['contact_note_disposition']='Contact qualifiers reviewed against facts; material routes/numbers displayed with source labels. Narrative research context retained in evidence.'
draft['courts'][1]['resources']=facts['indian-river-ryan-butler']['county_resource_links']
draft['coverage_note']='Indian River personnel baseline includes six county-assigned judges, two magistrates, two child-support offices (one vacant), four traffic hearing officers, the clerk and circuit-wide chief. Meadows is a separate entry with conflicting county assignments. Traffic-officer court contacts and individual procedures were not established; no named senior assignment was established in the bounded review.'
draft['content_sha256']=digest({k:v for k,v in draft.items() if k!='content_sha256'});validate_supplement(draft,preview=True)
(p/'draft.json').write_text(json.dumps(draft,indent=2)+'\n');(p/'field-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Validated pending draft:',len(draft['people']),'entries; explicit county members',sum('county_indian_river' in x['court_ids'] for x in draft['people']))
