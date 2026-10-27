# Deterministic weekly update coordinator

This is the standard sequence for new weekly updates. It replaces run-specific
report/roster assembly scripts. Existing source/opinion review and publication
validators remain authoritative. It does not expand research coverage, change
historical reports, or start an inference server. Use the invoking model.

## Start or recover

For an existing `RUN/workflow/contract.json`, resume with `workflow next-task`
using the pinned checkout, after waiting for any live command. Its database-backed
result overrides stale RESUME.md checklists. Resume notes retain useful context;
they do not authorize another initialization, acquisition or replacement run.

Run from the current checkout with its Python environment and absolute `PYTHONPATH`.
The installed skill launcher supports `--checkout PATH`; verify actual imports.

```
flwu workflow init --run-dir RUN --database DB --registry REGISTRY \
  --run-id UNIQUE_ID --end YYYY-MM-DD --mode publish --archive website/updates
flwu workflow next-task --run-dir RUN
```

Supply `--start YYYY-MM-DD` only for an explicit interval. Otherwise the last
finalized report is the baseline; a partial research run never advances it.
Resolve the end date once (normally the last completed Sunday, Monday–Sunday
reporting). Init pins the checkout, database, registry, interval, run ID, mode,
directory paths and baseline. Repeating identical init is safe; changing a pinned
input requires a new run directory. All current county/court supplements are
selected by default; use explicit repeatable `--directory PATH` for a narrower
scope, or `--no-directories` for an isolated opinion-only exercise.

For a preview use `--mode preview`; do not supply a production archive or promote
the result. Preview completion never finalizes a report or deploys a site.

Save the run path, goal and process session in RUN/RESUME.md. After compaction,
read that file and use `workflow status`; do not repeat setup or invent a run ID.
The workflow database events are authoritative, not the presence of output files.

## Follow one returned step

1. `workflow next-task` returns either an exact shell command or a packet path.
   Execute that command with its pinned interpreter/checkout. Do not substitute a
   global `flwu`, script your own report assembly, or write database SQL.
2. For a packet, read its returned `review_guide` and linked current/previous evidence.
   The guide indexes verbose prior findings by key, version and file hash; open
   each full finding you need before changing it. The full immutable packet keeps
   all original inputs and remains the submission identity.
   The entry guide links the exact receipt template and changed-line JSON instead
   of duplicating their quotations. Follow `receipt_template` and
   `inputs.changed_text_lines_path` when present; inspect every changed line with
   its source context. Read one needed indexed finding at a time, not all files
   through a wildcard. If output is truncated, read the missing JSON field or
   section before deciding. The original full guide remains separately available
   as `full_review_guide`; these links do not waive any evidence review.
   Copy `receipt-template.json` to `save_receipt`, fill its prescribed fields,
   and execute the returned submit command. The packet contains an envelope
   schema, field guidance, save paths, exact evidence/version bindings and checks.
   Do not edit packet.json, invent hashes, or fill unrelated future receipts.
3. After success request the next task. Each task is one source, opinion, finding,
   person, named roster or final editorial acceptance. A multi-person source may
   contain several findings; finish and save each person's full fields rather
   than switching courts. Never load the whole research history into context.
4. Validation failures are actionable errors, not permission to loosen a gate.
   Reopen the referenced evidence/field and correct that receipt. If a completed
   interpretation is wrong, use `workflow revise` for source reviews or `opinion-revise`
   for opinion corrections and regenerate tasks; do not edit immutable accepted receipts.

`workflow acquire` calls the actual standard update implementation: all seven
appellate listings, active/inactive feeds, pagination, overlap, tracked status
checks, original-byte storage, hashes and source gate. It holds both the per-run
coordinator lock and existing database acquisition lock. It never calls a model.
Preserve and wait on its numeric tool session. Progress/heartbeats appear on
stderr. Do not start a competing acquisition because stdout is quiet.
`acquisition_complete:false` is a recorded coverage gap, not a no-change finding.
A completed acquire command still requires all subsequent review/assembly steps.

`status`/`next-task` refresh saved queues without network retrieval. Resume an
interrupted acquire with its identical command; saved checkpoints are reused.
Recorded failed sources require a fresh run ID for a deliberate retry; preserve
the failure and limit retries under SOURCE_HASH_REVIEW.md. Never delete evidence
or restart inference as a repair. A busy lock means wait, not delete the lock.

## Task-specific review

- **source_review:** Read current text, prior findings and code-generated diff.
  Code decides equality. The model screens practical civil/commercial relevance,
  explains significance, preserves conflicting official statements and returns
  full source-bound findings. The support entries have exactly raw hash, text
  hash, quotation and locator. Finding citations additionally bind URL/time.
  Changed-byte no-change decisions must cover every changed line on both sides.
  Templates prefill those exact quotations, including nonbreaking spaces and
  extraction-path lines. Preserve them instead of retyping them. Code supplying
  quotations is not a review: read their original context and supply the outcome,
  scope, summary and substantive explanation. New/identical-text sources still
  require the reviewer to select supporting passages where quotes are blank.
  Changed originals with identical extracted text also require
  `raw_change_review`. Read `raw_comparison_path`: HTML comparisons include
  attributes and embedded JSON, while binary span comparisons require review of
  the original documents with appropriate tools. Explain each exact change and
  inspection method; never infer harmless metadata from an empty text diff.
  Earlier same-text reviews lacking this evidence are retained but not reused.
  Later identical fetches retain the unreviewed original-content transition;
  retrieval alone cannot clear that pending review.
  Missing extraction stays unresolved. Preserve complete existing nested facts
  and `expected_version`; a partial replacement cannot erase prior fields.
- **opinion_review:** Read original/extracted opinion and status metadata. Relevant
  opinions need concise summary, holding, disposition, author names and quotations.
  An unchanged PDF with changed withdrawal/substitution status still needs review.
  Identical completed reviews are reused. `uncertain` is not completed screening.
- **coverage_review:** Describe the exact saved failure or supported exclusion.
  Never turn an unavailable listing into “no new opinions.” Available unread
  sources cannot be dismissed as unavailable. Resolve material effective dates.
- **publication_mapping:** Use the supplied reporting window and exact saved
  finding/version. Choose news inclusion, directory inclusion, or a cited exclusion.
  Accepted opinion fields are preserved. Directory additions require named roster
  entities plus complete matching personnel records; optional inventories/personnel
  use the packet's explicit shapes. A role heading is not a person. A missing page
  does not prove departure. Missing roster reconciliation blocks preparation.
- **directory_review:** Review proposed contacts and explicit target IDs for one
  person. Exact IDs/recorded aliases are prefilled; name similarity is only a
  candidate, never an automatic merge. Alias decisions require acquired quotations.
  Matching contact categories are replaced; absent fields, county-specific
  assignments and other people remain unchanged unless an explicit source-bound
  assignment_updates entry identifies that scope and new assignment. Inspect the field audit. This
  projection does not infer new county coverage or departures.
- **roster_review / publication_acceptance:** Named membership and removals must
  reconcile. Then inspect the rendered report, built site, citations, opinions and
  current directory changes. Fill the actual reviewer and legal/visual review.
  Screening, structural validation and a successful build do not establish that
  editorial review occurred. Do not claim human/independent review you did not get.

## Assembly, persistence and publication

`prepare-report` deterministically assembles saved, validated findings and explicit
mapping decisions. It preserves citations, opinion fields and coverage limits;
retains prior personnel/rosters from the pinned finalized baseline without copying
old news into the new issue. It writes a new reviewable capture and acceptance
template. Source failures remain explicit and affected sections incomplete.

`refresh-directory` creates private copies of supplied current supplements and a
field-by-field before/after audit. It preserves original IDs or records an explicit
alias, evidence URLs/hashes/timestamps, unchanged records and county assignments.
It never silently edits live website files. Existing supplements with no supplied
weekly changes are copied unchanged. A source omission is not an instruction to
remove a person/contact. Explicit departures generate separately reviewed removal packets; assignment
corrections use explicit per-scope assignment_updates with acquired quotations.
Unsupported departures or assignments remain blocked rather than inferred.

`workflow build` builds an isolated review site containing the current issue and
supplied supplements. A hash-checked build is required for editorial acceptance.
Interrupted output is preserved; a fresh attempt directory is used. A changed
input invalidates a prior projection/build. Preview mode ends only after separate
acceptance and returns `preview_complete`, `publication_performed:false`.

Publish mode next returns the exact existing `history finalize` command. Only the
separately accepted current capture may advance the baseline. Then `workflow export`
creates a production-format release bundle and a handoff manifest with exact
source/destination paths and destination hashes. It does not deploy. Execute the
returned `workflow integrate` command, then `workflow release-plan`; do not use
legacy unguarded copy commands from older manifests. Follow the release steps
below and [WEB_PUBLICATION.md](WEB_PUBLICATION.md) for credential scanning and
authorized Git/PR/Pages operations. The coordinator advances through
`publication_handoff`, `release_required`, `merge_required` and
`deployment_verification` as applicable. Only `verify-deployment` can record
`publication_complete`. Do not mark the skill's persistent goal complete before
that verification. Do not audit historical reports.

## Isolated reproducible trial

```
flwu workflow trial-init --trial-root /absolute/empty/TRIAL \
  --run-dir /absolute/empty/TRIAL/normal --scenario normal
flwu workflow next-task --run-dir /absolute/empty/TRIAL/normal
```

Follow the generated commands and manually complete the bounded review receipts.
The supported transport supplies synthetic official-shaped pages/PDFs for all
seven courts, with no HTTP fallback. It uses only TRIAL/trial.sqlite and preview
outputs. No manual database edits or orchestration scripts are needed.

After completing normal review, use separate child run directories with scenarios
`unchanged`, `failure`, `duplicates`, and `interrupted`. They reuse the same isolated
trial database. Unchanged reviews must be reused. Failure/duplicate listing scans
must remain incomplete; duplicates must not create duplicate opinion identities.
Interrupted acquisition exits once after a saved page, then the identical command
resumes without refetching that page. Request export before finalization/acceptance
and confirm rejection. Trial mode always rejects production export.

Tests also cover directory aliases, preserving unsupplied fields/other people,
stale input rejection, receipt tampering and interruption between domain-review
commit and coordinator completion. Automated fixture editorial text is test data,
not proof of a model's legal accuracy. Trial records should identify the actual
model review and distinguish rendered UI inspection from HTML-only checks.

Keep executable code fixed during a model trial. Use a dedicated checkout at a
recorded commit when implementation work will continue concurrently, and give the
worker that absolute checkout explicitly. A pinned checkout path does not freeze
its contents: task contracts contribute to packet hashes, so changing code under
a running worker can invalidate pending packets. Record such operator changes
separately from model errors. If submission reports a stale packet, request
`workflow next-task`, read the regenerated contract and revalidate any draft
against its current evidence before submitting; do not alter hashes or rerun
acquisition. Preserve the rejected draft and logs.

## Correcting a completed coordinator decision

Never edit an accepted receipt in place or delete database events. To correct a
current source review, publication mapping, coverage disposition, directory match or removal:

1. Run `flwu workflow decision --run-dir RUN --packet PACKET` to obtain the
   current decision and its `decision_sha256`. Pass that exact digest as
   `--predecessor`. The submission `capture_id`, packet hash and receipt hash
   identify different objects and cannot substitute for this digest.
2. Save a separate corrected receipt using the same schema and acquired evidence.
3. Run `flwu workflow revise --run-dir RUN --packet PACKET --receipt CORRECTION
   --predecessor DECISION_SHA256 --reason "Explanation of the correction"`.
4. Resume `workflow next-task`. Mapping changes require a new report. Directory
   changes invalidate the directory projection and build approval. Complete all
   regenerated review stages before export.

The predecessor check rejects concurrent/stale corrections; an identical retry
is idempotent. Earlier decisions and artifacts remain intact. Once any report in
that workflow has been finalized, initialize a new correction run instead.
Source-review corrections retain the exact accepted source ID, observation,
raw hash and protocol. They revalidate quotations, raw-change review and finding
versions before appending a domain review and a superseding coordinator decision.
An intervening observation or independent domain review requires reconciliation;
do not bypass the predecessor guard. If interrupted after saving the domain review,
repeat the exact correction command and receipt: the domain write is reused and
the missing coordinator decision is appended. Status and downstream preparation
reject a domain/coordinator mismatch until that correction is reconciled.
Resume `next-task` to regenerate
report/build acceptance for the corrected review. Existing reports stay untouched.
Opinion corrections continue to use `opinion-revise`; coordinator correction cannot
change the accepted opinion's holding or authors.

For a damaged review-site build use `flwu workflow build --repair --run-dir RUN`.
The coordinator preserves the damaged attempt and builds a new one. Every output
hash must equal the recorded build; a mismatch requires investigation and cannot
silently inherit approval. This command repairs review-site output only.

## Restoring generated report and directory files

Newly prepared report HTML, acceptance templates, public-preview JSON, directory
supplements, directory audits and export bundles are saved as hash-addressed
original bytes in the research database. Run `flwu workflow repair --run-dir RUN`
when one of these generated files is missing or altered. The command restores the
recorded bytes atomically and retains damaged bytes under `workflow/damaged/`.
It never repairs or overwrites source captures, input supplements or public
website files. It does not repeat research or create replacement review decisions.
Resume `workflow next-task` after repair. Review-site builds use the separate
`workflow build --repair` command above.

Older events without `projection_hashes` have no saved projection set for this
command. Use `prepare-report --repair --run-dir RUN` and then
`refresh-directory --repair --run-dir RUN` to preserve and regenerate their stage
folders from accepted evidence. Regenerated report/template/preview hashes must
match the earlier recorded hashes. New directory projections are validated and
bound to subsequent build acceptance. Do not infer a successful repair from an
empty repair list: run the next-task integrity checks. Missing original evidence
or a regeneration hash mismatch remains a real blocker, not a reason to invent
replacement content.

## Publication mapping reuse

`workflow next-task` and `workflow status` persist deterministic reuse receipts
from the pinned, noninvalidated last finalized report. The complete finding input
(including review version and source binding) must match. Reuse is permitted for:

- The identical reporting period.
- An unchanged directory finding with no removal decisions.
- An unchanged opinion already published in a finalized report whose publication
  date precedes the new period. Code records its exclusion from repeat news and
  retains the original decision reference. Later runs can reuse this exclusion.

Other changed-period decisions still receive model review. Changed opinion bytes,
status or editorial review version do not inherit a stale mapping. Removals never
replay automatically. Preview-only and incomplete runs supply no reusable baseline.
Every reuse receipt records its policy, baseline capture and predecessor decision
hash; it can be corrected through the normal coordinator revision command.

## Publication integration and observed completion

After export, run the emitted `workflow integrate --run-dir RUN` command. It
checks all destination hashes, records an integration intent, and installs only
the accepted bundle. Retry the same command after interruption; already installed
files are recognized by exact bytes. Concurrent edits block integration. Private
preview mode cannot integrate. Do not use the older manifest's unguarded copy
commands.

Commit/push the exact integrated files and open/reuse the release PR under the
existing authorization. Run `workflow verify-deployment --run-dir RUN --pr NUMBER`
to record the observed PR state. The verifier checks that the remote PR commit
contains each integrated file, and requires main as the target. An open PR remains
`merge_required`; merge authorization is unchanged.

After merge, run `workflow verify-deployment --run-dir RUN --pr NUMBER
--deployment-run RUN_ID`. Completion requires the exact merged commit, successful
GitHub Pages workflow and deploy job on main, and matching current issue and
selected directory data fetched from the live site. Failed/skipped deployment,
stale live content or mismatched files leave the run incomplete. These checks do
not inspect historical reports. `workflow status` records the verified completion
and timestamp; it does not silently initiate repeated network checks.

Before Git mutations run `workflow release-plan --run-dir RUN`. The coordinator
persists the intended branch, starting commit, exact file list and shell-quoted
commands. On interruption inspect/reuse the recorded branch, commit and remote PR
before repeating a step. Run the credential scan and check the no-reply identity
before committing; the commit command limits content to the release paths.
Commit/push/PR creation and authorized merge remain explicit agent-executed steps
under the existing release procedure. The durable plan and observed PR state
supply their recovery checkpoint; no autonomous merge permission is implied.
