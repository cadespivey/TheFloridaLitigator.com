# The Florida Litigator

The Florida Litigator uses free research sources, public web pages, and government information to provide weekly updates about Florida law and procedural changes that civil litigators are likely to encounter. Commercial civil litigation is the principal focus: jurisdiction, contracts, business entities, commercial transactions, property, foreclosure, collections, remedies, evidence, appellate practice, and relevant court administration.

**[Read the updates](https://thefloridalitigator.com/)** · **[Court personnel directory](https://thefloridalitigator.com/directory.html)** · **[About](https://thefloridalitigator.com/about.html)**

## Website sections and their research flows

The four update headings correspond to separate research flows. Each flow saves source evidence, compares it with the relevant earlier observations, and submits supported findings for review before publication.

| Website section | Sources and research flow | Published result |
| --- | --- | --- |
| **Statutes** | Consult the Florida Statutes on Online Sunshine and official enactment/amendment materials. Retain the entire statutes compilation as a comparison baseline; examine changes relevant to civil litigation. Distinguish enactment, publication, and effective dates. | Summaries of relevant statutory changes, their timing, and links to the underlying official materials. A newly collected statute is not automatically a new legal development. |
| **Case Law** | Review Florida Supreme Court and all six District Courts of Appeal opinion sources, using CourtListener as a discovery or access aid where available. Read the opinion and check its date, disposition, and any available correction or withdrawal information. | Cited summaries with distinct **Holding**, **Disposition**, and **Author** labels, including panel information when supported. |
| **Procedural Rules** | Review statewide court-rule amendments, Florida Supreme Court rulemaking opinions and orders, and relevant official administrative procedure materials. Compare dated amendments with the saved rule baseline and identify effective dates. | Changes affecting statewide civil procedure, evidence, appellate practice, or other shared procedures relevant to civil litigation. Administrative review is targeted, not an assertion that every agency rule was examined. |
| **Local Rules** | Review official circuit, county, clerk, and individual judge pages; screen administrative orders for material civil-practice or access effects, and review practical division and judge-specific procedures. Compare each source separately, including individual procedures alongside governing circuit rules. | Relevant local changes in filing, hearings, scheduling, submissions, and other litigation practices, with links to supporting sources. |
| **Personnel Directory** | Check official judicial rosters, individual profiles, assignment information, and clerk pages. Preserve contacts, judicial assistants, assignments, and official procedure links in the research record. | A separate, court-filtered table of personnel, court/county, chambers or office contacts, and judicial assistants. Presentation removes duplicate contact lines; original evidence remains available to the research workflow. |

The **Courts** menu is a source-navigation aid: it links to covered courts and county official-records, court-records, and property-appraiser sites. The **Links** menu collects research and practice resources. These menus are not findings or proof that every linked page was reviewed. **About** explains the project's purpose, methods, creator, and acknowledgments.

Coverage began with the Florida Supreme Court, all six DCAs, and seven counties: Duval, St. Johns, Putnam, Nassau, Baker, Union, and Clay. County research is expanding toward all 67 Florida counties. The current directory adds reviewed county supplements to the original snapshot; coverage varies, and partial counties are labeled. Florida federal courts are planned for a later phase. A listed court is not a claim that all its procedures have been reviewed.

Research proceeds one judge at a time, reusing shared official sources. Capture contacts, assignments, official procedure links, and concise practical requirements for scheduling, communications, submissions, proposed orders, courtesy copies and appearances. Administrative orders receive substantive review when they materially affect civil practice, filing location, courthouse access or shared administration. Family, criminal and diversionary assignments receive basic contacts and office procedures; exhaustive specialty review is outside scope.

### Finding information

- **Updates:** the four research sections, with saved reporting periods selected through dates or 30/60/90/180-day shortcuts.
- **Courts and Personnel Directory:** expandable court categories and alphabetical county groups. DCAs and circuits are ordered numerically. County resources are limited to Official Records, Court Records and Tax Assessor, alongside the court website link, where saved destinations are available.
- **Quick search:** keywords, judge names or counties across saved update titles/summaries and the current personnel directory. All entered words must match, without regard to case. Results link to the matching report section or person. This searches published content, not the private source corpus or the live web; it is independent of the date filter.
- **Links and About:** practice resources, project methods, creator information and acknowledgments.

Current directory supplements may be newer than the latest weekly publication. Explicit historical issue/date selections exclude those supplements; quick-search personnel results are labeled as current directory records.

## From sources to a weekly update

1. **Define the interval and scope.** Normal weekly periods run Monday through Sunday, with Sunday as the cutoff. Research generally occurs weekly on Sundays unless an earlier update was published that week. This is the operating policy, not a claim that an unattended scheduler is implemented.
2. **Collect evidence before interpretation.** Save the original document or page, URL, retrieval timestamp, checksum, extracted text, and stated publication, revision, and effective dates. Track documents collected, content reviewed, and conflicts recorded separately.
3. **Compare against saved observations.** Use the last **finalized report**, or an explicitly requested start date, as the comparison baseline. Failed or partial runs do not advance it. The cumulative SQLite history retains finding versions and repeated observations so later work can focus on changes.
4. **Review candidate findings.** Confirm source support and civil-litigation relevance. Preserve conflicting official statements and briefly identify the discrepancy without deciding which authority controls. Missing evidence is a gap; an empty search is not proof that nothing changed.
5. **Finalize and publish.** After legal and visual review, export a reviewed snapshot to the public archive and build the static website. Summaries appear under the corresponding research headings with source links. Internal quotations and research evidence need not appear as reader-facing panels.

The site's date selector and 30/60/90/180-day shortcuts select saved reports whose reporting periods overlap the requested dates. They do **not** launch research or recompute legal analysis. Older selections use their saved personnel snapshot rather than silently substituting current contacts. The latest-update label displays a publication date; individual source and effective dates retain their own meanings.

The initial five-report baseline includes reconstructed historical findings. Current website captures and contacts are not backdated to those earlier periods, and the historical reports are not a certification that every intervening change was found. See the [baseline scope](docs/workflow/EVIDENCE_BASELINE.md) and [delivery record](docs/workflow/BASELINE_DELIVERY.md).

## Implementation status

Implemented components include the reviewed research archive, cumulative history storage, reference-directory import, synthetic preview, static date-range website, and GitHub Pages publication. Live research has been performed through an **agent-led evidence workflow**. The legacy live source adapters, `produce`, and unattended scheduling remain scaffolds; building the website does not execute a fresh weekly research run.

Additional local research-coordinator and controlled-model tooling is being developed alongside this repository. Its synthetic trials test bounded evidence handling and resumability; they do not establish live-source coverage or legal correctness. Availability of development commands depends on the checkout. The checked-in publication archive can be built independently of that tooling.

## Install and build the website

Requires Python 3.11 or newer. From a checkout:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e . pytest
# Include every reviewed county supplement, as the Pages workflow does.
.venv/bin/python - <<'PYBUILD'
from pathlib import Path
from flwu.site import build_site
build_site("website/updates", "build/site",
           county_directories=sorted(Path("website/county-directories").glob("*.json")))
PYBUILD
python3 -m http.server 8000 --directory build/site
```

Open `http://localhost:8000`. Use a new output directory for subsequent builds; publication does not overwrite an existing artifact. GitHub Pages deployment is configured in the repository's Actions workflow. Exporting a new issue requires a reviewed, finalized history capture; see the [publication contract and commands](docs/workflow/WEB_PUBLICATION.md).

For isolated synthetic and reference previews:

```sh
.venv/bin/flwu preview --fixture fixtures/synthetic-source.json \
  --state-root /tmp/flwu-fixture-state --output /tmp/flwu-fixture-output
.venv/bin/flwu directory --database /tmp/flwu-reference.sqlite \
  --output /tmp/flwu-reference
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests
```

Synthetic preview rejects production mode. Directory import uses the bundled reference; it does not fetch sources or advance verification dates. Tests verify the behavior they exercise, not the completeness of a legal research run.

## Data and project layout

- `src/flwu/`: Python CLI, evidence/history storage, validation, rendering, and publication code.
- `src/flwu/data/web/`: website templates, navigation, styles, and reviewed contact-presentation mappings.
- `website/county-directories/`: reviewed current directory supplements, with saved capture dates and partial-coverage notes.
- `website/updates/`: public, reviewed report snapshots used to build the site. Preserve their validation hashes rather than editing exported summaries by hand.
- `config/sources.json` and its packaged counterpart: research entry points. A registered source is not necessarily a reviewed source.
- `fixtures/` and `tests/`: synthetic inputs and automated checks.
- `docs/workflow/`: workflow and publication documentation. Start with [AGENTS.md](AGENTS.md) for agent instructions; development checkouts also contain the detailed research runbook, module contracts, and test plan.

Agent-led research uses a separate cumulative database at `~/.local/share/flwu/research-history.sqlite` (overridable with `FLWU_HISTORY_DB`). It preserves the frozen legacy schema, separates live and synthetic streams, and supports comparison from the last finalized report or an explicit inclusive start date. Run receipts, original documents, and checkpoints belong in ignored research workspaces, generally under `runs/`; never commit credentials. Existing files do not become historical observations until captured, and unavailable history must remain unknown.

## License and acknowledgments

Copyright © 2026 Cade Spivey. The project's original software is licensed under the **[Apache License 2.0](LICENSE)**; see [NOTICE](NOTICE). Third-party research materials retain their own applicable terms and attributions. The software license does not relicense court opinions, government documents, or other collected source material.

Thank you to [CourtListener](https://www.courtlistener.com/) and the [Free Law Project](https://free.law/) for improving public access to law. [Donate to support their work](https://www.courtlistener.com/donate/).

Current personnel directories may be newer than the last weekly report. Separately
reviewed county supplements add saved contacts and official procedure links to the
current directory, with observation dates and any partial-coverage notice. Searching
an earlier update retains that report's original contact snapshot. See the
[county directory publication procedure](docs/workflow/COUNTY_DIRECTORY_PUBLICATION.md)
for review, evidence verification, and deployment requirements.
