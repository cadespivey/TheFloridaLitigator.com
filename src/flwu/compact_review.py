"""One evidence view and a short semantic answer; existing receipts stay internal.

This adapter copies acquired evidence. It does not decide relevance, explain raw
changes, accept uncertain work, or relax the source/opinion validators.
"""
from __future__ import annotations
import copy
import difflib
import json
import re
from pathlib import Path
from flwu import history as h, source_gate as gate

VERSION = 1
MAX_EVIDENCE_CHARACTERS = 128_000
CONTEXT_LINES = 16

# Named contact fields whose text may differ from the acquired page in
# formatting whitespace only. Punctuation, digits, spelling, case, URL- and
# email-bearing values and every other field remain exact.
CONTACT_FIELDS = frozenset({
    'office_phone', 'office_address', 'office_contact',
    'chambers_phone', 'chambers_address', 'chambers_contact',
    'assistant_name', 'assistant_phone', 'assistant_address', 'assistant_contact',
})


def _whitespace_form(value):
    """Collapse every whitespace run (spaces, tabs, newlines, NBSP) to single
    spaces. Used for contact comparison only; submitted values are never rewritten."""
    return ' '.join(value.split())


def _contact_whitespace_allowed(field, value):
    # Contact descriptions can contain embedded or uppercase URLs, not only a
    # value beginning with a lowercase scheme. Those still need exact support.
    return field in CONTACT_FIELDS and not re.search(r'https?://|mailto:|@', value, re.I)


def _contact_text_supported(field, value, quote):
    """Exact substring matching stays the first route. Whitespace-equivalent
    matching is a fallback for named contact fields only; it never applies to
    narrative fields or URL/email-bearing values."""
    if value in quote:
        return True
    if not _contact_whitespace_allowed(field, value):
        return False
    return _whitespace_form(value) in _whitespace_form(quote)


def _unique(values):
    return list({h.sha(value): value for value in values}.values())


def _ranges(before, after, side):
    lines = after if side == 'current' else before
    windows = []
    for tag, a, b, c, d in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if tag == 'equal': continue
        start, end = (c, d) if side == 'current' else (a, b)
        if not lines: continue
        start, end = max(0, start-CONTEXT_LINES), min(len(lines), end+CONTEXT_LINES)
        if windows and start <= windows[-1][1]: windows[-1][1] = max(windows[-1][1], end)
        else: windows.append([start, end])
    return windows


def _previous_source(conn, source):
    if not source.get('previous_text_sha256'):return None
    row=conn.execute("SELECT payload FROM captures WHERE stream=(SELECT stream FROM captures WHERE capture_id=?) AND json_extract(payload,'$.source_gate.url')=? AND json_extract(payload,'$.source_gate.sha256')=? AND json_extract(payload,'$.source_gate.text_sha256')=? AND json_extract(payload,'$.source_gate.success')=1 AND seq<(SELECT seq FROM captures WHERE capture_id=?) ORDER BY seq DESC LIMIT 1",(source.get('capture_id'),source.get('url'),source.get('previous_sha256'),source.get('previous_text_sha256'),source.get('capture_id'))).fetchone()
    return json.loads(row[0])['source_gate'] if row else None


def _source_context(source):
    """Describe the code-owned task purpose, without deciding source meaning."""
    comparison = source.get('change') == 'changed'
    context = dict(
        purpose='comparison' if comparison else 'baseline',
        previous_text_available=bool(source.get('previous_text_sha256')),
        instructions=(
            'Compare the acquired previous and current passages. Missing required comparison evidence remains unresolved.'
            if comparison else
            'Establish the current source baseline; no earlier passage is required. Record supported material information. '
            'If the complete acquired page contains only navigation and no substantive information, explain that briefly; '
            'no_material_change means no material finding in this baseline, not proof that the website or law never changed. '
            'Missing expected body content or failed extraction remains insufficient_evidence.'),
    )
    from flwu.opinion_discovery import COURTS
    court = next((court for court in COURTS if source.get('url') in court.get('notice_urls', [])), None)
    if court:
        context.update(court=court['id'], role='configured_opinion_notice_page',
                       role_instructions='Review acquired standalone notices or release-page content here. '
                       'Official opinion listing/status discovery and PDF review are separate tasks. '
                       'This page review does not certify their coverage. The configured role alone does not prove a complete extraction.')
    return context


def prepare(conn, task):
    """Reproducible acquired evidence and hidden bindings; no files or decisions."""
    kind, inputs = task['kind'], task['inputs']
    if kind not in ('source_review', 'opinion_review'):
        from flwu.publication_driver import prepare_card
        return prepare_card(conn, task)
    exception = None
    if kind == 'source_review' and ('raw_change_review' in task['receipt_template'] or inputs.get('raw_comparison_basis')):
        exception = 'Changed originals require technical/nontext inspection; equal extracted text is not a completed review.'
    obs = inputs.get('observation') or inputs.get('source_observation') or {}
    previous_source=_previous_source(conn,obs) if kind=='source_review' else None
    evidence, bindings = [], {}
    texts = {}
    sources = [('current', obs, '')]
    if kind == 'source_review' and obs.get('previous_text_sha256'):
        sources.append(('previous', obs, 'previous_'))
    if kind == 'opinion_review':
        status = inputs['opinion'].get('status_source', {})
        if status.get('text_sha256'): sources.append(('status', status, ''))
    for side, source, prefix in sources:
        digest = source.get(prefix+'text_sha256')
        if not digest:
            exception = exception or 'Acquired extraction is unavailable; retain this source as unresolved.'
            continue
        try:texts[side] = gate.blob(conn, digest).decode('utf-8')
        except (ValueError,UnicodeError) as exc:
            exception = exception or 'Acquired extraction cannot be read: '+str(exc)
    # Oversized originals do not become excerpts with a false completeness claim.
    # For changed sources only the complete changed ranges + context are needed.
    if not exception:
        before = texts.get('previous', '').splitlines(keepends=True)
        after = texts.get('current', '').splitlines(keepends=True)
        selected = {}
        for side, source, prefix in sources:
            if side not in texts: continue
            lines = texts[side].splitlines(keepends=True)
            spans = (_ranges(before, after, side) if kind == 'source_review' and before and before != after
                     else [[0, len(lines)]])
            selected[side] = [(a, b, ''.join(lines[a:b])) for a, b in spans]
        size = sum(len(text) for parts in selected.values() for _, _, text in parts)
        if size > MAX_EVIDENCE_CHARACTERS:
            exception = f'Evidence needs {size} characters, beyond the self-contained card limit; use an explicit extended review, not silent truncation.'
        else:
            for side, source, prefix in sources:
                for start, end, text in selected.get(side, []):
                    if not text: continue
                    identifier = {'current':'C', 'previous':'P', 'status':'S'}[side] + str(1+sum(e['side']==side for e in evidence))
                    evidence.append(dict(id=identifier, side=side, passage=text))
                    binding = dict(sha256=source[prefix+'sha256'], text_sha256=source[prefix+'text_sha256'],
                                   quote=text, locator=f'{side} extraction lines {start+1}-{end}')
                    transport=(previous_source or {}) if prefix else source
                    for key in ('url','retrieved_at','http_status'):
                        if key in transport: binding[key] = transport[key]
                    bindings[identifier] = binding
            if not any(e['side']=='current' for e in evidence):
                exception = 'No nonempty acquired current passage is available.'
            if kind == 'source_review':
                for side, changed in inputs.get('changed_text_lines', {}).items():
                    if any(not any(line in e['passage'] for e in evidence if e['side']==side) for line in changed):
                        exception = 'Complete changed-line evidence does not fit the current card; extended review required.'
    people, prior = [], {}
    for finding in inputs.get('prior_findings', []):
        if finding['kind'] not in ('judge','clerk'): continue
        ref = 'person'+str(len(people)+1)
        prior[ref] = copy.deepcopy(finding)
        fields = {key: value.get('value') for key, value in finding['facts'].get('fields', {}).items() if isinstance(value, dict)}
        people.append(dict(person=ref, name=finding['facts'].get('name'), kind=finding['kind'], fields=fields))
    if kind == 'source_review':
        template = dict(decision='', summary='', evidence=[], people=[])
        context = _source_context(obs)
        question = ('What material civil/commercial law, procedure, or court-personnel information does this initial source baseline establish?'
                    if context['purpose']=='baseline' else
                    'Does this source contain a material civil/commercial law, procedure, or court-personnel change?')
        question += ' Describe supported material information and practical effect, or give a brief supported no-material-finding reason.'
        answer_help = {'decision':['no_material_change','material_change','insufficient_evidence'],
            'evidence':'Choose supplied C/P evidence IDs; code copies quotes and provenance.',
            'people':'Only changed judge/clerk records. Prefer chambers_phone/chambers_address/assistant_name/assistant_contact for judges and office_phone/office_address/office_contact for clerks; retain existing field names when updating. No source-provenance labels. Each: person (supplied person reference or new), name, kind (judge/clerk), evidence (IDs), fields {field_name:{value:...,evidence:ID}}. Omit unreviewed fields. A successor is new, not a rename.'}
        answer_help['contacts']='For a new person include current phone, address, email and assistant contacts explicitly supported in these passages, even if unchanged on the page. Phone, address and assistant contact text may differ from the page in formatting whitespace only (spaces, tabs, line breaks, nonbreaking spaces); spelling, case, punctuation, digits, emails, URLs and evidence must stay exact. Retain address line breaks when useful. Never invent missing contacts or inherit predecessor personal contacts. Existing-person updates preserve untouched fields. Omit career biography.'
        answer_help['repair']='A field rejection names the person and fields.<name>. Repair that field using this card and retain other supported fields. Do not drop all contacts or inspect code/raw packets or write diagnostic scripts.'
    else:
        template = dict(relevance='', summary='', holding='', disposition='', authors=[], evidence=[])
        question = 'Is this opinion relevant to civil/commercial litigation? If relevant, state its supported holding, disposition, practical significance, and author names. Keep issuance/effective/status dates distinct.'
        answer_help = {'relevance':['relevant','not_relevant','uncertain'],
            'scope':'General civil and appellate procedure matters, including individual and small-claims parties, are in scope. No new rule or case-specific application is required. Include relevant civil/commercial citation affirmances that state or quote applicable legal principles.',
            'bare_disposition':'Distinguish a bare PCA (Affirmed, without substantive reasons or stated applicable principles) from a citation affirmance quoting a civil rule, such as a contract-enforcement or preservation principle. The latter has substance to summarize even without novel law or case-specific analysis. A complete bare PCA may be not_relevant; do not research its underlying lawsuit.',
            'uncertain':'Missing/unreadable evidence or genuinely unresolved substantive significance stays uncertain. A documented source difference alone does not make a complete review incomplete; code never classifies a case automatically.',
            'status_changes':'A material official correction, withdrawal or status change may itself warrant an update even with unchanged PDF bytes or no new merits discussion.',
            'labels':'A Citation classification, PER CURIAM byline or absent reporter citation does not establish unpublished or nonprecedential status; do not infer those labels or finality.',
            'holding':'Concise operative facts and rule with express qualifications or exceptions; example language is illustrative, not exclusive; keep ordinarily/generally/on-this-record limits from the opinion.',
            'summary':'Practical effect, preserving the holding\'s material qualifications and exceptions, including ordinarily/generally/on-this-record limits. Such as veil piercing is an example, never an exclusive only-through-veil-piercing test. Do not broaden the rule when shortening it. No duplicate holding, research bookkeeping or party-name/source reconciliation narratives.',
            'disposition':'Court action only; issuance/effective/status dates are separate source metadata.',
            'authors':'Byline names only, not the panel as authors; empty for per curiam without an identified author. Uncertain remains unresolved.',
            'not_relevant':'Usually one supported sentence, e.g. Criminal postconviction appeal; outside civil/commercial scope. Leave holding empty; disposition may state the action; authors only if supplied. No specialized merits, biography or repeated status/date detail. Do not characterize underlying-order finality unless the acquired evidence expressly establishes it; an opinion rehearing-finality warning does not.',
            'evidence':'Choose supplied C/S evidence IDs; relevant opinions must cite the opinion (C).'}
    card = dict(question=question, source=obs.get('url'), evidence=evidence,
                answer=template, answer_help=answer_help,
                instructions='Use only these acquired passages. Do not write scripts, hashes or citations. Select evidence IDs and provide a concise semantic answer. Unknown significance is unresolved; do not invent technical or legal causes. A recorded official-source conflict alone is not missing evidence; preserve both statements without deciding control. Read the complete card; never infer truncated content.')
    if kind == 'source_review':
        card['source_context'] = context
    if not exception and kind=='source_review' and 'links' in obs:
        current_links=set(obs['links'])
        prior_links=set(previous_source['links']) if previous_source is not None and 'links' in previous_source else None
        added=sorted(current_links-(prior_links or set()));removed=sorted((prior_links or set())-current_links)
        if added or removed:
            card['link_changes']=dict(current_only=added,previous_only=removed,previous_inventory_known=prior_links is not None,
                evidence='Use current passage IDs for current URLs; URLs are verified against the acquired link inventory. Target document content/accessibility is not established. Unknown previous inventory does not prove a newly added link.')
    if not exception:
        answer_help['reviewer']='Optional actual model name if exposed by this session; otherwise code records identity unavailable. Do not inspect runtime files to find it.'
    if people: card['existing_people'] = people
    if kind == 'opinion_review':
        item = inputs['opinion']
        card['opinion'] = {k:item[k] for k in ('court','case_number','title','published_date','status') if k in item}
        if inputs.get('prior_review'):
            card['previous_review'] = {k:inputs['prior_review'][k] for k in ('summary','holding','disposition','authors') if k in inputs['prior_review']}
    if len(json.dumps(card,ensure_ascii=False)) > MAX_EVIDENCE_CHARACTERS:
        exception = exception or 'Task context exceeds the self-contained card limit; extended review required.'
    if exception:
        card = dict(question='Technical/evidence exception; do not provide a no-change verdict.', source=obs.get('url'), reason=exception,
                    instructions='Originals remain pending. Continue other ordinary tasks; this source requires explicit maintenance/extended review before completion.')
    return dict(version=VERSION, packet_sha256=task['packet_sha256'], card=card, bindings=bindings,
                prior_people=prior, answer_template=template, exception=exception)


def project(conn, config, task):
    from flwu import workflow as w
    from flwu.workflow_short import checked_command
    if task['kind']=='source_review':
        gate.export_task(conn,task['inputs'],Path(config['run_dir'])/'source-reviews',task['receipt_template']['review_protocol'])
    elif task['kind']=='opinion_review':
        from flwu import update
        update.export_opinion_task(conn,task['inputs'],Path(config['run_dir']))
    bundle = prepare(conn, task)
    folder = Path(task['packet_path']).parent
    w.write(task['packet_path'], task, immutable=True)
    digest = h.sha(bundle)
    path = folder/f'short-review-v{VERSION}-{digest}.json'
    card_path = folder/f'review-card-v{VERSION}-{digest}.json'
    answer_path = folder/f'answer-template-v{VERSION}-{digest}.json'
    w.write(path, bundle, immutable=True); w.write(card_path, bundle['card'], immutable=True)
    w.write(answer_path, bundle['answer_template'], immutable=True)
    return dict(kind=task['kind'], identity=task['identity'], packet=task['packet_path'],
                review_card=str(card_path), answer_template=str(answer_path), save_answer=str(folder/'answer.json'),
                answer_binding=str(path), exception=bundle['exception'],
                command=checked_command(config, 'answer', packet=task['packet_path'],
                                        answer=folder/'answer.json'))


def _text(value, label):
    if not isinstance(value, str) or not value.strip(): raise ValueError(label+' must be nonempty text')
    return value


def _refs(answer, bundle, *, full=False):
    ids = answer if isinstance(answer, list) else [answer]
    if not ids or any(not isinstance(i,str) or i not in bundle['bindings'] for i in ids):
        raise ValueError('Choose only the evidence IDs supplied by this task card')
    result = []
    for key in ids:
        source = bundle['bindings'][key]
        keys = ('url','sha256','text_sha256','retrieved_at','http_status','quote','locator') if full else ('sha256','text_sha256','quote','locator')
        result.append({k:source[k] for k in keys if k in source})
    return _unique(result)


def _slug(value):
    return re.sub(r'[^a-z0-9]+','-',value.casefold()).strip('-') or 'person'


def compile_answer(task, bundle, answer):
    """Copy metadata/evidence and preserve explicit model meaning, never infer it."""
    if bundle['packet_sha256'] != task['packet_sha256']:
        raise ValueError('Short answer is bound to another task')
    if bundle['exception']: raise ValueError(bundle['exception'])
    if not isinstance(answer,dict): raise ValueError('Answer must be an object')
    if task['kind'] not in ('source_review','opinion_review'):
        from flwu.publication_driver import compile_card
        return compile_card(task,bundle,answer)
    expected = set(bundle['answer_template'])
    if set(answer) not in (expected, expected|{'reviewer'}): raise ValueError('Use only this task answer template fields')
    reviewer = _text(answer.get('reviewer','Model identity unavailable'), 'reviewer')
    summary = _text(answer['summary'], 'summary')
    receipt = copy.deepcopy(task['receipt_template'])
    receipt['reviewer'] = reviewer; receipt['summary'] = summary
    if task['kind']=='opinion_review':
        if answer['relevance'] not in ('relevant','not_relevant','uncertain'): raise ValueError('Invalid opinion relevance')
        if answer['relevance']=='uncertain': return None
        for field in ('holding','disposition'):
            if not isinstance(answer[field],str): raise ValueError(field+' must be text')
            receipt[field] = answer[field]
        if not isinstance(answer['authors'],list) or any(not isinstance(a,str) for a in answer['authors']): raise ValueError('authors must be names')
        receipt.update(relevance=answer['relevance'], authors=copy.deepcopy(answer['authors']), citations=_refs(answer['evidence'],bundle))
        return receipt
    if answer['decision'] not in ('no_material_change','material_change','insufficient_evidence'): raise ValueError('Invalid source decision')
    if not isinstance(answer['people'],list): raise ValueError('people must be an array')
    if answer['decision']=='insufficient_evidence': return None
    refs = _refs(answer['evidence'], bundle, full=True)
    if not any(c['sha256']==task['inputs']['observation']['sha256'] for c in refs): raise ValueError('Answer must select current acquired evidence')
    receipt.update(review_scope='Complete changed ranges and acquired context in the current task card.', findings=[])
    # Changed-line support remains complete; model references supplement exact
    # prefilled support, never replace it with a reconstructed quote.
    for side in ('current','previous'):
        preserved = [c for c in receipt['support'][side] if c.get('quote')]
        selected = [c for key in bundle['bindings'] if key[0]==('C' if side=='current' else 'P') for c in _refs([key],bundle)]
        receipt['support'][side] = _unique(preserved or selected)
    receipt['support']['reason'] = summary
    if answer['decision']=='no_material_change':
        if answer['people']: raise ValueError('No-material-change answer cannot update people')
        receipt['outcome'] = 'no_relevant_change' if task['inputs']['observation']['change']=='changed' else 'baseline_reviewed'
        return receipt
    keys = set()
    for person in answer['people']:
        if not isinstance(person,dict) or set(person)!={'person','name','kind','evidence','fields'}: raise ValueError('Use the short person fields shown on the card')
        name = ' '.join(_text(person['name'],'person name').split())
        if person['kind'] not in ('judge','clerk'): raise ValueError('Person kind must be judge or clerk')
        cites = _refs(person['evidence'],bundle,full=True)
        if not any(c['sha256']==task['inputs']['observation']['sha256'] and ' '.join(name.split()).casefold() in ' '.join(c['quote'].split()).casefold() for c in cites): raise ValueError('Person name needs supplied identity evidence')
        if person['person']=='new':
            if any(' '.join(p['facts'].get('name','').split()).casefold()==' '.join(name.split()).casefold() for p in bundle['prior_people'].values()):
                raise ValueError('Use the supplied existing-person reference for this name')
            key='person-'+_slug(name)+'-'+h.sha([task['identity'],person['kind'],name.casefold()])[:12]
            finding=dict(key=key,kind=person['kind'],facts=dict(name=name,fields={}),citations=[],expected_version=None)
        else:
            prior=bundle['prior_people'].get(person['person'])
            if not prior: raise ValueError('Unknown existing-person reference')
            if ' '.join(name.split()).casefold()!=' '.join(prior['facts']['name'].split()).casefold() or person['kind']!=prior['kind']:
                raise ValueError('A successor requires a new person; do not rename the predecessor')
            finding=copy.deepcopy(prior)
            finding={k:finding[k] for k in ('key','kind','facts','expected_version')};finding['citations']=[]
        if finding['key'] in keys: raise ValueError('One answer per person, not duplicated person updates')
        keys.add(finding['key'])
        if not isinstance(person['fields'],dict): raise ValueError('Person fields must be a mapping')
        for field, update in person['fields'].items():
            try:
                if not re.fullmatch(r'[a-z][a-z0-9_]*',field): raise ValueError('Use a plain personnel field label')
                if not isinstance(update,dict) or set(update)!={'value','evidence'}: raise ValueError('A field needs value and evidence ID')
                value=_text(update['value'],field)
                citation=_refs(update['evidence'],bundle,full=True)
                supported_link=value.startswith(('https://','http://')) and value in task['inputs']['observation'].get('links',[])
                if len(citation)!=1 or (value not in citation[0]['quote'] and not supported_link
                                        and not _contact_text_supported(field, value, citation[0]['quote'])):
                    message='Field value must occur exactly in its supplied evidence or acquired current link inventory'
                    if len(citation)==1 and _contact_whitespace_allowed(field, value):
                        message+='; contact text may differ in whitespace only'
                    raise ValueError(message)
                if citation[0]['sha256']!=task['inputs']['observation']['sha256']:
                    raise ValueError('Current personnel fields require current evidence, not a former contact')
            except ValueError as exc:
                raise ValueError(f'{name}: fields.{field}: {exc}. Repair this field only; retain other supported fields.') from exc
            current=finding['facts'].setdefault('fields',{}).get(field,{})
            revised=copy.deepcopy(current) if isinstance(current,dict) else {}
            revised.update(value=value,status='verified',citation=citation[0])
            finding['facts']['fields'][field]=revised;cites.extend(citation)
        finding['citations']=_unique(cites)
        receipt['findings'].append(finding)
    if not receipt['findings']:
        key='source-change-'+task['identity']
        old=next((f for f in task['inputs'].get('prior_findings',[]) if f['key']==key),None)
        facts=copy.deepcopy(old['facts']) if old else {}
        facts['summary']=summary
        receipt['findings']=[dict(key=key,kind=old['kind'] if old else 'source_change',facts=facts,
                                   citations=refs,expected_version=old['expected_version'] if old else None)]
    receipt['outcome']='updated_findings'
    return receipt
