"""Standard acquisition/update entry: mandatory seven-court discovery, then hash gate."""
from __future__ import annotations
import copy
import difflib
import json
from pathlib import Path
from flwu import history as h, opinion_discovery as opinions, source_gate as gate


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
    (output/'expanded-registry.json').write_text(json.dumps(expanded, indent=2)+'\n')
    gate.run(conn, expanded, run_id, fetch=fetch)
    sources = gate.write_queue(conn, expanded, output/'source-reviews', start=bounds['start'], end=bounds['end'])
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
    sources['tasks'] = [t for t in sources['tasks'] if t.get('url') not in opinion_urls]
    sources['unregistered_previous_sources'] = [u for u in sources['unregistered_previous_sources']
                                                if not any(i.get('pdf_url') == u for e in opinions.events(conn, registry['stream']) for i in e.get('entries', []))]
    result = {'schema_version': 1, 'run_id': run_id, 'bounds': bounds,
              'discovery': discovery, 'source_reviews': sources, 'opinion_reviews': candidates,
              'all_seven_courts_wired': [c['id'] for c in opinions.COURTS],
              'acquisition_complete': discovery['complete'] and not sources['unregistered_previous_sources']
                                       and not any(t['reason'] in ('retrieval_failed', 'not_fetched') for t in sources['tasks'])
                                       and not any('opinion_download_unavailable' in t['reasons'] for t in candidates['tasks']),
              'publication_performed': False,
              'instructions': 'Use this queue, not the unfiltered source-reviews helper output. Process one person/opinion at a time. Listing failures prohibit a no-new-opinions conclusion. No automatic report finalization.'}
    (output/'update-queue.json').write_text(json.dumps(result, indent=2)+'\n')
    opinions.save(conn, registry['stream'], run_id, 'update-result',
                  {'kind': 'update-result', 'bounds': bounds, 'complete': result['acquisition_complete'],
                   'court_coverage': discovery, 'queue_sha256': h.sha(result)}, h.canonical(result).encode())
    return result
