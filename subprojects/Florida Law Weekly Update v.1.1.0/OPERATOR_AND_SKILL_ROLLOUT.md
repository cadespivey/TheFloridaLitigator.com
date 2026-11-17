# Operator instructions and shared skill rollout

These instructions guide implementation and future rollout. The candidate skill
is a draft. Do not install it before its protocol and recovery behavior exist.
Current production instructions and active runs remain unchanged by this package.

## Implementation handoff

Read README, the specification, implementation plan and test plan. Confirm user
approval of implementation, then work directly in the existing checkout/modules.
Start with profiling and scope reminders. Do not start by writing a scheduler or
replacing the codebase. Preserve working changes and saved update state. Do not
launch workers or alter inference settings merely because local-model support is
an acceptance goal. Record actual findings and bounded deviations in this subproject.

After approval, execute ordinary edits/tests autonomously. Ask again only for a
material deviation, permission not already granted, or unresolved product choice
that changes scope. End with final diff, test/benchmark evidence and the deployment
checkpoint. Implementation approval alone is not permission to publish legal data.

## Future routine operation

The model receives the current scope capsule and one complete card. It reads the
evidence and submits only the semantic fields through the code-supplied command.
It uses the returned state without asking for another copy. Python owns preparation,
bindings, persistence, counters, waiting and release mechanics.

| Returned state | Model action |
| --- | --- |
| Complete issued card | Answer that card once |
| Answer saved, pending validation | Preserve the acknowledgment; review a next card only if issued by code; otherwise use the supplied wait operation |
| Accepted plus next card | Continue with the returned card; do not resubmit or fetch next again |
| Rejected | Repair the named field from the exact error/evidence; follow existing rejection limit |
| Unresolved or stale | Preserve evidence and use the supplied recovery/checkpoint; do not invent no-change or rebind the answer |
| Verification card | Check only the named final item/delta; reuse listed closed verification |
| Release running | Wait on the existing process; do not create another PR, build or publication |
| Delivery failed | Resume the named failed step; do not redo source review or database export |
| Complete | Report result and limits; stop |

These are meanings, not invented CLI command names. The implemented checked helper
must supply the actual supported operation, handle, paths and waiting semantics.

## Scope reminder text

> Finish the authorized update for the stated period and stage. Use the supplied
> task and saved evidence. Reuse closed work; reopen it only for a named error,
> material gap, conflict, changed dependency or failed check. Repair only that issue.
> Do not enlarge research, repeat completed verification or change the workflow to
> satisfy generic concerns. Obtain approval before material scope expansion. Keep
> uncertainty explicit. Complete the remaining deliverables and stop at the stated
> stopping condition. No acknowledgment or plan restatement is needed.

The reminder accompanies current scope fields and the existing next response.
Code chooses emission under R1. A model must not create a heartbeat agent, timer,
new session or recurring tool call. Keep the current resume view short; historical
checkpoints remain linked and are read only for a concrete recovery question.

## Skill structure and capability

Keep one shared `florida-update` skill for cloud and local models. The candidate
entry point routes to review rules or release/recovery only when needed. Retain
exact semantic field names and code-owned commands; avoid long receipt schemas,
repetitive policy prose and model arithmetic. Fully supplied examples should be
added to the implementation's card fixtures, not copied into every prompt.

Do not promise all tasks fit a particular context window or model. Evaluate the
selected configuration against TEST_PLAN.md. A smaller model may need a more compact
complete card or an explicit exception; never remove necessary evidence or lower
acceptance criteria. Capability uncertainty is reported, not solved by secretly
changing model or launching a second worker.

## Installation ownership and observed profile paths

Repository source: `skills/florida-update/`.
Installer: `scripts/install_florida_update_skill.py`.
Canonical installed package:
`/Users/cadespivey/Developer/CodexSkills/florida-update`.

On November 17 all these entry points resolved to that canonical directory:

- `/Users/cadespivey/.codex/skills/florida-update`
- `/Users/cadespivey/Developer/LocalCodexSetup/codex-profiles/local/skills/florida-update`
- `/Users/cadespivey/Developer/LocalCodexSetup/codex-profiles/cloud/skills/florida-update`
- `/Users/cadespivey/Developer/LocalCodexSetup/codex-profiles/personal/skills/florida-update`

The three profile SKILL.md files had identical SHA-256:
`a80fe0443f4ad531ef36e3abab92d522e302cc869289ddb32ee1bc088d7969fb`.
This verifies filesystem resolution/content, not that an already running model
conversation has reloaded the skill. No active skill was modified during planning.

## Promotion procedure after implementation

1. Reconcile the candidate instructions with actual implemented states and commands.
   Preserve current installation metadata and unrelated skill resources. Update
   the repository skill, relevant references, AGENTS.md, short-review specification,
   deterministic-publication guidance, and resume instructions together. Mark old
   protocol instructions as compatibility guidance rather than leaving conflicts.
2. Validate frontmatter and links, run helper/launcher checks and behavioral tests.
   Keep model instructions independent of cloud-only tools: use goal tools when
   available and authorized; otherwise the durable run contract records scope and
   completion. Never replace an existing goal or create one contrary to host policy.
3. At a safe checkpoint, use the existing installer against the canonical directory
   with the owning checkout and established interpreter. The installer copies
   repository-owned files and writes installation bindings. Inspect the destination
   and preserve unrelated files; it does not remove obsolete references automatically.
   Do not follow a stale setup path or install a second divergent skill.
4. Verify resolved destination and hashes of all repository-owned skill files for
   codex-local, codex-cloud and codex-personal; verify installed launcher checkout,
   interpreter and supported protocol. Do not recreate links or change machine-wide
   configuration if a profile differs: report the concrete mismatch for resolution.
5. In each available harness, verify discovery of `florida-update`, displayed name/
   description and actual loaded protocol using a harmless fixture task. If a harness
   is unavailable, record that limitation; matching filesystem links alone do not
   establish in-session discovery. Do not restart a running update to force refresh.
6. Save version/hash and behavioral evidence. Existing conversations resume with
   explicit protocol compatibility; new instructions must not invalidate issued
   handles. Roll back through the documented compatible protocol, preserving pending
   submissions and accepted history.

The installer invocation uses real, verified paths at rollout. Its current supported
arguments are `--checkout`, `--python`, and `--destination`; no v1.1.0 CLI flag is
claimed to exist yet. Keep this package's draft separate until promotion.
