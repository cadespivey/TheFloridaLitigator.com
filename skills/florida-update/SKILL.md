---
name: florida-update
description: Run The Florida Litigator's bounded civil-litigation update for Florida case law, statutes, bar and court procedural rules, and court personnel; persist hash-gated findings and refresh reviewed website data.
---

# Florida Litigator update

Invocations: `$florida-update`, `$florida-update through YYYY-MM-DD`, or
`$florida-update since YYYY-MM-DD through YYYY-MM-DD`. A request for a preview or
no publication restricts the final phase accordingly.

## Bounded research purpose

Cover Florida case law, statutes, bar rules, court procedural rules and judicial
personnel, prioritizing civil/commercial practice. After launcher preflight read
the verified checkout's `docs/workflow/RESEARCH_SCOPE.md`; it governs every phase
and supersedes broader old examples. Preserve the whole statutes comparison corpus
and collected evidence without treating retention as exhaustive substantive review.
Pending bills, rulemaking processes and general agency regulation receive only
brief screening or status verification needed for an in-scope actual change or a
minimal follow-up link. Do not analyze every proposal, form, penalty schedule or
administrative order. Handle out-of-scope queued material with a short supported
disposition using the existing schema, then continue. Do not expand the run merely
because an old note or source index identifies more material.

## Execution and authority

Use the model selected in the invoking Codex or codex-local session. No named
model, local provider or cloud provider is required. Do not stop or ask the user
to change models because of an earlier preference. The skill cannot switch its
running model. Record the model/provider only when exposed by the session;
otherwise record unavailable rather than guessing. Do not restart inference
servers, unload models, install packages or launch another worker.

Do not infer the inference provider from the Codex client name. A local worker
still runs through Codex. If a supplied assignment or runtime preflight identifies
the model, cite that source; otherwise leave model/provider unavailable.

The current model-neutral request supersedes earlier named-model restrictions for
this workflow. Follow repository docs/workflow/MODEL_EXECUTION.md. It does not
resume the completed statewide baseline goal. Perform analysis in this session,
one task at a time. Invocation to update the database and website
authorizes the ordinary validated update and publication steps below; honor any
narrower request. Do not ask for the same publication authorization again.

## Persistent goal — required

The user explicitly authorized goal-backed execution for this skill in Codex and
codex-local. Use the session's persistent goal tools; a Markdown checklist alone
is not a goal. At invocation call `get_goal`. Reuse a matching unfinished Florida
update goal; do not create a duplicate on continuation or compaction. If another
unfinished goal has a different objective, ask how to handle that conflict; do not
mark it complete, replace it or pause it merely to start this workflow.

When no unfinished goal exists, call `create_goal` before acquisition with this
objective, inserting any dates or narrower scope the user supplied:

> Complete a bounded Florida Litigator update covering civil/commercial-relevant
> case law, statutes, bar rules, court procedural rules and judicial personnel,
> using the last finalized report
> as baseline unless an explicit start is supplied, and the resolved reporting
> cutoff. Run seven-court opinion discovery and registered-source hash acquisition;
> process all required review tasks and persist validated findings with evidence
> readback; prepare and validate the report and affected current directories;
> publish the authorized website data and verify successful deployment and live
> content. Preserve historical reports and record coverage failures honestly.
> Briefly screen or exclude out-of-scope pending legislation/rulemaking; exhaustive
> proposal, agency-regulation, form or litigation-merits analysis is not a task or
> completion gate. Preserve the full statutes corpus and existing evidence.
> Completion requires saved database capture IDs, disposition of every required
> review task, validation results, and publication/deployment evidence (or the
> explicitly requested preview deliverables). Starting or finishing acquisition
> alone is not completion.

Do not set a token budget unless explicitly requested. Pin the resolved dates,
registry, database, run ID and exact goal objective in RESUME.md once established;
do not create a replacement goal simply to add those details. If goal tools are
unexpectedly unavailable, report that capability failure rather than claiming
persistent continuation is enabled.

In an explicitly delegated validation trial, the parent may own the persistent
goal while a noninteractive worker lacks goal-tool support. Record that limitation
once and continue the authorized assignment in the same run; return its real
completion or blocker to the parent. Do not repeatedly call unavailable goal
tools or claim that a worker checklist creates automatic continuation. This
exception does not replace goal-backed execution for ordinary interactive runs.

On every automatic continuation: call `get_goal`, read RESUME.md, inspect the saved
process/session state, and perform the next unfinished phase. Do not rerun setup,
create a new run ID, or launch acquisition just because a new model turn began.
If `RUN/workflow/contract.json` exists, use the pinned checkout's
`workflow next-task --run-dir RUN` after any live command exits. Its database-backed
result is authoritative. RESUME.md supplies context and identifiers; its handwritten
checklist may be stale and cannot override coordinator state. Do not reconcile
stale notes by reinitializing, reacquiring, or inspecting old task/log directories.
Record the correct next command in the resume note while preserving useful context.
Keep the goal active while acquisition runs. Wait on its existing tool session;
when it exits, proceed to analysis, persistence and publication without waiting
for another user prompt. A turn boundary or compacted context is not a checkpoint
requiring permission to continue.

Never mark the goal complete for “started,” “background process running,”
“acquisition completed,” or “queue generated.” Call `update_goal` with complete
only after every authorized deliverable has actual verification evidence. Honor
explicit user pauses and the goal tool's blocking/budget rules. A persistent
source failure is a recorded gap, not permission to fabricate completeness;
continue independent work and apply the publication gates. If an external blocker
ultimately prevents completion, preserve progress and follow the tool's blocked
criteria rather than repeatedly relaunching or falsely completing the goal.

## Locate the working installation

Use the skill's pinned launcher for **every** `flwu` command:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py --check
```

Read the reported checkout and imported module paths; then change your shell's
working directory to that checkout before reading repository files or writing run
artifacts. The default is
the checkout recorded in the installed skill's `installation.json`; the repository
copy can use its own checkout. There is no development-worktree fallback.
The root `/Users/cadespivey/Developer/FloridaLitigator/florida-litigator-weekly-update` is an older dirty
checkout, not the workflow source. Its editable-installed `flwu` lacks `update`.
Do not use bare `flwu`, `.venv/bin/flwu`, or relative `PYTHONPATH=src` as a fallback.
Do not conclude the feature was removed after inspecting the old root checkout.

The launcher pins the absolute source path, verifies actual imports and the
`update` subcommand, and executes from the selected checkout. It uses the existing
root Python environment without installing anything. To select another current
checkout, pass `--checkout /absolute/path` on **every** launcher invocation and
verify `--check` first. If preflight fails, inspect Git worktrees and current main;
preserve dirty files and use a current isolated checkout. Do not reset either
checkout or reinstall the package to work around the mismatch.

Read AGENTS.md in the verified checkout. Fetch main and use a current branch or
worktree when needed, preserving unrelated changes. Database:
`/Users/cadespivey/.local/share/flwu/research-history.sqlite`.
Never substitute a trial database or the legacy directory database.

In this skill and linked runbooks, `flwu ARGS` is shorthand for
`python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py ARGS`.
Use that expansion consistently for history, source-gate, opinion-review,
research, site and publish commands. Relative run/output paths resolve inside the
verified checkout. For Python module helpers, use the root `.venv/bin/python`
with `PYTHONDONTWRITEBYTECODE=1` and an **absolute** `PYTHONPATH` to that checkout's
`src` directory, from that same checkout.

Keep scratch files and helper scripts under the assigned run directory. An
output-only assignment's allowed paths include these files too; `/tmp` is not an
exception. Read-only inspection does not authorize writing a helper elsewhere.
Use returned commands directly; if piping output, preserve the command's exit
status with `set -o pipefail` and inspect errors before continuing.

Read these current repository instructions before collection:
- `docs/workflow/RESEARCH_SCOPE.md`
- `docs/workflow/DETERMINISTIC_COORDINATOR.md`
- `docs/workflow/SOURCE_HASH_REVIEW.md`
- `docs/workflow/OPINION_DISCOVERY.md`

## Establish a durable run

1. Resolve dates in America/New_York. Default end is the most recent completed
   Sunday; on Sunday use the previous Sunday unless the user requests a partial
   current-day run. Explicit dates override this. Default start is the last
   finalized report's reporting-period end plus one day for the chosen stream,
   not its later publication date or the latest research attempt. Legacy
   period-less captures retain their timestamp fallback; an already covered
   cutoff stops rather than generating a duplicate interval.
2. Use `flwu history streams --database DB` and the current finalized report's
   capture/contract to identify the live weekly stream. Do not choose a trial,
   synthetic, county-only or acquisition stream. If multiple plausible weekly
   streams exist, ask for that choice before writing. No finalized baseline
   requires an explicit start; never invent one. If no new reporting interval
   exists, report that rather than issuing a duplicate weekly report.
3. Reuse a registry reviewed under the current bounded scope. A registry approved
   under the older broader scope needs one scope review before a new acquisition;
   thereafter reuse that list and classify only additions. Record parked source
   IDs, URLs and reasons in `RUN/registry-scope-review.json`, retaining prior
   registry/evidence files. Do not keep monitoring unrelated agency/proposal pages
   merely because they appeared in an old run; do not remove in-scope sources
   because retrieval failed. An existing pinned run keeps its registry unchanged.
   If no reviewed registry exists, run `flwu source-gate inventory
   --database DB --stream STREAM --output RUN/registry-candidates.json`; review its
   scope against the county source index and current public directory supplements.
   Inventory from one weekly stream does not automatically include all county
   baseline streams. Include their supported current profile/procedure/contact
   sources and relevant statewide statutes/rules. Save the reviewed ongoing
   registry at `runs/updates/registry.json`; record additions and known gaps.
   Do not certify statewide coverage from an unreviewed URL list.

   Before initializing a new statewide run, check the ongoing registry against
   the reviewed directory inputs (do not modify an already pinned run):

   ```sh
   flwu source-gate reconcile --registry runs/updates/registry.json --directories website/county-directories --output RUN/next-registry.json --manifest RUN/registry-reconciliation.json
   ```

   This preserves existing sources and adds published primary profile/procedure
   and court-index links from all 67 counties/20 circuits. Read its counts and
   supporting-candidate scope list; do not dump the full manifest into context or
   automatically collect all supporting citations. Use the reviewed next registry
   for the new run and retain the manifest path in RESUME.md. Registration is not
   a fresh retrieval or completed source review. For a new URL's baseline context:

   ```sh
   flwu source-gate context --registry REGISTRY --manifest MANIFEST --url 'EXACT_URL' --limit 5
   flwu history artifact --database DB --sha256 BASELINE_SHA256 --output RUN/baseline-original.bin
   ```

   Follow `next_offset` with `--offset` when needed. References identify the county
   directory, stable person ID, baseline stream/checkpoint and available original
   hashes/timestamps. Read one person and source. Do not invent a compatible gate
   receipt from a county directory's review status. An unmatched initial source
   still needs its bounded source review. Preserve baseline evidence and failures.
4. Use `runs/updates/<unique-run-id>/` for private evidence, receipts and progress.
   Write `RESUME.md` with checkout, DB, exact stream, registry, dates, run ID,
   next task, completed receipts, coverage gaps, persistent goal objective/status
   and publication status. Back up
   the live database with SQLite's backup API before the first write; do not copy
   a live SQLite file with ordinary filesystem copying.

## Follow the coordinator through completion

Public writing must describe a supported material legal/procedural/personnel
change and its practical effect. Exclude inconsequential differences and source-
reconciliation bookkeeping. Do not publish a research-incomplete notice or explain
that saved findings/compilations disagree as the news item. Keep those records
internally. Retrieval/discovery alone does not establish a new legal development.
For included statute/procedural/local-rule candidates, `candidate.change_analysis`
has exactly `material:true`, `previous_requirement`, `current_requirement`,
`practical_effect`, `basis_quote`. Supply an exact quote present in the publication
citations and concise, accurate public prose about what changed, to whom it applies,
when supported, and what practitioners should do. Do not guess effective dates or
resolve conflicting authorities by assertion. If an actual change cannot be
supported, exclude the item. The code's structural checks do not certify the model's
legal interpretation; the publication review must assess the claim and citations.

Read `docs/workflow/DETERMINISTIC_COORDINATOR.md` and
[process lifecycle](references/process-lifecycle.md). Initialize the resolved run:

```sh
flwu workflow init --run-dir RUN --database DB --registry REGISTRY --run-id RUN_ID \
  --end YYYY-MM-DD --mode publish --archive website/updates
flwu workflow next-task --run-dir RUN
```

Use the verified launcher above for these commands. Add `--start` for an explicit
start; use `--mode preview` for a preview request. Current supplements are selected
by default. Do not replace this with a hand-built report workspace or assembly script.

The registry is a JSON object: its source list is `registry["sources"]` and its
stream is `registry["stream"]`. Current supplement directories are
`website/county-directories/` and `website/court-directories/`; there is no
`website/directories/` input folder. Init selects both directories by default.

Execute each returned command, or read the returned `review_guide` (the full
packet remains available), copy its
receipt template to its specified receipt path, complete the evidence-bound fields,
and execute its submit command. Then request the next task. Packets supply schemas,
current/prior source evidence, full finding versions, save paths and completion
checks. Code compares hashes/status, maintains bookkeeping, assembles the report
and projects directory deltas. You interpret relevance, write supported findings
and summaries, resolve explicit identity choices, and perform editorial review.
Use concise civil/commercial operating summaries. Noncivil subjects need contacts,
assignments, links and basic shared instructions only. Preserve documented source
conflicts without deciding which authority controls.

Source templates prefill exact changed-line quotations, including whitespace and
extraction-path lines. Keep them intact; do not reconstruct them by typing or
replace them with paraphrases. Read every changed line and sufficient original
context, then supply the outcome and substantive explanation. Prefilled citations
are not completed review. When changing a prior finding, open its indexed full
file first and preserve its nested facts and version guard. If two receipt repair
attempts fail, save the exact errors and a checkpoint for supervisor review rather
than repeating speculative edits or claiming completion.

For source-review interpretation boundaries, follow the runbook's **Task-specific
review** section: retaining a finding does not reverify its other cited pages;
observed timestamps do not establish their cause, and different date formats do
not alone establish a conflict. Describe the effect on facts this source supports.

Code first reuses identical raw hashes or a versioned, supported content/component
hash proof. Reused entries already have machine provenance; do not reopen them or
write model receipts for them. See SOURCE_HASH_REVIEW.md's content/component policy.
Known metadata is preserved separately; arbitrary model-side filters are prohibited.

For the review loop, use the checked step helper instead of shell pipelines or
run-specific submission scripts:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py next --run-dir RUN
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py submit --run-dir RUN --packet PACKET --receipt RECEIPT
```

Pass `--checkout CHECKOUT` before the action when overriding installation.
Read the returned `next_state` file and follow its actual phase. The helper keeps
full stdout/stderr/exit codes in `RUN/agent-steps/`, stops after failed submission,
and atomically replaces `RUN/agent-next-task.json` only on successful valid output.
It does not complete the workflow or replace acquisition/publication commands.
Wait its existing tool session if still running; never launch another copy merely
because stdout is quiet.

If the returned phase is `source_review_correction`, read `correction_guide` and
the returned review guide. Copy `receipt_template` to `save_receipt`, complete the
specific observed differences, and use the returned predecessor/reason:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py revise --run-dir RUN --packet PACKET --receipt CORRECTION_RECEIPT --predecessor RETURNED_SHA256 --reason "RETURNED_REASON"
```

This appends a validated correction. Preserve the old accepted receipt and packet.
Repeated case/whitespace-normalized change explanations are rejected on submission
and excluded as reuse proof, including already saved receipts. Do not evade this
by adding counters/IDs to boilerplate. Code cannot establish semantic truth from
unique prose; each reason must explain an actual observed before/after difference.
Independent valid source/component proofs can still skip a page; a deficient
receipt is not itself such a proof. Do not restart acquisition to repair a review.
After a pause/compaction, start with `review_step.py next`, not an old scratch
classifier or receipt generator. Follow returned paths; do not guess JSON keys or
filenames. Record the session's actual model when exposed, not `codex-agent`.

Do not author automatic no-change receipts from substring/hostname tests or
blanket URL-case/host substitutions. The hash gate owns approved reuse. A returned
source packet needs bounded interpretation; read `field_changes` in its decoded
comparison for JavaScript/embedded-data differences instead of rewriting parsers
or repeatedly dumping entire originals. Original change IDs and evidence remain
authoritative. Report a specific unsupported comparison rather than inventing a
harmless-change conclusion.

For a newly changed shared component, explain the actual before/after changes,
including script logic outside rotating tokens. A Cloudflare label does not prove
that only challenge IDs changed. A URL case change does not prove equivalent
routing; state the observed link change and the bounded content-review conclusion,
without claiming the targets were verified unless they were. Do not infer that
an `og:updated_time` value is a retrieval time or a substantive edit date. Treat
unexplained component changes as unresolved rather than approving shared reuse.

When an officeholder changes, keep the predecessor and successor as distinct
people. Create or reuse the successor's own stable person key and reconcile the
office roster reference with that key in the supported findings. Do not put a
successor's name under a predecessor's person ID. A spelling correction to the
same person is different; preserve source discrepancies without inventing an
identity change. Final roster/person reconciliation remains required.

Preserve date meanings exactly: selection/appointment, publication, revision,
retrieval and effective dates are separate. Do not call a stated selection date
an effective date without explicit evidence. Describe observed metadata values
without inventing their cause or a per-session rotation schedule.

If the queue identifies an omitted prior source, follow SOURCE_HASH_REVIEW.md's
bounded supplemental acquisition sequence. The coordinator records
`reviewed_supplement` automatically only with current exact-source evidence and a
completed matching source review or official opinion-monitor signature. Do not
author another model review for that reuse or mislabel an in-scope reviewed source
as unavailable/excluded. Genuine failed acquisitions and changed evidence remain
pending. Save relevant additions in the ongoing registry for subsequent runs.
Opinion discovery/status, changed PDFs and effective-date triggers remain independent.

For a returned task whose original bytes change but extracted text is identical, read
`inputs.raw_comparison_path` and inspect the originals as needed. Complete the
required `raw_change_review`: preserve its comparison hash/change IDs, state your
inspection method and explain each change specifically. HTML comparisons include
attributes and embedded JSON; binary comparisons only identify changed spans and
require an appropriate original-document review. Do not infer harmless metadata
or CSS/JS changes from an empty text diff. Do not publish private comparison data
or embedded tokens as report content. Unresolved original-content changes stay
unfinished.

`workflow acquire` invokes the standard seven-court update and registered-source
hash gate under the same database acquisition lock. Wait on its actual tool session;
no stdout while it runs is normal. After completion proceed to `next-task`.
`status` and `next-task` refresh saved queues without fetching sources again.
After interruption resume the same generated acquire command once the process has
exited; do not create a competing run or use source-gate as a replacement.

Do not stop after launch, acquisition, screening or a build. Follow `prepare-report`,
`refresh-directory`, `workflow build`, roster review and separate publication
acceptance as returned by the coordinator. Missing extraction/evidence is unfinished;
source failures remain qualified gaps. Do not invent review attestations, IDs or
citations to clear validation. For a completed interpretation needing correction,
use the runbook's source/opinion correction path; never edit accepted artifacts.

Preview completion returns `preview_complete` only after actual editorial acceptance;
report that nothing was finalized or deployed. Publish mode returns the exact
finalize command, then `workflow export`, `workflow integrate`, and `workflow release-plan`. Follow
its file paths and destination-hash checks and repository WEB_PUBLICATION.md for
reviewed-file integration, credential scan, authorized Git/PR/Pages release and
live verification. `publication_handoff` is not live publication. Keep the persistent
goal active until deployment is verified; do not treat the coordinator handoff as
the whole update. Do not audit historical reports.

Record dates, actual selected model when known, reviewed/reused/pending counts,
database capture IDs, limitations, new files, tests and deployment evidence in
RESUME.md and the final response. Keep saved findings, local site builds and live
publication distinct. A blocked deployment does not justify repeating research or
advancing another baseline. Use the persistent goal's blocked rules if necessary.

## Installation and recovery

Install/update this repository's skill with `python3 scripts/install_florida_update_skill.py
--checkout CHECKOUT --python /Users/cadespivey/Developer/FloridaLitigator/florida-litigator-weekly-update/.venv/bin/python`.
The installed `installation.json` binds an explicit checkout and interpreter.
No development worktree is assumed. `--checkout` still overrides that binding.
Use a maintained current checkout; preserve the dirty historical research checkout.
For receipt corrections or damaged generated files, read the correction/recovery
sections of `docs/workflow/DETERMINISTIC_COORDINATOR.md`; use `workflow revise`,
`workflow repair`, or `workflow build --repair` rather than deleting a run.
If a checkout moved during source/opinion review, follow that runbook's
`workflow relocate --run-dir MOVED_RUN --reason EXPLANATION` recovery path from
the new checkout. Preserve the original contract and domain reviews. Do not edit
pinned paths in place, recreate retired links, initialize another run or refetch.
After relocation, use the newly returned task; an old packet/command may bind the
retired location. Downstream-stage relocation is intentionally refused.
