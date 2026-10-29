"""Machine proof of current supplemental review; never a legal interpretation."""
from datetime import datetime
import json
from urllib.parse import urlsplit

from flwu import content_fingerprint, history as h, opinion_discovery as opinions, source_gate as gate
from flwu.identity import document_id


class ReviewedSupplements:
    def __init__(self, index, queue):
        self.index, self.queue = index, queue
        self.protocol = queue.get('source_reviews', {}).get('review_protocol')
        self.anchor = index.conn.execute(
            "SELECT seq,capture_id,recorded_at FROM captures WHERE stream=? AND seq<=? "
            "AND json_extract(payload,'$.opinion_discovery.run_id')=? "
            "AND json_extract(payload,'$.opinion_discovery.checkpoint')='update-contract' ORDER BY seq LIMIT 1",
            (opinions.stream_for(index.target_stream)[0], index.through_seq, queue.get('run_id'))).fetchone()
        self.reviews = None
        self.content_index = None
        self.cache = {}

    def fresh(self, source, seq):
        if not self.anchor or not source or not source.get('success') or seq <= self.anchor['seq']:
            return False
        try:
            observed = datetime.fromisoformat(source['retrieved_at'])
            start = datetime.fromisoformat(self.anchor['recorded_at'])
            return observed.tzinfo is not None and observed >= start
        except (KeyError, ValueError, TypeError):
            return False

    def load_reviews(self):
        if self.reviews is not None:
            return
        self.reviews = {'source_gate_review': [], 'opinion_review': []}
        for row in self.index.conn.execute(
                "SELECT seq,capture_id,payload FROM captures WHERE stream=? AND seq<=? "
                "AND (json_type(payload,'$.source_gate_review')='object' OR json_type(payload,'$.opinion_review')='object') ORDER BY seq",
                (self.index.target_stream, self.index.through_seq)):
            payload = json.loads(row['payload'])
            for key in self.reviews:
                if key in payload:
                    self.reviews[key].append(dict(payload[key], review_capture_id=row['capture_id']))
        history = sorted(self.index.source_history, key=lambda x: x['seq'])
        self.content_index = content_fingerprint.ReviewIndex(
            history, self.reviews['source_gate_review'], gate.raw_bases(history), self.protocol,
            lambda digest: gate.blob(self.index.conn, digest))

    def source_proof(self, url):
        current = self.index.source_observations.get(url)
        if (not current or not current.get('text_sha256')
                or current.get('review_protocol') != self.protocol
                or not self.fresh(current, current['seq'])):
            return None
        self.index.validate(current)
        self.load_reviews()
        for review, prior in reversed(self.content_index.by_source.get(current['source_id'], [])):
            if (prior['url'] == url and prior['sha256'] == current['sha256']
                    and (prior.get('resolved_url') or url) == (current.get('resolved_url') or url)):
                return dict(kind='source_review', basis='raw_sha256', url=url,
                            observation_capture_id=current['acquisition_capture_id'],
                            sha256=current['sha256'], text_sha256=current['text_sha256'],
                            retrieved_at=current['retrieved_at'], review_capture_id=review['review_capture_id'],
                            review_receipt_sha256=review['receipt_sha256'],
                            reviewed_observation_capture_id=prior['capture_id'])
        proof = self.content_index.reuse(dict(current, capture_id=current['acquisition_capture_id']))
        if proof:
            return dict(kind='source_review', basis='content_and_component_hashes', url=url,
                        observation_capture_id=current['acquisition_capture_id'],
                        sha256=current['sha256'], text_sha256=current['text_sha256'],
                        retrieved_at=current['retrieved_at'], content_hash_reuse=proof)
        return None

    def opinion_proof(self, url):
        event = self.index.detail_events.get(url)
        if (not event or event.get('run_id') != self.queue.get('run_id') or not event.get('complete')
                or not self.fresh(event.get('source'), event['seq']) or len(event.get('entries', [])) != 1):
            return None
        item = event['entries'][0]
        court = next((c for c in opinions.COURTS if c['id'] == item.get('court')), None)
        status = item.get('status_source', {})
        if (not court or item.get('detail_url') != url or status.get('url') != url
                or urlsplit(url).hostname != urlsplit(court['listing_page']).hostname
                or item.get('id') != document_id(item['court'], 'content:'+str(item.get('content_id')))
                or status.get('sha256') != event.get('sha256')
                or h.sha(item.get('metadata')) != status.get('text_sha256')
                or item.get('state_sha256') != status.get('text_sha256')):
            return None
        pdf = self.index.source_observations.get(item.get('pdf_url'))
        if (not pdf or not self.fresh(pdf, pdf['seq']) or opinions.document_error(self.index.conn, pdf)):
            return None
        self.index.validate(status)
        self.index.validate(pdf)
        signature = h.sha([item['id'], item['state_sha256'], pdf['sha256'], self.protocol])
        self.load_reviews()
        review = next((r for r in reversed(self.reviews['opinion_review'])
                       if r['id'] == item['id'] and r['signature'] == signature
                       and r['pdf_sha256'] == pdf['sha256'] and r['state_sha256'] == item['state_sha256']
                       and r['relevance'] in ('relevant', 'not_relevant')), None)
        if not review:
            return None
        return dict(kind='opinion_monitor', scope='official_opinion_metadata_and_pdf', url=url,
                    opinion_id=item['id'], content_id=item['content_id'],
                    observation_capture_id=event['capture_id'], sha256=status['sha256'],
                    text_sha256=status['text_sha256'], retrieved_at=status['retrieved_at'],
                    pdf_observation_capture_id=pdf['acquisition_capture_id'], pdf_sha256=pdf['sha256'],
                    review_capture_id=review['review_capture_id'], review_receipt_sha256=review['receipt_sha256'],
                    signature=signature)

    def proof(self, url):
        if url not in self.cache:
            result = None
            if self.protocol and self.anchor:
                result = self.source_proof(url) or self.opinion_proof(url)
            self.cache[url] = (dict(result, proof_version=1, run_id=self.queue['run_id'],
                                    review_protocol=self.protocol,
                                    acquisition_anchor_capture_id=self.anchor['capture_id']) if result else None)
        return self.cache[url]
