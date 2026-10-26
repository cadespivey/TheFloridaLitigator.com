# Production-sized local trial — interim findings

This trial is ongoing, not an end-to-end pass. The selected worker is
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

## Outstanding evaluation

At this checkpoint there are no accepted receipts and no final worker response.
Completion, legal accuracy across the queue, practical context consumption,
directory refresh, visual acceptance and end-to-end preview reliability are
unproven. Do not assign a passing overall grade based on acquisition or unit
tests. Record subsequent accepted decisions, failures, repairs, final status and
observable usage before closing this trial.
