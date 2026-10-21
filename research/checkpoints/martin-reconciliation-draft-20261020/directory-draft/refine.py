import json,re
from pathlib import Path
from flwu.county_directory import validate_supplement
from flwu.publication import digest
r=Path(__file__).parent;d=json.loads((r/'initial-draft.json').read_text());a=json.loads((r/'initial-field-audit.json').read_text());p=json.loads(Path('output/county-review/martin-7905/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']}
labels={'civil_phone':'Civil division phone','civil_email':'Civil division email','civil_fax':'Civil division fax','county_phone':'Martin routing phone','county_email':'Martin submission email','alternate_published_email':'Email — special-set paragraph','probate_email':'Probate email','guardianship_email':'Guardianship email','foreclosure_email':'St. Lucie foreclosure email','case_management_email':'St. Lucie case-management email'}
for person in d['people']:
 f=facts[person['id']];c=f['contact'];audit=a[person['id']];role=f['role'];person['court_ids']=['county_martin'] if role=='County Judge' or 'Traffic' in role else ['circuit_nineteenth']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['county_martin','circuit_nineteenth']
 for field,label in labels.items():
  if c.get(field):
   value=c[field];row=dict(label=label,lines=[value],fact_path='contact.'+field)
   if 'email' in field:row['href']='mailto:'+value
   elif 'phone' in field or 'fax' in field:row['href']='tel:'+re.sub(r'\D','',value)
   if 'levin' in person['id'] and field=='probate_email':row['label']='St. Lucie probate email'
   person['contacts']['office'].append(row);path='contact.'+field
   if path in audit['omitted_contact_fields']:audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if c.get('contact_note'):person['contacts']['office'].append(dict(label='Contact scope',lines=[c['contact_note']],fact_path='contact.contact_note',type='note'))
 if f.get('gaps'):person['contacts']['office'].append(dict(label='Documented gaps',lines=[' '.join(f['gaps'])],fact_path='gaps',type='note'))
 for row in person['contacts']['assistant']:
  if row['fact_path']=='contact.assistant_phone':row['label']='Shared office phone'
 if 'mittleman' in person['id']:person['contacts']['office'].append(dict(label='Appointment status',lines=['Appointment is supported; assumption date and new judicial-office contacts are unconfirmed. No predecessor contact or procedure is adopted.'],fact_path='assignment',type='note'))
 if role=='Clerk of Circuit Court and Comptroller':
  for row in person['contacts']['office']:
   if row['fact_path']=='contact.fax':row['label']='Administration fax'
 audit['explicit_membership_reviewed']=True;audit['contact_note_disposition']='Source contact notes and gaps displayed; shared numbers labeled; county/circuit and dated successor scope explicit.'
d['courts'][1]['resources']=facts['martin-clerk-operations-resources']['resources']
d['coverage_note']='Martin source snapshot includes19 directory records, with Roby/Roberts current service qualified by later appointment evidence and Mittleman contacts/procedures unconfirmed. Hendriks appointment is recorded in research but his old St.Lucie county-office contacts are not presented as Martin circuit contacts. Senior current-service and traffic-officer personal-contact gaps remain explicit. Source discrepancies are preserved without resolving authorities.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True);(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('Validated pending draft',len(d['people']),'county',sum('county_martin' in x['court_ids'] for x in d['people']),'circuit',sum('circuit_nineteenth' in x['court_ids'] for x in d['people']))
