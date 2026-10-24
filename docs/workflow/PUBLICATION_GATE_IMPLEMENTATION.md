# Publication integrity hardening — active implementation

User objective: reconcile every relevant finding to publication or supported
exclusion; bind report references to saved acquisition metadata; reject invented
personnel and reconcile rosters; require supported no-change reviews; separate
screening from final publication acceptance.

## Authoritative regression evidence

The October 16–22 run / PR104 saved 44 relevant opinions but published zero items
in all four sections. Source scripts generated 374 no-change receipts using domain
and keyword templates, including an unreadable-source dismissal. Report generation
substituted same-host pages, replaced retrieval timestamps/HTTP status, inserted
Chief Judge/Court Clerk placeholders and set reconciliation flags. These receipts
passed existing structural validation. Full run artifacts remain local under
runs/updates/weekly-2026-10-22. Do not execute those generation scripts again.

## Implementation plan and acceptance evidence

1. Source review support: current quoted evidence plus substantive rationale;
   changed-source no-change review additionally binds previous evidence. Missing
   extraction stays pending. Version the acceptance gate so old unsupported
   receipts are not reused. Tests must reject the actual shortcut classes.
2. Evidence binding: exact original/extraction pair, URL, retrieval timestamp and
   HTTP result from immutable acquired observations. Same host is not same source;
   report-local file integrity is insufficient. Bind before research acceptance,
   again before finalization/export. Provide a supported mapping path so the model
   copies verified metadata instead of reconstructing it.
3. Identity/roster: reject placeholders/headings/locations; quote the actual full
   person name; roster acceptance must reconcile expected identities against the
   official source inventory, not a boolean or a count alone. Keep stable IDs and
   require explicit evidence-backed dispositions for additions/removals.
4. Publication reconciliation: bind report to an acquisition run and snapshot of
   reviewed findings. Every relevant finding must map to an actual included
   candidate/item or a supported explicit exclusion. Reject omissions, duplicates,
   stale review versions, unrelated mappings and empty report with relevant findings.
   Preserve late-posting semantics and do not silently redefine overlap as excluded.
5. Separate publication acceptance: a reviewed, immutable acceptance receipt must
   pin report bytes, capture, reconciliation and actual legal/visual checks. A
   screening receipt or passing research status is not this approval. Finalization
   and export enforce it; no alternate CLI path bypass. Synthetic test previews
   remain clearly distinct from production.
6. Update intents/specs/tests/runbooks and installed florida-update skill with
   executable commands and exact templates. Test actual CLI positive and negative
   paths using disposable databases, then full suite and current-publication checks.
   Do not recheck historical reports. Existing records remain preserved; explicit
   remediation of the erroneous latest finalized issue/baseline must be addressed
   before claiming current publication trustworthy, not hidden by new validators.

## Current checkpoint

Branch codex/publication-evidence-gates. Changes remain uncommitted; production DB
and website have not been modified. Source support v2, identity citation checks,
exact acquisition metadata binding, and separate publication acceptance are now
implemented with initial regression coverage. Acceptance requires explicit
relevant-finding dispositions and named roster evidence. Finalization/export call
the acceptance gate rather than treating screening as publication approval.

The latest verification completed with 647 tests passing in 6.37 seconds and
`git diff --check` passing. Two new regressions prove that later review activity
does not rewrite a previously accepted export, that stale reports cannot receive
new acceptance/finalization, and that sequence zero does not expose later evidence.
These tests use disposable databases; no historical production report was checked.

Research inspection now requires the exact task URL among acquired pages and honors
the database pinned by the prior capture marker; conflicting overrides fail before
opening another database. Regression tests cover genuine same-host substitution
and resume/override behavior. SOURCE_HASH_REVIEW.md now documents support receipts
and separate acceptance commands.

Still incomplete: acquisition-run linkage,
stronger roster reconciliation, substantive changed-text review coverage,
export snapshot/concurrency review,
remaining CLI/workflow/skill documentation, and explicit remediation of the erroneous latest
public issue. Passing tests are not evidence that those remaining requirements
are satisfied. Next implement those requirements and update their behavioral tests.


Acceptance and finalization now reserve the SQLite writer before validation and
hold that reservation through persistence. Regression tests use a second real
connection to prove a competing write fails during validation, then succeeds
after release. Failure rolls back without storing approval or advancing a report.
Malformed disposition IDs, candidate keys, citations, and roster identities are
rejected with validation errors. Current full suite: 627 passed; diff check clean.
No production database or website mutation was performed at this checkpoint.


Roster consistency checkpoint: person-task names are pinned to the discovered
roster identity; conflicting identities cannot silently share an ID. Publication
requires exact equality between named roster IDs and personnel finding IDs, plus
matching names and judge/clerk roles. Added regressions for missing/unrostered
people, name/role mismatch, and conflicting IDs. Full suite: 633 passed in 6.25s;
diff check passed. Official-roster completeness and prior-roster removal accounting
remain separate unfinished requirements; these tests prove consistency only.


Removal-accounting checkpoint: generated acceptance templates compare each roster
with the latest finalized predecessor and list removed IDs/names. Validation
requires every removal to have a substantive reason and acquired quoted evidence,
including when a whole inventory disappears. Added an end-to-end disposable DB
regression: finalize initial named roster, reject unsupported removal, accept
and finalize a cited retirement. Full suite 634 passed in 6.24s; diff check clean.
Official roster completeness and acquisition-run linkage remain unfinished.
Production data/publication remain unchanged.


No-change coverage checkpoint: source acceptance version 3 requires quotations
covering every nonblank changed extraction line on each side. Queue export supplies
those deterministic line lists alongside the diff. Changed sources cannot use
baseline_reviewed to bypass comparison. Old receipt versions are neither reused
nor accepted through exact-replay shortcuts. Regressions reject unchanged-heading
support, partial change coverage and baseline bypass; full suite 636 passed in
6.26s, diff check clean. Semantic significance still needs actual reviewer judgment;
quote coverage cannot prove the legal conclusion. No production mutations.


Skill/invocation checkpoint: installed florida-update SKILL.md and publication
reference now require exact acquisition bindings, supported reviews and separate
publication acceptance. AGENTS.md routes agents to these gates. Added actual CLI
regression for template creation, incomplete acceptance rejection, successful
accept/finalize, and rejection after report bytes change. Full suite 637 passed in
5.86s; diff check clean. Pinned launcher confirms new history actions. Skill
quick_validate.py could not run: PyYAML is absent in both tested environments;
no packages installed. Direct checks verified frontmatter, fences, references and
absence of TODO scaffolding, but are not a replacement YAML-validator pass.
Production remains unchanged; goal requirements still incomplete.


Acquisition-link checkpoint: acceptance now pins the latest matching saved
standard-update result before the report capture (target stream, reporting dates,
run ID, capture ID and queue hash). Missing/corrupt queue bytes or edited bindings
block acceptance. Fixtures now save real update-result artifacts; regressions
cover mismatched run binding, corruption and unmatched reporting dates. Full suite
640 passed in 5.90s; diff check clean. Remaining: reconcile unresolved acquisition
queue entries/coverage to explicit dispositions rather than only bind the result;
verify official roster completeness; complete specs and current-publication repair.
Also observed status-source records lack success/http_status fields needed by the
new acquisition index: inspect and correct that producer/consumer mismatch next.
No production writes at this checkpoint.


Opinion status evidence checkpoint: bind_status now saves actual http_status and
success with URL/time/raw and metadata hashes. Accepted opinion citations copy
actual HTTP status when available. AcquisitionIndex can reuse legacy parent-event
transport metadata only when URL, retrieval time and raw hash exactly match the
entry; it never invents defaults or mutates old records. Regression exercises
actual standard update, then validates status evidence and rejects HTTP mutation;
legacy tests reject URL/time/hash mismatches. Full suite 645 passed in 6.38s;
diff check clean. Pending queue reconciliation and official-roster completeness
remain unfinished; current bad publication still requires remediation.


Pending-queue reconciliation checkpoint: publication_pending.py enumerates every
source/opinion task, effective-date trigger, unregistered source and discovery
failure from the exact bound queue. Acceptance requires one explicit disposition
per item. Available unread evidence cannot be labeled unavailable. Scope exclusions
require acquired quoted support and matching task-source hash where present.
Instructions require completing in-scope reviews and refreshing the queue before
report capture; limitations never become no-change conclusions. Added regressions
for omission, unread-as-unavailable, unsupported exclusion, genuine retrieval gap,
and all queue categories. No production changes. Still required: complete coverage
and semantic review audit, specs, integration/release and faulty-publication repair.

Current-report correction checkpoint: implemented immutable report_invalidations
and history invalidate CLI. Baseline selectors in history comparison, opinion
discovery and roster reconciliation skip explicitly invalidated reports. Acceptance,
finalization and export reject invalidated captures. Disposable regression verifies
no capture/artifact/finalized-report deletion, replay, immutable explanation,
baseline fallback and refusal to invalidate an unfinalized capture. Production
has not been invalidated yet; public withdrawal still needs implementation.

Public withdrawal checkpoint: site build accepts separately hash-bound withdrawal
notices while preserving issue originals. Withdrawn issues are omitted from normal
selection/search/directory data; direct issue links show a text-only notice. Prepared
notice for update-1ac57a75b9533bce63e0 without modifying its archived JSON. Full suite
652 passed in 6.34s; JS syntax and diff checks passed. Current production-shaped build
using every Pages supplement argument succeeded: five eligible issues and 68
supplements; faulty issue excluded and withdrawal present. No historical report
re-review performed. Production DB invalidation and deployment still pending.


Current authoritative checkpoint — October 24, 2026 UTC:
PR105 merged as 926efe2. Production SQLite backup completed with quick_check=ok
at ~/.local/share/flwu/backups/pre-publication-invalidation-20261024T024714Z.sqlite.
The faulty capture 1ac57a75b9533bce63e09d2c505402e798c4f198d6801e52ccc44c06d595052e
was explicitly invalidated at 2026-10-24T02:47:56.815126+00:00; captures and original
artifacts remain intact. Its stream now has no valid finalized baseline, so a new
run requires an explicit start. These facts supersede earlier unchanged-production
checkpoint statements above.

Public withdrawal is committed but not yet deployed: main Pages run40055688597
failed in a county test that incorrectly required withdrawn issues to remain in
the built site. The repair replaces production-archive dependencies with synthetic
current/withdrawn fixtures and asserts both filtering and preservation of original
archive bytes. The complete suite with the withdrawal notice present passes:
652 tests in6.35s. Deployment/live verification remains pending.

Substantive replacement remains unfinished. Eight of44 previously relevant opinion
findings have individual correction drafts under the private run correction-review
workspace. Drafts are not publication acceptance or finalized findings. The next
unreviewed saved original is doc_41e5e772ac4432d26f74c7cc. Continue source-backed
review, then persist supported corrections and reconcile source/roster/pending
requirements before final acceptance. Do not rerun the old receipt generators.

Latest checkpoint — October 24, 2026, 03:12 UTC (supersedes counts above):
The faulty issue's withdrawal is deployed and verified in the live archive.
All 44 previously relevant opinions have individual correction drafts; 43 supported
corrections are persisted and independently read back (12 include, 31 exclude).
The remaining Dorticos response is a login page and remains an evidence gap.
Private persistence-audit.json records capture IDs, receipt digest checks, raw/text
hash checks, quotation containment, and citation URL/time consistency. These are
screening corrections, not a finalized replacement report.

HTML extraction now reads Florida Courts Next.js page/panel data and encoded
custom-tag HTML without executing JavaScript. Malformed known embedded content
fails extraction rather than silently accepting partial text. First DCA's saved
homepage demonstrated the defect: contact/news panels and the 2027 holiday order
link were absent from its previous extraction. Its reviewed derivative preserves
the original bytes and acquisition timestamp. Newly retrieved Order 26-2 states
August 5, 2026; discovery in October must not be represented as October issuance.
The updated complete local suite passes 661 tests in 5.78 seconds.

Source task dispositions, roster reconciliation, replacement report mapping and
separate legal/visual publication acceptance remain incomplete. CI security PR107
is blocked by the hosted Node runtime security floor; do not bypass that guard.
