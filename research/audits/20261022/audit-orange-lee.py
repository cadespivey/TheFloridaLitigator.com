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
for slug in ['orange','lee']:
 cache.clear();texts.clear()
 d=json.loads(Path(f'website/county-directories/{slug}.json').read_text())
 rows=c.execute("""with latest as (select o.entity_key,max(o.capture_seq) seq from finding_observations o join captures c on c.seq=o.capture_seq where c.stream=? group by o.entity_key) select o.entity_key,v.facts,o.citations,o.capture_seq from latest l join finding_observations o on o.entity_key=l.entity_key and o.capture_seq=l.seq join finding_versions v using(version_id)""",(d['stream'],)).fetchall()
 records={k:{'facts':json.loads(f),'citations':json.loads(ci),'seq':seq} for k,f,ci,seq in rows}
 if slug=='orange':
  roster=records['orange-roster-opening']['facts']['roster']['people']
  expected={p['profile_url'] for p in roster if 'orange' in p['county_screens'] and not p.get('unnamed_unit')}
  assert len(expected)==67 and expected<={p['profile_url'] for p in d['people']}
  extras=[p for p in d['people'] if p['profile_url'] not in expected];assert len(extras)==1 and extras[0]['kind']=='Clerk'
  acceptance=records['orange-current-roster-research-review']['facts'];assert len(d['people'])==68
 else:
  roster=records['lee-final-roster-reconciliation']['facts']['rows']
  expected={p['entity_key'] for p in roster if p['disposition']!='vacant_docket_not_person'}
  assert len(expected)==47 and expected<={p['id'] for p in d['people']}
  extras=[p for p in d['people'] if p['id'] not in expected];assert len(extras)==1 and extras[0]['kind']=='Clerk'
  acceptance=records['lee-bounded-county-review']['facts'];assert len(d['people'])==48
 people=[];shared={}
 for p in d['people']:
  r=records[p['id']];f=r['facts'];walk(f);walk(r['citations'])
  people.append({'id':p['id'],'name':p['name'],'kind':p['kind'],'capture_seq':r['seq'],'checklist_present':bool(f.get('checklist')),'summary_present':bool(f.get('summary')),'limitations':f.get('limitations',[]),'procedure_url':p['procedure_url'],'procedure_status':f.get('procedure',{}).get('status'),'procedure_search':f.get('procedure',{}).get('search_log')})
 for key,r in records.items():
  if key not in {p['id'] for p in d['people']}:
   walk(r['facts']);walk(r['citations']);shared[key]={'capture_seq':r['seq'],'summary':r['facts'].get('summary'),'limitations':r['facts'].get('limitations',[])}
 result={'checked_at':datetime.now(timezone.utc).isoformat(),'county':d['county'],'scope':'Saved roster and individual findings reconciled to published identities; source originals and quotations checked. No fresh-assignment or exhaustive legal-review claim.','roster_matches':len(expected),'published_people':len(people),'nested_artifact_hashes_checked':len(cache),'people':people,'shared_records':shared,'acceptance_counts':acceptance['counts'],'gaps':acceptance.get('gaps',acceptance.get('limitations',[]))}
 (out/(slug+'-coverage-audit.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(slug,len(people),'people',len(cache),'hashes; missing checklists:',[(p['name'],p['kind']) for p in people if not p['checklist_present']])
