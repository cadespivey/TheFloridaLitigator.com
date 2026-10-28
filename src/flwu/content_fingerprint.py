"""Versioned, conservative HTML content equivalence; no model classification.

Raw hashes remain authoritative observations. This profile proves only that a
source's reviewed core is equal and every shared widget has a completed review.
Unsupported documents and unknown differences retain ordinary source review.
"""
from __future__ import annotations

import copy
import base64
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Tag, NavigableString
from flwu import history as h

PROFILE = 'flcourts-content-v1'
HOSTS = frozenset(['supremecourt.flcourts.gov'] +
                  [f'{number}dca.flcourts.gov' for number in range(1, 7)])
WIDGETS = frozenset({'recent_opinions', 'calendarpreview'})
SENATE_PROFILE = 'flsenate-statutes-content-v1'
SUNSHINE_PROFILE = 'online-sunshine-statutes-content-v1'
PROFILES = (PROFILE, SENATE_PROFILE, SUNSHINE_PROFILE)
CF_PARAMETERS = re.compile(r"window\.__CF\$cv\$params=\{r:'([0-9a-f]{16})',t:'([A-Za-z0-9+/]+={0,2})'\}")


def _json(value):
    def unique(pairs):
        if len({key for key, _ in pairs}) != len(pairs):
            raise ValueError('Ambiguous duplicate JSON key')
        return dict(pairs)

    def constant(value):
        raise ValueError('Unsupported non-JSON constant')
    return json.loads(value, object_pairs_hook=unique, parse_constant=constant)


def profile_for(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https':
        return None
    if parsed.hostname in HOSTS:
        return PROFILE
    if parsed.hostname == 'www.flsenate.gov' and (
            parsed.path == '/Laws/Statutes' or parsed.path.startswith('/Laws/Statutes/')):
        return SENATE_PROFILE
    if parsed.hostname in {'www.leg.state.fl.us', 'leg.state.fl.us'} and (
            parsed.path.lower() == '/statutes' or parsed.path.lower().startswith('/statutes/')):
        return SUNSHINE_PROFILE
    return None


def _tree(raw):
    """Keep parent/child boundaries, which a flat inspection diff need not keep."""
    class Boundaries(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.duplicates = []

        def handle_starttag(self, tag, attrs):
            names = [key for key, _ in attrs]
            if len(names) != len(set(names)):
                # Parsers/browser recovery differ on duplicate attributes.
                # Retain their complete original spelling in the core as well.
                self.duplicates.append(self.get_starttag_text())

        handle_startendtag = handle_starttag

    def node(item, depth=0):
        if depth > 128:
            raise ValueError('HTML depth limit')
        if isinstance(item, Tag):
            return dict(tag=item.name, attrs=dict(item.attrs),
                        children=[node(child, depth + 1) for child in item.children])
        if isinstance(item, NavigableString):
            # Never JSON-decode visible quotations, ordinary attributes or JS.
            return dict(kind=type(item).__name__, value=str(item))
        raise ValueError('Unsupported HTML node')
    soup = BeautifulSoup(raw, 'html.parser')
    if soup.contains_replacement_characters:
        raise ValueError('Uncertain source encoding')
    boundaries = Boundaries()
    boundaries.feed(raw.decode(soup.original_encoding or 'utf-8') if isinstance(raw, bytes) else raw)
    result = node(soup)
    result['duplicate_attribute_tags'] = boundaries.duplicates
    return result


def _tags(node):
    if isinstance(node, dict) and 'tag' in node:
        yield node
        for child in node['children']:
            yield from _tags(child)


def policy_bytes():
    # Bind decisions to the actual implementation, not just a mutable label.
    return Path(__file__).read_bytes()


def eligible(observation):
    return bool(observation.get('success') and observation.get('sha256')
                and observation.get('text_sha256')
                and observation.get('content_type') == 'text/html'
                and profile_for(observation['url'])
                and urlsplit(observation.get('resolved_url') or observation['url']).hostname
                == urlsplit(observation['url']).hostname)


def _senate_metadata(nodes):
    metadata = []
    for node in nodes:
        attrs = node['attrs']
        if node['tag'] == 'input' and attrs.get('name') == '__RequestVerificationToken':
            value = attrs.get('value')
            if attrs.get('type') != 'hidden' or not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{108}', value):
                raise ValueError('Unknown request-verification field')
            metadata.append(dict(property='request_verification_token', value_sha256=h.sha(value.encode())))
            attrs['value'] = {'flwu_tracked_metadata': 'request_verification_token'}
        if node['tag'] != 'script':
            continue
        for child in node['children']:
            text = child.get('value')
            if not isinstance(text, str):
                continue
            def replace(match):
                ray, encoded = match.groups()
                decoded = base64.b64decode(encoded, validate=True)
                if (len(decoded) != 10 or not decoded.isdigit()
                        or base64.b64encode(decoded).decode() != encoded):
                    raise ValueError('Unknown Cloudflare request timestamp')
                metadata.append(dict(property='cloudflare_request_parameters',
                                     r_sha256=h.sha(ray.encode()), t_sha256=h.sha(encoded.encode())))
                return "window.__CF$cv$params={r:'FLWU_TRACKED_REQUEST_ID',t:'FLWU_TRACKED_REQUEST_TIME'}"
            child['value'] = CF_PARAMETERS.sub(replace, text)
    return metadata


def _sunshine_metadata(nodes):
    forms = [node for node in nodes if node['tag'] == 'form' and node['attrs'].get('id') == 'search_statutes']
    if len(forms) != 1 or forms[0]['attrs'].get('action') != '/statutes/index.cfm':
        raise ValueError('Unknown statute search header')
    rows = [node for node in _tags(forms[0]) if node['tag'] == 'tr' and node['attrs'].get('id') == 'datesearch']
    if len(rows) != 1:
        raise ValueError('Unknown statute date row')
    cells = [node for node in _tags(rows[0]) if node['tag'] == 'td' and node['attrs'].get('id') == 'date']
    if len(cells) != 1 or len(cells[0]['children']) != 1:
        raise ValueError('Ambiguous statute header date')
    leaf = cells[0]['children'][0]
    value = leaf.get('value')
    if not isinstance(value, str) or not re.fullmatch(r'\s*[A-Z][a-z]+ \d{1,2}, \d{4}\s*', value):
        raise ValueError('Unsupported statute header date')
    datetime.strptime(value.strip(), '%B %d, %Y')
    leaf['value'] = {'flwu_tracked_metadata': 'sunshine_display_date'}
    return [dict(property='sunshine_display_date', value=value)]


def fingerprint(raw, observation):
    """Keep all other nodes/attributes/scripts; separate two explicit widget types.

    This does not strip arbitrary timestamps, navigation, links, scripts or CSS.
    Each site profile tracks only explicit metadata fields. Court presentation
    must be recognized Next.js; legislative profiles retain their full HTML tree.
    """
    if not eligible(observation) or raw.startswith(b'%PDF-'):
        return None
    try:
        profile = profile_for(observation['url'])
        projected = _tree(raw)
        nodes = list(_tags(projected))
        court = urlsplit(observation['url']).hostname
        metadata, components = [], []
        if profile == SENATE_PROFILE:
            metadata = _senate_metadata(nodes)
        elif profile == SUNSHINE_PROFILE:
            metadata = _sunshine_metadata(nodes)
        if profile != PROFILE:
            policy = h.sha(policy_bytes())
            return dict(profile=profile, policy_sha256=policy, original_sha256=h.sha(raw), court=court,
                        core_sha256=h.sha(dict(profile=profile, policy_sha256=policy, court=court, nodes=projected)),
                        metadata=metadata, components=components)
        roots = [node for node in nodes
                 if node.get('tag') == 'script'
                 and node.get('attrs', {}).get('id') == '__NEXT_DATA__']
        if len(roots) != 1:
            return None
        root = roots[0]
        if len(root['children']) != 1:
            return None
        if root['attrs'].get('type') != 'application/json':
            return None
        data = _json(root['children'][0]['value'])
        root['children'][0]['value'] = data
        page = data['props']['pageProps']
        if not isinstance(page['pageData']['name'], str) or not page['pageData']['name'].strip():
            return None
        for node in nodes:
            if node.get('tag') == 'meta' and node.get('attrs', {}).get('property') == 'og:updated_time':
                value = node['attrs']['content']
                h.stamp(value)  # Malformed or ambiguous metadata falls back to review.
                metadata.append({'property': 'og:updated_time', 'value': value})
                node['attrs']['content'] = {'flwu_tracked_metadata': 'og:updated_time'}
        if len(metadata) > 1:
            return None

        def fragment(value, location):
            if not isinstance(value, str):
                raise ValueError('Unsupported presentation fragment')
            if not value.strip():
                return value
            found = []

            def project(item, depth=0):
                if depth > 64:
                    raise ValueError('Unresolved nested presentation')
                if isinstance(item, dict) and 'tag' in item:
                    result = copy.deepcopy(item)
                    attrs = result['attrs']
                    kind = attrs.get('data-customtag')
                    if isinstance(kind, str) and kind in WIDGETS:
                        payload = _json(attrs['data-content'])
                        if not isinstance(payload, dict):
                            raise ValueError('Unsupported shared widget')
                        if kind == 'recent_opinions' and not (
                            isinstance(payload.get('items'), dict)
                            and isinstance(payload.get('start_date'), str)
                            and isinstance(payload.get('end_date'), str)
                            and isinstance(payload.get('date_field'), str)):
                            raise ValueError('Unsupported opinion widget')
                        if kind == 'calendarpreview' and not (
                            isinstance(payload.get('events'), list)
                            and all(isinstance(event, dict) for event in payload['events'])):
                            raise ValueError('Unsupported calendar widget')
                        found.append(dict(court=court, kind=kind,
                                          sha256=h.sha(payload), location=location))
                        # Other widget attributes and all surrounding text stay in core.
                        result['attrs']['data-content'] = {'flwu_shared_component': kind}
                    elif kind == 'contentblock':
                        payload = _json(attrs['data-content'])
                        if not isinstance(payload, dict) or not isinstance(payload.get('content'), str):
                            raise ValueError('Unsupported component wrapper')
                        payload['content'] = project(_tree(payload['content']), depth + 1)
                        result['attrs']['data-content'] = payload
                    result['children'] = [project(child, depth + 1) for child in item['children']]
                    return result
                return item

            result = project(_tree(value))
            if not found:
                return value  # Do not canonicalize unrelated embedded HTML.
            components.extend(found)
            return result

        extra = page.get('extraData', {})
        if not isinstance(extra, dict):
            return None
        menu, blocks = extra.get('menu', []), extra.get('contentBlocks', [])
        if (not isinstance(menu, list) or not isinstance(blocks, list)
                or any(not isinstance(item, dict) for item in menu + blocks)):
            return None
        for index, item in enumerate(menu):
            display = item.get('menudisplay')
            if display not in (None, []) and not isinstance(display, dict):
                return None
            fields = display.get('fields') if isinstance(display, dict) else None
            if fields is not None and not isinstance(fields, dict):
                return None
            block = fields.get('right_block') if isinstance(fields, dict) else None
            if isinstance(block, dict) and 'html5' in block:
                block['html5'] = fragment(block['html5'], f'extraData.menu[{index}].right_block')
        for index, item in enumerate(blocks):
            if 'content' in item:
                item['content'] = fragment(item['content'], f'extraData.contentBlocks[{index}]')
        policy = h.sha(policy_bytes())
        return dict(profile=PROFILE, policy_sha256=policy,
                    original_sha256=h.sha(raw), court=court,
                    core_sha256=h.sha(dict(profile=PROFILE, policy_sha256=policy,
                                          court=court, nodes=projected)),
                    metadata=metadata, components=components)
    except (ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError, UnicodeError):
        return None


class ReviewIndex:
    """Reuse a source's own reviewed core and court/protocol-scoped components."""

    def __init__(self, observations, reviews, bases, protocol, load_blob):
        self.observations = {item['capture_id']: item for item in observations}
        self.load_blob = load_blob
        self.protocol = protocol
        self.cache = {}
        self.courts = {}
        latest = {(review['source_id'], review['observation_capture_id']): review
                  for review in reviews}
        self.reviews = []
        self.by_source = {}
        for review in latest.values():
            observed = self.observations.get(review['observation_capture_id'])
            if (review.get('acceptance_version') != 3 or review.get('review_protocol') != protocol
                    or not observed or not observed.get('success')
                    or observed['source_id'] != review['source_id']
                    or observed['sha256'] != review['sha256']
                    or (bases.get(review['observation_capture_id'])
                        and review.get('raw_review_verified') is not True)):
                continue
            self.reviews.append((review, observed))
            self.by_source.setdefault(review['source_id'], []).append((review, observed))

    def get(self, observation):
        if not eligible(observation):
            return None
        key = (observation['sha256'], observation['url'],
               observation.get('resolved_url'), observation.get('content_type'))
        if key not in self.cache:
            self.cache[key] = fingerprint(self.load_blob(observation['sha256']), observation)
        return self.cache[key]

    def reviewed_components(self, court):
        if court not in self.courts:
            known = {}
            for review, observed in self.reviews:
                if urlsplit(observed['url']).hostname != court:
                    continue
                value = self.get(observed)
                if value:
                    for component in value['components']:
                        known.setdefault((component['kind'], component['sha256']), dict(
                            source_id=review['source_id'],
                            observation_capture_id=review['observation_capture_id'],
                            raw_sha256=review['sha256'], receipt_sha256=review['receipt_sha256'],
                            component=component))
            self.courts[court] = known
        return self.courts[court]

    def reuse(self, current):
        value = self.get(current)
        if not value:
            return None
        # Never substitute another person's page for this source's full review.
        for review, previous in reversed(self.by_source.get(current['source_id'], [])):
            if (previous['url'] != current['url']
                    or (previous.get('resolved_url') or previous['url'])
                    != (current.get('resolved_url') or current['url'])):
                continue
            # A reading-aid upgrade is not a source change. Recompute both
            # fingerprints from verified originals; never trust derivative labels.
            basis = self.get(previous)
            if not basis or basis['core_sha256'] != value['core_sha256']:
                continue
            known = self.reviewed_components(value['court'])
            references = []
            for component in value['components']:
                completed = known.get((component['kind'], component['sha256']))
                if completed is None:
                    break
                references.append(dict(current_component=component, reviewed=completed))
            else:
                return dict(decision='content_hash_reuse', profile=value['profile'],
                            policy_sha256=value['policy_sha256'], review_protocol=self.protocol,
                            source_id=current['source_id'], url=current['url'],
                            observation_capture_id=current['capture_id'],
                            retrieved_at=current['retrieved_at'],
                            current_extraction=current.get('extraction'),
                            reviewed_extraction=previous.get('extraction'),
                            current_fingerprint=value, reviewed_fingerprint=basis,
                            reviewed_observation_capture_id=previous['capture_id'],
                            review_receipt=review['receipt_sha256'],
                            component_reviews=references)
        return None


def persist(conn, stream, reused):
    """Append machine provenance, never fabricate a human review or finding."""
    scope = {'profile': 'source-content-reuse-v1', 'target_stream': stream}
    audit_stream = 'manual_research:source-content-reuse-v1:' + h.sha(scope)[:12]
    for item in reused:
        proof = item.get('content_hash_reuse')
        if not proof:
            continue
        digest = h.sha(proof)
        payload = dict(status='incomplete', contract=scope, findings=[], drafts=[],
                       checks=[dict(id='source-content-hash-reuse', status='verified',
                                    checked_at=proof['retrieved_at'],
                                    hashes=[proof['current_fingerprint']['original_sha256'], digest])],
                       source_content_reuse=proof)
        h.record(conn, stream=audit_stream, mode='manual_research', scope=scope,
                 run_id='content-hash-reuse:' + digest, payload=payload,
                 artifacts={digest: h.canonical(proof).encode(),
                            proof['policy_sha256']: policy_bytes()})
