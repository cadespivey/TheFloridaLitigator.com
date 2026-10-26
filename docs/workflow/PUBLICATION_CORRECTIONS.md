# Evidence-preserving publication corrections

This supplement to SOURCE_HASH_REVIEW.md separates source review from editorial
acceptance. Use the invoking model; do not launch a local worker or repeat saved
acquisition merely because the session resumed. Preserve all prior captures.

## Editorial corrections to an already reviewed opinion

Use the pinned launcher:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py opinion-revise --database /absolute/history.sqlite --registry /absolute/expanded-registry.json --receipt /absolute/revision.json
```

Save the receipt in the run's `correction-review/editorial-revisions/` directory.
Start with the latest saved `opinion_review` for the exact opinion ID. Copy these
fields: `id`, `signature`, `reviewer`, `relevance`, `summary`, `holding`,
`disposition`, `authors`, `citations`. Add exactly:

- `predecessor_version`: the previous `receipt_sha256`.
- `reason`: why the reader-facing content needs correction.
- `review_protocol`: the registry protocol.
- `pdf_sha256` and `state_sha256`: the previous review's source bindings.

Update reviewer and the reader-facing content. Retain exact source quotations,
raw/text hashes and locators; each author name must occur in an opinion quotation.
Do not infer facts from authorities cited by a citation opinion. Do not change
relevance through this command. New bytes, changed status, unavailable sources,
or changed protocols require ordinary queued opinion review instead.

Save the returned capture ID/sequence. Read the new capture back and verify its
summary and predecessor. Regenerate report requirement versions after revisions;
old disposition versions are deliberately stale. The predecessor remains stored.
A revision is not report acceptance or publication.

## A required source genuinely cannot supply evidence

Use receipt status `reviewed_source_limitation` only for a source task with an
exact saved retrieval failure or demonstrably invalid HTTP200 body. It cannot
excuse a roster/person gap, available unread content, unfinished repair, or missing
extraction. Do not substitute another URL, even on the same hostname.

Set `pages_complete: false`, `reviewed_pages_complete: true`, actual `checked_at`,
`errors: []`, and the separately reviewed `pages`, `candidates`, and `entities`.
Where alternative pages exist, their pagination evidence must cover that reviewed
subset. Each included claim and person retains the normal evidence checks.
A clerk task still requires an identified clerk and its person receipt.

Add `source_limitation` with exactly these fields:

```json
{
  "task_id": "exact-contract-task-ID",
  "url": "exact-required-URL",
  "observation_capture_id": "saved-acquisition-capture-ID",
  "sha256": "saved-original-hash-or-null",
  "text_sha256": "saved-extraction-hash-or-null",
  "retrieved_at": "saved-acquisition-time",
  "http_status": 403,
  "category": "retrieval_failed",
  "reviewer": "actual reviewer",
  "reason": "Specific source failure and its effect on coverage.",
  "reviewed_scope": "Precisely what was reviewed and what remains unavailable.",
  "pending_work": [],
  "invalid_content_quote": null,
  "alternatives": []
}
```

Copy actual values from the saved observation; null is JSON null, not a string.
For `invalid_content`, preserve HTTP200 and quote the full saved extracted body
showing the domain-sale/login/access-denied response. Ordinary official text or a
navigation login link does not establish invalid content. Alternative evidence
must have its own exact URL, raw/text hashes, retrieval time, HTTP status, quote
and locator. Never rewrite the failed observation as a successful alternative.

Run `research status --run-dir /absolute/run --history-db /absolute/history.sqlite`
using the pinned launcher. Check the result: a limitation is counted separately
from `evidence_valid`, remains a nonverified history check, and cannot produce
`no_observed_change`. Keep unresolved work pending rather than emptying
`pending_work` to pass validation.

## Final acceptance and export

Generate a fresh `history review-template` only after actual report integration.
The template includes `source_limitations` when applicable. Independently review
each limitation and explicitly set `acknowledged: true` with a concrete rationale;
preserve its exact task ID and digest. Omissions, stale digests, duplicates and
unchecked acknowledgments fail acceptance. A ready-for-review capture is not a
finalized report. Use the existing separate accept/finalize/export sequence.

Public issue provenance retains source-limitation metadata without local paths.
There is no Evidence Coverage UI section. Failed sources remain failures in the
database; finalizing a reviewed report does not retroactively turn them into
successful source checks.

## Opinion listing evidence

`AcquisitionIndex` binds original saved JSON pages, including empty feeds, using
the original bytes as the UTF-8 text representation. No extraction observation is
invented. `discovery_evidence.validate_channel` rechecks the saved run contract,
exact acquisition IDs, URLs, hashes, filter parameters, stable totals, offsets,
and duplicate identities before supporting complete-channel claims. Validating
one page alone does not establish complete discovery coverage.

## Senior judges without a documented current county assignment

A current circuit senior-judge list may establish a named person's senior status
without establishing a current county assignment. Keep `counties: []`; do not
reuse a historical county judgeship as a present assignment. Use
`assignment_scope: "circuit_senior_roster"` and
`assignment_note: "Current county assignment not established by this circuit senior roster."`
only with role `Senior judge` and an exact named source quotation stating current
senior service. These entries remain in the circuit inventory and require their
own person/contact receipts. Active trial judges still require evidenced county
assignments; this exception does not excuse an unsupported identity.

Public exports keep source-limited sections marked `incomplete`, with the affected
section keys in each limitation's machine-readable provenance. Supported items
remain visible. A limitation cannot be removed while retaining an otherwise
unpublishable incomplete section, nor can the affected section be relabeled
fully reviewed. This uses the existing section-status presentation, not an
Evidence Coverage section.

### Linked-source failures

A task's successful landing page and its failed dependency are distinct acquisitions.
For a failure reached through that page, the ordinary limitation may additionally
contain `discovery_path`, an ordered list of at most eight hops. Each hop requires
`url`, `observation_capture_id`, `sha256`, `text_sha256`, `retrieved_at`, `http_status`,
`reference`, and `target_url`. Copy metadata from the saved successful observation.
`reference` must occur as a complete quoted string in the original bytes; resolving
it against that hop's URL must produce exactly `target_url`. The first hop must
start at the immutable task URL, each following hop starts at the previous target,
and the final target must equal the limitation's actual failed URL. Cycles, missing
captures, other streams, newer-than-report captures and invented references fail.
This path does not excuse missing extraction or available unread content.

Keep the failed endpoint's own URL/hash/time/status in the limitation. Never give
it the homepage's successful HTTP status, and never label the homepage as failed.
Save the receipt in the existing `report-projection/receipts/<task-id>.json` and
run `research status` through the pinned skill launcher. Capture, explicit
acceptance and public provenance retain the dependency observations; affected
sections remain incomplete. An acknowledgment of the exact limitation digest is
still required before finalization. Do not put original captured pages into Git.

Unregistered supplemental URLs remain explicit pending tasks in the standard
queue. For an `unavailable` disposition, publication validation now checks that
URL's latest saved acquisition in the report stream, bounded by the report
capture sequence. It must have `success: false`, and any saved artifacts must
still match their hashes. An absent observation, another stream, or a later
successful response does not excuse unread content. Successful supplemental
sources require acquired quoted support and their existing review/finding
reconciliation; exclude only duplicate generic registry work, not substantive
findings. The report capture pins this determination without rewriting the queue.
# Current directory and opinion projection

For each person receipt, select `public_links.profile` from that person's exact
named identity citation. Select `public_links.procedure` only from an actually
verified procedure citation. Each selection is the full saved citation object,
including original/extraction hashes, acquisition metadata, paths and quotation.
The capture validates these references; the public export emits only the selected
URL after matching its URL and quotation to that person's exported citations.
Omit an unavailable link. Do not guess a biography URL from a name or treat a
missing individual procedure as verified. A profile link may lead to the named
official roster where that is the supported identity source.

Structured case-law `holding`, `disposition` and `authors` fields must survive
the public export. They become labeled lines in the existing summary format;
conflicting embedded and structured labels fail export. Check the actual website,
not only the standalone review report, for all three labels and source links.

Current county supplements override the weekly directory. Reconcile affected
records before release so old supplement contacts cannot overwrite new findings.
Reuse stable IDs or explicitly reviewed county-scoped legacy mappings; a shared
profile URL alone is not permission to merge different county records. Preserve
unaffected people and their source observations. Preserve source discrepancies in
research evidence; public contact labels describe the contact's purpose, not the
document from which it was collected.

Presentation selections under `directory-format.json` → `person_fields` require
the exact person ID, field name and unchanged source value. Changed values fall
back to unmodified source text until reviewed. Check phone/email preservation,
address line breaks, county membership and actual desktop/mobile rendering.
Retain the private before/after field audit and explicit supplement review; do not
claim that a structural validation alone is substantive review or publication.
