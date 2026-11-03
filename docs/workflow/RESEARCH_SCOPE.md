# Bounded research scope

This is the current research purpose and stopping rule for the skill, agents,
module contracts, runbooks and trials. It supersedes broader research examples,
old task lists and exhaustive-review language. The project identifies and briefly
summarizes changes Florida civil litigators are likely to encounter, with a
commercial-litigation priority. It is not a comprehensive legislative or
regulatory monitoring service.

## Included work and primary sources

| Category | Where to look and what to establish | Stop condition |
| --- | --- | --- |
| Case law | Independent official opinion discovery for the Florida Supreme Court and all six DCAs; official opinions and correction/substitution/withdrawal notices. CourtListener may supplement discovery/access. | Screen civil/commercial relevance; for relevant changes save a short supported holding, disposition, attributed authors and source links. Do not investigate the underlying lawsuit or expand into specialized criminal/family merits. |
| Statutes | Online Sunshine's Florida Statutes and official enacted chapter laws; use legislative bill/status pages only as needed to verify enactment, changed text and stated dates. | Preserve the entire statutes compilation as the comparison corpus. Substantive review covers relevant actual statutory changes, not every chapter or pending bill. Distinguish enactment from a future effective date. |
| Bar rules | Official Florida Supreme Court adoption opinions/orders and Florida Bar rule texts. | Summarize material adopted changes affecting civil practice and their stated timing. A proposal or request for comments remains a proposal; no comprehensive rulemaking history or disciplinary-case research. |
| Court procedural rules | Official statewide rule amendments/compilations, local rules and individual judges' published procedures. Review administrative orders when they materially affect filing, hearings, access or shared civil operations. | Capture the practical change and link to the governing instructions. Do not analyze every order, appendix, form, calendar or motion-specific requirement. |
| Judicial-system personnel | Official court/circuit/county rosters, individual profiles, assignment notices and clerk pages. | Finish one person's supported name, role, assignment, chambers/office contacts, JA or other published support contact, and procedure links before the next. Use one complete canonical projection; preserve distinct office purposes and source conflicts. |

Practical civil priorities include jurisdiction, contracts, entities, commercial
transactions, property, foreclosure, collections, remedies, evidence and appellate
practice. Primarily criminal, family, juvenile or diversionary assignments require
contacts, assignments, official links and basic scheduling/submission/appearance
instructions, not specialized substantive review.

Executable entry points are in `config/sources.json` and
`src/flwu/data/opinion_sources.json`; county-specific source maps are in
`docs/research/counties/`. Prefer Online Sunshine (`S01-02`) for the statutes
compilation, official chapter/enactment materials for actual amendments, and
Supreme Court/Florida Bar official rule texts for rule changes. A registry entry
is a discovery lead, not a requirement to analyze every item on that site.

## Scope gate before additional research

1. Identify the included category and the specific changed-law question or missing
   personnel/operating field the next search or document would answer. A generic
   keyword, a saved document, a website heading or a queue item does not expand scope.
2. Use the standard acquisition and hash/status gates. Code determines source
   changes and reporting boundaries; the model interprets only returned work.
   Do not reopen `reused_reviews` or completed machine mapping receipts.
3. Screen a new candidate using its title, official status, dates and enough
   source context to establish relevance. Follow a further link only to support
   an included change or required personnel/practical-procedure field.
4. Pending legislation, rule-development notices and general agency regulation
   receive only brief screening or enactment/adoption verification needed for an
   included category. Save a link and minimal status/date context when useful.
   Do not track every stage, assess likely passage, analyze proposed legal effects,
   or study finance/licensing/program forms and penalty schedules. Commercial
   subject matter alone does not authorize an agency-regulation research project.
5. For out-of-scope material already collected, preserve the original evidence
   and record a concise cited scope disposition using the exact returned schema.
   A publication mapping uses `decision: "exclude"` and `candidate: null`; it does
   not require a new substantive opinion about the proposal. Keep separate court
   personnel projections when they are actually supported and needed. Never call
   unreviewed linked content reviewed, or a failed source unchanged.
6. Stop when the supported short update or required personnel field/checklist is
   complete. Do not add research merely to make every retained document fully read.
   Preserve each official conflict with its source and dates; resolving which
   authority controls is not a baseline or publication requirement.

An adopted rule or enacted statute with a future effective date can be relevant
now as an actual adoption/enactment. Label its present status accurately. Pending
proposals are not operative law. A hearing/comment date, retrieval timestamp or
index link is not an adoption, posting or effective date.

## Persistence, continuation and completion

Use the pinned coordinator command and database. Originals, URL, retrieval time,
SHA-256, extraction, stated dates, findings and review outcomes remain in the
append-only research history. Save receipts at the returned paths in the private
run directory. Keep documents collected, content reviewed and conflicts recorded
distinct; do not invent fields outside a generated receipt's contract.

Existing out-of-scope evidence stays preserved. Do not expand future registries
with unrelated proposal/agency links or reacquire them merely to finish an old
note. Do not rewrite a pinned registry/contract, delete evidence, or restart the
run to apply this scope. Resolve required old packets with bounded dispositions;
review the ongoing registry's scope before a subsequent acquisition.

Success is a source-supported update and current personnel data, with deterministic
change/reuse provenance, saved database findings and the authorized current website
publication verified. Required packets still need valid dispositions. Genuine
missing in-scope evidence needs attention; documented conflicts and intentional
nonreview of out-of-scope detail do not demand exhaustive research. Completion
does not require an all-bills report, full FAR issue/body review, regulatory advice,
every linked form, or historical-report audits.
