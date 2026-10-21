import json,hashlib,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flwu.history import now
r=Path('runs/county-martin/2026-10-20/review/baillie-astra');url='https://www.circuit19.org/judges/magistrate-bruce-baillie/'
with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as resp:
 b=resp.read();m=dict(url=url,resolved_url=resp.url,http_status=resp.status,retrieved_at=now(),sha256=hashlib.sha256(b).hexdigest())
(r/'profile.html').write_bytes(b);soup=BeautifulSoup(b,'html.parser');t=soup.get_text('\n',strip=True);(r/'profile.txt').write_text(t);m['text_sha256']=hashlib.sha256(t.encode()).hexdigest();(r/'meta.json').write_text(json.dumps(m,indent=2)+'\n');links=[dict(text=a.get_text(' ',strip=True),url=urljoin(url,a['href'])) for a in soup.select('a[href]')];(r/'links.json').write_text(json.dumps(links,indent=2)+'\n')
