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
slug='pinellas'
d=json.loads(Path(f'website/county-directories/{slug}.json').read_text())
rows=c.execute("""with latest as (select o.entity_key,max(o.capture_seq) seq from finding_observations o join captures c on c.seq=o.capture_seq where c.stream=? group by o.entity_key) select o.entity_key,v.facts,o.citations,o.capture_seq from latest l join finding_observations o on o.entity_key=l.entity_key and o.capture_seq=l.seq join finding_versions v using(version_id)""",(d['stream'],)).fetchall()
records={k:{'facts':json.loads(f),'citations':json.loads(ci),'seq':seq} for k,f,ci,seq in rows}
roster=records['pinellas-roster-discovery']['facts']
expected={p['profile_url'] for p in roster['all_cards'] if p['county_candidate']=='Pinellas'}
assert len(expected)==46 and expected<={p['profile_url'] for p in d['people']}
officers=records['pinellas-roster-phone-reconciliation-and-officer-discovery']['facts']['officer_candidates']
aliases={'Henry Palmer':'Henry T. Palmer'}
expected_officers={aliases.get(p['name'],p['name']) for p in officers}
actual_officers={p['name'] for p in d['people'] if p['kind'] in ['Hearing officer','General magistrate']}
assert len(expected_officers)==8 and expected_officers==actual_officers,(expected_officers,actual_officers)
extras=[p for p in d['people'] if p['profile_url'] not in expected and p['name'] not in actual_officers]
assert {p['name'] for p in extras}=={'Ken Burke','Shawn Crane'}
assert len(d['people'])==56
people=[]
for p in d['people']:
 r=records[p['id']];f=r['facts'];walk(f);walk(r['citations'])
 people.append({'id':p['id'],'name':p['name'],'kind':p['kind'],'capture_seq':r['seq'],'checklist_present':bool(f.get('checklist')),'summary_present':bool(f.get('summary')),'limitations':f.get('limitations',[]),'missing_evidence':f.get('evidence_gaps',[]),'search_log':f.get('search_log'),'procedure_search':f.get('procedure',{}).get('search_log'),'procedure_status':f.get('procedure',{}).get('status'), 'procedure_url':p['procedure_url']})
for p in people:
 if not p['checklist_present'] and p['kind']!='Clerk':
  assert p['procedure_search'] and p['procedure_status'],p['name']
shared={}
for key,r in records.items():
 if key not in {p['id'] for p in d['people']}:
  walk(r['facts']);walk(r['citations']);shared[key]={'capture_seq':r['seq'],'summary':r['facts'].get('summary'),'limitations':r['facts'].get('limitations',[])}
result={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Saved official roster, phone list and officers compared with public directory; 46 location-based judges plus separately reviewed Crane, eight officers and clerk. Existing evidence reused, not a fresh roster claim.','county':'Pinellas','published_people':56,'roster_profiles_matched':46,'officers_matched':8,'officer_name_aliases':aliases,'nested_artifact_hashes_checked':len(cache),'people':people,'shared_records':shared,'source_gaps':records['pinellas-bounded-county-review']['facts']['gaps'],'senior_scope':records['pinellas-county-assignment-reconciliation']['facts']['senior_coverage'],'historical_reports_changed':False}
(out/'pinellas-coverage-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('Pinellas:',len(people),'published records;',len(cache),'hashes; no checklist:',[p['name'] for p in people if not p['checklist_present']])
