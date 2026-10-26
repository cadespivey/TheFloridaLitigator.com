"""Explicit, allowlisted public exports from immutable research captures.

Public builds consume only these exports, never the private research database.
Finalization is the recorded editorial approval; synthetic previews are isolated.
"""
from __future__ import annotations
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from urllib.parse import urlsplit, parse_qs

SECTIONS = [('statutes', 'Statutes'), ('case_law', 'Case Law'),
            ('procedural_rules', 'Procedural Rules'), ('local_rules', 'Local Rules')]
KEYS = {k for k, _ in SECTIONS}
COUNTY_LABELS = {'baker': 'Baker', 'clay': 'Clay', 'duval': 'Duval',
                 'nassau': 'Nassau', 'putnam': 'Putnam', 'st_johns': 'St. Johns', 'union': 'Union'}


def directory_links(facts, citations, *, preview=False):
    """Publish only explicitly selected links supported by this person's evidence."""
    selected = facts.get('public_links', {})
    if not isinstance(selected, dict) or set(selected) - {'profile', 'procedure'}:
        raise ValueError('Invalid directory link selection')
    result = {}
    for role, ref in selected.items():
        if not isinstance(ref, dict) or not ref.get('quote') or not any(
            c['url'] == ref.get('url') and c['quote'] == ref['quote'] for c in citations
        ):
            raise ValueError('Directory link lacks an exact source citation')
        result[role + '_url'] = safe_url(ref['url'], preview=preview)
    return result


def candidate_summary(facts, section):
    summary = facts.get('summary') or '\n\n'.join(
        c['statement'] for c in facts.get('claims', []) if c.get('review') == 'supported')
    if section != 'case_law':
        return summary
    for label, value in (('Holding', facts.get('holding')), ('Disposition', facts.get('disposition')),
                         ('Author', ', '.join(facts.get('authors', [])))):
        if not value:
            continue
        line = label + ': ' + value
        existing = re.search(r'^' + label + r':\s*(.*)$', summary, re.MULTILINE)
        if existing:
            if existing.group(1).strip() != value.strip():
                raise ValueError('Conflicting structured opinion field: ' + label)
        else:
            summary += '\n\n' + line
    return summary


def _limited_sections(group):
    if group in ('statutes', 'bills'):
        return ('statutes',)
    if group in ('court_rules', 'bar_rules', 'agency_rules'):
        return ('procedural_rules',)
    if group == 'supreme_court':
        return ('case_law', 'procedural_rules')
    if group.startswith('dca_'):
        return ('case_law',)
    if group.startswith(('clerk_', 'circuit_')):
        return ('local_rules',)
    # An unknown category cannot silently escape a visible coverage limitation.
    return tuple(key for key, _ in SECTIONS)


def _day(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Evidence dates must use YYYY-MM-DD')
    return date.fromisoformat(value)


def _baseline_metadata(issue):
    if issue['report_type'] not in ('opening_baseline', 'period_update'):
        raise ValueError('Invalid report type')
    if issue['report_type'] == 'opening_baseline' and issue['window_start'] != issue['window_end']:
        raise ValueError('Opening baseline requires a single cutoff date')
    coverage = issue['coverage']
    if not isinstance(coverage, dict) or set(coverage) != {'summary', 'limitations', 'directory_observed_at'}:
        raise ValueError('Invalid coverage schema')
    if not isinstance(coverage['summary'], str) or not coverage['summary'].strip():
        raise ValueError('Coverage summary is required')
    limits = coverage['limitations']
    if not isinstance(limits, list) or any(not isinstance(x, str) or not x.strip() for x in limits):
        raise ValueError('Invalid coverage limitations')
    observed = coverage['directory_observed_at']
    if observed is not None:
        if not isinstance(observed, str) or datetime.fromisoformat(observed.replace('Z', '+00:00')).tzinfo is None:
            raise ValueError('Directory observation requires a timezone timestamp')
    if issue['directory'] and (not observed or not limits):
        raise ValueError('Directory requires observation timestamp and historical limitations')


def _inclusion(issue, item):
    start, end = _day(issue['window_start']), _day(issue['window_end'])
    pub = None if item['publication_date'] is None else _day(item['publication_date'])
    effective = None if item['effective_date'] is None else _day(item['effective_date'])
    basis = item['inclusion_basis']
    if pub is not None and pub > end:
        raise ValueError('Source issuance is after the report cutoff')
    if issue['report_type'] == 'opening_baseline':
        if basis != 'opening_baseline' or (pub is None and (effective is None or effective > end)):
            raise ValueError('Opening baseline needs a supported date on or before cutoff')
    elif basis == 'publication':
        if pub is None or not start <= pub <= end:
            raise ValueError('Publication basis requires issuance within the reporting period')
    elif basis == 'effective':
        if effective is None or not start <= effective <= end:
            raise ValueError('Effective basis requires an effective date within the reporting period')
    else:
        raise ValueError('Invalid inclusion basis for period update')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def safe_url(value, *, preview=False):
    if not isinstance(value, str) or any(ord(c) < 32 for c in value) or '\\' in value:
        raise ValueError('Invalid citation URL')
    if preview and re.fullmatch(r'evidence/[a-f0-9]{64}\.txt', value):
        return value
    url = urlsplit(value)
    if url.scheme not in ('https', 'http') or not url.hostname or url.username or url.password:
        raise ValueError('Citations require public HTTP(S) URLs without credentials')
    if set(k.lower() for k in parse_qs(url.query)) & {'token', 'access_token', 'api_key', 'apikey', 'key', 'password'}:
        raise ValueError('Credential-bearing URL cannot be exported')
    if not preview and (url.hostname.endswith('.invalid') or url.hostname in ('localhost', '127.0.0.1', '::1')):
        raise ValueError('Synthetic/local citation cannot be published')
    return value


def validate_issue(issue, *, preview=False):
    try:
        return _validate_issue(issue, preview=preview)
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Malformed public issue schema') from exc


def _validate_issue(issue, *, preview=False):
    allowed = {'schema_version', 'id', 'title', 'window_start', 'window_end', 'published_at',
               'synthetic', 'sections', 'directory', 'provenance', 'content_sha256'}
    version = issue['schema_version']
    if version == 2:
        allowed |= {'report_type', 'coverage'}
    if set(issue) != allowed or type(version) is not int or version not in (1, 2):
        raise ValueError('Invalid public issue schema')
    if version == 2:
        _baseline_metadata(issue)
    if not re.fullmatch(r'[a-z0-9-]+', issue['id']):
        raise ValueError('Invalid public issue ID')
    if not isinstance(issue['title'], str) or not issue['title'].strip():
        raise ValueError('Issue title must be text')
    if not isinstance(issue['synthetic'], bool) or (issue['synthetic'] and not preview):
        raise ValueError('Synthetic issue requires an explicit preview build')
    for key in ('window_start', 'window_end'):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', issue[key]):
            raise ValueError('Report dates must use YYYY-MM-DD')
    if date.fromisoformat(issue['window_start']) > date.fromisoformat(issue['window_end']):
        raise ValueError('Reversed report period')
    if datetime.fromisoformat(issue['published_at'].replace('Z', '+00:00')).tzinfo is None:
        raise ValueError('Publication timestamp requires timezone')
    if set(issue['sections']) != KEYS:
        raise ValueError('All four report sections are required')
    if issue['content_sha256'] != digest({k: v for k, v in issue.items() if k != 'content_sha256'}):
        raise ValueError('Public issue checksum mismatch; re-export the reviewed capture')
    provenance = issue['provenance']
    if set(provenance) - {'source_limitations', 'workflow_coverage'} != {'capture_id', 'report_sha256', 'review_status'}:
        raise ValueError('Invalid public provenance')
    coverage = provenance.get('workflow_coverage')
    if coverage is not None:
        if (not isinstance(coverage, dict) or set(coverage) != {'acquisition_complete','pending'}
                or type(coverage['acquisition_complete']) is not bool or not isinstance(coverage['pending'], list)):
            raise ValueError('Invalid workflow coverage metadata')
        for task in coverage['pending']:
            if (set(task) != {'task_id','decision','reason'} or not all(isinstance(v,str) and v for v in task.values())
                    or task['decision'] not in ('unavailable','scope_excluded')):
                raise ValueError('Invalid workflow coverage disposition')
    if 'source_limitations' in provenance:
        if not isinstance(provenance['source_limitations'], list) or not provenance['source_limitations']:
            raise ValueError('Public source limitations must be a nonempty list')
        for limitation in provenance['source_limitations']:
            if (not isinstance(limitation, dict) or limitation.get('category') not in ('retrieval_failed', 'invalid_content')
                    or not all(limitation.get(k) for k in ('task_id','url','observation_capture_id','reason','reviewed_scope'))):
                raise ValueError('Invalid public source limitation')
            affected = limitation.get('affected_sections')
            if not isinstance(affected, list) or not affected or any(section not in KEYS for section in affected):
                raise ValueError('Source limitation must identify affected report sections')
    if not re.fullmatch(r'[a-f0-9]{64}', provenance['capture_id']):
        raise ValueError('Invalid capture checksum')
    if not preview and (provenance['review_status'] != 'finalized' or not re.fullmatch(r'[a-f0-9]{64}', provenance['report_sha256'] or '')):
        raise ValueError('Public issue requires a finalized report')
    limited_sections = {key for limit in provenance.get('source_limitations', []) for key in limit['affected_sections']}
    if coverage and not coverage['acquisition_complete']:
        limited_sections.update(KEYS)
    for key, section in issue['sections'].items():
        if set(section) != {'status', 'items'} or section['status'] not in ('reviewed', 'incomplete'):
            raise ValueError('Section requires reviewed/incomplete status and items')
        if not preview and section['status'] != 'reviewed' and key not in limited_sections:
            raise ValueError('Incomplete section cannot be published')
        if key in limited_sections and section['status'] != 'incomplete':
            raise ValueError('A source-limited section cannot be represented as fully reviewed')
        if not isinstance(section['items'], list):
            raise ValueError('Section items must be a list')
        for item in section['items']:
            item_keys = {'id', 'title', 'summary', 'publication_date', 'effective_date', 'legal_status', 'citations'}
            if version == 2:
                item_keys.add('inclusion_basis')
            if set(item) != item_keys:
                raise ValueError('Unexpected public item fields')
            if not item['summary'] or not isinstance(item['citations'], list) or not item['citations']:
                raise ValueError('Every summary needs source citations')
            if any(not isinstance(item[k], str) for k in ('id', 'title', 'summary', 'legal_status')):
                raise ValueError('Item text fields must be strings')
            if version == 2:
                _inclusion(issue, item)
            elif item['publication_date']:
                day = date.fromisoformat(item['publication_date'])
                if not date.fromisoformat(issue['window_start']) <= day <= date.fromisoformat(issue['window_end']):
                    raise ValueError('Published item falls outside its reporting period')
            if item['effective_date']:
                date.fromisoformat(item['effective_date'])
            for cite in item['citations']:
                validate_citation(cite, preview)
    if not isinstance(issue['directory'], list):
        raise ValueError('Directory must be a list')
    for person in issue['directory']:
        if set(person) - {'court_ids', 'profile_url', 'procedure_url'} != {'id', 'name', 'kind', 'counties', 'details', 'procedures', 'governing_rules', 'citations'}:
            raise ValueError('Unexpected public directory fields')
        if 'court_ids' in person and (not isinstance(person['court_ids'], list) or any(not isinstance(v, str) for v in person['court_ids'])):
            raise ValueError('Court IDs must be a list of strings')
        if not isinstance(person['citations'], list) or not person['citations']:
            raise ValueError('Directory entry lacks citations')
        if person['kind'] not in ('judge', 'clerk') or any(not isinstance(person[k], str) for k in ('id', 'name', 'procedures')):
            raise ValueError('Invalid public person')
        if any(not isinstance(person[k], list) or any(not isinstance(v, str) for v in person[k]) for k in ('counties', 'governing_rules')):
            raise ValueError('Directory counties/rules must be lists of text')
        if not isinstance(person['details'], dict) or any(not isinstance(v, str) for v in person['details'].values()):
            raise ValueError('Directory contacts must be text')
        for cite in person['citations']:
            validate_citation(cite, preview)
        for field in ('profile_url', 'procedure_url'):
            if field in person:
                safe_url(person[field], preview=preview)
                if person[field] not in {c['url'] for c in person['citations']}:
                    raise ValueError('Directory link lacks an exact source citation')
    return issue


def validate_citation(cite, preview):
    if set(cite) != {'label', 'url', 'quote'} or not cite['label']:
        raise ValueError('Invalid public citation')
    if not isinstance(cite['label'], str) or not isinstance(cite['quote'], str) or not cite['quote'].strip():
        raise ValueError('Citation label and quotation must be text')
    safe_url(cite['url'], preview=preview)


def export_capture(database, capture_id, archive, *, preview=False):
    archive = Path(archive)
    conn = sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute('SELECT c.*,s.mode FROM captures c JOIN streams s ON s.stream=c.stream WHERE capture_id=?', (capture_id,)).fetchone()
        if not row:
            raise ValueError('Unknown research capture')
        payload = json.loads(row['payload']); contract = payload['contract']
        if digest([row['stream'], row['run_id'], payload]) != capture_id:
            raise ValueError('Research capture checksum mismatch')
        approval = conn.execute('SELECT * FROM finalized_reports WHERE capture_seq=? ORDER BY seq DESC LIMIT 1', (row['seq'],)).fetchone()
        synthetic = row['mode'] == 'synthetic_replay'
        if not preview and (synthetic or not approval or payload['status'] != 'ready_for_review'):
            raise ValueError('Publication requires a complete, finalized live research capture')
        if approval:
            report = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (approval['report_sha256'],)).fetchone()
            if not report or hashlib.sha256(report[0]).hexdigest() != approval['report_sha256']:
                raise ValueError('Finalized report bytes missing or changed')
        if not preview and not synthetic:
            from flwu.publication_acceptance import require
            require(conn, capture_id, report[0], require_latest=False)
        artifact_files = {}

        def citations(refs):
            result = []
            for ref in refs:
                if not ref.get('quote'):
                    continue
                raw = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (ref['sha256'],)).fetchone()
                if not raw or hashlib.sha256(raw[0]).hexdigest() != ref['sha256']:
                    raise ValueError('Citation original missing or changed')
                extracted = conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (ref['text_sha256'],)).fetchone()
                if not extracted or hashlib.sha256(extracted[0]).hexdigest() != ref['text_sha256'] or ref['quote'] not in extracted[0].decode('utf-8'):
                    raise ValueError('Citation quotation is absent from verified extracted text')
                if not preview and ref.get('synthetic'):
                    raise ValueError('Synthetic citation cannot enter a public issue')
                url = safe_url(ref['url'], preview=preview)
                if synthetic:
                    url = 'evidence/' + ref['sha256'] + '.txt'
                    artifact_files[url] = raw[0]
                item = {'label': (ref.get('endpoint') or urlsplit(ref['url']).hostname) + ' · ' + str(ref.get('locator', 'source')),
                        'url': url, 'quote': ref['quote']}
                if item not in result:
                    result.append(item)
            return result

        issue = {'schema_version': 1, 'id': 'update-' + capture_id[:20],
                 'title': 'Florida Law Weekly Update', 'window_start': contract['window_start'],
                 'window_end': contract['window_end'], 'published_at': approval['finalized_at'] if approval else row['recorded_at'],
                 'synthetic': synthetic, 'sections': {k: {'status': 'reviewed' if payload['status'] == 'ready_for_review' else 'incomplete', 'items': []} for k, _ in SECTIONS},
                 'directory': [], 'provenance': {'capture_id': capture_id,
                   'report_sha256': approval['report_sha256'] if approval else None,
                   'review_status': 'finalized' if approval else 'preview'}}
        if 'report_type' in contract:
            issue.update(schema_version=2, report_type=contract['report_type'], coverage=contract.get('coverage'))
        if 'workflow_report' in payload:
            from flwu.publication_acceptance import acquisition_queue
            from flwu.publication_pending import validate as validate_pending
            from flwu.evidence_binding import AcquisitionIndex
            queue = acquisition_queue(conn, row)
            pending = payload['workflow_report']['coverage_dispositions']
            validate_pending(queue, pending, AcquisitionIndex(conn, row['stream'], through_seq=row['seq']))
            coverage = dict(acquisition_complete=queue['acquisition_complete'],
                            pending=[{k:p[k] for k in ('task_id','decision','reason')} for p in pending])
            issue['provenance']['workflow_coverage'] = coverage
            if not coverage['acquisition_complete']:
                for section in issue['sections'].values():section['status'] = 'incomplete'
        limits = [check['limitation'] for check in payload['checks'] if check['status'] == 'reviewed_source_limitation']
        if limits:
            # Machine-readable provenance only; no public Evidence Coverage section.
            keys = ('task_id','url','observation_capture_id','sha256','text_sha256','retrieved_at',
                    'http_status','category','reason','reviewed_scope')
            issue['provenance']['source_limitations'] = [{k: limit[k] for k in keys} for limit in limits]
            groups = {task['id']: task.get('group', '') for task in contract.get('tasks', [])}
            for limit, public_limit in zip(limits, issue['provenance']['source_limitations']):
                if 'discovery_path' in limit:
                    public_limit['required_url'] = limit['discovery_path'][0]['url']
                    public_limit['discovery_observations'] = [
                        {k: hop[k] for k in ('url','observation_capture_id','sha256',
                                            'retrieved_at','http_status','target_url')}
                        for hop in limit['discovery_path']]
                group = groups.get(limit['task_id'], '')
                affected = _limited_sections(group)
                for section in affected:
                    issue['sections'][section]['status'] = 'incomplete'
                public_limit['affected_sections'] = list(affected)
        roster = {}
        court_roster = {}
        court_names = {'roster-supreme': 'supreme_court', **{'roster-dca-'+str(n): 'dca_'+word for n, word in enumerate(['first','second','third','fourth','fifth','sixth'], 1)},
                       'roster-circuit-4':'circuit_fourth', 'roster-circuit-7':'circuit_seventh', 'roster-circuit-8':'circuit_eighth'}
        for finding in payload['findings']:
            if finding['kind'] == 'source_inventory':
                for person in finding['facts'].get('entities', []):
                    key = 'person-' + person['id']
                    roster.setdefault(key, set()).update(person['counties'])
                    if finding['key'] in court_names:
                        court_roster.setdefault(key, set()).add(court_names[finding['key']])
        for finding in payload['findings']:
            facts = finding['facts']; kind = finding['kind']
            if kind == 'candidate' and facts.get('decision') == 'include':
                section = facts.get('section')
                if synthetic:
                    section = 'procedural_rules' if facts['id'].startswith('R-') else 'case_law'
                if section not in KEYS:
                    raise ValueError('Candidate needs explicit section before review/finalization: ' + finding['key'])
                if not synthetic and not facts.get('title'):
                    raise ValueError('Included candidate requires a reviewed public title')
                summary = candidate_summary(facts, section)
                issue['sections'][section]['items'].append({'id': finding['key'], 'title': facts.get('title') or facts['id'],
                    'summary': summary, 'publication_date': facts.get('publication_date'), 'effective_date': facts.get('effective_date'),
                    'legal_status': facts.get('legal_status', 'unknown'), 'citations': citations(finding['citations'])})
                if issue['schema_version'] == 2:
                    issue['sections'][section]['items'][-1]['inclusion_basis'] = facts.get('inclusion_basis')
            elif kind in ('judge', 'clerk'):
                details = {}
                labels = {'chambers_phone': 'Chambers', 'address': 'Address', 'assistant_name': 'Judicial assistant',
                          'assistant_contact': 'Assistant contact', 'division': 'Division', 'phone': 'Office phone', 'contact': 'Office contact'}
                for key, label in labels.items():
                    if facts.get(key): details[label] = str(facts[key])
                for key, field in facts.get('fields', {}).items():
                    details[key.replace('_', ' ').capitalize()] = str(field.get('value') or 'Not published in checked sources')
                procedure = facts.get('procedure', {})
                procedure_text = procedure.get('summary') or '; '.join(d.get('applicability', '') for d in procedure.get('documents', []))
                if procedure.get('status') == 'no_published_procedure_located':
                    procedure_text = procedure_text or 'No individual procedure located in the sources checked.'
                issue['directory'].append({'id': finding['key'], 'name': facts['name'], 'kind': kind,
                    'court_ids': sorted(court_roster.get(finding['key'], [])),
                    'counties': sorted({COUNTY_LABELS.get(c, c) for c in (facts.get('counties') or ([facts['county']] if facts.get('county') else roster.get(finding['key'], [])))}),
                    'details': details, 'procedures': procedure_text,
                    'governing_rules': [r.get('summary') or r.get('title') or 'See governing rule source.' for r in facts.get('governing_rules', [])],
                    'citations': citations(finding['citations'])})
                issue['directory'][-1].update(directory_links(facts, issue['directory'][-1]['citations'], preview=preview))
        issue['content_sha256'] = digest(issue)
        validate_issue(issue, preview=preview)
        # Write only an explicit public allowlist; no receipts, drafts, DB or prompts.
        target = archive / (issue['id'] + '.json')
        text = json.dumps(issue, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
        if target.exists():
            if json.loads(target.read_text(encoding='utf-8')) != issue:
                raise ValueError('Immutable public issue already exists with different content')
            return target
        archive.mkdir(parents=True, exist_ok=True)
        for relative, data in artifact_files.items():
            path = archive / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        with target.open('x', encoding='utf-8') as output:
            output.write(text)
        return target
    finally:
        conn.close()
