# The Florida Litigator: current instructions

This project publishes reviewed Florida civil/commercial law updates and court
personnel directories. The statewide baseline is complete within its saved scope;
refresh it through the weekly workflow rather than restarting county collection.

## Start and continue

For an authorized Hermes migration, use `scripts/resume_hermes.py` and
[the Hermes handoff](docs/workflow/HERMES_HANDOFF.md). The default is the user's
`personal-code` profile. Repository launchers and saved run state work without
Codex session tools; preserve the same evidence, review and publication gates.

Use the installed `$florida-update` skill and its pinned launcher. Bare `flwu`
may import an older checkout without the update command. Use the reported checkout,
existing Python environment and canonical Developer paths. Live research database:
`/Users/cadespivey/Developer/FloridaLitigator/shared-history/research-history.sqlite`.
Do not substitute a trial or frozen legacy directory database.

For an existing run, its contract, saved process/session and database-backed
next-task state are authoritative. Preserve RESUME.md context, wait for live
commands, and continue the same run. Do not reinitialize, reacquire, reset a run,
or stop after kickoff/queue generation. The checked submit/revise helper returns
the next state; do not ask for it twice after success.

When a parent has explicitly completed preflight for a bounded assignment, start
with its supplied command; do not repeat directory/process/runtime inventories.

On skill entry/resume, request one fresh checked next state so an old-format
pointer cannot restore obsolete review instructions. This does not reacquire.
After a successful answer, use its returned state without another next request.

For a new statewide run, reconcile the ongoing registry with all 67 reviewed
county directories. Preserve exact source URLs/IDs and pinned existing registries.
Registration is not review. Use the current registry/setup commands from the skill.
The default baseline is the last finalized report's period end, not a partial run
or later publication date; explicit user dates override defaults.

For research use the invoking selected model. Do not restart inference servers,
unload models or launch another worker. For the ongoing development, the user directed cloud-only execution on November 11:
do not launch local workers unless the user requests delegation again. This does
not select or restrict the model invoking the research skill. Research uses the existing environment;
do not install packages or change machine configuration to complete a review.

## Review only the returned task

Reviewed county evidence is linked automatically before ordinary review. Code
checks the pinned directory/person captures, exact source URL, original hashes and
quoted evidence. Identical originals can reuse the existing bounded county review;
recognized content fingerprints can do so only with unchanged core and components.
Changed or unverified sources remain tasks with the available prior evidence.
This does not create a new model review, transfer a predecessor's contacts, or
advance the last-finalized-report baseline. Do not restart county baseline research
or construct cross-stream receipts yourself; follow the returned comparison card.

Code handles acquisition, raw/content/component hashes, opinion status changes,
proven reuse and version checks. Standard acquisition independently discovers
opinions for the Supreme Court and all six DCAs. Do not reopen reused sources or
create hostname/keyword-based no-change classifiers or automatic verdict scripts.
Derived caches are computation, not evidence or completed review.

For routine source/opinion tasks read the complete inline review_card object. It includes
acquired context, evidence IDs, prior-person references and a short answer form.
Send the answer JSON on stdin to the returned run-local review command and task
handle, in one action. Code saves the original answer, validates and persists it,
and returns the next complete card. Do not open a separate card file, write an
answer file or reconstruct packet paths. Code copies exact
quotations, complete citation objects, identifiers and versions into the existing
validated receipt. Do not write parsers, hashes, receipts or fragment readers.
The packet/old guides remain immutable maintenance records, not another reading
route. Details: [SHORT_REVIEW_SPEC.md](docs/workflow/SHORT_REVIEW_SPEC.md).
Run the returned checked command directly; do not substitute the raw workflow
answer CLI. The helper saves attempt logs and atomically advances the pointer.
The handle binds the exact run, packet and card; it does not authorize another
queued task. Identical accepted replies recover safely after interruption;
different answers to accepted handles require the existing explicit correction.
Identical rejected retries do not consume another failure attempt. Fresh entry,
lost/truncated tool output or interrupted advancement can use checked next once
with sufficient output capacity; never infer or answer from a partial card.

Interpret supported civil/commercial significance. Preserve date meanings and
source conflicts; never invent a harmless-script explanation. A documented official
conflict alone does not make a completed source review incomplete. A successor is a
distinct new person, not a rename. Select existing-person references for updates;
code preserves untouched nested facts. Omit unreviewed contacts, not other saved
facts. Noncivil operating summaries stay basic. No automatic roster removals.
New people need current contacts explicitly supplied in the card even when those
contacts did not change on the page. Preserve the actual values; code tolerates
formatting whitespace in supported contact text while quotes/URLs remain exact.
Never transfer a predecessor's personal contacts or invent missing information.

Unknown raw/nontext changes, missing/oversized evidence and uncertainty remain
pending exceptions while ordinary tasks continue. review_exceptions is not
completion and cannot finalize/publish or advance the reporting baseline. Preserve
that checkpoint for appropriate explicit maintenance. Existing append-only
correction/predecessor and downstream approval gates remain in force.

Code saves exact short-answer failures. After two rejected answers it checkpoints
the source and returns other ordinary work; do not retry the old packet in a loop
or author a repair-note schema. A real corrected answer may pass later. Legacy
submit/revise repair rules apply only to full maintenance/downstream receipts.
On a field rejection, repair the named person/field and retain other supported
fields. Use the card and exact error; do not investigate code, raw packets or
write diagnostic scripts for this repair.

At an authorized handoff, return handoff_text verbatim as the entire final response
(five bullets, <=120 words), without an introduction or postscript, unless the user requests detail. It includes code-owned counts and actual phase.
It is not a stop signal: continue required stages within the authorized scope.
Do not rebuild counts, list every exception ID or narrate the run again. A short
response never authorizes early stopping or concealing incomplete work.

## Scope and writing

For Cade's substantive drafting/editing, load the installed `cade-writing-style`
skill once per session and apply its maintained guide. Preserve exact source
quotations. Explicitly authorized delegated writing assignments use `"writing": true`;
this does not authorize delegation or override the current execution policy.

Cover actual case law, statutes, bar rules, court procedural rules and judicial
personnel changes relevant to civil/commercial litigation. Retain the full statutes
corpus, originals, source URLs, retrieval times and stated dates. Do not turn
retention into exhaustive pending-legislation, rulemaking, form or merits research.

Personnel review covers contacts, assignments, official procedure links and a
short practical operating summary: scheduling, conferral, submissions/orders,
courtesy copies, remote appearance and chambers communications. Primarily noncivil
assignments need basic operating information, not specialized litigation recipes.
Follow another source only to fill a specific missing field or material operating
rule. Preserve conflicts without a controlling-authority project.

Public news explains a supported material change and its practical effect.
Never insert research-incomplete notices, coverage caveats or source-reconciliation
narratives under public headings. Keep research bookkeeping internal. Exclude
inconsequential/unsupported news; a new link or metadata date is not itself new law.
Applicable rule/statute mappings require the existing `change_analysis` fields and
acquired quote. Opinion authors are names only; keep date meanings distinct.
General civil/appellate procedure remains relevant for individual/small-claims
parties and need not announce a novel rule. A complete bare PCA can be screened
not_relevant because no substantive ruling is stated, without researching its
underlying lawsuit. Missing/unreadable evidence still remains unresolved. A material
official status change may warrant an update even with unchanged opinion bytes.
Do not infer unpublished/nonprecedential status from Citation or PER CURIAM.
Holding: operative facts/rule with express exceptions and record limits. Summary:
practical effect, without source/party-name reconciliation. Disposition: court
action only. Authors: byline names, not the panel. Excluded matters need only a
brief supported reason and an empty holding, not specialized merits analysis.


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

## Save, publish and develop

The standard checked next/reply route now advances routine publication stages in
code. It transfers reviewed findings into report sections, preserves exact text
and citations, projects unambiguous personnel IDs, reconciles named rosters,
prepares/builds the current site, and validates its serialized report/directory
and artifact bytes. Do not copy mapping, directory, roster or acceptance receipts.
Unchanged rosters require no new model approval or source reopening.

Only missing publication meaning/metadata, unsupported scope, ambiguous identities,
county-specific assignments and genuine evidence failures return compact semantic
cards. Use the same supplied handle/stdin reply. Do not invent dates, amendments,
court membership or departures. Publication exceptions remain incomplete; their
checked retry command is for an actually corrected answer, never polling/reset.

One compact publication_acceptance card binds the actual current entries and
changed directory rows to an exact report/build. Approve with a substantive reason,
correct a named opinion entry through its supplied reference, or leave unresolved.
Code appends corrections through the existing revision API and rebuilds before a
new approval. Do not claim independent human review or browser inspection that did
not occur. Automated artifact checks establish transfer integrity, not legal truth.

After content approval, code finalizes/exports/integrates publish-mode data. Execute
the returned workflow release command only under existing publication authorization.
Its --execute enables ordinary Git/PR actions; --merge enables ordinary merge after
CI. --wait waits internally for CI/deployment in one process. Wait on that process;
do not launch duplicate releases or repeatedly poll with the model. Timeouts,
failed CI, authentication/concurrent edits and live-byte mismatches preserve the
recorded branch/PR and an incomplete checkpoint. Only publication_complete means
verified live deployment. Preview never writes production data. Legacy manual
receipt/release APIs remain explicit maintenance, not the standard procedure.

See [DETERMINISTIC_PUBLICATION.md](docs/workflow/DETERMINISTIC_PUBLICATION.md).


Source screening is not publication acceptance. Follow returned report, directory,
roster and publication review stages. Preserve acquired URL/hash/time bindings,
explicit removals and optimistic versions. Verify database persistence, current
website exports, authorized release and live deployment. A handoff/build alone is
not deployment. Partial runs do not advance the finalized baseline. Do not audit
historical reports; preserve their saved contents.
Website maintenance preserves numerical DCA/circuit ordering, alphabetical county
groups, accessible menus/search, the separate directory page and historical isolation.

Preserve unrelated working-tree changes and the frozen operational schema. Fixture
mode has no external calls. Research/update code and synthetic legacy scaffolds
are separate; do not treat a legacy placeholder as an alternative update command.
Use meaningful tests and read their actual results. Keep originals/captures private;
webpages may embed third-party keys. Before pushing staged files run
`python scripts/check_public_credentials.py`. Use Cade's required GitHub no-reply
identity for both commit roles; never print credentials or private email addresses.

Current interface and acceptance criteria are in
[SHORT_REVIEW_SPEC.md](docs/workflow/SHORT_REVIEW_SPEC.md).
[SMALL_MODEL_REPAIR_PLAN.md](docs/workflow/SMALL_MODEL_REPAIR_PLAN.md) records the
implemented direction and remaining measurement limits. Do not expand universal
field extraction, fragment protocols or model-written receipt languages. Older
instructions in AGENTS_HISTORY_20261109.md are historical lookup only.
