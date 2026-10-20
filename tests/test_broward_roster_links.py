"""One-person extraction regression: identity ambiguity and real URL forms."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "broward_roster_links", Path(__file__).parents[1] / "scripts/broward_roster_links.py"
)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def row(name, division, href="//court.example/division-fx/"):
    return f'''<div class="abcfslItemCntrGridB"><h3>{name}</h3>
    <div class="LT-F6"><span>Division:</span><span>{division}</span></div>
    <a href="{href}">Division Procedures</a>
    <a href="../bio/?smid=123">Biography</a></div>'''


def test_exact_person_not_surname_substring_and_relative_links():
    # A substring search for USAN would select SUSAN first.
    html = row("SUSAN L. ALSPECTOR", "FV/57", "/wrong-person/") + row("MICHAEL A. USAN", "FX")
    result = adapter.resolve_person(html, "https://court.example/roster/", "Michael A Usan", "fx")
    assert result["name"] == "MICHAEL A. USAN"
    assert result["division"] == "FX"
    assert result["links"] == [
        {"label": "Division Procedures", "original_href": "//court.example/division-fx/",
         "resolved_url": "https://court.example/division-fx/"},
        {"label": "Biography", "original_href": "../bio/?smid=123",
         "resolved_url": "https://court.example/bio/?smid=123"},
    ]


@pytest.mark.parametrize("html,name,division,count", [
    (row("SUSAN L. ALSPECTOR", "FV/57"), "Michael A Usan", "FX", 0),
    (row("MICHAEL A. USAN", "FP"), "Michael A Usan", "FX", 0),
    (row("MICHAEL A. USAN", "FX") * 2, "Michael A Usan", "FX", 2),
    (row("MICHAEL A. USAN", "FX"), "Usan", "FX", 0),
    ("<div><h3>MICHAEL A. USAN</h3>FX</div>", "Michael A Usan", "FX", 0),
])
def test_ambiguous_missing_or_changed_markup_does_not_guess(html, name, division, count):
    with pytest.raises(ValueError, match=f"found {count}"):
        adapter.resolve_person(html, "https://court.example/", name, division)


@pytest.mark.parametrize("href", ["", "javascript:alert(1)", "mailto:someone@example.test"])
def test_unusable_procedure_destination_rejected(href):
    with pytest.raises(ValueError):
        adapter.resolve_person(row("MICHAEL A. USAN", "FX", href), "https://court.example/", "Michael A Usan", "FX")


def test_missing_required_link_rejected():
    html = row("MICHAEL A. USAN", "FX").replace("Biography", "Other")
    with pytest.raises(ValueError, match="lacks Biography"):
        adapter.resolve_person(html, "https://court.example/", "Michael A Usan", "FX")
