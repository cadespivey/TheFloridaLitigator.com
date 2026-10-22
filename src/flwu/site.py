"""Deterministic static archive; public builds read only reviewed public exports."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from datetime import datetime
from html import escape
from flwu.publication import validate_issue, safe_url
from flwu.directory_display import format_contacts, load_formats
from flwu.county_directory import load_supplements

ASSETS = Path(__file__).parent / 'data' / 'web'

def social_metadata(page):
    """Crawler-readable metadata; no JavaScript or authentication required."""
    paths = {'updates': '', 'directory': 'directory.html', 'about': 'about.html'}
    titles = {'updates': 'The Florida Litigator',
              'directory': 'Court Personnel Directory — The Florida Litigator',
              'about': 'About — The Florida Litigator'}
    descriptions = {
        'updates': 'Weekly Florida law and procedure updates for civil litigators: statutes, case law, court rules, and judicial contacts, with links to public sources.',
        'directory': 'Find Florida court personnel, chambers contacts, judicial assistants, and official judicial procedures.',
        'about': 'Learn about The Florida Litigator, its public research sources, weekly updates, and focus on Florida commercial civil litigation.'}
    url = 'https://thefloridalitigator.com/' + paths[page]
    image = 'https://thefloridalitigator.com/assets/social-preview.png'
    tags = [('og:type', 'website'), ('og:site_name', 'The Florida Litigator'),
            ('og:title', titles[page]), ('og:description', descriptions[page]),
            ('og:url', url), ('og:image', image), ('og:image:type', 'image/png'),
            ('og:image:width', '1200'), ('og:image:height', '630'),
            ('og:image:alt', 'The Florida Litigator — Florida law and procedure updates for civil litigators')]
    html = '<link rel="canonical" href="' + url + '">\n'
    html += '\n'.join('<meta property="'+key+'" content="'+escape(value, quote=True)+'">' for key, value in tags)
    html += '\n<meta name="twitter:card" content="summary_large_image">'
    for key, value in [('title', titles[page]), ('description', descriptions[page]), ('image', image)]:
        html += '\n<meta name="twitter:'+key+'" content="'+escape(value, quote=True)+'">'
    return html + '\n'


# Exact user-supplied notice, shown only in the main (updates) page footer.
HOMEPAGE_DISCLAIMER = ('<p>' + 'The information presented on TheFloridaLitigator.com is provided for informational purposes only. It is not intended as legal advice and does not form an attorney-client or representative relationship. Information presented on the site is aggregated using web search tools, autonomous AI agents, personal research, public databases, and other publically available information, which may or may not be accurate at the time it was collected or published. These systems are updated by people and aggregated using AI tools, both of which may make mistakes. When possible, source links are provided for verification purposes, and users are strongly encouraged to consult the provided sources and their attorney before relying on this information.' + '</p>')


QUICK_SEARCH = '<form class="quick-search" role="search" action="./"><label for="site-query">Search updates and personnel</label><div><input id="site-query" type="search" name="q" placeholder="Keyword, judge, or county" required maxlength="200"><button type="submit">Search</button></div></form>'


def navigation(page, *, courts=None, extra_groups=()):
    """Official destinations from registry scope and explicit county supplements."""
    groups = {row['group_id'] for row in json.loads((ASSETS.parent / 'sources.json').read_text())}
    groups.update(extra_groups)
    sections, personnel = {}, {}
    for row in courts if courts is not None else json.loads((ASSETS / 'courts.json').read_text()):
        if row['group_id'] in groups:
            url = escape(safe_url(row['url']), quote=True)
            label = escape(row['label'])
            resources = ''.join(
                f'<li><a href="{escape(safe_url(link["url"]), quote=True)}" '
                f'aria-label="{label}: {escape(link["label"], quote=True)}">{escape(link["label"])}</a></li>'
                for link in row.get('resources', []) if link['label'] in {'Official Records', 'Court Records', 'Tax Assessor'}
            )
            children = f'<ul class="county-resources">{resources}</ul>' if resources else ''
            entry = (f'<li><details class="county-menu"><summary>{label}</summary><a href="{url}">Court website</a>{children}</details></li>' if row['category'] == 'County Courts' else f'<li><a href="{url}">{label}</a>{children}</li>')
            sections.setdefault(row['category'], []).append((row['label'], entry))
            court = escape(row['group_id'], quote=True)
            personnel.setdefault(row['category'], []).append((row['label'], f'<li><a data-court="{court}" href="directory.html?court={court}">{label}</a></li>'))
    def panel(items):
        parts = []
        for title, entries in items.items():
            if title in {'Circuit Courts', 'District Courts of Appeal'}:
                ordinals = ('first second third fourth fifth sixth seventh eighth ninth tenth '
                            'eleventh twelfth thirteenth fourteenth fifteenth sixteenth '
                            'seventeenth eighteenth nineteenth twentieth').split()
                ranks = {word: number for number, word in enumerate(ordinals, 1)}
                entries = sorted(entries, key=lambda entry: (ranks.get(entry[0].split()[0].lower(), 999), entry[0]))
            else:
                entries = sorted(entries)
            if title == 'County Courts':
                ranges = [('A–F', 'A', 'F'), ('G–L', 'G', 'L'), ('M–R', 'M', 'R'), ('S–Z', 'S', 'Z')]
                groups = ''.join(f'<li><details><summary>{name}</summary><ul>{"".join(link for label, link in entries if first <= label[0].upper() <= last)}</ul></details></li>' for name, first, last in ranges if any(first <= label[0].upper() <= last for label, _ in entries))
                parts.append(f'<details class="county-section"><summary>County Courts</summary><ul>{groups}</ul></details>')
            else:
                parts.append(f'<details class="court-section"><summary>{escape(title)}</summary><ul>{"".join(link for _, link in entries)}</ul></details>')
        return ''.join(parts)
    resources = ''.join(
        f'<li><a href="{escape(safe_url(link["url"]), quote=True)}">{escape(link["label"])}</a></li>'
        for link in json.loads((ASSETS / 'links.json').read_text())
    )
    current = ' aria-current="page"'
    return ('<nav class="site-nav" aria-label="Main navigation">'
            f'<a id="updates-link" href="./"{current if page == "updates" else ""}>Updates</a>'
            '<details class="court-menu"><summary>Courts</summary>'
            f'<div class="court-links">{panel(sections)}</div></details>'
            '<details class="personnel-menu"><summary>Personnel Directory</summary>'
            f'<div class="court-links"><a id="directory-link" href="directory.html"{current if page == "directory" else ""}>All covered courts</a>{panel(personnel)}</div></details>'
            '<details class="resources-menu"><summary>Links</summary>'
            f'<div class="court-links"><ul class="resource-links">{resources}</ul></div></details>'
            f'<a id="about-link" href="about.html"{current if page == "about" else ""}>About</a></nav>')



def build_site(archive, output, *, preview=False, county_directories=()):
    archive, output = Path(archive).resolve(), Path(output).resolve()
    if not archive.is_dir():
        raise ValueError('Public archive directory does not exist')
    if output == archive or output in archive.parents or archive in output.parents:
        raise ValueError('Build output and source archive must be separate')
    if output.exists():
        raise ValueError('Use a new output directory; existing builds are preserved')
    supplements = load_supplements(county_directories, preview=preview)
    courts = json.loads((ASSETS / 'courts.json').read_text())
    court_map = {court['group_id']: court for court in courts}
    extra_groups = set()
    for supplement in supplements:
        for court in supplement['courts']:
            group = court['group_id']
            if group in court_map and court_map[group] != court:
                raise ValueError('County navigation conflicts with an existing court group')
            if group not in court_map:
                courts.append(court)
                court_map[group] = court
            extra_groups.add(group)
    issues, evidence = [], {}
    contact_formats = load_formats()
    for path in sorted(archive.glob('*.json')):
        if path.is_symlink():
            raise ValueError('Archive symlinks are not permitted')
        issue = validate_issue(json.loads(path.read_text(encoding='utf-8')), preview=preview)
        if any(i['id'] == issue['id'] for i in issues):
            raise ValueError('Duplicate public issue ID')
        issues.append(issue)
        for record in [p for s in issue['sections'].values() for p in s['items']] + issue['directory']:
            for citation in record['citations']:
                relative = citation['url']
                if relative.startswith('evidence/'):
                    source = archive / relative
                    if (archive / 'evidence').is_symlink() or source.resolve().parent != (archive / 'evidence').resolve() or source.is_symlink():
                        raise ValueError('Invalid preview evidence path')
                    content = source.read_bytes()
                    if hashlib.sha256(content).hexdigest() != source.stem:
                        raise ValueError('Preview evidence checksum mismatch')
                    evidence[relative] = content
    issues.sort(key=lambda i: (i['window_end'], i['window_start'], datetime.fromisoformat(i['published_at'].replace('Z', '+00:00')), i['id']), reverse=True)
    for supplement in supplements:
        new_people = {person['id']: person for person in supplement['people']}
        for person in supplement['people']:
            legacy_id = person.get('legacy_person_id')
            if legacy_id:
                matches = [old for issue in issues for old in issue['directory'] if old['id'] == legacy_id]
                if not matches or any(old['name'] != person['name'] or supplement['county'] not in old['counties'] for old in matches):
                    raise ValueError('Invalid county-scoped legacy identity mapping')
                if legacy_id in new_people:
                    raise ValueError('Duplicate county-scoped legacy identity mapping')
                new_people[legacy_id] = person
        for issue in issues:
            for person in issue['directory']:
                if person['id'] in new_people and (
                    (supplement['court_scope'] not in person.get('court_ids', []) or person['name'] != new_people[person['id']]['name']
                     if supplement['schema_version'] == 2 else supplement['county'] not in person['counties'])
                    or (len(person['counties']) > 1 and person['name'] != new_people[person['id']]['name'])
                ):
                    raise ValueError('County supplement would replace personnel from another county')
    directory_contacts = {issue['id']: {person['id']: format_contacts(person, contact_formats)
                                      for person in issue['directory']} for issue in issues}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.flwu-site-', dir=output.parent) as staging:
        root = Path(staging) / 'site'
        (root / 'assets').mkdir(parents=True)
        asset_names = ('site.css', 'search.js', 'florida-litigator-logo.png', 'favicon.svg',
                       'favicon-16x16.png', 'favicon-32x32.png',
                       'apple-touch-icon.png', 'icon-192.png', 'icon-512.png',
                       'site.webmanifest', 'cade-spivey.jpg', 'social-preview.png')
        for name in asset_names:
            shutil.copyfile(ASSETS / name, root / 'assets' / name)
        data = json.dumps({'preview': preview, 'issues': issues, 'directory_contacts': directory_contacts,
                           'courts': courts, 'county_directories': supplements}, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('&', '\\u0026')
        data_name = 'archive-' + hashlib.sha256(data.encode('utf-8')).hexdigest()[:16] + '.json'
        (root / 'assets' / data_name).write_text(data, encoding='utf-8')
        # Stable recovery pointer for cached HTML whose hashed archive was retired.
        (root / 'assets' / 'current-archive.json').write_text(
            json.dumps({'archive': data_name}), encoding='utf-8')
        def version_assets(html):
            for name in asset_names:
                version = hashlib.sha256((ASSETS / name).read_bytes()).hexdigest()[:12]
                html = html.replace('assets/'+name, 'assets/'+name+'?v='+version)
            return html
        template = version_assets((ASSETS / 'index.html').read_text(encoding='utf-8')).replace('<!--ARCHIVE-URL-->', 'assets/' + data_name).replace('<!--QUICK-SEARCH-->', QUICK_SEARCH)
        for page, filename in [('updates', 'index.html'), ('directory', 'directory.html')]:
            html = template.replace('<!--NAVIGATION-->', navigation(page, courts=courts, extra_groups=extra_groups)).replace('data-page="updates"', f'data-page="{page}"')
            if page == 'directory':
                html = html.replace('<title>The Florida Litigator</title>', '<title>Court Personnel Directory — The Florida Litigator</title>')
                html = html.replace('<!--PAGE-TITLE-->', '<h2 class="page-title">Personnel Directory</h2>')
                html = html.replace('In Florida’s legal system, justice is shaped by judges, who apply the law, and court personnel, who oversee its administration. These are their updates... <em>Dun-dun.</em>', 'Court contacts and judicial assistants.')
            html = html.replace('<!--HOMEPAGE-DISCLAIMER-->', HOMEPAGE_DISCLAIMER if page == 'updates' else '')
            html = html.replace('</head>', social_metadata(page) + '</head>')
            (root / filename).write_text(html.replace('<!--PAGE-TITLE-->', ''), encoding='utf-8')
        about = version_assets((ASSETS / 'about.html').read_text(encoding='utf-8')).replace('<!--NAVIGATION-->', navigation('about', courts=courts, extra_groups=extra_groups)).replace('<!--QUICK-SEARCH-->', QUICK_SEARCH)
        about = about.replace('</head>', social_metadata('about') + '</head>')
        (root / 'about.html').write_text(about, encoding='utf-8')
        (root / '.nojekyll').touch()
        for relative, content in evidence.items():
            target = root / relative
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(content)
        (root / 'procedures').mkdir()
        (root / 'procedures' / 'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../directory.html"><title>Judicial directory</title><a href="../directory.html">Open the judicial directory</a></html>', encoding='utf-8')
        root.rename(output)
    return output


def generate_site(issue, inventory_rows, output_dir):
    """Legacy callers must now supply a complete public export."""
    validate_issue(issue, preview=issue.get('synthetic', False))
    if inventory_rows:
        raise ValueError('Put reviewed directory entries in the public issue export')
    with tempfile.TemporaryDirectory() as temporary:
        archive = Path(temporary)
        (archive / 'issue.json').write_text(json.dumps(issue), encoding='utf-8')
        return build_site(archive, Path(output_dir) / 'public', preview=issue['synthetic'])


def _site_css():
    return (ASSETS / 'site.css').read_text(encoding='utf-8')


def _search_js():
    return (ASSETS / 'search.js').read_text(encoding='utf-8')
