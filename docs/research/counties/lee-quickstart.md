> Execution policy: [use the invoking model](../../workflow/MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Lee County: research and update source map

This map was assembled from saved source evidence on October22,2026; it is not a
fresh-source attestation. Follow [the active goal](../../workflow/STATEWIDE_BASELINE_GOAL.md)
and [checkpoint contract](../../workflow/BASELINE_CAPTURE.md). Astra-only execution
currently applies; finish/save one person before moving to the next.

## Resume and reuse

Court: Twentieth Circuit. Stream: `manual_research:county-baseline-v1:d007563d9b1b`. Last checked capture: **8983**.
Query the database for the latest stream capture before writing; this number is a
checkpoint reference, not a permanent latest value. Database:
`/Users/cadespivey/.local/share/flwu/research-history.sqlite`.
Run: `/Users/cadespivey/florida-litigator-weekly-update/runs/county-lee/2026-10-19`. Public supplement: `website/county-directories/lee.json`.

Inspect the latest payload's individual findings and roster/shared review findings,
then resolve their original/extracted hashes from the artifact store. Earlier roster
candidate lists are discovery evidence, not a replacement for final reconciliation.
Never rerun a successful one-shot save script or infer current state from an old
state.json. Reuse original acquisition timestamps when reusing sources.

## Where to search and what to collect

Start with https://www.ca.cjis20.org/About-The-Court/judiciary.aspx . Inspect all
Lee-tagged cards, including the separate `judge`, `Magistrate` and `HO` classes;
judges-only selectors omit required officers. Profile URLs use jud_profile.aspx
with a judge parameter. Read the profile and applicable linked guide together.
Shared and senior cards may list multiple counties; retain county-specific offices
and actual assignment qualifications. Do not infer current assignment from general
senior eligibility alone.

The existing final reconciliation is saved as `lee-final-roster-reconciliation`;
its source file is review/roster-reconciliation.json in the run below. Reuse the
saved shared civil case-management, professionalism and ADR/remote findings before
fetching their originals again. Clerk research starts with https://www.leeclerk.org/;
use separately labeled clerk/case-management channels rather than personal chambers
contacts. Keep individual guide requirements distinct from shared circuit practice.

For an actually missing field, search the official profile, linked guide and court
contact pages first, then a targeted query such as `site:OFFICIAL_DOMAIN "Full Name"
"judicial assistant"` or `site:OFFICIAL_DOMAIN "Full Name" procedures`. Save the
actual query, result and inspected URLs; an example query is not an executed search.
Do not guess email patterns, inherit a predecessor's contact, or treat a search
snippet as the original. Stop after a documented bounded gap; conflicts do not
require deciding which source controls.

## Save and publish

Save raw and extracted bytes with URL, timestamp, hashes and stated dates. Record
contacts, assistant, assignment, individual procedure link and concise practical
checklist; distinguish collected versus reviewed content. Noncivil assignments need
only basic operating instructions. Preserve source differences and unavailable fields.
Follow the existing packet contract and read back each saved finding/artifact;
verify identical replay and unchanged finalized reports before the next person.

Generate/review the current supplement against the pinned observations. Keep
phone/email separate, addresses in lines, and shared contacts clearly labeled.
Validate source associations, roster omissions, responsive rendering, date-selected
historical isolation and live publication. Do not change a finalized report to update
contacts. Stage metadata only; raw captures remain in the private evidence store.
