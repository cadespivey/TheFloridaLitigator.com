"""Connect pinned, reviewed county evidence to weekly comparisons.

This is a compatibility binding, not a fabricated source-gate/model receipt.
Original observations, county findings, review limits and reports stay immutable.
Only exact registered primary URLs from reviewed directory people are eligible.
"""
from __future__ import annotations
import json
from pathlib import Path
from flwu import history as h

PROFILE = 'county-baseline-link-v1'


def identity(target):
    scope = dict(profile=PROFILE, target_stream=target)
    return 'manual_research:'+PROFILE+':'+h.sha(scope)[:12], scope


def bindings(conn, target):
    stream, _ = identity(target)
    result = {}
    for row in conn.execute('SELECT payload FROM captures WHERE stream=? ORDER BY seq', (stream,)):
        for ref in json.loads(row[0]).get('county_baseline_links', {}).get('references', []):
            result[ref['source_id']] = ref
    return result


def apply(observations, references):
    """Derived comparison context; retain the acquisition's original change label."""
    result = []
    for original in observations:
        item = dict(original)
        ref = references.get(item['source_id'])
        if (ref and item['seq'] >= ref['attached_seq'] and item['url'] == ref['previous']['url']
                and h.stamp(item['retrieved_at']) >= h.stamp(ref['previous']['retrieved_at'])):
            item['county_baseline_reference'] = ref
            if not item.get('previous_sha256') and item.get('success'):
                item['acquired_change'] = item['change']
                item.update(previous_sha256=ref['previous']['sha256'],
                            previous_text_sha256=ref['previous']['text_sha256'],
                            change='unchanged' if item['sha256']==ref['previous']['sha256'] else 'changed')
        result.append(item)
    return result


def _capture(conn, capture, stream, *, person=False):
    seq = capture['capture_seq'] if person else capture['seq']
    row = conn.execute('SELECT c.capture_id,c.recorded_at,c.payload,c.stream,c.run_id,s.mode '
                       'FROM captures c JOIN streams s ON s.stream=c.stream WHERE c.seq=?', (seq,)).fetchone()
    if (not row or row[0] != capture['capture_id'] or row[1] != capture['recorded_at']
            or row[5] != 'manual_research' or (not person and row[3] != stream)):
        raise ValueError('County baseline checkpoint does not match saved capture')
    payload=json.loads(row[2])
    if h.sha([row[3],row[4],payload]) != row[0]:
        raise ValueError('County baseline capture checksum mismatch')
    # Current supplements may retain a person from a distinct older county
    # stream. Its explicit capture identity, never a name match, controls.
    return dict(payload, source_stream=row[3])


def ensure(conn, config, *, dry_run=False):
    """One resumable binding checkpoint after acquisition, before ordinary reviews.

    Does not fetch, replace existing decisions or import county findings as news.
    Invalid per-source evidence is recorded as a failure and left for review.
    """
    from flwu import source_gate as gate
    from flwu.county_directory import validate_supplement
    if not config.get('directories') or config['registry']['review_protocol'] != gate.PROTOCOL:
        return None
    target = config['registry']['stream']
    stream, scope = identity(target)
    run_id = config['run_id']
    saved = conn.execute('SELECT payload FROM captures WHERE stream=? AND run_id=?', (stream, run_id)).fetchone()
    if saved:
        return json.loads(saved[0])['county_baseline_links']
    # Raw capture rows: do not recursively apply this compatibility layer.
    observations = {}
    for row in gate.rows(conn, gate.gate_identity(target)[0]):
        o = json.loads(row['payload']).get('source_gate')
        if o:
            observations[o['source_id']] = dict(o, capture_id=row['capture_id'], seq=row['seq'])
    if not observations:
        return None
    reviewed = {(r['source_id'], r['sha256']) for r in gate.reviews(conn, target) if not gate.review_issue(r)}
    registered = {s['url']:s['id'] for s in config['registry']['sources']}
    candidates = {o['url']:o for o in observations.values() if o['url'] in registered
                  and o['success'] and not o.get('previous_sha256')
                  and (o['source_id'],o['sha256']) not in reviewed}
    artifacts, options, failures, directories = {}, {}, [], []
    loaded, parsed_originals = {}, {}
    def blob(digest):
        if digest not in loaded: loaded[digest] = gate.blob(conn, digest)
        return loaded[digest]
    for path in config['directories']:
        raw = Path(path).read_bytes(); data = json.loads(raw)
        if data.get('schema_version') != 1: continue
        primary={p.get(k) for p in data.get('people', []) for k in ('profile_url','procedure_url')}
        if not primary.intersection(candidates): continue
        validate_supplement(data)
        _capture(conn, data['through_capture'], data['stream'])
        digest = h.sha(raw); artifacts[digest] = raw
        directories.append(dict(path=path, sha256=digest, stream=data['stream'], through_capture=data['through_capture']))
        captures = {}
        for person in data['people']:
            urls = {person.get('profile_url'), person.get('procedure_url')} & candidates.keys()
            if not urls: continue
            observation = person['source_observation']
            key = observation['capture_id']
            if key not in captures:
                try:
                    captures[key] = _capture(conn, observation, data['stream'], person=True)
                except ValueError as exc:
                    failures.append(dict(person=person['id'],reason=str(exc),urls=sorted(urls)))
                    continue
            finding = next((f for f in captures[key]['findings'] if f['key']==person['id']), None)
            if finding is None and person.get('legacy_person_id'):
                finding=next((f for f in captures[key]['findings'] if f['key']==person['legacy_person_id']), None)
            if finding is None:
                failures.append(dict(person=person['id'], reason='Pinned person finding missing', urls=sorted(urls)))
                continue
            # Directory approval alone is not evidence: bind its exact cited source
            # to an actual saved finding, original, extraction and quoted passage.
            published = {(c['url'], c['sha256'], c['retrieved_at']) for c in person['sources']}
            for cite in finding['citations']:
                url = cite.get('url')
                if url not in urls or (url,cite.get('sha256'),cite.get('retrieved_at')) not in published: continue
                current = candidates[url]
                if h.stamp(cite['retrieved_at']) > h.stamp(current['retrieved_at']): continue
                try:
                    original = blob(cite['sha256']); extracted = blob(cite['text_sha256']).decode('utf-8')
                    if not cite.get('quote') or cite['quote'] not in extracted or not cite.get('locator'):
                        raise ValueError('Missing bound county quote/locator')
                    if cite.get('authority') != 'official' or cite.get('synthetic') is not False:
                        raise ValueError('County source is not official live evidence')
                    if cite.get('http_status') != 200:
                        # Browser observations need their original signed capture
                        # binding, not an invented transport status.
                        b = cite.get('browser_capture', {})
                        receipt = json.loads(blob(b['observation_sha256']))
                        if not (receipt.get('content_reviewed') is True
                                and receipt.get('original_sha256') == cite['sha256']
                                and receipt.get('page_url') == cite.get('resolved_url',url)
                                and receipt.get('observed_at') == cite['retrieved_at']):
                            raise ValueError('Unverified browser source binding')
                    from flwu.source_access import limitation
                    if limitation(url, original): raise ValueError('County source is an access challenge')
                    previous = dict(url=url, resolved_url=cite.get('resolved_url',url),
                        retrieved_at=cite['retrieved_at'], http_status=cite.get('http_status'), success=True,
                        sha256=cite['sha256'], content_type=current['content_type'])
                    parse_key=(cite['sha256'],url,current['content_type'])
                    if cite['sha256'] == current['sha256']:
                        # Hash first: identical originals need no new parsing.
                        text, method, links = '', 'reviewed-county-extraction', []
                    else:
                        if parse_key not in parsed_originals:
                            parsed_originals[parse_key] = gate.extract(original, previous)
                        text, method, links = parsed_originals[parse_key]
                    parsed = bool(text)
                    if not parsed:
                        # A saved, reviewed scan/OCR derivative remains evidence.
                        # Do not relabel it as a successful fresh parser result.
                        text, method = extracted, 'reviewed-county-extraction'
                    text_bytes=text.encode(); text_hash=h.sha(text_bytes); artifacts[text_hash]=text_bytes
                    previous.update(text_sha256=text_hash, extraction=method)
                    if parsed: previous['links'] = links
                    finding_hash = h.sha(finding)
                    artifacts[finding_hash] = h.canonical(finding).encode()
                    proof = dict(directory_sha256=digest, directory_review=data['review'],
                        stream=captures[key]['source_stream'], checkpoint=data['through_capture'], person=person['id'],
                        finding_capture=observation, finding_sha256=finding_hash, citation=cite,
                        scope='Previously reviewed county personnel/procedure findings; original review limits retained')
                    ref = dict(source_id=current['source_id'], attached_seq=current['seq'],
                        attached_capture_id=current['capture_id'], previous=previous, review=proof)
                    options.setdefault(url, []).append(ref)
                except (ValueError,KeyError,UnicodeError,TypeError) as exc:
                    failures.append(dict(url=url,person=person['id'],reason=str(exc)))
    references=[]
    for url, choices in sorted(options.items()):
        latest=max(h.stamp(r['previous']['retrieved_at']) for r in choices)
        choices=[r for r in choices if h.stamp(r['previous']['retrieved_at'])==latest]
        if len({r['previous']['sha256'] for r in choices}) != 1:
            failures.append(dict(url=url,reason='Conflicting raw hashes at the same prior retrieval time'))
            continue
        ref=choices[0]
        ref['related_reviews']=[r['review'] for r in choices[1:]]
        references.append(ref)
    result=dict(schema_version=1, policy=PROFILE, directories=directories,references=references,failures=failures)
    if dry_run:
        return result
    payload=dict(status='incomplete',contract=scope,findings=[],drafts=[],checks=[],county_baseline_links=result)
    h.record(conn,stream=stream,mode='manual_research',scope=scope,run_id=run_id,payload=payload,
             artifacts={**artifacts,h.sha(result):h.canonical(result).encode()})
    return result


def reuse(conn, current):
    """Prove unchanged evidence within the saved bounded county review scope."""
    from flwu import source_gate as gate, derived_cache
    ref=current.get('county_baseline_reference')
    if not ref or not current.get('success'):return None
    previous=ref['previous']
    if (current.get('resolved_url') or current['url']) != previous['resolved_url']:return None
    old=gate.blob(conn,previous['sha256']); new=gate.blob(conn,current['sha256'])
    if old==new:
        basis='county_baseline_exact_bytes'
    else:
        cache=derived_cache.Cache(conn)
        a=gate.cached_fingerprint(cache,old,previous)
        b=gate.cached_fingerprint(cache,new,current)
        if not a or not b or a['core_sha256']!=b['core_sha256'] or a['components']!=b['components']:return None
        basis='county_baseline_content_hashes'
    proof=dict(policy=PROFILE,reference=ref,current_capture_id=current['capture_id'],
               current_sha256=current['sha256'],basis=basis)
    return dict(source_id=current['source_id'],sha256=current['sha256'],change=current['change'],
                review_receipt=h.sha(proof),reuse_basis=basis,county_baseline_proof=proof)
