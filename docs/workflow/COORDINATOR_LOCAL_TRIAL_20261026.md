# Production-sized local trial — interim findings

This trial is incomplete, not an end-to-end pass. The selected worker is
Qwen3.8-27B-8bit, as established by launcher preflight. Its occasional self-label
as a cloud Codex agent is incorrect. The parent owns the persistent goal because
the noninteractive worker reported that goal tools require a persistent thread.

## Isolation and acquisition

The trial uses a consistent SQLite backup of the production research database,
the existing 769-source weekly registry, 67 county supplements and one court
supplement. It covers October 19–25, 2026 in preview mode. Production writes,
finalization, publication, code edits, package installation and model-server
restarts are outside the worker assignment. Registry size is not proof that all
possible statewide sources are covered.

Private original evidence is retained under
`runs/local-model-validation-20261026/`: `assignment.json`, `worker.jsonl`,
`worker.stderr`, `research-copy.sqlite` and `run/`. These ignored files must not
be committed. The copied database and acquisition are reused for continuation;
do not restart acquisition merely because a review fails.

Acquisition completed after approximately 63 minutes. The generated queue records
373 source tasks (367 changed and six retrieval failures) and 53 opinion tasks
(51 new/unreviewed candidates and two download failures). It reused 408 source
reviews and 1,322 opinion reviews. Independent court discovery produced 1,307
listing identities; tracked documents expanded acquisition to 2,156 sources.
`acquisition_complete: false` preserves the coverage failures. The worker
correctly continued to review instead of treating acquisition as completion.

## Observed instruction and implementation issues

- Setup guessed a nonexistent supplement directory and treated the registry
  object as a list. Current skill instructions now identify actual paths and
  the `sources` key.
- Model identity was inferred from the client name. Current instructions require
  launcher/preflight evidence or an explicit unknown identity.
- Queue export repeatedly scanned all latest findings for each source. The
  implementation now indexes latest findings by URL once per export. Existing
  acquisition was left running; the improvement was tested separately.
- The first review deliberated about invented outcome names before reading the
  full output contract. Task schemas now enumerate supported outcomes and direct
  reviewers to copy the receipt template before editing.
- The first draft used a parenthetical explanation as a purported previous-text
  quotation. It is not accepted evidence. Domain validation and independent
  review must verify exact quotes; a draft is not a saved, valid review.
- The supervising agent changed the task contract while the first packet was
  pending. Because the contract contributes to the packet hash, submission was
  rejected as stale before content validation. This is an operator-caused trial
  interruption, not evidence that the model modified the packet or that quotation
  validation ran. The worker correctly requested a new packet. Leave executable
  workflow code unchanged for the remainder of this running trial; apply further
  runtime changes after the worker reaches a terminal checkpoint.
- Independent inspection of the first source's saved texts confirms that the
  ACIS announcement, court-history paragraph and two operating links appear once
  in the previous text and twice in the current text. Thus the apparent additions
  include duplicated existing content; this supports considering no practical
  change, but does not excuse fabricated quotations or incomplete changed-line
  support. The regenerated packet is 283,289 bytes, including 17 prior findings,
  while the current extracted page is only 13,941 characters. This exposes a
  context-efficiency issue: evaluate moving verbose prior findings into linked,
  individually addressable evidence files with a compact index after the trial
  reaches a terminal checkpoint. Do not discard prior facts or change the running
  worker's packet contract to achieve that reduction.
- After requesting the fresh packet, the worker submitted its draft and received
  `Workflow error: Review support quote absent from acquired extraction`. This
  is direct live evidence that source-bound quotation validation rejected the
  unsupported draft. The worker then stated it would reread the extraction and
  correct the quotation. Acceptance and adequate changed-line coverage remain
  unproven; the rejection alone is not an end-to-end pass.
- The corrected submission reached the changed-line gate and was rejected with
  `No-change support must cover every changed text line on both sides; unchanged
  headings are insufficient`. The live validator therefore prevented a narrow
  quotation from standing in for review of the full change set. The model still
  needs to supply complete support and reasoning; do not relax this requirement
  to turn the trial green.

## Outstanding evaluation

An intermediate log measurement counted 113 completed shell commands returning
123,520 characters in total, before the first accepted review. This includes
setup, acquisition monitoring and review; it is not a count of research tasks.
The event stream had no usage event at that checkpoint, so no token-consumption
claim is supported. The 283 KB packet's on-disk size is likewise not proof that
the model ingested the entire packet: its reads were bounded. Retain these
distinctions when evaluating context efficiency.

The supervisor stopped the first worker assignment with SIGINT to its verified
launcher after repeated first-task quotation/coverage problems. The launcher
forwarded the signal to its own child and exited (status 1). No server restart,
model unload, evidence deletion or reacquisition occurred. The worker produced no
final response. This is a supervised failed attempt, not an autonomous completion.

The next patch addresses the demonstrated mechanical burden: exact changed-line
quotes are prefilled by code, while outcome, interpretation and review attestations
remain required. A compact review guide links every full prior finding and retains
the full immutable packet for validation. Tests cover nonbreaking spaces, changed
line coverage, rejection of unreviewed templates, lossless finding files and
unmodified packet identity. Resume the same saved run with a bounded first-review
assignment, inspect its accepted evidence, then continue the remaining queue.

## Bounded continuation checkpoint

The revised first-review assignment accepted its receipt on the first submission.
Coordinator capture `93e39cf9a6fa34d98a11866c7b441ec2ee5bed50d10329dbb1603b9638e20902`
and domain capture `03951415e11a5aaeb23e98b122eadcb878dbfbea1d0ea505388fa1b90072efc1`
are persisted in the isolated database. Independent inspection verified all 13
current and two previous quotes, complete changed-line coverage, and that every
added substantive line already occurred in the previous extraction. The removed
lines are empty heading markers. The no-relevant-change conclusion is supported.
The reviewer correctly identifies Qwen3.8-27B-8bit. This validates this correction,
not the entire source queue or unattended model reliability.

The continuation still made an unnecessary detour into earlier logs and a failed
shell separator (`==RESUME===`). Its client also warned that unsupported priority
service tier would be omitted; inference continued. The next assignment directs
the worker to authoritative current task output rather than old logs and retains
the two-repair-attempt limit. No runtime code changed during this continuation.

At this checkpoint one receipt is accepted.
The bounded worker exited successfully. Its final report incorrectly claimed
there were no prior findings: the guide indexed 17. No findings were replaced by
its no-change receipt. A separate supervisor correction preserves the original
report and explains the error; subsequent instructions explicitly identify the
index. Reported cumulative usage was 752,128 input tokens (715,234 cached) and
11,420 output tokens, including 4,593 reasoning output tokens. These are aggregate
request counts, not peak context occupancy. The original failed attempt had no
terminal usage event, so a complete before/after token comparison is unavailable.

## Original-byte review failure and correction

The full continuation accepted two further reviews, independently checked against
their saved evidence: cosmetic labels on the 1DCA judges page and two case-specific
confidentiality entries on the clerk page. Private supervisor review receipts are
saved in the trial directory. Its next receipt, for the Clerk of the Court page,
was structurally accepted but failed independent review: the worker read only the
page title and empty text diff, then asserted that the original-byte change was
harmless metadata/CSS/JS. No original-byte inspection supported that assertion.

The supervisor stopped that assignment through its verified launcher's SIGINT
handler (exit 1), preserving all evidence and receipts. Three reviews remain
independently supported; the fourth requires correction. The original files reveal
an update timestamp plus changes in embedded HTML fields, including date-bearing
menu data. Identical extracted text did not establish what changed.

The source gate now requires an original-content comparison review for changed
bytes with identical extraction. HTML comparison includes attributes and embedded
JSON; binary spans explicitly require original-document inspection. The receipt
must bind the comparison and explain every change. Older same-text approvals
without this evidence remain in history but are not reused. The actual trial's
next-task command now returns the deficient source for a new review, preserving
the three supported reviews. All 780 tests pass, including rejection of title-only
support, missing change explanations, stale comparison bindings and unsafe reuse.
This remains structural validation, not proof that a model's interpretation is
correct; independent review is still required for trial acceptance.
Completion, legal accuracy across the queue, practical context consumption,
directory refresh, visual acceptance and end-to-end preview reliability are
unproven. Do not assign a passing overall grade based on acquisition or unit
tests. Record subsequent accepted decisions, failures, repairs, final status and
observable usage before closing this trial.


## Corrected original-content review checkpoint

The bounded raw-comparison retry exited 0 and accepted the corrected fourth source
on its first submission. Independent inspection verified all three original
changes: timestamp, embedded opinion-menu date fields, and unchanged headshot
paths on a different media host. Coordinator capture
`837f62af76e4c52b0de02d3f2b01682de0f9d9d88216ef27da52d854ecd61912`
and domain capture
`3665902ef55b1d11a065ceb80ab4ca53e56832ebe539ae250bfed728a19a6854`
were read back from the isolated database. The reviewer label correctly names
Qwen3.8-27B-8bit. No findings were replaced. The supported conclusion concerns
clerk contacts and operating requirements; it does not establish no new opinions.
The receipt's broad phrase “all page content unchanged” is qualified by its own
explicit sidebar-change explanation. “CDN migration” describes the observed host
change, not independently verified deployment causation.

The worker unnecessarily investigated a stale RESUME.md that still said to init
and misidentified the original worker as cloud. Its original note is preserved;
the current note is corrected. The skill/runbook now explicitly make the
initialized coordinator's database-backed next-task result authoritative over
handwritten checklists. No runtime inputs changed during this bounded retry.
Observed cumulative usage: 632,878 input tokens, 579,722 cached input tokens,
8,523 output tokens including 3,018 reasoning output tokens. These cumulative
request counts are not peak context occupancy or a complete full-trial metric.
Four source reviews are independently supported; the full preview is incomplete.


## Current continuation — October 27

This checkpoint supersedes earlier counts and interpretations above. The full
preview remains incomplete. Forty unique current source decisions have
independently supported conclusions and matching domain/coordinator persistence.
Twenty-nine required append-only supervisor corrections to remove unsupported
timestamp causes, rendering/resource-equivalence claims or an incorrect roster
count. Original receipts, source bindings, quotations, outcomes and findings were
preserved. These are corrections to the current trial, not historical reports.

A later continuation produced three clean reviews using decoded comparison
evidence, then created another automatic no-change helper based on paths and
partial values. The supervisor stopped that assignment before its next receipt.
The helper and logs remain private evidence; do not execute it. Identical text or
familiar paths cannot determine the significance of changed original bytes.

The continuation process now uses one fresh `codex-local-worker code` assignment
per coordinator task, with the selected Qwen3.8-27B-8bit model. The parent owns the
persistent goal, waits for terminal completion, independently reviews the exact
evidence and saved decision, and only then obtains the next task. The assignment
allows the task receipt and coordinator database writes, prohibits classifiers
and new acquisition, and returns a capture ID or an exact unresolved error.
This changes supervision granularity, not the trial's production-sized scope.
No inference server was restarted or model unloaded.

The first such assignment, Judge Morris Silberman, completed successfully: nine
commands, no command failures, first-submit acceptance and no supervisor receipt
correction. Independent review reproduced the original comparison and checked
all changed values, identical extracted bytes and both saved database records.
Reported cumulative usage was 291,159 input tokens (256,515 cached) and 5,531 output
tokens, including 1,847 reasoning output tokens. These aggregate request counts
are not peak context occupancy; the worker JSONL provides no direct peak-context
measurement.

Khouzam subsequently passed independent review without a receipt correction.
Northcutt covered all six changes, but still asserted unverified CMS-save timing,
migration causes and destination equivalence, and skipped the requested original
comparison cross-check. A supervisor correction preserved the original decision,
source bindings, quotations, outcome and findings. Fresh one-task context therefore
has not eliminated instruction-adherence failures. The next assignment, Labrit,
explicitly requires both original and decoded comparisons and observed-value
explanations without inferred technical causes.

During the Northcutt correction the supervisor supplied a capture ID in place of
the decision digest; the predecessor guard rejected it before mutation. The
correction succeeded using `workflow decision` output. The runbook now explicitly
distinguishes these identifiers; this was an operator error, not a worker failure.

Private artifacts include `silberman-bounded-evaluation.json`, the bounded worker
logs, correction readbacks and `supervisor-reviews.jsonl`. They remain ignored.
The final evaluation still requires the remaining source/opinion review, report
and directory assembly, editorial/visual checks and preview completion. PR #109
remains draft; passing build/credential checks and skipped deployment do not prove
publication. Refresh the maintained installed checkout after merge and verify
current deployment without rechecking historical reports.

## Linked evidence guide checkpoint

Labrit still required a supervisor correction for an unsupported timestamp cause,
despite reading both original and decoded comparisons. Fresh context and explicit
instructions have reduced some mechanical errors but do not establish unattended
semantic reliability.

The Third DCA judges-page task subsequently completed without a receipt correction.
Its changed text supported updating the existing as-of-label discrepancy finding,
not announcing a new appointment. Independent inspection verified all 14 changed-line
quotes, current citation bindings, the new persisted finding version, and preservation
of the prior version. Thirty-six of the 37 supported source decisions are no-change
reviews; one updates a finding. These counts include the 27 corrected decisions.

That worker unnecessarily dumped every prior finding, producing 353,911 characters
in one command. Reported cumulative usage was 947,926 input tokens (894,236 cached)
and 22,081 output tokens, including 13,787 reasoning tokens. These are aggregate
request counts, not peak context. Complete logged output does not establish what
the model actually saw after tool-output truncation.

Commit `19b7d2a` introduces `review-overview-v1.json`: the entry guide links the exact
receipt template and changed-line evidence instead of embedding duplicate copies.
It directs the reviewer to inspect one needed prior finding at a time and recover
truncated output. Immutable packets and the legacy full guide remain unchanged.
The roster task's guide shrank from 40,813 to 20,140 bytes; an empty-text-diff task
grew by 111 bytes. This is a file-size measurement, not demonstrated context savings.
The full suite passed 791 tests in 21.39 seconds. The first live task using the
new entry guide is the Third DCA clerk-office review; its result remains pending
at this checkpoint. No running worker's task contract was changed.

## First linked-guide result and retrieval diagnostics

The Third DCA clerk-office review completed successfully on its first submission
with eight commands and no command failures. Independent review reproduced the
original and decoded comparisons, confirmed identical extracted bytes, and checked
both persisted records. The only change was the `og:updated_time` value; the receipt
did not invent a cause. No correction was required. This brings the independently
verified total to 38 (37 no-change decisions and one updated finding), including
27 supervisor-corrected decisions. The worker reported 282,914 cumulative input
tokens (261,293 cached) and 5,852 output tokens, including 3,010 reasoning tokens.
This simpler task does not establish an apples-to-apples context improvement.

Inspection of saved failure evidence identified four HTTP errors (three 403s and
one 404) and two responses rejected by the PDF-signature gate. Those two URLs end
in `.pdf` but returned HTTP 200, a Word-document content type, and valid ZIP
packages containing `[Content_Types].xml` and `word/document.xml`. Package structure
was verified from the saved database bytes; document contents were not reviewed.
The current retrieval gate rejects these format mismatches, and extraction does
not support DOCX. Do not relabel them successful, attach an extraction to a failed
observation, or infer that their contents are unchanged. Preserve the explicit
failure in this trial. A future format-recovery enhancement must validate the
actual format and record a new observation without overwriting original evidence;
HTML error/login pages at PDF endpoints must remain rejected.

Two Third DCA opinion downloads are also unavailable in the saved queue (case
numbers 2024-2322 and 2025-2523). Their listing metadata is not a substitute for
reviewing the opinions. Source-specific details are saved privately in
`retrieval-failure-diagnostics.json`. No reacquisition, production writes or
historical-report checks were performed for these diagnostics. The trial and
release remain incomplete.

## Original-comparison aid for changed-text tasks

The next clerk-profile review required correction of an unsupported CMS-generation
claim. Bokor's subsequent profile review correctly described the calendar changes
but incorrectly said the court address was unchanged in its captures. That address
was supported by a separate clerk-page citation and appeared in neither profile
capture. Append-only corrections preserve both original receipts, evidence bindings,
quotations, findings and supported no-change conclusions. The current total is 40
independently supported source decisions (39 no-change and one updated finding),
including 29 corrected decisions. The trial remains supervised and incomplete.

Bokor's worker recreated raw-byte and escaped-HTML comparisons because the task
provided only a text diff. One custom diff produced 179,649 characters; there were
22 commands and three nonzero command exits. Its reported cumulative usage was
1,393,627 input tokens (1,316,483 cached) and 23,681 output tokens, including 10,017
reasoning tokens. These are aggregate request counts, not peak context. The worker
completed on its first receipt submission, but that does not erase helper failures
or the source-attribution correction.

The tested patch now supplies existing original and decoded comparisons as an
inspection aid when extracted text changes. It does not change acceptance or reuse
policy, select relevance, or require an extra receipt field. Mandatory original
review remains mandatory where the existing template requires it. On Bokor's saved
files the structured comparison has two changes, 15,583 bytes of original output
and 22,093 bytes of decoded output, with no decoding-limit paths. This demonstrates
a smaller comparison artifact, not actual model context savings. Ten focused tests
and all 795 tests passed (full suite: 21.16 seconds). The patch was integrated only
after the worker exited and its corrected decision was verified. No reacquisition
or production writes occurred.

Next assignments explicitly prohibit rebuilding byte-diff and quote-containment
helpers when supplied comparisons and coordinator validation already cover those
mechanics. They also distinguish prior facts citing other sources from facts
verified by the task's own captures. Retaining a prior finding does not reverify
every source cited by that finding.
