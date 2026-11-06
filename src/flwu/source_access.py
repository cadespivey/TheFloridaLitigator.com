"""Recognize a known non-document response, without treating HTTP 200 as review proof."""
import re
from urllib.parse import urlsplit
from bs4 import BeautifulSoup


def candidate(url):
    parsed=urlsplit(url)
    return parsed.hostname=='www.flsenate.gov' and parsed.path.lower().startswith('/laws/statutes')


def limitation(url, raw):
    if not candidate(url) or not raw or len(raw)>20_000:return None
    soup=BeautifulSoup(raw,'html.parser')
    scripts='\n'.join(tag.get_text() for tag in soup.find_all('script'))
    visible=' '.join(soup.get_text(' ',strip=True).split())
    cookie=re.search(r"document\.cookie\s*=\s*['\"]fls_st=[0-9a-f]{40};[^'\"]+['\"]\s*;\s*location\.replace\(location\.href\)",scripts)
    expected='Florida Statutes Loading Florida Statutes… Please enable JavaScript to view Florida Statutes.'
    if cookie and visible in (expected,expected.replace('…','...')):
        return dict(kind='access_challenge',reason='HTTP response contains the Senate cookie/JavaScript verification stub, not the requested statute text. Statutory content is unavailable in this acquisition.')
    return None


def correct_observation(conn, registry, observation_capture_id, reviewer):
    """Append a content-status correction, never a fictitious new retrieval."""
    import json
    from flwu import history as h, source_gate as gate
    row=conn.execute('SELECT payload FROM captures WHERE capture_id=?',(observation_capture_id,)).fetchone()
    old=json.loads(row[0]).get('source_gate') if row else None
    if not old or old['source_id'] not in {s['id'] for s in registry['sources']} or not reviewer.strip():
        raise ValueError('Content correction requires an exact registered observation and reviewer')
    blocked=limitation(old['url'],gate.blob(conn,old['sha256']))
    if not blocked:raise ValueError('Observation is not the recognized source access challenge')
    for observed in reversed(gate.observations(conn,registry['stream'])):
        if observed['source_id']!=old['source_id']:continue
        if observed.get('correction_of')==observation_capture_id:return dict(capture_id=observed['capture_id'],seq=observed['seq'],replayed=True)
        if observed['capture_id']!=observation_capture_id:raise ValueError('A newer observation exists; do not overwrite current source state')
        break
    corrected=dict(old,success=False,transport_success=old.get('transport_success',bool(old.get('success'))),
                   failure_kind=blocked['kind'],error=blocked['reason'],content_available=False,
                   correction_of=observation_capture_id,correction_reviewer=reviewer)
    stream,scope=gate.gate_identity(registry['stream'])
    payload=dict(status='incomplete',contract=scope,findings=[],drafts=[],
                 checks=[dict(id=old['source_id'],status='incomplete',checked_at=h.now(),hashes=[old['sha256']])],
                 source_gate=corrected)
    return h.record(conn,stream=stream,mode='manual_research',scope=scope,
        run_id='source-content-correction:'+observation_capture_id,payload=payload,artifacts={})
