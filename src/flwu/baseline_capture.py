"""Bounded evidence-checkpoint helper for the Florida county baseline.

This is a *save* helper, not a workflow engine. It validates one research
checkpoint packet and stores it in the research-history database through
:mod:`flwu.history`. It preserves the source material a researcher already has
(raw bytes, extracted text, hashes, retrieval times, the reviewed findings and
the still-open checks) so that work survives across sessions and can later be
compared against a finalized baseline.

What it validates is **structural source preservation only**. It never claims
source authenticity or legal accuracy, and it never finalizes a report: every
checkpoint it accepts has ``status == "incomplete"`` (reviewed judges saved
within an unfinished county). It uses the existing research-history schema and
rejects the frozen operational database. Callers must use disposable databases
for trials; a filename alone cannot identify whether a database is live.

Required researcher distinctions (see ``docs/workflow/BASELINE_CAPTURE.md``):

* **researched** — the researcher actually collected/checked a source; that is
  what a packet's artifacts, checks and findings record.
* **saved** — the validated snapshot now lives in the research-history DB.
* **reviewed** — a finding is a reviewed item; the open checks are *not*
  reviewed yet. Saving a checkpoint is not reviewing or finalizing it.

The packet is validated entirely **before** the database is opened, so an
invalid packet creates no DB file and performs no write.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qsl, urlparse

from flwu import history

_PROFILE = "county-baseline-v1"
_MODES = ("manual_research", "synthetic_replay")
_TOP_KEYS = ("stream", "scope", "run_id", "payload", "artifacts")
_SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
_COUNTY_RE = re.compile(r"[a-z]+(?:_[a-z]+)*\Z")
_SECRET_TOKENS = {
    "key", "apikey", "token", "secret", "password", "passwd", "pwd", "auth",
    "authorization", "credential", "credentials", "session", "sessionid",
    "cookie", "jwt", "bearer", "signature", "access", "accesskey", "secretkey",
    "accesstoken", "refreshtoken", "authtoken", "sessiontoken", "clientsecret",
}


class BaselineCaptureError(ValueError):
    """A checkpoint packet failed structural validation before any DB write."""


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def _aware_utc(value, field):
    """Reuse :func:`flwu.history.stamp` to require a timezone-aware timestamp."""
    try:
        normalized = history.stamp(value)
    except (ValueError, AttributeError, TypeError) as exc:
        raise BaselineCaptureError(f"{field} must be a timezone-aware timestamp, got {value!r}") from exc
    return datetime.fromisoformat(normalized)


def _not_in_future(dt_utc, value, field):
    if dt_utc > datetime.now(timezone.utc):
        raise BaselineCaptureError(f"{field} is in the future")


def _validate_url(url, *, is_live):
    """Public http(s) only; no embedded credentials; no secret-bearing query params.

    For a live (manual_research) citation a synthetic ``.invalid`` host is also
    rejected so a synthetic/test citation cannot be relabeled as live.
    """
    if not isinstance(url, str) or not url:
        raise BaselineCaptureError("citation url must be a nonempty string")
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or '').lower().rstrip('.')
        parsed.port  # Validate malformed/out-of-range ports, without fetching.
    except ValueError:
        raise BaselineCaptureError("citation url is malformed") from None
    if parsed.scheme not in ("http", "https") or not host or any(c.isspace() for c in url):
        raise BaselineCaptureError("citation url must be public http(s)")
    if parsed.username is not None:
        raise BaselineCaptureError("citation url embeds credentials")
    for name, _value in parse_qsl(parsed.query, keep_blank_values=True):
        separated = re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()
        tokens = [t for t in re.split(r"[^a-z0-9]+", separated) if t]
        if any(tok in _SECRET_TOKENS for tok in tokens):
            raise BaselineCaptureError("citation url has a secret-bearing query parameter")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        # Reject local/reserved suffixes and numeric alternate IP spellings.
        if ('.' not in host or host.endswith(('.localhost', '.local', '.internal', '.test', '.example'))
                or not re.fullmatch(r'[a-z0-9.-]+', host)
                or any(not label or label.startswith('-') or label.endswith('-') for label in host.split('.'))
                or not re.search(r'[a-z]', host.split('.')[-1])):
            raise BaselineCaptureError("citation url host is not public")
    else:
        if not address.is_global or address.is_multicast:
            raise BaselineCaptureError("citation url address is not public")
    if is_live and host.endswith('.invalid'):
        raise BaselineCaptureError("live citation may not use a synthetic .invalid host")


def _validate_citation(cite, *, artifacts_bytes, artifacts_keys, is_live, where):
    """Validate one finding/draft citation against the provided artifacts."""
    if not isinstance(cite, dict):
        raise BaselineCaptureError(f"{where}: citation must be an object")
    raw_sha = cite.get("sha256")
    if not isinstance(raw_sha, str) or raw_sha not in artifacts_keys:
        raise BaselineCaptureError(f"{where}: citation raw sha256 {raw_sha!r} is not a provided artifact")
    text_sha = cite.get("text_sha256")
    if not isinstance(text_sha, str) or text_sha not in artifacts_keys:
        raise BaselineCaptureError(f"{where}: citation extracted-text sha256 {text_sha!r} is not a provided artifact")
    quote = cite.get("quote")
    if not isinstance(quote, str) or not quote.strip():
        raise BaselineCaptureError(f"{where}: citation quote must be a nonempty string")
    locator = cite.get("locator")
    if not isinstance(locator, str) or not locator.strip():
        raise BaselineCaptureError(f"{where}: citation locator must be a nonempty string")
    try:
        extracted = artifacts_bytes[text_sha].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BaselineCaptureError(f"{where}: extracted text {text_sha} is not valid UTF-8") from exc
    if quote not in extracted:
        raise BaselineCaptureError(f"{where}: citation quote is not an exact substring of the extracted text")
    _validate_url(cite.get("url"), is_live=is_live)
    if 'resolved_url' in cite:
        _validate_url(cite['resolved_url'], is_live=is_live)
    retrieved_at = cite.get("retrieved_at")
    if not isinstance(retrieved_at, str):
        raise BaselineCaptureError(f"{where}: citation retrieved_at must be a string")
    _not_in_future(_aware_utc(retrieved_at, "citation retrieved_at"), retrieved_at, "citation retrieved_at")
    if is_live:
        if cite.get("synthetic") is not False:
            raise BaselineCaptureError(f"{where}: a live citation requires explicit synthetic=false")
        if cite.get("authority") != "official":
            raise BaselineCaptureError(f"{where}: a live citation requires authority 'official'")
    elif cite.get('synthetic') is not True:
        raise BaselineCaptureError(f"{where}: synthetic replay requires explicit synthetic=true")
    if cite.get('http_status') is None and 'browser_capture' in cite:
        # Native Save Page Source does not expose a response status. Preserve
        # that unknown instead of inventing 200; require a separate review record.
        capture = cite['browser_capture']
        if not isinstance(capture, dict):
            raise BaselineCaptureError(f"{where}: invalid browser capture")
        receipt_sha = capture.get('observation_sha256')
        try:
            receipt = json.loads(artifacts_bytes[receipt_sha])
        except (KeyError, TypeError, ValueError, UnicodeDecodeError):
            raise BaselineCaptureError(f"{where}: missing/invalid browser observation artifact") from None
        if not isinstance(receipt, dict) or not (
            receipt.get('method') in ('native_browser_save_page_source', 'native_browser_save_pdf')
            and receipt.get('content_reviewed') is True
            and receipt.get('page_url') == cite.get('resolved_url', cite['url'])
            and receipt.get('original_sha256') == raw_sha
            and receipt.get('observed_at') == retrieved_at
            and isinstance(receipt.get('page_title'), str)
            and receipt['page_title'].strip()
            and isinstance(receipt.get('review_note'), str)
            and receipt['review_note'].strip()
        ):
            raise BaselineCaptureError(f"{where}: browser observation does not match source")
        raw = artifacts_bytes[raw_sha]
        if receipt['method'] == 'native_browser_save_pdf':
            from io import BytesIO
            from pypdf import PdfReader
            try:
                if not raw.startswith(b'%PDF-') or not PdfReader(BytesIO(raw), strict=True).pages:
                    raise ValueError('missing PDF pages')
            except Exception as exc:
                raise BaselineCaptureError(f"{where}: browser source must be a readable saved PDF") from exc
        elif b'<html' not in raw.lower() or b'</html>' not in raw.lower():
            raise BaselineCaptureError(f"{where}: browser source must be saved HTML")
    elif cite.get('http_status') != 200:
        raise BaselineCaptureError(f"{where}: a supporting citation requires HTTP 200")


def _resolve_artifact(root_resolved, rel_path, sha_key):
    """Read one artifact inside the capture root, rejecting escape and traversal.

    Returns the file bytes. The resolved target must stay inside ``root`` so a
    symlink cannot point outside; the content must hash to ``sha_key``.
    """
    if not isinstance(rel_path, str) or not rel_path:
        raise BaselineCaptureError(f"artifact {sha_key}: path must be a nonempty string")
    if Path(rel_path).is_absolute() or rel_path.startswith(("/", "\\")):
        raise BaselineCaptureError(f"artifact {sha_key}: absolute path {rel_path!r} is not allowed")
    if "\\" in rel_path:
        raise BaselineCaptureError(f"artifact {sha_key}: backslash in path {rel_path!r} is not allowed")
    if ".." in PurePosixPath(rel_path).parts:
        raise BaselineCaptureError(f"artifact {sha_key}: path {rel_path!r} escapes the capture root")
    candidate = root_resolved / rel_path
    component = root_resolved
    for part in PurePosixPath(rel_path).parts:
        component = component / part
        if component.is_symlink():
            raise BaselineCaptureError(f"artifact {sha_key}: symlink traversal is not allowed")
    try:
        resolved = candidate.resolve()
    except (OSError, RuntimeError) as exc:
        raise BaselineCaptureError(f"artifact {sha_key}: cannot resolve {rel_path!r}: {exc}") from exc
    if not resolved.is_relative_to(root_resolved):
        raise BaselineCaptureError(f"artifact {sha_key}: path {rel_path!r} resolves outside the capture root (symlink traversal)")
    if not resolved.is_file():
        raise BaselineCaptureError(f"artifact {sha_key}: {rel_path!r} is not a regular file")
    data = resolved.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha_key:
        raise BaselineCaptureError(f"artifact {sha_key}: sha256 mismatch for {rel_path!r}")
    return data


def _iter_ref_dicts(value):
    """Yield every dict in ``value`` carrying a raw or extracted-text sha ref.

    Used to catch a raw/text reference hidden anywhere in facts or drafts so no
    unsupported reference can bypass the artifact check.
    """
    if isinstance(value, dict):
        if "sha256" in value or "text_sha256" in value:
            yield value
        for child in value.values():
            yield from _iter_ref_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_ref_dicts(child)


def _load_packet(packet_path):
    path = Path(packet_path)
    if not path.is_file():
        raise BaselineCaptureError(f"packet {packet_path} is not a file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise BaselineCaptureError(f"cannot read packet {packet_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise BaselineCaptureError(f"packet {packet_path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise BaselineCaptureError("packet must be a JSON object")
    keys = set(data.keys())
    if keys != set(_TOP_KEYS):
        missing = sorted(set(_TOP_KEYS) - keys)
        extra = sorted(keys - set(_TOP_KEYS))
        raise BaselineCaptureError(
            f"packet must have exactly the top-level keys {list(_TOP_KEYS)}; missing={missing} extra={extra}"
        )
    return data


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

def save_checkpoint(root, packet_path, db_path):
    """Validate a checkpoint packet and save it via :func:`flwu.history.record`.

    ``root`` is the directory containing the original/extracted artifact files;
    ``packet_path`` is the checkpoint JSON; ``db_path`` is the research-history
    database. All validation runs before the database is opened, so an invalid
    packet creates no file and performs no write. Returns the capture
    acknowledgment plus the resolved database path.
    """
    root_p = Path(root).expanduser()
    if not root_p.is_dir():
        raise BaselineCaptureError(f"capture root {root} is not a directory")
    root_resolved = root_p.resolve()
    db_resolved = Path(db_path).expanduser().resolve()

    packet = _load_packet(packet_path)
    stream = packet["stream"]
    scope = packet["scope"]
    run_id = packet["run_id"]
    payload = packet["payload"]
    artifacts_map = packet["artifacts"]

    # -- scalar / type guards ------------------------------------------------
    if not isinstance(stream, str) or not stream:
        raise BaselineCaptureError("stream must be a nonempty string")
    if not isinstance(scope, dict):
        raise BaselineCaptureError("scope must be an object")
    if not isinstance(run_id, str) or not run_id:
        raise BaselineCaptureError("run_id must be a nonempty string (a stable caller identifier)")
    if not isinstance(payload, dict):
        raise BaselineCaptureError("payload must be an object")
    if not isinstance(artifacts_map, dict):
        raise BaselineCaptureError("artifacts must be an object mapping sha256 to a relative path")

    # -- scope ---------------------------------------------------------------
    if scope.get("profile") != _PROFILE:
        raise BaselineCaptureError(f"scope.profile must be {_PROFILE!r}")
    county = scope.get("county")
    if not isinstance(county, str) or not _COUNTY_RE.fullmatch(county):
        raise BaselineCaptureError(f"scope.county must be a lowercase county slug, got {county!r}")
    circuit = scope.get("circuit")
    if isinstance(circuit, bool) or not isinstance(circuit, int) or not (1 <= circuit <= 20):
        raise BaselineCaptureError(f"scope.circuit must be an integer from 1 to 20, got {circuit!r}")

    # -- payload contract / mode / status -----------------------------------
    contract = payload.get("contract")
    if not isinstance(contract, dict):
        raise BaselineCaptureError("payload.contract must be an object")
    mode = contract.get("mode")
    if mode not in _MODES:
        raise BaselineCaptureError(
            "payload.contract.mode must be 'manual_research' or 'synthetic_replay' (explicitly pinned)"
        )
    is_live = mode == "manual_research"
    if payload.get("status") != "incomplete":
        raise BaselineCaptureError(
            "this helper only saves incomplete checkpoints (unfinished county); status must be 'incomplete'"
        )

    # -- stream must be derived from mode + scope ---------------------------
    expected_stream = f"{mode}:{_PROFILE}:{history.sha(scope)[:12]}"
    if stream != expected_stream:
        raise BaselineCaptureError(f"stream {stream!r} does not match the derived {expected_stream!r}")

    # -- artifacts: paths, hash integrity, no escape/symlink traversal ------
    artifacts_bytes = {}
    for sha_key, rel_path in artifacts_map.items():
        if not isinstance(sha_key, str) or not _SHA_RE.fullmatch(sha_key):
            raise BaselineCaptureError(f"artifact key {sha_key!r} is not a lowercase sha256 hex string")
        artifacts_bytes[sha_key] = _resolve_artifact(root_resolved, rel_path, sha_key)
    artifacts_keys = set(artifacts_bytes)

    # -- checks --------------------------------------------------------------
    checks = payload.get("checks")
    if not isinstance(checks, list):
        raise BaselineCaptureError("payload.checks must be a list")
    seen_check_ids = set()
    incomplete_count = 0
    for i, check in enumerate(checks):
        where = f"checks[{i}]"
        if not isinstance(check, dict):
            raise BaselineCaptureError(f"{where}: must be an object")
        cid = check.get("id")
        if not isinstance(cid, str) or not cid:
            raise BaselineCaptureError(f"{where}: id must be a nonempty string")
        if cid in seen_check_ids:
            raise BaselineCaptureError(f"{where}: duplicate check id {cid!r}")
        seen_check_ids.add(cid)
        status = check.get("status")
        if status not in ("verified", "incomplete"):
            raise BaselineCaptureError(f"{where}: status must be 'verified' or 'incomplete'")
        if status == "incomplete":
            incomplete_count += 1
        else:  # verified
            checked_at = check.get("checked_at")
            if not isinstance(checked_at, str):
                raise BaselineCaptureError(f"{where}: a verified check requires checked_at")
            _not_in_future(_aware_utc(checked_at, f"{where}.checked_at"), checked_at, f"{where}.checked_at")
            hashes = check.get("hashes")
            if not isinstance(hashes, list) or not hashes:
                raise BaselineCaptureError(f"{where}: a verified check requires a nonempty hashes list")
            for h in hashes:
                if not isinstance(h, str) or h not in artifacts_keys:
                    raise BaselineCaptureError(f"{where}: verified check hash {h!r} is not a provided artifact")
    if incomplete_count == 0:
        raise BaselineCaptureError("at least one incomplete check is required to represent the remaining county work")

    # -- findings ------------------------------------------------------------
    findings = payload.get("findings")
    if not isinstance(findings, list):
        raise BaselineCaptureError("payload.findings must be a list")
    seen_finding_keys = set()
    for i, finding in enumerate(findings):
        where = f"findings[{i}]"
        if not isinstance(finding, dict):
            raise BaselineCaptureError(f"{where}: must be an object")
        key = finding.get("key")
        if not isinstance(key, str) or not key:
            raise BaselineCaptureError(f"{where}: key must be a nonempty string")
        if key in seen_finding_keys:
            raise BaselineCaptureError(f"{where}: duplicate finding key {key!r}")
        seen_finding_keys.add(key)
        if not isinstance(finding.get("kind"), str) or not finding.get("kind"):
            raise BaselineCaptureError(f"{where}: kind must be a nonempty string")
        if not isinstance(finding.get("facts"), dict):
            raise BaselineCaptureError(f"{where}: facts must be an object")
        citations = finding.get("citations")
        if not isinstance(citations, list) or not citations:
            raise BaselineCaptureError(f"{where}: findings require nonempty citations")
        for j, cite in enumerate(citations):
            _validate_citation(cite, artifacts_bytes=artifacts_bytes, artifacts_keys=artifacts_keys,
                               is_live=is_live, where=f"{where}.citations[{j}]")

    # -- drafts (unvalidated receipts; never enter reviewed context) --------
    drafts = payload.get("drafts", [])
    if not isinstance(drafts, list):
        raise BaselineCaptureError("payload.drafts must be a list")
    for i, draft in enumerate(drafts):
        where = f"drafts[{i}]"
        if not isinstance(draft, dict):
            raise BaselineCaptureError(f"{where}: must be an object")
        draft_cites = draft.get("citations")
        if draft_cites is not None:
            if not isinstance(draft_cites, list):
                raise BaselineCaptureError(f"{where}: citations must be a list")
            for j, cite in enumerate(draft_cites):
                _validate_citation(cite, artifacts_bytes=artifacts_bytes, artifacts_keys=artifacts_keys,
                                   is_live=is_live, where=f"{where}.citations[{j}]")

    # -- nested raw/text references anywhere in the payload must resolve ----
    for ref in _iter_ref_dicts(payload):
        for field in ("sha256", "text_sha256"):
            if field in ref:
                val = ref[field]
                if not isinstance(val, str) or val not in artifacts_keys:
                    raise BaselineCaptureError(f"unsupported {field} reference {val!r} in payload (not a provided artifact)")

    # Citation-bearing fields are checked at every depth. Inventory entries and
    # image/failed-response metadata need artifact integrity, not invented quotes.
    def validate_nested(value, where='payload'):
        if isinstance(value, dict):
            if 'quote' in value or 'locator' in value:
                _validate_citation(value, artifacts_bytes=artifacts_bytes,
                                   artifacts_keys=artifacts_keys, is_live=is_live, where=where)
            for name, child in value.items():
                if name == 'citation' and child is not None:
                    _validate_citation(child, artifacts_bytes=artifacts_bytes,
                                       artifacts_keys=artifacts_keys, is_live=is_live, where=where+'.citation')
                if name == 'citations':
                    if not isinstance(child, list):
                        raise BaselineCaptureError(f'{where}: citations must be a list')
                    for cite in child:
                        _validate_citation(cite, artifacts_bytes=artifacts_bytes,
                                           artifacts_keys=artifacts_keys, is_live=is_live, where=where+'.citations')
                validate_nested(child, where+'.'+name)
        elif isinstance(value, list):
            for child in value:
                validate_nested(child, where+'[]')
    validate_nested(payload)

    # -- record (transactional; only reached after every check passes) ------
    with history.database(db_resolved) as conn:
        result = history.record(conn, stream=stream, mode=mode, scope=scope, run_id=run_id,
                                payload=payload, artifacts=artifacts_bytes)

    return {
        **result,
        "mode": mode,
        "scope": scope,
        "status": "incomplete",
        "finalized": False,
        "database": str(db_resolved),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="flwu.baseline_capture",
        description="Validate and save a bounded county-baseline evidence checkpoint.",
    )
    parser.add_argument("--root", required=True, help="Capture root containing the original/extracted artifact files.")
    parser.add_argument("--packet", required=True, help="Path to the checkpoint packet JSON.")
    parser.add_argument("--database", required=True, help="Path to the research-history SQLite database.")
    args = parser.parse_args(argv)
    try:
        ack = save_checkpoint(args.root, args.packet, args.database)
    except BaselineCaptureError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1
    except Exception as exc:  # unexpected failure: report, do not bypass
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}), file=sys.stderr)
        return 1
    print(json.dumps(ack, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
