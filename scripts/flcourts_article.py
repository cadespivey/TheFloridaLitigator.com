"""Extract an FL Courts article from retained Next.js HTML without executing scripts."""
import argparse
import json
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup


def extract_article(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", id="__NEXT_DATA__")
    if len(scripts) != 1 or scripts[0].get("type") != "application/json":
        raise ValueError("Expected one __NEXT_DATA__ JSON script")
    try:
        data = json.loads(scripts[0].get_text())["props"]["pageProps"]["pageData"]
        title = data["title"]
        body = data["body"]["html5"]
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError("Unsupported article data structure") from exc
    if not isinstance(title, str) or not title.strip() or not isinstance(body, str):
        raise ValueError("Article title and HTML body must be strings")
    content = BeautifulSoup(body, "html.parser")
    for node in content(["script", "style"]):
        node.decompose()
    text = content.get_text("\n", strip=True)
    if not text.strip():
        raise ValueError("Article body has no text")
    return {"title": title, "text": text,
            "json_path": "__NEXT_DATA__.props.pageProps.pageData.body.html5"}


def extract_form(html, page_url):
    """Read an observed FL Courts form record; never execute page JavaScript.

    Preserve the source's month/year string and versioned relative download URI.
    This extracts metadata only, not the contents or freshness of the PDF.
    """
    base = urlsplit(page_url)
    if base.scheme != 'https' or base.hostname != 'www.flcourts.gov' or base.username or base.password or base.port not in (None, 443):
        raise ValueError('Expected an official HTTPS Florida Courts page URL')
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', id='__NEXT_DATA__')
    if len(scripts) != 1 or scripts[0].get('type') != 'application/json':
        raise ValueError('Expected one __NEXT_DATA__ JSON script')
    try:
        data = json.loads(scripts[0].get_text())['props']['pageProps']['pageData']
        if data['_contentInfo']['contentType']['identifier'] != 'form':
            raise ValueError('Expected form content type')
        title, number, date, pdf = data['name'], data['number'], data['date'], data['filePdf']
        uri, filename = pdf['uri'], pdf['fileName']
        if not all(isinstance(v, str) and v.strip() for v in [title, number, date, uri, filename]):
            raise ValueError('Form metadata fields must be nonempty strings')
        parts = urlsplit(uri)
        if pdf['mimeType'] != 'application/pdf' or parts.scheme or parts.netloc or not parts.path.startswith('/content/download/') or parts.fragment or '\\' in uri or any(ord(c) < 32 for c in uri):
            raise ValueError('Unsupported PDF download metadata')
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('Unsupported form data structure') from exc
    return {'title': title, 'number': number, 'stated_date': date,
            'pdf_filename': filename, 'pdf_uri': uri, 'pdf_url': urljoin(page_url, uri),
            'json_path': '__NEXT_DATA__.props.pageProps.pageData'}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(extract_article(args.html.read_bytes()), indent=2))
    except ValueError as exc:
        parser.error(str(exc))
