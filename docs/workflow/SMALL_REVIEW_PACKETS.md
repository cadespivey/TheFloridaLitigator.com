# Routine short-review operator guide

Current live-comparison corrections: execute the returned checked helper command,
not the underlying raw workflow answer CLI. At an authorized stopping point copy
returned handoff_text; it is not a stop signal and does not replace downstream
approval/publication. Do not inspect task/log directories or reconstruct counts.
Opinion cards include the complete short guidance: general civil/appellate matters
remain in scope without a novel-rule requirement; complete bare PCAs need no
underlying-case research; missing evidence stays pending. Do not infer publication
status, drop express legal exceptions or add source bookkeeping to summaries.


This implements [SHORT_REVIEW_SPEC.md](SHORT_REVIEW_SPEC.md). Normal source/opinion
review has one evidence view and a short answer. The old v7 fragment/receipt
interface remains explicit maintenance compatibility, not routine required reading.

## Normal sequence

1. On entry/resume, use installed review_step.py next once, even if a saved
   pointer exists. It refreshes old-format views without reacquisition. Read the returned
   review_card only. It contains the question, acquired before/after passages,
   short evidence IDs, any prior-person references and the answer form.
2. Read the complete inline card object. Supply only its semantic answer form and
   supplied evidence IDs; do not author hashes, timestamps, full citations, stable
   IDs or versions. Do not open a separate card or write an answer file.
3. Send JSON on stdin to the exact returned run-local `review HANDLE` command.
   The checked helper saves original answer bytes, validates, persists and returns
   the next complete inline card in one action. Handles bind the run/card/packet;
   they are not paths to reconstruct. Old file-based answer is compatibility-only.

4. Use the returned next state after success. Code compiles the answer through the
   existing source/opinion validator and persists the result. A saved submission
   followed by failed advancement is recovered with next or the identical answer.
   Never reset/reacquire to repair a review.

Source form: decision, summary, evidence, people. Decision is material_change,
no_material_change or insufficient_evidence. Explain the actual material change
and practical effect, or a short supported no-material reason. Evidence is an
array of supplied IDs. People is empty unless named personnel facts changed.
A changed person supplies person (existing reference or new), name, kind
(judge/clerk), evidence, and fields mapping each supported label to value/evidence.
Code preserves untouched facts and expected versions and copies field citations
into the complete finding automatically. No automatic predecessor removal.
For a new person include contacts explicitly supported by the current passages,
even when unchanged on the page. Preserve factual text and useful address line breaks; code tolerates formatting whitespace in supported contact fields only. Quotes, URLs/emails, digits and punctuation remain exact.
Do not invent absent contacts or transfer predecessor personal contacts.

Opinion form: relevance, summary, holding, disposition, authors, evidence.
Relevance is relevant, not_relevant or uncertain. Relevant opinions need the actual
holding/disposition and opinion support; status notices require their own support.
Authors are names only. A former role or selection date is not a current assignment
or effective service date. Reviewer is optional if the actual model is exposed;
otherwise code records identity unavailable. Do not inspect runtime files for it.

Observed link changes appear on the same card when relevant inventories differ;
code compares them. They do not prove that a linked document was reviewed or that
a target URL works. URL-valued fields must match the acquired current inventory.

## Failure and unknown evidence

Code preserves raw originals, source URLs/times, exact Unicode quotations,
optimistic versions and accepted history. Unknown evidence IDs, unsupported values,
malformed answers and stale packets fail closed. Correct only the short answer
from the exact saved error. After two rejected answers code records an unresolved
checkpoint and continues other ordinary work; no model repair-note schema is needed.
A genuine corrected answer can pass later. Full failure accounting stays in logs
and database events; the model is not asked to diagnose technical causes.
Field errors name the person and fields.<name>. Repair that field using the card;
retain other supported contacts. Do not drop the whole collection or inspect code,
raw packets or write diagnostic scripts to repair an answer.

Changed originals needing raw/nontext inspection, missing/oversized acquired text
and uncertainty remain pending. No evidence is silently truncated or certified
harmless. The model does not inspect 13 frontend script groups to answer a legal
question. At review_exceptions, ordinary reviews are exhausted; preserve/report
that checkpoint without polling or claiming a complete update. It blocks report
finalization/publication and default-baseline advancement until appropriately resolved.

Default final response: at most 120 words/five bullets unless asked for detail.
Use returned total_sources/reviewed_sources/machine_reused_sources/pending_sources,
actual phase/delivery, failures, separate remaining opinion work and one log or
next-step link. Link the exception list rather than reproducing it. Do not count
checkpoints as completed reviews or reconstruct totals from saved files.

## Explicit maintenance and downstream approval

The returned workflow maintenance-task command exposes the compatible legacy
v7 guide/template for a separate technical/extended review. Existing packet,
receipt, fragment, raw-group validation and quote-selection functions remain
available to that reviewer. They do not become normal model reading because an
optional comparison file exists. See REVIEW_INTEGRITY.md for predecessor-bound
corrections and full submit/revise repair notes. Other publication/directory
approval phases retain their returned contracts. Never edit historical reports.

## Exact quotes

Explicit maintenance only: the returned v7 guide can be used with the pinned
launcher and this read-only selection command:

    flwu workflow quote --run-dir RUN --guide LEGACY_GUIDE --side current --start-line N --end-line M

Line bounds are inclusive and 1-based. Alternatively use --start-char N and
--end-char M (0-based, end-exclusive). Copy the returned support/citation object
mechanically in the maintenance receipt. This selection is not a review, and
normal short-answer models use evidence IDs instead of this command.

## Validation

Run tests/test_compact_review.py and tests/test_review_step.py, plus the source,
opinion, coordinator, integrity, recovery and installation regressions. Test actual
CLI/helper behavior, not just strings in guidance. Isolated fixture or frozen-byte
checks do not establish live source completeness or model speed improvements.
