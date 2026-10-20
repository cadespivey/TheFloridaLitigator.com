"""Validate a magistrate/hearing-officer receipt without relabeling it a judge.

The legacy person validator checks office fields for nonjudges but does not
check their procedures. This supplement preserves that validator and explicitly
checks the procedure association, assistant role, checklist and shared rules.
It validates structure and evidence bindings, not legal accuracy or completeness.

Procedure contract:
- ``status="verified"`` requires the exact person association, a real citation
  and a nonempty document inventory whose entries carry applicability, review
  scope and their own citations.
- ``status="no_published_procedure_located"`` is an evidence-backed negative
  finding: a documented absence, not verified instructions. It requires the
  exact person association, a real citation, an absence reason and a nonempty
  structured search log whose rows each carry a real http(s) URL, a search
  term and a result. Documents must be empty when nothing was located; a
  source-only inventory belongs in a separate field (for example
  ``governing_rules``), never as fabricated procedure documents.
- Any other status is rejected. The method never mutates the receipt, never
  converts a status, and never invents instruction content.
"""
from flwu.research import _citation, _person
from urllib.parse import urlsplit


def _assistant_name(field):
    """A completed search can leave the name unknown; never name a placeholder."""
    if field.get("status") == "not_published":
        log = field.get("search_log")
        if field.get("value") is not None or not field.get("absence_reason"):
            raise ValueError("Unpublished assistant name needs null value and reason")
        if not isinstance(log, list) or not log or any(
            not isinstance(item, dict)
            or not isinstance(item.get("url"), str)
            or not item["url"].startswith(("https://", "http://"))
            or not item.get("search") or not item.get("result")
            for item in log
        ):
            raise ValueError("Unpublished assistant name needs checked URLs, terms and results")
        published = field.get("published_value")
        if published is not None and (
            not isinstance(published, str) or not published.strip()
            or published not in field.get("citation", {}).get("quote", "")
        ):
            raise ValueError("Published assistant placeholder is not in cited source")
        return
    value = field.get("value")
    if (field.get("status") != "verified" or not isinstance(value, str)
            or not value.strip() or value.strip().casefold() in
            {"tbd", "unknown", "n/a", "none", "vacant", "not published", "to be determined"}):
        raise ValueError("Assistant name is unverified or a placeholder")


def _negative_search_log(log, what):
    """A documented absence needs checked rows {url, search, result} with real URLs."""
    if not isinstance(log, list) or not log:
        raise ValueError(what + " needs a nonempty structured search log")
    for item in log:
        if not isinstance(item, dict):
            raise ValueError(what + " search log rows need url, search and result")
        url = item.get("url")
        if (not isinstance(url, str) or any(c.isspace() for c in url)
                or urlsplit(url).scheme not in {"http", "https"}
                or not urlsplit(url).hostname):
            raise ValueError(what + " search log rows need real http(s) URLs")
        if not isinstance(item.get("search"), str) or not item["search"].strip():
            raise ValueError(what + " search log rows need a search term")
        if not isinstance(item.get("result"), str) or not item["result"].strip():
            raise ValueError(what + " search log rows need a result")


def _check_documents(root, procedure):
    for document in procedure.get("documents") or []:
        if not document.get("applicability") or not document.get("content_review_status"):
            raise ValueError("Procedure needs applicability and review scope")
        _citation(root, document["citation"])


def validate_officer(root, receipt):
    role = receipt.get("entity_type")
    if role not in {"general_magistrate", "hearing_officer"}:
        raise ValueError("Expected a general_magistrate or hearing_officer")
    key = receipt.get("person_key")
    if not key or receipt.get("task_id") != "person-" + key:
        raise ValueError("Officer task/person identity mismatch")
    if receipt.get("status") != "complete":
        raise ValueError("Officer review is not complete")
    _person(root, receipt, trial=False)
    for name in ("assistant_name", "assistant_contact", "assistant_role"):
        field = receipt["fields"][name]
        if name == "assistant_name":
            _assistant_name(field)
        elif field.get("status") != "verified" or not field.get("value"):
            raise ValueError("Unverified assistant field: " + name)
        _citation(root, field["citation"])
    procedure = receipt["procedure"]
    status = procedure.get("status")
    if status not in {"verified", "no_published_procedure_located"}:
        raise ValueError("Officer procedure status must be verified or no_published_procedure_located")
    if procedure.get("applies_to") != key:
        raise ValueError("Officer procedure belongs to another person")
    if "citation" not in procedure:
        raise ValueError("Officer procedure needs a source citation")
    _citation(root, procedure["citation"])
    if status == "verified":
        if not procedure.get("documents"):
            raise ValueError("Verified officer procedure inventory is empty")
        _check_documents(root, procedure)
    else:
        # Evidence-backed absence: a negative finding is not verified content.
        reason = procedure.get("absence_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Negative officer procedure needs an absence reason")
        _negative_search_log(procedure.get("search_log"), "Negative officer procedure")
        if procedure.get("documents") != []:
            raise ValueError("Negative officer procedure documents must be empty")
    if not receipt.get("checklist") or not receipt.get("governing_rules"):
        raise ValueError("Officer needs a checklist and governing-rule evidence")
    for item in receipt["checklist"]:
        if item.get("review_status") != "reviewed" or not item.get("summary") or not item.get("citations"):
            raise ValueError("Checklist item is not reviewed and supported")
        for citation in item["citations"]:
            _citation(root, citation)
    for rule in receipt["governing_rules"]:
        _citation(root, rule["citation"])
