# Website publication contract and operating procedure

The website is a static view of reviewed research snapshots. It does not perform
new legal analysis when a reader changes dates. Its public archive is separate
from the private cumulative research database.

## Reader behavior and design

- Default: the reporting period with the latest end date, then latest start date,
  then latest publication timestamp. Filesystem modification time is irrelevant.
- Date range: inclusive reporting-period overlap, not individual opinion dates.
  Both dates are required. Reversed or invalid dates return an explanatory message.
- Quick date links apply the last 30, 60, 90 or 180 calendar days immediately:
  Through is today in America/New_York; From is today minus N−1 days so the
  inclusive range contains exactly N days. Calculate on each click, including
  month/year/leap-day and DST boundaries. Reuse the date-range route so inputs,
  results, URL, Back/Forward and directory court selection stay synchronized.
- Date controls occupy a subtle shaded band without surrounding divider lines.
  Use equal-width fields and buttons, 14px labels/control text and 44px control
  heights; reflow to two columns, then one on narrow screens. The first report
  heading below this band has no additional top divider.
- Render each selected report's summaries beneath Statutes, Case Law, Procedural
  Rules, and Local Rules. Show the latest publication date once in a compact
  14px line directly below the site description, before the date controls. Do not
  repeat reporting-period labels within sections or entries. Preserve individual
  publication/effective dates. Show individual-period navigation links only when
  multiple periods match. In case-law summaries, bold the line-leading Holding:,
  Disposition: and Author: labels while keeping their following text normal weight.
  Display only deduplicated source links, not quoted-source panels or
  excerpts. Keep quotations in the underlying evidence/archive for validation.
  Links open the original source webpage or exported saved source. Empty sections say no items were
  included; they do not imply complete proof that no law changed.
- Same-period revisions: display the latest published revision in range results;
  retain earlier revisions through `?issue=ID` links. Date ranges use
  `?from=YYYY-MM-DD&to=YYYY-MM-DD`. Reload, Back and Forward preserve selection.
- The personnel directory is a separate `directory.html` page, linked in the top
  masthead beside the site title. Navigation order is Updates, Courts, Personnel
  Directory, Links, About (at the far right). Courts, Personnel Directory and Links are dropdowns;
  CourtListener appears in Links only. The personnel dropdown supplies an all-courts
  view and individual `directory.html?court=GROUP-ID` links.
  Court categories expand into nested menus. County Courts expands into A–F,
  G–L, M–R and S–Z groups, omitting empty groups. County names sort alphabetically;
  circuit courts and DCAs sort numerically. Both menus use the same ordering.
  Menu scope combines packaged registry groups and explicitly reviewed county
  supplements. Presence in navigation is not certification of complete review.
- County resource links are restricted to Official Records, Court Records and
  Tax Assessor, where recorded; retain the court website destination. Additional
  collected resource URLs stay in research data rather than the county menu.
  Official navigation comes from `data/web/courts.json` and supplement court rows.
  General practice links come from `data/web/links.json`. Nested menus support
  keyboard/touch, preserve open ancestors and close the innermost menu on Escape.
- Quick search (`?q=...`) submits from every page to the Updates page. Match every
  whitespace-separated word case-insensitively against saved update title/summary/
  section and current personnel fields. Search uses the latest revision per period
  and current directory supplements, independently of date selection. It does not
  query the private database or live sources. Label personnel results as current;
  link to their row, and link update results to their saved issue and section.
  Show a no-results message. Clear the search query when navigating to court views.
- The directory page uses the newest selected issue's saved snapshot. Selecting
  one older issue shows its saved contacts. Do not
  merge current contacts into historical results. Navigation between Updates and
  Directory preserves the date-range or individual-issue query parameters. The
  update page itself renders only the four research sections.
- Personnel records render as a four-column table: personnel, court/county,
  chambers/office, and judicial assistant. Use one contact datum per line and
  separate address heading, street, and city/state/postal lines. Deduplicate
  repeated values, preserve genuinely distinct contacts and source conflicts,
  and retain original procedure/source evidence in immutable exports. Exact
  source-value presentation mappings must not silently follow changed facts.
  Do not render an Evidence Coverage section on any website page. On narrow
  screens each record becomes labeled rows without horizontal clipping.
  County selections match county assignments; circuit selections show personnel
  serving covered counties in that circuit (including county courts and clerks),
  explicitly described on the page. Appellate selections require `court_ids`
  derived from the saved `roster-supreme` / `roster-dca-N` inventory membership;
  never infer a person's court from a cited appellate opinion. Old exports without
  appellate assignment metadata show a qualified empty view, not invented people.
  Date submission, reset and individual-issue links preserve the court filter.
- Current approved typography: 17px system body, 25px section headings,
  20px Charter/Iowan/Georgia item headings, and 15.5px system directory table text.
  Use the actual responsive CSS as the layout authority. The intro/publication
  date and quick search share a desktop row; below 740px they stack. Footer text
  spans the body container. About prose and its entire creator photo/text block
  share a 68ch maximum width. Preserve the portrait and approved creator wording.
- Use a restrained single column, left alignment, whitespace between paragraphs,
  and plain underlined links. No external fonts, analytics or framework runtime.
  Guidance: Butterick's [line length](https://typographyforlawyers.com/line-length.html),
  [headings](https://typographyforlawyers.com/headings.html),
  [paragraph spacing](https://practicaltypography.com/space-between-paragraphs.html)
  and [browser alignment](https://practicaltypography.com/justified-text.html).

## Prepare one publishable issue

1. Complete the live research runbook. Each included candidate must have an
   explicit `section`: `statutes`, `case_law`, `procedural_rules`, or `local_rules`,
   plus a readable `title`, publication/effective dates, supported claim text and
   complete citations. Choose based on the document, not an ID prefix. Save these
   fields in the candidate's source receipt before the final capture and review.
   Do not add sections or rewrite summaries inside exported JSON.
2. Check all roster-derived people, individual procedures, governing rules, and
   clerk/contact fields. County associations come from saved roster entities.
   A negative procedure search remains qualified as a search result.
3. Run `flwu research status --run-dir RUN --history-db DB`. Resolve missing tasks.
   Read the exact `capture_id` from `RUN/history-capture.json`.
4. Independently review the final document's legal content and appearance. Record
   that actual review, not an assertion generated by the model:

   ```sh
   flwu history finalize --database DB --capture-id CAPTURE --report REPORT.html --review 'Reviewer: completed legal and visual review; details in review record'
   flwu site export --database DB --capture-id CAPTURE --archive website/updates
   flwu publish --archive website/updates --output build/site-REVIEW-ID
   ```

5. Serve and inspect the exact built artifact. Read its latest issue, date filters,
   source links and directory. Obtain explicit publication authorization unless
   already provided for this concrete release. Stage only the reviewed export and
   intended code changes. Commit/push the authorized change to main. Do not
   publish private research workspaces, SQLite files, model prompts or raw dumps.

The exporter opens the database read-only; it does not finalize or mutate history.
It requires a complete finalized live capture, validates the saved final report's
hash and cited original/extracted bytes, and checks quotations. Public JSON has
an exact field allowlist, content checksum, capture ID and report hash. IDs are
immutable; a changed report requires a new reviewed capture. These checks establish
integrity and recorded approval, not source authenticity or legal entailment.
Review must ensure the exported claims also match the reviewed final document.

A build validates the entire archive before atomically creating a new output
directory. Existing builds are never deleted or overwritten. Only packaged web
assets, embedded public JSON and the directory redirect enter production builds.
An empty archive builds an honest “No reviewed updates have been published yet”
page. No trial is automatically promoted just to fill the page.

## GitHub Pages

`.github/workflows/pages.yml` tests and builds the public archive, uploads only
`build/site`, then deploys via `actions/deploy-pages`. PRs build/test without
publishing. Main changes to the archive or site code and manual workflow dispatch
can deploy. Repository Settings → Pages → Source must be **GitHub Actions**.
The deployment uses the `github-pages` environment; configure protection rules
there if each release needs a separate review. Preserve any existing protections.
See [GitHub's custom workflow instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

`flwu publish` builds the artifact; it does not push Git or change Pages settings.
The old `release.py` manifest API remains fail-closed and is not this publishing
path. `produce`, automatic live acquisition and scheduling remain separate,
unaccepted capabilities. Do not claim they became operational because Pages did.

## Synthetic preview and verification

Use a directory outside `website/updates` and explicit `--preview` on both steps:

```sh
flwu site export --database TRIAL_DB --capture-id CAPTURE --archive output/web-preview/archive --preview
flwu site build --archive output/web-preview/archive --output output/web-preview/site-NEW --preview
```

Previews omit the header banner at the user's request; synthetic flags remain in
the archive. Previews copy cited synthetic evidence into content-addressed local
text files. Production rejects synthetic or unfinalized
exports. Never commit preview data to the production archive. A manually authored
archive UI fixture must be labeled as such; it is not a historical research run.

Acceptance: run `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q`; build/install a
wheel outside the repository and build an empty production archive. In a browser
at a project subpath, check latest, one older period, multi-period range, inclusive
boundaries, reversed/invalid/empty range, reset, issue link, Back/Forward/reload,
source links (without quoted-source panels), historical directory identity, keyboard labels,
320px mobile width and desktop computed fonts. Check console/network failures.
Inspect screenshots. Publication success additionally requires an observed green
Actions deployment and an HTTP/browser check of the live URL; local tests alone
must never be reported as live deployment.

## Evidence-baseline date semantics (public schema version 2)

Existing version 1 archives retain their exact schema and publication-window
checks. For a reviewed evidence-baseline capture, set the immutable contract's
`report_type` to `opening_baseline` or `period_update` and supply `coverage` with
exact fields `summary` (nonempty text), `limitations` (list of nonempty strings),
and `directory_observed_at` (timezone timestamp or null). A nonempty directory
requires a timestamp and limitations explaining its historical scope. Record the
actual observation time even when later than the report cutoff; never represent
current contacts as a reconstructed historical roster. Retain this coverage metadata in the archive for validation and provenance.
The website does not render an Evidence Coverage section; directory observation
dates and applicable partial-coverage qualifications remain visible.

Every included version 2 candidate must explicitly supply `inclusion_basis`:

- `opening_baseline`: only for a single-date opening baseline. Known issuance
  must be on or before cutoff; if issuance is unknown, a known effective date on
  or before cutoff is required. An already-issued future-effective authority may
  be included, retaining its future effective date.
- `publication`: issuance must fall within the inclusive report window.
- `effective`: the stated effective date must fall within that window; known
  issuance may be older but cannot be later than cutoff.

Opening reports require the opening basis; period reports allow publication or
effective basis. Preserve original publication/effective dates in stored and
exported items. The display labels baseline and effective-event inclusions.
Coverage statements describe evidence limitations; they do not certify missing
research complete. All existing original/text checksum, quotation, synthetic
separation, complete-capture and finalization checks remain mandatory. Version 2
is an export representation, not a change to ordinary research receipt gates.

## Documentation consistency at release

For changes to reader-facing behavior, check the About template, README, and this
guide against the generated site. Keep baseline collection, current directory
refreshes, and finalized weekly reports distinct. Do not describe source collection
as a newly discovered legal change or claim unattended research is operational.
Keep dated county release entries historical and identify the latest replacement;
do not leave an earlier partial roster described as the current release. Preserve
the approved creator copy, source acknowledgments, and shared narrow About measure.

## Social preview verification

Build-time Open Graph metadata must appear in each main page head before JavaScript
runs, with a page-specific canonical URL, title and description. The public
`assets/social-preview.png` is1200×630 and must remain under5MB. Verify both HTML
and image return200 without login after deployment. LinkedIn may cache old previews;
refresh the exact shared URL with its Post Inspector. Do not claim LinkedIn rendering
was verified merely from local metadata checks.
