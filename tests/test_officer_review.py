"""The nonjudge branch must not silently skip individual procedure checks."""
import copy
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("officer_review", Path(__file__).parents[1] / "scripts/officer_review.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture
def receipt(monkeypatch):
    # Binding integrity remains tested by research/history tests and live save.
    # These unit tests isolate the added role/procedure requirements.
    monkeypatch.setattr(module, "_person", lambda *a, **kw: None)
    monkeypatch.setattr(module, "_citation", lambda *a, **kw: None)
    return dict(entity_type="general_magistrate", person_key="officer-one",
                task_id="person-officer-one", status="complete",
                fields={k: dict(status="verified", value=v, citation={}) for k, v in
                        [("assistant_name", "A Person"), ("assistant_contact", "954-555-0100"),
                         ("assistant_role", "Administrative Assistant")]},
                procedure=dict(status="verified", applies_to="officer-one", citation={},
                               documents=[dict(citation={}, applicability="Division 98",
                                               content_review_status="reviewed")]),
                checklist=[dict(review_status="reviewed", summary="Email Word orders", citations=[{}])],
                governing_rules=[dict(citation={})])


@pytest.mark.parametrize("role", ["general_magistrate", "hearing_officer"])
def test_preserves_nonjudge_identity(receipt, role):
    receipt["entity_type"] = role
    before = copy.deepcopy(receipt)
    module.validate_officer(Path.cwd(), receipt)
    assert receipt == before


@pytest.mark.parametrize("path,value", [
    (("entity_type",), "judge"),
    (("task_id",), "person-neighbor"),
    (("status",), "incomplete"),
    (("procedure", "applies_to"), "neighbor"),
    (("procedure", "status"), "collected"),
    (("procedure", "documents"), []),
    (("checklist",), []),
    (("governing_rules",), []),
    (("fields", "assistant_role", "value"), ""),
])
def test_rejects_missing_review_or_wrong_association(receipt, path, value):
    target = receipt
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        module.validate_officer(Path.cwd(), receipt)


def test_calls_real_binding_hooks_for_all_required_evidence(receipt, monkeypatch):
    calls = []
    monkeypatch.setattr(module, "_person", lambda root, r, **kw: calls.append(("person", kw)))
    monkeypatch.setattr(module, "_citation", lambda root, c: calls.append(("citation", c)))
    module.validate_officer(Path.cwd(), receipt)
    assert calls[0] == ("person", {"trial": False})
    assert len([c for c in calls if c[0] == "citation"]) == 7


def unpublished_name():
    return dict(status="not_published", value=None, published_value="TBD",
                absence_reason="Official profile publishes a placeholder, not a name",
                citation={"quote": "Administrative Assistant: TBD"},
                search_log=[dict(url="https://example.gov/profile", search="assistant name",
                                 result="TBD; roster and official search yielded no name")])


def test_documented_unpublished_name_preserves_unknown(receipt):
    receipt["fields"]["assistant_name"] = unpublished_name()
    before = copy.deepcopy(receipt)
    module.validate_officer(Path.cwd(), receipt)
    assert receipt == before
    assert receipt["fields"]["assistant_name"]["value"] is None


@pytest.mark.parametrize("value", ["TBD", " tBd ", "Unknown", "N/A", "To be determined", 123])
def test_placeholder_is_not_a_verified_name(receipt, value):
    receipt["fields"]["assistant_name"]["value"] = value
    with pytest.raises(ValueError, match="placeholder"):
        module.validate_officer(Path.cwd(), receipt)


@pytest.mark.parametrize("changes", [
    {"value": "A guessed name"}, {"absence_reason": ""}, {"search_log": []},
    {"search_log": ["searched"]},
    {"search_log": [dict(url="https://example.gov", search="name")]},
    {"search_log": [dict(url="not a URL", search="name", result="none")]},
    {"published_value": "Vacant"}, {"published_value": ""},
])
def test_unpublished_name_requires_negative_evidence(receipt, changes):
    receipt["fields"]["assistant_name"] = unpublished_name() | changes
    with pytest.raises(ValueError):
        module.validate_officer(Path.cwd(), receipt)


def test_unpublished_name_still_validates_citation(receipt, monkeypatch):
    receipt["fields"]["assistant_name"] = unpublished_name()
    def reject(root, citation):
        raise ValueError("broken source binding")
    monkeypatch.setattr(module, "_citation", reject)
    with pytest.raises(ValueError, match="broken source binding"):
        module.validate_officer(Path.cwd(), receipt)


def negative_procedure():
    return dict(status="no_published_procedure_located",
                applies_to="officer-one", citation={},
                absence_reason="Profile publishes contacts only; bounded official sources searched publish no individual procedure",
                documents=[],
                search_log=[dict(url="https://example.gov/profile",
                                 search="procedure paragraphs and forms links",
                                 result="no individual procedure content or links"),
                            dict(url="https://example.gov/roster",
                                 search="individual procedure page for this officer",
                                 result="roster links shared table only; no individual procedure page")])


def test_negative_procedure_accepted_without_mutation(receipt):
    receipt["procedure"] = negative_procedure()
    receipt["source_inventory_note"] = "Shared sources recorded separately in governing_rules"
    before = copy.deepcopy(receipt)
    module.validate_officer(Path.cwd(), receipt)
    assert receipt == before
    assert receipt["procedure"]["documents"] == []


@pytest.mark.parametrize("path,value", [
    (("procedure", "status"), "collected"),
    (("procedure", "status"), ""),
    (("procedure", "applies_to"), "neighbor"),
    (("procedure", "absence_reason"), ""),
    (("procedure", "absence_reason"), None),
    (("procedure", "search_log"), []),
    (("procedure", "search_log"), None),
    (("procedure", "search_log"), ["checked the profile"]),
    (("procedure", "search_log"), [dict(url="https://example.gov", search="procedure")]),
    (("procedure", "search_log"), [dict(url="https://example.gov", result="none")]),
    (("procedure", "search_log"), [dict(search="procedure", result="none")]),
    (("procedure", "search_log"), [dict(url="not a URL", search="procedure", result="none")]),
    (("procedure", "search_log"), [dict(url="ftp://example.gov", search="procedure", result="none")]),
    (("procedure", "search_log"), [dict(url="https://", search="procedure", result="none")]),
    (("procedure", "search_log"), [dict(url="http:// ", search="procedure", result="none")]),
    (("procedure", "search_log"), [dict(url="https://example.gov", search="  ", result="none")]),
    (("procedure", "search_log"), [dict(url="https://example.gov", search="procedure", result="   ")]),
    (("procedure", "search_log"), [dict(url="https://example.gov", search="procedure", result="none"), 42]),
])
def test_negative_procedure_rejects_weak_or_wrong_evidence(receipt, path, value):
    receipt["procedure"] = negative_procedure()
    target = receipt
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        module.validate_officer(Path.cwd(), receipt)


def test_negative_procedure_rejects_missing_citation(receipt):
    receipt["procedure"] = negative_procedure()
    del receipt["procedure"]["citation"]
    with pytest.raises(ValueError):
        module.validate_officer(Path.cwd(), receipt)


def test_negative_procedure_still_calls_citation_binding(receipt, monkeypatch):
    receipt["procedure"] = negative_procedure()
    calls = []
    monkeypatch.setattr(module, "_person", lambda *a, **kw: None)
    monkeypatch.setattr(module, "_citation", lambda root, c: calls.append(c))
    module.validate_officer(Path.cwd(), receipt)
    # 3 assistant fields + 1 procedure + 1 checklist + 1 governing rule; no documents.
    assert len(calls) == 6
    assert negative_procedure()["citation"] in calls


def test_negative_procedure_rejects_borrowed_documents_without_binding(receipt):
    receipt["procedure"] = negative_procedure()
    receipt["procedure"]["documents"] = [dict(citation={}, applicability="Division Z-2")]
    with pytest.raises(ValueError, match="documents must be empty"):
        module.validate_officer(Path.cwd(), receipt)


def test_negative_procedure_rejects_positive_document_inventory(receipt):
    receipt["procedure"] = negative_procedure()
    receipt["procedure"]["documents"] = [dict(
        citation={}, applicability="officer-one", content_review_status="reviewed")]
    with pytest.raises(ValueError, match="documents must be empty"):
        module.validate_officer(Path.cwd(), receipt)
