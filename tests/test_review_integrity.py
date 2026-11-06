import copy
from pathlib import Path
import pytest
from flwu import aligned_review as a, raw_comparison as raw, history as h, source_gate as g
from flwu import workflow as w, review_withdrawal as withdrawal
from tests.test_source_gate import env, acquire, receipt
from tests.test_workflow import environment,answer


def test_aligned_removal_preserves_every_new_script_link_and_nesting_change():
    options=''.join(f'<option value="{n}">Member {n}</option>' for n in range(220))
    before=('<html><body><select>'+options+'</select><a href="/old">Office</a><script>rule=1;</script></body></html>').encode()
    after=b'<html><body><a href="/new">Office</a><script>rule=2;</script></body></html>'
    comparison=raw.compare(before,after,'text/html');alignment=a.compare(before,after,'text/html')
    assert len(alignment['groups']) < 10
    values=str(alignment)
    assert 'rule=1;' in values and 'rule=2;' in values and '/old' in values and '/new' in values
    review=a.template(comparison,alignment)
    review['method']='Compared complete structural token groups and retained originals.'
    for group in review['groups']:group.update(observed_change='Fixture group inspected.',impact='Fixture change retained for review.',unresolved=False)
    a.validate(review,comparison,alignment)
    review['groups'].pop()
    with pytest.raises(ValueError,match='every aligned'):a.validate(review,comparison,alignment)


def test_added_script_cannot_pass_a_previous_alignment_receipt():
    before=b'<html><body><div>Office</div></body></html>'
    after=before.replace(b'<div>',b'<div class="new">')
    cmp=raw.compare(before,after,'text/html');aligned=a.compare(before,after,'text/html');review=a.template(cmp,aligned)
    for group in review['groups']:group.update(observed_change='Class changed.',impact='Fixture class only.',unresolved=False)
    amended=after+b'<script>window.newRule=true;</script>'
    with pytest.raises(ValueError,match='exact original'):a.validate(review,raw.compare(before,amended,'text/html'),a.compare(before,amended,'text/html'))


def test_serialization_and_duplicate_attributes_remain_obligations():
    before=b'<html><div id="one" id="two">Office</div></html>'
    after=b'<html><div id="different" id="two">Office</div></html>'
    assert a.compare(before,after,'text/html')['groups']
    assert a.compare(b'<HTML>Office</HTML>',b'<html>Office</html>','text/html')['groups']
    before=b'<html><div><span>Office</span></div></html>'
    after=b'<html><div></div><span>Office</span></html>'
    assert a.compare(before,after,'text/html')['groups']


def test_unresolved_group_never_qualifies_as_completed_review():
    before=b'<p>Contact</p>';after=b'<p class="changed">Contact</p>'
    cmp=raw.compare(before,after,'text/html');alignment=a.compare(before,after,'text/html')
    review=a.template(cmp,alignment)
    review['method']='Inspected the changed attribute group.'
    for group in review['groups']:group.update(observed_change='Opaque value changed.',impact='Meaning unresolved.')
    with pytest.raises(ValueError,match='unresolved'):a.validate(review,cmp,alignment)


def test_senate_ray_query_reuse_requires_exact_binding_and_preserves_logic():
    from tests.test_content_fingerprint import senate_page,meta,SENATE_URL
    from flwu import content_fingerprint as f
    before=senate_page(ray='a',logic="var u='/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray="+'a'*16+"';")
    after=senate_page('B','b',logic="var u='/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray="+'b'*16+"';")
    assert f.fingerprint(before,meta(SENATE_URL,before))['core_sha256']==f.fingerprint(after,meta(SENATE_URL,after))['core_sha256']
    bad=after.replace(b'?ray='+b'b'*16,b'?ray='+b'c'*16)
    assert f.fingerprint(bad,meta(SENATE_URL,bad)) is None
    changed=after.replace(b'var u=',b'window.extraBehavior=true;var u=')
    assert f.fingerprint(changed,meta(SENATE_URL,changed))['core_sha256']!=f.fingerprint(after,meta(SENATE_URL,after))['core_sha256']
    listing='https://www.flsenate.gov/Session/Bills/2026?PageNumber=12'
    assert f.profile_for(listing)==f.SENATE_LISTING_PROFILE
    assert f.profile_for('https://www.flsenate.gov/Session/Bill/2026/1') is None
    first=f.fingerprint(before,meta(listing,before));second=f.fingerprint(after,meta(listing,after))
    assert first['core_sha256']==second['core_sha256']
    assert f.fingerprint(changed,meta(listing,changed))['core_sha256']!=second['core_sha256']


def test_cookie_stub_is_unavailable_even_with_http_200(env):
    c,r,_=env
    url='https://www.flsenate.gov/Laws/Statutes/2026/Title23/'
    r['sources']=[dict(id=g.source_id(url),url=url)]
    body=b'<html><title>Florida Statutes</title><body>Loading Florida Statutes\xe2\x80\xa6 Please enable JavaScript to view Florida Statutes.<script>document.cookie=\'fls_st=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa; Path=/; Max-Age=3600; SameSite=Lax; Secure\';location.replace(location.href);</script></body></html>'
    def fetch(url):return dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,content_type='text/html'),body
    queue=g.run(c,r,'one',fetch=fetch);observation=queue['tasks'][0]['observation']
    assert observation['http_status']==200 and observation['transport_success'] is True
    assert observation['success'] is False and observation['failure_kind']=='access_challenge'
    assert g.blob(c,observation['sha256'])==body
    # A historical transport-success record must also receive an append-only
    # correction without a new URL, retrieval timestamp or invented download.
    original=g.observations(c,r['stream'])[-1]
    from flwu.source_access import correct_observation
    corrected=correct_observation(c,r,original['capture_id'],'Fixture reviewer')
    newest=g.observations(c,r['stream'])[-1]
    assert newest['retrieved_at']==original['retrieved_at'] and newest['sha256']==original['sha256']
    assert newest['correction_of']==original['capture_id'] and newest['success'] is False
    assert correct_observation(c,r,original['capture_id'],'Fixture reviewer')['capture_id']==corrected['capture_id']


def test_legacy_transport_success_stub_is_flagged_for_content_correction(env):
    c,r,_=env
    url='https://www.flsenate.gov/Laws/Statutes/2026/Title23/'
    r['sources']=[dict(id=g.source_id(url),url=url)]
    body=b'<html><title>Florida Statutes</title><body>Loading Florida Statutes\xe2\x80\xa6 Please enable JavaScript to view Florida Statutes.<script>document.cookie=\'fls_st=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa; Path=/; Max-Age=3600; SameSite=Lax; Secure\';location.replace(location.href);</script></body></html>'
    stream,scope=g.gate_identity(r['stream'])
    o=dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,content_type='text/html',
           sha256=h.sha(body),text_sha256=h.sha(b'Florida Statutes'),extraction='html-presentation-v2',
           source_id=g.source_id(url),run_id='legacy',registry_sha256=h.sha(r),review_protocol=r['review_protocol'],
           previous_sha256=None,previous_text_sha256=None,change='new')
    h.record(c,stream=stream,mode='manual_research',scope=scope,run_id='legacy',
             payload=dict(status='incomplete',contract=scope,checks=[],findings=[],drafts=[],source_gate=o),
             artifacts={h.sha(body):body,h.sha(b'Florida Statutes'):b'Florida Statutes'})
    task=g.queue(c,r)['tasks'][0]
    assert task['requires_content_correction'] is True and task['reason']=='retrieval_failed'
    with pytest.raises(ValueError,match='access challenge'):g.accept(c,r,receipt(task,r,c))


def test_parser_derivative_preserves_acquisition_and_cannot_invent_text(env,monkeypatch):
    from flwu.html_evidence import extract_html
    c,r,_=env
    body=b'<html><p>Office</p><a href="/instructions.pdf">Instructions</a></html>'
    def fetch(url):return dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,content_type='text/html'),body
    with monkeypatch.context() as patch:
        patch.setattr(g,'extract',lambda *a:('Legacy reading aid','legacy',[]))
        g.run(c,r,'one',fetch=fetch)
    old=g.observations(c,r['stream'])[0]
    text,links=extract_html(body,old['url'])
    rec=dict(source_id=old['source_id'],observation_capture_id=old['capture_id'],sha256=old['sha256'],
             method='html-presentation-v3',reviewer='Fixture reviewer',scope='Verified parser derivative')
    with pytest.raises(ValueError,match='exact parser output'):g.attach_text(c,r,rec,text+'invented')
    g.attach_text(c,r,rec,text)
    new=g.observations(c,r['stream'])[-1]
    assert new['sha256']==old['sha256'] and new['retrieved_at']==old['retrieved_at']
    assert new['links']==links and new['text_sha256']==h.sha(text.encode())


def test_withdrawal_preserves_original_and_disables_raw_reuse_and_replay(env):
    c,r,_=env;first,_=acquire(env,'one');rec=receipt(first['tasks'][0],r,c);saved=g.accept(c,r,rec)
    assert len(g.queue(c,r)['reused_reviews'])==1
    source=c.execute('SELECT payload FROM captures WHERE capture_id=?',(saved['capture_id'],)).fetchone()[0]
    marked=withdrawal.withdraw(c,r['stream'],h.sha(rec),'Cloud reviewer','Original explanation was unsupported.')
    assert c.execute('SELECT payload FROM captures WHERE capture_id=?',(saved['capture_id'],)).fetchone()[0]==source
    assert not g.queue(c,r)['reused_reviews']
    assert withdrawal.withdraw(c,r['stream'],h.sha(rec),'Cloud reviewer','Original explanation was unsupported.')['capture_id']==marked['capture_id']
    with pytest.raises(ValueError,match='withdrawn'):g.accept(c,r,rec)
    with pytest.raises(ValueError,match='immutable'):withdrawal.withdraw(c,r['stream'],h.sha(rec),'Other','Changed reason')
    corrected=copy.deepcopy(rec);corrected['summary']='Re-reviewed with bounded support.';g.accept(c,r,corrected)
    assert len(g.queue(c,r)['reused_reviews'])==1


def test_coordinator_withdrawal_requires_explicit_correction_and_invalidates_snapshot(tmp_path):
    run,db,r,_=environment(tmp_path);state=w.inspect(run,emit=True);answer(run,db,state)
    old=w.read(state['save_receipt']);original_packet=Path(state['packet']).read_bytes()
    with h.database(db) as c:withdrawal.withdraw(c,r['stream'],h.sha(old),'Cloud reviewer','Unsupported source classification.')
    with pytest.raises(ValueError,match='withdrawn'):w.submit(run,state['packet'],state['save_receipt'])
    next_state=w.inspect(run,emit=True);assert next_state['phase']=='source_review_correction'
    assert next_state['command'].endswith(' --advance')
    corrected=copy.deepcopy(old);corrected['summary']='Source re-reviewed and corrected.'
    path=run/'supported-correction.json';w.write(path,corrected)
    w.revise(run,next_state['packet'],path,next_state['predecessor'],next_state['correction_reason'])
    assert w.inspect(run)['phase']!='source_review_correction'
    assert Path(state['packet']).read_bytes()==original_packet


def test_current_guide_has_aligned_schema_without_changing_accepted_packet(tmp_path):
    from flwu import update
    before=b'<html><h1>Office</h1><div data-rule="old">Contact</div></html>'
    run,db,r,server=environment(tmp_path,profile=before)
    def fetch(url):
        meta,body=server(url);return dict(meta,content_type='text/html'),before if url=='https://court.gov/profile' else body
    with h.database(db) as c:g.run(c,r,'html-baseline',fetch=fetch);update.refresh(c,r,'trial',run)
    state=w.inspect(run,emit=True);answer(run,db,state)
    after=before.replace(b'old',b'new')
    with h.database(db) as c:
        g.run(c,r,'html-change',fetch=lambda url:(dict(fetch(url)[0]),after));update.refresh(c,r,'trial',run)
    state=w.inspect(run,emit=True);guide=w.read(state['review_guide']);template=w.read(state['receipt_template'])
    assert guide['guide_version']==6 and guide['aligned_groups']
    assert template['raw_change_review']['schema_version']==2
    assert '--advance' in state['command']
    assert w.read(state['packet'])['receipt_template']['raw_change_review'].get('schema_version') is None
