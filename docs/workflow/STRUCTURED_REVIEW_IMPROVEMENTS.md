# Structured review investigation and proposed next work

**Withdrawn as the next implementation plan — November 9, 2026.** The repeated
BF16 trial exposed more navigation, output and runtime without adequate accuracy
gains. Follow [SMALL_MODEL_REPAIR_PLAN.md](SMALL_MODEL_REPAIR_PLAN.md) for the
reconsidered, smaller design. Do not implement this document's expanded catalogs,
identity layers or broad schema migration. The earlier investigation below is
retained as design history, not active model instructions.

Status: **proposal for approval, not an active receipt contract**. The implemented
runtime remains guide v7 and [SMALL_REVIEW_PACKETS.md](SMALL_REVIEW_PACKETS.md).
Do not add the fields described here to an existing receipt, replace pinned run
inputs, restart research or migrate historical reports to implement this proposal.

## Findings from the current implementation

| Area | Working components to reuse | Remaining model burden / gap |
| --- | --- | --- |
| Source acquisition | `source_gate.run` persists original bytes and actual retrieval metadata. Exact-URL IDs, raw hashes, scoped content/component fingerprints, status checks and incomplete-source gates already exist. | The recurring registry accepts only `id` and `url` for each source. Purpose, expected page shape, court/person fields and extraction instructions are spread across county notes, baseline context and code. |
| Change identity | `raw_comparison.compare` and `aligned_review.compare` generate SHA-256 change/group IDs. Existing receipts bind comparison and alignment hashes. | IDs are deterministic already. Positional/aligned structural changes are not yet a canonical person/contact/assignment/rule-section diff, so models still translate page differences into domain fields. |
| Personnel | V7 supplies typed new judge/clerk drafts, complete existing-person drafts, exact quote selection and early new-person shape checks. Publication has roster/person identity checks. | Existing-person drafts still ask the model to carry full nested facts. Underlying contact/assignment layouts vary; new stable keys and source-to-person associations still need identity judgment. |
| Published directories | Read-only inspection found 67 county supplements and 1,557 person entries, including repeated/multi-county identities. All entries have structured `contacts.office` and `contacts.assistant` columns. | Those rows contain 580 distinct display-label strings. This is not 580 different semantic field types; it indicates that display labels should not serve as comparison keys or contact meaning. Do not flatten genuinely different phone/office purposes. |
| Opinions | All seven courts have explicit official listing/feed configuration, stable content identities, independent discovery and PDF/status signatures. Review has relevance, summary, holding, disposition, authors and acquired citations. | Evidence is attached to the whole review rather than each analytical claim. Initial acceptance checks author strings, but the stronger quoted-author-name check is currently in editorial revision. Relevance screening and analysis share one envelope. |
| Rules/statutes | `editorial.validate_change` requires materiality, different previous/current requirements, practical effect and a quote. Publication preserves accepted opinion content. | The legal-change object is supplied later during mapping; the template is not a dedicated adoption/section/before-and-after evidence analysis. Only the basis quote is explicitly checked there, not a separate citation binding for each previous/current requirement. |
| Evidence selection | V7 exact quote selection and bounded lossless files are now implemented. `worker_contract.span_citations` demonstrates supplied-span selection. | Normal review still requires assembling citation objects and moving facts into a complete receipt. The old controlled worker is a separate model-specific/extractive path; do not invoke or transplant its full prompt, status rules or runtime. |

Inspected implementation: [source gate](../../src/flwu/source_gate.py),
[court registry](../../src/flwu/court_registry.py),
[fingerprints](../../src/flwu/content_fingerprint.py),
[aligned review](../../src/flwu/aligned_review.py),
[opinion discovery/review](../../src/flwu/opinion_discovery.py),
[mapping](../../src/flwu/workflow_report.py),
[editorial checks](../../src/flwu/editorial.py),
[span validation](../../src/flwu/worker_contract.py) and
[directory projection](../../src/flwu/county_directory.py).
This is repository inspection, not a live source, personnel or legal-content audit.

## Proposed design

### 1. Versioned source recipes and typed evidence projections

Keep the exact acquired URL and current source ID. Add a **versioned sidecar
catalog**, pinned by hash for a new run, instead of adding ad hoc fields to the
strict v1 registry or editing contracts of runs already in progress. Seed the
catalog from the existing court/opinion configuration, 67 county supplements,
reconciliation manifest and county source notes. Reuse those findings; do not
repeat statewide research merely to populate recipes.

Each recipe supplies court/county IDs, source purpose, official URLs, permitted
redirect/alias rules, extractor/profile ID and version, expected structure,
required anchors/columns, bounded fallback instructions and fields it can support.
Opinion recipes retain listing pagination, date-window overlap, detail/status
sources and document retrieval independently. Rule recipes distinguish an
adoption source, current compilation and individual procedure document. Discovery
pages are not themselves proof of a substantive amendment.

Concrete reuse example: the recorded Supreme Court listing is
`https://supremecourt.flcourts.gov/Opinions`; its configured search endpoint is
`https://flcourts-media.flcourts.gov/_search/opinions/`. The existing query builder
supplies `siteaccess=supreme2`, `scopes[]=supreme_court`, `searchtype=opinions`,
`sort=opinion/disposition_date desc`, resolved `startdate`/exclusive `enddate`,
`limit`/`offset`, and `nonactive_only=1` for the inactive channel. Standard defaults
are a 30-day overlap, 50 entries per page and 200 pages maximum. These values
should be emitted from the pinned configuration into source context, not copied
into a second hand-maintained URL list or reconstructed by the model. All six
DCA configurations already exist in `src/flwu/data/opinion_sources.json`.
These are repository-recorded endpoints, not a new live availability check.

Code emits typed facts with exact evidence spans, not semantic guesses. Use
separate identities for **person**, **court/office**, **assignment**, **contact
route**, and **procedure document**. A clerk's stable office URL identifies the
office; it does not establish that a successor is the same person. Reuse existing
person keys. Official stable person IDs may support deterministic associations;
ambiguous successor/name/alias changes receive one explicit identity decision.
Never merge people automatically by name or office URL.

Proposed canonical field families:

- Court: level, numeric circuit/DCA number, counties, official source references.
- Person: stable identity, full name, evidenced role, official profile references.
- Assignment: person, court/office, division, supported civil/noncivil assignment,
  stated start/end dates and date meaning; absence is not a departure.
- Contact: owner, purpose (`chambers`, `scheduling`, `assistant`, `clerk_service`,
  etc.), medium (`phone`, `email`, `fax`, physical/mailing address), value and
  separate address components. Preserve extension, service restriction and source
  variants. Public labels are generated from meaning, never “Phone — PDF.”
- Procedure: stable document identity, applicability, official URL, stated
  revision/effective dates and bounded operating categories from the existing
  civil-practice checklist. Retain originals and reviewed scope separately.

Each field stores observed value, comparison value, normalization-policy version,
evidence references and explicit state (`observed`, `not_published` with searched
evidence, `unreviewed`, `conflicting`). Keep conflicts as a list of source-bound
statements, not an overwritten winning value. A normalized comparison value is
not permission to discard its original spelling, URL, address or date meaning.

### 2. Code-owned comparison and patch compilation

Retain the existing order: acquire -> raw hash -> approved content/component hash
reuse -> deterministic typed projection/comparison -> model interpretation only
where needed. Do not turn a parser or a model keyword filter into a new blanket
no-change policy. Changed PDFs, status notices, unknown content, failed retrieval
and effective-date triggers keep their existing obligations.

Equal typed fields alone are insufficient for reuse if other original content
changed. Track unassigned/unknown regions and their hashes alongside the typed
projection. Only the existing approved presentation/component policies or a
separately reviewed, versioned coverage policy may account for those differences.
A changed unparsed procedure block or script must remain a task even when every
recognized phone and name is unchanged. Otherwise a convenient schema becomes a
silent source of false negatives.

Versioned comparison output contains code-supplied source/entity identity,
comparison ID, field pointer, previous/current value and supporting span IDs.
Generate IDs with SHA-256 over explicitly versioned canonical JSON; retain the
current exact original-byte hash bindings. Specify UTF-8, type preservation,
Unicode/whitespace rules and ordered-versus-set arrays per field. Unknown values
remain different. Do not lowercase arbitrary paths, discard qualifiers, infer
equivalent routing or ignore timestamps indiscriminately.

For new field comparisons, a concrete candidate ID scheme is:

```text
comparison_id = SHA256(canonical_json([
  "field-comparison-v1", existing_source_id,
  before_raw_sha256, after_raw_sha256, extractor_policy_sha256
]))
diff_id = SHA256(canonical_json([
  "field-diff-v1", comparison_id, existing_entity_key, field_path,
  SHA256(canonical_json(before_value)), SHA256(canonical_json(after_value))
]))
span_id = SHA256(canonical_json([
  "evidence-span-v1", existing_source_id, raw_sha256, text_sha256,
  start_character, end_character
]))
```

Use the existing `history.canonical` representation: sorted object keys, compact
separators, `ensure_ascii=False`, UTF-8; arrays remain ordered unless an explicit
field policy defines set semantics. Bind observation capture/URL/retrieval time
separately; clock changes alone must not change a logical evidence span. Preserve
existing source/person/group IDs and old receipts rather than retroactively
restamping them. Recipe context should expose the actual selected profile,
extractor/policy hashes, boundaries and diagnostic status as code output. Models
need that resolved context, not instructions to compute SHA-256 themselves.

All source, evidence, comparison, diff and proposed-record IDs come from code.
The model selects supplied IDs and interprets the supported change. It never
calculates, retypes or invents those IDs. An ambiguous person identity remains a
review decision; code generates the final identifier from that decision.

Replace full-record reauthoring in the new contract with **bounded field decisions**:
code supplies the diff ID, permitted field path, old value, proposed observed
value and exact source spans. The model confirms or corrects the interpretation
using acquired support. A compiler applies validated decisions to the complete
prior record with `expected_version`, preserves unaffected nested facts, and
builds the existing full source-gate finding/citation envelope. Reject stale
versions, unknown IDs, unsupported values, added paths and uncited replacements.
Do not ask the model to copy every unchanged field just to update one phone.

This should be an additive, versioned projection/receipt layer over the current
append-only history, not a replacement for the frozen operational schema or
historical report format. Old captures and accepted receipts remain immutable.

### 3. Claim-bound opinion and rule analysis

Use a short screening result first: supplied candidate ID, relevant/not-relevant/
uncertain, one concise reason and evidence IDs. A clearly irrelevant noncivil
opinion should not require a complete civil case brief. Uncertain screening
remains unfinished. Preserve the existing bounded scope.

For relevant opinions, present code-prefilled court, case identifiers, publication
date, PDF hash, official status and related opinion IDs. Ask for:

- legal issue and concise holding, with opinion span IDs;
- disposition, with opinion span IDs;
- author names/attribution type and support for each name (per curiam may have
  no individual author; a concurrence-panel listing is not author attribution);
- a short practical civil/commercial effect and only material qualifications;
- the source-stated correction/withdrawal/substitution effect, if applicable,
  with status-source evidence independent of the PDF.

Generate the public summary and mapping from this accepted analysis. Do not ask
the model to write the same holding at acquisition, mapping and publication.
Reuse a completed analysis only for the identical evidence/status signature and
compatible review policy; a partial run cannot move the reporting baseline.

For rule/statute/local-procedure changes, supply a dedicated template:
authority/document/section; adoption/publication/revision/effective dates with
their meanings; prior requirement + prior span IDs; current requirement + current
span IDs; scope/applicability; material practical effect; public title/summary.
Code supplies the changed-section IDs and pre/post text when available. Bind each
claim to its own acquired support. A newly enacted provision may have no prior
equivalent; record that supported change type rather than inventing an old rule.
When prior evidence is missing, do not claim an unsupported before/after change.

Allow explicit “no material legal change” and internal conflict/unknown outcomes.
Formatting noise, newly found old instructions and compilation discrepancies do
not alone become public news. Do not add research-incomplete or source-comparison
commentary under public headings. Proposals receive only the existing brief
screening/status check, not an expanded rulemaking or pending-bill project.

### 4. Format-drift handling without silent data loss

Use strict **core semantics** with flexible, source-bound **extensions**. Optional
fields are not mandatory boilerplate. New legitimate fields can be preserved in
an extensions collection with raw path/label/value, evidence and unreviewed state
until a reviewed adapter maps them. Extensions cannot override known identity,
contact, timing or status fields or bypass citation validation.

Adapters report `complete`, `partial` or `unrecognized`, plus deterministic
diagnostics: missing anchors, changed headers, unexpected row identities, invalid
types, ambiguous associations or missing pagination. Zero parsed people after a
roster structure change is not an empty roster or mass departure. A missing field
is not `not_published`. Same-body HTTP-200 access stubs remain unavailable content.

For format drift, preserve originals, retain the last verified projection, and
emit one bounded adapter-repair/evidence-selection task for that source family.
Record each affected source failure independently. Reuse a repaired versioned
extractor on preserved bytes, comparing the resulting fields deterministically;
do not reacquire or repeat completed substantive analyses without a dependency
change. Independent sources continue. A familiar hostname never proves that an
unknown script, link or document format is harmless.

## Recommended implementation order and acceptance

1. **Personnel pilot + evidence IDs.** Add shared span selection/receipt compilation,
   source-recipe sidecars, typed contact/assignment projections and field patch
   decisions for one representative court family. Reuse the saved clerk-successor
   and judge-profile evidence. Preserve other source formats through current v7
   fallback; do not claim statewide adapter coverage from one pilot.
2. **Opinion contract.** Add claim-bound analysis and identical initial/revision
   author checks; exercise ordinary opinions, status-only withdrawals, changed
   PDFs and unknown authors through the actual seven-court standard command.
3. **Rules contract.** Add section-aware pre/post/adoption evidence and structured
   practical-effect analysis, retaining current editorial gates and scope.
4. **Expand proven recipes.** Work through shared court CMS families and measured
   remaining model burdens; preserve county/judge completion order and shared
   source reuse. Do not build 67 bespoke crawlers or promise universal parsing.

For each phase, test unchanged bytes, approved metadata-only change, real contact/
assignment changes, successors at unchanged office URLs, duplicate names,
conflicting sources, renumbered/reordered fields, escaped URLs, missing fields,
unknown scripts/qualifiers, HTML layout drift, scanned PDFs, stale versions and
interrupted recovery. A changed-field task must carry exactly the required prior/
current evidence and preserve every unaffected fact after compilation/readback.

Measure an identical saved 20-source corpus before and after, with a pinned model
and settings if a live trial is authorized. Separate retrieval/CPU time, model
time, input/cached/output tokens, tool calls, failed attempts and substantive
accuracy. No production writes/publication from that trial. Initial acceptance:
all IDs/bindings supplied by code, zero model-authored hashes, zero full-record
copies for a one-field change, no false no-change after drift, complete preserved
evidence and claim-level citation validation. Set speed targets after the baseline
measurement rather than claiming an untested improvement.

The investigation does not authorize implementation of these next phases.
