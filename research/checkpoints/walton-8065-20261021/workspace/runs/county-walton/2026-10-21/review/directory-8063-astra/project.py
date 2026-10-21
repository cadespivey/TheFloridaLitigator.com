import json,copy,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-walton/2026-10-21/review/directory-8063-astra');r.mkdir(exist_ok=True);p=json.loads(Path('output/county-review/walton-8063/packet.json').read_text());before=copy.deepcopy(p);facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[{'category':'Circuit Courts','group_id':'circuit_first','label':'First Judicial Circuit','url':'https://www.firstjudicialcircuit.org/'},{'category':'County Courts','group_id':'county_walton','label':'Walton','url':'https://www.firstjudicialcircuit.org/legal-professionals/judges/','resources':facts['walton-public-county-resources']['resources']}]
d,a=make_supplement(p,courts);assert p==before;(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n')
for person in d['people']:
 k=person['id'];f=facts[k];audit=a[k];c=f['contact'];person['court_ids']=['county_walton'] if f['role']=='County Judge' else ['circuit_first']
 if f['role']=='Clerk of Circuit Court and Comptroller':person['court_ids']=['county_walton','circuit_first']
 if k in ['walton-chief-john-simon','walton-jan-shackelford']:
  audit['publication_disposition']='Retain existing Escambia chief / Santa Rosa senior entry in First Circuit view; Walton applicability is saved without duplicating same person.';continue
 labels={'contact_note':'Contact scope','hours':'Office hours','branch_contact.address':'South Walton annex address','branch_contact.phone':'South Walton annex phone','branch_contact.fax':'South Walton annex fax'}
 for field,label in labels.items():
  path='contact.'+field
  if path not in audit['omitted_contact_fields'] and not (field.startswith('branch_contact.') and 'branch_contact' in c):continue
  v=c
  for part in field.split('.'):v=v[part]
  row={'label':label,'lines':v if isinstance(v,list) else [v],'fact_path':path}
  if 'address' in field:row['type']='address'
  if field=='contact_note':row['type']='note'
  if field.endswith(('phone','fax')):row['href']='tel:'+re.sub(r'\D','',v)
  person['contacts']['office'].append(row);
  if path in audit['omitted_contact_fields']:audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path)
 if k=='walton-crystal-sconiers':
  # The branch office name is already the address first line; avoid duplicate label data.
  audit['omitted_contact_fields'].remove('contact.branch_contact');audit['omission_reasons'].pop('contact.branch_contact');audit['nested_branch_fields']='Address,phone,fax displayed separately; office name is first address line.'
 if f.get('gaps'):person['contacts']['office'].append({'label':'Contact/procedure gaps','lines':[' '.join(f['gaps'])],'fact_path':'gaps','type':'note'})
 audit['explicit_court_membership_reviewed']=True
# Shared chief and senior already appear in this circuit under prior reviewed observations.
d['people']=[x for x in d['people'] if x['id'] not in ['walton-chief-john-simon','walton-jan-shackelford']]
d['coverage_note']='Walton: four active judges and Clerk Crystal Sconiers. Shared chief and senior remain under existing First Circuit entries. A 2023 magistrate reference does not establish current service; current status remains unconfirmed. The indexed 2026 senior-assignment order body was unavailable in the bounded search. Individual contact gaps and source differences remain recorded. Property-appraiser link is verified by an official referral; destination access was blocked.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('5 entries, county2/circuit4; existing chief/senior retained.')
for k,v in a.items():print(k,v['omitted_contact_fields'])
print(json.dumps(next(x for x in d['people'] if x['id']=='walton-crystal-sconiers')['contacts'],indent=2))
