# Polk baseline continuation

Workspace: `runs/county-polk/2026-10-19`. Read `state.json` and `RESUME.txt` first. The county stream is `manual_research:county-baseline-v1:252190e9d79c`; the database is `/Users/cadespivey/.local/share/flwu/research-history.sqlite`. Do not initialize the legacy seven-county workflow for this scope.

Start from the saved `review/roster-candidates.json` profile URL. Complete one person's contacts and short operating checklist before advancing. The official `/judges` roster has five pages; preserve repeated observations and reconcile against the separately linked circuit, county, senior, magistrate and hearing-officer lists before asserting completeness. A person absent from the initial Polk filter is not automatically outside scope.

Profiles expose assignment, assistant, email, phone, fax, mailing address and linked documents. Preserve the original HTML, normalized text, retrieval timestamp and hashes as demonstrated by `review/swenson/acquire.py`. The named general-procedure guide supplies a physical courthouse address and recurring operating instructions. Keep mailing and physical addresses distinct. Compare visible email text with PDF annotations and HTML targets; do not invent a mailto target when the page uses plain text.

Use six short categories: scheduling, courtesy materials, appearances, proposed orders, communications/cancellations, and notice/access. Read only the relevant general-office sections. Keep trial calendars, templates and specialized litigation sections as links unless needed for a concrete missing operating requirement. Retain whole downloaded originals without describing unreviewed pages as reviewed.

Prepare a source-backed receipt following `review/swenson/prepare.py`; validate with `flwu.research._person`. Save through `flwu.baseline_capture.save_checkpoint` using a new cumulative packet and the actual current capture sequence. Trial in a temporary database first, then check identical replay, artifact bytes, saved facts, and unchanged finalized reports. Do not rerun an old save script after its expected capture has advanced. Update pending/completed state only after successful readback. Check copied scripts for stale county names and next-action text.

County research acceptance, directory projection and public release are separate steps. Preserve prior county work and historical reports. The full statewide goal remains in `docs/workflow/STATEWIDE_BASELINE_GOAL.md`.

## Current audit checkpoint

The reviewed 46-person supplement is published in `website/county-directories/polk.json`.
The older 6629 acceptance record's release backlog is historical. Later publication
reconciliation is captured at9005; the live-site audit remains a separate requirement.
The October22 audit verifies46 published people, ten separate senior scope reviews
and257 nested citation hashes. Checkpoint9137 preserves the individual review of ten
absent checklists and bounded search follow-ups. Missing guides and mismatched
current-division applicability remain explicit; do not manufacture instructions.

Freeman's November2 M2 assignment/contact and Allison Kaylor's transition are dated
observations in `polk-october-assignment-observations`, not current October assignments.
Shared order findings preserve paper/electronic submission differences, the blank
signature day in3-42.2 and separate official-index date, and scoped public-access
requirements. Source conflicts do not require a controlling-authority decision.
Use the current statewide handoff for the next county; do not rerun old save scripts.
