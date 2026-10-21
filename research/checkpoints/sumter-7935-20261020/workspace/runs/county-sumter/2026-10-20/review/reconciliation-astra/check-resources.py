import urllib.request,urllib.error,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
p=Path(__file__).parent;result=[]
for name,u in [('official-records','https://www.myfloridacounty.com/orisearch/60'),('court-records','https://www.civitekflorida.com/ocrs/county/60/'),('tax-assessor','https://www.sumterpa.com/')]:
 try:
  try:r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20)
  except urllib.error.HTTPError as e:r=e
  b=r.read();(p/(name+'.html')).write_bytes(b);m=dict(name=name,url=u,resolved_url=r.url,http_status=r.status,retrieved_at=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest());result.append(m)
 except Exception as e:result.append(dict(name=name,url=u,error=str(e),retrieved_at=datetime.now(timezone.utc).isoformat()))
(p/'resource-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
