# Supreme Court and DCA opinion discovery

This is part of the [standard hash-driven update](SOURCE_HASH_REVIEW.md), not an
optional helper. `flwu update` always invokes all seven courts before the ordinary
source gate. Do not run only a hash check of previously saved opinion PDFs and
claim new-opinion discovery.

## Official source map

The executable configuration is `src/flwu/data/opinion_sources.json`. Each court
uses its own scope and siteaccess in the official search service exposed by its
opinion page. The service is `https://flcourts-media.flcourts.gov/_search/opinions/`.
All opinion types are collected for screening; the collector does not guess civil
relevance from case names or omit PCAs before the model screens them.

| Court | Official listing | Siteaccess | Search scope |
| --- | --- | --- | --- |
| Supreme Court | https://supremecourt.flcourts.gov/Opinions | `supreme2` | `supreme_court` |
| First DCA | https://1dca.flcourts.gov/Opinions | `1dca` | `first_district_court_of_appeal` |
| Second DCA | https://2dca.flcourts.gov/Opinions | `2dca` | `second_district_court_of_appeal` |
| Third DCA | https://3dca.flcourts.gov/Opinions | `3dca` | `third_district_court_of_appeal` |
| Fourth DCA | https://4dca.flcourts.gov/Opinions | `4dca` | `fourth_district_court_of_appeal` |
| Fifth DCA | https://5dca.flcourts.gov/Opinions | `5dca` | `fifth_district_court_of_appeal` |
| Sixth DCA | https://6dca.flcourts.gov/Opinions | `6dca` | `sixth_district_court_of_appeal` |

The command also registers each court's linked Most Recent Written Opinions and
PCA/release pages (Supreme: Most Recent Opinions; Third: Most Recent Opinion
Release), as enumerated in the executable configuration. Those notice pages are
retrieved and hashed independently. Their changed content creates ordinary source
review tasks, including potential notices outside the structured opinion fields.

The search API was identified from the official site's own frontend implementation,
then exercised against its responses. Preserve raw API responses and inspect the
actual parser failure if its contract changes; do not fabricate a compatible
response or fall back to interpreting an empty HTML shell as an empty listing.

## Discovery contract

For each court, query the ordinary feed and `nonactive_only=1` channel separately.
Requests include `siteaccess`, `scopes[]`, `startdate`, exclusive next-day `enddate`,
`limit`, `offset`, `searchtype=opinions`, and date-descending sorting. Verify echoed
court/scope, bounds, offset and inactive filter. `totalCount` must be a nonnegative
integer and every item an opinion with a CMS content ID and publication date.

Advance offset by **actual returned count**, since a server can cap page size.
Stop only when the accumulated count reaches the declared total. A changed total,
duplicate identity, premature empty page, schema mismatch or page-budget limit is
incomplete coverage. Deduplicate candidates by `document_id(court, content:<CMS ID>)`;
case numbers and titles alone are not unique opinion identities. A corrected
opinion and a correction notice can be separate CMS objects for the same case.
Keep both; do not collapse one merely because the case number matches.

Default discovery start is the report baseline minus 30 days; `--overlap-days`
accepts 1–366. Include discovered entries through the requested reporting end.
First observed entries within the overlap remain candidates even if their stated
publication date predates the report start. Preserve both dates and have the
reviewer explain late discovery; do not backdate acquisition or label it new law.

The database also tracks previously discovered opinions. Every run revisits their
official detail pages regardless of age, compares exact official note/disposition/
date/type metadata, and retrieves their current PDF independently. A changed
metadata hash creates a review task even when the PDF hash is identical. Changed
PDF bytes create a task even when metadata is identical. No disappearance is
inferred to mean withdrawal. Preserve the source's exact withdrawal, correction,
substitution or supersession wording for review rather than selecting controlling
authority by keyword.

Older saved official `/content/download/<id>/opinion/…pdf` URLs from the registry
or stream citations are bootstrapped through scoped case-number searches. The
exact CMS ID must match before a court is assigned. Failed identity resolution is
a recorded coverage gap. Existing documents in unsupported URL formats require
explicit source registration/identity work; do not assert they were monitored.

## Execute and locate output

```sh
flwu update --database /absolute/path/research-history.sqlite \
  --registry runs/updates/registry.json --run-id weekly-2026-10-25 \
  --output runs/updates/weekly-2026-10-25 --end 2026-10-25
```

Use `--start` only for an explicit baseline or a stream without finalized reports.
The stream's last finalized report governs by default; incomplete acquisition or
review never changes that marker. Defaults are 50 items/page and 200 pages/channel.
Increase the documented limits for a catch-up run when needed; budget exhaustion
never becomes success. Use a new run ID if changing dates, registry or limits.

`update-queue.json` contains fourteen court/channel coverage records, detail and
legacy-identity failures, source tasks, opinion tasks and effective-date tasks.
Each opinion task supplies:

- Stable `opinion.id`, court, case number, stated publication date and title.
- Exact official metadata, metadata SHA-256 and preserved status-source binding.
- Current original/extracted opinion paths, prior opinion where available, status
  originals/metadata/diff, and the prior completed interpretation.
- Code-generated reasons: new/unreviewed, changed PDF, changed official metadata,
  unavailable original, or unfinished/protocol-changed review.
- A generated `review_template` with an immutable candidate `signature`.

Source originals live in SQLite `artifacts` keyed by SHA-256. Page/discovery
observations use an isolated `manual_research:opinion-discovery-v1:…` stream;
source acquisitions use `manual_research:source-gate-v1:…`. Accepted opinion
interpretations are saved into the selected weekly research stream with stable
opinion keys. This uses the existing append-only schema; no legacy migration.

## Model review — one opinion at a time

1. Read the task, current original, source notes and relevant prior interpretation.
   Check the cited court/case identity. A text diff helps locate changes but does
   not establish completeness, especially for scans or complex formatting.
2. Screen for practical civil/commercial relevance: procedure, jurisdiction,
   contracts, entities, transactions, property, foreclosure, collections, remedies,
   evidence and appellate practice. A generally applicable procedural holding can
   matter even in a noncivil case. Give a concise reason for exclusion.
3. For relevant opinions, write the holding, disposition and author names separately.
   Preserve competing opinions and qualifications accurately. Use a short cited
   summary; do not invent an author, holding or legal effect from a case title.
4. For a corrected/substituted/withdrawn item, describe the source-stated change
   and connect related case identifiers in the summary. Do not resolve conflicts
   between an unchanged PDF and a changed notice. Cite official metadata for the
   notice and the opinion for its holding/disposition.
5. Copy the exact template to `<workspace>/receipts/<opinion-id>.json`:
   `id`, `signature`, `reviewer`, `relevance`, `summary`, `holding`, `disposition`,
   `authors` (list of names), and `citations` (list). Relevance is `relevant`,
   `not_relevant`, or `uncertain`. Completed screening needs a supporting citation;
   relevant findings also require holding/disposition and an opinion-PDF citation.
   Each citation supplies `sha256`, `text_sha256`, exact `quote`, and `locator`.
   Copy hashes from `source_observation` for the PDF or `opinion.status_source`
   for the official notice/metadata. Code binds URL/time automatically.
6. Save before opening the next opinion:

```sh
flwu opinion-review --database /absolute/path/research-history.sqlite \
  --registry <workspace>/expanded-registry.json \
  --receipt <workspace>/receipts/<opinion-id>.json
```

The validator rejects stale candidate signatures, missing current originals,
unsupported quotations and incomplete required fields. Exact receipt replay is a
no-op. `uncertain` outcomes remain queued; they do not become completed reviews.
Code cannot prove the legal interpretation, so check each quotation against the
actual original. If extraction is unavailable, use the explicitly scoped
`source-gate extract` procedure in the standard runbook; never invent OCR output.

## Failure, recovery and coverage limits

Every page and source is saved before proceeding. Resume with the same run ID and
arguments; completed pages/documents are reused. To retry a recorded HTTP/schema
failure, start a new run ID. A blocked court does not stop the other six, but the
combined command returns incomplete acquisition (exit 2). Even zero candidates
cannot justify “no new opinions” when any required channel is incomplete.

The structured inactive channel, official detail metadata and release pages are
monitored sources—not a certification of every ACIS docket or unpublished status
order. An inaccessible detail page remains a gap. Late postings older than the
overlap and unregistered legacy URL formats need explicit catch-up work. A newly
published notice can have its own CMS ID; the model must interpret its relationship
to the underlying case. Do not call metadata change a legal amendment automatically.

Finish current database/website integration through existing reviewed report and
directory publication steps. No old report contents, renderings or hashes need
rechecking as part of this work. Keep the previous finalized baseline intact until
a genuinely completed new report is explicitly finalized.

### Opinion response validation

An HTTP 200 response is not proof that the requested opinion was retrieved.
The standard update validates the PDF signature for every discovered opinion URL,
including extensionless download endpoints. Non-PDF response bytes and actual
URL/time/status remain preserved as failed observations. Opinion queue/review
acceptance additionally parses the saved PDF and requires nonempty saved text
extraction. A login page, malformed PDF, or missing extraction remains an
`opinion_download_unavailable` task with `document_error`; it cannot be screened
as relevant/not relevant or reused from a prior completed receipt. Exact replay
cannot override changed or unavailable evidence. Supply a reviewed extraction
through the existing extraction command when a genuine PDF needs OCR; never
invent a holding from its caption or a login screen. A corrected retry uses a new
run ID and preserves the original failure. Replaying an interrupted run reuses its
saved responses and does not silently replace the failed evidence.
