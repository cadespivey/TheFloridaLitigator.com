"""Whitespace policy for contact fields: real acquired bytes, real validators, fail-closed otherwise."""
import copy
import pytest
from flwu import history as h, source_gate as g, workflow as w, compact_review as short
from flwu import workflow_report
from tests.test_source_gate import env, acquire, receipt

BEFORE = 'Sandra Williams was Clerk.\nPhone: 555-0100\n'
NBSP_PAGE = ('Kristopher Warburton was selected as Clerk on October 30, 2026.\n'
             'Office: 300 South\u00a0Beach Street\nDaytona\u00a0Beach, FL 32114\n'
             'Phone: (386) 947-1530\n')
RUN_PAGE = ('Kristopher Warburton was selected as Clerk on October 30, 2026.\n'
            'Phone:\t(386)  947-1530\n'
            '300 South Beach Street\nDaytona Beach, FL 32114\n')


def changed_task(env, after, before=BEFORE):
    c, r, root = env
    first, _ = acquire(env, 'before', page=before.encode())
    for t in first['tasks']:
        g.accept(c, r, receipt(t, r, c))
    acquire(env, 'after', page=after.encode())
    q = g.write_queue(c, r, root/'sources')
    task = next(w.tasks(c, {'run_dir': str(root/'run')}, {'source_reviews': q, 'opinion_reviews': {'tasks': []}}))
    return task, short.prepare(c, task)


def clerk_answer(bundle, fields):
    ref = next(e['id'] for e in bundle['card']['evidence'] if e['side'] == 'current')
    return dict(decision='material_change',
                summary='Kristopher Warburton was selected as Clerk on October 30, 2026; the page lists office contact details.',
                evidence=[ref],
                people=[dict(person='new', name='Kristopher Warburton', kind='clerk', evidence=[ref], fields=fields)])


def record(person):
    return {k: person[k] for k in ('key', 'kind', 'facts', 'citations')}


def test_ordinary_space_contact_is_supported_by_nbsp_source(env):
    c, r, _ = env
    task, bundle = changed_task(env, NBSP_PAGE)
    frozen_task, frozen_bundle, submitted = copy.deepcopy(task), copy.deepcopy(bundle), '300 South Beach Street\nDaytona Beach, FL 32114'
    answer = clerk_answer(bundle, dict(
        office_address=dict(value=submitted, evidence='C1'),
        office_phone=dict(value='(386) 947-1530', evidence='C1')))
    frozen_answer = copy.deepcopy(answer)
    draft = short.compile_answer(task, bundle, answer)
    person = draft['findings'][0]
    address, phone = person['facts']['fields']['office_address'], person['facts']['fields']['office_phone']
    # Whitespace-equivalent route: the submitted text is not a byte-exact substring.
    assert submitted not in address['citation']['quote']
    # The receipt quote is the exact acquired passage, still bound to current originals.
    assert '300 South\u00a0Beach Street' in address['citation']['quote']
    assert address['citation']['quote'] in g.blob(c, address['citation']['text_sha256']).decode()
    assert address['citation']['sha256'] == task['inputs']['observation']['sha256']
    # Submitted values are preserved exactly and the other contact is retained.
    assert address['value'] == submitted and phone['value'] == '(386) 947-1530'
    assert address['citation'] in person['citations'] and phone['citation'] in person['citations']
    assert task == frozen_task and bundle == frozen_bundle and answer == frozen_answer
    saved = g.accept(c, r, draft)
    workflow_report.validate_records(c, {'registry': r}, [record(person)])
    assert g.accept(c, r, draft)['capture_id'] == saved['capture_id']


def test_whitespace_runs_and_newlines_in_contact_text(env):
    c, r, _ = env
    task, bundle = changed_task(env, RUN_PAGE)
    answer = clerk_answer(bundle, dict(
        office_phone=dict(value='(386) 947-1530', evidence='C1'),
        office_address=dict(value='300 South Beach Street Daytona Beach, FL 32114', evidence='C1')))
    compiled = short.compile_answer(task, bundle, answer)
    fields = compiled['findings'][0]['facts']['fields']
    # Source runs and the submitted newline flattening are preserved in the receipt values.
    assert fields['office_phone']['value'] == '(386) 947-1530'
    assert fields['office_address']['value'] == '300 South Beach Street Daytona Beach, FL 32114'
    assert '\t' in fields['office_phone']['citation']['quote']
    g.accept(c, r, compiled)
    workflow_report.validate_records(c, {'registry': r}, [record(compiled['findings'][0])])


@pytest.mark.parametrize('field,value,match', [
    ('office_phone', '(386) 947-1531', 'Field value'),                      # changed digit
    ('office_phone', '(386). 947-1530', 'Field value'),                     # changed punctuation
    ('assistant_name', 'DANA Ellis', 'Field value'),                        # changed case
    ('office_address', '300 North Beach Street\nDaytona Beach, FL 32114', 'Field value'),  # changed text
    ('procedure', 'Civil motions require five  days notice.', 'Field value must occur exactly'),  # narrative normalization
])
def test_nonwhitespace_contact_differences_fail_closed(env, field, value, match):
    task, bundle = changed_task(env, 'Kristopher Warburton was selected as Clerk.\nAssistant: Dana Ellis\nPhone: (386) 947-1530\n300 South Beach Street\nDaytona Beach, FL 32114\nCivil motions require five days notice.\n')
    answer = clerk_answer(bundle, dict(assistant_name=dict(value='Dana Ellis', evidence='C1')))
    answer['people'][0]['fields'][field] = dict(value=value, evidence='C1')
    with pytest.raises(ValueError, match=match) as error:
        short.compile_answer(task, bundle, answer)
    assert f'fields.{field}:' in str(error.value)


def test_previous_only_evidence_cannot_support_current_contact(env):
    task, bundle = changed_task(env, 'Kristopher Warburton was Clerk.\nPhone: (386) 947-1530\n')
    answer = clerk_answer(bundle, dict(office_phone=dict(value='555-0100', evidence='P1')))
    with pytest.raises(ValueError, match='Current personnel fields'):
        short.compile_answer(task, bundle, answer)


def test_url_and_email_contact_values_keep_exact_matching_only(env):
    c, r, root = env
    before = b'<h1>Kristopher Warburton</h1><p>Guide</p>'
    after = (b'<h1>Kristopher Warburton is Clerk</h1>'
             b'<p>Guide: <a href="https://court.gov/guide.pdf">https://court.gov/guide.pdf</a></p>'
             b'<p>Email: clerk@daytonabeachcourt.gov</p>'
             b'<p>Backup: clerk@  court.gov</p>')
    def fetch(body):
        return lambda url: (dict(url=url, resolved_url=url, retrieved_at=h.now(), success=True,
                                 http_status=200, content_type='text/html'), body)
    first = g.run(c, r, 'contact-links-before', fetch=fetch(before))
    for t in first['tasks']:
        g.accept(c, r, receipt(t, r, c))
    g.run(c, r, 'contact-links-after', fetch=fetch(after))
    q = g.write_queue(c, r, root/'exports')
    task = next(w.tasks(c, {'run_dir': str(root/'run')}, {'source_reviews': q, 'opinion_reviews': {'tasks': []}}))
    bundle = short.prepare(c, task)
    # Exact URL (passage + link inventory) and exact email values still pass.
    g.accept(c, r, short.compile_answer(task, bundle,
        clerk_answer(bundle, dict(office_contact=dict(value='https://court.gov/guide.pdf', evidence='C1')))))
    email = short.compile_answer(task, bundle,
        clerk_answer(bundle, dict(office_contact=dict(value='clerk@daytonabeachcourt.gov', evidence='C1'))))
    assert email['findings'][0]['facts']['fields']['office_contact']['value'] == 'clerk@daytonabeachcourt.gov'
    # Whitespace-mutated URL and email values fail even when whitespace-equivalent text exists.
    for field, mutated in (('office_contact', 'https://court.gov/guide.pdf '),
                           ('office_contact', 'https://court.gov/guide.pdf  '),
                           ('office_contact', 'clerk@ daytonabeachcourt.gov'),
                           ('office_contact', 'clerk@ court.gov')):
        answer = clerk_answer(bundle, dict(**{field: dict(value=mutated, evidence='C1')}))
        with pytest.raises(ValueError, match='Field value must occur exactly'):
            short.compile_answer(task, bundle, answer)


def test_existing_person_patch_preserves_nested_prior_facts_and_inputs(env):
    c, r, root = env
    old = 'Judge Elise Grant\nChambers: (813) 555-0100\nAssistant: Dana Ellis\n'
    first, _ = acquire(env, 'initial-judge', page=old.encode())
    for t in first['tasks']:
        rec = receipt(t, r, c)
        if t['source_id'] == r['sources'][0]['id']:
            o = t['observation']
            ci = {k: o[k] for k in ('url', 'sha256', 'text_sha256', 'retrieved_at', 'http_status')}
            ci.update(quote=old, locator='Initial complete source')
            facts = dict(name='Elise Grant',
                         fields={'chambers_phone': dict(value='(813) 555-0100', status='verified', citation=ci),
                                 'assistant_name': dict(value='Dana Ellis', status='verified', citation=ci)},
                         procedure={'documents': [{'url': 'https://court.gov/civil', 'detail': {'untouched': True}}]})
            rec.update(outcome='updated_findings',
                       findings=[dict(key='person-elise-grant', kind='judge', facts=facts, citations=[ci], expected_version=None)])
        g.accept(c, r, rec)
    updated = 'Judge Elise Grant\nChambers: (813)\u00a0555-0142\nAssistant: Dana Ellis\n'
    acquire(env, 'judge-nbsp-update', page=updated.encode())
    q = g.write_queue(c, r, root/'judge-exports')
    task = next(w.tasks(c, {'run_dir': str(root/'run')}, {'source_reviews': q, 'opinion_reviews': {'tasks': []}}))
    bundle = short.prepare(c, task)
    frozen_task, frozen_bundle = copy.deepcopy(task), copy.deepcopy(bundle)
    prior_fields = copy.deepcopy(bundle['prior_people']['person1']['facts']['fields'])
    answer = dict(decision='material_change', summary='Judge Grant now lists chambers phone (813) 555-0142.',
                  evidence=['C1'],
                  people=[dict(person='person1', name='Elise Grant', kind='judge', evidence=['C1'],
                               fields={'chambers_phone': dict(value='(813) 555-0142', evidence='C1')})])
    compiled = short.compile_answer(task, bundle, answer)
    person = compiled['findings'][0]
    assert person['key'] == 'person-elise-grant' and person['expected_version']
    # Only the named field changes; prior contacts and nested facts survive byte-for-byte.
    assert person['facts']['fields']['assistant_name'] == prior_fields['assistant_name']
    assert person['facts']['procedure'] == {'documents': [{'url': 'https://court.gov/civil', 'detail': {'untouched': True}}]}
    assert person['facts']['fields']['chambers_phone']['value'] == '(813) 555-0142'
    assert '(813)\u00a0555-0142' in person['facts']['fields']['chambers_phone']['citation']['quote']
    assert task == frozen_task and bundle == frozen_bundle
    g.accept(c, r, compiled)
    workflow_report.validate_records(c, {'registry': r}, [record(person)])
    conflicting = copy.deepcopy(compiled)
    conflicting['findings'][0]['expected_version'] = 'stale'
    with pytest.raises(ValueError, match='changed since review'):
        g.accept(c, r, conflicting)


def test_opinion_card_keeps_six_field_template_with_decision_guidance(env):
    c, r, _ = env
    first, _ = acquire(env, 'opinion-base', page=b'Opinion fixture text.\n')
    for t in first['tasks']:
        g.accept(c, r, receipt(t, r, c))
    observations = g.observations(c, 'research')
    judge = next(o for o in observations if o['url'] == 'https://court.gov/judge' and o['success'])
    pdf = next(o for o in observations if o['url'] == 'https://court.gov/procedure.pdf' and o['success'])
    task = dict(kind='opinion_review', identity='opinion:1D26-0001', packet_sha256='fixture-packet',
                receipt_template=dict(relevance='', summary='', holding='', disposition='', authors=[], evidence=[]),
                inputs=dict(source_observation=judge,
                            opinion=dict(id='1D26-0001', court='First DCA', case_number='1D26-0001',
                                         title='Fixture v. Fixture', published_date='2026-11-01', status='published',
                                         status_source=pdf)))
    bundle = short.prepare(c, task)
    assert not bundle['exception']
    # Exact six-field answer shape is unchanged.
    assert bundle['answer_template'] == dict(relevance='', summary='', holding='', disposition='', authors=[], evidence=[])
    assert set(bundle['card']['answer']) == {'relevance', 'summary', 'holding', 'disposition', 'authors', 'evidence'}
    # Compact decision guidance ships in the card itself, on top of evidence IDs.
    help_text = bundle['card']['answer_help']
    assert {'relevance', 'evidence', 'authors', 'scope', 'bare_disposition', 'uncertain', 'labels',
            'holding', 'summary', 'disposition', 'not_relevant'} <= set(help_text)
    assert help_text['relevance'] == ['relevant', 'not_relevant', 'uncertain']
    assert all(isinstance(v, str) and v for k, v in help_text.items() if k != 'relevance')
    assert {e['side'] for e in bundle['card']['evidence']} == {'current', 'status'}


@pytest.mark.parametrize('link', ['HTTPS://court.gov/guide.pdf', 'https://court.gov/guide.pdf', 'mailto:clerk'])
def test_embedded_link_contact_descriptions_never_use_whitespace_fallback(env, link):
    exact = 'Guide: ' + link + '\u00a0(updated)'
    task, bundle = changed_task(env, 'Kristopher Warburton is Clerk.\n' + exact + '\n')
    answer = clerk_answer(bundle, dict(office_contact=dict(value=exact, evidence='C1')))
    compiled = short.compile_answer(task, bundle, answer)
    assert compiled['findings'][0]['facts']['fields']['office_contact']['value'] == exact
    answer['people'][0]['fields']['office_contact']['value'] = exact.replace('\u00a0', ' ')
    with pytest.raises(ValueError, match='fields.office_contact:.*Field value must occur exactly'):
        short.compile_answer(task, bundle, answer)
