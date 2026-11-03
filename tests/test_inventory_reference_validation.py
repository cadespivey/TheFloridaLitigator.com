"""Inventory transport provenance and quoted identity claims have distinct roles."""
import copy
import json

import pytest

from flwu import history as h, workflow as w, workflow_report as report
from tests.test_person_projection_identity import acquired_person
from tests.test_workflow import answer, complete_analysis, environment


@pytest.fixture
def acquired_inventory(acquired_person):
    run, database, person = acquired_person
    claim = copy.deepcopy(person['citations'][0])
    transport = {k: claim[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status')}
    inventory = dict(key='roster-transport', kind='source_inventory',
                     facts={'candidate_ids': [], 'entities': [dict(id=person['key'].removeprefix('person-'),
                            name=person['facts']['name'], type='judge', counties=['Broward'], citation=claim)]},
                     citations=[transport])
    return run, database, person, inventory


def test_inventory_keeps_acquisition_references_and_separate_quoted_identities(acquired_inventory):
    run, database, _, inventory = acquired_inventory
    before = copy.deepcopy(inventory)
    with h.database(database) as conn:
        report.validate_records(conn, w.load(run), [inventory])
    assert inventory == before
    assert 'quote' not in inventory['citations'][0]
    assert inventory['facts']['entities'][0]['citation']['quote']


@pytest.mark.parametrize(('field', 'replacement'), [
    ('url', 'https://court.gov/another-page'),
    ('sha256', '0' * 64),
    ('retrieved_at', '2020-01-01T00:00:00Z'),
    ('http_status', 404),
])
def test_unquoted_inventory_reference_still_requires_exact_acquisition(acquired_inventory, field, replacement):
    run, database, _, inventory = acquired_inventory
    inventory['citations'][0][field] = replacement
    with h.database(database) as conn, pytest.raises(ValueError, match='does not match an acquired'):
        report.validate_records(conn, w.load(run), [inventory])


@pytest.mark.parametrize('failure', ['missing_quote', 'different_name', 'missing_citation'])
def test_acquisition_metadata_never_substitutes_for_a_named_person_claim(acquired_inventory, failure):
    run, database, _, inventory = acquired_inventory
    entity = inventory['facts']['entities'][0]
    if failure == 'missing_quote':
        entity['citation']['quote'] = ''
    elif failure == 'different_name':
        entity['name'] = 'Different B. Person'
    else:
        entity['citation'] = {}
    with h.database(database) as conn, pytest.raises(ValueError, match='actual full person name'):
        report.validate_records(conn, w.load(run), [inventory])


def test_person_record_still_requires_quoted_top_level_evidence(acquired_inventory):
    run, database, person, inventory = acquired_inventory
    person['citations'] = copy.deepcopy(inventory['citations'])
    with h.database(database) as conn, pytest.raises(ValueError, match='Projection requires quoted evidence'):
        report.validate_records(conn, w.load(run), [person])


def test_standard_report_prepares_inventory_metadata_without_rewriting_it(acquired_inventory):
    run, database, person, inventory = acquired_inventory
    before = copy.deepcopy(inventory)
    attached = False
    for _ in range(40):
        task = w.inspect(run, emit=True)
        if 'packet' not in task:
            break
        packet = w.read(task['packet'])
        if packet['kind'] == 'publication_mapping' and not attached:
            receipt = copy.deepcopy(packet['receipt_template'])
            receipt.update(decision='include', reason='Fixture opinion and source-bound named roster.',
                           personnel=[person], inventories=[inventory])
            w.write(task['save_receipt'], receipt)
            w.submit(run, task['packet'], task['save_receipt'])
            attached = True
        else:
            answer(run, database, task)
    assert attached and task['phase'] == 'prepare_report'
    prepared = report.prepare(run)
    assert inventory == before
    assert [(p['id'], p['name']) for p in w.read(prepared['public_preview'])['directory']] == [
        (person['key'], person['facts']['name'])]
    with h.database(database) as conn:
        payload = json.loads(conn.execute('SELECT payload FROM captures WHERE capture_id=?',
                                          (prepared['capture_id'],)).fetchone()[0])
        assert next(f for f in payload['findings'] if f['key'] == inventory['key']) == before
        assert h.latest_finalized(conn, 'weekly') is None


def test_one_index_per_assembly_pass_and_fresh_artifact_checks_on_next_pass(tmp_path, monkeypatch):
    run, database, _, server = environment(tmp_path)
    phase, _ = complete_analysis(run, database)
    assert phase['phase'] == 'prepare_report'
    fetches = len(server.calls)
    real_index = report.AcquisitionIndex
    built = []
    def counting_index(*args, **kwargs):
        index = real_index(*args, **kwargs)
        built.append(index)
        return index
    monkeypatch.setattr(report, 'AcquisitionIndex', counting_index)
    with h.database(database) as conn:
        config = w.load(run)
        queue = w.latest_queue(conn, config)
        records, _, _, _ = report.assemble(conn, config, queue)
        assert len(built) == 1
        cited = next(record['citations'][0] for record in records.values() if record['kind'] == 'candidate')
        conn.execute('UPDATE artifacts SET bytes=? WHERE sha256=?', (b'changed fixture artifact', cited['sha256']))
        conn.commit()
        with pytest.raises(ValueError, match='artifact missing or changed'):
            report.assemble(conn, config, queue)
        assert len(built) == 2
        assert built[0] is not built[1]
    assert len(server.calls) == fetches
