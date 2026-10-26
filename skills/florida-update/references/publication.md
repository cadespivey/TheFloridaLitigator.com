# Coordinator release handoff

For new weekly runs, follow repository docs/workflow/DETERMINISTIC_COORDINATOR.md and the exact workflow next-task commands. Do not create a second research workspace or write report/directory assembly scripts. The generated release handoff does not mean deployed.

## Durable integration and release

Run the emitted `workflow integrate` command, then `workflow release-plan`.
The plan records the branch, starting commit and exact file list. Inspect its
commands before running them. On recovery, check the recorded branch, Git log,
remote branch and existing PR first; reuse completed operations. Do not blindly
repeat branch/commit/PR creation. Git mutations remain explicit steps, while the
coordinator persists integration intent, release plan, remote PR observations and
deployment completion.

Run `workflow verify-deployment --run-dir RUN --pr NUMBER` after opening the PR;
repeat with `--deployment-run RUN_ID` after merge and successful deployment.
Only `publication_complete` means deployed. The verifier checks the exact remote
commit and live current issue/directory bytes. Do not mark a handoff complete.

## Build and release

- Use `flwu publish --archive website/updates --output NEW_BUILD` with every current
  `--county-directory` and `--directory-supplement` argument from
  `.github/workflows/pages.yml`; do not omit unaffected counties. This is a local
  build, not deployment. Inspect latest issue, changed directory rows, source links,
  desktop/mobile layout and keyboard navigation where browser tools are available.
- Run applicable current-data/renderer tests and the existing CI suite; do not add
  historical-production-report verification. Record actual warnings/failures.
- Inspect the diff and stage only intended public metadata/exports and any expressly
  authorized supporting changes. Never stage the database, private workspace,
  raw webpages/PDFs, prompts or logs. Run
  `python scripts/check_public_credentials.py` after staging, before every push.
- Confirm both effective Git author and committer use
  `259985078+cadespivey@users.noreply.github.com`; never print private identity or keys.
  Commit, push an ordinary branch, and open a PR with scope and real validation.
  Once required checks pass, merge the authorized release. No force pushes,
  history rewrites, credential changes or Pages configuration changes.
- Observe successful GitHub Pages deployment and check the live latest report and
  affected directory content. If deployment fails, preserve accepted findings and
  report the failure; do not rerun research or advance another baseline to fix it.
- Save final capture IDs, exported file paths, PR/deployment URLs, and completion
  status in RESUME.md. Do not call pending publication deployed.
