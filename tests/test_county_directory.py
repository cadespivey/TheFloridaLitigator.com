import copy
import json
from pathlib import Path
import shutil
import subprocess

from bs4 import BeautifulSoup
import pytest

from flwu.county_directory import make_supplement, validate_supplement, contact_rows, load_supplements
from flwu.publication import digest
from flwu.site import build_site


def seal(value):
    value['content_sha256'] = digest({k: v for k, v in value.items() if k != 'content_sha256'})
    return value


@pytest.fixture
def supplement():
    contacts = dict(phone='954-555-0100', assistant_name='Example Assistant', division_email='div@example.org',
                    email_role='Division mailbox, not personal judge email',
                    address_lines=['Courthouse, Room 1', '100 Court Street', 'City, FL 00000'],
                    interpreter_phone='954-555-9999')
    def entity(key, kind, facts):
        return dict(entity_key=key, kind=kind, facts=facts,
                    observation=dict(capture_seq=1, capture_id='a'*64, recorded_at='2026-10-16T12:00:00Z'),
                    citations=[dict(url='https://court.example/procedure', sha256='b'*64, retrieved_at='2026-10-16T11:00:00Z')])
    packet = dict(scope=dict(county='broward'), stream='test-county',
                  through_capture=dict(seq=2, capture_id='c'*64, recorded_at='2026-10-16T13:00:00Z', research_status='incomplete'),
                  entities=[entity('example-judge', 'county_judge_baseline', dict(name='Example Judge', contact=contacts,
                            profile_url='https://court.example/judge', procedure_url='https://court.example/procedure', assignment='Civil division')),
                            entity('example-senior', 'county_judge_baseline', dict(name='Example Senior',
                            current_contact=None, current_contact_verified=False, historical_contact={'phone': '954-555-7777'},
                            assignment={'role': 'Senior judge'})),
                            entity('historical', 'county_roster_reconciliation', dict(name='Historical Judge'))])
    courts = [dict(group_id='clerk_broward', category='County Courts', label='Broward County', url='https://court.example/')]
    result, audit = make_supplement(packet, courts)
    assert audit['example-judge']['omitted_contact_fields'] == ['contact.interpreter_phone']
    return result


def test_draft_projection_keeps_roles_and_historical_contacts_separate(supplement):
    assert len(supplement['people']) == 2
    first, senior = supplement['people']
    assert senior['kind'] == 'Senior judge' and senior['contacts'] == {'office': [], 'assistant': []}
    assert senior['contact_status'] == 'not_verified'
    office = first['contacts']['office']
    assert next(row for row in office if row['label'] == 'Division email')['href'] == 'mailto:div@example.org'
    assert next(row for row in office if row['label'] == 'Email role')['lines'] == ['Division mailbox, not personal judge email']
    assert '954-555-9999' not in json.dumps(first['contacts'])
    assert '954-555-7777' not in json.dumps(supplement)
    assert len(next(row for row in office if row.get('type') == 'address')['lines']) == 3
    validate_supplement(supplement, preview=True)
    with pytest.raises(ValueError, match='preview'):
        validate_supplement(supplement)


def test_source_conflict_qualifiers_are_not_dropped_or_made_contact_recommendations():
    contact = dict(phone='954-831-6974', procedure_header_phone_as_printed='945-831-6974',
                   source_competing_order_email='Div40@17th.flcourts.org',
                   source_competing_order_email_scope='Conflicts with header Division38; not verified alternate',
                   address_basis='Combined physical location, not certified mailing destination')
    rows, omitted = contact_rows({'contact': contact})
    assert not omitted
    by_path = {row['fact_path']: row for row in rows['office']}
    assert by_path['contact.phone']['href'] == 'tel:9548316974'
    assert 'href' not in by_path['contact.procedure_header_phone_as_printed']
    assert 'href' not in by_path['contact.source_competing_order_email']
    assert by_path['contact.address_basis']['lines'] == [contact['address_basis']]


def test_compact_contact_order_exact_room_deduplication_and_historical_notes():
    facts = {'contact': dict(address_lines=['Chambers WW-16-127', '100 Court St', 'City, FL 00000'],
                            chamber_code='WW16127', courtroom='WW16155', phone='954-555-0100',
                            assistant_email='ja@example.org', assistant_name='Example Name',
                            historical_assistant_email={'value': 'old@example.org', 'source_context': '2020 only'},
                            fax=None, fax_availability='no_facsimile_available_official_statement')}
    contacts, omitted = contact_rows(facts)
    assert contacts['assistant'][0]['label'] == 'Name'
    assert contacts['office'][0]['label'] == 'Phone'
    assert 'contact.chamber_code' in omitted and 'contact.fax' in omitted
    assert next(r for r in contacts['office'] if r['fact_path']=='contact.fax_availability')['lines'] == ['No fax available (official statement).']
    historical = next(r for r in contacts['assistant'] if r['fact_path']=='contact.historical_assistant_email')
    assert historical['type'] == 'note' and 'href' not in historical
    facts['contact']['chamber_code'] = 'NW16127'
    different, omitted = contact_rows(facts)
    assert 'contact.chamber_code' not in omitted
    assert any(r['lines'] == ['NW16127'] for r in different['office'])


def test_unlabeled_anchor_is_a_qualified_note_not_a_contact_action():
    rows, _ = contact_rows({'contact': dict(additional_published_mailto_target='target@example.org',
                                           mailto_target_note='Not explicitly identified as assistant mailbox')})
    target = next(r for r in rows['office'] if r['fact_path'].endswith('additional_published_mailto_target'))
    assert target['type'] == 'note' and 'href' not in target


def test_duplicate_values_remain_accounted_for_in_field_audit():
    rows, omitted = contact_rows({'contact':{'phone':'954-555-0100'}, 'contacts':{'phone':'954-555-0100'}})
    assert len(rows['office']) == 1
    assert omitted == ['contacts.phone']


def test_contact_note_editorial_selection_is_pinned_to_source_facts():
    conflicts = [{'issue': 'Room', 'description': 'Header says 1; body says 2.'}]
    packet = dict(scope={'county':'broward'}, stream='fixture', through_capture={}, entities=[dict(
        entity_key='person',kind='county_judge_baseline',facts={'name':'Example', 'conflicts':conflicts},
        observation={},citations=[])])
    notes = {'person': {'expected_conflicts_sha256':digest(conflicts),
                       'notes':[{'conflict_index':0,'title':'Room difference','text':'The header lists 1; the body lists 2.'}]}}
    result, _ = make_supplement(packet, [], contact_notes=notes)
    assert result['people'][0]['contact_notes'][0]['fact_path'] == 'conflicts.0'
    conflicts[0]['description'] = 'Changed source statement'
    with pytest.raises(ValueError, match='source changed'):
        make_supplement(packet, [], contact_notes=notes)


@pytest.mark.parametrize('change', [
    lambda s: s.update(private_database='/private/path'),
    lambda s: s['people'].append(copy.deepcopy(s['people'][0])),
    lambda s: s['people'][0].update(counties=['Duval']),
    lambda s: s['people'][0]['source_observation'].update(capture_seq=3),
    lambda s: s['people'][0]['source_observation'].update(recorded_at='2026-10-17T00:00:00Z'),
    lambda s: s['people'][0]['contacts']['office'][0].update(href='javascript:alert(1)'),
    lambda s: s.update(review_status='reviewed'),
    lambda s: s['courts'][0].update(url='https://example.org/?api_key=secret'),
])
def test_reject_malformed_or_unreviewed_data(supplement, change):
    change(supplement)
    with pytest.raises(ValueError):
        validate_supplement(seal(supplement), preview=True)


def test_site_draft_gate_navigation_and_unchanged_issues(supplement, tmp_path):
    # The existing archived reports are read-only inputs, not rewritten to add a county.
    archive = Path('website/updates')
    if not archive.exists():
        pytest.skip('Reviewed archive unavailable in this checkout')
    before = {p.name: p.read_bytes() for p in archive.glob('*.json')}
    supplement_path = tmp_path/'county.json'; supplement_path.write_text(json.dumps(supplement))
    with pytest.raises(ValueError, match='preview'):
        build_site(archive, tmp_path/'rejected', county_directories=[supplement_path])
    assert not (tmp_path/'rejected').exists()
    output = build_site(archive, tmp_path/'preview', preview=True, county_directories=[supplement_path])
    for name in ('index.html', 'directory.html', 'about.html'):
        soup = BeautifulSoup((output/name).read_text(), 'html.parser')
        assert soup.select_one('[data-court="clerk_broward"]')
    soup = BeautifulSoup((output/'directory.html').read_text(), 'html.parser')
    data = json.loads((output/soup.select_one('#archive-data')['href']).read_text())
    assert data['county_directories'] == [supplement]
    assert {i['id']: i for i in data['issues']} == {json.loads(raw)['id']: json.loads(raw) for raw in before.values()}
    assert {p.name: p.read_bytes() for p in archive.glob('*.json')} == before


def test_duplicate_county_and_cross_county_replacement_rejected(supplement, tmp_path):
    path = tmp_path/'county.json'; path.write_text(json.dumps(supplement))
    with pytest.raises(ValueError, match='one current supplement'):
        load_supplements([path, path], preview=True)
    archive = Path('website/updates')
    if not archive.exists():
        pytest.skip('Reviewed archive unavailable')
    old = next(person for p in archive.glob('*.json') for person in json.loads(p.read_text())['directory'])
    supplement['people'][0]['id'] = old['id']
    path.write_text(json.dumps(seal(supplement)))
    with pytest.raises(ValueError, match='another county'):
        build_site(archive, tmp_path/'rejected', preview=True, county_directories=[path])
    assert not (tmp_path/'rejected').exists()


def test_shared_legacy_identity_requires_matching_name_and_county(supplement, tmp_path):
    archive = Path('website/updates')
    old = next(person for path in archive.glob('*.json')
               for person in json.loads(path.read_text())['directory']
               if len(person['counties']) > 1)
    supplement['county'] = old['counties'][0]
    for person in supplement['people']:
        person['counties'] = [supplement['county']]
    supplement['people'][0].update(id=old['id'], name=old['name'])
    path = tmp_path/'shared.json'
    path.write_text(json.dumps(seal(supplement)))
    build_site(archive, tmp_path/'accepted', preview=True, county_directories=[path])
    supplement['people'][0]['name'] = 'Different person'
    path.write_text(json.dumps(seal(supplement)))
    with pytest.raises(ValueError, match='another county'):
        build_site(archive, tmp_path/'rejected', preview=True, county_directories=[path])


def test_js_temporal_selection_preserves_saved_contacts(supplement):
    node = shutil.which('node')
    if not node:
        pytest.skip('Node required for actual JavaScript selection tests')
    script = Path('src/flwu/data/web/search.js').resolve()
    program = r'''
const assert=require('node:assert/strict');
const {countyDirectoryView}=require(process.argv[1]);
let text='';process.stdin.on('data',x=>text+=x);process.stdin.on('end',()=>{
  const supplement=JSON.parse(text), base={id:'old',directory:[{id:'duval',name:'Existing',counties:['Duval']}]};
  const contacts={duval:{office:[{label:'Phone',lines:['old number']}],assistant:[]}};
  const before=JSON.stringify({base,contacts,supplement});
  const live=countyDirectoryView(base,'?court=clerk_broward',[supplement],contacts);
  assert.equal(live.entries.length,3);assert.equal(live.applied.length,1);
  assert.deepEqual(live.contacts.duval,contacts.duval);
  const person=supplement.people[0];
  const saved={id:person.id,name:person.name,counties:['Union'],court_ids:['circuit_eighth']};
  const overlap={id:'old',directory:[saved]};
  const overlapBefore=JSON.stringify(overlap);
  const refreshed=countyDirectoryView(overlap,'',[supplement],{});
  assert.equal(refreshed.entries.filter(p=>p.id===person.id).length,1);
  const current=refreshed.entries.find(p=>p.id===person.id);
  assert.ok(current.counties.includes('Union'));
  assert.ok(current.counties.includes(supplement.county));
  assert.ok(current.court_ids.includes('circuit_eighth'));
  assert.deepEqual(refreshed.contacts[person.id],person.contacts);
  assert.deepEqual(countyDirectoryView(overlap,'?issue=old',[supplement],{}).entries,[saved]);
  assert.equal(JSON.stringify(overlap),overlapBefore);
  for(const query of ['?issue=old','?from=2026-10-01&to=2026-10-31','?from=','?to=bad']){
    const view=countyDirectoryView(base,query,[supplement],contacts);
    assert.deepEqual(view.entries,base.directory);assert.equal(view.applied.length,0);
    assert.deepEqual(view.contacts,contacts);
  }
  const empty=countyDirectoryView(null,'',[supplement],{});
  assert.equal(empty.entries.length,2);
  assert.equal(JSON.stringify({base,contacts,supplement}),before);
});'''
    subprocess.run([node, '-e', program, str(script)], input=json.dumps(supplement), text=True, check=True, capture_output=True)


def test_legacy_judge_and_flat_clerk_are_projected_without_rewriting_sources():
    def entity(key, kind, facts):
        return dict(entity_key=key, kind=kind, facts=facts,
                    observation=dict(capture_seq=1, capture_id='a'*64, recorded_at='2026-10-16T12:00:00Z'),
                    citations=[dict(url='https://court.example/source', sha256='b'*64,
                                    retrieved_at='2026-10-16T11:00:00Z')])
    clerk = dict(name='Example Clerk', office_phone='813-555-0100',
                 mailing_address_lines=['Clerk', 'PO Box 1', 'Tampa, FL 33601'],
                 electronic_contact={'url': 'https://clerk.example/contact',
                                     'direct_civil_email': None,
                                     'review_scope': 'Public form only; no message submitted'},
                 locations=[{'name': 'Civil counter', 'address_lines': ['1 Court St', 'Tampa, FL 33602'],
                             'phone': '813-555-0100', 'hours': '8 AM–5 PM'},
                            {'name': 'Recording counter', 'address_lines': ['2 Court St', 'Tampa, FL 33602'],
                             'phone': '813-555-0199', 'service_scope': 'Recording only; not civil counter'}],
                 location_scope_note='Different sources list different services; not interchangeable')
    packet = dict(scope={'county': 'hillsborough'}, stream='test',
                  through_capture=dict(seq=1, capture_id='a'*64, recorded_at='2026-10-16T12:00:00Z', research_status='incomplete'),
                  entities=[entity('judge', 'judge', dict(name='Example Judge', contact={'phone': '813-555-0101'})),
                            entity('clerk', 'clerk', clerk),
                            entity('history', 'county_roster_reconciliation', dict(name='Old identity', historical_contact={'phone': '813-555-0111'}))])
    before = copy.deepcopy(packet)
    result, audit = make_supplement(packet, [dict(group_id='clerk_hillsborough', category='County Courts', label='Hillsborough County', url='https://court.example/')])
    assert packet == before
    assert [(p['id'], p['kind']) for p in result['people']] == [('judge', 'Judge'), ('clerk', 'Clerk')]
    rows = result['people'][1]['contacts']['office']
    by_path = {r['fact_path']: r for r in rows}
    assert by_path['mailing_address_lines']['lines'] == clerk['mailing_address_lines']
    assert by_path['mailing_address_lines']['type'] == 'address'
    assert by_path['locations.1.service_scope']['type'] == 'note'
    assert by_path['location_scope_note']['lines'] == [clerk['location_scope_note']]
    assert by_path['electronic_contact.url']['lines'] == ['https://clerk.example/contact']
    assert 'electronic_contact.direct_civil_email' not in by_path
    assert 'locations.0.phone' not in by_path  # common phone shown once
    assert by_path['locations.1.phone']['lines'] == ['813-555-0199']
    assert result['people'][1]['contacts']['assistant'] == []
    validate_supplement(result, preview=True)
    with pytest.raises(ValueError, match='preview'):
        validate_supplement(result)


def test_contact_container_projects_saved_clerk_division_routes_with_links():
    def entity(key, kind, facts):
        return dict(entity_key=key, kind=kind, facts=facts,
                    observation=dict(capture_seq=1, capture_id='a'*64, recorded_at='2026-10-20T12:00:00Z'),
                    citations=[dict(url='https://clerk.example/contact-us', sha256='b'*64,
                                    retrieved_at='2026-10-20T11:00:00Z')])
    clerk = dict(name='Example Clerk', role='Clerk of Circuit Court',
                 contact={'phone': '(850) 981-5554', 'fax': '(850) 626-7849',
                          'office_address': ['Santa Rosa County Court House', '4025 Avalon Blvd.', 'Milton, FL 32583'],
                          'mailing_address': ['6495 Caroline St. Suite A', 'Milton, FL 32570'],
                          'circuit_civil_phone': '(850) 981-5667',
                          'circuit_civil_email': 'Civil@example.gov',
                          'circuit_civil_fax': '(850) 983-4627',
                          'county_civil_phone': '(850) 981-5567',
                          'county_civil_email': 'Civil@example.gov',
                          'county_civil_fax': '(850) 983-4627',
                          'administration_phone': '(850) 983-1975',
                          'administration_email': 'Administration@example.gov',
                          'public_records_email': 'PublicRecordRequest@example.gov',
                          'court_related_correspondence': '4025 Avalon Blvd, Milton FL, 32583',
                          'other_correspondence': '6495 Caroline Street, Milton, FL 32570',
                          'website': 'https://clerk.example/'})
    packet = dict(scope={'county': 'santa_rosa'}, stream='test',
                  through_capture=dict(seq=1, capture_id='a'*64, recorded_at='2026-10-20T12:00:00Z', research_status='incomplete'),
                  entities=[entity('clerk', 'clerk', clerk)])
    before = copy.deepcopy(packet)
    result, audit = make_supplement(packet, [dict(group_id='county_santa_rosa', category='County Courts',
                                                  label='Santa Rosa', url='https://court.example/')])
    assert packet == before
    rows = result['people'][0]['contacts']['office']
    by_path = {r['fact_path']: r for r in rows}
    # Division routes display with their saved labels and contact links.
    assert by_path['contact.circuit_civil_phone']['label'] == 'Circuit civil phone'
    assert by_path['contact.circuit_civil_phone']['href'] == 'tel:8509815667'
    assert by_path['contact.circuit_civil_email']['href'] == 'mailto:Civil@example.gov'
    assert by_path['contact.circuit_civil_fax']['href'] == 'tel:8509834627'
    assert by_path['contact.county_civil_phone']['href'] == 'tel:8509815567'
    assert by_path['contact.county_civil_fax']['href'] == 'tel:8509834627'
    assert by_path['contact.administration_phone']['href'] == 'tel:8509831975'
    assert by_path['contact.administration_email']['href'] == 'mailto:Administration@example.gov'
    assert by_path['contact.public_records_email']['href'] == 'mailto:PublicRecordRequest@example.gov'
    # Identical shared email displays once per distinct division label.
    assert by_path['contact.circuit_civil_email']['lines'] == ['Civil@example.gov']
    assert by_path['contact.county_civil_email']['lines'] == ['Civil@example.gov']
    # Addresses render line-per-component with display whitespace repair.
    assert by_path['contact.office_address']['lines'] == ['Santa Rosa County Court House', '4025 Avalon Blvd.', 'Milton, FL 32583']
    assert by_path['contact.mailing_address']['lines'] == ['6495 Caroline St. Suite A', 'Milton, FL 32570']
    # Non-OFFICE correspondence routing stays in the research packet with a reason.
    omitted = audit['clerk']['omitted_contact_fields']
    assert 'contact.court_related_correspondence' in omitted
    assert 'contact.other_correspondence' in omitted
    assert 'contact.website' in omitted
    assert audit['clerk']['omission_reasons']['contact.website'] == 'ancillary_or_source_format_field_retained_in_research_packet'
    validate_supplement(result, preview=True)
    with pytest.raises(ValueError, match='preview'):
        validate_supplement(result)


def test_literal_source_path_backslash_encoding_preserves_url_security():
    from flwu.county_directory import directory_source_url
    assert directory_source_url('https://court.example/forms/a\\b.pdf') == 'https://court.example/forms/a%5Cb.pdf'
    assert directory_source_url('https://court.example/forms/a%5Cb.pdf') == 'https://court.example/forms/a%5Cb.pdf'
    for bad in ['https://court.example\\evil.example/file', 'https://user:pass@court.example/a\\b',
                'javascript:alert(1)', 'https://court.example/\na\\b', 'https://court.example/file?bad=\\value']:
        with pytest.raises(ValueError):
            directory_source_url(bad)


def test_unpublished_fax_displays_status_without_research_log_noise():
    field = {'status': 'not_published_in_reviewed_sources', 'value': None,
             'search_log': [{'url': 'https://court.example/directory', 'terms': 'fax',
                             'result': 'No chambers fax; program fax belongs to another office'}]}
    facts = {'contact': {'fax': field}}
    before = copy.deepcopy(facts)
    rows, omitted = contact_rows(facts)
    assert rows['office'] == [{'label': 'Fax', 'lines': ['Not published in the reviewed sources.'],
                              'fact_path': 'contact.fax', 'type': 'note'}]
    assert not omitted and facts == before
    # A contradictory supplied value must remain visible for review.
    facts['contact']['fax']['value'] = '813-555-0199'
    rows, _ = contact_rows(facts)
    assert '813-555-0199' in json.dumps(rows)


def test_officer_office_fields_and_source_variants_are_preserved_in_display():
    facts = {'contact': {'office_phone': '813-555-0100', 'office_email': 'office@example.org',
             'office_address': ['Room 3', '100 Court St', 'Tampa, FL 33602'],
             'office_fax': '813-555-0101', 'dependency_email': 'dependency@example.org',
             'procedure_email': 'different@example.org', 'office_email_scope': 'Header differs from procedure',
             'alternative_published_phone': '813-555-0102 (unresolved directory variant)',
             'mailing_address': {'lines': ['Room 5', '200 Court St', 'Tampa, FL 33602']},
             'phone_citation': {'quote': 'research-only evidence'}, 'zoom_meeting_id': '12345'}}
    rows, omitted = contact_rows(facts)
    paths = {r['fact_path']: r for r in rows['office']}
    assert paths['contact.office_phone']['href'] == 'tel:8135550100'
    assert paths['contact.office_email']['href'] == 'mailto:office@example.org'
    assert paths['contact.office_address']['type'] == 'address'
    assert paths['contact.mailing_address']['lines'] == facts['contact']['mailing_address']['lines']
    assert paths['contact.procedure_email']['type'] == 'note' and 'href' not in paths['contact.procedure_email']
    assert paths['contact.alternative_published_phone']['type'] == 'note'
    assert paths['contact.office_email_scope']['lines'] == ['Header differs from procedure']
    assert set(omitted) == {'contact.phone_citation', 'contact.zoom_meeting_id'}


def test_manual_receipt_fields_preserve_contacts_and_uncertainty():
    facts = {'fields': {
        'chambers_phone': {'status': 'verified', 'value': '305-555-0100; source differs: 305-555-0101'},
        'chambers_fax': {'status': 'verified', 'value': '305-555-0102'},
        'chambers_address': {'status': 'verified', 'value': ['Court Building', '1 Main St', 'Miami, FL 33128']},
        'assistant_name': {'status': 'verified', 'value': 'Named Assistant'},
        'assistant_contact': {'status': 'not_published', 'value': None, 'search_log': ['private research details']},
    }}
    before = copy.deepcopy(facts)
    rows, _ = contact_rows(facts)
    assert facts == before
    assert rows['office'][0]['lines'] == ['305-555-0100', 'source differs: 305-555-0101']
    assert 'href' not in rows['office'][0]
    fax = next(r for r in rows['office'] if r['fact_path'] == 'fields.chambers_fax.value')
    assert fax['label'] == 'Fax' and fax['lines'] == ['305-555-0102']
    assert 'href' not in fax
    assert next(r for r in rows['office'] if r.get('type') == 'address')['lines'] == ['Court Building', '1 Main St', 'Miami, FL 33128']
    assert rows['assistant'][0]['lines'] == ['Named Assistant']
    assert rows['assistant'][1]['type'] == 'note'
    assert 'private research details' not in json.dumps(rows)
    assert rows['assistant'][1]['fact_path'] == 'fields.assistant_contact.value'
    facts['contact'] = {'phone': '305-555-9999'}
    rows, _ = contact_rows(facts)
    assert len(rows['office']) == 1 and rows['office'][0]['lines'] == ['305-555-9999']
    assert rows['assistant'][0]['lines'] == ['Named Assistant']


@pytest.mark.parametrize('cards,assignment,expected', [
    ([{'role': 'Senior Judge'}], 'Senior assignment', 'Senior judge'),
    ([{'role': 'Administrative Magistrate'}], 'Title IV-D', 'General magistrate'),
    ([], 'Circuit Civil General Magistrate03 (CVGM03)', 'General magistrate'),
    ([{'role': 'County Judge'}], 'Refers matters to General Magistrate', 'Judge'),
])
def test_manual_person_role_uses_saved_roster_or_explicit_assignment(cards, assignment, expected):
    packet = dict(scope={'county': 'example'}, stream='test', through_capture={}, entities=[{
        'entity_key': 'person', 'kind': 'judge', 'facts': {'name': 'Person', 'assignment': assignment,
        'roster_cards_reviewed': cards}, 'citations': [], 'observation': {}}])
    before = copy.deepcopy(packet)
    result, _ = make_supplement(packet, [])
    assert result['people'][0]['kind'] == expected
    assert packet == before


@pytest.mark.parametrize('role,expected', [
    ('Magistrate', 'General magistrate'),
    ('Administrative Magistrate', 'General magistrate'),
    ('General Magistrate', 'General magistrate'),
    ('Special Master', 'Special master'),
    ('CSE Director & Hearing Officer', 'Hearing officer'),
    ('Hearing Officer', 'Hearing officer'),
    ('Administrative Hearing Officer', 'Hearing officer'),
    ('Traffic Hearing Officer', 'Hearing officer'),
    ('Civil Traffic Hearing Officer', 'Hearing officer'),
    ('General Magistrate / Hearing Officer', 'General magistrate'),
    ('Judge', 'Judge'),
    (None, 'Judge'),
])
def test_manual_receipt_explicit_officer_role_survives_projection(role, expected):
    packet = dict(scope={'county': 'orange'}, stream='test', through_capture={}, entities=[{
        'entity_key': 'person', 'kind': 'judge', 'facts': {
            'name': 'Person', 'role': role,
            'assignment': 'Division 5; hearings before assigned officer',
            'fields': {'chambers_phone': {'status': 'verified', 'value': '407-555-0100'}}},
        'citations': [], 'observation': {}}])
    before = copy.deepcopy(packet)
    result, _ = make_supplement(packet, [])
    assert result['people'][0]['kind'] == expected
    assert result['people'][0]['contacts']['office'][0]['lines'] == ['407-555-0100']
    assert packet == before


def test_building_address_preserves_chambers_and_does_not_duplicate_full_address():
    facts = {'fields': {'chambers_address': {'status': 'verified', 'value': 'Courthouse, Room 207'}},
             'building_address': {'value': '100 Court Street\nMiami, FL 33128', 'citation': {'url': 'https://court.example'}}}
    rows, _ = contact_rows(facts)
    assert [r['lines'] for r in rows['office']] == [['Courthouse, Room 207'], ['100 Court Street', 'Miami, FL 33128']]
    facts['fields']['chambers_address']['value'] += '\n100 Court Street\nMiami, FL 33128'
    rows, _ = contact_rows(facts)
    assert len(rows['office']) == 1
    assert rows['office'][0]['lines'] == ['Courthouse, Room 207', '100 Court Street', 'Miami, FL 33128']


def test_county_display_uses_matching_reviewed_navigation_label():
    packet = {'scope': {'county': 'miami_dade'}, 'stream': 'test', 'through_capture': {}, 'entities': []}
    courts = [{'category': 'County Courts', 'label': 'Miami-Dade County'}]
    result, _ = make_supplement(packet, courts)
    assert result['county'] == 'Miami-Dade'
    result, _ = make_supplement(packet, [{'category': 'County Courts', 'label': 'Broward County'}])
    assert result['county'] == 'Miami Dade'


@pytest.mark.parametrize('role,expected', [
    (None, 'General magistrate'),
    ('Family Law Magistrate', 'General magistrate'),
    ('Child Support Hearing Officer', 'Hearing officer'),
    ('Child Support Enforcement Hearing Officer', 'Hearing officer'),
    ('General Magistrate and Child Support Enforcement Hearing Officer', 'General magistrate'),
    ('Child Support Enforcement Hearing Officer', 'Hearing officer'),
])
def test_explicit_magistrate_record_is_not_silently_omitted(role, expected):
    packet = dict(scope={'county': 'palm_beach'}, stream='test', through_capture={}, entities=[{
        'entity_key': 'magistrate', 'kind': 'magistrate',
        'facts': {'name': 'Example Magistrate', 'assignment': 'Title IV-D', 'role': role,
                  'fields': {'chambers_phone': {'status': 'verified', 'value': '561-555-0100'},
                             'assistant_name': {'status': 'verified', 'value': 'Example Assistant'}}},
        'citations': [], 'observation': {}}])
    before = copy.deepcopy(packet)
    result, _ = make_supplement(packet, [])
    assert len(result['people']) == 1
    person = result['people'][0]
    assert person['kind'] == expected
    assert person['contacts']['office'][0]['lines'] == ['561-555-0100']
    assert person['contacts']['assistant'][0]['lines'] == ['Example Assistant']
    assert packet == before


def test_hearing_officer_kind_preserves_missing_contacts():
    packet = dict(scope={'county': 'volusia'}, stream='test', through_capture={}, entities=[{
        'entity_key': 'traffic-officer', 'kind': 'hearing_officer',
        'facts': {'name': 'Example Officer', 'role': 'Civil Traffic Infraction Hearing Officer',
                  'fields': {'office_phone': {'status': 'not_published', 'value': None}}},
        'citations': [], 'observation': {}}])
    before = copy.deepcopy(packet)
    result, _ = make_supplement(packet, [])
    assert len(result['people']) == 1
    person = result['people'][0]
    assert person['id'] == 'traffic-officer'
    assert person['kind'] == 'Hearing officer'
    assert person['contacts']['office'][0]['lines'] == ['Not published in the reviewed sources.']
    assert packet == before


def test_shared_identity_requires_matching_facts_and_retains_membership(supplement, tmp_path):
    other = copy.deepcopy(supplement)
    other['county'] = 'Miami-Dade'
    other['through_capture']['seq'] = 3
    for person in other['people']:
        person['counties'] = ['Miami-Dade']
        person['source_observation']['capture_seq'] = 3
    seal(other)
    paths = [tmp_path/'first.json', tmp_path/'second.json']
    for path, data in zip(paths, [supplement, other]):
        path.write_text(json.dumps(data))
    assert len(load_supplements(paths, preview=True)) == 2
    other['people'][0]['contacts']['office'][0]['lines'] = ['Different contact']
    paths[1].write_text(json.dumps(seal(other)))
    with pytest.raises(ValueError, match='Conflicting identity'):
        load_supplements(paths, preview=True)


def test_js_shared_identity_unions_evidence_without_changing_history(supplement):
    node = shutil.which('node')
    if not node:
        pytest.skip('Node required for actual JavaScript selection tests')
    program = r'''
const assert=require('node:assert/strict');
const {countyDirectoryView}=require(process.argv[1]);
let text='';process.stdin.on('data',x=>text+=x);process.stdin.on('end',()=>{
 const first=JSON.parse(text),second=structuredClone(first);
 second.county='Miami-Dade';
 second.people.forEach(p=>{p.counties=['Miami-Dade'];p.court_ids=['county_miami_dade'];p.source_observation.capture_seq=3;});
 const before=JSON.stringify([first,second]);
 const a=countyDirectoryView(null,'',[first,second],{});
 const b=countyDirectoryView(null,'',[second,first],{});
 assert.deepEqual(a.entries,b.entries);assert.equal(a.entries.length,2);
 for(const p of a.entries){assert.deepEqual(p.counties,['Broward','Miami-Dade']);assert.equal(p.source_observations.length,2);assert(p.court_ids.includes('county_miami_dade'));}
 assert.deepEqual(a.contacts,b.contacts);assert.equal(JSON.stringify([first,second]),before);
 for(const query of ['?issue=old','?from=2026-01-01&to=2026-02-01']){
  const history=countyDirectoryView({directory:[]},query,[first,second],{});
  assert.deepEqual(history.entries,[]);assert.deepEqual(history.applied,[]);
 }
});'''
    subprocess.run([node, '-e', program, str(Path('src/flwu/data/web/search.js').resolve())],
                   input=json.dumps(supplement), text=True, check=True, capture_output=True)


def test_public_metadata_retains_conflict_evidence_without_private_locations(supplement):
    from flwu.county_directory import public_metadata
    original = {'summary': 'Two official sources differ.', 'citations': [
        {'url': 'https://court.example/guide', 'sha256': 'a'*64,
         'retrieved_at': '2026-10-19T10:00:00Z', 'quote': 'Room 2',
         'path': '/Users/private/raw.pdf', 'text_path': 'runs/private.txt'}],
        'annotation_artifact': 'runs/annotations.json'}
    clean = public_metadata(original)
    assert clean['summary'] == original['summary']
    assert clean['citations'][0] == {k: v for k, v in original['citations'][0].items()
                                     if k not in {'path', 'text_path'}}
    assert 'annotation_artifact' not in clean
    assert original['citations'][0]['path'] == '/Users/private/raw.pdf'
    supplement['review_status'] = 'reviewed'
    supplement['review'] = dict(reviewed_by='Test reviewer', reviewed_at='2026-10-19T12:00:00Z', attestation='Test')
    supplement['people'][0]['conflicts'] = [original]
    with pytest.raises(ValueError, match='private evidence'):
        validate_supplement(seal(supplement))
    validate_supplement(seal(public_metadata(supplement)))


def test_county_filter_honors_reviewed_membership_and_preserves_legacy_fallback():
    node = shutil.which('node')
    if not node:
        pytest.skip('Node required for actual JavaScript selection tests')
    program = r'''
const assert=require('node:assert/strict');
const {matchesDirectoryCourt}=require(process.argv[1]);
const county={group_id:'clerk_example',label:'Example County'};
const circuit={group_id:'circuit_example',label:'Example Circuit'};
const scopes={circuit_example:['Example']};
const judge={counties:['Example'],court_ids:['circuit_example'],source_observation:{capture_seq:1}};
assert.equal(matchesDirectoryCourt(judge,county,scopes),false);
assert.equal(matchesDirectoryCourt(judge,circuit,scopes),true);
assert.equal(matchesDirectoryCourt({...judge,court_ids:['clerk_example']},county,scopes),true);
assert.equal(matchesDirectoryCourt({counties:['Example']},county,scopes),true);
assert.equal(matchesDirectoryCourt(judge,null,scopes),true);
'''
    subprocess.run([node, '-e', program, str(Path('src/flwu/data/web/search.js').resolve())],
                   check=True, capture_output=True)


@pytest.mark.parametrize('role,expected', [
    ('Circuit Judge', 'Judge'), ('County Judge', 'Judge'),
    ('Circuit Judge (Chief Judge)', 'Judge'),
    ('Special Master', 'Special master'),
    ('Chief Judge', 'Judge'),
    ('Senior Judge', 'Senior judge'), ('General Magistrate', 'General magistrate'),
    ('Child Support Hearing Officer', 'Hearing officer'),
    ('Child Support Enforcement Hearing Officer', 'Hearing officer'),
    ('General Magistrate and Child Support Enforcement Hearing Officer', 'General magistrate'),
    ('Hearing Officer', 'Hearing officer'),
    ('Civil Traffic Hearing Officer', 'Hearing officer'),
    ('Clerk of Circuit Court and Comptroller', 'Clerk'),
    ('Clerk', 'Clerk'),
])
def test_generic_person_is_projected_with_explicit_role_and_evidence(role, expected):
    entity = dict(entity_key='person-example', kind='person',
                  facts=dict(name='Example Person', role=role, assignment='Recorded assignment',
                             contact=dict(phone='850-555-0100', assistant_email='ja@example.org')),
                  observation={'capture_seq': 12},
                  citations=[dict(url='https://court.example/person', sha256='a'*64,
                                  retrieved_at='2026-10-20T12:00:00Z')])
    packet = dict(scope={'county': 'bay'}, stream='test', through_capture={},
                  entities=[entity, dict(entity_key='source', kind='source_review', facts={})])
    before = copy.deepcopy(packet)
    result, audit = make_supplement(packet, [])
    assert packet == before  # Publication must not rewrite research facts/history.
    assert len(result['people']) == 1
    person = result['people'][0]
    assert person['kind'] == expected
    assert person['assignment'] == 'Recorded assignment'
    assert person['source_observation'] == entity['observation']
    assert person['sources'] == entity['citations']
    assert any(row['lines'] == ['850-555-0100'] for row in person['contacts']['office'])
    assert any(row.get('href') == 'mailto:ja@example.org' for row in person['contacts']['assistant'])
    assert set(audit) == {'person-example'}


@pytest.mark.parametrize('role', [None, '', 'Retired volunteer', 'Judge?'])
def test_generic_person_unknown_role_requires_review(role):
    packet = dict(scope={'county': 'bay'}, stream='test', through_capture={}, entities=[
        dict(entity_key='unclassified', kind='person', facts=dict(name='Example', role=role))])
    with pytest.raises(ValueError, match='Unsupported explicit personnel role: unclassified'):
        make_supplement(packet, [])


def test_empty_address_remains_an_explicit_gap_without_invalid_empty_row():
    facts = {'contact': {'office_address': [], 'assistant_email': 'ja@example.org'}}
    before = copy.deepcopy(facts)
    rows, omitted = contact_rows(facts)
    assert rows['office'] == [{'label': 'Address',
                              'lines': ['Not published in the reviewed sources.'],
                              'fact_path': 'contact.office_address', 'type': 'note'}]
    assert rows['assistant'][0]['href'] == 'mailto:ja@example.org'
    assert 'contact.office_address' not in omitted
    assert facts == before


@pytest.mark.parametrize('role, expected', [
    ('Senior Judge', 'Senior judge'),
    ('General Magistrate and Child Support Enforcement Hearing Officer', 'General magistrate'),
])
def test_judge_record_preserves_explicit_office_without_roster_cards(role, expected):
    packet = dict(scope=dict(county='hendry'), stream='test-hendry',
                  through_capture=dict(seq=1), entities=[dict(
                      entity_key='hendry-officer', kind='judge',
                      facts=dict(name='Example Officer', role=role, assignment='Circuit-wide roster; specific sitting not established.',
                                 contact=dict(office_phone='863-555-0100')),
                      observation=dict(capture_seq=1), citations=[])])
    result, _ = make_supplement(packet, [])
    assert result['people'][0]['kind'] == expected
    assert result['people'][0]['assignment'] == packet['entities'][0]['facts']['assignment']
    assert result['people'][0]['contacts']['office'][0]['lines'] == ['863-555-0100']
