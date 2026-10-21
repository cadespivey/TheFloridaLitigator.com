import json,re
from pathlib import Path
from flwu.county_directory import validate_supplement
from flwu.publication import digest
r=Path(__file__).parent;d=json.loads((r/'initial-draft.json').read_text());a=json.loads((r/'initial-field-audit.json').read_text());p=json.loads(Path('output/county-review/highlands-8013/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']}
labels={'civil_email':'Civil email','civil_fax':'Civil fax','civil_phone':'Circuit civil phone','records_email':'Official records email','records_fax':'Official records fax'}
for person in d['people']:
 f=facts[person['id']];c=f['contact'];audit=a[person['id']];role=f['role'];person['court_ids']=['county_highlands'] if role in ['County Judge','Civil Traffic Hearing Officer'] else ['circuit_tenth']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['county_highlands','circuit_tenth']
 for field,label in labels.items():
  if c.get(field):
   value=c[field];row=dict(label=label,lines=[value],fact_path='contact.'+field)
   if 'email' in field:row['href']='mailto:'+value
   elif 'fax' in field or 'phone' in field:row['href']='tel:'+re.sub(r'\D','',value)
   person['contacts']['office'].append(row);path='contact.'+field;audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if c.get('contact_note'):
  text=c['contact_note'].replace('at590SouthCommerce','at 590 South Commerce').replace('hours8:00AM','hours 8:00 AM').replace('4:30PM','4:30 PM').replace('November2','November 2')
  person['contacts']['office'].append(dict(label='Contact scope',lines=[text],fact_path='contact.contact_note',type='note'));path='contact.contact_note';audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if f.get('gaps'):person['contacts']['office'].append(dict(label='Documented gaps',lines=[' '.join(f['gaps'])],fact_path='gaps',type='note'))
 for row in person['contacts']['assistant']:
  if row['fact_path']=='contact.assistant_phone':row['label']='Shared office phone'
 if f.get('office_status')=='future_assignment_as_stated':person['name']='Gary Ellis — assignment effective November 2, 2026'
 audit['explicit_membership_reviewed']=True;audit['contact_note_disposition']='Qualifications and gaps displayed; shared phone duplicate omitted; vacancy and future appointee distinguished.'
d['courts'][1]['resources']=facts['highlands-jerome-kaszubowski']['county_resources'];d['coverage_note']='Highlands snapshot: four circuit judges, circuit chief, clerk, nine circuit-appointed magistrates/hearing officers and two traffic hearing officers. The county website lists a vacancy; Gary Ellis’s assignment is stated effective November 2, 2026 and is shown separately. Conflicting sources and missing direct contacts remain qualified. Circuit senior roster retained in the database; no routine Highlands senior assignment established.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True);(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('Pending draft',len(d['people']),'county',sum('county_highlands' in x['court_ids'] for x in d['people']),'circuit',sum('circuit_tenth' in x['court_ids'] for x in d['people']))
for key,v in a.items():print(key,v['omitted_contact_fields'],v['omission_reasons'])
