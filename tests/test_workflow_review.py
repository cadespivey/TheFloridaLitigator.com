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
    assert w.read(guide['receipt_template'])==task['receipt_template']
    assert guide['receipt_template_sha256']==h.sha(Path(guide['receipt_template']).read_bytes())
    assert w.read(guide['inputs']['changed_text_lines_path'])==inputs['changed_text_lines']
    assert Path(result['review_guide']).stat().st_size < Path(result['packet']).stat().st_size / 10
    assert w.materialize(config,task)==result
    assert task['inputs']==inputs  # No mutation of the bound packet or queue.


def test_entry_guide_links_large_quotes_without_changing_packets_or_legacy_guides(tmp_path):
    config={'run_dir':str(tmp_path/'run')}
    quote='Calendar entry with exact nonbreaking space\u00a0and nested data. '*6000
    changed={'current':[quote], 'previous':['Previous '+quote]}
    template={'outcome':'','support':{'reason':'','current':[{'quote':quote}],
                                   'previous':[{'quote':'Previous '+quote}]}}
    task=w.packet(config,'source_review','calendar',{'changed_text_lines':changed},
                  template,'Read complete changed evidence.')
    result=w.materialize(config,task)
    entry=w.read(result['review_guide'])
    assert 'changed_text_lines' not in entry['inputs']
    assert w.read(entry['inputs']['changed_text_lines_path'])==changed
    assert entry['inputs']['changed_text_lines_sha256']==h.sha(Path(entry['inputs']['changed_text_lines_path']).read_bytes())
    assert entry['inputs']['changed_text_line_counts']=={'current':1,'previous':1}
    assert w.read(entry['receipt_template'])==template
    assert w.read(result['packet'])==task
    legacy=Path(result['full_review_guide']).read_bytes()
    assert w.read(result['full_review_guide'])['receipt_template']==template
    assert Path(result['review_guide']).stat().st_size < len(legacy)/20
    assert entry['submit_command']==task['submit_command']
    assert w.materialize(config,task)==result
    assert Path(result['full_review_guide']).read_bytes()==legacy
    # Linked bytes are still immutable evidence, not a lossy summary or bypass.
    Path(entry['inputs']['changed_text_lines_path']).write_text('{}')
    with pytest.raises(ValueError,match='Immutable workflow artifact differs: .*changed-text-lines.json'):
        w.materialize(config,task)
