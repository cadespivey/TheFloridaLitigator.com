"""Content reuse boundaries, provenance and standard-command integration."""
import copy
import base64
import html
import json

import pytest

from flwu import content_fingerprint as f, history as h, raw_comparison, source_gate as g
from flwu import update, workflow as w
from tests.test_source_gate import env, receipt
from tests.test_opinion_discovery import Server, pdf_bytes


BEFORE = '2026-10-20T12:00:00Z'
AFTER = '2026-10-21T12:00:00Z'
URL = 'https://5dca.flcourts.gov/Judges/A'


def page(name='Judge A', stamp=BEFORE, day='2026-10-20', kind='recent_opinions',
         phone='555-0100', href='/instructions', runtime=1, body='<p>Contact</p>'):
    payload = dict(content='', start_date='10/01/2026', end_date=day,
                   date_field='disposition_date', items={'Written': {'date': day}})
    if kind == 'calendarpreview':
        payload = dict(content='', events=[{'name': 'Oral argument', 'date': day}])
    inner = '<div data-customtag="' + kind + '" data-content="' + html.escape(json.dumps(payload), quote=True) + '"></div>'
    outer = '<div data-customtag="contentblock" data-content="' + html.escape(json.dumps({'content': inner}), quote=True) + '"></div>'
    data = {'props': {'pageProps': {
        'pageData': {'name': name, 'chambersStaff': {'html5': '\n'},
                     'description': {'html5': '<p>Phone ' + phone + '</p><a href="' + href + '">Instructions</a>'}},
        'extraData': {'menu': [{'menudisplay': []}, {'menudisplay': {'fields': {'right_block': {'html5': outer}}}}]},
        'runtime': runtime}}}
    return ('<html><head><meta property="og:updated_time" content="' + stamp + '">'
            '<script id="__NEXT_DATA__" type="application/json">' + json.dumps(data) + '</script>'
            '</head><body>' + body + '</body></html>').encode()


def meta(url, raw, *, success=True, resolved=None):
    return dict(url=url, resolved_url=resolved or url, retrieved_at=h.now(),
                success=success, http_status=200 if success else 403, content_type='text/html',
                sha256=h.sha(raw), text_sha256=h.sha(b'nonempty extraction'), extraction='html-presentation-v2')


SENATE_URL = 'https://www.flsenate.gov/Laws/Statutes/2026'
SUNSHINE_URL = 'https://www.leg.state.fl.us/Statutes/'


def senate_page(token='A', ray='a', epoch='1792765800', law='Payment required.', logic='runChallenge()'):
    encoded = base64.b64encode(epoch.encode()).decode()
    return ('<html><head><title>Florida Statutes - The Florida Senate</title></head><body>'
            '<form action="/Laws/Statutes/2026"><input name="__RequestVerificationToken" type="hidden" value="' + token * 108 + '"></form>'
            '<p>' + law + '</p><script>window.__CF$cv$params={r:\'' + ray * 16 + '\',t:\'' + encoded + '\'};'
            + logic + ';</script></body></html>').encode()


def sunshine_page(clock='October 20, 2026', law='Payment required.', action='/statutes/index.cfm'):
    return ('<html><body><form id="search_statutes" action="' + action + '"><table>'
            '<tr id="datesearch"><td id="date">\r\n        ' + clock + '</td></tr>'
            '</table></form><p>' + law + '</p></body></html>').encode()


@pytest.mark.parametrize('url,before,after,profile', [
    (SENATE_URL, senate_page(), senate_page('B', 'b', '1792852200'), f.SENATE_PROFILE),
    (SUNSHINE_URL, sunshine_page(), sunshine_page('October 21, 2026'), f.SUNSHINE_PROFILE)])
def test_legislative_metadata_profiles_preserve_raw_evidence_and_reuse_completed_review(env, url, before, after, profile):
    conn, registry, _ = env
    setup(registry, (url,))
    first = acquire(conn, registry, 'first', {url: before})
    complete(conn, registry, first['tasks'][0])
    second = acquire(conn, registry, 'second', {url: after})
    assert not second['tasks']
    proof = second['reused_reviews'][0]['content_hash_reuse']
    assert proof['profile'] == profile
    assert proof['current_fingerprint']['core_sha256'] == proof['reviewed_fingerprint']['core_sha256']
    assert proof['current_fingerprint']['metadata'] != proof['reviewed_fingerprint']['metadata']
    assert g.blob(conn, proof['current_fingerprint']['original_sha256']) == after
    assert g.blob(conn, proof['reviewed_fingerprint']['original_sha256']) == before
    assert len(g.reviews(conn, registry['stream'])) == 1


@pytest.mark.parametrize('url,before,after', [
    (SENATE_URL, senate_page(), senate_page(law='Payment prohibited.')),
    (SENATE_URL, senate_page(), senate_page(logic='newSecurityLogic()')),
    (SENATE_URL, senate_page(), senate_page().replace(b'type="hidden"', b'type="text"')),
    (SENATE_URL, senate_page(), b'<html><h1>Just a moment. Verify you are human.</h1></html>'),
    (SUNSHINE_URL, sunshine_page(), sunshine_page(law='New effective date: November 1, 2026.')),
    (SUNSHINE_URL, sunshine_page(law='October 20, 2026'), sunshine_page(law='October 21, 2026')),
    (SUNSHINE_URL, sunshine_page(), sunshine_page(action='/new-filing-site'))])
def test_legislative_profiles_do_not_hide_law_script_form_or_challenge_changes(env, url, before, after):
    conn, registry, _ = env
    setup(registry, (url,))
    complete(conn, registry, acquire(conn, registry, 'first', {url: before})['tasks'][0])
    result = acquire(conn, registry, 'second', {url: after})
    assert [task['url'] for task in result['tasks']] == [url]
    assert not result['reused_reviews']


def test_legislative_scope_and_malformed_parameters_stay_conservative():
    raw = senate_page()
    assert f.fingerprint(raw, meta('https://www.flsenate.gov/Session/Bill', raw)) is None
    raw = senate_page(epoch='not-a-request-time')
    assert f.fingerprint(raw, meta(SENATE_URL, raw)) is None
    raw = sunshine_page(clock='Effective immediately')
    assert f.fingerprint(raw, meta(SUNSHINE_URL, raw)) is None
    raw = senate_page().replace(b'value="' + b'A' * 108, b'value="not-the-known-format')
    assert f.fingerprint(raw, meta(SENATE_URL, raw)) is None


def test_request_token_values_are_not_copied_into_fingerprint_metadata():
    raw = senate_page()
    projected = f.fingerprint(raw, meta(SENATE_URL, raw))
    assert projected and 'A' * 108 not in json.dumps(projected)
    assert projected['metadata'][0]['value_sha256'] == h.sha(b'A' * 108)


def test_ambiguous_duplicate_json_keys_cannot_be_normalized_away():
    raw = page().replace(b'"runtime": 1', b'"runtime": 1, "runtime": 2')
    assert f.fingerprint(raw, meta(URL, raw)) is None


def setup(registry, urls=(URL,)):
    registry['sources'] = [dict(id=g.source_id(url), url=url) for url in urls]


def acquire(conn, registry, name, bodies, *, failed=(), resolved=None):
    def fetch(url):
        item = meta(url, bodies[url], success=url not in failed, resolved=resolved)
        for key in ('sha256', 'text_sha256', 'extraction'):
            item.pop(key)
        return item, bodies[url]
    return g.run(conn, registry, name, fetch=fetch)


def complete(conn, registry, task):
    rec = receipt(task, registry, conn)
    o = task['observation']
    if o['change'] == 'changed':
        rec['outcome'] = 'no_relevant_change'
        rec['support']['previous'] = [dict(sha256=o['previous_sha256'],
            text_sha256=o['previous_text_sha256'], quote=g.blob(conn, o['previous_text_sha256']).decode(),
            locator='Entire fixture extraction')]
    if raw_comparison.required(o):
        comparison = raw_comparison.compare(g.blob(conn, o['previous_sha256']),
                                            g.blob(conn, o['sha256']), o['content_type'])
        raw = raw_comparison.template(comparison)
        raw['method'] = 'Entire synthetic original comparison inspected.'
        for change in raw['changes']:
            change['reason'] = 'Synthetic fixture metadata/widget change, not a live legal conclusion.'
        rec['raw_change_review'] = raw
    return g.accept(conn, registry, rec)


def test_timestamp_is_preserved_separately_and_all_other_content_is_hashed():
    before, after = page(), page(stamp=AFTER)
    a, b = f.fingerprint(before, meta(URL, before)), f.fingerprint(after, meta(URL, after))
    assert a['original_sha256'] != b['original_sha256']
    assert a['core_sha256'] == b['core_sha256']
    assert a['metadata'] == [{'property': 'og:updated_time', 'value': BEFORE}]
    assert b['metadata'] == [{'property': 'og:updated_time', 'value': AFTER}]
    assert b['profile'] == f.PROFILE and b['policy_sha256'] == h.sha(f.policy_bytes())


@pytest.mark.parametrize('change', [dict(name='Judge B'), dict(phone='555-0200'),
    dict(href='/new-instructions'), dict(runtime={'effective_date': '2026-11-01'}),
    dict(body='<p data-new-rule="required">Contact</p>'),
    dict(body='<div><p>Contact</p></div>')])
def test_contacts_links_identity_scripts_attributes_and_dom_boundaries_never_disappear(change):
    before, after = page(), page(stamp=AFTER, **change)
    a, b = f.fingerprint(before, meta(URL, before)), f.fingerprint(after, meta(URL, after))
    assert a and b and a['core_sha256'] != b['core_sha256']


def test_dom_parent_move_detected_even_when_flat_inspection_diff_matches():
    before = page(body='<a href="/a">Link</a><p>Text</p>')
    after = page(body='<a href="/a">Link<p>Text</p></a>')
    assert raw_comparison.html_structure(before) == raw_comparison.html_structure(after)
    assert f.fingerprint(before, meta(URL, before))['core_sha256'] != f.fingerprint(after, meta(URL, after))['core_sha256']


@pytest.mark.parametrize('before_body,after_body', [
    ('<p>"Contact"</p>', '<p>Contact</p>'),
    ('<script>"runAction()"</script>', '<script>runAction()</script>'),
    ('<p title="&quot;Notice&quot;">Contact</p>', '<p title="Notice">Contact</p>'),
    ('<a href="/old" href="/same">Records</a>', '<a href="/new" href="/same">Records</a>')])
def test_literal_text_scripts_attributes_and_duplicate_attributes_remain_distinct(before_body, after_body):
    before, after = page(body=before_body), page(body=after_body)
    a, b = f.fingerprint(before, meta(URL, before)), f.fingerprint(after, meta(URL, after))
    assert a and b and a['core_sha256'] != b['core_sha256']


def test_surrounding_widget_text_is_not_json_decoded_or_omitted():
    from bs4 import BeautifulSoup
    def with_caption(caption):
        soup = BeautifulSoup(page(), 'html.parser')
        script = soup.find('script', id='__NEXT_DATA__')
        data = json.loads(script.string)
        data['props']['pageProps']['extraData']['menu'][1]['menudisplay']['fields']['right_block']['html5'] += '<p>' + caption + '</p>'
        script.string = json.dumps(data)
        return str(soup).encode()
    before, after = with_caption('"Notice"'), with_caption('Notice')
    a, b = f.fingerprint(before, meta(URL, before)), f.fingerprint(after, meta(URL, after))
    assert a['components'] == b['components']
    assert a['core_sha256'] != b['core_sha256']


@pytest.mark.parametrize('kind', ['recent_opinions', 'calendarpreview'])
def test_widgets_have_separate_complete_state_hashes(kind):
    before, after = page(kind=kind), page(kind=kind, stamp=AFTER, day='2026-10-21')
    a, b = f.fingerprint(before, meta(URL, before)), f.fingerprint(after, meta(URL, after))
    assert a['core_sha256'] == b['core_sha256']
    assert a['components'][0]['sha256'] != b['components'][0]['sha256']
    assert a['components'][0]['kind'] == kind
    assert a['components'][0]['court'] == '5dca.flcourts.gov'


def test_unknown_widget_is_in_core_not_an_ignored_component():
    before, after = page(kind='new_legal_notice'), page(kind='new_legal_notice', day='2026-10-21')
    a, b = f.fingerprint(before, meta(URL, before)), f.fingerprint(after, meta(URL, after))
    assert a['components'] == []
    assert a['core_sha256'] != b['core_sha256']


@pytest.mark.parametrize('raw,url', [
    (page(stamp='not-a-timestamp'), URL), (page(), 'https://court.gov/Judges/A'),
    (page().replace(b'__NEXT_DATA__', b'OTHER_DATA'), URL),
    (page().replace(b'"pageData":', b'"unknownPage":'), URL),
    (page().replace(b'</head>', b'<meta property="og:updated_time" content="' + BEFORE.encode() + b'"></head>'), URL),
    (b'%PDF-changed-scan', URL)])
def test_unsupported_or_ambiguous_sources_fall_back_to_review(raw, url):
    assert f.fingerprint(raw, meta(url, raw)) is None


def test_missing_extraction_failure_and_changed_redirect_are_not_reused(env):
    conn, registry, _ = env
    setup(registry)
    first = acquire(conn, registry, 'first', {URL: page()})
    complete(conn, registry, first['tasks'][0])
    failed = acquire(conn, registry, 'failed', {URL: page(stamp=AFTER)}, failed=[URL])
    assert failed['tasks'][0]['reason'] == 'retrieval_failed'
    redirect = acquire(conn, registry, 'redirect', {URL: page(stamp=AFTER)}, resolved=URL + '/moved')
    assert redirect['tasks'] and not redirect['reused_reviews']
    observed = g.observations(conn, registry['stream'])[-1]
    observed['text_sha256'] = None
    assert not f.eligible(observed)


def test_metadata_reuse_is_machine_provenance_not_fabricated_human_review(env):
    conn, registry, root = env
    setup(registry)
    first = acquire(conn, registry, 'first', {URL: page()})
    complete(conn, registry, first['tasks'][0])
    before_reviews = g.reviews(conn, registry['stream'])
    second = acquire(conn, registry, 'second', {URL: page(stamp=AFTER)})
    assert not second['tasks']
    reused = second['reused_reviews'][0]
    assert reused['change'] == 'changed' and reused['reuse_basis'] == 'content_and_component_hashes'
    proof = reused['content_hash_reuse']
    assert proof['current_fingerprint']['original_sha256'] != proof['reviewed_fingerprint']['original_sha256']
    assert proof['current_fingerprint']['core_sha256'] == proof['reviewed_fingerprint']['core_sha256']
    assert proof['component_reviews'][0]['reviewed']['receipt_sha256'] == before_reviews[0]['receipt_sha256']
    assert g.reviews(conn, registry['stream']) == before_reviews
    audits = [json.loads(row['payload']) for row in conn.execute('SELECT payload FROM captures')
              if 'source_content_reuse' in json.loads(row['payload'])]
    assert len(audits) == 1 and audits[0]['source_content_reuse'] == proof
    assert audits[0]['findings'] == [] and 'source_gate_review' not in audits[0]
    assert conn.execute('SELECT count(*) FROM finalized_reports').fetchone()[0] == 0
    count = conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    g.write_queue(conn, registry, root / 'refreshed')
    g.write_queue(conn, registry, root / 'refreshed')
    assert conn.execute('SELECT count(*) FROM captures').fetchone()[0] == count
    assert g.blob(conn, proof['current_fingerprint']['original_sha256']) == page(stamp=AFTER)


def test_reading_aid_upgrade_does_not_requeue_equal_reviewed_original_content(env, monkeypatch):
    conn, registry, _ = env
    setup(registry, (SUNSHINE_URL,))
    native = g.extract
    def old_extractor(raw, metadata):
        text, _, links = native(raw, metadata)
        return text, 'html-visible-text', links
    with monkeypatch.context() as patch:
        patch.setattr(g, 'extract', old_extractor)
        first = acquire(conn, registry, 'first', {SUNSHINE_URL: sunshine_page()})
    complete(conn, registry, first['tasks'][0])
    second = acquire(conn, registry, 'second', {SUNSHINE_URL: sunshine_page('October 21, 2026')})
    assert not second['tasks']
    proof = second['reused_reviews'][0]['content_hash_reuse']
    assert proof['reviewed_extraction'] == 'html-visible-text'
    assert proof['current_extraction'] == 'html-presentation-v2'
    third = acquire(conn, registry, 'third', {SUNSHINE_URL: sunshine_page('October 22, 2026', law='New legal requirement.')})
    assert third['tasks']  # The same transition cannot hide changed original content.


def test_changed_shared_component_reviewed_once_per_court_and_protocol(env):
    conn, registry, _ = env
    other = 'https://5dca.flcourts.gov/Judges/B'
    setup(registry, (URL, other))
    first = acquire(conn, registry, 'first', {URL: page(), other: page('Judge B')})
    for task in first['tasks']:
        complete(conn, registry, task)
    second = acquire(conn, registry, 'second', {
        URL: page(stamp=AFTER, day='2026-10-21'),
        other: page('Judge B', stamp=AFTER, day='2026-10-21')})
    assert len(second['tasks']) == 2  # New widget state has no completed interpretation.
    complete(conn, registry, second['tasks'][0])
    refreshed = g.queue(conn, registry)
    assert not refreshed['tasks']
    reused = next(item for item in refreshed['reused_reviews'] if item['source_id'] == g.source_id(other))
    proof = reused['content_hash_reuse']
    assert proof['reviewed_observation_capture_id'] == first['tasks'][1]['observation']['capture_id']
    assert proof['component_reviews'][0]['reviewed']['source_id'] == g.source_id(URL)
    assert len(g.reviews(conn, registry['stream'])) == 3  # No cloned fourth model receipt.
    changed_protocol = copy.deepcopy(registry)
    changed_protocol['review_protocol'] = 'changed-review-scope'
    assert len(g.queue(conn, changed_protocol)['tasks']) == 2


def test_new_review_of_known_component_does_not_churn_existing_reuse_audits(env):
    conn, registry, root = env
    urls = [URL, 'https://5dca.flcourts.gov/Judges/B', 'https://5dca.flcourts.gov/Judges/C']
    setup(registry, urls)
    first = acquire(conn, registry, 'first', {url: page('Judge ' + str(index)) for index, url in enumerate(urls)})
    for task in first['tasks'][:2]:
        complete(conn, registry, task)
    second = acquire(conn, registry, 'second', {url: page('Judge ' + str(index), stamp=AFTER) for index, url in enumerate(urls)})
    before = {item['source_id']: item['content_hash_reuse'] for item in second['reused_reviews']}
    assert len(second['tasks']) == 1 and len(before) == 2
    complete(conn, registry, second['tasks'][0])
    count = conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    refreshed = g.write_queue(conn, registry, root / 'after-new-review')
    after = {item['source_id']: item['content_hash_reuse'] for item in refreshed['reused_reviews'] if item.get('content_hash_reuse')}
    assert after == before
    assert conn.execute('SELECT count(*) FROM captures').fetchone()[0] == count


def test_other_court_component_and_unreviewed_source_cannot_borrow_full_review(env):
    conn, registry, _ = env
    other = 'https://6dca.flcourts.gov/Judges/B'
    new = 'https://5dca.flcourts.gov/Judges/New'
    setup(registry, (URL, other, new))
    first = acquire(conn, registry, 'first', {URL: page(), other: page('Judge B'), new: page('New')})
    for task in first['tasks'][:2]:
        complete(conn, registry, task)
    second = acquire(conn, registry, 'second', {URL: page(stamp=AFTER, day='2026-10-21'),
        other: page('Judge B', stamp=AFTER, day='2026-10-21'), new: page('New', stamp=AFTER, day='2026-10-21')})
    complete(conn, registry, second['tasks'][0])
    assert {task['url'] for task in g.queue(conn, registry)['tasks']} == {other, new}


def test_changed_pdf_and_effective_date_trigger_survive_html_reuse(env):
    conn, registry, _ = env
    pdf = 'https://5dca.flcourts.gov/rules.pdf'
    setup(registry, (URL, pdf))
    def fetch(body, document):
        def get(url):
            if url == pdf:
                return dict(url=url, resolved_url=url, retrieved_at=h.now(), success=True,
                            http_status=200, content_type='application/pdf'), document
            return {key: value for key, value in meta(url, body).items()
                    if key not in ('sha256', 'text_sha256', 'extraction')}, body
        return get
    original_pdf = pdf_bytes('Unchanged extracted text.')
    first = g.run(conn, registry, 'first', fetch=fetch(page(), original_pdf))
    for task in first['tasks']:
        complete(conn, registry, task)
    h.record(conn, stream=registry['stream'], mode='manual_research', scope={'profile': 'test'},
        run_id='effective-date', payload=dict(status='incomplete', contract={}, checks=[], drafts=[],
        findings=[dict(key='rule', kind='rule', facts={'effective_date': '2026-10-22'},
                       citations=[{'url': URL}])]), artifacts={})
    second = g.run(conn, registry, 'second', fetch=fetch(page(stamp=AFTER), original_pdf + b'\n% corrected version\n'))
    assert [task['url'] for task in second['tasks']] == [pdf]
    observed = second['tasks'][0]['observation']
    assert observed['sha256'] != observed['previous_sha256']
    assert observed['text_sha256'] == observed['previous_text_sha256']
    assert g.queue(conn, registry, start='2026-10-01', end='2026-10-31')['effective_date_tasks']


def test_cached_projection_cannot_hide_new_contact_bytes(env):
    conn, registry, _ = env
    setup(registry)
    complete(conn, registry, acquire(conn, registry, 'first', {URL: page()})['tasks'][0])
    acquire(conn, registry, 'second', {URL: page(stamp=AFTER, phone='555-0200')})
    observations = g.observations(conn, registry['stream'])
    old, current = observations[-2:]
    current['content_fingerprint'] = old['content_fingerprint']  # Untrusted/stale cache.
    index = f.ReviewIndex(observations, g.reviews(conn, registry['stream']),
                         g.raw_bases(observations), registry['review_protocol'], lambda digest: g.blob(conn, digest))
    assert index.reuse(current) is None


def test_unsubstantiated_legacy_review_cannot_seed_content_reuse(env):
    conn, registry, _ = env
    setup(registry)
    acquire(conn, registry, 'first', {URL: page()})
    second = acquire(conn, registry, 'second', {URL: page(stamp=AFTER)})
    rec = receipt(second['tasks'][0], registry, conn)
    saved = dict(rec, receipt_sha256=h.sha(rec), acceptance_version=3)
    h.record(conn, stream=registry['stream'], mode='manual_research', scope={'profile': 'test'},
             run_id='legacy-unverified', payload=dict(status='incomplete', contract={}, checks=[],
             findings=[], drafts=[], source_gate_review=saved), artifacts={})
    third = acquire(conn, registry, 'third', {URL: page(stamp='2026-10-22T12:00:00Z')})
    assert third['tasks'] and not third['reused_reviews']


def test_recovery_after_audit_saved_but_queue_write_interrupted(env, monkeypatch):
    conn, registry, root = env
    setup(registry)
    complete(conn, registry, acquire(conn, registry, 'first', {URL: page()})['tasks'][0])
    acquire(conn, registry, 'second', {URL: page(stamp=AFTER)})
    count = conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    from pathlib import Path
    original = Path.write_text
    def fail(path, *args, **kwargs):
        if path.name == 'queue.json':
            raise OSError('interrupted queue projection')
        return original(path, *args, **kwargs)
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'write_text', fail)
        with pytest.raises(OSError, match='interrupted queue'):
            g.write_queue(conn, registry, root / 'projection')
    assert not g.write_queue(conn, registry, root / 'projection')['tasks']
    assert conn.execute('SELECT count(*) FROM captures').fetchone()[0] == count


def test_standard_update_and_coordinator_use_hash_reuse_without_reacquisition(tmp_path):
    database = tmp_path / 'database.sqlite'
    registry = dict(schema_version=1, stream='weekly', review_protocol=g.PROTOCOL,
                    sources=[dict(id=g.source_id(URL), url=URL)])
    registry_path = tmp_path / 'registry.json'
    w.write(registry_path, registry)
    server = Server([])
    current = page()
    def fetch(url):
        if url == URL:
            server.calls.append(url)
            return {key: value for key, value in meta(url, current).items()
                    if key not in ('sha256', 'text_sha256', 'extraction')}, current
        return server(url)
    with h.database(database) as conn:
        h.record(conn, stream='weekly', mode='manual_research', scope={'profile': 'test'}, run_id='initial',
                 payload=dict(status='incomplete', contract={}, checks=[], drafts=[], findings=[]), artifacts={})
        first = update.run(conn, registry, 'first', tmp_path / 'first', start='2026-10-15', end='2026-10-22', fetch=fetch)
        expanded = g.load_registry(tmp_path / 'first' / 'expanded-registry.json')
        for task in first['source_reviews']['tasks']:
            complete(conn, expanded, task)
    run = tmp_path / 'second'
    w.initialize(run, database, registry_path, 'second', start='2026-10-15', end='2026-10-22')
    current = page(stamp=AFTER)
    server.calls.clear()
    with h.database(database) as conn:
        result = update.run(conn, registry, 'second', run, start='2026-10-15', end='2026-10-22', fetch=fetch)
    assert len([url for url in server.calls if '_search/opinions/' in url]) == 14
    assert not result['source_reviews']['tasks'] and not result['opinion_reviews']['tasks']
    assert next(item for item in result['source_reviews']['reused_reviews']
                if item['source_id'] == g.source_id(URL))['reuse_basis'] == 'content_and_component_hashes'
    calls = list(server.calls)
    assert w.inspect(run, emit=True)['phase'] == 'prepare_report'
    assert server.calls == calls
