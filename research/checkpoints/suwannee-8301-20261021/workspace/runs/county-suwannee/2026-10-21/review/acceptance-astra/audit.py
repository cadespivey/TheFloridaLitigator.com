import json,hashlib,sqlite3,re
from pathlib import Path
from flwu.site import build_site
r=Path('runs/county-suwannee/2026-10-21/review/directory-8297-astra');d=json.loads((r/'draft.json').read_text());p=json.loads(Path('output/county-review/suwannee-8297/packet.json').read_text());facts={f['entity_key']:f['facts'] for f in p['entities']};a=json.loads((r/'field-audit.json').read_text());count=0;duplicates=0
def value(f,path):
 for part in path.split('.'):f=f[int(part)] if isinstance(f,list) else f[part]
 return f if isinstance(f,list) else [f]
for person in d['people']:
 f=facts[person['id']];audit=a[person['id']]
 for rows in person['contacts'].values():
  for row in rows:
   expected=value(f,row['fact_path'])
   assert [re.sub(r'\s','',v) for v in row['lines']]==[re.sub(r'\s','',v) for v in expected],(person['name'],row)
   count+=1
 for path in audit['omitted_contact_fields']:
  reason=audit['omission_reasons'][path];assert reason.startswith('Exact same value displayed at ')
  target=reason.removeprefix('Exact same value displayed at ');assert value(f,path)==value(f,target);duplicates+=1
cp=json.loads(Path('runs/county-suwannee/2026-10-21/draft/checkpoint-011.json').read_text())
with sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==8297
 for h,file in cp['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 assert len(c.execute('select * from finalized_reports').fetchall())==5
out={'capture':8297,'supplement_people':9,'contact_rows':count,'duplicate_values_suppressed':duplicates,'artifact_hashes_verified':len(cp['artifacts']),'historical_hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('website/updates').glob('*.json')}}
(r/'contact-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
build_site('website/updates','output/suwannee-8297-preview-v2',preview=True,county_directories=[*sorted(Path('website/county-directories').glob('*.json')),r/'draft.json'])
