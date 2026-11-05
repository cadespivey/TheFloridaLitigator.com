import pytest

from flwu import content_fingerprint as f
from tests.test_content_fingerprint import env,setup,acquire,complete,meta

URL='https://www.ca.cjis20.org/About-The-Court/jud_profile.aspx?judge=example'
BEFORE=b'<html>\r\n<p>Judge Example: 555-0100.</p>\r\n<a href="/procedures">Procedures</a>\r\n<script>window.deadline=10;</script></html>'


def test_only_crlf_lf_change_reuses_this_sources_review(env):
    conn,registry,_=env;setup(registry,(URL,))
    complete(conn,registry,acquire(conn,registry,'before',{URL:BEFORE})['tasks'][0])
    result=acquire(conn,registry,'after',{URL:BEFORE.replace(b'\r\n',b'\n')})
    assert not result['tasks'] and result['reused_reviews'][0]['content_hash_reuse']['profile']==f.LINE_ENDING_PROFILE


@pytest.mark.parametrize('after',[
    BEFORE.replace(b'555-0100',b'555-0200'),BEFORE.replace(b'/procedures',b'/new-procedures'),
    BEFORE.replace(b'deadline=10',b'deadline=20'),BEFORE.replace(b'\r\n',b'\n '),BEFORE.replace(b'\r\n',b'\r'),
])
def test_contact_link_script_and_other_whitespace_changes_remain_tasks(env,after):
    conn,registry,_=env;setup(registry,(URL,))
    complete(conn,registry,acquire(conn,registry,'before',{URL:BEFORE})['tasks'][0])
    assert acquire(conn,registry,'after',{URL:after})['tasks']


def test_unknown_site_or_non_html_body_never_qualifies():
    assert f.fingerprint(b'{"data":"unknown"}',meta(URL,b'{}')) is None
    assert f.profile_for('https://other-circuit.gov/judge') is None
