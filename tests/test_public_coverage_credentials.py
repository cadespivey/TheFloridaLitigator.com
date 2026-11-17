import copy
import json
from pathlib import Path

import pytest
from flwu import publication as pub, workflow as w, history as h
from tests.test_workflow import environment, answer


@pytest.mark.parametrize('domain',['azurewebsites.us','azurewebsites.net'])
def test_only_azure_code_value_is_redacted(domain):
    key='fixture-'+'X'*48
    url='https://fixture.'+domain+'/api/rules?type=active&code='+key+'&page=2'
    reason='Unavailable: '+url+'; preserve uncertainty.'
    actual=pub.public_coverage_reason(reason)
    assert actual==reason.replace(key,'%5BREDACTED%5D')
    assert pub.public_coverage_reason(actual)==actual
    ordinary='https://court.example/rule?code=12D-16.002'
    assert pub.public_coverage_reason(ordinary)==ordinary
    final='Unavailable '+url.split('&page=')[0]+'. Retry later.'
    assert pub.public_coverage_reason(final)==final.replace(key,'%5BREDACTED%5D')


def test_real_export_redacts_failure_reason_but_retains_private_receipt(tmp_path):
    run,db,_,_=environment(tmp_path,fail=True)
    key='fixture-'+'Y'*48
    url='https://fixture.azurewebsites.us'+'/api/rules?code='+key
    reason='Unavailable request '+url+'; no no-change conclusion.'
    for _ in range(40):
        state=w.inspect(run,emit=True)
        if 'packet' not in state:break
        if state['kind']=='coverage_review':
            task=w.read(state['packet']);receipt=copy.deepcopy(task['receipt_template'])
            receipt.update(decision='unavailable',reason=reason)
            w.write(state['save_receipt'],receipt);w.submit(run,state['packet'],state['save_receipt'])
        else:answer(run,db,state)
    assert state['phase']=='prepare_report'
    from flwu.workflow_report import prepare
    prepared=prepare(run);raw=Path(prepared['public_preview']).read_text()
    assert key not in raw and '%5BREDACTED%5D' in raw
    issue=json.loads(raw)
    assert all(p['decision']=='unavailable' for p in issue['provenance']['workflow_coverage']['pending'])
    with h.database(db) as conn:
        receipts=[e['receipt'] for e in w.accepted(conn,w.load(run)).values()
                  if e['task']['kind']=='coverage_review']
    assert receipts and all(r['reason']==reason for r in receipts)
