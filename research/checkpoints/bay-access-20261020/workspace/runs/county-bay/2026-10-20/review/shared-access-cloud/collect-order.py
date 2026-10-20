import httpx,json,hashlib,pymupdf
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urljoin
p=Path(__file__).parent
links=json.loads((p.parent/'shared-civil-cloud/orders-index-links.json').read_text());names=['2026-00-10']
with httpx.Client(follow_redirects=True,timeout=45) as c:
 for name in names:
  url=urljoin('https://jud14.flcourts.org',next(x['url'].strip() for x in links if x['text']==name));start=datetime.now(timezone.utc).isoformat();r=c.get(url);end=datetime.now(timezone.utc).isoformat();f=p/f'{name}-original.pdf';f.write_bytes(r.content);meta=dict(url=url,resolved_url=str(r.url),http_status=r.status_code,request_started_at=start,retrieved_at=end,sha256=hashlib.sha256(r.content).hexdigest(),path=str(f),content_type=r.headers.get('content-type'));(p/f'{name}-receipt.json').write_text(json.dumps(meta,indent=2)+'\n')
  if r.status_code==200:
   doc=pymupdf.open(f);text='\n'.join(f'--- PAGE {i+1} ---\n'+page.get_text() for i,page in enumerate(doc));(p/f'{name}-text.txt').write_text(text);print(name,len(doc),'pages',len(text),'characters')
