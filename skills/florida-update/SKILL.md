---
name: florida-update
description: Run The Florida Litigator research update, analyze hash-generated review tasks, persist evidence and findings, and update reviewed website reports and personnel data. Use for a Florida Litigator weekly update or database/website refresh.
---

# Florida Litigator update

Invocations: `$florida-update`, `$florida-update through YYYY-MM-DD`, or
`$florida-update since YYYY-MM-DD through YYYY-MM-DD`. A request for a preview or
no publication restricts the final phase accordingly.

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

> Complete the requested Florida Litigator update using the last finalized report
> as baseline unless an explicit start is supplied, and the resolved reporting
> cutoff. Run seven-court opinion discovery and registered-source hash acquisition;
> process all required review tasks and persist validated findings with evidence
> readback; prepare and validate the report and affected current directories;
> publish the authorized website data and verify successful deployment and live
> content. Preserve historical reports and record coverage failures honestly.
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
The root `/Users/cadespivey/florida-litigator-weekly-update` is an older dirty
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
- `docs/workflow/DETERMINISTIC_COORDINATOR.md`
- `docs/workflow/SOURCE_HASH_REVIEW.md`
- `docs/workflow/OPINION_DISCOVERY.md`

## Establish a durable run

1. Resolve dates in America/New_York. Default end is the most recent completed
   Sunday; on Sunday use the previous Sunday unless the user requests a partial
   current-day run. Explicit dates override this. Default start is the last
   finalized report for the chosen stream, not the latest research attempt.
2. Use `flwu history streams --database DB` and the current finalized report's
   capture/contract to identify the live weekly stream. Do not choose a trial,
   synthetic, county-only or acquisition stream. If multiple plausible weekly
   streams exist, ask for that choice before writing. No finalized baseline
   requires an explicit start; never invent one. If no new reporting interval
   exists, report that rather than issuing a duplicate weekly report.
3. Reuse a reviewed registry if present. Otherwise run `flwu source-gate inventory
   --database DB --stream STREAM --output RUN/registry-candidates.json`; review its
   scope against the county source index and current public directory supplements.
   Inventory from one weekly stream does not automatically include all county
   baseline streams. Include their supported current profile/procedure/contact
   sources and relevant statewide statutes/rules. Save the reviewed ongoing
   registry at `runs/updates/registry.json`; record additions and known gaps.
   Do not certify statewide coverage from an unreviewed URL list.
4. Use `runs/updates/<unique-run-id>/` for private evidence, receipts and progress.
   Write `RESUME.md` with checkout, DB, exact stream, registry, dates, run ID,
   next task, completed receipts, coverage gaps, persistent goal objective/status
   and publication status. Back up
   the live database with SQLite's backup API before the first write; do not copy
   a live SQLite file with ordinary filesystem copying.

## Follow the coordinator through completion

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

When original bytes change but extracted text is identical, read
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
--checkout CHECKOUT --python /Users/cadespivey/florida-litigator-weekly-update/.venv/bin/python`.
The installed `installation.json` binds an explicit checkout and interpreter.
No development worktree is assumed. `--checkout` still overrides that binding.
Use a maintained current checkout; preserve the dirty historical research checkout.
For receipt corrections or damaged generated files, read the correction/recovery
sections of `docs/workflow/DETERMINISTIC_COORDINATOR.md`; use `workflow revise`,
`workflow repair`, or `workflow build --repair` rather than deleting a run.
