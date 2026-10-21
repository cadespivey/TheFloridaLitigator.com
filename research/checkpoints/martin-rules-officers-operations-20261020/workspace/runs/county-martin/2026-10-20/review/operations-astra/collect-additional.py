import json,hashlib,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
import pymupdf
from flwu.history import now
r=Path('runs/county-martin/2026-10-20/review/operations-astra')
for name,url in [('appraiser','https://www.pamartinfl.gov/'),('linked-order','https://www.martinclerk.com/DocumentCenter/View/648/Admin-Order-2-312-efiling-PDF'),('court-search','https://court.martinclerk.com/Home.aspx/Search'),('official-records','https://or.martinclerk.com/landmarkweb/')]:
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as resp:b=resp.read();m=dict(url=url,resolved_url=resp.url,http_status=resp.status,retrieved_at=now(),sha256=hashlib.sha256(b).hexdigest())
  if name=='linked-order':(r/(name+'.pdf')).write_bytes(b);d=pymupdf.open(stream=b,filetype='pdf');t='\n'.join(p.get_text() for p in d)
  else:(r/(name+'.html')).write_bytes(b);t=BeautifulSoup(b,'html.parser').get_text('\n',strip=True)
  (r/(name+'.txt')).write_text(t);m['text_sha256']=hashlib.sha256(t.encode()).hexdigest();(r/(name+'-meta.json')).write_text(json.dumps(m,indent=2)+'\n');print(name,m['http_status'])
 except Exception as e:(r/(name+'-error.json')).write_text(json.dumps(dict(url=url,checked_at=now(),error=str(e)),indent=2)+'\n');print(name,str(e))
