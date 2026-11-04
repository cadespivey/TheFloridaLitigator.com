"""Optional directory citations remain bound without indexing absent citations."""
import copy

import pytest

from flwu import history as h, workflow as w, workflow_directory as directory


@pytest.fixture
def directory_review(tmp_path):
    path = tmp_path / 'directory.json'
    current = {'people': [{'id': 'person-test', 'name': 'Actual Person'}]}
    w.write(path, current)
    target = {'path': str(path), 'id': 'person-test'}
    receipt = dict(person_id='person-test', targets=[target], reviewer='Fixture editor',
                   reason='Keep the existing supported entry.', identity_citations=[],
                   assignment_updates=[])
    task = dict(kind='directory_review', identity='person-test',
                receipt_template={key: None for key in receipt},
                inputs=dict(person={'id': 'person-test', 'name': 'Actual Person'},
                            capture_id='prepared-fixture', exact_matches=[target],
                            scopes={str(path): {'sha256': h.sha(current)}}))
    return path, task, receipt


def forbid_index(*args, **kwargs):
    raise AssertionError('No supplied citations: acquisition index must not be constructed')


def test_exact_directory_target_without_extra_citations_needs_no_index(directory_review, monkeypatch):
    path, task, receipt = directory_review
    before = (path.read_bytes(), copy.deepcopy(task), copy.deepcopy(receipt))
    monkeypatch.setattr(directory, 'AcquisitionIndex', forbid_index)
    assert directory.validate_decision(None, {'registry': {'stream': 'report'}}, task, receipt) == {
        'validated': 'directory_projection', 'capture_id': 'prepared-fixture'}
    assert (path.read_bytes(), task, receipt) == before


def test_no_extra_citations_still_rejects_changed_directory_bytes(directory_review, monkeypatch):
    path, task, receipt = directory_review
    monkeypatch.setattr(directory, 'AcquisitionIndex', forbid_index)
    w.write(path, {'people': [{'id': 'person-test', 'name': 'Independently edited'}]})
    before = path.read_bytes()
    with pytest.raises(ValueError, match='Directory changed since review packet'):
        directory.validate_decision(None, {'registry': {'stream': 'report'}}, task, receipt)
    assert path.read_bytes() == before


def acquired(conn):
    raw = b'Fixture original bytes'
    text = b'Judge Actual Person serves Example civil division.'
    observation = dict(url='https://court.example/profile', sha256=h.sha(raw),
                       text_sha256=h.sha(text), retrieved_at='2026-10-22T12:00:00Z',
                       http_status=200, success=True)
    h.record(conn, stream='acquisition', mode='manual_research',
             scope={'target_stream': 'report'}, run_id='fixture-acquisition',
             payload=dict(status='incomplete', contract={}, checks=[], findings=[], drafts=[],
                          source_gate=observation), artifacts={h.sha(raw): raw, h.sha(text): text})
    return dict({key: value for key, value in observation.items() if key != 'success'},
                quote=text.decode(), locator='Fixture named assignment')


def assignment(path, ref):
    return dict(path=str(path), value='Example civil division', reason='Named official-shaped fixture.',
                citations=[ref])


def test_identity_and_assignment_citations_share_one_real_index(directory_review, tmp_path, monkeypatch):
    path, task, receipt = directory_review
    built = []
    actual = directory.AcquisitionIndex
    def counted(conn, stream):
        built.append(stream)
        return actual(conn, stream)
    monkeypatch.setattr(directory, 'AcquisitionIndex', counted)
    with h.database(tmp_path / 'history.sqlite') as conn:
        ref = acquired(conn)
        receipt['identity_citations'] = [ref]
        receipt['assignment_updates'] = [assignment(path, ref)]
        before = (path.read_bytes(), copy.deepcopy(receipt), conn.execute('SELECT count(*) FROM captures').fetchone()[0])
        result = directory.validate_decision(conn, {'registry': {'stream': 'report'}}, task, receipt)
        assert result['validated'] == 'directory_projection'
        assert built == ['report']
        assert (path.read_bytes(), receipt, conn.execute('SELECT count(*) FROM captures').fetchone()[0]) == before


@pytest.mark.parametrize('route', ['identity', 'assignment'])
@pytest.mark.parametrize('damage', ['url', 'hash', 'time', 'quote', 'artifact', 'stream'])
def test_supplied_citation_binding_checks_are_not_skipped(directory_review, tmp_path, route, damage):
    path, task, receipt = directory_review
    with h.database(tmp_path / 'history.sqlite') as conn:
        ref = acquired(conn)
        stream = 'report'
        if damage == 'url': ref['url'] = 'https://court.example/another-page'
        elif damage == 'hash': ref['sha256'] = '0' * 64
        elif damage == 'time': ref['retrieved_at'] = '2026-10-23T12:00:00Z'
        elif damage == 'quote': ref['quote'] = 'Judge Actual Person serves Imaginary division.'
        elif damage == 'artifact':
            conn.execute('UPDATE artifacts SET bytes=? WHERE sha256=?', (b'Damaged bytes', ref['sha256']))
        elif damage == 'stream': stream = 'unrelated'
        if route == 'identity': receipt['identity_citations'] = [ref]
        else: receipt['assignment_updates'] = [assignment(path, ref)]
        before = (path.read_bytes(), copy.deepcopy(receipt), conn.execute('SELECT count(*) FROM captures').fetchone()[0])
        with pytest.raises(ValueError, match='does not match|quote absent|artifact missing or changed'):
            directory.validate_decision(conn, {'registry': {'stream': stream}}, task, receipt)
        assert (path.read_bytes(), receipt, conn.execute('SELECT count(*) FROM captures').fetchone()[0]) == before
