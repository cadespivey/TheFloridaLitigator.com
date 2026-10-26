import copy
import json

import pytest

from flwu import history as h
from flwu.publication import candidate_summary, directory_links, export_capture, validate_issue, digest
from tests.test_publication_evidence_gates import report_fixture


def test_export_preserves_only_explicit_evidence_bound_person_links(tmp_path):
    db = tmp_path / 'db'
    with h.database(db) as conn:
        cap, _, _, ref = report_fixture(conn, tmp_path)
        payload = json.loads(conn.execute('SELECT payload FROM captures WHERE capture_id=?',
                                         (cap['capture_id'],)).fetchone()[0])
        payload['findings'][0]['facts'].update(holding='Reviewed holding.', disposition='Affirmed.', authors=['Actual Author'])
        facts = dict(name='Actual Person', fields={}, public_links={'profile': ref, 'procedure': ref})
        payload['findings'].append(dict(key='person-one', kind='judge', facts=facts, citations=[ref]))
        cap = h.record(conn, stream='report', mode='manual_research', scope={}, run_id='links',
                       payload=payload, artifacts={})
    output = export_capture(db, cap['capture_id'], tmp_path/'archive', preview=True)
    issue = json.loads(output.read_text())
    person = issue['directory'][0]
    summary = issue['sections']['case_law']['items'][0]['summary']
    for line in ('Holding: Reviewed holding.', 'Disposition: Affirmed.', 'Author: Actual Author'):
        assert line in summary
    assert person['profile_url'] == ref['url'] == person['procedure_url']
    validate_issue(issue, preview=True)
    for field in ('profile_url', 'procedure_url'):
        invalid = copy.deepcopy(issue)
        invalid['directory'][0][field] = 'https://court.example/invented'
        invalid['content_sha256'] = digest({k:v for k,v in invalid.items() if k!='content_sha256'})
        with pytest.raises(ValueError, match='exact source citation'):
            validate_issue(invalid, preview=True)


def test_link_selection_never_guesses_or_accepts_unbound_quotes():
    citation = dict(url='https://court.example/person', quote='Actual Person', label='Profile')
    assert directory_links({}, [citation]) == {}
    for selection in ({'profile':dict(citation,url='https://court.example/other')},
                      {'procedure':dict(citation,quote='Unverified procedure')},
                      {'unknown':citation}, {'profile':None}):
        with pytest.raises(ValueError):
            directory_links({'public_links':selection}, [citation])


def test_opinion_projection_retains_existing_text_and_rejects_conflicting_labels():
    facts = dict(summary='Intro.\nHolding: Same holding.', holding='Same holding.', authors=['One', 'Two'])
    assert candidate_summary(facts, 'case_law') == 'Intro.\nHolding: Same holding.\n\nAuthor: One, Two'
    assert candidate_summary(facts, 'procedural_rules') == facts['summary']
    with pytest.raises(ValueError, match='Conflicting structured opinion field'):
        candidate_summary(dict(facts,holding='Different holding.'), 'case_law')
