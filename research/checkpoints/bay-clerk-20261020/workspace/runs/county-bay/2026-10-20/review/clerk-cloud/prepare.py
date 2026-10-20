import json,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
p=Path(__file__).parent
emails=[]
for slug in ['contact','civil','court-records','official-records']:
 s=BeautifulSoup((p/f'{slug}-original.html').read_bytes(),'html.parser')
 for e in s.select('[data-cfemail],a[href*="email-protection#"]'):
  raw=e.get('data-cfemail') or e['href'].split('#')[-1];b=bytes.fromhex(raw); value=bytes(x^b[0] for x in b[1:]).decode();emails.append(dict(source=slug,label=e.get_text(' ',strip=True),encoded=raw,email=value))
(p/'decoded-public-emails.json').write_text(json.dumps(dict(method='Cloudflare public HTML email obfuscation decoded by XOR of each subsequent byte with first byte; original HTML retained.',values=emails),indent=2)+'\n')
print(json.dumps(emails,indent=2))
links={}
for slug in ['court-records','official-records']:
 links[slug]=[x for x in json.loads((p/f'{slug}-links.json').read_text()) if ('search' in x['text'].lower() or 'accept terms' in x['text'].lower()) and x['url'].startswith('http')]
print(json.dumps(links,indent=2))
