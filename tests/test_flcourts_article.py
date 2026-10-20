import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("flcourts_article", Path(__file__).parents[1] / "scripts/flcourts_article.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(body, title="Appointment"):
    data = {"props": {"pageProps": {"pageData": {"title": title, "body": {"html5": body}}}}}
    encoded = json.dumps(data).replace('<', '\\u003c')
    return '<nav>Unrelated December 2020 date</nav><script id="__NEXT_DATA__" type="application/json">' + encoded + '</script>'


def test_article_not_navigation_or_executable_script():
    result = module.extract_article(fixture('<p>Effective <b>December 1, 2026</b>.</p><script>throw "bad"</script><style>ignored</style><p>A &amp; B</p>'))
    assert result['text'] == 'Effective\nDecember 1, 2026\n.\nA & B'
    assert result['title'] == 'Appointment'
    assert '2020' not in result['text'] and 'throw' not in result['text']


@pytest.mark.parametrize('html', [
    '<p>Shell only</p>',
    '<script id="__NEXT_DATA__" type="application/json">not json</script>',
    '<script id="__NEXT_DATA__" type="application/json">{"props":{}}</script>',
    fixture('<p>Valid</p>') * 2,
    fixture('<p>Valid</p>', title=None),
    fixture({'html': 'unsupported'}),
    fixture('<script>not content</script>'),
])
def test_missing_or_changed_structure_fails_closed(html):
    with pytest.raises(ValueError):
        module.extract_article(html)
