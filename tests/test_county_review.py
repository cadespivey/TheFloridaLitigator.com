"""County exports preserve evidence without changing research/publication state."""
import json
from pathlib import Path
import sqlite3

from bs4 import BeautifulSoup
import pytest

from flwu import history as h
from flwu.county_review import export_review, entity_filename, load_packet, index_page


def test_magistrate_is_grouped_with_personnel_not_shared_procedures():
    packet = dict(scope={'county': 'pasco'}, through_capture={'seq': 1, 'recorded_at': '2026-10-19'},
                  entities=[dict(entity_key='officer', kind='magistrate',
                                 facts={'name': 'Example Officer', 'assignment': 'Family Law Magistrate'})])
    soup = BeautifulSoup(index_page(packet), 'html.parser')
    tables = soup.find_all('table')
    assert 'Example Officer' in tables[0].get_text()
    assert 'Example Officer' not in tables[2].get_text()


@pytest.fixture
def history(tmp_path):
    db = tmp_path / 'history.sqlite'
    raw = b'<p>Fixture contact 555-0100</p>'
    cite = dict(url='https://court.example/profile', sha256=h.sha(raw),
                retrieved_at='2026-10-15T12:00:00Z', quote='Fixture contact', locator='paragraph 1')
    facts = dict(name='Judge <Example>', assignment='Civil division',
                 contacts=dict(phone='555-0100', judicial_assistant='Example Assistant',
                               division_email='division@example.org',
                               address_lines=['Courthouse, Room 1', '100 Court Street', 'City, FL 00000'],
                               email_role='Division mailbox; no personal assistant email established'),
                 dates={'effective_date': None}, checklist=[{'topic': 'orders', 'summary': 'Use portal', 'scope': 'civil only'}],
                 additional_field_states={'assistant_email': {'status': 'not_located'}},
                 conflicts=[{'description': 'Source A says 5 days; B says 10 days.'}])
    def save(conn, stream, county, value, run):
        return h.record(conn, stream=stream, mode='manual_research',
                        scope=dict(profile='county-baseline-v1', county=county, circuit=17), run_id=run,
                        payload=dict(status='incomplete', checks=[], drafts=[], findings=[dict(
                            key='same-person', kind='county_judge_baseline', facts=value, citations=[cite])]),
                        artifacts={h.sha(raw): raw}, recorded_at='2026-10-15T13:00:00Z')
    with h.database(db) as conn:
        first = save(conn, 'county-a', 'broward', facts, 'first')
        save(conn, 'county-b', 'other', {**facts, 'name': 'Different county'}, 'other')
        later = save(conn, 'county-a', 'broward', {**facts, 'name': 'Later name'}, 'later')
    return db, first['seq'], later['seq'], facts, cite


def snapshot(db):
    with sqlite3.connect(db) as conn:
        return '\n'.join(conn.iterdump())


def test_capture_scope_lossless_and_no_database_mutations(history, tmp_path):
    db, first, later, facts, cite = history
    before = snapshot(db)
    output = tmp_path / 'review'
    manifest = export_review(db, 'county-a', first, output)
    data = json.loads((output / 'packet.json').read_text())
    assert data['entities'][0]['facts'] == facts
    assert data['entities'][0]['citations'] == [cite]
    assert data['through_capture']['seq'] == first
    assert data['through_capture']['research_status'] == 'incomplete'
    assert manifest['entities'] == 1 and manifest['artifacts'] == 1
    assert manifest['publication_status'] == 'not_published'
    assert snapshot(db) == before
    # An explicit later cutoff changes the selected observation, not the old packet.
    with sqlite3.connect(db) as conn:
        assert load_packet(conn, 'county-a', later)['entities'][0]['facts']['name'] == 'Later name'
    with pytest.raises(ValueError, match='does not belong'):
        export_review(db, 'county-b', first, tmp_path / 'wrong')
    assert not (tmp_path / 'wrong').exists()


def test_repeatable_export_and_refuses_overwrite(history, tmp_path):
    db, first, *_ = history
    a, b = tmp_path / 'a', tmp_path / 'b'
    assert export_review(db, 'county-a', first, a) == export_review(db, 'county-a', first, b)
    assert {p.relative_to(a): p.read_bytes() for p in a.rglob('*') if p.is_file()} == {
        p.relative_to(b): p.read_bytes() for p in b.rglob('*') if p.is_file()}
    with pytest.raises(ValueError, match='already exists'):
        export_review(db, 'county-a', first, a)


@pytest.mark.parametrize('failure', ['missing', 'corrupt'])
def test_missing_or_corrupt_original_rejected_before_output(history, tmp_path, failure):
    db, first, *_ = history
    with sqlite3.connect(db) as conn:
        if failure == 'missing':
            conn.execute('DELETE FROM artifacts')
        else:
            conn.execute("UPDATE artifacts SET bytes=x'00'")
    output = tmp_path / 'rejected'
    with pytest.raises(ValueError, match='Missing or corrupt'):
        export_review(db, 'county-a', first, output)
    assert not output.exists()


def test_html_labels_qualifiers_dates_sources_and_local_links(history, tmp_path):
    db, first, *_ = history
    output = tmp_path / 'review'
    export_review(db, 'county-a', first, output)
    data = json.loads((output / 'packet.json').read_text())
    detail = BeautifulSoup((output / entity_filename(data['entities'][0])).read_text(), 'html.parser')
    assert detail.h1.get_text() == 'Judge <Example>'
    assert not detail.find('example')
    text = detail.get_text(' ', strip=True)
    for expected in ['Division email', 'no personal assistant email established', 'Effective date',
                     'Not established in this record', 'civil only', 'Source A says 5 days', 'not_located']:
        assert expected in text
    assert 'Fixture contact' not in text  # Original quotes belong in evidence JSON.
    assert len(detail.find_all('br')) == 2
    for html in output.glob('*.html'):
        soup = BeautifulSoup(html.read_text(), 'html.parser')
        assert soup.html['lang'] == 'en' and soup.find(id='main')
        assert soup.find('meta', attrs={'name': 'viewport'})
        for link in soup.select('a[href]'):
            href = link['href']
            if not href.startswith(('http:', 'https:', '#')):
                assert (output / href).is_file(), href


def test_historical_contact_never_becomes_current_directory_contact(history, tmp_path):
    db, first, _, _, cite = history
    with h.database(db) as conn:
        receipt = h.record(conn, stream='county-a', mode='manual_research',
                           scope=dict(profile='county-baseline-v1', county='broward', circuit=17), run_id='senior',
                           payload=dict(status='incomplete', checks=[], drafts=[], findings=[dict(
                               key='senior', kind='county_judge_baseline', facts=dict(name='Senior Example',
                               current_contact=None, current_contact_verified=False,
                               historical_contact={'phone': '555-9999'}, status='reviewed_with_gaps'), citations=[cite])]),
                           artifacts={})
    output = tmp_path / 'senior-review'
    export_review(db, 'county-a', receipt['seq'], output)
    text = BeautifulSoup((output / 'index.html').read_text(), 'html.parser').get_text(' ', strip=True)
    assert 'Individual contacts not established' in text and 'reviewed_with_gaps' in text
    assert '555-9999' not in text
    assert '555-9999' in (output / 'packet.json').read_text()


def test_legacy_judge_and_clerk_use_personnel_groups_with_flat_contacts():
    from flwu.county_review import index_page
    packet = {'scope': {'county': 'hillsborough'},
              'through_capture': {'seq': 1, 'recorded_at': '2026-10-18T12:00:00Z'},
              'entities': [
                  {'entity_key': 'judge', 'kind': 'judge', 'facts': {'name': 'Test Judge', 'contact': {'phone': '813-555-0100'}}},
                  {'entity_key': 'clerk', 'kind': 'clerk', 'facts': {'name': 'Test Clerk', 'office_phone': '813-555-0111',
                   'mailing_address_lines': ['Clerk', 'PO Box 2', 'Tampa, FL'], 'electronic_contact': {'url': 'https://clerk.example/contact'},
                   'locations': [], 'location_scope_note': 'Scope preserved'}}]}
    soup = BeautifulSoup(index_page(packet), 'html.parser')
    judge_group = soup.find('h2', string='Judges and judicial officers').find_next('table').get_text(' ', strip=True)
    clerk_group = soup.find('h2', string='Clerk and court administration').find_next('table').get_text(' ', strip=True)
    assert 'Test Judge' in judge_group and '813-555-0100' in judge_group
    assert 'Test Clerk' in clerk_group and '813-555-0111' in clerk_group and 'PO Box 2' in clerk_group
    assert 'Test Clerk' not in judge_group and 'Test Judge' not in clerk_group
