# Coordinator operational gap closure

Authorized objective: address the six gaps supplied October 26, 2026, through
narrow patches or explicit process improvements. Existing evidence, accepted
history, unrelated edits and historical reports remain untouched. No package
installation or inference-server restart is part of this work.

## Sequence and acceptance criteria

1. Correction: add explicit append-only supersession of mapping/directory
   decisions, with predecessor checks, domain validation and downstream
   invalidation. Reject stale corrections and preserve every earlier receipt.
   Finalized output must require a new publication rather than rewriting history.
2. Recovery: regenerate damaged projections from authoritative inputs into new
   attempt paths. Preserve damaged files. Verify exact bytes before retaining
   acceptance. Cover report, directory, review-site and release projections.
3. Publication: persist integration, Git/release and deployment checkpoints;
   protect concurrent destination edits, make retry safe, and require observed
   deployment evidence before completion. Reuse existing release tooling.
4. Mapping reuse: reuse only validated decisions with identical source/review
   identity and compatible reporting scope. Date-dependent relevance decisions
   must not be carried into another reporting window blindly.
5. Local trial: run a production-sized isolated preview with the selected local
   model, retaining logs, task counts, context usage where observable, failures
   and correction burden. Do not substitute synthetic unit tests for this trial.
6. Installation: integrate the reviewed implementation and make the installed
   skill resolve a durable verified checkout; test launch from outside the repo.

For each patch inspect the diff and run targeted behavioral tests. Final checks
cover current/future behavior, credential scanning and actual installation/release
state; no historical-report audit. Record limitations honestly.

## Current checkpoint

Correction, projection recovery, guarded integration/release tracking, compatible
mapping reuse and explicit maintained-checkout installation are implemented.
The full suite passed 791 tests at `19b7d2a`, including append-only source
corrections, interrupted domain/coordinator reconciliation and decoded original-content
comparisons, alongside finalized-correction, recovery and mapping-reuse coverage.
PR #109 is still open;
merge, final installation refresh and actual release verification remain pending.
The separate maintained checkout and installed skill were refreshed to candidate
`168facd`; installer validation and launcher preflight from `/tmp` passed, with
all workflow imports resolving inside `/Users/cadespivey/flwu-current/src`.
This does not establish merge to main; repeat against merged main at completion.
The production-sized local trial has saved acquisition but incomplete review.
Several continuations required supervisor intervention for unsupported explanations
and attempted path-based no-change classifiers. The same saved run now continues
through fresh, single-task local assignments; the parent reviews each saved result
before requesting the next task. Thirty-seven source reviews are independently
verified at this checkpoint. This is supervised evaluation, not an unattended pass.
Its observed failures and operator interventions are recorded in
[the interim trial report](COORDINATOR_LOCAL_TRIAL_20261026.md). Neither acquisition
completion nor passing tests prove end-to-end model reliability.

## Chronological implementation log

The entries below record earlier checkpoints; statements that work was pending
describe that checkpoint and are superseded by later entries and the current
checkpoint above.

- Review-site recovery implemented as `workflow build --repair --run-dir RUN`.
  New attempt paths preserve damaged output; regenerated file hashes must equal
  the recorded build. Unexpected extra files now fail integrity checks too.
- Remaining projection recovery and items 1, 3–6 are still pending.
- Explicit `workflow decision` / `workflow revise` now supports append-only
  corrections with exact predecessor and evidence validation. Mapping changes
  rebuild report identity; directory changes invalidate projections and require
  approval of the new build. Finalized runs reject in-place corrections.
- Generated report/template/preview, directory/audit and release-bundle bytes now
  persist in the database. `workflow repair` restores missing or corrupt saved
  projections atomically and preserves damaged bytes. Existing events lacking
  stored projections remain an explicit compatibility limitation. Targeted
  tests verify exact restoration, no new reviews/acquisition, and retry safety.
- Mapping reuse now reads decisions contributing to the pinned finalized baseline,
  checks exact source/review inputs, and records the reuse policy and predecessor.
  Supported cases: identical period, unchanged directory findings, and previously
  published unchanged opinions outside the new period. Changed-period editorial
  exclusions and removals remain explicit review tasks. Tests cover compatible
  periods, older published opinions and an incompatible expanded period.
- Publication integration now journals intent and exact before/after hashes;
  retries preserve concurrent edits. `verify-deployment` records remote PR state
  and requires the exact merged commit, successful Pages deploy job, and exact
  live current issue/directory data before completion. Tests use mocked GitHub
  and live responses; no actual release/deployment is claimed. Git operation
  automation/recovery remains pending.

- Git release recovery now uses `workflow release-plan`: saved branch/base commit,
  explicit file list and scoped commands, followed by observed remote PR state.
  Git mutations/merge remain explicit under existing authorization rather than
  being automatically executed by status. This is the process-improvement route
  for release recovery, with actual deployment checks in code.
- Installer preflight passed from outside the repo. The launcher now uses explicit
  installation.json and no hard-coded development checkout fallback. Actual
  maintained-checkout installation and branch integration are still pending.
- Production-sized Qwen3.8-27B-8bit preview started against a consistent 39 GB
  database copy, 769-source registry and all current supplements. Private evidence
  lives in runs/local-model-validation-20261026; worker session 98994. No production
  writes, code edits, finalization or publication authorized in that trial.

- Legacy report/directory stage regeneration is now supported with explicit
  --repair flags, preserved prior stage folders, and report hash equality checks.
  Regression tests also cover publication with real directory changes: integration
  now retains its pinned before-state so installing new public supplements does
  not incorrectly invalidate the run's own projection on resume.
- Local trial setup exposed incorrect registry-list assumptions, a guessed
  supplement path, unsupported worker goal tools and an incorrectly inferred cloud
  model identity. Skill guidance now gives exact registry keys/paths and explains
  parent-goal ownership for explicitly delegated trials. Raw worker evidence is
  preserved for the final report card; these are not claimed resolved in the run.

- Installed the skill against dedicated maintained checkout
  `/Users/cadespivey/flwu-current` at candidate commit `4a27a6a`. Installer and
  installed launcher preflights passed with the existing venv; no package install
  occurred. The trial remains pinned to the separate implementation checkout.
  Advance the maintained checkout to merged main after trial review and refresh
  the installed skill again. PR #109 remains draft pending that review.
- Production-sized queue export exposed a full latest-finding scan per source.
  Queue generation now builds the same URL-indexed latest-version map once, and
  identical extracted text skips unnecessary sequence matching. Raw-byte gates
  and required source reviews are unchanged. Tests assert one lookup scan for
  multiple sources, latest-version/citation behavior and exact-text fast paths.
  The already-running acquisition was not interrupted or restarted; subsequent
  commands use the patch.
