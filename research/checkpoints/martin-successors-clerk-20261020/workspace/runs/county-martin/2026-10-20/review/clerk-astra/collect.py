import json,hashlib,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flwu.history import now
r=Path('runs/county-martin/2026-10-20/review/clerk-astra')
for name,url in [('profile','https://www.martinclerk.com/185/Meet-the-Clerk'),('offices','https://www.martinclerk.com/190/Office-Directory'),('civil','https://www.martinclerk.com/189/Civil')]:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as resp:
  b=resp.read();m=dict(url=url,resolved_url=resp.url,http_status=resp.status,retrieved_at=now(),sha256=hashlib.sha256(b).hexdigest())
 (r/(name+'.html')).write_bytes(b);soup=BeautifulSoup(b,'html.parser');t=soup.get_text('\n',strip=True);(r/(name+'.txt')).write_text(t);m['text_sha256']=hashlib.sha256(t.encode()).hexdigest();(r/(name+'-meta.json')).write_text(json.dumps(m,indent=2)+'\n');links=[dict(text=a.get_text(' ',strip=True),url=urljoin(url,a['href'])) for a in soup.select('a[href]')];(r/(name+'-links.json')).write_text(json.dumps(links,indent=2)+'\n')
 print(name,[(a['text'],a['url']) for a in links if 'Email' in a['text'] or 'mailto:' in a['url']])
