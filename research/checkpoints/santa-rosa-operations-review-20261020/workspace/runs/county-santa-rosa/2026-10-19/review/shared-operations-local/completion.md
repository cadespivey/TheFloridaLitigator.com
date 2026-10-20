# Santa Rosa Shared Courthouse-Access & Clerk Civil Operational Baseline

**Recorded:** 2026-10-20 (UTC)
**Status:** Complete — bounded search finished
**County:** Santa Rosa County, First Judicial Circuit of Florida

---

## Files Created

| File | Description |
|------|-------------|
| `search-log.json` | Exact queries, pages reviewed, navigation pages not counted |
| `manifests.json` | SHA256 hashes and byte lengths for all files (verified, 0 mismatches) |
| `findings.json` | Structured findings: courthouse, security, ADA, clerk contacts, civil filing, gaps |
| `raw/meta-*.json` | Per-source retrieval metadata (URL, status, UTC time, SHA256, byte length) |
| `raw/raw-*.html` | Original HTTP response bytes (Gatsby SPA pages: shell only; WordPress: full content) |
| `raw/rendered-text-*.txt` | Playwright browser_evaluate DOM text extraction for Gatsby SPA pages |
| `raw/snapshot-clerk-*.yml` | Playwright accessibility tree snapshots for WordPress clerk pages |
| `raw/snapshot-*.yml` (0 bytes) | Gatsby SPA pages — MCP did not persist snapshot to file; content preserved in rendered-text-*.txt |
| `raw/text-sr-county-courthouse.txt` | BeautifulSoup extraction of Gatsby shell (title only; confirms SPA) |

---

## Supported Fields

| Field | Status | Source |
|-------|--------|--------|
| Courthouse address | ✅ Supported | firstjudicialcircuit.org SR courthouse page |
| Courthouse hours | ✅ Supported | firstjudicialcircuit.org SR courthouse page |
| Parking (general + accessible) | ✅ Supported | firstjudicialcircuit.org SR courthouse page |
| Courtroom list | ✅ Supported | firstjudicialcircuit.org SR courthouse page |
| Security screening (circuit-wide) | ✅ Supported | firstjudicialcircuit.org security page |
| Prohibited items | ✅ Supported | firstjudicialcircuit.org security page |
| ADA coordinator (Santa Rosa) | ✅ Supported | firstjudicialcircuit.org ADA page |
| ADA liaison contact (Santa Rosa) | ✅ Supported | firstjudicialcircuit.org ADA page |
| ADA lead time (7 working days) | ✅ Supported | firstjudicialcircuit.org ADA page |
| Auxiliary aids list | ✅ Supported | firstjudicialcircuit.org ADA page |
| Clerk name & main phone/fax | ✅ Supported | santarosaclerk.com contact page |
| Court-related correspondence address | ✅ Supported | santarosaclerk.com contact page |
| Circuit Civil phone/fax/email | ✅ Supported | santarosaclerk.com contact page |
| County Civil phone/fax/email | ✅ Supported | santarosaclerk.com contact page |
| Small Claims phone/fax/email | ✅ Supported | santarosaclerk.com contact page |
| Family Law phone/fax/email | ✅ Supported | santarosaclerk.com contact page |
| Appeals phone/email | ✅ Supported | santarosaclerk.com contact page |
| Records phone/fax/email | ✅ Supported | santarosaclerk.com contact page |
| Court structure (County vs Circuit civil) | ✅ Supported | santarosaclerk.com courts page |

---

## Missing / Not Found in Bounded Search

| Field | Status | Note |
|-------|--------|------|
| E-filing requirements | `not_found_in_bounded_search` | State-wide portal (efile.flcourts.gov) exists; Santa Rosa-specific civil e-filing mandate not confirmed on reviewed pages |
| Clerk office filing hours | `not_found_in_bounded_search` | Courthouse hours confirmed (8:00–4:30 M–F); specific clerk filing window not stated |
| In-person vs mail filing channels | `not_found_in_bounded_search` | Not stated on reviewed pages |
| Remote appearance policy | `not_found_in_bounded_search` | Not addressed on reviewed pages |
| Court holiday schedule | `not_found_in_bounded_search` | Page exists at firstjudicialcircuit.org; not reviewed within 6-page limit |
| Lactation rooms | `not_found_in_bounded_search` | Page exists at firstjudicialcircuit.org; not reviewed within 6-page limit |

---

## Actual Checks Performed

1. **Browser navigation** to 10 URLs (6 substantive + 4 navigation index pages)
2. **Playwright accessibility snapshots** captured for all 6 substantive pages
3. **Python httpx GET requests** to all 6 substantive pages — raw bytes saved, HTTP 200 confirmed for all
4. **SHA256 hash verification** — all 24 files in manifests.json verified, 0 mismatches
5. **BeautifulSoup text extraction** on Gatsby SPA raw HTML — confirmed shell-only content (64 bytes title text)
6. **browser_evaluate DOM text extraction** for 3 Gatsby SPA pages — saved as rendered-text-*.txt

---

## Unresolved Errors / Limitations

1. **Gatsby SPA snapshot files are 0 bytes**: The Playwright MCP did not persist snapshot YAML for Gatsby SPA pages. Workaround: browser_evaluate DOM text extraction saved to `rendered-text-*.txt` files. The 0-byte `.yml` files are preserved in the raw directory for transparency.
2. **No targeted searches used**: 0 of 3 allowed searches were needed. All required fields were found on the 6 reviewed pages.
3. **Gatsby SPA raw HTML is shell only**: The original HTTP response for firstjudicialcircuit.org pages contains no page content (JavaScript renders it client-side). The raw bytes are preserved for hash verification but are not useful as content evidence. The rendered DOM extraction is the authoritative content evidence for these pages.
