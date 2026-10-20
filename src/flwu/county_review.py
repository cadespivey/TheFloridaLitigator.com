"""Read-only, capture-pinned county review export; never imports or finalizes.

The JSON is a lossless view of the latest observation of each entity through the
specified capture. HTML is a review aid, not a normalized production directory.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import sqlite3
from urllib.parse import urlsplit


PERSON_KINDS = {"county_judge_baseline", "county_officer_baseline", "judge", "magistrate"}
ADMIN_KINDS = {"county_clerk_baseline", "county_administration_baseline", "clerk"}
HASH = re.compile(r"[0-9a-f]{64}\Z")
CSS = """
*{box-sizing:border-box}body{font:16px/1.55 system-ui,sans-serif;color:#222;
margin:0 auto;padding:1.5rem;max-width:76rem}h1{font-size:1.8rem}h2{font-size:1.4rem}
a{color:#245582;overflow-wrap:anywhere}a:focus-visible,summary:focus-visible{
outline:3px solid #245582;outline-offset:3px}p,dd,td{overflow-wrap:anywhere}
table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;
padding:.65rem;border-bottom:1px solid #ccc}th{background:#f1f1ee}
dl{margin:.3rem 0}dt{font-weight:600}dd{margin:0 0 .6rem 1rem}
td dl dd{margin-left:0}.table-scroll{overflow-x:auto}summary{cursor:pointer;
font-weight:600;padding:.5rem 0}li{margin-bottom:.4rem}.muted{color:#555}
@media(max-width:40rem){body{padding:1rem}th,td{padding:.4rem}}
"""


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def references(value):
    if isinstance(value, dict):
        if {"sha256", "url", "retrieved_at"} <= value.keys():
            yield value
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def load_packet(conn, stream, through_capture):
    """Read within the caller's transaction; no implicit schema creation/migration."""
    if conn.execute("SELECT version FROM history_meta").fetchone()[0] != 1:
        raise ValueError("Unsupported history schema")
    stream_row = conn.execute("SELECT mode,scope FROM streams WHERE stream=?", (stream,)).fetchone()
    if not stream_row or stream_row[0] != "manual_research":
        raise ValueError("County review requires an existing manual research stream")
    scope = json.loads(stream_row[1])
    if scope.get("profile") != "county-baseline-v1" or not scope.get("county"):
        raise ValueError("Expected pinned county-baseline-v1 scope")
    capture = conn.execute("SELECT capture_id,recorded_at,payload FROM captures WHERE seq=? AND stream=?",
                           (through_capture, stream)).fetchone()
    if not capture:
        raise ValueError("Capture does not belong to the requested stream")
    rows = conn.execute("""
        SELECT o.entity_key,v.kind,v.version_id,v.facts,o.citations,
               c.seq,c.capture_id,c.recorded_at
        FROM finding_observations o JOIN finding_versions v USING(version_id)
        JOIN captures c ON c.seq=o.capture_seq
        WHERE c.stream=? AND c.seq<=? AND NOT EXISTS (
          SELECT 1 FROM finding_observations newer JOIN captures nc ON nc.seq=newer.capture_seq
          WHERE newer.entity_key=o.entity_key AND nc.stream=c.stream
            AND nc.seq>c.seq AND nc.seq<=?) ORDER BY o.entity_key
        """, (stream, through_capture, through_capture)).fetchall()
    entities = [dict(entity_key=r[0], kind=r[1], version_id=r[2], facts=json.loads(r[3]),
                     citations=json.loads(r[4]), observation=dict(capture_seq=r[5],
                     capture_id=r[6], recorded_at=r[7])) for r in rows]
    if not entities:
        raise ValueError("No saved findings at the requested checkpoint")
    # Retain exact facts/citations; no assignment inferred from an entity-key prefix.
    return dict(format_version=1, purpose="county_review_not_publication", scope=scope,
                stream=stream, through_capture=dict(seq=through_capture, capture_id=capture[0],
                recorded_at=capture[1], research_status=json.loads(capture[2])["status"]),
                counts=dict(Counter(e["kind"] for e in entities)), entities=entities)


def verified_artifacts(conn, packet):
    hashes = set()
    for ref in references(packet["entities"]):
        for field in ("sha256", "text_sha256"):
            if field in ref:
                digest = ref[field]
                if not isinstance(digest, str) or not HASH.fullmatch(digest):
                    raise ValueError("Invalid evidence hash")
                hashes.add(digest)
    blobs = {}
    for digest in sorted(hashes):
        row = conn.execute("SELECT bytes FROM artifacts WHERE sha256=?", (digest,)).fetchone()
        if row is None or sha256(row[0]).hexdigest() != digest:
            raise ValueError("Missing or corrupt evidence artifact: " + digest)
        blobs[digest] = row[0]
    return blobs


def label(key):
    return str(key).replace("_", " ").capitalize()


def web_link(value, title=None):
    try:
        parsed = urlsplit(value)
        safe = parsed.scheme in {"https", "http"} and parsed.netloc and not parsed.username and not parsed.password
    except ValueError:
        safe = False
    if safe:
        return '<a href="' + escape(value, quote=True) + '">' + escape(title or value) + '</a>'
    return escape(title or value)


def display(value):
    """Keep labels and nested qualifiers; never relabel division mail as JA mail."""
    if value is None:
        return '<span class="muted">Not established in this record</span>'
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, dict):
        return '<dl>' + ''.join('<dt>' + escape(label(k)) + '</dt><dd>' + display(v) + '</dd>'
                               for k, v in value.items()) + '</dl>'
    if isinstance(value, list):
        return '<ul>' + ''.join('<li>' + display(v) + '</li>' for v in value) + '</ul>' if value else 'None recorded'
    return web_link(str(value)) if str(value).startswith(('https://', 'http://')) else escape(str(value))


def contacts(facts):
    # Explicit legacy names only; historical_contact is deliberately excluded.
    result = {k: facts[k] for k in ("contact", "contacts", "current_contact") if k in facts}
    if not result and 'office_phone' in facts and 'electronic_contact' in facts and 'locations' in facts:
        result['office'] = {k: facts[k] for k in (
            'office_phone', 'mailing_address_lines', 'electronic_contact',
            'locations', 'location_scope_note') if k in facts}
    return result


def contact_display(facts):
    blocks = contacts(facts)
    if not blocks or all(v is None for v in blocks.values()):
        return display(None)
    parts = []
    for name, block in blocks.items():
        if len(blocks) > 1:
            parts.append('<p><strong>' + escape(label(name)) + '</strong></p>')
        if not isinstance(block, dict):
            parts.append(display(block))
            continue
        parts.append('<dl>')
        for key, value in block.items():
            parts.append('<dt>' + escape(label(key)) + '</dt><dd>')
            if key.endswith('address_lines') and isinstance(value, list):
                parts.append('<br>'.join(escape(str(line)) for line in value))
            else:
                parts.append(display(value))
            parts.append('</dd>')
        parts.append('</dl>')
    return ''.join(parts)


def page(title, content, *, index=False):
    nav = '<a href="index.html">County overview</a>' if not index else '<a href="packet.json">Complete structured packet</a>'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>' + escape(title) + '</title><style>' + CSS + '</style></head><body>'
            '<a href="#main">Skip to content</a><nav aria-label="Review packet">' + nav + '</nav>'
            '<main id="main"><h1>' + escape(title) + '</h1>' + content + '</main></body></html>')


def entity_filename(entity):
    # Stable opaque file identity avoids filesystem meaning in external keys.
    return 'entity-' + sha256(entity['entity_key'].encode()).hexdigest() + '.html'


def entity_page(entity):
    f = entity['facts']
    title = f.get('name') or entity['entity_key'].replace('-', ' ')
    content = '<p>Saved observation: ' + escape(entity['observation']['recorded_at']) + '. '
    content += 'Source revision and effective dates are listed separately below.</p>'
    if 'summary' in f:
        content += display(f['summary'])
    if contacts(f):
        content += '<h2>Published contacts</h2>' + contact_display(f)
    for key in ('assignment', 'dates', 'procedure_url', 'profile_url', 'checklist', 'procedure_checklist',
                'conflicts', 'additional_field_states', 'contact_field_states', 'limitations', 'evidence_limitations'):
        if key in f:
            content += '<h2>' + escape(label(key)) + '</h2>' + display(f[key])
    shown = {'summary', 'contact', 'contacts', 'current_contact', 'assignment', 'dates', 'procedure_url',
             'profile_url', 'checklist', 'procedure_checklist', 'conflicts', 'additional_field_states',
             'contact_field_states', 'limitations', 'evidence_limitations'}
    other = {k: v for k, v in f.items() if k not in shown}
    content += '<details><summary>Other saved findings and review scope</summary>' + display(other) + '</details>'
    refs = {}
    for ref in references(entity):
        identity = (ref['url'], ref['sha256'], ref['retrieved_at'])
        refs.setdefault(identity, ref)
    content += '<details><summary>Source documents and retrieval dates</summary><ul>'
    for (url, digest, retrieved), ref in sorted(refs.items()):
        extension = Path(urlsplit(url).path).suffix.lower()
        if extension not in {'.pdf', '.html', '.doc', '.docx', '.txt', '.json'}:
            extension = '.html'
        content += ('<li>' + web_link(url, 'Official source') + ' · retrieved ' + escape(retrieved)
                    + ' · <a href="artifacts/' + digest + '.bin" download="' + digest + extension
                    + '">Saved original</a></li>')
    content += '</ul></details>'
    return page(str(title), content)


def index_page(packet):
    county = packet['scope']['county'].title()
    content = ('<p>County review packet. These findings were observed at their recorded retrieval times; '
               'they are not a finalized update or a certification that every contact is current. '
               'Documented conflicts remain separate source statements.</p><p>Through capture '
               + str(packet['through_capture']['seq']) + ' · '
               + escape(packet['through_capture']['recorded_at']) + '</p>')
    groups = [('Judges and judicial officers', lambda e: e['kind'] in PERSON_KINDS),
              ('Clerk and court administration', lambda e: e['kind'] in ADMIN_KINDS),
              ('Shared procedures and source reconciliation', lambda e: e['kind'] not in PERSON_KINDS | ADMIN_KINDS)]
    for heading, predicate in groups:
        members = sorted((e for e in packet['entities'] if predicate(e)), key=lambda e: e['facts'].get('name', e['entity_key']))
        content += '<h2>' + heading + '</h2><p>' + str(len(members)) + ' saved records.</p>'
        content += '<div class="table-scroll" role="region" aria-label="' + heading + '" tabindex="0"><table>'
        content += '<caption>' + heading + '</caption><thead><tr><th scope="col">Name / record</th><th scope="col">Assignment / review scope</th><th scope="col">Contacts / evidence state</th></tr></thead><tbody>'
        for e in members:
            f = e['facts']
            name = f.get('name') or e['entity_key'].replace('-', ' ')
            state = f.get('status') or f.get('review_status')
            description = f.get('assignment', f.get('scope', f.get('summary')))
            content += '<tr><th scope="row"><a href="' + entity_filename(e) + '">' + escape(str(name)) + '</a></th><td>' + display(description) + '</td><td>'
            # The full attributed block is on the entity page. This compact list
            # never promotes ancillary clerk/interpreter numbers into chambers.
            blocks = contacts(f)
            if e['kind'] in PERSON_KINDS and not any(isinstance(b, dict) for b in blocks.values()):
                content += '<p>Individual contacts not established; see documented gaps.</p>'
            for block in blocks.values():
                if isinstance(block, dict):
                    compact = {k: v for k, v in block.items() if k in {
                        'phone', 'assistant_name', 'judicial_assistant', 'assistant_role',
                        'assistant_email', 'division_email', 'address_lines',
                        'office_phone', 'mailing_address_lines'}}
                    content += contact_display({'contact': compact})
            if state:
                content += '<p>Saved review state: ' + escape(str(state)) + '</p>'
            content += '</td></tr>'
        content += '</tbody></table></div>'
    return page(county + ' county review', content, index=True)


def export_review(database, stream, through_capture, output):
    """Validate before writing; refuse existing destinations and all DB writes."""
    output = Path(output)
    if output.exists():
        raise ValueError('Output already exists; choose a new review directory')
    uri = Path(database).expanduser().resolve().as_uri() + '?mode=ro'
    with closing(sqlite3.connect(uri, uri=True)) as conn:
        conn.execute('PRAGMA query_only=ON')
        conn.execute('BEGIN')
        packet = load_packet(conn, stream, through_capture)
        blobs = verified_artifacts(conn, packet)
    files = {'packet.json': encode(packet).encode(), 'index.html': index_page(packet).encode()}
    files.update({entity_filename(e): entity_page(e).encode() for e in packet['entities']})
    output.mkdir(parents=True)
    (output / 'artifacts').mkdir()
    for name, data in files.items():
        (output / name).write_bytes(data)
    for digest, data in blobs.items():
        (output / 'artifacts' / (digest + '.bin')).write_bytes(data)
    manifest = dict(format_version=1, stream=stream, through_capture=packet['through_capture'],
                    entities=len(packet['entities']), counts=packet['counts'], artifacts=len(blobs),
                    files={name: sha256(data).hexdigest() for name, data in sorted(files.items())},
                    artifact_hashes=sorted(blobs), publication_status='not_published',
                    normalization_status='source_fields_preserved_not_production_directory')
    (output / 'manifest.json').write_text(encode(manifest))
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--stream', required=True)
    parser.add_argument('--through-capture', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = export_review(args.database, args.stream, args.through_capture, args.output)
    print(encode({k: v for k, v in result.items() if k not in {'files', 'artifact_hashes'}}), end='')


if __name__ == '__main__':
    main()
