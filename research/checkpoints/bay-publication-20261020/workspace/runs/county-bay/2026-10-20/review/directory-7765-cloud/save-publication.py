import json,hashlib,sqlite3,tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import now
root=Path.cwd();run=Path('runs/county-bay/2026-10-20');review=run/'review/directory-7765-cloud';receipt=review/'publication-ack.json';assert not receipt.exists()
p=json.loads((run/'draft/checkpoint-028.json').read_text());live=json.loads((review/'deployed-browser.txt').read_text().splitlines()[1]);assert [live[k]['rows'] for k in ['bay','circuit','santaRosa']]==[6,22,4] and live['historicalBay']==0
for k in ['bay','circuit','santaRosa']:assert live[k]['status']==200 and not live[k]['390'] and not live[k]['1280']
stamp=now();p['run_id']='bay-live-publication-astra-20261020';p['payload']['contract']['created_at']=stamp
for f in p['payload']['findings']:
 if f['key']=='bay-county-review':f['facts'].update(publication_status='published_verified',published_reviewed_at=stamp,merge_commit='287bcbed8d2cc7c707d028c9c706cb4096f2867a',pages_run=39517117982,live_browser=live,next_action='Indian River initial roster saved7769; Cynthia L. Cox next; statewide goal remains active.')
for file in [review/'deployed-browser.txt',Path(__file__).relative_to(root)]:p['artifacts'][hashlib.sha256(file.read_bytes()).hexdigest()]=str(file)
p['payload']['checks']=[c for c in p['payload']['checks'] if c['id']!='county-publication']+[dict(id='county-publication',status='verified',checked_at=stamp,hashes=[hashlib.sha256((review/'deployed-browser.txt').read_bytes()).hexdigest()],scope='Actual live county/circuit/prior-county/historical filters and responsive widths'),dict(id='future-period-refresh',status='incomplete',scope='Future research remains pending; this does not mark accepted baseline review incomplete.')]
path=run/'draft/checkpoint-029.json';path.write_text(json.dumps(p,indent=2)+'\n');db=Path('/Users/cadespivey/.local/share/flwu/research-history.sqlite')
with tempfile.TemporaryDirectory() as t:save_checkpoint(root,path,Path(t)/'preflight.sqlite')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert c.execute('select max(seq) from captures where stream=?',(p['stream'],)).fetchone()[0]==7767
 before=c.execute('select * from finalized_reports order by seq').fetchall();assert len(before)==5
ack=save_checkpoint(root,path,db);assert ack==save_checkpoint(root,path,db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
 assert before==c.execute('select * from finalized_reports order by seq').fetchall()
 assert json.loads(c.execute('select payload from captures where capture_id=?',(ack['capture_id'],)).fetchone()[0])==p['payload']
 for h,file in p['artifacts'].items():assert c.execute('select bytes from artifacts where sha256=?',(h,)).fetchone()[0]==Path(file).read_bytes()
 for f in p['payload']['findings']:
  row=c.execute('select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?',(ack['seq'],f['key'])).fetchone();assert json.loads(row[0])==f['facts']
ack.update(artifacts_readback=len(p['artifacts']),findings_readback=len(p['payload']['findings']),replay_verified=True,finalized_reports_unchanged=5);receipt.write_text(json.dumps(ack,indent=2)+'\n');print(receipt.read_text())
