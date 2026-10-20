import httpx,json,hashlib
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
p=Path(__file__).parent
with httpx.Client(follow_redirects=True,timeout=45) as c:
 for slug,url in [('ada','https://jud14.flcourts.org/ada-information'),('remote','https://jud14.flcourts.org/technology/video-conferencing')]:
  start=datetime.now(timezone.utc).isoformat();r=c.get(url);end=datetime.now(timezone.utc).isoformat(); f=p/f'{slug}-original.html';f.write_bytes(r.content)
  meta=dict(url=url,resolved_url=str(r.url),http_status=r.status_code,request_started_at=start,retrieved_at=end,sha256=hashlib.sha256(r.content).hexdigest(),path=str(f),content_type=r.headers.get('content-type'));(p/f'{slug}-receipt.json').write_text(json.dumps(meta,indent=2)+'\n')
  soup=BeautifulSoup(r.content,'html.parser');links=[dict(text=a.get_text(' ',strip=True),url=a.get('href')) for a in soup.select('a[href]')];(p/f'{slug}-links.json').write_text(json.dumps(links,indent=2)+'\n')
  for el in soup.select('script,style'):el.decompose()
  (p/f'{slug}-text.txt').write_text(soup.get_text('\n',strip=True)+'\n');print(slug,r.status_code,len(r.content))
