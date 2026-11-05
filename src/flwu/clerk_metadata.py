"""Known Nassau CivicPlus Cloudflare fields; preserve addresses and script logic."""
import base64
import re

from flwu import history as h
from flwu.site_metadata import CF


def email(token):
    if not isinstance(token,str) or not re.fullmatch(r'(?:[0-9a-f]{2}){4,256}',token):
        raise ValueError('Unknown email-obfuscation format')
    raw=bytes.fromhex(token)
    decoded=bytes(x^raw[0] for x in raw[1:]).decode('ascii')
    if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',decoded):
        raise ValueError('Unresolved obfuscated email address')
    return decoded


def normalize(nodes,court):
    if not any(n['tag']=='a' and n['attrs'].get('href')=='https://connect.civicplus.com/referral'
               for n in nodes):raise ValueError('Unrecognized Nassau CivicPlus page')
    metadata,components=[],[]
    for node in nodes:
        attrs=node['attrs']
        if node['tag']=='a' and str(attrs.get('href','')).startswith('/cdn-cgi/l/email-protection#'):
            token=attrs['href'].split('#',1)[1]
            attrs['href']={'flwu_decoded_email':email(token)}
            metadata.append(dict(property='cf_email_href',value_sha256=h.sha(token)))
        if node['tag']=='span' and '__cf_email__' in attrs.get('class',[]) and 'data-cfemail' in attrs:
            token=attrs['data-cfemail'];attrs['data-cfemail']={'flwu_decoded_email':email(token)}
            metadata.append(dict(property='cf_email_span',value_sha256=h.sha(token)))
        if node['tag']!='script':continue
        for child in node['children']:
            text=child.get('value')
            if not isinstance(text,str) or 'window.__CF$cv$params=' not in text:continue
            matches=list(CF.finditer(text))
            if (len(matches)!=1 or not text.startswith('(function(){function c(){')
                    or '/cdn-cgi/challenge-platform/scripts/jsd/main.js' not in text):
                raise ValueError('Unknown Cloudflare wrapper')
            match=matches[0];ray,encoded=match.groups();decoded=base64.b64decode(encoded,validate=True)
            if len(decoded)!=10 or not decoded.isdigit() or base64.b64encode(decoded).decode()!=encoded:
                raise ValueError('Unknown challenge timestamp')
            normalized=text[:match.start()]+"window.__CF$cv$params={r:'FLWU_RAY',t:'FLWU_TIME'}"+text[match.end():]
            normalized=normalized.replace('/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray='+ray,
                                           '/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=FLWU_RAY')
            metadata.append(dict(property='cloudflare_request',value_sha256=h.sha(dict(ray=ray,time=encoded))))
            components.append(dict(court=court,kind='cloudflare_challenge',sha256=h.sha(normalized),location='script'))
            child['value']={'flwu_shared_component':'cloudflare_challenge'}
    return metadata,components
