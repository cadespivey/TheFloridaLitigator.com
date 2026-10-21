import json,sqlite3,hashlib
from pathlib import Path
r=Path('runs/county-nassau/2026-10-20/review/directory-8039-astra');d=json.loads((r/'draft.json').read_text());p=json.loads(Path('output/county-review/nassau-8039/packet.json').read_text());a=json.loads((r/'field-audit.json').read_text());facts={e['entity_key']:e['facts'] for e in p['entities']};lookup={v.get('published_identity',k):k for k,v in a.items()};count=0
for person in d['people']:
 key=lookup[person['id']]
 for rows in person['contacts'].values():
  for row in rows:
   if row.get('type')=='note':continue
   v=facts[key]
   for k in row['fact_path'].split('.'):v=v[k]
   value=v if isinstance(v,list) else [v]
   for repair in a[key].get('address_spacing_repairs',[]):
    if repair['fact_path']==row['fact_path']:assert value==repair['original_lines'];value=repair['display_lines']
   assert row['lines']==value,(key,row,value);count+=1
c=sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True);cp=json.loads(Path('runs/county-nassau/2026-10-20/draft/checkpoint-011.json').read_text())
for h,path in cp['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(path).read_bytes()
assert len(list(Path('website/updates').glob('*.json')))==5
out={'people':8,'contact_rows':count,'artifacts_verified':len(cp['artifacts']),'pinned_capture':8039,'stable_snapshot_replacements':7,'new_person':'Deirdre Wallace','chief_disposition':'Existing Duval circuit-chief record preserved; no duplicate Nassau row. Source qualification preserved in research.','remaining_omissions':'Duplicate shared phone/address only for published people; all other source-specific contact fields displayed.'}
(r/'contact-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
