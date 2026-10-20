"""Independent acceptance checks for the controlled replay; no answer repairs."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from flwu.controlled_worker import check_report, make_packet, validate_receipt
from flwu.research import write_json
from controlled_replay import verify_contract, tasks_from_evidence


def evaluate(root):
    load = lambda p: json.loads((root/p).read_text())
    c = verify_contract(root); state = load('state.json'); refs = load('evidence.json')
    tasks, clerks = tasks_from_evidence(root, refs)
    receipts = {p.stem: json.loads(p.read_text()) for p in (root/'accepted').glob('*.json')}
    answers = {k: v['answer'] for k,v in receipts.items()}
    calls = [json.loads(p.read_text()) for p in sorted((root/'calls').glob('*.json'))]
    blocked = load('blocked-report.json'); before = load('before-restoration.json')['accepted_hashes']
    checks = []
    def check(name, ok): checks.append({'name': name, 'passed': bool(ok)})
    raw_ok = all(hashlib.sha256((root/r['path']).read_bytes()).hexdigest() == r['sha256'] for r in refs.values())
    check('All 23 required endpoints acquired with immutable originals', len(refs) == state['required_endpoints'] == 23 and raw_ok)
    check('All six candidates and three current judges validated', set(receipts) == {t['id'] for t in tasks} and len(receipts) == 9)
    check('Blocked checkpoint incomplete and procedure unavailable', blocked['status'] == 'incomplete' and any(p.get('task_id') == 'casey-morgan' for p in blocked['pending']))
    check('Pending work restored and production still false', state['status'] == 'ready_for_review' and not state['pending'] and state['production_ready'] is False)
    check('Eight accepted answers unchanged across coordinator restart', len(before) == 8 and all(hashlib.sha256((root/'accepted'/name).read_bytes()).hexdigest() == sha for name,sha in before.items()) and len(state['reused_this_run']) == 8)
    check('Only restored judge required inference on resume', state['accepted_this_run'] == ['casey-morgan'])
    network = load('network.json')
    check('429 and 503 recovery logged', [e['status'] for e in network if e['endpoint'] == 'opinions/C-START'] == [429,200] and all([e['status'] for e in network if e['endpoint'] == p] == [503,200] for p in ['circuits/orders','procedures/casey-morgan']))
    check('Boundary opinions included; pre-window excluded', all(answers.get(i,{}).get('decision') == 'include' for i in ['C-START','C-END']) and answers.get('C-OLD',{}).get('decision') == 'exclude')
    check('Withdrawal included as notice with withdrawn status', answers.get('C-WITHDRAWN',{}).get('decision') == 'include' and answers.get('C-WITHDRAWN',{}).get('legal_status') == 'withdrawn')
    check('Changed effective dates correctly classified', all(answers.get(i,{}).get('effective_date') == '2027-02-01' and answers.get(i,{}).get('legal_status') == 'future_effective' for i in ['R-APEX','R-PUBLICATION']))
    apex = answers.get('R-APEX', {}); publication = answers.get('R-PUBLICATION', {})
    check('Apex historical context and qualified concurrence retained', '2021' in apex.get('summary','') and 'not newly' in apex.get('summary','').lower() and 'result only' in str(apex.get('concurrence','')).lower())
    check('Only actual amendments appear in changes', all(ch['before'] != ch['after'] for a in answers.values() for ch in a.get('changes',[])) and len(publication.get('changes',[])) == 1)
    check('Print optional and website mandatory preserved', 'optional' in publication.get('summary','').lower() and 'mandatory' in publication.get('summary','').lower() and 'website' in publication.get('summary','').lower())
    check('Altered current assistants retained against archive injection', answers.get('alex-rowan',{}).get('assistant_name') == 'Morgan Ellis' and answers.get('dana-reed',{}).get('assistant_name') == 'Taylor Finch')
    alex = answers.get('alex-rowan',{}).get('procedure',{}); casey = answers.get('casey-morgan',{}).get('procedure',{}); dana = answers.get('dana-reed',{}).get('procedure',{})
    check('Altered personal deadlines retained', '6' in alex.get('summary','') and '12' in alex.get('summary','') and alex.get('legal_status') == 'future_effective' and any(x in casey.get('summary','').lower() for x in ['three business days','3 business days']))
    check('Negative finding has bounded status and search log', dana.get('status') == 'no_published_procedure_located' and dana.get('search_log') and 'only apply' not in dana.get('summary',''))
    validated = []
    for task in tasks:
        if task['id'] not in receipts: continue
        _, spans = make_packet(root, task, [refs[p] for p in task['dependencies']], c['window_start'], c['window_end'])
        try: validate_receipt(root, task, receipts[task['id']]['worker_answer'], spans, c['window_start'], c['window_end'])
        except (ValueError, KeyError, TypeError) as exc: validated.append(str(exc))
    check('Shared schema/evidence validation passes every answer', not validated and len(receipts) == 9)
    link = check_report(root/'report/report.html')
    check('Every report link works and directory closes report', link['valid'] and link['links'] > 0)
    report = load('report/report.json')
    check('Seven clerks and explicit candidate counters', len(clerks) == 7 and report['counters']['appellate_candidates_reviewed'] == 6 and report['counters']['appellate_candidates_included'] == 5 and report['counters']['appellate_candidates_excluded'] == 1)
    check('All worker calls bounded to one task and no model-proposed execution fields accepted', all('task' in x['request'] and x['request']['task']['kind'] in ['candidate','judge'] for x in calls) and all(set(r['answer']).isdisjoint({'execute','tools','command','tool_calls'}) for r in receipts.values()))
    starts = [datetime.fromisoformat(x['started_at']) for x in calls]
    ends = [datetime.fromisoformat(x['finished_at']) for x in calls if x.get('finished_at')]
    result = {'score': round(100*sum(x['passed'] for x in checks)/len(checks),1),
              'automated_acceptance': all(x['passed'] for x in checks), 'checks': checks,
              'manual_semantic_review_required': True, 'production_ready': False,
              'calls': len(calls), 'rejected_calls': [{'task':x['task_id'],'attempt':x['attempt'],'error':x.get('error')} for x in calls if x['status'] != 'accepted'],
              'model_active_seconds': round(sum((datetime.fromisoformat(x['finished_at'])-datetime.fromisoformat(x['started_at'])).total_seconds() for x in calls if x.get('finished_at')),2),
              'elapsed_first_to_last_call_seconds': round((max(ends)-min(starts)).total_seconds(),2) if starts and ends else None,
              'max_packet_input_tokens': max((x.get('usage',{}).get('prompt_tokens',0) for x in calls),default=0),
              'links':link, 'limits':['Synthetic corpus only','Orchestration differs from original shell-agent trial','No native compaction or PDF visual acceptance','Keyword checks require manual semantic adjudication']}
    write_json(root/'evaluation.json', result)
    print(json.dumps(result,indent=2))
    return result

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);evaluate(p.parse_args().root)
