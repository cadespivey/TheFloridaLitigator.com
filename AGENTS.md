# The Florida Litigator: current instructions

This project publishes reviewed Florida civil/commercial law updates and court
personnel directories. The statewide baseline is complete within its saved scope;
refresh it through the weekly workflow rather than restarting county collection.

## Start and continue

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

For a new statewide run, reconcile the ongoing registry with all 67 reviewed
county directories. Preserve exact source URLs/IDs and pinned existing registries.
Registration is not review. Use the current registry/setup commands from the skill.
The default baseline is the last finalized report's period end, not a partial run
or later publication date; explicit user dates override defaults.

For research use the invoking selected model. Do not restart inference servers,
unload models or launch another worker. Development work follows the user's
development/delegation instructions. Research uses the existing environment;
do not install packages or change machine configuration to complete a review.

## Review only the returned task

Code handles acquisition, raw/content/component hashes, opinion status changes,
proven reuse and version checks. Standard acquisition independently discovers
opinions for the Supreme Court and all six DCAs. Do not reopen reused sources or
create hostname/keyword-based no-change classifiers or automatic verdict scripts.
Derived caches are computation, not evidence or completed review.

Read the returned guide and receipt template. Consult a detailed reference only
for a specific question. Optional comparison artifacts do not add mandatory raw
review; fill `raw_change_review` only when the current template includes it.
Required same-text raw review, changed PDFs/statuses, failed extraction and
unknown differences retain their gates. HTTP 200/loading stubs are not completed
source retrieval. Unclear technical evidence stays unfinished; do not invent a
harmless-script explanation or claim identical browser behavior from equal text.

Preserve prefilled quotations, hashes, timestamps, paths and finding versions.
Use supplied exact-quote helpers for blanks; do not retype quotes or write parsers.
Finish one person/source task before the next. Preserve all nested facts when
updating a person. A successor uses a separate stable person key and judge/clerk
kind; roster removal needs explicit evidence, not omission. Omit unreviewed new
contacts rather than inventing absence searches. Record distinct contact purposes
and source conflicts internally without deciding controlling authority.

Keep failures and exact errors. Use the returned correction/revise command and
predecessor; accepted history is append-only. After two rejected drafts use the
existing repair checkpoint. Do not repeat guesses, edit accepted evidence or
manufacture citations to clear validation.

## Scope and writing

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

## Save, publish and develop

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

Current development direction is [SMALL_MODEL_REPAIR_PLAN.md](docs/workflow/SMALL_MODEL_REPAIR_PLAN.md).
The expanded schema/catalog plan is withdrawn. Do not expand fragment paging or
invent a new model-facing receipt language. The smaller-answer interface is a
proposal requiring a short pilot, not an active schema or a claimed speed gain.
Older instructions are retained in AGENTS_HISTORY_20261109.md for lookup only.
