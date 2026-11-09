# Workflow detail — lookup only

Use SKILL.md for the normal loop and start-run.md for new-run setup. Read only
the phase/error details needed below. The returned task/template governs review;
optional comparisons are not extra mandatory work.

## Follow the coordinator through completion

Public writing must describe a supported material legal/procedural/personnel
change and its practical effect. Exclude inconsequential differences and source-
reconciliation bookkeeping. Do not publish a research-incomplete notice or explain
that saved findings/compilations disagree as the news item. Keep those records
internally. Retrieval/discovery alone does not establish a new legal development.
For included statute/procedural/local-rule candidates, `candidate.change_analysis`
has exactly `material:true`, `previous_requirement`, `current_requirement`,
`practical_effect`, `basis_quote`. Supply an exact quote present in the publication
citations and concise, accurate public prose about what changed, to whom it applies,
when supported, and what practitioners should do. Do not guess effective dates or
resolve conflicting authorities by assertion. If an actual change cannot be
supported, exclude the item. The code's structural checks do not certify the model's
legal interpretation; the publication review must assess the claim and citations.

For setup or lifecycle questions consult `docs/workflow/DETERMINISTIC_COORDINATOR.md` or
[process lifecycle](process-lifecycle.md). Initialize the resolved run:

```sh
flwu workflow init --run-dir RUN --database DB --registry REGISTRY --run-id RUN_ID \
  --end YYYY-MM-DD --mode publish --archive website/updates
flwu workflow next-task --run-dir RUN
```

Use the verified launcher above for these commands. Add `--start` for an explicit
start; use `--mode preview` for a preview request. Current supplements are selected
by default. Do not replace this with a hand-built report workspace or assembly script.

The registry is a JSON object: its source list is `registry["sources"]` and its
stream is `registry["stream"]`. Current supplement directories are
`website/county-directories/` and `website/court-directories/`; there is no
`website/directories/` input folder. Init selects both directories by default.

Execute each returned command, or read the returned `review_guide` (the full
packet remains available), copy its
receipt template to its specified receipt path, complete the evidence-bound fields,
and use the checked step helper below to submit and receive the next task. Packets supply schemas,
current/prior source evidence, full finding versions, save paths and completion
checks. Code compares hashes/status, maintains bookkeeping, assembles the report
and projects directory deltas. You interpret relevance, write supported findings
and summaries, resolve explicit identity choices, and perform editorial review.
Use concise civil/commercial operating summaries. Noncivil subjects need contacts,
assignments, links and basic shared instructions only. Preserve documented source
conflicts without deciding which authority controls.

Source templates prefill exact changed-line quotations, including whitespace and
extraction-path lines. Keep them intact; do not reconstruct them by typing or
replace them with paraphrases. Read every changed line and sufficient original
context, then supply the outcome and substantive explanation. Prefilled citations
are not completed review. When changing a prior finding, open its indexed full
file first and preserve its nested facts and version guard. If two receipt repair
attempts fail, save the exact errors and a checkpoint for supervisor review rather
than repeating speculative edits or claiming completion.

For source-review interpretation boundaries, follow the runbook's **Task-specific
review** section: retaining a finding does not reverify its other cited pages;
observed timestamps do not establish their cause, and different date formats do
not alone establish a conflict. Describe the effect on facts this source supports.

Code first reuses identical raw hashes or a versioned, supported content/component
hash proof. Reused entries already have machine provenance; do not reopen them or
write model receipts for them. See SOURCE_HASH_REVIEW.md's content/component policy.
Known metadata is preserved separately; arbitrary model-side filters are prohibited.

For the review loop, use the checked step helper instead of shell pipelines or
run-specific submission scripts:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py next --run-dir RUN
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py submit --run-dir RUN --packet PACKET --receipt RECEIPT
```

Pass `--checkout CHECKOUT` before the action when overriding installation.
Development/CI may also pass `--python PATH` before the action; preserve the
virtual-environment interpreter path. Ordinary installed runs use their existing
installation binding and need no runtime changes.
Read the returned `next_state` file and follow its actual phase. The helper keeps
full stdout/stderr/exit codes in `RUN/agent-steps/`, stops after failed submission,
and atomically replaces `RUN/agent-next-task.json` only on successful valid output.
Submit/revise now use `workflow submit/revise --advance`: one launcher preflight
and one process return the next task. Do not issue a redundant `next` after a
successful helper submission. If acceptance succeeded but advancement failed,
keep the exact receipt and retry `next` or the identical submission; do not create
another review, reacquire sources or reset the run. The old pointer is preserved.

Code caches derived comparisons and updates only affected work; unchanged bytes
reuse extraction under the same parser policy. `.flwu-derived-cache/` beside the
history database is disposable computation, never evidence or accepted review.
Missing/corrupt/old cache entries recompute automatically. Do not inspect cached
entries or re-review machine-reused sources. New observations, review corrections,
opinion statuses, protocol/policy changes and finalized-baseline changes invalidate
their dependencies; discovery of all seven appellate courts remains mandatory.
It does not complete the workflow or replace acquisition/publication commands.
Wait its existing tool session if still running; never launch another copy merely
because stdout is quiet.

If the returned phase is `source_review_correction`, read `correction_guide` and
the returned review guide. Copy `receipt_template` to `save_receipt`, complete the
specific observed differences, and use the returned predecessor/reason:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py revise --run-dir RUN --packet PACKET --receipt CORRECTION_RECEIPT --predecessor RETURNED_SHA256 --reason "RETURNED_REASON"
```

This appends a validated correction. Preserve the old accepted receipt and packet.
Repeated case/whitespace-normalized change explanations are rejected on submission
and excluded as reuse proof, including already saved receipts. Do not evade this
by adding counters/IDs to boilerplate. Code cannot establish semantic truth from
unique prose; each reason must explain an actual observed before/after difference.
Independent valid source/component proofs can still skip a page; a deficient
receipt is not itself such a proof. Do not restart acquisition to repair a review.
After a pause/compaction, start with `review_step.py next`, not an old scratch
classifier or receipt generator. Follow returned paths; do not guess JSON keys or
filenames. Record the session's actual model when exposed, not `codex-agent`.

Do not author automatic no-change receipts from substring/hostname tests or
blanket URL-case/host substitutions. The hash gate owns approved reuse. A returned
source packet needs bounded interpretation; read the decoded fields in its v7
group fragments for JavaScript/embedded-data differences instead of rewriting parsers
or repeatedly dumping entire originals. The original comparison remains evidence;
use aligned group IDs for the current schema 2 template, or original change IDs
for a legacy schema 1 template. Report a specific unsupported comparison rather than inventing a
harmless-change conclusion.

For a newly changed shared component, explain the actual before/after changes,
including script logic outside rotating tokens. A Cloudflare label does not prove
that only challenge IDs changed. A URL case change does not prove equivalent
routing; state the observed link change and the bounded content-review conclusion,
without claiming the targets were verified unless they were. Do not infer that
an `og:updated_time` value is a retrieval time or a substantive edit date. Treat
unexplained component changes as unresolved rather than approving shared reuse.

When an officeholder changes, keep the predecessor and successor as distinct
people. Create or reuse the successor's own stable person key and reconcile the
office roster reference with that key in the supported findings. Do not put a
successor's name under a predecessor's person ID. A spelling correction to the
same person is different; preserve source discrepancies without inventing an
identity change. Final roster/person reconciliation remains required.

Preserve date meanings exactly: selection/appointment, publication, revision,
retrieval and effective dates are separate. Do not call a stated selection date
an effective date without explicit evidence. Describe observed metadata values
without inventing their cause or a per-session rotation schedule.

If the queue identifies an omitted prior source, follow SOURCE_HASH_REVIEW.md's
bounded supplemental acquisition sequence. The coordinator records
`reviewed_supplement` automatically only with current exact-source evidence and a
completed matching source review or official opinion-monitor signature. Do not
author another model review for that reuse or mislabel an in-scope reviewed source
as unavailable/excluded. Genuine failed acquisitions and changed evidence remain
pending. Save relevant additions in the ongoing registry for subsequent runs.
Opinion discovery/status, changed PDFs and effective-date triggers remain independent.

For a returned task whose original bytes change but extracted text is identical, read
`inputs.raw_comparison_path` and inspect the originals as needed. Complete the
required `raw_change_review` from the returned current guide/template. For schema
2 preserve comparison/alignment hashes and explain every aligned group; do not
also fill one answer per legacy positional change. Schema 1 retains comparison
hash/change IDs. State your inspection method. HTML comparisons include
attributes and embedded JSON; binary comparisons only identify changed spans and
require an appropriate original-document review. Do not infer harmless metadata
or CSS/JS changes from an empty text diff. Do not publish private comparison data
or embedded tokens as report content. Unresolved original-content changes stay
unfinished.

`workflow acquire` invokes the standard seven-court update and registered-source
hash gate under the same database acquisition lock. Wait on its actual tool session;
no stdout while it runs is normal. After completion proceed to `next-task`.
`status` and `next-task` refresh saved queues without fetching sources again.
After interruption resume the same generated acquire command once the process has
exited; do not create a competing run or use source-gate as a replacement.

Do not stop after launch, acquisition, screening or a build. Follow `prepare-report`,
`refresh-directory`, `workflow build`, roster review and separate publication
acceptance as returned by the coordinator. Missing extraction/evidence is unfinished;
source failures remain qualified gaps. Do not invent review attestations, IDs or
citations to clear validation. For a completed interpretation needing correction,
use the runbook's source/opinion correction path; never edit accepted artifacts.

Preview completion returns `preview_complete` only after actual editorial acceptance;
report that nothing was finalized or deployed. Publish mode returns the exact
finalize command, then `workflow export`, `workflow integrate`, and `workflow release-plan`. Follow
its file paths and destination-hash checks and repository WEB_PUBLICATION.md for
reviewed-file integration, credential scan, authorized Git/PR/Pages release and
live verification. `publication_handoff` is not live publication. Keep the persistent
goal active until deployment is verified; do not treat the coordinator handoff as
the whole update. Do not audit historical reports.

Record dates, actual selected model when known, reviewed/reused/pending counts,
database capture IDs, limitations, new files, tests and deployment evidence in
RESUME.md and the final response. Keep saved findings, local site builds and live
publication distinct. A blocked deployment does not justify repeating research or
advancing another baseline. Use the persistent goal's blocked rules if necessary.

## Installation and recovery

Install/update this repository's skill with `python3 scripts/install_florida_update_skill.py
--checkout CHECKOUT --python /Users/cadespivey/Developer/FloridaLitigator/florida-litigator-weekly-update/.venv/bin/python`.
The installed `installation.json` binds an explicit checkout and interpreter.
No development worktree is assumed. `--checkout` still overrides that binding.
Use a maintained current checkout; preserve the dirty historical research checkout.
For receipt corrections or damaged generated files, read the correction/recovery
sections of `docs/workflow/DETERMINISTIC_COORDINATOR.md`; use `workflow revise`,
`workflow repair`, or `workflow build --repair` rather than deleting a run.
If a checkout moved during source/opinion review, follow that runbook's
`workflow relocate --run-dir MOVED_RUN --reason EXPLANATION` recovery path from
the new checkout. Preserve the original contract and domain reviews. Do not edit
pinned paths in place, recreate retired links, initialize another run or refetch.
After relocation, use the newly returned task; an old packet/command may bind the
retired location. Downstream-stage relocation is intentionally refused.
