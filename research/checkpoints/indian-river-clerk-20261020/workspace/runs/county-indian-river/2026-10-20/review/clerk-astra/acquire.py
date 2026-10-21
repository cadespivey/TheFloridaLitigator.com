import urllib.request, json, hashlib
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup
p=Path(__file__).parent
for name,url in [('contact','https://indianriverclerk.com/contact-us/'),('courts','https://indianriverclerk.com/court-services/')]:
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(req,timeout=45) as r:
  body=r.read();meta=dict(url=r.url,status=r.status,retrieved_at=datetime.now(timezone.utc).isoformat())
 (p/f'{name}.html').write_bytes(body)
 soup=BeautifulSoup(body,'html.parser')
 links=[dict(text=a.get_text(' ',strip=True),url=a.get('href')) for a in soup.select('a[href]')]
 for el in soup(['script','style']):el.decompose()
 text=soup.get_text('\n',strip=True);(p/f'{name}.txt').write_text(text)
 meta.update(sha256=hashlib.sha256(body).hexdigest(),text_sha256=hashlib.sha256(text.encode()).hexdigest(),links=links)
 (p/f'{name}.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(name,meta['status'])
