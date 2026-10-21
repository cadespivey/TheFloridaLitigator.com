import json,re
from pathlib import Path
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
p=Path(__file__).parent;packet=json.loads(Path('output/county-review/citrus-7853/packet.json').read_text());initial=json.loads((p/'initial-draft.json').read_text());d,audit=make_supplement(packet,initial['courts']);facts={e['entity_key']:e['facts'] for e in packet['entities']}
for person in d['people']:
 f=facts[person['id']];c=f['contact'];a=audit[person['id']];role=f['role'];person['court_ids']=['county_citrus'] if role=='County Judge' else ['circuit_fifth']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['circuit_fifth','county_citrus']
 def add(field,label,kind=None):
  v=c[field];row=dict(label=label,lines=v if isinstance(v,list) else [v],fact_path='contact.'+field)
  if kind:row['type']=kind
  if field in ['directory_phone','tdd']:row['href']='tel:'+re.sub(r'\D','',v)
  if field in ['contact_form','public_records_portal']:row.update(lines=['Available through the linked official contact page.'],type='note')
  person['contacts']['office'].append(row);path='contact.'+field
  if path in a['omitted_contact_fields']:a['omitted_contact_fields'].remove(path);a['omission_reasons'].pop(path)
 for field,label,kind in [('directory_phone','Phone — circuit directory',None),('administration_fax','Administration fax',None),('branch_address','Branch office','address'),('hours','Hours',None),('phone_extension','Civil phone routing',None),('tdd','TDD',None),('contact_form','General inquiry form',None),('public_records_portal','Public records and general inquiries',None)]:
  if c.get(field):add(field,label,kind)
 for row in person['contacts']['assistant']:
  if row['fact_path']=='contact.assistant_phone':row['label']='Shared office phone — officer page' if 'schenck' in person['id'] else 'Shared office phone'
 for row in person['contacts']['office']:
  if row['fact_path']=='contact.email':row['label']='Orders / materials email'
  if row['fact_path']=='contact.fax' and role=='Clerk of Circuit Court and Comptroller':row['label']='Civil fax'
 if c.get('assistant_role') and not any(r['fact_path']=='contact.assistant_role' for r in person['contacts']['assistant']):person['contacts']['assistant'].append(dict(label='Staff role',lines=[c['assistant_role']],fact_path='contact.assistant_role'))
 if c.get('assistant_email') is None and role!='Clerk of Circuit Court and Comptroller':person['contacts']['assistant'].append(dict(label='Email',lines=['Not established in reviewed official sources.'],fact_path='contact.assistant_email',type='note'))
 if 'office_address' in c and c['office_address'] is None:person['contacts']['office'].append(dict(label='Address',lines=['Not established in reviewed official sources.'],fact_path='contact.office_address',type='note'))
 if 'fax' in c and c['fax'] is None:person['contacts']['office'].append(dict(label='Fax',lines=['Not published in reviewed profile/roster.'],fact_path='contact.fax',type='note'))
 if role=='Clerk of Circuit Court and Comptroller':person['contacts']['office'].append(dict(label='Email / filing',lines=['No general email published; inquiry forms and fax are not established filing channels.'],fact_path='contact.contact_note',type='note'))
 for i,conflict in enumerate(person['conflicts']):
  if any(word in conflict.get('subject','').lower() for word in ['name','phone','assistant','title','spelling']):person['contact_notes'].append(dict(title=conflict['subject'],text='; '.join(conflict['statements'])+'. Source differences retained.',fact_path=f'conflicts.{i}'))
 a['explicit_membership_reviewed']=True;a['contact_note_disposition']='Shared numbers labeled; source-specific phone/staff-role/contact-route differences displayed. Null contact gaps explicit. Narrative review context retained in evidence.'
d['courts'][1]['resources']=facts['citrus-traci-perry']['county_resource_links']
d['coverage_note']='Citrus baseline: seven resident judges, two judicial officers, the clerk and circuit-wide chief. Email/address gaps for officers, Thomas assistant email and Lambert fax remain explicit. No current named senior assignment was established in the bounded review; older appointment/backlog references do not establish current service. Source conflicts are retained without choosing controlling authority.'
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
(p/'draft.json').write_text(json.dumps(d,indent=2)+'\n');(p/'field-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('Pending supplement validated:',len(d['people']),'people; county members',sum('county_citrus' in x['court_ids'] for x in d['people']))
