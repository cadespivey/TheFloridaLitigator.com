"""Revalidate saved listing bytes without manufacturing an extraction event."""
from __future__ import annotations
import json

from flwu import history as h
from flwu import opinion_discovery as opinions


def page_binding(conn, event, capture_id, contract):
    capture = conn.execute('SELECT seq,stream,payload FROM captures WHERE capture_id=?', (capture_id,)).fetchone()
    if capture is None or json.loads(capture['payload']).get('opinion_discovery') != event:
        raise ValueError('Discovery page does not match its saved acquisition capture')
    saved_contract = None
    for row in conn.execute('SELECT payload FROM captures WHERE stream=? AND seq<? ORDER BY seq DESC',
                            (capture['stream'], capture['seq'])):
        prior = json.loads(row['payload']).get('opinion_discovery', {})
        if prior.get('kind') == 'contract' and prior.get('run_id') == event.get('run_id'):
            saved_contract = prior['contract']
            break
    if saved_contract != contract:
        raise ValueError('Discovery page contract is missing or differs from the saved run')
    if event.get('kind') != 'page' or event.get('complete') is not True:
        raise ValueError('Discovery page was not successfully parsed')
    source = event.get('source', {})
    if source.get('success') is not True or source.get('http_status') != 200:
        raise ValueError('Discovery page transport failed')
    courts = {c['id']: c for c in contract['courts']}
    court = courts[event['court']]
    channel = event['channel']
    if channel not in (court['id']+':listing', court['id']+':inactive'):
        raise ValueError('Discovery channel does not match court')
    prefix = channel+':'
    checkpoint = event['checkpoint']
    if not checkpoint.startswith(prefix) or not checkpoint[len(prefix):].isdigit():
        raise ValueError('Invalid discovery page checkpoint')
    offset = int(checkpoint[len(prefix):])
    inactive = channel.endswith(':inactive')
    expected_url = opinions.query_url(court, contract['bounds'], offset,
                                      contract['page_size'], inactive)
    if source.get('url') != expected_url or not source.get('retrieved_at'):
        raise ValueError('Discovery source does not match saved query contract')
    digest = event.get('sha256')
    row = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (digest,)).fetchone()
    if row is None or h.sha(row[0]) != digest:
        raise ValueError('Discovery original artifact missing or changed')
    raw = row[0]
    raw.decode('utf-8')  # Text citations use these exact bytes, not a new extraction.
    total, entries = opinions.parse_page(raw, court, contract['bounds'], offset, inactive)
    ids = [e['id'] for e in entries]
    saved_entries = [{k: v for k, v in entry.items() if k != 'status_source'}
                     for entry in event.get('entries', [])]
    expected_entries = [entry for entry in entries if entry['published_date'] <= contract['bounds']['end']]
    if (event.get('total') != total or event.get('returned') != len(entries)
            or event.get('page_ids') != ids or len(ids) != len(set(ids))
            or saved_entries != expected_entries):
        raise ValueError('Discovery page metadata differs from original response')
    if offset + len(entries) > total or (not entries and offset != total):
        raise ValueError('Premature empty page or inconsistent total')
    return dict(url=source['url'], retrieved_at=source['retrieved_at'],
                http_status=source['http_status'], success=True,
                sha256=digest, text_sha256=digest,
                acquisition_capture_id=capture_id,
                extraction='original UTF-8 JSON bytes')


def validate_channel(conn, captures, contract, channel):
    """Validate a complete channel; a valid page alone never proves coverage."""
    pages = {}
    run_ids = set()
    for capture_id, event in captures:
        if event.get('kind') == 'page' and event.get('channel') == channel:
            key = event['checkpoint']
            if key in pages:
                raise ValueError('Duplicate discovery page checkpoint')
            pages[key] = (capture_id, event)
            run_ids.add(event.get('run_id'))
    if len(run_ids) != 1:
        raise ValueError('Discovery channel must belong to one saved run')
    offset, total, seen, bindings = 0, None, set(), []
    while True:
        pair = pages.pop(channel+':'+str(offset), None)
        if pair is None:
            raise ValueError('Discovery channel has a missing page')
        capture_id, event = pair
        bindings.append(page_binding(conn, event, capture_id, contract))
        if total is not None and total != event['total']:
            raise ValueError('Discovery pagination total drift')
        total = event['total']
        if seen.intersection(event['page_ids']):
            raise ValueError('Duplicate discovery identities across pages')
        seen.update(event['page_ids'])
        offset += event['returned']
        if offset == total:
            break
    if pages or len(seen) != total:
        raise ValueError('Discovery channel has extra pages or inconsistent identities')
    return bindings
