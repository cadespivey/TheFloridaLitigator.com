"""Read retained FL Courts folder descriptions; never execute embedded content."""
import html as html_module
import json
from bs4 import BeautifulSoup


def extract_folder(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all('script', id='__NEXT_DATA__')
    if len(nodes) != 1 or nodes[0].get('type') != 'application/json':
        raise ValueError('Expected one __NEXT_DATA__ JSON script')
    try:
        data = json.loads(nodes[0].get_text())['props']['pageProps']['pageData']
        if data['_contentInfo']['contentType']['identifier'] != 'folder':
            raise ValueError('Expected folder')
        title, description = data['name'], data['description']['html5']
        if not isinstance(title, str) or not title.strip() or not isinstance(description, str):
            raise ValueError('Expected folder name and HTML description')
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError('Unsupported folder metadata') from exc
    body = BeautifulSoup(description, 'html.parser')
    for node in list(body.select('[data-customtag]')):
        if node.get('data-customtag') not in {'contentblock', 'rawhtml', 'separator'}:
            raise ValueError('Unsupported folder custom tag')
        try:
            content = json.loads(node['data-content'])['content']
            if not isinstance(content, str):
                raise ValueError('Expected string content')
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError('Unsupported folder block') from exc
        # The observed rawhtml block stores an escaped iframe inside a paragraph.
        fragment = BeautifulSoup(html_module.unescape(content), 'html.parser')
        if fragment.select('[data-customtag]'):
            raise ValueError('Nested custom tags require separate review')
        node.replace_with(fragment)
    for node in body(['script', 'style']):
        node.decompose()
    links = [{'label': a.get_text(' ', strip=True), 'href': a['href']} for a in body.select('a[href]')]
    frames = [a['src'] for a in body.select('iframe[src]')]
    text = body.get_text('\n', strip=True)
    if not text:
        raise ValueError('Folder description has no text')
    return {'title': title, 'text': text, 'links': links, 'iframe_sources': frames,
            'json_path': '__NEXT_DATA__.props.pageProps.pageData.description.html5',
            'scope': 'Description and supported blocks only; children and videos not fetched'}
