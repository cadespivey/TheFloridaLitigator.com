"""Bind report references to immutable acquisition observations, never host guesses."""
from __future__ import annotations
import base64
import binascii
import json
from flwu import history as h


class AcquisitionIndex:
    def __init__(self, conn, target_stream, *, through_seq=None):
        self.conn = conn
        self.target_stream = target_stream
        self.through_seq = through_seq if through_seq is not None else 9223372036854775807
        self.observations = []
        self.source_observations = {}
        self.source_history = []
        self.detail_events = {}
        # Read only acquisition streams for the selected report stream.
        for row in conn.execute('SELECT stream,scope FROM streams'):
            try:
                scope = json.loads(row['scope'])
            except (ValueError, TypeError):
                continue
            if not isinstance(scope, dict) or scope.get('target_stream') != target_stream:
                continue
            discovery_contracts = {}
            for capture in conn.execute('SELECT seq,capture_id,payload FROM captures WHERE stream=? AND seq<=? ORDER BY seq',
                                        (row['stream'], through_seq if through_seq is not None else 9223372036854775807)):
                payload = json.loads(capture['payload'])
                observed = payload.get('source_gate')
                if observed:
                    self.source_history.append(dict(observed, seq=capture['seq'], capture_id=capture['capture_id']))
                    previous = self.source_observations.get(observed.get('url'))
                    if previous is None or previous['seq'] < capture['seq']:
                        self.source_observations[observed['url']] = dict(
                            observed, seq=capture['seq'], acquisition_capture_id=capture['capture_id'])
                if observed and observed.get('success'):
                    self.observations.append(dict(observed, acquisition_capture_id=capture['capture_id']))
                discovery = payload.get('opinion_discovery', {})
                if discovery.get('kind') == 'detail' and discovery.get('source', {}).get('url'):
                    url = discovery['source']['url']
                    if capture['seq'] > self.detail_events.get(url, {}).get('seq', -1):
                        self.detail_events[url] = dict(discovery, seq=capture['seq'], capture_id=capture['capture_id'])
                if discovery.get('kind') == 'contract':
                    discovery_contracts[discovery['run_id']] = discovery['contract']
                if discovery.get('kind') == 'page' and discovery.get('complete') is True:
                    from flwu.discovery_evidence import page_binding
                    contract = discovery_contracts.get(discovery.get('run_id'))
                    if contract is not None:
                        self.observations.append(page_binding(conn, discovery, capture['capture_id'], contract))
                for item in discovery.get('entries', []):
                    source = item.get('status_source')
                    # Older entries omitted transport fields, but the parent event
                    # retained the real response. Reuse it only with exact bindings.
                    transport = discovery.get('source', {})
                    if (source and transport.get('success') is True
                            and discovery.get('sha256') == source.get('sha256')
                            and all(transport.get(k) == source.get(k) for k in ('url', 'retrieved_at'))):
                        source = dict(source)
                        for key in ('http_status', 'success'):
                            if key not in source and key in transport:
                                source[key] = transport[key]
                    if source and source.get('success'):
                        self.observations.append(dict(source, acquisition_capture_id=capture['capture_id']))
        self.by_pair = {}
        for observed in self.observations:
            self.by_pair.setdefault((observed.get('sha256'), observed.get('text_sha256')), []).append(observed)

    def reviewed_supplement(self, queue, url):
        from flwu.supplemental_coverage import ReviewedSupplements
        if not hasattr(self, '_reviewed_supplements'):
            self._reviewed_supplements = {}
        key = (queue.get('run_id'), queue.get('source_reviews', {}).get('review_protocol'))
        if key not in self._reviewed_supplements:
            self._reviewed_supplements[key] = ReviewedSupplements(self, queue)
        return self._reviewed_supplements[key].proof(url)

    def unavailable(self, url):
        """Only the latest saved acquisition within this report's boundary counts."""
        observed = self.source_observations.get(url)
        if not observed or observed.get('success') is not False:
            return False
        for key in ('sha256', 'text_sha256'):
            if observed.get(key):
                blob = self.conn.execute('SELECT bytes FROM artifacts WHERE sha256=?',
                                         (observed[key],)).fetchone()
                if blob is None or h.sha(blob[0]) != observed[key]:
                    raise ValueError('Unavailable-source acquisition artifact missing or changed')
        return True

    def _validate_browser_pdf(self, observed):
        """Bind a non-HTTP PDF body to its saved browser result and exact bytes."""
        if observed.get('acquisition_method') != 'browser-embedded-pdf-data-uri-v1':
            raise ValueError('Evidence without HTTP status needs a bound browser PDF acquisition')
        digest = observed.get('browser_snapshot_sha256')
        blob = self.conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (digest,)).fetchone()
        if not blob or h.sha(blob[0]) != digest:
            raise ValueError('Browser PDF snapshot artifact missing or changed')
        try:
            snapshot = json.loads(blob[0])
            if not isinstance(snapshot, dict) or any(snapshot.get(k) != observed.get(k)
                                                   for k in ('url', 'retrieved_at')):
                raise ValueError('Browser PDF snapshot URL or retrieval time mismatch')
            uri = snapshot.get('pdf')
            if not isinstance(uri, str) or not uri.startswith('data:application/pdf;base64,'):
                raise ValueError('Browser PDF snapshot needs an embedded PDF data URI')
            raw = base64.b64decode(uri.split(',', 1)[1], validate=True)
        except (json.JSONDecodeError, UnicodeDecodeError, binascii.Error) as exc:
            raise ValueError('Invalid browser PDF snapshot') from exc
        if not raw.startswith(b'%PDF-') or h.sha(raw) != observed['sha256']:
            raise ValueError('Browser PDF snapshot does not contain the acquired original')

    def validate(self, ref):
        required = ('url', 'sha256', 'retrieved_at')
        if not isinstance(ref, dict) or any(k not in ref for k in required):
            raise ValueError('Report evidence needs original acquisition URL, hash and time')
        if ref.get('text_sha256'):
            choices = self.by_pair.get((ref['sha256'], ref['text_sha256']), [])
        else:
            choices = [o for o in self.observations if o.get('sha256') == ref['sha256']]
        match = next((o for o in choices if all(ref[k] == o.get(k) for k in required)
                      and ref.get('http_status') == o.get('http_status')
                      and (not ref.get('acquisition_capture_id') or ref['acquisition_capture_id'] == o['acquisition_capture_id'])), None)
        if match is None:
            raise ValueError('Report evidence does not match an acquired URL/raw-text pair/timestamp/HTTP result; same-host substitution is forbidden')
        if ref.get('http_status') is None:
            self._validate_browser_pdf(match)
        for key in ('sha256', 'text_sha256'):
            if not ref.get(key):
                continue
            blob = self.conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (ref[key],)).fetchone()
            if not blob or h.sha(blob[0]) != ref[key]:
                raise ValueError('Acquired evidence artifact missing or changed')
        if ref.get('quote'):
            if not ref.get('text_sha256') or not ref.get('locator'):
                raise ValueError('Quoted evidence requires bound extraction and locator')
            text = self.conn.execute('SELECT bytes FROM artifacts WHERE sha256=?', (ref['text_sha256'],)).fetchone()[0].decode('utf-8')
            if ref['quote'] not in text:
                raise ValueError('Report quote absent from acquired extraction')
        return match

    def validate_tree(self, value):
        if isinstance(value, dict):
            if {'url', 'sha256', 'retrieved_at'} <= value.keys():
                self.validate(value)
            for child in value.values():
                self.validate_tree(child)
        elif isinstance(value, list):
            for child in value:
                self.validate_tree(child)
