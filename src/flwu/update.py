"""Standard acquisition/update entry: mandatory seven-court discovery, then hash gate."""
from __future__ import annotations
import copy
import difflib
import json
from pathlib import Path
from flwu import history as h, opinion_discovery as opinions, source_gate as gate
from flwu.acquisition import progress


def pinned_registry(conn, registry, run_id, expanded):
    """Freeze acquisition inputs; later opinion reviews must not rewrite a run."""
    saved = next((e for e in opinions.events(conn, registry['stream'])
                  if e['run_id'] == run_id and e['checkpoint'] == 'update-registry'), None)
    observations = [o for o in gate.observations(conn, registry['stream'])
                    if o['run_id'] == run_id]
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
    (output/'expanded-registry.json').write_text(json.dumps(expanded, indent=2)+'\n')
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
    for task in candidates['tasks']:
        item = task['opinion']
        task['document_files'] = source_tasks.get(gate.source_id(item['pdf_url']), {}) if item['pdf_url'] else {}
        folder = output/'opinion-reviews'/item['id']
        folder.mkdir(parents=True, exist_ok=True)
        src = item['status_source']
        (folder/'status-original.bin').write_bytes(gate.blob(conn, src['sha256']))
        (folder/'status-metadata.json').write_bytes(gate.blob(conn, src['text_sha256']))
        task['status_original_path'] = str(folder/'status-original.bin')
        task['status_metadata_path'] = str(folder/'status-metadata.json')
        current = task['source_observation']
        if current and current['success']:
            (folder/'opinion-original.bin').write_bytes(gate.blob(conn, current['sha256']))
            task['opinion_original_path'] = str(folder/'opinion-original.bin')
            if current.get('text_sha256'):
                (folder/'opinion-text.txt').write_bytes(gate.blob(conn, current['text_sha256']))
                task['opinion_text_path'] = str(folder/'opinion-text.txt')
        prior = task['prior_review']
        if prior:
            (folder/'previous-opinion.bin').write_bytes(gate.blob(conn, prior['pdf_sha256']))
            before = gate.blob(conn, prior['state_sha256']).decode()
            after = gate.blob(conn, item['state_sha256']).decode()
            (folder/'status.diff').write_text(''.join(difflib.unified_diff([before+'\n'], [after+'\n'], fromfile='previous', tofile='current')))
            task['previous_opinion_path'] = str(folder/'previous-opinion.bin')
            task['status_diff_path'] = str(folder/'status.diff')
    # PDF interpretation belongs in opinion tasks; avoid asking the model twice.
    # Older versioned URLs remain in a pinned acquisition registry. Their
    # interpretation belongs to the same stable opinion's review history, not
    # a duplicate generic source task. Current opinion tasks still cover any
    # changed bytes/status or unavailable current document.
    tracked_opinion_urls = {i.get('pdf_url') for e in opinions.events(conn, registry['stream'])
                            for i in e.get('entries', []) if i.get('pdf_url')}
    sources['tasks'] = [t for t in sources['tasks'] if t.get('url') not in tracked_opinion_urls]
    sources['unregistered_previous_sources'] = [u for u in sources['unregistered_previous_sources']
                                                if not any(i.get('pdf_url') == u for e in opinions.events(conn, registry['stream']) for i in e.get('entries', []))]
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
    (output/'update-queue.json').write_text(json.dumps(result, indent=2)+'\n')
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
    (output/'expanded-registry.json').write_text(json.dumps(expanded, indent=2)+'\n')
    return refresh_queue(conn, expanded, run_id, output, contract['bounds'], result['court_coverage'])
