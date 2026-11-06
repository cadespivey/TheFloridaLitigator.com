"""Append-only withdrawal of an unsupported review; original evidence stays intact."""
import json
from flwu import history as h


def withdrawals(conn, stream, *, through_seq=None):
    sql = "SELECT payload FROM captures WHERE stream=? AND json_type(payload,'$.source_review_withdrawal')='object'"
    args = [stream]
    if through_seq is not None: sql += ' AND seq<=?'; args.append(through_seq)
    result = {}
    for row in conn.execute(sql+' ORDER BY seq',args):
        item = json.loads(row[0])['source_review_withdrawal']
        result[item['receipt_sha256']] = item
    return result


def withdraw(conn, stream, receipt_sha256, reviewer, reason):
    if not reviewer.strip() or not reason.strip(): raise ValueError('Withdrawal requires reviewer and specific evidence-based reason')
    row = conn.execute("SELECT payload FROM captures WHERE stream=? AND json_extract(payload,'$.source_gate_review.receipt_sha256')=? ORDER BY seq DESC LIMIT 1",(stream,receipt_sha256)).fetchone()
    if not row: raise ValueError('No accepted source review with that exact receipt')
    old = json.loads(row[0]); source = old['source_gate_review']
    entry = dict(receipt_sha256=receipt_sha256,source_id=source['source_id'],
                 observation_capture_id=source['observation_capture_id'],reviewer=reviewer,reason=reason)
    existing = withdrawals(conn,stream).get(receipt_sha256)
    if existing and existing != entry: raise ValueError('Withdrawal is immutable; preserve the original reason')
    if existing:
        return dict(conn.execute("SELECT seq,capture_id,recorded_at FROM captures WHERE stream=? AND json_extract(payload,'$.source_review_withdrawal.receipt_sha256')=? ORDER BY seq LIMIT 1",(stream,receipt_sha256)).fetchone())
    payload = dict(status='incomplete',contract=old['contract'],findings=[],drafts=[],
        checks=[dict(id='withdraw-source-review:'+source['source_id'],status='incomplete',checked_at=h.now(),hashes=[receipt_sha256])],
        source_review_withdrawal=entry)
    return h.record(conn,stream=stream,mode='manual_research',scope=old['contract'],
                    run_id='source-review-withdrawal:'+h.sha(entry),payload=payload,
                    artifacts={h.sha(entry):h.canonical(entry).encode()})
