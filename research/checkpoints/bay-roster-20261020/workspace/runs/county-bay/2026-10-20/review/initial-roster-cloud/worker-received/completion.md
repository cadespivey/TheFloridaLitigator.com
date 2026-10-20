# Bay County Initial Roster Discovery — Completion

## Status: Complete (roster/source discovery only)

## Assignment Scope
Collect the initial official Bay County, Florida judicial roster and official
profile/procedure links for later one-person-at-a-time review. Bay belongs to the
Fourteenth Judicial Circuit (14). This is roster/source discovery only, not
individual judge research or county acceptance.

## Pages Reviewed
1. **https://jud14.flcourts.org/judges** — Primary roster page. HTTP 200.
   Retrieved 2026-10-20T18:06:29Z. SHA-256: `91a8defc...057d20`. 62,685 bytes.
2. **https://jud14.flcourts.org/** — Homepage (supplementary). HTTP 200.
   Retrieved 2026-10-20T18:06:52Z. SHA-256: `16a79c5d...b7d605`. 64,480 bytes.

## Observed Counts by Scope

| Category | Count | Notes |
|----------|-------|-------|
| Bay Circuit Court Judges | 11 | All explicitly listed as "Bay" on roster |
| Bay County Court Judges | 5 | All explicitly listed as "Bay" in County Judges section |
| Bay Senior Judges | 1 | Dedee S. Costello |
| **Total Bay-assigned** | **17** | |
| Multi-county (Bay + other) | 2 | Patterson (Bay+Washington), J. Patterson (Bay+Gulf) |
| Non-Bay circuit judges (context) | 3 | Garcia (Jackson), Roberts (Holmes), B. Young (Calhoun+Jackson) |
| Non-Bay county judges (context) | 5 | Grover, McFarland, Taylor, Mercer, Peel |
| Judges with profile links (Bay) | 13 of 17 | Missing: Gay, Mallory, Stephenson, Costello |
| Judges without profile links (Bay) | 4 | Noted with `profile_note` in roster.json |

## Candidates Requiring Later Screening
- **Shonna Young Gay** — no profile link; confirm whether profile exists at alternate URL
- **Peter A. Mallory** — no profile link; confirm whether profile exists
- **Dustin Stephenson** — no profile link; confirm whether profile exists
- **Dedee S. Costello** — no profile link but has procedure PDF; senior judge scope
- **Christopher N. Patterson** — Chief Judge with dual Bay/Washington assignment; circuit-wide authority
- **Jarred Patterson** — dual Bay/Gulf assignment

## Officer/Senior Index
No separate officer/senior index link discovered beyond the Senior Judges table
section on the roster page. The single senior judge (Costello) is the complete
observed senior listing for Bay. No judicial officers (e.g., bankruptcy or
administrative law judges) are listed on this page for the 14th Circuit.

## Original vs Rendered Capture Limitations
- The page is **server-rendered** (no client-side JS modifies the judge table).
- The curl HTTP response is the authoritative source document.
- The browser accessibility snapshot was used for data extraction and matches
  the HTTP content.
- No separate rendered DOM file was stored because the page requires no JS
  rendering to display the judge table. Browser capture timestamp noted in
  `raw/jud14_judges_browser_dom_meta.json`.

## Conflicts or Discrepancies
- None observed. The roster is internally consistent.
- Note: Jarred Patterson appears as "Jarred Patterson" on the roster but the
  profile URL slug is "judge-jarred-h-patterson", implying the full name is
  Jarred H. Patterson. This is recorded but not resolved here.

## First Bay-Assigned Person for Next Bounded Review
**Brantley S. Clark, Jr.** — first circuit judge listed, explicit Bay assignment,
profile link available at https://jud14.flcourts.org/judges/brantley-s-clark-jr.

## Deliverables
- `roster.json` — structured roster (12,132 bytes)
- `sources.json` — source registry (2,023 bytes)
- `manifest.json` — file hashes (1,800 bytes)
- `raw/` — original HTTP evidence + metadata (5 files)
- `text/` — extracted text (1 file)
- `completion.md` — this file

## Stop
Roster discovery complete. No individual judge research, procedure review, or
county acceptance performed. Ready for cloud review and checkpoint.
