> Execution policy: [use the invoking model](../../workflow/MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Bay County: research and update source map

This map was assembled from saved source evidence on October22,2026; it is not a
fresh-source attestation. Follow [the active goal](../../workflow/STATEWIDE_BASELINE_GOAL.md)
and [checkpoint contract](../../workflow/BASELINE_CAPTURE.md). Astra-only execution
currently applies; finish/save one person before moving to the next.

## Resume and reuse

Court: Fourteenth Circuit. Stream: `manual_research:county-baseline-v1:2a610b4105b7`. Last checked capture: **7771**.
Query the database for the latest stream capture before writing; this number is a
checkpoint reference, not a permanent latest value. Database:
`/Users/cadespivey/.local/share/flwu/research-history.sqlite`.
Run: `runs/county-bay/2026-10-20`. Public supplement: `website/county-directories/bay.json`.

Inspect the latest payload's individual findings and roster/shared review findings,
then resolve their original/extracted hashes from the artifact store. Earlier roster
candidate lists are discovery evidence, not a replacement for final reconciliation.
Never rerun a successful one-shot save script or infer current state from an old
state.json. Reuse original acquisition timestamps when reusing sources.

## Where to search and what to collect

Start with https://jud14.flcourts.org/judges and the county labels in that roster.
Check https://jud14.flcourts.org/magistrates-hearing-officers separately; judges-only
roster extraction omits officers. Preserve each officer's listed county coverage.
Shannon Lord is explicitly listed for Bay, Gulf, Holmes and Washington; do not
infer every circuit officer serves every county. Chief, outer-county administrator,
senior and specialized roles require explicit applicability, not a generic circuit
membership assumption.

Open each linked individual judge profile and only its applicable civil/basic
operating guide. PDF filenames are not revision dates. Some profiles have no guide;
record bounded gaps instead of substituting another judge's procedures. Clerk
Bill Kinsaul's profile is https://www.baycoclerk.com/about-us/. Use the clerk's own
civil/contact pages for office routing; preserve different judicial/clerk contacts.

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
