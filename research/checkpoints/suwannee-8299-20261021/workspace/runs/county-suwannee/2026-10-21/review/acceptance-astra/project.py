import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-suwannee/2026-10-21/review/directory-8297-astra');r.mkdir(exist_ok=True);p=json.loads(Path('output/county-review/suwannee-8297/packet.json').read_text());before=copy.deepcopy(p);facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[{'category':'Circuit Courts','group_id':'circuit_third','label':'Third Judicial Circuit','url':'https://thirdcircuitfl.org/'},{'category':'County Courts','group_id':'county_suwannee','label':'Suwannee','url':'https://thirdcircuitfl.org/suwannee-county/','resources':facts['suwannee-shared-civil-access-baseline']['county_resource_links']}]
notes={}
for k,indices in {'suwannee-kathryn-land':[0],'suwannee-mark-feagle':[0],'suwannee-melissa-olin':[0],'suwannee-steven-johnson':[0]}.items():
 notes[k]=dict(expected_conflicts_sha256=digest(facts[k]['conflicts']),notes=[dict(conflict_index=i,title='Source difference',text=(facts[k]['conflicts'][i].get('summary') if isinstance(facts[k]['conflicts'][i],dict) else facts[k]['conflicts'][i])) for i in indices])
d,a=make_supplement(p,courts,contact_notes=notes);assert p==before;assert len(d['people'])==9;(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n')
labels={'contact_note':'Contact scope','directory_assistant_email':'Email — circuit directory','directory_fax':'Fax — circuit directory','directory_mailing_address':'Mailing address — circuit directory','directory_address':'Address — circuit directory','administration_phone':'Court Administration referral phone','administration_fax':'Court Administration referral fax','administration_address':'Court Administration referral address','civil_case_manager_name':'Civil case manager','civil_case_manager_email':'Civil case manager email','civil_case_manager_phone':'Civil case manager phone','civil_case_manager_address':'Civil case manager address','general_phone':'Main office phone','civil_supervisor_name':'Civil and records supervisor','civil_supervisor_phone':'Civil and records supervisor phone','official_records_phone':'Official Records phone','probate_phone':'Probate phone','appeals_phone':'Appeals phone','hours':'Office hours','directory_address_lines':'Address — circuit directory','circuit_civil_phone':'Circuit civil phone','county_civil_phone':'County civil phone','recording_phone':'Recording phone'}
for person in d['people']:
 k=person['id'];f=facts[k];c=f['contact'];audit=a[k]
 person['court_ids']=['county_suwannee'] if k=='suwannee-darren-jackson' else ['circuit_third']
 if k=='suwannee-jennifer-griffin':person['court_ids']=['county_suwannee','circuit_third']
 if person['kind']=='Clerk':person['court_ids']=['county_suwannee','circuit_third']
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
   if k in {'suwannee-christina-seifert','suwannee-steven-johnson'} and key=='office_phone':row['label']='Court Administration phone'
   if k in {'suwannee-christina-seifert','suwannee-steven-johnson'} and key=='fax':row['label']='Court Administration fax'
   if k=='suwannee-christina-seifert' and key=='email':row['label']='Probate proposed orders email'
   if k=='suwannee-clerk-barry-baker' and key=='email':row['label']='Public records email'
   if len(row['lines'])==1 and re.fullmatch(r'\d{3}-\d{3}-\d{4}',row['lines'][0]):row['href']='tel:'+re.sub(r'\D','',row['lines'][0])
 for rows in person['contacts'].values():
  for row in rows:
   if 'fax' in row['fact_path'] or (k=='suwannee-mark-feagle' and 'email' in row['fact_path']):row.pop('href',None)
 if k=='suwannee-christina-seifert':
  order=['contact.office_phone','contact.email','contact.fax','contact.mailing_address','contact.civil_case_manager_name','contact.civil_case_manager_phone','contact.civil_case_manager_email','contact.civil_case_manager_address','contact.contact_note']
  person['contacts']['office'].sort(key=lambda row:order.index(row['fact_path']))
 if k=='suwannee-clerk-barry-baker':
  order=['contact.office_phone','contact.circuit_civil_phone','contact.county_civil_phone','contact.recording_phone','contact.email','contact.fax','contact.mailing_address','contact.contact_note']
  person['contacts']['office'].sort(key=lambda row:order.index(row['fact_path']))
 audit['explicit_court_membership_reviewed']=True
d['coverage_note']='Suwannee: six judge records, two court officers and the clerk. Douglas is included by the county-tag roster without a confirmed routine Suwannee assignment; Jackson is a named county recusal successor. Shared administration contacts and missing personal procedures remain qualified. Court records are not online according to the clerk; the Court Records link provides official access guidance.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
print('Nine-person draft; omissions are exact duplicate values only.')
for k,v in a.items():print(k,v['omission_reasons'])
