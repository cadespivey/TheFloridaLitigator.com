"""Extract published Broward clerk rows without inferring contact roles or hours."""
from bs4 import BeautifulSoup


def extract_directory(html):
    soup = BeautifulSoup(html, 'html.parser')
    panels = soup.select('#ClerkDirectory')
    if len(panels) != 1:
        raise ValueError('Expected one ClerkDirectory panel')
    tables = panels[0].find_all('table')
    if len(tables) != 1:
        raise ValueError('Expected one directory table')
    table = tables[0]
    headers = [' '.join(x.get_text(' ', strip=True).split()) for x in table.select('thead th')]
    if headers != ['Division, Address and Room Number', 'Hours of Operation and Phone Numbers']:
        raise ValueError('Unexpected directory headers')
    rows, names = [], set()
    for row in table.select('tbody > tr'):
        cells = row.find_all('td', recursive=False)
        if len(cells) != 2 or any(c.get('colspan') or c.get('rowspan') for c in cells):
            raise ValueError('Expected two unmerged cells')
        links = cells[0].select('a[href]')
        if not links:
            raise ValueError('Division link missing')
        name = ' '.join(links[0].get_text(' ', strip=True).split())
        if not name or name in names:
            raise ValueError('Missing or duplicate division name')
        names.add(name)
        values = [c.get_text('\n', strip=True).replace('\r\n', '\n').replace('\r', '\n') for c in cells]
        if not all(values):
            raise ValueError('Empty directory cell')
        rows.append({'division': name, 'original_href': links[0]['href'],
                     'address_text': values[0], 'hours_and_contact_text': values[1],
                     'quote': row.get_text('\n', strip=True).replace('\r\n', '\n').replace('\r', '\n')})
    if not rows:
        raise ValueError('Directory table has no rows')
    return rows
