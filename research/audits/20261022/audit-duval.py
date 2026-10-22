import sqlite3,json,hashlib,sys
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from datetime import datetime,timezone
c=sqlite3.connect('file:/Users/cadespivey/.local/share/flwu/research-history.sqlite?mode=ro',uri=True);cache=set();texts={};out=Path('runs/statewide-completion-audit/2026-10-22')
def walk(v):
 if isinstance(v,dict):
  if all(k in v for k in ['sha256','text_sha256','quote','url']):
   for k in ['sha256','text_sha256']:
    h=v[k]
    if h not in cache:
     b=c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone();assert b and hashlib.sha256(b[0]).hexdigest()==h;cache.add(h)
     if k=='text_sha256':texts[h]=b[0].decode()
   if v['text_sha256'] not in texts:texts[v['text_sha256']]=c.execute('select bytes from artifacts where sha256=?',(v['text_sha256'],)).fetchone()[0].decode()
   assert v['quote'] in texts[v['text_sha256']],v['url']
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
import re
d=json.loads(Path('website/county-directories/duval.json').read_text())
report=Path('website/updates/update-d8e4f025e85cf8325f15.json')
original=[p for p in json.loads(report.read_text())['directory'] if 'Duval' in p['counties']]
assert len(original)==47 and len(d['people'])==13
assert not {p['id'] for p in original}&{p['id'] for p in d['people']}
def latest(key,stream=None):
 sql='select v.facts,o.citations,o.capture_seq from finding_observations o join finding_versions v using(version_id) join captures c on c.seq=o.capture_seq where o.entity_key=?'
 args=[key]
 if stream:sql+=' and c.stream=?';args.append(stream)
 row=c.execute(sql+' order by o.capture_seq desc limit 1',args).fetchone();assert row,key
 return json.loads(row[0]),json.loads(row[1]),row[2]
f,ci,seq=latest('duval-roster-comparison',d['stream']);walk(f);walk(ci)
norm=lambda s:re.sub('[^A-Z]','',s.upper())
roster={norm(x['cells'][1]) for x in f['rows']};names={norm(p['name']) for p in original if p['kind']!='clerk'}
assert len(roster)==46 and roster==names
people=[]
for p in original+d['people']:
 f,ci,seq=latest(p['id'],d['stream'] if p in d['people'] else None);walk(f);walk(ci)
 proc=f.get('procedure',{})
 people.append({'id':p['id'],'name':p['name'],'kind':p['kind'],'capture_seq':seq,'origin':'original_report' if p in original else 'county_supplement','fields':{k:v.get('status') for k,v in f.get('fields',{}).items()},'procedure_status':proc.get('status'),'procedure_keys':list(proc),'checklist_present':bool(f.get('checklist') or proc.get('checklist')),'limitations':f.get('limitations',[])})
acceptance,ci,seq=latest('duval-bounded-county-review',d['stream']);walk(acceptance);walk(ci)
result={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Saved 46-row official judge roster reconciled with original report directory, plus13 reviewed county supplement officers and existing clerk. Original records retain earlier evidence dates.','county':'Duval','original_people':47,'supplement_people':13,'combined_people':60,'nested_artifact_hashes_checked':len(cache),'people':people,'source_gaps':acceptance['gaps'],'original_report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'remaining_review':'Presence of structured practical summaries in older baseline records requires separate check; roster/hash reconciliation alone is not substantive completeness.'}
(out/'duval-coverage-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('Duval60 combined records;',len(cache),'hashes; checklist',sum(p['checklist_present'] for p in people))
