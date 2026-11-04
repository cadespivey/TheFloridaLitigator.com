"""Reuse real site-noise classes without hiding personnel, links or script changes."""
import copy
import base64
import html
import json

import pytest

from flwu import content_fingerprint as f, source_gate as gate
from tests.test_content_fingerprint import env, setup, acquire, complete, page, meta, URL


WP_URL='https://circuit7.org/judges/example/'


def wordpress(token='a', widget='12345678', text='Judge Example: call 555-0100.',
              href='/procedures.pdf', ajax='/wp-admin/admin-ajax.php', posts='unchanged',
              extra_script='', challenge_logic='', menu_id=17):
    def script(variable,data,identifier=None):
        attr=' id="'+identifier+'"' if identifier else ''
        return '<script'+attr+'>\nvar '+variable+' = '+json.dumps(data)+';\n</script>'
    pixel='https://moderate14-v4.cleantalk.org/pixel/'+token*32+'.gif'
    result='<html><head><meta name="generator" content="Elementor 4.3.2">'
    result+='<link rel="https://api.w.org/" href="https://circuit7.org/wp-json/">'
    result+='</head><body><p>'+text+'</p><a href="'+href+'">Procedures</a>'
    result+=script('ctPublicFunctions',{'_ajax_nonce':token*10,'_rest_nonce':token*10,'ajaxurl':ajax})
    result+=script('ctPublic',{'_ajax_nonce':token*10,'ct_checkjs_key':123456789 if token=='a' else 987654321,
                             'emailEncoderPassKey':token*32,'pixel__url':pixel})
    result+=script('ecs_ajax_params',{'nonce':token*10,'posts':posts},'ecs_ajax_load-js-extra')
    # WordPress can localize the same variable twice in one script.
    result+=script('jetMenuPublicSettings',{'restNonce':token*10},'jet-menu-public-scripts-js-extra').replace(
        '</script>','var jetMenuPublicSettings = '+json.dumps({'restNonce':token*10})+';\n</script>')
    result+='<div class="jet-mega-menu" data-settings="'+html.escape(json.dumps({
        'menuId':menu_id,'menuUniqId':token*13}),quote=True)+'"></div>'
    result+='<img id="apbct_pixel" alt="Cleantalk Pixel" title="Cleantalk Pixel" src="'+pixel+'">'
    result+='<div class="gtranslate_wrapper" id="gt-wrapper-'+widget+'"></div>'
    settings={'default_language':'en','languages':['en','es'],'wrapper_selector':'#gt-wrapper-'+widget}
    result+='<script id="gt_widget_script_'+widget+'-js-before">\nwindow.gtranslateSettings = /* document.write */ window.gtranslateSettings || {};window.gtranslateSettings[\''+widget+'\'] = '+json.dumps(settings)+';\n//# sourceURL=gt_widget_script_'+widget+'-js-before\n</script>'
    result+='<script data-gt-widget-id="'+widget+'" src="/wp-content/plugins/gtranslate/js/dwf.js"></script>'
    epoch=base64.b64encode(('1700000000' if token=='a' else '1700000001').encode()).decode()
    result+='<script>(function(){function c(){window.__CF$cv$params={r:\''+token*16+'\',t:\''+epoch+'\'};var u=\'/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray='+token*16+'\';'+challenge_logic+'}})();</script>'
    return (result+extra_script+'</body></html>').encode()


def nav_page(name='Judge A', target='/Clerk-s-Office', **kwargs):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(page(name,**kwargs),'html.parser');script=soup.find('script',id='__NEXT_DATA__')
    data=json.loads(script.string)
    menu=data['props']['pageProps']['extraData']['menu']
    menu[0].update(location={'id':42,'url':target},url=target,
                   subitems=[{'name':'Calendar','location':{'id':43,'url':target+'/Calendar'}}])
    script.string=json.dumps(data);return str(soup).encode()


def test_request_metadata_reuses_source_review_and_preserves_originals(env):
    conn,registry,_=env;setup(registry,(WP_URL,))
    old=wordpress();new=wordpress('b','87654321')
    complete(conn,registry,acquire(conn,registry,'first',{WP_URL:old})['tasks'][0])
    result=acquire(conn,registry,'second',{WP_URL:new})
    assert not result['tasks'] and len(result['reused_reviews'])==1
    proof=result['reused_reviews'][0]['content_hash_reuse']
    assert proof['profile']==f.WORDPRESS_PROFILE
    assert proof['current_fingerprint']['metadata']!=proof['reviewed_fingerprint']['metadata']
    assert len(gate.reviews(conn,registry['stream']))==1
    assert gate.blob(conn,proof['current_fingerprint']['original_sha256'])==new
    assert gate.blob(conn,proof['reviewed_fingerprint']['original_sha256'])==old
    assert 'a'*32 not in json.dumps(proof) and 'b'*32 not in json.dumps(proof)


@pytest.mark.parametrize('change',[
    {'text':'Judge Different: call 555-0200.'}, {'href':'/new-procedures.pdf'},
    {'ajax':'/new-filing-endpoint'}, {'posts':'different search result payload'},
    {'extra_script':'<script>window.newRule="AI disclosure required";</script>'},
    {'extra_script':'<div data-deadline="30 days">Contact</div>'},
    {'challenge_logic':'window.unknownAction=true;'}, {'menu_id':99},
])
def test_cosmetic_changes_cannot_hide_real_or_unknown_changes(env,change):
    conn,registry,_=env;setup(registry,(WP_URL,))
    complete(conn,registry,acquire(conn,registry,'first',{WP_URL:wordpress()})['tasks'][0])
    result=acquire(conn,registry,'second',{WP_URL:wordpress('b','87654321',**change)})
    assert [t['url'] for t in result['tasks']]==[WP_URL]
    assert not result['reused_reviews']


@pytest.mark.parametrize('damage',[
    lambda raw:raw.replace(b'"_ajax_nonce": "aaaaaaaaaa"',b'"_ajax_nonce": "unknown format"',1),
    lambda raw:raw.replace(b'"_ajax_nonce": "aaaaaaaaaa"',b'"_ajax_nonce": "aaaaaaaaaa", "_ajax_nonce": "bbbbbbbbbb"',1),
    lambda raw:raw.replace(b'#gt-wrapper-12345678',b'#gt-wrapper-00000000'),
    lambda raw:raw.replace(b'Elementor 4.3.2',b'Unrecognized framework'),
])
def test_ambiguous_metadata_does_not_create_an_equivalence_proof(damage):
    raw=damage(wordpress())
    assert f.fingerprint(raw,meta(WP_URL,raw)) is None


def test_new_navigation_is_reviewed_once_then_reused_without_lowercasing_urls(env):
    conn,registry,_=env;other='https://5dca.flcourts.gov/Judges/B';setup(registry,(URL,other))
    first=acquire(conn,registry,'first',{URL:nav_page(),other:nav_page('Judge B')})
    for task in first['tasks']:complete(conn,registry,task)
    second=acquire(conn,registry,'second',{
        URL:nav_page(target='/clerk-s-office'),other:nav_page('Judge B',target='/clerk-s-office')})
    assert len(second['tasks'])==2 # Case alone is not proof of equivalent routing.
    complete(conn,registry,second['tasks'][0])
    result=gate.queue(conn,registry)
    assert not result['tasks']
    proof=next(x for x in result['reused_reviews'] if x['source_id']==gate.source_id(other))['content_hash_reuse']
    nav=next(x for x in proof['component_reviews'] if x['current_component']['kind']=='court_navigation_links')
    assert nav['reviewed']['source_id']==gate.source_id(URL)
    assert len(gate.reviews(conn,registry['stream']))==3
    # A changed person/contact remains a task even with the reviewed menu.
    changed=acquire(conn,registry,'third',{
        URL:nav_page(target='/clerk-s-office'),
        other:nav_page('New Clerk',target='/clerk-s-office',phone='555-0200')})
    assert [t['url'] for t in changed['tasks']]==[other]


def test_wordpress_reuse_is_wired_into_standard_update_and_coordinator(tmp_path):
    from flwu import history as h, update, workflow as w
    from tests.test_opinion_discovery import Server
    database=tmp_path/'database.sqlite';run=tmp_path/'run';registry_path=tmp_path/'registry.json'
    registry=dict(schema_version=1,stream='weekly',review_protocol=gate.PROTOCOL,
                  sources=[dict(id=gate.source_id(WP_URL),url=WP_URL)])
    w.write(registry_path,registry);server=Server([]);current=wordpress()
    def fetch(url):
        if url==WP_URL:
            server.calls.append(url)
            return {k:v for k,v in meta(url,current).items() if k not in ('sha256','text_sha256','extraction')},current
        return server(url)
    with h.database(database) as conn:
        h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},run_id='initial',
                 payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[]),artifacts={})
        first=update.run(conn,registry,'first',tmp_path/'first',start='2026-10-15',end='2026-10-22',fetch=fetch)
        expanded=gate.load_registry(tmp_path/'first/expanded-registry.json')
        for task in first['source_reviews']['tasks']:complete(conn,expanded,task)
    w.initialize(run,database,registry_path,'second',start='2026-10-15',end='2026-10-22')
    current=wordpress('b','87654321');server.calls.clear()
    with h.database(database) as conn:
        result=update.run(conn,registry,'second',run,start='2026-10-15',end='2026-10-22',fetch=fetch)
    assert sum('_search/opinions/' in url for url in server.calls)==14
    assert not result['source_reviews']['tasks'] and not result['opinion_reviews']['tasks']
    reused=next(v for v in result['source_reviews']['reused_reviews'] if v['source_id']==gate.source_id(WP_URL))
    assert reused['content_hash_reuse']['profile']==f.WORDPRESS_PROFILE
    calls=list(server.calls)
    assert w.inspect(run,emit=True)['phase']=='prepare_report'
    assert server.calls==calls
