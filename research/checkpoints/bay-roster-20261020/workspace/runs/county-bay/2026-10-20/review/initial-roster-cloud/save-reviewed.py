"""Save initial Bay roster discovery once; never rerun after acknowledgement."""
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path
from flwu.baseline_capture import save_checkpoint
from flwu.history import sha, now

root = Path.cwd()
run = Path("runs/county-bay/2026-10-20")
review = run / "review/initial-roster-cloud"
receipt = review / "checkpoint-ack.json"
assert not receipt.exists()
db = Path("/Users/cadespivey/.local/share/flwu/research-history.sqlite")
scope = dict(profile="county-baseline-v1", county="bay", circuit=14)
stream = "manual_research:county-baseline-v1:" + sha(scope)[:12]
base = json.loads(Path("runs/county-santa-rosa/2026-10-19/draft/checkpoint-019.json").read_text())
contract = dict(base["payload"]["contract"], scope=scope, stream=stream, created_at=now())
roster = json.loads((review / "reviewed-roster.json").read_text())
assert sum(len(roster[key]) for key in ("bay_circuit_court_judges", "bay_county_court_judges", "bay_senior_judges")) == 17
citations = []
for source, quote in zip(json.loads((review / "review-acquisitions.json").read_text()), ("Brantley S. Clark, Jr.", "Robyn Gable")):
    assert quote in Path(source["text_path"]).read_text()
    citation = {k: source[k] for k in ("url", "resolved_url", "http_status", "retrieved_at", "sha256", "text_sha256")}
    citation.update(quote=quote, locator="Original HTTP HTML, roster tables or homepage introduction; direct extraction",
                    authority="official", synthetic=False)
    citations.append(citation)
artifacts = {hashlib.sha256(p.read_bytes()).hexdigest(): str(p)
             for p in sorted(review.rglob("*")) if p.is_file()}
facts = {
    "county": "bay", "circuit": 14, "title": "Initial official Bay judicial roster",
    "roster": roster,
    "counts": {"circuit_judges": 11, "county_judges": 5, "listed_senior_judges": 1},
    "review_scope": "Initial roster, listed contacts and links only; no individual procedure review or county completeness claim.",
    "remaining": ["Review each of17listed people individually, beginning Brantley S. Clark, Jr.",
                  "Reconcile officers and additional senior candidates; clerk and shared material access/procedures.",
                  "County acceptance, directory projection and publication."],
    "provenance_corrections": ["Worker summary is not exact extraction; fresh original HTML and direct extraction support this record.",
                               "Worker approximate browser timestamp/equivalence and hardcoded homepage status are not relied on.",
                               "No expanded personal name inferred from URL slug."],
}
payload = dict(status="incomplete", contract=contract, checks=[dict(id="county-roster", status="incomplete")],
               drafts=[], findings=[dict(key="bay-initial-roster", kind="source_review", facts=facts, citations=citations)])
packet = dict(scope=scope, stream=stream, run_id="bay-initial-roster-reviewed-20261020", payload=payload, artifacts=artifacts)
(run / "draft").mkdir(exist_ok=True)
packet_path = run / "draft/checkpoint-001.json"
packet_path.write_text(json.dumps(packet, indent=2) + "\n")
with tempfile.TemporaryDirectory() as temporary:
    save_checkpoint(root, packet_path, Path(temporary) / "preflight.sqlite")
with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
    assert conn.execute("select count(*) from captures where stream=?", (stream,)).fetchone()[0] == 0
    before = conn.execute("select * from finalized_reports order by seq").fetchall()
    assert len(before) == 5
ack = save_checkpoint(root, packet_path, db)
assert ack == save_checkpoint(root, packet_path, db)
with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
    assert before == conn.execute("select * from finalized_reports order by seq").fetchall()
    assert json.loads(conn.execute("select payload from captures where capture_id=?", (ack["capture_id"],)).fetchone()[0]) == payload
    for h, path in artifacts.items():
        assert conn.execute("select bytes from artifacts where sha256=?", (h,)).fetchone()[0] == Path(path).read_bytes()
    row = conn.execute("select v.facts from finding_versions v join finding_observations o using(version_id) where o.capture_seq=? and o.entity_key='bay-initial-roster'", (ack["seq"],)).fetchone()
    assert json.loads(row[0]) == facts
receipt.write_text(json.dumps(dict(ack, artifacts_readback=len(artifacts), findings_readback=1, replay_verified=True, finalized_reports_unchanged=5), indent=2) + "\n")
print(receipt.read_text())
