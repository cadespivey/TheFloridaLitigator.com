"""Evaluate the two-run synthetic history trial without editing worker answers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from flwu.history import database, compare
from flwu.research import write_json
from flwu.controlled_worker import check_report


def load(path):
    return json.loads(path.read_text())


def differences(before, after, path=''):
    if isinstance(before, dict) and isinstance(after, dict):
        return [d for k in sorted(before.keys() | after.keys())
                for d in differences(before.get(k), after.get(k), path + '/' + k)]
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [d for i, (a, b) in enumerate(zip(before, after))
                for d in differences(a, b, path + '/' + str(i))]
    return [] if before == after else [{'path': path, 'before': before, 'after': after}]


def evaluate(root):
    baseline, followup = root/'baseline', root/'followup-run'
    baseline_marker = load(baseline/'history-capture.json')
    stream = baseline_marker['stream']
    checks = []

    def check(name, passed, evidence=None):
        checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})

    with database(root/'history.sqlite') as conn:
        context = compare(conn, stream)
        explicit = compare(conn, stream, start=baseline_marker['recorded_at'])
        calendar = compare(conn, stream, start='2026-10-11', end='2026-10-11')
        counts = {table: conn.execute('SELECT count(*) FROM '+table).fetchone()[0]
                  for table in ('captures', 'artifacts', 'finding_versions', 'finding_observations', 'finalized_reports')}
        finalizations = [dict(r) for r in conn.execute('SELECT * FROM finalized_reports')]
        artifacts_valid = all(hashlib.sha256(r['bytes']).hexdigest() == r['sha256']
                              for r in conn.execute('SELECT * FROM artifacts'))
    prior = load(followup/'prior-history.json')
    blocked = load(root/'blocked-check.json')
    state = load(followup/'state.json')
    before = prior['current_findings']; after = context['current_findings']
    deltas = {key: differences(before[key]['facts'], after[key]['facts']) for key in before if key in after}
    deltas = {key: value for key, value in deltas.items() if value}
    expected = set(load(root/'plan.json')['expected_changed_entities'])
    calls = [load(p) for p in sorted((followup/'calls').glob('*.json'))]
    packets = [load(p) for p in sorted((followup/'packets').glob('*.json'))]
    answers = {p.stem: load(p)['answer'] for p in (followup/'accepted').glob('*.json')}
    snapshots = load(followup/'before-restoration.json')['accepted_hashes']
    preserved = all(hashlib.sha256((followup/'accepted'/name).read_bytes()).hexdigest() == sha
                    for name, sha in snapshots.items())
    alex = answers.get('alex-rowan', {})
    apex = answers.get('R-APEX', {})
    casey = answers.get('casey-morgan', {})
    check('Baseline finalized only after recorded synthetic source and visual review',
          load(baseline/'manual-review.json')['accepted_for_trial_baseline'] and len(finalizations) == 1)
    check('Second-run frozen context identifies finalized baseline', prior['baseline_known'] and prior['start_utc'] == baseline_marker['recorded_at'])
    check('Every task receives only its matching previous entity facts', len(packets) == 9 and all(
          p.get('historical_context', {}).get('facts') == before[p['task']['kind']+':'+p['task']['id']]['facts'] for p in packets))
    check('Actual model requests include historical context', bool(calls) and all('historical_context' in c['request'] for c in calls))
    check('Current JA and contact override old history', alex.get('assistant_name') == 'Quinn Harper' and 'quinn.harper' in alex.get('assistant_contact', ''))
    check('Current personal deadline overrides old history while retaining future date',
          '15 days' in alex.get('procedure', {}).get('summary', '') and alex.get('procedure', {}).get('legal_status') == 'future_effective')
    check('Current amendment effective date overrides old history', apex.get('effective_date') == '2027-03-01' and apex.get('legal_status') == 'future_effective')
    check('Blocked checkpoint retains both required source gaps', set(blocked['gap_ids']) == {'circuits/orders', 'procedures/casey-morgan'})
    check('Blocked checkpoint retains previous Casey finding without claiming freshness', blocked['casey_preserved'] and blocked['status'] == 'incomplete')
    check('Incomplete finalization rejected and baseline unchanged', blocked['finalize_rejected'] and finalizations[0]['capture_seq'] == baseline_marker['seq'])
    check('Restored task adopts new procedure', 'four business days' in casey.get('procedure', {}).get('summary', ''))
    check('Resume preserves eight accepted answers and infers only pending task', len(snapshots) == 8 and preserved and state['accepted_this_run'] == ['casey-morgan'] and len(state['reused_this_run']) == 8)
    check('Final coverage complete with no pending work', state['status'] == 'ready_for_review' and not state['pending'] and not context['coverage_gaps'] and not context['not_rechecked_since_baseline'])
    check('Only deliberately changed entities have new finding values', set(deltas) == expected, {'expected': sorted(expected), 'actual': sorted(deltas)})
    check('Every observed source change matches a deliberate source edit',
          {e['source'] for e in context['events'] if e['type'] == 'source_changed'} == set(load(root/'preparation-correction.json')['source_edits']))
    # Explicit starts are inclusive; the finalized capture itself can be included
    # but contributes no transition because its preceding same-run facts match.
    check('Explicit timestamp and finalized-baseline transitions agree', context['events'] == explicit['events'])
    check('Calendar date comparison includes both runs and marks missing earlier history', not calendar['baseline_known'] and any(e['type'] == 'first_observed' for e in calendar['events']))
    check('Repeated observations outnumber deduplicated versions', counts['finding_observations'] > counts['finding_versions'])
    check('All persisted artifact bytes match content hashes', artifacts_valid)
    links = check_report(followup/'report/report.html')
    check('Final report evidence links and closing directory valid', links['valid'])
    check('Synthetic scope never becomes production-ready', state['synthetic'] and state['production_ready'] is False)
    result = {'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks),
              'automated_acceptance': all(c['passed'] for c in checks), 'counts': counts,
              'finding_differences': deltas, 'unexpected_changed_entities': sorted(set(deltas)-expected),
              'followup_model_calls': len(calls), 'rejected_calls': [{'task': c['task_id'], 'error': c.get('error')} for c in calls if c['status'] != 'accepted'],
              'links': links, 'manual_review_required': True, 'production_ready': False}
    write_json(root/'comparison-finalized.json', context)
    write_json(root/'comparison-explicit.json', explicit)
    write_json(root/'comparison-calendar.json', calendar)
    write_json(root/'evaluation.json', result)
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('root', type=Path)
    evaluate(parser.parse_args().root)
