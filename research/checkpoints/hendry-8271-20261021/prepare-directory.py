import json
from pathlib import Path
from flwu.county_review import export_review
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
run=Path('runs/county-hendry/2026-10-21');r=run/'review/directory-8271-astra';r.mkdir(exist_ok=True)
export_review('/Users/cadespivey/.local/share/flwu/research-history.sqlite','manual_research:county-baseline-v1:e675ddd5a9a7',8271,'output/county-review/hendry-8271')
p=json.loads(Path('output/county-review/hendry-8271/packet.json').read_text());f=next(e['facts'] for e in p['entities'] if e['entity_key']=='hendry-shared-civil-access-resources')
courts=[dict(category='Circuit Courts',group_id='circuit_twentieth',label='Twentieth Judicial Circuit',url='https://www.ca.cjis20.org/'),dict(category='County Courts',group_id='county_hendry',label='Hendry',url='https://www.ca.cjis20.org/About-The-Court/Court-Schedules/hendryschedules.aspx/1000',resources=[{k:x[k] for k in ['label','url']} for x in f['resources']])]
notes={}
for e in p['entities']:
 if e['entity_key']=='hendry-clerk-kimberley-barrineau':indices=[0]
 elif e['entity_key']=='hendry-matthew-henry':indices=[0,1]
 elif e['entity_key']=='hendry-howard-atkin':indices=[0]
 else:continue
 notes[e['entity_key']]=dict(expected_conflicts_sha256=digest(e['facts']['conflicts']),notes=[dict(conflict_index=i,title='Source qualification',text=e['facts']['conflicts'][i]) for i in indices])
d,a=make_supplement(p,courts,contact_notes=notes);(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n');members=[]
for person in d['people']:
 key=person['id'];ef=next(e['facts'] for e in p['entities'] if e['entity_key']==key)
 if key in ['hendry-randy-merrill','hendry-theodore-walters','hendry-edward-larsen']:ids=['county_hendry']
 elif key in ['hendry-darrell-hill','hendry-kenneth-thompson','hendry-matthew-henry','hendry-howard-atkin']:ids=['circuit_twentieth']
 else:ids=['circuit_twentieth','county_hendry']
 person['court_ids']=ids;members.append(dict(id=key,court_ids=ids,source_facts_sha256=digest(ef),basis=ef.get('assignment','Clerk serves both circuit and county courts.')))
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d,preview=True)
for name,obj in [('draft',d),('field-audit',a),('court-membership',members)]: (r/(name+'.json')).write_text(json.dumps(obj,indent=2)+'\n')
print('PEOPLE',len(d['people']));print([(x['id'],x['kind'],x['court_ids']) for x in d['people']]);print('OMITTED',json.dumps({k:v.get('omitted_contact_fields') for k,v in a.items()}))
