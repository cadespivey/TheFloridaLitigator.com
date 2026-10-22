# Current repository execution instructions

Astra performs the remaining statewide research, implementation, validation and
corrections directly. Do not delegate to Qwen or another local worker. Do not
restart inference servers or unload models. Continue through the statewide
completion audit; there is no pause or user approval checkpoint between counties.
Finish and save one person before researching the next. Reuse verified evidence.

Read [the active goal](docs/workflow/STATEWIDE_BASELINE_GOAL.md), then
[the current handoff](docs/workflow/LOCAL_AGENT_HANDOFF.md). They supersede older
checkpoint-specific stop/resume instructions. Historical instructions are retained
in [the archived instructions](AGENTS_HISTORY_20261022.md), not active commands.
Never infer completion from the number of supplement files or passing tests.

Raw webpages can embed third-party API keys. Preserve originals in the local
research database, but do not stage checkpoint workspace captures or force-add
ignored evidence. Before every push, run `python scripts/check_public_credentials.py`
after staging intended files. It checks index blobs without printing credentials.
Public metadata retains source URLs, timestamps and hashes; do not promise that
local artifact paths exist in public Git. Do not rewrite history or revoke keys
without authorization.

## Final integration scope — October 22, 2026

Verify the current database, current website publication and future update/comparison
behavior. Do not conduct historical-report verification as part of final integration.
Leave existing historical reports untouched; retrospective content, rendering, hash
and provenance checks are not completion gates. This supersedes older audit plans
requiring those checks; already collected validation evidence remains preserved.

## Research worker environment boundary

Use `/Users/cadespivey/florida-litigator-weekly-update/.venv/bin/python` with
`PYTHONDONTWRITEBYTECODE=1` for research scripts. Do not run pip, brew, npm or other
package installation/upgrade commands. An output-only research assignment does not
authorize changing a Python environment or machine configuration. If a library or
OCR executable is unavailable, preserve the error and report the specific missing
capability; use available visual review with explicitly labeled transcription where
appropriate. Do not pipe failing commands into `tail` and treat the pipeline's
successful exit as validation. Preserve full warnings and errors. Never install
another PDF parser merely because a scanned PDF has no text layer.


## Practical baseline stopping rule — renewed user clarification

This applies to civil/commercial judges too, including Business Court. Relevance
alone is not permission to exhaustively analyze a litigation subject. Capture
contacts, assignments, official procedure links, and a concise structured account
of recurring operating requirements: scheduling, conferral, motion submissions,
proposed orders, courtesy copies, remote appearances and chambers communications.
Preserve material filing-location, courthouse-access and shared administration rules.

Do not research particular lawsuits, merits, case-specific litigation strategies,
individual case deadlines, docket histories, specimen litigation packets, or every
linked form/calendar. Read the sections needed to establish the practical operating
requirements; preserve longer collected manuals with the exact review scope. Follow
a further link only to fill an identified required field or clarify a material
operating requirement. A commercial assignment does not itself justify expansion.
Once those fields and the bounded procedure checklist are supported, record any
conflict or gap and save the judge checkpoint before proceeding to the next person.
Intentional nonreview of detailed litigation material is not a missing baseline
requirement. Preserve existing originals, findings and history without claiming
unread content was reviewed. This rule takes precedence over older exhaustive
review examples or instructions to follow all forms and procedure links.

Execution limit: the checklist is a short practitioner reference, not an abstract
of the entire manual. For primarily criminal, family, juvenile or diversionary
assignments, capture contacts, assignment and official procedure links plus only
basic scheduling, submission and appearance instructions readily available on
those sources. Do not enumerate specialized deadlines, evidentiary requirements,
trial packets or substantive standards. Record source discrepancies briefly;
do not pursue additional sources merely to resolve them. Open another source
only when a required contact/assignment field or material civil operating rule
is actually missing. Finish the supported person record and move on.

Before any additional research, identify the specific missing directory field or
recurring court operating requirement it will fill. If neither exists, stop
researching that person or source and proceed to validation/integration. Do not
expand the checklist merely because a manual offers more detail. County acceptance
requires accurate supported contacts, official procedure links and the bounded
operating summary, not analysis of particular litigation. Preserve collected
material without expanding its review solely to make every document fully reviewed.

Operational presentation limit: summarize each applicable checklist category in a
short entry and link to the official instructions for detail. Stop at how to contact
the office, schedule, submit materials and appear. Do not extract the requirements
for litigating individual motion types, claims or defenses; retain their official
procedure link instead. Material generally applicable filing/access rules remain
in scope. Do not reproduce
motion-specific litigation recipes or expand source collection to explain them.
Routine progress updates should identify roster progress and material gaps, rather
than narrating individual litigation requirements. This is an execution correction;
it does not add another research or documentation deliverable.


## Research-depth correction — October 18 user feedback

The user identified scope drift into particular litigation. Prioritize the statewide
personnel/contact baseline, each judge's practical civil procedures, and broadly
applicable filing, scheduling, service, submissions, remote appearance, courthouse
access and material court administration. A county baseline is not an exhaustive
analysis of every administrative order, specialized docket or historical program.

Screen specialized and historical orders for scope and status. Ordinarily retain
the official link, any already collected original, and a concise applicability or
vacatur note. Do not extract case lists, old reassignment schedules, program forms,
merits requirements or every deadline unless a concrete current effect on general
civil/commercial practice requires it. An index entry is a screening candidate,
not automatically a mandatory full-content review. Explain any exception before
expanding. Existing material findings remain preserved; no deletion or relabeling
of collected-only documents as fully reviewed.

For Palm Beach, stop exhaustive order-by-order expansion. Screen the remaining
specialized candidates, reconcile roster/contact and practical-procedure gaps,
and proceed to county validation and the next county. Do not hold completion for
exhaustive historical or specialized litigation analysis. Genuine missing required
contacts/evidence and publication validation remain separate requirements.



## Existing development and publication instructions

## Project Overview

**The Florida Litigator** publishes reviewed Florida civil/commercial legal
updates and court personnel directories at https://thefloridalitigator.com/.
The public static site is implemented; live evidence collection is agent-led.
Legacy source adapters and scheduling are scaffolds, not proof of unattended
research. The working statewide baseline is separate from finalized reports.
See README.md and docs/workflow/WEB_PUBLICATION.md for current reader behavior,
and docs/workflow/COUNTY_DIRECTORY_PUBLICATION.md for dated supplements.

For website maintenance, preserve numerical DCA/circuit ordering, alphabetical
county groups, accessible nested menus, quick search and historical isolation.
Publish reviewed supplements explicitly; never advance a finalized report just
to refresh contacts. Use current remote main and preserve unrelated local research
changes. The statewide baseline goal is active; follow the current research handoff for its next county and checkpoint.

- **Package name**: `flwu` (Python import)
- **CLI entry point**: `flwu` (exposed via `pyproject.toml`)
- **Python**: 3.11+
- **State store**: SQLite (frozen schema v1, WAL mode, foreign keys enforced)
- **External calls**: None in fixture mode; production adapters use bounded HTTP (httpx)
- **Public build**: deterministic rendering of reviewed exports; no model calls. Research model selection follows the active project instructions.

## Repository Layout

```
florida-litigator-weekly-update/
├── .git/
├── AGENTS.md                        # ← this file
├── README.md                        # User-facing readme
├── pyproject.toml                   # Poetry project config (C07)
├── requirements.lock                # Constraints lockfile (C11)
├── config/
│   ├── defaults.json                # Global config schema (C07)
│   ├── adapter_bindings.json        # Per-adapter HTTP limits (C10)
│   ├── sources.json                 # 60 source URL registry (C09)
│   └── public-export.json           # Publication policy (C36)
├── docs/
│   └── acceptance/
│       └── production-readiness.md  # Full integration checklist (C01–C40)
├── fixtures/
│   ├── README.md
│   ├── synthetic-source.json        # Test fixture (C08)
│   └── expected-identities.json     # Expected hash outputs (C06)
├── src/
│   └── flwu/
│       ├── __init__.py              # Package entry
│       ├── cli.py                   # CLI (C08) — preview, registry, fetch, etc.
│       ├── config.py                # Config loading + production enforcement (C07)
│       ├── records.py               # Record models + validators (C01)
│       ├── identity.py              # Deterministic IDs (C06)
│       ├── normalize.py             # Fixture → DocumentRecord (C02)
│       ├── diff.py                  # Semantic change detection (C03)
│       ├── state.py                 # SQLite state machine (C05)
│       ├── fetch.py                 # Bounded HTTP (C10)
│       ├── fixture_pipeline.py      # End-to-end pipeline (C08)
│       ├── inventory.py             # Search catalog (C35)
│       ├── roster.py                # Judge roster reconciliation (C31)
│       ├── model.py                 # Deterministic analysis (C32)
│       ├── analysis.py              # Job lifecycle (C33)
│       ├── orchestrator.py          # Weekly run (C34)
│       ├── sections.py              # Report sections (C34)
│       ├── search_index.py          # Search index (C35)
│       ├── site.py                  # Static site generation (C36)
│       ├── publish.py               # GitHub Pages publish (C39)
│       ├── release.py               # Release gating (C37)
│       ├── scheduler.py             # Schedule integration (C40)
│       ├── registry.py              # Source registry (C09)
│       ├── render.py                # HTML/Markdown render (C08)
│       ├── scope_docs.py            # Scope documentation (C09)
│       └── adapters/                # 20 source adapters (C11–C30)
│           ├── agency_rules.py
│           ├── circuit_eighth.py, circuit_fourth.py, circuit_seventh.py
│           ├── clerk_baker.py, clerk_clay.py, clerk_duval.py,
│           │      clerk_nassau.py, clerk_st_johns.py, clerk_union.py
│           ├── court_bar_rules.py
│           ├── dca_first.py…dca_sixth.py
│           ├── fl_bills.py
│           ├── fl_statutes.py
│           └── fl_supreme.py
├── tests/
│   ├── conftest.py
│   └── test_*.py                    # 101 tests (all pass)
└── website/
    └── assets/
        ├── site.css
        └── search.js
```

## Core Pipeline (C01–C08)

| Card | Module | Description |
|------|--------|-------------|
| C01 | `records.py` | Document record models; 30+ validated enums; strict validators |
| C02 | `normalize.py` | Fixture → validated DocumentRecord; stamps IDs; rejects synthetic=false |
| C03 | `diff.py` | Semantic diff: added, amended, withdrawn, superseded, unchanged |
| C04 | (reserved) | — |
| C05 | `state.py` | SQLite state machine: runs, attempts, documents, revisions, snapshots |
| C06 | `identity.py` | Deterministic IDs from inputs; no randomness; stable across time |
| C07 | `config.py` | Schema-validated config; production security enforcement |
| C08 | `cli.py` + `fixture_pipeline.py` | `flwu preview` — end-to-end fixture pipeline |

## Extended Cards (C09–C40)

| Card | Module | Description |
|------|--------|-------------|
| C09  | `registry.py`, `scope_docs.py` | Source registry (60 URLs); scope documentation |
| C10  | `fetch.py`, `adapter_bindings.json` | Bounded HTTP (pages, bytes, timeout, retries, spacing) |
| C11  | `requirements.lock` | Constraints lockfile |
| C12–C30 | `adapters/*.py` (20 files) | Source adapters for FL statutes, bills, DCA, circuits, clerks |
| C31  | `roster.py` | Judge roster reconciliation from verified records |
| C32  | `model.py` | Deterministic analysis (no cloud fallback) |
| C33  | `analysis.py` + `state.py` extensions | Analysis job lifecycle (enqueue, claim, finish, recover) |
| C34  | `orchestrator.py`, `sections.py` | Weekly orchestration; report sections |
| C35  | `inventory.py`, `search_index.py` | Search catalog and index |
| C36  | `site.py` | Static site generation (HTML/CSS/JS) |
| C37  | `release.py` | Release gating (manual/automated approval) |
| C39  | `publish.py` | GitHub Pages workflow |
| C40  | `scheduler.py` | Scheduled run integration |

## Testing

```bash
.venv/bin/python -m pytest tests/ -v
# Read the actual result; do not infer current test counts from historical notes.
```

## Development Rules

1. **No external calls in fixture mode.** The pipeline is fully deterministic.
2. **Deterministic identity only.** Never use Python `hash()` or randomness for IDs.
3. **Preserve existing adapters.** Do not rename columns or loosen constraints.
4. **Clone adapters**, never modify existing ones. New sources get new files.
5. **Production mode** enforces `external_usd=0`, loopback-only model URL, no cloud fallback.
6. **Migrations are frozen.** Schema version 1 is the only supported version.

## CLI Usage

```bash
# Preview with synthetic fixture
flwu preview \
  --fixture fixtures/synthetic-source.json \
  --state-root /tmp/flwu_state \
  --output /tmp/flwu_output

# Future subcommands (stubs):
flwu registry  # Source registry management
flwu fetch     # Acquire source data
flwu analyze   # Run analysis jobs
flwu produce   # Produce report
flwu publish   # Publish to GitHub Pages
flwu schedule  # Schedule recurring runs
```

## Fixture Mode vs Production Mode

| Aspect | Fixture Mode | Production Mode |
|--------|-------------|-----------------|
| Data source | Synthetic JSON | Live HTTP adapters |
| Network | None | Bounded HTTP (per-adapter limits) |
| Model | Deterministic analysis | Same (no cloud fallback) |
| external_usd | 0 required | 0 required |
| state_root | Can be any path | Must not point to fixture |
| model.base_url | None | Loopback only (localhost/127.0.0.1) |
| Publication | Manual | Manual approval required |
