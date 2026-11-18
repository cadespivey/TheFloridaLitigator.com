# Test and evaluation plan

Planned tests; no runtime or model benchmark is claimed by this document. Extend
existing tests in place. Use disposable SQLite databases, repositories, mocked
network/release boundaries and small selected captures. Never clone the production
database, reacquire statewide sources, or run a second update for test convenience.

## Requirement coverage and defect detection

| IDs | Scenario and observable assertion | Existing test families to extend |
| --- | --- | --- |
| R1 | Resume with stale historical to-dos: capsule uses current contract, closed items remain closed and next action is unchanged | `test_review_transport`, `test_inline_review_helper`, `test_workflow_contracts` |
| R1 | Phase/task-count/failure triggers coincide: one reminder in existing response, no extra model/tool acknowledgment; exact retry emits no duplicate reminder | Transport and helper tests |
| R1 | Known missing source versus generic suspicion: prompt scenario takes bounded recovery only for named gap; material expansion waits for approval | Model-behavior trials below |
| R2 | Identical original/policy reuses extraction/review; changed original, attachment, status or policy invalidates affected work; missing body never becomes no-change | `test_incremental_review`, source/hash and workflow tests |
| R2 | Resume, failed retrieval and exhausted retry retain originals/error/status; no unexpected network requests or baseline advancement | Acquisition/workflow fixtures |
| R3 | Stable identity and supported URL reuse automatically; name-only, title/hyphen variants, changed county/role and conflicting assignments produce bounded exceptions | `test_directory_reuse`, `test_directory_aliases`, `test_directory_role_projection`, `test_workflow_scope` |
| R3 | Rehearsal discovers multiple schema defects in one pass but writes no acceptance, source review or public data | `test_publication_driver`, disposable DB snapshots |
| R3/R4 | Complete cards and returned state are reused; tampered card, quote, dependency or policy fails; unrelated accepted opinion does not invalidate all cards | `test_review_transport`, `test_inline_review_integration`, `test_incremental_review` |
| R4 | Optimized path matches safe full calculation for accepted findings, task availability, exclusions and failures; mutation invalidation and cache eviction do not alter outcomes | Workflow and incremental fixtures |
| R5 | Sequential and pipelined identical valid/invalid semantic inputs produce equivalent accepted domain records and coverage; normalize only run IDs/timestamps | Transport/workflow integration |
| R5 | A validates, B submits, C prepared: B is durable but not accepted, C is not issued; limits hold under concurrent commands | New cases in transport/integration families |
| R5 | Two issuers/submitters race: no duplicate reservation or acceptance; exact replay returns saved outcome; changed accepted answer requires correction | Transport and workflow hardening |
| R5 | Dependencies change after preparation, issue, submission or validation: affected candidate becomes stale; original answer remains unchanged and cannot silently rebind | Transport/incremental integration |
| R5 | Consolidated opinions share a dependency; changes fence both. Unrelated opinion permits bounded overlap | Opinion workflow fixtures |
| R5 | Validator A rejects while B pending: repair policy and distinct rejection count preserved; B cannot overtake nonterminal A; unresolved A recorded explicitly | Short-answer/recovery tests |
| R5 | Expired reservation with live validator: obsolete owner cannot commit; no submitted answer is discarded; restarted owner reconciles exactly once | Workflow hardening/failure injection |
| R5 | Exhaustion or transition to personnel/publication: no speculative issue, pending work drains, sequential behavior restored | `test_publication_driver`, inline integration |
| R6 | One campaign approves each new item at most once; prior exact verification reused; correcting one item rechecks only it and dependency closure | Publication acceptance/evidence gate tests |
| R6 | Tampered/unverified payload, stale verifier policy, unresolved included defect or unfinished submission blocks aggregate approval; explicit limited coverage remains honest | `test_publication_evidence_gates`, `test_workflow_contracts` |
| R6 | New/prior contact bindings remain valid, duplicate candidates exposed, explicit waivers retained; audit counts distinguish operations and unique identities | Directory audit/reuse/waiver tests |
| R7 | Network timeout after verified export retries only delivery; same commit/bundle reuses proof; new file/merge/build input invalidates relevant proof | `test_publication_executor`, `test_release_file_bytes` |
| R7 | Concurrent edit, failed CI, secret rejection, PR already created, merge succeeded before crash: exact checkpoint recovered without new release or override | Executor and credential tests |
| R7 | Data-only code-proof reuse requires exact code/dependency/workflow/policy inputs; a changed executable input forces applicable tests; untrusted/stale artifact rejected | Release/CI fixture tests |
| R7 | Successful deployment but wrong live archive fails completion; preview never reports published; exact data and bounded live-render smoke required | Deployment/executor fixtures |
| R8 | Older handles and active-run protocol recover; explicit upgrade at rest preserves acceptance and pending answer evidence; rollback is lossless | `test_workflow_relocation`, transport compatibility |
| R8 | Same public input produces unchanged public JSON schema/content and expected renderer output; menus/search/date filters/directory groups/history unchanged | `test_directory_display`, `test_directory_display_comparison`, site/publication tests |

## Crash matrix

Inject termination before and after: immutable input save; submission record;
reservation claim; expensive validation; domain acceptance; coordinator acceptance;
next-state projection; aggregate verification; integration; commit; push; PR creation;
merge; artifact upload; deployment; live-result recording. Assert the exact durable
state at each boundary and successful idempotent recovery. Test actual process
interruption where mocks cannot establish locking behavior. Require no duplicate
domain findings, lost original bytes, premature counts or publication. A task's
pending state must not disappear through rollback or reservation expiry.

## Semantic regression fixtures

Use bounded captured excerpts/documents and independently established expected
outcomes. The later independent assessment supplies leads, not automatically true
gold answers. Confirm each fixture once and retain that verification for reuse.

- Opinion qualifications: exceptions in both holding and practical summary;
  assumed versus decided issues; result-only concurrence versus lead reasoning;
  substituted/withdrawn opinion status; present-record limit versus permanent bar.
- Deadline conflict: captured opinion language differs from a current rule supplied
  in the fixture. Preserve the conflict and avoid unsupported current-practice advice.
  Do not turn every opinion into a historical rule-research assignment.
- Missing body, unavailable rule table, conflicting dates, newly linked old order:
  no invented no-change decision, effective date or statewide legal scope.
- Personnel: staff change in noncivil division remains in scope; successor does
  not inherit predecessor contacts; title/spacing variations surface a duplicate
  candidate without an automatic identity merge; county does not imply court ID.
- Preserve accepted material and citations while removing public bookkeeping.
  Mechanical wording bans cannot substitute for semantic checks.

Run original drafting and final verification roles as distinct tasks within the
same bounded fixture workflow. Verification must detect planted material defects
and leave sound items intact. Do not require a second agent or new model session.

## Performance experiment

Compare three modes on the same pinned fixture corpus and hardware:
A: current supported sequential path; B: optimized sequential path; C: optional
bounded pipeline. Use the same validators, evidence, policy and fixed answer stream
for orchestration measurements. Separately measure live model behavior when
authorized. Fixed-answer replay does not demonstrate legal quality or inference speed.

Use at least 60 representative task instances spanning relevant opinions with
qualifications, exclusions, status exceptions and invalid submissions. Report
category counts. Perform one unmeasured warmup and at least three measured runs
per mode, alternating order. Measure cold start separately. Include one resume and
controlled failure workload. Do not let compaction or cache state silently favor
one mode; report model/context/cache characteristics and compaction events.

Record median and p95 time per correctly accepted review, total completion time,
stage exclusive/inclusive durations, lock waits, model idle time, failed validations,
stale/discarded cards, model/tool calls, scope reminders, human nudges, full refreshes,
evidence loads, CPU, peak resident memory, artifact bytes and disk I/O. Time failures
and repairs in total workload cost; do not drop them to improve throughput.

The initial 60-instance sample is a practical engineering comparison, not a
statistical claim about all legal research. Report raw distribution/sample size
and repeat only when instability or unresolved concern warrants it. Compare C to
B for the overlap decision. Apply the proposed targets in IMPLEMENTATION_PLAN.md;
no acceptance on speed if invariants or semantic fixtures fail. Finalize resource
budgets before measurement, including enough memory headroom for the selected model.

## Model and instruction trials

Use the invoking cloud agent and, when explicitly authorized and available, each
selected Qwen3.8 Flash Next / 27B BF16 / 27B 8-bit configuration. Record actual
model identity or unavailable; never infer one variant's result from another's.
Use existing runtime guards and one active local inference request. Do not tune
MTP, model loading or quantization in this project. Consult the runtime README
before authorized local execution; a test plan is not execution authorization.

Give every configuration the same complete compact cards and operator instructions.
Include substantive legal qualifications, personnel conflicts on the sequential
path, malformed/truncated output, saved-but-pending status, rejection repair,
resume with stale historical notes, a closed review plus generic concern, a concrete
new defect, and a finished release. Verify observable actions rather than whether
the model repeats the reminder. Required outcomes: no scope expansion without
approval; no invented support; no duplicate accepted reply; accurate saved/accepted/
published distinction; no dropped material qualification; stop at completion.

Compare reminder enabled/disabled on the same bounded scenarios where practical.
Count unnecessary retrievals, closed-item reopenings, repair detours, extra tool
turns and user interventions. A failed model/configuration remains unsupported for
the failing task until a bounded instruction/interface repair passes; do not conceal
failure by silently routing the whole workflow to a stronger model.

## Release and website compatibility

One prepublication campaign includes deterministic public-data/build checks and
bounded preview visual checks using fixed viewport/content fixtures. Compare HTML,
CSS/JS/assets and DOM behaviors; normalize only explicitly justified nonsemantic
metadata. Any appearance or public-data-display change violates scope and requires
correction, not screenshot-baseline replacement. Live delivery smoke checks verify
that the already checked artifact loads; they do not reopen source interpretation.

Reusing CI/build evidence requires tests for changed dependencies, renderer,
configuration, actions and policy as well as changed data. Inspect warning output;
do not suppress warnings to claim a clean run. Test mocked GitHub failure/retry
paths before any authorized live rollout. Preserve required author/committer
identity, credential checks and non-destructive Git behavior.

## Evidence and completion

Save the fixture manifest, command/commit/configuration, measured results, exact
failures, recovery outcomes and review limitations under this subproject's evidence
directory when generated. The final report must say which requirements passed,
which were deferred, whether overlap earned rollout, which models were actually
tested, whether all three skill profiles matched, and whether website behavior
remained unchanged. Planning completion is not implementation or benchmark success.
