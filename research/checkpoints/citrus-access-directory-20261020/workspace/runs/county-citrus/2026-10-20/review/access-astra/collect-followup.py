import urllib.request,json,datetime,hashlib,pymupdf
from pathlib import Path
p=Path(__file__).parent
for name,u in [('remote','https://www.circuit5.org/wp-content/uploads/2021/12/a-2021-58.pdf'),('rescission','https://www.circuit5.org/wp-content/uploads/2026/02/a-2026-05.pdf'),('senior-backlog','https://www.circuit5.org/wp-content/uploads/2021/08/a-2021-31.pdf')]:
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:b=r.read();m=dict(url=u,resolved_url=r.url,http_status=r.status,retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (p/(name+'.pdf')).write_bytes(b);d=pymupdf.open(stream=b,filetype='pdf');t='\n'.join(f'PAGE {i+1}\n'+x.get_text() for i,x in enumerate(d));(p/(name+'.txt')).write_text(t);m.update(sha256=hashlib.sha256(b).hexdigest(),text_sha256=hashlib.sha256(t.encode()).hexdigest(),pages=len(d));(p/(name+'-meta.json')).write_text(json.dumps(m,indent=2)+'\n');print(name,len(d),t[:14000])
 for i,page in enumerate(d):
  if not page.get_text().strip():page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(p/f'{name}-{i+1}.png')
