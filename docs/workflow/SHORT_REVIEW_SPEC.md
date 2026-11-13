# Short-answer review: intent, specification and acceptance

Approved November 9, 2026. Replaces the proposed-only interface in
SMALL_MODEL_REPAIR_PLAN.md. Preserve the existing source/opinion validators,
immutable evidence and accepted history. No production database migration.

## Intent

Reduce routine review to a court/law/personnel decision. Code owns evidence
selection, exact quotations, citation duplication, identifiers, versions, receipt
assembly and failure accounting. The selected model interprets significance.
This is not permission to infer harmlessness from equal extracted text or to
hide unknown original-content changes. Do not extend universal website parsers.

## County baseline reuse and comparison

The November 12 repair connects reviewed county checkpoints to weekly source
comparisons through `county_baseline_link`, with the contract in
[SOURCE_HASH_REVIEW.md](SOURCE_HASH_REVIEW.md). This is code-owned evidence reuse,
not new model acceptance. The existing review answer format and publication gates
remain unchanged. A changed page receives before/after evidence instead of a full
new-baseline assignment when the earlier source can be verified. Original county
findings and their review limits remain preserved; only supported changes belong
in the weekly output.

## Normal interface

The checked `review_step.py next` entry invokes `workflow model-next` and returns
`review_mode:inline_answer`: a complete `review_card` object, short `task_handle`,
one checked `command`, phase/completion and code-owned progress. The card is
self-contained JSON: question, acquired before/after passages with
short evidence IDs, small prior-person summaries and only the answer fields this
kind needs. No fragment indexes, raw-group narratives, receipt schemas or hashes
are required model reading. Complete acquired evidence remains available in the
maintenance artifacts; existing packets/receipts stay immutable.

Send the semantic answer JSON on stdin to the returned run-local `review HANDLE`
command. It pins the exact checkout/interpreter/run and invokes checked
`review_step.py reply`. The helper saves the original bytes before invoking
`workflow reply`, which resolves the handle and uses the existing compiler and
validators. It returns the next complete inline card in the same action. The
model does not read a separate card file, create an answer file, repeat long paths
or write receipts. Detailed packet/binding/receipt/diagnostic paths remain in
private maintenance artifacts, not the ordinary model response.

The handle binds protocol, verified run contract, checkout/interpreter, packet
and complete evidence card. Code revalidates against acquired database evidence;
a modified manifest/card/packet or another run's handle fails closed. A new reply
must address the actual current task. Exact replay after acceptance/commit is
idempotent and returns the current state; a changed accepted answer requires the
existing explicit correction. Identical rejected retries reuse the stored error
and do not consume another rejection attempt. Replies serialize per run; existing
coordinator/optimistic-version checks remain authoritative. A busy run is waited
on, never restarted. Exact inputs, failure causes and raw coordinator states are
retained. The helper updates the next-state pointer only
from the actual successful coordinator output. Old submit/revise remain available
for maintenance and downstream stages. `workflow next-task` and file-based
`answer --advance` remain compatibility APIs, not a second routine model UI.
On entry/resume or lost/truncated output, refresh checked next with sufficient
output capacity; this never reacquires. Never answer a truncated card.

Source answer: `decision` (no_material_change, material_change, or
insufficient_evidence), `summary` (supported concise reason), `evidence` (supplied
IDs), `people` (empty unless named personnel facts changed). A person has
`person` (supplied prior-person reference or new), `name`, `kind` (judge/clerk),
`evidence`, and `fields` mapping supported field names to `{value, evidence}`.
Existing names cannot be silently renamed into a successor. Code creates stable
new-person IDs, preserves all prior nested facts/version fields, inserts exact
citations in both field and finding citation collections, and omits unreviewed
fields. No automatic roster removal. Material nonperson changes become cited
source-change findings for the existing separate publication mapping/review.
For a new person, include current phone/address/email/assistant contacts explicitly
supported in the card, including unchanged office contacts. Contact text may differ
only in formatting whitespace; code compares that narrow equivalence while keeping
submitted values and exact original citations. Noncontact text, URLs/emails,
punctuation, case, digits and source quotations retain exact support requirements.
Preserve useful address line breaks. Never infer unpublished contacts or inherit personal
contacts from the predecessor; name-only source evidence remains legitimate.

Opinion answer: `relevance` (relevant, not_relevant, uncertain), `summary`,
`holding`, `disposition`, `authors` (names only), and `evidence`. Acquired status,
identity and signatures come from code. Relevant opinions still require cited
holding/disposition/author analysis; uncertain is unresolved, not completed.
General civil/appellate procedure is in scope for individual/small-claims parties;
a novel rule or case-specific application is not required. A complete unexplained PCA can be not_relevant for
lack of a stated substantive ruling, without underlying-lawsuit research. Reserve
uncertainty for missing/unreadable evidence or genuinely unresolved significance;
a documented source conflict alone is not incomplete review. A material official
correction/withdrawal/status change can itself warrant an update with unchanged PDF bytes.
Never infer unpublished/nonprecedential status from Citation/PER CURIAM or a
missing reporter cite. Holding states operative facts/rule with express exceptions
and record limits; illustrative examples are not exclusive tests. Summary gives
practical effect while retaining the same material qualifications and exceptions;
it must not broaden a qualified holding. Exclude research bookkeeping and party-name reconciliation.
Disposition states court action only. Authors are identified bylines, not panels;
per curiam without an identified author uses an empty list. Excluded matters need
a brief supported reason and empty holding rather than specialized merits analysis.


A citation affirmance quoting applicable civil/commercial principles is not a bare
PCA: include it when relevant even without new law or case-specific application.
A bare PCA provides no substantive reasons or stated applicable principles.
Preserve material qualifications in BOTH holding and summary: “ordinarily” stays
qualified; “such as veil piercing” gives an example, not the only available test.
Excluded matters usually need one supported sentence, without specialized merits,
biography or repeated dates/status. Do not infer underlying-order finality from a
rule number or the opinion's rehearing-finality warning.

For source tasks, use code-owned source_context: baseline establishes supported
current information and requires no prior passage; comparison needs the supplied
before/after evidence. A navigation-only baseline may yield no material finding,
without certifying historical no-change or opinion-discovery coverage. Missing
expected body content/extraction still remains unresolved. Configured opinion
notice-page review is separate from official listing/status discovery and PDFs;
the role label alone is not proof of complete extraction.

Code copies quote bytes/Unicode exactly from acquired extraction, not model
transcription. Missing/unknown evidence IDs, unsupported contact values, stale
packets, malformed decisions and mismatched versions fail closed. Acquired link inventories are compared deterministically and shown on the same
card when links change, including when visible text also changes. A listed URL
does not establish target content or accessibility. URL-valued personnel facts
are verified against the acquired current inventory; invented or removed URLs
are rejected. The model does
not author raw hashes, timestamps, full citations or optimistic version IDs.

## Deterministic downstream route

The standard model-next/reply entry runs publication_driver between semantic
answers. Reviewed opinions are mapped to case_law with copied text/dates/citations;
complete structured candidates retain their explicit section/change analysis;
known personnel IDs and named inventories are projected, not retyped. Unchanged
prebaseline findings do not become new news. Code applies exact identity targets,
preserves untouched contacts/county assignments and reconciles roster departures
only from explicit reviewed removal decisions. Routine mapping/directory/roster
receipts are generated privately through existing validators.

Unknown legal metadata, new personnel scope, ambiguous aliases, county-specific
assignment and actual coverage failures use compact inline cards/short answers.
Code owns evidence IDs and full receipt compilation. Missing scope, dates or
substantive meaning cannot be inferred merely to complete publication.

One compact publication_acceptance card carries current entries and changed
personnel rows. Its answer is decision (approve/correct/unresolved), reason and
corrections. Approve requires an actual content decision with empty corrections.
Correct identifies an N-reference, substantive reason and only changed opinion
summary/holding/disposition/authors. Existing source-bound append-only revision
APIs invalidate the report/build/mapping; no generated archive is edited in place.
Code checks exact build bytes, current serialized issue/directory data and page
rendering targets before generating acceptance. It never asserts independent
human/browser review. Semantic truth still depends on the substantive review.

After approval, code advances local finalize/export/integration. The explicit
workflow release --execute --merge --wait command handles the recorded Git/PR/CI
and exact deployment verification under existing publication authorization. Waits
are code-owned and bounded; failures preserve one resumable checkpoint. No source
reacquisition or historical audit is part of deployment recovery.

publication_exceptions is incomplete. Its checked retry command reopens only the
current preserved semantic task with a substantively corrected answer; it does
not reset evidence or rejection accounting. Do not poll an unchanged checkpoint.

## Exceptions and continuity

Returned review_progress gives saved/remaining decisions, checkpointed reviews and
failed short answers from code. A checkpoint remains visible while another task
is returned. Do not infer zero unresolved work from a successful next step. A
documented official-source conflict alone is not incomplete review; retain both
statements without choosing control. Read complete cards, never truncated output.

The additional source counters total_sources, reviewed_sources,
machine_reused_sources and pending_sources partition the current filtered source
queue. Reviewed means a distinct source accepted in this run whose raw hash
matches a current reused item; remaining reused sources count as machine reuse.
Deduplicate IDs; obsolete/duplicate/opinion decisions do not inflate source counts.
Checkpoints are pending, never completed reviews. Opinion work stays separate.
Counts remain available after source/opinion review, including downstream stages.
When an authorized stopping point is reached, copy code-generated handoff_text:
five bullets, <=120 words, phase/completion status, exact counts, failures and log
location. Return it verbatim as the entire final response without an introduction
or postscript, unless the user requests detail. It is not a stop signal; the ordinary workflow continues through its
authorized downstream stages. Do not inspect directories or reconstruct counts.
User-requested detail overrides this default. Routine task views omit handoff text.

Same-text changed originals requiring raw review, unavailable extraction, evidence
beyond a bounded self-contained card, and explicit uncertainty remain pending.
They get source/observation-bound exception records, with exact cause and paths;
no no-change receipt is fabricated. Automatic review continues other ordinary
tasks. When only exceptions remain, return `review_exceptions`, complete:false,
and the maintenance actions. This is not a completed update and must not advance
report finalization/publication or the default reporting baseline.

On later queue advances, reuse an unresolved checkpoint only for its exact
packet. Read checkpoint events once per locked inspection, with a fresh progress
readback and a fresh snapshot on the next inspection. Verify its saved packet
projection; do not rebuild its evidence card
or rewrite the same exception on every unrelated review. This is pending-state
reuse, never an accepted review or a no-change verdict. A different packet takes
the ordinary preparation path. Explicit maintenance and corrected answers still
prepare and validate acquired evidence before resolving the checkpoint.

Defer publication coverage/mapping reuse until the queue has no available source
or opinion review tasks. Unresolved review checkpoints still own that review
stage. At the publication boundary, run the existing coverage and mapping reuse
validators in their established order before choosing a publication task. This
avoids repeating downstream evidence joins during every unrelated review; it
does not skip source checks, accept an exception or advance the reporting baseline.

Record rejected short answers and exact validator errors. Identical request replay
reuses its durable outcome and does not count as a new failure. After two distinct
rejected answers for one current packet, checkpoint it as unresolved and advance to other
ordinary work; do not require a model-authored repair-note schema. A genuinely
corrected answer may pass the unchanged validators later. A saved submission
followed by failed advancement must remain replayable without duplicate findings.
Read-only status cannot create failure records or new review checkpoints.
Personnel-field errors identify the person and fields.<name>, retain the actual
reason and instruct a repair of that field while preserving other supported fields.
Use the card/error rather than code inspection or diagnostic scripts. Validation
does not mutate the submitted answer or silently delete contacts.

## Acceptance tests

Use synthetic/acquired frozen evidence in disposable databases. No production
writes, retrieval or historical-report audit. Verify:

- Changed name/date/contact: short answer becomes typed person, exact acquired
  citations, distinct successor, deduplicated field/top-level citations and real
  directory projection; no career/current-role confusion introduced by code.
- Existing person: all unmentioned nested facts and expected version preserved;
  stale version and successor-as-rename rejected.
- Material rule/source finding and no-material widget change: explicit model
  decision retained, changed-line support complete, no invented verdict.
- Unknown raw/script or nontext change: persisted exception, ordinary task still
  reachable, no completed review or finalization; repeated status idempotent.
- Missing/malformed evidence, extra/unknown answer fields, quote whitespace and
  NBSP: exact code copying, tampered cards refused, originals never rewritten.
- Opinion/status: normal relevant/nonrelevant summaries go through the existing
  opinion validator; uncertainty cannot complete an opinion review.
- Interrupted commit/advance, exact replay, invalid-answer accounting/recovery,
  installed launcher/helper outside the repository and old accepted receipts.
- Main skill, AGENTS, current specs/plans/test instructions describe this route.
  Legacy raw receipts/fragment instructions are maintenance-only, not parallel
  mandatory reading. No new measured speed claim without a model pilot.
- Complete inline cards, stdin snapshots, run/packet/card handles, tamper/stale
  rejection, accepted/invalid idempotent replay, crash after domain acceptance,
  pointer recovery and concurrent replies under a separate transport lock.
- A supported phone plus malformed address names the address/person in the error;
  correcting only that field preserves both contacts through real source acceptance.
- Current source counts partition reviewed/reused/pending IDs even with duplicate,
  obsolete and opinion decisions; a review also in reused items is counted once.
