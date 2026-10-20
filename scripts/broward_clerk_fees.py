"""Extract an inspected Broward fee table without inferring payable totals."""
from collections import Counter
import re

from bs4 import BeautifulSoup


def extract_fees(html: bytes, expected_counts: dict[str, int]) -> list[dict]:
    """Require known headings/counts; changed source structure needs review.

    Amounts remain decimal strings. Repeated charges in different sections are
    preserved. The returned exact row quote can be cited against retained text.
    This does not validate legal fees, combine charges, or fetch any links.
    """
    if not expected_counts or any(not k or type(v) is not int or v < 1 for k, v in expected_counts.items()):
        raise ValueError('Supply reviewed section headings and positive row counts')
    soup = BeautifulSoup(html, 'html.parser')
    panels = soup.select('#FilingFees')
    if len(panels) != 1 or len(panels[0].find_all('table')) != 1:
        raise ValueError('Expected one FilingFees panel and one fee table')
    rows = panels[0].find('table').find_all('tr')
    result = []
    seen = set()
    section = None
    for index, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        if any(c.name != 'td' or c.get('rowspan', '1') != '1' for c in cells):
            raise ValueError('Unexpected header or row-spanning fee cell')
        if len(cells) == 1:
            text = cells[0].get_text(' ', strip=True)
            if cells[0].get('colspan') != '2':
                raise ValueError('Expected two-column payment/section row')
            if index == 0:
                if not text.startswith('Valid Forms of Payment'):
                    raise ValueError('Expected payment instructions before sections')
                continue
            if text not in expected_counts or text in seen:
                raise ValueError('Unknown or repeated fee section')
            section = text
            seen.add(text)
            continue
        if index == 0 or section is None or len(cells) != 2:
            raise ValueError('Fee row outside a section or unexpected cell count')
        if any(c.get('colspan', '1') != '1' for c in cells):
            raise ValueError('Unexpected merged fee row')
        label, amount = (c.get_text(' ', strip=True) for c in cells)
        if not label or not re.fullmatch(r'\$(?:\d+|\d{1,3}(?:,\d{3})+)\.\d{2}', amount):
            raise ValueError('Missing label or unrecognized fee amount')
        result.append({
            'section': section,
            'label': label,
            'amount_usd': amount[1:].replace(',', ''),
            'row_index': index,
            'quote': row.get_text('\n', strip=True).replace('\r\n', '\n').replace('\r', '\n'),
        })
    if Counter(r['section'] for r in result) != Counter(expected_counts):
        raise ValueError('Fee section counts changed; inspect source before updating expectations')
    return result
