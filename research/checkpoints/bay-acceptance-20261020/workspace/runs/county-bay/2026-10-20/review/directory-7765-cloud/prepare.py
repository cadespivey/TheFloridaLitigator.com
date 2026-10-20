import json,copy
from pathlib import Path
from collections import Counter
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
p=Path(__file__).parent
packet=json.loads(Path('output/county-review/bay-7765-b/packet.json').read_text());before=copy.deepcopy(packet)
courts=[dict(group_id='circuit_fourteenth',category='Circuit Courts',label='Fourteenth Judicial Circuit',url='https://jud14.flcourts.org/'),dict(group_id='county_bay',category='County Courts',label='Bay',url='https://jud14.flcourts.org/court-locations/bay-county')]
draft,audit=make_supplement(packet,courts);facts={e['entity_key']:e['facts'] for e in packet['entities'] if e['kind']=='person'}
assert len(draft['people'])==22 and set(facts)=={x['id'] for x in draft['people']}
for person in draft['people']:
 role=facts[person['id']]['role']
 person['court_ids']=['county_bay'] if role=='County Judge' else ['circuit_fourteenth']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['circuit_fourteenth','county_bay']
refinement=next(e for e in packet['entities'] if e['entity_key']=='bay-directory-refinement')
rf=refinement['facts'];draft['courts'][1]['resources']=rf['resource_links']
for person in draft['people']:
 f=facts[person['id']]
 slug=person['id'].removeprefix('bay-judge-')
 if slug in rf['dated_assignment_display']:
  prior=person['assignment'] or 'No assignment stated in the earlier individual source review.'
  person['assignment']=prior+' | AO2026-00-03 (July1,2026–January1,2029, unless amended/rescinded): '+rf['dated_assignment_display'][slug]
  for c in refinement['citations']:
   if c['url'].endswith('2026-00-03.pdf'):
    source={k:c[k] for k in ['url','sha256','retrieved_at']}
    if source not in person['sources']:person['sources'].append(source)
 if person['id']=='bay-judge-russell-roberts':
  for row in person['contacts']['office']:
   if row['fact_path']=='contact.phone':row['label']='Holmes office phone'
   if row['fact_path']=='contact.fax':row['label']='Holmes office fax'
   if row['fact_path']=='contact.office_address':row['label']='Bay chambers — procedure manual'
  person['contacts']['office'].append(dict(label='Holmes office — profile',lines=f['contact']['other_office_address'],fact_path='contact.other_office_address',type='address'))
 if person['id']=='bay-clerk-bill-kinsaul':
  dep=f['departments'][0]
  for field,label in [('phone','Civil department phone'),('fax','Civil department fax'),('email','Civil department email'),('office_address','Civil department address')]:
   row=dict(label=label,lines=dep[field] if isinstance(dep[field],list) else [dep[field]],fact_path='departments.0.'+field)
   if field=='office_address':row['type']='address'
   if field=='email':row['href']='mailto:'+dep[field]
   person['contacts']['office'].append(row)
ra=audit['bay-judge-russell-roberts']
ra['omitted_contact_fields'].remove('contact.other_office_address')
ra['omission_reasons'].pop('contact.other_office_address')
ra['omission_reasons']['contact.contact_note']='Qualification rendered in explicit Holmes phone/fax and separate office-address labels'
ra['editorial_labels_verified']=True
draft['coverage_note']='Reviewed personnel baseline with explicit source-specific gaps and conflicts; dated assignments and contact qualifications remain in supporting research. Publication review pending.'
draft['content_sha256']=digest({k:v for k,v in draft.items() if k!='content_sha256'});validate_supplement(draft,preview=True);assert packet==before
(p/'draft.json').write_text(json.dumps(draft,indent=2)+'\n');(p/'field-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
counts=Counter(g for person in draft['people'] for g in person['court_ids']);assert counts=={'county_bay':6,'circuit_fourteenth':17}
(p/'projection-check.json').write_text(json.dumps(dict(capture=7765,people=22,memberships=dict(counts),source_packet_unchanged=True,review_status='pending',remaining=['Browser validation, release integration and historical isolation','Appraiser target HTTP403; county official referral verified']),indent=2)+'\n')
print(dict(people=22,memberships=dict(counts),roles=dict(Counter(x['kind'] for x in draft['people']))))
print(json.dumps({k:v for k,v in audit.items() if v['omitted_contact_fields']},indent=2))
