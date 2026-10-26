"""Trusted adapters from research workspaces to cumulative history.

Only revalidated receipts become comparison facts. Incomplete receipt JSON is
retained as draft evidence, never promoted to the last known supported finding.
"""
from __future__ import annotations

import json
from pathlib import Path

from flwu.history import database, record, compare, sha, stamp, default_database
from flwu.research import digest, write_json, _evidence, _citation, _file


def load(path):
    return json.loads(path.read_text())


def references(value):
    if isinstance(value, dict):
        if {"path", "sha256", "url", "retrieved_at"} <= value.keys():
            yield value
        else:
            for child in value.values():
                yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def facts(value):
    """Drop evidence locations and bookkeeping, retaining substantive values."""
    if isinstance(value, dict):
        if {"path", "sha256", "url", "retrieved_at"} <= value.keys():
            return {k: value[k] for k in ("url", "quote", "locator") if k in value}
        return {k: facts(v) for k, v in value.items() if k not in {
            "citation", "citations", "checked_at", "validated_at", "retrieved_at",
            "packet_sha256", "answer_sha256", "next_action", "errors"}}
    if isinstance(value, list):
        return [facts(v) for v in value]
    return value


def stream_for(contract):
    scope = {"counties": sorted(contract["counties"]),
             "profile": contract.get("profile", "controlled-replay"),
             "circuits": sorted(contract.get("circuits", []))}
    return contract["mode"] + ":" + scope["profile"] + ":" + sha(scope)[:12], scope


def capture(root, *, db_path=None, manual_status=None):
    root = Path(root).resolve()
    contract = load(root / "contract.json")
    if digest(contract) != (root / "contract.sha256").read_text().strip():
        raise ValueError("History capture rejected: changed run contract")
    mode = contract["mode"]
    previous_marker = load(root / "history-capture.json") if (root / "history-capture.json").exists() else {}
    pinned_db = contract.get("history_database") or previous_marker.get("database")
    if db_path and pinned_db and Path(db_path).expanduser().resolve() != Path(pinned_db).resolve():
        raise ValueError("Run history database is pinned; use its existing database")
    db_path = Path(db_path or pinned_db or default_database()).expanduser().resolve()
    artifacts, findings, checks, drafts = {}, [], [], []

    def save_refs(value):
        refs = list(references(value))
        for ref in refs:
            _evidence(root, ref, mode=mode)
            artifacts[ref["sha256"]] = _file(root, ref["path"]).read_bytes()
            if "text_path" in ref:
                data = _file(root, ref["text_path"]).read_bytes()
                if sha(data) != ref["text_sha256"]:
                    raise ValueError("History extraction checksum mismatch")
                artifacts[ref["text_sha256"]] = data
            if ref.get("quote"):
                _citation(root, ref, mode=mode)
        return refs

    def finding(key, kind, value, refs):
        findings.append({"key": key, "kind": kind, "facts": facts(value), "citations": refs})

    if mode == "manual_research":
        if manual_status is None:
            # inspect_run owns validation and invokes this adapter exactly once.
            from flwu.research import inspect_run
            inspect_run(root, history_db=db_path)
            return load(root / "history-capture.json")
        status = manual_status["status"]
        for result in manual_status["tasks"]:
            task_id = result["task_id"]
            path = root / "receipts" / (task_id + ".json")
            try:
                receipt = load(path)
            except (OSError, ValueError):
                receipt = {"task_id": task_id, "error": "missing or malformed receipt"}
            limited = result['status'] == 'reviewed_source_limitation'
            if limited:
                from flwu import source_limitations
                task = next(t for t in contract['tasks'] if t['id'] == task_id)
                with database(db_path) as validation_conn:
                    source_limitations.validate(validation_conn, stream_for(contract)[0], task,
                                                receipt.get('source_limitation'))
            valid = result["status"] == "evidence_valid" or limited
            refs = save_refs({k: v for k, v in receipt.items() if k != 'source_limitation'}) if valid else []
            checks.append({"id": task_id, "status": 'reviewed_source_limitation' if limited else "verified" if valid else "incomplete",
                           "checked_at": min(stamp(r["retrieved_at"]) for r in refs) if refs else None,
                           "reviewed_at": receipt.get("checked_at") if valid else None,
                           "hashes": sorted({r["sha256"] for r in refs}),
                           "reason": result.get("reason")})
            if limited:
                checks[-1]['limitation'] = receipt['source_limitation']
            if not valid:
                drafts.append(receipt)
                for ref in references(receipt):
                    try:
                        save_refs(ref)
                    except (ValueError, KeyError, TypeError, OSError):
                        pass  # Invalid bytes stay in the run, never in validated history.
                continue
            if task_id.startswith("person-"):
                finding(task_id, receipt["entity_type"], receipt, refs)
            elif refs:
                inventory = {"entities": receipt.get("entities", []),
                             "candidate_ids": sorted(c["id"] for c in receipt.get("candidates", []))}
                if receipt.get('review_scope'):
                    inventory['review_scope'] = receipt['review_scope']
                    inventory['reviewed_source_records'] = receipt.get('reviewed_source_records', [])
                finding(task_id, "source_inventory", inventory, refs)
                for candidate in receipt.get("candidates", []):
                    finding(task_id + ":" + candidate["id"], "candidate", candidate, list(references(candidate)))
    elif mode == "synthetic_replay":
        from flwu.controlled_worker import make_packet, validate_receipt
        state = load(root / "state.json")
        evidence = load(root / "evidence.json")
        for endpoint in state["required"]:
            ref = evidence.get(endpoint)
            if ref:
                save_refs(ref)
            checks.append({"id": endpoint, "status": "verified" if ref else "incomplete",
                           "checked_at": ref["retrieved_at"] if ref else None,
                           "hashes": [ref["sha256"]] if ref else []})
        accepted_ids = set()
        for path in sorted((root / "accepted").glob("*.json")):
            saved = load(path)
            try:
                task = saved["task"]
                packet, spans = make_packet(root, task, [evidence[p] for p in task["dependencies"]],
                                            contract["window_start"], contract["window_end"])
                rebuilt = validate_receipt(root, task, saved["worker_answer"], spans,
                                           contract["window_start"], contract["window_end"])
                if digest(packet) != saved["packet_sha256"] or rebuilt["answer"] != saved["answer"] or digest(saved["answer"]) != saved["answer_sha256"]:
                    raise ValueError("Accepted receipt hashes or source-grounded answer changed")
                refs = save_refs(rebuilt["citations"])
                finding(task["kind"] + ":" + task["id"], task["kind"], rebuilt["answer"], refs)
                accepted_ids.add(task["id"])
            except (ValueError, KeyError, TypeError, OSError) as exc:
                drafts.append({"receipt": saved, "error": str(exc)})
        # Clerk rows are coordinator-extracted and still require saved citations.
        if "clerks/current" in evidence:
            ref = evidence["clerks/current"]
            for line, text in enumerate(_file(root, ref["path"]).read_text().splitlines(), 1):
                cols = [c.strip() for c in text.split("|")]
                if len(cols) == 5:
                    clerk = dict(zip(("county", "name", "phone", "contact", "address"), cols))
                    cite = {**ref, "quote": text, "locator": f"line {line}"}
                    finding("clerk:" + clerk["county"], "clerk", clerk, save_refs(cite))
        complete = (state.get("status") == "ready_for_review" and not state.get("pending") and not drafts
                    and bool(state.get("tasks")) and {t["id"] for t in state["tasks"]} <= accepted_ids
                    and all(c["status"] == "verified" for c in checks))
        status = "ready_for_review" if complete else "incomplete"
    else:
        raise ValueError("Unsupported research history mode")
    stream, scope = stream_for(contract)
    payload = {"status": status, "contract": contract, "origin": str(root),
               "checks": sorted(checks, key=lambda c: c["id"]),
               "findings": sorted(findings, key=lambda f: f["key"]), "drafts": drafts}
    with database(db_path) as conn:
        result = record(conn, stream=stream, mode=mode, scope=scope,
                        run_id=sha([str(root), digest(contract)]), payload=payload, artifacts=artifacts)
        context = compare(conn, stream)
    result["database"] = str(db_path)
    write_json(root / "history-capture.json", result)
    write_json(root / "history-context.json", context)
    return result
