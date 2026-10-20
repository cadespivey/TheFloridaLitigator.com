"""Trial-only transport and citation validator; no real network or legal grading."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def dump(value): print(json.dumps(value,indent=2))


def fetch(endpoint):
    sources=json.loads((ROOT/'corpus/sources.json').read_text())
    control=json.loads((ROOT/'state/control.json').read_text())
    log=ROOT/'work/network.jsonl'
    prior=[json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
    item=sources.get(endpoint)
    attempts=sum(x['endpoint']==endpoint for x in prior)
    status=404 if item is None else (503 if item.get('blocked') and not control['restored'] else (429 if item.get('retry_once') and attempts==0 else 200))
    event={'endpoint':endpoint,'status':status,'retrieved_at':datetime.now(timezone.utc).isoformat(),'synthetic':True}
    if status==429: event['retry_after']=0
    if status==200:
        data=item['body'].encode()
        sha=hashlib.sha256(data).hexdigest()
        evidence_id='ev-'+hashlib.sha256(endpoint.encode()).hexdigest()[:12]
        path=ROOT/'work/raw'/f'{evidence_id}-{sha[:12]}.txt'
        if not path.exists(): path.write_bytes(data)
        event.update(evidence_id=evidence_id,path=str(path.relative_to(ROOT)),sha256=sha,body=item['body'])
        metadata=path.with_suffix('.json')
        if not metadata.exists(): metadata.write_text(json.dumps({k:v for k,v in event.items() if k!='body'},indent=2))
    with log.open('a') as f:f.write(json.dumps({k:v for k,v in event.items() if k!='body'})+'\n')
    dump(event)


def verify(path):
    candidate=(ROOT/path).resolve()
    if not candidate.is_relative_to((ROOT/'work').resolve()): raise ValueError('Answers must be under work/')
    data=json.loads(candidate.read_text())
    evidence={}
    for meta in (ROOT/'work/raw').glob('*.json'):
        ref=json.loads(meta.read_text())
        raw=ROOT/ref['path']
        if hashlib.sha256(raw.read_bytes()).hexdigest()!=ref['sha256']:raise ValueError('Modified original: '+ref['path'])
        evidence[ref['evidence_id']]=raw.read_text()
    count=0
    def walk(value):
        nonlocal count
        if isinstance(value,dict):
            if 'quote' in value:
                if not value.get('quote') or value.get('evidence_id') not in evidence or value['quote'] not in evidence[value['evidence_id']]:
                    raise ValueError('Citation does not match a saved source: '+str(value))
                count+=1
            for child in value.values():walk(child)
        elif isinstance(value,list):
            for child in value:walk(child)
    if data.get('synthetic') is not True:raise ValueError('Replay outputs must retain synthetic=true')
    walk(data)
    dump({'status':'structurally_valid','citations_checked':count,'legal_reviewed':False,'coverage_verified':False,'production_ready':False})


if __name__=='__main__':
    try:
        if sys.argv[1]=='fetch':fetch(sys.argv[2])
        elif sys.argv[1]=='verify':verify(Path(sys.argv[2]))
        else:raise ValueError('Use fetch ENDPOINT or verify work/answers/FILE.json')
    except (ValueError,KeyError,OSError,IndexError) as error:
        dump({'error':str(error)})
        raise SystemExit(1)
