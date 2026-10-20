import importlib.util
import json
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('flcourts_form', Path(__file__).parents[1] / 'scripts/flcourts_article.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
URL = 'https://www.flcourts.gov/Services/family-law-forms/example'


def record(**overrides):
    data = {'_contentInfo': {'contentType': {'identifier': 'form'}},
            'name': 'Designation of Current Address', 'number': '12.915', 'date': '08/2023',
            'filePdf': {'uri': '/content/download/685859/7661591?version=4',
                        'fileName': '915 8.25.23.pdf', 'mimeType': 'application/pdf'}}
    data.update(overrides)
    return '<nav>Wrong form 99.999, date 2026</nav><script id="__NEXT_DATA__" type="application/json">' + json.dumps({'props': {'pageProps': {'pageData': data}}}) + '</script>'


def test_shell_form_uses_embedded_record_and_preserves_version_and_date_precision():
    result = module.extract_form(record(), URL)
    assert result['number'] == '12.915'
    assert result['stated_date'] == '08/2023'
    assert result['pdf_url'] == 'https://www.flcourts.gov/content/download/685859/7661591?version=4'
    assert result['pdf_filename'] == '915 8.25.23.pdf'
    assert '2026' not in str(result)


@pytest.mark.parametrize('html', ['<p>Shell only</p>', record()*2,
    record(number=None), record(date=''), record(filePdf=None),
    record(_contentInfo={'contentType': {'identifier': 'article'}}),
    '<script id="__NEXT_DATA__" type="application/json">bad json</script>'])
def test_changed_or_missing_form_record_is_not_a_success(html):
    with pytest.raises(ValueError): module.extract_form(html, URL)


@pytest.mark.parametrize('uri', ['https://example.com/form.pdf', '//example.com/form.pdf',
    'javascript:alert(1)', '/unrelated/file.pdf', '/content/download/1/2#fragment',
    '/content/download/1/2\n', '/content/download/1\\2'])
def test_download_must_match_observed_official_relative_endpoint(uri):
    with pytest.raises(ValueError):
        module.extract_form(record(filePdf={'uri': uri, 'fileName': 'form.pdf', 'mimeType': 'application/pdf'}), URL)


def test_non_pdf_metadata_is_rejected():
    with pytest.raises(ValueError):
        module.extract_form(record(filePdf={'uri': '/content/download/1/2', 'fileName': 'form.docx', 'mimeType': 'application/msword'}), URL)


@pytest.mark.parametrize('url', ['https://example.com', 'http://www.flcourts.gov', 'https://www.flcourts.gov@evil.example', 'https://www.flcourts.gov:444/'])
def test_unexpected_source_origin_is_rejected(url):
    with pytest.raises(ValueError): module.extract_form(record(), url)
