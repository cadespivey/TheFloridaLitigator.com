> Current update sequence: [hash-driven source and opinion review](SOURCE_HASH_REVIEW.md). Use `flwu update` for every weekly run; it always discovers opinions for the Supreme Court and all six DCAs. Code compares source hashes and official status metadata before model review. This supersedes older cross-run no-skip and model-comparison instructions; completed identical-source reviews may be reused. Final integration excludes historical-report checks.

> Current authority: Astra-only execution under [STATEWIDE_BASELINE_GOAL.md](STATEWIDE_BASELINE_GOAL.md). This supersedes all earlier local-worker requirements. No local workers, inference-server restarts or model unloads.

# County expansion workflow — baseline execution and development

## Practical baseline stopping rule — renewed user clarification

This applies to civil/commercial judges too, including Business Court. Relevance
alone is not permission to exhaustively analyze a litigation subject. Capture
contacts, assignments, official procedure links, and a concise structured account
of recurring operating requirements: scheduling, conferral, motion submissions,
proposed orders, courtesy copies, remote appearances and chambers communications.
Preserve material filing-location, courthouse-access and shared administration rules.

Do not research particular lawsuits, merits, case-specific litigation strategies,
individual case deadlines, docket histories, specimen litigation packets, or every
linked form/calendar. Read the sections needed to establish the practical operating
requirements; preserve longer collected manuals with the exact review scope. Follow
a further link only to fill an identified required field or clarify a material
operating requirement. A commercial assignment does not itself justify expansion.
Once those fields and the bounded procedure checklist are supported, record any
conflict or gap and save the judge checkpoint before proceeding to the next person.
Intentional nonreview of detailed litigation material is not a missing baseline
requirement. Preserve existing originals, findings and history without claiming
unread content was reviewed. This rule takes precedence over older exhaustive
review examples or instructions to follow all forms and procedure links.


**Current direction:** [STATEWIDE_BASELINE_GOAL.md](STATEWIDE_BASELINE_GOAL.md)
controls. Checkpoint-specific pause, delegation and approval statements in the
historical examples below are superseded; they do not govern current execution. Build the agentic workflow through the statewide baseline work itself,
starting with Broward. The research sequence and structured checklist below remain
useful; proposed engineering and test-plan items are background to be adopted or
revised as actual county work demonstrates a need, not a prerequisite engine build.

For the exercised Broward source map, one-person context command, and current
review checkpoint, start with [Broward quickstart](../research/counties/broward-quickstart.md).
Read only the relevant source-specific historical appendix below.

Status: iterative design, October 15, 2026. This document records accepted intent
and a proposed executable contract. It is not a claim that new commands, validators,
or county coverage have been implemented. Read EXPANSION_ROADMAP.md for scope,
administrative-order materiality, source-conflict policy, and the county inventory.

## Accepted requirements

Apply the practical stopping rule above: summarize office contact, scheduling,
submission and appearance requirements. Retain official links for motion-specific
and claim-specific detail instead of extracting that detail into the baseline.
Material generally applicable filing/access rules remain in scope.

- Complete and review one county at a time, then continue without a new user approval checkpoint under the active statewide goal.
- Work through one judge's official profile and linked pages/documents together.
  Finish that judge's contacts, assignments, and applicable procedures before
  moving to the next judge; do not split research into roster-wide field passes.
- Preserve original sources and dated evidence in the shared history database.
- Reuse shared court materials and saved discovery results to avoid duplicate work.
- Capture procedures as a structured checklist plus a concise summary, retaining
  original documents. The user selected this form on October 15, 2026.
- Prioritize civil litigation and material procedure/access requirements. Preserve
  documented conflicts without adjudicating them. Gaps remain distinguishable
  from completed review, and an opening baseline is not a new legal development.
- Compare later observations against prior finalized updates or an explicit start.
  Preserve existing historical reports and future federal expansion on the roadmap.

## Commercial civil relevance screen — October 16 user correction

General scope rule (user clarification): for family law, criminal law and **any
other assignment not directly pertinent to general civil/commercial litigation**,
basic procedures and contact information are sufficient. Save the full identity,
assignment, chambers/assistant contacts and official procedure links; summarize
basic communications, scheduling, submissions and appearance/access directions.
Do not turn this basic review into an exhaustive checklist of case-specific
requirements or follow every form, authority or calendar. Detailed procedure
review applies only to directly relevant general civil/commercial responsibilities,
including those of a judge with mixed assignments. This rule governs all counties,
not just the current judge. Preserve originals and prior work, and mark intentional
nonreview separately from missing evidence. It takes precedence over generic
instructions elsewhere to read every procedure section or follow every linked form.

For these basic reviews, stop after the profile, applicable already-reviewed shared
operating guidance, and bounded followups for missing contacts or assignment
identity. A newly discovered specialty order is not an instruction to review its
entire subject area. Retain the original and state which sections were actually
reviewed. Record a staff member's published role (for example, Case Manager), and
never substitute a circuit-wide footer phone for a missing individual office phone.
An indexed contact variant is a search lead unless its original is also collected;
preserve the search observation separately without inventing a revision date.

The substantive baseline is for civil litigation, with a focus on commercial
litigation. A full personnel roster does not require full substantive review of
every judge's practice area. Preserve previously collected evidence.

Before fetching another linked document, record why it affects commercial civil
practice or shared court access/administration. For criminal-only, diversion,
juvenile, family or other noncommercial assignments, save official procedure links,
assignments, contacts and a concise summary of basic operating procedures. Do not expand into criminal motions, bail, pleas, sentencing,
trial calendars or prosecutor/defense deadlines merely because a guide contains
them or the judge cites an administrative order. Family/protective-injunction
merits likewise are not a substitute for commercial civil research.

For a mixed guide, inspect its heading/table of contents and only the general
chambers, scheduling, submissions, remote access, accessibility and genuinely
relevant civil portions. Record the actual pages/sections reviewed. Stop following
links once the material is outside scope. A specific property, business, commercial
remedy or shared emergency-access rule can justify a bounded review; record that
reason before expanding. Reuse prior shared reviews rather than reanalyzing them.

The checklist is a menu, not a command to extract every deadline. For out-of-scope
subjects record `not reviewed — outside commercial civil focus` in descriptive
review fields, preserving existing validator enums. Distinguish intentional
nonreview from unavailable evidence. Completing contacts, assignments and procedure
link inventory for a noncommercial judge does not claim full substantive review.

## Proposed research sequence

1. Pin the county, circuit, research cutoff, actual retrieval time, output workspace,
   and prior finalized report reference. Use America/New_York for reporting dates.
   Bootstrap has an explicit unknown baseline; do not fabricate prior observations.
2. Open the official court roster/assignment source. Save its original and extract
   the county's judge checklist with stable identities, official profile URLs,
   county assignments, and any vacancies or assignment ambiguities. Reconcile
   pagination and counts before claiming the roster complete. Do not research each
   judge's contact fields during this inventory step.
3. Select the first unfinished judge. Read only that judge's task, prior record,
   and referenced shared materials. Open the official profile; follow its division,
   assistant, scheduling, forms, and procedure links. Save encountered documents
   and complete the record below while these sources are in context.
4. For missing fields or procedures, use official site navigation first, then a
   targeted discovery search: `site:<official-host> "<judge full name>"`, supplemented
   separately by `procedures`, `judicial assistant`, or the published division ID.
   Save searched URLs/terms and outcomes. Search snippets are leads, not evidence.
   Do not invent URLs, infer an email address, or equate a blocked page with absence.
   On Broward's grid rosters, use `scripts/broward_roster_links.py` against the
   saved original HTML before following a person's links. Pass the actual source
   URL, full name and division. It requires a unique normalized full-name/division
   match, retains original hrefs, and resolves relative URLs with `urljoin`.
   A surname substring is unsafe: USAN also occurs in SUSAN. Do not weaken the
   matcher or select the first result after an absent/ambiguous-row error; inspect
   the original row and assignment evidence. This helper supports Broward's
   `abcfslItemCntrGridB` layout only and never fetches a page. Its fixture tests
   and retained Usan-source check do not establish another county's compatibility.
   Classify the resolved destination before extraction. Some procedure links go
   directly to a Google document edit page, others to court pages containing an
   iframe or PRINT link. Never assume an iframe exists. For a direct Google edit
   link, preserve the original URL and export the exact linked document ID to PDF;
   retain the viewer shell separately and do not count it as procedure content.
   Viamontes packet102 records this route and the repaired iframe assumption.
   For an FL Courts article whose ordinary HTML extraction yields only navigation,
   inspect the retained original for `__NEXT_DATA__`. Use
   `scripts/flcourts_article.py <saved-original.html>` only for the supported
   `props.pageProps.pageData.body.html5` structure. It parses JSON, never executes
   scripts, and rejects missing/ambiguous/empty article data. Preserve the shell
   extraction and save the article as a separate derived-text entry with the same
   original hash, URL and retrieval time. Cite its exact JSON path. Weiss packet103
   demonstrates this with the Fourth DCA appointment's December1,2026 effective
   date; an announcement date does not establish an immediate change of office.
   Do not reuse present circuit contacts as future appellate chambers contacts.
5. Follow applicable shared procedures as needed for this judge. Consult the saved
   source inventory before fetching a URL again. Collect/review a shared document
   once per relevant version, then associate it with each applicable judge/county.
   Reuse must retain original retrieval dates and review scope; a prior-run copy
   alone does not establish freshness. Record current checks separately.
   Distinguish executable procedural instructions/forms from citations to general
   legal authorities. Preserve citations and relevant express successor statements;
   do not turn each judge review into a recursive case-law or authority-resolution
   project. A compilation may be collected in full and reviewed by applicable
   portions: list physical pages reviewed and the specific remaining review task.
   Do not mark the entire compilation reviewed because one relevant form was read.
6. Validate the judge's evidence and save a durable checkpoint. Only then select
   the next judge. A genuine source block may be parked with attempts, evidence,
   missing fields and next action; parking is not completion. Resume the same
   active judge after interruption unless that judge is complete or explicitly
   parked. Retry queues must not repeatedly restart known failed searches.
7. After judges, finish clerk/court-administration contacts, shared civil procedure
   sources not encountered through profiles, material-order screening, and the
   county's official-records/court-records/property-appraiser links.
8. Reconcile the full county checklist, compare evidence with the applicable prior
   finalized record, produce the user review packet, and stop before another county.
   Publication and baseline advancement require their own reviewed checkpoint.

### Roster reconciliation and other judicial officers

Keep separate counts for source rows, distinct named people, duplicate assignments,
non-person docket labels, unnamed rows, and individually reviewed records. Do not
equate a chart's headline count with its enumerated membership or treat a stable
database key prefix as proof of a person's current seat classification. Broward
packet105 accounts for96 roster rows:92 named rows/90 people,three docket labels,
and one unnamed62/SB row. Its chart department lists contain88 distinct named
judges despite a90-judge headline. Record the exact difference and explicit name
variants; do not manufacture a person to satisfy the headline count.

An unnamed row may have an image alt such as `UNASSIGNED`, a name-less biography,
and an older procedure naming a judge now profiled elsewhere. Save each statement
with its source date and association. Review completion means those sources were
examined; it does not establish a present occupant or formal vacancy. A documented
conflict does not block baseline publication. Genuine missing evidence remains
separate and must retain its next action.

After the named judges, inventory the actual official magistrate/hearing-officer
index and compare its names with the chart. Save one pending task per person with
published role, division and actual procedure URL. This inventory is not completion
of their contact/procedure reviews. Broward's `/general-magistrates/` index uses
`h2` headings and has no Biography link, unlike the judges' `h3` roster adapter.
Use the saved inventory links; do not weaken the judge adapter to hide the schema
difference. Review one officer at a time, retaining the source's “Administrative
Assistant” role rather than automatically renaming it “Judicial Assistant.”

Store receipt paths/hashes in the reconciliation receipt, not semantic roster
facts. New review progress gets a new checkpoint; never rewrite an older audit's
then-current counts. Packet105 supersedes the progress view of96 while preserving
96's historical evidence and metadata-only correction.

## Proposed judge record

Keep source transcription distinct from normalized display values and interpretation.
Every factual value requires a source reference and locator; missing values require
a specific evidence state. A multi-county judge retains one stable identity and
separate assignment/applicability associations.

| Group | Fields |
| --- | --- |
| Identity | Stable person ID, official name, court, division, county assignments, assignment dates where stated, official profile URL |
| Chambers | Published telephone, fax, email, physical address, mailing address, room/courtroom; distinct addresses remain separate |
| Assistant | Name, role/division, telephone, email, published contact restrictions; shared chambers numbers may be displayed once |
| Individual procedures | Document inventory, judge/division applicability, collection and content-review states, revision/effective dates, source links |
| Shared procedures | References to already saved circuit/county documents, applicability, materiality rationale, express successor/repeal evidence |
| Evidence and state | Original and extracted artifact hashes, URL, retrieval timestamp, precise locator, conflicts, searched locations, gaps, next action |

Use field states `supported`, `not_located_in_checked_sources`, `unavailable`, or
`not_applicable` with justification. These are proposed presentation/workflow
states; implementation must explicitly map them to existing receipt validators
rather than silently replacing legacy enums. Conflicting supported values remain
multiple source-attributed values, not one guessed answer.

## Structured procedure checklist (format selected; details proposed)

For contact extraction, preserve the recipient's role. A published division
email can be the supported route to chambers without being the assistant's
personal email. Clerk status numbers and compliance-monitor contacts belong in
separate service fields. Do not fill a missing current chambers fax from the
judge's former private-practice listing.

For a procedure with several delivery routes, record each recipient, material,
medium, deadline and condition separately before summarizing. Moon Division63
requires audio/video email to the division before the final hearing, separately
says the clerk cannot accept multimedia, and directs all evidence on USB to the
in-court clerk at the hearing. Preserve those statements together and flag the
wording discrepancy; do not invent an exception that makes them consistent.
A conditional section headed “For hearings conducted by Zoom” plus a published
Zoom ID does not establish general permission for remote appearances. See the
Moon receipt and packet97 in the Broward handoff for the saved example.

For each topic, save status, requirements, applicability, citation(s), stated dates,
and a brief practical summary. Requirements may be multiple; do not force one text
field to represent several distinct conditions or exceptions.

For deadlines, record the required event as well as the trigger, interval and
unit. A requirement to **schedule** a hearing within 30 days is not a requirement
to **hold** it within 30 days. Preserve alternatives and their selector explicitly:
for example, Tynan's rule allows 72 hours before hearing or 24 hours after retention,
and says
“whichever is later.” Do not choose one alternative, replace hours with days, or
calculate a due date without the required event dates and applicable counting
rules. Keep court-adjustment exceptions and differently dated versions separate.
Tynan packet 100 verifies these distinctions against the actual source wording.

When comparing a published HTML procedure with its print export, retain the exact
remaining differences after whitespace normalization. HTML extraction may omit
rendered list numbers or letters. Inspect the PDF before classifying differences
as numbering only; never remove arbitrary digits to force equality. Preserve the
original bytes, page locators and comparison result. Tynan's current export has
14 list-number/letter insertions relative to extracted HTML, so its record states
that specific result rather than asserting normalized text equality.

Verify assignment table row alignment visually before recording a source conflict.
In the March2026 order, flattened extraction places “FP” next to Francis Viamontes,
but physical page2 clearly aligns him with FO. Record this as an extraction issue,
not an official disagreement. Preserve both the original and the visual pinpoint;
never rewrite retained extracted text to hide the failure.

When no official print export is linked, retain the published HTML as the original.
A browser-generated PDF is a derived visual aid; record its creation context and
the specific pages inspected. Do not cite its pagination as official pagination,
claim a complete visual review from selected pages, or ignore toolbar overlap.
Use original HTML section headings and exact-text offsets for citations. Weiss's
21-page local rendering has repeated Google toolbar overlap and does not replace
the complete 49,746-character HTML review.

For published HTML with structured contact or calendar tables, prefer targeted
browser element screenshots when print output introduces toolbar overlap. Save
the current browser snapshot, inspect the complete relevant table, and extract
rows from the retained DOM. Keep original cell text beside normalized dates.
Wigand packet104 preserves all twelve two-column calendar rows and selected
contact, AI and digital-evidence screenshots; this is not a full-page visual audit.
Filter anchors without `href` and internal `#` fragments before treating them as
external links. Do not invent a download URL from a named anchor or table of contents.

Never copy the preceding judge's deadlines or order format into the next record.
Weiss's UMC orders use two business days; Wigand's use 48 hours. Wigand separately
uses two days for special-set orders and five days for requested orders after a
trial. Preserve the submission condition, recipient and medium for each rule.
His published individual AI certification and the later circuit-wide vacatur are
separate evidence statements; the latter alone does not prove removal of the former.

| Topic | What to extract when applicable |
| --- | --- |
| Hearing scheduling | Scheduling channel, coordination, reserved times, duration limits, cancellation process |
| Motions | Required conferral, submissions, notice or briefing requirements, hearing prerequisites |
| Proposed orders | Submission channel, format, timing, service/copy requirements |
| Courtesy copies | Required documents, delivery method, timing, paper/electronic distinctions |
| Remote appearances | Permitted proceedings, permission process, published access instructions |
| Chambers communications | Authorized channels, copying opposing parties, prohibited submissions, emergency requests |
| Other material civil requirements | Case management, trial practices, exhibits, geographic filing, AI disclosures, or other material requirements not captured above |

Checklist statuses: supported requirement; expressly no requirement; not located
in checked sources; not applicable; unavailable; pending review. Source silence
never becomes 'no requirement.' Express supersession records the successor,
scope and effective date; an unresolved authority conflict remains separately
flagged. This checklist is internal research structure; it does not restore the
procedure/source columns removed from the public personnel directory.

For timing requirements, save the source's force as well as its amount, unit,
trigger and exceptions. A preference is not a mandatory lead time: Ross's JB
procedure prefers hard copies three business days before a hearing but states
copies at the hearing as the minimum. Keep those as separate rules. Likewise,
a chambers statement about returning phone calls is a stated service practice,
not a litigant filing deadline or a verified performance guarantee.

If PDF extraction splits words or email addresses, preserve that extracted text
and the original PDF. Make a separately identified readable derivative, and
visually verify any normalized contact or operative term before saving it as a
fact. Inspect actual link annotations separately: blue or underlined text does
not prove the PDF contains a clickable destination. Record an unlinked low-priority
plea-form label without guessing its URL or expanding substantive review merely
to complete that link. Explicitly distinguish the linked current procedure from
other official copies whose revision or effective dates are unstated.

## Proposed persistence and resume contract

See [checkpoint and comparison design](COUNTY_CHECKPOINT_DESIGN.md) only for
historical design considerations and failure cases. Its broad implementation plan
has been superseded. Document and validate the actual save/resume path used during
each county's baseline research before claiming that path operational.

Use `runs/county-<slug>/<run-id>/` for isolated workspaces, preserving existing runs.
Reuse the established `raw/`, `text/`, `receipts/`, `review/`, and `draft/` layout.
Keep original bytes at content-addressed paths and preserve each retrieval event.
The shared history database remains
`~/.local/share/flwu/research-history.sqlite` (or explicitly pinned override).

Keep semantic facts separate from observation metadata. Store retrieval/review
timestamps, raw/extracted hashes and source quotes in citations and the preserved
review receipt; the finding's compared facts contain supported values, requirements,
source associations and stated revision/effective dates. A new retrieval timestamp
alone must not create a purported factual or legal change. Preserve the whole
receipt as a draft alongside validated findings for audit/resume purposes.

Apply that separation inside nested roster rows too. Receipt paths and receipt
hashes belong in the reconciliation receipt's matching evidence, not in the
compared roster facts. Before accepting a roster checkpoint, change only those
provenance values in a copy and verify that the projected semantic rows remain
identical. If a saved capture contains provenance in facts, preserve that capture
and append an explicitly documented correction; do not rewrite history or label
the maintenance correction as a personnel or legal change. Broward packets95–96
provide the recorded example and verification script.

Proposed additional state: roster inventory and reconciliation, a judge queue with
exactly one active judge, parked follow-ups, and shared-source/version references.
Before switching judges or compacting, persist the receipt and artifacts to the
database, verify the capture acknowledgment, and write a small resume packet with
active judge ID, completed steps, unresolved tasks, referenced artifacts and next
action. File edits alone must not be reported as a successful database checkpoint.
Restart must reconcile an interrupted database-write/resume-write sequence without
duplicating evidence or skipping a judge. These additions require implementation.

## Architecture findings and implementation checkpoints

Read-only inspection on October 15 identified these constraints:

- `research.initialize` accepts only `weekly-seven` or `statewide-circuits`; it
  pins seven counties and creates source-wide tasks. `inspect_run` chooses the
  first missing task, not a persisted active judge. A county task queue is needed.
- `history_capture.stream_for` hashes county/circuit scope; `history.record`
  prohibits changing scope within a stream. `history.compare` uses the finalized
  report within that stream. Simply adding a county loses the comparison link to
  the prior stream; it does not delete old evidence, but creates an unknown baseline.
- `publication.py` has seven county display labels; `site.py` limits navigation
  to packaged registry groups; `search.js` has circuit county lists. A county
  addition needs consistent research, export, navigation, and filter associations.
- Local research coordinator files and several earlier changes are not committed.
  Preserve and inspect these dependencies; do not assume the public checkout
  contains them or include unrelated changes indiscriminately.
- The first direct read-only history query failed with
  `sqlite3.OperationalError: unable to open database file`. The database header
  specifies WAL mode; no WAL/SHM files or open handles were observed. A separate
  filesystem copy was queried read-only with `immutable=1`, leaving the original
  untouched. This verified five finalized reports in
  `manual_baseline:ea3da59ca4bd`, profile `baseline-seven-full-statutes`, with the
  existing seven counties and circuits 4/7/8. The inspection receipt is
  `runs/county-workflow-design/history-inspection.json`. This confirms preserved
  history, not live writer/checkpoint availability or new-county readiness.

The live writer was subsequently exercised successfully: Broward capture 4272
preserved 28 original/text artifacts and an incomplete first-judge draft in the
existing database. Byte read-back, exact replay idempotence and preservation of
the five finalized reports were checked. See the county handoff for the packet
and acknowledgment. This supersedes the earlier writer-availability uncertainty,
but does not prove the reusable helper or judge-completion validation implemented.

Remaining engineering considerations (not a gate on authorized baseline research;
adopt bounded changes as evidence exposes the need):

1. Introduce explicit county contracts and sequential judge state while retaining
   existing seven-county behavior. Supply literal verified source URLs per county.
2. Define immutable county/circuit history identities and an explicit report-to-
   capture baseline mapping so scope growth preserves prior comparisons. Review
   this persistence decision separately before coding it; do not rewrite history.
3. Add source reuse, checklist validation, checkpoint recovery, and a small county
   review packet. Make missing/current/unchanged/conflicting/first-observed distinct.
4. Integrate reviewed county data with archive/navigation without replacing other
   counties, backdating new rosters, or adding empty claims of completed research.
5. October 17 execution policy: local Qwen3.8-27B-8bit workers perform bounded
   research, implementation, builds/tests and routine repairs. Cloud reviews
   completed person/court evidence and code/tests before accepting and advancing.
   Require completion reports and wait for terminal notifications instead of
   repeated cloud status polling. Preserve the single-worker runtime guard.
   Earlier cloud-only and user-approval-between-counties notes below are history;
   STATEWIDE_BASELINE_GOAL.md now authorizes automatic county progression.

## Required validation evidence

When a procedure is a PDF, collect URI annotations as well as visible text.
Check every distinct target within a wrapped heading; one apparent title can
link to multiple different documents. Preserve the original PDF and a separate
derived target/rectangle/page extraction. Deduplicate by actual content hash,
not title or apparent link label. For required forms referenced only through
the court homepage, follow the Forms menu and appropriate division submenu;
record that navigation and the actual attachment URL in the county handoff.
If two versions appear similar, validate both responses as documents before
comparing, review each substantive difference, and retain each source statement.

- Interrupt mid-judge; resume that judge with no skipped steps or lost evidence.
- Reuse one shared document for two judges; retain both applicability links and
  one artifact per hash, with honest retrieval/check timestamps.
- Re-run a checkpoint; do not create duplicate facts or discard observations.
- Change a contact and a procedure; compare against the finalized baseline.
  A partial run must not advance it; adding a county must not erase prior coverage.
- Exercise blocked sources, supported conflicting contacts, explicit supersession,
  negative procedure searches, source silence, and scoped criminal-only review.
- Reject wrong-judge attribution, missing originals, incorrect checksums, unsupported
  quotations, and incomplete county completion claims.
- Check the resulting website court filters, directory presentation, archived
  snapshots, citation links, and preservation of existing county entries.
- Complete a reviewed live pilot for one user-selected county before calling the
  workflow operational. Synthetic replay alone cannot establish legal accuracy,
  discovery completeness, or live source coverage. Stop for the user's county review.

The goal remains active until the accepted workflow is implemented where required,
validated against these behaviors and live evidence, and delivered with its roadmap.

The bounded save helper is now implemented and checked against the actual
Phillips packet in a temporary database. Follow [BASELINE_CAPTURE.md](BASELINE_CAPTURE.md)
for the exact packet contract, CLI, validation limits, read-back, replay and
state-update sequence. Continue person/content review before saving findings;
the helper does not certify legal accuracy or county completion. Direct cloud
review repaired the interrupted worker draft; local workers were not restarted.

HTML procedure review must inspect link targets as well as extracted text. For
an email or document-link discrepancy, save the original HTML plus a derived
record containing the visible label, containing paragraph and actual target.
Do not replace a visible division email with a different `mailto:` target or
label a target as a named assistant's email without supporting attribution.

Inspect visible contact text as well as `mailto:` anchors. A named assistant's
published address may be plain text (Bober's `stracy@17th.flcourts.org`), while
operative hearing instructions use the separate division mailbox. Save both with
their attributed roles; an absent mailto link does not make the address missing.
Keep reception/drop-off locations separate from chambers and courtrooms. Likewise,
a clerk department's attorneys-only number is neither a chambers number nor the
elected clerk's personal contact. Retain “Unassigned” as the source's staffing
statement rather than manufacturing a person record.

Separate a judge's assignment from rules for distributing newly filed cases.
An omitted division in a new-case allocation table does not prove that the judge
left that assignment or has no retained cases. Check the complete order for other
case categories and exceptions, and retain the distinct official assignment
statement. A procedure header saying “Circuit Civil Judge” likewise does not
establish an ordinary commercial docket when the profile/order identify combined
dependency, family and juvenile divisions. Bristol's packet69 records this case.

For a cross-division statement inside an individual procedure, save both the
document owner and the division actually named in the statement. Do not repair
the subject from context. Carbuccia's Division40 document says Division38 adopted
the status-quo order: record `document_owner_division=40`,
`source_stated_division=38` and `status=reference_names_other_division`. This does
not establish either adoption or non-use for40. Preserve the source citation and
confirm this distinction survives the exact judge's saved comparison context.

When saving PyMuPDF annotation inventories as JSON, convert both `Rect` and
`Point` geometry to numeric coordinate arrays. Retain original PDF bytes and
physical page numbers; verify external annotation destinations against the HTML
inventory. Successful serialization does not establish that page content was read.

Check embedded images for substantive text/forms and layout tables for omitted
values; retain an image/layout review artifact when needed.

A revision label is a source statement, not a freshness guarantee. Preserve its
actual precision (for example, month only) even when later references appear in
the body. Record the inconsistency without inventing a revision date. For orders
with multiple printed numbers, reuse the same original and preserve number/scope
aliases. If an exact-number original concerns a different subject, record the
mismatch; do not silently replace it with a presumed intended order. Record the
search path and any missing supporting original separately from completion of
the judge's available procedure review. A discovery index is not evidence that
all linked documents were collected or substantively reviewed.

For a shared county procedure discovered during a judge review, save an independently
addressable county finding in the same incomplete checkpoint when useful. Keep the
judge's applicability link and the common source original. Use the existing
`findings` list; no schema change or report finalization is required. Read back
**every** finding's semantic facts, not just the first judge. A source/order number
changing does not by itself create a new procedural-topic identity: reuse the
existing entity key and version the facts so subsequent comparisons retain history.

Structured source tables require a content check in addition to hash validation.
For example, compare each filing-location ZIP list to its actual source table and
inspect columns visually. Preserve explicit exceptions, prefixes, missing-value
rules and source wording. Do not infer ZIP geography, silently repair unusual
"before/after" text, or turn an evidence table into a case-specific calculator.
A passed citation-containment check alone does not validate the summarized rule.

Observed comparison integration limit (Clermont live checkpoint): `history changes
--entity` can retrieve a separately saved county finding and its `first_observed`
event, but manual `person-...` check IDs and a standalone county finding are not
necessarily associated by the existing endpoint/entity filter. Also,
`unvalidated_receipts` currently counts all latest payload draft containers, even
when one contains a manually reviewed receipt. Preserve those truthful incomplete
signals during baseline collection. Before declaring the county workflow ready,
implement and test explicit check/entity and manual-review associations; do not
solve this by changing status labels or finalizing an incomplete county. Verify
that completed historical draft checks receive a new closing observation and that
partial captures still cannot advance the finalized-report baseline.

Di Pietro checkpoint 4322 exercises a compatible check association: set a new
judge finding's verified `checks[].id` to its exact `findings[].key`, and include
only the original/text hashes supporting that judge's reviewed evidence. Retain
the receipt's `task_id` separately. After saving, run `history changes --entity`
and assert that `source_checks[entity_key].status` is `verified`, the finding is
present, and an incomplete county still reports `review_required`. This fixes
association for that new observation without a schema change. It does not repair
older check IDs, finalize the county, or solve the generic draft-container count;
those reconciliation/integration checks remain required before workflow readiness.

Keep the shared-source inventory separate from a judge's applicable-source list.
Retain all collected originals, but populate the person's `shared_source_reviews`
and semantic `shared_rules` only with sources actually cited or relevant to that
judge's assignment. Record each source's case-type limits and reviewed pages.
Do not copy every previously reviewed circuit, foreclosure, criminal or special
division order into the next county judge's governing rules. Earlier broad
associations need reconciliation before directory/report export; preserve their
history when adding corrected observations. Keep stated effective dates in facts
without treating them as verified event dates in comparison output automatically.

Record addresses and appearances with their conditions: a small-claims pretrial
room can differ from the ordinary courtroom and chambers mailing address without
being a conflict. Preserve genuinely inconsistent times as separate statements.
When a judge cites a rule with different terminology in the retained compilation,
review that specific rule and record both statements; do not resolve priority or
expand the entire compilation to “reviewed.” Do not infer requirements from a
case-specific preliminary order that is described but not publicly supplied.

For a combined civil/criminal procedure, use the heading to identify possible
assignment coverage, then classify each paragraph by its actual subject. An
“all divisions” heading does not justify silently converting State/plea/speedy-trial
requirements into civil requirements. Record shared directions and ambiguous
timing statements separately with explicit applicability limits. Preserve criminal
form labels and actual target URLs as `link_only` / `not_reviewed_criminal_deprioritized`;
do not fetch plea forms merely because they are adjacent to civil instructions.
If search returns the same judge's old division document, retain its date and
division and inspect identity before using its contacts. A collected historical
PDF need not be exhaustively analyzed when it is not the current assignment's
procedure; record exactly which pages were inspected and do not import old fax,
phone, address or forms into current fields.

For an old document found by search, use its own stated revision/effective date;
a search engine's “published” age or an upload-directory date is not a substitute.
Keep historical assignment/contact facts in a separate dated entry, outside the
current contact fields. A Google Docs “Updated automatically every 5 minutes”
banner describes delivery behavior, not a substantive revision date. Leave that
date unknown unless the author states one. After saving, inspect the exact judge's
history context to ensure current and historical contacts remain separate. Bailey's
FH record and January 14, 2013 Family41 PDF exercise this distinction in packet67.

If a procedure says a form is “attached,” inventory the actual end matter, image
content and link targets. When an official print/edit-document link is available,
check its PDF export as well as the published HTML. Record an absent attachment
as a supporting-source gap with the versions and searches checked. A similar
generic county form or another judge's form is a separate source, not proof that
the missing judge-specific attachment was found or approved. Preserve conditional
division clauses in supplied forms instead of silently replacing the division
number. Save mailing-box and physical-chambers addresses in distinct fields.

Write checklist summaries as readable sentences with spaces, explicit time units
and named actors. Keep exact source quotations separately in citations. If review
improves only wording, preserve the earlier capture and record an editorial
revision reason; a new finding version alone does not prove a legal change.
Compare supporting source hashes and the underlying requirements before treating
an editorial update as reportable. Metadata revision months retain month precision;
search-result titles or stale snippets must not override the retained document.

For apparently truncated PDFs, inspect the rendered page and all remaining pages
before calling the extraction incomplete. Count blank pages separately from
substantive pages. Check a form's heading, division and signature independently;
a mismatched signature is not evidence of judicial reassignment. Preserve actual
link targets: two different labels may point to the same document. If a purported
form link leads to a catalog, record that result and whether the individual form
was obtained. A package listing is not the form's contents. Use free official
sources within this project; preserve a paid-package limitation without purchasing
or running a self-extracting download. Do not equate CMS order submission with
efiling merely because the source uses the terms inconsistently.


For a judge with multiple division profiles, collect each division's contact and
official procedure links within the same person task. Save the mapping of profile
ID, division, published iframe URL, print URL and division-specific email when
available. Read only the sections needed for the brief office checklist; compare
the relevant passages before reusing a summary. A shared print URL can point to only
one division's document; it is not proof that the other division uses that email
or that the published text is redundant. Preserve a wrong division label inside
a document separately from actual profile assignment. Contact-table and image
inspection must distinguish substantive content from seals or decoration. Save
one person checkpoint only after all that person's listed division pages have
been covered, with assignment-specific links/contacts retained.


Do not derive the next judge's assignment from linear PDF text when a roster chart
uses columns. Inspect the rendered chart and compare current profile/assignment
orders. Record source dates and divergent placements without inventing a transfer
date. An absent biography search result does not prevent using an official current
procedure page that supplies the required contact fields; record the exact checked
paths and never guess a profile ID. Historical order citations without amendment
numbers remain unspecified: identify the amendment actually acquired and limit
review to relevant provisions. A recent procedure revision label does not establish
that every copied legal deadline was updated. Preserve such differences against
reviewed rule text, and retain links' display/target mismatches without silently
correcting or endorsing third-party services.


When search/browser text caches disagree with a direct retrieval, inspect and save
the current official original before classifying a present-source conflict. Keep
cache observations as research notes, not replacement current contact values.
Store a revision found only in PDF metadata with its metadata location; do not
present it as visible-body language or legal effectiveness. Reuse shared form
originals by exact document ID/URL and preserve their actual retrieval timestamps;
a new association/review is not a new download. Maintain separate conditional
courtrooms, and record distinct deadline acts (requesting a hearing versus setting
one) instead of flattening them into a single reconciled requirement.


Represent required hearing sequences explicitly: a motion-calendar request to set
a later merits hearing is not the merits hearing itself. Preserve distinct actors
and actions when permission differs: permission to set an assistance-motion hearing
unilaterally does not authorize a unilateral deposition. Keep scheduling, hearing,
sua-sponte disposition and under-advisement follow-up intervals as separate facts.
For satellite judges, use their supported regional address, distinguish civil and
criminal division emails, and preserve the jury-transfer order’s case-type
conditions rather than expanding a judge’s short paraphrase into a circuit rule.


### Do not transfer terms between similar judge forms

Inspect each attached form through its actual ending and the next form heading.
Record division, response trigger/interval, exceptions, date blanks and signature
fields from that judge's original. A generic "except as provided below" clause
does not establish exceptions absent from the supplied form. Verify suspect
extraction gaps against a rendered page before recording an omission. Angione's
Division 71 invocation form ends without the Division 53 / 1.440 / 7.135 / 7.150
clause present in DeLuca's form; her discovery year is blank rather than fixed
2024. Reuse acquisition and validation code, not another judge's substantive
checklist. Likewise preserve JA scheduling versus self-scheduling references and
multiple delivery/cancellation instructions as separate source statements; do
not merge them into an invented single requirement. This is a manual content
review criterion, not something a matching citation or hash alone verifies.


### Separate date values, event labels and scheduling actions

For holiday calendars, compare the actual closure date separately from its label
and weekday. Hurley's December 24/25, 2026 dates agree with the circuit memorandum,
but the Christmas holiday labels differ. A partial list beginning midyear does not
prove earlier holidays were working days. Record the list's stated coverage.
For unilateral scheduling, distinguish a hearing from a deposition and preserve
both waiting period and number of coordination attempts. Hurley allows deposition
setting after five business days and two attempts; another judge's ban cannot be
reused. Source-specific instructions outrank a generic checklist default.


### Fee-order templates and conditional submission channels

Read the full preliminary fee order, including continuation pages. For each step,
record actor, trigger, interval, calendar/business unit, submission recipient and
prerequisite to scheduling. Do not change "not more than two business days
immediately preceding" to "at least two business days before." Record the source
as a template, not an order entered in a case. Preserve written expert waivers,
itemized-objection requirements and good-cause exceptions. Mollica pages 14–16
provide a completed worked example with five checklist topics.

Read represented/pro-se and registered-email conditions before recording CMS,
email or physical-delivery routes. A generally-no-courtesy statement does not
cancel specific courtesy requirements elsewhere. Do not import criminal-only
certificates, interpreter instructions or next-day cutoffs into civil fields.
Search-tool export errors do not establish an unavailable original when direct
HTTP succeeds. Preserve a failed exact link separately from a successful alternate
path and retain the original retrieval times when reusing shared documents.


Keep signing and entry of an order as distinct deadline triggers when the prose
and attached form differ. Eves's discovery instructions use signing, while the
form uses entry. Separately record court receipt of hearing materials and clerk
filing of evidence, even where their intervals differ; parallel obligations are
not necessarily contradictory. A Google publication auto-refresh banner is not
a stated revision date. If a complete published document has no print/edit link,
review its original HTML and rendered forms; do not guess an opaque export ID or
label an otherwise complete source missing merely because no PDF was supplied.


### Unfilled source templates

When a published procedure contains "insert deadline" or an unfilled destination,
check the officially linked print version and render the relevant page. Record
literal text, affected field as unknown, URLs and searches checked. Do not fill
an exhibit email from a general contact header or a deadline from another judge.
Keep this in evidence limitations separately from source conflicts and retrieval
failures. Complete review of available originals does not certify a complete
operational instruction. Preserve empty checkbox glyphs and do not assert selected
options from their adjacent text. Feld's published and print procedures provide
worked examples for later agent review.

### Empty extraction, images and incomplete conditions

An empty extracted PDF page is not evidence of a blank page. Inspect page images
before marking the document reviewed; classify each image-only section as civil,
shared, or outside substantive scope. Retain its original and page numbers. If
civil/shared, review visually or obtain an OCR derivative tied to the original
hash. If criminal-only, record its title/type and deliberate scope exclusion
without exhaustive review. Levine's pages15–21 contain scanned criminal/traffic
forms absent from both HTML text and PDF extraction. Collection, visual scope
screening and substantive review are different states.

Follow external bookmarks independently of embedded appendices. A failed external
copy does not erase an available embedded appendix, but the embedded version does
not establish the external target's contents. Save both acquisition outcomes and
review scope. For conditional requirements, preserve strict versus inclusive
comparisons and identify unaddressed boundary cases: Levine's under-ten/over-ten
staffing rule leaves exactly ten unspecified. Do not invent an equality branch.
If malformed text remains visible in the original, store it and any contextual
reading separately; visual review does not authorize silently repairing the source.

### Image-only header contacts and form-specific actors

Check header images as well as body text before declaring an address absent.
When visually transcribing, preserve the original bytes and retrieval time, save
an explicitly labeled derivative with its own text hash, and cite its actual
image/header location plus screenshot evidence. Never overwrite the ordinary text
extraction or pretend the transcript was text supplied by the website. Peffer's
embedded header provides the street address omitted from ordinary extraction.

A familiar fee-order title does not establish familiar terms. Peffer's two-page
order uses ten/twenty/ten-day steps and an attorney conference by the preceding
business day, unlike nearby judges' three-page expert/timesheet forms. Record the
actual actors and timing. When the source says the nonmoving party must state an
amount the moving party believes reasonable, retain the apparent actor mismatch;
do not repair it in the stored quotation or silently rewrite the operative rule.


### Hearing-unit limits and case-issued orders

Record the unit of each calendar cap: per case, firm, docket, session or day.
Cawthon has two hearings per case per UMC session and three motions per firm per
single docket. Similar nearby wording does not justify changing either to per day.
For cancellations, preserve whether the route depends on how the hearing was
originally scheduled. For unilateral settings, distinguish proof attached to a
notice from proof presented at the hearing. For competing orders, preserve whether
one combined email or separate submissions are required and the actual file format.

A procedure saying the judge will enter a preliminary fee order does not establish
that a public form exists. Check the full original, attachments and official links;
perform a targeted official search. If no template is supplied, record that narrow
limitation and the stated case-issued-order sequence. Do not borrow deadlines,
expert requirements or entitlement prerequisites from another judge. Complete
review of available sources can coexist with unknown future case-order terms.


### Link labels, handwritten dates and apparent copied references

For email and form links, inspect the original href as well as the visible label.
Save mismatches as separate label/target observations tied to original bytes;
do not label the target a verified alternate contact. Search renderers may append
link destinations in parentheses even when those words are absent from the page.
Friedman's civil/criminal links provide a worked example. No messages are sent.

Inspect signature/date images even when a document has selectable text. Save
manual transcription as a labeled derivative with original hash/time and visual
page evidence; keep ordinary extraction unchanged. An observed handwritten date
or signature mark is not authentication or proof of docket entry. Record an
entry-based effective condition separately from an observed execution date.

Do not repair another judge's name or division inside a required form. Preserve
the literal condition and describe its mismatch with the cover/profile; do not
apply the repaired hypothetical condition. Separate a judge's cited authority
from independently collected/reviewed authority. A scoped review of the judge's
requirements does not assert every cited case/rule was reviewed, and a no-result
search does not prove a cited case nonexistent. Retain conflicting dated sources
without turning the baseline into authority resolution.


### Criminal-only assignments and common access requirements

Record current contacts, assignments and official procedure links for every judge,
including criminal-only assignments. Screen their combined documents for common
contact, courthouse-access or civil responsibilities, but do not expand into plea,
bail, diversion or sentencing research. Save precise collected/screened/reviewed
scopes. Retain genuinely applicable shared court-access rules, such as the reviewed
circuit ADA notice order; an empty governing-rules list is not an evidenced negative
finding. Do not weaken validation or claim no rules merely to complete the record.

When a dated assignment order differs from current profiles and procedure covers,
retain both with their dates. Do not invent a transfer effective date, assign a
successor's current procedure to the earlier judge, or classify an unnamed roster
row as a vacancy without evidence. Review its official link and assignment sources
as a separate roster-reconciliation task before creating a person record.


### Source-association checkpoints without premature person completion

An empty roster name can link to a dated document naming a person who now appears
in another division. Save the exact row, its actual href and the linked original,
then check that person's current profile and all related procedures together.
Record a roster-source-association finding separately from the person. A verified
association means the saved sources say those things; it does not establish current
occupancy, vacancy, transfer date or completion of the judge review.

Use a labeled selected-row derivative tied to the original response hash/time.
Search existing person records before creating another key for a changed court
level/division. Preserve an existing identity and add dated assignments/aliases;
do not double-count the person or rename old history to match the current title.
Keep procedure checklists scoped by document/division. Fifteen-minute county UMC
and five-minute family UMC, or fresh email versus same-thread instructions, cannot
be merged into one unqualified rule.

Checkpoint unfinished text/visual/source-review notes in drafts, with an incomplete
check for the actual judge and no accepted person finding. Save and read back the
originals through the same history database. Verify the filtered roster context
and unfinished-person context separately, and leave completed_judges unchanged.
Only add the judge after the full scoped review and person/citation validation.


### Family assignments encountered during the civil baseline

When a judge's current profile is family and an older document is county civil,
keep one identity with separately dated assignment and contact evidence. Review
the county-civil document's substantive requirements; review the family document
for shared filing, access, scheduling, orders and ancillary commercial concerns.
Preserve specialized family/criminal material without silently claiming exhaustive
merits review. An old division link does not establish current occupancy.

For a linked family template, inspect the current family administrative-order
index for the same material subject and retain both originals when they differ.
Compare form dates, signature/date blanks, contact-letter ranges, remote versus
physical attendance, filing recipient, deadline trigger/units and ADA particulars.
Keep the administrative order's date separate from its unexecuted attached form;
never fill missing case-specific deadlines or fees. State reviewed pages/topics
and separately record visual checks. Do not call every paragraph substantively
reviewed merely because the full text was collected or screened.

Carry conditions through the summary: an order's modification need not terminate
unchanged provisions; a general hearing duration may have a case-type exception.
If final review exposes a wording error, save a corrected finding as a new
checkpoint and verify its read-back without deleting the prior observation.
Continue to distinguish source conflicts from researcher corrections.


### Shared templates, contact roles and inaccessible form shells

Do not copy requirements between judges because their procedure layouts match.
Compare next-day cutoffs, order formats and channels, physical-copy thresholds,
and deadline units. For example, the reviewed MV and MA sources differ in noon
versus3PMcutoffs and CMS versus email order options; MM instead specifies PDF
orders and different continuance deadlines. Store the actual person's statement.

For contact evidence, distinguish a header phone from the assistant/profile phone,
chambers from courtroom and interpreter-office fax from chambers fax. Preserve
name variants in one identity. Record both visible link label and actual target
when they differ; a label saying Clerk does not establish a clerk source when its
href points elsewhere. Never invent a division email from a naming convention.

When a search result PDF fails, keep its failed acquisition and inspect the saved
official order index for the actual href before guessing a replacement path.
Retain signature dates separately from URL upload months. Record a successful
replacement URL as a new acquisition entry. An HTTP200 JavaScript app shell only
proves that response was received, not that its form fields were reviewed or a
request successfully submitted. Keep that limitation explicit; do not submit a
court request as part of research. Newly reviewed shared sources should be linked
to affected earlier observations during county reconciliation, preserving the
old observations and their original dates rather than silently rewriting them.

Before moving to the next judge, freeze the saved packet's mutable artifact paths
as described in BASELINE_CAPTURE.md and replay the frozen packet. A hash-verified
database save preserves evidence, but a receipt's working filename can change
later. A packet must reference the captured bytes, not the latest shared JSON.
Keep frozen replay validation separate from substantive source review. Audit
older packet bindings at county reconciliation; do not claim all history packets
are replayable from a check of only the newest packet.


### Preserve the strength and identity of source statements

Keep preferred/recommended directions distinct from mandatory requirements.
Do not turn a preferred evidentiary hard copy into a universal filing requirement,
or a published Zoom ID into permission to appear remotely. Preserve conditions
such as prior court approval and whether a motion must be both sent and ruled on.

A profile's assistant name and a linked procedure's different name/email are
separate observations. Do not infer a name change, same-person identity, replacement
date, or ownership of the old email. Label the procedure-specific contact alongside
the profile contact. Header office email does not establish a judge's direct email.
Preserve literal dial-in numbers and partial revision labels; do not normalize a
phone prefix from memory or invent a day for a month/year revision.

When a combined document includes extensive diversion material, retain the entire
original and identify reviewed general/shared pages separately from substantively
unreviewed program pages. Rendering pages is not evidence that they were reviewed.
Do not pursue extra diversion manuals or clinical/referral material just because
its link appears in the collected original. Record all actual assignments within
the same person task, even when the profile lists only one of them.

## Source decoding and scoped language checks

Inspect response bytes before extracting text. Extensionless Google document
image URLs may return PNG or JPEG; retain those bytes and inspect the image,
without treating binary decoding output as supporting text. The Broward run's
`review/acquire-singer.py` recognizes common image signatures; its isolated
`review/check-acquisition-images.py` exercises PNG/JPEG and HTML/PDF handling.
This run helper is not a general production acquisition adapter.

Read each procedural heading in context. A judge's “courtesy copies” paragraph
may mean copies of already entered orders, rather than prehearing submissions.
Preserve qualifiers such as “approximately,” “preferred,” and business versus
unspecified days. Record overlapping timing statements with their separate
scopes and sources. Do not silently harmonize them or borrow another judge's
deadline. A malformed source sentence stays documented as malformed.

## Civil forms and shared probate sources

Determine relevance from a document's function. A criminal-history affidavit
required in an estate proceeding is part of the civil baseline, even though
exhaustive criminal-law research is excluded. Preserve checkbox alternatives,
footnotes, exceptions and certification requirements as separate conditions.
Do not interpret a prechecked template box as an instruction or completed fact.

When an order permits checklists to change without an amended order, monitor
both the order and each form's actual current link. A search result may expose
another official version with different text. Save both originals and describe
the difference; do not choose a controlling version or infer dates from upload
paths and search-engine labels. A requested supporting memo not found publicly
remains an explicit limitation; do not claim it reviewed or send an unsolicited
request to court staff.

After completing a shared review, associate its saved evidence with the next
judge only when applicable. Do not reacquire every shared document just to create
that association. Record individual procedure differences and their stated dates.

If an official procedure link opens only a public Google Docs interface shell,
retain that response as an extraction limitation. The public PDF export for the
same linked document ID may provide the content; record the derived URL and
official discovery path. Never guess a different document ID or claim the shell
contains reviewed procedure text. Compare published and print/export versions
when both are offered; preserve substantive differences and original bytes.

A judge's link to another circuit's forms is not blanket adoption of that
circuit's local rules. Label external form resources and their review depth
separately. Likewise, a training-video title is not evidence that its contents
were reviewed or that court technology was tested. Keep source contact conflicts
explicit; do not infer a personnel change date or merge different people merely
because their names appear under the same division.


## Senior judges and multi-judge procedure documents

A shared division number does not identify a person or an occupied regular seat.
When a roster includes a senior judge, retain that role and the expressly stated
assignment separately from regular circuit/county seat counts. A prior county
appointment is not evidence of the current assignment. Use the person's own
profile and its actual procedure link even if a colleague shares the division.
Different Google document IDs remain different sources unless their content and
relationship have been verified; do not presume one is the current version of
another or copy a colleague's checklist unchanged.

For a multi-judge document, inspect the header visually and assign each contact,
room, meeting ID and procedural exception to the named judge or shared unit.
An assistant in an adjacent roster block or another judge's header is not the
active judge's assistant. Preserve unlocated fields and the searches performed.
An unnamed disclosure in such a document is a document statement until its
person-specific attribution is supported. Do not silently apply it to both judges.
Retain separately discovered matching forms with their actual discovery paths;
a form label without a link is not proof of an invented hyperlink destination.

Broward example: Pole's profile2793 links a13-page document distinct from
Garcia-Wood's11-page document. Pole-specific remote/live trials and witness-list
designations coexist with shared hearing directions. The review retained each
statement and differences without deciding which source controls. See the county
handoff and `receipts/person-christopher-pole.json` for exact source associations.

## Keep comparison context bounded

The history CLI prints the full comparison JSON even when `--output` saves it.
Redirect stdout to a run artifact rather than displaying the entire response.
A single-entity result can still repeat substantial original evidence in events,
current findings and drafts. Inspect only keys/scalars first, then select the
specific facts or citations needed for the next reasoning step. Do not paste the
entire comparison or cumulative acquisition inventory into a later local task.

Example for the saved Pole checkpoint, from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/flwu history changes \
  --stream manual_research:county-baseline-v1:6bf5ac02ab39 \
  --entity broward-senior-christopher-pole \
  --output runs/county-broward/2026-10-15/review/pole-context.json \
  > runs/county-broward/2026-10-15/review/pole-context-cli.json
```

Check `baseline_known`, `assessment`, the exact entity's `source_checks` entry
and `current_findings` membership. Then read only that entity's relevant semantic
facts. Read original evidence by stored path/page when needed. This bounds model
input without deleting evidence, weakening validation or substituting summaries
for original documents.

## Hearing-specific deadlines and shared-order adoption

Preserve timing rules by subject and source clause. The Arthmann38 receipt adds
`deadline_rules` to both receipt and semantic comparison facts: subject, action,
amount, unit, direction, triggering event, literal source wording, exceptions,
conflict group and citations. Keep `days_unspecified` when the source says only
“days”; do not infer calendar or business days. Do not turn “within five business
days prior” into “at least five business days before.” No automatic due-date
calculation is authorized by these evidence fields.

Arthmann is a concrete comparison case: UMC/CMC orders two business days;
emergency orders two business days in one section versus two days in another;
special-set/trial orders two weeks; DV orders seven days; GAL orders five days.
General courtesy materials, exhibit exchange, courtesy exhibits and trial
stipulations have distinct subjects and exceptions. Do not merge them into a
single “materials due” deadline. Verify all entries survive receipt-to-fact
serialization and appear in entity-filtered history context.

Shared-order reuse must preserve positive as well as negative applicability.
Division38 expressly adopts the status-quo order; Divisions33/35 decline it for
specified cases. Save `expressly_adopted` or the evidenced non-use status with the
individual source, case scope and any stated policy dates. Do not invent an
adoption date from the procedure's revision date or reuse another judge's policy.

For a recovered historical order, retain issuance, nunc-pro-tunc date, literal
effective wording and retrieval time separately in receipt and comparison facts.
Arthmann's alternate official2011-53 copy is signed2013-11-12, states nunc pro tunc
2011-10-28 and says “effective immediately.” The order number is not its signing
date. Preserve the failed actual link and alternate URL; do not claim identical
bytes when the original destination was unavailable. Use physical PDF pages for
pinpoints when the source's own table of contents is stale. Identical duplicated
blocks may have one summary with both locations retained, not duplicate duties.

## Visible labels, actual links and embedded QR codes

Inspect the original HTML anchor target as well as its label. Decode a Google
redirect's `q` parameter for the inventory without opening that target. Collect
embedded images before deciding they are decorative; an image can contain an
unextracted QR destination. Keep the original image, retrieval time and hash, and
store any decoded payload as derived evidence tied to that original. Never join
a meeting, follow a payment link or execute decoded text as part of extraction.

On macOS with Xcode/Vision, `scripts/decode_source_qr.swift` is an exercised offline
helper. It reads one local image, emits source hash/time/method/payloads as JSON,
and never opens a destination. Compile and run from the repository root:

```sh
mkdir -p .build/module-cache
CLANG_MODULE_CACHE_PATH="$PWD/.build/module-cache" swiftc -module-cache-path .build/module-cache scripts/decode_source_qr.swift -o .build/decode-source-qr
.build/decode-source-qr path/to/saved-image.png > path/to/review/qr-decoded.json
```

Use real source/output paths from the acquisition manifest, not those illustrative
paths. Nonzero exit means extraction failed; empty payloads mean this decoder did
not extract a QR payload, not proof that the image contains none. Record tool/host
limitations if unavailable; do not install machine-wide dependencies or invent
a payload. Persist the derived JSON with the original image hash and citation.
Alspector/FV provides a checked example: profile/visible ID328337467 differs from
both procedure anchor and QR458523246. Its clerk label also points to the defender
site. Preserve these differences without silently repairing source evidence.

For mixed criminal/domestic-violence profiles, check the official subject hub's
own judge card and targeted civil-procedure searches. A hub describing both civil
and criminal courts does not establish that every listed judge handles every
matter. Record the actual individual link and any unlocated separate civil
procedure; do not copy criminal schedules into a general civil checklist. Keep
CMS features distinct: Alspector permits agreed-order submission but expressly
does not use online hearing scheduling. Label an in-court clerk separately from
the elected Clerk of Court, and an interpreter-office fax separately from chambers.

## Individual revisions, linked originals and reused rules

For each new judge, read the whole individual procedure before reusing a similar
judge's checklist. Alperstein/35 and Achille/33 are a regression pair: Division35
says upload supporting papers once the hearing appears in CMS; do not import
Division33's two-business-day wording, unilateral-setting permission or actual
2025 holiday link. A colored label or printed URL is not proof of an HTML anchor.
Record actual anchors separately from printed destinations. Follow the wrapper's
real print/edit link, retain its document ID and compare its content against the
published iframe before using export-page pinpoints.

Keep date precision: “October 2026” is a revision month, not October1. A signature
date is an issuance date; do not fill an effective date unless the source states
one. Preserve a linked original even when later amendments are already saved.
For Alperstein's AI provisions, retain January2026 original, amendments, June
vacatur and October individual statement as separate evidence. Briefly identify
the discrepancy; neither resolve it nor hold a completed source review open for
that reason. Distinguish circuit-order references to Supreme Court action from
independent review of the underlying Supreme Court originals.

If header/profile name a different assistant than older body instructions, retain
the verified header/profile contact and the conflicting body addressee with
citations; do not infer a personnel change date or manufacture a second assistant.
Similarly retain meeting-link IDs and inconsistent one-tap IDs separately. Check
PDF images/tables in manageable batches. A truncated image-tool result does not
establish visual review; reopen the omitted pages before marking them reviewed.

## Explicit non-use of shared procedures

Reuse of a shared document is not automatic applicability. If an individual
procedure expressly declines a shared template, record the exception in the
receipt **and in semantic comparison facts**, with source key/URL, division,
case cohort, stated policy date, earlier-case uncertainty and supporting citations.
Broward Achille's `shared_source_applicability` is an exercised example: status
`expressly_not_used_for_specified_cases`, case filing start2025-01-01, individual
policy effective2025-03-01, earlier-case applicability `not_determined`.
Citations remain in the receipt; the semantic version excludes retrieval/quote
metadata. Retain the shared original without describing its requirements as
applicable to the excluded cohort. Do not infer circuit-wide repeal or a judge's
appointment date from the policy dates. If this association is added after saving,
make a new capture and preserve the earlier one; metadata enrichment is not a
new legal development. Verify the entity-filtered comparison returns the exception.

Keep unusual time-direction words and units exact. “At least two business days
after the hearing has been set” must not become “before the hearing” or “within
two days.” Record the awkward statement rather than generating a corrected rule.
Similarly, compare the body and appended deadline checklist independently; a
checklist can state a different premarking deadline from the operative paragraph.

## Court-linked editor pages and proposed-rule targets

A court may link directly to a Google edit document rather than a published iframe.
An HTTP200 editor shell containing a JavaScript warning is collection evidence,
not readable procedure evidence. Record the exact court-supplied document ID and
try that same ID's PDF export. Preserve both responses and their retrieval times;
never guess another document ID. Coleman/FP is a successful example. Keep original
extraction and a separately hashed readable extraction if word spacing is damaged.
PDF annotations can retain a different destination from the displayed address;
save both and visually check the associated text without opening a meeting.

Classify each linked rule document by its own contents. A link labeled “Rule2.530”
can lead to a proposed-amendment notice. Read its title, adoption language, dates
and visible amendment markings before assigning legal status. Store a comment
deadline as a comment deadline, not a revision/effective date. A proposal may be
collected and reviewed while remaining `proposal_not_adoption_evidence`; neither
the court link nor its surrounding mandatory language establishes adoption.
Reuse the separately maintained statewide baseline for current-rule research;
do not hold a completed individual source review for adjudication of conflicts.

Keep source-specific dates separate: Coleman has an individual revision date,
an express reassignment date, a CMS commencement date and an older assignment
order. A document title retaining an old division is not by itself a new assignment.
Historical named assistant email may be retained separately without replacing a
currently published shared division contact. Search-result age labels and URL
filenames are not author-stated dates. Source records, not assumptions about what
is probably current, drive semantic comparison facts.

For procedural tasks, retain the required object and destination as well as the
deadline. Duffy/FD requires witness/exhibit **lists** filed and exchanged five
business days before hearing; that is not evidence of the same deadline for
exchanging underlying exhibits. Her text separately refers to motions filed with
the Clerk, court courtesy copies, and CMS supporting documents/orders. Save those
directions separately, including any ambiguous use of “file through CMS.” Do not
infer that an upload to chambers satisfies clerk filing. A published Zoom link
likewise does not by itself establish permission or a remote-hearing entitlement.

Inspect linked examples before treating them as reusable blank forms. Fein/FT's
“Example of Proposed Order Word Format” leads to a populated case order. Save
its caption/case identity and dates under a separate `example_scope`; exclude
case-specific deadlines from general `deadline_rules`, and do not use its order
date as the individual procedure's revision date. A format requirement can be
verified from the general procedure while the linked illustration remains
case-specific. Review enough of the example to establish its format and scope;
do not expand into criminal merits or copy case parties into future submissions.
Retain conjunctive instructions exactly: Fein emergencies require call **and**
email, not either one. Shared building hours do not establish chambers/JA hours.

When a referral discrepancy requires comparing multiple sources, preserve each
source statement independently in semantic facts. Gamm's individual procedure
names Vicki Plant; a distribution order maps JT/46 to GMX; an assignment order
names Denise Kistner for GMX. Store each statement with its own date, role and
citation rather than overwriting the procedure's name with a joined inference.
Mark the discrepancy without declaring which magistrate controls. This preserves
an evidence baseline while allowing future comparisons to identify which source
actually changed. Check footnotes for exceptions before completing the checklist:
Gamm's goal-date extension exception and conferral method/date/time details are
in notes. Keep a separate roman-numeral note even when numbered notes also exist.

## Literal calendars and linked compilations

Harris42 supplies a useful validation case. Save an individual procedure's dated
calendar as `trial_calendar`, separate from general `deadline_rules`. Keep each
row's printed call/start/end dates and unexplained markers. Its December18,2026
call precedes a printed January19–28,2026 trial period in the table, but follows
that period chronologically. Preserve those dates and flag the discrepancy;
do not repair the year to2027. Do not turn a public calendar into a case-specific
setting. Verify the original years survive serialization and entity-context
read-back, with no inferred correction or date calculation.

Compare visible link text with the actual PDF annotation or HTML target. Harris's
visible Zoom hostname is `z-oom.us`; its annotation and profile use `zoom.us`.
Retain both source statements, identifying the actual destination, without
entering the meeting. Inspect numerical boundaries too: “more than30minutes”
and “30minutes or more” differ at exactly30. Never normalize these into one rule.

A linked rule may be an entire historical or amendment compilation. Collect the
original, identify the relevant pages and state exactly which pages were reviewed.
Harris's Rule12.200 link opens128pages; the relevant rule/commentary is on1–4,
with blank5. Remaining123pages were collected, not reviewed. Do not infer an
adoption date, effective date or currentness from its filename. Preserve differing
triggers: the individual30dayCMC clause omits “service”; the linked rule includes
it. Original evidence plus a scoped review is sufficient for this link's purpose.

Treat different Local Rule copies as separate originals unless hashes match.
Harris's2018/01 approved copy works; the2018/03 final-copy link is broken; a
separate2026/04 final copy is available. The approved copy has a January23,2018
Supreme Court approval stamp and blank circuit execution fields. Check images
when OCR misreads a handwritten year; preserve a labeled manual transcription
bound to that original. Do not import the final copy's March5 issuance date into
the approved copy. Existing shared sources should be reused with their recorded
scope and dates, not downloaded again merely because another judge links them.

## Calendar categories and misdirected submission instructions

Holden FC illustrates why headings, narrative and closing schedule must all be
checked. Preserve weekday lists and time-of-day statements independently: its
motion-calendar heading omits Thursday, while the narrative includes it; calendar
call is listed at8:45a.m. but described elsewhere as Thursday afternoon. Store
these discrepancies without picking a preferred calendar. Hearing schedules do
not establish chambers office hours. A generally5–10minute motion calendar,
an express5minute CMS clause, a more-than10minute special-set instruction and
a15minute-or-longer heading do not establish a rule for the11–14minute gap.

Keep the destination and purpose of each instruction separate from the contact
record. Holden's self-represented CMS paragraph names `div07@17th.flcourts.org`
inside the FC procedure. Preserve that destination as a discrepancy; do not
silently replace it with FC or promote it to the assistant's address. Likewise,
retain the visible clerk URL and decoded actual link separately when they differ.
Do not transmit identity documents or test these submission instructions.

Search hits for former civil assignments are leads, not current assignments.
Check the dated original and the current official subject index when relevant.
Save each assignment statement and its exact supersession language. The2025 DV
alternate order names2023-19 as superseded; do not rewrite it as expressly
superseding the2022 order that happened to appear in search. This evidence task
does not require reconstructing the entire intervening authority chain. Review
current contacts and shared procedure, preserve historical scope, and leave
low-priority criminal forms as explicit unreviewed links.

## Named-email annotations and similar procedure templates

Izquierdo's visible header gives Laura Gonzalez's name without printing her named
email. Its PDF annotation links that name to `lgonzale@17th.flcourts.org`; the
communications text separately directs correspondence to `divjq@17th.flcourts.org`.
Extract link annotations, retain their rectangle, and record the visible text
within that rectangle. This establishes which name owns the link without guessing
an address from a surname. Preserve the shared destination and named contact as
separate fields. A contact being published does not establish deliverability.

Do not copy details merely because two judges use similar dependency templates.
Izquierdo's TPR pretrial clause clearly says not less than10days **before trial**;
Gamm's differently worded clause has an ambiguous setting anchor. Izquierdo leaves
exhibit directions to the court or case-specific order; do not import another
judge's alphabetic premarking. His referral mapping is JQ/34→GMZ→Denise Kistner;
Gamm's is JT/46→GMX→Denise Kistner. Keep the distinct division keys even when the
named person is the same. Preserve the individual Vicki Plant statement
separately in each record and verify the correct division join in comparison facts.

Record remote-appearance conditions alongside the deadline: the72hour motion and
notice rule, late unavailability requiring conferral, continuance if agreement is
unavailable, and the interpreter/residence clause. Do not turn agreement or an
exception into automatic permission where the document also requires court
authorization. A footnote may independently limit an apparent permission:
Izquierdo's agreed continuance is still subject to the court's decision.

## Published HTML without a print link; section-specific exceptions

Kanner Division37 provides a published Google document but no edit/print link in
the collected wrapper or document. Read and save the published HTML, including
tables, actual hyperlink targets, images, appended forms and final notes. Do not
guess a private document ID or report a PDF review that did not occur. Cite actual
HTML sections and retained-text intervals; contents-page numbers are not verified
physical PDF pages. Check the final star note before interpreting a starred time.
Kanner's star is a general reminder, so it does not resolve9a.m. versus8:45a.m.

Keep document owner, statement subject and destination distinct. Division37's
status-quo sentence names38; a competing-order sentence actually linksDiv40 while
the specific section/header useDiv37. Preserve the discrepancy without changing
the contact record or inferring adoption. Compare durations within the same
document: temporary relocation is3hours in special sets and1hour in relocation.
Store both, with section citations. Similar family templates still differ:
Kanner's pretrial conference on UMC is explicitly physical, and her custody
paragraph does not contain Carbuccia's additional appearance/interpreter conditions.
Check these distinctions in saved comparison facts before moving to another judge.

## Division-specific routing and unavailable cited originals

Kaplan59/57 has no online scheduling or motion calendar: the court sets and cancels
hearings. Its emergency motions/status go through the clerk, not the JA. Do not
copy another family judge's mandatory emergency-email route. The physical-evidence
rule says bring exhibits on the hearing day, not in advance; the expressly
authorized remote-appearance exception instead uses CMS supporting documents.
Store the condition with each route. A published Zoom link supplies no permission.
Keep PDF **and** Word order formats, rather than replacing them with a CMS default.

Distinguish a litigant's follow-up cue from a promised court decision deadline.
Kaplan's10days concerns contacting the clerk when no response has arrived; it does
not expressly define the clock's starting event. Do not create a more precise
deadline than the source supplies. Named-email search hits from an assistant's
former judge are historical leads, not verified current contact fields.

When an individual procedure cites an order without linking it, check the official
subject index and targeted order-number/subject searches. If trying a known public
legacy path, label it a constructed probe, not an observed link. Save responses,
URLs, timestamps and search evidence. A404probe does not establish the order never
existed or was repealed. Kaplan's2012-12-UFC original remains missing evidence;
retain that gap and the supported individual transfer instruction separately.
Do not relabel a different allocation order as the missing original or resolve its
supersession by inference. Completed individual source review does not certify
collection/review of every cited original or completion of the county baseline.

## Verify table associations, not just citation validity

The Izquierdo review exposed an agent error: a valid page6 citation accompanied
the wrong semantic name for GMZ. The original2026-09 table says GMZ Denise Kistner;
the agent had copied Lucy Ramos Miller from adjacent rows. Citation-substring and
database round-trip checks passed because neither compared the fact with its row.

For each assignment mapping, identify the exact division row in text and visually
check the original table when layout could cause confusion. Validate the saved
name against that row, including a negative control for a plausible adjacent-row
name. Do not call an agent transcription error a source discrepancy. Append a
corrected observation with reason, prior capture identifier and unchanged original
hash; preserve the old capture. Correct current documentation and comparison facts.
Keep independently conflicting source statements separate, and do not advance the
finalized-report baseline. Packet80 demonstrates this repair; historical packet77
and its writer scripts must not be used to regenerate current state.

## Email-looking text and conditional scheduling rules

Kollra's header prints and links `tsugar`, while the hearing-request instruction
prints and links `TSGUAR`. Case normalization does not make these the same address.
Save both spellings, their contexts and actual targets; do not silently correct one
or send a test message. A prohibition on “FF division email” does not supply its
full address. Keep an unpublished address unknown rather than constructing it.

An email-looking label may target an unrelated web host or another person's
mailto. Preserve the source inventory without treating those targets as verified
contacts or visiting them merely because they appear in the document. Kollra's
CMS link includes literal`/THIS` and returns404; the clean official help URL is
separately printed and available. Record those as separate observations, not a
successful redirect. Keep plea-form destinations as explicitly unreviewed links.

Extract scheduling conditions together: five-minuteZoom/no-written-motion and
mandatory-client physical appearance, plus separate special-set witness agreement
and notice requirements. Do not generalize the short-hearing permission. Preserve
strict “more than10pages” rather than “at least10”; distinguish3signaturecopies
from a deadline; retain the general90minute afternoon statement alongside a
specific3–5session. An October1,2025CMS commencement is not a revision date for
the whole document. Validate these distinctions in persisted comparison facts.

## Blank trial templates and source-number discrepancies

For a judge's appended or separately linked trial template, record whether case,
hearing and execution dates are blank. Keep the original and its source link;
do not treat a blank form as an entered case order or compute actual case dates.
If both embedded and linked versions are collected, retain their separate hashes
and review scopes. Similar text is not proof of identical versions.

For each extracted time requirement, record the action, amount, unit, direction,
trigger event, time of day, condition and exception. Verify the trigger against
the original paragraph before saving: Ledee's sample disclosure deadline is
30 calendar days before the **pretrial conference**, by5PM, conditional on an
election of reciprocal discovery. Its continuance instruction requires a motion
to be **set**10 calendar days before **trial**, with client consent and an exception
for a truly unforeseen emergency. Do not replace these actions with generic
“file before trial” deadlines. Preserve less-than versus more-than thresholds;
a missing equality case remains unspecified, not an inferred inclusive rule.

When an individual procedure cites an administrative-order number, compare the
number and subject of the actual official document. Preserve a mismatch as a
source discrepancy. An independently located relevant order is a separate source,
not permission to silently correct the judge's citation. Limit review to what is
needed: for Ledee's2022-002-GEN reference, the official2022-2-Gen title/effective
clause onpage1 establishes the subject discrepancy. All6pages are collected,
but onlypage1 is reviewed; do not claim the historical assignment appendix was
reviewed. Record an explicit “no facsimile available” statement differently from
an unsuccessful search for a fax number. Do not promote a historical assistant
email or assignment into the current roster merely because a search finds it.

## Magistrates and hearing officers: preserve roles and verify procedures

The judge grid adapter is deliberately limited to h3 headings and a Biography
link. Broward's magistrate index uses h2 headings and has no biography links.
Select the exact full published name AND division within one roster block; verify
its actual procedure link and the individual document heading before attribution.
Do not weaken the judge adapter or use a surname substring to accommodate this
different layout. The first worked example is Creary98 in packet106.

Save `entity_type` as `general_magistrate` or `hearing_officer`, use `person_key`,
and retain the source's assistant role. The legacy `_person` nonjudge branch
checks `office_phone`, `office_address`, and `office_contact`, but does not validate
individual procedures. Use `scripts/officer_review.py:validate_officer` for a
completed officer review; it supplements those checks with assistant name/contact/
role, exact task/person/procedure association, document inventory, supported
checklist and shared-rule evidence. The helper accepts two procedure statuses:
`verified` (nonempty document inventory with applicability, review scope and
citations) and `no_published_procedure_located`, an evidence-backed negative
finding. The negative status is a documented absence, not verified instructions:
it requires the exact person association (`applies_to`), a real citation, a
nonempty `absence_reason`, and a nonempty structured `search_log` whose rows each
carry a real http(s) `url`, a `search` term and a `result`. `documents` may be
empty when nothing was located; a source-only inventory belongs in a separate
field (for example `governing_rules`), never as fabricated procedure documents.
Unknown statuses are rejected, and the method never converts statuses, invents
instruction content, or mutates the receipt. Applicable shared instructions are
recorded separately from individual instructions, with their own search scope.
Missing evidence beyond a documented negative finding remains a draft; do not
relabel an officer as a judge or bypass validation to mark the review complete.

Attribute roster categories from the original HTML card markup (per-card
classes), not from flattened extracted-text filter headings. Hillsborough's
hearing-officer roster has seven cards in total: exactly one in the Civil
Infractions category (Joseph Frank) and six in Unified Family Court (Denton,
Frey, Hill, Lawler, Phillips, Stello); `roster-attribution.json` in the Frank
review packet retains the derivation with the source hash.

Follow `review/creary-body.py` and `review/save-creary.py` in the Broward run for
the receipt and save contract. Supply the next person's actual evidence and
requirements, not Creary's values. Save under `county_officer_baseline` in the
existing county stream, validate every nested citation, read back original bytes
and semantic facts, and replay the new frozen packet without advancing finalized
reports. Check the exact entity through `history changes --entity PERSON_KEY`.
Only then move its stable key from `remaining_personnel` to
`completed_other_personnel`. Preserve the 90 completed judge records separately.
Historical roster inventories retain the counts at their capture time; do not
rerun an older finalizer that would overwrite the current progress state.

For recommended orders, distinguish the recommended instrument from the order
ratifying it and preserve separate format, channel, attachments and service
requirements. Creary requires Word by email, not CMS. Distinguish deadlines with
different triggers: notice within ten days AFTER scheduling confirmation versus
child-support notice at least ten days BEFORE hearing. Record conflicting evidence
submission paragraphs independently; never silently choose the shortest or longest
period. A referral terminology transition is not a procedure revision date.
Shared orders may expressly exempt magistrates/hearing officers from a requirement
that applies to judges, such as an in-court clerk at a remote evidentiary hearing.
Read those exceptions before copying a shared rule into the individual checklist.

Frieden DOR95 (packet107) provides the contrasting officer example: recommended
order **PDF**, ratifying order **Word**, no CMS scheduling, and no referral needed
to schedule according to her procedure. Never inherit the prior officer's formats,
deadlines or referral conditions. Preserve general scheduling intervals separately
from duration allocations by matter type. A condition of **more than120minutes**
does not include an exactly120-minute hearing.

An expressly alternative submission route is not itself a source conflict.
Frieden permits clerk filing at least one week before hearing OR PDF email to
both named recipients at least48hours before. Save the action, channel, recipients,
time and alternative relationship together. Compare shared requirements separately
without resolving which controls. Record a strongly discouraged practice as such,
not as an absolute prohibition. Preserve inconsistent Zoom IDs and email spellings
with their paragraph contexts; do not test them by contacting a court or joining
a meeting.

Where the court links both published HTML and a printable Google document, use
the actual PRINT link's documentID for export. Preserve both originals and compare
them. A relocated letterhead in PDF extraction is a layout difference, not proof
of a substantive version change. Read the rendered pages and retain a comparison
receipt identifying the exact difference. If `pdftoppm` is unavailable, the
installed `pymupdf` renderer is a usable local alternative; a successful text
extraction alone is not visual verification.

When an individual procedure points to a shared service such as Court Reporting,
follow its actual request-form links once and save the reviewed service as its own
history entity as well as a shared-source receipt. Gonzalez99/packet108 uses
`broward-court-reporting-procedures`; subsequent officers can reuse those originals
and review scopes. Do not copy service telephone/fax numbers into chambers fields.
Retain each form, FAQ and administrative-order version separately even when they
appear on the same current landing page. Save differences in duration units,
trigger dates, payment sequence, service methods and exceptions without deciding
which source controls. A source's reference to an original order is distinct from
independently reviewing that original; label a collected amendment accurately.

Inspect every relevant PDF page that extracts only a page number. It may contain
an image-only form rather than being blank. For necessary statements, retain a
clearly labeled visual transcription as a separate text artifact bound to the
same original PDF hash and retrieval timestamp. Preserve the ordinary extraction
too. Record which pages were read, visually checked, or merely collected. In
Gonzalez's source chain, AO2023-32 Amendment2's page14 is such a form; its text is
stored under `reporting-2023-32-a2-form-text` in the acquisition manifest.

Read issuance/effective clauses in the original. The amended reporting order
under a `/2026/04/` URL is signed May27,2025 and effective immediately; the URL
does not establish a 2026 legal change. AOSC11-22's attached standards have a
revision label distinct from the order's signing date. Maintain those distinctions
in comparison facts and preserve narrower review scopes for low-priority material.

Johnston69G/packet109 illustrates two additional checks. An actual iframe URL
contains a literal space after `?`, causing curl to reject the input before any
HTTP response. Preserve the raw href and exact transport error; percent-encode
the space for retrieval without inventing a different documentID or silently
removing the query. Record the fetched URL separately. A successful same-ID PDF
export does not establish that the court supplied a PRINT link.

Inspect linked templates for stale names, dates and blank fields. Johnston's
current procedure links an ETG report naming Claudette Vanni with a preprinted
2020 year. Keep that original and flag the discrepancy; do not add the template's
signer to the current roster, fill or sign the form, or treat it as an entered
case order. Check apparently empty PDF pages visually before labeling them blank.

Extract timing by matter and action. Johnston's ETG draft report is due three
HOURS before hearing, its petition/current-address delivery is24HOURS before,
and a restoration draft is due three DAYS before. Its template final accounting
runs from emergency-order expiration. Show-cause continuance instructions differ
from agreed incapacity/guardian-advocate/APS rescheduling instructions. Preserve
those scopes rather than introducing one division-wide deadline or motion rule.
## Visible links and exact deadline triggers (Kistner GMX/GMZ)

Inspect actual HTML anchor destinations as well as visible procedure text. When a
Google redirect wraps an official link, retain the original href and parse its
`q` destination locally; do not join Zoom meetings to test which number is correct.
If visible-text extraction omits a material attribute, retain the original HTML
unchanged as a separately identified text artifact and cite the exact attribute.
Record discrepancies without silently replacing either statement. Kistner's
printed Zoom number and linked target differ; a separate paragraph names another
magistrate's assistant while supplying Kistner's division email.

Store each deadline's trigger independently: after hearing, before submission,
after the initial scheduling request, and after scheduling are different events.
Do not turn a seven-day packet requirement **from scheduling** into seven days
before the hearing. Do not infer Word/PDF or CMS when a source merely says
"Reports" and "portal." Reuse relevant shared orders with their stated scopes;
an unnamed administrative-order reference is not a proved match to a nearby order.
An absent individual evidence deadline is not itself a conflict with a shared
remote-evidence deadline. Distinguish unstated details from unavailable documents.

For published Google documents with only a `2PACX` identifier and no PRINT link,
review and retain the complete available HTML. Do not invent a normal document ID
or assert PDF/visual review. Keep collection, text review, markup review and visual
review as separate recorded facts. The reproducible example is
`runs/county-broward/2026-10-15/review/kistner-body.py` and packet110.

## Ambiguous timing and advertised downloads without links (Laventure68)

Preserve ambiguous deadline wording literally. “Within three days of the hearing”
does not establish “at least three days before”; use a structured ambiguous timing
state and retain the exact quote. A clock time on the preceding day is distinct
from a duration in hours. Do not inherit another officer's deadlines, unavailable
hearing types, or remote-appearance permissions from a similar document.

Check email anchor targets, including PDF URI annotations. Displayed division
email and `mailto:` destination may differ. Preserve both with original artifacts;
do not send an email to test which is intended. Retain conflicting room numbers
with their source dates and roles rather than silently normalizing them.

If “Click HERE” has no anchor, inspect the PDF annotations, retained official
forms indexes and a bounded official-domain search for the named form. Save search
terms, candidates, actual links and the negative result. Do not fabricate a link
or substitute another magistrate's template. Keep a separate incomplete evidence
check even when the available individual document review is finished. An old
official PDF found by search remains a distinct source; record pages actually
reviewed and do not import its contacts into the current roster. A URL's upload
year and search-engine publication label are not the document's stated date.
See packet111 and `review/laventure-template-discovery.json` in the Broward run.

## Florida Courts form pages with embedded metadata (Matalon93)

An HTTP200 form page may expose only the site header/footer to ordinary HTML text
extraction. Inspect the retained original for a single application/json script
`__NEXT_DATA__`. For the observed form structure, use
`scripts.flcourts_article.extract_form(original_html_bytes, official_page_url)`;
this reads `props.pageProps.pageData` and validates the form identifier, required
metadata, PDF MIME type and official relative `/content/download/` URI. It does
not execute JavaScript, retrieve a PDF, or establish substantive review. Do not
apply the article-body extractor to a form record or treat the shell as a complete
form. Changed/missing structure must fail explicitly.

Save the original shell HTML in the acquisition manifest, returned metadata in
`review/<person>-form-links.json`, then acquire each actual `pdf_url` through the
existing original-byte pipeline. Preserve the query's version value and the
stated month/year precision. Read the downloaded PDF separately and record exact
text/visual page scopes. Store reusable reviewed forms in shared receipts and a
separate history finding with a matching verified source check and nonempty
artifact hashes. Matalon112 demonstrates this with
`receipts/family-notice-forms-reviewed.json`, shared entity
`broward-family-notice-and-address-forms`, and two independently queried contexts.
Do not infer a case-specific order from an unexecuted form or reconcile differing
dated service instructions on the reader's behalf.

Keep each person's evidence/notice/cancellation paragraph distinct by hearing
type, representation/access condition, recipient, unit and trigger. Matalon's
Zoom14days, special-set3BUSINESSdays and CSC2BUSINESSdays are separate statements.
Preserve literal channel wording such as “upload ... via email.” An assistant's
offer to provide a sample upon request is not a public download promise; record
that availability without initiating contact or calling it a broken link.

## Unlabeled links and limited criminal assignments (Miller113)

When an unexpected URL appears in HTML/PDF annotations, inspect its actual anchor
text and PDF rectangle before describing a discrepancy. A whitespace-only anchor
beside a correctly linked meeting number is not the displayed link's destination.
Save visible text, actual href, decoded target, physical PDF page and annotation
rectangle separately. Do not merge it into the primary contact link or join the
meeting to test identity. Miller113 demonstrates an unlabeled894164912 anchor
alongside correctly linked595222547 text; Kistner110 has a different association.

For officers with dependency and criminal/diversion assignments, preserve every
assignment and the applicable appearance format. Review the short individual
document for shared access, contacts, scheduling, evidence and communication
instructions; do not expand into program manuals or criminal merits absent direct
commercial/shared relevance. Record unstated referral, order-format, portal or
deadline fields rather than copying another officer's more detailed directions.
Keep organizational-chart roles and dates separate from individual procedure
revision dates and assistant job-title variants.

## Explicit exceptions and missing alternative-route deadlines (Sullivan114)

Store exceptions alongside the rule they qualify. Sullivan's telephone notary
requirement expressly excludes a non-testifying observer; a generic “telephone
requires notary” summary loses that instruction. Similarly, a filed motion/petition
can be required even when a referral is expressly unnecessary to schedule.

Read each alternative submission route independently. Sullivan's PDF-email option
does not state the 48-hour deadline that Frieden's does. Record an unstated timing
field rather than copying a deadline from a similar officer's page. A different
officer's correctly spelled agency email is comparative evidence, not authority to
silently correct the current source. Keep literal addresses, source URLs and the
discrepancy; do not send test messages. DOR service addresses/hours copied from an
individual procedure remain source-specific statements unless independently
checked against the agency itself.

## Multiple notice triggers and repurposed guidance links (Szorosy115)

Keep notice deadlines relative to confirmation separate from deadlines relative
to the hearing date. Preserve a next-business-day instruction and a two-business-
day cancellation threshold as distinct statements. Keep status inquiries measured
from receipt of a referral separate from those measured from objection-period
expiration. Do not compute a single deadline from those different events.

Distinguish prehearing exhibits, admitted evidence after hearing, and attachments
to a proposed order. A prohibition on putting prehearing exhibits in the public
file does not automatically contradict a later admitted-evidence filing rule or
an instruction to file order attachments. Record each stage and document type.
Preserve general scheduling-only email restrictions alongside specific evidence,
order and delay-notification instructions without deleting either.

Check the actual content of linked guidance pages. If a fragment points to a page
that now contains a different subject, retain that original response and search
the official domain for the fragment's quoted text. Save a matching alternate as
a separate source, not a redirect or identical copy. Do not import old directory
contacts from an interim page merely because a current procedure links there.
For embedded training videos, distinguish the landing page and link collected
from a video actually watched; do not claim live CMS behavior from either alone.

## Hearing allocations and strict triggers (Tannenbaum116)

Do not flatten a general calendar interval into the allowed duration for every
matter. Save the interval, each matter-specific allocation, and the conditions for
requesting more time separately. Tannenbaum96 gives half-hour attorney-calendar
intervals alongside 15/30/60-minute allocations. Preserve a trigger of **more than
120 minutes** as `>120`, not `>=120`; preserve an **approximately** two-week status
conference as approximate rather than an exact computed deadline.

An express exception on one officer's page is not a default for another officer.
Sullivan94 expressly exempts non-testifying telephone observers from its notary
requirement; Tannenbaum96 does not state that exception and allows a notary OR
another locally qualified oath administrator. Record exactly what each says.
Likewise distinguish pro se reports prepared by OAG from counsel-prepared reports,
recommended-order PDF from ratifying-order Word, and an unstated submission
deadline from a copied two-week rule. A short notify-assistant-ASAP interpreter
instruction does not itself contradict the shared CMS request procedure.

Validate these distinctions against the retained individual text, then inspect the
saved entity context after database readback. Packet116's finalizer checks duration
categories, strict threshold, approximate timing, alternative 48-hour evidence
route, order formats and absent observer exception, while preserving Sullivan's
different facts. These are checkpoint assertions, not proof of substantive legal
accuracy or a new production automation feature.

## Linked templates and hydrated folders (Woods117)

Read each actual link destination before assigning its label as a document type.
Woods's notice-template and GM recommended/final-order links point to the same
two-page PDF, which contains only a recommended order. Save that document once,
retain both link associations, record the missing advertised component, and keep
official notice forms as separately sourced alternatives. A linked HO template
does not supply a missing GM template. Preserve a mismatched review notice within
a template rather than rewriting it to match the title.

Check binary signatures before choosing an extractor. The actual HO `.doc` begins
with OLE magic `d0cf11e0a1b11ae1`; save original bytes with a `.doc` extension and
use the installed `textutil -convert txt -stdout <original>` for derived UTF-8 text.
Do not feed this binary document to the HTML branch of `acquire-singer.py`. Keep
the original hash/URL/retrieval time and a separate extracted-text hash; text
extraction does not establish pagination or visual review. Woods117 records full
DOC text review and separate two-page PDF visual review.

For FL Courts pages, determine the actual embedded content type before selecting
an extractor. The article helper must reject folders; do not weaken it into a
generic fallback. For the observed folder structure use
`scripts.flcourts_folder.extract_folder(original_html_bytes)`: it validates one
JSON script, folder type, `name`, and `description.html5`; expands only supported
`contentblock`, `rawhtml`, and `separator` blocks; and returns text, links and iframe
URLs. It rejects unsupported/nested custom tags rather than silently losing them.
It executes no scripts and fetches no links, videos or children. Treat the result's
scope literally; the description is not proof that child-page/video content was
reviewed. Preserve the original shell extraction and derived description as distinct
manifest entries referring to the same original bytes, as demonstrated by
`woods-*-alternate` and `woods-*-alternate-body` in packet117.

A TLS hostname error is not permission to disable verification. Save the exact
failed URL and error; search the official domain for the title and retain any
alternate as a separately discovered source. Likewise, a CMS app shell is not a
training manual, and a related video landing page is not a recovered missing manual.

Keep dates and requirements attached to their paragraph scope: a March2026 header,
September2017 embedded note, and April2022 referral transition are different facts.
Preserve conflicting weekday and communication directions. CMS registration to
submit evidence does not grant permission to schedule hearings where the individual
page expressly excludes pro se online scheduling. A five-day review warning is
not an absolute filing bar; an order-review target is not a guaranteed deadline.

## Institutional contacts versus operational review (Broward118)

After the named judge/officer queue, reconcile the Clerk and court administration
as separate institutions. Follow actual site navigation: Broward's footer Contact
Us links to `AboutTheOffice#ContactUs`, whereas `/aboutus/contactus` alone renders
a generic assistance/confirmation shell. Reading that shell is not a submitted
message. Do not label generic assistance, accessibility, public-records or media
mailboxes as a named official's personal email.

For the observed ClerkDirectory panel use
`scripts.broward_clerk_directory.extract_directory(original_html_bytes)`. It requires
one panel, one table with the two observed headers, two unmerged cells per row,
and unique nonempty division links. Returned row text preserves phone/fax/option
labels, address and hours; downstream normalization must keep those associations.
Match normalized values to exact row citations. Preserve leading-zero rooms and
keep street addresses in three display lines. A department's room is not a judge's
chambers. Telephone-agent hours, counter hours and location summaries are different
services; do not collapse them into one schedule or call that difference a conflict.

Retain contact-directory observations at their actual retrieval time when reused.
Save current/future holiday rows as source statements with their year, and verify
the stated weekday against the literal date. Do not infer additional holidays.
Keep office biography/appointment dates separate from webpage revision dates.

Contact review does not complete commercial operational research. Save an explicit
queue for CircuitCivil, CountyCivil, Appeals, Evidence, Archives, RecordsRequest,
efiling and fees, plus material dated news and outstanding court-wide procedures.
Screen article headings first; a large news page collected is not every article
reviewed. Preserve the actual source panel IDs and reviewed scope in the receipt.
The Broward `review/county-operational-review-queue.json` is the concrete next queue.

For broken Clerk links to circuit orders, retain the original failed URLs and
responses, inspect the already collected circuit order index, then follow its
actual href. Do not blindly correct punctuation or treat a newer upload directory
as a new order date. Packet118's 2025 security order is signed October3,2025 despite
its working `2026/04` URL. Check actual annex pages before claiming a promised form
was included. Record a missing low-priority law-enforcement annex without expanding
into criminal procedure. Distinguish that gap from reviewed commercial access rules.

## Clerk operational panels and linked forms (Broward119)

Follow the actual division link from the Clerk site. For Circuit Civil, read all
six bodies at `/Divisions/CircuitCivil`: `CircuitCivilFiling`, `CourtRegistry`,
`ForeclosureSales`, `IndigentStatus_Civil`, `FormsandSelfHelp`, and `FilingFees`.
An accordion/tab title is discovery evidence; review the body before marking it
reviewed. Save the panel ID, exact quote, original HTML and retrieval timestamp.
Check existing acquisition and shared-review inventories before downloading orders
again; AO2014-17 was already retained and reviewed and should be reused.

Keep each fee row's label, amount, tier boundary, per-unit qualifier and section.
The observed Circuit Civil fee table has 34 rows: a payment instruction row,
three section headings spanning two columns, and 30 two-cell fee rows (17 filing,
9 miscellaneous, 4 copies). Assert this structure before extraction; changed
structure requires inspection, not silent omission. This is a source fee schedule,
not a fee calculator. Preserve the published registry-charge formula, documentary
stamp rounding language, unusual statutory references and payment-method wording.
Record payment receipt deadlines with the event, direction, business-day qualifier,
printed timezone and judgment exception. Do not turn certificate-filing deadlines
into auction-date deadlines or compute dates without an expressly requested task.

Collect actual linked forms, preserving PDF and editable variants independently.
The 14-file inventory and reviewed receipt are at
`runs/county-broward/2026-10-15/review/circuit-civil-form-inventory.json` and
`receipts/clerk-circuit-civil-reviewed.json`. Read each form and its instructions;
compare fees, paragraph references and rule citations against the parent page.
Save discrepancies without selecting controlling authority. A form's blank case
date is not its revision date; June2024 and May1,2019 printed footers are revisions,
whereas July1,2013 inside the foreclosure affidavit is case applicability.

PDF extraction can omit prepopulated form-field appearances. Inspect with
`pypdf.PdfReader(...).get_fields()` and render relevant pages using `pymupdf`;
retain the field dictionary as a derived artifact and original text unchanged.
Do not fill out or submit forms. Word files need signature-aware handling: ZIP
DOCX is not HTML. Preserve raw bytes, read `word/document.xml` and separately
inspect header/footer/footnote/endnote parts. Field codes and cached page numbers
do not establish rendered pagination. Record text review and visual review
separately; do not claim PDF/DOCX identity merely from matching filenames.
Percent-encode literal brackets in a curl URL (or use `--globoff`) while retaining
the original published href. Never disable TLS verification to recover a source.

Save operational facts under stable entity `broward-clerk-circuit-civil`, separate
from `broward-clerk` contact records, using packet119's existing contract/scope and
`flwu.baseline_capture.save_checkpoint`. Use the body/save scripts in this run as
the concrete mapping, not as generic code to execute after the run advances.
Validate citations, read saved facts/artifacts back, replay the frozen packet, and
query this entity with `flwu history changes`. Partial research must not advance
the finalized-report comparison baseline. Update the operational queue with the
specific completed source; Circuit Civil fees do not complete global FeesAndCosts.
For inaccessible auction links, retain failed response bytes and browser outcome;
the parent's guidance can be reviewed while linked instructions remain a gap.

## County Civil comparison and fee extraction (Broward120)

Reuse the retained County Civil page (`mchugh-clerk-civil`) before fetching it again.
Its ten panel IDs are `Overview`, `CountyCivilFiling`, `Evictions`, `CourtRegistry`,
`ForeclosuresSales` (plural), `SmallClaims`, `AdministrativeOrders`,
`IndigentStatus_Civil`, `FormsandSelfHelp`, and `FilingFees`. Save new facts under
`broward-clerk-county-civil`, with the receipt at
`runs/county-broward/2026-10-15/receipts/clerk-county-civil-reviewed.json`.
Keep the existing ZIP-filing-location entity intact; county venue and courthouse
allocation are separate questions. Consult the operational receipt's
`source_reviews` as well as `shared-civil-reviewed.json` when reusing sources.

Use `scripts.broward_clerk_fees.extract_fees(original_bytes, expected_counts)`
for the inspected table. County headings/counts are `County Civil Filing Fees`:17,
`County Civil Miscellaneous Charges`:10, `County Civil Additional Fees`:10.
Circuit headings/counts are `Circuit Civil Filing Fees`:17,
`Circuit Civil Miscellaneous Charges`:9, `Circuit Civil Photocopying Fees`:4.
The helper rejects unexpected panels, tables, headings, counts, merged cells and
amounts. If it rejects a changed source, inspect that original and deliberately
revise expectations; do not suppress the error or omit rows. Keep repeated charges
under their respective headings. It returns decimal strings and exact row quotes,
not a payable total. Validate every quote against the saved extracted text.

Follow free information-sheet and notice links before paid form catalogs. The
County Civil page links three distinct PDFs: eviction filing instructions,
County Court/Small Claims Information, and a garnishment notice/exemption form.
Capture their copy counts, service modes, deadlines, court captions and printed
revision dates. Preserve January2017 printed on the small-claims PDF even though
its text contains an $8,000 threshold. Do not invent a revision date from contents.
The forms catalog has names without download links; a list is not the underlying
forms. The SelfService landing requires acceptance and starts a form-preparation
program. Do not report a completed questionnaire or generated form from that page.

For each linked order, inspect the retained court index for amendments or express
vacatur. Search the official domain by exact order number when necessary. Here
`county-order-index-benson` links `2023/08/2023-35-CO.pdf`, expressly vacating the
Clerk-linked2017-79. Search `site:17th.flcourts.org "2021-6-CO" vacated` located
`2021/08/2021-6-CO-Amendment_3.pdf`. Record original and later statements together.
An express vacatur is a source fact; finding it does not require a project to
resolve competing authorities. A current link to a pandemic-era order does not
prove its assistance program is funded now. Do not turn residential instructions
into commercial tenancy requirements.

Inspect PDF physical page count and page headings before printing or reviewing
large files. These mediation downloads contain27 and26pages despite order-body
footers saying3 and2pages. Read material procedural bodies/notices; retain tax and
historical assistance annexes with explicit review limits. Generated page images
do not establish visual review. Filter discovery inputs by actual file type before
HTML parsing; a PDF passed to BeautifulSoup can emit decoding warnings and cannot
be treated as an HTML link index. Packet120's 23 reviewed pages are distinct from
64 collected pages. Save those scopes and discrepancies, then validate/read back,
freeze/replay and query the stable entity before advancing the operational queue.

## Appeals review: filing destinations, source versions and extraction failures

Broward example: start with retained `clerk-appeals` at
`https://www.browardclerk.org/Divisions/Appeals`. Read all six panels: `Appeals`,
`HowtoFile`, `ProceduresandGuidelines`, `IndigentStatus_Civil`, `FormsandSelfHelp`,
`FilingFees`, plus the contact sidebar. Save actual hrefs before following them;
reuse existing general-order index and civil form originals. Keep notice filing,
appellate jurisdiction, fee payee, and courtesy-copy destination as separate facts.
Do not transform a jurisdiction change into a notice-filing instruction. Where
these sources differ, save each statement and identify the difference without
choosing a controlling source.

The Appeals fees have three tables with payment/payee rows and repeated HTML IDs.
The single-table County/Circuit fee helper deliberately rejects this shape. Inspect
all tables; preserve five charges with their headings, payees and per-unit labels.
County Civil is absent from the first fee heading; do not infer that heading's
charges apply to it. A payment method omitted from one list is not automatically
prohibited. A fee destination does not establish where a notice must be filed.

The Clerk's `PDF/Appeals/AppellateGuidelines.pdf` returns HTTP200 but has garbled
font encoding in both pypdf and pymupdf. Retain those original bytes and extraction.
Render and inspect the page, then save a separately labeled manual transcription
or verified OCR with its own text hash, same original hash/URL/retrieval timestamp,
physical-page locator, and extraction method. Never guess a character-shift decode
or treat HTTP200/text length as readable evidence. Do not alter the source's typos.

Fourth DCA Forms at `https://4dca.flcourts.gov/Practice-and-Procedures/Forms`
uses Next.js folder content. Its stripped HTML can be only a shell. Inspect
`__NEXT_DATA__.props.pageProps.pageData` and its content type before selecting
`scripts/flcourts_folder.py`, article, or form extractor. Unsupported-type errors
are evidence to inspect the source, not authorization to weaken validators. Save
the derived description with original provenance and actual links. Read trial-court
and administrative notice instructions separately; they have different recipients.
An inventory of nine form links is not nine reviewed forms.

Read current-index AO2020-89 and its attachments; the upload directory `2026/04`
is not its issuance date. Body signed November3,2020, effective January1,2021,
expressly supersedes2019-6. Its extension template still cites2019-6 and includes
reply briefs while quantified body limits address initial/answer briefs. Preserve
both without silently repairing the form or inferring reply extensions. Keep older
communications guidelines in history. Reuse AO2020-97 Second Amended for historical
pending-case transfer context, with body review distinct from case-list attachments.
For session laws inspect strike/underline markup visually; extracted deleted text
must not become an operative requirement. Narrow the review to relevant provisions.

Save `broward-clerk-appeals` with structured checklist, timings/formats, fees,
contact, dated source events, conflicts and per-document collection/review scope.
Packet121 uses `review/appeals-body.py`, `save-appeals.py` and `finish-appeals.py`.
Validate citations, database bytes/facts, replay, entity context, previous gaps and
unchanged finalized reports before advancing to Evidence. Keep the county incomplete.

## Clerk Evidence and Archives review (Broward122)

After Appeals, follow actual Clerk navigation links to `/Divisions/Evidence` and
`/Divisions/Archives`. Save originals before interpretation. Evidence has six panels:
`GeneralInformation`, `EvidenceViewing`, `ExhibitProcedures`, `EvidenceRequests`,
`FeesandCosts` (lowercase a), and `FAQs`. Archives has `GeneralInformation`,
`PaymentMethods`, `ArchivesFees`, and `FAQs`. Read collapsed FAQ bodies and
`Contact-1`, not just menu labels. Inventories go to `review/clerk-evidence-links.json`
and `review/clerk-archives-links.json`. An empty attachment list is not evidence
that a judge's separately published forms disappeared.

For Evidence, separate exhibit-list number, identification letter and admitted
exhibit number. Preserve all color mappings, required list/label fields and the
recommended back placement. Store first-day list delivery separately from the
remote-order two-business-day conferral/upload and five-business-day post-log
filing requirements. CMS Supporting Documents upload is not Clerk filing. Reuse
`ao-2022-37` and `coleman-evidence-linked`; preserve their September12/September2,
2022 dates and the amended in-court-clerk exception for magistrate/hearing-officer
proceedings. No new download or fabricated freshness timestamp is needed for a
comparison with already saved originals. Keep each source's scope without deciding
which governs a particular hearing. Preserve phone5537 and5539 as phones: the HTML
marks both with phone icons. Do not invent a room or convert the second to fax.

Read viewing appointments/ID, delegated release, release for proceedings, court-
ordered release and sealed/exempt access as separate conditions. A signed release
on someone's behalf does not erase the independently stated court-order condition.
Preserve five fee rows with per-year/per-page/per-document/per-item qualifiers and
oversize dimensions. An omitted payment method is not an express prohibition.

Archives' published date ranges are service descriptions, not proof every file
survives or is online. Preserve generic search-field wording without requiring
corporate litigants to supply criminal/arrest data. Distinguish four fees and
PaymentMethods from the shorter payment list inside ArchivesFees. Preserve their
difference without resolving it. The FAQ explains records-service escrow, not a
court-registry deposit: deposit plus request letter, use-based deposit amount,
organization account number, charges against balance. Follow actual Finance link
`https://www.browardclerk.org/AboutUs/Finance` to verify contact and look for escrow
instructions. Its invoice email must not become escrow intake email. No account
creation, deposits, payments or individual case requests are part of this review.

Save separate stable findings `broward-clerk-evidence` and `broward-clerk-archives`
and separate receipts, even if persisted in one checkpoint. Packet122's
`review/evidence-archives-body.py` and `save-evidence-archives.py` implement that
scoped save. Preserve the existing institution directory and judge-specific
procedures. Validate exact citations/fees/contacts, original bytes, semantic facts,
idempotent replay, context and previous gaps before advancing to RecordsRequest.

## Court records requests and access standards (Broward123)

Use the Clerk's actual `/GeneralInformation/RecordsRequest` link. Read `Overview`,
`ElectronicCertifiedDocuments`, `InPersonRecordsRequest`, `CourtRecordsbyRequest`
and `OtherRecordTypes`. The source repeats `MarriageRecordsRequest` twice; retain
both and screen for scope without turning duplicate markup into two services.
Do not weaken the unique-panel assertion for the five relevant panels. Save links
in `review/clerk-records-request-links.json`. The24in-person directory rows match
prior38-row institution directory quotes after whitespace normalization; compare
and reuse that evidence instead of re-researching every department.

Follow both actual request-form hrefs ending `.pdf` and `.PDF` once when alias
identity is unknown. Here both HTTP200 responses have identical original/text hashes:
one physical page, not two documents. Inspect the form visually, including footer
revision2022-08-22, email Redactarchives@browardclerk.org, fax9548315550 and fee/
payment fields. Preserve source spelling and mail cash prohibition. Do not send the
form, enter payment details or invent an intake email from a generic clerk address.

Follow `/OnlineServices/ElectronicCertifiedDocuments`, reading all four panels and
15FAQ answers. Keep100-page purchase limit,8-dollar electronic certification,
30-day download availability, claimed nonexpiration and receiving-agency acceptance
as distinct facts. Delivery estimates differ by channel. A page describing checkout
is not a completed purchase test. Do not submit searches, accept transaction terms,
register, upload certificates or enter receipt/reference numbers for this baseline.
Record actual `/Web2/CaseSearchECA` and navigation `/web2/eReceipt` landings only.
Two FAQ hrefs are malformed; preserve them and separately record working navigation,
not a guessed repair. Verification widgets use scripts; describe published code/file
methods without claiming runtime authentication or video review. Preserve Clerk
cryptographic assertions as source claims, not independently established security.

Follow the public search's `//Web2/Services/StandardsForECA` link. Its legacy
`http://www.flcourts.org/resources-and-services/court-technology/technology-standards.stml`
returns HTTP200 with a not-found body. Content checks, not status alone, determine
whether evidence was obtained. Search the official domain for the named access
standards/matrix. Current index is
`https://www.flcourts.gov/Services/information-technology/oit-resources/technology-standards`.
Its Next.js content type is folder; use the existing folder extractor and retain
original provenance for derived text. Actual PDF links are in
`review/records-statewide-standards-links.json`; retain the broken original too.

AOSC24-65 has18physical pages:3-page order plus standards/matrix attachments.
Standalone standards have14pages; matrixv15 is one landscape page. Review commercial
roles, general access definitions and operational limits, not every criminal/agency
cell. This checkpoint reviews standards1,2,4,5,6,8,13,14; visual1,2,4,5,6,13,14;
order1–3text/3visual; matrix selected civil rows and roles3/4/5/7/11 with legend and
sealed/expunged overrides, visually checked. Do not infer cell associations from
linear PDF text alone. Category rows do not override confidentiality restrictions.
Save exact revision/issuance dates and distinguish standalone review from collected
attachments. No automatic certification that no later authority exists.

For future retrieval planning, public-case search first200results and missing images
are not exhaustive evidence. These standards describe authorized automated searches
solely on indices; no baseline source review establishes authorization for automated
case-record collection. Laws, court procedures and public instruction pages remain
the research targets. Preserve local contact/referral/payment differences without
choosing controlling authority. Save stable `broward-clerk-records-request`, receipt,
packet123, original bytes, scoped findings and citations. Verify replay/context and
prior records/gaps/finalized reports before advancing to eFILING.

## E-filing source comparison (Broward124)

Start at `https://www.browardclerk.org/GeneralInformation/eFILING` and reuse its
saved `clerk-efile-form-search` original. Read `General`, `AdministrativeOrders`
and `FAQs`, including `EFiling-1` through `EFiling-26`. Save actual links in
`review/clerk-efiling-links.json`. Separate Clerk processing help (case type and
reference number in subject), Portal technical support and firm registration.
Do not send messages, register, search private cases, submit filings or pay fees.

Follow the Clerk's correction-manual link and its separate Training Materials link
`https://www.myflcourtaccess.com/authority/training-materials`. Save that index's
actual hrefs in `review/efiling-training-links.json`. The linked December2018 manual
is136pages; the index's September2025 manual is113pages. Review the relevant
correction chapters at physical/printed126–134 and109–113 respectively. Do not
assume an older manual is current because the Clerk still links it. Keep full
originals but distinguish selected chapter review from whole-manual review.

Record conflicting source statements as separate dated facts. Here the Clerk says
5days, the2018manual5business days, and2025manual30business days. Do not normalize
unspecified days to business days or calculate a deadline. The Clerk says replaced
files receive a new timestamp; both manuals distinguish replacement (old stamp)
from deleting/adding (new stamp). November2021 commerce notice describes settlement
at submission/refund on correction, while Clerk and2018manual describe settlement
at acceptance. Preserve these differences; do not decide which governs or hold
baseline completion for conflict resolution. Record exact citation/page/date for
both sides, including a document's visible editorial comment without adopting it.

Read the one-page document standards and commerce notice. Scope PDF/A FAQ review
to cover and policy pages1,3,4; Word/Acrobat tutorials need not be exhaustively
reviewed. The cover visibly saysAugust24,2021, the indexApril2021 and machine text
also containsFebruary11,2019. Keep each date's provenance. PDF/A preference versus
requirement, permitted electronic signatures versus excluded encrypted digital
signatures, and8.5x11 versus the8.5x12 typo must remain distinct. Read relevant
service-list and failed-delivery instructions; list membership does not prove
service, and list removal does not prove withdrawal as counsel. Screenshots in an
old manual are not validation of today's authenticated interface.

Inspect scan-only attachments visually. The two-page pro hac vice letter has empty
machine text. Save selected manual transcription under a new text hash, retaining
the original hash/URL/retrieval timestamp and the empty extraction. Label it partial
transcription, not full OCR. Keep the2013letter date and avoid presenting its named
staff or inquiry phone as independently reverified current personnel. Inspect the
firm form's2013revision footer rather than inferring its date from the upload path.

The Clerk labels its SC11-399 revised opinion an administrative order. Read the
actual document heading/date. Its2012appendix contains stricken text that ordinary
extraction includes: visually distinguish additions/deletions before summarizing.
A deleted follow-up-paper requirement or deleted risk clause must not become a
current rule. Review shared2.520/2.525 portions; criminal rollout AOSC13-48 needs
scope screening only. Preserve historical25MB thresholds separately from50MB local
instructions, without replacing the current statewide rules baseline.

Clerk complex-case2025/07link returns404. Reuse `ao-2025-22`, already collected from
the court's actual2026/04index link, with its own provenance. Do not claim failed
bytes equal the alternate. Initial FormB versus existing-case transfer remains
separate. Keep proposed orders, court filing and service of process distinct:
Clerk filing does not send an unsigned proposed order to the judge or arrange
Sheriff service. Consult the already completed judge-specific receipt for CMS/
email requirements; don't re-research all judges during this shared source review.

Persist stable entity `broward-clerk-efiling` and
`receipts/clerk-efiling-reviewed.json` in the pinned Broward stream. Packet124's
`review/efiling-derived.py`, `efiling-body.py`, `save-efiling.py` and
`finish-efiling.py` record this checkpoint. They have predecessor-state assertions:
future runs create a new packet and reuse the validated save API, rather than
rerunning an old finalizer over later state. Preserve prior findings, genuine gaps,
and finalized reports; verify exact citations, hashes, facts, replay and entity
context. Eleven new PDF originals total396pages collected,65text pages and23visual
pages reviewed within stated scopes. Reused complex order is not counted again.

## Consolidated Clerk fees (Broward125)

Follow the actual General Information link to
`https://www.browardclerk.org/GeneralInformation/FeesAndCosts`. Save the original
as `clerk-global-fees`. The relevant panel is `CourtFilingFees`, containing eight
tables, not the division pages' single `FilingFees` table. Confirm table headings
before mapping indexes: appeals, traffic appeals, archives, Circuit Civil, County
Civil, Family, Mental Health, Probate/Guardianship. Retain marriage/passport panels
without expanding this commercial civil review into those services.

Use `review/global-fees-extract.py` as the worked example. It scopes table3 and4
into temporary single-table fragments for the existing strict `extract_fees`
helper. The wrapper is a parser input, not source evidence; every citation still
uses the saved original HTML, original text/hash and actual table/row location.
Do not relax the single-table helper to silently accept the whole global page.
Expected Circuit Civil sections have17/9/4 rows; County Civil17/10/10. Other selected
rows use inspected table/row indexes with cell/amount assertions. Preserve appeals
payee notes in the following rows: a blank amount is a note, not a zero-dollar fee.

Compare label and decimal amount pairs against the saved division receipts. Here
all73 pairs match (30CircuitCivil,37CountyCivil,2civil appeals,4Archives). Do not
refetch every division or call this a longitudinal no-change determination. Retain
the independently observed originals and timestamps. Add the Family table's shared
Circuit/Family new-case row because its >15,000 threshold differs from Circuit
Civil's >50,000; preserve both contexts. Seven estate/trust-related probate entries
are relevant to property/creditor practice; other personal-status fees need only
screening. The resulting selected schedule has81entries, not a payable total.

Keep fee bounds, per-unit qualifiers, conditional charges and payees in each label.
Repeated writ/summons/subpoena/bond entries across sections must not be added twice.
No jurisdiction, case eligibility or statutory fee-waiver opinion follows solely
from a fee-table label. Preserve the global indigence note alongside the previously
reviewed civil-indigence page/form and the Archives payment-list difference.
Do not infer a prohibition from an omitted payment method or use a copyright/
retrieval date as the schedule's effective date. No revision/effective date is
stated in the reviewed table bodies/headings.

Save `broward-clerk-global-fees`, receipt `clerk-global-fees-reviewed.json`, packet125
using the established pinned stream and save helper. Verify exact row citations,
73comparison pairs,81selected entries,3source differences, artifact/fact readback,
replay and unchanged prior history. Mark the eight-source operations subtask
reviewed within scope; leave overall Clerk/county coverage incomplete for selected
news and the remaining material-order/navigation/gap review. Do not silently clear
those outstanding coverage checks when the fee page is complete.

## Dated Clerk announcements (Broward126)

Start from the Clerk's actual About Us → About the Office → News and Announcements
link, `https://www.browardclerk.org/AboutUs/AboutTheOffice`. Reuse the saved original
when it belongs to the same observation; a new research run needs a fresh check.
Scope extraction to `#NewsAndAnnouncements`, then all `[id="newsItem"]` descendants.
The page repeats IDs and hides older articles with CSS: neither a global ID lookup
nor the first visible article is a complete archive inventory. Record each title,
its date label (last `li` in `ul.blog-info-v2`), original body and actual links.
Screen all headlines for commercial civil/shared relevance; read selected bodies
and material attachments, explicitly recording which others were only screened.

Preserve publication labels separately from retrieval, revision, issuance and
operative dates. A June2025 label with an October2025 order link is evidence of
present page content, not proof that content existed in June. Follow the actual
attachment, checking its cover/date and amendment markings; a link labeled with
a rule number may return an older version. Preserve each version and discrepancy
without choosing controlling authority. Historical emergency windows and fee
increases must not be described as newly effective on the observation date.

For backslashes in HTTP links, retain the literal href and verify browser/WHATWG
URL resolution (for example `new URL(href, pageURL)`). Python `urljoin` alone does
not reproduce that behavior. Do not silently repair other malformed URLs or claim
an unvisited destination failed. Inventory unvisited links as unvisited. For scans,
retain the original and empty extraction, inspect rendered pages and save only
necessary verified excerpts with the original hash, URL and retrieval time.
Distinguish rendered pages from pages actually viewed. Respect copyright limits
for newspaper commentary, even when hosted by a government clerk; attribution
and hosting do not turn commentary into an administrative order.

Save a structured receipt in `receipts/clerk-dated-news-reviewed.json`, discoveries
in `review/clerk-selected-news.json`, collection entries in `review/acquisition.json`,
and scoped progress in `review/county-operational-review-queue.json`. Use stable
entity `broward-clerk-dated-news`, kind `county_procedure`, under the pinned county
stream. Packet126 is the historical example: use a new packet on later runs.
Link previous e-filing, fee and civil records rather than overwriting them with
newly discovered versions. A scoped operational completion check needs evidence
hashes for its supporting receipts. Genuine missing-source gaps stay unresolved.

Validate exact citations, original hashes, saved facts/artifacts, repeat-save
idempotence, frozen replay, entity context and preservation of finalized reports.
Entity-filtered context intentionally omits unrelated source checks; inspect the
saved packet or an unfiltered comparison for the overall operational check.
Update state/RESUME and the county handoff only after those checks pass. Completion
of selected Clerk news does not finalize the county or authorize the next county.

## Material access orders and exact identifiers (Broward127)

Use the General Orders table at `https://www.17th.flcourts.org/general-orders/`;
follow actual row links and reuse previously collected security/ADA/room evidence.
Read operative paragraphs, defined facilities/person classes, exemptions, signature
dates and vacatur clauses. Preserve the whole order identifier, including suffix:
2023-44-Gen names2023-28-Temp, not2023-28-Gen. Do not infer supersession from a
matching year/number, neighboring index row or filename alone. A download path
containing2026/04 is not an order's issuance or revision date.

Keep employee/judge badge requirements distinct from private-attorney access;
security recording distinct from courtroom/media rules; closure authority distinct
from an actual closure announcement or deadline extension. A nonexclusive example
list and a separate defined-facility list can differ without a conflict. Record each
scope before classifying differences. A calendar labeled2025 does not establish
2026closures. Limit low-priority law-enforcement annex followup as already directed.

Save a separate county_procedure entity `broward-courthouse-access-orders`, receipt
`receipts/courthouse-access-orders-reviewed.json`, and the operational queue update.
Packet127 demonstrates save/readback/frozen replay; later observations require new
packets. Validate exact suffixes and dates against originals. Keep navigation work
separate: raw403 responses, provider-extracted text and browser-launch failures are
different evidence. Provider extraction must never be mislabeled original HTML or
successful browser inspection. No unsupported HTTP status may be invented for it.

## County navigation and final source audit (Broward128–129)

For Broward, start from the Clerk homepage's separate Property Appraiser, Records
Division and Tax Collector links. Court Records uses the public Clerk landing
`https://www.browardclerk.org/Web2/CaseSearchECA`; Tax Assessor uses
`https://www.bcpa.net/`, whose actual Property Search link is `RecMenu.asp`.
Tax Collector is `https://browardtax.org/`. Official Records is the separate
county destination `https://officialrecords.broward.org/AcclaimWeb`, discovered
through Records, Taxes and Treasury. Do not confuse its case-number search with
the court docket. Inspect landing/menu navigation without submitting personal
record searches, accepting terms, creating accounts or making payments.

Retain failed original responses separately from web-provider extraction. The
provider's retrieval representation is not original HTML, and its source HTTP
status may be unknown. Do not invent200 to satisfy the citation validator or
weaken that validator. Store provider-only discovery with explicit limitations
and the actual provider artifact; keep an original-source gap. Save navigation
as `broward-resource-navigation`, receipt `resource-navigation-reviewed.json`.

Before county completion, audit the actual local-rule, civil, general, county and
relevant temporary-order indexes. Read titles and record inclusion/exclusion
reasons; ambiguous vacatur titles require content review to determine relevance.
Compare actual links against acquisition inventory and prior citation hashes.
Neither a URL mismatch nor citation presence determines review completion:
check exact order identifiers, alternate official copies and recorded review scope.
Use `review/county-completion-audit.json` and the bounded
`review/material-orders-next.json` queue; complete one shared source at a time.

Inspect embedded evidence_limitations, limitations and next_actions as well as
source checks. Keep unpublished optional contact fields separate from missing
promised documents. Reconcile stale actions using later observation/capture IDs
without deleting history. Preserve genuinely unknown current-person fields.
An audit inventory is a draft, not a completed finding. Packet129 shows how to
persist that draft and update stale umbrella reasons while retaining incomplete
status, all earlier findings and finalized-report baselines. Check context and
frozen replay before advancing RESUME. No next county before user review.

## Revised exhibits and separate form libraries (Broward arbitration130)

For nonbinding arbitration, follow Civil Administrative Orders →2023-10-Civ
Amendment1, then `https://www.17th.flcourts.org/mediation-arbitration/` for the
actual form library. Read the signed body and inventory actual exhibits before
assuming every described attachment exists. Here the body is signedApril30,2024,
expressly allows separate exhibit revisions, and the filename identifies revised
June2026exhibits without an exact day. Store those meanings separately.

The hub has11arbitration links but10uniquePDFs: general and county acceptance labels
share one URL. Scope acquisition to arbitration; nearby parenting forms are a
separate subject. Compare actual general, panel and county forms, retaining each
fee's unit, cap/flat wording, conditions, allocation and agreement exceptions.
Do not merge per-day and three-hour rates or add an advance to the total. Record
hearing-selection/notice/occurrence/reporting deadlines with their separate actors
and triggers. No case deadline or payable amount is computed for this baseline.

Preserve form-library differences from revised exhibits without selecting authority.
A separately located acceptance form addresses discovery but does not prove it is
the omitted attachment described in the order. Check consequential wording and
contact destinations visually; preserve extraction errors alongside a separately
identified, verified transcript tied to original bytes/retrieval. The revised
statistical question's before/after extraction error is a regression example.
Do not infer the current holder of an office from an older form's named email.

Save `broward-nonbinding-arbitration`, receipt
`receipts/nonbinding-arbitration-reviewed.json`, and update only its priority queue
entry. Preserve the historical county audit; it is not a mutable completion tally.
The arbitrator roster remains a discovery link, separate from judicial personnel.

## Joint orders and replacement property forms (Broward131–132)

For property fraud, compare Civil Administrative Orders row25 with County
Administrative Orders row34, then read the actual PDF header. Both identify
2023-16-Civ/2023-17-CO Amendment2. The county2024/04 URL returns404; the circuit
2026/04 URL supplies the complete joint order. Preserve both retrievals, but cite
only the successful original for substantive statements. Header identity supports
covering both order numbers; it does not establish byte identity to a failed URL.
Keep the qualifying ownership/fraud predicate, discretionary reassignment by
order, limited reassignment-fee waiver and remote-hearing option. Do not turn
these into automatic routing, an initial-filing-fee exemption or a remote ban.

For first-party property loss, follow Civil Administrative Orders →2025-25-Civ:
`https://www.17th.flcourts.org/wp-content/uploads/2026/06/AO2025-25-Civ-Circuit-Civil-First-Party-Property-Loss-Cases-combined.pdf`.
Physical pages1–2 are the signed body,3–13 ExhibitA and14–16 ExhibitB. Read all
three parts. Body signedJuly24,2025; no separately stated effective date or exhibit
revision date. Exhibits may change independently. Never treat the2026/06 URL
folder as a stated revision date or blank form date as an entered case order.

Store the15 deadline-table rows separately from explanatory paragraphs. For every
rule record actor, event, number/unit, anchor, exceptions and citation. Distinguish
filing, service, setting, hearing, commencement and completion. The pleading-motion,
pretrial-motion and mediation table/prose differences, and45-day objections versus
20-day designations, remain separate statements. Preserve the literal disposition
anchor without computing calendar dates. No missing case inputs are guessed.

Record express supersession as a relationship to the older orders; preserve their
originals and prior judge observations. Compare the older AI paragraph and mediator
window with the new forms without asserting absence of all separate AI obligations.
A query showing13entities citing the old hash is a provenance lead, not proof each
judge adopted that form or handles these cases. Reuse existing ESI and service-
notice evidence; do not silently relabel the older generic notice as a2025-25form.

Save separate county_procedure entities `broward-property-fraud-procedure` and
`broward-property-loss-procedure`, their reviewed receipts, original/text hashes,
reviewed page scopes and structured facts. Advance only the matching priority
queue entries after verified saves; retain the historical county audit unchanged.
Use the existing checkpoint helper, exact/frozen replay, entity-context checks,
artifact/fact readback and prior-record/finalized-report preservation assertions.
These scoped source reviews do not finalize the county or publish a report.

## County mediation branches (Broward133)

Follow County Administrative Orders →2023-6-CO Amendment1, actual URL
`https://www.17th.flcourts.org/wp-content/uploads/2024/10/2023-6-CO.docx-amendment-1-with-attached.pdf`.
The body occupies physical pages 1–3; county/nonresidential referral A pages 4–7;
small-claims B pages 8–9; residential C pages 10–12; report D page 13. Read all
parts and keep case paths distinct. Small claims invoking the civil rules follows
the county path. Do not apply a residential five-day selection window or conditional
free CMAP service to all county cases, or substitute arbitration forms for mediation.

Preserve the body/form differences: may versus shall stipulate; under $15,000 versus
the program webpage's $15,000 or less; residential extension by agreement versus
court-only continuance; required actual start/case type versus report D's scheduled
time and missing separate case-type field. Keep reporting actor, act, recipient and
trigger: Clerk filing upon completion; private/designated report through eportal
within five days; CMAP report/time/invoice return within thirty days; residential
statistical sheet within ten days. These are not one interchangeable deadline.

Fee facts retain dollars per hour, per-party session, minimum earned time, payment
anchors, indigence, allocation checkboxes and case conditions. COINX OR damages
strictly greater than $30,000 selects the stated higher private cap; a blank referral
is not an actual appointment, selected exemption or bill. Preserve interpreter
language separately from the forms' ADA assistance notices.

Reuse `mediation-arbitration/` for program contacts and county scheduling telephone
ranges. Search Court Forms → County/Circuit Miscellaneous Forms and the program
page for specifically named supporting templates. Check actual MIME/signature before
HTML parsing: exports without .pdf URLs may still be PDFs. The first broad inspection
emitted decoding warnings and was discarded; exact four-HTML-source inspection
with a PDF guard succeeded. Bounded official-site searches found references but no
current standalone county statistical/time/invoice templates. Record the gap; do
not invent identity with AttachmentD or expand into unrelated family forms.

Save `broward-county-mediation-procedure`, reviewed receipt and source-search evidence;
retain `county-mediation-supporting-templates` as a distinct incomplete check. The
order review is complete in scope despite documented contradictions. Replay/readback
and history-preservation checks precede queue advancement to the credit-card order.

## Reuse audit and credit-card scope (Broward134)

Inspect each audit row's source_keys/cited_by before acquiring another copy. For
County Administrative Orders row48, `ao-2026-25` already has the exact original and
full reviews in McCarthy, McCaul Ricca and Clermont receipts. The repeated retrieval
in checkpoint134 had identical original/text hashes; keep both timestamps but do
not treat it as new legal content. Inspect review scope and underlying original,
then mark the row reviewed by reuse. Citation presence alone is insufficient.

AO2026-25-CO applies only to small-claims credit-card cases in47/101/102, signed
June29,2026 and effectiveJuly1,2026. Preserve the literal130-days-before/150-days-
after interval; flag it and compute no case dates. Keep120-day proof-of-service,
five-day extension submission, noon-three-business-day waiver/transfer and
30-calendar-day default-package triggers separate. Represented waiver needs an
entered order; paragraph6 states timely jury-demand/transfer submission excuses
in-person attendance. Preserve the different judge-procedure statements already
reviewed; do not resolve them or overwrite historical person records. The30-day
package period starts with the case order entered upon default, not this AO date.
Special waived-pretrial mediation at party expense is not the general CMAP rule.

When inspecting large receipts, print selected semantic fields and citation locators,
not every full quotation. If output truncates, reread the required portion with a
smaller filter. Save `broward-credit-card-procedure` with prior receipt hashes,
original identity comparison, source-specific structured facts and retained
conflicts. Validate prior person observations unchanged and finalized baseline
preserved; advance only the matching queue entry.

## Administrative history, designation and panel procedure (Broward135–137)

General Administrative Orders row19 links `2020-87-Gen-1.pdf` under2026/04.
Read its two pages as establishment of an ESI advisory panel, signed October27,
2020. The120-day period belongs to that panel and starts from an effective date
not separately specified. Do not manufacture a litigant deadline or mandatory
special-master appointment. Five named attorneys are historical appointees, not
new judicial personnel. Existing2021-20-Gen recitals identify the panel and its
recommendations; reuse that evidence and the earlier substantive ESI review.

General row31 links `2023-43-Gen-Designating-Record-Newspaper-1.pdf` under2026/04.
The one-page order designates Sun Sentinel for matters under section50.0711 and
replaces2012-21-Gen. Preserve the November13,2023 signature and unknown separate
effective date. Do not turn the designation into an exclusive rule for every
legal notice or repeat its Daily Business Review recital as present business news.

General row37 links the professionalism order, referral form and member sheet.
Read the five-page2025-45-Gen order and two-page referral form together. The order
is signed November26,2025 and replaces2023-29-Gen Amendment1. Distinguish informal
counseling from discipline and compulsory attendance; the latter powers are absent,
but nonappearance may be considered for a Bar referral. Preserve the order's stated
confidentiality/Bar-referral exception without resolving broader privilege law.
June/December reporting is a panel duty, not a deadline for litigants. No private
referrals need to be collected to establish the public procedural baseline.

For the member sheet, the general-index April path and search-result January path
returned404. Follow `https://www.17th.flcourts.org/broward-professionalism-panel/`
to its actual `https://www.17th.flcourts.org/wp-content/uploads/2026/06/LPPmembersupdated11426.pdf`.
The working sheet states January14,2026 and has13members,including4judges. Inspect
the table visually before associating names,roles,addresses and expiration years.
Preserve both failures; do not assert byte identity to unavailable originals or
retain a missing-content gap after the identified document is recovered. A search
snippet is only a lead. Check HTTP success AND text_path before reading/rendering;
the failed alternate triggered a KeyError and missing-image error, neither counted
as review. Directly retrieved originals remain distinct from web-provider errors.

Record the chair's public referral destination from form page2; preserve the member
sheet as dated panel membership and do not overwrite separate judge contact reviews.
Inventory public report links without asserting their bodies reviewed: labels for
June3,2025 and December15,2024 share one URL on this hub. Report contents and program
compliance are outside this material-procedure review. Save separate entities
`broward-esi-panel-history`, `broward-record-newspaper-designation` and
`broward-professionalism-procedure`, then verify citations, facts, artifacts, exact
and frozen replay, entity context and earlier history. A standalone form/member
list is not an attachment to the order merely because the index links them together.

Completion of the nine-entry priority batch is not county completion. Set its next
index to null and retain the next action: reconcile all remaining158-row historical
index-audit entries against actual original identities and review scopes, then
record dispositions for remaining evidence gaps. Preserve the historical audit;
do not replace its original observations with a retroactive completion tally.

### Assignment-table and source-reuse checkpoint (Broward 138–140)

Before downloading an indexed order, match its exact URL and known alternate
URLs against acquisition records and page-specific review receipts. A collected
file alone does not prove review; an order review does not cover separately linked
forms. Preserve the original index audit and save subsequent dispositions in a
separate progress ledger. Broward's `review/index-reconciliation.json` records
receipt paths/hashes and review scope; `review/index-followup-progress.json`
contains the remaining queue.

For assignment orders, read the complete table and footnotes. Render ambiguous
cell pairings and formatting that indicates administrative or chairperson roles.
Store each assignment's printed name, division, page, effective date and citation;
keep issuance, immediate-effect language, delayed changes and temporary authority
separate. Only express vacancies become vacant entries. Link existing person keys
without replacing contact findings. Preserve printed name discrepancies and do
not treat absence from one order as departure from office. Collect the exact
referring index URL as `discovery_parent`, not a guessed generic orders landing
page. Correct a saved provenance error with an additional capture; retain history.
Artifact paths must be repository-relative; dependent freezing/readback steps run
only after a successful save acknowledgement.

### Senior judges and reciprocal assignments (Broward 141–142)

Reconcile the ordinary public directory against the current temporary/senior
assignment order before declaring the named roster complete. Broward's temporary
orders index (`https://www.17th.flcourts.org/temporary-administrative-orders-2/`)
contains the fiscal-year senior list; its 2026–27 order identified eight additional
people beyond the already reviewed Pole record. Keep each judge's research
sequential. Reciprocal circuit/county authority does not establish a permanent
division, current contact details, or departure from office when a name is absent.
Store the stated start/end dates; preserve preceding-quarter lists for comparison.

For a senior without an ordinary profile: check the surname-filtered judiciary
page, official site search, current senior appointment, Chief Judge page and the
linked Supreme Court Senior Judges page; then bounded official-domain searches
for that person's name plus assistant/contact/procedures. Save exact queries and
rejected stale leads. Do not import old contact-list search snippets, another
judge's current division contacts, a senior-application phone, or general
administration contacts into missing individual fields. Record unknown fields and
an incomplete source check; a bounded review with gaps is not a completed contact
record. Preserve separately labeled administrative inquiry routes without sending
requests unless authorized.

The Supreme senior page may return HTTP200 with only navigation in visible HTML.
Inspect `__NEXT_DATA__.props.pageProps.pageData` and reuse
`scripts/flcourts_folder.py` for a supported folder body. Preserve original bytes
and shell extraction, save derived content under a separate text hash, and read
that body before claiming it lacks individual information. See Broward's
`review/eade-search-log.json` and `receipts/senior-richard-d-eade-reviewed.json`.

### Dated directories and cross-circuit senior contact routes (143–145)

A search engine may return stale PDF text even for a live directory URL. Download
the original, inspect its printed report timestamp and relevant roster page, and
retain its hash. Do not replace that evidence with cached snippets. A generated
report timestamp is not an appointment or effective date. Preserve an older
static directory separately when it supplies a materially different statement.
Karlan's March19 Miami list names her;the October16 API-generated list does not;
Broward's October senior appointment still names her. Preserve dates and court
scope without treating omission as resignation or selecting controlling authority.

For a senior serving in more than one circuit, save a published coordinator route
with that court's scope. Do not label the coordinator as the individual's judicial
assistant or transfer the number into Broward chambers fields without evidence.
Langer's current Miami senior listing and PDF provide such a route. The directory
card's `data-judgeid` and query parameter only filter cards;they do not establish
an individual profile or procedure page. Save the actual link behavior inspected.
Reuse already collected current originals and shared surname filters for the next
judge, while separately reviewing that person's source associations. Academic CVs,
committee contacts and historical family assignments are not substitutes for
current individual judicial contacts/procedures.

### Completing bounded senior searches (Broward 146–149)

Finish each person's search log and cited receipt before starting the next person.
The eight newly identified senior judges now have individual saved reviews, with
missing current chambers/assistant/procedure fields explicitly unresolved. Do not
increase the completed-contact count merely because every name has a record.
Historical retirement stories, ordinary-seat vacancies and old contact lists do
not negate a later senior appointment or establish current contact assignments.
Match full names/suffixes:Joseph A.Murphy III is not John J.Murphy III.

For Speiser,save the2025assignment's title,individual division11/22footnotes and
signature as separate dated evidence;the reviewed pages are1,2,6of6. Current
retrieved foreclosure-page blocks name Pole/Garcia-Wood;do not transfer their
contacts/procedures to Speiser. Preserve discovery provenance:a document found
through a web query has that query logged and no invented referring-index URL.

The run-local `review/finish-basic-senior.py PACKET SLUG` verifies already saved,
frozen,partially documented senior records. It does not perform research or clear
missing-field checks. Run it only after save acknowledgement and successful
`freeze-replay-packets.py PACKET`;it rejects a stale packet before writing any
handoff. Its use does not replace source-specific legal/identity review or the
existing person validator. Finished bounded searches return the queue to county
index followups;genuine evidence gaps remain for county disposition.

### Alternate formats and dated civil orders (Broward 150)

Work from the retained index row and exact href. If a public index points to an
internal hostname (Broward's `callisto-vm` worksheet), record the href without
requesting it. Look for public alternatives on the same court and official Clerk
pages. Keep the missing original distinct from the alternate; do not claim they
are identical. An accessible DOC may supply the needed text even when its PDF
link is unusable. Save original binary bytes/hash/time before using `textutil`
for text extraction; preserve field codes and state that pagination/layout were
not reviewed. Do not feed an old binary DOC through the HTML extraction branch.

Reuse exact previously reviewed originals with receipt path/hash and JSON pointer.
For distinct original files, record the actual comparison performed. Equality
after removing whitespace/punctuation/page labels is only normalized text equality,
not original-file or layout identity. Retain each URL, hash and retrieval date.

Read a material order's scope before expanding research. Initial-rollout e-filing
orders remain dated historical evidence; do not turn their old division lists,
contact details or fee language into current instructions. Record express vacatur
without automatically researching the entire vacated order/case-law history.
Treat signature, effective date and nunc pro tunc date separately. A service order
limited to risk-protection proceedings does not authorize general commercial
service; document that screen and stop the low-priority subject review.

Save receipts under the county run's `receipts/`, evidence in `raw/` and `text/`,
and exact collection/text/visual scope in each receipt. Update only the reviewed
rows in `review/index-followup-progress.json`; preserve its original audit and
other queues. Save the bounded findings through the pinned county history helper,
then verify facts/artifacts, exact frozen replay and unchanged finalized reports.
An index row may be dispositioned with a documented unavailable alternate format;
keep a separate incomplete evidence check so it is not silently counted as collected.

### Operative text and alternate paths (Broward151)

Read the operative paragraph even when the title appears unambiguous. AO2012-51
is titled as a vacatur but immediately reinstates VI-02-D-3. Record the title and
actual action separately. Corrected2012-24 has a2016signature and2012nunc-pro-tunc
date; preserve both alongside the reinstatement without choosing current control.
Do not expand a traffic/criminal cost schedule into exhaustive review merely because
its generic title says court costs. Screen scope and save the collected attachment.

If a signature line omits a year, leave the complete signature date unknown and
store the stated month/day plus the order identifier's year in separate fields.
Broward2023-37/38 illustrate this; the filename does not supply a missing statement.

After an indexed public URL404, reuse an already retained official counterpart
or make a bounded alternate-path check where the site's observed migration supplies
a concrete lead. Record an inferred candidate path as such, never as a followed
link. Keep the404response and retrieved original separately. Match order number,
title, body and attachments before using the alternate; cached snippets alone do
not prove original content. For vehicle-title and emergency matters, include the
attached blank forms in the review and keep specific certifications/attachments
in structured facts. Do not submit forms or retrieve private case information.

### Conditional forms and completed index queues (Broward152)

Save applicability before extracting deadlines. The older county pretrial form
has a case-filing cutoff and an express end to its permitted use. Its mediation,
arbitration and some pretrial requirements depend on unchecked boxes. Preserve
the condition and anchor with each offset; do not convert blank historical forms
into present case deadlines. The possession order measures writ issuance from
judgment, with different60/30day periods; it is not a deadline measured from service.
Firm-specific filing exceptions stay separate from the general zip-code scheme.

Different official menus can expose different generations of the same form.
Broward's general-order index links older ADA forms while the ADA page links
newer filenames. Save both names, dates and originals; a filename's revision date
does not establish appointment, effective date or supersession. If a PDF contact
block is garbled in text extraction, inspect the rendered original and record a
separate visual transcription without silently rewriting extracted source text.

An empty index-followup queue means its identified rows were reviewed, reused or
screened with recorded scope. It does not establish roster/contact completeness.
Next reconcile the original county audit's limitations, contact states and prior
actions against subsequent saved findings. Preserve the original audit and create
a separate disposition ledger; distinguish bounded unavailable evidence, source
conflict, superseded task status and genuine unfinished research. Do not restart
completed reviews merely because their original audit entries predate later work.

### Gap disposition before county export (Broward153)

Use `review/county-gap-disposition.json` alongside the immutable original audit.
Every original limitation/contact/action keeps its original observation reference
and value. Preservation categories are not resolutions: unavailable content stays
unreviewed, unknown fields stay unknown, and conflicts stay attributed. Update a
stale pending task only with a later saved finding/receipt; Marra's completed review
does not resolve Rebollo's present identity/contact gap. Treat named direct emails,
separate assistant lines,faxes and hours independently from published shared routes.
An explicitly unavailable fax is different from a failed search or an undated fax.

Reconcile assignment names as sets, not row counts: a person may serve multiple
divisions. The ordinary Broward order names89judges/12officers; a separate order
names9seniors. Existing person reviews cover every ordinary-order name and Pole;
the8additional seniors have bounded reviews with missing individual evidence.
Do not add seniors to occupied ordinary seats or silently count historical Rebollo
as a verified current contact. Keep his source association available separately.

Include every referenced receipt in a save packet's artifacts, including nested
additional-limit references. The validator rejected153before save when two such
receipt references were omitted; adding the actual hash-checked receipts repaired
the packet. Do not weaken validation or replace missing bytes with summaries.
The next phase is a review/export packet, followed by source/normalization and
presentation checks; the ordinary `directory` command imports its bundled dataset
and is not by itself an importer for arbitrary county-history findings.


### Read-only county review export from capture4886

Broward read-only review export built from capture4886: output/county-review/broward-4886/index.html. 178 exact saved findings (98 judge,12 officer,clerk,administration and shared procedures/reconciliations),1274 original/extraction artifacts. All facts/citations and artifact bytes read back;2398 local links checked;deterministic second export and unchanged database/directory/finalized reports verified. Six exporter tests and24 directory/history regression tests passed. No browser visual check or public release. Next inspect and implement the bounded production-directory integration: preserve all existing counties/history, explicitly add reviewed Broward scope, map source-attributed contacts without substituting historical/ancillary values, preserve conflicting assignment evidence, and review rendered output. Eight senior contact gaps and Rebollo historical/current uncertainty remain explicit. User county review before another county. Statewide goal active; cloud direct.

See `docs/workflow/COUNTY_REVIEW_EXPORT.md` for the reproducible command and
limitations. This export is not a new research observation and did not advance
the comparison baseline. Retain the immutable checkpoint153 and its frozen replay.


### Dated directory integration draft

Broward website integration draft built: output/county-review/broward-site-4886-v4/directory.html; pending supplement draft/county-directory-4886-v3.json derives from capture4886.112personnel records:89ordinary judges,9seniors,9magistrates,3hearing officers,clerk and court administrator. Default view combines them with181existing personnel;explicit issue/date queries retain saved historical contacts. 810projected contact lines and source observations/citations checked against packet;five archived reports/10historical JS selections unchanged;CLI preview deterministic and production gate rejects draft. 74focused/regression tests passed before final circuit-membership display adjustment;final actual-data CLI/Node check and JS syntax passed afterward. Source contact qualifiers retained in expandable notes;8senior gaps and Rebollo historical/current uncertainty preserved. No browser visual check: prior wrapper permission denial,execute bits absent;no workaround. Next complete manual projection audit for112records and omitted field ledger,inspect final rendered directory when browser capability is available,then present concrete county checkpoint for user review. Use docs/workflow/COUNTY_DIRECTORY_INTEGRATION.md. No research capture/finalized report changed,no public release,no next county. Statewide goal active;cloud direct.

### Hillsborough clerk services: source and comparison procedure

Start from the actual clerk navigation captured in
`runs/county-hillsborough/2026-10-16/review/clerk-core-links.json`, then use
`review/clerk-civil-followup-routes.json` to select an unfinished material topic.
Search `review/acquisition.json` for exact URL and same host/path variants before
fetching. A case/query variant is a reuse candidate, not proof of equal bytes.
For a collected source, use its latest matching review; do not reset a reviewed
service to pending merely because another page links the same destination.

The six service pages reviewed in packet78 are:

- `/court-services/court-registry`: deposit tender, signed-order instruction,
  registry fee, release estimate and public balance route.
- `/court-services/efiling`: Portal exceptions, division-assignment request,
  summons and writ issuance, publication process, exhibits and eviction mailings.
- `/court-services/foreclosure-sales`: dated changes, sale fees, notice/proof,
  bidder deposits, final payment, objections and cancellation.
- `/Court-Services/Serving-Summons-Subpoenas-and-Documents`: sheriff versus
  private process-server routing, contact phone and outside-county service.
- The preceding path plus `/Subpoena-Issued-Pursuant-to-UIDDA`: foreign subpoena
  issuance, separate preparation/issuance charges and official rules routes.
- `/court-services/attorney-and-pro-se-legal-resources/judicial-division-lookup`:
  static map instructions and the already reviewed S-2024-079 original.

The host for these paths is `https://hillsclerk.com`. Preserve the exact retained
URL, original bytes, extracted text, retrieval timestamp and stated dates from
the manifest. Main content follows the page's `h1`; repeated navigation is not
new procedure content. UIDDA's fee instructions occur after an intervening Court
Services menu, so stopping at that menu would omit relevant information.

Save actual anchors in a source-bound link inventory. In this review, the E-Filing
anchor labeled County Civil downloads the summons-request form. The division
assignment and sale-cancellation links also download PDFs. Inspect checkbox
hierarchy, revision footers and embedded links on their page images. A PDF link
rectangle must be serialized as numeric coordinates before saving JSON; a
PyMuPDF Rect is not directly JSON serializable. Do not modify source PDFs.

Store source findings separately from cross-source discrepancy findings, with
exact citations. Preserve payment methods and charges by service. Keep service
estimates separate from party deadlines and preserve amount, unit, direction,
trigger, actor and conditions. In particular, certificate filing and issuance
are different triggers, and prior day does not mean prior business day. Form
choices are not established case-specific response deadlines. Map classification
does not establish which address controls filing under an administrative order.

Packet78 contains nine new document reviews and one discrepancy finding;
`receipts/clerk-services-reviewed.json` records their scopes and four visual page
checks. Run-local `save-clerk-services.py` assembled the checkpoint through the
existing helper. It is a one-shot historical assembler; resume from state and
replay the immutable packet rather than rerunning it. Validation confirms exact
citation support, all artifact/fact read-backs, replay, prior findings and finalized
report preservation. Remaining routes concern records/access, fees, evictions and
judgment interest; those are not marked reviewed by this checkpoint. Officer
reviews remain separate and sequential. No live form, filing, payment, auction,
personal-case search or map interaction is needed for this evidence review.

Hillsborough packet79 completes the next clerk source review batch. Start from
`review/clerk-remaining-request.json` and its parent routes; child URLs are in
`review/clerk-remaining-children-request.json`. Reproduce the observed sources,
not guessed legacy paths. `review/clerk-remaining-links.json` retains actual
anchors and image alt labels. Paper-file instructions omit button names in plain
text extraction; inspect original `img` alt values and the email anchor before
recording the steps or contact. A generic email-us label alone is not an address.

For the fee page, use actual HTML tables and direct row cells. Reviewed indices
0/1/2/4/5/17/18 correspond to general, county appeal, circuit appeal, circuit civil,
county civil, real estate and recording services. The 88 saved rows retain their
indices, exact labels and value strings, including malformed inequality expressions
and conflicting summons charges. Do not normalize these into a computed fee rule.
Future table indices may change: confirm section headings and representative rows
before reusing this mapping. Preserve multi-part rows without guessing omitted
conditions or treating a blank value as zero.

Read closure exceptions after the holiday table. June19 court-service locations
are expressly open despite the starred holiday entry; the PlantCity March2 closure
is location-specific. For confidentiality, distinguish submission to clerk from
service on parties. Review both pages of the notice: its second page contains
qualifiers and timing. For eviction, retain the chart's explicit residential scope;
shared registry/mailing operations do not make every chart deadline commercial.

Legacy CFO link failure was preserved, then official-domain search located the
current rate page. The independent current URL and original are in
`review/clerk-interest-request.json` and `clerk-interest-current` acquisition entry.
Store all four rate-table columns with effective dates; percent and decimal daily
rates are distinct fields. No rate calculation or selection for an individual
judgment occurs in a baseline review. Current retrieval does not backdate a capture.

Do not mark search applications reviewed from HTTP success alone. Packet79 keeps
HOVER transport/web failure and official-record HTTP200 shell as incomplete shared
access evidence. `review/clerk-browser-attempts.json` records iab unavailable and
empty browser inventory, rather than claiming a successful browser check. Continue
other authorized research while those limits remain explicit; do not repeat the
same failed action indefinitely or bypass unavailable browser controls.

`receipts/clerk-remaining-reviewed.json` and immutable checkpoint79 retain13 source
reviews,7 discrepancies,3 visual PDF checks,88 fee rows and the access limitations.
Validation covered26 citations,2051 artifact read-backs,411 findings, replay and
unchanged prior facts/finalized reports. Next person is the first pending officer
in `state.json`, Michelle Blume. Review her basic family operating procedures and
contacts before moving to the next person; shared access followups remain separate.

### Hillsborough officers: basic-scope example

Use `state.pending_officers[0].profile_url`, not a name-derived URL. Michelle
Blume's roster URL redirects; retain both requested/resolved URLs. The generic
Judge Alvarez H1 does not override the substantive magistrate header, biography
and official roster. Verify the administrative assistant's published role rather
than calling every assistant a JA. Keep family and dependency email/Zoom routes
separate, and preserve a fax's stated notice/cancellation purpose.

`review/blume-links.json` records actual mailto/tel/aria and linked form targets.
For basic family review, use profile scheduling, communications, submissions,
appearance and shared-access sections. Do not exhaustively fetch family forms or
review temporary-relief/parenting merits. A legacy Skype paragraph naming another
magistrate is an association defect; retain it without copying the other person's
contacts or resolving control between competing appearance instructions.

The official roster's General Magistrate Division Referral Assignment Table is
saved as `officer-referral-assignments`. Its one-page PDF is revised2026-10. Check
column boundaries visually before associating suffixes and contact rows with a
person. Packet80 reviewed only Blume GM-3; later officers reuse the original and
review their own relevant entries. A name on that page is inventory, not completion
of contacts/procedures. Probate officers may not appear in a family-referral table.

Keep `entity_type=general_magistrate` or `hearing_officer` and use
`scripts/officer_review.py:validate_officer`, which supplements the legacy person
validator with assistant-role and individual-procedure checks. Packet80 exercised
it on the real receipt with50 nested citation checks. Preserve scoped checklist
and linked documents with applicability/review status. No validator weakening or
role relabeling is needed. Save the officer finding as `county_officer_baseline`
for the existing county review/export path. Maintain completed/pending officers
separately from the69 opening judge profiles and validate total15 after each save.

Cadigan packet81 adds a second officer example: probate/guardianship/trust GM1
is not the family GM1 referral-table assignment. Keep division labels qualified
by case type. Inspect phone icons in original markup when plain text loses their
meaning: his second number is labeled by `fal-fax`, with no separate fax anchor.
`review/cadigan-links.json` retains that markup, URL, hashes and retrieval time.

Read individual order-delivery instructions before applying shared conventions.
Cadigan permits Word orders by email or his own JAWS magistrate queue; Blume says
not to use JAWS. Cadigan's hearing IDs/passcodes are unique and office supplied,
so an unknown public Zoom ID is not a missing-contact research task. Preserve
property-report recency as twelve months and distinguish confidential document
delivery to the clerk from filing in the public case record.

Reuse `hillsborough-probate-ao-s-2022-020` and
`hillsborough-probate-diligent-search-form` for the previously reviewed shared
civil/trust referral and constructive-service sources. Retain source dates and
scope. A guardian-screening order link and specialized guardian/physician forms
do not require an exhaustive noncommercial review. Cadigan's generic JudgeAlvarez
heading defect is recorded; substantive header/biography/roster support identity.
Packet81 validates his actual officer receipt,36 citations,2069 artifacts/414
findings, replay and preserved finalized history. At packet81, Tracy Ellis was next;
use the county handoff and state file for the current pending officer.

Neaves packet84 demonstrates why superficially similar profiles still need an
individual read: her Word-order email and JAWS report-delivery registration do
not include Cadigan's alternative upload queue. An omitted alternative is neither
permission to import another officer's instructions nor an express prohibition.
Reuse shared document reviews, preserving each person's actual submission rules.

When an officer profile says `Administrative Assistant: TBD`, do not import `TBD`
as a verified person or guess from an older guide. Check the official profile,
roster/shared contact table and a bounded official-domain name/office search.
Save `assistant_name.status=not_published`, `value=null`, the exact published
placeholder separately, `absence_reason`, source citation, and `search_log` rows
with URL/search/result. Keep the published role and shared office phone/email
verified independently. The officer validator enforces this documented absence
path; a completed source review can retain an unknown name for a later refresh.
Williams packet87 exercises this distinction alongside unrelated-person names
left in exhibit/Skype sections: preserve those clauses as source discrepancies,
not current staff or a reason to research those other people.

Frank revision 1 (accepted packet89) exercises the negative-procedure contract:
his profile is contacts-only, so `procedure.status=no_published_procedure_located`
carries the profile citation, an absence reason and a structured search log over
the profile, roster, GM/HO referral table and AO index; `documents` is empty and
the applicable shared division order (S-2025-057 Civil Traffic Division,
Division Z-2) is recorded in `governing_rules` with its own reviewed scope, not
as a Frank procedure. The office email is a documented `not_published` field
with its own checked search log. Missing email/procedure are evidence
limitations, not conflicts; the only recorded conflict is the generic Judge
Alvarez H1. The S-2025-057 association to Frank is division-level (the order
designates Division Z-2 and the roster lists exactly one civil-infractions
hearing-officer card); the order does not name individual hearing officers, and
cloud checked page4: enteredOctober31,2025,ChristopherC.Sabella,ChiefJudge. The
original ScanSnap OCR omissions and scanmetadata remain preserved.

### Native browser source recovery (Palm Beach clerk directory)

When HTTP and web retrieval fail but the official page renders in a native browser,
use `cua.getApp` with the available browser application. An empty browser-provider
inventory does not establish that native app control is unavailable. Verify the
loaded page URL and content; use Save Page Source to retain original HTML. Inspect
the save destination and actual filename before claiming persistence. Extract text
from the saved bytes; preserve original and extracted hashes and retrieval time.

Do not invent HTTP 200 when the UI does not expose a response status. Set
`http_status: null` and include `browser_capture.observation_sha256`, referring to
an immutable JSON artifact with `method: native_browser_save_page_source`,
`content_reviewed: true`, `page_url`, `original_sha256`, `observed_at`, `page_title`,
and a concrete `review_note`. URL, raw hash and timestamp must match the citation;
store this observation artifact in the checkpoint alongside the original HTML.
The validator still verifies quote/text hashes, public URL, official provenance and
timestamps; known non-200 results cannot use this alternate path. This receipt is
an auditable researcher observation, not an independent HTTP-status measurement.
Record access-denied/challenge pages as failures, never as reviewed source content.
A recovered directory resolves only that directory's content gap; unrelated
biographies, forms, PDFs and procedure pages require their own successful reviews.

Browser PDF recovery extension (Palm Beach packet187): when native Safari renders
an official linked PDF but direct HTTP returns403, save the PDF itself with Save,
without filling fields. Preserve the earlier failed response. Use the same browser
observation linkage as HTML, with method `native_browser_save_pdf`; do not invent
HTTP200. The checkpoint validator requires a PDF signature and a readable PDF with
at least one page, in addition to the URL/hash/time/review checks. Visually inspect
all pages and inventory widgets/choices and link destinations before content-review
acceptance. PDF metadata and URL suffixes are not stated legal revision dates.
Test coverage includes valid replay, malformed PDF, HTML posing as PDF, known403
and mismatched original hash. Actual source authenticity and legal accuracy remain
researcher review duties, not claims made by the structural validator.

### Shared-order coverage reconciliation

Before repeating a county order review, inspect the prior finding's source-specific
review node, not merely its top-level citation list. Record the finding key and
nested facts path, actual page/content scope, source URL, original hash and text
hash. Verify retained bytes against both hashes and the current checkpoint's
artifact registry. Preserve the original observation/review dates and any partial
review or unresolved conflict. Reuse does not establish a fresh retrieval.

An individual standing order that cites an administrative order is not a review
of that administrative order. Reject such incidental-reference matches even when
its citation inventory contains the target URL. Palm Beach checkpoint206 records
this distinction for DiGangi's standing order versus AO3.110. Preserve judge-specific
comparisons in reused summaries as comparisons; do not promote them to county-wide
requirements. Only advance the coverage queue for the actual scoped review accepted.

## Research-depth correction — October 18 user feedback

The user identified scope drift into particular litigation. Prioritize the statewide
personnel/contact baseline, each judge's practical civil procedures, and broadly
applicable filing, scheduling, service, submissions, remote appearance, courthouse
access and material court administration. A county baseline is not an exhaustive
analysis of every administrative order, specialized docket or historical program.

Screen specialized and historical orders for scope and status. Ordinarily retain
the official link, any already collected original, and a concise applicability or
vacatur note. Do not extract case lists, old reassignment schedules, program forms,
merits requirements or every deadline unless a concrete current effect on general
civil/commercial practice requires it. An index entry is a screening candidate,
not automatically a mandatory full-content review. Explain any exception before
expanding. Existing material findings remain preserved; no deletion or relabeling
of collected-only documents as fully reviewed.

For Palm Beach, stop exhaustive order-by-order expansion. Screen the remaining
specialized candidates, reconcile roster/contact and practical-procedure gaps,
and proceed to county validation and the next county. Do not hold completion for
exhaustive historical or specialized litigation analysis. Genuine missing required
contacts/evidence and publication validation remain separate requirements.


### Twentieth Circuit roster discovery check

The judiciary page uses separate `judge`, `Magistrate`, and `HO` classes. Enumerate all county-tagged profile cards, not only cards with the `judge` class. Reconcile profile URLs against saved records; classify vacancies separately and verify officer assignments individually. Lee reconciliation evidence: `runs/county-lee/2026-10-19/review/roster-reconciliation.json`.
