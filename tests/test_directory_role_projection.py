"""New directory entries retain reviewed office titles instead of becoming judges."""
import copy
import pytest

from flwu import history as h, workflow as w, workflow_directory as directory, workflow_report as report
from tests.test_county_directory import supplement, seal
from tests.test_workflow import answer, environment


@pytest.mark.parametrize('kind,role,expected', [
    ('judge', 'Special master; General Counsel', 'Special master'),
    ('judge', 'General magistrate', 'General magistrate'),
    ('judge', 'Senior judge', 'Senior judge'),
    ('judge', None, 'Judge'),
    ('clerk', None, 'Clerk'),
    ('judge', 'Unsupported office title', None),
])
def test_new_entry_preserves_reviewed_role_and_existing_people(tmp_path, supplement, kind, role, expected):
    supplement['review_status'] = 'reviewed'
    supplement['review'] = dict(reviewed_by='Prior editor', reviewed_at='2026-10-17T13:00:00Z',
                                attestation='Fixture directory reviewed.')
    seal(supplement)
    current = tmp_path/'broward.json'
    w.write(current, supplement)
    text = f'Riley Example. {role or expected}. Broward office. Phone: 954-555-0200.'.encode()
    run, database, _, _ = environment(tmp_path, directories=[current], profile=text)
    for _ in range(40):
        task = w.inspect(run, emit=True)
        if 'packet' not in task:
            break
        packet = w.read(task['packet'])
        receipt = copy.deepcopy(packet['receipt_template'])
        if packet['kind'] == 'source_review' and packet['inputs']['url'] == 'https://court.gov/profile':
            observation = packet['inputs']['observation']
            ref = {k: observation[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status')}
            ref.update(quote=text.decode(), locator='Named fixture office')
            facts = dict(name='Riley Example', fields={'chambers_phone': dict(value='954-555-0200', citation=ref)})
            if role is not None:
                facts['role'] = role
            person = dict(key='person-role-person', kind=kind, facts=facts, citations=[ref], expected_version=None)
            inventory = dict(key='role-roster', kind='source_inventory', citations=[ref], expected_version=None,
                             facts={'entities': [dict(id='role-person', name='Riley Example', type=kind,
                                                      counties=['Broward'], citation=ref)]})
            receipt.update(reviewer='Fixture editor', outcome='updated_findings', summary='Named office and contacts.',
                           review_scope='One new directory entry.', findings=[person, inventory],
                           support=dict(reason='Official fixture names this office.', previous=[],
                                        current=[{k: ref[k] for k in ('sha256', 'text_sha256', 'quote', 'locator')}]))
        elif packet['kind'] == 'publication_mapping' and packet['inputs']['finding']['kind'] != 'opinion':
            finding = packet['inputs']['finding']
            receipt.update(decision='include_directory' if finding['kind'] in ('judge', 'clerk') else 'exclude',
                           candidate=None, reason='Supported directory record, not a new legal development.')
            if finding['kind'] == 'source_inventory':
                receipt['inventories'] = [finding]
        else:
            answer(run, database, task)
            continue
        w.write(task['save_receipt'], receipt)
        w.submit(run, task['packet'], task['save_receipt'])
    assert task['phase'] == 'prepare_report'
    report.prepare(run)
    task = w.inspect(run, emit=True)
    packet = w.read(task['packet'])
    assert packet['identity'] == 'person-role-person'
    assert packet['inputs'].get('source_role') == role
    receipt = copy.deepcopy(packet['receipt_template'])
    receipt.update(targets=[dict(path=str(current), id=None)], reviewer='Fixture directory editor',
                   reason='New named office with the reviewed role and published contact.')
    w.write(task['save_receipt'], receipt)
    w.submit(run, task['packet'], task['save_receipt'])
    if expected is None:
        with pytest.raises(ValueError, match='Unsupported explicit directory role'):
            directory.refresh(run)
        assert w.read(current) == supplement
        return
    refreshed = directory.refresh(run)
    output = w.read(refreshed['directory_paths'][0])
    assert output['people'][:len(supplement['people'])] == supplement['people']
    new = next(p for p in output['people'] if p['id'] == 'person-role-person')
    assert new['kind'] == expected
    assert '954-555-0200' in str(new['contacts'])
    assert w.read(current) == supplement
    with h.database(database) as conn:
        assert h.latest_finalized(conn, 'weekly') is None
