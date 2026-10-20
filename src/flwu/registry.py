"""Source and document registries for Florida Litigator Weekly Update.

Manages source registries, scope documentation, and document alias resolution.
Maps equivalent official mirror routes to canonical document identifiers.

Uses config/sources.json with an identical packaged fallback.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# Packaged mirror of config/sources.json; discovery entries are uninspected.
_SOURCE_REGISTER = json.loads((Path(__file__).parent / "data" / "sources.json").read_text())


# Seven county roots and three circuit roots.
_COUNTY_ROOTS = ["duval", "st_johns", "putnam", "clay", "nassau", "baker", "union"]
_CIRCUIT_ROOTS = ["fourth", "seventh", "eighth"]


def resolve_document_alias(document_id: str, aliases: dict) -> str:
    """Resolve an alias chain to the canonical document_id.

    Follows alias chains: aliases[document_id] → aliases[target] → ...
    Stops when the target is not a key in aliases.

    Fails (raises ValueError) on:
    - Cycles (detected by visited set)

    Callers must supply reviewed aliases; this helper does not verify authority.
    """
    if not aliases:
        return document_id

    visited = set()
    current = document_id

    while current in aliases:
        if current in visited:
            raise ValueError(f"Alias cycle detected starting at {document_id}")
        visited.add(current)
        current = aliases[current]

    return current


def load_sources(path: Path | None = None) -> list[dict]:
    """Load source register from a JSON file.

    If path is None, loads from the default config path.
    Returns the list of source definitions.
    """
    if path is None:
        path = Path("config/sources.json")

    if path.is_file():
        text = path.read_text(encoding="utf-8")
        return json.loads(text)

    return list(_SOURCE_REGISTER)


def validate_sources(sources: list[dict], *, required_ids: set[str] | None = None) -> None:
    """Validate that all sources have required fields.

    Required: source_id, group_id, url, authority, scope_ids, critical,
    adapter_id, access_status, checked_at.

    Fails (raises ValueError) on missing required fields.
    """
    required_keys = {"source_id", "group_id", "url", "authority", "scope_ids", "critical", "adapter_id", "access_status", "checked_at"}
    for src in sources:
        missing = required_keys - set(src.keys())
        if missing:
            raise ValueError(f"Source {src.get('source_id', '?')} missing keys: {sorted(missing)}")

    expected = required_ids if required_ids is not None else {s["source_id"] for s in _SOURCE_REGISTER if s["critical"]}
    ids = [s["source_id"] for s in sources]
    if len(ids) != len(set(ids)) or not expected <= set(ids):
        raise ValueError("Duplicate or missing required source IDs")
    if any(s["source_id"] in expected and s["critical"] is not True for s in sources):
        raise ValueError("Required source cannot be downgraded to optional")
    # Registry metadata is not live coverage evidence.
    for src in sources:
        if src.get("critical") and src.get("access_status") not in ("available", "blocked", "uninspected"):
            raise ValueError(f"Critical source {src['source_id']} must be available, blocked or uninspected, got {src['access_status']}")


def scope_blueprint() -> list[dict]:
    """Generate scope blueprint from source register.

    Returns a list of scope definitions, each with:
    - scope_id
    - intent (description)
    - specification (detailed spec)
    - test_plan (test plan description)
    - sources (list of source IDs)
    - comparisons (list of comparison descriptions)
    """
    groups = {}
    catalog = load_sources()
    validate_sources(catalog)
    for src in catalog:
        group = src.get("group_id", "other")
        groups.setdefault(group, []).append(src["source_id"])

    scopes = []
    for group_id, source_ids in sorted(groups.items()):
        scope = {
            "scope_id": group_id,
            "intent": f"Track and report on {group_id} sources.",
            "specification": f"Follow docs/workflow/RUNBOOK.md source-search and evidence contracts for {group_id}. Required source IDs: {', '.join(sorted(source_ids))}. Read config/sources.json for literal entry URLs. Save raw bytes and receipts under the pinned run directory; do not infer completeness from returned hit totals.",
            "test_plan": f"Apply docs/workflow/TEST_PLAN.md to {group_id}: withhold each required source in turn ({source_ids}); status must remain incomplete. Test pagination, exhausted retry, old dates, missing evidence and modified artifacts. An empty source still requires a saved index and explicit terminal pagination evidence.",
            "sources": sorted(source_ids),
            "source_entries": [{"source_id": src["source_id"], "url": src["url"]} for src in catalog if src["source_id"] in source_ids],
            "comparisons": ["Compare each source with its prior accepted snapshot; save original and changed passages. Imported references do not establish current verification."],
        }
        scopes.append(scope)

    return scopes


def write_scope_docs(scope: dict, *, output_root: Path) -> list[Path]:
    """Write scope documentation to output_root.

    Returns list of written file paths.
    Generates: scope_spec.md, scope_test_plan.md, scope_sources.json.
    """
    output_root.mkdir(parents=True, exist_ok=True)
    scope_id = scope.get("scope_id", "unknown")

    paths = []

    # Write scope spec
    spec_path = output_root / f"{scope_id}_spec.md"
    spec_path.write_text(
        f"# {scope_id} Scope Specification\n\n"
        f"Intent: {scope.get('intent', '')}\n\n{scope.get('specification', '')}\n\n"
        f"## Sources\n\n"
        + "\n".join(f"- `{src['source_id']}`: {src['url']}" for src in scope.get("source_entries", []))
        + f"\n\n## Comparisons\n\n"
        + "\n".join(f"- {c}" for c in scope.get("comparisons", []))
        + "\n",
        encoding="utf-8",
    )
    paths.append(spec_path)

    # Write scope test plan
    test_path = output_root / f"{scope_id}_test_plan.md"
    test_path.write_text(
        f"# {scope_id} Test Plan\n\n"
        f"{scope.get('test_plan', '')}\n",
        encoding="utf-8",
    )
    paths.append(test_path)

    # Write scope sources
    sources_path = output_root / f"{scope_id}_sources.json"
    sources_path.write_text(
        json.dumps({"scope_id": scope_id, "sources": scope.get("sources", []), "source_entries": scope.get("source_entries", [])}, indent=2),
        encoding="utf-8",
    )
    paths.append(sources_path)

    return paths
