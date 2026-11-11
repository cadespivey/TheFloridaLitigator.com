"""Maintenance-only lossless projections and exact quotation selection.

Ordinary source/opinion models use compact_review, not fragment navigation.

These files are reading aids, never change/relevance verdicts or review proof.
Original packets, alignments and source-gate validators remain authoritative.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

from flwu import history as h

MAX_FILE_BYTES = 8192
FRAGMENT_BYTES = 4096
PAGE_ENTRIES = 6


def _inside(path, run):
    path = Path(path).resolve()
    if not path.is_relative_to(Path(run).resolve()):
        raise ValueError('Review evidence paths must stay inside the run directory')
    return path


def _save(folder, value, suffix='.json'):
    from flwu.workflow import write
    if suffix == '.json':
        path = folder / (h.sha(value) + suffix)
        write(path, value, immutable=True)
    else:
        from flwu.derived_cache import write_bytes
        raw = value.encode('utf-8')
        path = folder / (h.sha(raw) + suffix)
        if path.exists() and path.read_bytes() != raw:
            raise ValueError('Immutable review fragment differs: ' + str(path))
        write_bytes(path, raw)
    raw = path.read_bytes()
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError('Review evidence file exceeds its byte limit')
    return dict(path=str(path), sha256=h.sha(raw), bytes=len(raw))


def _pages(folder, entries):
    """A linked index keeps even very large evidence manifests bounded."""
    following = None
    for start in reversed(range(0, len(entries), PAGE_ENTRIES)):
        following = _save(folder, dict(entries=entries[start:start+PAGE_ENTRIES], next=following))
    return dict(count=len(entries), first=following)


def _fragments(text):
    # Chunk Unicode characters without losing/replacing bytes or splitting UTF-8.
    position = 0
    while position < len(text):
        end = min(len(text), position + FRAGMENT_BYTES)
        while len(text[position:end].encode('utf-8')) > FRAGMENT_BYTES:
            end = position + max(1, (end-position)//2)
        yield position, end, text[position:end]
        position = end


def _value(folder, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n').encode()
    if len(raw) <= MAX_FILE_BYTES:
        return dict(format='json', **_save(folder, value))
    text = raw.decode('utf-8')
    parts = [dict(start_char=a, end_char=b, **_save(folder, fragment, '.txt'))
             for a, b, fragment in _fragments(text)]
    return dict(format='json_text_fragments', serialized_sha256=h.sha(raw),
                characters=len(text), parts=_pages(folder, parts))


def project(folder, alignment=None, texts=None, changed_text=None):
    """Return a small manifest; all referenced evidence files are <=8 KiB."""
    folder = Path(folder)
    groups = []
    for group in (alignment or {}).get('groups', []):
        encoded = (json.dumps(group, ensure_ascii=False, indent=2, sort_keys=True)+'\n').encode()
        if len(encoded) <= MAX_FILE_BYTES:
            groups.append(dict(id=group['id'], kind=group['kind'], format='complete_group', **_save(folder, group)))
            continue
        fields = [dict(field=key, value=_value(folder, value))
                  for key, value in group.items() if key not in ('id', 'kind')]
        card = dict(id=group['id'], kind=group['kind'], fields=_pages(folder, fields))
        groups.append(dict(id=group['id'], kind=group['kind'], format='field_index', **_save(folder, card)))
    manifest = dict(schema_version=1, max_file_bytes=MAX_FILE_BYTES,
                    alignment_sha256=h.sha(alignment) if alignment is not None else None,
                    groups=_pages(folder, groups), texts={})
    if alignment is None and changed_text:
        manifest['changed_text'] = {side: _value(folder, lines) for side, lines in changed_text.items()}
    for side, binding in (texts or {}).items():
        path = Path(binding['path'])
        raw = path.read_bytes()
        if h.sha(raw) != binding['text_sha256']:
            raise ValueError('Extraction hash mismatch while projecting ' + side)
        text = raw.decode('utf-8')
        parts = [dict(start_char=a, end_char=b, **_save(folder, fragment, '.txt'))
                 for a, b, fragment in _fragments(text)]
        manifest['texts'][side] = dict(binding, characters=len(text), fragments=_pages(folder, parts))
    return _save(folder, manifest)


def bindings(task):
    inputs = task['inputs']
    observation = inputs.get('observation') or inputs.get('source_observation') or {}
    result = {}
    for side, prefix in [('current', ''), ('previous', 'previous_')]:
        path = inputs.get(side+'-text_path') or (inputs.get('opinion_text_path') if side == 'current' else None)
        if path and observation.get(prefix+'text_sha256'):
            result[side] = dict(path=path, sha256=observation.get(prefix+'sha256'),
                               text_sha256=observation[prefix+'text_sha256'])
            if side == 'current':
                result[side].update({k: observation[k] for k in ('url','retrieved_at','http_status') if k in observation})
    return result


def augment(config, task, overview, alignment=None):
    """New guide only: do not change legacy packet IDs, schemas or receipts."""
    from flwu.workflow import write
    from flwu.personnel_review import new_template, existing_template
    guide = copy.deepcopy(overview)
    guide['guide_version'] = 7
    folder = Path(task['packet_path']).parent / 'evidence-v7'
    texts = bindings(task)
    guide['evidence_packets'] = project(folder, alignment, texts, task['inputs'].get('changed_text_lines'))
    guide['quote_bindings'] = texts
    # Keep full artifacts available for escalation without inviting a full dump.
    guide['audit_evidence'] = {key: guide.pop(key) for key in ('aligned_review','aligned_groups') if key in guide}
    guide.pop('aligned_instructions', None)
    guide['evidence_instructions'] = [
        'Open evidence_packets.path, then its groups.first index. Follow every next pointer. A complete_group is one entire small group file; a field_index card links every field/value fragment of a larger group. Read the whole group before completing it. File hashes/counts bind coverage, not significance.',
        'A json_text_fragments value is the complete serialized JSON split at Unicode character offsets. Read every part in order; no part is a summary. When changed_text is supplied, inspect all of it. Text fragments cover the acquired extraction for selective context/quote lookup; they do not require rereading unchanged content. Unknown or decoding-limited evidence remains unresolved until inspected.',
        'Do not dump audit_evidence, the original packet, whole alignments or all prior findings. Use those originals only for a specific missing context/decoding question. Never infer omitted content from truncated tool output.',
        'For a blank quote, select exact extraction lines or absolute character offsets with workflow quote. Copy its support or citation object mechanically; never retype, normalize whitespace or invent timestamps. Selection is not substantive review.',
    ]
    if task['kind'] == 'source_review':
        templates = {}
        for kind in ('judge','clerk'):
            value = new_template(kind)
            path = folder / ('new-'+kind+'-'+h.sha(value)+'.json')
            write(path, value, immutable=True)
            templates[kind] = str(path)
        existing = []
        for prior in task['inputs'].get('prior_findings', []):
            if prior['kind'] not in ('judge','clerk'): continue
            value = existing_template(prior)
            path = folder / ('existing-person-'+h.sha(value)+'.json')
            write(path, value, immutable=True)
            existing.append(dict(key=prior['key'], path=str(path)))
        # Link templates individually instead of embedding full personnel facts.
        guide['personnel_templates'] = dict(new=templates, existing=_pages(folder, existing))
        guide['personnel_instructions'] = [
            'New directory people use kind judge or clerk and their own stable person- key; personnel_change is not a directory person. Choose the role from evidence. A successor is a distinct person, never a rename of the predecessor.',
            'For an existing person use the indexed existing-person template; it preserves ALL nested facts and expected_version. Templates deliberately leave citations empty: supply current acquired evidence, not stale citation bindings.',
            'New templates include role-specific contact slots marked unreviewed. Fill facts.name and supported fields; remove slots you did not review. A contact object has value, status verified, citation (also in findings.citations); explicit not_published needs citation and a search_log. Unreviewed is a draft marker, never an accepted absence. Use human office labels such as office_phone/chambers_address, not source-provenance labels.',
            'Preserve date meanings and conflicts. Selection is not effective service; a previous job is not a current assignment. Reconcile the named office roster separately; this template does not authorize removing a predecessor or inventing missing contacts.',
        ]
    guide['reading_order'] = [
        'Read research_scope, source_role when present, and the output contract first. Copy the returned receipt template to the draft path; do not edit evidence/templates.',
        'Read evidence_instructions and the small evidence_packets manifest. Finish one group and its fragments before the next. Existing review gates still apply; unchanged hashes were already handled by code.',
        'For an affected person read personnel_instructions and just that person template/prior finding. Save a compact checkpoint containing completed group IDs and remaining evidence pointers across compaction.',
    ]
    path = Path(task['packet_path']).with_name('review-overview-v7-'+h.sha(guide)+'.json')
    # The command is generated outside the hashed guide to avoid self-reference.
    write(path, guide, immutable=True)
    return path


def quote(run, guide_path, side, *, start_line=None, end_line=None, start_char=None, end_char=None):
    """Read-only exact selection. Final acceptance still checks the database."""
    guide = json.loads(_inside(guide_path, run).read_text())
    binding = guide.get('quote_bindings', {}).get(side)
    if not binding: raise ValueError('No acquired extraction for this side in the current guide')
    raw = _inside(binding['path'], run).read_bytes()
    if h.sha(raw) != binding['text_sha256']: raise ValueError('Extraction hash mismatch; do not quote altered evidence')
    text = raw.decode('utf-8')
    lines = start_line is not None or end_line is not None
    chars = start_char is not None or end_char is not None
    if lines == chars: raise ValueError('Choose one complete line range or character range')
    if lines:
        values = text.splitlines(keepends=True)
        if type(start_line) is not int or type(end_line) is not int or not 1 <= start_line <= end_line <= len(values):
            raise ValueError('Line range is 1-based, inclusive and must exist in the extraction')
        selected = ''.join(values[start_line-1:end_line])
        locator = f'{side} extraction lines {start_line}-{end_line}'
    else:
        if type(start_char) is not int or type(end_char) is not int or not 0 <= start_char < end_char <= len(text):
            raise ValueError('Character range is 0-based, end-exclusive and must exist in the extraction')
        selected = text[start_char:end_char]
        locator = f'{side} extraction characters {start_char}:{end_char}'
    if not selected.strip() or len(selected.encode('utf-8')) > MAX_FILE_BYTES:
        raise ValueError('Select a nonblank quote no larger than 8 KiB; narrow the range')
    support = dict(sha256=binding['sha256'], text_sha256=binding['text_sha256'], quote=selected, locator=locator)
    citation = (dict(support, **{k: binding[k] for k in ('url','retrieved_at','http_status') if k in binding})
                if all(binding.get(k) for k in ('url','retrieved_at')) else None)
    return dict(support=support, citation=citation,
                instruction='Selection only; verify relevance and use existing receipt fields. citation=null means full acquisition metadata is unavailable here; do not invent it.')
