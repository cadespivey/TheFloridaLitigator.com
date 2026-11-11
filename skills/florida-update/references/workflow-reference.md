Current downstream policy: checked next/reply transfers reviewed data and builds
in code. Only semantic exceptions and compact content approval need model answers.
Use publication.md for the explicit resumable release executor. Full downstream
receipt examples below are maintenance compatibility, not mandatory routine steps.

# Workflow detail — lookup only

Current live-comparison corrections: execute the returned checked helper command,
not the underlying raw workflow answer CLI. At an authorized stopping point copy
returned handoff_text; it is not a stop signal and does not replace downstream
approval/publication. Do not inspect task/log directories or reconstruct counts.
Opinion cards include the complete short guidance: general civil/appellate matters
remain in scope without a novel-rule or case-specific-application requirement;
citation affirmances stating applicable civil principles can be relevant; complete bare PCAs need no
underlying-case research; missing evidence stays pending. Do not infer publication
status, drop express legal exceptions or add source bookkeeping to summaries.


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

At entry/resume obtain one fresh checked next state even if a pointer already
exists; cached pointers can predate the short interface. This is not reacquisition.
After an answer succeeds, use its returned state without another next call.

For `review_mode:inline_answer`, read the complete review_card object and send
its answer form as JSON on stdin to the returned run-local review HANDLE command.
It saves input and returns the next complete card without separate file operations. Code owns exact quotation,
provenance, stable IDs, version preservation and receipt assembly. Do not traverse
fragments or read full packets. Personnel changes retain separate predecessor and
successor identities; omit career history and unsupported fields. Opinion answers
retain holding, disposition, author names and source/status support.
For a new person include explicitly supported current contacts even if unchanged
on the page. Preserve factual text and useful address line breaks; code tolerates formatting whitespace in supported contact fields only. Quotes, URLs/emails, digits and punctuation remain exact.
Do not invent missing information or transfer predecessor personal contacts.

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py next --run-dir RUN
# Then use the returned command with JSON on stdin, e.g. /absolute/RUN/review HANDLE.
# Do not reconstruct packet/answer paths or call the compatibility answer API.
```

Overrides --checkout/--python go before the action. Normal installed runs use the
existing binding. The helper preserves answer bytes, logs and the last good pointer.
On success use its actual next state, not another next request. After a saved
submission/failed advancement retry next or the identical answer. First rejection:
correct only the short answer. After two rejected answers code checkpoints the
source and continues ordinary reviews; no model-authored repair note is needed.
For a field error, correct the named person/field and preserve other supported
contacts. Use the card/error rather than code, raw packets or diagnostic scripts.

At review_exceptions, report the exact pending maintenance work and keep the goal
unfinished. Do not repeat next, invent a harmless verdict, finalize or advance the
baseline. Appropriate technical/extended review uses its supplied maintenance
command. Downstream coverage, mapping, directory/roster and publication approval
retain separate returned receipts and validation; they are not short source answers.
Copy the returned total_sources/reviewed_sources/machine_reused_sources/pending_sources;
opinions are separate and checkpoints are pending. Default final response is at most
120 words/five bullets unless requested otherwise: phase/delivery, supplied counts,
failures/remaining work and one log/next-step link. Do not enumerate hashes or repeat
the research narrative to reconstruct completion.

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

## Explicit maintenance only

A review_exceptions result may include a predecessor-bound correction or a
maintenance-task command. Use those exact commands for the appropriate separate
technical review; never bypass them through a new acquisition or permissive
checkout. See review-integrity.md. V7 fragments and full receipt schemas are not
normal model inputs. Maintenance proof must account for actual changed script
logic/links/nontext content; a token label or equal text is insufficient. Full
submit/revise retains its repair-note gate and immutable accepted history.

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

Changed originals with equal text are routed to pending technical/extended
review. Do not manufacture raw-group narratives during routine legal screening.
Unknown significance and missing extraction remain unfinished. Original bytes,
URLs and retrieval times stay in the database; no comparison bookkeeping belongs
in public update prose.

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
