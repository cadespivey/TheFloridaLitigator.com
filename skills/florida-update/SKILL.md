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
For Cade's substantive drafting, apply the installed `cade-writing-style` skill
once per session; keep its guide as the maintained source rather than copying it
into every card. Other installations follow the invoking user's writing preferences.
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

3. For an existing run, read RESUME.md, wait for any live command, then refresh
   the next-state pointer once with the checked helper—even if an older pointer
   exists. This upgrades old-format task views without reacquisition:

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

When a parent explicitly completes preflight for a bounded assignment, start with
its supplied command; skip repeated directory/process/runtime inventories.

## Review one task

For `review_mode:inline_answer`, read the complete returned `review_card` object.
Read the complete card; request sufficient tool output if it is truncated.
It contains acquired before/after passages, short evidence IDs, prior-person
references and the answer form. Send your answer JSON on stdin to the returned
`command` in the same action; code saves, validates, persists and returns the
next complete card. No separate card read, answer-file write or path assembly.
Do not inspect packets, receipt schemas,
fragment manifests or source code for normal source/opinion review.

Code already compared hashes/status and reused completed reviews. Interpret only
the returned court/law/personnel question. Give the supported material change and
practical effect or a brief no-material-change reason. Preserve date meanings;
do not invent technical causes, browser behavior or legal effective dates.
For people, select the supplied existing-person reference or a distinct new
successor. Report changed names/roles and supported operating fields; omit career
biography and unreviewed fields. Code preserves other nested facts and versions.
For a new person, include contacts explicitly stated in the current card even
when unchanged on the page. Preserve facts and useful address line breaks; code
accepts formatting whitespace in supported contact text. URLs/quotes remain exact;
never inherit a predecessor's personal contacts or invent absent information.
For opinions retain holding, disposition and author names. Select supplied evidence
IDs; code copies exact quotes, citations, hashes, timestamps and identifiers.
Civil/appellate procedure matters for individual/small-claims parties are in scope;
no novel-rule requirement. A complete bare PCA can be not_relevant for lack of a
stated substantive ruling, without researching the underlying case. Missing or
unreadable evidence stays unresolved; a documented conflict alone does not. A
material official status change can warrant an update even with unchanged bytes.
Never infer unpublished/nonprecedential
status from Citation/PER CURIAM. Preserve express exceptions and record limits.
Holding gives the operative rule/facts; summary gives practical effect; disposition
gives court action only; authors are byline names, not panel members. Keep source
bookkeeping out of summary text. Excluded matters need a brief reason and empty holding.


A citation affirmance quoting applicable civil/commercial principles is not a bare
PCA: include it when relevant even without new law or case-specific application.
A bare PCA provides no substantive reasons or stated applicable principles.
Preserve material qualifications in BOTH holding and summary: “ordinarily” stays
qualified; “such as veil piercing” gives an example, not the only available test.
Excluded matters usually need one supported sentence, without specialized merits,
biography or repeated dates/status. Do not infer underlying-order finality from a
rule number or the opinion's rehearing-finality warning.

For source tasks, use code-owned source_context: baseline establishes supported
current information and requires no prior passage; comparison needs the supplied
before/after evidence. A navigation-only baseline may yield no material finding,
without certifying historical no-change or opinion-discovery coverage. Missing
expected body content/extraction still remains unresolved. Configured opinion
notice-page review is separate from official listing/status discovery and PDFs;
the role label alone is not proof of complete extraction.

Use the exact returned command with a quoted stdin heredoc, for example:

```sh
/absolute/RUN/review TASK_HANDLE <<'ANSWER_JSON'
{...the card's answer fields and supplied evidence IDs...}
ANSWER_JSON
```

RUN and TASK_HANDLE above illustrate code-owned values, not paths to invent.
The run-local command pins the checkout/interpreter and task evidence. Existing
file-based answer/submit/revise commands are compatibility or maintenance paths.

Follow the returned next state after success; do not request it again.
Use the returned checked command as written; do not replace it with the raw
workflow answer CLI, which does not manage the helper's logs/pointer. First
rejection: repair the named person/field from the saved error and card; retain
the other supported fields. Do not drop all contacts, inspect code/raw packets,
or write diagnostic scripts to repair an answer. After two rejected
answers code records an unresolved checkpoint and continues other ordinary tasks;
no model-authored repair note is needed. A saved submission/failed advance can be
recovered with `next` or the identical handle/answer, without resetting or
reacquiring. Identical rejected retries reuse the error instead of consuming a
second failure attempt. A changed answer to an accepted handle is not a retry;
use the returned explicit correction path. If tool output was lost/truncated,
refresh checked next once with enough output capacity and read the complete card.

Unknown technical changes, unavailable/oversized evidence and uncertainty stay
pending. At `review_exceptions`, ordinary work is exhausted: preserve and report
the exact maintenance checkpoint; do not poll it, certify no change, finalize or
mark the goal complete. Appropriate explicit maintenance uses the returned command
and [review-integrity.md](references/review-integrity.md). Full submit/revise and
fragment instructions apply only to maintenance or separate downstream approvals.

## Finish the workflow

A next/reply command can remain quiet while code prepares a large directory/site
build. If the tool returns a running numeric session_id, wait on that process.
Do not resubmit the answer, restart acquisition or call the run complete. After
it exits, follow its actual returned state or refresh checked next once.

The same checked next/reply route now runs routine report mapping, exact-ID
directory projection, roster reconciliation and build checks in code. Do not
create large receipts or re-review unchanged rosters. Missing legal metadata,
ambiguous identity/scope and evidence failures are compact semantic cards using
the same handle/stdin interface.

At publication_acceptance, approve the supplied current entries/changed directory
rows with an actual substantive reason; correct a named opinion entry using its
N-reference; or return unresolved. Code owns all receipt fields and appends
source-bound corrections before rebuilding. A correct citation does not establish
legal accuracy. Do not claim independent human/browser review. Code checks exact
artifact bytes and current report/directory serialization.

After approval, publish mode finalizes/exports/integrates automatically. Follow the
returned workflow release --execute command under existing publication authorization;
--merge permits ordinary merge only after CI, and --wait waits internally for CI,
merge and exact live-data verification. Wait on the existing process; do not launch
another or manually recreate its branch/PR. Preview completes without production
writes. Read [publication.md](references/publication.md) for checkpoints/recovery.
Only publication_complete means deployed; partial runs never become completed.

At publication_exceptions preserve the checkpoint. Use its checked retry command
only when an actually corrected semantic answer is available. Do not poll it,
reacquire, reset, create a receipt schema or certify missing evidence as no-change.
Legacy downstream receipts are maintenance compatibility, not mandatory reading.

Public updates describe supported material changes and practical effects. Never
insert research-incomplete notices or source-reconciliation narratives under
public headings. Exclude unsupported/inconsequential news claims. Keep provenance,
conflicts and gaps internal; never fabricate completeness.

Keep a short RESUME.md with exact paths and next command. Use returned review_progress
counts, including total_sources/reviewed_sources/machine_reused_sources/pending_sources,
and link RUN/agent-steps logs; do not reconstruct counts or abbreviate hashes/paths.
At an authorized stopping point, return handoff_text verbatim as the entire final response (five bullets,
<=120 words), without an introduction or postscript, unless the user asks for detail. Do not inspect task/log directories
or reconstruct counts. Handoff text is not a stop signal; continue required
stages within the authorized scope. Link the supplied checkpoint for details.
Report actual failures and verification evidence. Mark the goal complete only
when all authorized deliverables are verified; honor user pauses and goal-tool
blocking rules. Do not restart inference servers, unload models, install packages
or launch another worker. Explicit isolated test assignments use their own trial
instructions and parent-owned goal limits; they do not authorize production runs.
