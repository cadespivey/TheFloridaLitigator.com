import urllib.request,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
p=Path(__file__).parent
for name,url in [(n,'https://www.sumterclerk.com/courts/civil/'+n+'/') for n in ['circuit-court','county-court','small-claims']]:
 assert not (p/(name+'.html')).exists()
 r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45);b=r.read();(p/(name+'.html')).write_bytes(b);s=BeautifulSoup(b,'html.parser')
 for el in s(['script','style']):el.decompose()
 t=s.get_text('\n',strip=True);(p/(name+'.txt')).write_text(t);m=dict(url=url,resolved_url=r.url,http_status=r.status,retrieved_at=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest(),text_sha256=hashlib.sha256((p/(name+'.txt')).read_bytes()).hexdigest(),authority='official',synthetic=False);(p/(name+'-meta.json')).write_text(json.dumps(m,indent=2)+'\n')
 links=[dict(text=a.get_text(' ',strip=True),url=a['href']) for a in s.select('a[href]')];(p/(name+'-links.json')).write_text(json.dumps(links,indent=2)+'\n');a=t.find('Type your search phrase');z=t.find('Other Services',a);print(name,t[a:z])
