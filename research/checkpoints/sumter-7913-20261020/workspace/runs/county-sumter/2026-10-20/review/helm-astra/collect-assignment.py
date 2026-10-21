import urllib.request,json,hashlib,pymupdf
from pathlib import Path
from datetime import datetime,timezone
p=Path(__file__).parent;u='https://www.circuit5.org/wp-content/uploads/2026/05/s-2025-58-a-1.pdf';assert not (p/'assignment.pdf').exists()
r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45);b=r.read();(p/'assignment.pdf').write_bytes(b)
d=pymupdf.open(stream=b,filetype='pdf');t='\n'.join(f'PAGE {i+1}\n'+page.get_text() for i,page in enumerate(d));(p/'assignment.txt').write_text(t)
m=dict(url=u,resolved_url=r.url,http_status=r.status,retrieved_at=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest(),text_sha256=hashlib.sha256((p/'assignment.txt').read_bytes()).hexdigest(),authority='official',synthetic=False,pages=len(d));(p/'assignment-acquisition.json').write_text(json.dumps(m,indent=2)+'\n');d[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(p/'assignment-page1.png');print(t)
