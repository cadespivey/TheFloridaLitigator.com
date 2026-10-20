"""Rejections and persistence tests for the model/data execution boundary."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest
from flwu.controlled_worker import make_packet, run_task, validate_receipt, check_report, render_report
from flwu.research import _citation
from flwu.worker_contract import temporal_status

TRIALS = Path(__file__).resolve().parents[1]/'trials'
sys.path.insert(0, str(TRIALS))
from controlled_replay import prepare, acquire, tasks_from_evidence


@pytest.fixture
def packet(tmp_path):
    root = tmp_path/'trial'; prepare(root); refs = acquire(root)
    tasks, _ = tasks_from_evidence(root, refs)
    task = next(t for t in tasks if t['id'] == 'R-APEX')
    data, spans = make_packet(root, task, [refs[p] for p in task['dependencies']], '2026-10-05', '2026-10-11')
    current = next(k for k,v in spans.items() if 'We change' in v['quote'])
    prior = next(k for k,v in spans.items() if v['endpoint'].startswith('rules/') and 'Cross-reference:' in v['quote'])
    answer = {'id': task['id'], 'decision': 'include', 'reason': 'in_window', 'publication_date': '2026-10-05',
              'effective_date': '2027-02-01', 'legal_status': 'future_effective', 'summary_spans': [current],
              'author': 'Chief Justice John D. Couriel', 'concurrence': 'Justice Jorge Labarga concurs in result only.',
              'citations': [current], 'changes': [{'before': 'subdivision (b)', 'after': 'subdivision (c)', 'citations': [current, prior]}]}
    return root, refs, task, data, spans, answer


@pytest.mark.parametrize('failure', ['future', 'invented_span', 'shell', 'missing', 'prior', 'outside_window', 'no_op_change', 'withdrawal_omission', 'contradictory_prose'])
def test_mutations_rejected(packet, failure):
    root, refs, task, data, spans, answer = packet
    if failure == 'future': answer['legal_status'] = 'operative; takes effect 2027-02-01'
    if failure == 'invented_span': answer['citations'] = ['../../private-corpus.json']
    if failure == 'shell': answer['execute'] = 'cat private-corpus.json'
    if failure == 'missing': del answer['concurrence']
    if failure == 'prior': answer['changes'][0]['citations'] = answer['citations']
    if failure == 'outside_window': answer['publication_date'] = '2026-10-04'
    if failure == 'no_op_change': answer['changes'][0]['after'] = answer['changes'][0]['before']
    if failure == 'contradictory_prose': answer['reason'] = 'Included with operative status until the future effective date'
    if failure == 'withdrawal_omission': answer.update(legal_status='withdrawn', decision='exclude', effective_date=None)
    with pytest.raises(ValueError): validate_receipt(root, task, answer, spans, '2026-10-05', '2026-10-11')


def test_replay_cannot_be_live_evidence(packet):
    root, _, _, _, spans, _ = packet
    ref = next(iter(spans.values()))
    _citation(root, ref, mode='synthetic_replay')
    with pytest.raises(ValueError): _citation(root, ref)
    altered = {**ref, 'synthetic': False}
    with pytest.raises(ValueError): _citation(root, altered, mode='synthetic_replay')


def test_future_worker_receives_only_frozen_history_for_its_entity(packet):
    from flwu.history_capture import capture
    root, refs, task, _, _, answer = packet
    run_task(root, task, [refs[p] for p in task['dependencies']], '2026-10-05', '2026-10-11',
             complete=lambda _: (json.dumps(answer), {}))
    capture(root)
    future = root.parent/'future'; prepare(future); new_refs = acquire(future)
    tasks, _ = tasks_from_evidence(future, new_refs)
    same_task = next(t for t in tasks if t['id'] == task['id'])
    evidence = [new_refs[p] for p in same_task['dependencies']]
    data, _ = make_packet(future, same_task, evidence, '2026-10-05', '2026-10-11')
    assert data['historical_context']['facts']['effective_date'] == '2027-02-01'
    assert 'current_findings' not in data['historical_context']
    assert not data['historical_context']['baseline_known']
    (future/'prior-history.json').write_text('{}')
    with pytest.raises(ValueError, match='Frozen historical context'):
        make_packet(future, same_task, evidence, '2026-10-05', '2026-10-11')


def test_longitudinal_edits_are_verified_and_frozen_before_inference(tmp_path):
    from controlled_replay import verify_contract
    root = tmp_path/'edited'
    edits = {'procedures/casey-morgan': {'three business days': 'four business days'}}
    prepare(root, source_edits=edits)
    assert verify_contract(root)['source_edits'] == edits
    assert 'four business days' in json.loads((root/'private-corpus.json').read_text())['procedures/casey-morgan']['body']
    invalid = tmp_path/'invalid'
    with pytest.raises(ValueError, match='Trial edit does not match'):
        prepare(invalid, source_edits={'roster/current': {'nonexistent assistant': 'new assistant'}})
    assert not (invalid/'contract.json').exists()


def test_validation_feedback_then_immutable_resume(packet):
    root, refs, task, _, _, answer = packet
    calls = []
    def complete(request):
        calls.append(request)
        result = copy.deepcopy(answer)
        if len(calls) == 1: result['legal_status'] = 'operative'
        return json.dumps(result), {}
    evidence = [refs[p] for p in task['dependencies']]
    receipt, status = run_task(root, task, evidence, '2026-10-05', '2026-10-11', complete=complete)
    assert status == 'accepted' and len(calls) == 2
    assert 'validation_feedback' in calls[1]
    from flwu.history_capture import capture
    from flwu.history import database, compare
    marker = capture(root)
    with database() as conn:
        context = compare(conn, marker['stream'])
        assert context['current_findings']['candidate:R-APEX']['facts']['effective_date'] == '2027-02-01'
        assert context['coverage_gaps']  # The blocked source remains required.
        assert conn.execute('SELECT count(*) FROM artifacts').fetchone()[0] > 0
    original = (root/'accepted/R-APEX.json').read_bytes()
    again, status = run_task(root, task, evidence, '2026-10-05', '2026-10-11', complete=lambda _: pytest.fail('Must not rerun accepted task'))
    assert status == 'reused' and (root/'accepted/R-APEX.json').read_bytes() == original
    (root/refs[task['dependencies'][0]]['path']).write_text('tampered')
    with pytest.raises(ValueError, match='hash mismatch'):
        run_task(root, task, evidence, '2026-10-05', '2026-10-11', complete=complete)


def test_coordinator_keeps_blocked_denominator_and_discovers_roster(packet):
    root, refs, _, _, _, _ = packet
    state = json.loads((root/'state.json').read_text())
    assert len(state['required']) == 23 and len(refs) == 21
    assert 'circuits/orders' not in refs and 'procedures/casey-morgan' not in refs
    events = json.loads((root/'network.json').read_text())
    assert [e['status'] for e in events if e['endpoint'] == 'opinions/C-START'] == [429, 200]
    tasks, clerks = tasks_from_evidence(root, refs)
    assert len(tasks) == 9 and len(clerks) == 7
    assert 'blake-quinn' not in {t['id'] for t in tasks}
    (root/'control.json').write_text('{"restored":true}')
    assert len(acquire(root)) == 23


@pytest.mark.parametrize('failure', ['negative_log', 'procedure_citations', 'governing_citations', 'wrong_circuit', 'archive_contact'])
def test_judge_rejections(packet, failure):
    root, refs, _, _, _, _ = packet
    tasks, _ = tasks_from_evidence(root, refs)
    task = next(t for t in tasks if t['id'] == 'dana-reed')
    _, spans = make_packet(root, task, [refs[p] for p in task['dependencies']], '2026-10-05', '2026-10-11')
    ids = lambda ep: [k for k,v in spans.items() if v['endpoint'] == ep]
    answer = {'name': 'Dana Reed', 'county': 'Putnam', 'circuit': 7, 'division': 'Civil C', 'chambers_phone': '386-555-0301',
              'address': '300 Example Street', 'assistant_name': 'Taylor Finch', 'assistant_contact': 'taylor.finch@example.invalid',
              'citations': ids(task['profile']),
              'procedure': {'status': 'no_published_procedure_located', 'effective_date': None, 'legal_status': 'unknown',
                            'summary_spans': ids('procedures/index'), 'search_log': ['procedures/index: zero results for Dana Reed'],
                            'citations': ids('procedures/index')},
              'governing_rules': [{'summary_spans': ids('circuits/AO-2025-01'), 'citations': ids('circuits/AO-2025-01')}]}
    validate_receipt(root, task, answer, spans, '2026-10-05', '2026-10-11')
    if failure == 'negative_log': answer['procedure']['search_log'] = []
    if failure == 'procedure_citations': answer['procedure']['citations'] = []
    if failure == 'governing_citations': answer['governing_rules'][0]['citations'] = []
    if failure == 'wrong_circuit': answer['circuit'] = 4
    if failure == 'archive_contact': answer['assistant_name'] = 'Riley Brook'
    with pytest.raises(ValueError): validate_receipt(root, task, answer, spans, '2026-10-05', '2026-10-11')


def test_deterministic_render_links_and_closing_directory(packet):
    root, _, task, _, spans, answer = packet
    receipt = validate_receipt(root, task, answer, spans, '2026-10-05', '2026-10-11')
    status = {'status': 'incomplete', 'pending': ['blocked'], 'required_endpoints': 23, 'fetched_endpoints': 21}
    render_report(root, [receipt], status, [], ['Duval', 'St. Johns'])
    path = root/'report/report.html'
    assert check_report(path)['valid']
    original = path.read_bytes()
    render_report(root, [receipt], status, [], ['Duval', 'St. Johns'])
    assert path.read_bytes() == original
    path.write_text(path.read_text().replace('../raw/', 'raw/'))
    assert not check_report(path)['valid']


def test_synthetic_original_cannot_be_relabelled_live(packet):
    root, _, _, _, spans, _ = packet
    ref = next(iter(spans.values()))
    with pytest.raises(ValueError, match='Synthetic original'):
        _citation(root, {**ref, 'synthetic': False, 'authority': 'official'})


def test_partial_provider_response_is_retained_and_never_accepted(packet):
    from flwu.controlled_worker import GenerationRejected
    root, refs, task, _, _, _ = packet
    partial = {'choices': [{'finish_reason': 'length', 'message': {'content': 'partial'}}], 'usage': {'output_tokens': 6500}}
    def fail(_): raise GenerationRejected('Incomplete generation: finish_reason=length', partial)
    receipt, status = run_task(root, task, [refs[p] for p in task['dependencies']], '2026-10-05', '2026-10-11', complete=fail, attempts=1)
    assert receipt is None and status == 'validation_failed'
    trace = json.loads((root/'calls/R-APEX-1.json').read_text())
    assert trace['provider_response'] == partial
    assert trace['error'].endswith('finish_reason=length')
    assert not (root/'accepted/R-APEX.json').exists()


def test_transport_exposes_no_tools_or_proxy_or_redirects(monkeypatch):
    from flwu.controlled_worker import local_completion, MODEL, BASE_URL
    seen = {}
    class Response:
        def raise_for_status(self): pass
        def json(self): return {'choices': [{'finish_reason':'stop','message':{'content':'{}'}}], 'usage': {}}
    class Client:
        def __init__(self, **kwargs): seen['client'] = kwargs
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def post(self, url, json): seen.update(url=url, payload=json); return Response()
    monkeypatch.setattr('flwu.controlled_worker.httpx.Client', Client)
    assert local_completion({'task': {'id': 'one'}}) == ('{}', {})
    assert seen['url'] == BASE_URL+'/chat/completions'
    assert seen['payload']['model'] == MODEL and 'tools' not in seen['payload']
    assert seen['client']['trust_env'] is False and seen['client']['follow_redirects'] is False


def test_summary_prose_cannot_replace_selected_source_passages(packet):
    root, refs, task, _, spans, answer = packet
    receipt = validate_receipt(root, task, answer, spans, '2026-10-05', '2026-10-11')
    assert receipt['answer']['summary'] == '\n'.join(spans[s]['quote'] for s in answer['summary_spans'])
    prose = copy.deepcopy(answer)
    prose['summary'] = 'Unsupported new interpretation'
    del prose['summary_spans']
    with pytest.raises(ValueError): validate_receipt(root, task, prose, spans, '2026-10-05', '2026-10-11')
    uncited = copy.deepcopy(answer)
    uncited['citations'] = [s for s in spans if s not in answer['summary_spans']][:1]
    with pytest.raises(ValueError, match='Every summary span'):
        validate_receipt(root, task, uncited, spans, '2026-10-05', '2026-10-11')


def test_explicit_operative_source_cannot_be_unknown(packet):
    root, refs, _, _, _, _ = packet
    tasks, _ = tasks_from_evidence(root, refs)
    task = next(t for t in tasks if t['id'] == 'C-OLD')
    _, spans = make_packet(root, task, [refs[p] for p in task['dependencies']], '2026-10-05', '2026-10-11')
    ids = list(spans)
    answer = {'id': 'C-OLD', 'decision': 'exclude', 'reason': 'outside_window', 'publication_date': '2026-10-04',
              'effective_date': None, 'legal_status': 'unknown', 'summary_spans': ids, 'author': None,
              'concurrence': None, 'citations': ids, 'changes': []}
    with pytest.raises(ValueError, match='explicitly states'):
        validate_receipt(root, task, answer, spans, '2026-10-05', '2026-10-11')
