import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-monroe/2026-10-21/review/directory-8097-astra');p=json.loads(Path('output/county-review/monroe-8097/packet.json').read_text());before=copy.deepcopy(p);facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[{'category':'Circuit Courts','group_id':'circuit_sixteenth','label':'Sixteenth Judicial Circuit','url':'https://keyscourts.net/'},{'category':'County Courts','group_id':'county_monroe','label':'Monroe','url':'https://keyscourts.net/judges-of-the-16th-circuit/','resources':facts['monroe-shared-access']['county_resource_links']}]
d,a=make_supplement(p,courts);assert p==before;(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n')
def add(person,label,value,path,kind=None):
 row={'label':label,'lines':value if isinstance(value,list) else [value],'fact_path':path}
 if kind:row['type']=kind
 if isinstance(value,str):
  if '@' in value and ' ' not in value:row['href']='mailto:'+value
  elif re.fullmatch(r'[\d()-]+',value):row['href']='tel:'+re.sub(r'\D','',value)
 person['contacts']['office'].append(row)
for person in d['people']:
 k=person['id'];f=facts[k];c=f['contact'];audit=a[k]
 person['court_ids']=['county_monroe'] if f['role']=='County Judge' else ['circuit_sixteenth']
 if f['role']=='Clerk of Circuit Court and Comptroller':person['court_ids']=['county_monroe','circuit_sixteenth']
 if f.get('assignment_order_statement'):
  st=f['assignment_order_statement'];person['assignment']=f['assignment']+' Dated assignment order: '+st['summary']+' '+st['stated_effective_period']+'.'
 person['dates']=f.get('stated_dates')
 for path in list(audit['omitted_contact_fields']):
  key=path.split('.',1)[1];value=c[key]
  if key=='case_managers':
   for n,manager in enumerate(value):
    prefix=manager['role']+' — '+', '.join(manager['locations'])
    for field in ['name','email','phone']:add(person,prefix+' '+field,manager[field],f'contact.case_managers.{n}.{field}')
  elif key=='branch_contacts':
   for n,branch in enumerate(value):
    for field in ['address','phone','fax']:add(person,branch['office']+' '+field,branch[field],f'contact.branch_contacts.{n}.{field}','address' if field=='address' else None)
  elif isinstance(value,(str,list)):
   label={'contact_note':'Contact scope','alternative_communication_phone':'Alternative phone — see contact scope','hours':'Office hours'}.get(key,key.replace('_',' ').capitalize())
   add(person,label,value,path,'note' if key=='contact_note' else None)
  else:continue
  audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 if f.get('conflicts'):
  for n,conflict in enumerate(f['conflicts']):
   if isinstance(conflict,dict) and conflict.get('summary'):person['contact_notes'].append({'title':'Source difference','text':conflict['summary'],'fact_path':f'conflicts.{n}'})
 # Gap notes remain evidence-qualified without internal workflow narration.
 gaps=[g for g in f.get('gaps',[]) if not any(w in g for w in ['pending','remains county','remains shared','Tax Assessor','Records endpoint'])]
 if gaps:add(person,'Published-information gaps',' '.join(gaps),'gaps','note')
 audit['explicit_court_membership_reviewed']=True
 audit['assignment_projection']='Profile plus separate dated order statement where available; no authority resolution.'
d['coverage_note']='Monroe: eight active judges, General Magistrate Holly Aliprandi and Clerk Kevin Madok. The court overview mentions senior judges and a child-support hearing officer without current names established in the reviewed roster and assignment sources. Case managers retain their published roles. Source discrepancies remain recorded. Property-appraiser link is verified through county government; destination access returned403.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
print('people',len(d['people']))
for k,v in a.items():print(k,v['omitted_contact_fields'])
