import html
import json

import pytest
from flwu import source_gate as g
from flwu.html_evidence import extract_html


def page(body):
    return ('<p>Visible introduction</p><script id="__NEXT_DATA__" type="application/json">'+
            json.dumps({'props':{'pageProps':{'pageData':{'body':{'html5':'<p>Body</p>'}},
                'extraData':{'panels':[{'contentLeft':{'html5':body}}]}}}})+'</script>').encode()


def test_embedded_panels_custom_tags_and_links_survive_extraction():
    payload = html.escape(json.dumps({'content':'<p>Clerk: (850) 488-6151</p><a href="/orders/26-2.pdf">2027 Holidays</a>'}),quote=True)
    raw = page('<h2>Contact Information</h2><div data-customtag="responsive_column" data-content="'+payload+'"></div>')
    text, links = extract_html(raw, 'https://1dca.flcourts.gov/')
    assert all(x in text for x in ['Visible introduction','Body','Contact Information','Clerk: (850) 488-6151','2027 Holidays'])
    assert 'https://1dca.flcourts.gov/orders/26-2.pdf' in links
    assert 'data-content' in text  # locator for hidden presentation evidence
    assert raw == page('<h2>Contact Information</h2><div data-customtag="responsive_column" data-content="'+payload+'"></div>')


@pytest.mark.parametrize('raw', [page('<div data-customtag="responsive_column" data-content="invalid"></div>'),
    b'<p>Visible</p><script id="__NEXT_DATA__">invalid</script>'])
def test_malformed_embedded_content_is_unavailable_not_partial_success(raw):
    text, method, links = g.extract(raw, {'content_type':'text/html','resolved_url':'https://court.gov/'})
    assert (text,method,links) == ('','unavailable',[])


def test_plain_html_ignores_executable_script_and_unsafe_links():
    text,links=extract_html(b'<p>Office</p><script>SECRET</script><a href="javascript:evil()">Bad</a>', 'https://court.gov/')
    assert 'Office' in text and 'SECRET' not in text and not links


def test_directory_child_profiles_retain_chambers_staff_and_procedure_links():
    data = {'props': {'pageProps': {'childrenInfos': [{'props': {'content': {
        'name': 'Judge Example', 'fields': {
            'chambers_staff': {'html5': '<p>Alex Example, Judicial Assistant</p>'},
            'description': {'html5': '<a href="/civil-procedures.pdf">Civil procedures</a>'}
        }}}}], 'siteaccess': {'password': 'NOT PRESENTATION CONTENT'}}}}
    raw = ('<script id="__NEXT_DATA__">' + json.dumps(data) + '</script>').encode()
    text, links = extract_html(raw, 'https://court.gov/Judges')
    assert 'Judge Example' in text
    assert 'Alex Example, Judicial Assistant' in text
    assert 'Civil procedures' in text
    assert 'https://court.gov/civil-procedures.pdf' in links
    assert 'NOT PRESENTATION CONTENT' not in text


def test_contact_content_blocks_retain_details_not_only_heading():
    data = {'props': {'pageProps': {'extraData': {'contentBlocks': [{
        'heading': 'Contact Information',
        'content': '<p>2000 Drayton Drive<br>Clerk: (850) 488-6151</p><a href="/ada">ADA Information</a>'
    }]}}}}
    raw = ('<script id="__NEXT_DATA__">' + json.dumps(data) + '</script>').encode()
    text, links = extract_html(raw, 'https://court.gov/clerk')
    assert '2000 Drayton Drive' in text and 'Clerk: (850) 488-6151' in text
    assert 'https://court.gov/ada' in links


def test_calendar_events_preserve_dates_metadata_and_resolve_source_links():
    event = {'thisDate': {'date': '2026-11-10 14:30:00.000000', 'timezone': 'UTC'},
             'content': {'name': 'Session - 2026-10-11', 'url': '/calendar/session',
                         'fields': {'file': {'uri': '/downloads/calendar.pdf', 'fileSize': 40973}}}}
    def calendar(events):
        payload = html.escape(json.dumps({'content': '', 'events': events}), quote=True)
        return page('<div data-customtag="calendarpreview" data-content="'+payload+'"></div>')
    text, links = extract_html(calendar([event]), 'https://3dca.flcourts.gov/judges/bokor')
    assert '2026-11-10 14:30:00.000000' in text and 'UTC' in text
    assert 'Session - 2026-10-11' in text and '40973' in text
    assert 'https://3dca.flcourts.gov/downloads/calendar.pdf' in links
    assert 'https://3dca.flcourts.gov/calendar/session' in links
    event['content']['fields']['file']['fileSize'] = 42565
    changed, _ = extract_html(calendar([event]), 'https://3dca.flcourts.gov/judges/bokor')
    assert changed != text and '42565' in changed
    empty, _ = extract_html(calendar([]), 'https://3dca.flcourts.gov/')
    assert '.events: []' in empty


@pytest.mark.parametrize('events', [None, 'unavailable', [None]])
def test_malformed_calendar_is_not_silently_accepted(events):
    payload = html.escape(json.dumps({'content': '', 'events': events}), quote=True)
    raw = page('<div data-customtag="calendarpreview" data-content="'+payload+'"></div>')
    assert g.extract(raw, {'content_type': 'text/html', 'resolved_url': 'https://court.gov/'}) == ('', 'unavailable', [])
