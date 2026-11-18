# Implementation plan

This plan is ready for user review. Approval of this plan authorizes its bounded
implementation stages; it does not authorize production publication, inference
reconfiguration, or local-model execution beyond permissions already given.
Do not request repeated approval for routine work within the approved plan.
Obtain approval for material deviations, architecture changes, broader audits,
or deployment outside existing authorization.

## Entry and ownership

Work in the owning checkout and its existing module/test layout. Re-read current
AGENTS.md, inspect Git status and active run/process ownership, and preserve all
unrelated edits. Do not interrupt an active update to profile it. Prefer disposable
fixtures and narrowly extracted saved evidence; never copy the large production
database. Keep implementation evidence under this subproject's `evidence/` when
generated; do not create placeholder evidence or results now.

The planning snapshot was HEAD `a39e2c60d824601fbefe1d84bca92c5f12c1966e` on
November 17, 2026. That is provenance, not a pin requiring restoration. Integrate
with the then-current approved code without discarding subsequent work.

## Work sequence

| Stage | Work and owning components | Exit evidence |
| --- | --- | --- |
| 0. Measure and map | Instrument existing transport, short answers, workflow, acquisition and publication stages; classify reads versus mutations; inventory actual dependencies and harness waiting support | Task-bound profile, side-effect/dependency map, baseline fixture workload and assumptions |
| 1. Keep the agent on task | Add current scope capsule and coalesced reminders through transport; provide concise resume projection and unchanged-state waiting | Scope/restart tests, no extra acknowledgment/tool turns, exact closed-work reuse |
| 2. Simplify sequential work | Remove repeated preparation/refresh within a transition; reuse immutable extraction/cards; keep relevant freshness checks; batch projection rehearsal | Sequential accepted outputs equivalent, invalidation tests, measured optimized baseline |
| 3. Consolidate verification | Assemble candidate, one campaign with per-item verification/reuse, targeted correction invalidation and one aggregate acceptance | Complete/partial campaign recovery, named semantic regressions, no duplicate whole-update review |
| 4. Simplify release | Reuse verified bundle through finalize/export/integrate; durable executor checkpoints; reuse applicable code CI/build proof; retry failed delivery step only | End-to-end mocked release, exact artifact/merge proof, failure recovery, unchanged website behavior |
| 5. Evaluate overlap | Only if residual profile warrants it: versioned reservations, durable submissions, one validator/writer and bounded preparation for independent opinions | Recovery/concurrency tests and comparative benchmark against Stage 2, not only the original slow path |
| 6. Release protocol and instructions together | Update existing AGENTS/specs/helper guidance, promote candidate skill, synchronize installation, run compatibility/model trials when authorized | Final diff, applicable regression results, profile skill hashes/launcher checks, operator handoff and rollback proof |

Stages 1–4 are the primary revision. Stage 5 may be omitted with evidence that the
optimized sequential path makes overlap uneconomic. Completing v1.1.0 does not
require adding concurrency merely because this plan contains its design.

## Stage 0 decisions

Report median/p95 time per accepted review with sample size, stage breakdowns,
lock time, cache hits, model idle time and storage effects. Distinguish validation
from advancement and card preparation. Measure both actual elapsed time and
repeated call counts. Do not sum nested timings or treat replay without inference
as a live-model benchmark.

Identify the existing domain/coordinator persistence boundary and exact recovery
behavior before modifying submission. Confirm what can safely run outside write
transactions. Map opinion identity, consolidated groups, status and prior findings;
write the dependency matrix used for invalidation. Identify current CI paths and
build metadata before proposing artifact reuse. Record the selected foreground or
long-poll integration; no unsupported promise of pushing into an idle conversation.

If these findings materially contradict the specification, present the concrete
conflict and smallest alternative for approval. Ordinary choices among helpers,
cache structures and test fixtures remain within this plan.

## Implementation constraints

- Add behavior in the existing owning modules; preserve database fundamentals and
  public serialization/rendering. Avoid a universal abstraction for this one workflow.
- Prefer additive/versioned internal events over schema migrations. If the existing
  store cannot safely represent required states, stop for a concrete design review.
- Scope capsule and counters are derived from authoritative state. No model-written
  progress arithmetic, fabricated completed reviews, or parallel source-of-truth file.
- Batch fixes by demonstrated mechanism. Run relevant tests after edits and one
  full suite on the completed code candidate; broaden testing when failures or
  changed dependencies justify it. Do not release a separate PR per routine card.
- An optimization may reuse a proven validator result; it may not redefine invalid
  evidence as valid to avoid latency. Preserve actual exceptions and warnings.
- Preserve optional identity waivers exactly as authorized. Do not silently verify,
  broaden, or revoke them. Machine checks still detect supported duplicate candidates.
- The current content defects are fixture leads, not an assignment to repair the
  live November report as part of implementing infrastructure.

## Performance decision gate

Use the proposed experiment in TEST_PLAN.md. Seek at least a 20% reduction in
median Python overhead on the representative sequential workload, with no more
than 10% p95 regression. These are proposed engineering targets, not measured
outcomes. If safe simplification delivers less, report that result; do not weaken
checks or expand scope to manufacture the target.

Ship optional overlap enabled only when it improves median end-to-end time per
correctly accepted review by at least 10% versus the optimized sequential path,
with no more than 10% p95 regression, no correctness failures, and no memory/disk
pressure that makes the selected local-model configuration less stable. Otherwise
retain sequential default and document the experiment. Do not tune inference or
relax semantics to pass this gate. Resource budgets must be set from the Stage 0
baseline before the comparison, including a fixed cap on speculative artifact bytes.

## Rollout and rollback

1. Complete disposable-fixture implementation and failure injection. No production
   acquisition, acceptance, or deployment is needed to develop the protocol.
2. Run offline selected-evidence replay with the same input/evidence policy. Confirm
   outputs and coverage states, including failures, before using any live run.
3. Run authorized model-behavior trials with cloud and available selected local
   configurations. Follow the runtime README for any requested local execution.
   Missing model trials remain a stated support limitation, not a claimed pass.
4. Stage a preview run under explicit run ownership. Existing active runs stay on
   their old protocol unless explicitly upgraded at a quiescent checkpoint. Do not
   terminate a live validator to make an upgrade possible.
5. Promote code and skill together after applicable checks and approval. Keep one
   release/PR for coherent related changes unless an actual dependency requires split.
6. If reverting, stop new speculative issuance; reconcile in-flight ownership and
   drain or retain submitted answers. Resume sequentially from durable state using
   a compatible reader. Never delete submissions, rewrite accepted history, or roll
   back the public site as an implicit side effect of disabling the pipeline.

## Final implementation deliverables

Architecture/dependency map; measured baseline and stage profile; code diff within
the existing modules; regression/recovery results; comparative performance report;
one-pass verification and release evidence; website compatibility results; installed
skill/profile checks; concise operator instructions; deviations and unresolved limits.
Update this subproject with actual evidence links. Do not label any result verified
until its output has been read. The current planning package supplies none of those
future execution results.
