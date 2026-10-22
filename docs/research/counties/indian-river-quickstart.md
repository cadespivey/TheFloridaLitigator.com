# Indian River County: research and update source map

This map was assembled from saved source evidence on October22,2026; it is not a
fresh-source attestation. Follow [the active goal](../../workflow/STATEWIDE_BASELINE_GOAL.md)
and [checkpoint contract](../../workflow/BASELINE_CAPTURE.md). Astra-only execution
currently applies; finish/save one person before moving to the next.

## Resume and reuse

Court: Nineteenth Circuit. Stream: `manual_research:county-baseline-v1:a1bbb956b326`. Last checked capture: **7821**.
Query the database for the latest stream capture before writing; this number is a
checkpoint reference, not a permanent latest value. Database:
`/Users/cadespivey/.local/share/flwu/research-history.sqlite`.
Run: `runs/county-indian-river/2026-10-20`. Public supplement: `website/county-directories/indian-river.json`.

Inspect the latest payload's individual findings and roster/shared review findings,
then resolve their original/extracted hashes from the artifact store. Earlier roster
candidate lists are discovery evidence, not a replacement for final reconciliation.
Never rerun a successful one-shot save script or infer current state from an old
state.json. Reuse original acquisition timestamps when reusing sources.

## Where to search and what to collect

Start with the filtered official roster:
https://www.circuit19.org/judges/?_location=indian-river-county . Reconcile every
named card and vacancy separately. Confirm role and county on each profile;
chief and circuit-wide magistrate listings need an applicability qualification.
Adrienne Fleming's civil magistrate profile is
https://www.circuit19.org/judges/magistrate-civil/; the chief profile is
https://www.circuit19.org/judges/chief-judge/ .

Individual profiles may link PDFs under /wp-content/uploads/ with dated filenames.
Read the document's own date and civil/basic operating sections. Do not infer an
effective date from the upload directory or copy St. Lucie/Martin/Okeechobee contacts
without explicit shared-office evidence. Clerk research starts with
https://indianriverclerk.com/ and its current contact/court-record pages.

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
