import copy
import json
import pytest
from flwu import history as h, raw_comparison as raw, source_gate as g
from tests.test_source_gate import env, receipt


def test_html_comparison_detects_nonvisible_attributes_and_embedded_json():
    before=b'<p>Clerk</p><a href="/old">Records</a><script type="application/json">{"status":"active"}</script>'
    after=b'<p>Clerk</p><a href="/new">Records</a><script type="application/json">{"status":"withdrawn"}</script>'
    result=raw.compare(before,after,'text/html')
    changes=result['changes']
    assert any(c['before']=='/old' and c['after']=='/new' for c in changes)
    assert any(c['before']=='active' and c['after']=='withdrawn' for c in changes)
    review=raw.template(result)
    with pytest.raises(ValueError):raw.validate(review,result)
    review['method']='Inspected the original attribute and embedded status change.'
    for item in review['changes']:item['reason']='Fixture change requires relevance analysis; text alone cannot establish no change.'
    raw.validate(review,result)
    incomplete=copy.deepcopy(review);incomplete['changes'].pop()
    with pytest.raises(ValueError,match='every original-content change'):raw.validate(incomplete,result)
    stale=copy.deepcopy(review);stale['comparison_sha256']='0'*64
    with pytest.raises(ValueError,match='exact comparison'):raw.validate(stale,result)


def test_binary_comparison_preserves_bounds_and_requires_original_inspection():
    result=raw.compare(b'abc\x00oldxyz',b'abc\x00newxyz','application/pdf')
    assert result['kind']=='original_bytes'
    change=result['changes'][0]
    assert change['before']==dict(start=4,end=7,sha256=h.sha(b'old'),bytes=3)
    assert change['after']==dict(start=4,end=7,sha256=h.sha(b'new'),bytes=3)
    assert 'Inspect original documents' in result['limitation']


def test_same_text_review_cannot_use_title_only_or_reuse_legacy_approval(env):
    conn,registry,root=env
    def fetch(body):
        return lambda url: (dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,
                                http_status=200,content_type='text/html'),body)
    before=b'<html><meta property="og:updated_time" content="before"><h1>Clerk</h1><p>Hours 9-5.</p></html>'
    after=before.replace(b'content="before"',b'content="after"')
    g.run(conn,registry,'before',fetch=fetch(before))
    result=g.run(conn,registry,'after',fetch=fetch(after));task=result['tasks'][0]
    assert raw.required(task['observation'])
    rec=receipt(task,registry,conn);rec['outcome']='no_relevant_change'
    o=task['observation']
    rec['support']['previous']=[dict(sha256=o['previous_sha256'],text_sha256=o['previous_text_sha256'],quote='Clerk',locator='heading')]
    with pytest.raises(ValueError,match='raw_change_review'):g.accept(conn,registry,rec)
    # Simulate an accepted pre-fix receipt in this disposable database only.
    saved=dict(rec,receipt_sha256=h.sha(rec),acceptance_version=3)
    h.record(conn,stream=registry['stream'],mode='manual_research',scope={'profile':'test'},run_id='legacy',
             payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[],source_gate_review=saved),artifacts={})
    assert not g.queue(conn,registry)['reused_reviews']
    with pytest.raises(ValueError,match='before reusing'):g.accept(conn,registry,rec)
    # A later identical retrieval must not erase the unreviewed raw transition.
    repeated=g.run(conn,registry,'unreviewed-repeat',fetch=fetch(after))
    task=repeated['tasks'][0]
    assert task['reason']=='unreviewed'
    assert task['raw_comparison_basis']['previous_sha256']==h.sha(before)
    rec=receipt(task,registry,conn);rec['outcome']='no_relevant_change'
    o=task['observation']
    rec['support']['previous']=[dict(sha256=o['previous_sha256'],text_sha256=o['previous_text_sha256'],quote='Clerk',locator='heading')]
    with pytest.raises(ValueError,match='raw_change_review'):g.accept(conn,registry,rec)
    written=g.write_queue(conn,registry,root/'review')['tasks'][0]
    from pathlib import Path
    assert Path(written['raw_comparison_previous_path']).read_bytes()==before
    comparison=json.loads(Path(written['raw_comparison_path']).read_text())
    assert any(c['before']=='before' and c['after']=='after' for c in comparison['changes'])
    rec['raw_change_review']=written['review_template']['raw_change_review']
    rec['raw_change_review']['method']='Inspected original HTML and every structured comparison entry.'
    for item in rec['raw_change_review']['changes']:
        item['reason']='Only the og:updated_time metadata value changed; the fixture operating hours and contact content remain unchanged.'
    accepted=g.accept(conn,registry,rec)
    assert accepted['capture_id']
    assert len(g.queue(conn,registry)['reused_reviews'])==1
    # An unchanged later retrieval can reuse only the corrected review.
    g.run(conn,registry,'later',fetch=fetch(after))
    assert len(g.queue(conn,registry)['reused_reviews'])==1
