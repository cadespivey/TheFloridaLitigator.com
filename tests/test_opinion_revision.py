import copy
import json

import pytest

from flwu import history as h, opinion_discovery as d, publication_acceptance as pa
from tests.test_opinion_discovery import env, Server, opinion, run, accept


def prepared(env):
    result = run(env, Server([opinion(1)]))
    accept(env, result)
    conn, registry, _ = env
    rows = [(row, json.loads(row['payload']).get('opinion_review'))
            for row in conn.execute('SELECT * FROM captures ORDER BY seq')]
    row, previous = next((row, r) for row, r in reversed(rows) if r)
    receipt = {k: previous[k] for k in ('id', 'signature', 'reviewer', 'relevance', 'summary',
                                       'holding', 'disposition', 'authors', 'citations')}
    receipt.update(summary='A concise commercial holding summary.', reviewer='Editorial reviewer',
                   predecessor_version=previous['receipt_sha256'], reason='Remove internal acquisition narrative.',
                   pdf_sha256=previous['pdf_sha256'], state_sha256=previous['state_sha256'],
                   review_protocol=registry['review_protocol'])
    receipt['citations'][0]['quote'] = 'Commercial holding. Affirmed. Author Example.'
    return receipt, row['capture_id'], previous


def test_revision_preserves_predecessor_and_drives_publication_requirement(env):
    conn, registry, _ = env
    receipt, predecessor_id, previous = prepared(env)
    before = conn.execute('SELECT payload FROM captures WHERE capture_id=?', (predecessor_id,)).fetchone()[0]
    result = d.revise_review(conn, registry, receipt)
    assert conn.execute('SELECT payload FROM captures WHERE capture_id=?', (predecessor_id,)).fetchone()[0] == before
    row = conn.execute('SELECT * FROM captures WHERE capture_id=?', (result['capture_id'],)).fetchone()
    new = json.loads(row['payload'])['opinion_review']
    assert new['editorial_revision']['predecessor_version'] == previous['receipt_sha256']
    requirement = pa.requirements(conn, row)['opinion:'+receipt['id']]
    assert requirement['summary'] == receipt['summary']
    assert requirement['version'] == new['receipt_sha256'] != previous['receipt_sha256']
    assert not d.review_queue(conn, registry)['tasks']
    with pytest.raises(ValueError, match='stale'):
        d.revise_review(conn, registry, receipt)


@pytest.mark.parametrize('field,value', [('predecessor_version', 'stale'), ('signature', 'changed'),
    ('pdf_sha256', 'changed'), ('state_sha256', 'changed'), ('review_protocol', 'different'),
    ('relevance', 'not_relevant'), ('authors', ['Invented Name']), ('citations', [])])
def test_revision_rejects_stale_or_unsupported_receipt_without_write(env, field, value):
    conn, registry, _ = env
    receipt, _, _ = prepared(env)
    count = conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    receipt[field] = value
    with pytest.raises(ValueError):
        d.revise_review(conn, registry, receipt)
    assert conn.execute('SELECT count(*) FROM captures').fetchone()[0] == count


def test_revision_rejects_changed_current_pdf(env):
    conn, registry, _ = env
    receipt, _, _ = prepared(env)
    server = Server([opinion(1)])
    from tests.test_opinion_discovery import pdf_bytes
    server.pdf = pdf_bytes('Changed commercial holding. Reversed. Author Example.')
    run(env, server, run_id='changed')
    with pytest.raises(ValueError, match='ordinary opinion review'):
        d.revise_review(conn, registry, receipt)
