import json,hashlib,sqlite3,tempfile
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from flwu.baseline_capture import save_checkpoint,history
R=Path('runs/county-santa-rosa/2026-10-19');D=R/'review/roster';assert not (R/'state.json').exists();r=json.JSONDecoder().raw_decode((D/'judges-response.txt').read_text().split('### Result\n')[1])[0];artifacts={}
def put(b,suffix,folder):
 h=hashlib.sha256(b).hexdigest();p=R/folder/(h+suffix);p.write_bytes(b);artifacts[h]=str(p);return h,str(p)
h,path=put(r['html'].encode(),'.html','raw');dh,dp=put(r['dom'].encode(),'.html','raw');th,tp=put(r['text'].encode(),'.txt','text');a=dict(url=r['url'],http_status=r['http_status'],retrieved_at=r['retrieved_at'],sha256=h,path=path,text_sha256=th,text_path=tp,authority='official',synthetic=False,quote='Santa Rosa County',locator='Rendered county roster; original HTML plus rendered DOM retained');assert a['quote'] in r['text'];s=BeautifulSoup(r['dom'],'html.parser');people=[];collecting=False
for x in s.select('a[href]'):
 if '/judges/' in x['href'] and x['href'].rstrip('/')!='/legal-professionals/judges':
  name=x.get_text(' ',strip=True).removesuffix(' Learn More');
  if name=='Jeffrey E. Lewis':break
  if name=='Darlene F. Dickey':collecting=True
  if not collecting:continue
  people.append(dict(name=name,url=urljoin(r['url'],x['href'])))
assert len(people)==8;scope=dict(profile='county-baseline-v1',county='santa_rosa',circuit=1);stream='manual_research:county-baseline-v1:'+history.sha(scope)[:12];db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite');now=datetime.now(timezone.utc).isoformat();base=json.loads(Path('runs/county-st-lucie/2026-10-19/draft/checkpoint-001.json').read_text());contract=dict(base['payload']['contract'],scope=scope,stream=stream,created_at=now)
f=dict(key='santa_rosa-initial-roster',kind='source_review',facts=dict(county='santa_rosa',circuit=1,reviewed_at=now,title='Initial official Santa Rosa judge roster',people=people,review_scope='County roster identification only; individual contact/procedure reviews pending.',limitations=['Magistrates/hearing officers and senior/assignment reconciliation remain.','Rendered site content differs from response HTML; both retained with rendered text. Reused circuit-wide source originally retrieved for Escambia; original retrieval timestamp preserved.']),citations=[a]);packet=dict(scope=scope,stream=stream,run_id='santa_rosa-roster-20261019',payload=dict(status='incomplete',contract=contract,checks=[dict(id='county-roster',status='incomplete')],drafts=[],findings=[f]),artifacts=artifacts)
(D/'roster-acquisition.json').write_text(json.dumps(a,indent=2));(D/'candidates.json').write_text(json.dumps(people,indent=2));put((D/'candidates.json').read_bytes(),'.json','raw');put(Path(__file__).read_bytes(),'.py','raw');p=R/'draft/checkpoint-001.json';p.write_text(json.dumps(packet,indent=2)+'\n')
with tempfile.TemporaryDirectory() as t:save_checkpoint(Path.cwd(),p,Path(t)/'trial.sqlite')
with sqlite3.connect(db) as c:
 assert c.execute('select count(*) from captures where stream=?',(stream,)).fetchone()[0]==0;before=c.execute('select * from finalized_reports order by seq').fetchall()
v=save_checkpoint(Path.cwd(),p,db);assert v==save_checkpoint(Path.cwd(),p,db)
with sqlite3.connect(db) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 for h,pth in artifacts.items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(pth).read_bytes()
 row=c.execute('select v.facts from finding_versions v join finding_observations o using(version_id) where o.capture_seq=? and o.entity_key=?',(v['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
state=dict(county='santa_rosa',circuit=1,database_save=v,completed_people=[],pending_people=[x['name'] for x in people],next_actions=['Review Darlene F. Dickey next, save before next person.','Later officer/assignment screen, clerk/shared material sources, county directory acceptance.']);(R/'state.json').write_text(json.dumps(state,indent=2)+'\n');(D/'validation.json').write_text(json.dumps(dict(result=v,artifacts_readback=len(artifacts),facts_readback=1,replay_verified=True,finalized_reports_unchanged=len(before)),indent=2));print(json.dumps(v,indent=2))
