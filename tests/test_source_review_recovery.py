"""Legacy blanket reviews stay recorded, but cannot silently bypass correction."""
import copy
from pathlib import Path

import pytest

from flwu import history as h, source_gate as gate, update, workflow as w
from tests.test_workflow import environment,answer


@pytest.mark.parametrize('interrupt_after_domain',[False,True])
def test_saved_blanket_review_returns_explicit_correction_and_recovers_after_interruption(tmp_path,interrupt_after_domain):
    before=b'<html><h1>Profile</h1><div data-rule="10">Contact</div><script>window.rule=10;</script></html>'
    after=before.replace(b'data-rule="10"',b'data-rule="20"').replace(b'rule=10',b'rule=20')
    run,db,registry,server=environment(tmp_path,profile=before)
    def html_before(url):
        meta,body=server(url)
        return dict(meta,content_type='text/html'),before
    with h.database(db) as conn:
        gate.run(conn,registry,'html-baseline',fetch=html_before)
        update.refresh(conn,registry,'trial',run)
    answer(run,db,w.inspect(run,emit=True))
    def fetch(url):
        meta,body=server(url)
        return dict(meta,content_type='text/html'),after if url=='https://court.gov/profile' else body
    with h.database(db) as conn:
        gate.run(conn,registry,'changed-source',fetch=fetch)
        update.refresh(conn,registry,'trial',run)
    state=w.inspect(run,emit=True);task=w.read(state['packet']);packet_before=Path(state['packet']).read_bytes()
    receipt=copy.deepcopy(task['receipt_template']);o=task['inputs']['observation']
    receipt.update(reviewer='Legacy fixture',outcome='no_relevant_change',summary='All technical rotation',review_scope='Uninspected legacy fixture')
    for side in ('current','previous'):
        receipt['support'][side][0].update(quote='Profile',locator='heading')
    receipt['support']['reason']='Identical visible text proves no change'
    receipt['raw_change_review']['method']='Generic helper'
    for change in receipt['raw_change_review']['changes']:change['reason']='Technical rotation; no visible text change'
    assert len(receipt['raw_change_review']['changes'])==2
    # Seed an old acceptance as immutable fixture history; current API rejects it.
    with h.database(db) as conn:
        config=w.load(run);saved=dict(receipt,receipt_sha256=h.sha(receipt),acceptance_version=3,raw_review_verified=True)
        legacy=h.record(conn,stream=registry['stream'],mode='manual_research',scope=gate.target(conn,registry['stream']),
            run_id='legacy-blanket',payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[],source_gate_review=saved),artifacts={h.sha(receipt):h.canonical(receipt).encode()})
        event=dict(kind='decision',packet_sha256=task['packet_sha256'],task=task,receipt=receipt,validation=legacy)
        w.record(conn,config,event)
    w.write(task['receipt_path'],receipt)
    old_receipt=Path(task['receipt_path']).read_bytes()
    correction=w.inspect(run,emit=True)
    assert correction['phase']=='source_review_correction' and correction['complete'] is False
    assert 'revise' in correction['command'] and correction['predecessor']==h.sha(event)
    assert correction['save_receipt']!=task['receipt_path']
    assert Path(correction['packet']).read_bytes()==packet_before
    assert Path(task['receipt_path']).read_bytes()==old_receipt
    assert w.inspect(run,emit=True)==correction # Restart/compaction recovers same checkpoint.
    from flwu.workflow_report import prepare
    with pytest.raises(ValueError,match='Finish source_review_correction'):
        prepare(run)
    with pytest.raises(ValueError,match='Repeated boilerplate'):w.submit(run,task['packet_path'],task['receipt_path'])
    fixed=copy.deepcopy(receipt)
    fixed['review_scope']='Inspected fixture attribute and embedded script'
    fixed['support']['reason']='The data attribute and embedded script change; this synthetic fixture has no real-world legal significance.'
    fixed['raw_change_review']['changes'][0]['reason']='The data-rule attribute changes from 10 to 20 in this synthetic fixture.'
    fixed['raw_change_review']['changes'][1]['reason']='Embedded rule changes from 10 to 20. This synthetic fixture has no real legal significance.'
    fixed_path=Path(correction['save_receipt']);w.write(fixed_path,fixed)
    with pytest.raises(ValueError,match='Stale predecessor'):
        w.revise(run,task['packet_path'],fixed_path,'wrong','Correct source review')
    if interrupt_after_domain:
        # Simulate exit after the domain commit but before its coordinator event.
        with h.database(db) as conn:
            gate.accept(conn,gate.load_registry(run/'expanded-registry.json'),fixed)
        with pytest.raises(ValueError,match='Source review and coordinator decision disagree'):
            w.inspect(run,emit=True)
    saved=w.revise(run,task['packet_path'],fixed_path,correction['predecessor'],correction['correction_reason'])
    assert saved['capture_id']
    assert w.inspect(run,emit=True)['phase']!='source_review_correction'
    assert Path(task['receipt_path']).read_bytes()==old_receipt
    assert Path(task['packet_path']).read_bytes()==packet_before
    with h.database(db) as conn:
        reviews=gate.reviews(conn,registry['stream'])
        assert any(r['receipt_sha256']==h.sha(receipt) for r in reviews)
        assert reviews[-1]['receipt_sha256']==h.sha(fixed)
    assert w.revise(run,task['packet_path'],fixed_path,correction['predecessor'],correction['correction_reason'])['replayed']
