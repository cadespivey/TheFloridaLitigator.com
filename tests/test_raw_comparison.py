import copy
import json
import pytest
from pathlib import Path
from flwu import history as h, raw_comparison as raw, source_gate as g
from tests.test_source_gate import env, receipt


def test_changed_text_gets_original_comparison_aid_without_changing_receipt_policy(env):
    conn, registry, root = env
    before = b'<h1>Clerk</h1><p>Calendar Monday</p><a href="/old">Records</a>'
    after = b'<h1>Clerk</h1><p>Calendar Tuesday</p><a href="/new">Records</a>'
    def fetch(body):
        return lambda url: (dict(url=url, resolved_url=url, retrieved_at=h.now(),
                                success=True, http_status=200, content_type='text/html'), body)
    g.run(conn, registry, 'aid-before', fetch=fetch(before))
    g.run(conn, registry, 'aid-after', fetch=fetch(after))
    task = g.write_queue(conn, registry, root/'review')['tasks'][0]
    assert task['changed_text_lines']['current']
    assert task['raw_comparison_role'] == 'inspection_aid'
    assert 'raw_comparison_basis' not in task
    assert 'raw_change_review' not in task['review_template']
    comparison = json.loads(Path(task['raw_comparison_path']).read_text())
    assert comparison == raw.compare(before, after, 'text/html')
    assert Path(task['raw_comparison_previous_path']).read_bytes() == before
    assert Path(task['raw_comparison_current_path']).read_bytes() == after
    assert any(c['before']=='/old' and c['after']=='/new' for c in comparison['changes'])
    assert any(c['before']=='Calendar Monday' and c['after']=='Calendar Tuesday'
               for c in comparison['changes'])
    assert json.loads(Path(task['raw_comparison_decoded_path']).read_text()) == raw.decoded_view(comparison)
    # Merely exporting an aid cannot mark evidence reviewed or add receipt fields.
    assert not g.queue(conn, registry)['reused_reviews']
    rec = receipt(task, registry, conn)
    extraneous = copy.deepcopy(rec)
    extraneous['raw_change_review'] = raw.template(comparison)
    with pytest.raises(ValueError, match='does not apply'):
        g.accept(conn, registry, extraneous)
    # Existing changed-source outcome gate remains intact too.
    with pytest.raises(ValueError):
        g.accept(conn, registry, rec)
    again = g.write_queue(conn, registry, root/'review')['tasks'][0]
    assert again == task


@pytest.mark.parametrize('state', ['new', 'unchanged', 'failed'])
def test_comparison_aid_does_not_misrepresent_new_identical_or_failed_sources(env, state):
    conn, registry, root = env
    def fetch(body, success=True):
        return lambda url: (dict(url=url, resolved_url=url, retrieved_at=h.now(),
                                success=success, http_status=200 if success else 403,
                                content_type='text/html'), body)
    g.run(conn, registry, 'initial', fetch=fetch(b'<p>Clerk</p>'))
    if state != 'new':
        g.run(conn, registry, 'later', fetch=fetch(
            b'<p>Forbidden</p>' if state=='failed' else b'<p>Clerk</p>', state!='failed'))
    task = g.write_queue(conn, registry, root/'review')['tasks'][0]
    assert 'raw_comparison_path' not in task
    assert 'raw_comparison_role' not in task


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
    decoded=json.loads(Path(written['raw_comparison_decoded_path']).read_text())
    assert decoded['comparison_sha256']==h.sha(comparison)
    assert [c['id'] for c in decoded['changes']]==[c['id'] for c in comparison['changes']]
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


def test_decoded_view_exposes_nested_attributes_and_json_without_relevance_decision():
    import html
    def block(day):
        inner='<div data-content="'+html.escape(json.dumps({'end_date':day,'url':'https://court.gov/opinions'}),quote=True)+'"></div>'
        return '<div data-content="'+html.escape(json.dumps({'content':inner}),quote=True)+'"></div>'
    before=block('10/23/2026');after=block('10/26/2026')
    item=dict(path=['embedded'],before=before,after=after)
    comparison=dict(changes=[dict(id=h.sha(item),**item)])
    original=copy.deepcopy(comparison)
    view=raw.decoded_view(comparison)
    assert comparison==original
    assert view['comparison_sha256']==h.sha(comparison)
    assert [c['id'] for c in view['changes']]==[comparison['changes'][0]['id']]
    old=view['changes'][0]['before']['decoded_html'][0]['attrs']['data-content']['content']['decoded_html'][0]['attrs']['data-content']
    new=view['changes'][0]['after']['decoded_html'][0]['attrs']['data-content']['content']['decoded_html'][0]['attrs']['data-content']
    assert old=={'end_date':'10/23/2026','url':'https://court.gov/opinions'}
    assert new=={'end_date':'10/26/2026','url':'https://court.gov/opinions'}
    assert not view['decoding_limit_paths']
    assert 'outcome' not in view and 'reason' not in view['changes'][0]


def test_decoded_view_retains_malformed_text_and_signals_depth_limit():
    item=dict(path=['embedded'],before='{invalid JSON',after='<literal with no closing bracket')
    comparison=dict(changes=[dict(id=h.sha(item),**item)])
    view=raw.decoded_view(comparison)
    assert view['changes']==comparison['changes']
    limited=raw.decoded_view(comparison,max_depth=0)
    assert limited['changes']==comparison['changes']
    assert limited['decoding_limit_paths']==[[comparison['changes'][0]['id'],'before'],[comparison['changes'][0]['id'],'after']]


def test_decoded_view_preserves_script_and_link_evidence():
    before=b'<a href="/old">Records</a><script>window.changed=false;</script>'
    after=b'<a href="/new">Records</a><script>window.changed=true;</script>'
    comparison=raw.compare(before,after,'text/html')
    view=raw.decoded_view(comparison)
    assert view['changes']==comparison['changes']
    assert any(c['after']=='window.changed=true;' for c in view['changes'])
