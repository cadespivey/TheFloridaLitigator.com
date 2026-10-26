"""Explicit, acquisition-bound source failures; never successful coverage."""
from __future__ import annotations

import json
import re
from urllib.parse import urljoin
from flwu import history as h
from flwu.evidence_binding import AcquisitionIndex

STATUS = 'reviewed_source_limitation'


def _discovery_path(conn, target, task, limitation, through_seq):
    """Prove each dependency from original bytes, not hostname similarity."""
    path = limitation.get('discovery_path')
    if not isinstance(path, list) or not path or len(path) > 8:
        raise ValueError('A linked failure requires a bounded saved discovery path')
    expected = task['url']
    seen = set()
    fields = {'url', 'observation_capture_id', 'sha256', 'text_sha256',
              'retrieved_at', 'http_status', 'reference', 'target_url'}
    for hop in path:
        if not isinstance(hop, dict) or set(hop) != fields or hop['url'] != expected:
            raise ValueError('Discovery path must start at the exact task URL and remain contiguous')
        if expected in seen:
            raise ValueError('Discovery path contains a cycle')
        seen.add(expected)
        row = conn.execute('SELECT c.*,s.scope FROM captures c JOIN streams s USING(stream) WHERE capture_id=?',
                           (hop['observation_capture_id'],)).fetchone()
        if (row is None or (through_seq is not None and row['seq'] > through_seq)
                or json.loads(row['scope']).get('target_stream') != target):
            raise ValueError('Discovery observation is missing, out of stream, or newer than report')
        obs = json.loads(row['payload']).get('source_gate', {})
        if (obs.get('success') is not True or obs.get('http_status') != 200
                or any(hop[k] != obs.get(k) for k in
                       ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status'))):
            raise ValueError('Discovery path differs from successful saved acquisition')
        raw = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (hop['sha256'],)).fetchone()
        if raw is None or h.sha(raw[0]) != hop['sha256']:
            raise ValueError('Discovery original is missing or changed')
        reference = hop['reference']
        if (not isinstance(reference, str) or not reference
                or not any(delimiter + reference.encode() + delimiter in raw[0]
                           for delimiter in (b'"', b"'", b'\\"'))
                or urljoin(hop['url'], reference) != hop['target_url']):
            raise ValueError('Discovery reference is not present in the original or targets another URL')
        expected = hop['target_url']
    if expected != limitation['url'] or expected in seen:
        raise ValueError('Discovery path does not end at the exact failed URL')


def validate(conn, target, task, limitation, *, through_seq=None):
    fields = {'task_id', 'url', 'observation_capture_id', 'sha256', 'text_sha256',
              'retrieved_at', 'http_status', 'category', 'reviewer', 'reason',
              'reviewed_scope', 'pending_work', 'invalid_content_quote', 'alternatives'}
    if not isinstance(limitation, dict) or set(limitation) not in (fields, fields | {'discovery_path'}):
        raise ValueError('Use the exact source-limitation template')
    if task.get('kind') != 'source' or limitation['task_id'] != task['id']:
        raise ValueError('Limitation must identify its exact source task and URL')
    if 'discovery_path' in limitation:
        _discovery_path(conn, target, task, limitation, through_seq)
    elif limitation['url'] != task.get('url'):
        raise ValueError('Limitation must identify its exact source task and URL')
    if any(not isinstance(limitation[k], str) or not limitation[k].strip()
           for k in ('reviewer', 'reason', 'reviewed_scope', 'observation_capture_id')):
        raise ValueError('Limitation needs a reviewer, reason, scope and saved observation')
    if limitation['pending_work'] != []:
        raise ValueError('Available unread material or unfinished repair remains pending')
    if limitation['category'] not in ('retrieval_failed', 'invalid_content'):
        raise ValueError('Unreviewed material and incomplete extraction are not source limitations')
    row = conn.execute('SELECT c.*,s.scope FROM captures c JOIN streams s USING(stream) WHERE capture_id=?',
                       (limitation['observation_capture_id'],)).fetchone()
    if (row is None or (through_seq is not None and row['seq'] > through_seq)
            or json.loads(row['scope']).get('target_stream') != target):
        raise ValueError('Limitation observation is missing, belongs to another stream, or postdates report')
    observation = json.loads(row['payload']).get('source_gate')
    keys = ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status')
    if not observation or any(limitation[k] != observation.get(k) for k in keys):
        raise ValueError('Limitation differs from exact saved acquisition metadata')
    for key in ('sha256', 'text_sha256'):
        if limitation[key] is not None:
            artifact = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (limitation[key],)).fetchone()
            if artifact is None or h.sha(artifact[0]) != limitation[key]:
                raise ValueError('Limitation original or extraction artifact missing or changed')
    quote = limitation['invalid_content_quote']
    if limitation['category'] == 'retrieval_failed':
        if observation.get('success') is not False or quote is not None:
            raise ValueError('A successful acquisition cannot be relabeled a retrieval failure')
    else:
        if observation.get('success') is not True or observation.get('http_status') != 200:
            raise ValueError('Invalid-content review requires the saved HTTP200 body')
        if not isinstance(quote, str) or not quote.strip() or not limitation['text_sha256']:
            raise ValueError('Invalid-content review requires a quoted saved extraction')
        text = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (limitation['text_sha256'],)).fetchone()[0].decode()
        signature = re.search(r'domain.{0,100}for sale|\A\s*(?:sign in|log in|access denied|captcha)|the page you have requested cannot be found',
                              quote[:500], re.IGNORECASE | re.DOTALL)
        if quote.strip() != text.strip() or not signature:
            raise ValueError('Quote does not substantiate invalid content; incomplete extraction is not excused')
    alternatives = limitation['alternatives']
    if not isinstance(alternatives, list):
        raise ValueError('Alternative evidence must be a list of separately bound citations')
    index = AcquisitionIndex(conn, target, through_seq=through_seq)
    for citation in alternatives:
        if not isinstance(citation, dict) or not citation.get('quote'):
            raise ValueError('Alternative evidence requires a supporting quotation')
        index.validate(citation)
    return h.sha(limitation)


def validate_checks(conn, row):
    payload = json.loads(row['payload'])
    tasks = {t['id']: t for t in payload.get('contract', {}).get('tasks', [])}
    limits = []
    for check in payload['checks']:
        if check['status'] == STATUS:
            task = tasks.get(check['id'])
            if task is None:
                raise ValueError('Source limitation has no contract task')
            limitation = check.get('limitation')
            digest = validate(conn, row['stream'], task, limitation, through_seq=row['seq'])
            limits.append(dict(task_id=task['id'], sha256=digest, limitation=limitation))
        elif check['status'] != 'verified':
            raise ValueError('Incomplete research cannot receive publication acceptance')
    return limits
