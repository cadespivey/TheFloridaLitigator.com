"""Person display casing must not alter quoted or acquired identity evidence."""
import copy

import pytest

from flwu import history as h, source_gate as g, workflow as w
from flwu import workflow_report as report
from flwu.evidence_binding import AcquisitionIndex
from tests.test_workflow import answer, environment


PROFILE = b"Chief Judge\nCATHERINE  A.\nSAMPLE\nBroward Circuit Civil\nOffice phone: 954-555-0200."
NAME = 'Catherine A. Sample'


@pytest.fixture
def acquired_person(tmp_path):
    run, database, registry, _ = environment(tmp_path, profile=PROFILE)
    with h.database(database) as conn:
        observation = AcquisitionIndex(conn, registry['stream']).source_observations['https://court.gov/profile']
        ref = {k: observation[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status')}
        ref.update(quote=g.blob(conn, observation['text_sha256']).decode(), locator='Fixture roster and office')
    person = dict(key='person-case-format-judge', kind='judge',
                  facts=dict(name=NAME, fields={'chambers_phone': dict(value='954-555-0200', status='verified', citation=ref)}),
                  citations=[ref])
    return run, database, person


@pytest.mark.parametrize('display_name', [NAME, 'CATHERINE A. SAMPLE', '  Catherine   A. Sample  '])
def test_projection_accepts_supported_case_and_whitespace_without_rewriting_evidence(acquired_person, display_name):
    run, database, person = acquired_person
    person['facts']['name'] = display_name
    before = copy.deepcopy(person)
    with h.database(database) as conn:
        report.validate_records(conn, w.load(run), [person])
        assert g.blob(conn, person['citations'][0]['sha256']) == PROFILE
    assert person == before


@pytest.mark.parametrize('unsupported_name', ['Different B. Person', 'Catherine Sample', 'Catherine A. Samples'])
def test_projection_rejects_different_or_incomplete_names(acquired_person, unsupported_name):
    run, database, person = acquired_person
    person['facts']['name'] = unsupported_name
    with h.database(database) as conn, pytest.raises(ValueError, match='not supported by cited identity evidence'):
        report.validate_records(conn, w.load(run), [person])


def test_projection_still_rejects_role_heading(acquired_person):
    run, database, person = acquired_person
    person['facts']['name'] = 'Chief Judge'
    with h.database(database) as conn, pytest.raises(ValueError, match='placeholder, heading or location'):
        report.validate_records(conn, w.load(run), [person])


def test_projection_cannot_recase_the_original_quote(acquired_person):
    run, database, person = acquired_person
    person['citations'][0]['quote'] = NAME
    with h.database(database) as conn, pytest.raises(ValueError, match='quote absent from acquired extraction'):
        report.validate_records(conn, w.load(run), [person])


def test_projection_finds_identity_after_another_valid_citation(acquired_person):
    run, database, person = acquired_person
    other = dict(person['citations'][0], quote='Office phone: 954-555-0200.')
    person['citations'].insert(0, other)
    with h.database(database) as conn:
        report.validate_records(conn, w.load(run), [person])


def test_standard_report_preparation_accepts_uppercase_roster_with_display_case(tmp_path):
    run, database, _, _ = environment(tmp_path, profile=PROFILE)
    for _ in range(40):
        task = w.inspect(run, emit=True)
        if 'packet' not in task:
            break
        packet = w.read(task['packet'])
        receipt = copy.deepcopy(packet['receipt_template'])
        if packet['kind'] == 'source_review' and packet['inputs']['url'] == 'https://court.gov/profile':
            observation = packet['inputs']['observation']
            with h.database(database) as conn:
                quote = g.blob(conn, observation['text_sha256']).decode()
            ref = {k: observation[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status')}
            ref.update(quote=quote, locator='Fixture roster and office')
            person = dict(key='person-case-format-judge', kind='judge', expected_version=None,
                          facts=dict(name=NAME, fields={'chambers_phone': dict(value='954-555-0200', status='verified', citation=ref)}), citations=[ref])
            roster = dict(key='roster-case-format', kind='source_inventory', expected_version=None,
                          facts={'entities': [dict(id='case-format-judge', name=NAME, type='judge', counties=['Broward'], citation=ref)]}, citations=[ref])
            receipt.update(reviewer='Fixture editor', summary='Named civil judge and office.',
                           review_scope='Fixture roster only', outcome='updated_findings', findings=[person, roster],
                           support=dict(reason='Original uppercase roster supports this display name.',
                                        current=[{k: ref[k] for k in ('sha256', 'text_sha256', 'quote', 'locator')}], previous=[]))
        elif packet['kind'] == 'publication_mapping' and packet['inputs']['finding']['kind'] != 'opinion':
            finding = packet['inputs']['finding']
            receipt.update(decision='include_directory' if finding['kind'] == 'judge' else 'exclude', candidate=None,
                           reason='Source-bound person and named roster belong in the directory.')
            if finding['kind'] == 'source_inventory':
                receipt['inventories'] = [finding]
        else:
            answer(run, database, task)
            continue
        w.write(task['save_receipt'], receipt)
        w.submit(run, task['packet'], task['save_receipt'])
    assert task['phase'] == 'prepare_report'
    prepared = report.prepare(run)
    people = w.read(prepared['public_preview'])['directory']
    assert [(person['id'], person['name']) for person in people] == [('person-case-format-judge', NAME)]
    with h.database(database) as conn:
        assert g.blob(conn, ref['sha256']) == PROFILE
        assert h.latest_finalized(conn, 'weekly') is None
