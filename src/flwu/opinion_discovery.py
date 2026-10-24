"""Official Florida opinion discovery, checkpointed independently of document checks."""
from __future__ import annotations
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode, urljoin, urlparse, urlsplit, urlunsplit, quote
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from flwu import history as h, source_gate as g
from flwu.identity import document_id
from flwu.acquisition import progress

COURTS = json.loads((Path(__file__).parent/'data/opinion_sources.json').read_text())


def stream_for(target):
    scope = {'profile': 'opinion-discovery-v1', 'target_stream': target}
    return 'manual_research:opinion-discovery-v1:' + h.sha(scope)[:12], scope


def events(conn, target):
    return [json.loads(r['payload'])['opinion_discovery'] for r in g.rows(conn, stream_for(target)[0])]


def save(conn, target, run_id, key, event, raw=None):
    stream, scope = stream_for(target)
    artifacts = {h.sha(raw): raw} if raw is not None else {}
    for item in event.get('entries', []):
        if item.get('status_source'):
            data = h.canonical(item['metadata']).encode()
            artifacts[h.sha(data)] = data
    payload = {'status': 'incomplete', 'contract': scope, 'findings': [], 'drafts': [],
               'checks': [{'id': key, 'status': 'verified' if event.get('complete') else 'incomplete',
                           'checked_at': h.now(), 'hashes': list(artifacts)}],
               'opinion_discovery': dict(event, run_id=run_id, checkpoint=key)}
    return h.record(conn, stream=stream, mode='manual_research', scope=scope,
                    run_id=run_id+':'+key, payload=payload, artifacts=artifacts)


def window(conn, target, start=None, end=None, overlap=30):
    upper = date.fromisoformat(end) if end else datetime.now(ZoneInfo('America/New_York')).date()
    baseline = None
    if start:
        lower = date.fromisoformat(start)
    else:
        row = h.latest_finalized(conn, target, before_time=h.boundary(str(upper), end=True))
        if row is None:
            raise ValueError('No finalized report for this stream; supply an explicit --start date')
        baseline = row['capture_id']
        lower = datetime.fromisoformat(row['recorded_at']).astimezone(ZoneInfo('America/New_York')).date()
    if lower > upper or not 1 <= overlap <= 366:
        raise ValueError('Invalid reporting dates or overlap (1–366 days)')
    return {'start': str(lower), 'end': str(upper), 'discovery_start': str(lower-timedelta(days=overlap)),
            'api_end_exclusive': str(upper+timedelta(days=1)), 'overlap_days': overlap,
            'finalized_baseline_capture': baseline}


def query_url(court, bounds, offset, limit, inactive=False):
    params = {'query': '', 'siteaccess': court['siteaccess'], 'searchtype': 'opinions',
              'scopes[]': court['scope'], 'sort': 'opinion/disposition_date desc',
              'startdate': bounds['discovery_start'], 'enddate': bounds['api_end_exclusive'],
              'limit': limit, 'offset': offset}
    if inactive:
        params['nonactive_only'] = 1
    return court['endpoint']+'?'+urlencode(params)


def normalized(court, content_id, fields, detail_url, *, inactive=False):
    if not isinstance(content_id, int) or not fields.get('case_number'):
        raise ValueError('Missing stable official content ID or case number')
    published = fields['disposition_date']['date']['date'][:10]
    date.fromisoformat(published)
    uri = (fields.get('opinion') or {}).get('uri')
    pdf = urljoin(court['endpoint'], uri) if uri else None
    def encoded_path(url):
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, quote(parts.path, safe="/%:@!$&'()*+,;=-._~"), parts.query, parts.fragment))
    if pdf:
        pdf = encoded_path(pdf)
        g._validate_url(pdf, is_live=True)
    detail_url = encoded_path(detail_url)
    g._validate_url(detail_url, is_live=True)
    if urlparse(detail_url).hostname != urlparse(court['listing_page']).hostname:
        raise ValueError('Opinion belongs to another court')
    # Preserve exact official words; do not infer which legal status controls.
    metadata = {k: v for k, v in fields.items() if k not in ('opinion', 'oral_argument', 'video_external_link', 'video_internal_links')}
    metadata['document_filename'] = (fields.get('opinion') or {}).get('fileName')
    metadata['listed_in_inactive_feed'] = inactive
    return {'id': document_id(court['id'], 'content:'+str(content_id)), 'court': court['id'],
            'content_id': content_id, 'case_number': fields['case_number'],
            'published_date': published, 'title': fields.get('case_style', ''),
            'detail_url': detail_url, 'pdf_url': pdf, 'metadata': metadata,
            'state_sha256': h.sha(metadata)}


def bind_status(entries, meta, raw):
    for item in entries:
        item['status_source'] = {k: meta[k] for k in ('url', 'retrieved_at', 'http_status', 'success')}
        item['status_source'].update(sha256=h.sha(raw), text_sha256=h.sha(item['metadata']),
                                     extraction='canonical official metadata fields')
    return entries


def parse_page(raw, court, bounds, offset, inactive=False):
    data = json.loads(raw)
    total = data['totalCount']; params = data['searchParams']; entries = data['searchResults']
    if type(total) is not int or total < 0 or not isinstance(entries, list):
        raise ValueError('Invalid listing count/results')
    if (params['siteaccess'] != court['siteaccess'] or params['scopes'] != [court['scope']]
            or int(params['offset']) != offset or params['startDate'] != bounds['discovery_start']
            or params['endDate'] != bounds['api_end_exclusive']
            or bool(params.get('nonActiveOnly')) != inactive
            or bool(params.get('activeOnly'))
            or set(params.get('types', [])) != {'Written', 'PCA', 'Citation'}):
        raise ValueError('Listing did not honor court, offset, date or status filters')
    parsed = []
    for entry in entries:
        content = entry['content']
        if content['typeIdentifier'] != 'opinion':
            raise ValueError('Unexpected listing record type')
        item = normalized(court, content['id'], content['fields'], content['url'], inactive=inactive)
        if not bounds['discovery_start'] <= item['published_date'] <= bounds['api_end_exclusive']:
            raise ValueError('Listing contains out-of-window record')
        parsed.append(item)
    return total, parsed


def detail(raw, court, previous):
    soup = BeautifulSoup(raw, 'html.parser')
    node = soup.find('script', id='__NEXT_DATA__')
    if not node:
        raise ValueError('Opinion detail metadata unavailable')
    page = json.loads(node.string)['props']['pageProps']['pageData']
    if page['_contentInfo']['id'] != previous['content_id']:
        raise ValueError('Opinion identity changed at detail URL')
    # Translate the detail page's GraphQL shape to the listing's fields.
    fields = dict(previous['metadata'])
    fields.pop('listed_in_inactive_feed', None)
    for key, dest in [('caseNumber', 'case_number'), ('caseStyle', 'case_style'),
                      ('disposition', 'disposition'), ('note', 'note'), ('remoteId', 'remote_id')]:
        if key not in page:
            raise ValueError('Missing opinion detail field: '+key)
        fields[dest] = page[key]
    fields['disposition_date'] = dict(fields['disposition_date'])
    fields['disposition_date']['date'] = dict(fields['disposition_date']['date'], date=page['dispositionDate']['format']+' 00:00:00.000000')
    fields['opinion'] = page.get('opinion')
    return normalized(court, previous['content_id'], fields, previous['detail_url'],
                      inactive=previous['metadata'].get('listed_in_inactive_feed', False))


def known(conn, target):
    found = {}
    for event in events(conn, target):
        for item in event.get('entries', []):
            found[item['id']] = item
    return found


def seed_tracked(conn, registry, run_id, *, fetch=g.retrieve, max_pages=200):
    """Locate saved official opinion PDFs outside the overlap by their official case number.

    Search results must contain the exact CMS content ID from the saved URL before
    that court is associated with the opinion. Filename alone never assigns court.
    """
    urls = {s['url'] for s in registry['sources']} | {s['url'] for s in g.inventory(conn, registry['stream'])['sources']}
    tracked = {i['content_id'] for i in known(conn, registry['stream']).values()}
    cached = {e['checkpoint']: e for e in events(conn, registry['stream']) if e['run_id'] == run_id}
    failures = []
    for url in sorted(urls):
        match = re.search(r'/content/download/(\d+)/opinion/(?:Opinion_)?([^/?]+)\.pdf', url)
        if not match or int(match[1]) in tracked:
            continue
        content_id, number = int(match[1]), match[2]
        if not re.fullmatch(r'(?:SC|[1-6]D)?\d{2,4}-\d+', number, re.I):
            failures.append({'url': url, 'error': 'Cannot derive a case-number search from tracked opinion URL'})
            continue
        found = False
        for court in COURTS:
            offset = 0
            for _ in range(max_pages):
                key = 'seed:'+str(content_id)+':'+court['id']+':'+str(offset)
                event = cached.get(key)
                if event is None:
                    params = {'query': number, 'siteaccess': court['siteaccess'], 'searchtype': 'opinions',
                              'scopes[]': court['scope'], 'opinions_search_fields[]': 'case_number',
                              'limit': 50, 'offset': offset}
                    meta, raw = fetch(court['endpoint']+'?'+urlencode(params))
                    event = {'kind': 'seed', 'source': meta, 'complete': False, 'entries': []}
                    try:
                        if not meta['success']:
                            raise ValueError('Failed legacy opinion lookup')
                        data = json.loads(raw); p = data['searchParams']
                        if type(data['totalCount']) is not int or data['totalCount'] < 0:
                            raise ValueError('Invalid tracked-opinion search count')
                        if p['query'] != number or p['scopes'] != [court['scope']] or int(p['offset']) != offset:
                            raise ValueError('Legacy opinion query not honored')
                        entries = [normalized(court, e['content']['id'], e['content']['fields'], e['content']['url']) for e in data['searchResults']]
                        matched = [e for e in entries if e['content_id'] == content_id]
                        event.update(complete=True, entries=bind_status(matched, meta, raw), returned=len(entries), total=data['totalCount'])
                    except (ValueError, KeyError, TypeError):
                        event['error'] = 'Tracked opinion identity lookup incomplete'
                    save(conn, registry['stream'], run_id, key, event, raw)
                if event['entries']:
                    found = True; tracked.add(content_id); break
                if not event['complete'] or not event['returned'] or offset+event['returned'] >= event['total']:
                    break
                offset += event['returned']
            if found:
                break
        if not found:
            failures.append({'url': url, 'content_id': content_id, 'error': 'Tracked opinion status identity not located; PDF checks alone do not establish status'})
    return failures


def discover(conn, target, run_id, bounds, *, fetch=g.retrieve, page_size=50, max_pages=200):
    """Every court and inactive feed independently fetched; page receipts resume."""
    g.target(conn, target)
    if not 1 <= page_size <= 200 or not 1 <= max_pages <= 1000:
        raise ValueError('page_size must be 1–200 and max_pages 1–1000')
    cached = {e['checkpoint']: e for e in events(conn, target) if e['run_id'] == run_id}
    contract = dict(bounds=bounds, courts=COURTS, page_size=page_size, max_pages=max_pages)
    if 'contract' in cached and cached['contract']['contract'] != contract:
        raise ValueError('Opinion run ID already bound to another window/configuration')
    if 'contract' not in cached:
        save(conn, target, run_id, 'contract', {'kind': 'contract', 'contract': contract, 'complete': True})
    coverage = []
    for court in COURTS:
        for inactive in (False, True):
            channel = court['id']+(':inactive' if inactive else ':listing')
            offset, total, seen, complete, error = 0, None, set(), False, None
            for _ in range(max_pages):
                progress('opinion_listing', court=court['id'], channel=channel, offset=offset)
                key = channel+':'+str(offset)
                event = cached.get(key)
                if event is None:
                    url = query_url(court, bounds, offset, page_size, inactive)
                    meta, raw = fetch(url)
                    event = {'kind': 'page', 'court': court['id'], 'channel': channel,
                             'source': meta, 'sha256': h.sha(raw) if raw is not None else None,
                             'complete': False, 'entries': []}
                    try:
                        if not meta['success']:
                            raise ValueError('Listing retrieval failed')
                        count, entries = parse_page(raw, court, bounds, offset, inactive)
                        event.update(total=count, returned=len(entries),
                                     entries=bind_status([x for x in entries if x['published_date'] <= bounds['end']], meta, raw),
                                     page_ids=[x['id'] for x in entries], complete=True)
                    except (ValueError, KeyError, TypeError, AttributeError):
                        event['error'] = 'Blocked, invalid or unrecognized opinion listing; coverage incomplete'
                    save(conn, target, run_id, key, event, raw)
                if not event['complete']:
                    error = event.get('error'); break
                if total is not None and total != event['total']:
                    error = 'Listing total changed during pagination'; break
                total = event['total']
                ids = event['page_ids']
                if len(ids) != len(set(ids)) or seen.intersection(ids):
                    error = 'Duplicate listing identities; possible pagination drift'; break
                seen.update(ids)
                if offset + event['returned'] == total:
                    complete = True; break
                if not event['returned'] or offset + event['returned'] > total:
                    error = 'Premature empty page or inconsistent total'; break
                offset += event['returned']  # honor actual server page size, not requested limit
            result = {'kind': 'coverage', 'court': court['id'], 'channel': channel,
                      'complete': complete, 'total': total, 'unique_seen': len(seen),
                      'error': error or (None if complete else 'Page budget exhausted')}
            save(conn, target, run_id, channel+':coverage', result)
            coverage.append(result)
    # Revisit tracked official status metadata regardless of publication age or listing success.
    failures = []
    court_map = {c['id']: c for c in COURTS}
    for item in known(conn, target).values():
        progress('opinion_detail', opinion_id=item['id'])
        key = 'detail:'+item['id']; event = cached.get(key)
        if event is None:
            meta, raw = fetch(item['detail_url'])
            event = {'kind': 'detail', 'id': item['id'], 'source': meta,
                     'sha256': h.sha(raw) if raw is not None else None, 'complete': False, 'entries': []}
            try:
                if not meta['success']:
                    raise ValueError('Detail retrieval failed')
                updated = detail(raw, court_map[item['court']], item)
                event.update(complete=True, entries=bind_status([updated], meta, raw))
            except (ValueError, KeyError, TypeError, AttributeError):
                event['error'] = 'Official opinion status/detail unavailable; previous record retained'
            save(conn, target, run_id, key, event, raw)
        if not event['complete']:
            failures.append(event)
    return {'courts': coverage, 'detail_failures': failures,
            'complete': all(c['complete'] for c in coverage) and not failures}


def review_queue(conn, registry):
    obs = g.observations(conn, registry['stream'])
    accepted = [r for row in g.rows(conn, registry['stream'])
                if (r := json.loads(row['payload']).get('opinion_review'))]
    tasks, reused = [], []
    current_items = known(conn, registry['stream'])
    latest_details = {e['id']: e for e in events(conn, registry['stream']) if e.get('kind') == 'detail'}
    for item in current_items.values():
        status_failed = not latest_details.get(item['id'], {}).get('complete', False)
        current = next((o for o in reversed(obs) if o['url'] == item['pdf_url']), None)
        signature = h.sha([item['id'], item['state_sha256'], current['sha256'] if current else None, registry['review_protocol']])
        old = next((r for r in reversed(accepted) if r['signature'] == signature and r['relevance'] != 'uncertain'), None)
        if current and current['success'] and old and not status_failed:
            reused.append(item['id']); continue
        prior = next((r for r in reversed(accepted) if r['id'] == item['id']), None)
        reasons = []
        if status_failed:
            reasons.append('official_status_source_unavailable')
        if not prior:
            reasons.append('new_or_unreviewed_opinion')
        if prior and prior['state_sha256'] != item['state_sha256']:
            reasons.append('official_status_metadata_changed')
        if not current or not current['success']:
            reasons.append('opinion_download_unavailable')
        elif not prior or prior['pdf_sha256'] != current['sha256']:
            reasons.append('new_or_changed_pdf')
        if not reasons:
            reasons.append('unfinished_or_protocol_changed_review')
        tasks.append({'opinion': item, 'signature': signature, 'reasons': reasons,
                      'prior_review': prior,
                      'related_opinion_ids': [other['id'] for other in current_items.values()
                                             if other['id'] != item['id'] and other['court'] == item['court']
                                             and other['case_number'] == item['case_number']],
                      'source_observation': current,
                      'review_template': {'id': item['id'], 'signature': signature, 'reviewer': '',
                                          'relevance': 'uncertain', 'summary': '', 'holding': '',
                                          'disposition': '', 'authors': [], 'citations': []}})
    return {'tasks': tasks, 'reused_reviews': reused}


def _accept_review(conn, registry, receipt):
    required = {'id', 'signature', 'reviewer', 'relevance', 'summary', 'holding', 'disposition', 'authors', 'citations'}
    if (not isinstance(receipt, dict) or set(receipt) != required
            or not all(isinstance(receipt[k], str) for k in required - {'authors', 'citations'})
            or receipt['relevance'] not in ('relevant', 'not_relevant', 'uncertain')
            or not receipt['reviewer'].strip() or not receipt['summary'].strip()
            or not isinstance(receipt['citations'], list)):
        raise ValueError('Complete the exact opinion review template with relevance and explanation')
    digest = h.sha(receipt)
    for row in g.rows(conn, registry['stream']):
        old = json.loads(row['payload']).get('opinion_review')
        if old and old['receipt_sha256'] == digest:
            return {'capture_id': row['capture_id'], 'seq': row['seq'], 'replayed': True}
    task = next((t for t in review_queue(conn, registry)['tasks'] if t['opinion']['id'] == receipt['id']), None)
    if not task or task['signature'] != receipt['signature']:
        raise ValueError('Opinion candidate changed or already reviewed; regenerate queue')
    current = task['source_observation']; item = task['opinion']
    if not current or not current['success']:
        raise ValueError('Cannot accept an opinion with failed/missing original')
    if 'official_status_source_unavailable' in task['reasons']:
        raise ValueError('Official status lookup is incomplete; retain the pending task')
    if receipt['relevance'] == 'relevant' and (not receipt['holding'].strip() or not receipt['disposition'].strip() or not receipt['citations']):
        raise ValueError('Relevant opinion needs holding, disposition and source quotations')
    if receipt['relevance'] == 'relevant' and not any(isinstance(ci, dict) and ci.get('sha256') == current['sha256'] for ci in receipt['citations']):
        raise ValueError('Holding/disposition require citation to the opinion, not listing metadata alone')
    if receipt['relevance'] != 'uncertain' and not receipt['citations']:
        raise ValueError('Completed relevance screening requires source support')
    if not isinstance(receipt['authors'], list) or any(not isinstance(a, str) for a in receipt['authors']):
        raise ValueError('authors must be a list of names (empty if not established)')
    for ci in receipt['citations']:
        if not isinstance(ci, dict) or not all(isinstance(ci.get(k), str) and ci[k] for k in ('quote', 'locator', 'sha256', 'text_sha256')):
            raise ValueError('Citations need quote, locator and raw/text hashes')
        supported = next((source for source in (current, item['status_source'])
                          if ci['sha256'] == source['sha256'] and ci['text_sha256'] == source.get('text_sha256')), None)
        if not supported or ci['quote'] not in g.blob(conn, ci['text_sha256']).decode():
            raise ValueError('Opinion citation does not match current acquired original/extraction')
    citation = {k: current[k] for k in ('url', 'sha256', 'retrieved_at')}
    bound_citations = []
    for ci in receipt['citations']:
        source = current if ci['sha256'] == current['sha256'] else item['status_source']
        bound_citations.append(dict(ci, **{k: source[k] for k in ('url', 'retrieved_at', 'http_status') if k in source}))
    facts = dict(item, relevance=receipt['relevance'], summary=receipt['summary'],
                 holding=receipt['holding'], disposition=receipt['disposition'], authors=receipt['authors'])
    review = dict(receipt, state_sha256=item['state_sha256'], pdf_sha256=current['sha256'], receipt_sha256=digest)
    scope = g.target(conn, registry['stream'])
    payload = {'status': 'incomplete', 'contract': scope, 'drafts': [],
               'findings': [{'key': item['id'], 'kind': 'opinion', 'facts': facts,
                             'citations': bound_citations or [citation]}],
               'checks': [{'id': 'opinion-review:'+item['id'], 'status': 'verified' if receipt['relevance'] != 'uncertain' else 'incomplete',
                           'checked_at': h.now(), 'hashes': [current['sha256']]},
                          {'id': 'report-review-and-publication', 'status': 'incomplete'}],
               'opinion_review': review}
    return h.record(conn, stream=registry['stream'], mode='manual_research', scope=scope,
                    run_id='opinion-review:'+digest, payload=payload,
                    artifacts={digest: h.canonical(receipt).encode()})


def accept_review(conn, registry, receipt):
    conn.execute('BEGIN IMMEDIATE')
    try:
        result = _accept_review(conn, registry, receipt)
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
