"""Review ergonomics preserve exact evidence and leave interpretation explicit."""
import copy
from pathlib import Path
import pytest
from flwu import history as h, source_gate as g, workflow as w
from tests.test_source_gate import env, acquire


def test_changed_quotes_are_exact_and_do_not_complete_review(env):
    conn,registry,root=env
    acquire(env,'before',page='Old heading: \nACIS\u00a0access'.encode())
    acquire(env,'after',page='New heading: \nACIS\u00a0access\nACIS\u00a0access'.encode())
    queue=g.write_queue(conn,registry,root/'sources')
    task=next(w.tasks(conn,{'run_dir':str(root/'run')},
                      {'source_reviews':queue,'opinion_reviews':{'tasks':[]}}))
    receipt=copy.deepcopy(task['receipt_template'])
    assert receipt['outcome']==''
    for side,prefix in [('current',''),('previous','previous_')]:
        entries=receipt['support'][side]
        assert [entry['quote'] for entry in entries]==task['inputs']['changed_text_lines'][side]
        text=g.blob(conn,task['inputs']['observation'][prefix+'text_sha256']).decode()
        assert all(entry['quote'] in text for entry in entries)
    with pytest.raises(ValueError,match='Complete the exact review template'):
        g.accept(conn,registry,receipt)
    receipt.update(reviewer='Fixture reviewer',summary='Heading change and repeated ACIS text.',
                   review_scope='Both complete fixture extracts.',outcome='no_relevant_change')
    receipt['support']['reason']='The heading changes and already-present ACIS text is duplicated; the fixture adds no operating requirement.'
    g.accept(conn,registry,receipt)
    assert len(g.queue(conn,registry)['reused_reviews'])==1


def test_review_guide_links_lossless_prior_findings_without_embedding_them(tmp_path):
    config={'run_dir':str(tmp_path/'run')}
    finding=dict(key='person-example',kind='judge',expected_version='v1',
                 facts={'nested':{'detail':'large evidence '*20000}},citations=[{'url':'https://court.gov/profile'}])
    inputs={'prior_findings':[finding], 'review_template':{'outcome':'baseline_reviewed'},
            'changed_text_lines':{'current':['New heading'], 'previous':['Old heading']}}
    task=w.packet(config,'source_review','example',inputs,{'outcome':''},'Read all changed lines.')
    result=w.materialize(config,task)
    guide=w.read(result['review_guide'])
    assert 'prior_findings' not in guide['inputs']
    assert 'review_template' not in guide['inputs']
    indexed=guide['inputs']['prior_findings_index'][0]
    assert w.read(indexed['path'])==finding
    assert indexed['sha256']==h.sha(Path(indexed['path']).read_bytes())
    assert indexed['expected_version']=='v1'
    assert w.read(result['packet'])==task
    assert guide['receipt_template']==task['receipt_template']
    assert Path(result['review_guide']).stat().st_size < Path(result['packet']).stat().st_size / 10
    assert w.materialize(config,task)==result
    assert task['inputs']==inputs  # No mutation of the bound packet or queue.
