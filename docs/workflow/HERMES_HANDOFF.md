# Resume an existing update in Hermes

From the current checkout, run:

```sh
python3 scripts/resume_hermes.py --check
python3 scripts/resume_hermes.py
```

The default profile is `personal-code`. The script uses its configured model and
permissions without changing them. It opens an interactive Hermes conversation
with this handoff as its initial request. It does not start a local worker, switch
providers, bypass approvals, initialize a run, retrieve sources or publish data.
Use `--run-dir PATH` for a different existing run and `--profile NAME` only when
the user requests another profile. Do not run two agents against the same queue.

## Objective and first action

Complete the saved update from the last finalized reporting period through the
contract's cutoff: seven-court opinion discovery/status checks, registered-source
hash comparisons, supported civil/commercial law and personnel reviews, validated
database persistence, current website publication and live verification. Preserve
historical reports. Partial runs must not advance the finalized reporting baseline.

Read the checkout's `AGENTS.md`, the run's `RESUME.md`, and
`skills/florida-update/SKILL.md`. Apply Cade's writing guide to substantive prose;
its maintained source is
`/Users/cadespivey/Developer/CodexSkills/cade-writing-style/SKILL.md`.
This Hermes handoff supersedes runtime-specific Codex entry-point requirements:
use the repository-bundled Python launchers below, without installing Codex or
requiring Codex session/goal tools. If Hermes exposes goal tracking, attach this
objective; otherwise maintain the objective, next action and status in `RESUME.md`.
A missing Codex goal tool is not a research blocker. Do not claim the Codex goal
was transferred or completed.

After confirming no earlier workflow command is live, refresh the pointer once:

```sh
python3 skills/florida-update/scripts/review_step.py --checkout "$PWD" next --run-dir RUN
```

Replace `RUN` with the absolute run directory supplied in the initial prompt.
Read the complete returned card. Submit one semantic JSON answer through the
exact returned run-local `review HANDLE` command. Follow the next card returned
after success; do not request it twice. Wait for an actual running command rather
than restarting it. A lost output permits one checked `next` recovery. Database
and code-issued handles are authoritative; old handoff counts are dated snapshots.

For other FLWU commands use:

```sh
python3 skills/florida-update/scripts/flwu.py --checkout "$PWD" COMMAND
```

Do not use bare `flwu`: another editable installation may target the wrong checkout.

## Keep the review bounded

Code determines byte, content and status changes. Reuse verified baseline reviews
and inspect the supplied meaningful differences; do not reopen unchanged research.
Focus on civil/commercial case law, statutes, bar rules, practical court procedures
and court personnel. For family, criminal and diversionary divisions, contacts,
assignments, official links and basic operating instructions suffice. Do not
review decorative seals or expand this run into fresh county baseline research.
An explicitly bounded text/contact review must not claim whole-file equality.
Unknown substantive changes or genuinely missing evidence remain accurately
recorded exceptions, not invented no-change decisions.

Complete one judge before moving to the next. Preserve original bytes, URLs,
timestamps, stated dates and documented conflicts; do not resolve conflicting
authorities as a separate project. Current roster information is not proof of a
new appointment. Retrieval dates and revision labels are not inferred effective
dates. Public summaries explain supported material changes and practical effects,
with citations. Do not add research-incomplete disclaimers, evidence-coverage
sections or source-reconciliation narratives to public pages.

Normal review uses the compact card and code-owned receipts. The current run also
has an explicitly authorized embedded-document repair. Its exact next step,
remaining document reviews and saved acquisition locations are in `RESUME.md`
and `maintenance/embedded-wrapper-repair/README.md`. These documents have already
been downloaded; do not reacquire them. Use the saved comparison helper for one
judge only when handling that maintenance, not as a replacement for normal cards.
Do not use scripts to manufacture legal/relevance verdicts.

## Completion and handoff

Continue through the coordinator's source, opinion, exception, current-directory,
report and publication stages. Review exceptions do not authorize finalization.
Use the actual returned commands and the current
`docs/workflow/DETERMINISTIC_PUBLICATION.md` instructions for acceptance and release.
Verify current database persistence, current website data, the displayed date
window/buttons and expanded headings. Do not audit historical reports.
Starting a background process, producing a queue, making a commit or exiting a
Hermes turn is not completion. Preserve the next action and process identity when
interrupted. Report completion only after `publication_complete` and live-content
verification. Existing authorization covers ordinary validated publication; do
not infer authorization for force pushes or destructive recovery.

The local run directory and shared SQLite database are intentionally outside Git.
They must stay in place on this Mac; a Git clone alone cannot resume the research.
Do not copy the live database with an ordinary file copy or publish raw captures.
