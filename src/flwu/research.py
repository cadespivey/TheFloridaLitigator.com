"""Offline evidence accounting for agent-led research; never a live crawler.

Workspace receipts are deliberately separate from the frozen SQLite schema.
Validation proves structural evidence coverage, not legal correctness or approval.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import urlsplit

from flwu.registry import load_sources, validate_sources
from flwu.worker_contract import temporal_status, negative_search

COUNTIES = ["duval", "st_johns", "putnam", "nassau", "baker", "union", "clay"]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def initialize(root: Path, start: str, end: str, profile="weekly-seven", *, as_of=None):
    if profile not in ("weekly-seven", "statewide-circuits"):
        raise ValueError("Unknown profile")
    if not start or not end or date.fromisoformat(start) > date.fromisoformat(end):
        raise ValueError("Explicit valid inclusive window-start and window-end are required")
    if date.fromisoformat(end) > datetime.now(timezone.utc).date():
        raise ValueError("A research window cannot end in the future")
    sources = load_sources()
    validate_sources(sources)
    tasks = [{"id": s["source_id"], "kind": "source", "url": s["url"], "group": s["group_id"]}
             for s in sources if s["critical"]]
    # Independent roster obligations: opinions are not current personnel evidence.
    courts = [("supreme", "https://supremecourt.flcourts.gov/")]
    courts += [(f"dca-{n}", f"https://{n}dca.flcourts.gov/") for n in range(1, 7)]
    circuits = [4, 7, 8] if profile == "weekly-seven" else list(range(1, 21))
    for n in circuits:
        url = {4: "https://www.jud4.org/", 7: "https://circuit7.org/", 8: "https://circuit8.org/"}.get(n, "https://www.flcourts.gov/Florida-Courts/Trial-Courts-Circuit")
        courts.append((f"circuit-{n}", url))
        if n not in (4, 7, 8):
            tasks.append({"id": f"orders-circuit-{n}", "kind": "source", "url": url, "group": "circuit_orders"})
    tasks += [{"id": "roster-" + court, "kind": "roster", "url": url, "group": court} for court, url in courts]
    contract = {"schema_version": 1, "mode": "manual_research", "profile": profile,
                "window_start": start, "window_end": end, "timezone": "America/New_York",
                "interval": "inclusive publication dates",
                "cutoff_utc": datetime.combine(date.fromisoformat(end) + timedelta(days=1), time.min,
                    ZoneInfo("America/New_York")).astimezone(timezone.utc).isoformat(), "counties": COUNTIES,
                "circuits": circuits, "tasks": tasks,
                "publication": "manual approval after independent legal and visual review"}
    if as_of is not None:
        cutoff = _timestamp(as_of)
        if cutoff.astimezone(ZoneInfo("America/New_York")).date() != date.fromisoformat(end):
            raise ValueError("As-of cutoff must fall on window-end in America/New_York")
        contract["cutoff_utc"] = cutoff.astimezone(timezone.utc).isoformat()
        contract["partial_final_day"] = True
        contract["interval"] = "inclusive publication dates through explicit as-of cutoff; final day incomplete"
    if root.exists() and any(root.iterdir()):
        old = json.loads((root / "contract.json").read_text())
        if old != contract:
            raise ValueError("Existing run contract differs; use a new run directory")
        return
    root.mkdir(parents=True, exist_ok=True)
    for name in ("raw", "text", "receipts", "draft", "review"):
        (root / name).mkdir()
    write_json(root / "contract.json", contract)
    (root / "contract.sha256").write_text(digest(contract) + "\n")
    for task in tasks:
        write_json(root / "receipts" / (task["id"] + ".json"), {
            "task_id": task["id"], "status": "uninspected", "checked_at": None,
            "pages_complete": False, "freshness_verified": False, "pages": [],
            "candidates": [], "entities": [], "errors": [],
            "pagination": {"next": "uninspected", "stop_reason": None, "evidence": None},
            "next_action": "Open " + task["url"],
        })


def _timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result > datetime.now(timezone.utc):
        raise ValueError("Timestamp must be timezone-aware and not in the future")
    return result


def _file(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("Evidence path is missing or outside the run directory")
    return path


def _evidence(root, ref, *, mode="manual_research"):
    """Require original artifact + independently saved extraction + capture metadata."""
    url = urlsplit(ref["url"])
    if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
        raise ValueError("Evidence requires a public source URL without credentials")
    if mode not in ("manual_research", "synthetic_replay"):
        raise ValueError("Unknown evidence mode")
    authority = "synthetic" if mode == "synthetic_replay" else "official"
    if ref.get("authority") != authority:
        raise ValueError("Evidence authority does not match the trusted run mode")
    _timestamp(ref["retrieved_at"])
    data = _file(root, ref["path"]).read_bytes()
    if not data or hashlib.sha256(data).hexdigest() != ref["sha256"]:
        raise ValueError("Empty or changed source artifact")
    if ref.get("http_status") != 200:
        raise ValueError("Evidence did not return HTTP 200")
    if mode == "synthetic_replay":
        if ref.get("synthetic") is not True or not url.hostname.endswith(".invalid") or not data.startswith(b"SYNTHETIC REPLAY"):
            raise ValueError("Replay evidence requires synthetic=true, .invalid URL and a synthetic original")
    else:
        if data.startswith(b"SYNTHETIC REPLAY"):
            raise ValueError("Synthetic original cannot be relabelled as live evidence")
        if ref.get("synthetic") is not False:
            raise ValueError("Live evidence must explicitly be synthetic=false")
    return ref


def _citation(root, cite, *, mode="manual_research"):
    _evidence(root, cite, mode=mode)
    text = _file(root, cite["text_path"]).read_text()
    if hashlib.sha256(text.encode()).hexdigest() != cite["text_sha256"]:
        raise ValueError("Extracted text changed")
    if not cite.get("locator") or str(cite["locator"]).startswith("fixture:"):
        raise ValueError("A real page/paragraph/heading locator is required")
    if not cite.get("quote") or cite["quote"] not in text:
        raise ValueError("Claim quote is absent from saved source text")


def validate_person_identity(entity):
    """Require an actual named person supported by their quoted roster evidence."""
    name = entity.get('name')
    if not isinstance(name, str):
        raise ValueError('Roster person requires a full name')
    clean = ' '.join(name.split())
    normalized = re.sub(r'[^a-z0-9 ]', '', clean.lower())
    placeholders = {'chief judge', 'chief justice', 'court clerk', 'clerk of court',
                    'judge', 'justice', 'clerk', 'unnamed', 'unknown', 'not published'}
    if (normalized in placeholders or len(clean.split()) < 2
            or re.search(r'courthouse|justice center|locations|contact us|as chief', clean, re.I)):
        raise ValueError('Roster identity is a placeholder, heading or location, not an actual person')
    quote = entity.get('citation', {}).get('quote', '')
    if not isinstance(quote, str) or clean.casefold() not in ' '.join(quote.split()).casefold():
        raise ValueError('Roster citation must quote the actual full person name')


def _source(root, contract, receipt, kind, *, mode="manual_research"):
    if not receipt.get("pages") or receipt.get("pages_complete") is not True or receipt.get("freshness_verified") is not True:
        raise ValueError("Missing index, pagination completion, or freshness evidence")
    for ref in receipt["pages"]:
        _evidence(root, ref, mode=mode)
    terminal = receipt["pagination"]
    if terminal.get("next") is not None or not terminal.get("stop_reason"):
        raise ValueError("Unresolved pagination cursor/boundary")
    _citation(root, terminal["evidence"], mode=mode)
    candidates = receipt["candidates"]
    if len({c["id"] for c in candidates}) != len(candidates):
        raise ValueError("Duplicate candidate IDs")
    for candidate in candidates:
        if candidate.get("decision") not in ("include", "exclude") or not candidate.get("reason"):
            raise ValueError("Every discovered candidate needs a decision and reason")
        _citation(root, candidate["citation"], mode=mode)
        if candidate["decision"] == "include":
            published = date.fromisoformat(candidate["publication_date"])
            if not date.fromisoformat(contract["window_start"]) <= published <= date.fromisoformat(contract["window_end"]):
                raise ValueError("Included candidate is outside publication window")
            claims = candidate.get("claims", [])
            if not claims:
                raise ValueError("Included candidate lacks reviewed claims")
            for claim in claims:
                if not claim.get("statement") or claim.get("review") != "supported":
                    raise ValueError("Claim needs an explicit supported review")
                _citation(root, claim["citation"], mode=mode)
                if claim.get("change") is True:
                    _citation(root, claim["prior_citation"], mode=mode)
                    if not claim.get("added_text") and not claim.get("deleted_text"):
                        raise ValueError("Change claim lacks amendment comparison")
            effective = candidate.get("effective_date")
            temporal_status(candidate.get("legal_status"), effective, contract["window_end"])
            if candidate.get("effective_date_reviewed") is not True:
                raise ValueError("Effective date must be independently checked, including unknown dates")
    if kind == "roster" or receipt.get("entities"):
        entities = receipt.get("entities", [])
        if not entities or receipt.get("roster_reconciled") is not True:
            raise ValueError("Current roster must be reconciled, including removals and assignments")
        if kind == "roster" and not any(e.get("type") == "judge" for e in entities):
            raise ValueError("Court roster lacks judges")
        ids = [e["id"] for e in entities]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate roster entities")
        for entity in entities:
            if not re.fullmatch(r"[a-z0-9-]+", entity["id"]) or not entity.get("name"):
                raise ValueError("Entity requires stable safe ID and full name")
            if entity.get("type") not in ("judge", "clerk") or not isinstance(entity.get("counties"), list):
                raise ValueError("Entity requires type judge/clerk and county IDs")
            validate_person_identity(entity)
            _citation(root, entity["citation"], mode=mode)


def _person(root, receipt, trial, *, mode="manual_research"):
    fields = receipt["fields"]
    required = ("chambers_phone", "chambers_address", "assistant_name", "assistant_contact") if receipt["entity_type"] == "judge" else ("office_phone", "office_address", "office_contact")
    for key in required:
        field = fields[key]
        if field.get("status") not in ("verified", "not_published"):
            raise ValueError("Contact field is unresolved: " + key)
        if field["status"] == "verified" and not field.get("value"):
            raise ValueError("Verified contact is empty: " + key)
        _citation(root, field["citation"], mode=mode)
        if field["status"] == "not_published" and not field.get("search_log"):
            raise ValueError("Unpublished contact needs searched URLs/terms: " + key)
    if trial and receipt["entity_type"] == "judge":
        procedure = receipt["procedure"]
        if procedure.get("status") not in ("verified", "no_published_procedure_located"):
            raise ValueError("Individual procedure is unresolved")
        _citation(root, procedure["citation"], mode=mode)
        if procedure["status"] == "verified":
            if procedure.get("applies_to") != receipt["task_id"].removeprefix("person-"):
                raise ValueError("Procedure must identify this roster person's ID")
            if not procedure.get("documents"):
                raise ValueError("Procedure requires its applicable document inventory")
            for document in procedure["documents"]:
                _citation(root, document["citation"], mode=mode)
                if not document.get("applicability"):
                    raise ValueError("Procedure document lacks division/judge applicability")
        negative_search(procedure["status"], procedure.get("search_log"))
        if not receipt.get("governing_rules"):
            raise ValueError("Trial judge lacks governing circuit rules or an evidenced negative finding")
        for rule in receipt["governing_rules"]:
            _citation(root, rule["citation"], mode=mode)


def inspect_run(root: Path, *, history_db=None):
    contract = json.loads((root / "contract.json").read_text())
    if digest(contract) != (root / "contract.sha256").read_text().strip():
        raise ValueError("Run contract changed; initialize a new run instead")
    from flwu.history import database, default_database
    from flwu.history_capture import stream_for
    from flwu.evidence_binding import AcquisitionIndex
    # Keep an immutable acquisition lookup for this validation pass.
    marker_path = root / "history-capture.json"
    marker = json.loads(marker_path.read_text()) if marker_path.exists() else {}
    pinned_db = contract.get("history_database") or marker.get("database")
    if history_db and pinned_db and Path(history_db).expanduser().resolve() != Path(pinned_db).expanduser().resolve():
        raise ValueError("Run history database is pinned; use its existing database")
    binding_database = Path(history_db or pinned_db or default_database()).expanduser().resolve()
    with database(binding_database) as binding_conn:
        binding = AcquisitionIndex(binding_conn, stream_for(contract)[0])
    tasks = list(contract["tasks"])
    results = []
    seen_people = {}
    for task in tasks:
        try:
            receipt = json.loads((root / "receipts" / (task["id"] + ".json")).read_text())
            if receipt["task_id"] != task["id"] or receipt["status"] != "complete" or receipt.get("errors"):
                raise ValueError("Uninspected, blocked, mismatched, or unresolved receipt")
            checked = _timestamp(receipt["checked_at"])
            if checked < datetime.fromisoformat(contract["cutoff_utc"]):
                raise ValueError("Receipt predates this run's cutoff")
            def check_capture_times(value):
                if isinstance(value, dict):
                    if "retrieved_at" in value:
                        captured = _timestamp(value["retrieved_at"])
                        if captured > checked or captured < datetime.fromisoformat(contract["cutoff_utc"]):
                            raise ValueError("Capture is stale for this run or later than its review")
                    for child in value.values():
                        check_capture_times(child)
                elif isinstance(value, list):
                    for child in value:
                        check_capture_times(child)
            check_capture_times(receipt)
            if task.get("url") and not any(
                isinstance(page, dict) and page.get("url") == task["url"]
                for page in receipt.get("pages", [])
            ):
                raise ValueError("Required task URL was not reviewed; another page on the same host is not a substitute")
            with database(binding_database) as binding_conn:
                binding.conn = binding_conn
                binding.validate_tree(receipt)
            if task["kind"] == "person":
                if receipt.get("name") != task["name"]:
                    raise ValueError("Person receipt name differs from its official roster identity")
                if receipt["entity_type"] != task["entity_type"]:
                    raise ValueError("Person type differs from roster")
                _person(root, receipt, task["trial"])
            else:
                _source(root, contract, receipt, task["kind"])
                if task["kind"] == "roster" or task["group"].startswith("clerk_"):
                    if task["group"].startswith("clerk_") and not any(e.get("type") == "clerk" for e in receipt.get("entities", [])):
                        raise ValueError("Clerk source must identify its current clerk")
                    trial = task["group"].startswith("circuit-")
                    if task["kind"] == "roster" and not trial and not any(e.get("type") == "clerk" for e in receipt["entities"]):
                        raise ValueError("Appellate roster lacks its current clerk")
                    for person in receipt["entities"]:
                        if trial and person["type"] == "judge" and not person["counties"]:
                            raise ValueError("Trial judge requires an evidenced county assignment")
                        if trial and contract["profile"] == "weekly-seven" and not set(person["counties"]) & set(COUNTIES):
                            continue
                        pid = "person-" + person["id"]
                        identity = (person["name"], person["type"])
                        if pid in seen_people and seen_people[pid] != identity:
                            raise ValueError("Conflicting roster identities share a person ID")
                        if pid not in seen_people:
                            seen_people[pid] = identity
                            tasks.append({"id": pid, "kind": "person", "trial": trial,
                                          "entity_type": person["type"], "name": person["name"]})
                            path = root / "receipts" / (pid + ".json")
                            if not path.exists():
                                keys = ("chambers_phone", "chambers_address", "assistant_name", "assistant_contact") if person["type"] == "judge" else ("office_phone", "office_address", "office_contact")
                                write_json(path, {"task_id": pid, "entity_type": person["type"],
                                    "name": person["name"], "status": "uninspected", "checked_at": None,
                                    "errors": [], "fields": {k: {"status": "uninspected", "value": None,
                                    "citation": None, "search_log": []} for k in keys},
                                    "procedure": {"status": "uninspected", "applies_to": person["id"],
                                    "citation": None, "documents": [], "search_log": []}, "governing_rules": []})
            results.append({"task_id": task["id"], "status": "evidence_valid"})
        except (OSError, ValueError, KeyError, TypeError) as exc:
            results.append({"task_id": task["id"], "status": "incomplete", "reason": str(exc)})
    missing = [r for r in results if r["status"] != "evidence_valid"]
    result = {"status": "incomplete" if missing else "ready_for_review", "required": len(results),
              "evidence_valid": len(results) - len(missing), "tasks": results,
              "publication_ready": False, "next_action": (missing[0]["task_id"] if missing else "Independent legal and visual review; publication requires explicit approval")}
    write_json(root / "status.json", result)
    (root / "RESUME.txt").write_text("Read AGENTS.md and docs/workflow/RUNBOOK.md.\n"
        f"Run directory: {root.resolve()}\nContract SHA256: {digest(contract)}\n"
        f"Next task: {result['next_action']}\nRead only contract.json, this task's receipt and its evidence.\n"
        "Run flwu research status --run-dir <this-directory> after editing the receipt.\n"
        "Saved imports are not fresh verification; never mark the overall goal complete from this checkpoint alone.\n")
    from flwu.history_capture import capture
    capture(root, db_path=history_db, manual_status=result)
    return result
