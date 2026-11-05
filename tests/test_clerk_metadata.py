import base64

import pytest

from flwu import content_fingerprint as f, source_gate as gate
from tests.test_content_fingerprint import env,setup,acquire,complete,meta

URL='https://www.nassauclerk.com/244/Circuit-Civil'
OTHER='https://www.nassauclerk.com/252/County-Civil'


def page(mask=10,ray='a',address='civil@example.gov',logic='window.challengeMode=1;',text='Call the clerk.'):
    token=bytes([mask]+[b^mask for b in address.encode()]).hex()
    time=base64.b64encode(b'1793805911').decode()
    return ('<html><body><p>'+text+'</p><a href="/cdn-cgi/l/email-protection#'+token+'">Email</a>'
            '<span class="__cf_email__" data-cfemail="'+token+'">[email protected]</span>'
            '<a href="https://connect.civicplus.com/referral">CivicPlus</a>'
            '<script>(function(){function c(){window.__CF$cv$params={r:\''+ray*16+'\',t:\''+time+'\'};'
            'var u="/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray='+ray*16+'";'+logic+'}})();</script></body></html>').encode()


def test_challenge_tokens_and_obfuscation_masks_reuse_but_email_addresses_do_not(env):
    conn,registry,_=env;setup(registry,(URL,));old=page()
    complete(conn,registry,acquire(conn,registry,'before',{URL:old})['tasks'][0])
    result=acquire(conn,registry,'after',{URL:page(20,'b')})
    assert not result['tasks'] and result['reused_reviews'][0]['content_hash_reuse']['profile']==f.NASSAU_PROFILE
    result=acquire(conn,registry,'changed-address',{URL:page(30,'c',address='new@example.gov')})
    assert [t['url'] for t in result['tasks']]==[URL]


def test_changed_challenge_logic_requires_one_same_host_review(env):
    conn,registry,_=env;setup(registry,(URL,OTHER))
    for task in acquire(conn,registry,'first',{URL:page(),OTHER:page(text='Other clerk page.')})['tasks']:complete(conn,registry,task)
    result=acquire(conn,registry,'second',{URL:page(20,'b',logic='window.challengeMode=2;'),
        OTHER:page(30,'c',logic='window.challengeMode=2;',text='Other clerk page.')})
    assert len(result['tasks'])==2
    complete(conn,registry,result['tasks'][0]);assert not gate.queue(conn,registry)['tasks']


@pytest.mark.parametrize('damage',[
    lambda b:b.replace(b'data-cfemail="',b'data-cfemail="unknown'),
    lambda b:b.replace(b'https://connect.civicplus.com/referral',b'https://unrecognized.gov/'),
])
def test_unknown_encodings_or_templates_do_not_qualify(damage):
    raw=damage(page())
    assert f.fingerprint(raw,meta(URL,raw)) is None


def test_unrecognized_request_time_and_changed_hidden_rule_stay_significant(env):
    body=page().replace(base64.b64encode(b'1793805911'),base64.b64encode(b'not-a-time'))
    assert f.fingerprint(body,meta(URL,body)) is None
    conn,registry,_=env;setup(registry,(URL,));complete(conn,registry,acquire(conn,registry,'before',{URL:page()})['tasks'][0])
    changed=page(20,'b').replace(b'<p>',b'<p data-deadline="30">')
    assert acquire(conn,registry,'changed',{URL:changed})['tasks']
    assert f.fingerprint(page(),meta('https://other-clerk.gov/',page())) is None
