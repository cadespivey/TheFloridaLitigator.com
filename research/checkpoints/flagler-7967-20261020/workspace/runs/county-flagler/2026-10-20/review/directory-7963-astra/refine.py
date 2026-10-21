import json,re
from pathlib import Path
from flwu.county_directory import validate_supplement
from flwu.publication import digest
r=Path(__file__).parent;d=json.loads((r/'initial-draft.json').read_text());a=json.loads((r/'initial-field-audit.json').read_text());p=json.loads(Path('output/county-review/flagler-7965/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']}
labels={'submission_email':'Division submissions email','hearing_materials_email':'Hearing materials email'}
for person in d['people']:
 f=facts[person['id']];c=f['contact'];audit=a[person['id']];role=f['role'];person['court_ids']=['county_flagler'] if role=='County Judge' else ['circuit_seventh']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['county_flagler','circuit_seventh']
 for field,label in labels.items():
  if c.get(field):
   value=c[field];row=dict(label=label,lines=value if isinstance(value,list) else [value],fact_path='contact.'+field)
   if 'email' in field:row['href']='mailto:'+value
   elif 'fax' in field:row['href']='tel:'+re.sub(r'\D','',value)
   person['contacts']['office'].append(row);path='contact.'+field
   if path in audit['omitted_contact_fields']:audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if c.get('contact_note'):
  person['contacts']['office'].append(dict(label='Contact scope',lines=[c['contact_note']],fact_path='contact.contact_note',type='note'))
  path='contact.contact_note'
  if path in audit['omitted_contact_fields']:audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if f.get('gaps'):person['contacts']['office'].append(dict(label='Documented gaps',lines=[' '.join(f['gaps'])],fact_path='gaps',type='note'))
 for row in person['contacts']['assistant']:
  if row['fact_path']=='contact.assistant_phone':row['label']='Shared office phone'

 audit['explicit_membership_reviewed']=True;audit['contact_note_disposition']='Contact qualifications/gaps displayed; shared numbers labeled; county/circuit roles explicitly mapped.'
d['courts'][1]['resources']=[{'label':x['label'],'url':x['url']} for x in facts['flagler-tom-bexley']['county_resources']]
d['coverage_note']='Flagler snapshot: six roster judges, clerk, circuit chief and named Flagler hearing officer. County-specific assignments, source conflicts and missing contacts retained. Indexed clerk departmental leads are not promoted as verified contacts; other routine senior/traffic appointments not established by bounded review.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True);(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('Validated pending draft',len(d['people']),'county',sum('county_flagler' in x['court_ids'] for x in d['people']),'circuit',sum('circuit_seventh' in x['court_ids'] for x in d['people']))
for k,v in a.items():print(k,v['omitted_contact_fields'],v['omission_reasons'])
