import json,hashlib,sqlite3,re
from pathlib import Path
from flwu.site import build_site
r=Path('runs/county-putnam/2026-10-21/review/directory-8131-astra');d=json.loads((r/'draft.json').read_text());p=json.loads(Path('output/county-review/putnam-8131/packet.json').read_text());facts={f['entity_key']:f['facts'] for f in p['entities']};mapping={f.get('prior_baseline_id',k):k for k,f in facts.items()};a=json.loads((r/'field-audit.json').read_text());count=0
for person in d['people']:
 key=mapping.get(person['id'],person['id']);f=facts[key];assert not a[key]['omitted_contact_fields']
 for rows in person['contacts'].values():
  for row in rows:
   value=f
   for part in row['fact_path'].split('.'):value=value[int(part)] if isinstance(value,list) else value[part]
   expected=value if isinstance(value,list) else [value]
   if row.get('type')=='address':assert [re.sub(r'\s','',v) for v in row['lines']]==[re.sub(r'\s','',v) for v in expected],(person['name'],row)
   else:assert row['lines']==expected,(person['name'],row)
   count+=1
cp=json.loads(Path('runs/county-putnam/2026-10-21/draft/checkpoint-014.json').read_text())
with sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True) as conn:
 assert conn.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8131
 for h,f in cp['artifacts'].items():assert conn.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(f).read_bytes()
issues=[json.loads(f.read_text()) for f in Path('website/updates').glob('*.json')];latest=max(issues,key=lambda i:i['published_at']);old={x['id']:x for x in latest['directory']}
for person in d['people']:
 if person['id'] in old:assert old[person['id']]['counties']==['Putnam'] and old[person['id']]['name']==person['name']
shared={f['prior_baseline_id']:f for k,f in facts.items() if k in ['putnam-chief-leah-case','putnam-dennis-craig','putnam-howard-mcgillin']}
for id,f in shared.items():assert old[id]['name']==f['name'] and set(old[id]['counties'])=={'Putnam','St. Johns'}
out={'capture':8131,'supplement_people':8,'shared_existing_people':3,'contact_rows':count,'artifact_hashes_verified':len(cp['artifacts']),'historical_hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('website/updates').glob('*.json')},'shared_record_comparison':{id:{'saved_contact':f['contact'],'existing_details':old[id]['details']} for id,f in shared.items()}}
(r/'contact-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('Verified',count,'contact rows,',len(cp['artifacts']),'artifacts and stable identities.')
build_site('website/updates','output/putnam-8131-refined-preview',preview=True,county_directories=[*sorted(Path('website/county-directories').glob('*.json')),r/'draft.json'])
