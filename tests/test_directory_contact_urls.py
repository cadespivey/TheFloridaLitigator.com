"""Public contact pages are links; unsafe/local/credential-bearing URLs are not."""
import copy
import pytest

from flwu import county_directory as directory
from flwu import workflow_directory as workflow
from tests.test_county_directory import supplement, seal


@pytest.mark.parametrize('url', [
    'https://5dca.flcourts.gov/Clerk-s-Office',
    'https://court.example/contact?department=civil',
])
def test_directory_accepts_public_https_contact_pages_without_changing_them(supplement, url):
    row = dict(label='Case inquiries', lines=['Contact the Clerk’s Office.'],
               href=url, fact_path='contacts.public_inquiries', type='note')
    supplement['people'][0]['contacts']['office'].append(row)
    seal(supplement)
    assert directory.validate_supplement(supplement, preview=True) is supplement
    assert supplement['people'][0]['contacts']['office'][-1] == row


@pytest.mark.parametrize('url', [
    'javascript:alert(1)', 'data:text/html,test', 'file:///tmp/contact',
    '//court.example/contact', 'http://court.example/contact',
    'https://localhost/contact', 'https://127.0.0.1/contact', 'https://[::1]/contact',
    'https://user:password@court.example/contact',
    'https://court.example/contact?api_key=secret',
    'https://court.example/contact?access_token=secret',
    'https://court.example/contact\n', 'https://court.example/contact\\path',
    'mailto:ja@court.example?bcc=other@court.example', 'tel:+15550100',
])
def test_directory_rejects_unsafe_or_unsupported_contact_links(supplement, url):
    supplement['people'][0]['contacts']['office'][0]['href'] = url
    seal(supplement)
    with pytest.raises(ValueError, match='Invalid county contact link'):
        directory.validate_supplement(supplement, preview=True)


@pytest.mark.parametrize('stage', ['projection', 'replacement'])
def test_unsafe_links_stop_before_review_packet_creation(stage, monkeypatch):
    row = dict(label='Contact', lines=['Published value'], href='javascript:alert(1)')
    if stage == 'projection':
        displayed = dict(office=[row], assistant=[])
        monkeypatch.setattr(workflow, 'format_contacts', lambda *args: copy.deepcopy(displayed))
        call = lambda: workflow.contacts(dict(id='fixture-person', name='Fixture Person', details={}))
    else:
        formats = dict(contact_replacements={'fixture-person': [dict(
            side='office', before=[dict(label='Contact', lines=['Old value'])],
            after=[row], reason='Fixture replacement.')]})
        monkeypatch.setattr(workflow, 'load_formats', lambda: formats)
        call = lambda: workflow.contact_replacements('fixture-person')
    with pytest.raises(ValueError, match='Invalid county contact link'):
        call()
