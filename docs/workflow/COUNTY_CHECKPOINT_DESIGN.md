> Execution policy: [use the invoking model](MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# County checkpoints and report comparisons — proposal for review

**Superseded as an implementation plan by the October 15 user clarification.**
Follow [STATEWIDE_BASELINE_GOAL.md](STATEWIDE_BASELINE_GOAL.md): collect the statewide
baseline and build the agentic workflow incrementally during research, beginning
with Broward. This prior architecture proposal is retained as design background
and possible validation cases. Its five-assignment implementation plan and pending
approval question are not prerequisites for research and are not approved schema
changes. Revisit individual engineering needs only when the actual work requires.

October 15, 2026. Design only; implementation is not authorized by this document.
This supplements COUNTY_WORKFLOW.md. The accepted unit is one judge, researched
from the profile through its applicable linked material before changing judges.

## User-visible behavior

1. An interrupted run resumes the same judge and shows the exact next unfinished
   step. Previously saved documents and completed steps are reused.
2. A county has its own research progress. A completed new county cannot erase
   the seven existing counties or make them appear newly reviewed.
3. A finalized report identifies the exact reviewed observations it uses. Later
   drafts do not alter that report or become the comparison baseline.
4. First-time collection creates the new county's baseline. It does not imply
   that the judge, address, or procedural requirement is new.
5. The user receives one county review packet, then decides whether to accept it
   and which county comes next. No next-county research begins automatically.

## Evidence from the existing implementation

- `history.record` already provides transactional captures and content-addressed
  artifact storage. It rejects scope changes inside one stream.
- `history_capture.stream_for` derives identity from the county/circuit list.
  Thus enlarging that list creates a new comparison stream.
- `history.compare` selects the last finalized report for one stream. It retains
  absent prior facts and distinguishes first observation, changed facts, historical
  observations and effective-date triggers. It does not compose different streams.
- The five current public reports are finalized in
  `manual_baseline:ea3da59ca4bd`; the latest uses capture sequence 4271 and covers
  October 2–11. Their report artifacts were finalized October 12, 2026.
- The latest report capture has 167 judges, 14 clerks, 10 source inventories and
  33 publication candidates. Its report contract is a baseline-specific shape,
  not the regular `research.initialize` contract. It has two summary checks;
  these do not prove a new county's judge-level completion. Do not feed the
  baseline contract through the normal initializer or invent missing checks.

Read-only inspection: `runs/county-workflow-design/baseline-structure.json`.
The inspection copy is separate from the source DB. It proves the stored shape
and references, not present-day source freshness or legal completeness.

## Recommended persistence approach

Keep the shared database and all existing tables/reports intact. Use stable
county research streams plus an explicit, immutable composition manifest for
each future report. Store shared circuit source evidence once, with applicability
links; a circuit source is not a demand to research every county in that circuit.

Proposed implementation boundaries:

- A new county coordinator owns work order, checkpoints, evidence validation,
  and the county review packet. It does not repurpose the seven-county initializer.
- Reuse existing artifact hashing and capture transactions where their contracts
  apply. Add separately versioned coordinator tables in the same database for
  run contracts, checkpoint state, and report references; preserve the frozen
  legacy schema and existing history metadata version. Validate additive migration
  and rollback on a disposable database before touching the production DB.
- The report composer reads explicit component references. It carries forward
  prior accepted components unless replaced by a newly reviewed component, with
  original observation times and source scope intact. It never promotes a parked
  or merely collected record into a reviewed current component.
- Existing publication candidates are not automatically reprinted as new findings
  when their directory/state components are carried forward.
- Export uses a versioned allowlisted schema when new provenance is needed.
  Keep old exports byte-for-byte unchanged and preserve their rendering behavior.

This is a material persistence decision requiring the user's design checkpoint
before implementation. The exact additive schema and migration are a bounded
implementation task to be reviewed before use on the shared production database.

### Contract and state fields

The immutable run contract pins schema version, mode, county ID, circuit ID,
official source roots, reporting cutoff/timezone, initial roster evidence reference,
shared DB path, prior finalized report ID and hash (or explicit bootstrap), and
source/review scope. A changed contract requires a new run; never alter its hash.

Durable checkpoint state includes:

- Run ID and monotonically increasing revision; expected previous revision for
  stale-write rejection. Permit only one active writer per run.
- Roster identity list and reconciled inventory evidence, including unresolved
  assignments. Newly discovered judges require an appended inventory revision
  in checkpoint state, retaining the initial inventory reference in the contract.
  Do not edit the contract to add a judge. A changed county/circuit scope still
  requires a new contract. Retain the prior queue and explicit assignments when
  recording an inventory revision; absence from a new page is not proof of removal.
- Ordered queue: pending, active, complete, or parked-with-gap. At most one active
  judge; exactly one while judge work is underway.
- For each judge: stable identity, completed substeps, receipt hash/version,
  source observations, checklist values, conflicts, gaps and next action.
- Shared-source references: source identity, original/extracted hashes, retrieved
  time, response status, reviewed scope and explicit applicability links.
- Validation result and persisted capture ID. A saved draft may be incomplete;
  it must not be used as a supported current fact.

The database checkpoint is authoritative. Workspace JSON and RESUME.txt are
derived handoff views, not competing authorities. Human-edited receipts are inputs
until validated and committed. A coordinator must reject stale revisions rather
than silently overwrite newer work.

### Durable save order

1. Save acquired bytes and extraction to temporary content-addressed files,
   validate hashes, then atomically install the complete files in the workspace.
2. Validate the current judge's receipt, checklist, attribution, and source refs.
   Preserve valid partial evidence even when the judge is not yet complete.
3. In one DB transaction, store missing artifact bytes, the checkpoint/receipt
   version, observation records and queue transition. Verify the expected previous
   revision; a second writer must fail without changing state.
4. After commit, emit the capture acknowledgment and regenerate status/resume
   files. If this final file-write step fails, resume regenerates them from the DB.
5. A failed DB transaction leaves the previous active judge and revision intact.
   Retained workspace files can be retried; their existence does not prove a save.

Do not change to the next judge before step 3 commits. Compaction can occur after
any committed substep, not only after an entire judge is complete. The resume
packet loads only the active judge, relevant prior facts, and referenced sources.

### Shared sources and freshness

Reuse the exact saved source version during one run when its scope applies. Save
a distinct observation for a later fetch/check even if the bytes are identical.
Do not create multiple artifact blobs for identical hashes. Do not collapse distinct
URLs/observations merely because bytes match. Preserve redirects and resolved URLs.

A prior-run artifact is background until checked for the new run. If using a 304
response, retain the conditional request metadata, response observation, and the
prior bytes it validates; do not manufacture a new raw body. Failed checks retain
the prior evidence and create a freshness gap. Reuse of an extracted file does
not imply that extraction or substantive review has been repeated.

When an updated shared document changes a completed judge's applicable procedures,
create a dependency follow-up for that judge. Before county review, resolve those
follow-ups or identify them as gaps. Do not silently rewrite a completed record.

## Comparison and report composition

Each finalized report's internal manifest pins the prior finalized report ID,
report period, and component references: logical scope, immutable capture ID,
entity/version IDs, observation/review times, and reviewed versus carried-forward
status. Store the manifest and approval record atomically with the finalized report
reference. Publishing failure is separate from research finalization; retain its
deployment status without silently reselecting a baseline.

For the existing five reports, use their original finalized capture and report
hashes as legacy references. A mapping adapter can resolve current structured
fields from them with provenance, but must not rewrite history, rename existing
people without an explicit identity link, or treat mapping time as retrieval time.
Missing checklist structure in a legacy record is unknown, not 'no requirement.'

To compare:

1. Pin the last finalized report at run initialization; never substitute the latest
   research run. Explicit-date mode pins the requested interval instead.
2. Resolve each entity's prior supported state from that report's frozen component
   refs. If the county or entity was not covered, mark baseline unknown.
3. Compare normalized factual values and reviewed procedure requirements. Keep
   bookkeeping, formatting changes and re-extraction differences separate from
   substantive differences. An interpretation change is a review event, not proof
   that the law changed.
4. Preserve all recorded transitions, including reversals within an interval.
   Distinguish changed source bytes, changed contacts/assignments, supported
   procedural change, reached effective date, first observation, unresolved
   discrepancy, and incomplete recheck.
5. Determine legal-event dates from source evidence. Unknown adoption/revision
   dates remain unknown. A newly discovered older requirement belongs in baseline
   context unless a supported event places it in the update interval.
6. No-observed-change requires a known baseline and completed current checks for
   the stated scope. It is not proof of continuous monitoring. A failed fetch or
   missing roster entry alone never establishes repeal, retirement, or deletion.

Explicit-date comparison must expose separately: observations saved during the
requested interval, supported legal events dated within it, and historical gaps.
Do not imply the database observed July changes contemporaneously when the first
capture occurred in October. Preserve occurrence, retrieval and knowledge times.

Before finalization, if another report was finalized after the pinned baseline,
require a comparison refresh and renewed review of affected findings. No silent
rebase and no baseline advancement from a partial county run.

The public site continues to use the four update headings and concise personnel
table. Internal completeness/mapping information stays in the research review
packet; do not restore the removed Evidence Coverage section or source columns.
Public findings must still avoid unsupported current-status or no-change claims.

## Bounded implementation plan for approval

| Assignment | Deliverable | Acceptance evidence |
| --- | --- | --- |
| 1. County contract and judge queue | New coordinator module and focused CLI commands; county IDs/source roots explicit; durable active judge | Interrupt/restart mid-judge, stale-writer rejection, one-active invariant, parked-gap handling, roster revision tests |
| 2. Structured records and source reuse | Validated checklist, provenance, shared-source observations and applicability | Wrong-person rejection; preserved conflicts; silence distinct from no requirement; two judges reuse one blob; failed fresh check does not update observed time |
| 3. Comparison and report mappings | Additive versioned persistence and legacy read adapter | Five original report hashes preserved; new county baseline unknown; existing county comparisons retained; partial runs do not advance finalization; reversals/effective dates/explicit-date gaps covered |
| 4. Review packet and website integration | County summary + judge records + gaps; complete composite export; registry/filter entries | Existing counties and historical views retained; new county isolated; no synthetic public data; no restored evidence panels; links, keyboard and mobile rendering inspected |
| 5. Controlled replay and live pilot | Saved replay evidence then one user-selected county run | Crash recovery, idempotence, comparison cases, manual source fidelity, roster reconciliation, and user-review packet |

Use the invoking model under MODEL_EXECUTION.md. Preserve the working tree,
originals and history. The proposed design decisions below are historical and
do not override the current user request.

Pending decisions: user acceptance of this checkpoint/comparison behavior and
implementation plan; selection of the first live pilot county. Continue design
review until those decisions are settled rather than treating silence as approval.

## Failure-case acceptance matrix

These are required behavioral checks, not executed test results. Each implemented
test must demonstrate the observable result below and fail when the relevant guard
is removed. Cloud review must inspect assertions and actual stored/rendered output;
worker-reported passing totals alone are insufficient.

| Scenario | Required observable result |
| --- | --- |
| Stop after saving a profile but before procedure review | Resume identifies the same active judge and outstanding procedure task; it does not refetch the saved profile merely to rediscover its links |
| DB failure before commit | Old revision/active judge remains; no capture acknowledgment or complete status is emitted; retained bytes can be retried |
| Process stops after DB commit but before resume-file write | Restart recovers the committed receipt and queue; regenerates resume files; retry does not duplicate observations |
| Two writers submit the same expected revision | At most one transition commits; the other receives a stale-state failure and cannot overwrite evidence |
| Roster changes during the run | Append a cited inventory revision without changing the contract hash; add newly assigned judges; do not infer departure from absence |
| One procedure is linked from two judges | One artifact blob per hash; separate supported applicability links; both judge checklists are complete for their own scope |
| Same bytes at different URLs, or a fresh unchanged response | Preserve distinct source observations/URLs and actual check times while reusing the blob |
| Cached source is blocked on recheck | Prior source remains available as prior evidence; current freshness is unavailable, never silently updated or counted as unchanged |
| Shared order changes after the first judge is completed | First judge gets a dependency follow-up; the county cannot pass while an applicable follow-up remains unresolved |
| Conflicting official phone numbers or procedures | Preserve both source-attributed statements and dates; an accurately recorded conflict alone does not fail source-review completion |
| No mention of a requirement, versus an express statement of no requirement | Different checklist states; both retain the source/search support; no conversion of silence into an exemption |
| Primarily criminal judge with no civil responsibility | Contacts, assignments, official procedure links and applicable shared procedures checked; no forced exhaustive criminal-manual review |
| New county's first collection | Baseline unknown before collection; old requirements become first observations, not new procedural amendments |
| Existing county included in a new composite report without a recheck | Existing records retained with original observations; no new freshness or no-change claim; prior source hashes remain identical |
| New county has a blocked judge | That judge remains in the denominator; no complete county/finalization result; review packet identifies the precise gap |
| Newer draft differs from finalized baseline | Comparison still uses the pinned finalized report, includes supported transitions, and leaves finalization unchanged |
| Value changes A to B to A in the interval | Both recorded transitions appear; net equality does not hide them |
| Effective date is reached without changed source bytes | Flag the effective event for review, with its supported date and applicability; byte equality cannot suppress it |
| An old local AI order has an express successor | Record both documents and exact supersession scope/date; retain history; do not apply replacement to unrelated provisions without support |
| Legacy record has prose but no structured checklist | Preserve the source-backed prose; unmapped topics remain unknown until reviewed; adapter does not manufacture requirements |
| County filter, old report, and new combined directory | New county is isolated correctly; all prior counties remain available; old reports retain their original contents; no Evidence Coverage panel or deleted source columns return |
| Partial or unreviewed record selected for public export | Export rejects the selection; valid original reports are unchanged |

Before live pilot acceptance, manually compare every pilot judge's roster identity,
contacts and procedure summaries to saved official originals. Record exact omissions
and unsupported claims separately from structural test failures. Verify complete
county discovery through official roster/index reconciliation, not a sample of
judges or the number of tests passing. A pilot gap may be presented for review but
does not satisfy the goal's completed-workflow validation requirement.
