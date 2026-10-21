import json,hashlib,urllib.request
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pymupdf
r=Path('runs/county-martin/2026-10-20/review/roberts-astra')
for name,url in [('profile','https://www.circuit19.org/judges/judge-kathleen-h-roberts/'),('appointment','https://www.flgov.com/eog/sites/default/files/judicial/2026/Letter%20to%20Mittleman_Redacted.pdf')]:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as resp:
  b=resp.read();m=dict(url=url,resolved_url=resp.url,http_status=resp.status,retrieved_at=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest())
 if name=='profile':
  (r/'profile.html').write_bytes(b);s=BeautifulSoup(b,'html.parser');t=s.get_text('\n',strip=True);(r/'links.json').write_text(json.dumps([dict(text=a.get_text(' ',strip=True),url=urljoin(url,a['href'])) for a in s.select('a[href]')],indent=2))
 else:
  (r/'appointment.pdf').write_bytes(b);d=pymupdf.open(stream=b,filetype='pdf');t='\n'.join(p.get_text() for p in d);d[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(str(r/'appointment-1.png'))
 (r/(name+'.txt')).write_text(t);m['text_sha256']=hashlib.sha256(t.encode()).hexdigest();(r/(name+'-meta.json')).write_text(json.dumps(m,indent=2)+'\n')
print('Collected profile and appointment letter.')
