import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-columbia/2026-10-21/review/directory-8163-astra');p=json.loads(Path('output/county-review/columbia-8163/packet.json').read_text());before=copy.deepcopy(p);facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[{'category':'Circuit Courts','group_id':'circuit_third','label':'Third Judicial Circuit','url':'https://thirdcircuitfl.org/'},{'category':'County Courts','group_id':'county_columbia','label':'Columbia','url':'https://thirdcircuitfl.org/columbia-county/','resources':facts['columbia-shared-civil-access-baseline']['county_resource_links']}]
d,a=make_supplement(p,courts);assert p==before;assert len(d['people'])==10;(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n')
labels={'contact_note':'Contact scope','directory_assistant_email':'Email — circuit directory','directory_fax':'Fax — circuit directory','directory_mailing_address':'Mailing address — circuit directory','directory_address':'Address — circuit directory','administration_phone':'Court Administration referral phone','administration_fax':'Court Administration referral fax','administration_address':'Court Administration referral address','civil_case_manager_name':'Civil case manager','civil_case_manager_email':'Civil case manager email','civil_case_manager_phone':'Civil case manager phone','civil_case_manager_address':'Civil case manager address','general_phone':'Main office phone','civil_supervisor_name':'Civil and records supervisor','civil_supervisor_phone':'Civil and records supervisor phone','official_records_phone':'Official Records phone','probate_phone':'Probate phone','appeals_phone':'Appeals phone','hours':'Office hours'}
for person in d['people']:
 k=person['id'];f=facts[k];c=f['contact'];audit=a[k]
 person['court_ids']=['county_columbia'] if f['role']=='County Judge' or k=='columbia-thomas-kennon' else ['circuit_third']
 if person['kind']=='Clerk':person['court_ids']=['county_columbia','circuit_third']
 person['dates']=f.get('stated_dates')
 for path in list(audit['omitted_contact_fields']):
  key=path.split('.',1)[1];value=c[key];lines=value if isinstance(value,list) else [value]
  existing=next((row for rows in person['contacts'].values() for row in rows if row['lines']==lines),None)
  if existing:
   audit['omission_reasons'][path]='Exact same value displayed at '+existing['fact_path']
   if key in {'assistant_phone','office_phone'}:existing['label']='Shared office phone'
   if key=='office_address' or key=='mailing_address':existing['label']='Office and mailing address'
   continue
  row={'label':labels.get(key,key.replace('_',' ').capitalize()),'lines':lines,'fact_path':path}
  if 'address' in key:row['type']='address'
  if key=='contact_note':row['type']='note'
  if isinstance(value,str):
   if '@' in value and ' ' not in value:row['href']='mailto:'+value
   elif re.fullmatch(r'[\d()-]+',value):row['href']='tel:'+re.sub(r'\D','',value)
  person['contacts']['assistant' if 'assistant' in key else 'office'].append(row)
  audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 for rows in person['contacts'].values():
  for row in rows:
   key=row['fact_path'].split('.')[-1]
   if key in labels:row['label']=labels[key]
   if k in {'columbia-christina-seifert','columbia-steven-johnson'} and key=='office_phone':row['label']='Court Administration phone'
   if k in {'columbia-christina-seifert','columbia-steven-johnson'} and key=='fax':row['label']='Court Administration fax'
   if k=='columbia-christina-seifert' and key=='email':row['label']='Probate proposed orders email'
   if len(row['lines'])==1 and re.fullmatch(r'\d{3}-\d{3}-\d{4}',row['lines'][0]):row['href']='tel:'+re.sub(r'\D','',row['lines'][0])
 for n,conflict in enumerate(f.get('conflicts',[])):
  if conflict.get('summary'):person['contact_notes'].append({'title':'Source difference','text':conflict['summary'],'fact_path':f'conflicts.{n}'})
 audit['explicit_court_membership_reviewed']=True
d['coverage_note']='Columbia: six judges (including a named civil-recusal successor), three court officers and the clerk. Missing personal contacts and procedures remain qualified; Court Administration referrals are not personal chambers contacts. A current named senior assignment was not established in the bounded review.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
print('Tenperson draft; omissions are exact duplicate values only.')
for k,v in a.items():print(k,v['omission_reasons'])
