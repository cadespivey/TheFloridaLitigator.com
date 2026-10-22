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
for slug in (sys.argv[1:] or ['hillsborough','miami-dade']):
 cache.clear();texts.clear()
 d=json.loads(Path(f'website/county-directories/{slug}.json').read_text());rows=c.execute('''with latest as (select o.entity_key,max(o.capture_seq) capture_seq from finding_observations o join captures c on c.seq=o.capture_seq where c.stream=? group by o.entity_key) select o.entity_key,v.kind,v.facts,o.citations,o.capture_seq from latest l join finding_observations o on o.entity_key=l.entity_key and o.capture_seq=l.capture_seq join finding_versions v using(version_id)''',(d['stream'],)).fetchall();records={k:{'kind':kind,'facts':json.loads(f),'citations':json.loads(ci),'seq':seq} for k,kind,f,ci,seq in rows};opening=records[slug+'-roster-opening']['facts'];acceptance=records[slug+'-county-research-acceptance-20261018']['facts'];people=[];scope_records={}
 if slug=='hillsborough':
  expected={p['profile_url'] for p in opening['people']};actual={p['profile_url'] for p in d['people']};assert len(expected)==69 and expected<=actual;expected_count=85
 elif slug=='palm-beach':
  roster=records['palm-beach-roster-reconciliation']['facts'];walk(roster);walk(records['palm-beach-roster-reconciliation']['citations'])
  aliases={'Lourdes Casanova':'Lourdes Maria Casanova','Howard Coates, Jr.':'Howard K. Coates, Jr.'}
  for name in aliases.values():
   person=next(p for p in d['people'] if p['name']==name);facts=records[person['id']]['facts']
   assert facts['name']==name and any(name in citation['quote'] for citation in facts['identity_citations'])
   walk(facts['identity_citations'])
  expected={aliases.get(' '.join(p['name'].split()),' '.join(p['name'].split())) for p in roster['people']};actual={p['name'] for p in d['people']}
  assert len(expected)==80 and expected<=actual
  assert actual-expected=={'Division AA — shared judicial office','Karina Rodriguez-Matzen','Shannon Ramsey-Chessman'};expected_count=83
 else:
  expected={str(p['judge_id']) for p in opening['people']};actual=set();senior_matches=[]
  roster={str(p['judge_id']):p for p in opening['people']}
  for p in d['people']:
   profile_id=parse_qs(urlparse(p['profile_url'] or '').query).get('judgeid',[''])[0]
   if profile_id:actual.add(profile_id);continue
   if p['kind']=='Clerk':continue
   f=records[p['id']]['facts'];cards=f['roster_cards_reviewed']
   assert f['name']==p['name'] and f['profile_url']==p['profile_url']
   assert len(cards)==1 and cards[0]['division']=='Active Senior Judges'
   card=cards[0];judge_id=str(card['judge_id'])
   assert card['printed_name'] in roster[judge_id]['names']
   assert any(card['printed_name'] in citation['quote'] for citation in f['identity_citations'])
   walk(f['identity_citations']);assert judge_id not in actual
   actual.add(judge_id);senior_matches.append({'name':p['name'],'judge_id':judge_id,'printed_name':card['printed_name'],'profile_url':p['profile_url']})
  assert len(senior_matches)==11 and len(expected)==153 and expected==actual;expected_count=154
 assert len(d['people'])==expected_count
 for p in d['people']:
  rec=records[p['id']];f=rec['facts'];walk(f);walk(rec['citations']);people.append({'id':p['id'],'name':p['name'],'kind':p['kind'],'capture_seq':rec['seq'],'checklist_present':bool(f.get('checklist')),'summary_present':bool(f.get('summary')),'procedure_url':p['procedure_url'],'next_actions':f.get('next_actions',[]),'evidence_limitations':f.get('evidence_limitations',[]),'bounded_search_status':f.get('bounded_search_status'),'review_limits':f.get('review_limits'),'search_log':f.get('search_log') if not f.get('checklist') else None})
 for keys in acceptance.get('coverage_matrix',{}).values():
  for key in keys:
   if key in records:walk(records[key]['facts']);walk(records[key]['citations']);scope_records[key]=records[key]['seq']
 result={'checked_at':datetime.now(timezone.utc).isoformat(),'county':d['county'],'scope':'Saved official roster profile URLs/IDs compared to published identities and latest individual findings; existing scoped reviews reused. No fresh acquisition or new legal interpretation.','matched_roster_profiles':len(expected),'published_people':len(people),'acceptance_counts':acceptance['counts'],'source_gaps':acceptance.get('gaps',acceptance.get('source_gap_disposition',[])),'people':people,'shared_coverage_records':scope_records,'missing_shared_record_references':[key for keys in acceptance.get('coverage_matrix',{}).values() for key in keys if key not in records],'cumulative_nested_artifact_hashes_checked':len(cache)};assert not result['missing_shared_record_references'];
 if slug=='miami-dade':result['shared_url_senior_identity_matches']=senior_matches
 if slug=='palm-beach':
  result['roster_name_aliases']=aliases
  result['match_method']='80 roster names, whitespace normalized; two full names verified through individual identity quotations; three named service/office additions. Senior contact/procedure gaps remain explicit.'
  seniors=[p for p in people if p['kind']=='Senior judge'];assert len(seniors)==8
  assert all(p['bounded_search_status'] and p['search_log'] for p in seniors)
 (out/(slug+'-coverage-audit.json')).write_text(json.dumps(result,indent=2)+'\n');print(slug,len(expected),'roster profiles',len(people),'published identities','missing checklist',[(p['name'],p['kind']) for p in people if not p['checklist_present']],'hashes cumulative',len(cache))
