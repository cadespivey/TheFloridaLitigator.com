# New-run setup

Use this only when no run is in progress. For an existing run, use its saved
contract and returned next state; do not repeat setup. `flwu` below always means
the installed pinned launcher, not the bare executable.

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
`/Users/cadespivey/Developer/FloridaLitigator/shared-history/research-history.sqlite`.
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

For a specific setup/scope problem, consult the relevant section of these references (not a mandatory reading list):
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
