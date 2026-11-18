# v1.1.0 specification

Proposed requirements. IDs link to the implementation and test plans. Existing
architecture and public behavior remain controlling constraints.

## R1 — Scope and progress

Maintain one concise current task capsule, derived from the run contract and saved
progress: objective, reporting window, authorized stages, current task/next action,
remaining deliverables, closed work with evidence pointers, explicit exclusions,
waivers, and stopping condition. Keep history append-only separately; the current
capsule must not accumulate superseded to-do lists. Proposed representation: a
versioned record in the existing workflow stream with an atomic run-local projection.
It is derived guidance, never a new source of acceptance authority.

Emit a reminder on resume/compaction when the harness exposes that event, phase
transition, attempted scope expansion, and repeated failure checkpoint. Use a
configurable fallback of 20 completed semantic tasks since the last reminder.
Coalesce triggers; show at most one short reminder with the next existing response.
No independent timer, model session, extra tool call, or required acknowledgment.
If compaction is not detectable, use normal resume and task-count triggers.

The reminder directs the next action: consult saved verification; identify the
deliverable and concrete reopening reason; reuse closed work; correct only defects;
obtain approval before material expansion; stop at verified completion. It must
not cause the model to repeat its plan, enumerate all sources, or reread all logs.
Persist reminder emission so a restart does not repeat it unnecessarily. Explicit
new user instructions update the scope; elapsed time does not provide approval.

## R2 — Collection and database organization

Use existing registry reconciliation, seven-court discovery, source acquisition,
hash reuse, baseline selection and extraction paths. At the start of a new run,
organize acquired originals, URLs, retrieval/status dates, normalized text and
components, prior evidence, court/person identifiers and coverage failures in the
existing database. Retain the full statutes corpus within the established scope.

Compute immutable extraction/indexing once per original and parser policy; apply
incremental updates only to affected dependencies. Store observable facts early:
retrieved, failed, missing body, extraction incomplete, changed, or proven reusable.
None of these automatically determines legal significance. A shared template,
hostname or unchanged title cannot certify no substantive change.

Use existing bounded network/retry policy. Recover an additional source only for
a specific material gap; exhausted failures receive an explicit disposition.
No global reacquisition on resume, speculative historical research, model-written
source classifiers, or endless retries. Discovery/status updates may invalidate
affected opinions even when document bytes match. Registration is not review.

## R3 — Compact substantive review and deterministic transfer

Keep the existing semantic-answer forms and code-owned receipts. A complete card
contains the actual task, relevant evidence, prior comparison when needed, short
references, scope/date distinctions, and only fields required for that task. Keep
hashes, receipts, broad workflow history and repeated quotations out of model prose.
Models must be able to access complete necessary evidence; do not silently truncate
or choose fragments that omit qualifications. Oversized evidence becomes an explicit
checkpoint using the existing supported evidence route, not a guessed answer.

Accept draft findings through the existing binding and domain validators. This is
original substantive review and integrity validation, not a separate independent
verification campaign. Code transfers accepted findings automatically using proven
stable identity or supported name-plus-official-URL matching. Name alone, title
normalization, matching county, or a similar contact is insufficient to merge people.
Return ambiguity, changed assignment, conflicting role, unsupported scope or missing
publication meaning as a bounded card. Preserve unchanged contacts and evidence.

Before serial mapping, rehearse all eligible projections against a consistent saved
snapshot without persisting acceptances. Collect structural/contract failures by
actual mechanism; correct related schema mismatches together. Do not infer legal
verdicts, silently remove people, or queue every row for another model approval.
Rehearsal output is disposable computation, not proof of substantive review.

## R4 — Efficient advancement

Instrument nested spans with run/task identity, monotonic duration, outcome and
cache behavior: history loading; refresh/selection; evidence/card construction;
binding/projection checks; compilation/domain checks; persistence; next-state
preparation; and lock acquisition/hold time. Separate inclusive and exclusive
times; never add overlapping spans. Avoid logging answer bodies or secrets.

Use one authoritative next-state calculation per successful transition. Reuse its
result in transport rather than reconstructing it. Cache immutable computations
by original/evidence version, extraction/policy/contract version and relevant prior
finding/status dependencies. Recheck mutable assumptions at issue and commit.
Unrelated accepted opinions should not invalidate every card through a global
progress number alone. Unknown dependency-changing events fail closed or fall back
to the existing safe full refresh. Correctness comparisons must prove equivalence.

## R5 — Optional bounded overlap

Introduce this only after profiling and sequential simplification, behind an
explicit option. Existing runs default to their existing protocol. Restrict the
initial implementation to ordinary opinion tasks with demonstrably independent
dependencies. Consolidated opinions or shared status/evidence are not presumed
independent. Personnel, corrections, withdrawals and all publication stages remain
sequential. No new model or inference process is authorized.

| Resource | Maximum |
| --- | ---: |
| Active model reviews | 1 |
| Active validators | 1 |
| Authoritative acceptance writers | 1 |
| Unaccepted tasks, including active review and validation | 2 |
| Additional complete prepared but unissued candidate | 1 |

Represent prepared, issued/reserved, submitted, validating, accepted, rejected,
unresolved and stale outcomes explicitly using versioned records in the existing
workflow storage. Durable submission stores original answer bytes and its exact
run/task/card/evidence/contract/dependency bindings before acknowledgment. An
acknowledgment states `saved; acceptance pending`; pending answers affect neither
accepted counts nor downstream publication inputs.

Use deterministic issue-order acceptance. If A validates while B is reviewed,
C may be prepared. If B finishes first, save B and stop model work until capacity
is available. Prioritize repair of A under the existing rejection policy; B remains
pending if independent. If A reaches an unresolved checkpoint, record that terminal
outcome before continuing B. No acceptance may pass a nonterminal predecessor.

Replace single-current-task assumptions with tested reservations, not removal of
locks. Include ownership/generation fencing and dependency versions so an expired
or superseded validator cannot commit. Expiry never discards a submitted answer
or proves the old validator stopped. Each background worker owns its connection.
Do expensive pure checks outside a write transaction where safe; acquire protection
and recheck dependencies at commit. Preserve the domain/coordinator recovery boundary.

On crash, reconcile durable states before issuing work. Exact replay recovers the
recorded result; altered accepted answers require the correction route. Retain
exact failures and existing distinct-rejection accounting. Stale submitted answers
remain evidence and cannot be silently rebound to a new card. Drain or preserve
pending work on opt-out; never reset it to empty. Stage transitions require no
issued or validating tasks and explicit outcomes for every submitted answer.

The existing checked interface owns waiting, preferably through one foreground
command or supported long poll. Do not assume a Python background task can inject
cards into an existing conversation. Investigate the actual harness before choosing
delivery mechanics. Provide one routine interface with a versioned compatibility
path, not a competing command family or generic scheduler.

## R6 — One prepublication verification campaign

Assemble a current update and directory delta from accepted findings. Freeze its
input manifest and complete candidate build before substantive verification. Include
exclusions/coverage dispositions, explicit waivers, affected identities, and known
defect leads. Apply existing credential redaction before freezing public artifacts.

Use one resumable campaign across this bounded candidate:

1. Machine checks establish schema validity, evidence bindings, faithful transfer,
   reporting-date treatment, supported scope, duplicate candidates, preserved fields,
   directory consistency, public credential safety, and build/render success.
2. Complete compact verification cards check final news meaning and changed-person
   decisions against their bound evidence. Preserve outcome qualifications, panel
   reasoning, status/rehearing distinctions, dates, and identity conflicts. Reuse
   substantive verification already performed on the identical item/evidence/policy;
   do not ask the model to repeat it. Unchanged roster members and copied contacts
   need integrity checks, not fresh individual source review.
3. One aggregate publication acceptance binds these results to the exact candidate.
   The aggregate action must not ask the model to reread all completed cards.

Record for each item whether individually verified, reused on a supported basis,
explicitly waived, excluded with reason, or unresolved. Hash checks never imply
legal truth. Do not use a five-row sample to claim every identity was verified.
Keep the review queue bounded to final content and concrete exceptions; no second
independent whole-update audit by default.

A named defect invalidates its item and actual dependents. Correct append-only,
rebuild affected derivations, and recheck that delta within the same campaign.
Reuse unaffected results. A code/policy change invalidates the results it can
actually affect; unknown impact blocks approval pending a bounded assessment.
The final aggregate manifest is refreshed mechanically without another full review.

Coverage-limited finalized publication remains supported under the existing schema.
Incomplete acquisition alone does not block it if required dispositions are honest
and the selected update is supportable. A material unresolved defect in included
content blocks that item or release until corrected or explicitly excluded with
authorized handling. Do not invent “no change,” hide gaps, or promote preview merely
by relabeling it. Preserve existing public display and internal provenance placement.

## R7 — Simplified release and delivery confirmation

Use the existing release executor as the sole owner of branch, PR, CI, merge,
deployment and completion state. Prepare one immutable verified bundle. Finalization,
export and integration reuse its proof rather than recalculate all mappings and
request new approval. Bind code/policy/configuration, research dependencies, data
files, public payload and build assets explicitly. Distinguish permitted provenance
metadata changes at finalization from substantive payload changes; no unchecked
byte change may be smuggled through that distinction.

Persist external operation intent and observed outcome. A retry locates its
existing branch/PR/commit/run and continues from the failed boundary. Python owns
waiting; model progress messages add no validation. No force push, API merge that
violates required Git identities, secret-scanning override, or unrelated file discard.

Use focused tests while developing related fixes and one applicable full regression
suite for the final code candidate. For routine data-only publication, reuse passed
code-suite evidence only when executable code, dependencies, workflow and policy
inputs match. Retain data-contract, credential and build checks. Invalidate proof
when relevant inputs change; never skip checks merely because they are slow.

Build the production artifact once per content/build-input identity. Reuse it for
preview and deployment when the current publication contract permits; otherwise
record the minimal required production transformation and verify its exact result.
CI must authenticate artifact provenance and relevant input hashes. Match tested
merge tree and release files; retain a safe fresh build fallback when proof is
missing. Do not claim exact-artifact reuse before it is implemented and tested.

After deployment, confirm successful Pages run, exact current archive/data identity,
and a bounded homepage/directory load/render smoke check. This is delivery
confirmation, not a second source-verification pass. Reuse immutable remote-byte
proof for the same commit/bundle. Retry only failed or unresolved transport steps;
do not restart database export or source review because a network read timed out.
Completion requires verified live delivery, or the explicitly requested preview.

## R8 — Compatibility and model capability

Keep all website data schemas and rendering contracts stable. New workflow records
must not leak into public summaries. Preserve active runs, issued handles, accepted
records, original inputs and historical reports. Upgrade through an explicit
versioned checkpoint with no validator in flight; older runs retain sequential
compatibility. Rollback preserves pending answers and accepted history.

Instructions must work for the invoking cloud agent or selected local model,
including Qwen3.8 Flash Next and Qwen3.8 27B BF16/8-bit configurations, without
assuming equal capabilities or context limits. Code owns mechanics; each model
gets one complete task, a short answer form, and a concrete recovery action.
Unsupported cases remain explicit. Do not change inference settings to meet a
benchmark or spawn workers without authorization. See the operator/skill rollout
and model-behavior tests before enabling a configuration.
