# Florida Law Weekly Update v.1.1.0

Status: consolidated proposal for implementation approval. This package authorizes
no production migration, update run, inference change, or new publication. The
user requested the planning documents; implementation awaits approval of the plan.

The revision should reduce elapsed time per correctly accepted review and the
number of interventions needed to keep an agent on task. Preserve the existing
Python/SQLite architecture, evidence history, repository organization, public data
contracts, and website appearance and behavior.

The preferred sequence is collection and database organization, compact substantive
review, automatic projection, **one prepublication verification campaign**, and a
resumable release of that verified artifact. Reuse successful work at each boundary.
One campaign can contain several bounded cards; it is not a demand to fit an
entire statewide publication into one model context. A demonstrated defect receives
a targeted repair and delta check, not a restart of the campaign.

## Read in this order

1. [Architecture and evidence](ARCHITECTURE_AND_EVIDENCE.md): findings, limitations,
   existing integration points, and the proposals selected or deferred.
2. [Specification](SPECIFICATION.md): required behavior and invariants.
3. [Implementation plan](IMPLEMENTATION_PLAN.md): staged work, dependencies,
   approval checkpoints, and rollout.
4. [Test plan](TEST_PLAN.md): defect detection, recovery, performance, scope,
   model capability, and unchanged website behavior.
5. [Operator and skill rollout](OPERATOR_AND_SKILL_ROLLOUT.md): implementation
   handoff, profile consistency, compatibility, and operator instructions.
6. [Candidate skill](skill-draft/SKILL.md): proposed model-facing instructions.
   This draft is not installed and must not be used to assume unimplemented commands.
7. [Planning validation](PLANNING_VALIDATION.md): checks actually performed and
   the distinction between this package and future implementation evidence.

## Boundaries

- Improve the existing modules in place. No replacement workflow engine, database,
  frontend, repository restructuring, service deployment, or general agent framework.
- Keep full source acquisition and organization early; avoid model-authored receipt,
  identifier, citation, hash, or queue bookkeeping.
- Review substantive meaning once during drafting and verify the assembled output
  once before publication. Do not add independent serial approvals at mapping,
  directory, roster, preview, finalization, export, and deployment.
- Preserve cheap input integrity, concurrency, credential, and delivery checks.
  They establish valid persistence and artifact identity, not new legal review.
- Unavailable sources remain unavailable. A bounded, finalized update may retain
  disclosed coverage gaps; do not turn them into no-change findings or require
  exhaustive reacquisition to finish.
- Keep the current website layout, wording conventions, navigation, search,
  filtering, directory display, historical views, and public schemas unchanged.
- Published-content defects identified by the later independent assessment are
  regression leads. This planning assignment does not reopen or repair that update.

## Proposed success criteria

No invented evidence, premature acceptance, lost answers, duplicated findings,
unapproved scope expansion, changed public rendering, or weaker publication gate.
Unchanged verified items require no additional semantic approval. Scope reminders
reduce unnecessary actions without creating extra model turns. Performance gains
must be measured against an equivalent workload and the optimized sequential path.
Optional overlap ships only if it earns its complexity under the test plan.

## Current delivery

These are planning artifacts only. No runtime code, website data, active run,
installed skill, or inference configuration is changed. The profile paths were
inspected: codex-local, codex-cloud, and codex-personal resolve their Florida update
skill to the same canonical installation. The rollout document defines how to
update and verify all three together when the implemented protocol is ready.
