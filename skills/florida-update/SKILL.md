---
name: florida-update
description: Run The Florida Litigator's bounded civil-litigation update for Florida case law, statutes, bar and court procedural rules, and court personnel; persist hash-gated findings and refresh reviewed website data.
---

# Florida Litigator update

Use the model selected in this Codex or codex-local session. This skill updates
Florida case law, statutes, bar/court procedural rules and court personnel, with
a civil/commercial focus. Retain the full statutes corpus and existing evidence.
Pending bills, specialized noncivil merits and exhaustive agency research are
outside the task. Noncivil personnel need contacts, assignment, links and basic
operating instructions.
Record the actual model when exposed; otherwise record it as unavailable.
Invocation authorizes the ordinary validated update and publication steps;
honor any explicit preview or narrower limit.

## Start or resume

1. Call `get_goal`. Reuse a matching unfinished update goal. If none exists,
   create one with the objective below before acquisition. Do not replace an
   unrelated active goal; ask which goal to use. Do not set an unrequested budget.
   If goal tools are unavailable, report that capability failure honestly.
2. Verify the installation:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/flwu.py --check
```

Use the reported checkout and its AGENTS.md. Use this launcher for every `flwu`
command; bare `flwu` may import the wrong checkout. Live database:
`/Users/cadespivey/Developer/FloridaLitigator/shared-history/research-history.sqlite`.
Preserve unrelated changes. Never substitute a trial or legacy database.

3. For an existing run, read RESUME.md and use the last successful next-state
   pointer. If it is missing, use the checked helper:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py next --run-dir RUN
```

Do not initialize, reacquire or restart an existing run. Wait on an already
running process, then continue when it exits. For a genuinely new run, read [start-run.md](references/start-run.md) for registry,
date and initialization commands. Default baseline is the last finalized
report's period end; default cutoff is the latest completed Sunday. Honor explicit
dates and preview limits. Code must determine the actual reporting window.

Goal objective:

> Complete the authorized bounded Florida Litigator update: seven-court opinion
> discovery and registered-source hash acquisition; supported relevance reviews;
> validated database persistence and readback; reviewed report/current directories;
> authorized website publication with deployment/live-content verification, or
> the expressly requested preview. Use the last finalized report as baseline
> unless a start date is supplied. Preserve evidence and historical reports.
> Starting a process or producing a queue is not completion.

## Review one task

Read the returned `review_guide` and current receipt template. They contain the
current task, evidence, output fields and save path. Detailed manuals are lookups
for a specific uncertainty, not another checklist to read for every task.

- Code has already checked hashes/status and reused eligible reviews. Process
  only the returned task. Do not reopen machine reuse or classify changes using
  your own hostname/keyword script.
- Review the supplied before/after evidence for the court/law/personnel question.
  State observed facts and supported practical effects. Do not invent CMS causes,
  equivalent routing, harmless script behavior or legal effective dates.
- Do not turn optional comparisons into extra mandatory raw review. Complete
  `raw_change_review` only when the returned template includes it. Required raw
  review still applies; unclear evidence stays unfinished, never no-change.
- Preserve prefilled quotes, hashes, paths and versions exactly. For blank quotes
  use the returned quote bindings and `workflow quote`; see **Exact quotes** in
  repository `docs/workflow/SMALL_REVIEW_PACKETS.md` only if syntax is needed.
  Do not retype a quote or write an ad hoc data parser.
- Personnel use the returned judge/clerk template and a distinct successor key.
  Preserve existing facts/version. Fill supported contact slots or omit unreviewed
  ones. Summarize the changed role/name, stated date and operating facts; omit
  education and career history unless needed to distinguish identities. Do not
  invent a missing-contact search or carry former work into a current assignment.
  Keep documented source conflicts in internal evidence.
- If the task requires expertise or evidence you do not have, save the exact
  unfinished state and specific blocker. Do not improvise a technical explanation,
  reset the run or repeatedly vary wording to force validation.

Save at the returned receipt path and submit with the checked helper:

```sh
python3 /Users/cadespivey/.codex/skills/florida-update/scripts/review_step.py submit --run-dir RUN --packet PACKET --receipt RECEIPT
```

On success use its returned next state; do not request it again. On failure read
the saved error. For correction/repair use [review-integrity.md](references/review-integrity.md)
and the exact returned revise/predecessor command. After two rejected drafts the
existing repair-note gate applies. Preserve all failed attempts in run accounting.

## Finish the workflow

Follow the coordinator's returned phases through report/directory review,
publication acceptance, finalize/export/integrate and deployment verification.
For release steps read [publication.md](references/publication.md) and the relevant
**Follow the coordinator through completion** section of the workflow reference.
A publication handoff is not a live deployment. A partial run cannot advance the
finalized baseline. Do not audit historical reports.

Public updates describe supported material changes and practical effects. Never
insert research-incomplete notices or source-reconciliation narratives under
public headings. Exclude unsupported/inconsequential news claims. Keep provenance,
conflicts and gaps internal; never fabricate completeness.

Keep a short RESUME.md with exact paths, next command and saved capture IDs. Report
actual counts, failures and verification evidence. Mark the goal complete only
when all authorized deliverables are verified; honor user pauses and goal-tool
blocking rules. Do not restart inference servers, unload models, install packages
or launch another worker. Explicit isolated test assignments use their own trial
instructions and parent-owned goal limits; they do not authorize production runs.
