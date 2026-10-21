"""Dated county directory supplements, separate from immutable weekly issues.

Generation always produces a pending review draft. No publication approval or
research finalization is inferred from extraction or passing tests.
"""
from __future__ import annotations
from datetime import datetime
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit

from flwu.publication import digest, safe_url

KINDS = {'county_judge_baseline': 'Judge', 'county_officer_baseline': 'Judicial officer',
         'county_clerk_baseline': 'Clerk', 'county_administration_baseline': 'Court administration',
         'judge': 'Judge', 'clerk': 'Clerk', 'magistrate': 'General magistrate',
         'hearing_officer': 'Hearing officer'}
ROLES = set(KINDS.values()) | {'Senior judge', 'General magistrate', 'Hearing officer', 'Special master'}
PERSON_ROLES = {
    'special master': 'Special master',
    'circuit judge': 'Judge',
    'circuit judge (chief judge)': 'Judge',
    'chief judge': 'Judge',
    'county judge': 'Judge',
    'senior judge': 'Senior judge',
    'general magistrate': 'General magistrate',
    'general magistrate and child support enforcement hearing officer': 'General magistrate',
    'child support enforcement hearing officer': 'Hearing officer',
    'child support hearing officer': 'Hearing officer',
    'hearing officer': 'Hearing officer',
    'civil traffic hearing officer': 'Hearing officer',
    'traffic hearing officer': 'Hearing officer',
    'general magistrate / hearing officer': 'General magistrate',
    'clerk of circuit court and comptroller': 'Clerk',
    'clerk': 'Clerk',
}
LABELS = {
    'address_lines': 'Address', 'mailing_address_lines': 'Mailing address',
    'header_address_lines': 'Address — letterhead',
    'procedure_address_lines': 'Address — procedure',
    'procedure_header_address_lines': 'Address — procedure header',
    'source_stated_address_lines': 'Address — source statement',
    'shared_unit_mailing_address_lines': 'Shared unit mailing address',
    'chamber_code': 'Chambers', 'courtroom_code': 'Courtroom', 'courtroom_header': 'Courtroom — header',
    'judicial_assistant': 'Name', 'assistant_name': 'Name', 'assistant_role': 'Role',
    'assistant_email': 'Email', 'assistant_named_email': 'Email', 'assistant_work_email': 'Email',
    'assistant_personal_email': 'Email', 'assistant_personal_email_current': 'Email',
    'assistant_phone': 'Phone', 'assistant_names_by_source': 'Names by source',
    'chambers_fax_current': 'Fax', 'fax_availability': 'Fax',
    'actual_secondary_mailto_target': 'Linked email — source target',
    'additional_published_mailto_target': 'Linked email — source target',
    'procedure_mailto_email': 'Linked email — procedure target',
    'judge_header_mailto': 'Email linked to judge name',
    'judge_name_mailto_target': 'Email linked to judge name',
    'contact_form_url': 'Contact form', 'office_closed_daily': 'Daily office closure',
}
TEXT_VALUES = {
    'not_published_in_checked_sources': 'Not published in the reviewed sources.',
    'no_facsimile_available_official_statement': 'No fax available (official statement).',
    'documented_source_discrepancy_not_resolved': 'Sources differ; neither statement is selected as controlling.',
    'two_distinct_source_spellings_no_deliverability_or_priority_determined':
        'Sources give different email spellings; neither address has been confirmed as controlling or deliverable.',
    'Shareddivisionroute; personalemailnotseparatelyestablished':
        'Shared division address; a separate personal email was not established.',
    'Division route shared with assistant; personalemailnotseparatelyestablished':
        'Division address shared with the assistant; a separate personal email was not established.',
    'Shared division route; no separately published personalemail':
        'Shared division address; no separately published personal email.',
    'Shared division route; no separate personalemail verified':
        'Shared division address; no separate personal email verified.',
}
VARIANT_NOTES = {
    'actual_secondary_mailto_target', 'additional_published_mailto_target', 'procedure_mailto_email',
    'judge_header_mailto', 'judge_name_mailto_target', 'historical_assistant_email',
    'assistant_nickname', 'assistant_body_reference', 'assistant_other_source_statement',
    'procedure_assistant_contact', 'assistant_name_in_procedure', 'assistant_procedure_name',
    'procedure_assistant_name', 'source_assistant_name_variant', 'assistant_source_variant',
    'assistant_name_profile_spelling', 'assistant_spelling_variants', 'procedure_assistant_role',
    'procedure_chambers', 'procedure_chamber_label', 'procedure_courtroom', 'procedure_hearing_room',
    'source_room_variants', 'source_address_suite', 'procedure_address_room', 'procedure_room_text',
    'source_header_room', 'source_courtroom_variant', 'letterhead_address_suffix',
    'division_email_other_source_spelling', 'email_conflict_status',
}
OFFICE = {
    'phone', 'fax', 'chambers_fax_current', 'fax_availability', 'address_lines',
    'mailing_address_lines', 'procedure_address_lines', 'header_address_lines',
    'procedure_header_address_lines', 'source_stated_address_lines',
    'chamber_code', 'courtroom', 'courtroom_code', 'courtroom_header',
    'courtroom_statements', 'alternate_chamber_statement', 'alternate_published_room',
    'procedure_chambers', 'procedure_chamber_label', 'procedure_courtroom',
    'procedure_hearing_room', 'source_location_section_courtroom', 'source_room_variants',
    'letterhead_room_as_printed', 'address_discrepancy',
    'division_email', 'division_emails', 'division_email_limited_purpose',
    'division_email_scope', 'division_email_role', 'division_email_other_source_spelling',
    'email', 'email_role', 'email_roles', 'email_basis', 'email_conflict_status',
    'profile_email', 'judge_email', 'judge_header_mailto', 'judge_header_mailto_scope',
    'judge_name_mailto_target', 'judge_name_mailto_note',
    'additional_published_mailto_target', 'mailto_target_note',
    'actual_secondary_mailto_target', 'secondary_mailto_role', 'other_published_email',
    'office_hours', 'office_closed_daily', 'contact_scope_note',
    'administration_phones', 'administration_counter_hours', 'administration_room',
    'generic_assistance_email', 'public_records_custodian', 'public_records_email',
    'contact_form_url', 'telephone_hours',
    'address_basis', 'address_source', 'address_provenance', 'address_city_source_note',
    'phone_source', 'procedure_header_phone_as_printed', 'procedure_header_phone',
    'source_competing_order_email', 'source_competing_order_email_scope',
    'hearing_request_email_as_printed', 'procedure_header_office_email',
    'postjudgment_email_link_note', 'postjudgment_email_link_target',
    'mailing_address_source_labels', 'source_header_room', 'source_courtroom_variant',
    'procedure_address_room', 'procedure_room_text', 'procedure_mailto_email',
    'shared_unit_mailing_address_lines', 'shared_unit_mailing_address_scope',
    'letterhead_address_suffix', 'source_address_suite', 'fax_source_label',
}

# Hillsborough's saved field names retain division and source-role distinctions.
OFFICE.update({
    'office_phone', 'office_email', 'office_fax', 'office_address',
    'office_email_scope', 'mailing_address', 'physical_address',
    'entrance_address', 'visitor_entrance', 'guide_mailing_address_lines',
    'email_conflict', 'guide_email', 'risk_protection_email', 'directory_postal_code',
    'division_r_email', 'division_u_email_dated_ao', 'division_t_email',
    'division_m_email', 'division_v_email', 'division_v_phone', 'division_w_email',
    'division_p_visible_email', 'protective_injunction_guide_courtroom',
    'address_qualification', 'courtrooms', 'division_phones', 'family_n_email_status',
    'alternative_published_phone', 'additional_published_email', 'room_variants',
    'courtroom_dated_directories', 'courtroom_profile_guide', 'additional_email',
    'address_variants', 'county_civil_phone', 'protective_injunction_email',
    'civil_traffic_w_email', 'civil_y_email', 'criminal_x_email_as_published',
    'procedure_notice_mailing_room', 'profile_display_email',
    'courtesy_notice_cancellation_fax', 'dependency_email', 'family_email',
    'fax_scope', 'procedure_email',
})
# Santa Rosa's saved clerk facts retain division telephone routes by name.
OFFICE.update({
    'circuit_civil_phone', 'circuit_civil_email', 'circuit_civil_fax',
    'county_civil_email', 'county_civil_fax',
    'administration_phone', 'administration_email',
})
VARIANT_NOTES.update({
    'assistant_name_variant',
    'assistant_name_variants', 'alternative_published_assistant_name',
    'guide_assistant_name', 'guide_judicial_assistant', 'assistant_email_status',
    'email_conflict', 'guide_email', 'division_u_email_dated_ao',
    'directory_postal_code', 'protective_injunction_guide_courtroom',
    'address_qualification', 'courtrooms', 'family_n_email_status',
    'alternative_published_phone', 'additional_published_email', 'room_variants',
    'courtroom_dated_directories', 'courtroom_profile_guide', 'additional_email',
    'address_variants', 'procedure_notice_mailing_room', 'profile_display_email',
    'criminal_x_email_as_published', 'procedure_email',
})
LABELS.update({'office_phone': 'Phone', 'office_email': 'Office email',
               'office_fax': 'Fax', 'office_address': 'Address',
               'mailing_address': 'Mailing address', 'physical_address': 'Physical address',
               'circuit_civil_phone': 'Circuit civil phone',
               'circuit_civil_email': 'Circuit civil email',
               'circuit_civil_fax': 'Circuit civil fax',
               'county_civil_email': 'County civil email',
               'county_civil_fax': 'County civil fax',
               'administration_phone': 'Administration phone',
               'administration_email': 'Administration email'})


def text_lines(value):
    if value is None:
        return ['Not established as a current contact']
    if isinstance(value, dict):
        return [k.replace('_', ' ') + ': ' + '; '.join(text_lines(v)) for k, v in value.items()]
    if isinstance(value, list):
        return [line for v in value for line in text_lines(v)]
    return [TEXT_VALUES.get(str(value), str(value))]


def chamber_repeated_in_address(key, value, block):
    """Only remove the same fully qualified code, never guess a wing/room match."""
    if key != 'chamber_code' or not isinstance(value, str):
        return False
    code = re.sub(r'[^A-Z0-9]', '', value.upper())
    address = ' '.join(block.get('address_lines', []))
    tokens = re.findall(r'\b[A-Z]{1,2}[- ]?\d[\d-]*\b', address.upper())
    return code in {re.sub(r'[^A-Z0-9]', '', token) for token in tokens}


def row_order(row):
    key = row['fact_path'].split('.')[-1]
    if row['fact_path'].startswith('fields.') and key == 'value':
        key = row['fact_path'].split('.')[1]
    if row.get('type') == 'note':
        return (9, row['label'])
    rank = 0 if key in {'assistant_name', 'judicial_assistant', 'assistant_names_by_source'} else \
        1 if key == 'assistant_role' else 2 if 'phone' in key else 3 if 'email' in key else \
        4 if 'fax' in key else 5 if row.get('type') == 'address' else 6
    return (rank, row['label'])


def unpublished_fax(value):
    return (isinstance(value, dict) and 'value' in value and value['value'] is None
            and value.get('status') in {'not_published', 'not_published_in_reviewed_sources'})


def address_display_lines(lines):
    """Whitespace-only display repair; never change address tokens or source facts."""
    return [re.sub(r'\b(Room|Suite)(?=\d)', r'\1 ',
                   re.sub(r'\bFL(?=\d{5}\b)', 'FL ',
                          re.sub(r',(?=\S)', ', ', line))) for line in lines]


def qualified_fax(value):
    return (isinstance(value, dict) and set(value) == {'source_label', 'status', 'value'}
            and value['status'] == 'verified' and isinstance(value['value'], str)
            and isinstance(value['source_label'], str))


def contact_rows(facts):
    result, omitted = {'office': [], 'assistant': []}, []
    seen = set()
    for container in ('contact', 'contacts', 'current_contact'):
        block = facts.get(container)
        if not isinstance(block, dict):
            continue
        for key, value in block.items():
            assistant = 'assistant' in key or key == 'judicial_assistant'
            if (key not in OFFICE and not assistant) or value is None or chamber_repeated_in_address(key, value, block):
                omitted.append(container + '.' + key)
                continue
            label = LABELS.get(key, key.replace('_', ' ').capitalize())
            if key == 'assistant_email' and block.get('assistant_email_scope'):
                label = 'Email — see purpose in contact notes'
            lines = text_lines(value)
            if key in {'mailing_address', 'physical_address'} and isinstance(value, dict) and set(value) == {'lines'}:
                lines = text_lines(value['lines'])
            if not lines:
                result['assistant' if assistant else 'office'].append({
                    'label': label, 'lines': ['Not published in the reviewed sources.'],
                    'fact_path': container + '.' + key, 'type': 'note',
                })
                continue
            if key == 'fax' and unpublished_fax(value):
                lines = ['Not published in the reviewed sources.']
            elif key == 'fax' and qualified_fax(value):
                label = value['source_label'].rstrip(': ')
                lines = [value['value']]
            row = {'label': label, 'lines': lines, 'fact_path': container + '.' + key}
            if key == 'fax' and unpublished_fax(value):
                row['type'] = 'note'
            elif key.endswith('address_lines') or key in {'office_address', 'mailing_address', 'physical_address'}:
                row['type'] = 'address'
                row['lines'] = address_display_lines(lines)
            elif key in VARIANT_NOTES or key != 'assistant_role' and (key.endswith(('_basis', '_source', '_provenance', '_note', '_scope', '_role', '_roles')) or key in {'fax_source_label', 'assistant_name_status'}):
                row['type'] = 'note'
            elif not key.startswith(('source_', 'postjudgment_', 'procedure_header_')) and len(lines) == 1 and re.fullmatch(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', lines[0]):
                row['href'] = 'mailto:' + lines[0]
            elif key in {'phone', 'fax', 'chambers_fax_current', 'assistant_phone', 'office_phone', 'office_fax',
                             'circuit_civil_phone', 'circuit_civil_fax', 'county_civil_phone', 'county_civil_fax',
                             'administration_phone'} and len(lines) == 1 and re.fullmatch(r'(?:\(\d{3}\)\s*|\d{3}[-. ])\d{3}[-. ]\d{4}', lines[0]):
                row['href'] = 'tel:' + re.sub(r'\D', '', lines[0])
            identity = (row.get('type', row['label']), tuple(lines))
            if identity not in seen:
                result['assistant' if assistant else 'office'].append(row)
                seen.add(identity)
            else:
                omitted.append(container + '.' + key)
    # Manual research receipts keep evidenced values in fields, not contact.
    # Fill only empty columns so established legacy formatting is unchanged.
    fields = facts.get('fields', {})
    for column, selections in {
        'office': [('chambers_phone', 'Phone'), ('chambers_fax', 'Fax'), ('chambers_address', 'Address'),
                   ('office_phone', 'Phone'), ('office_address', 'Address'), ('office_contact', 'Contact')],
        'assistant': [('assistant_name', 'Name'), ('assistant_contact', 'Contact')],
    }.items():
        if result[column]:
            continue
        for key, label in selections:
            field = fields.get(key)
            if not isinstance(field, dict) or field.get('status') not in {'verified', 'not_published'}:
                continue
            value = field.get('value')
            if not value:
                value = 'Not published in the reviewed sources.'
            lines = [part.strip() for line in text_lines(value)
                     for part in re.split(r'[\r\n;]+', line) if part.strip()]
            row = dict(label=label, lines=lines, fact_path='fields.' + key + '.value')
            if field['status'] == 'not_published':
                row['type'] = 'note'
            elif key.endswith('_address'):
                row['type'] = 'address'
            # Qualified or conflicting strings remain intact, never guessed links.
            result[column].append(row)
    building = facts.get('building_address')
    if isinstance(building, dict) and building.get('value') and building.get('citation'):
        lines = [part.strip() for line in text_lines(building['value'])
                 for part in re.split(r'[\r\n]+', line) if part.strip()]
        normalize = lambda value: re.sub(r'[^a-z0-9]', '', value.lower())
        shown = normalize(' '.join(line for row in result['office'] for line in row['lines']))
        if normalize(' '.join(lines)) not in shown:
            result['office'].append(dict(label='Building address', lines=lines, type='address',
                                         fact_path='building_address.value'))
    for rows in result.values():
        rows.sort(key=row_order)
    return result, omitted


def legacy_clerk_rows(facts):
    """Project the saved flat clerk shape without changing research facts.

    Location-specific service restrictions stay next to their addresses; no
    counter is silently substituted for another or treated as chambers.
    """
    office = []

    def row(label, value, path, kind=None):
        if value is None or value == '' or value == []:
            return
        item = dict(label=label, lines=text_lines(value), fact_path=path)
        if kind:
            item['type'] = kind
        office.append(item)

    row('Phone', facts.get('office_phone'), 'office_phone')
    row('Mailing address', facts.get('mailing_address_lines'), 'mailing_address_lines', 'address')
    electronic = facts.get('electronic_contact') or {}
    row('Public contact form', electronic.get('url'), 'electronic_contact.url')
    row('Contact form scope', electronic.get('review_scope'), 'electronic_contact.review_scope', 'note')
    row('Civil email', electronic.get('direct_civil_email'), 'electronic_contact.direct_civil_email')
    for i, location in enumerate(facts.get('locations', [])):
        prefix = f'locations.{i}.'
        name = location.get('name', 'Office')
        row(name, location.get('address_lines'), prefix + 'address_lines', 'address')
        row(name + ' — hours', location.get('hours'), prefix + 'hours')
        if location.get('phone') != facts.get('office_phone'):
            row(name + ' — phone', location.get('phone'), prefix + 'phone')
        row(name + ' — services', location.get('service_scope'), prefix + 'service_scope', 'note')
    row('Location service limits', facts.get('location_scope_note'), 'location_scope_note', 'note')
    return {'office': office, 'assistant': []}


def directory_source_url(value):
    """Encode a literal path backslash, never reinterpret it as a separator.

    Reject unsafe authorities/control characters using the unchanged public URL
    policy. Original citations remain in the research packet and projection audit.
    """
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        return safe_url(value)
    parts = urlsplit(value)
    if '\\' in parts.netloc:
        raise ValueError('Invalid citation URL authority')
    if '\\' not in parts.path:
        return safe_url(value)
    encoded = urlunsplit(parts._replace(path=parts.path.replace('\\', '%5C')))
    return safe_url(encoded)


def public_metadata(value):
    """Keep source statements and provenance, excluding private storage locations."""
    private_keys = {'path', 'text_path', 'original_text_path', 'annotation_artifact', 'search_artifact'}
    if isinstance(value, dict):
        return {k: public_metadata(v) for k, v in value.items() if k not in private_keys}
    if isinstance(value, list):
        return [public_metadata(v) for v in value]
    return value


def make_supplement(packet, courts, *, contact_notes=None):
    """Pure projection; caller supplies reviewed county navigation destinations."""
    people, audit = [], {}
    contact_notes = contact_notes or {}
    unused_notes = set(contact_notes)
    county = packet['scope']['county'].replace('_', ' ').title()
    # Prefer the reviewed navigation spelling (e.g. Miami-Dade), while
    # refusing a label belonging to a different county.
    county_key = re.sub(r'[^a-z0-9]', '', county.lower())
    for court in courts:
        label = court.get('label', '').removesuffix(' County')
        if court.get('category') == 'County Courts' and re.sub(r'[^a-z0-9]', '', label.lower()) == county_key:
            county = label
            break
    for entity in packet['entities']:
        if entity['kind'] not in KINDS and entity['kind'] != 'person':
            continue  # Historical identity reconciliation is not a current person.
        f = entity['facts']
        if entity['kind'] == 'person':
            role = PERSON_ROLES.get(str(f.get('role', '')).strip().lower())
            if role is None:
                raise ValueError(f"Unsupported explicit personnel role: {entity['entity_key']}")
        else:
            role = KINDS[entity['kind']]
        if entity['kind'] in {'judge', 'magistrate'}:
            explicit_role = {
                'senior judge': 'Senior judge',
                'general magistrate and child support enforcement hearing officer': 'General magistrate',
                'special master': 'Special master',
                'general magistrate': 'General magistrate',
                'cse director & hearing officer': 'Hearing officer',
                'magistrate': 'General magistrate',
                'magistrate / child support hearing officer': 'General magistrate',
                'administrative magistrate': 'General magistrate',
                'hearing officer': 'Hearing officer',
                'administrative hearing officer': 'Hearing officer',
                'traffic hearing officer': 'Hearing officer',
                'civil traffic hearing officer': 'Hearing officer',
                'general magistrate / hearing officer': 'General magistrate',
                'child support hearing officer': 'Hearing officer',
                'child support enforcement hearing officer': 'Hearing officer',
            }.get(str(f.get('role', '')).strip().lower())
            source_roles = {card.get('role', '').lower() for card in f.get('roster_cards_reviewed', [])}
            if explicit_role:
                role = explicit_role
            elif source_roles and source_roles <= {'senior judge'}:
                role = 'Senior judge'
            elif source_roles and all('magistrate' in value for value in source_roles):
                role = 'General magistrate'
            elif not source_roles and isinstance(f.get('assignment'), str) and re.match(
                r'^(?:Circuit Civil )?General Magistrate\b|^Circuit Civil General Magistrate\d', f['assignment']
            ):
                role = 'General magistrate'
        assignment = f.get('assignment')
        if entity['kind'] == 'county_judge_baseline' and (
            isinstance(assignment, dict) and assignment.get('role') == 'Senior judge'
            or isinstance(assignment, str) and assignment.startswith('Senior judge,')
        ):
            role = 'Senior judge'
        if entity['kind'] == 'county_officer_baseline':
            role = {'general_magistrate': 'General magistrate', 'hearing_officer': 'Hearing officer'}.get(f.get('entity_type'), role)
        contacts, omitted = contact_rows(f)
        flat_clerk = entity['kind'] == 'clerk' and not any(contacts.values())
        if flat_clerk:
            contacts = legacy_clerk_rows(f)
        notes = []
        if entity['entity_key'] in contact_notes:
            selection = contact_notes[entity['entity_key']]
            if selection['expected_conflicts_sha256'] != digest(f.get('conflicts', [])):
                raise ValueError('Contact-note source changed; review the new findings before reuse')
            for note in selection['notes']:
                index = note['conflict_index']
                if type(index) is not int or not 0 <= index < len(f.get('conflicts', [])):
                    raise ValueError('Contact note references an absent source difference')
                notes.append(dict(title=note['title'], text=note['text'], fact_path='conflicts.' + str(index)))
            unused_notes.remove(entity['entity_key'])
        reasons = {}
        for path in omitted:
            container, key = path.split('.')
            block = f[container]
            reasons[path] = ('no_established_value' if block[key] is None else
                             'same_chamber_code_in_address' if chamber_repeated_in_address(key, block[key], block) else
                             'duplicate_value_already_displayed' if key in OFFICE or 'assistant' in key else
                             'ancillary_or_source_format_field_retained_in_research_packet')
        if flat_clerk:
            electronic = f.get('electronic_contact') or {}
            if electronic.get('direct_civil_email') is None:
                omitted.append('electronic_contact.direct_civil_email')
                reasons[omitted[-1]] = 'no_established_value'
            for i, location in enumerate(f.get('locations', [])):
                if location.get('phone') and location['phone'] == f.get('office_phone'):
                    omitted.append(f'locations.{i}.phone')
                    reasons[omitted[-1]] = 'duplicate_value_already_displayed'
        audit[entity['entity_key']] = {'omitted_contact_fields': omitted, 'omission_reasons': reasons}
        formatting = []
        for rows in contacts.values():
            for row in rows:
                if row.get('type') != 'address' or flat_clerk or row['fact_path'].startswith(('fields.', 'building_address.')):
                    continue
                container, field = row['fact_path'].split('.')
                original = f[container][field]
                if isinstance(original, dict) and set(original) == {'lines'}:
                    original = original['lines']
                original = text_lines(original)
                if original != row['lines']:
                    formatting.append(dict(fact_path=row['fact_path'], original_lines=original,
                                           display_lines=row['lines']))
        if formatting:
            audit[entity['entity_key']]['address_spacing_repairs'] = formatting
        summarized = [container + '.fax' for container in ('contact', 'contacts', 'current_contact')
                      if isinstance(f.get(container), dict) and unpublished_fax(f[container].get('fax'))]
        if summarized:
            audit[entity['entity_key']]['summarized_contact_fields'] = {
                path: 'Unpublished status displayed; search logs and original field retained in research packet'
                for path in summarized}
        for container in ('contact', 'contacts', 'current_contact'):
            if isinstance(f.get(container), dict) and qualified_fax(f[container].get('fax')):
                audit[entity['entity_key']].setdefault('summarized_contact_fields', {})[container + '.fax'] = (
                    'Source label and fax value displayed; internal verification status retained in research packet')
        source_refs = {}
        encodings = []
        for ref in entity['citations']:
            identity = (ref['url'], ref['sha256'], ref['retrieved_at'])
            public_url = directory_source_url(ref['url'])
            if public_url != ref['url']:
                encoding = dict(original_url=ref['url'], public_url=public_url, sha256=ref['sha256'])
                if encoding not in encodings:
                    encodings.append(encoding)
            source_refs[identity] = dict(url=public_url, sha256=ref['sha256'], retrieved_at=ref['retrieved_at'])
        if encodings:
            audit[entity['entity_key']]['source_url_path_encodings'] = encodings
        people.append(dict(id=entity['entity_key'], name=f['name'], kind=role,
                           counties=[county], court_ids=[c['group_id'] for c in courts],
                           contacts=contacts, assignment=f.get('assignment'),
                           profile_url=f.get('profile_url'), procedure_url=f.get('procedure_url'),
                           dates=f.get('dates'), source_observation=entity['observation'],
                           sources=list(source_refs.values()),
                           contact_status='not_verified' if f.get('current_contact_verified') is False else 'source_recorded',
                           conflicts=public_metadata(f.get('conflicts', [])), contact_notes=notes))
    if unused_notes:
        raise ValueError('Contact-note selection refers to personnel absent from this packet')
    result = dict(schema_version=1, county=county, stream=packet['stream'],
                  through_capture=packet['through_capture'], review_status='pending',
                  review=None, people=people, courts=courts)
    result['content_sha256'] = digest(result)
    return result, audit


def validate_supplement(data, *, preview=False):
    """An allowlist prevents private research paths/receipts entering public data."""
    try:
        if set(data) - {'coverage_note'} != {'schema_version', 'county', 'stream', 'through_capture', 'review_status',
                         'review', 'people', 'courts', 'content_sha256'} or data['schema_version'] != 1:
            raise ValueError('Invalid county directory schema')
        if 'coverage_note' in data and (not isinstance(data['coverage_note'], str) or not data['coverage_note'].strip()):
            raise ValueError('Invalid county coverage note')
        if not preview and public_metadata(data) != data:
            raise ValueError('Public directory contains private evidence storage paths')
        if data['content_sha256'] != digest({k: v for k, v in data.items() if k != 'content_sha256'}):
            raise ValueError('County directory checksum mismatch')
        if data['review_status'] not in {'pending', 'reviewed'}:
            raise ValueError('Invalid county directory review status')
        if not preview and data['review_status'] != 'reviewed':
            raise ValueError('Pending county directory requires a preview build')
        if data['review_status'] == 'reviewed':
            review = data['review']
            if set(review) != {'reviewed_by', 'reviewed_at', 'attestation'} or not all(isinstance(v, str) and v.strip() for v in review.values()):
                raise ValueError('County directory needs explicit review')
            aware(review['reviewed_at'])
        elif data['review'] is not None:
            raise ValueError('Pending directory cannot claim approval')
        capture = data['through_capture']
        if set(capture) != {'seq', 'capture_id', 'recorded_at', 'research_status'}:
            raise ValueError('Invalid county checkpoint metadata')
        aware(capture['recorded_at'])
        if type(capture['seq']) is not int or capture['seq'] < 1 or not re.fullmatch(r'[0-9a-f]{64}', capture['capture_id']):
            raise ValueError('Invalid county capture hash')
        groups = set()
        for court in data['courts']:
            if set(court) - {'resources'} != {'group_id', 'category', 'label', 'url'}:
                raise ValueError('Invalid county court navigation')
            if court['group_id'] in groups:
                raise ValueError('Duplicate county court group')
            groups.add(court['group_id'])
            safe_url(court['url'])
            for resource in court.get('resources', []):
                if set(resource) != {'label', 'url'}:
                    raise ValueError('Invalid county navigation resource')
                safe_url(resource['url'])
        seen = set()
        if not data['people'] or not groups:
            raise ValueError('County directory requires people and court groups')
        for person in data['people']:
            if set(person) - {'legacy_person_id'} != {'id', 'name', 'kind', 'counties', 'court_ids', 'contacts', 'assignment',
                               'profile_url', 'procedure_url', 'dates', 'source_observation', 'sources',
                               'contact_status', 'conflicts', 'contact_notes'}:
                raise ValueError('Unexpected county personnel fields')
            if 'legacy_person_id' in person and (
                not isinstance(person['legacy_person_id'], str)
                or not person['legacy_person_id'].strip()
                or person['legacy_person_id'] == person['id']
            ):
                raise ValueError('Invalid county-scoped legacy identity')
            if person['id'] in seen or not person['id'] or not person['name']:
                raise ValueError('Duplicate or empty county person identity')
            seen.add(person['id'])
            if person['kind'] not in ROLES or person['counties'] != [data['county']] or not set(person['court_ids']) <= groups:
                raise ValueError('Invalid county personnel scope')
            observation = person['source_observation']
            if set(observation) != {'capture_seq', 'capture_id', 'recorded_at'} or type(observation['capture_seq']) is not int:
                raise ValueError('Invalid person observation')
            aware(observation['recorded_at'])
            if not 0 < observation['capture_seq'] <= capture['seq'] or datetime.fromisoformat(observation['recorded_at'].replace('Z', '+00:00')) > datetime.fromisoformat(capture['recorded_at'].replace('Z', '+00:00')):
                raise ValueError('Person observation is after directory cutoff')
            if not re.fullmatch(r'[0-9a-f]{64}', observation['capture_id']):
                raise ValueError('Invalid person capture hash')
            if person['contact_status'] not in {'source_recorded', 'not_verified'}:
                raise ValueError('Invalid contact evidence state')
            for note in person['contact_notes']:
                if set(note) != {'title', 'text', 'fact_path'} or not all(isinstance(v, str) and v.strip() for v in note.values()):
                    raise ValueError('Invalid reviewed contact note')
                if not re.fullmatch(r'conflicts\.\d+', note['fact_path']) or int(note['fact_path'].split('.')[1]) >= len(person['conflicts']):
                    raise ValueError('Contact note source is absent')
            if set(person['contacts']) != {'office', 'assistant'}:
                raise ValueError('Invalid contact columns')
            for rows in person['contacts'].values():
                for row in rows:
                    if set(row) - {'type', 'href'} != {'label', 'lines', 'fact_path'} or not row['lines']:
                        raise ValueError('Invalid contact row')
                    if 'type' in row and row['type'] not in {'address', 'note'}:
                        raise ValueError('Invalid contact row type')
                    if not all(isinstance(v, str) and v for v in row['lines']):
                        raise ValueError('Contact lines must be text')
                    href = row.get('href')
                    if href and not re.fullmatch(r'(?:mailto:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|tel:\d{7,15})', href):
                        raise ValueError('Invalid county contact link')
            for field in ('profile_url', 'procedure_url'):
                if person[field] is not None:
                    safe_url(person[field])
            if not person['sources']:
                raise ValueError('County person requires evidence')
            for source in person['sources']:
                if set(source) != {'url', 'sha256', 'retrieved_at'} or not re.fullmatch(r'[0-9a-f]{64}', source['sha256']):
                    raise ValueError('Invalid county source')
                safe_url(source['url']); aware(source['retrieved_at'])
        return data
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Malformed county directory') from exc


def aware(value):
    if datetime.fromisoformat(value.replace('Z', '+00:00')).tzinfo is None:
        raise ValueError('County observation requires a timezone')


def load_supplements(paths, *, preview=False):
    supplements, counties, identities = [], set(), {}
    for path in paths:
        data = validate_supplement(json.loads(Path(path).read_text()), preview=preview)
        if data['county'] in counties:
            raise ValueError('Only one current supplement per county')
        counties.add(data['county'])
        for person in data['people']:
            # Membership and evidence may differ; personnel facts must agree.
            shared_fields = {'counties', 'court_ids', 'source_observation', 'sources', 'contact_notes'}
            facts = {k: v for k, v in person.items() if k not in shared_fields}
            if person['id'] in identities and identities[person['id']] != facts:
                raise ValueError('Conflicting identity across county supplements')
            identities[person['id']] = facts
        supplements.append(data)
    return supplements
