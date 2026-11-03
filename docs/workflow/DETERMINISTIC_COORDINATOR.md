# Deterministic weekly update coordinator

The [bounded research scope](RESEARCH_SCOPE.md) governs all returned tasks: Florida
case law, statutes, bar rules, court procedural rules and judicial personnel, with
a civil/commercial focus. Required packets still need supported dispositions;
their presence does not authorize exhaustive pending-bill or rulemaking analysis.
Screen out-of-scope retained material briefly, preserve its evidence and continue.
Do not change existing packet schemas, contracts or dates to apply this scope.

This is the standard sequence for new weekly updates. It replaces run-specific
report/roster assembly scripts. Existing source/opinion review and publication
validators remain authoritative. It does not expand research coverage, change
historical reports, or start an inference server. Use the invoking model.

## Start or recover

For an existing `RUN/workflow/contract.json`, resume with `workflow next-task`
using the pinned checkout, after waiting for any live command. Its database-backed
result overrides stale RESUME.md checklists. Resume notes retain useful context;
they do not authorize another initialization, acquisition or replacement run.

### Moving a checkout during research

For a moved checkout whose acquired run is still in source/opinion review, use
the installed launcher from the **new** checkout:

```
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py \
  --checkout /absolute/new/checkout workflow relocate \
  --run-dir /absolute/new/checkout/runs/existing-run \
  --reason 'Checkout moved; preserve the existing acquisition and reviews'
```

The original database must remain available and the run must retain its relative
location inside the moved checkout. Update the installed skill's checkout binding
separately if necessary. Do not restore retired path links, replace strings in
accepted evidence, edit contract JSON, call `init`, or refetch to recover a move.

`relocate` preserves the exact original contract under
`RUN/workflow/relocations/ORIGINAL_CONTRACT_SHA/contract.json`. It freezes the old
coordinator stream with an append-only relocation marker and records a new binding
with the same database, registry, run ID, dates, mode and baseline. Original source
captures, accepted packets/receipts and domain reviews are unchanged. Existing
hash gates reuse completed reviews. Prior coordinator history stays in its original
stream, linked by the new contract's `relocated_from` provenance; it is not silently
rewritten or copied as new model review. Machine supplemental coverage is re-proven.

Run the returned `next-task` command after success. It regenerates path-bound
pending tasks without acquisition; use that current packet, not an old submission
command. New task/acceptance files use a contract-specific `bindings` subdirectory
so even an unchanged machine packet cannot overwrite its pre-move counterpart.
Compare any privately drafted answer against the current evidence binding
before applying it. A retry after an interrupted relocation restores the same saved
binding. Both coordinator and acquisition locks must be idle. Missing/tampered
original contracts, still-existing source runs, unresolved submissions and any
downstream editorial/assembly/publication state are refused. Resolve those states
before moving; this command does not discard them or relocate the database.

A rejected draft followed by an accepted receipt for the exact same packet is a
completed review, even when the repaired receipt differs; both attempts stay in
history. A source-domain correction without its matching coordinator decision
still blocks recovery and downstream work, including across predecessor bindings.
If a source decision predates a completed move, pass the preserved packet's actual
new filesystem location to `workflow decision` and `workflow revise`, using the
current run directory. Do not edit the old paths inside the packet. The correction
is appended to the current binding, preserving the original decision and packet.

Run from the current checkout with its Python environment and absolute `PYTHONPATH`.
The installed skill launcher supports `--checkout PATH`; verify actual imports.

```
flwu workflow init --run-dir RUN --database DB --registry REGISTRY \
  --run-id UNIQUE_ID --end YYYY-MM-DD --mode publish --archive website/updates
flwu workflow next-task --run-dir RUN
```

Supply `--start YYYY-MM-DD` only for an explicit interval. Otherwise the last
finalized report is the baseline and the interval starts the day after its
`contract.window_end`; a later publication timestamp does not skip intervening
days. Legacy period-less captures retain their timestamp fallback. A partial
research run never advances this baseline.
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
Keep this entry note current and concise. Archive superseded checkpoints with
their bytes preserved and link the archive; do not append stale instructions
indefinitely or load that history unless a specific evidence question requires it.
The workflow database events are authoritative, not the presence of output files.

## Follow one returned step

1. `workflow next-task` returns either an exact shell command or a packet path.
   Execute that command with its pinned interpreter/checkout. Do not substitute a
   global `flwu`, script your own report assembly, or write database SQL.
2. For a packet, read its returned `review_guide` and linked current/previous evidence.
   The version-3 entry guide includes `research_scope`: the common purpose and
   stopping rules plus directions for this task type. Read it first. These are
   guide instructions, not receipt fields; use the unchanged exact template.
   Existing packets, accepted decisions and older guide files remain unchanged.
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

### Reused discovery exclusions

`workflow next-task` can record `unchanged_finalized_discovery_exclusion_v1`
without another model receipt. This is limited to source findings classified
with exact Boolean `discovery_only: true` and `publication_ready: false`, in
statute, court-rule, administrative-rule or case-law metadata inventories. The
finding must be no newer than the pinned finalized baseline, retain its exact complete
finding hash, and have a checksum-verified finalized exclusion with no candidate.
Acquired quoted citations and the required source hash are validated again in
code. A prior coordinator decision containing personnel, inventory or removal
projections is ineligible.

Available unfinished source reviews and any effective-date task disable this
reuse. Changed/new finding versions, substantive candidates, personnel, opinions,
missing or invalid evidence, and incomplete classifications retain their normal
review paths. Source/status discovery and hash gates run independently. Retrieval
failures still require coverage dispositions and do not become no-change results.

Machine receipts preserve the original finding, evidence, review scope and gaps;
their provenance identifies the finalized baseline, acceptance checksum, prior
disposition hash and exact finding/source hashes. Do not reopen those unchanged
inventories or author replacement model exclusions. A reused discovery inventory
does not claim review of its linked documents, resolve a conflict, certify roster
or source completeness, or advance the reporting baseline. Process the next
returned packet and retain its separate candidate/body reviews.

### One canonical personnel projection

For each stable person ID, put the complete current personnel projection in one
owning publication mapping. Companion source mappings retain their own citations
and decisions, with `personnel: []`; they do not supply competing snapshots of the
same person. Preserve each source's statements and any recorded conflicts in the
owning record. Additional supported contact fields belong in that same complete
record, without discarding earlier fields or choosing which conflicting source
controls.

Person-name support uses the existing roster validator's case and whitespace
normalization. An uppercase or line-wrapped full source name can support its
display casing; aliases, missing initials and different names are not inferred.
Keep quotation bytes exact: never recase or retype a quote to satisfy the gate.

Roster inventories may retain unquoted acquisition references in `citations`;
code still checks their exact URL, raw/text hashes, timestamp and HTTP result.
Each `facts.entities[].citation` must separately quote and support that person's
full name. Judge/clerk records still require quoted top-level evidence. Do not
invent excerpts for transport metadata or treat metadata as a reviewed identity.
Assembly shares one acquisition index only within its read-only pass; a later
pass constructs a fresh index, and referenced artifact hashes remain checked.

For a new directory entry, `inputs.source_role` carries the accepted finding's
published role when present. Code maps it through the shared supported-role table
(for example, special master or general magistrate); the internal `judge` record
category does not establish a judge title. Unsupported explicit titles stop the
new projection rather than silently becoming judges. Existing directory titles
remain unchanged by contact updates.

After source/hash review, code skips exact existing-person directory projections
when names, supplied official links, assignments and displayed contact rows are
unchanged. Only contact-row `fact_path` provenance is ignored; labels, values,
links, types, order, duplicates and other metadata remain significant. This is
not another model review or a waiver of source, identity or publication checks.

If later evidence requires changing an already accepted projection, inspect the
owning decision with `workflow decision`, save a new full receipt, and use
`workflow revise` with its exact predecessor hash. Alternatively, consolidate into
a newer complete owning mapping and append-only revise the earlier mapping to
remove its duplicate projection. Keep original receipts and captures intact. Two
different active projections for one stable ID block assembly; do not repair this
by editing accepted files or silently dropping contact fields.

### Contact presentation changes

`src/flwu/data/web/directory-format.json` contains reviewed display rules; it does
not replace source evidence. `person_fields` rules apply only to the exact saved
field value. When a renamed label would retain an obsolete duplicate row, add a
`contact_replacements` entry keyed by the canonical person ID. Each rule has
exactly `side` (`office` or `assistant`), nonempty `before` and `after` arrays of
rendered contact rows, and a substantive `reason`. Copy `before` from the current
directory and `after` from the validated proposal. Retain phone extensions,
email purposes and distinct office/mailing locations. Do not infer equivalence
from similar labels, or delete a contact merely because a partial source omits it.

The coordinator binds that person's rules into the `directory_review` packet.
Review the exact old and proposed rows and their source-bound facts before
submitting the ordinary receipt. A rule removes only its exact old rows, only
when every declared replacement occurs in the current proposal. Only
`fact_path` provenance metadata is ignored in matching. Changed values or other
metadata prevent the rule from applying; unmatched rows follow the existing
label-based merge. Refresh uses the packet-bound rules. Editing configuration
after review requires a newly generated packet and review, rather than editing
an accepted receipt. Never edit public supplements to bypass this sequence.

The v2 entry guide includes `entity_entry_counts` for indexed findings containing
an entity list. Use `by_recorded_type` when describing its saved role counts:
the total includes every entry, including clerks and duplicates. Missing types
are counted separately as `untyped`; no role is inferred. These counts do not
certify unique people, current membership or roster completeness, and do not add
receipt fields. Existing v1 guides, finding files and task packets stay unchanged.

### Hash identities and submission handoff

Preserve supplied hashes; the submit command validates their bindings. Source
and extracted-text hashes identify exact bytes. `raw_comparison_sha256`, packet
identities and decision identities instead hash canonical JSON objects using
`flwu.history.sha`: sorted keys, compact separators and UTF-8 without ASCII
escaping. Hashing a pretty-printed JSON file with `shasum` is not an equivalent
check. Linked template, changed-line and indexed-finding file hashes explicitly
identify those files' bytes. Do not rebuild hash or quotation validators during
research; use the coordinator and investigate its actual validation errors.

For a bounded delegated task, successful submission means the submit command
exits zero and returns the expected `packet_sha256` and a `capture_id`. Return
those values and the receipt path to the parent, then stop. The parent performs
independent persistence and semantic review. The returned capture identifies the
coordinator decision; `validation.capture_id` in its saved event identifies the
underlying domain review and can legitimately differ. Do not search filesystem
text or inspect implementation code to reconcile these distinct identities.
An exact replay may instead return `replayed: true` and the packet identity;
report that response without inventing a new capture ID. The parent can inspect
the accepted decision with `workflow decision --run-dir RUN --packet PACKET`.

### Review requirements

The coordinator applies the [versioned content/component hash gate](SOURCE_HASH_REVIEW.md#versioned-contentcomponent-reuse)
before generating tasks. Proven reuse has append-only machine provenance; it is
not another model review. Process only returned packets. Do not reopen reused
sources, recalculate their hashes or create replacement no-change receipts.
Unsupported or unresolved changes still receive the normal review below.

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
  A previously reviewed shared block may supply its interpretation on another
  page only after code verifies that both before and after values are exactly
  equal in the supplied original and decoded comparison entries. Record the
  prior reviewed packet and equality evidence in the run workspace. Inspect the
  current source's identity, relevant personnel/operating fields and every unique
  change separately; a shared widget does not establish that a whole source is
  unchanged or irrelevant. Keep the current template's source bindings, comparison
  hash and change IDs, and explain every current change. Reuse only the supported
  meaning of the matched block within the current reporting scope. Do not copy
  another person's name, contact facts, citations or entire receipt. A path,
  hostname, tag name or empty text diff is insufficient evidence of equivalence.
  This permits bounded interpretation reuse, not an automatic no-change classifier
  or omission of required review tasks.
  Changed originals with identical extracted text also require
  `raw_change_review`. Read `raw_comparison_path`: HTML comparisons include
  attributes and embedded JSON, while binary span comparisons require review of
  the original documents with appropriate tools. Explain each exact change and
  inspection method; never infer harmless metadata from an empty text diff.
  Earlier same-text reviews lacking this evidence are retained but not reused.
  Later identical fetches retain the unreviewed original-content transition;
  retrieval alone cannot clear that pending review.
  When extracted text changes, the task also supplies the original and decoded
  comparisons as an `inspection_aid`. Read them alongside the text diff rather
  than writing byte-diff or decoding scripts. This aid makes no relevance decision
  and does not change receipt acceptance or completed-review reuse. Fill
  `raw_change_review` only when it appears in the supplied receipt template;
  otherwise explain material original-content differences in `support.reason`
  without adding receipt fields. Parser output is not browser rendering, and
  document byte spans still require appropriate original-document inspection.
  Missing extraction stays unresolved. Preserve complete existing nested facts
  and `expected_version`; a partial replacement cannot erase prior fields.
  Limit verification claims to facts supported by this task's source. A prior
  finding may cite several pages: retaining its other facts does not reverify
  those pages. State observed field/value changes without inventing their cause;
  a timestamp alone does not prove CMS generation, publication or refresh.
  Different date formats alone do not establish conflicting dates. Distinguish
  added entries from retained entries, and linked-file metadata from inspected
  file contents. Keep the explanation focused on the effect on supported facts;
  the exact quotations already preserve the underlying values.
  An early link-discovery finding may retain an old `review_status` label after
  a separate document review was completed. Before declaring the document unread,
  inspect its related current findings, inventory review records and URL-bound
  accepted reviews. Retain their actual review and provenance limits. A missing
  registry entry does not prove missing evidence. Add relevant omitted URLs to
  the ongoing registry so future acquisitions can compare their hashes; do not
  change a pinned run contract or repeat completed legal analysis to repair
  registration. Identical accepted document reviews still use machine reuse.
- **opinion_review:** Read original/extracted opinion and status metadata. Relevant
  opinions need concise summary, holding, disposition, author names and quotations.
  An unchanged PDF with changed withdrawal/substitution status still needs review.
  If code confirms an identical PDF and a completed prior interpretation, retain
  that interpretation's actual scope; review the full metadata change and bind
  current citations without asserting a new full-PDF merits review. New or changed
  PDFs require their normal original-document review.
  Identical completed reviews are reused. `uncertain` is not completed screening.
- **coverage_review:** Describe the exact saved failure or supported exclusion.
  Completed supplemental sources are reconciled automatically as
  `reviewed_supplement` only with current exact-source acquisition/review proof;
  follow SOURCE_HASH_REVIEW.md for supplemental registry commands and evidence
  locations. Do not write a model receipt for machine reuse. Queue and packet
  identities bind the current evidence, so a later change cannot reuse an older
  URL-only disposition. Interrupted receipt projections are restored from the
  database without repeating completed analysis.
  Never turn an unavailable listing into “no new opinions.” Available unread
  sources cannot be dismissed as unavailable. Resolve material effective dates.
- **publication_mapping:** Use the supplied reporting window and exact saved
  finding/version. Choose news inclusion, directory inclusion, or a cited exclusion.
  For an already-reviewed opinion, first inspect its issue date, official metadata,
  accepted review summary and reporting window. Retain the accepted interpretation
  of any correction, substitution or withdrawal: an earlier original issue date
  alone cannot exclude an in-period revision or status event. For a date-only
  exclusion, a short literal issue-date excerpt with its exact acquisition binding
  and locator is sufficient; do not copy the entire opinion quotation or repeat
  completed merits analysis. Before including an opinion or changing reader-facing
  fields, read its complete accepted finding and preserve its qualifications.
  These publication choices follow the source hash/status gate; they do not replace
  that gate or let the model infer source equality. Accepted opinion fields are
  preserved. A separate effective-date task remains meaningful when the opinion's
  earlier issuance was excluded as old news. Read the event's saved finding and
  citations, preserve current source-status limitations, and decide its relevance
  to this period. If inclusion is warranted, supply the supported `effective_date`
  and use `workflow revise` to correct any completed machine mapping that excludes
  the same opinion by its older issue date. Do not treat unchanged bytes or the
  old-news exclusion as completion of the effective-date review. A coverage
  disposition must explain where that event is handled or why it is outside scope.
  Clock triggers recognize explicit `effective_date` and `row_effective_date`
  fields, including nested assignment rows. Preserve each conflicting statement;
  issuance/recording dates are not effective dates. The event requests review of
  the saved evidence and current status, not automatic application of an assignment.
  Directory additions require named roster
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
- An opinion interpretation accepted before the pinned finalized baseline, with
  a current, completed PDF/status reuse signature and an issue date before the
  reporting start. This also handles a legacy baseline without mapping receipts.
  Code records `unchanged_prebaseline_opinion_outside_period`, the accepted review
  hash, current acquisition capture and signature. It excludes repeat news; it
  does not assert that the opinion was previously published by this site.
  Recorded issue and official metadata dates must agree. Available citations must
  validate against exact stored acquisition evidence; missing legacy HTTP fields
  are never guessed. Without sufficient bound citations, return a model task.
  If the official PDF URL changes (for example its version parameter),
  `unchanged_prebaseline_opinion_url_alias_v1` can reuse the interpretation only
  when the same stable opinion identity, raw PDF hash, official status hash and
  review signature match. A validated citation must bind the accepted old URL,
  and the current official URL must have a successful acquisition of those exact
  bytes. The machine receipt preserves the old citations and records both URLs
  and acquisition capture IDs. A URL change alone is not a substantive revision;
  failed retrieval, changed bytes/status and missing original evidence remain tasks.

Other changed-period decisions still receive model review. Changed opinion bytes,
status or editorial review version do not inherit a stale mapping. Removals never
replay automatically. Preview-only and incomplete runs supply no reusable baseline.
Every reuse receipt records its policy, baseline capture and predecessor decision
or accepted interpretation hash; it can be corrected through the normal
coordinator revision command.

The pre-baseline policy additionally requires the accepted interpretation itself
to predate that baseline. A late-discovered opinion with an old issue date, a later
editorial correction, a date inside/on the reporting boundary, a failed current
download/status check or a changed review protocol remains explicit work. Code
performs the date comparison after the hash/status review gate; a model does not
re-review unchanged merits merely to decide whether an old date is before start.
Previously accepted current-run mappings remain immutable and are not overwritten.

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
