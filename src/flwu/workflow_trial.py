"""Supported offline workflow exercise; never fall through to a network fetch.

The fixture intentionally uses official-shaped responses with unmistakably synthetic
content. Trial databases and outputs are confined to an explicitly initialized root.
"""
from pathlib import Path
import json
from urllib.parse import parse_qs, urlparse
from flwu import workflow as w, history as h, source_gate as g, opinion_discovery as d

STREAM = 'workflow-offline-trial-v1'
SCENARIOS = ('normal', 'unchanged', 'failure', 'duplicates', 'interrupted')


def initialize(root, run_dir, scenario):
    root, run_dir = Path(root).resolve(), Path(run_dir).resolve()
    if root == run_dir or root not in run_dir.parents or scenario not in SCENARIOS:
        raise ValueError('Trial run must be a child of its isolated root, with a supported scenario')
    marker = root/'offline-trial.json'
    if not marker.exists() and root.exists() and any(root.iterdir()):
        raise ValueError('A new trial root must be empty; existing work is not a trial workspace')
    w.write(marker, dict(schema_version=1, root=str(root), stream=STREAM), immutable=True)
    db = root/'trial.sqlite'
    with h.database(db) as conn:
        streams = {r[0] for r in conn.execute('SELECT stream FROM streams')}
        if streams and STREAM not in streams:raise ValueError('Refusing a non-trial database')
        h.record(conn, stream=STREAM, mode='manual_research', scope={'profile':STREAM}, run_id='init',
                 payload=dict(status='incomplete', contract={}, checks=[], findings=[], drafts=[]), artifacts={})
    registry = dict(schema_version=1, stream=STREAM, review_protocol=g.PROTOCOL, sources=[])
    w.write(root/'registry.json', registry, immutable=True)
    return w.initialize(run_dir, db, root/'registry.json', run_dir.name, start='2026-10-15', end='2026-10-22',
                        trial=dict(root=str(root), scenario=scenario))


def opinion(n):
    court=d.COURTS[1]
    return {'type':'opinion', 'content':{'id':n, 'typeIdentifier':'opinion',
        'url':court['listing_page'].replace('/Opinions','/opinion/'+str(n)),
        'fields':{'case_number':'TRIAL-'+str(n), 'case_style':'Synthetic Company v. Synthetic Business',
                  'disposition':'Affirmed', 'note':'Synthetic trial only', 'remote_id':'trial-'+str(n),
                  'disposition_date':{'date':{'date':'2026-10-20 00:00:00.000000','timezone':'+00:00'},'stringFormat':'l d F Y'},
                  'type':{'selection':[0]}, 'opinion':{'uri':'/content/download/'+str(n)+'/opinion/file.pdf'}}}}


def pdf_bytes():
    import io
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
    writer=PdfWriter(); page=writer.add_blank_page(width=612,height=792)
    font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
    stream=DecodedStreamObject()
    stream.set_data(b'BT /F1 12 Tf 40 720 Td (SYNTHETIC TRIAL ONLY. A written commercial contract governs. Affirmed. Author Example.) Tj ET')
    page[NameObject('/Contents')]=writer._add_object(stream)
    out=io.BytesIO(); writer.write(out); return out.getvalue()


class Transport:
    def __init__(self, config):
        self.config=config; self.root=Path(config['trial']['root']).resolve()
        self.scenario=config['trial']['scenario']; self.run=Path(config['run_dir']).resolve()
        marker=w.read(self.root/'offline-trial.json')
        if (marker != dict(schema_version=1,root=str(self.root),stream=STREAM)
            or self.root not in self.run.parents or Path(config['database']).resolve()!=self.root/'trial.sqlite'
            or config['registry']['stream']!=STREAM or config['mode']!='preview' or self.scenario not in SCENARIOS):
            raise ValueError('Invalid isolated trial boundary')
        self.pdf=pdf_bytes(); self.entries=[opinion(1),opinion(2)]

    def __call__(self,url):
        # No HTTP client exists here. Unknown URLs fail rather than going live.
        with (self.run/'fixture-requests.jsonl').open('a') as log:
            log.write(json.dumps(dict(url=url,at=h.now(),scenario=self.scenario))+'\n')
        meta=dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,content_type='text/plain')
        q=parse_qs(urlparse(url).query)
        if '_search/opinions/' in url:
            site=q['siteaccess'][0]; offset=int(q['offset'][0]); inactive=q.get('nonactive_only')==['1']
            if self.scenario=='failure' and site=='2dca':
                return dict(meta,success=False,http_status=403),b'Synthetic blocked source'
            marker=self.run/'interruption-fired.json'
            if self.scenario=='interrupted' and site=='1dca' and not inactive and offset==1 and not marker.exists():
                w.write(marker,dict(interrupted=True,url=url),immutable=True)
                raise OSError('Synthetic interruption after the first saved listing page; resume workflow acquire')
            entries=self.entries if site=='1dca' and not inactive else []
            page=entries[offset:offset+1]
            if self.scenario=='duplicates' and offset and page:page=entries[:1]
            body=dict(searchParams=dict(siteaccess=site,scopes=q['scopes[]'],offset=offset,
                        startDate=q['startdate'][0],endDate=q['enddate'][0],nonActiveOnly=inactive,types=['Written','PCA','Citation']),
                      totalCount=len(entries),searchResults=page)
            return dict(meta,content_type='application/json'),json.dumps(body).encode()
        if '/opinion/' in url and '/content/download/' not in url:
            n=int(url.rsplit('/',1)[1]); f=self.entries[n-1]['content']['fields']
            page=dict(_contentInfo={'id':n},caseNumber=f['case_number'],caseStyle=f['case_style'],
                      disposition=f['disposition'],dispositionDate={'format':'2026-10-20'},note=f['note'],remoteId=f['remote_id'],opinion=f['opinion'])
            return dict(meta,content_type='text/html'),('<script id="__NEXT_DATA__">'+json.dumps({'props':{'pageProps':{'pageData':page}}})+'</script>').encode()
        if '/content/download/' in url:return dict(meta,content_type='application/pdf'),self.pdf
        if url in {u for court in d.COURTS for u in court['notice_urls']}:
            return meta,b'SYNTHETIC TRIAL ONLY. No additional release notices are supplied in this fixture.'
        raise ValueError('Offline trial has no response for requested URL')
