"""Resolve one person's links from a retained Broward grid roster; never fetch.

This adapter deliberately supports the court's abcfslItemCntrGridB markup only.
Changed markup, absent people and duplicate full-name/division matches fail closed.
Original hrefs are retained beside URLs resolved against the actual source URL.
"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup


def _tokens(value):
    return tuple(re.findall(r"[^\W_]+", value.casefold()))


def _http_url(value):
    parts = urlsplit(value)
    if parts.scheme not in {"https", "http"} or not parts.hostname:
        raise ValueError("Expected an absolute HTTP(S) URL")
    return value


def resolve_person(html, source_url, name, division):
    """Return one exact normalized full-name/division match or raise ValueError."""
    _http_url(source_url)
    if not _tokens(name) or not division.strip():
        raise ValueError("A full name and division are required")
    soup = BeautifulSoup(html, "html.parser")
    matches = []
    for row in soup.select(".abcfslItemCntrGridB"):
        heading = row.select_one("h3")
        field = row.select_one(".LT-F6")
        if heading is None or field is None:
            continue
        actual_name = heading.get_text(" ", strip=True)
        actual_division = re.sub(
            r"^Division\s*:\s*", "", field.get_text(" ", strip=True), flags=re.I
        )
        if _tokens(actual_name) == _tokens(name) and actual_division.casefold() == division.strip().casefold():
            matches.append((row, actual_name, actual_division))
    if len(matches) != 1:
        raise ValueError(f"Expected one exact name/division match; found {len(matches)}")
    row, actual_name, actual_division = matches[0]
    links = []
    for anchor in row.select("a[href]"):
        original = anchor["href"]
        if not original.strip():
            raise ValueError("Empty href in selected roster row")
        links.append({
            "label": anchor.get_text(" ", strip=True),
            "original_href": original,
            "resolved_url": _http_url(urljoin(source_url, original.strip())),
        })
    labels = {x["label"] for x in links}
    if not {"Biography", "Division Procedures"} <= labels:
        raise ValueError("Selected row lacks Biography or Division Procedures link")
    return {"source_url": source_url, "name": actual_name,
            "division": actual_division, "links": links}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Retained original HTML file")
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--division", required=True)
    args = parser.parse_args()
    try:
        result = resolve_person(args.html.read_bytes(), args.source_url, args.name, args.division)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
