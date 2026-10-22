# Standard review and update sequence

This is the current update contract. It supersedes earlier instructions requiring
model-based website comparison or prohibiting reuse solely because identical
bytes were observed. Code decides whether source bytes or official opinion
metadata changed. A model screens relevance, interprets requirements and writes
supported findings. It does not decide source equality, calculate hashes, invent
source identities or mark blocked acquisition successful.

The statewide baseline is complete within its documented scope. These commands
maintain current evidence and future updates; they do not recheck historical
reports. Current execution remains cloud-only unless the user later authorizes a
local worker. The same bounded input/output contract is suitable for that worker.

## Required inputs and locations

- Database: `~/.local/share/flwu/research-history.sqlite`, or explicit `--database`.
  Always pin this path in the assignment. Trial runs use a separate database.
- Target `stream`: the existing **weekly research stream associated with the
  finalized reporting baseline**, selected from `flwu history streams`. Do not
  silently substitute a county stream or another stream's finalized report.
- Registry: a reviewed JSON file under `config/` or the private run directory.
  Exact keys are `schema_version: 1`, `stream`, nonempty `review_protocol`, and
  `sources: [{"id": "source-…", "url": "https://…"}]`. Generate IDs with commands,
  not by model reasoning. Register each relevant parent page AND each linked
  document independently. Stable URL identity is separate from content SHA-256.
- Run workspace: `runs/updates/<unique-run-id>/`. Original bytes and immutable
  observations live in the database; exported originals, diffs and work receipts
  stay in this private workspace. Never commit raw pages, PDFs or the database.
- On this checkout use the root project's `.venv/bin/flwu` with `PYTHONPATH=src`
  and `PYTHONDONTWRITEBYTECODE=1`. Do not install packages or restart inference.

Bootstrap a URL candidate registry once from saved citations:

```sh
flwu history streams --database /absolute/path/research-history.sqlite
flwu source-gate inventory --database /absolute/path/research-history.sqlite \
  --stream '<exact-weekly-stream>' --output runs/updates/registry.json
```

Inspect that candidate list against the [county source index](../research/counties/README.md)
and [appellate map](../research/APPELLATE_QUICKSTART.md). It is not a certification
of complete source registration. Remove obsolete/case-irrelevant candidates only
with an explicit scope decision; do not silently drop a blocked source. Save the
reviewed registry as the ongoing input. Add a newly discovered relevant document:

```sh
flwu source-gate add --registry runs/updates/registry.json --url 'https://official-host/document'
```

Inventory reads saved citations, not the entire web. The seven opinion listings,
tracked opinion PDFs and court release-notice pages are added by the standard
command automatically; they do not depend on the user remembering to register them.

## 1. Acquire and compare — mandatory standard entry point

```sh
flwu update --database /absolute/path/research-history.sqlite \
  --registry runs/updates/registry.json --run-id weekly-2026-10-25 \
  --output runs/updates/weekly-2026-10-25 --end 2026-10-25
```

Default reporting start is the last finalized report's capture date for this exact
stream. With no finalized report the command stops; supply an explicit `--start
YYYY-MM-DD`. `--end` is inclusive, default today in America/New_York. Ordinary
weekly reporting ends Sunday. Partial research never advances the finalized
baseline. The source gate compares against the **last successful source retrieval**
for efficiency; the reporting comparison remains last-finalized or explicit-start.
These are different, intentionally separate baselines.

Every run executes, without model selection:

1. Independently query the Supreme Court and all six DCA official opinion search
   feeds, including their inactive-status channels, with a default 30-day overlap.
   Follow pages using actual returned counts and verify court/date/offset/count
   metadata. Detect duplicates, premature empty pages and pagination drift.
2. Revisit tracked official opinion detail/status pages even outside the discovery
   window. Locate saved official opinion PDFs by exact CMS identity when bootstrapping
   from older citations. Unknown identities remain explicit acquisition gaps.
3. Fetch each registered source, court release-notice page and tracked/new opinion
   PDF independently. An unchanged parent page never exempts a linked document.
4. Preserve original response bytes, URL, resolved URL, actual retrieval time,
   response status and SHA-256. Save each successful or failed observation before
   proceeding. Failed/empty/oversized responses never replace the last success.
5. Compare raw SHA-256 in code. Different bytes create a review task even if a text
   extraction is identical. HTML timestamps or scripts may produce conservative
   false positives; there is no model-based normalization or equality decision.
6. Reuse a completed review only for the same source hash and review protocol.
   Identical but unreviewed material remains queued. Opinion reuse also requires
   identical official status metadata. Known effective-date triggers remain queued
   separately even when source bytes match.

Exit codes: **0** acquisition completed (reviews can still be pending), **2**
source/discovery coverage incomplete, **1** configuration/validation error.
An empty opinion task list with failed listings does not mean no new opinions.
There is no command that automatically finalizes or publishes these findings.

`source-gate run` is a lower-level maintenance/test helper, **not** the standard
weekly command: it does not perform seven-court discovery. Use `flwu update`.

## 2. Read only the next task

Open `<workspace>/update-queue.json`. Its sections are:

- `bounds`: pinned report and overlap dates, plus finalized baseline capture ID.
- `discovery`: fourteen court/channel coverage records and tracked-detail/identity
  failures. Review failures first; no court may disappear from the denominator.
- `source_reviews.tasks`: changed/new/unreviewed source tasks, original/extracted
  paths, unified text diffs, prior findings/version IDs and exact review templates.
- `source_reviews.effective_date_tasks`: date triggers generated from saved facts;
  resolve through normal report review, not by declaring source bytes changed.
- `opinion_reviews.tasks`: stable opinion ID, exact official metadata, original
  opinion and status-source paths, prior review, change reasons and review template.
- `reused_reviews`: successful reusable reviews; do not send their documents back
  to the model merely to re-establish equality.

Use this combined queue, not the lower-level unfiltered `source-reviews/queue.json`
(which may also include opinion documents). Process one judge/source or opinion
completely before moving to the next. Compact between tasks if useful. Retain the
workspace/database/registry paths and next task ID across compaction.

For sources: read the original and relevant changed sections; the diff is a
navigation aid, not evidence completeness. Check practical civil/commercial
requirements, contacts and assignment. Noncivil sources need only contacts,
assignment, official links and basic operations. Inspect newly linked relevant
sources in `observation.links`; register/fetch them before claiming their contents
reviewed. Record source conflicts without deciding which authority controls.

For opinions: see [the seven-court instructions](OPINION_DISCOVERY.md). Screen
civil/commercial relevance first; relevant opinions need a concise holding,
disposition, author names and exact source quotations with locators. Do not treat
first discovery or a corrected PDF as proof that new law was announced that day.

## 3. Handle extraction limits honestly

HTML/PDF/text extraction is deterministic and used only as a reading/diff aid.
Scans, unusual binary formats or embedded content can have empty/incomplete text.
Inspect the saved original using available tools. Do not install an OCR package.
If needed, save a reviewed UTF-8 transcription and an extraction receipt with
exact keys `source_id`, `observation_capture_id`, `sha256`, `method`, `reviewer`,
`scope`. Specify page/topic scope and label selected visual transcription as such.

```sh
flwu source-gate extract --database /absolute/path/research-history.sqlite \
  --registry <workspace>/expanded-registry.json --receipt <workspace>/extraction.json \
  --text <workspace>/transcription.txt
```

The derivative is bound to the current original; its hash does not replace the
original SHA-256. Regenerate the queue by repeating the standard command with the
same run arguments. An unreadable document remains an unfinished task, not an
unchanged or completed review.

## 4. Save one completed interpretation

Copy the task's generated `review_template` into `<workspace>/receipts/<id>.json`.
For ordinary sources fill `reviewer`, concise `summary`, exact `review_scope`, and
`outcome`: `baseline_reviewed`, `no_relevant_change` or `updated_findings`.
Only `updated_findings` supplies a nonempty `findings` array. Each finding requires
`key`, `kind`, complete `facts`, `expected_version` (from `prior_findings`, or null
for a new entity), and `citations`. Preserve existing IDs, kinds and all nested fact fields.
Do not replace an entire person record with just the changed telephone number.

Each citation requires `url`, original `sha256`, `text_sha256`, actual
`retrieved_at`, exact `quote` and `locator`. Copy source bindings from the observed
artifact, not from memory. Code checks stored bytes, original/extraction pairing,
quote containment, current source version and optimistic finding version. These
checks do not prove that the interpretation is legally correct; the reviewer must
verify that the cited passage supports it.

```sh
flwu source-gate review --database /absolute/path/research-history.sqlite \
  --registry <workspace>/expanded-registry.json --receipt <workspace>/receipts/<id>.json
```

A first hash-gate run can reuse earlier baseline bytes for comparison. Earlier
review completion is not inferred from mere artifact presence. If an existing
baseline receipt already covers the identical bytes and required scope, use that
receipt to supply the review summary/scope and record its location; no redundant
substantive rereading is required. Otherwise complete the queued review.

Opinion receipts use `flwu opinion-review` and their own exact template, described
in the opinion instructions. Review outcomes, including uncertainty, are durable.
No model-supplied “changed/unchanged” field controls the gate.

## 5. Resume, retry and integrate

Repeat the exact standard command/run ID to resume: completed acquisition pages
and sources are reused, and queues rebuild from persisted observations/reviews.
Do not change registry/window arguments under an existing run ID. Use a **new run
ID** to retry a blocked source or make a fresh retrieval; a resumed failed attempt
is still a recorded failure. After adding sources, start a new run ID.

A source that vanishes from a listing is not automatically withdrawn. Preserve the
last supported record and investigate the source-specific gap. Registry removals
are surfaced in `unregistered_previous_sources`. Reuse and changed statuses do
not establish complete web coverage: discovery remains bounded to the configured
feeds, overlap and tracked records. Late postings older than the overlap can be
missed unless independently discovered; increase overlap for a targeted catch-up.

After reviews, rerun the same command to rebuild the queue. Resolve pending date
triggers, uncertain opinions and coverage failures explicitly. Use existing
validated report/export and directory-publication procedures; a successful
acquisition or review command alone is never publication approval. Preserve report
baselines and history. Final integration checks current persistence, current
website consistency and future updates, without historical-report revalidation.
