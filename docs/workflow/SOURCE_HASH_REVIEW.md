> Execution policy: [use the invoking model](MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Standard review and update sequence

This is the current update contract. It supersedes earlier instructions requiring
model-based website comparison or prohibiting reuse solely because identical
bytes were observed. Code decides whether source bytes or official opinion
metadata changed. A model screens relevance, interprets requirements and writes
supported findings. It does not decide source equality, calculate hashes, invent
source identities or mark blocked acquisition successful.

The statewide baseline is complete within its documented scope. These commands
maintain current evidence and future updates; they do not recheck historical
reports. Use the invoking Codex or codex-local model under MODEL_EXECUTION.md.
The same bounded input/output and validation contract applies to both.

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

## Acquisition lifecycle

Both `update` and `source-gate run` hold a nonblocking OS lock at the canonical
database path plus `.acquisition.lock`, from before opening SQLite through final
queue export. A competing CLI acquisition exits 1 with owner PID/run ID; wait,
do not delete the sidecar or kill the owner. The OS releases the lock after normal
exit, exceptions or process death; leftover metadata is not a stale held lock.
The scope is CLI acquisition on this host, not arbitrary direct library/SQL writers
or distributed locking. Processes launched before this feature are unguarded and
must finish before a new acquisition starts. Symlink database aliases resolve to
the same lock; use one canonical database path (not hard-link aliases).

Progress JSON is flushed to stderr at phase/source/page transitions and every
30 seconds while waiting. Stdout remains the final result. Heartbeats indicate a
live process, not successful network retrieval. The last phase identifies current
work; a completed phase does not certify reviewed coverage.

Run only one acquisition against a database at a time. Save the exact command,
absolute paths, run ID, phase and returned tool session ID in RUN/RESUME.md before
continuing. A “Process running with session ID” response is not a failed command.
Wait on that numeric session with empty-input write_stdin; preserve it through
compaction. Read RESUME.md before any recovery action. The CLI may be silent while
saving hundreds of observations, and output queues are exported after collection.
Neither silence nor a missing queue file justifies killing or relaunching it.

If a tool session is lost, check the recorded OS process and children plus recent
read-only database captures. Do not restart an active acquisition. If multiple
acquisitions already exist, preserve them and request an intentional recovery
choice rather than killing arbitrary processes. A fresh run ID is allowed only
after the preceding acquisition has actually exited and a retry is warranted.
An interrupted, exited run resumes with its exact original arguments/run ID.

Use only arguments shown by --help. There is no --resume, --verbose, --log-level,
source-gate resume/kill, or FLWU_PAGE_SIZE setting. Do not tune overlap or page size
to cure a silent process. Never replace standard update with source-gate run.
After one corrective attempt at a repeated failure, save the precise error and
checkpoint and report it instead of cycling through new IDs or guessed options.

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
Every source receipt also requires `support` with exactly these fields:

```json
{
  "reason": "Explain the observed content and why it does or does not affect the scoped practice requirements.",
  "current": [{"sha256": "COPY_CURRENT_RAW_HASH", "text_sha256": "COPY_CURRENT_TEXT_HASH", "quote": "EXACT_CURRENT_PASSAGE", "locator": "section or page"}],
  "previous": []
}
```

Copy both hashes from this task's acquisition record. Read the current original or
extraction and the generated diff. For changed bytes, read the relevant previous
passages too; a `no_relevant_change` receipt must include at least one previous
citation with the same four keys, bound to the previous raw/extraction pair.
Explain the actual differences and their significance in `support.reason`.
The exported task includes `changed_text_lines.previous` and `.current`, computed
by code from the saved extractions. For `no_relevant_change`, quotations on each
side must cover every listed nonblank changed line. Multiple quoted passages are
allowed. Do not quote only a heading or one of several changes. A changed source
cannot use `baseline_reviewed`; choose supported `no_relevant_change` or save
`updated_findings`. Current acceptance version 3 prevents older unsupported
receipts from being reused as completed reviews.
A domain, page title, keyword match, generic “no actionable change,” or unchanged
navigation quotation is not a substantive comparison. If extracted text is
identical despite changed raw bytes, describe that fact and inspect the original
for material omitted content before concluding the change is immaterial.

Review one task at a time. Do not generate bulk completion receipts from hostnames
or keyword categories. Missing text is an extraction problem, never evidence of
irrelevance. Use the extraction procedure above or leave the review unfinished.
Older receipts without this support are not reusable completed reviews under the
current acceptance version. Quotation/hash validation establishes provenance;
it does not replace the model's substantive review of the changed content.

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


## 6. Separate report acceptance from screening

Research inspection must use the database pinned in `contract.json` or the saved
`history-capture.json` marker. A conflicting database override is an error.
For each source/roster task, `pages` must include its exact required URL with saved
acquisition metadata. A different page on the same domain cannot complete that
task. Additional evidence pages may supplement the required page. If its URL has
moved, retain the acquisition observation of the requested URL and its redirect;
do not relabel another capture or invent a successful response.

Once the reviewed report capture exists, generate a separate acceptance template:

```sh
flwu history review-template --database /absolute/path/research-history.sqlite \
  --capture-id <report-capture-id> --report <workspace>/report.html \
  --output <workspace>/publication-acceptance.json
```

The template also pins `acquisition` (`capture_id`, `run_id`, `queue_sha256`) to
the last saved standard-update result for this stream and reporting window before
the report capture. Do not edit this binding. If no matching result exists, finish
or resume the standard update and capture the report afterward. The database must
retain the queue artifact with its original hash; a hand-built report without a
standard update result cannot receive acceptance.

The template's `pending` list accounts for every task still present in that saved
queue: source/opinion reviews, effective-date triggers, unregistered sources and
discovery failures. Complete in-scope available reviews, rerun the same update to
refresh the queue, and capture the report afterward. Do not label unread evidence
unavailable. For a genuine saved retrieval failure, use `decision: unavailable`
with a specific explanation. For material outside the requested scope, use
`decision: scope_excluded`, explain why, and provide acquired quotations supporting
that exclusion (including the task's source when available). Preserve generated
`task_id`; each record has exactly `task_id`, `decision`, `reason`, `citations`.
These dispositions record limitations; they do not establish “no new opinions” or
“no relevant change.” Do not use a scope exclusion to avoid an in-scope review.

Keep the generated finding identities and versions. For every disposition choose
`include` with the actual included candidate key, or `exclude` with a substantive
reason and exact acquired citations supporting exclusion. Do not drop relevant
findings to make an empty report pass. For a reviewed judge/clerk update, `include_directory` instead maps `candidate_key`
to the personnel finding with identical reviewed facts and acquired source. Include
the directory row in the reviewed report artifact. Included news titles and summaries must appear
in the reviewed report. Reconcile each personnel inventory to cited actual named
people; “Chief Judge,” “Court Clerk,” buildings, and navigation headings are not
person identities. Every named roster entity must have exactly one matching
`person-<stable-id>` finding, with the same full name and judge/clerk role. No
personnel finding may enter the report without a roster identity. Reuse one ID
across multiple court inventories only when both name and role agree; preserve a
source conflict for review rather than silently merging different people. A
person-task receipt must retain the name from its roster-generated template.
The acceptance template compares inventories with the last finalized report and
prepopulates `removals` for missing IDs, including a wholly omitted inventory.
Each removal has exactly `id`, `name`, `reason`, and `citations`. Preserve its
original ID/name; explain the departure, reassignment or supported scope change,
and supply acquired source citations with exact quotes. An empty or missing
roster is not evidence that everyone departed. Partial research captures never
replace the finalized comparison baseline. Unsupported removals block acceptance.
These identity checks do not establish roster completeness: inspect all relevant
pages of the official roster and explicitly account for additions and removals.
Record actual legal and visual checks in `legal_review` and
`visual_review`, and identify the reviewer. Screening completion is not this check.

```sh
flwu history accept --database /absolute/path/research-history.sqlite \
  --receipt <workspace>/publication-acceptance.json --report <workspace>/report.html
flwu history finalize --database /absolute/path/research-history.sqlite \
  --capture-id <report-capture-id> --report <workspace>/report.html \
  --review '<reviewer and actual completed legal/visual checks>'
```

Acceptance pins the exact report bytes and finding versions. Edits require new
acceptance; newly captured review work requires rebuilding the report before
acceptance/finalization. Export of an already accepted finalized snapshot remains
bound to that snapshot's evidence, not subsequent reviews. Do not treat an old
screening receipt or the `ready_for_review` status as permission to bypass this gate.


Opinion listing/detail status evidence carries its actual response status alongside
URL, retrieval time and original/metadata hashes. For older entries, code may bind
missing transport fields from the saved parent acquisition event only when URL,
time and raw hash match exactly. The model must not assume HTTP 200 or reconstruct
missing timestamps. Unrecoverable metadata remains an evidence gap.
