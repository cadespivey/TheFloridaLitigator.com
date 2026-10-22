> Current update sequence: [hash-driven source and opinion review](SOURCE_HASH_REVIEW.md). Use `flwu update` for every weekly run; it always discovers opinions for the Supreme Court and all six DCAs. Code compares source hashes and official status metadata before model review. This supersedes older cross-run no-skip and model-comparison instructions; completed identical-source reviews may be reused. Final integration excludes historical-report checks.

> Current authority: Astra-only execution under [STATEWIDE_BASELINE_GOAL.md](STATEWIDE_BASELINE_GOAL.md). This supersedes all earlier local-worker requirements. No local workers, inference-server restarts or model unloads.

# County-baseline checkpoint save

`flwu.baseline_capture` validates and saves an **incomplete county checkpoint**
through the existing `flwu.history` API. It creates no new persistence model and
never finalizes or publishes a report. Use it after collecting originals,
reviewing the relevant contents, and preparing the judge receipt. Astra performs
research, implementation, validation and corrections directly; no local-worker
assignment is authorized. See
[STATEWIDE_BASELINE_GOAL.md](STATEWIDE_BASELINE_GOAL.md) for the active goal.

## What the save establishes

- **Collected:** original response bytes and extracted text have been acquired.
  Record HTTP status, source URL, actual retrieval timestamp, stated dates, and
  hashes. A failed response or image can be retained in the acquisition inventory.
- **Reviewed:** a researcher checked applicable content, correct person/assignment,
  citations, and page/table interpretation. Mark partially reviewed documents with
  explicit page/topic scope. Record conflicting statements without choosing which
  authority controls. Missing evidence remains distinct from conflict.
- **Saved:** the supplied bytes and structured observations are stored together.
  Structural validation cannot establish source authenticity, substantive legal
  accuracy, review completeness, or whether a pinpoint supports the conclusion.

Use `flwu.research._person(root, receipt, trial=True)` and the county research
checklist before adding a completed judge to findings. This helper does not run
that domain-specific review or turn unfinished drafts into accepted findings.
A first observation is not a new legal requirement. The finalized report, not the
latest partial capture, remains the default comparison baseline.

### First comparison for a county baseline

Comparison baselines are scoped to the exact saved stream. A reviewed directory
supplement does not finalize that research stream. Until a report has actually
been finalized for that stream, a default comparison correctly reports
`baseline_known: false`; do not silently substitute the most recent research run
or another stream's report. For baseline follow-up, supply an explicit start date
and retain the resulting coverage limitations. A date before the first observation
cannot establish an earlier baseline. First observations are not new law.

The October 22 Calhoun read-only exercise records three corrected findings with
an explicit October 22 start; the default remains unknown because that county
stream has no finalized report. See
[comparison evidence](../../research/audits/20261022/current-comparison-exercise.json).
This exercises existing behavior; it does not create a new finalized report or
advance any comparison baseline.

### Evidence freshness in comparisons

Keep acquisition metadata in citations rather than semantic facts when preparing
new adapters. Existing county records sometimes contain nested citation objects.
`history.compare` ignores only `retrieved_at`, `extracted_at`, `path` and
`text_path` inside objects with nonempty string `url`, `sha256` and `retrieved_at`
fields. This prevents an unchanged source recheck or local file relocation from
becoming a substantive finding change. URLs, hashes, quotes, stated effective or
revision dates and all other fields remain significant. A similarly named field
outside a recognizable evidence object is not silently ignored.

This is a read-time comparison rule, not a migration: raw captures, finding
versions, evidence bytes and returned current findings remain unchanged. Legacy
records may therefore retain multiple raw versions without a substantive change
event. Source-check hash changes still request review. Both explicit-date and
last-finalized-report comparisons use this rule; older evidence cannot roll back
current findings. Regression coverage is in `tests/test_research_history.py`.

When a reviewed source has several timing clauses, the receipt may include
`deadline_rules`: subject, action, amount, unit, direction, trigger, source wording,
exceptions, conflict group and citations. Include these entries in semantic facts
after removing citation metadata; retain their citations in the full receipt.
Arthmann packet66 is an exercised example. Do not merge conflicting units or
calculate legal deadlines from these fields. Likewise preserve shared-source
adoption/non-use associations and separate issuance, nunc-pro-tunc and stated
effective wording in comparison facts. The save helper validates evidence bindings;
it does not infer these legal meanings or extract them automatically.

## Packet contract

Exactly five top-level keys are required:

| Key | Meaning |
| --- | --- |
| `scope` | Object containing `profile: county-baseline-v1`, lowercase county slug, integer `circuit` 1–20. Pin and retain the exact object. |
| `stream` | `MODE:county-baseline-v1:` followed by the first 12 characters of `flwu.history.sha(scope)`. |
| `run_id` | Stable caller identity for the research checkpoint. |
| `payload` | Existing history payload, with explicit contract mode and incomplete status. |
| `artifacts` | Map from lowercase SHA-256 to a repository-relative path containing those exact bytes. |

`payload.contract.mode` is `manual_research` or `synthetic_replay`.
`payload.status` must be `incomplete`; at least one check must remain incomplete
for remaining county work. Verified checks require an aware, nonfuture
`checked_at` and a nonempty list of hashes present in the packet. Check IDs and
finding keys must be unique.

Every finding has `key`, `kind`, `facts` (object), and nonempty `citations`.
When augmenting an existing finding, retain its entity key and kind. Verify that
run IDs, check IDs and review labels name the actual subject before saving; do not
carry another judge's labels forward from an example. Compare preserved fields
against the previous saved facts, in addition to validating the new checklist.

Keep semantic facts separate from retrieval/check timestamps and quoted evidence;
the helper preserves caller facts unchanged. A citation contains:

```json
{
  "sha256": "<original SHA-256>",
  "text_sha256": "<UTF-8 extracted-text SHA-256>",
  "quote": "Exact text from the retained extraction",
  "locator": "PDF physical page 3, paragraph 2",
  "url": "https://www.17th.flcourts.org/<verified-source-path>",
  "retrieved_at": "<actual ISO timestamp with timezone>",
  "http_status": 200,
  "authority": "official",
  "synthetic": false
}
```

This is a shape illustration, not runnable evidence. Do not invent hashes,
retrieval times, URLs, or quotations. Use the existing `authority` field, not
`source_authority`. Live citations require explicit boolean `synthetic=false`;
replay citations require `true`. Both original and text hashes must reference
provided artifacts; quotes must occur exactly in UTF-8 text. Normalize derived
HTML text to LF before hashing while retaining original response bytes unchanged.
Optional `resolved_url` undergoes the same URL checks as `url`.

All citation-bearing dictionaries and `citation`/`citations` fields are checked
recursively, including facts and nested receipts. All nested raw/text hash
references must resolve to packet artifacts. Inventory entries without quotes
are not citations: failed responses and image bytes may be retained without
pretending to support a finding. Null unfinished citation placeholders are
allowed in drafts; they do not satisfy a finding's required citations.

Artifact paths cannot be absolute, escape the root, or traverse symlinks within
it. The explicit root may itself resolve through the platform's normal path
aliases. Known local/private addresses, non-HTTP URLs, credential-bearing URLs,
and secret query parameters are rejected; `.invalid` is allowed only for replay.
This is offline input checking, not DNS verification or a network security proxy.
Validation happens before opening the database. Runtime database failures still
propagate; the existing history transaction protects writes. A failed initial
runtime write can leave an initialized empty history database, unlike a rejected
packet, which does not create a database.

## Save a reviewed checkpoint

From the repository root, the completed Phillips packet is a working example:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m flwu.baseline_capture \
  --root "$PWD" \
  --packet runs/county-broward/2026-10-15/draft/checkpoint-18.json \
  --database /Users/cadespivey/.local/share/flwu/research-history.sqlite
```

The packet's referenced local files must exist. This command targets the real
research database: use it only for reviewed live evidence, never fixture trials.
Exact replay returns the original capture ID. The reviewed Phillips packet was
exercised against a **temporary** database with 243 artifacts and one finding;
its capture ID matched the existing history-API save. No helper trial was written
to the shared database.

For a new judge, assemble a new packet using the preceding checkpoint's immutable
scope/stream/contract; use the judge's validated receipt for semantic findings,
retain the full receipt and acquisition inventory in drafts, and include all
referenced original/text bytes. Record remaining county work explicitly. Save
JSON acknowledgment outside the packet, then read back artifacts/facts, verify
identical replay, and confirm finalized reports remain unchanged. Update
`state.json` only after successful save/read-back. On error, preserve the packet
and repair the evidence or extraction; never relabel it to bypass validation.

A changed retrieval observation creates a capture even when facts are stable.
Unchanged facts reuse a version; changed facts create another version; identical
artifact bytes reuse their blob. Nothing deletes prior observations. Review
changes against `history.compare` with the finalized baseline or explicit start
and end dates; do not infer deletion from absence or legal change from a hash.

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m pytest \
  tests/test_baseline_capture.py tests/test_research_history.py \
  tests/test_publication.py tests/test_research_as_of.py -q
```

October 15 validation: 159 tests passed. Tests use temporary directories and cover
nested malformed citations, timestamp/mode/source markers, exact byte integrity,
UTF-8 extraction, symlinks/escape, secret URL redaction, replay, observation and
fact versioning, unchanged-source blob reuse, changed-source bytes, transaction
rollback, preservation of finalized reports/unrelated tables, legacy DB rejection,
and CLI behavior. These are storage/validation results, not county completeness
or substantive legal review. The statewide live pilot remains unfinished.

## Stable packet replay after later research

A successful replay immediately after saving does not prove that local packet
paths will remain replayable. Shared review JSON, working receipts, original-name
roster files and screenshots can change during later tasks. Their old bytes remain
in the history database, but an old packet pointing at a mutable working path will
fail its hash check after that file changes. Do not weaken hash validation.

After each save, bind such artifacts to hash-named local copies and retain a new
`*-frozen.json` packet. Preserve payload, run_id, stream, scope and every hash;
change only the artifact-map paths. For existing captures, recover bytes by their
recorded SHA-256 from the database, verify the digest, and write a new local copy.
Never reconstruct an old artifact from today's receipt or alter the original
packet/history. For new captures, hash-named copies can be prepared before saving.

The exercised Broward utility is
`runs/county-broward/2026-10-15/review/freeze-replay-packets.py`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python \
  runs/county-broward/2026-10-15/review/freeze-replay-packets.py 49 50 51
```

This is a pinned-run utility, not a generic county CLI. It uses read-only artifact
queries, verifies byte hashes, writes new hash-named copies and packet files, then
replays through the unchanged validated helper. It requires the saved capture
acknowledgment and fails if the recorded bytes cannot be found. The three exercised
packets returned their original capture IDs/sequences with unchanged payloads,
no new capture and unchanged finalized reports. Evidence is in
`review/frozen-replay-results.json`. Prefer these frozen packets for later replay.
Older county packets still need the same binding audit before county completion;
the current three-packet check does not establish all historical files are stable.

October 16 expanded binding audit: all Broward packets1–61 now have verified
frozen artifact maps and successful exact replay. The run utility accepts the
original zero-padded01–09 filenames without renaming historical packets. Each
replay returned its recorded capture ID/sequence, with unchanged payload and no
new capture or finalized-report change. This supersedes the older-packet pending
status above. The result remains a storage-integrity check, not substantive legal
accuracy, source completeness, or county-publication acceptance. Redirect the
utility's cumulative JSON output to a run artifact to avoid filling model context.

## Sequence numbers are not contiguous (October 20 review correction)

Assert the expected latest capture *before* a write to detect concurrent changes.
Do not require the returned sequence to equal the previous maximum plus one.
`captures` uses SQLite AUTOINCREMENT and `record` uses INSERT OR IGNORE; an exact
replay can consume an allocator value without adding a row. Gaps alone are not
evidence of deletion, rollback or tampering. Verify the returned capture ID,
payload, stream, unique row, artifact/fact readback and idempotent replay instead.
A new regression test reproduces this without any DELETE statements.
