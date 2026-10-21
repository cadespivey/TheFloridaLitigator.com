import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-putnam/2026-10-21/review/directory-8131-astra');p=json.loads(Path('output/county-review/putnam-8131/packet.json').read_text());before=copy.deepcopy(p);facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[{'category':'Circuit Courts','group_id':'circuit_seventh','label':'Seventh Judicial Circuit','url':'https://circuit7.org/'},{'category':'County Courts','group_id':'county_putnam','label':'Putnam','url':'https://circuit7.org/putnam-county/','resources':facts['putnam-shared-rules-access-resources']['county_resource_links']}]
d,a=make_supplement(p,courts);assert p==before;assert len(d['people'])==11;(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n')
shared={'putnam-chief-leah-case','putnam-dennis-craig','putnam-howard-mcgillin'}
d['people']=[x for x in d['people'] if x['id'] not in shared]
for k in shared:a[k]['public_projection']='Existing multi-county archived directory identity retained; contacts reviewed without duplicating/replacing other-county coverage.'
def add(person,label,value,path,kind=None):
 row={'label':label,'lines':value if isinstance(value,list) else [value],'fact_path':path}
 if kind:row['type']=kind
 if isinstance(value,str):
  if '@' in value and ' ' not in value:row['href']='mailto:'+value
  elif re.fullmatch(r'[\d()-]+',value):row['href']='tel:'+re.sub(r'\D','',value)
 person['contacts']['office'].append(row)
for person in d['people']:
 k=person['id'];f=facts[k];c=f['contact'];audit=a[k];person['id']=f.get('prior_baseline_id',k);audit['public_id']=person['id']
 person['court_ids']=['county_putnam'] if f['role']=='County Judge' else ['circuit_seventh']
 if f['role']=='Clerk of Circuit Court and Comptroller':person['court_ids']=['county_putnam','circuit_seventh']
 person['dates']=f.get('stated_dates')
 for path in list(audit['omitted_contact_fields']):
  key=path.split('.',1)[1];value=c[key]
  if key=='branch_contacts':
   for n,branch in enumerate(value):
    for field in ['address','hours']:add(person,branch['office']+' '+field,branch[field],f'contact.branch_contacts.{n}.{field}','address' if field=='address' else None)
  elif isinstance(value,(str,list)):
   label={'contact_note':'Contact scope','procedure_fax':'Fax — procedure document','procedure_mailing_address':'Mailing address — procedure document','hearing_address':'Hearing location','submission_email':'Order submissions','proposed_orders_email':'Proposed orders','hearing_materials_email':'Hearing materials','customer_service_address':'Customer service address'}.get(key,key.replace('_',' ').capitalize())
   add(person,label,value,path,'note' if key=='contact_note' else 'address' if 'address' in key else None)
  else:continue
  audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 for n,conflict in enumerate(f.get('conflicts',[])):
  if conflict.get('summary'):person['contact_notes'].append({'title':'Source difference','text':conflict['summary'],'fact_path':f'conflicts.{n}'})
 for row in list(person['contacts']['office']):
  if row['fact_path']=='contact.ja_email':
   person['contacts']['office'].remove(row);row['label']='Email';person['contacts']['assistant'].append(row)
 audit['explicit_court_membership_reviewed']=True
 assert not audit['omitted_contact_fields'],(k,audit)
d['coverage_note']='This supplement covers Putnam’s six roster judges, magistrate and clerk; choose the Seventh Circuit directory for circuit personnel. Existing circuit-chief and special cross-county contacts remain available in the Seventh Circuit directory. A current Putnam-specific senior-judge assignment was not established in the reviewed sources; source differences are preserved.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('Eight supplement records; three existing shared records retained.')
