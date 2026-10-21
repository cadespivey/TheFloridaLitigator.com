import json,re,copy
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-nassau/2026-10-20/review/directory-8039-astra');r.mkdir(exist_ok=True)
p=json.loads(Path('output/county-review/nassau-8039/packet.json').read_text());before=copy.deepcopy(p)
courts=[{'category':'Circuit Courts','group_id':'circuit_fourth','label':'Fourth Judicial Circuit','url':'https://www.jud4.org/'}]+[x for x in json.loads(Path('src/flwu/data/web/courts.json').read_text()) if x['group_id']=='clerk_nassau']
d,a=make_supplement(p,courts);(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n');assert p==before
facts={e['entity_key']:e['facts'] for e in p['entities']};ids={'nassau-mitch-keiter':'person-clerk-da9db5cf75d14d04','nassau-steven-fahlgren':'person-judge-0d4622dfd74a4503','nassau-jenny-higginbotham':'person-judge-27897e6ce6f44c7f','nassau-meredith-charbula':'person-judge-9284bd4ca0ed4370','nassau-lester-bass':'person-judge-abee1dfe83704d17','nassau-robert-foster':'person-judge-c3c95a933d9c6b9e','nassau-sarah-bell':'person-judge-dbbf0bc7c89c4762'}
labels={'scheduling_contact_name':'Scheduling contact','scheduling_contact_role':'Scheduling role','scheduling_email':'Scheduling email','orders_contact_name':'Orders contact','orders_contact_role':'Orders role','family_services_phone':'Shared Family Court Services phone','appellate_inquiries_email':'Appellate Division inquiries only','additional_physical_address':'Additional location','branch_phone':'Fernandina Beach office phone','public_records_email':'Public records requests only','contact_note':'Contact scope'}
for person in d['people']:
 key=person['id'];f=facts[key];c=f['contact'];audit=a[key]
 person['court_ids']=['clerk_nassau'] if f['role']=='County Judge' else ['circuit_fourth']
 if f['role']=='Clerk':person['court_ids']=['clerk_nassau','circuit_fourth']
 for field,label in labels.items():
  path='contact.'+field
  if field not in c or path not in audit['omitted_contact_fields']:continue
  value=c[field];row={'label':label,'lines':value if isinstance(value,list) else [value],'fact_path':path}
  if 'email' in field:row['href']='mailto:'+value
  elif 'phone' in field:row['href']='tel:'+re.sub(r'\D','',value)
  elif isinstance(value,list):row['type']='address'
  elif field=='contact_note':row['type']='note'
  person['contacts']['office'].append(row);audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if f.get('gaps'):person['contacts']['office'].append({'label':'Contact/procedure gaps','lines':[' '.join(f['gaps'])],'fact_path':'gaps','type':'note'})
 if key=='nassau-mitch-keiter':
  person['contacts']['office']=[row for row in person['contacts']['office'] if row['fact_path']!='contact.mailing_address']
  for row in person['contacts']['office']:
   if row['fact_path']=='contact.physical_address':row['label']='Physical / mailing address'
  audit['omitted_contact_fields'].append('contact.mailing_address');audit['omission_reasons']['contact.mailing_address']='same address displayed as physical / mailing address'
 if key=='nassau-chief-lance-day':
  audit['publication_disposition']='Existing Duval-scoped chief record remains in Fourth Circuit view; Nassau observation retained in research without duplicating the same chief.'
 if key in ids:person['id']=ids[key];audit['published_identity']=ids[key];audit['identity_reason']='Matches same named person in existing Nassau finalized snapshot; changes apply only to current supplement.'
 audit['explicit_court_membership_reviewed']=True
# Existing circuit chief remains visible; no duplicate Nassau copy.
d['people']=[x for x in d['people'] if x['id']!='nassau-chief-lance-day']
d['coverage_note']='Nassau: five active judges, General Magistrate Deirdre Wallace, Senior Judge Robert Foster and Clerk Mitch Keiter. Shared contacts and unavailable direct contacts are qualified. The circuit chief remains listed under the existing Duval record in the Fourth Circuit directory. Procedures are linked from each available official guide; source differences remain in the research baseline.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
print('8 current entries; 7 stable replacements; Wallace added. County3, Nassau circuit6.')
for k,x in a.items():print(k,x['omitted_contact_fields'])
