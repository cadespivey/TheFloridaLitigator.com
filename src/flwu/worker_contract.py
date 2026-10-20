"""Narrow worker contracts shared by research validation and controlled replay.

No executor is exposed to model output. Span IDs are resolved by trusted code.
"""
from datetime import date
import re

LEGAL_STATUSES = {'operative', 'future_effective', 'withdrawn', 'unknown'}
COUNTY_CIRCUITS = {'Duval': 4, 'Nassau': 4, 'Clay': 4, 'St. Johns': 7,
                   'Putnam': 7, 'Baker': 8, 'Union': 8}


def temporal_status(status, effective, cutoff):
    if status not in LEGAL_STATUSES:
        raise ValueError('legal_status must be operative, future_effective, withdrawn, or unknown')
    future = effective is not None and date.fromisoformat(effective) > date.fromisoformat(cutoff)
    if future and status not in {'future_effective', 'withdrawn'}:
        raise ValueError('Future-effective item cannot be described as operative at cutoff')
    if status == 'future_effective' and not future:
        raise ValueError('future_effective requires an effective date after the cutoff')


def negative_search(status, log):
    if status in {'no_published_procedure_located', 'not_published'} and (
            not isinstance(log, list) or not log or any(not isinstance(x, str) or not x.strip() for x in log)):
        raise ValueError('Negative finding requires a nonempty search log naming searched sources/terms')


def require_keys(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError('Required exact fields: ' + ', '.join(keys))


def span_citations(ids, spans):
    if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or i not in spans for i in ids):
        raise ValueError('citations must contain supplied span IDs, never paths or invented quotes')
    return [spans[i] for i in dict.fromkeys(ids)]


def validate_answer(answer, task, spans, start, end):
    """Validate a single worker answer; return it without repairing model facts."""
    if task['kind'] == 'candidate':
        require_keys(answer, ['id', 'decision', 'reason', 'publication_date', 'effective_date',
                            'legal_status', 'summary_spans', 'author', 'concurrence', 'citations', 'changes'])
        if answer['id'] != task['id'] or answer['decision'] not in {'include', 'exclude'}:
            raise ValueError('Candidate ID/decision mismatch')
        day = date.fromisoformat(answer['publication_date'])
        if task.get('publication_date') and answer['publication_date'] != task['publication_date']:
            raise ValueError('Publication date must match the acquired index date')
        if answer['decision'] == 'include' and not date.fromisoformat(start) <= day <= date.fromisoformat(end):
            raise ValueError('Included candidate outside publication window')
        temporal_status(answer['legal_status'], answer['effective_date'], end)
        if answer['legal_status'] == 'withdrawn' and date.fromisoformat(start) <= day <= date.fromisoformat(end) and answer['decision'] != 'include':
            raise ValueError('In-window withdrawal must be included as a withdrawal notice, not operative precedent')
        in_window = date.fromisoformat(start) <= day <= date.fromisoformat(end)
        expected_reason = 'outside_window' if not in_window else 'withdrawal_notice' if answer['legal_status'] == 'withdrawn' else 'in_window'
        if answer['reason'] != expected_reason:
            raise ValueError('reason must be the exact code ' + expected_reason + '; no free-form explanation')
        summary_refs = span_citations(answer['summary_spans'], spans)
        if not set(answer['summary_spans']) <= set(answer['citations']):
            raise ValueError('Every summary span must also appear in citations')
        primary = '\n'.join(v['quote'] for v in spans.values() if v['endpoint'] == 'opinions/'+task['id'])
        if 'Status: operative' in primary and answer['legal_status'] == 'unknown':
            raise ValueError('Source explicitly states Status: operative; unknown is not supported')
        for k in ('author', 'concurrence'):
            if answer[k] is not None and (not isinstance(answer[k], str) or answer[k] not in primary):
                raise ValueError(k + ' must be verbatim supported primary-source text or null')
        span_citations(answer['citations'], spans)
        if not isinstance(answer['changes'], list):
            raise ValueError('changes must be an array')
        for change in answer['changes']:
            require_keys(change, ['before', 'after', 'citations'])
            refs = span_citations(change['citations'], spans)
            if change['before'] == change['after']:
                raise ValueError('Unchanged before/after text is not a change; keep it in summary only')
            if not change['before'] or not change['after'] or not any('/prior-' in r['endpoint'] for r in refs):
                raise ValueError('Change requires before/after text and a prior-source citation')
    elif task['kind'] == 'judge':
        require_keys(answer, ['name', 'county', 'circuit', 'division', 'chambers_phone', 'address',
                            'assistant_name', 'assistant_contact', 'citations', 'procedure', 'governing_rules'])
        if answer['name'] != task['name'] or answer['county'] != task['county']:
            raise ValueError('Judge must match current roster task')
        if answer['circuit'] != COUNTY_CIRCUITS.get(answer['county']):
            raise ValueError('County/circuit mapping mismatch')
        for k in ('division', 'chambers_phone', 'address', 'assistant_name', 'assistant_contact'):
            if not isinstance(answer[k], str) or not answer[k].strip():
                raise ValueError('Missing contact: ' + k)
        refs = span_citations(answer['citations'], spans)
        # Contact values must be transcription from the current profile, never an archive.
        profile = '\n'.join(r['quote'] for r in refs if r['endpoint'] == task['profile'])
        for k in ('chambers_phone', 'assistant_name', 'address', 'division'):
            if answer[k] not in profile:
                matching = [sid for sid, ref in spans.items() if ref['endpoint'] == task['profile'] and answer[k] in ref['quote']]
                raise ValueError(k + ' lacks current-profile support in citations. Add these supplied supporting span IDs: ' + ', '.join(matching))
        for value in re.split(r';\s*', answer['assistant_contact']):
            if value.strip() not in profile:
                raise ValueError('Every assistant contact must be transcribed from cited current-profile spans')
        p = answer['procedure']
        require_keys(p, ['status', 'effective_date', 'legal_status', 'summary_spans', 'search_log', 'citations'])
        if p['status'] not in {'verified', 'no_published_procedure_located'}:
            raise ValueError('Procedure unresolved; coordinator keeps blocked tasks pending')
        negative_search(p['status'], p['search_log'])
        temporal_status(p['legal_status'], p['effective_date'], end)
        procedure_refs = span_citations(p['citations'], spans)
        allowed = [ep for ep in task['dependencies'] if ep.startswith('procedures/')]
        if not any(r['endpoint'] in allowed for r in procedure_refs):
            raise ValueError('Personal procedure requires its linked procedure/index source')
        if p['status'] == 'verified' and not any(r['endpoint'] in allowed and r['endpoint'] != 'procedures/index' for r in procedure_refs):
            raise ValueError('Circuit order or index alone cannot verify personal procedures')
        selected = span_citations(p['summary_spans'], spans)
        if not set(p['summary_spans']) <= set(p['citations']) or any(r['endpoint'] not in allowed for r in selected):
            raise ValueError('Procedure summary must select cited linked procedure/index spans')
        if not isinstance(answer['governing_rules'], list) or not answer['governing_rules']:
            raise ValueError('Governing rules required separately from individual procedure')
        for rule in answer['governing_rules']:
            require_keys(rule, ['summary_spans', 'citations'])
            selected = span_citations(rule['summary_spans'], spans)
            if not set(rule['summary_spans']) <= set(rule['citations']) or any(not r['endpoint'].startswith('circuits/') for r in selected):
                raise ValueError('Governing summary must select cited circuit-order spans')
            if not any(r['endpoint'].startswith('circuits/') for r in span_citations(rule['citations'], spans)):
                raise ValueError('Governing rules require a circuit source citation')
    else:
        raise ValueError('Unknown worker task kind')
    return answer
