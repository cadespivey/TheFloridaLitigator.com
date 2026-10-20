import html
import json
import pytest
from scripts.flcourts_folder import extract_folder


def page(body, kind='folder'):
    data = {'props': {'pageProps': {'pageData': {
        '_contentInfo': {'contentType': {'identifier': kind}},
        'name': 'Actual folder', 'description': {'html5': body}}}}}
    return '<nav>Unrelated navigation date 2099</nav><script id="__NEXT_DATA__" type="application/json">' + json.dumps(data).replace('<', '\\u003c') + '</script>'


def block(kind, content):
    return '<div data-customtag="' + kind + '" data-content="' + html.escape(json.dumps({'content': content}), quote=True) + '"></div>'


def test_preserves_folder_text_block_links_and_escaped_iframe_without_shell():
    result = extract_folder(page('<h2>Instructions</h2>' + block('contentblock', '<p>Read the notice. <a href="/actual?version=4">Guide</a></p>') + block('rawhtml', '<p>&lt;iframe src="https://www.youtube.com/embed/example"&gt;&lt;/iframe&gt;</p>') + '<script>secret()</script>'))
    assert result['title'] == 'Actual folder'
    assert 'Read the notice.' in result['text'] and 'Instructions' in result['text']
    assert '2099' not in result['text'] and 'secret' not in result['text']
    assert result['links'] == [{'label': 'Guide', 'href': '/actual?version=4'}]
    assert result['iframe_sources'] == ['https://www.youtube.com/embed/example']
    assert result['scope'].endswith('children and videos not fetched')


@pytest.mark.parametrize('source', [
    '<p>shell only</p>',
    page('<p>text</p>') + page('<p>duplicate</p>'),
    page('<p>text</p>', 'article'),
    page(''),
    page(block('unknown', 'text')),
    page('<div data-customtag="contentblock" data-content="invalid"></div>'),
    page(block('contentblock', 42)),
    page(block('contentblock', '<div data-customtag="rawhtml"></div>')),
])
def test_rejects_unsupported_or_incomplete_structures(source):
    with pytest.raises(ValueError):
        extract_folder(source)
