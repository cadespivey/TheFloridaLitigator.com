> Execution policy: [use the invoking model](MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Model-neutral execution policy

Research, analysis, implementation, validation and publication use the model that
invoked the workflow, in either Codex or codex-local. No named model or provider
is required. Do not stop because the session differs from a historical model
selection. A skill cannot switch its own running model; report model identity only
when exposed by the session, otherwise say it is unavailable.

This policy supersedes earlier Astra-only, cloud-only, Qwen-only, local-worker and
mandatory hybrid-delegation requirements in this repository. Execute directly in
the invoking session unless the user explicitly requests delegation. Do not start
another worker, restart inference servers or unload models to satisfy old notes.
Use available tools; preserve and report an actual missing capability instead of
claiming a check succeeded or switching models without direction.

The evidence and publication requirements are identical for local and cloud
models. Code determines source changes using hashes and official status metadata;
the model interprets relevance and significance. Finish and persist one review
task before the next, retain durable progress for compaction, and never equate a
model name with review quality. Do not claim independent or human review when the
invoking model performed the review itself.

Use SOURCE_HASH_REVIEW.md and OPINION_DISCOVERY.md for updates. The installed
$florida-update skill can be invoked in either Codex or codex-local. Its local
installation is ~/.codex/skills/florida-update/SKILL.md. Model selection belongs to
the calling session, not the skill. No model-specific launch flag is required by
the workflow.

Dated county notes, prior handoffs, evaluation results and original review
attributions remain historical evidence, not execution instructions. Their old
model restrictions, pause/resume directions and next-county assignments do not
reactivate completed goals. Start from the current database checkpoint and the
user's current request. Preserve historical reports without rechecking them as a
final integration requirement.
