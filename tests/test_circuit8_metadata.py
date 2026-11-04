"""Circuit 8 generated IDs cannot mask real procedure/link/script changes."""
import copy
import json

import pytest

from flwu import content_fingerprint as f, history as h, source_gate as gate
from tests.test_content_fingerprint import env, setup, acquire, complete, meta

URL='https://circuit8.org/courts-judges/example/'
OTHER='https://circuit8.org/courts-judges/second/'


def page(token='a',version='7.1.3',row='a',expand='1234',text='Judge Example: phone 555-0100.',
         href='/procedures.pdf',logic='window.rule=10;',nonce=None):
    nonce=nonce if nonce is not None else token*10
    data=dict(ajaxurl='https://circuit8.org/wp-admin/admin-ajax.php',postID='123',loveNonce=nonce)
    emoji=dict(baseUrl='https://s.w.org/images/emoji/',source=dict(concatemoji=
        'https://circuit8.org/wp-includes/js/wp-emoji-release.min.js?ver='+version))
    return ('<html><head><meta name="generator" content="WordPress '+version+'">'
        '<meta name="generator" content="Powered by WPBakery Page Builder - editor">'
        '<link rel="https://api.w.org/" href="https://circuit8.org/wp-json/">'
        '<link rel="stylesheet" id="parent-style-css" href="https://circuit8.org/wp-content/themes/salient/style.css?ver='+version+'">'
        '</head><body><div class="wpb_row vc_row" id="fws_'+row*13+'"><p>'+text+'</p>'
        '<div id="uvc-exp-wrap-'+expand+'-1" role="button" class="ult_exp_section"'
        ' aria-controls="uvc-exp-wrap-'+expand+'-1-content" data-ultimate-target="#uvc-exp-wrap-'+expand+'-1"'
        ' data-title="Scheduling" aria-expanded="false">Schedule</div>'
        '<div id="uvc-exp-wrap-'+expand+'-1-content" class="ult_exp_content"><a href="'+href+'">Procedures</a></div></div>'
        '<script id="nectar-frontend-js-extra">\nvar nectarLove = '+json.dumps(data)+';\nvar nectarOptions = {"delay_js":"false"};'+logic+'</script>'
        '<script id="wp-emoji-settings" type="application/json">'+json.dumps(emoji)+'</script></body></html>').encode()


def test_generated_id_bindings_and_nonce_changes_reuse_without_another_model_review(env):
    conn,registry,_=env;setup(registry,(URL,))
    old=page();new=page('b',row='b',expand='5678')
    complete(conn,registry,acquire(conn,registry,'before',{URL:old})['tasks'][0])
    result=acquire(conn,registry,'after',{URL:new})
    assert not result['tasks'] and len(result['reused_reviews'])==1
    proof=result['reused_reviews'][0]['content_hash_reuse']
    assert proof['profile']==f.CIRCUIT8_PROFILE
    assert proof['current_fingerprint']['metadata']!=proof['reviewed_fingerprint']['metadata']
    assert gate.blob(conn,proof['current_fingerprint']['original_sha256'])==new
    assert gate.blob(conn,proof['reviewed_fingerprint']['original_sha256'])==old
    assert len(gate.reviews(conn,registry['stream']))==1


def test_new_release_urls_need_one_review_before_shared_reuse(env):
    conn,registry,_=env;setup(registry,(URL,OTHER))
    first=acquire(conn,registry,'before',{URL:page(),OTHER:page(text='Second judge')})
    for task in first['tasks']:complete(conn,registry,task)
    second=acquire(conn,registry,'after',{
        URL:page('b',version='7.1.4',row='b',expand='5678'),
        OTHER:page('c',version='7.1.4',row='c',expand='6789',text='Second judge')})
    assert len(second['tasks'])==2
    complete(conn,registry,second['tasks'][0])
    result=gate.queue(conn,registry)
    assert not result['tasks']
    proof=next(r['content_hash_reuse'] for r in result['reused_reviews'] if r['source_id']==gate.source_id(OTHER))
    assert any(x['reviewed']['source_id']==gate.source_id(URL) for x in proof['component_reviews'])


@pytest.mark.parametrize('change',[
    {'text':'Judge New: phone 555-0200.'},{'href':'/new-procedure.pdf'},
    {'logic':'window.rule=20;'},
])
def test_contacts_rules_and_links_remain_significant(env,change):
    conn,registry,_=env;setup(registry,(URL,))
    complete(conn,registry,acquire(conn,registry,'before',{URL:page()})['tasks'][0])
    result=acquire(conn,registry,'after',{URL:page('b',row='b',expand='5678',**change)})
    assert [r['url'] for r in result['tasks']]==[URL]


@pytest.mark.parametrize('damage',[
    lambda b:b.replace(b'aria-controls="uvc-exp-wrap-1234-1-content"',b'aria-controls="wrong-panel"'),
    lambda b:b.replace(b'data-ultimate-target="#uvc-exp-wrap-1234-1"',b'data-ultimate-target="#wrong"'),
    lambda b:b.replace(b'class="ult_exp_content"',b'class="unexpected"'),
    lambda b:b.replace(b'<p>Judge',b'<a href="#fws_aaaaaaaaaaaaa">Section</a><p>Judge'),
    lambda b:b.replace(b'"loveNonce": "aaaaaaaaaa"',b'"loveNonce": "unknown"'),
    lambda b:b.replace(b'"loveNonce": "aaaaaaaaaa"',b'"loveNonce": "aaaaaaaaaa", "loveNonce": "bbbbbbbbbb"'),
    lambda b:b.replace(b'WordPress 7.1.3',b'Unknown CMS'),
    lambda b:b.replace(b'https://circuit8.org/wp-content/themes/salient/style.css',b'https://other.example/style.css'),
    lambda b:b.replace(b'<p>Judge',b'<div id="fws_aaaaaaaaaaaaa">Duplicate</div><p>Judge'),
])
def test_unbound_or_unrecognized_shapes_cannot_prove_equivalence(damage):
    body=damage(page());assert f.fingerprint(body,meta(URL,body)) is None


def test_unknown_attributes_widget_changes_and_dom_reorganization_stay_significant(env):
    conn,registry,_=env;setup(registry,(URL,))
    complete(conn,registry,acquire(conn,registry,'before',{URL:page()})['tasks'][0])
    changed=page('b',row='b',expand='5678').replace(b'aria-expanded="false"',b'aria-expanded="true"')
    result=acquire(conn,registry,'after',{URL:changed})
    assert result['tasks'] and not result['reused_reviews']
    assert f.fingerprint(page(),meta('https://unrelated.gov/judge',page())) is None


def test_blanket_legacy_review_is_not_an_exact_or_shared_reuse_proof(env,monkeypatch):
    conn,registry,_=env;setup(registry,(URL,))
    task=acquire(conn,registry,'first',{URL:page()})['tasks'][0]
    saved=complete(conn,registry,task)
    good=gate.reviews(conn,registry['stream'])[-1]
    bad=copy.deepcopy(good);bad['raw_change_review']=dict(method='Uninspected generic script',changes=[
        dict(id='one',reason='Technical rotation'),dict(id='two',reason='Technical rotation')])
    bad['receipt_sha256']=h.sha(bad)
    # Synthetic legacy event simulates a review accepted by the old permissive gate.
    h.record(conn,stream=registry['stream'],mode='manual_research',scope=gate.target(conn,registry['stream']),
        run_id='legacy-unsafe',payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[],source_gate_review=bad),artifacts={})
    idx=f.ReviewIndex(gate.observations(conn,registry['stream']),[bad],{},registry['review_protocol'],lambda digest:gate.blob(conn,digest))
    assert idx.reuse(task['observation']) is None
    # A separate valid historical review remains reusable, rather than blanket invalidation.
    result=gate.queue(conn,registry)
    assert not result['tasks'] and result['reused_reviews']
    original=gate.reviews
    monkeypatch.setattr(gate,'reviews',lambda *args:[bad])
    result=gate.queue(conn,registry)
    assert [r['url'] for r in result['tasks']]==[URL] and not result['reused_reviews']
    with pytest.raises(ValueError,match='does not apply'):
        gate.accept(conn,registry,{k:v for k,v in bad.items() if k not in ('acceptance_version','receipt_sha256')})
