"""Bind report references to immutable acquisition observations, never host guesses."""
from __future__ import annotations
import json
from flwu import history as h


class AcquisitionIndex:
    def __init__(self, conn, target_stream, *, through_seq=None):
        self.conn = conn
        self.observations = []
        # Read only acquisition streams for the selected report stream.
        for row in conn.execute('SELECT stream,scope FROM streams'):
            try:
                scope = json.loads(row['scope'])
            except (ValueError, TypeError):
                continue
            if not isinstance(scope, dict) or scope.get('target_stream') != target_stream:
                continue
            for capture in conn.execute('SELECT seq,capture_id,payload FROM captures WHERE stream=? AND seq<=? ORDER BY seq',
                                        (row['stream'], through_seq if through_seq is not None else 9223372036854775807)):
                payload = json.loads(capture['payload'])
                observed = payload.get('source_gate')
                if observed and observed.get('success'):
                    self.observations.append(dict(observed, acquisition_capture_id=capture['capture_id']))
                discovery = payload.get('opinion_discovery', {})
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

    def validate(self, ref):
        required = ('url', 'sha256', 'retrieved_at', 'http_status')
        if not isinstance(ref, dict) or any(k not in ref for k in required):
            raise ValueError('Report evidence needs original acquisition URL, hash, time and HTTP status')
        if ref.get('text_sha256'):
            choices = self.by_pair.get((ref['sha256'], ref['text_sha256']), [])
        else:
            choices = [o for o in self.observations if o.get('sha256') == ref['sha256']]
        match = next((o for o in choices if all(ref[k] == o.get(k) for k in required)
                      and (not ref.get('acquisition_capture_id') or ref['acquisition_capture_id'] == o['acquisition_capture_id'])), None)
        if match is None:
            raise ValueError('Report evidence does not match an acquired URL/raw-text pair/timestamp/HTTP result; same-host substitution is forbidden')
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
