"""Byte-based acquisition gate. No model participates in source-change detection.

Uses append-only captures/artifacts in the existing history database. Source
observations live in a separate stream; accepted interpretations live in the
specified research stream. Nothing here finalizes or publishes a report.
"""
from __future__ import annotations

import difflib
import io
import json
from pathlib import Path
from urllib.parse import urldefrag, urljoin

import httpx

from flwu import history as h, raw_comparison
from flwu.baseline_capture import _validate_url

PROTOCOL = "practical-civil-v1"
MAX_BYTES = 20_000_000


def source_id(url):
    return "source-" + h.sha(url)[:24]


def load_registry(path):
    data = json.loads(Path(path).read_text())
    if set(data) != {"schema_version", "stream", "review_protocol", "sources"} or data['schema_version'] != 1:
        raise ValueError("Registry requires schema_version=1, stream, review_protocol and sources")
    if not isinstance(data['review_protocol'], str) or not data['review_protocol'].strip():
        raise ValueError("Nonempty review_protocol required")
    if not isinstance(data['sources'], list):
        raise ValueError("Registry sources must be a list (empty means no additional non-opinion sources)")
    seen = set()
    for s in data['sources']:
        if set(s) != {'id', 'url'} or s['id'] != source_id(s['url']):
            raise ValueError("Source IDs must be derived from the exact URL; use inventory or source_id")
        _validate_url(s['url'], is_live=True)
        if urldefrag(s['url'])[1] or s['url'] in seen:
            raise ValueError("Duplicate source or URL fragment; register each document once")
        seen.add(s['url'])
    return data


def target(conn, stream):
    row = conn.execute('SELECT mode,scope FROM streams WHERE stream=?', (stream,)).fetchone()
    if not row or row['mode'] != 'manual_research':
        raise ValueError("An existing manual_research target stream is required")
    return json.loads(row['scope'])


def gate_identity(stream):
    scope = {'profile': 'source-gate-v1', 'target_stream': stream}
    return 'manual_research:source-gate-v1:' + h.sha(scope)[:12], scope


def rows(conn, stream):
    return conn.execute('SELECT * FROM captures WHERE stream=? ORDER BY seq', (stream,)).fetchall()


def observations(conn, stream):
    result = []
    for row in rows(conn, gate_identity(stream)[0]):
        item = json.loads(row['payload']).get('source_gate')
        if item:
            result.append(dict(item, capture_id=row['capture_id'], seq=row['seq']))
    return result


def reviews(conn, stream):
    return [r for row in rows(conn, stream)
            if (r := json.loads(row['payload']).get('source_gate_review'))]


def blob(conn, digest):
    row = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (digest,)).fetchone()
    if not row or h.sha(row[0]) != digest:
        raise ValueError("Missing or corrupt source artifact")
    return row[0]


def prior_findings(conn, stream, url):
    """Current saved interpretations for this source, including version guards."""
    return prior_findings_by_url(conn,stream).get(url,[])


def prior_findings_by_url(conn,stream):
    """Index the latest finding versions once per queue, not once per source."""
    latest = {}
    for row in conn.execute('SELECT o.entity_key,o.version_id,o.citations,v.kind,v.facts FROM finding_observations o JOIN captures c ON c.seq=o.capture_seq JOIN finding_versions v USING(version_id) WHERE c.stream=? ORDER BY c.seq', (stream,)):
        latest[row['entity_key']] = row
    result = {}
    for row in latest.values():
        cites = json.loads(row['citations'])
        finding={'key': row['entity_key'], 'kind': row['kind'],
                           'expected_version': row['version_id'],
                           'facts': json.loads(row['facts']), 'citations': cites}
        for url in dict.fromkeys(ci.get('url') for ci in cites):
            result.setdefault(url,[]).append(finding)
    return result


def legacy_source(conn, stream, url):
    """Reuse hash-verified baseline bytes without inventing a completed gate review."""
    candidates = []
    for row in conn.execute('SELECT o.citations FROM finding_observations o JOIN captures c ON c.seq=o.capture_seq WHERE c.stream=?', (stream,)):
        for ci in json.loads(row[0]):
            if ci.get('url') != url or not ci.get('sha256') or not ci.get('retrieved_at') or ci.get('http_status', 200) != 200:
                continue
            try:
                when = h.stamp(ci['retrieved_at'])
                blob(conn, ci['sha256'])
                if ci.get('text_sha256'):
                    blob(conn, ci['text_sha256'])
            except (ValueError, TypeError):
                continue
            candidates.append((when, ci))
    if not candidates:
        return None
    return max(candidates, key=lambda pair: pair[0])[1]


def inventory(conn, stream):
    """Bootstrap URL candidates from saved citations, not a claim of coverage."""
    target(conn, stream)
    urls = set()
    def walk(value):
        if isinstance(value, dict):
            if value.get('url') and value.get('sha256'):
                url = urldefrag(value['url'])[0]
                try:
                    _validate_url(url, is_live=True)
                except ValueError:
                    pass
                else:
                    urls.add(url)
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)
    for row in conn.execute('SELECT o.citations FROM finding_observations o JOIN captures c ON c.seq=o.capture_seq WHERE c.stream=?', (stream,)):
        walk(json.loads(row[0]))
    return {'schema_version': 1, 'stream': stream, 'review_protocol': PROTOCOL,
            'sources': [{'id': source_id(url), 'url': url} for url in sorted(urls)]}


def retrieve(url, *, transport=None):
    """Bounded GET; preserve unsuccessful response bytes without accepting them."""
    started = h.now()
    try:
        with httpx.Client(timeout=30, follow_redirects=False, transport=transport,
                          trust_env=False, headers={'User-Agent': 'FLWU-source-gate/1'}) as client:
            current = url
            for redirect in range(6):
                _validate_url(current, is_live=True)
                with client.stream('GET', current) as response:
                    if response.status_code in {301, 302, 303, 307, 308}:
                        if redirect == 5 or not response.headers.get('location'):
                            raise ValueError('Redirect limit or missing Location')
                        current = urljoin(current, response.headers['location'])
                        continue
                    body = bytearray()
                    for part in response.iter_bytes():
                        body.extend(part)
                        if len(body) > MAX_BYTES:
                            raise ValueError('Response exceeds byte limit')
                    raw = bytes(body)
                    meta = {'url': url, 'resolved_url': current, 'retrieved_at': started,
                            'http_status': response.status_code,
                            'content_type': response.headers.get('content-type', '').split(';')[0].lower()}
                    if response.status_code != 200 or not raw:
                        return dict(meta, success=False, error='HTTP failure or empty body'), raw
                    # A PDF endpoint returning an HTML login/error page is not a new PDF.
                    if (url.lower().split('?')[0].endswith('.pdf') or meta['content_type'] == 'application/pdf') and not raw.startswith(b'%PDF-'):
                        return dict(meta, success=False, error='Expected PDF signature'), raw
                    return dict(meta, success=True), raw
    except (httpx.HTTPError, ValueError):
        # Do not leak URLs/tokens from exception messages. No hash of a partial body.
        return {'url': url, 'retrieved_at': started, 'success': False,
                'error': 'Retrieval failed: network, URL, redirect or size validation'}, None


def extract(raw, meta):
    """Diff aid only. Raw bytes, never this extraction, determine equality."""
    try:
        if raw.startswith(b'%PDF-'):
            from pypdf import PdfReader
            return '\n'.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(raw)).pages), 'pypdf', []
        if 'html' in meta['content_type']:
            from flwu.html_evidence import extract_html
            text, links = extract_html(raw, meta.get('resolved_url') or meta['url'])
            return text, 'html-presentation-v2', links
        if meta['content_type'].startswith('text/') or meta['content_type'] == 'application/json':
            return raw.decode('utf-8'), 'utf8', []
    except Exception:
        # Unsupported/scanned documents still have originals requiring visual review.
        return '', 'unavailable', []
    return '', 'unavailable', []


def attach_text(conn, registry, receipt, text):
    """Attach an explicitly reviewed derivative; never change the original hash."""
    if set(receipt) != {'source_id', 'observation_capture_id', 'sha256', 'method', 'reviewer', 'scope'}:
        raise ValueError('Extraction receipt requires source_id, observation_capture_id, sha256, method, reviewer, scope')
    if not text.strip() or not all(isinstance(v, str) and v.strip() for v in receipt.values()):
        raise ValueError('Extraction and receipt fields must be nonempty')
    if receipt['source_id'] not in {s['id'] for s in registry['sources']}:
        raise ValueError('Source is not registered')
    digest = h.sha(text.encode())
    stream, scope = gate_identity(registry['stream'])
    target(conn, registry['stream'])
    conn.execute('BEGIN IMMEDIATE')
    try:
        obs = observations(conn, registry['stream'])
        current = next((o for o in reversed(obs) if o['source_id'] == receipt['source_id']), None)
        if current and current.get('extraction_receipt') == receipt and current['text_sha256'] == digest:
            conn.rollback()
            return {'capture_id': current['capture_id'], 'seq': current['seq'], 'replayed': True}
        if not current or not current['success'] or current['capture_id'] != receipt['observation_capture_id'] or current['sha256'] != receipt['sha256']:
            raise ValueError('Extraction must bind to the latest successful observation')
        updated = {k: v for k, v in current.items() if k not in ('seq', 'capture_id')}
        updated.update(text_sha256=digest, extraction=receipt['method'], extraction_receipt=receipt)
        payload = {'status': 'incomplete', 'contract': scope, 'findings': [], 'drafts': [],
                   'checks': [{'id': receipt['source_id'], 'status': 'verified',
                               'checked_at': current['retrieved_at'], 'hashes': [current['sha256']]}],
                   'source_gate': updated}
        return h.record(conn, stream=stream, mode='manual_research', scope=scope,
                        run_id='extraction:'+h.sha([receipt, digest]), payload=payload,
                        artifacts={digest: text.encode()})
    except Exception:
        conn.rollback()
        raise


def run(conn, registry, run_id, *, fetch=retrieve):
    """Persist after each retrieval. Repeating a run resumes without refetching."""
    target(conn, registry['stream'])
    stream, scope = gate_identity(registry['stream'])
    fingerprint = h.sha(registry)
    from flwu.acquisition import progress
    for index, s in enumerate(registry['sources'], 1):
        progress('source', index=index, total=len(registry['sources']), source_id=s['id'])
        prior = observations(conn, registry['stream'])
        same_run = [o for o in prior if o['run_id'] == run_id]
        if any(o['registry_sha256'] != fingerprint for o in same_run):
            raise ValueError('Run ID already used with a different registry')
        if any(o['source_id'] == s['id'] for o in same_run):
            continue
        expected_seq = prior[-1]['seq'] if prior else 0
        old = next((o for o in reversed(prior) if o['source_id'] == s['id'] and o['success']), None)
        if old is None:
            old = legacy_source(conn, registry['stream'], s['url'])
        meta, raw = fetch(s['url'])
        if meta['url'] != s['url']:
            raise ValueError('Fetcher returned a different source URL')
        if meta['success'] and not raw:
            raise ValueError('Successful retrieval requires nonempty original bytes')
        h.stamp(meta['retrieved_at'])
        artifacts = {}
        digest = h.sha(raw) if raw is not None else None
        if raw is not None:
            artifacts[digest] = raw
        text, method, links = extract(raw, meta) if meta['success'] else ('', 'unavailable', [])
        text_hash = h.sha(text.encode()) if text else None
        if text_hash:
            artifacts[text_hash] = text.encode()
        change = ('failed' if not meta['success'] else 'new' if old is None else
                  'unchanged' if old['sha256'] == digest else 'changed')
        observation = dict(meta, source_id=s['id'], run_id=run_id, registry_sha256=fingerprint,
                           review_protocol=registry['review_protocol'], sha256=digest,
                           text_sha256=text_hash, extraction=method, links=links,
                           previous_sha256=old['sha256'] if old else None,
                           previous_text_sha256=old.get('text_sha256') if old else None,
                           change=change)
        payload = {'status': 'incomplete', 'contract': scope, 'findings': [], 'drafts': [],
                   'checks': [{'id': s['id'], 'status': 'verified' if meta['success'] else 'incomplete',
                               'checked_at': meta['retrieved_at'], 'hashes': [digest] if meta['success'] else []}],
                   'source_gate': observation}
        conn.execute('BEGIN IMMEDIATE')
        try:
            fresh = observations(conn, registry['stream'])
            if (fresh[-1]['seq'] if fresh else 0) != expected_seq:
                raise ValueError('Concurrent acquisition changed gate state; resume this run')
            h.record(conn, stream=stream, mode='manual_research', scope=scope,
                     run_id=run_id+':'+s['id'], payload=payload, artifacts=artifacts)
        except Exception:
            conn.rollback()
            raise
    progress('source_queue')
    return queue(conn, registry)


def raw_bases(observations):
    """Carry a raw-only transition through later identical, unreviewed fetches."""
    pending,bases={},{}
    for observation in observations:
        key=(observation['source_id'],observation.get('sha256'),observation.get('text_sha256'))
        if raw_comparison.required(observation):pending[key]=observation
        bases[observation['capture_id']]=pending.get(key)
    return bases


def queue(conn, registry, *, start=None, end=None):
    target(conn, registry['stream'])
    obs = observations(conn, registry['stream'])
    bases=raw_bases(obs)
    accepted = reviews(conn, registry['stream'])
    tasks, unchanged = [], []
    for s in registry['sources']:
        current = next((o for o in reversed(obs) if o['source_id'] == s['id']), None)
        if not current:
            tasks.append({'source_id': s['id'], 'url': s['url'], 'reason': 'not_fetched'})
            continue
        approved = next((r for r in reversed(accepted) if r['source_id'] == s['id']
                         and r['sha256'] == current['sha256']
                         and r['review_protocol'] == registry['review_protocol']
                         and r.get('acceptance_version') == 3
                         and (not bases.get(r['observation_capture_id'])
                              or r.get('raw_review_verified') is True)), None)
        if current['success'] and approved:
            unchanged.append({'source_id': s['id'], 'sha256': current['sha256'],
                              'review_receipt': approved['receipt_sha256'], 'change': current['change']})
        else:
            tasks.append({'source_id': s['id'], 'url': s['url'],
                          'reason': 'retrieval_failed' if not current['success'] else
                                    current['change'] if current['change'] in ('new', 'changed') else 'unreviewed',
                          'observation': current})
            if bases.get(current['capture_id']):
                basis=bases[current['capture_id']]
                tasks[-1]['raw_comparison_basis']={k:basis.get(k) for k in
                    ('capture_id','sha256','previous_sha256','content_type')}
    comparison = h.compare(conn, registry['stream'], start=start, end=end)
    triggers = [e for e in comparison['events'] if e['type'] in ('effective_date_reached', 'unresolved_effective_date')]
    return {'schema_version': 1, 'stream': registry['stream'], 'registry_sha256': h.sha(registry),
            'review_protocol': registry['review_protocol'], 'tasks': tasks, 'reused_reviews': unchanged,
            'effective_date_tasks': triggers, 'baseline_known': comparison['baseline_known'],
            'unregistered_previous_sources': sorted({o['url'] for o in obs} - {s['url'] for s in registry['sources']}),
            'baseline_note': 'Report comparison uses last finalized report or explicit start, not last retrieval.',
            'publication_performed': False}


def write_queue(conn, registry, output, *, start=None, end=None):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    data = queue(conn, registry, start=start, end=end)
    previous_findings=prior_findings_by_url(conn,registry['stream'])
    for task in data['tasks']:
        o = task.get('observation')
        if not o:
            continue
        folder = output / o['source_id']
        folder.mkdir(exist_ok=True)
        for label, key in [('current', 'sha256'), ('previous', 'previous_sha256'),
                           ('current-text', 'text_sha256'), ('previous-text', 'previous_text_sha256')]:
            if o.get(key):
                name = label + '-' + o[key] + ('.txt' if 'text' in label else '.bin')
                (folder / name).write_bytes(blob(conn, o[key]))
                task[label+'_path'] = str(folder / name)
        if o.get('text_sha256') and o.get('previous_text_sha256'):
            before = blob(conn, o['previous_text_sha256']).decode().splitlines(True)
            after = blob(conn, o['text_sha256']).decode().splitlines(True)
            diff = '' if before==after else ''.join(difflib.unified_diff(before, after, fromfile='previous', tofile='current'))
            diff_path = folder / ('diff-'+o['capture_id']+'.txt')
            diff_path.write_text(diff)
            task['diff_path'] = str(diff_path)
            task['changed_text_lines'] = changed_text_lines(''.join(before), ''.join(after))
        task['diff_note'] = 'Raw-byte comparison controls; empty/missing text diff does not prove unchanged content. Inspect original, including scans/embedded content.'
        task['prior_findings'] = previous_findings.get(o['url'],[])
        task['review_template'] = {'source_id': o['source_id'], 'observation_capture_id': o['capture_id'],
                                   'sha256': o['sha256'], 'review_protocol': registry['review_protocol'],
                                   'reviewer': '', 'summary': '', 'review_scope': '',
                                   'outcome': 'baseline_reviewed', 'findings': [],
                                   'support': {'reason': '', 'current': [], 'previous': []}}
        if task.get('raw_comparison_basis'):
            basis=task['raw_comparison_basis']
            comparison=raw_comparison.compare(blob(conn,basis['previous_sha256']),blob(conn,o['sha256']),o.get('content_type') or '')
            before_path=folder/('original-before-'+basis['previous_sha256']+'.bin')
            before_path.write_bytes(blob(conn,basis['previous_sha256']))
            task['raw_comparison_previous_path']=str(before_path)
            task['raw_comparison_current_path']=task['current_path']
            path=folder/('original-comparison-'+o['capture_id']+'.json')
            path.write_text(json.dumps(comparison,indent=2,ensure_ascii=False)+'\n')
            task['raw_comparison_path']=str(path)
            task['raw_comparison_sha256']=h.sha(comparison)
            task['raw_comparison_note']=comparison['limitation']
            task['review_template']['raw_change_review']=raw_comparison.template(comparison)
    (output / 'queue.json').write_text(json.dumps(data, indent=2)+'\n')
    return data


def changed_text_lines(before, after):
    """Deterministic changed-line coverage; significance remains a review judgment."""
    if before==after:return {'previous': [], 'current': []}
    old, new = before.splitlines(), after.splitlines()
    result = {'previous': [], 'current': []}
    for tag, i, j, k, l in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag != 'equal':
            result['previous'].extend(line for line in old[i:j] if line.strip())
            result['current'].extend(line for line in new[k:l] if line.strip())
    return result


def accept(conn, registry, receipt):
    """Pin reviewed version; validate quoted evidence and optimistic finding updates."""
    scope = target(conn, registry['stream'])
    required = {'source_id', 'observation_capture_id', 'sha256', 'review_protocol',
                'reviewer', 'summary', 'review_scope', 'outcome', 'findings', 'support'}
    if set(receipt) not in (required,required|{'raw_change_review'}) or not all(isinstance(receipt[k], str) and receipt[k].strip()
                                         for k in required - {'findings', 'support'}):
        raise ValueError('Complete the exact review template, including review scope and reviewer')
    if receipt['outcome'] not in {'baseline_reviewed', 'no_relevant_change', 'updated_findings'}:
        raise ValueError('Unsupported review outcome')
    if receipt['review_protocol'] != registry['review_protocol']:
        raise ValueError('Review protocol mismatch')
    if receipt['source_id'] not in {s['id'] for s in registry['sources']}:
        raise ValueError('Source is not registered')
    digest = h.sha(receipt)
    # Exact replay is a no-op, even if later source observations exist.
    for row in rows(conn, registry['stream']):
        review = json.loads(row['payload']).get('source_gate_review')
        if review and review.get('acceptance_version') == 3 and review['receipt_sha256'] == digest:
            basis=raw_bases(observations(conn,registry['stream'])).get(review['observation_capture_id'])
            if basis and not review.get('raw_review_verified'):
                raise ValueError('Original-content review required before reusing this receipt; refresh the task')
            return {'capture_id': row['capture_id'], 'seq': row['seq'], 'replayed': True}
    conn.execute('BEGIN IMMEDIATE')
    try:
        observed=observations(conn,registry['stream'])
        current = next((o for o in reversed(observed)
                        if o['source_id'] == receipt['source_id']), None)
        if not current or not current['success'] or current['capture_id'] != receipt['observation_capture_id'] or current['sha256'] != receipt['sha256']:
            raise ValueError('Review must match the latest successful current observation; refresh the queue')
        basis=raw_bases(observed).get(current['capture_id'])
        needs_raw=bool(basis)
        if needs_raw:
            comparison=raw_comparison.compare(blob(conn,basis['previous_sha256']),blob(conn,current['sha256']),current.get('content_type') or '')
            raw_comparison.validate(receipt.get('raw_change_review'),comparison)
        elif 'raw_change_review' in receipt:
            raise ValueError('Original-content comparison does not apply to this observation; refresh the task')
        support = receipt['support']
        if (not isinstance(support, dict) or set(support) != {'reason', 'current', 'previous'}
                or not isinstance(support['reason'], str) or not support['reason'].strip()
                or not isinstance(support['current'], list) or not support['current']
                or not isinstance(support['previous'], list)):
            raise ValueError('Completed review requires cited substantive reasoning, not a hostname or keyword classification')
        if not current.get('text_sha256'):
            raise ValueError('Unavailable extraction requires reviewed extraction before completion')
        for side, raw_key, text_key in (('current', 'sha256', 'text_sha256'),
                                        ('previous', 'previous_sha256', 'previous_text_sha256')):
            for cite in support[side]:
                if (not isinstance(cite, dict) or set(cite) != {'sha256', 'text_sha256', 'quote', 'locator'}
                        or not all(isinstance(v, str) and v.strip() for v in cite.values())
                        or cite['sha256'] != current.get(raw_key)
                        or cite['text_sha256'] != current.get(text_key)):
                    raise ValueError('Review support must bind to the exact current/previous acquired pair')
                if cite['quote'] not in blob(conn, cite['text_sha256']).decode('utf-8'):
                    raise ValueError('Review support quote absent from acquired extraction')
        if (receipt['outcome'] == 'no_relevant_change' and current['change'] == 'changed'
                and not support['previous']):
            raise ValueError('No relevant change for changed bytes requires previous and current evidence')
        if current['change'] == 'changed' and receipt['outcome'] == 'baseline_reviewed':
            raise ValueError('Changed source requires updated_findings or supported no_relevant_change, not baseline_reviewed')
        if receipt['outcome'] == 'no_relevant_change' and current['change'] == 'changed':
            changes = changed_text_lines(blob(conn, current['previous_text_sha256']).decode('utf-8'),
                                         blob(conn, current['text_sha256']).decode('utf-8'))
            for side, lines in changes.items():
                if any(not any(line in cite['quote'] for cite in support[side]) for line in lines):
                    raise ValueError('No-change support must cover every changed text line on both sides; unchanged headings are insufficient')
        findings = receipt['findings']
        if not isinstance(findings, list) or (receipt['outcome'] == 'updated_findings') != bool(findings):
            raise ValueError('updated_findings requires findings; other outcomes must not replace findings')
        validated = []
        def preserves_fields(old, new):
            if isinstance(old, dict):
                return isinstance(new, dict) and old.keys() <= new.keys() and all(
                    preserves_fields(v, new[k]) for k, v in old.items())
            return True
        for finding in findings:
            if (set(finding) != {'key', 'kind', 'facts', 'citations', 'expected_version'}
                    or not isinstance(finding['facts'], dict) or not isinstance(finding['citations'], list)
                    or not finding['citations'] or not all(isinstance(finding[k], str) and finding[k].strip() for k in ('key', 'kind'))):
                raise ValueError('Finding requires key, kind, full facts, citations and expected_version')
            prior = conn.execute('SELECT o.version_id,v.facts,v.kind FROM finding_observations o JOIN captures c ON c.seq=o.capture_seq JOIN finding_versions v USING(version_id) WHERE c.stream=? AND o.entity_key=? ORDER BY c.seq DESC LIMIT 1', (registry['stream'], finding['key'])).fetchone()
            if finding['expected_version'] != (prior['version_id'] if prior else None):
                raise ValueError('Finding changed since review began')
            if prior and (finding['kind'] != prior['kind'] or not preserves_fields(json.loads(prior['facts']), finding['facts'])):
                raise ValueError('Preserve existing finding kind and all nested fact fields')
            bound = False
            for cite in finding['citations']:
                if not isinstance(cite, dict) or not all(isinstance(cite.get(k), str) and cite[k] for k in ('url', 'sha256', 'text_sha256', 'quote', 'retrieved_at', 'locator')):
                    raise ValueError('Every citation needs URL, raw/text hashes, exact quote, timestamp and locator')
                _validate_url(cite['url'], is_live=True)
                h.stamp(cite['retrieved_at'])
                blob(conn, cite['sha256'])
                if cite['quote'] not in blob(conn, cite['text_sha256']).decode('utf-8'):
                    raise ValueError('Citation quote is absent from stored extraction')
                # Both raw and text must be a genuine acquired pair, not arbitrary blobs.
                matches = [o for o in observations(conn, registry['stream']) if o['success'] and
                           all(cite[k] == o[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at'))]
                if not matches:
                    raise ValueError('Citation is not bound to an acquired source/text pair')
                if cite['sha256'] == current['sha256'] and cite['url'] == current['url']:
                    bound = True
            if not bound:
                raise ValueError('Each replacement finding must cite the reviewed source')
            validated.append({k: v for k, v in finding.items() if k != 'expected_version'})
        saved_review = dict(receipt, receipt_sha256=digest, acceptance_version=3)
        if needs_raw:saved_review['raw_review_verified']=True
        payload = {'status': 'incomplete', 'contract': scope, 'findings': validated, 'drafts': [],
                   'checks': [{'id': 'source-review:'+receipt['source_id'], 'status': 'verified',
                               'checked_at': h.now(), 'hashes': [receipt['sha256']]},
                              {'id': 'report-review-and-publication', 'status': 'incomplete'}],
                   'source_gate_review': saved_review}
        return h.record(conn, stream=registry['stream'], mode='manual_research', scope=scope,
                        run_id='source-review:'+digest, payload=payload,
                        artifacts={digest: h.canonical(receipt).encode()})
    except Exception:
        conn.rollback()
        raise
