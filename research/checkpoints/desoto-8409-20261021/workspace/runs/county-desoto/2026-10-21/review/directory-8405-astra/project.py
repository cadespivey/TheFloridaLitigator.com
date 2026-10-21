import json
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
r=Path('runs/county-desoto/2026-10-21/review/directory-8405-astra');r.mkdir(exist_ok=True)
p=json.load(open('output/county-review/desoto-8405/packet.json'));facts={e['entity_key']:e['facts'] for e in p['entities']}
courts=[dict(category='Circuit Courts',group_id='circuit_twelfth',label='Twelfth Judicial Circuit',url='https://www.jud12.flcourts.org/'),dict(category='County Courts',group_id='county_desoto',label='DeSoto',url='https://jud12.flcourts.org/About/Courthouses/Desoto-County-Courthouse',resources=facts['desoto-resources-access-roster']['resources'])]
notes={}
for k,indices in [('desoto-diana-moreland',[0]),('desoto-medisa-turner',[0,2])]:
 f=facts[k];notes[k]=dict(expected_conflicts_sha256=digest(f['conflicts']),notes=[dict(conflict_index=i,title='Source difference',text=f['conflicts'][i]['summary'] if isinstance(f['conflicts'][i],dict) else f['conflicts'][i]) for i in indices])
d,a=make_supplement(p,courts,contact_notes=notes);assert len(d['people'])==12
for person in d['people']:
 k=person['id'];f=facts[k];audit=a[k]
 person['court_ids']=['county_desoto'] if k in ['desoto-parker-hall','desoto-matthew-peters'] else ['circuit_twelfth']
 if k=='desoto-nadia-daughtrey':person['court_ids']=['county_desoto','circuit_twelfth']
 for path in list(audit['omitted_contact_fields']):
  container,key=path.split('.');v=f[container][key]
  if v is None:continue
  lines=v if isinstance(v,list) else [v]
  existing=next((row for rows in person['contacts'].values() for row in rows if row['lines']==lines),None)
  if existing:audit['omission_reasons'][path]='Exact same value displayed at '+existing['fact_path'];continue
  row=dict(label=key.replace('_',' ').capitalize(),lines=lines,fact_path=path,type='note')
  person['contacts']['assistant' if 'assistant' in key else 'office'].append(row);audit['omitted_contact_fields'].remove(path);audit['omission_reasons'].pop(path,None)
 for rows in person['contacts'].values():
  for row in rows:
   key=row['fact_path'].split('.')[-1]
   if 'fax' in key or key in ['profile_phone_link_target','cancellation_link_email','resume_email_note','division_email']:
    row.pop('href',None)
   if key=='division_email':row['label']='Manatee Division 3 orders email (not a DeSoto filing address)'
   if key in ['profile_phone_link_target','cancellation_link_email']:row['type']='note'
 audit['explicit_court_membership_reviewed']=True
 person['dates']=f.get('stated_dates')
d['coverage_note']='DeSoto: twelve personnel, including shared circuit administrators and officers with qualified county assignments. Current county judge and historical assignment differences remain preserved; shared roles do not imply regular county trial assignments.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(r/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'field-audit.json').write_text(json.dumps(a,indent=2)+'\n')
(r/'project.py').write_text(Path('/tmp/project-desoto.py').read_text())
for x in d['people']:print(x['id'],x['court_ids'],a[x['id']]['omitted_contact_fields'])
