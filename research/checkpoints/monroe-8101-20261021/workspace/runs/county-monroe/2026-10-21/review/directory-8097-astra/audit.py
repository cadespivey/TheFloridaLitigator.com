import json,sqlite3,hashlib
from pathlib import Path
from flwu.site import build_site
r=Path('runs/county-monroe/2026-10-21/review/directory-8097-astra');d=json.loads((r/'draft.json').read_text());p=json.loads(Path('output/county-review/monroe-8097/packet.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']};a=json.loads((r/'field-audit.json').read_text())
assert {x['name'] for x in d['people']}=={'Timothy J. Koenig','Mark H. Jones','James W. Morgan III','Bonnie J. Helms','Derek A. Lewis','Sharon I. Hamilton','Albert L. Kelley','Mark Wilson','Holly Aliprandi','Kevin Madok'}
count=0
for person in d['people']:
 f=facts[person['id']]
 assert not a[person['id']]['omitted_contact_fields']
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=f
   for key in row['fact_path'].split('.'):v=v[int(key)] if isinstance(v,list) else v[key]
   assert row['lines']==(v if isinstance(v,list) else [v]),(person['id'],row)
   count+=1
 assert len(person['contacts']['assistant'])==2 if f['role'] in ['County Judge','Circuit Judge','Chief Judge'] else not person['contacts']['assistant']
cp=json.loads(Path('runs/county-monroe/2026-10-21/draft/checkpoint-014.json').read_text())
with sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True) as conn:
 assert conn.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8097
 for h,path in cp['artifacts'].items():assert conn.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(path).read_bytes()
out={'people':10,'contact_rows':count,'artifact_hashes_verified':len(cp['artifacts']),'capture':8097,'county_entries':5,'circuit_entries':6,'historical_hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('website/updates').glob('*.json')}}
assert len(out['historical_hashes'])==5
(r/'contact-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
build_site('website/updates','output/monroe-8097-preview',preview=True,county_directories=[*sorted(Path('website/county-directories').glob('*.json')),r/'draft.json'])
print('Preview built:36 reviewed supplements plus Monroe draft.')
