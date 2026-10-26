# Coordinator implementation and isolated trial — October 25, 2026

## Scope and result

Implemented the approved deterministic coordinator: saved-state next-task/status,
report assembly and reconciliation, directory projection with per-person review,
explicit source limitations, separate editorial acceptance, and a local release
handoff using existing publication gates. The invoking model remains responsible
for relevance, supported interpretation and editorial acceptance. No new research,
production database writes, historical-report audit or live publication occurred.

The maintained skill source is now included in `skills/florida-update`. Its launcher
verifies update, workflow, prepare-report and refresh-directory in the selected
checkout. Generated commands use that checkout's absolute module path/interpreter.
The normal preview was conducted through supported CLI commands and individual
model-authored JSON receipts. No ad hoc assembly script or manual database edit
was used. Subsequent scenarios exercise acquisition/reuse/failure boundaries rather
than pretending each negative case is a completed publishable report.

## Actual CLI trial

Private root: `/Users/cadespivey/flwu-orchestration-trial-20261025`.
Database: `trial.sqlite`; input responses are explicitly synthetic, with no network
fallback. Scenarios are initialized with `workflow trial-init` and run with the
coordinator's actual acquire/submit/prepare/refresh/build/status commands.

- **Normal:** all seven courts' active/inactive listing scans ran. Twelve notice
  sources and two opinion interpretations were reviewed; two separate stable
  opinion identities were mapped. `prepare-report`, `refresh-directory` and
  `workflow build` completed. This fixture has no personnel changes; the separate
  directory integration test exercises actual contact/alias projection.
- **Missing acceptance:** `history finalize` rejected the prepared report with
  “Separate publication acceptance is required before finalization/export.”
- **Editorial acceptance:** actual invoking-model review of the fixture evidence,
  report and rendered site was recorded separately. Status became
  `preview_complete`, `complete:true`, `publication_performed:false`.
- **Unchanged:** twelve source reviews and both opinion reviews were reused;
  source/opinion review task counts were zero. Publication mapping remained an
  explicit editorial stage for the requested period.
- **Source failure:** the Second DCA fixture returned 403. Acquisition remained
  incomplete and next-task emitted a specific coverage-review packet.
- **Duplicates:** a repeated listing page was not accepted as complete discovery.
  Acquisition remained incomplete; no new duplicate opinion review was created.
- **Interrupted:** acquisition exited once after a saved page. Status returned the
  same acquire command. Resume succeeded and the first active First DCA page was
  requested exactly once across both attempts.
- **Baseline safety:** readback with the project's Python interpreter confirmed
  zero finalized reports in the trial database after these exercises.

Normal report capture:
`8471e31ac82d72a58b8212b4e976785410f9d2db6132b1aaa18f4accdb160f50`.
Acceptance coordinator capture:
`91e996c5855aa76a007a15dfffb824b7a5ec4f6941a791ef5cb375be6ad97be3`.
Report SHA-256:
`c6d1adc808770eb55741c5ef47caa71a7437286407eba2dcdbb0c6f563c5835c`.

## Visual checks and environment limitations

Existing cached Chromium rendered the standalone report and website at desktop
and 390-pixel mobile width. Screenshots are in the trial's `output/playwright/`.
Case-law fields/source links were present and controls/text wrapped within the
viewport. This is a targeted rendering check, not a new accessibility certification.
The standalone report requested an absent favicon (404); its content and the
website's own favicon/assets loaded. The trial server and browser were closed.

The in-app browser was unavailable. The Playwright default Chrome path was absent;
using the already installed Chromium executable succeeded, without installation.
The skill creator's Python validator could not import PyYAML in either available
Python. Ruby's existing YAML parser validated its two frontmatter fields, references
were inspected and the launcher preflight succeeded. No package was installed.
System Python's SQLite could not open the WAL database read-only; the project's
Python read it successfully. All workflow commands use the project interpreter.

## Boundaries

The trial validates orchestration and integrity, not real-world legal accuracy or
unattended local-model performance. Existing county-specific assignments remain
preserved; a substantive reassignment requires an explicit cited per-scope assignment update.
New county coverage is outside this change. Publish mode produces a reviewed
release bundle and exact file handoff; GitHub Pages release and live verification
remain explicit existing steps. `publication_handoff` is never reported as complete
or deployed. Existing historical reports and the original dirty research checkout
remain untouched.

## Regression evidence

Full repository suite: **756 passed in 11.57 seconds**, with no warnings reported
by pytest. A final receipt-replay guard was then added; the final focused
coordinator suite passed **16 tests in 4.45 seconds**. Meaningful additional cases include changed preview/build
rejection, the existing database acquisition lock, actual publish-mode transition
through finalization/export to a nondeployed handoff, explicit directory removal,
and per-scope cited reassignment while preserving other people and fields.
