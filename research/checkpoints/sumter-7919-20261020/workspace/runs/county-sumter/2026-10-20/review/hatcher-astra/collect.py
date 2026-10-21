import urllib.request,urllib.error,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
p=Path(__file__).parent; url='https://www.circuit5.org/courts-judges/sumter-county/judiciary/mary-p-hatcher/';assert not (p/'profile.html').exists()
try:r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45)
except urllib.error.HTTPError as exc:r=exc
content=r.read();stamp=datetime.now(timezone.utc).isoformat();(p/'profile.html').write_bytes(content);s=BeautifulSoup(content,'html.parser')
for el in s(['script','style']):el.decompose()
text=s.get_text('\n',strip=True);(p/'profile.txt').write_text(text)
meta=dict(url=url,resolved_url=r.url,http_status=r.status,retrieved_at=stamp,sha256=hashlib.sha256(content).hexdigest(),text_sha256=hashlib.sha256((p/'profile.txt').read_bytes()).hexdigest(),authority='official',synthetic=False)
(p/'acquisition.json').write_text(json.dumps(meta,indent=2)+'\n');links=[dict(text=a.get_text(' ',strip=True),url=a.get('href')) for a in s.select('a[href]') if a.find_parent('main') or ('uploads/' in a['href']) or ('oncehub' in a['href'])];(p/'links.json').write_text(json.dumps(links,indent=2)+'\n');print(r.status);print(text[text.find("Judicial Assistant:"):]);print(json.dumps(links,indent=2))
