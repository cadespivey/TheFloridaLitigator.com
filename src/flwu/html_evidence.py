"""Read court HTML and embedded presentation data without executing JavaScript."""
import json
from urllib.parse import urldefrag, urljoin

from bs4 import BeautifulSoup


def extract_html(raw, base_url):
    blocks, links, seen = [], set(), set()

    def add(text):
        if text.strip() and text not in seen:
            seen.add(text); blocks.append(text)

    def link(value):
        if isinstance(value, str):
            absolute = urldefrag(urljoin(base_url, value))[0]
            if absolute.startswith(('https://', 'http://')):
                links.add(absolute)

    def walk(value, path, depth):
        if depth > 32:
            raise ValueError('Embedded presentation nesting exceeds limit')
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'html5':
                    if not isinstance(child, str):
                        raise ValueError('Embedded HTML must be text')
                    fragment(child, path+'.html5', depth+1)
                elif key == 'content' and isinstance(child, str):
                    # Shared contact panels use content rather than an html5 wrapper.
                    fragment(child, path+'.content', depth+1)
                elif key in ('url', 'uri', 'href', 'downloadUrl', 'fileUrl'):
                    link(child)
                elif key in ('name', 'title', 'heading', 'description') and isinstance(child, str) and child.strip():
                    add(path+'.'+key+': '+child)
                elif isinstance(child, (dict, list)):
                    walk(child, path+'.'+key, depth+1)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path+'['+str(index)+']', depth+1)

    def fragment(html, path, depth):
        if depth > 32:
            raise ValueError('Embedded presentation nesting exceeds limit')
        soup = BeautifulSoup(html, 'html.parser')
        # FL Courts custom tags store rendered contents as entity-encoded JSON.
        for node in soup.select('[data-customtag][data-content]'):
            payload = json.loads(node['data-content'])
            if not isinstance(payload, dict) or not isinstance(payload.get('content'), str):
                raise ValueError('Unsupported court custom-tag content')
            fragment(payload['content'], path+'.data-content', depth+1)
            if node['data-customtag'] == 'calendarpreview':
                events = payload.get('events')
                if not isinstance(events, list) or any(not isinstance(event, dict) for event in events):
                    raise ValueError('Unsupported court calendar events')
                # Dates/timezones and attachment metadata are evidence too.
                # Preserve their literal values; never infer a date from a title.
                add(path+'.data-content.events: '+json.dumps(events, ensure_ascii=False, sort_keys=True))
                walk(events, path+'.data-content.events', depth+1)
        for node in soup.select('a[href]'):
            link(node['href'])
        for node in soup(['script', 'style']):
            node.decompose()
        text = soup.get_text('\n', strip=True)
        if text:
            add(path+'\n'+text if path else text)

    document = BeautifulSoup(raw, 'html.parser')
    nodes = document.find_all('script', id='__NEXT_DATA__')
    fragment(raw, '', 0)
    if nodes:
        if len(nodes) != 1:
            raise ValueError('Ambiguous Next.js presentation data')
        data = json.loads(nodes[0].get_text())['props']['pageProps']
        if not isinstance(data, dict):
            raise ValueError('Unsupported Next.js pageProps')
        # Directory indexes embed rendered child profiles outside pageData.
        # Keep these along with page/panel/menu content, excluding runtime config.
        for key in ('childrenInfos', 'pageData', 'extraData'):
            if key in data:
                walk(data[key], '$.props.pageProps.'+key, 0)
    return '\n\n'.join(blocks), sorted(links)
