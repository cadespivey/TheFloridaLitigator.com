"""One-time reviewed acceptance append. Never rerun after receipt exists."""
import copy
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path

from flwu.baseline_capture import save_checkpoint
from flwu.county_directory import validate_supplement, public_metadata
from flwu.publication import digest
from flwu.history import now

root = Path.cwd()
run = Path("runs/county-santa-rosa/2026-10-19")
review = run / "review/directory-7709-cloud"
receipt = review / "acceptance-ack.json"
assert not receipt.exists(), "Already saved; do not rerun."
db = Path("/Users/cadespivey/.local/share/flwu/research-history.sqlite")
packet = copy.deepcopy(json.loads((run / "draft/checkpoint-018.json").read_text()))
draft = json.loads((review / "corrected-draft.json").read_text())
validate_supplement(draft, preview=True)
assert len(draft["people"]) == 10 and draft["through_capture"]["seq"] == 7709
audit = json.loads((review / "export-database-audit.json").read_text())
assert audit["entities_matched_latest_database_observation"] == 18
assert audit["cited_artifact_hashes_verified"] == 53
browser = json.loads((review / "browser-review.json").read_text())
assert (browser["county_rows"], browser["circuit_rows"], browser["historical_county_rows"]) == (4, 44, 0)
assert not browser["horizontal_document_overflow"]
actual = json.loads((review / "links-keyboard-result.txt").read_text().splitlines()[1])
assert actual["contactNotesKeyboard"] == {"enterOpens": True, "spaceCloses": True}
expected_links = []
for person in draft["people"]:
    if "county_santa_rosa" not in person["court_ids"]:
        continue
    expected_links += [u for u in (person["profile_url"], person["procedure_url"]) if u]
    for rows in person["contacts"].values():
        expected_links += [row["href"] for row in rows if row.get("href")]
assert sorted(x["href"] for x in actual["links"]) == sorted(expected_links)

stamp = now()
reviewed = public_metadata(copy.deepcopy(draft))
reviewed["review_status"] = "reviewed"
reviewed["review"] = {
    "reviewed_by": "Cloud review of bounded local collection",
    "reviewed_at": stamp,
    "attestation": "Pinned source/field and court-membership review; combined desktop/mobile and historical-isolation checks. Explicit bounded-search gaps remain. No controlling-authority conflict resolution.",
}
reviewed["coverage_note"] = (
    "Eight active judges, one circuit-wide senior judge and the clerk reviewed. "
    "Senior-judge personal contacts and procedures were not located in a bounded search. "
    "Historical officer references do not establish current service."
)
reviewed["content_sha256"] = digest({k: v for k, v in reviewed.items() if k != "content_sha256"})
validate_supplement(reviewed)
reviewed_path = review / "reviewed-supplement.json"
reviewed_path.write_text(json.dumps(reviewed, indent=2, ensure_ascii=False) + "\n")

packet["run_id"] = "santa-rosa-bounded-acceptance-reviewed-20261020"
packet["payload"]["contract"]["created_at"] = stamp
for folder in (review, Path("output/county-review/santa-rosa-7709-a")):
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            packet["artifacts"][hashlib.sha256(path.read_bytes()).hexdigest()] = str(path)
for name in ("santa-rosa-7709-senior-mobile.png", "santa-rosa-7709-senior-desktop.png"):
    path = Path("output/playwright") / name
    packet["artifacts"][hashlib.sha256(path.read_bytes()).hexdigest()] = str(path)
membership_hash = hashlib.sha256((review / "expected-membership.json").read_bytes()).hexdigest()
for check in packet["payload"]["checks"]:
    if check["id"] == "county-roster":
        check.update(status="verified", checked_at=stamp, hashes=[membership_hash],
                     scope="Eight active judges, circuit-wide senior and clerk reconciled; historical officer status and senior contact gaps explicitly retained.")
packet["payload"]["checks"].append({"id": "county-publication", "status": "incomplete"})
finding = next(f for f in packet["payload"]["findings"] if f["kind"] == "county_review")
facts = finding["facts"]
facts.update(
    basis_capture=7709,
    counts={"active_judges": 8, "circuit_wide_senior": 1, "clerk": 1, "directory_people": 10},
    research_review_status="bounded_accepted_with_documented_gaps",
    reviewed_at=stamp,
    reviewed_by="Cloud independent review of bounded local collection",
    next_action="Integrate reviewed supplement through publication gate; next county Bay, Fourteenth Judicial Circuit.",
    publication_status="reviewed_supplement_not_published",
    validation={
        "pinned_export_entities": 18,
        "repeat_export_identical_files": 74,
        "cited_artifact_hashes_verified": 53,
        "people": 10,
        "combined_preview_supplements": 27,
        "county_rows": 4,
        "circuit_rows": 44,
        "historical_county_rows": 0,
        "viewports": [390, 1280],
        "horizontal_overflow": False,
        "keyboard_notes_and_skip_link": "verified",
        "rendered_links": "matched saved draft",
        "tests": "530 passed; no source changes since test run",
        "reviewed_supplement_sha256": reviewed["content_sha256"],
    },
)
packet_path = run / "draft/checkpoint-019.json"
packet_path.write_text(json.dumps(packet, indent=2) + "\n")
with tempfile.TemporaryDirectory() as temporary:
    save_checkpoint(root, packet_path, Path(temporary) / "preflight.sqlite")
with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
    assert conn.execute("select max(seq) from captures where stream=?", (packet["stream"],)).fetchone()[0] == 7709
    before = conn.execute("select * from finalized_reports order by seq").fetchall()
    assert len(before) == 5
ack = save_checkpoint(root, packet_path, db)
assert ack == save_checkpoint(root, packet_path, db)
with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
    assert before == conn.execute("select * from finalized_reports order by seq").fetchall()
    assert json.loads(conn.execute("select payload from captures where capture_id=?", (ack["capture_id"],)).fetchone()[0]) == packet["payload"]
    for sha, path in packet["artifacts"].items():
        assert conn.execute("select bytes from artifacts where sha256=?", (sha,)).fetchone()[0] == Path(path).read_bytes()
    for f in packet["payload"]["findings"]:
        row = conn.execute("select v.facts from finding_observations o join finding_versions v using(version_id) where o.capture_seq=? and o.entity_key=?", (ack["seq"], f["key"])).fetchone()
        assert json.loads(row[0]) == f["facts"]
receipt.write_text(json.dumps(dict(ack, artifacts_readback=len(packet["artifacts"]), findings_readback=len(packet["payload"]["findings"]), replay_verified=True, finalized_reports_unchanged=5), indent=2) + "\n")
print(receipt.read_text())
