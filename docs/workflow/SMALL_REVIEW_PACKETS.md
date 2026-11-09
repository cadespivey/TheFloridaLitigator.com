# Small evidence packets and personnel output contract

This is the current v7 reading/drafting contract for returned review tasks. It
supersedes instructions to dump an entire alignment, decoded comparison, full
packet, or every prior finding. Older immutable packets/guides remain identity
and history records. Receipt schemas, comparison hashes, acceptance gates and
the last finalized reporting baseline remain unchanged.

## Intent and stopping rule

Reduce model context and transcription errors after code has performed the
raw/content/component hash checks. Code decides whether evidence changed; the
model interprets the remaining change and civil/commercial significance. This
feature does not broaden research, approve unknown scripts, automate a verdict,
remove people, restart acquisition, or publish a trial. Follow
[RESEARCH_SCOPE.md](RESEARCH_SCOPE.md) and [REVIEW_INTEGRITY.md](REVIEW_INTEGRITY.md).

## Input locations and reading sequence

1. Obtain the next task using the installed `review_step.py next`, or use the
   next state already returned by successful `submit/revise --advance`. Read
   the returned `review_guide`. Copy its `receipt_template` to `save_receipt`.
   Do not open the original packet to reconstruct the drafting contract.
2. Read the current guide's scope, source role, output contract and
   `evidence_instructions`. Open `evidence_packets.path`. Its manifest and
   referenced evidence files are each at most **8 KiB**. SHA-256 values bind
   exact file bytes. These are lossless reading projections, not source originals
   or a relevance judgment.
3. For aligned HTML, follow `groups.first`, then each index page's `next` until
   null. The count is the exact number of entries. Open one group card at a
   time. `format:complete_group` is the whole small group in one file;
   `format:field_index` links a larger group's `fields.first` chain and values.
   Inspect every field/fragment in that chain. Group IDs
   and order are the same as the complete alignment. Scripts, nesting,
   attributes, context, decoded fields, decoding limits and serialization-only
   obligations are retained. Finish one group before moving to the next.
4. A value with `format:json` points to one complete JSON file. A value with
   `format:json_text_fragments` contains `parts.first`: follow every page/part
   in order. `.txt` fragments concatenate to the complete serialized JSON;
   `start_char`/`end_char` are Unicode character offsets, zero-based and
   end-exclusive. `serialized_sha256` binds its UTF-8 bytes. Fragments are not
   independent summaries and must not be treated as complete fields.
5. If no alignment exists, read every `changed_text` value when provided.
   `texts.current/previous.fragments` cover complete acquired extractions for
   selective context and quote lookup. Their offsets address the original
   extraction, not the serialized change fields. Do not reread unchanged text
   solely because it is linked. Missing extraction or unknown raw changes still
   require their existing original-document review; these projections are not
   an OCR, PDF-layout or original-byte substitute.
6. Read only affected `prior_findings_index` files and person templates. Save
   a short checkpoint with finished group IDs, remaining fragment pointers,
   affected person keys and draft path before compaction. Resume the same task.

The complete alignment remains under `audit_evidence.aligned_review`. Use it,
originals or legacy positional comparisons only for a specific missing-context
or decoding question. Never assume a truncated tool response covered the rest.
An unresolved field/group cannot prove a completed no-change review. Counts and
hashes preserve coverage; they do not prove that a model read or understood it.

## Exact quotes: select, do not retype

Use the pinned launcher. Replace uppercase paths with the actual returned paths:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py \
  workflow quote --run-dir RUN --guide CURRENT_GUIDE --side current \
  --start-line 12 --end-line 15
```

Line numbers are **1-based and inclusive**. Alternatively select absolute Unicode
character offsets in the extraction:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py \
  workflow quote --run-dir RUN --guide CURRENT_GUIDE --side current \
  --start-char 120 --end-char 460
```

The command returns `support` (exact `sha256`, `text_sha256`, `quote`, `locator`)
and `citation` (also acquired URL/time/status; null when full metadata is absent).
Mechanically copy
the suitable object into the existing draft JSON; serialization is allowed,
automatic interpretation/verdict generation is not. Opinion citation members
use the `support` shape. Previous-side selections may lack full citation
metadata: use their support object and never invent a retrieval time. Preserve
prefilled exact quotes unless evidence requires a different supported selection.

The helper reads only run-contained files, verifies the extraction's SHA-256,
and rejects missing sides, mixed/out-of-range selections, blank or >8 KiB quotes
and escaped paths. Select a narrower range when required. CRLF, nonbreaking
spaces and Unicode remain exact. It does not access/write the research database,
submit a review, advance a task, or certify factual support. Final acceptance
still checks the database's acquired original/extraction pair and current version.

## Personnel templates and outputs

For source reviews, `personnel_templates.new.judge` and `.new.clerk` point to
blank finding drafts. Choose the evidenced role; do not infer it from a URL.
Use these objects inside `receipt.findings` only for `updated_findings`. Their
envelope is shown below with contact slots abbreviated:

```json
{
  "key": "person-<stable-id>",
  "kind": "clerk",
  "facts": {"name": "", "fields": {}},
  "citations": [],
  "expected_version": null
}
```

Replace placeholders with the supported full name and the person's own stable
key. A named directory person uses `judge` or `clerk`, not `personnel_change`.
That event kind does not render a person in the directory. A successor is a new
person, never a renamed predecessor. Source inventory/office membership and
explicit departure/removal decisions remain separate validated steps; a new
person finding does not automatically remove anyone.

Use the guide's `personnel_templates.existing.first` index for an existing
judge/clerk. Each linked template deep-copies the complete saved facts and
`expected_version`. Preserve every nested field. Top-level citations are blank
deliberately: bind the changed facts to current acquired evidence, rather than
copying obsolete acquisition bindings into a new receipt. Existing nested facts
and their provenance remain retained under the existing preservation contract.

Generated templates include role-specific contact slots marked `unreviewed`,
with blank value/citation. Fill supported slots or remove unreviewed ones before
submitting; that draft marker is rejected on acceptance. Contact fields belong
in `facts.fields`, using human office labels:

```json
{
  "office_phone": {
    "value": "<supported phone>",
    "status": "verified",
    "citation": {"url": "<acquired URL>", "sha256": "<raw hash>",
      "text_sha256": "<text hash>", "retrieved_at": "<actual timestamp>",
      "quote": "<exact supporting passage>", "locator": "<location>"}
  }
}
```

Common judge fields: `chambers_phone`, `chambers_address`, `assistant_name`,
`assistant_contact`. Common clerk fields: `office_phone`, `office_address`,
`office_contact`. Retain supported assignments and official procedure/governing
rule links using the existing facts layout. Do not invent source labels such as
“Procedure address” or “Phone — profile.” Put provenance/conflicts in internal
evidence, preserving distinct supported contact meanings.

Do not treat a blank template as a completed search. Omit new unreviewed contacts.
Include each new field's citation in the finding's top-level `citations` too so
the normal acquisition-pair validator checks it. Use `status:not_published` only with cited checked sources and a nonempty
`search_log`; never fabricate an absence. A new verified field requires a value
and citation. Keep selection, appointment, effective service, former employment,
revision and retrieval dates distinct. Preserve contradictory statements without
deciding which controls. Limit noncivil review to the existing bounded scope.

New named `personnel_change` findings and malformed new typed contact objects
are rejected before persistence. Existing findings retain legacy compatibility
and full-field/version guards; old accepted receipts are not rewritten.

## Save, failure handling and completion

Write the draft to returned `save_receipt`; use the checked `review_step.py`
submit/revise with exact returned packet/predecessor/reason. Read the real exit
status and next state. Do not submit a group fragment as a complete receipt.
After two rejected drafts use the existing evidence-bound repair checkpoint.
Preserve exact errors and report them; do not claim “no validation failures”
because the final attempt passed. Hash/fragment failures require regenerating
the current projection from preserved inputs through the coordinator, never
editing originals or reacquiring to conceal a failure.

Implementation acceptance: deterministic byte-bounded lossless projections;
full aligned obligations and text preservation; exact quote selection/failure
paths; typed new and complete existing person drafts; early shape rejection;
unchanged packet identity/replay/recovery; installed launcher/skill agreement.
Tests are in `test_review_evidence.py`, `test_personnel_review.py` and the existing
workflow/source-gate/integrity suites. This patch's synthetic checks do not claim
a new live model speed measurement, current research completion or publication.

## Implementation verification — November 9, 2026

The complete suite passed **1,248 tests** without reported warnings. The staged
public-credential scan found no Google API key patterns. Read-only reuse of four
saved trial alignments (79,006–368,841 bytes) produced entry manifests of
507–509 bytes; the largest evidence piece was 8,093 bytes. Private measurements,
test XML/logs and the canceled coding-worker log are retained under
`runs/small-review-packets/`. No new live-model speed test, production research
write, weekly finalization, website data change or historical-report audit was
performed. A bounded local coding assignment was canceled after repeated shell
inspection errors and no edits; implementation was completed directly. The
inference server was neither restarted nor unloaded.

The maintained checkout passed 67 focused tests after checked installation;
58 unrelated pre-existing modified files retained their hashes. The installed
skill matches its repository source, and its launcher selected an exact CRLF/
nonbreaking-space quote successfully from outside the checkout. The skill's
explicit database location uses the canonical Developer/shared-history path.
