# Architecture and evidence

This is a planning assessment, not a fresh production benchmark or source audit.
The inspected owning checkout is `/Users/cadespivey/Developer/FloridaLitigator/flwu-current`.
Read its current [AGENTS.md](../../AGENTS.md) again at implementation entry; preserve
any intervening changes. Current instructions govern execution until approved
v1.1.0 behavior and documentation are released together.

## Existing foundation to retain

| Component | Existing responsibility | Bounded revision target |
| --- | --- | --- |
| `src/flwu/history.py` | SQLite evidence and immutable history, publication transactions | Reuse event storage and transaction guarantees; no foundational schema replacement |
| `src/flwu/update.py`, source acquisition modules | Discovery, acquisition, reuse and incremental queue updates | Measure and eliminate repeated refreshes; preserve original bytes and status meaning |
| `src/flwu/compact_review.py` | Complete compact evidence cards and semantic-answer compilation | Reuse immutable preparation with explicit dependency bindings |
| `src/flwu/review_transport.py` | Issued handles, current-task checks, immutable input, serialized replies | Scope capsule, durable status distinctions; optional versioned reservation protocol |
| `src/flwu/workflow_short.py` | Compilation, error accounting, submission and recovery | Remove redundant preparation while preserving exact errors and authoritative acceptance |
| `src/flwu/workflow.py` | Workflow state, tasks, acceptance and coordination | Dependency-aware snapshots and one owner of advancement |
| `src/flwu/publication_driver.py` | Automatic mapping, roster handling, assembly and stage transitions | Batch projection rehearsal; consolidated verification and sequential publication barrier |
| `workflow_report.py`, `workflow_directory.py`, `workflow_release.py` | Report/directory artifacts, build, acceptance/export/integration | Reuse a verified immutable bundle through release; invalidate only affected dependencies |
| `publication_executor.py`, `workflow_deployment.py` | Git, CI, merge, deployment observation and live data checks | One durable release state machine; no repeated content review during polling/retry |
| `skills/florida-update/scripts/review_step.py` | Checked model interface and process/pointer recovery | One compatible interface, foreground wait and compact status |
| `skills/florida-update/`, installer, profile skill links | Shared operator instructions | Short common skill with task-specific references and synchronized deployment |

No new top-level code package, alternate database, queue service, or second routine
review interface is proposed. Additional internal helpers should have clear owners
in these existing modules. Any necessary additive history records must be compatible
with the existing schema/version policy; do not quietly introduce a database migration.

## What the saved evidence establishes

The November 15 records under
`/Users/cadespivey/Developer/LocalCodexSetup/evidence/mtp-comparison-20261115/`
report approximately 103 seconds per Python command and 112 seconds between
completed post-MTP reviews. The post-change sample contained eight completed
reviews, all bare per curiam affirmance screenings. Approximately 39 tokens/second
is aggregate server response throughput, not an isolated decode or legal-quality
benchmark. Prompt differences, a small sample, and a pre-change compaction limit
causal claims. Read `analysis-final.txt` and `assessment.json` for the actual data.

If about 103 seconds remains one serialized Python stage and model work takes
about nine seconds, ideal overlap saves only about eight percent of that cycle.
This is illustrative arithmetic, not a performance promise or a rigorous bound
derived from independent medians. Larger savings require less Python work or
measured separation of stages.

The saved `runs/updates/weekly-2026-11-08/PERFORMANCE_DIAGNOSIS.md` documents
implemented reuse and incremental repairs. Its older “not implemented” sections
are historical, superseded by later entries. Residual overhead is real; a claim
that no repair was implemented is incorrect. Prior profiles are leads for new
measurement, not current timings for every task type.

Current code inspection identifies repeated calls, without assigning their cost:

- `review_transport.model_state` invokes `w.inspect`, refreshes the queue, finds
  tasks, and prepares the card again before issuing its handle.
- `reply` holds its per-run reply lock across submission and next-state production;
  it inspects current state and checks tasks before calling `short.answer`.
- `workflow_short.answer` refreshes the queue and calls compact preparation and
  projection before compiling and submitting.
- `publication_driver.advance` repeatedly inspects and advances mechanical stages.
- `history.database` can initialize storage and sets SQLite pragmas. It is not a
  pure read-only accessor. Function names do not establish absence of side effects.

Do not remove these checks until their protected invariants have explicit owners.
No production command was run to advance a workflow during this planning review.

## Assessment of quality and scope

The previous continuation repeatedly exceeded the intended checking scope. User
nudges corrected it. A short, current scope capsule is therefore a higher-priority
intervention than a second supervising agent or broader audit.

The final November update was deployed with 57 news entries and 63 changed
directory files. Its artifact identity and delivery were verified. That evidence
does not establish legal correctness. The subsequent independent assessment at
`/Users/cadespivey/Developer/FloridaLitigator/completion-watcher/reports/attempt-001/assessment.md`
reports missing opinion qualifications and duplicate directory identities, while
confirming the earlier Multack and AO 26-20 corrections. These are named test leads;
an implementer must establish expected outcomes from bounded captured evidence
before treating them as regression oracles. Do not repeat its statewide review.

The audit's 980 change records are operations, not necessarily 980 distinct people.
Machine evidence bindings, individual semantic checks, supported reuse, and explicit
identity waivers must retain distinct meanings and counts.

## Decisions on the proposals

| Proposal | Decision and reason |
| --- | --- |
| Scope heartbeat | Adopt event-triggered reminders and a bounded task-count fallback in the existing conversation; no timer-driven agent or extra acknowledgment turn |
| Early collection and organization | Adopt. Store evidence, normalized extraction, identity/status relations and failure reasons before routine model review |
| Default reviewed-finding reuse | Adopt existing supported identity/evidence criteria; return only genuine conflicts or missing meaning to the model |
| Pre-loop projection rehearsal | Adopt as a non-mutating batch derivation over saved inputs; expose schema failures together |
| One prepublication verification | Adopt one resumable campaign with per-item reuse and targeted correction checks, followed by immutable-artifact release |
| Incremental advancement and immutable caches | Prioritize after stage profiling; keep dependency checks and existing validators |
| Bounded single-model overlap | Conditional second-stage optimization for independent opinion tasks only |
| Publish partial previews | Use the existing finalized, coverage-limited publication contract instead. Preview remains preview; false acquisition completeness is unnecessary |
| Verify every waived identity after publication | Reject as a default assignment. Honor the waiver; reopen only a named conflict or defect |
| Repeated independent audits and full-suite runs at every data stage | Reject. Retain one verification campaign and reuse applicable code/test/build proof |
| Runtime/model tuning | Outside this revision. Test selected models as configured; do not change MTP, context capacity, quantization or runtime guards |
| Website redesign or public-schema changes | Excluded by the user's instruction |

## Questions implementation must resolve

Measure actual stage time and side effects; identify the full dependency set for
opinion cards (including consolidated cases and status changes); verify the harness's
supported waiting/resume behavior; establish whether build inputs are deterministic
enough for artifact reuse; identify CI proof bindings that permit safe reuse across
data-only commits. Resolve these in the approval-ready stage profile, not by
guessing or installing a parallel system.
