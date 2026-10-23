> Execution policy: [use the invoking model](MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Module intents, specifications and implementation plan

## Review findings and scope

The trial combined instruction deficiencies, reasoning mistakes and instruction
nonadherence. Existing specs referenced missing ARCHITECTURE.md, RECORDS.md and
SOURCE-REGISTER.md; generic scope docs and stale “all cards accepted” notes did
not supply an executable live workflow. Local App Support contained a task-status
ledger, not the referenced full specifications. This document and RUNBOOK.md are
the operational replacement; history remains labeled historical.

The implementation authorized by the user is workflow hardening: precise task
cards and file contracts, saved compaction handoffs, enforceable evidence checks,
and repair of misleading success paths. It does not implement all live crawlers,
a production legal analyzer or scheduler deployment. The later website work adds
reviewed public exports and Pages deployment; its governing specification is
[WEB_PUBLICATION.md](WEB_PUBLICATION.md). Live research acceptance remains separate.

| Affected modules | Intent | Required specification and acceptance evidence |
|---|---|---|
| AGENTS, README, baselines, acceptance docs | Give one consistent entry point | Operational authority is AGENTS → RUNBOOK → these contracts/test plan; mark baselines historical; no fixed passing-test or implemented-card claims |
| registry, scope_docs, config/sources, bundled sources | Explicit source and geographic denominator | Seven county clerks including Putnam; Supreme + six DCAs; circuits 4/7/8 map to correct counties; uninspected is honest metadata, never coverage; missing critical IDs fail; generated scopes reference actual URL registry, runbook and rejection tests |
| research, cli research | Separate acquisition evidence from completion assertions | Immutable window/profile/tasks; one receipt per source; dynamic people from current roster; hashed raw artifacts and extracted citations; no missing source disappears; status rebuilds from files after compaction; ready_for_review is never publication approval |
| cli preview, normalize, records | Keep test data isolated | Preview rejects production mode before any output/state writes; fixture validator still rejects synthetic=false; real source bytes never enter fixture normalizer; receipt types remain separate from DocumentRecord enums |
| identity, fixture_pipeline, diff | Reproducible identities and honest window | SHA-based issue identity; distinct attempt IDs; rerun same DB without duplicate content; prior snapshot loaded before acquisition; inclusive publication filtering; future-effective status reviewed separately; no-change semantics require complete inventory, never missing sources |
| state, migrations | Atomic accepted state and terminal runs | Keep schema v1; explicit complete/pages/freshness booleans; transaction rollback on any acquisition error; reuse revisions with new observations; JSON serialized as JSON; checkpoint never regresses; failed attempts preserve prior checkpoint; finalizer requires source/scope coverage and completed attempts |
| fetch, adapter bindings | Bound each HTTP attempt without hiding gaps | Count failed requests and retries; stream byte limit; retry 429/502/503/504 and timeout with cap/Retry-After; >60-second wait becomes resumable failure; reuse client for all source pages; one-shot fetch_url is not source-wide budget enforcement |
| adapters (all 20) | Eventually acquire actual source inventories | Currently raise NotImplementedError; preserve existing files. New adapters need offline paginated replay plus limited live pilot before enabled; registration is not acquisition acceptance |
| directory, roster | Maintain reviewed personnel facts | Import seed is reference_imported, never source_fetched or freshly_verified. Separate current official roster evidence; reconcile removals, aliases and assignments, not just additions. All seven counties and every current applicable judge remain visible; no invented contacts |
| directory_render, render, sections | Readable report with complete directory | Four report sections plus closing county appendix; all trial judges with individual procedures and governing rules, explicit gaps, clerk contacts; full appellate contacts electronic; PDF visual review and link checks mandatory, unit rendering alone insufficient |
| model, analysis, state job helpers | Source-grounded analysis, eventually | Current model is a template, not a local-model integration. No confidence inferred from text length as legal accuracy. Three-pass transcription/comparison/implication in runbook. Job helpers are not accepted for concurrent production execution until source filtering, leases, claims and recovery integration tests pass |
| config | Enforce local execution policy at loading | Production load invokes enforcement; parse hostname exactly, reject localhost-lookalike hosts, userinfo and cloud fallback; no external spending; no secrets in config/logs |
| orchestrator | Never claim unperformed work | Fixture path executes actual preview. Without fixture, fail NOT_IMPLEMENTED; research tracker cannot be labeled automated weekly execution |
| publication, site | Historical views from reviewed captures | Read-only finalized live capture export; report/source hashes and quotations checked; exact public field allowlist. Immutable archive, latest default, inclusive period overlap, original fonts, historical directory and cited summaries. Explicit isolated synthetic preview. See WEB_PUBLICATION.md |
| release, publish | Publish concrete reviewed authorized artifacts | New CLI builds validated public archive; Pages workflow tests/builds then deploys only main. No private DB uploads or synthetic production exports. Legacy release.py manifest API remains blocked; finalization is editorial review, not automatic permission to publish |
| scheduler | Run only a validated entry point | Generated launchd plist points to an unimplemented command; not an operational schedule. Do not install/enable until end-to-end production acceptance and user authorization |

## Implementation sequence and checkpoint

1. Replace ambiguous operating instructions and correct source entry points; remove
   stale availability claims and add Putnam to the denominator.
2. Add file-based run contract, source receipts, evidence validation, roster-derived
   person obligations, status and RESUME handoff without changing SQLite v1.
3. Repair preview/live boundary, identity/window/state behavior, HTTP retries,
   config enforcement and false orchestration/release success.
4. Replace weak assertions and add regression cases from the trial; run full tests
   and wheel/package smoke tests. Inspect final diff, preserve preexisting DB/PDF
   and tracked bytecode changes. Report live/legal/PDF acceptance as unperformed.

## Attribution and controls

- Poor instructions: missing paths/schemas, six-versus-seven counties, ambiguous
  “complete,” unspecified source/cursor handling. Remedy: explicit registry,
  workspace layout, task cards and coverage denominator.
- Reasoning load: amendment redlines, historical versus current rosters, temporal
  status and multiple courts mixed in one context. Remedy: one item per context,
  mandatory saved transcription/comparison/claim passes and independent review.
- Nonadherence: synthetic relabeling, skipped scopes, unchecked goal completion,
  deletion retry through another interpreter. Remedy: hard mode/status checks and
  explicit operation boundary instructions. Instructions alone cannot guarantee
  adherence; record the actual evidence and reject unsupported transitions.

Checksums, quoted passages and explicit receipts reduce accidental errors. They
cannot establish legal entailment, authenticity of a self-authored receipt,
complete discovery of an index, or independence of a reviewer. Those are named
manual acceptance duties, not silently claimed machine guarantees.

## Validation of this hardening pass

On 2026-10-11, the full local suite passed: 134 tests, with no warnings reported.
The former no-op crash test was removed; the replacement injects a real partial
acquisition failure and checks rollback plus preservation of an accepted checkpoint.
Thirty new regression cases supplement strengthened assertions in existing tests.
A wheel built successfully without reported warnings. An isolated subprocess
loaded the extracted wheel outside the repository, migrated a temporary SQLite v1
database, initialized a research workspace with the packaged source catalog and
confirmed incomplete status. `git diff --check` passed.

No live weekly research run, local-model compaction trial, independent legal review,
or final PDF visual review was performed in this implementation pass. Those remain
explicit acceptance work in TEST_PLAN.md. Existing database, output artifacts and
preexisting bytecode modifications were not edited or discarded by this pass.

## Controlled local worker revision (2026-10-11)

The first local replay showed that instructions alone did not prevent direct corpus
reads, missing nested evidence, future-effective status errors, or broken links.
The authorized follow-up implements a narrow worker in `controlled_worker.py`,
shared rules in `worker_contract.py`, and an offline coordinator in
`trials/controlled_replay.py`. This is a runnable synthetic integration, not a new
live court crawler or an enabled production publisher.

| Component | Intent and exact contract |
|---|---|
| Trusted coordinator | Own acquisition, immutable originals, discovered-source denominator, roster-derived tasks, writes, retries, counters and report generation. Only registered synthetic endpoints are resolved; endpoint strings never become filesystem paths. |
| Model boundary | Send one JSON evidence packet per candidate/judge to the pinned loopback model. Do not expose shell, filesystem, URL-fetch or function-call tools. Never execute model output, even when it resembles a command. No cloud fallback, redirects or inherited proxy authentication. |
| Evidence packet | Task ID, dates, exact output schema, line-addressed source spans. No private corpus, controls, answer keys, parent paths or unrelated task history. Select citations by span ID; trusted code supplies original bytes, hashes, paths and locators. |
| Worker output | Exact field set; legal status enum; window and effective-date checks; current roster identity; current-profile contact evidence; separate nested personal-procedure/governing-rule citations; negative search log; amendment before/after and prior-source citations. Unknown facts remain null where allowed. |
| Validation | Use shared research citation/person checks with coordinator-selected `synthetic_replay` mode. Require synthetic originals, synthetic authority and `.invalid` URLs. Existing live research validation continues rejecting synthetic evidence; model output cannot select a mode. Structural validation never proves legal entailment. |
| Persistence | Save request/response/error for every attempt. Accept only validated answers with packet/answer hashes. Three attempts maximum per task; unresolved tasks remain pending. A restarted coordinator revalidates and reuses accepted answers without rewriting them. |
| Renderer | Single accepted data model generates JSON and escaped HTML. Compute explicitly named candidate, endpoint and judge counters. Resolve local links from recorded paths, check every link, and require four sections followed by the closing county directory. No model-authored HTML or manual filename reconstruction. |

The controlled adapter parses only the explicit synthetic text format. Its link
and roster parsing is not approved for arbitrary live HTML. Live rollout requires
source-specific adapters, full inventory checks, independent legal review and
visual PDF acceptance. Fresh item requests do not test native compaction.

Follow-up trial repairs also require: an explicit index-derived publication-window
flag; mandatory inclusion of in-window withdrawal notices; rejection of identical
before/after change text; exact current-profile citation support for division,
address, phone and JA; actionable missing-span feedback; and retention of rejected
provider responses with their exact finish reason. Known synthetic original bytes
cannot be made live merely by changing receipt metadata. Model-selected excerpts still require relevance and completeness review; these
checks do not prove a legal conclusion beyond the quoted source.

Inclusion reasons are the exact codes `in_window`, `outside_window` or
`withdrawal_notice`, validated against the index date and legal status. The renderer
generates their explanatory text. The model does not write a second legal-status
explanation that can contradict its structured fields. Accepted summaries are now exact source passages selected by `summary_spans` and
assembled by code. Model-written interpretive commentary is not accepted by this
worker. Relevance, completeness and legal implications still require review.

## Longitudinal research memory: intent, specification and plan

User-approved baseline: **last finalized report**, never the latest partial or
completed research run. Objective: every research checkpoint preserves reusable
facts/evidence and supports comparisons against that report or an explicit start.

| Module | Contract and implementation |
|---|---|
| `history.py` storage | Separate SQLite database, explicit schema marker, rejects legacy DB. Immutable canonical-hash captures, content-addressed raw/extracted BLOBs, deduplicated finding versions and repeated observations. One transaction per checkpoint, including all artifacts/versions/observations. Same mode and scope required for a stream. Drafts never become supported current facts. |
| `history_capture.py` adapters | Revalidate saved contracts and receipts; save source bytes before accepting facts. Stable keys for sources, candidates, people and clerks. Strip retrieval/path bookkeeping from fact comparisons, retain full provenance separately. Preserve incomplete draft receipts and required-source denominators. Replay and manual evidence validation remain separate. Capture state is pinned to a shared DB path. |
| `research.inspect_run` | Every status check persists validated findings plus incomplete tasks and writes `history-capture.json`/`history-context.json`. Capture failures propagate; workspace status alone is not proof of successful persistence. Before compaction ensure this command completed successfully. |
| Controlled coordinator/worker | Persist after acquisition, each task checkpoint, and final output. Freeze pre-run context in the contract; expose only the current entity's prior facts to the worker. Changed historical-context hash fails. Resume packets remain immutable. Historical facts never replace current source spans. |
| `history.compare` | Inclusive NY dates or aware timestamp bounds; default report baseline. Replay all transitions in capture order, including reversals. Retain known findings when absent/blocked. Separate source-byte changes, finding revisions, first observations and effective-date triggers. Unknown baseline, failed checks, stale checks and unfinished analysis prevent a no-observed-change assessment. |
| `history.finalize` | Explicit review attestation plus actual nonempty report bytes. Only latest complete capture eligible. Store report hash/bytes and baseline marker atomically; never finalize automatically or publish. |
| CLI/context consumer | `history streams/capture/changes/finalize/artifact`; explicit stream for comparisons, optional per-entity context and output JSON. Reject unknown stream, missing required arguments, conflicting pinned DB or wrong schema. |

Implementation sequence: add isolated persistence and comparison primitives;
connect validated workspace adapters and automatic checkpoints; provide CLI and
bounded worker context; test multi-run transitions/failures/temporal boundaries;
backfill the completed synthetic regression; document acceptance and limits.
The frozen legacy schema and public release path are unchanged.

Knowledge time means capture/import time. Publication, retrieval and effective
dates are separate data. Database contents do not prove coverage before the first
observation or continuous coverage between checks. Backfilled old law must not be
called new law. A changed model interpretation or publication-window eligibility
may create a finding revision without a legal amendment. Comparisons are review
inputs, not a legal-change oracle. The current source gate reuses completed reviews when original hashes and review
protocol match; opinion reuse also requires matching official status metadata.
Unreviewed content, failed retrieval and effective-date triggers are not skipped.
Raw original bytes remain the review source. See SOURCE_HASH_REVIEW.md.


## Active evidence-baseline acceptance clarification

Follow [EVIDENCE_BASELINE.md](EVIDENCE_BASELINE.md). Verify separately: collected originals, scoped content review, recorded source conflicts, and unavailable evidence. Two faithfully cited conflicting official statements pass source-review acceptance without selecting a winner. Missing or misattributed evidence does not pass. Criminal/diversion links plus contacts/assignments satisfy that scoped requirement; civil/shared responsibilities still require substantive review. Verify all five supported reports disclose historical gaps and do not equate a collected document with reviewed substance. Preserve existing provenance, identity, persistence and publication tests.

## Officer assistant-name absence (Hillsborough packet87)

Intent: preserve an officially unreported assistant name without inventing a
person or preventing a completed, bounded source review from being saved.
`scripts/officer_review.py` permits `assistant_name.status=not_published` only
with a null value, an absence reason, cited source, and a nonempty search log
containing checked URLs, search terms and results. An optional `published_value`
(such as `TBD`) must occur in the citation quotation. Keep the published role and
shared office contact independently verified. This is not proof that no assistant
exists, and does not remove the name from later refresh followups. Verified names
must be nonempty strings and must not be placeholders. All individual-procedure,
identity, role, contact and citation checks remain required.

## Officer negative procedure (Hillsborough Frank revision 1, accepted packet89)

Intent: let a completed bounded source review document that no individual
procedure is published, without labeling a contacts-only profile as verified
instructions. `validate_officer` accepts `procedure.status=no_published_procedure_located`
only with the exact person association (`applies_to`), a real citation, a
nonempty `absence_reason`, and a nonempty structured `search_log` whose rows each
carry a real http(s) `url`, a `search` term and a `result`. `documents` must be
empty; a source-only inventory belongs in a separate field (for example
`governing_rules`), never as fabricated procedure documents. A negative finding
is a documented absence, not verified instructions; applicable shared
instructions are recorded separately with their own search scope. Unknown
statuses are rejected; the method never converts statuses, invents instruction
content, or mutates the receipt. All positive guards remain required: the
verified path still needs a nonempty document inventory with applicability,
review scope and citations, plus person association, identity, role, assistant,
contact, checklist and governing-rule citation checks. Roster category
attribution comes from original HTML card markup (per-card classes), not
flattened filter headings; Hillsborough's seven hearing-officer cards are one
Civil Infractions (Frank) plus six Unified Family Court (`roster-attribution.json`).
The contract is exercised by the negative-procedure cases in
`tests/test_officer_review.py` and by the real Frank receipt validated with
recursive citations alongside all previously accepted officer receipts.

## Standard hash-driven update and opinion discovery

Intent: code controls acquisition, identity, equality and candidate routing; the
model interprets only queued evidence. `flwu update` always runs all seven official
opinion feeds and their inactive channels, then checks registered documents and
court release notices. It is an acquisition/review coordinator, not unattended
legal analysis or automatic publication. Older adapter stubs remain unchanged.

| Module | Required contract |
| --- | --- |
| source_gate | Independently fetch registered sources, persist each observation, compare SHA-256 against last successful bytes, preserve failures, reuse only completed same-protocol reviews, export originals/diffs, bind reviewed updates to current hashes and optimistic finding versions. |
| opinion_discovery | Stable court/CMS identity; verified pagination/date/court filters; overlapping discovery; tracked detail/status and PDF checks; metadata changes queue even with identical PDF; incomplete listings cannot mean no new opinions; durable relevance outcomes. |
| update / CLI | Mandatory seven-court wiring, pinned run inputs, resumable page/source checkpoints, combined bounded review queue, no publication/finalization; reporting baseline remains last finalized report or explicit date. |

The executable specification and exact formats are SOURCE_HASH_REVIEW.md and
OPINION_DISCOVERY.md. Regression acceptance is in tests/test_source_gate.py and
tests/test_opinion_discovery.py. Validate with official-response-shaped fixtures
and a bounded isolated live trial before accepting upstream format support.
