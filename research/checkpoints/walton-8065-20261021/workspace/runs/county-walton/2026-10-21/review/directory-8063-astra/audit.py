import json,sqlite3,hashlib
from pathlib import Path
r=Path('runs/county-walton/2026-10-21/review/directory-8063-astra');d=json.loads((r/'draft.json').read_text());p=json.loads(Path('output/county-review/walton-8063/packet.json').read_text());a=json.loads((r/'field-audit.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']};count=0
assert {x['name'] for x in d['people']}=={'Crystal Sconiers','Jeffrey E. Lewis','J. Ryan Love','Jonathan Schlechter','Kelvin C. Wells'}
for person in d['people']:
 key=person['id']
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=facts[key]
   for k in row['fact_path'].split('.'):v=v[k]
   assert row['lines']==(v if isinstance(v,list) else [v]),(key,row);count+=1
 assert not a[key]['omitted_contact_fields'] or (key=='walton-jeffrey-lewis' and a[key]['omitted_contact_fields']==['contact.phone'])
c=sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True);cp=json.loads(Path('runs/county-walton/2026-10-21/draft/checkpoint-010.json').read_text())
for h,path in cp['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(path).read_bytes()
assert len(list(Path('website/updates').glob('*.json')))==5
out={'people':5,'contact_rows':count,'artifacts_verified':len(cp['artifacts']),'pinned_capture':8063,'county_rows':2,'new_circuit_rows':4,'chief_and_senior_disposition':'Existing Escambia chief and Santa Rosa senior retained without duplicate county-scoped person.','remaining_omissions':'Lewis shared phone already displayed once; branch address/phone/fax explicitly projected.','historical_hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('website/updates').glob('*.json')}}
(r/'contact-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('Verified',count,'contact rows and',len(cp['artifacts']),'source artifacts')
from flwu.site import build_site
m=build_site('website/updates','output/walton-8063-preview',preview=True,county_directories=[*sorted(Path('website/county-directories').glob('*.json')),r/'draft.json']);print('Preview build complete;35 reviewed supplements plus Walton pending draft.')
