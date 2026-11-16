"""Standard acquisition/update entry: mandatory seven-court discovery, then hash gate."""
from __future__ import annotations
import copy
import difflib
import json
from pathlib import Path
from flwu import history as h, opinion_discovery as opinions, source_gate as gate, derived_cache
from flwu.acquisition import progress


def pinned_registry(conn, registry, run_id, expanded):
    """Freeze acquisition inputs; later opinion reviews must not rewrite a run."""
    saved = next((e for e in opinions.events(conn, registry['stream'])
                  if e['run_id'] == run_id and e['checkpoint'] == 'update-registry'), None)
    # Run/source lookup uses the existing capture_stream index; do not decode
    # every prior run just to validate this pinned acquisition.
    observations = [json.loads(row['payload'])['source_gate'] for row in conn.execute(
        "SELECT payload FROM captures WHERE stream=? AND json_extract(payload,'$.source_gate.run_id')=? ORDER BY seq",
        (gate.gate_identity(registry['stream'])[0], run_id))]
    fingerprints = {o['registry_sha256'] for o in observations}
    if saved:
        expanded = saved['registry']
        if h.sha(expanded) != saved['registry_sha256']:
            raise ValueError('Saved update registry fingerprint mismatch')
    elif fingerprints and fingerprints != {h.sha(expanded)}:
        # Legacy completed runs did not persist this checkpoint. Recover only
        # if the complete ordered registry reproduces the original fingerprint.
        recovered = copy.deepcopy(registry)
        base_urls = {s['url'] for s in recovered['sources']}
        recovered['sources'].extend(
            {'id': gate.source_id(url), 'url': url}
            for url in sorted({o['url'] for o in observations} - base_urls))
        if fingerprints != {h.sha(recovered)}:
            raise ValueError('Cannot recover original update registry; fingerprint mismatch')
        expanded = recovered
    if fingerprints and fingerprints != {h.sha(expanded)}:
        raise ValueError('Saved update registry differs from acquisition observations')
    if not saved:
        opinions.save(conn, registry['stream'], run_id, 'update-registry',
                      {'kind': 'update-registry', 'registry': expanded,
                       'registry_sha256': h.sha(expanded), 'complete': True})
    return expanded


def run(conn, registry, run_id, output, *, start=None, end=None, overlap=30,
        page_size=50, max_pages=200, fetch=gate.retrieve):
    gate.target(conn, registry['stream'])
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    # The run contract pins the reporting baseline, even if a report is finalized later.
    existing = next((e for e in opinions.events(conn, registry['stream'])
                     if e['run_id'] == run_id and e['checkpoint'] == 'update-contract'), None)
    requested = dict(registry_sha256=h.sha(registry), start=start, end=end, overlap=overlap,
                     page_size=page_size, max_pages=max_pages)
    if existing:
        if existing['requested'] != requested:
            raise ValueError('Update run ID is already bound to different arguments')
        bounds = existing['bounds']
    else:
        bounds = opinions.window(conn, registry['stream'], start, end, overlap)
        opinions.save(conn, registry['stream'], run_id, 'update-contract',
                      {'kind': 'update-contract', 'requested': requested, 'bounds': bounds, 'complete': True})
    progress('legacy_opinion_identity')
    seed_failures = opinions.seed_tracked(conn, registry, run_id, fetch=fetch, max_pages=max_pages)
    discovery = opinions.discover(conn, registry['stream'], run_id, bounds, fetch=fetch,
                                  page_size=page_size, max_pages=max_pages)
    discovery['tracked_identity_failures'] = seed_failures
    discovery['complete'] = discovery['complete'] and not seed_failures
    expanded = copy.deepcopy(registry)
    urls = {s['url'] for s in expanded['sources']}
    notice_urls = {u for c in opinions.COURTS for u in c['notice_urls']}
    opinion_urls = {i['pdf_url'] for i in opinions.known(conn, registry['stream']).values() if i['pdf_url']}
    for url in sorted(notice_urls | opinion_urls):
        if url not in urls:
            expanded['sources'].append({'id': gate.source_id(url), 'url': url})
            urls.add(url)
    expanded = pinned_registry(conn, registry, run_id, expanded)
    derived_cache.write_bytes(output/'expanded-registry.json',(json.dumps(expanded, indent=2)+'\n').encode())
    def fetch_source(url):
        meta, raw = fetch(url)
        if url in opinion_urls and meta.get('success') and (not raw or not raw.startswith(b'%PDF-')):
            meta = dict(meta, success=False, error='Expected opinion PDF signature')
        return meta, raw
    gate.run(conn, expanded, run_id, fetch=fetch_source)
    return refresh_queue(conn, expanded, run_id, output, bounds, discovery)


def refresh_queue(conn, expanded, run_id, output, bounds, discovery):
    """Rebuild saved review work after analysis, without performing acquisition."""
    output = Path(output)
    registry = expanded
    progress('exporting_source_queue')
    sources = gate.write_queue(conn, expanded, output/'source-reviews', start=bounds['start'], end=bounds['end'])
    progress('exporting_opinion_queue')
    candidates = opinions.review_queue(conn, expanded)
    source_tasks = {t['source_id']: t for t in sources['tasks']}
    cache = derived_cache.Cache(conn)
    exported = []
    for task in candidates['tasks']:
        item = task['opinion']
        task['document_files'] = source_tasks.get(gate.source_id(item['pdf_url']), {}) if item['pdf_url'] else {}
        inputs = dict(task=task, output=str(output.resolve()))
        value = cache.get('opinion-export', inputs)
        if value is None or any(not Path(v).is_file() for k,v in value.items() if k.endswith('_path')):
            value = export_opinion_task(conn, task, output)
            cache.put('opinion-export', inputs, value)
        exported.append(value)
    candidates['tasks'] = exported
    # PDF interpretation belongs in opinion tasks; avoid asking the model twice.
    # Older versioned URLs remain in a pinned acquisition registry. Their
    # interpretation belongs to the same stable opinion's review history, not
    # a duplicate generic source task. Current opinion tasks still cover any
    # changed bytes/status or unavailable current document.
    tracked_opinion_urls = {i.get('pdf_url') for e in opinions.events(conn, registry['stream'])
                            for i in e.get('entries', []) if i.get('pdf_url')}
    sources['tasks'] = [t for t in sources['tasks'] if t.get('url') not in tracked_opinion_urls]
    # The URLs are already indexed above. Reloading the full persisted opinion
    # history for every omitted source makes each coordinator step quadratic.
    sources['unregistered_previous_sources'] = [u for u in sources['unregistered_previous_sources']
                                                if u not in tracked_opinion_urls]
    result = {'schema_version': 1, 'run_id': run_id, 'bounds': bounds,
              'discovery': discovery, 'source_reviews': sources, 'opinion_reviews': candidates,
              'all_seven_courts_wired': [c['id'] for c in opinions.COURTS],
              'acquisition_complete': discovery['complete']
                                       and not any(t['reason'] in ('retrieval_failed', 'not_fetched') for t in sources['tasks'])
                                       and not any('opinion_download_unavailable' in t['reasons'] for t in candidates['tasks']),
              'publication_performed': False,
              'instructions': 'Use this queue, not the unfiltered source-reviews helper output. Process one person/opinion at a time. Listing failures prohibit a no-new-opinions conclusion. No automatic report finalization.'}
    from flwu.evidence_binding import AcquisitionIndex
    index = AcquisitionIndex(conn, registry['stream'])
    result['reviewed_supplements'] = {
        url: proof for url in sources['unregistered_previous_sources']
        if (proof := index.reviewed_supplement(result, url)) is not None}
    result['unregistered_source_evidence'] = {
        url: dict(source_observation_capture_id=index.source_observations.get(url, {}).get('acquisition_capture_id'),
                  opinion_status_capture_id=index.detail_events.get(url, {}).get('capture_id'))
        for url in sources['unregistered_previous_sources']}
    result['acquisition_complete'] = result['acquisition_complete'] and not (
        set(sources['unregistered_previous_sources']) - set(result['reviewed_supplements']))
    return save_queue(conn, registry, run_id, output, result)


def save_queue(conn, registry, run_id, output, result):
    bounds, discovery = result['bounds'], result['discovery']
    derived_cache.write_bytes(output/'update-queue.json',(json.dumps(result, indent=2)+'\n').encode())
    previous = next((e for e in reversed(opinions.events(conn, registry['stream']))
                     if e['run_id'] == run_id and e['checkpoint'] == 'update-result'), None)
    if previous is None or previous['queue_sha256'] != h.sha(result):
        opinions.save(conn, registry['stream'], run_id, 'update-result',
                      {'kind': 'update-result', 'bounds': bounds, 'complete': result['acquisition_complete'],
                       'court_coverage': discovery, 'queue_sha256': h.sha(result)}, h.canonical(result).encode())
    return result


def refresh(conn, registry, run_id, output):
    """Resume queue projection only from this run's saved acquisition contract."""
    events = [e for e in opinions.events(conn, registry['stream']) if e['run_id'] == run_id]
    contract = next((e for e in events if e['checkpoint'] == 'update-contract'), None)
    pinned = next((e for e in events if e['checkpoint'] == 'update-registry'), None)
    result = next((e for e in reversed(events) if e['checkpoint'] == 'update-result'), None)
    if not contract or not pinned or not result:
        raise ValueError('Acquisition has not completed; resume the exact standard update command')
    if contract['requested']['registry_sha256'] != h.sha(registry):
        raise ValueError('Registry differs from saved acquisition inputs')
    expanded = pinned_registry(conn, registry, run_id, pinned['registry'])
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    derived_cache.write_bytes(output/'expanded-registry.json',(json.dumps(expanded, indent=2)+'\n').encode())
    cache = derived_cache.Cache(conn)
    def dependencies():
        from flwu import county_baseline_link
        return dict(registry=h.sha(registry), run_id=run_id, output=str(output.resolve()),
            bounds=contract['bounds'], state=derived_cache.dependencies(conn,
                [registry['stream'], gate.gate_identity(registry['stream'])[0], opinions.stream_for(registry['stream'])[0],
                 county_baseline_link.identity(registry['stream'])[0]]))
    before = dependencies()
    cached = cache.get('update-queue', before)
    if cached is not None and h.sha(cached) == result['queue_sha256']:
        gate.blob(conn, result['queue_sha256'])  # DB-backed evidence, not cache alone.
        if dependencies() != before:
            raise ValueError('Acquisition/review inputs changed during queue lookup; request next-task again')
        return cached
    snapshot_key = dict(registry=h.sha(registry), run_id=run_id, output=str(output.resolve()), bounds=contract['bounds'])
    previous = cache.get('update-snapshot', snapshot_key)
    refreshed = incremental_sources(conn, expanded, run_id, output, before, previous, result['queue_sha256'])
    if refreshed is None:
        refreshed = refresh_queue(conn, expanded, run_id, output, contract['bounds'], result['court_coverage'])
    # refresh_queue can append its own update-result event. Key the completed
    # snapshot after that commit, so the next unchanged request is a true hit.
    after = dependencies()
    opinion_stream = opinions.stream_for(registry['stream'])[0]
    # A separate run/CLI can acquire or correct evidence while this run holds
    # its own coordinator lock. Never bind a stale result to newer inputs.
    expected = copy.deepcopy(after)
    expected['state']['streams'][opinion_stream] = before['state']['streams'][opinion_stream]
    additions = [json.loads(row['payload'])['opinion_discovery'] for row in conn.execute(
        'SELECT payload FROM captures WHERE stream=? AND seq>?',
        (opinion_stream, before['state']['streams'][opinion_stream][0]))]
    if (expected != before or any(e.get('checkpoint') != 'update-result' for e in additions)):
        raise ValueError('Acquisition/review inputs changed during queue refresh; request next-task again')
    cache.put('update-queue', after, refreshed)
    cache.put('update-snapshot', snapshot_key, dict(dependencies=after, queue=refreshed))
    return refreshed


def export_opinion_task(conn, task, output):
    task = copy.deepcopy(task)
    output = Path(output)
    item = task['opinion']
    folder = output/'opinion-reviews'/item['id']
    folder.mkdir(parents=True, exist_ok=True)
    src = item['status_source']
    derived_cache.write_bytes(folder/'status-original.bin',gate.blob(conn,src['sha256']))
    derived_cache.write_bytes(folder/'status-metadata.json',gate.blob(conn,src['text_sha256']))
    task['status_original_path'] = str(folder/'status-original.bin')
    task['status_metadata_path'] = str(folder/'status-metadata.json')
    current = task['source_observation']
    if current and current['success']:
        derived_cache.write_bytes(folder/'opinion-original.bin',gate.blob(conn,current['sha256']))
        task['opinion_original_path'] = str(folder/'opinion-original.bin')
        if current.get('text_sha256'):
            derived_cache.write_bytes(folder/'opinion-text.txt',gate.blob(conn,current['text_sha256']))
            task['opinion_text_path'] = str(folder/'opinion-text.txt')
    prior = task['prior_review']
    if prior:
        derived_cache.write_bytes(folder/'previous-opinion.bin',gate.blob(conn,prior['pdf_sha256']))
        before = gate.blob(conn, prior['state_sha256']).decode()
        after = gate.blob(conn, item['state_sha256']).decode()
        derived_cache.write_bytes(folder/'status.diff',''.join(difflib.unified_diff([before+'\n'], [after+'\n'], fromfile='previous', tofile='current')).encode())
        task['previous_opinion_path'] = str(folder/'previous-opinion.bin')
        task['status_diff_path'] = str(folder/'status.diff')
    return task


def incremental_sources(conn, registry, run_id, output, current, previous, queue_sha256):
    """Recompute the dependency closure of accepted source-review receipts.

    Changed observations, opinions/statuses, baseline or unknown events
    use the full refresh. The same-court closure includes completed reused pages.
    Finding changes also invalidate their old/new citation hosts and date events.
    """
    from urllib.parse import urlsplit
    if not previous or h.sha(previous.get('queue')) != queue_sha256:
        return None
    gate.blob(conn, queue_sha256)
    old = previous['dependencies']
    expected = copy.deepcopy(current)
    target = registry['stream']
    expected['state']['streams'][target] = old['state']['streams'][target]
    if expected != old: return None
    additions = [json.loads(row['payload']) for row in conn.execute(
        'SELECT payload FROM captures WHERE stream=? AND seq>? ORDER BY seq',
        (target, old['state']['streams'][target][0]))]
    if not additions or any(not p.get('source_gate_review') for p in additions):
        return None
    by_id = {s['id']: s for s in registry['sources']}
    if any(p['source_gate_review']['source_id'] not in by_id for p in additions): return None
    hosts = {urlsplit(by_id[p['source_gate_review']['source_id']]['url']).hostname for p in additions}
    changed_findings = [f for p in additions for f in p.get('findings', [])]
    for finding in changed_findings:
        hosts.update(urlsplit(c['url']).hostname for c in finding['citations'])
        # A replacement may remove a citation. Refresh its former sources too.
        prior = conn.execute(
            'SELECT o.citations FROM finding_observations o JOIN captures c ON c.seq=o.capture_seq '
            'WHERE c.stream=? AND o.entity_key=? AND c.seq<=? ORDER BY c.seq DESC LIMIT 1',
            (target, finding['key'], old['state']['streams'][target][0])).fetchone()
        if prior:
            hosts.update(urlsplit(c['url']).hostname for c in json.loads(prior[0]))
    affected = {s['id'] for s in registry['sources'] if urlsplit(s['url']).hostname in hosts}
    result = copy.deepcopy(previous['queue'])
    sources = result['source_reviews']
    subset = gate.queue(conn, registry, start=result['bounds']['start'], end=result['bounds']['end'],
        only_sources=affected, prior_comparison=(None if changed_findings else
            dict(events=sources['effective_date_tasks'], baseline_known=sources['baseline_known'])))
    subset = gate.write_queue(conn, registry, output/'source-reviews', prepared=subset, write_summary=False)
    # Generic review cannot change an opinion PDF interpretation. Retain the
    # standard queue's exclusion of tracked opinion URLs in this delta too.
    tracked = {i['pdf_url'] for i in opinions.known(conn, target).values()}
    subset['tasks'] = [t for t in subset['tasks'] if t['url'] not in tracked]
    order = {s['id']: n for n,s in enumerate(registry['sources'])}
    for key in ('tasks','reused_reviews'):
        sources[key] = sorted([t for t in sources[key] if t['source_id'] not in affected]+subset[key],
                              key=lambda t: order[t['source_id']])
    for key in ('effective_date_tasks', 'baseline_known'):
        sources[key] = subset[key]
    derived_cache.write_bytes(output/'source-reviews'/'queue.json',(json.dumps(sources,indent=2)+'\n').encode())
    return save_queue(conn, registry, run_id, output, result)
