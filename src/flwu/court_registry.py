"""Reconcile recurring primary sources with reviewed county directories.

No acquisition, review receipt, database mutation or pinned-run edit. Supporting
citations are retained as scope candidates, not silently promoted to weekly work.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urldefrag

from flwu import history as h, source_gate as gate
from flwu.county_directory import validate_supplement
from flwu.workflow import write

ORDINALS=('first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth',
          'eleventh','twelfth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth',
          'eighteenth','nineteenth','twentieth')
NUMBERS={'circuit_'+name:number for number,name in enumerate(ORDINALS,1)}


def reconcile(registry, paths):
    original={s['url'] for s in registry['sources']}
    primary={};supporting={};circuits={};inputs=[];counties=set()

    def add(mapping,url,reference):
        if not url:return
        url=urldefrag(url)[0]
        gate._validate_url(url,is_live=True)
        mapping.setdefault(url,[]).append(reference)

    for path in sorted(map(Path,paths)):
        data=json.loads(path.read_text());validate_supplement(data)
        if data['schema_version']!=1:raise ValueError('Use county, not appellate, directory supplements')
        if data['county'] in counties:raise ValueError('Duplicate county directory')
        counties.add(data['county'])
        groups=[c for c in data['courts'] if c['group_id'] in NUMBERS]
        if len(groups)!=1:raise ValueError('Each county directory needs exactly one recognized circuit')
        court=groups[0];number=NUMBERS[court['group_id']]
        entry=circuits.setdefault(number,dict(number=number,group_id=court['group_id'],
            counties=[],court_urls=[],primary_urls=set()))
        if data['county'] in entry['counties']:raise ValueError('Duplicate county directory')
        entry['counties'].append(data['county'])
        if court['url'] not in entry['court_urls']:entry['court_urls'].append(court['url'])
        reference=dict(directory=str(path),county=data['county'],circuit=number,
            directory_sha256=h.sha(path.read_bytes()),stream=data['stream'],through_capture=data['through_capture'])
        inputs.append(reference)
        for c in data['courts']:
            add(primary,c['url'],dict(reference,role='court_index'))
        for person in data['people']:
            for key in ('profile_url','procedure_url'):
                if person.get(key):
                    evidence=[{k:c[k] for k in ('url','sha256','retrieved_at') if k in c}
                              for c in person['sources'] if urldefrag(c['url'])[0]==urldefrag(person[key])[0]]
                    add(primary,person[key],dict(reference,person_id=person['id'],role=key,baseline_sources=evidence))
                    entry['primary_urls'].add(urldefrag(person[key])[0])
            for cite in person['sources']:
                add(supporting,cite['url'],dict(reference,person_id=person['id'],role='supporting_citation',
                    evidence={k:cite[k] for k in ('url','sha256','retrieved_at') if k in cite}))
    merged=json.loads(json.dumps(registry))
    added=sorted(set(primary)-original)
    merged['sources'].extend(dict(id=gate.source_id(url),url=url) for url in added)
    audit=[]
    for number in range(1,21):
        entry=circuits.get(number)
        if entry is None:
            audit.append(dict(number=number,status='missing_directory',registered_before=0,registered_after=0));continue
        urls=set(entry.pop('primary_urls'))|{urldefrag(u)[0] for u in entry['court_urls']}
        audit.append(dict(entry,status='primary_sources_registered',
            registered_before=len(urls&original),registered_after=len(urls),added=len(urls-original)))
    result=dict(schema_version=1,target_stream=registry['stream'],review_protocol=registry['review_protocol'],
        input_registry_sha256=h.sha(registry),output_registry_sha256=h.sha(merged),
        scope='Published primary personnel/procedure and court-index URLs only; no new substantive research',
        directories=inputs,circuits=audit,added=[dict(url=url,reasons=primary[url]) for url in added],
        supporting_candidates=[dict(url=url,reasons=refs,status='scope_review_required')
                               for url,refs in sorted(supporting.items()) if url not in original and url not in primary],
        missing_circuits=[v['number'] for v in audit if v['status']=='missing_directory'],
        initialization_note='New registration is not a completed source review. Preserve county baseline evidence; current retrieval and compatible completed source reviews are still required. Do not fabricate gate receipts from directory review status.',
        database_writes=0,acquisition_performed=False,pinned_run_modified=False)
    return merged,result


def context(registry,manifest,url,*,offset=0,limit=5):
    """Return bounded exact-URL baseline pointers, never whole-directory dumps."""
    if manifest.get('target_stream')!=registry['stream'] or manifest.get('review_protocol')!=registry['review_protocol']:
        raise ValueError('Reconciliation context belongs to another stream/protocol')
    if offset<0 or not 1<=limit<=50:raise ValueError('Context offset must be nonnegative and limit between 1 and 50')
    url=urldefrag(url)[0];gate._validate_url(url,is_live=True)
    match=next((item for key in ('added','supporting_candidates') for item in manifest[key] if item['url']==url),None)
    if match is None:raise ValueError('URL has no addition/candidate provenance in this manifest')
    refs=match['reasons']
    return dict(url=url,source_id=gate.source_id(url),target_stream=registry['stream'],
        registered=url in {s['url'] for s in registry['sources']},
        registry_matches_snapshot=h.sha(registry)==manifest['output_registry_sha256'],
        status=match.get('status','primary_source_registered'),references=refs[offset:offset+limit],
        total_references=len(refs),next_offset=offset+limit if offset+limit<len(refs) else None,
        note='Pointers to previously published county evidence, not a new acquisition or compatible completed source-gate review. Read one person and original artifact as needed; never fabricate an accepted review from directory status.')


def run(registry_path, directory, output, manifest):
    registry_path=Path(registry_path).resolve();output=Path(output).resolve();manifest=Path(manifest).resolve()
    if len({registry_path,output,manifest})!=3:raise ValueError('Input, output and manifest paths must be distinct; never rewrite a pinned registry')
    paths=sorted(Path(directory).glob('*.json'))
    if not paths:raise ValueError('No county directories found')
    merged,audit=reconcile(gate.load_registry(registry_path),paths)
    if len(paths)!=67 or audit['missing_circuits']:
        raise ValueError('Statewide reconciliation requires 67 reviewed counties and all 20 circuits; missing circuits: '+str(audit['missing_circuits']))
    # Refuse stale/different outputs before writing either projection; exact retries are safe.
    for path,value in ((output,merged),(manifest,audit)):
        if path.exists() and json.loads(path.read_text())!=value:raise ValueError('Output already contains different data: '+str(path))
    write(output,merged,immutable=True);write(manifest,audit,immutable=True)
    return dict(registered=len(merged['sources']),added=len(audit['added']),
        supporting_candidates=len(audit['supporting_candidates']),circuits_present=20-len(audit['missing_circuits']),
        missing_circuits=audit['missing_circuits'],output=str(output),manifest=str(manifest),acquisition_performed=False)
