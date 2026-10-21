import json,sqlite3,hashlib
from pathlib import Path
from flwu.history import now
r=Path('runs/county-martin/2026-10-20/review/schwab-astra');p=json.loads(Path('runs/county-indian-river/2026-10-20/review/schwab-astra/reviewed-person.json').read_text());p['key']='martin-charles-schwab';f=p['facts'];f['county']='martin';f['reviewed_at']=now();f['assignment']=f['assignment'].replace('Indian River','Martin');f['gaps']=[x.replace('Indian River','Martin') for x in f['gaps']];f['reuse'].update(prior_entity='indian-river-charles-schwab',prior_checkpoint=7797)
with sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True) as db:
 for c in p['citations']:
  for field in ['sha256','text_sha256']:
   h=c[field];b=db.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0];assert hashlib.sha256(b).hexdigest()==h;(r/(h+('.txt' if field=='text_sha256' else '.bin'))).write_bytes(b)
(r/'reviewed-person.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r.parent/'presley-astra/save.py').read_text().replace('review/presley-astra','review/schwab-astra').replace("p=json.loads((run/'draft/checkpoint-012.json')","p=json.loads((run/'draft/checkpoint-013.json')").replace("path=run/'draft/checkpoint-013.json'","path=run/'draft/checkpoint-014.json'").replace('martin-presley-astra-20261020','martin-schwab-astra-20261020').replace('==7881','==7883').replace("['Kameisha Presley']","['Charles A. Schwab']").replace("name!='Kameisha Presley'","name!='Charles A. Schwab'").replace('Reconcile successors, chief/seniors and assignment sources, then clerk/shared operations.','Reconcile successors, seniors and assignment sources, then clerk/shared operations.');(r/'save.py').write_text(s)
