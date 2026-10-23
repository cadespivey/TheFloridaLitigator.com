> Execution policy: [use the invoking model](../../workflow/MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Broward County — research handoff

Selected by the user as the first statewide expansion county on October 15, 2026.
Status: see the current checkpoint below. This handoff preserves both current
review status and historical source observations; it is not a blanket freshness
certification for every linked source. Follow ../../workflow/STATEWIDE_BASELINE_GOAL.md.

Current checkpoint: Broward manual contact-presentation review completed for112personnel against saved capture4886. Current preview output/county-review/broward-site-4886-v6/directory.html;pending supplement draft/county-directory-4886-v5.json. 729display rows;72duplicate chamber-code lines and9empty lines omitted with reasons;402ancillary/source-format fields retained in full research packet. Allcontactfields accounted;19reviewed contact-difference notes for18people pinned to exact conflict hashes. Manual audit review/directory-manual-presentation-review.json;actual validation review/county-directory-v6-validation.json. 78tests passed;CLI rebuild and historical JS selection preserve all5reports and181existingpersonnel,default293. Compact docs/research/counties/broward-quickstart.md tested (1602byte one-person context);roadmap67unique counties:7existing,59planned,Browardreview. Browser verification remains unperformed. A user question asks permission to add execute permission to the installed Playwright wrapper;await explicit response,no workaround. After browser review (or user election to perform it),present/complete usercountycheckpoint before anothercounty. Eight senior individual-contact gaps and Rebollo historical/current-identity limits remain recorded;not blockers requiring invented values. No newsourceacquisition,DBcapture,reportfinalization orpublicrelease. Goalactive;clouddirect.

Start with [the bounded quickstart](broward-quickstart.md). The material below is
a historical research log: earlier pending-task statements are superseded by the
current checkpoint and state, not instructions to repeat completed research.

## Verified discovery paths

Start at the [Seventeenth Judicial Circuit](https://www.17th.flcourts.org/).

| Information | Navigation and destination | What to inspect/save |
| --- | --- | --- |
| Roster, assistant, phone, room/division, individual procedures | Home → Judges & Magistrates → Judges Practices & Procedures → [Judiciary List and Category](https://www.17th.flcourts.org/judiciary-list-and-category/) | Table columns include Judge, Judicial Assistant, Phone Number, Chamber, Courtroom, Division and Division Procedures. Save the rendered roster and linked judge/procedure destinations. |
| Division-specific responsibilities and shared resources | Home → Court Divisions → [Divisions of the Court](https://www.17th.flcourts.org/divisions-of-the-court-new/) | Follow Circuit Civil, County Court Civil and Criminal, Foreclosure, and other applicable civil/shared links. Do not substitute division descriptions for judge assignments. |
| Material local rules and administrative orders | Home → Court Reference → Administrative Orders & Local Rules → [Administrative Orders](https://www.17th.flcourts.org/administrative-orders/) | Screen Civil, County, General and Temp categories and the Local Rules table. Follow relevant original orders and later modification/repeal evidence. |
| Courthouse street addresses | Home → Locations | Separate Main, North Regional, West Regional and South Regional. Match location to the particular judge before recording a street address. |

The roster table's explanatory note defines WW as West Wing, NW as North Wing,
and N/S/W as North/South/West Satellite. Preserve the original room code and the
source supporting any normalized address. Do not assume every judge sits downtown.

## Observed extraction issue and recovery

The initial web text extraction returned category controls and table headers but
no judge rows. Treat this as an extraction gap, not an empty roster. The rendered
table loads a public JSON response from `/wp-admin/admin-ajax.php`, using POST
form fields `action=sls_body_tbl_c`, `searchCatSlug=all`, `tplateID=2611`,
`debugt=0`, `topr=0`, `loops=0`, `staffTplateID=407`. This is a read request.
The response fields are F1 name, F2 assistant, F3 phone, F4 chambers, F5 courtroom,
F6 division, F8 procedure-link display, F9 Zoom link, F10 meeting ID. Circuit-civil
filter uses `searchCatSlug=circuitcivil`. Verify these against current page code
before reuse; parameters can change.

On October 15 the seven rendered pages contained 15/15/15/15/15/15/6 rows, matching
all 96 response rows by name multiplicity. The set contains duplicated names,
three docket labels and one unnamed row (division 62/SB); these are not 96 people.
There are 90 distinct named entries, pending reconciliation with the assignment
chart and current individual profiles. Keep multiple assignments for a person;
do not research the same person twice. Save unresolved rows rather than inventing
a vacancy or person. Sources are under `runs/county-broward/2026-10-15/raw/`;
`roster-browser-pages.json` preserves the rendered pages, and
`roster-response.json` preserves the server response.

The `/judiciary/` page links an October 2026 assignment-chart PDF, currently
`/wp-content/uploads/2026/10/Judiciary-assignment-chart-10-02-2026-C1.pdf`.
Its chart labels 90 judges (58 circuit, 32 county); this stated total is not proof
that all named roster entries match. Its columns must be read visually, because
plain text interleaves county satellites and probate. Magistrates/hearing officers
occupy a separate column. Preserve the chart's month and the filename separately;
do not infer an effective date from its upload path.

After that inventory step, finish the selected first civil judge's contacts,
assignment and procedure checklist, including linked PDFs, before moving to another
judge. Save the exact profile URL, links followed and any further field locations
here as they are learned. Reuse shared documents already saved for the county.

## Completed judge: Shari Africk-Olefson, Division 25

Profile: `https://www.17th.flcourts.org/2726-2/?smid=8348`.
Procedures: `https://www.17th.flcourts.org/division-25/` embeds a published Google
document. Follow its iframe and save the published HTML itself, not merely the
wrapper's near-empty text. The acquisition manifest at
`runs/county-broward/2026-10-15/review/acquisition.json` records the exact published
URL, original/text hashes, retrieval timestamps and official discovery parent.
The profile fields give assistant Joshua Carrasco, phone, chambers and courtroom;
the document header supplies assistant email, fax and street address. Do not
label the division email for in-camera submissions as the judge's personal email.

Core instructions end at `*END OF DIVISION PROCEDURES*`; the same original includes
sample pretrial and special-set orders. The sample pretrial order says revised
December 3, 2024; do not assign that date to the entire document. Preserve its
internal courtroom discrepancy (header 15150 versus later 14155), differing
emergency-order references, and apparent tensions concerning trial readiness and
proposed orders. Record the statements and locators without resolving authority.
The original's own applicable-law qualification is also part of the evidence.
Individual review was completed and validated using the existing `_person` and
`_citation` validators. Capture 4274 (see current state below) preserves the full
receipt and source passages, with semantic facts stored separately from retrieval
metadata. Twenty checklist topics cover individual and applicable shared procedures.
This does not certify the county roster or all shared sources complete.

## Materiality and historical checks

- Investigate the user's ZIP-code/geographic filing lead through county/civil
  orders and clerk filing pages. No controlling address, rule number or current
  legal requirement has yet been verified.
- Investigate local AI-use/disclosure requirements and any express later Florida
  Supreme Court action. Do not assume blanket supersession.
- The Local Rules index visibly distinguishes two Rule 10A links by dates around
  March 5, 2018. Collect and read the applicable original and check later changes;
  an index label alone is not a current-law determination.
- Clerk, Official Records, Court Records, property-appraiser source paths, working
  acquisition/persistence commands, and saved capture IDs remain to be filled in
  through research. Do not invent them or mark these tasks complete from this map.

## State and storage

Use a new ignored workspace under `runs/county-broward/`. Preserve original bytes,
extracted text, per-judge receipts and a small handoff identifying the active judge
and exact next action. The shared research database remains
`~/.local/share/flwu/research-history.sqlite`; do not write to the legacy directory
database as a substitute for evidence capture or change the old stream's scope.
Document and validate the actual evidence-to-database save steps during the first
judge review; that working recipe becomes part of this handoff for later agents.

Initial persistence has now been exercised through existing `history.record`:
capture 4272, ID `a033102935f1880b5e97896945c6413589b57aa651739aa1e8b5e2b398ad160b`,
stream `manual_research:county-baseline-v1:6bf5ac02ab39`. Scope is exactly
`{"profile":"county-baseline-v1","county":"broward","circuit":17}`.
The packet is `runs/county-broward/2026-10-15/draft/checkpoint-01.json`; artifact
paths are relative to the repository root. Save receipt and read-back validation
are in `review/history-capture-01.json`. This capture contains 28 original/text
artifacts and an incomplete judge-review draft, not accepted findings. Hashes,
retrieval timestamps and quote containment were checked; identical replay was
idempotent and finalized reports did not change. The interrupted local-worker
draft remains preserved in `runs/county-broward/worker-save`. Direct cloud review
subsequently repaired and validated the helper in `src/flwu/baseline_capture.py`;
follow [BASELINE_CAPTURE.md](../../workflow/BASELINE_CAPTURE.md) for future saves.
The helper/history/publication/as-of run passed 159 tests; actual packet18 replayed
successfully in a temporary database. It still requires prior person/content
review and subsequent read-back. Reserve local agents for retrieval and analysis
after the research and update workflows are built and validated.

Resume from `runs/county-broward/2026-10-15/state.json`. The completed first-judge
receipt is `receipts/person-shari-africk-olefson.json`. Shared follow-through used the
official Civil and General order indexes (`/civil-administrative-orders/` and
`/general-orders/`). AO 2021-50, 2022-31, 2022-37 (Amendment 1), 2022-44,
2025-44 and 2021-20 originals are now collected and reviewed, alongside Local
Rules 8/10A and older linked originals. `receipts/shared-civil-reviewed.json`
contains exact review scope, dates, summaries and page citations for reuse.
The 73-page AO2025-24 compilation is collected in full; main order, circuit
general/streamlined forms and Exhibit L are reviewed (physical pages 1–22, 51–63,
72). Complex and county forms remain for their applicable shared review tasks.
Do not treat that partial review as full compilation review. The jury order's
older November-2025 URL returned 404; the current index links its April-2026 path,
which returned the original dated November 18, 2025. Upload path is not issuance.

Completed-person capture: 4274,
`0d10660293f6704620ac8e1a98d62f7adbd9796b89b07ca79f24e41797e184b1`.
`draft/checkpoint-02.json` and `review/history-capture-02.json` preserve input and
verified acknowledgment. All 104 nested citations were checked, artifact bytes and
semantic facts read back, and replay idempotence/finalized-report preservation
verified. The public website has not been changed by these incomplete-county saves.

## Completed judge: Catalina Avalos, Division 04

Next in saved circuit-civil roster. Profile:
`https://www.17th.flcourts.org/2726-2/?smid=2804`.
The official profile/roster directly links a shared Google document (ID
`102Z2eylT4IhqexnuYF5Sci_PPF5CsEWKZdqXei3qVko`), rather than a court-hosted PDF.
Save the original shared page and, when publicly available, its PDF export to read
the complete procedures. Record export URL and official discovery chain in the
manifest. Do not treat an edit-page text extraction as the complete document.
The public PDF export returned the complete 14-page document. The edit-page
extraction contained only application controls, so it was not used as substantive
evidence. The two-page calendar-call form was downloaded from its official-linked
Drive file. Both were read; header and screenshot-heavy appendices were checked
visually. Capture 4276 saves the validated review (`draft/checkpoint-03.json`,
`review/history-capture-03.json`); next judge is Martin J. Bidwill.

Important reuse/discovery lessons from this judge:

- Inspect PDF hyperlink targets as well as visible text. The displayed Division04
  email points to a Division38 mailto link; preserve the mismatch separately.
  `division04-link-annotations` in the manifest preserves extracted targets from
  the original PDF. Do not replace the displayed contact with the link target.
- The original header says updated September29,2026; the footer says revised
  August7,2026. Preserve both with their locations rather than choosing one.
- AI-order reference: January-path Amendment1 link returned404; official search
  found `/wp-content/uploads/2026/04/AO2026-03-GEN-Amendment-1-Use-of-AI-in-Court-Filings.pdf`.
  The official May19 press-release PDF contains a hyperlink to Amendment2 even
  though ordinary text extraction does not show it. Amendment2 expressly supersedes
  Amendment1. The General index's AO2026-19 expressly vacates Amendment2 effective
  June15,2026 at12:01am. All three originals were collected/read. The later judge
  document still references Amendment1; this discrepancy does not block the review.
- Reuse LocalRule10A, emergency order, remote-evidence rules, ESI order and
  case-management forms from the shared receipt. AO2022-5 rehearing instructions
  have now also been collected/read. Shared source reuse must not carry another
  judge's individual procedure requirements into the new judge's record.
- Do not collapse conflicting calendar-call attendance, email spelling, Zoom
  one-tap meeting, paper-copy exception, or summary-judgment timing instructions.
  The receipt stores each relevant passage. For track-specific deadlines read the
  appropriate form and actual case order, not a prior judge's checklist.

## Completed judge: Martin J. Bidwill, roster Division 27

Profile: `https://www.17th.flcourts.org/2726-2/?smid=2749`.
Its procedure link leads to `/multiple-procedures/`, then `/division-05/` and
`/division-27/`. Each embeds a public Google published document. Save both wrapper
pages and both embedded originals, keeping the official discovery chain. Both
name Bidwill; the roster lists 27. Do not infer a current Division 05 assignment
solely from its extra linked procedure page. Record checklist requirements by
stated division, including different UMC days and remote-appearance instructions.

Both documents were read in full. Capture 4280
(`2ce3b44c2926199b1f295d975b263d3f2cbdc7d840edf84c12e136ea03cfe104`)
saves 17 checklist topics, ten discrepancies and all 39 acquisition-manifest entries.
The receipt is `receipts/person-martin-j-bidwill.json`; packet and acknowledgment
are `draft/checkpoint-06.json` and `review/history-capture-06.json` under the run.
All 214 nested citations validated; 77 artifacts and semantic facts were read back;
identical replay and unchanged finalized reports were verified. Next: John B. Bowman.

Shared case-management compilation pages 23–36 (complex business forms) were read;
pages 37–50 (complex tort) were compared in full, page by page, removing whitespace
only. Differences were track/exhibit labels and one placeholder underscore; all
were reviewed. Page 29's deadline table was visually checked. Save the comparison
in `review/complex-business-tort-diff.txt` and reuse the updated shared receipt.
County forms on pages 64–71 and 73 remain collected, not reviewed. A template's
track requirements are not evidence of a particular pending case's assignment or
computed deadlines. Apparent calendar errors and placeholder dates in judge
procedures remain source discrepancies, not silently corrected dates.

## Completed judge: John B. Bowman, Division 02

Profile: `https://www.17th.flcourts.org/2726-2/?smid=2752`.
Procedure wrapper `/division-02/` embeds a public Google published document. Both
wrapper and original were saved. Full text and appended discovery-order form were
read; revision precision is September 2026, not an invented September day. The
form's preprinted 2024 year is separately retained. Capture 4282
(`7d96a0eeb95ecf2b9fed6899448ae3d2bfadd061e78104df221660f39bc374fb`)
contains 19 checklist topics and seven discrepancies, with 172 nested citations
validated, 88 artifacts/facts read back, replay and finalized-history preservation
verified. Receipt: `receipts/person-john-b-bowman.json`; checkpoint/acknowledgment
07. Next judge: Daniel A. Casey.

Do not copy another judge's electronic-only submission method into this record.
Bowman publishes paper submission requirements with electronic agreed-order and
courtesy-copy exceptions, and a separate appellate email route. Store these as
separate checklist topics with exact scope. His assigned courtroom clerk contact
is limited to exhibit questions; it is not the elected Clerk of Court contact.

Directly cited Local Rule 11 was collected through the Administrative Orders
landing page and read. Its official text expressly concerns county court civil,
although Bowman's circuit procedures cite it. Record this discrepancy, not a new
interpretation of applicability. The General Orders index supplies both
`I-94-o-1.pdf` (1994 order plus older attachment) and
`Standards_of_Professional_Courtesy.pdf` (Version 1.4, no date located). Both were
read; the older three-column page was checked visually. Four versus five business
days' hearing notice and aspirational versus expected conduct remain attributed
to their respective documents. Neither an upload-folder date nor a side-by-side
index link proves supersession. Reuse these shared originals and summaries rather
than searching them again for every judge.

## Completed judge: Daniel A. Casey, Division 03

Profile: `https://www.17th.flcourts.org/2726-2/?smid=8352`.
Wrapper `/division-03/` embeds document ID
`1X0rsRCdYFd3hZgbRF8OoVqffNgsHIUHJjy0fcKn2vik`. The first public `/pub?embedded=true`
request returned HTTP500; retain that failed response with its status. A public
`/export?format=pdf` request and retry of the original both returned200. Their
text matches after removing whitespace and extractor PAGE markers only. Both
were read in full; PDF pages1,6,7 checked visually. Do not treat a transient error
as proof the procedures are unavailable, and do not cite its error body as rules.

Capture4284 (`07ef51dc63fd645796e1fb08fb78b2145041da132493b2bee6bb32d71760dae6`)
saves20topics/fourdiscrepancies,183nestedcitationvalidations and98verifiedartifacts.
Receipt `receipts/person-daniel-a-casey.json`; packet/acknowledgment08. No overall
revision date located; June15,2023 belongs only to the hearing-mode policy.
Do not convert working days to calendar days. Distinguish preferred ten-day
courtesy timing from mandatory five-day uploads for shorter hearings and ten-day
uploads for hearings over60minutes. The25page threshold concerns delivery method,
not a motion-length limit; exactly25pages is unstated. Preserve order-submission
exceptions and conflicts. Next judge: Michael Davis, whose two roster rows must
be handled together before moving to another person.

## Completed judge: Michael Davis, civil 24 and criminal FN/ZD

Two official profiles: `/2726-2/?smid=400` and `/2726-2/?smid=18450`.
Procedure wrappers: `/division-24/` and `/division-fnzd/`. Both link published
Google documents. Match name, assistant, phone and chambers across both before
consolidating the person; keep the distinct profile URLs, assignments, procedure
links and Zoom IDs. Do not merge this person with N. Hunter Davis.

Civil procedures read in full. The short FN/ZD contact/assignment page was read;
its drug-court handbook URL was recorded only, not collected or substantively
reviewed. This follows the user's criminal/diversion priority. Karen Sisson's
published contacts are shared division contacts, not an inferred personal email.
Civil profile email div38 differs from procedure div24; letterhead WW11131 differs
from body/profile NW6790; two civil Zoom IDs differ. Preserve each location.

Capture4288 (`ad5265c2ec5358e599603f80d1fc89f9d32d2c435463f3872ff44b4801dc6ddb`)
is the latest reviewed version; initial4286 remains in history. The later save
improves prose readability, not legal-source content. Receipt:
`receipts/person-michael-davis.json`; packet/acknowledgment10. All228 nested
citations,118artifacts/facts, replay and finalized-report preservation checked.
Next: N. Hunter Davis.

Reusable shared-source findings:

- The civil index supplies `/wp-content/uploads/2026/04/2025-22-Civ-Combined.pdf`.
  Read its five-page body and Forms A/B. It expressly vacates every 2017-35 version
  still referenced by the judge. Complex business/tort filing criteria, forms,
  hearing routes and thresholds are material commercial procedures. Record the
  body/form construction, arbitration and trial-duration differences; do not
  choose a controlling threshold. Forms A pages6–7 were visually checked.
- The judge directly links the 2018 appellate communication guidelines and
  `/wp-content/uploads/2019/01/2019-6-Gen.pdf`; both originals were read. The older
  guidelines cite2018-93;2019-6 expressly vacates it. Its referenced Exhibit A
  extension form is absent from the downloaded eight-page file and was not located
  in this scoped historical review. Do not assert the attachment was collected.
- The General index supplies `2020-97-Gen_2d-amended.pdf`. Only its main pages1–3
  were substantively reviewed for the stated 2021 jurisdiction change and transfer
  procedure. The historical case lists and transfer form remain collected, not
  reviewed. Do not infer current appellate jurisdiction from older procedure
  boilerplate or equate these specified transfers with abolition of all writ review.
- Use readable sentences, separated names/numbers/units and explicit deadlines in
  checklist summaries. Preserve exact quotations separately; compressed notes
  are not suitable public summaries. A prose cleanup is not a change in law.

## Completed judge: N. Hunter Davis, Division 14

Profile `/2726-2/?smid=5926`; wrapper `/division-14/`; embedded document ID
`1qvFTRnIdCFk6OHLelYwZ43-gy4hqoNcBtZ7dxTLZJXo`. Full public HTML read, with stated
revision April7,2025 and appendix calendar years2026–2028. Optional PDF export
returned401 HTML. Do not treat an export extension or zero exit code as PDF proof.
An attempted diff against that failed export was invalidated before findings were
saved. **Before PDF parsing/comparison, require HTTP200, PDF signature and valid
page count.** Failed response remains evidence of acquisition failure, not rules.
Public HTML already supplied all procedure text. Weekly table inspected in a
browser using its actual table element; initial narrow screenshot clipped the time
column, so a wider view was also inspected. No authentication was attempted.

Capture4290 (`e7be2754b251abe43f3f96f0cc60b863e75c6ec00bfec1b0f4c66aa59d17f0fc`)
saves23topics/eightdiscrepancies,194nestedcitations and125verifiedartifacts.
Receipt `receipts/person-n-hunter-davis.json`; packet/acknowledgment11. Next:
Fabienne E. Fahnestock. Preserve the profile/procedure courtroom difference,
DivisionFB label within Division14 text, FridayUMC versus shared Monday–Thursday,
5:15/5:30 schedule endpoints, filing-versus-service track dates, and rehearing
order number2022-002 versus the saved2022-5 order. No authority selection implied.

## Completed judge: Fabienne E. Fahnestock, Division 18

Profile `/2726-2/?smid=2788` is linked from `/judiciary/?staff-page-no=2`.
Reuse the saved second profile page for later judges. Wrapper `/division-18/`
embeds a published Google document with ID
`2PACX-1vT1xYR9ueXpZbGBMvzCMuMueeuTgpegu54XLaXLh1yxZOmiwgtDQzb1WozsNw6gwjr63h8G2_MYpAa4`.
Use its public `/document/d/e/<id>/pub` page; this published ID is not a private
document ID from which to invent an export URL. The full 486-line document,
Exhibits A–D, calendar table and seven original images were reviewed. Images are
a seal and six hyperlinking tutorial screenshots, not additional substantive
case authorities. Save image originals with retrieval metadata; do not rely on
plain-text extraction to prove their review. Linked training videos/manuals were
not independently reviewed and are not described as such.

Capture 4292 (`f589ad0b46bc66e13f879fdaada79361193a238fb92bcba0718b8a340c78a31e`)
saves 24 topics, twelve discrepancies, 252 nested citation validations and 151
artifact read-backs. Receipt `receipts/person-fabienne-e-fahnestock.json`;
packet/acknowledgment 12. Next: Keathan Frink. The stated procedure revision is
October 14, 2026; do not turn that into an inferred effective date for every rule.

Additional shared-source reuse:

- The old judge-linked `/2017/08/2017-34-civ.pdf` returned 404. The saved civil
  administrative-order index points to `/2026/04/2017-34-civ.pdf`; its two pages
  were read. Preserve both acquisition results rather than overwriting the failure.
- Judge-linked `/2024/12/2023-9-Civ-Amendment-1-with-attachments-.pdf` contains
  sixteen pages, all reviewed. The civil index points to
  `/2026/04/2023-9-Civ-Amendment-3.pdf`, also sixteen pages, all reviewed. Its
  express supersession of Amendments 1 and 2 is recorded. Amendment 2 was not
  separately collected in this scoped review. Table images checked: Amendment 1
  pages 5–6 and Amendment 3 pages 6–7.
- Retain the property form's AI clause alongside the separately saved later
  AI order/vacatur. A vacatur naming another order does not justify silently
  removing this clause or asserting a blanket repeal.
- Preserve calendar-call 3 p.m./4 p.m., collective/single-document 50-page
  thresholds, general versus specific scheduling/cancellation instructions, UMC
  8:30/8:45 a.m., and five-day/five-business-day CMC order statements. The table
  actually prints year 1016 in its first trial row; save that value and flag it,
  rather than silently substituting 2026.
- Emergency-link label names 2021-50-CIV but its target concatenates two filenames.
  Reuse the reviewed current-index AO 2021-50; original HTML retains the broken
  target. Do not turn a malformed link into a claim that no emergency procedure exists.

## Completed judge: Keathan B. Frink, Division 12

Profile `/2726-2/?smid=2794` is in the saved second judiciary profile page. Find
the `FRINK` text node and its enclosing `abcfslItemCntrGridB` card to recover the
Biography and Division Procedures links; the name itself need not be a hyperlink.
The wrapper `/division-12/` directly embeds
`https://docs.google.com/document/d/1nieW_1I_tnZa7zHP9qnYO2SSaWAM016O/export?format=pdf`.
The browser search tool failed on its export redirect, but ordinary public curl
retrieved HTTP 200 and a valid 24-page PDF. Preserve actual per-method outcomes;
one tool failure is not proof of source unavailability.

All 24 pages were read. Many words occupy separate extraction lines; collapsing
whitespace for reading does not authorize changing saved evidence or exact quotes.
Use physical PDF page citations. Visually inspect calendars and forms for meaning
lost in extraction: page 10 strikes out August 16, 2027 and explicitly substitutes
August 23. Do not report these as two equally current dates. Pages 14–20 contain
the pretrial checklist; pages 21–22 withdrawal form; pages 23–24 discovery form.
Blank replacement-counsel time in the withdrawal form is not a fixed deadline.

Capture 4294 (`b6dccd5fea7d6e1a2eb5cb07aa58f30d85b116fb6f6d0f028eeb2490722b981f`)
saves 24 topics, nine discrepancies, 271 nested citation validations and 162
artifact read-backs. Receipt `receipts/person-keathan-b-frink.json`;
packet/acknowledgment 13. Next: Marina Garcia-Wood. The procedure revision is
October 8, 2026; shared sources retain their own dates.

Reuse previously reviewed Local Rule 10A, emergency, rehearing, case-plan and AI
order sequence. New shared source AOSC20-16 is the historical March 18, 2020
remote-oath order, three pages, expressly limited by the stated AOSC20-13 duration
condition. Original judge-linked URL redirects to official
`https://flcourts-media.flcourts.gov/content/download/632105/7182680/AOSC20-16.pdf`.
Both URLs and retrieval time are recorded. The reference is not evidence that the
emergency suspension remains operative. Do not recursively resolve the entire
emergency-order chain to complete this baseline source review.

The judge's circuit-civil clerk email is saved as a published contact statement;
the county clerk's full review is still pending. CMS help and technology videos
are linked aids, not asserted reviewed. The sample withdrawal form's printed
`myfloridaaccess.com` target is retained as text, not promoted as a verified filing
portal or followed for credentials. Record instructions separately when general
and specific passages differ, including Thursday appearances, courtesy-copy time
units, proposed-order routing, AI references, MSJ timing and withdrawal stay versus
unchanged trial/hearing settings.

## Completed judge: Marina Garcia-Wood, Division 11

Profile `/2726-2/?smid=2841` and saved second judiciary page link directly to
Google document `1gPKaUMlD5v9xbpGZnhCbYiOXcAqNOKGmD9uBW-P3XfQ`. Its edit-page
extraction contains only the application shell; the public `/export?format=pdf`
response is HTTP 200 with eleven pages. All pages and the linked two-page
`/wp-content/uploads/2017/08/help_desk_flyer.pdf` were read. The profile image alt
text identifies Carlos Rodriguez; requested contact/assignment fields are
corroborated by the roster and procedure. Do not import the unrelated biography.

Capture 4296 (`953d5882ba328d2dd579aac49f808fa48558151265a03616934eb21b5e29eba7`)
saves 24 topics, fifteen discrepancies, 331 nested citation validations and 195
artifact read-backs. Receipt `receipts/person-marina-garcia-wood.json`;
packet/acknowledgment 14. Next: David A. Haimes. Assignment starts August 17, 2026
as stated; no overall procedure revision date was located.

- Extract PDF `/Annots` URI actions with physical page and rectangle as well as
  visible text. Displayed Zoom meeting 852787101 has some links to 402065339 and
  one-tap strings containing 763453911. The self-represented email label differs
  from its `mailto:11@17th.flcourts.org` target. Preserve both, without substituting
  a preferred URL into the source record. The annotation extraction reuses the
  original PDF hash, URL and retrieval time; it is not a new acquisition.
- Christopher Pole is separately identified as the assigned senior trial judge,
  with room and Zoom information. Reuse this source for his eventual review; do
  not count him complete merely because another judge's document mentions him.
- Current civil index supplies AO 2014-17 (five pages, including affidavit),
  2009-12 (two pages, including worksheet), 2013-54 amended (three pages, status
  forms), 2018-100 (two pages, distribution) and 2020-68 (one-page vacatur). All
  were read. The internal-host worksheet link need not be followed: the public
  2009-12 PDF already includes the complete worksheet.
- Judge-linked 2015-26 and old emergency Form A were also read. A targeted official
  search for `"2020-40" "Second"` located the historical five-page order with
  attachment; its express 2020-68 vacatur is retained. Do not infer current
  pandemic restrictions from a judge's still-present reference.
- AO 2014-17 text extraction duplicates layers and misreads some characters.
  Visual review of all five pages confirms April 15, 2014 and Form 1.996(b).
  Preserve the raw extraction; never count repeated text as multiple requirements.
- Record ordinary versus emergency sale-cancellation timing, hearing locations,
  paperless versus delivery instructions, old emergency/evidence references,
  clerk-assisted flyer details and case-distribution replacement separately.
  These discrepancies do not prevent completing this source review.

## Completed judge: David A. Haimes, Division 07

Profile `/2726-2/?smid=399` leads to Google document
`1qbJymeFPPTKsvd_kIPD9gYCmHi5ViuMkBC-mo6jHXGc`. Public PDF export has ten pages;
the edit-page extraction is only a shell. Reviewed all pages, forms, calendar
and contact details for Christine Kortabani, named work email and shared div07.
Receipt `receipts/person-david-a-haimes.json`; packet/acknowledgment 15.
Capture 4300 (`e01cefbe896df9a1de9ae215db6ac09f43c187914aec27350809180eee1a1255`)
saves 24 topics, ten discrepancies, 363 citation validations and 214 artifact
read-backs. Earlier capture 4298 preserves the initial summary spacing. Next:
Jeffrey Levenson; eleven distinct judges complete, county incomplete.

- Inspect every PDF link rectangle, including wrapped headings. Page 9's CMO
  title links document `1bUpadNGQTKR1C8mmhsyaCRhstwYwVA5v` (16 pages), while the
  subtitle below the discovery heading links
  `17lkWeCzo53mc-Y5CXX6F03s3VgdjWz_wEAifrwjcy6o` (15-page CMO). The discovery
  title itself links `1mIhlcHtEsozzWHT3fr19LeBpIszMpkTHekdeb6ZaJ8A` (two pages).
  All three were read, not deduplicated by visible title. The UTO is document
  `1YCiXUxRMdwzA57otvPnU6-EyJ85sjgNa` (three pages).
- Both CMO texts were compared with only whitespace and page labels removed.
  Four differences were inspected: five-day post-CMC draft sentence, rule-based
  exception to early discovery, duplicated wording, and continuance-conferral
  sanctions. Preserve their distinct original URLs and bytes.
- Main instructions use 20 days before hearing for MSJ responses; both CMOs
  use 40 days after motion service. Main exhibit threshold is 100 pages; CMOs
  use 100 exhibits. Appearance thresholds differ between pages 2 and 3. CMO
  trial timing differs from shared AO 2025-24. Record, do not resolve.
- For the referenced service notice, follow `/courtforms/` →
  `/circuit-civil-miscellaneous-forms/` →
  `/wp-content/uploads/2025/01/notice-of-service-of-complaint-Fillable-1.pdf`.
  The one-page form was saved, read and visually checked; it retains older
  2024-26 references. Do not infer a revision date from its URL. Both exhibit
  forms linked on page 8 were also read and visually checked.
- Eight substantive documents total 49 reviewed pages. Tutorials and training
  presentation/video remain links only. No training-content review is asserted.

## Completed judge: Jeffrey R. Levenson, Division 09

Use the third judiciary page (`/judiciary/?staff-page-no=3`), profile
`/2726-2/?smid=2816` and `/division-09/`. The wrapper embeds published Google HTML
document `2PACX-1vTRH1IQKG5K0sqbCZyD7DZ0EyztNC9QU967C-IJeOi0zKoQE5wf7GqAiKQc4WFuWdQ9wIbf49GI2xsB`.
All 262 extracted lines were read, including the eight calendar-call/trial rows
and order categories. No embedded images. Calendar was inspected in the browser.
The stated revision date remains December 29, 2025; later calendar dates do not
prove a later revision date. Older probate pages found in search were not used
as current Division 09 evidence.

Capture 4302 (`d87c43dab50ed93b830a19a83d5605fad349aa2ebfaf4ef229ce8a848013ebff`)
contains 24 topics, nine discrepancies, 274 citation validations and 215 verified
artifact read-backs. Receipt `receipts/person-jeffrey-r-levenson.json`;
packet/acknowledgment 16. Twelve distinct judges completed. Next: Carol-Lisa Phillips.

- Dalia Dooley, shared Div09 email and published phone; no named assistant email
  was located in the full current profile/procedures. Do not adopt an assistant
  from older probate PDFs surfaced by broad search.
- Preserve Thursday in-person versus withdrawal Zoom directions, general
  special-set versus minor-settlement Zoom wording, 20/15-page limits, 10 business
  days versus 10 days for materials, CMS versus internal calendar setting, three
  motions versus Local Rule 10A's two, and differing MSJ response deadlines.
- Judge expressly excepts limine hearing scheduling from the UTO while requiring
  other UTO deadlines. Do not generalize that exception to unrelated deadlines.
- The linked `/court-schedule/` was acquired/read: 2026 and 2027 holidays and
  Monday–Friday 8:30–5 hours. Training and courtroom AV tutorials remain links
  only. No separate judge-specific UTO attachment link is present.
- Reuse `ao-2017-34-index`, the already reviewed current-index PDF. The manifest
  entry `ao-2017-34` is the old 404 response and has no supporting text. A wrong
  key was caught before this checkpoint was written; no failed response was
  promoted into a citation.

Phillips completed October 15: official profile `2726-2/?smid=2831` →
`/division-26/` → published Google document (manifest `phillips-document`).
All 460 extracted lines reviewed; browser calendar screenshots for 2026/2027
retained. Contacts appear at the top; scheduling, proposed orders and motion
requirements follow; quarterly calendars close the document. Reuse Haimes exhibit
list/worksheet originals rather than download duplicates. Historical AO2017-33,
SC20-1490 (April 29, 2021) and AOSC21-17 have separate scoped shared reviews.
For amendment PDFs, inspect visual strikeout/underline before summarizing text.

Confidentiality form: procedure instructs Attorney Portal → Forms but provides
no attachment. Public clerk eFiling → Form Downloads lists paid bundles;
Attorney of Record Access describes verified registration. Those pages and the
2021 redaction notice are preserved. The exact public form was not located;
do not claim its contents reviewed or treat a third-party form as the official
Broward form. County packet must retain this unavailable-copy limitation.

Receipt `receipts/person-carol-lisa-phillips.json`, final packet
`draft/checkpoint-18.json`, acknowledgment `review/history-capture-18.json`:
capture 4306, 28 topics, ten discrepancies, 345 nested citation validations,
243 artifacts read back; replay, facts and unchanged finalized reports checked.
Capture 4304 remains historical; 4306 corrects the pandemic supersession pinpoint
to physical pages 3–4. Next judge: Michael A. Robinson. Thirteen complete.

Acquisition lesson: normalize derived HTML text to LF before calculating its
text checksum. Some clerk HTML contains CRLF inside text nodes; Python text-mode
reads normalize these, so hashing unnormalized extraction can fail validation.
Keep original response bytes untouched and retain prior derived files. Citation
containment validates quoting but does not prove substantive support: review
page pinpoints against the actual statement before accepting a checkpoint.

Robinson completed October 15: official judiciary page3 profile
`/2726-2/?smid=2840` → `/division-13/` → published Google document. All391
extracted lines reviewed, including fee scheduling form and seven trial-calendar
rows. Calendar screenshot verified. Profile gives Angela Stitt/954-831-7258,
WW14131/WW14150, Division13. Shared division email is in procedure header.
West Building address was separately verified on clerk Hours and Locations;
no clerk office room was substituted for the judge's chambers.

Robinson's text/links disagree: rehearing label2017-33 points to2010-47;
emergency label2021-50 points to2014-32-amended. Derived anchor metadata retains
visible label, href and decoded Google target under `robinson-link-targets`.
Old2010-47/2008-41 PDF paths404; official `/wp-content/uploads/2017/08/` copies
were retrieved and reviewed. The shared2017/2022 replacement texts are retained
without deciding controlling authority. Public CMS registration form was located
through `/knowledge-base/workbench-menu/` → Pro Se Registration Form →
`/wp-content/uploads/2018/04/pro_se_on_line_user_agreement.pdf`; one page read and
visually checked. Original fees form is embedded at the end of the judge's HTML.

Receipt `person-michael-a-robinson.json`, packet19, acknowledgment19: capture4308
(`25bec0467e0b2d5508070512a6f3e6000da84f99699907b8ac511de581cf4a0e`),
26 topics, eight discrepancies,338 nested citations,259 artifacts. First live
save through `flwu.baseline_capture.save_checkpoint`; artifacts/facts read back,
identical replay checked, finalized reports unchanged. Next Carlos Rodriguez.

Acquisition manifests must have a single writer. Parallel network fetches may
return independent results, but merge/write them serially against the latest
manifest. Do not append a derived extraction while another process holds an old
manifest snapshot. During this review a concurrent write dropped a derived link
entry; it was regenerated from the unchanged original and its presence verified
before saving. No original file or prior database capture was lost.

Rodriguez completed October 15: official profile `/2726-2/?smid=22402` and
roster-linked Google document `1SvefBmEbFKnPI6YlEO5sJAg6oJUndfHEE2ddOelt1-Y`.
The public PDF export succeeded when the editor view failed. All 15 physical
pages were reviewed, including calendars, embedded discovery/withdrawal/fees
forms, published court-conflict disclosures and the blank final page. Retain
the July 8, 2025 effective date separately from the 2026–2028 calendar entries.
Header room 16125 conflicts with body 15127/profile WW15127; preserve both.
The last calendar entry specifies January 2028 only: do not invent trial dates.

The historical trial-order chain was found on the official uploads path:
2014-2 (all five pages reviewed), 2016-28 (main pages 1–2 reviewed; attachment
pages 3–7 collected), and 2018-62 (all seven pages reviewed). Record express
supersession statements without deciding present controlling authority. Reuse
the saved 2025 case-management compilation with its existing review scope.

Receipt `person-carlos-augusto-rodriguez.json`, packet20, acknowledgment20:
capture4310 (`6e3c6099c24f011f88e242485786d5d90e8a01358910735b58475f64348f03dd`),
16 topics, six discrepancies, 24 calendar rows,336 nested citations,273 artifacts.
The save helper's exact replay, artifact/fact read-back and unchanged finalized
reports were verified. Fifteen judges saved; next Michele Towbin Singer.
Cloud research and workflow development continue directly under the user's
October 15 override; local retrieval/analysis begins only after workflows are built
and validated. No other county has been started.

Singer completed October 15: official profile `/2726-2/?smid=416` →
`/division-21/` → published Google document, manifest `singer-document`.
All 745 extracted lines reviewed, including the embedded fee scheduling order
and 2026/2027 calendars. Amanda Abrams' named email is in the procedure header;
the shared division email appears in both profile and procedure. Preserve the
letterhead address suffix `#214` separately from chambers `WW15125`.
Two anchors visibly labeled `div21@17th.flcourts.org` target
`mailto:div25@17th.flcourts.org`; actual anchors are saved in
`singer-link-targets`. Do not let an extraction silently substitute one for the
other. The December 2025 revision label remains distinct from later calendar
dates and scheduling-availability statements.

The linked AOSC20-23 Amendment 10 Google Drive download returns HTTP200 with
a sign-in page. It is preserved as an unavailable document response, not a
supporting legal citation. The official workgroup report's footnote supplied
the Supreme Court original at `/content/download/724015/file/`.
All 31 pages collected; civil/shared pages 1–3,13–21,31 reviewed. Other pages
are not asserted substantively reviewed. Existing historical AOSC21-17 and
local/shared sources were reused with their original review scopes.

Calendar tables were visually checked. September–December 2027 supply month
labels only in both columns: keep exact dates null, retain the month, and do
not extrapolate a recurring weekday. Four highlighted extra-week annotations
are stored separately. A screenshot initially clipped text because the browser
retained horizontal scroll; resetting horizontal scroll produced the complete
2027 table. The one embedded image is a seal, not procedural text.

Optional calendar-call form: procedure says the court emails it to parties;
no public attachment was found in the complete profile/procedure. Its unseen
contents are not inferred. The exact confidentiality notice repeats Phillips'
public-copy limitation; reuse that recorded investigation instead of repeating
identical searches. These limitations remain in the county review packet.

Receipt `person-michele-towbin-singer.json`, packet21, acknowledgment21:
capture4312 (`6b4b3b42cff51e8003c4b2056aface389a290060f98690ec3ed5262cf251eb4d`),
32 topics, ten discrepancies,24 calendar rows,389 nested citations,280 artifacts.
Person validation, artifact/fact read-back, exact replay and unchanged finalized
reports verified. Before persistence, manual pinpoint review corrected several
draft line ranges; quote containment alone does not prove that a quoted passage
supports the associated summary. A draft call using an unsupported `_citation`
keyword failed before any database write; the existing API is `_citation(root,
citation)` for manual research, not `_citation(..., trial=True)`.

Next: County Civil chair Daniel J. Kanner. Sixteen judges have reviewed records;
full county roster reconciliation, remaining people, clerk and material shared
procedure checks remain pending. No other county has begun.

Kanner completed October 15 (save timestamp October16 UTC): official profile
`/2726-2/?smid=2811` → `/division-55/` → published Google document, manifest
`kanner-document`. The full 91-line document is amended October14,2026. Header
supplies Jody Kling, shared div55 email, telephone and address; profile supplies
WW chambers/courtroom codes and County Civil Chairperson role. The sole image
was acquired and visually checked: it is the state seal, not a missing form.

The current document says the small-claims invocation/appearance-waiver form is
attached, but only a discovery form follows. Official Forms → County Court
Miscellaneous Forms contains no invocation form. Targeted official-site searches
(`Kanner invoke order`; `order waiving pretrial 55`) located the historical PDF
`/wp-content/uploads/2017/08/div55procedures.pdf`. Its cover dates the document
October2014; page15 contains the requested type of form. Pages1 and15 reviewed,
page15 rendered; pages2–14 collected only. Do not present this older form as
currently approved, or its older assistant/room as current contacts. The missing
current-version confirmation remains an evidence limitation.

The County Court Miscellaneous Forms page separately links
`/wp-content/uploads/2017/10/Compel-Order.pdf`. Its one page was read and rendered;
the operative ten-day discovery-compliance terms match the current embedded
form, but signature-year placeholders are2012 and2019 respectively. Blank form
signature years are not issuance/effective dates. General eviction/lease links
on the index remain navigation leads, not individually reviewed local procedures.

Shared AO2025-24: county Exhibits J/K (physical pages64–71) and pathway table M
(page73) were fully read; numeric deadlines and table checked visually. The
earlier recorded reviews plus this review cover all73 physical pages. The
structured `county_case_management_baseline` in Kanner's receipt/facts retains
separate streamlined/general offsets, their case-order anchor, mediation's
conditional application, service/trial-date anchors, and case-type exclusions.
Do not compute actual case deadlines from an unissued template. Reuse this shared
review for subsequent county judges while checking their own instructions.

Receipt `person-daniel-j-kanner.json`, packet22, acknowledgment22: capture4314
(`374a0b63616a1933a578315d64f0713977a72c45c32ee85abf16b2b0e60a1dec`),16 topics,
four discrepancies,353 nested citations and297 artifacts. Person/citation
validation, artifacts/facts read back, identical replay and unchanged finalized
reports verified. Seventeen judges saved. Next Florence Taylor Barner; complete
her civil review and record both civil/criminal contacts, assignments and official
links together before another judge. Substantive criminal-only review remains
deprioritized. County roster reconciliation and clerk/material-order work remain.

Barner completed October 15 (save timestamp October 16 UTC): official profile
`/2726-2/?smid=2745` → `/division-54/` → published Google document, manifest
`barner-document`. All 193 extracted lines reviewed, including discovery form,
AI clause and dated 2025 holiday list; header/seal visually checked. Yvette Tomkins,
shared division email, phone and address are preserved. Profile courtroom WW13156
and mandatory small-claims pretrial room 10165 remain separate purpose-specific
statements. The procedure has no stated revision date.

The March 2026 assignment order labels CMF Community Court. Its pages 1,4,5,6
were reviewed (county tables visually checked); pages 2–3 remain collected only.
Retain the October roster and this earlier order independently. The official
profile links the civil Division 54 page for the combined 54/CMF listing; targeted
official searches found no distinct Barner CMF procedure. Record that search
result and do not infer that civil directions govern Community Court. Criminal
contacts, assignments and official links are covered; exhaustive criminal-only
procedure review is outside the current priority.

New shared sources: AO 2023-8, all 29 pages collected, main pages 1–6 and county
forms/pathway pages 17–29 reviewed; circuit appendices 7–16 not claimed reviewed.
The Florida Bar's official rules index supplied the October 1, 2026 civil-rules
compilation. All 340 pages collected; only Rule 1.530 and notes, physical pages
174–176, reviewed, with page 174 visually checked. Preserve the judge's ten-day
new-trial statement alongside the rule's fifteen-day statement and amendment
note without selecting controlling authority. An updated compilation date does
not establish every rule's effective date.

The emergency order cited as 2021-51-CO is the same four-page original already
saved as 2021-50-Civ/2021-52-PRC. Reuse it, including Exhibit A; number aliases
are not separate evidence acquisitions. Older case-plan/rehearing references,
continuance language and AI directions remain documented source discrepancies.
The commercial nonmilitary-affidavit service is preserved as a link only; no
private-party search or transaction is needed for this baseline.

Receipt `person-florence-taylor-barner.json`, packet23, acknowledgment23:
capture4316 (`5d12a550dcfa8d600f07f8019db52fd067f2c974504f6a4070c68e2daf783606`),
22 topics, six discrepancies,385 nested citations and308 artifact read-backs.
Person/citation validation, semantic facts, exact replay and unchanged finalized
reports verified. Eighteen judges saved. Next Betsy Benson, County Civil 56.
Broward remains incomplete; no other county has begun.

Benson completed October 15 (save timestamp October 16 UTC): official profile
`/2726-2/?smid=2748` → `/division-56/` → published Google document,
manifest `benson-document`. All 206 extracted lines, including discovery form,
reviewed; header/seal visually checked. Carol Mosley, shared div56 email,
telephone, WW13131 chambers, WW13154 courtroom and Zoom ID saved. Header says
revised April 2023, while the body references a 2026 AI order; retain month-only
revision precision and the source discrepancy without backdating the body.

One HTML anchor displays the domain portion of the div56 address but targets
`mailto:cmosley@17th.flcourts.org`. Original HTML and `benson-link-targets`
derived extraction preserve the containing paragraph, visible label and actual
target. The target is a public address, but the source does not explicitly label
it as Mosley's individual email; the verified assistant contact uses the shared
division address. Do not silently substitute the anchor destination for its label.

New shared sources: AO 2020-85-CO Amendment 1, both pages reviewed, reached through
`/county-administrative-orders/`. Preserve sole-insurer-defendant scope, waived
pretrial, Form 1.902 summons, Rule 1.440 exception and Small Claims Rules 7.135/
7.150 priority over Rule 1.430. AO 2016-8-Gen and express replacement 2020-61-Gen
were reviewed with their Version 1.4 professional-standards attachments (nine and
ten physical pages). The exact 2021-66-Temp original has three pages about
January 2022 election canvassing; it does not support Benson's mask citation.
This mismatch is recorded without guessing the intended order.

The April 13, 2022 Canady virtual-hearing resources memorandum referenced without
a link was not located after title/date/official-site searches. A Tenth Circuit
announcement points to statewide self-help resources but is not that memorandum;
retain it as a discovery lead, not a substitute original or a new county review.
This supporting-source gap remains in the receipt. Case-specific fee/pretrial
orders are described, not public attachments whose unseen terms can be inferred.

Receipt `person-betsy-benson.json`, packet24, acknowledgment24: capture4318
(`e73d2cc4ebfe49fbb5ad483079a2aa056fbbf8594d8f700ad49b824560d1ddf7`),26 topics,
11 discrepancies,439 nested citations and324 artifact read-backs. Person/citation
validation, semantic facts, exact replay and unchanged finalized reports verified.
Nineteen judges saved. Next Woody R. Clermont in the County Civil chart sequence.
County reconciliation, remaining personnel, clerk and material shared orders
remain incomplete, including the county filing-location review. The index links
AO 2025-40-CO (filing locations) and 2026-25-CO (specified credit-card divisions);
these remain substantive-review leads, not reviewed orders in this checkpoint.

Clermont completed October 15 (save timestamp October 16 UTC): official profile
`/2726-2/?smid=23665` links directly to Google document
`1XJNSrxiOpwmdO4P0nRpKGtyM7-ELINVrNdNPNpxrHvc`. Public PDF export succeeded;
all 19 pages and three linked one-page forms were reviewed. Original editing
response, PDF, derived text and PDF URI annotations are retained. Header and
standing orders were visually checked. The header's March 23, 2026 dates apply
to judge/assistant assignments, not the whole procedure's revision. Embedded
standing orders are signed April 9 and May 15, 2026.

PDF annotations matter: page 4 prints a 2020-82 Amendment 1 URL but targets
2025-41; page 13 displays div102 email but targets div47. All three credit-card
orders (2020-82 Amendment 1, 2025-41, 2026-25) were collected and fully reviewed.
Keep their distinct scope, stated dates, replacement clauses and deadlines.
The 2026 order says noon three business days before pretrial for waiver/transfer;
the judge says preceding business day for waiver and two business days for
transfer, with different entered-order language. The original pretrial-window
sentence literally says days "before" filing; visual review confirmed it.
Do not silently correct that word or derive calendar dates from it.

The transfer template names Division 10, although the judge is Division 102.
Its unrelated email string is retained in the original but not imported into
court contacts. Judgment forms are blank templates; their optional fact-information
sheet provisions and no-filing instruction were captured without collecting any
private litigant information.

County filing-location order AO 2025-40 was fully reviewed (six pages), including
visual ZIP-table review and an assertion comparing all four structured ZIP lists
against the extracted original. The separate finding key is
`broward-county-filing-locations-2025-40` in the same Broward stream. Although the
key includes the initially reviewed order number, keep this entity key stable
when a later source updates the same county filing-location topic; store a new
order number in its facts rather than creating a disconnected topic. The receipt
is `receipts/county-filing-locations-2025-40.json`. It preserves plaintiff versus
primary attorney-office ZIP, regional/prefix rules, co-counsel priority, missing-ZIP
handling, anti-circumvention provisions, credit-card filing codes and sole-insurer
exceptions. This is an evidence finding, not a case-specific venue calculator or
an exhaustive audit of separate-order exceptions.

New shared reviews also cover general device, media and judicial-branch-record
orders, the ADA request information/form, and replacement ADA order 2026-20.
The older 2018-10 Amendment 1 link on the ADA page returned 404 twice; failed
responses remain. The replacement preserves earlier notices and requires bold
14-point Bookman Old Style or Arial notice text effective July 1, 2026, 12:01 a.m.
The old order original is not claimed reviewed. The official Local Rules table
and targeted searches did not locate a separate "Local Rule 11A" original;
retain Clermont's joint discovery pre-motion statement requirement as his own
published instruction, with that supporting-source gap. Criminal-case-specific
media orders remain links only. News links are roster leads, not verified changes.

October 2026 civil-rules compilation: Rule 1.202, physical pages 64–66, now has a
scoped review in addition to the prior Rule 1.530 pages 174–176. The compilation's
other contents remain collected, not newly substantively reviewed. The initial-
service-extension exemption missing from the judge's list is preserved as a
source discrepancy; no controlling-authority determination was made.

Receipt `person-woody-r-clermont.json`, packet25, acknowledgment25: capture4320
(`124fdcb1443d20db29b6f0a813e0e6e66222b8632c5c9b66fab407736b34f337`),28 topics,
12 discrepancies,511 nested citations and376 artifacts. Person/citation
validation, both judge and county facts read back, ZIP-list assertions, identical
replay and unchanged finalized reports verified. Twenty judges saved. Next Nina
W. Di Pietro; remaining roster, personnel, clerk and material-source checks remain
incomplete. No other county has begun.

The existing history CLI was exercised against the new county finding:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/flwu history changes \
  --stream manual_research:county-baseline-v1:6bf5ac02ab39 \
  --entity broward-county-filing-locations-2025-40 \
  --output runs/county-broward/2026-10-15/review/filing-location-context.json
```

It returned that entity, one `first_observed` event, `baseline_known=false`,
`latest_research_status=incomplete` and `assessment=review_required`. This proves
retrievable comparison context, not a finalized county baseline or a newly enacted
rule. Its `unvalidated_receipts=2` counts the two payload draft containers; the
current implementation does not independently classify the manual review receipt.
Its filtered `source_checks` is empty because existing manual check IDs do not map
to this county entity. Before county publication, integration must explicitly link
entity checks and manual review evidence, close completed historical draft checks
through new observations, and validate finalized-baseline comparison. Do not mark
the county ready merely to suppress these conservative incomplete-state signals.

### Nina W. Di Pietro — verified checkpoint 4322

Twenty-first judge, County Civil Division 49. Official discovery path:
`/10-county-court-civil-and-criminal/` → biography
`https://www.17th.flcourts.org/2726-2/?smid=2784` →
`https://www.17th.flcourts.org/division-49/` → iframe
`https://docs.google.com/document/d/e/2PACX-1vRWnmUdgibMLtGolpw0VeE2oxbNBVAuIMAVhn7wRRejJgzlWIeiUT_1RsTJ0psZld2zuXA6ctTy1rKU/pub?embedded=true`.
Manifest keys `dipietro-county-index`, `dipietro-bio`, `dipietro-division49`,
`dipietro-document`; original HTML and extracted text saved. Profile lines locate
Tamar Hemmings, 954-831-5708, WW13135, WW13158, Division49 and Zoom906144255.
Procedure header and communications paragraph supply shared
`div49@17th.flcourts.org` and three-line mailing address. No individually named
assistant email, judge direct email or fax located in checked sources.

All 163 extracted procedure lines and embedded discovery order reviewed. One
header table, no images, mailto destinations match visible address. No separately
linked substantive attachment. UMC general paragraph says 9:15 a.m.; dedicated
section says 9 a.m.; both Tuesday–Thursday to10 a.m. Store both. Courtroom10165
is specifically small-claims pretrial; ordinary courtroom13158 is not an error.
Online scheduling covers UMC/15/30-minute represented-party settings; longer by
copied email. Unilateral scheduling requires two documented attempts24hours apart
and24hours to respond after second. Remote evidence filed/served five days before;
shared2022-37 CMS/log requirements retained separately. Orders may be electronic
or paper with stamped envelopes. Discovery form must not gain extra privilege
language. Fee hearing follows entitlement and compliance with a case-specific
preliminary order whose unprovided terms are not inferred. Withdrawal consent
permits no hearing; corporate warning specifies20days for new counsel.

Judge's Rule1.440(b) “Notice for Trial” differs from the retained October2026
compilation's “Motion for Trial.” Added scoped Rule1.440 review on physical
pages147–149; neighboring rules not marked reviewed. Shared compilation review
now covers1.202,1.440,1.530 only. Reused relevant Local11, emergency2021-51-CO
(alias of2021-50-Civ/2021-52-PRC), rehearing2022-5, remote evidence2022-37 and
county case-management2025-24. Four differences saved without deciding control.
No publication/revision/effective date stated in the judge procedure.

Receipt `receipts/person-nina-w-di-pietro.json`, save script
`review/save-dipietro.py`, packet`draft/checkpoint-26.json`, acknowledgment
`review/history-capture-26.json`, all relative to the pinned workspace.
Capture4322 `c2d8645bbd92fb8b2738a59a54310828852a3bc6dc26646066339eff58ef7677`:
21topics, four differences, six applicable shared sources,156nested citations,
371artifact byte read-backs, semantic fact read-back, exact replay and unchanged
finalized reports verified. Source inventory199 entries. Smaller citation count
reflects bounded applicable-source links, not lost shared originals.

`history changes --stream manual_research:county-baseline-v1:6bf5ac02ab39
--entity broward-county-nina-w-di-pietro --output
runs/county-broward/2026-10-15/review/dipietro-context.json` verified that exact
entity-keyed check is returned as verified. Assessment remains `review_required`,
baseline is last finalized report and unknown for this county stream. Generic
`unvalidated_receipts=2` remains the draft-container count. This bounded fix does
not reconcile earlier broad rule associations/check IDs or make the county ready.
Next judge **John D. Fry**; do not start another county.

### John D. Fry — verified checkpoint 4324

Twenty-second judge. Official profile
`https://www.17th.flcourts.org/2726-2/?smid=2795` lists74/MW/MI and links
`https://www.17th.flcourts.org/division-mt-mw-74/`, whose iframe is
`https://docs.google.com/document/d/e/2PACX-1vSjq_ADtIIbGaJ_8idGI8u9HLbjpLILRpIpGZJw_V3deGb3U0BbNCvr2K3Xpk18iSI14uVphG9-7h2A/pub?embedded=true`.
Manifest`fry-bio`, `fry-divisions`, `fry-document`; header gives revision
August27,2026, Stephanie Nesbitt,954-831-1673,divmw@17th.flcourts.org for all
divisions, chambers6135/courtroom6165 at201SE6thStreet,FortLauderdale33301,
Zoom272833508. Profile uses WW prefixes. MT appears in procedure heading but is
not confirmed by checked profile/March assignment list; preserve discrepancy.

Combined document134textlines: shared/civil directions reviewed, criminal-only
parts screened for scope. Default in person unless court permits Zoom; email
scheduling with opponent copied; notice within24hours of confirmation; motions
must be visible on clerk docket before sending materials; evidentiary courtesy
hardcopies two business days before; exhibits filed with notice five days before.
Mixed pretrial/calendar/continuance/withdrawal paragraphs retain their
State/plea/speedy-trial/defendant context and unconfirmed civil applicability.
Six criminal form links retained with labels and destinations, not downloaded or
substantively reviewed. Header image downloaded and visually verified as seal;
no image-only procedural content. No separately stated current named-assistant
email, judge email or fax located.

Shared ADA paragraph labels2018-10 Amendment1 but targets
`https://www.17th.flcourts.org/wp-content/uploads/2018/02/2018-10-Gen.pdf`.
That original was collected and both pages reviewed (`fry-linked-ada-2018`);
February12,2018 issuance, historical Diana Sobel contact, TimesNewRoman/Courier
notice. Preserve alongside2026-20's BookmanOldStyle/Arial requirement and express
vacatur of Amendment1, effectiveJuly1 with prior-notice savings. Obtaining the
original does not fill the earlier missing Amendment1 original. Reuse shared
Local11, emergency2021-50/51/52, remote-evidence2022-37 and countyCMO2025-24 with
civil applicability limits.

Targeted official searches for Fry/civil/procedures and Fry/74/2026 also located
`https://www.17th.flcourts.org/wp-content/uploads/2017/08/div70procedures.pdf`.
Nine pages collected, first page reviewed only: explicitly September20,2015,
Division70, North Regional address and old phone/fax. Do not use those as current
Division74 contacts or treat old forms as current procedure. No distinct current
civil-only procedure found in checked sources; shared portions of combined source
remain the reviewed evidence. No exhaustive criminal review undertaken.

Receipt`receipts/person-john-d-fry.json`; script`review/save-fry.py`;
packet`draft/checkpoint-27.json`; acknowledgment`review/history-capture-27.json`.
Capture4324 `65da8fc2f814d0e3452061802fd77795a2c665f166025e384286438b5fe105d5`:
14topics, six differences/ambiguities,148nested citations,381artifact byte
read-backs, semantic read-back, identical replay and preserved finalized reports.
205source inventory entries. `review/fry-context.json` verifies entity-filtered
finding/check retrieval; county remains incomplete with unknown finalized baseline.
Next **Jennifer Wigand Hilal**. Cloud performs research and workflow development.

### Jennifer Wigand Hilal — checkpoint 4326

Twenty-third judge, CountyCivil48. Profile
`https://www.17th.flcourts.org/2726-2/?smid=2806` →
`https://www.17th.flcourts.org/division-48/` → published iframe
`https://docs.google.com/document/d/e/2PACX-1vQVoGh93jA6Bleo5sMsosk9FFkV_YH9F5IN7FSK243vPJYgukKQL-Xvt32-1TpbgILP9bxhLitvjzaQ/pub?embedded=true`.
Separate print link uses document`1ZtBMnDsM6OK7Y8Jzo-fdfc5iKiM3xyMCZtERps5J0oc`;
PDF export succeeded. Manifest keys`hilal-bio`,`hilal-division48`,
`hilal-document`,`hilal-print-document`. Full150-line HTML and9PDFpages reviewed;
PDFpages1,2,8,9 rendered/inspected, including seal/ZoomQR and form columns.

Header supplies Bibi Khan,954-831-7898,div48@17th.flcourts.org,physicalWW6129
and distinct mailing#174/Box174,201SE6thStreet,FortLauderdale33301. Ordinary
approved in-person special sets12178; small-claims pretrial10165; Zoom292953734.
No extra named assistant email/judge email/fax located. No revision date stated.

Key distinctions: Zoom default except jury/pretrial; in-person motion approval;
hardcopies of all hearing material five business days before, separately closing
paragraph requires motions over10pages mailed toBox174. JA-only eviction,
unlawful detainer,fees,over30minutes,nonjury,rehearing settings. Unilateral
coordination says several phone/email attempts, no invented number/wait.
Both online cancellation andJA notification required; signed agreed order needed
to excuse attendance. Paper exhibits overfourpages consecutively paginated with
copies. Electronic orders limited to named categories. Waiver form reviewed:
entered order needed before pretrial;20dayresponse; conditionalDivision53 clause
retained literally without applying it universally to48. Missing discovery form:
neither HTML nor print contains claimed attachment; targeted Hilal/compel and
Division48/discovery searches plus official generic county forms checked.
Generic county Compel-Order is not represented as Hilal's attachment. Retain gap.

Reused Local11,2014/2021emergency originals,2022-5rehearing,2022-37remote,
2025-24countyCMO, scoped1.440/1.530 and generic county form. Historical emergency
reference and other paper/electronic differences retained, no control decision.
Receipt`receipts/person-jennifer-wigand-hilal.json`; script`review/save-hilal.py`;
packet28; ack`review/history-capture-28.json`; comparison`review/hilal-context.json`.
Capture4326 `1ed69576730ba47faeb406e7f31021fcd8293656f975da709214e44492cdff61`:
23topics,5differences,177nested citations,393artifactreadbacks,exact replay/facts
and finalized preservation verified. Entity-filtered check verified; county
remains incomplete.209inventory entries. Next **Kathleen McCarthy**.

### Kathleen McCarthy — verified checkpoint 4330

Twenty-fourth judge, County Civil Division 101 (credit-card small claims).
Official profile `https://www.17th.flcourts.org/2726-2/?smid=2823` links
`https://www.17th.flcourts.org/division-101/`. Published iframe:
`https://docs.google.com/document/d/e/2PACX-1vStEOqxuafmthf5H4El9UPG9h3fO_TppchplLGGQ2p5QdFoasuTOW8DNUVv3D-j1CI5hr3r3JtjyGQd/pub?embedded=true`.
Print document ID `1YvMV1wmDtufI4mWdF2fq7OeUnRfM6Tr7zBkP46i4rcA` exported
successfully to PDF. Manifest `mccarthy-bio`, `mccarthy-division101`,
`mccarthy-document`, `mccarthy-print-document`. All 470 extracted HTML lines and
12 PDF pages read; first/last pages visually checked. One state-seal image, no
tables. Saved PDF metadata title says “updated 10/2026”; retain month precision,
not an invented day or an older search-result title. `mccarthy-pdf-metadata`
retains that extraction against original PDF hash.

Christina Rodriguez; 954-831-5601; div101@17th.flcourts.org; chambers WW5133;
courtroom WW5150. Mailing Box 192 at 201 SE 6th Street, Fort Lauderdale 33301.
Tuesday-afternoon nonjury trials use 10165, distinct from Tuesday-morning 5150.
Pretrials alternate Mondays at 1 p.m. and Thursdays at 9 a.m./1 p.m.; motion and
special-set Zoom calendar alternate Monday mornings, Wednesday/Friday mornings,
subject to express notice/order authorization. Zoom ID 401645765.

`mccarthy-link-targets` preserves displayed labels, parent paragraphs and actual
targets. Judge-name anchor targets kmccarthy@17th.flcourts.org, while office
instructions designate div101. Postjudgment visible div101 anchor targets div47.
Do not substitute the mismatched target or infer named assistant email/fax.

Three form IDs exactly match Clermont's saved originals; reuse
`clermont-default-form`, `clermont-settlement-form`, `clermont-transfer-form`.
All three single pages reviewed again in this assignment. Transfer still says
Division 10 and includes an unrelated email; do not import it as a court contact.
Judgment optional Form 7.343 clause has 45-day delivery, stated exceptions and
express direction not to file the completed sheet with court. Standalone
`https://www.17th.flcourts.org/wp-content/uploads/2021/09/FORM.pdf` acquired and
reviewed in full (`mccarthy-emergency-form`); follows the existing triple-number
2021 emergency order's Exhibit A subject, with its own original preserved.

Reuse AO 2026-25 and filing-location 2025-40. Preserve literal 130-days-before/
150-days-after interval. Waiver due noon three business days before pretrial,
entered order required. Jury paragraph alternatively says timely submission
excuses appearance, then says entry required: preserve both. CMS supports need
efiling numbers; reopen closed cases first. JA-only over-15-minute, evidentiary,
fee, exemption/garnishment/postjudgment and pre-pretrial settings. Online only
after pretrial, maximum two cases per firm/day absent leave. Notice five business
days e-service or ten by mail; unilateral after three full business days without
response and specified notice wording. Settlement submission by 5 p.m. day before;
notice alone does not cancel. Counsel exhibits CMS/prose clerk five days before;
numbered/color photos and court copies if over 25 pages. Garnishment supports
include judgment, motion, notice/answer where applicable and writ-fee proof.

AI section cites Amendment 2 despite separately saved 2026-19 express vacatur.
Retain judge text, original exceptions and vacatur without deciding control.
Physical emergency-filing paragraph says clerk forwards with no further steps;
underlying order's presentation directions remain separate. No detailed fee
exchange, withdrawal/substitution or case-specific trial-order terms inferred.

Receipt `receipts/person-kathleen-mccarthy.json`; initial packet29/capture4328
retained, reviewed packet30/capture4330
`a8f617ca88fc28314cb0aaf9fab0a136b94b0f2e8f98883508d024bd570e0d3b` improves
summary readability only. Supporting source hashes unchanged; facts expressly
identify editorial revision, not legal change. Save script
`review/save-mccarthy-reviewed.py`; acknowledgment `review/history-capture-30.json`;
comparison `review/mccarthy-context.json`. Verified 23 topics, six differences,
128 nested citations, 403 artifact byte read-backs, semantic facts, identical
replay and preserved finalized reports. Entity-filtered check present and verified;
county remains incomplete. Inventory 216 entries. Next **Kathleen McHugh**.

### Kathleen McHugh — checkpoint 4332

Twenty-fifth judge, County Civil 51. Profile
`https://www.17th.flcourts.org/2726-2/?smid=2824` links directly to
`https://docs.google.com/document/d/1G22OK8oq9OvjinKj_CrPCWuYFgbxhDN_CLcJYAlFITc/edit`.
PDF export succeeded, manifest `mchugh-document-pdf`; all nine physical pages
checked, substantive pages 1–7 and visually confirmed blank pages 8–9. Page 1
expressly revised May 21, 2026. Profile identifies Eva-Tanja Cuthbert; procedure
supplies div51@17th.flcourts.org and 954-831-7489. Physical chambers WW11121,
courtroom WW11172, 201 SE 6th Street, Fort Lauderdale 33301; pretrials 10165;
Zoom874680432. No named assistant email, judge email or fax located.

All three linked PDFs acquired/reviewed:
`https://www.17th.flcourts.org/wp-content/uploads/2022/01/div51_Exparte_Form-2.pdf`,
`https://www.17th.flcourts.org/wp-content/uploads/2022/01/div51_Pretrial_Waiver_Form-1-1.pdf`,
`https://www.17th.flcourts.org/wp-content/uploads/2022/01/NOTICE_OF_VOLUNTARY_DISMISSAL.pdf`.
Discovery form has McHugh heading and McCarthy signature, visually confirmed;
second page blank. Waiver has Rule1.440 exclusion, Rules7.135/7.150 reservation,
20-day response, venue checkbox and PIP-treatment county. Dismissal form is blank,
with postal service certificate/contact fields. No private case data entered.

Procedure: three written coordination attempts (no waiting interval stated),
three motions per firm/day (not three cases), JA settings for over30minutes and
unrepresented parties absent online consent; video required absent permission for
audio. Final hearings/trials/calendar calls physical; other hearings Zoom. CMS
support uploads, generally no courtesy copies. Fee entitlement may be online;
amount hearing follows disposition, preliminary order compliance and JA setting.
Substitution requires client consent, both lawyer signatures and incoming counsel
certification. Written withdrawal consent avoids hearing, with stated future
service and corporate warning. Literal continuance sentence on page7 ends at
“CMS work”; preceding prohibition on agreed continuation of court-ordered hearings
remains separately recorded. No continuation hidden on blank pages. Older2023-8
CMO citation, current2025-24 and trial-setting/source exceptions retained.

`mchugh-pdf-targets` records actual label/URI pairs. Emergency-order and request-form
labels both target the same2021-51-CO PDF; reuse original triple-number order and
its ExhibitA, plus separately saved standalone form. Tutorial video remains a link,
not watched. Summons link
`https://www.browardclerk.org/ClerkWebsite/BCCOC2/filedownload.aspx` is a paid-package
catalog. Also checked official CountyCivil page for form navigation and
`https://www.browardclerk.org/clerkwebsite/bccoc2/FormLists/County%20Civil%20Forms.aspx`,
which lists the summons but does not supply a standalone original. No paid purchase
or self-extracting executable run. Preserve the current-form gap and the judge’s
warning against obsolete COVID summons. Other clerk-page content collected only,
not substantively reviewed in this judge pass.

Receipt `receipts/person-kathleen-mchugh.json`, script`review/save-mchugh.py`,
packet31, acknowledgment`review/history-capture-31.json`; capture4332
`0011e84aaaafa015946a2767be95e24303282afd5b577ee368289a6aba715c4a`.
22 topics, six differences,198 nested citations,423 artifact byte read-backs,
semantic read-back, exact replay and unchanged finalized reports verified.
`review/mchugh-context.json` retrieves verified entity check; county remains
incomplete. Inventory226 entries. Next **Giuseppina Miranda**, both52/53 before
moving to another judge.


### Giuseppina Miranda — checkpoint 4334

Twenty-sixth judge, County Civil 52 and 53 reviewed together. Official profile
IDs `https://www.17th.flcourts.org/2726-2/?smid=2827` (52) and `?smid=2814` (53)
identify Carol Hermiston, 954-831-7230, WW13137, courtroom WW13162 and Zoom530095888.
Procedure headers supply 201 SE 6th Street, Fort Lauderdale33301 and separate
`div52@17th.flcourts.org` / `div53@17th.flcourts.org` addresses. Named assistant
email, judge email and fax not located in the checked sources.

Division pages `https://www.17th.flcourts.org/division-52/` and `/division-53/`
contain distinct published iframes. Manifest keys `miranda-document52` and
`miranda-document53` retain those exact URLs and complete originals/text. Their
280/276 extracted lines, contact tables, embedded discovery order and Zoom end
instructions were read/compared; both header images are state seals, collected and
visually checked. Both state Updated December7,2025. The only substantive field
differences are division/email and telephone presentation; retain each version.
Both Print buttons target the same editing document:
`https://docs.google.com/document/d/1zuuT9hv0lwFI7nJ56i0toDQK-zxPz2lGWiDg2qYaTHI/edit?usp=sharing`.
Its ten-page PDF export was read and page1 visually checked. It is titled
Division52 and uses div52; the published Division53 body uses div53. Division52
also retains a Division53 label above its Zoom link. Do not use the print target
to overwrite either published division's contact or infer a reassignment.

Checklist preserves five-minute header versus five-to-ten-minute UMC section;
Monday/Thursday online slots, JA for other days, over30minutes, evidentiary matters,
evictions and unlawful detainer; all-schedulers conference for disputed dates;
add-on approval/agreement conditions; immediate hearing notice; distinct two
business day materials, two day courtesy and three day exhibit deadlines.
Pretrials/most evidence/trials are in person unless ordered otherwise. Remote
motion for evidence/trials due five days before absent good cause; testifying
witnesses need video. CMS orders need agreement/disagreement cover letter and are
due ten days after hearing; eviction/unlawful-detainer defaults need paper copies
and stamped envelopes. Paper plus electronic evidence directions retained.
Fees follow disposition, preliminary order, compliance and JA setting. Waiver
submission does not excuse pretrial without entered order; insurance-only
small-claims exception retains AO2020-85a1 rule exclusions. Discovery form gives
ten days after order entry for complete nonresponse without extension request.
ADA contact and trial-setting differences preserved alongside scoped shared sources.
No separate waiver or case-specific fee/trial order supplied; no terms invented.

Receipt `receipts/person-giuseppina-miranda.json`, script `review/save-miranda.py`,
packet32, acknowledgment `review/history-capture-32.json`; capture4334
`15b71caaf4caabbbb70dfd0911410b3f20b981a3273bd87597364e5f772a8a15`.
21 topics, six differences, 144 nested citations, 435 artifacts, facts, exact replay
and unchanged finalized reports verified. `review/miranda-context.json` retrieves
the verified entity check, with no finalized county baseline and review-required
assessment. Inventory235 entries. Next **Jackie Powell**; county incomplete.


### Jackie Powell — checkpoint 4336

Twenty-seventh judge, County Civil100. Current roster links directly to
`https://www.17th.flcourts.org/division-100/`; no separate current biography URL
was located through the county category page and targeted search. Use the official
procedure URL as profile, not a guessed smid or an old Division61 contact.
Landing page iframe:
`https://docs.google.com/document/d/e/2PACX-1vRurErf6vKCeYkRU_uCMAuKWSj5uHdymvcAz93l_Z2_HNrzy36K_5P8RSTt1V9mgzhyOJ_slawZ1a0t/pub?embedded=true`.
No separate print link present. Manifest `powell-document` retains all281 lines.
Both attached forms (small-claims waiver/invocation and discovery order) read;
waiver columns, signatures and rule exclusions checked in browser. Header image
is circuit seal, collected/viewed; two HTML tables contain contact and ex-parte
warning text. August2026 revision has month precision, not an invented day.

Header/roster: Simone Tucker Reid, 954-831-5597, div100@17th.flcourts.org,
WW5129 chambers, WW5155 courtroom, 201 SE6th Street, Fort Lauderdale33301;
Zoom85695743585. JIS calendar@17th.flcourts.org is technical support, not JA
personal email. No named-assistant email, direct judge email or fax located.
Office closed noon–1 p.m.; no ex-parte staff relay.

UMC Monday/Wednesday9–10 Zoom, everyone ready9,20 cases or allotted time,
five-minute non-evidentiary matters; JA copies five working days. Special sets
15/30 online, over30 and evidentiary through JA; two cases/firm/day absent leave,
multiple motions within reserved time; two full business days without response
permits unilateral setting with prescribed notice. CMS materials five business
days; paper over25 pages five days. Preserve25-page motion cap without treating
paper provision as leave. Evidence physical5155, hardcopy five business days,
exhibits overfour pages numbered/copied; CMC Zoom; rent determination physical
unless order says otherwise. Dispositive cancellation needs court approval.
Default orders need filed nonmilitary affidavit; the example's displayed plural
`servicememberscivilreliefact.com` differs from singular actual target
`http://www.servicemembercivilreliefact.com`. No commercial lookup/private data
submitted and no government status inferred.

Waiver: clerk stipulation plus separate e-order at least one business day before
pretrial, appearance remains required until order entered. Form excludes1.440,
reserves7.135/7.150 over1.430,20-day response and venue checkbox. Discovery form
requires complete failure/no objection/no extension and gives ten days from order.
Fees require disposition, preliminary order compliance and JA scheduling.
Withdrawal consent, future-service/20-day entity language and electronic versus
paper order directions retained. Substitution signed by old/new counsel.

Historical references collected without resolving priority:
- `powell-aos20-23-a2`: official17-page AOSC20-23 Amendment2 at
  `https://flcourts-media.flcourts.gov/content/download/633282/7195631/AOSC20-23.pdf`.
  Identity/context1–2, oath5–6 and signature17 read; substantive review limited to
  oath provisions. Other pages and adjacent non-oath topics not asserted reviewed.
- `powell-2022-24-a1`: three pages fully read at
  `https://www.17th.flcourts.org/wp-content/uploads/2022/06/2022-24-Temp_Amendment_1.pdf`.
  SignedJune2,2022/effectiveJune6; court operations, trials, attendance-by-notice
  and stated exceptions retained, not represented as current pandemic status.
- `powell-2021-19-a2`:28 pages collected at
  `https://www.17th.flcourts.org/wp-content/uploads/2021/05/2021-19-Civ_Amendment_2.pdf`.
  Main order1–6 reviewed; page7 identified ExhibitA start only, appendices7–28
  not substantively reviewed. May19,2021 signature and last-defendant-service
  application terms retained alongside2023/2025 sources. Judge's bare citation
  does not establish which amendment intended.

Published ten-day new-trial text differs from reviewed Rule1.530's15 days;
AI disclosure differs from retained2026-19 vacatur; rehearing cites2010-47 despite
saved2017-33/2022-5 successor statements. Preserve both, no controlling instruction
selected. Browser screenshots in `output/playwright/broward-powell-*.png` saved
with originals. These are collected-source differences, not proof of new changes.

Receipt `receipts/person-jackie-powell.json`, script `review/save-powell.py`,
packet33, acknowledgment `review/history-capture-33.json`; capture4336
`79b411cb9b7157fbb5ca83d0e19561669bb5207d14bfc2f437960a5cd65fea28`.
25 topics, seven differences,226 nested citations,447 artifact byte read-backs,
facts, replay and unchanged finalized reports verified. Entity-filtered
`review/powell-context.json` shows verified check and no finalized county baseline.
Inventory241 entries. Next **Michele McCaul Ricca**, checking her current profile
against October chart's County Criminal placement and March order's Civil47.
October chart columns visually rechecked; plain text interleaves neighboring lists.


### Michele McCaul Ricca — checkpoint 4338

Twenty-eighth judge. Live profile
`https://www.17th.flcourts.org/2726-2/?smid=16301`, current roster and
`https://www.17th.flcourts.org/division-47/` identify County Civil47; March order
page4 agrees. October chart visually places her under County Criminal. Preserve
that classification discrepancy without inventing a reassignment date or skipping
civil review. Search tool's cached biography gave old WW14127/WW14170 rooms;
directly retrieved current original gives WW13138/WW12168 matching procedure.
Do not promote cache-only differences into current conflicting official records.

Current contacts: Jose Corilloclla,954-831-7796,div47@17th.flcourts.org,
WW13138 chambers,WW12168 ordinary courtroom,201 SE6th Street West Wing,
Fort Lauderdale33301,Zoom95687147196. Pretrial5150 and trial12168/10165 are
conditional rooms. Named assistant email, judge email and fax not located.
Clerk954-831-5622 is scoped reopening contact, not complete clerk review.

Manifest `ricca-document` published iframe:
`https://docs.google.com/document/d/e/2PACX-1vTZSediPppJ6Ym1hiMgSqnVhPFsrZp7SHQY_JTy1oIYvWRJHqRXw66A2QhiMIBrSr76AmMubIXxiQXd/pub?embedded=true`.
All330 lines read. `ricca-print` comes from official print editing-document ID
`1640-1lzSvhMhipQfUE_2MdSYAapA1nluNdUFwWgfH1A`; all nine pages read, page5
rendered for waiver/jury/appearance provisions. PDF Title says LAST UPDATE08.26.26;
`ricca-print-metadata` retains derived metadata tied to same original PDF. Body has
no revision date. Record metadata location, not an inferred effective date.
Header table checked; seal and QR images collected. Seal viewed, QR presence
checked on page5, payload not independently decoded. Text supplies Zoom URL/ID.

Pretrial third-Monday1p.m./Wednesday9a.m.and1p.m.,trialTuesday,CMC/special-set
Thursday/Friday mornings,UMCThursday,postjudgmentFriday; source says schedules
subject to change. Pretrial/trial physical; listed other hearings Zoom with
physical option and notice-specific authorization language. Opening requires
motion setting within30days except pre-pretrial motions; later section requires
email hearing request within60days. Preserve different acts/periods. No online
self-setting before pretrial. JA-only:15minutes or longer,exemption/garnishment,
postjudgment,evidence,fees,pre-pretrial hearings. Motions filed/visible and case
reopened before setting. Two cases/firm/day; notice7business days e-service,
10business days postal; three full business days without response for unilateral
setting with prescribed notice. General courtesy copies optional, request copy
and order support separately required.

All orders CMS with efile-stamped support, even before clerk processing. Judgment
support includes indebtedness/nonmilitary/costs affidavits; settlement/default
and garnishment support explicitly listed. Counsel exhibits CMS,prose clerk,
both serve five days before trial; numbered/color,over25pages copies trial day.
Waiver and jury transfer noon three business days pretrial; separate entered-order
warnings retained. Settlement5p.m.beforetrial plus immediate email and required
approval/JA cancellation; notice alone never cancels. AO2026-25 applies only to
stated credit-card cases/divisions. Emergency2021-50/51/52, rehearing2022-5 and
Local11 reused within recorded scope. No unprovided fee/substitution/withdrawal
requirements invented.

Three form link IDs exactly match already collected Clermont/McCarthy originals:
`1OyEJqEC_yJCRs53FytaqPqcUnLGNZnhSZnnYiqlt9bw`,
`1Vs2visZHlwRDsFyuKj7RflJ0sL2Ap4zsz_nfGguEsTM`,
`1w2IMOi5sP4LeM_E1b5WfohjWJ7Z6eRRkoAgBsR1aRsI`.
Reused/reread originals retain earlier retrieval timestamps. Default/settlement
forms contain optional45-day7.343 return and exceptions,not filed with court.
Transfer form says Division10 and has unrelated email; neither imported as Ricca
contact or silently corrected. No personal-data blanks filled.
Linked holiday original
`https://www.17th.flcourts.org/wp-content/uploads/2026/04/2026-Court-Holidays.pdf`
fully reviewed: July7,2025 memorandum,2026 closure dates match shared schedule;
upload path is not issuance date. Saved as `ricca-holidays` shared review.

Receipt `receipts/person-michele-mccaul-ricca.json`, script `review/save-ricca.py`,
packet34, acknowledgment `review/history-capture-34.json`; capture4338
`fad05337b3f491ca2afca00c613e656373f52751133f47688416a6bbf064410a`.
23 topics,six differences,98 nested citations,460 artifacts,facts,replay and
unchanged finalized reports verified. `review/ricca-context.json` retrieves the
verified check; no finalized county baseline. Inventory249 entries. Next
**Steven P. DeLuca**, all North Satellite/civil/criminal assignments together.


### Steven P. DeLuca — checkpoint 4340

Twenty-ninth judge, North Satellite Chairperson, Civil73/Criminal-TrafficND.
Profile `https://www.17th.flcourts.org/2726-2/?smid=3805` and procedure
`https://www.17th.flcourts.org/division-73/`; published document
`https://docs.google.com/document/d/17uD4IulV7OyWRpYFbjsb2N-GJEBIojufX3VhnR0bdYw/pub?embedded=true`.
Same-ID PDF export succeeded without a separate print link. All243 HTML lines
and14PDF pages inspected: civil/shared substance and both forms reviewed;
criminal appearance categories recorded without expanded criminal doctrine review.
Pages1/12/13/14 rendered: header seal/address, Division53 conditional clause,
fixed2024 discovery date, footer-only final page. Visible revision July17,2024.

Tandakwa Walker,954-831-0322,chambersN138,courtroomN2,
1600 West Hillsboro Boulevard,Deerfield Beach33442; div73 civil,divND criminal,
Zoom499985495. No extra fax/direct judge/named assistant email located. March
assignment order says Stephen; current profile/procedure/chart say Steven.
Retain one person and both source spellings. Regional address must not be replaced
with downtown courthouse. ND and73 share official procedure URL.

UMC Wednesday9/11,15minutes equally divided,30casecap; originals filed five
business days before. Special sets follow preliminary UMC; summary-judgment/
disposition merits hearing date/duration set by judge after Motion to Set onUMC.
No double booking; add-ons by party agreement/time available. Small-claims
pretrial,nonjury trial,fee/cost evidence physical; CMC follows notice; special sets
andUMC Zoom. CMS e-orders, courtesy copies generally unnecessary. Trial exhibits
overfourpages numbered/copied,hardcopy/no-device; remote-evidence rules retained.
Fee/garnishment/rehearing settings JA-only. Hearings scheduled withinfive days
excluding weekends/holidays,heard35days absent good cause; separate40day sua-sponte
language preserved. Under-advisement follow-up30days after hearing.

Invocation discretionary/rare,form e-order,appearance remains until order entered.
Form has20day response and conditional Division53 exception inside Division73
packet; not silently changed. Discovery form complete nonresponse/no extension,
ten days from entry,unmodified and fixed2024 template year. Substitution client
consent and incoming counsel certification; agreed extensions max20days.
Deposition may not be set unilaterally, but UMC assistance motion may; keep actors
and actions separate. No detailed withdrawal or unseen fee order inferred.

New reusable sources:
- `deluca-2021-23-amended`,two pages fully reviewed:
  `https://www.17th.flcourts.org/wp-content/uploads/2023/02/2021-23-CO-Amended.pdf`.
  SignedFebruary3,2023. Satellite may retain jury case or transfer under specified
  conditions; small-claims/eviction distinction, pending-motion disposition,
  stipulation and factual-issues CMC requirements retained. Judge says all jury
  trials transfer; preserve both rather than flatten to unconditional transfer.
- `deluca-2021-69`,three pages read for civil/shared/date provisions:
  `https://www.17th.flcourts.org/wp-content/uploads/2021/12/2021-69-Temp-1.pdf`.
  SignedDecember6,2021,beginsJanuary3,2022,preambleendMarch30/finalendMarch31.
- `deluca-2022-4`,three pages read for same limited subject scope:
  `https://www.17th.flcourts.org/wp-content/uploads/2022/01/2022-4-Temp.pdf`.
  SignedJanuary11,2022,expressly replaces2021-69; saved2022-24Amendment1 replaces
  this. No current pandemic effectiveness asserted or exhaustive criminal/family
  analysis performed. Sources remain useful historical comparison evidence.

Existing2023-8/2025-24 case-management,2010-47/2017-33/2022-5 rehearing,
currentRule1.440 and2018quotedADA/2026-20 replacement differences preserved.
HistoricalADAAmendment1 original remains earlier404gap; not reclassified acquired.
Receipt `receipts/person-steven-p-deluca.json`,script`review/save-deluca.py`,
packet35,acknowledgment`review/history-capture-35.json`;capture4340
`88df5baa439fc3ab6073062e6ba840a0a5cd4324fd560da44b9817b5e1918fee`.
20topics,eightdifferences,222nestedcitations,477artifacts,facts,replay and unchanged
finalized reports verified. `review/deluca-context.json` retrieves verified check,
no finalizedcountybaseline. Inventory256entries. Next **Kathleen E. Angione**,
all listed assignments together.


### Kathleen E. Angione — checkpoint 4342

Thirtieth judge, Civil 71 / Criminal-Traffic NA / Community Court CMP.
Profile `https://www.17th.flcourts.org/2726-2/?smid=2845` and procedure
`https://www.17th.flcourts.org/division-71/`; published Google document
`https://docs.google.com/document/d/1_SM7KRycFxYBXT_YmZidNXyayfrhyUVhud4PG8t9H04/pub?embedded=true`.
Same-ID PDF export succeeded. All 184 HTML lines and nine PDF pages inspected;
civil/shared procedure and both forms reviewed, criminal categories recorded
without exhaustive analysis. Pages 1, 2 and 8 visually checked. Visible revision:
January 8, 2025. Assignment order 2026-09 page 5 identifies CMP as Community Court;
profile links combined 71/NA procedure, not a standalone CMP document.

Rebecca Raupp, 954-831-7839, chambers N144, courtroom N3. North Regional Courthouse,
1600 West Hillsboro Boulevard, Deerfield Beach 33442; div71 civil, divNA criminal,
Zoom 294767991. No extra fax, judge email, named assistant email or separate CMP
contact inferred. Procedure and profile preserve shared versus named contacts.

All hearings through JA is repeated alongside online registration/self-scheduling
language; civil heading says 15 minutes or less while following parenthetical says
less than ten minutes and no Motion Calendars. Preserve each statement. Schedule
within five days excluding weekends/holidays, heard within 35 days absent good
cause; possible sua-sponte ruling if unscheduled 40 days. Supporting documents
filed five days before hearing; no business-day unit added. Hardcopy courtesies
required at N144. No double booking; add-ons require court approval. Special-set
conferral cites circuit/family Local Rule 10A: preserve scope mismatch.

CMC Zoom unless otherwise noticed; civil pretrial, nonjury/final, fee/cost evidence
and rent-determination evidence physical. Zoom-permitted language also requires
motion/order for telephonic appearance five days before and movant initiating call.
Cancellation has restricted grounds and JA/opponent email, while later instruction
says online cancellation. Trial notice appears both as mail/deliver with envelopes
and status conference, and mail/email with likely mediation/arbitration. Jury
transfer statement is broader than cited amended order's conditions/retention.
Historical courthouse-order chain, case-management/trial-setting and ADA-reference
differences retained without resolving authority.

Invocation requires agreed motion and attached e-order, discretionary, no excused
pretrial appearance before entered order. Division 71 form gives 20-day response
from order; despite general exception wording, it contains **no Division 53 or
1.440/7.135/7.150 exception clause** before discovery form. PDF page 8 confirms.
Discovery form unchanged, complete nonresponse/no extension, ten days from entry,
blank 20___ year. Never import clauses or fixed year from similar DeLuca form.
Substitution requires client consent and counsel certification; agreed extensions
max 20 days. Depositions not unilateral; assistance hearing may be. Emergency
request and hardcopy numbered exhibits saved with relevant shared references.

Receipt `receipts/person-kathleen-e-angione.json`, script `review/save-angione.py`,
packet 36, acknowledgment `review/history-capture-36.json`; capture 4342
`b6b5348f53948f5a0c746f00b1b210fbcb319d0169d5bb49f7233a2445f33ec0`.
23 topics, ten differences, 227 nested citations, 484 artifacts, semantic facts,
exact replay and unchanged finalized reports verified. `review/angione-context.json`
returns the entity's verified check; no finalized county baseline. Inventory 260
entries. No new shared original needed; relevant existing sources reused with
original retrieval dates and review limits. Next **John Hurley**.


### John Hurley — checkpoint 4344

Thirty-first judge, North Satellite Civil 72 / Criminal-Traffic NB. Profile
`https://www.17th.flcourts.org/2726-2/?smid=2809`, procedure
`https://www.17th.flcourts.org/division-72/`, published document
`https://docs.google.com/document/d/1OJelOCQ5C39yEaKzWMTvZlrJbDfonqNvAEP5QwHsN-Y/pub?embedded=true`.
Same-ID PDF export acquired. All 468 HTML lines and 16 PDF pages inspected;
civil/shared content, two forms and holiday list reviewed. Criminal categories
and schedule on pages 2/4 recorded without expanded analysis. Pages 1/13/14/15
visually inspected. Updated August 28, 2026. One header table and seal image.

Inga Alexeev, 954-831-1272, div72@17th.flcourts.org, N140 chambers, N1 courtroom,
North Regional Courthouse, 1600 West Hillsboro Boulevard, Deerfield Beach 33442;
Zoom 402362403. Header name JOHN M.B.HURLEY retained as variant of roster John
Hurley; no middle-name expansion. No separate NB/named assistant email inferred.

All hearings special set: CMS through 30 minutes, JA longer or no agreeable time.
Bulk same-parties/same-motion settings allowed with separate orders. Unilateral
hearing after two full business days without response; source separately states
five-to-20-day interval from known conflict. Add-ons need approval; notice filing
alone insufficient. Deposition may be unilateral after five business days and two
coordination attempts; no compel-dates hearing. These differ from Angione’s rules.
Motion hearing set within five days excluding weekends/holidays, heard within
60 days absent good cause; unscheduled 60-day sua-sponte statement preserved.

Physical small-claims pretrial and evidentiary hearings including eviction unless
approved written motion; Zoom CMC/special sets and later notice-specific exceptions
preserved. Counsel video/full name, no driving, no more than five minutes early;
technical failure call JA. Non-file documents CMS two business days before.
Rehearing courtesy plus contemporaneous call within five business days. In limine
five days before trial; other pretrial motions ten days; Daubert two weeks before
pretrial conference. Exhibits premarked at pretrial, over-four-page pagination.
Continuance/extension needs actual relief, not merely filing. Withdrawal client
contact/service details and all-client consent exception saved. Party-set versus
court-ordered cancellation kept separate; settlement alone does not cancel.

PIP upload directions exclude blanks/style/signature/end paragraph; pro-se paper
exception. Non-PIP invocation discretionary and entered order required to excuse
appearance; body reserves 7.135 generally. Division 72 form nevertheless contains
Division 53-only 1.440/7.135/7.150 exception and 20-day response. Discovery form
has fixed 2024/Fort Lauderdale wording. Originals unchanged. Holiday dates
December 24/25 agree with memorandum but labels differ; do not invent closure-date
difference or treat omitted earlier holidays as open. Rule 1.202 quotation, case
management, ADA, appearance and scheduling-assistance differences recorded.

Receipt `receipts/person-john-hurley.json`, script `review/save-hurley.py`, packet37,
acknowledgment `review/history-capture-37.json`; capture4344
`ffaf2f3b2f6dd75b74a04529e98ac59b734bab3347a21cf0a120e4e93fbee587`.
27 topics, eight differences, 216 nested citations, 493 artifacts, semantic facts,
exact replay and unchanged finalized reports verified. `review/hurley-context.json`
returns verified check; no finalized county baseline. Inventory264 entries. Shared
sources reused with original timestamps; no new shared original required. Next
**Kim Theresa Mollica**, all North Satellite assignments together.


### Kim Theresa Mollica — checkpoint 4346

Thirty-second judge, North Satellite Civil 70 / Criminal-Traffic NC. Profile
`https://www.17th.flcourts.org/2726-2/?smid=2828`, wrapper
`https://www.17th.flcourts.org/division-70/`, official PDF target
`https://docs.google.com/document/d/1z_tZpSLCzfKRlu4hsktyoCS0ElVbcI-x8QPI2JAA4lI/export?format=pdf`.
Search tool could not follow export redirect; direct HTTP returned 200. All 18
pages inspected, civil/shared substance and three forms reviewed. Criminal-specific
paragraphs on pages 6/7/9/10 preserved without exhaustive analysis. Pages
1/3/7/8/14/16/17 visually checked. Visible revision September 10, 2026.

Suzanne Randall, 954-831-1236, div70 civil and divnc criminal, N142 chambers,
N4 courtroom, North Regional Courthouse, 1600 West Hillsboro Boulevard,
Deerfield Beach 33442; Zoom 561587919, separate dial-in 305-224-1968. No named
assistant/direct judge email or fax inferred. Page 1 prosecutor display and mailto
annotation disagree (Alight versus Dwilliams); both retained in PDF/link extraction,
neither imported as court contact or used to expand low-priority research.

Source says through-30-minute/motion-calendar hearings Zoom with exceptions,
later all appearances physical absent order, and civil CMC/pretrial physical absent
remote order. General audio options coexist with advance approval required for
audio-only. Preserve rather than merge. Civil motion filed then courtesy, CMS/JA
setting, subject case number/all names, notice efiled. Pro-se scheduling JA unless
consent to online; unilateral nonresponsive-attorney hearing after two full business
days. Three motions per firm/day, no double booking or add-ons without approval;
over 30 minutes JA coordination. Deposition may be unilateral after two business
days without reasonable dates, no compel-dates hearing; do not import Hurley terms.

Authority/responses two business days; over-20-page authority/discovery hardcopy.
Remote evidence Notice of Filing five days before, separate CMS/log requirements.
Paper numbered exhibits retained alongside remote directions. Generally no
courtesies except specific requests. Settlement/cancellation requires filing,
JA email and acknowledgment; continuation package/e-order exception versus
court-ordered-hearing restriction preserved. Under-advisement follow-up 30 days.
Pro-se no-email orders physically to chambers, all requests filed with clerk.

Attached discovery form pages 12–13: complete nonresponse/no extension, ten days
from entry, blank year and Deerfield Beach. Invocation pages 13–14: 20-day response,
Division 53-only exceptions within Division 70 procedure, no silent replacement.
Preliminary fee form pages 14–16: timesheets within 30 days of order and served
compliance notice before setting; cost support 15 days from request; objections
30 days from compliance-notice service; reply ten days from objection receipt,
then JA setting. Opponent hours ten days from informal request; expert conference
**not more than two business days immediately preceding** hearing. Preserve
this comparator, discovery limits, itemized objections and good-cause exceptions.
Template is not evidence of entry in a particular case.

AI link uses January path, returned 404 and response retained as `mollica-ai-linked`.
Previously saved official April-path Amendment 1 and later Amendment 2/vacatur
supply comparison; no extra AI requirement invented from link heading. Procedure
now cites 2026-20 ADA, so no copied historical ADA gap. July–December holiday dates
and labels agree with shared memorandum. Older case-management/trial terminology
retained separately from later sources. No new shared substantive source needed.

Receipt `receipts/person-kim-theresa-mollica.json`, script `review/save-mollica.py`,
packet38, acknowledgment `review/history-capture-38.json`; capture4346
`69293918598df91be1f7d67a1e7649503558d26a832549c0ceec9c003420f5a6`.
31 topics, eight differences, 241 nested citations, 504 artifacts, semantic facts,
exact replay and unchanged finalized reports verified. `review/mollica-context.json`
returns verified check; inventory268 entries. Link annotation derivative and seven
rendered pages included in saved artifacts. Next **Tabitha B. Eves**.


### Tabitha B. Eves — checkpoint 4348

Thirty-third judge, West Satellite Civil 81 / Criminal-Traffic WE. Profile
`https://www.17th.flcourts.org/2726-2/?smid=11958`, wrapper
`https://www.17th.flcourts.org/division-81/`, published source
`https://docs.google.com/document/d/e/2PACX-1vQ9Ohj4Tw90UBbXxxoT3Cww3r6nafusBxBg2PkCOnrKZ0yokiRedgeWqG_4CUCpUM4hxV9nHpTWZZq1/pub?embedded=true`.
All 138 lines reviewed, including two forms; six browser screenshots cover the
published page, header table and seal. No separate print/edit link supplied;
no guessed ID or unavailable attachment asserted. Last modified October 8, 2025.
Google auto-refresh text is platform behavior, not a procedure revision.

Shanetta Brown, 954-831-2314, div81 civil/divwe criminal, W210 chambers,
W240 courtroom; West Regional Courthouse, 100 North Pine Island Road,
Room/Suite 210, Plantation 33324; Zoom 855034385. Chart uses Tabitha Blackmon Eves,
profile/procedure Tabitha B. Eves, retained under one person. Physical and mailing
labels preserved. No extra fax, direct judge or named assistant email inferred.

Motion calendar/special sets Monday/Tuesday, CMS; pro-se or over 30 minutes email
JA, no available slot email JA copying all. Unilateral hearing after three
reasonable unsuccessful good-faith attempts, notice label plus correspondence;
no invented waiting period. Immediately file/serve notice with Zoom and ADA.
Court all-material receipt three business days includes nonjury trials; evidence
filed with clerk two days before evidentiary hearing. Different acts/recipients/
units preserved. Continuance five days before, requesting party signs. Settlement/
dismissal filing, courtesy with efiling number and cancellation notice required.

Word orders via CMS with agreement/disagreement cover letter. No dates-compel
hearing; deposition unilateral after five business days without reasonable dates.
Discovery body says ten days from signing, form from entry. Form COWE case template
and incomplete year "20 in Plantation" preserved. Invocation expressly names
Division 81 for rule exceptions, so no copied Division 53 discrepancy. It begins
at order text, no invented separate attorney waiver-signature requirement.
Screen-share email at least one business day before, distinct from evidence filing.
Rehearing points to 2022-5; emergency motion identifies issues, need and each
party's time; court determines/sets emergency. Shared orders retained separately.

Hybrid paragraph and closing Zoom-calendar default kept separate. ADA paragraph
names Diana Sobel; saved information sheet names Taiwo Akinkunmi but body dates
April 2017 despite 2025 filename; current 2026-20 names coordinator title. Preserve
both dated statements without asserting personnel change. No unprovided fee,
under-advisement or trial-setting details imported from another judge.

Receipt `receipts/person-tabitha-b-eves.json`, script `review/save-eves.py`, packet39,
acknowledgment `review/history-capture-39.json`; capture4348
`9a3d4b006a63e2708fd475f2db9f0cca084034cfae5004ade9a100c853267d5e`.
18 topics, four differences, 150 nested citations, 508 artifacts, semantic facts,
exact replay and unchanged finalized reports verified. `review/eves-context.json`
returns verified check; inventory271 entries. Six screenshots saved as artifacts.
Next **Ellen Feld**, all West Satellite assignments together.


### Ellen Feld — checkpoint 4350

Thirty-fourth judge, West Satellite Civil 83 / Criminal-Traffic WA. Profile
`https://www.17th.flcourts.org/2726-2/?smid=2790`, wrapper
`https://www.17th.flcourts.org/division-83/`, published document
`https://docs.google.com/document/d/e/2PACX-1vSEZNFxdVPKVT8WZdpUMz1s2WmjRMhEu_AXBuZRRYG0fkXxu832LlHnRzyfkvLo0bUQzKKDdn7dERAS/pub?embedded=true`.
Print/edit link uses `1R6vK9MJMhB_kWn5IUWkZ27FdTuB1a4bd1JReZkODYFU`;
same-ID PDF export acquired. All 192 HTML lines and ten PDF pages reviewed,
including complete appended discovery form. Pages 1/2/5/6/7/10 visually inspected.
No stated revision/effective date or PDF metadata creation/modification date.

Paula Galluccio, 954-831-3304, fax 954-831-3340 under source label "if applicable";
div83 civil/divwa criminal, W210 chambers and W240 courtroom. West Regional,
100 North Pine Island Road, Plantation 33324; header Room 210, mailing paragraph
omits room. Zoom 684278427. No extra named assistant/direct judge email inferred.

General communications telephone/no texts, but email-copy and trial-notice email
requirements also supplied; retain scopes. JA one-business-day response aim is not
court deadline. Empty checkbox glyphs beside e-service text preserved, no invented
selected state. CMS through 30 minutes and over 30 with court approval; unavailable
slot prompts conference call with JA/all parties. Immediate notice/ADA/Zoom; cancel
via JA notification, filing/service and CMS. Continuance specifies basis/knowledge,
opposition, concrete preparation/participant dates and proposed ready date; party
signature except good cause. No universal five-day cutoff or unilateral rule copied.

CMS hearings Zoom unless notice says otherwise; camera/quiet space/no vehicle,
muted mic and witness equipment tests. Remote-objection deadline literally
**insert deadline** in both versions, visually confirmed. Electronic exhibit email
literally **Insert Division or Judicial E-mail**, also in both. Targeted official-site
searches returned no result. Save as unknown source fields; header contacts and
trial-notice div83 address cannot fill them. Complete source review does not mean
the published instructions are operationally complete.

PDF/ proposed-order format, proposed-order efiling portal or CMS, pro-se excused
mail/hand-delivery. No courtesies generally; printed exhibits clerk, copies for
clerk/court/parties and electronic exhibits five days before. CMC attorneys/pro-se
mandatory absent advance excuse, represented parties need not attend; reasoned
conference requests then online setting if granted. Notice for Trial emailed div83;
retain current Rule 1.440 comparison. Emergency motion issues/need/time, court
sets if emergency. ADA title/contact and interpreter office 954-831-2807 recorded
without eligibility/payment assumptions. Discovery form names Feld, ten days from
entry, blank year/Fort Lauderdale, no invented invocation or fee form.

Receipt `receipts/person-ellen-feld.json`, script `review/save-feld.py`, packet40,
acknowledgment `review/history-capture-40.json`; capture4350
`fc6cbd66e914f8df175dcbe62f1c3d8a2b60b55423381d0eeab6f5e2d1900c93`.
18 topics, three differences, 162 nested citations, 517 artifacts, semantic facts,
exact replay and unchanged finalized reports verified. `review/feld-context.json`
returns verified check; inventory275 entries. Next **Olga Levine**.

### Olga Levine — checkpoint 4352

Thirty-fifth judge, West Satellite Civil 80 / Criminal-Traffic WB. Profile
`https://www.17th.flcourts.org/2726-2/?smid=2818`, wrapper
`https://www.17th.flcourts.org/division-80/`, published document
`https://docs.google.com/document/d/11SkCjbvr_Gx7gGidx_KFomiCMAP5UTrf0n-ymwVV51c/pub?embedded=true`.
Same-ID PDF export is 22 pages. Civil/shared pages 1–14 reviewed; page 22 WB link
recorded. Extraction-empty pages 15–21 contain scanned criminal/traffic forms,
visually classified and retained without substantive review. Never call them blank.
Published text has 278 lines and states Last Updated August 19, 2026.

Andyel Hernandez, 954-831-7571, shared civil div80, W270/W220, Zoom489403007,
dial1-646-876-9923. Judge header says West Regional,100NorthPineIslandRoom270,
FortLauderdale33324; clerk locations page says Plantation for same street.
Preserve both statements and do not substitute clerk Room170 for chambers270.
No fax, named assistant email, judge direct email or WB email inferred.

Linked forms PDF:
`https://www.17th.flcourts.org/wp-content/uploads/2018/04/Div80ProceduresAmendment.pdf`.
All ten pages reviewed: telephone counsel/party and witness orders; four-page
pretrial order; discovery order; three-page fee order. No revision date stated;
parent August2026 date is not inherited. Witness form names Bibi Khan at same
phone. Pretrial ADA names Diana Sobel,Room20140; fee ADA gives Room470; retain
current AO2026-20 and dated information-sheet comparisons.

CMS five-minute UMC and15/30-minute special sets; JA-only eviction/unlawful
detainer, exemptions, fees, over30minutes, nonjury/final and rehearing. All landlord-
tenant matters specially set; rent determination brought to court attention and
scheduled within ten days of filing or source says waived. Do not change schedule
to conduct. Three unsuccessful reasonable good-faith coordination attempts allow
unilateral hearing with notice label/correspondence; deposition uses five business
days without reasonable dates, not imported hearing-attempt rule.

Five-business-day hearing documents, pro-se JA mail/email plus copy certification,
represented supporting documents; efiling does not deliver judge copy. Notice of
filing limited to100 documents, not pages; policy/riders separate exception.
UMC order within5days; agreed form online, disputed PDF/Word orders emailed with
cover letters. Continuance conferral/filing, agreed order permitted, opposed hearing;
cancellation CMS plus JA, special-set written merits stipulation or court approval.

Physical small-claims pretrial and evidentiary/nonjury unless approved written
remote stipulation; non-evidentiary/CMC/LOP Zoom. Small-claims plaintiff under10cases
minimum2attorneys, over10minimum4; exactly10 and counting window unaddressed.
Remote-witness objection10days from order; linked form telephone court-initiated
call vs current Zoom text. No recording vs historical consent/media exceptions
retained. Withdrawing counsel supplies client contacts/service and30day order;
written consent permits no hearing. Substitution requires signatures, client consent
and incoming counsel certification of docket/counsel/deadline knowledge.

Discovery complete nonresponse/noextension uses prescribed form, no additions;
signing/entry/date-of-order triggers preserved. Invocation text only two paragraphs,
20day response fromorder; no invented Division53 exception. Trial readiness notice,
mail/deliver JA envelopes and prior joint stipulation; current Rule1.440 comparison.
Trial exhibits over4pages paginated, hard copies; separate remote CMS/log duties.

Pretrial template discovery90days, plaintiff/defense experts30/40, jointstip100;
mediation105/arbitration120 only if checked. PTC-dependent block and optional
summary-judgment10day/prior-motion-ruling boxes remain conditional. Within block,
limine5days beforetrial, Daubert2weeks beforePTC, premarking/settlement requirements.
Joint submission has actual named alphabetical witnesses, specific exhibits/
objections, instructions/verdict forms where applicable. No case dates computed.
Fee template time sheets30days fromorder, cost support15days fromrequest,
objections30days fromcompliance-notice service, reply10days fromreceipt thenJA,
opponent hours10days frominformalrequest. Expert conference not more than2business
days immediately preceding; discovery/objection limits and good-cause exceptions.
Paragraph5 visibly contains malformed `9m`; next page expressly says expert.
Retain that ambiguity rather than silently repair source text.

New shared reviews: six-page AO2020-42 Amendment1 datedMarch29,2021 for civil/shared
remote procedures; criminal-only paragraph not expanded. Five-page SC2024-0662
May23,2024 opinion/appendix (stated effectiveJan1,2025) visually checked for deleted/
added text; current Rule1.202 comparison retained. AI disclosure, older emergency
and rehearing references recorded beside existing replacement/vacatur sources.
No controlling-authority resolution asserted.

External ExhibitA Google ID `19HnMI4ESII3HAHtNUSWWrHFNYwE6bB2xizzRDk92R0s`
edit/bookmark and PDF export both410. Embedded CMS ExhibitA lines229–276 reviewed;
do not claim it proves external target contents. WB docket link
`https://drive.google.com/file/d/1zNzU6zYKfw09ApnbL0FqM6BSgoCA_Ral/view?usp=drive_link`
recorded without criminal substantive expansion.

Receipt `receipts/person-olga-levine.json`, script `review/save-levine.py`, packet41,
acknowledgment `review/history-capture-41.json`; capture4352
`e96cbca4e5d4bb9f39533ee82893d940d5045e3b93d3ac2a20964d04f32c3b65`.
31 topics, ten differences,262 nested citations,550 artifacts, semantic facts,
exact replay and unchanged finalized reports verified. `review/levine-context.json`
returns verified check; inventory284 entries. Next **Lauren N. Peffer**.

### Lauren N. Peffer — checkpoint 4354

Thirty-sixth judge, West Satellite Civil82 / Criminal-Traffic WC. Profile
`https://www.17th.flcourts.org/2726-2/?smid=21191`, wrapper
`https://www.17th.flcourts.org/division-82/`, published document
`https://docs.google.com/document/d/e/2PACX-1vQnz8XBkyhDHoxy72Yt9PWItTYB67-ujBlXK7igtYvXJB4ZhPjpDT_A9w1yYQjXfEJ7WSfQQxdTvk4h/pub?embedded=true`.
All260 extracted lines, rendered document and two appended forms reviewed.
Updated January28,2025. Three header images include address, seal and name;
address/name manually transcribed in `peffer-header-transcription` manifest entry,
retaining original HTML hash/time and explicit derivative label. Full HTML body
extraction unchanged. Browser screenshots saved; no full-procedure print/edit link
supplied, no export ID guessed.

Jennifer Castaneda,954-831-3381,shared div82,W270/W260,West Regional100NorthPineIsland
Room270,Plantation33324; Zoom190948749,dial1-646-876-9923. No WC email, fax or direct
judge/assistant email inferred. Header image and profile/clerk sources corroborate
address/rooms without borrowing clerk Room170.

CMS scheduling includes JA advice on time/calendar; JA-only over30minutes,
eviction/unlawful detainer, exemption, fees. Pro-se requires JA unless agrees online.
Firm cap three motions/day, no double booking/add-ons absent approval. Motion set
for hearing within60days of filing; no invented separate heard-by date. Three
reasonable unsuccessful attempts permit unilateral hearing with notice/correspondence;
deposition separately two business days without reasonable dates. UMC cancellation
online plus JA; specialset email reason/court approval/JA cancellation.

Case law highlighted to court/opponent five business days before viaCMS/email/paper;
general supporting-document paragraph forbids sending even byemail, while pro-se
paragraph requires mail/email and represented permitsCMS five business days before.
Preserve scopes. CMC listed Zoom and later physical absent remote order. Written
remote motion/order paragraph retained beside Zoom default. Camera on, no recording,
vehicle recalled until parked; screen-share request one business day before.

Orders online when all represented, broad hardcopy ban beside pro-se mailcopies;
posthearing agreed form online, disputed PDF/Word email with coverletter. UMC order
within5days. General no courtesies does not erase emergency/fee/case-law directions.
Emergency filed/courtesy copied email, judge determination,2021-51Request form.
Exhibits over4pages paginated; four hardcopies; shared remote evidence separately.

Historical2023-8 case plan except evictions compared with2025-24. Notice for Trial
mailed/delivered JA with envelopes, mediation/arbitration then unresolved trial;
currentRule1.440 comparison retains invocation exception. Invocation four paragraphs
expressly Division82,20day response,1.440 excluded and7.135/7.150 over1.430,PTC waiver.
Discovery ten days from entry, no added form language; incomplete year20 in
Plantation retained. Substitution consent/newcounsel certification; withdrawal
contacts/service/30days, no unprovided consent exception. Continuance conferral,
file/upload and opposed hearing; no imported cutoff. Rehearing2010-47 compared
with2017-33/2022-5; AI disclosure compared with later amendments/vacatur.

Fee form editID `1gRuRa15bVeGPYis-bXNRRzSXBZL3cilX`, same-ID PDF export, two pages
fully read/rendered. Disposition required before preliminary order; entitlement
before hearing; comply thenJA setting. Form records/support10days fromorder,
objections20days fromorder,reply10days fromreceipt. Attorney conference no later
than preceding business day, written agreements/order; limited discovery, cost
guidelines, goodfaith/sanctions, potential mediation/arbitration. Paragraph4 says
nonmoving party states amount **moving party** believes reasonable; visible actor
mismatch preserved. Preprinted2025 is template year, not revision date. Do not reuse
nearby judges’ thirty-day fee sequence or expert-conference terms.

Legacy `http://www.17th.flcourts.org/index.php/self-help/eorders` returns404.
Current `https://www.17th.flcourts.org/cms3-manuals/` accessible and saved; existing
workbench source reused. Navigation/index reviewed; linked upload training is video,
not watched or asserted identical to old page. No communications sent to court.

Receipt `receipts/person-lauren-n-peffer.json`, script `review/save-peffer.py`, packet42,
acknowledgment `review/history-capture-42.json`; capture4354
`f733f507dc0f9c467cfe9c344f6c1d3c4a433e09624b9bb69be33345dafbb104`.
29topics,8differences,240nested citations,551artifacts, semantic facts, exact replay
and unchanged finalized reports verified. `review/peffer-context.json` returns
verified check; inventory291entries. Next **Corey Amanda Cawthon**.


## Completed judge 37: Corey Amanda Cawthon, 61/SC/CMH

Profile `https://www.17th.flcourts.org/2726-2/?smid=8353`; official procedure
wrapper `https://www.17th.flcourts.org/division-61/` embeds/downloads
`https://docs.google.com/document/d/1x1X2SAfE_hNpNIV5GUGcj4HqwXfkllHa/export?format=pdf`.
The original is11pages, revised July19,2024. All pages visually checked; civil/shared
text and forms reviewed. Criminal portions screened for assignment/contact/shared
relevance, without expanding into separate SC or community-court manuals. Page11
is visually footer-only. See manifest keys `cawthon-bio`, `cawthon-division61`,
`cawthon-procedures` for original URLs, timestamps, hashes and extraction files.

Samantha Broderick;954-831-0308; shared `div61@17th.flcourts.org` and
`divsc@17th.flcourts.org`; chambersS226/courtroomS230. Header and page5 physical
submission address: South Regional Courthouse,3550HollywoodBoulevard,Suite226,
HollywoodFL33021. Zoom606672692, dial16468769923 is conferencing, not chambers.
No named assistant/judge email, fax or separate CMH email inferred.

Distinct requirements to retain: motion filed AND online-docket-visible before
scheduling; UMC5minutes, special15/30online, over30JA; at most2hearings per case
per UMCsession and3motions per firm per singledocket. New JA email per request,
court case number/party names in subject and courtesy filed motion attached.
Exemption/eviction/unlawfuldetainer/evidentiaryfees require JA coordination.
Three unanswered attempts permit unilateral notice with prescribed label and
proof AT HEARING. Cancellation follows original online/JA scheduling channel.
Do not import another judge's per-day limits, proof attachments or dual-channel
cancellation instructions.

Posthearing competing Word orders and covers go in ONE email. All-represented
agreed/discovery/invocation CMS instructions coexist with specific physical
pro-se-without-registered-email and property/collection order options. Trial
notice email and stamped-envelope language remains explicit; physical continuance
packet and agreed-CMS directions are separately recorded. Exhibit deadlines come
from the actual hearing/trial order, with court hardcopies beforeZoom/atphysical
hearing and shared remote evidence duties preserved separately. Countycivil-only
interpreter instructions are not applied to criminal cases.

Page9 invocation form has Division61,20days fromorder,1.440 exclusion and
7.135/7.150 over1.430, plus both attorneys' waiver signature/contact blocks.
Page10 discovery form uses10days fromENTRY, complete nonresponse and no requested
extension. Preliminary fee order is described as issued in the case but no public
form is appended/linked or found in targeted official search; no borrowed fee
terms or finaljudgment/entitlement prerequisite. Exact legacy eorders URL404 is
reused from Peffer with its original retrieval timestamp; current manuals/workbench
navigation retained, training videos not reviewed. Historical2023-8/current2025-24
and trial-settingRule1.440 differences are recorded without authority resolution.

Receipt `receipts/person-corey-amanda-cawthon.json`; save script
`review/save-cawthon.py`; packet `draft/checkpoint-43.json`; acknowledgment
`review/history-capture-43.json`, all relative to the pinned run. Capture4356
`c5f84aedb6ff8b7121a8e617d8b7d96f53063a8901c788bd25d4ccd31420a97f`:
22topics,3differences,193 validated nested citations,555 artifact byte read-backs,
294 cumulative source entries, exact replay and facts read-back; finalized reports
unchanged. `review/cawthon-context.json` confirms exact-entity verified check,
currentfinding, unknown finalized baseline and `review_required`. Remaining
county work stays incomplete. Next Corey B. Friedman, all assignments together;
reconcile conflicting roster/assignment statements with Gilman and unnamed62/SB
without silently overwriting historical observations.


## Completed judge 38: Corey B. Friedman, 60/SA

Profile `https://www.17th.flcourts.org/2726-2/?smid=12290`; wrapper
`https://www.17th.flcourts.org/division-60/`. Follow its actual published iframe
and print link; print document ID `1QMU8nn17H_ts8ZDkWQMqLtM2xKenrNuZ_K9Vmz9aLhM`.
Manifest keys `friedman-bio`, `friedman-division60`, `friedman-document`,
`friedman-print` retain exact URLs, bytes, dates and hashes. Full353-line published
text and17-page PDF reviewed; all17 page images inspected. Civil/shared procedures
1–9, waiver10, invocation11, discovery12, virtual13–14, AI15–17. SA substantive
criminal expansion was deliberately omitted; shared orders were reviewed.

Shelly Skofstad,954-831-0306, chambersS214/courtroomS210; South Regional,
3550HollywoodBoulevard,Suite214,HollywoodFL33021; Zoom990901272. Visible emails
div60/divsa are supported by procedure text. **Some mailto targets differ**:
first civil and courtesy anchors point todiv62; criminal anchors todivsb. Two
hearing/fee anchors correctly point todiv60. `friedman-email-anchors` preserves
labels and targets separately from original HTML. Search-renderer parenthetical
addresses are not extra source prose or verified alternate contacts. No personal
email, fax or dial-in inferred.

Revision October1,2026. PDF14/17 have handwritten1st October2026 and signature
marks omitted by extraction. `friedman-signed-dates` is a manual derivative tied
to original PDF/hash/time and page images. It is not signature authentication or
proof of docket entry. AI order applies from date of entry, which is not separately
verified. March2026 assignment order lists FriedmanMN and Gilman60/SA; current
profile/procedure and October chart separately place FriedmanSouth60/SA. No
transfer effective date invented.

Keep two full BUSINESS days for nonresponsive scheduling, not Cawthon's three
attempts; source says attach written attempts without expressly identifying the
attachment destination. Two hearings per case/session; no borrowed firm cap.
Status calls barred before14business days after submission. Remote bench trial
requires all-party filed stipulation. Competing Word orders/covers together in one
email; cancellation follows initial scheduling route. Invocation prose names
Franker and form condition literally saysDivision61 despite Friedman/60cover.
These are recorded, not silently corrected. No fee template appended/linked or
found by targeted official search; case-issued order terms remain unknown.

Virtual order says camera OFF/muted and contains both pull-over and automatic-
removal driving language. AI standing order15–17 includes oversight, above-signature
disclosure with routine-use exceptions, a separate broadly worded certification,
prohibitions/red flags, notice/hearing and sanctions, entry-based scope. Body and
standing order cite2026-03Gen; amendments and2026-19vacatur separately retained
without deciding controlling authority. Lisandrillo/Rule2.515/57.105 citations are
judge-source statements; not independent holdings/rule review in this task.
Targeted officialDCA search returned no results, not proof of absence. Search log
`review/friedman-search-review.json` saved. Current shared case-plan/trial, delivery
and source-association differences remain explicit.

Receipt `receipts/person-corey-b-friedman.json`; save script
`review/save-friedman.py`; packet `draft/checkpoint-44.json`; acknowledgment
`review/history-capture-44.json` relative to pinned run. Capture4358
`29a2075d9eb780604f9501737a98dd5b80425187a6bb810111fadf14ec0f86df`:
28topics,8differences,250 validated nested citations,573 artifact read-backs,
300 cumulative source entries, facts/read-back/replay and finalized reports
unchanged. `review/friedman-context.json` confirms exact-entity verified check,
current finding, unknown finalized baseline and review_required. Next Allison
Gilman; county roster and remaining review still incomplete.


## Completed judge 39: Allison Gilman, MN

Current judiciary page2 links profile `http://www.17th.flcourts.org/2726-2/?smid=21192`
(successful redirected acquisition) and `https://www.17th.flcourts.org/division-mn/`.
Wrapper print ID `1LR3zDImHIxm9XdAvKX9ZRHzAEmpzZTID`; actual published iframe,
print/export, URLs/hashes/timestamps in `gilman-*` manifest entries. Current profile
and October1,2026 procedure name GilmanMN. Cindy Kydd;954-831-5509;divmn; chambers
WW5135/courtroomWW4155; Broward County Courthouse,WestTower,201SE6thStreet,
FortLauderdale33301. No direct personal email/fax/dial-in inferred. Mailto targets
checked and match displayed divmn. Court Administration9548317740 is separate.

Seven-page PDF collected and all pages visually screened; common contacts,
communications, access and source associations reviewed. Bail/probable-cause,
pleas and victim-rights materials retained without exhaustive criminal analysis.
No current civil assignment supplied by current profile/procedure; March2026
order's Gilman60/SA statement retained separately. Do not attribute Friedman's
current60procedure to Gilman merely because the dated assignment differs.

Profile/header/links use Zoom620446048 but SectionC prints95486630441. SectionC
calls May19,2026 standing order Gilman's; image appendix6–7 names/signatureline
CoreyB.Friedman and handwritten19thMay2026. `gilman-standing-transcription`
retains selected image passages tied to original PDF/hash/time; not signature
authentication or docket-entry proof. Attorney video-on/checkin, observer-off-
unless-speaking, breakout audio/video and attached general camera-off directions
remain contextual source differences. MN access hours recorded as source statements,
not verification of particular dockets; duty-schedule and constitutional links
retained without expanding into substantive criminal research.

Initial person validation correctly rejected an empty governing-rules list before
any database save. Repaired by including the previously reviewed circuit-wide
2026-20 ADA notice/access requirement with its actual scope, not by claiming no
local rules or weakening validation. Later agents must retain shared court-access
rules for criminal-only assignments while respecting the limited substantive scope.

Receipt `receipts/person-allison-gilman.json`; script `review/save-gilman.py`;
packet `draft/checkpoint-45.json`; acknowledgment `review/history-capture-45.json`
relative to pinned run. Capture4360
`d8cdbab88906a872fe66f9edfd60bce21e4a92aff85c7aacdc2608ff98dc0fe9`:
10topics,4differences,61 nested citations,571 artifact byte read-backs,306 cumulative
source entries, semantic facts/exact replay and finalized reports unchanged.
`review/gilman-context.json` verifies exact-entity check/current finding with
unknown finalized baseline and review_required. Next inspect unnamed62/SB official
row/procedure; do not count a blank name as a person or declare vacancy by inference.


## Roster-source checkpoint46: unnamed62/SB and active Franker review

The original roster response contains one62/SB row with empty name and assistant,
phone0473,S216/S220,Zoom98661669177. Its actual href is Google document
`1oIel8d4OmdhwsmR830rjSeZIqCuC-YercbZsEGKNu28`, not the guessed circuit wrapper.
PDF export is10pages and names JeremyI.Franker, revisedMay4,2026. The separately
acquired `division-62/` iframe also names Franker. Original row is preserved as
`division62-roster-row`, a labeled JSON derivative tied to the original response
bytes/time. No anonymous person, vacancy or current occupant inferred.

Current named profile `http://www.17th.flcourts.org/2726-2/?smid=18371` redirects
successfully and names Franker36,TiairaThomas,9548310608,WW11133/WW11162,
Zoom206892036. `https://www.17th.flcourts.org/division-36/` links publishedHTML
and printID `1W5NoAHvEJKhaLGWcXtmjucZUqpgdhXky` (23pages). July30,2026 source
contact table names Franker but header KevinP.Tynan/9548317704 and repeatedTynan
references remain. Division36 is FAMILY, not criminal. Source address row gives
courtroom11162 while chambers/profilegive11133; preserve the distinction.

Complete36published609-line text and62civil/shared/form text have been read.
Visual checks so far:62pages1,2,3,4,9,10;36pages1,9,10. All33PDFpage images rendered,
but rendering is not review. Newly collected family-emergency2019-9(3pages),
statusquo2019-15(7),linked2017mediationform(4),temporary2026-06(2),current2026-05
Amendment1mediation order/form and2026-33distribution retained. Their full material
scope review remains pending except2026-33text screening:36family classification,
September10issuance/September14effectiveness and express2026-10replacement.
This order does not name Franker or establish a personal transfer date.

No completed person receipt yet. `review/franker-in-progress.json` records exact
review scope, source-specific notes, remaining checks and source associations;
`review/franker36-links.json` retains extracted actual links for later agents.
Continue one person across both divisions; do not copy15minuteUMC from62into36's
5minuteUMC or combine email-thread, conferral, cancellation or order deadlines.
Required common/civil material and links should be reviewed; specialized family
merits/forms and criminal material stay proportionate to commercial-civil priority.

`review/save-division62-checkpoint.py` saved packet `draft/checkpoint-46.json`,
acknowledgment `review/history-capture-46.json`, capture4362
`f796b281989d29287deee32e9e34921dfc36b52f9ff6755b32eef9e42f645aba`.
Nine bounded citations validated,321 cumulative source entries,626 packetartifact
byte read-backs, semantic facts/exact replay and finalized reports unchanged.
`review/division62-context.json` verifies the source-association finding;
`review/franker-incomplete-context.json` confirms incomplete check and no accepted
person finding. Judge count remains39. ActiveFranker; next packet47orlatest after
full scoped review, person validation and read-back. County remains incomplete.

## Completed judge: Jeremy I. Franker — 36 and dated 62/SB

Current profile: `https://www.17th.flcourts.org/2726-2/?smid=18371`.
Current wrapper: `https://www.17th.flcourts.org/division-36/`; follow the actual
published Google iframe and linked print document recorded in the acquisition
manifest as `franker-36-document` and `franker-36-print`. July 30, 2026 revision.
Contact table/profile identify Franker and Tiaira Thomas, 954-831-0608,
`div36@17th.flcourts.org`, chambers WW11133, courtroom WW11162 and Zoom206892036.
Header names Kevin P. Tynan/7704; Address row prints Room11162. Preserve these
with their source fields rather than declaring a unique mailing destination.

The unnamed roster row's actual href and the `/division-62/` wrapper lead to a
May 4, 2026 Franker county civil62/criminalSB document. Preserve that date and
scope: Tiaira, 954-831-0473, div62/divsb, South Suite216/courtroom220,
3550 Hollywood Boulevard, Hollywood33021, Zoom98661669177. Do not use it to
identify the unnamed row's current occupant. The attached invocation form names
Franker but literally states Division61. The original remains unmodified.

Read `receipts/person-jeremy-i-franker.json` for 35 scoped checklist topics and
nine differences. All ten county PDF pages were visually checked. Family text
was read completely; visual checks covered pages1 and9–20. Family substantive
merits, criminalSB merits and training videos were not exhaustively reviewed.
`review/franker36-links.json` preserves actual destinations. The legacy e-orders
404 was reused from the earlier acquisition; no replacement instructions inferred.
A bounded two-query official-domain fee-form search returned no results; the
procedure describes a case-issued preliminary fee order, not an attached form.

Six newly reviewed shared sources are in `receipts/shared-civil-reviewed.json`:
2019-9 family emergency;2019-15 status quo with family asset/business-record
provisions; linked2017mediation template;2026-06temporary relief;2026-05Amendment1
mediation form;2026-33distribution (family36 classification/dates only).
Use the exact URLs in the acquisition manifest. The family AO index is
`https://www.17th.flcourts.org/unified-family-administrative-orders-2/`.
The old mediation template and current form differ in scheduling letters/phones,
attendance methods and ADA particulars. Save both; do not decide authority.
A modified status-quo order does not necessarily terminate the entire order;
unchanged portions remain effective, and the template ends on final judgment.
No case-specific blank form was treated as an executed order.

Capture4364 was followed by reviewed wording refinement4366; prior observations
remain in history. Latest packet `draft/checkpoint-48.json`, acknowledgment
`review/history-capture-48.json`:321 source entries,652 artifacts,268 nested
citations validated,19 shared reviews; replay, byte/fact read-back and unchanged
finalized reports verified. `review/franker-context.json` has exact-entity verified
status/current finding, no finalized baseline, review_required. Earlier
`franker-in-progress.json` is historical and points to this completed review.
Next select a remaining named judge; retain the county-level incomplete checks.

## Completed judges: Chris Brown, Melinda Brown, Deborah Carpenter-Toye

These three criminal-assignment records were researched and saved sequentially.
Each includes contacts/assignments/original procedure links and scoped shared
access/submission review. Criminal merits/pleas/diversion manuals were not
exhaustively analyzed. No civil assignment was inferred from an old header.

| Person | Official profile | Procedure entry | Contact and assignment | Save |
| --- | --- | --- | --- | --- |
| Chris Brown (procedure: Chris M. Brown) | `https://www.17th.flcourts.org/2726-2/?smid=18558` | `/division-mv-57-mxd/` | MV/MXD; Maria Prieto (procedure Maria E. Prieto),9548317690,maprieto@17th.flcourts.org,divmv@17th.flcourts.org;WW10137/WW10170;Zoom458523246 |4368,packet49;10topics,4conflicts |
| Melinda Brown (procedure: Melinda Kirsch Brown) | `https://www.17th.flcourts.org/2726-2/?smid=2754` | `/division-ma/` | MA;Stephanie Woodberry,9548317675,divma@17th.flcourts.org;WW5131/WW5165;Zoom373669451 |4370,packet50;12topics,2conflicts |
| Deborah Carpenter-Toye | `https://www.17th.flcourts.org/2726-2/?smid=2755` | `/division-mm/` | County Criminal Chairperson/MM;Anna Marie Perez,9548317039,aperez@17th.flcourts.org;WW6127/WW6175;Zoom224754993 |4372,packet51;11topics,1conflict |

All wrappers are on `https://www.17th.flcourts.org`. Follow their actual iframe
and print links; raw/text manifest keys are `brown-chris-*`, `brown-melinda-*`
and `carpenter-*`. Brown names and longer variants are one person each, not
separate roster entries. Standard courthouse street/city is201SE6thStreet,
FortLauderdale33301. Brown procedure address rows use courtroom rooms; their
normalized chambers locations combine profile room with street/city, without
certifying a mailing destination. Carpenter's street/city is cited from official
clerk West Building locations; do not borrow the clerk department's room.

Chris: current profile omits57 retained in procedure heading. Header phone1673
versus profile/assistant7690 preserved. Source HTML/tables reviewed; sole embedded
image is state seal, collected and visually checked. Browser wrapper returned
permission denied and was not bypassed; no rendered-page check claimed. No
individual revision date found. The split Clerk Website label links to the
public defender; retain originalhref/decoded target in`brown-chris-links.json`.
Do not substitute this for clerk-source research.

Melinda: ten-page PDF collected, shared sections reviewed, visual checks1,4–7.
No revision date or named assistant email found. Same mislabeled clerk anchor
preserved in`brown-melinda-links.json`, alongside a separate valid clerk-domain
link. Her3PMnext-day cutoff, physical copies of case law over15pages at least
one businessday before hearing, and emailed Word/PDForders differ from Chris's
noon/CMSoptions. Reusing a template does not authorize copying requirements.

Carpenter: all six individual PDF pages text/visually checked within shared scope.
All hearings viaJA; e-file notice emailed toASA/JA before docket appearance.
Remote-request motion must be filed AND ruled on5days before hearing. PDForder
submission; status continuance3businessdays, trial and coordinated-motion resets
7businessdays, intended authorities3businessdays. No divmm email guessed.
No current civil assignment or individualAIpolicy located in the checked source.

### Reusable interpreter source review and remaining county comparison

- `ao-2019-27`: original4pageorder, signedApril9,2019; shared access/evidence
  portions reviewed, page3visually checked. Spanish/Creole8317270at least2business
  days; other-language email at least7days. Original preserved.
- `ao-2026-11-currentpath`: original5pageorder, signedMarch27,2026; all text read,
  scoped sharedaccess/evidence review, visualpages2–3. Actual GeneralOrdersindex
  (`https://www.17th.flcourts.org/general-orders/`) links
  `https://www.17th.flcourts.org/wp-content/uploads/2026/04/2026-11-Gen-Court-Interpreters-Office.pdf`.
  Search result'sMarchpath returned404 and remains in acquisition as`ao-2026-11`.
  Order requires online interpreter request;Spanish/Creole2businessdays,others7days;
  late requests online PLUS8317290call. Expressly vacates2019-27Amendment2.
  Intermediate2024amendments surfaced but were not independently reviewed.
- Court employees/contractors do not translate offered evidence; offering party
  supplies English translation/transcript at its expense under both originals.
  Satellite/access and qualification conditions retained in shared receipt.
- `interpreter-request-form`: official`https://CMS.17th.flcourts.org/interpreter-request-form`
  returned200but text onlyCMSapp shell. Link/AOrequirement supported; no UI fields,
  rendering, successful submission or interpreter booking claimed.

Before county completion, associate2026-11with prior judge interpreter-source
statements without rewriting earlier receipts or selecting controlling authority.
Both orders are now reusable in`receipts/shared-civil-reviewed.json`. Other
unfinished county gates still apply.

Each of the three captures passed person/citation validation, exact replay,
artifact/fact read-back and unchanged finalized reports. Filtered contexts
`brown-chris-context.json`, `brown-melinda-context.json`, `carpenter-context.json`
show exact-entity verified current findings with no finalized countybaseline.
Latest packet51contains337source entries and637artifacts; earlier packet artifacts
remain in the database. Next PhoebeeFrancois/MD, all assignments together.

### Packet replay repair after the interpreter review

After adding shared interpreter reviews, packets49/50's shared-JSON working path
no longer matched their saved hashes. Database originals remained intact. The
pinned-run `review/freeze-replay-packets.py` recovered saved bytes by hash, wrote
hash-named artifacts, and created `checkpoint-49-frozen.json` through
`checkpoint-51-frozen.json` without editing the original packets or history.
All three replayed to the same capture IDs/sequences, with unchanged payloads,
no new captures and unchanged finalized reports. Use the frozen copies for replay.
`review/frozen-replay-results.json` records the verified paths and results.
Freeze subsequent saves before advancing; audit older packets before county
completion. This check covers49–51only, not every earlier checkpoint.

## Completed judges: Phoebee Francois, Kenneth A. Gottlieb, Ginger Lerner-Wren

These records were completed one at a time. Their actual official source paths
and scope distinctions are below; all acquisition metadata is in the pinned run.

### Phoebee Francois — MD

Profile `https://www.17th.flcourts.org/2726-2/?smid=2867` and wrapper
`https://www.17th.flcourts.org/division-md-2/`. Wrapper's actual print link has
leading whitespace; trim whitespace and retain documentID
`1HqExoplfN1lDp15NYo70NPuMVTSiy40-p8DYN80PjG8`, not a guessed alternate.
Keys`francois-bio`, `francois-wrapper`, `francois-document`, `francois-print`.
Four-page text/visual review covered contacts/shared procedure; extradition,
truancy, probation and criminal merits remained scope-screened only.

Profile names Grace Valentin,9548318503,WW5127/WW5160,Zoom735441388; division
email`divmd@17th.flcourts.org`. Procedure name is Phoebee R. Francois, one identity.
Literal revision`updated03/26` retained with month interpretation2026-03 and no
day/effective date invented. Other explicit requirements: e-file AND validate,
48hours to confirm offered date, Wednesday-AM remote/9AMcalendar call, prior
approval for5minute remote special motions, hardcopy evidentiary materials and
continuance requests2businessdays before hearing. Source tollfree8338535257was
visually checked and preserved without changing its prefix or making a test call.
Shared2026-11interpreter comparison retained; no individual AI rule inferred.
Capture4380,packet52:9topics,1conflict;36nested citations validated.

### Kenneth A. Gottlieb — MQ and county administrative role

Profile `https://www.17th.flcourts.org/2726-2/?smid=2800`; wrapper
`https://www.17th.flcourts.org/division-mq/`. Published iframe retained as
`gottlieb-document`; wrapper provides no print link. Full published text and DOM
table inspected; sole embedded image collected and visually identified as state
seal. No rendered-browser/PDF review claimed. No document revision date found.

Jennifer Swift,9548317567,`divmq@17th.flcourts.org`,WW6131/WW6160;
bodyWW06160is retained as a room-code formatting variant. Individual source
supplies chambers/street address. Profile states county administrative judge and
Zoom142715973only with approval/notice. Default physical appearance; Zoommotion
and underlying motion sent and ruled on5days before hearing. Evidentiary hard
copies2businessdays ahead are PREFERRED, not a mandatory rule.3PMnext-day cutoff;
agreed orders CMS or emailPDF; signed order andJAcancellation steps remain
separate. Preserve source sentence calling agreed motions`Agreed Order` alongside
its clearer order-section wording. Actual interpreter-form link matches newly
reviewed shared source; app-shell limitation remains. Capture4384,packet53:
9topics,1conflict;35nested citations validated.

### Ginger Lerner-Wren — MS and linked MI duties

Profile `https://www.17th.flcourts.org/2726-2/?smid=11866`; actual roster/profile
procedure link is Google document
`https://docs.google.com/document/d/1CLW6Jj81Dl323X8v6_fIeEUhNkDiOK-DqCL74XDfzXQ/edit?usp=sharing`.
Its PDF export is saved as`lerner-print`; no alternate wrapper guessed. Entire
17-page original preserved; general/shared pages1–7text/visually reviewed.
Pages8–17diversion history/clinical/program/referral matter not substantively
reviewed. Do not pursue external diversion manuals/videos/transport templates.

Profile assistantJoAnneCappiello; procedureJoAnneIovino with
`jiovino@17th.flcourts.org`. Preserve both; no same-person, separate-person or
transition-date finding. Phone9548317240, procedurefax9548316533, header office
email`jwren@17th.flcourts.org` (not identified as judge's direct address).
WW6133/WW6155,Zoom500897463; MSprofile plus MIcombined-procedure assignment.
Procedure supports remote arraignment/status/calendar-call; other remote requests
in writing to namedJA. Orders preferably bothWord/PDF, courtesy copies to
chambers/all opponents, motions identify recipients. Shared access, courtroom
rules, evidence marking and emergency channels preserved. No revision date or
current Cappiello-specific email inferred. Capture4388,packet54:9topics,3conflicts;
43nested citations validated.

All three have exact-entity verified current findings in `francois-context.json`,
`gottlieb-context.json`, `lerner-context.json`; no finalized countybaseline yet.
Packet54has347cumulative sources and657artifacts. Frozen copies52–54return their
original capture IDs/sequences; artifact hashes/facts and unchanged finalized
reports checked. Replay log now retains previous49–54results instead of replacing
the log each time; repeated54replay preserved all entries and created no capture.
Latest frozen packet:`draft/checkpoint-54-frozen.json`. Next Jill K. Levy, all
assignments together. County roster/clerk/material reviews and older binding audit
remain incomplete.

## October 16 — Levy, Evans and Merrigan

Completed separately and sequentially: Jill K. Levy/MP, Kal Evans/MJ and Edward H.
Merrigan Jr./FE/VF/MVC. Receipt filenames are `person-jill-k-levy.json`,
`person-kal-evans.json` and `person-edward-h-merrigan-jr.json` in the pinned
run's `receipts/`; packets55–57 and `review/history-capture-55.json` through57
record captures4394,4398,4402. Each save passed receipt/nested-citation validation,
artifact and semantic-fact read-back, identical replay, unchanged finalized
reports and entity-filtered context verification. None finalizes Broward.

| Judge | Profile | Official procedure entry | Scope/distinctions |
| --- | --- | --- | --- |
| Jill K. Levy | `http://www.17th.flcourts.org/2726-2/?smid=2819` | `https://www.17th.flcourts.org/division-mp/` | Isabel Garcia/Isabel G. Garcia;7302;WW6125/WW6170;divmp. Evidentiary hardcopy2businessdays and following Otherwise CMS sentence retained separately. Cancellation requires approval before notice. Interpreter phone/email versus2026-11 comparison recorded. |
| Kal Evans | `http://www.17th.flcourts.org/2726-2/?smid=2787` | `https://www.17th.flcourts.org/division-mj/` | Emily Bates;7783;WW5125/WW5170;divmj. Header5170 is courtroom, not chambers. FridayZoom special settings,48hours request,4businessdays hardcopy. Overlapping continuance/pretrial timing, malformed cancellation, older ADA/interpreter references recorded without resolution. |
| Edward H. Merrigan Jr. | `http://www.17th.flcourts.org/2726-2/?smid=2825` | `https://www.17th.flcourts.org/division-fe/` | Marlene Henderson;7671;NW6910/NW6870;Divfe. FE/VF/MVC one person. Veterans Monday1:30PM; program eligibility/plea link outside exhaustive review. Courtesy copies means entered orders. Exhibit timing approximately5days, no business-day qualifier inferred. |

Each wrapper embeds an actual published Google document and offers no print link.
Follow its iframe rather than guessing an export ID. Full originals/text, contact
header tables and one seal image per source retained/inspected. No rendered-browser
or PDF check claimed. Exact published URLs are in acquisition.json; actual href
inventories are review/levy-links.json, evans-links.json and merrigan-links.json.
Merrigan's biography link sits inside the containing staff card on judiciary page3,
not on the name heading itself. Walk up to that card and use its Biography href;
searching only anchor display text for the surname misses it. Page4 was acquired
from actual pagination but did not supply the biography. Do not reacquire it merely
to repeat that search.

Shared reviews reuse ADA2026-20 and, for Levy/Evans, interpreter2026-11. Criminal
forms are links-only unless civil/shared relevance warrants content review.
Levy/Evans/Merrigan have10/11/10checklist topics and1/5/0documented conflicts.
These counts reflect scoped review, not a determination that no other legal
conflict exists. No individual revision date was located in their checked sources.

Acquisition warning repaired: extensionless seal URLs can return PNG/JPEG bytes.
The run helper now checks PNG/JPEG/GIF/WebP signatures before HTML parsing and
stores images without text_sha256/text_path. Evans's initial binary-to-HTML decode
warning was investigated; the spurious extraction is excluded from citations and
packet inventory. Original bytes remain intact. `review/check-acquisition-images.py`
passed isolated PNG/JPEG byte preservation and unchanged HTML/PDF extraction checks;
GIF/WebP paths not exercised. Merrigan live JPEG acquisition followed the repaired
path without a decoder warning. No tests wrote to the shared history database.

Next: reconcile remaining county identities, then continue unreviewed circuit
judges with civil/probate/shared priorities. All90 named roster entries still
require final identity/assignment accounting;49completed records are not full
coverage. Reuse frozen packets49–57 for replay; older packet bindings need audit.

## October 16 — Gillespie and shared probate evidence

Kenneth L. Gillespie/62J completed in capture4406, packet58, receipt
`receipts/person-kenneth-l-gillespie.json`.50judges now completed.389acquisition
entries and753artifacts in the packet;232nested citations validated, semantic
facts/artifacts read back, identical replay/finalized preservation verified.
`review/gillespie-context.json` shows entity verified, review_required and no
finalized county baseline. Frozen58 created immediately; frozen57 replays after
the shared registry changed without creating a capture. Do not replay mutable
historical packets when frozen equivalents are available.

Discovery: judiciary page2 staff-card Biography href
`http://www.17th.flcourts.org/2726-2/?smid=2799`; wrapper
`https://www.17th.flcourts.org/division-62j-2/` embeds published Google document.
Actual iframe URL retained under `gillespie-document` in acquisition.json.
No print link, table or image in individual procedure. Text reviewed in full;
no rendered-browser/PDF layout claim. It says Updated2/12/2025, not effective.
Profile assistant Taneshia Barbary-Snell versus procedure Taneshia Barbary;
Tbarbary@17th.flcourts.org, div62j@17th.flcourts.org,954-831-7565,
WW14133/WW14160, Zoom713315119. Handbook malformed WW1413312125 preserved.

Shared entry: `https://www.17th.flcourts.org/probate-and-guardianship/`.
Actual href inventories: review/probate-hub-links.json and
review/probate-orders-links.json; material orders from
`https://www.17th.flcourts.org/probate-administrative-orders-2/`.
These list both procedural orders and routine/clinical/training subjects; screen
by civil/shared relevance rather than exhaustively following every link.
Shared reviews now include the22-page October2023 local handbook, order-submission
clarification, AO2021-49 Amendment1,2022-45 Amendment1,2023-42,2019-94,
IV-03-A-27,2025-23 with attachments, checklist instructions, all10mandatory
petition checklists, heirs/criminal-history affidavits,2015expenditure certification
memo/order and special-needs/pooled-trust memo. Reused LocalRule10A,
AO2021-50/51/52emergency,2022-37evidence Amendment1 and2026-20ADA.
Review scope and visual page lists are explicit in receipts/shared-civil-reviewed.json.
Text review does not imply every PDF page was visually inspected.

Search `site:17th.flcourts.org probate "qualified trust beneficiaries" memorandum`
did not locate the discharge checklist's request-only memo. It did locate a
second formal-testate checklist: official hub links
`/wp-content/uploads/2017/08/Petition.for_.Formal.Administration.of_.Testate.Estate.pdf`
(revised9/9/2016), while search found
`/wp-content/uploads/2017/08/Checklist.for_.Petition.for_.Formal.Administration.of_.Testate.Estate.pdf`.
Both originals saved. Page2qualified-beneficiary instructions differ; pages3–4
text identical. No version selected as controlling; no current date inferred
from search publication labels or upload paths.

Nine discrepancies recorded: malformed chambers; order-attachment/ex-parte
wording; virtual evidence timing; old calendar/named-judge references; ancillary
certification petition label; alternate formal-testate forms; summary estate
less-than versus not-exceeding value wording; homestead timing; expenditure
memo versus attached emergency exception. Primary statements remain with their
original documents, dates, retrieval times and URLs. No conflict-resolution task
or extra publication gate created.

Workflow findings: an affidavit about criminal history can be a required civil
probate filing; decide relevance by use, not title keywords. Keep checkbox OR
branches, footnotes, signature-page requirements and missing-item certification
separate. File-presentation instructions differ from substantive eligibility.
Mandatory checklists may be revised without amendment to their governing order;
future updates must fetch the actual current form hrefs as well as the order.

Reconciliation artifact: review/roster-reconciliation-49.json. Token-reordered
exact names matched51roster rows to49completed people before Gillespie. This
is a navigation aid, not a blanket identity-merging algorithm. Visually inspected
October chart places Alspector/Kaplan in Unified Family/Domestic Violence;
division57 alone did not classify either as county judge.31canonical county
records versus chart32 remains an accounting discrepancy; unnamed62/SB not
inferred to be vacancy. Remaining roster includes Christopher Pole/11, which
requires individual source review rather than merging with another11entry.

Next: DePrimo61J individually, then Lopane60J. Reuse probate shared sources.
Remaining judges, clerk and material county review still precede county completion.

## October 16 — DePrimo and Lopane

Completed sequentially, each saved and verified before next person:

| Judge | Profile and procedure entry | Capture and receipt |
| --- | --- | --- |
| Natasha DePrimo,61J | `https://www.17th.flcourts.org/2726-2/?smid=8278`; official link to Google document `1aPCyJqkCWqKvV-g74ZRKbL8dKQbGuy4K3Q0MZTd-qWk` |4411, packet59, `receipts/person-natasha-deprimo.json` |
| Nicholas Lopane,60J | `https://www.17th.flcourts.org/2726-2/?smid=2820`; `https://www.17th.flcourts.org/division-60j/` |4415, packet60, `receipts/person-nicholas-lopane.json` |

DePrimo Google edit page returned only interface text. Public PDF export using
that exact official-linked ID returned the nine-page procedure; all pages read
and visually checked. Do not cite the interface shell as procedural evidence.
Lisa Tucker,954-831-5614,div61j@17th.flcourts.org,WW14127/WW14170.
No named assistant email or individual revision date found. Under-one-hour Zoom
and one-hour-or-longer physical settings; attorney telephone permission;
three failed coordination attempts permit only non-evidentiary unilateral sets;
two-hour-or-longer evidentiary pretrial requirement; five/ten-day list/expert
rules; agreement verification, rejection/resubmission, continuances and physical
fee rehearings recorded. Seven source discrepancies include older rooms,
email/upload instructions, evidence timing, AI reference/vacating order,
county emergency-order number, old checklist and telephone fallback wording.

Lopane wrapper offers published iframe and actual print/edit link for document
`1wF-EulRG70xQnBrxOSz2AiRl2rZuEqFsVYVUcN-0XrA`. Same-ID PDF export retained;
all seven pages read/visually checked. Published/PDF text comparison found eight
spacing/numbering differences only; review/lopane-published-pdf-comparison.json
retains the differences. Profile Denae Mc Neal and procedure Denae McNeal versus
probate landing-page Luisa Prieto are distinct source statements.954-831-7608,
div60j@17th.flcourts.org,WW14129/WW14155. Header adds judge middle initialR.
Individual clerk label5645 differs from other probate procedure7154 and handbook
closed-file5645 role; no global clerk number replaced on this basis.

Lopane’s <=30minute CMS versus >30minute JA setting directions and separate
>45minute five-WORKING-day supporting deadline retained. Zoom evidence binder
is at least five days (not labeled working days), one bookmarked/paginated PDF.
Witness ID redaction/filing references, prefiled versus custodial exhibit wording,
Word orders through CMS after hearing versus shared before-hearing email,
physical emergency/rehearing requirements and old agreed-order language retained.
No witness-list or standalone continuance interval borrowed from another judge.

DePrimo links the older2017Checklist.Instructions.pdf (nine petitions) and the
live `/memorandum-mandatory-checklists/` page (ten, including real-property sale).
Actual hub href inventories retained. Its ancillary2017PDF differs in bytes from
main probate hub2025path but all four extracted page texts match; source URLs and
raw hashes stay separate. All other material mandatory-checklist URLs reused.
Lopane’s `/probate-and-guardianship-smart-forms-home-page/` includes four-line and
case-number signature-page rule, manual calculations, local saving and PDF/A.
Material previously reviewed forms reused; not every routine form body reviewed.

Lopane’s EleventhCircuit `/Probate-Smart-Forms` link is retained as a preferred-form
resource. Landing-page text and links reviewed; its AO22-02 directions are labeled
Miami-Dade-specific and not imported into Broward requirements. No Miami-Dade
county baseline started. Supporting-documents YouTube link and three embedded
Broward evidence-presentation videos inventoried, not watched; no operational
or additional procedural claim made from their titles.

DePrimo/Lopane records have17/16topics, seven discrepancies each,227/221nested
citation validations. Exact saves/replays, artifact/fact read-backs, unchanged
finalized reports and entity-filtered contexts verified. Frozen58/59/60 rechecked
against every artifact hash after later shared registry changes; all replayed to
original captures without a new capture. `review/probate-three-replay-check.json`
records that check. Current county still has no finalized comparison baseline.

Next: Christopher Pole/11, a remaining named official roster entry requiring
individual source review. Chart/roster differences remain documented, not
resolved by guessing.52records is not full county coverage. County clerk and
material procedure reconciliation remain, with older packet-binding audit.


## October 16 — Senior Judge Christopher Pole and historical packet bindings

Own profile: `https://www.17th.flcourts.org/2726-2/?smid=2793`.
The judiciary and dedicated `/09-foreclosure-division/` page link Google document
`12FXPTLrl7E7yOjtAWQ84o2JS3iMIWFc3MaVPXsss2Qg`. Its edit response is an interface
shell; the same-ID public PDF export yielded 13 pages, all read and visually
inspected. Manifest keys `pole-bio`, `pole-document`, `pole-procedure-pdf`,
`pole-pdf-links`, `foreclosure-hub`, `civil-division-hub` preserve originals,
actual retrieval times and independently extracted PDF link destinations.

Record `receipts/person-christopher-pole.json`, entity
`broward-senior-christopher-pole`: phone9548316072, WW3121/WW4150, Zoom91496393836,
shared foreclosure/div11 emails. Street address uses the shared courthouse header
and profile room with that synthesis explicitly labeled. NW4910 is the unit's
mailing location in the procedure, not Pole's personal chambers. Melinda Fleming
is identified for Garcia-Wood, not copied to Pole. Searches and missing-field
states are in `review/pole-discovery.json`. Senior trial assignment is explicit;
do not use it as evidence for filling a regular-seat roster discrepancy.

Pole-specific trials: Monday–Wednesday9–5, lunch12–1, day-to-day continuation;
remote or live participation designated in witness lists. Continuance motion
heard before trial, not submitted as an agreed order. The separate source also
requires a reporter and identity/entitlement documents for surplus disbursement
hearings, with physical attendance unless permitted otherwise. Distinguish its
shared 30-minute Zoom threshold and9–10:15UMC from Garcia-Wood's separately linked
15-minute/9–9:45document. Preserve differences in CMC rooms, rehearing delivery,
surplus exceptions and disclosures; neither document is deemed to supersede the
other. Reused shared foreclosure/remote-evidence/emergency orders retain original
review scopes and explicit supersession/vacatur statements.

Page2 Pole visible malformed Zoom URL differs from its correct actual annotation.
Garcia-Wood's block has different displayed/target/one-tap meeting IDs. Record
those independently and never assign another judge's meeting to Pole. The linked
procedure's final unnamed disclosure is retained as a document statement; the
multi-judge header does not establish that it applies to both judges. No separate
standing-recusal instrument is claimed collected. Optional training video not
watched. The registration label has no annotation; the previously located public
CMS pro-se agreement is a separate matching resource, with its Workbench discovery
path retained. No forms, IDs, hearings or emails submitted.

Capture4422 (`2c7bfbf20872d4b1155d845e39fceda0fabf1be7816b63a5bee235a643ee5129`)
passed person validation,287nested citation validations,769artifact and semantic
fact read-backs, identical replay and unchanged finalized-report checks. It has
24checklist topics,14discrepancies and20associated shared reviews. Entity context
shows the verified check/current finding, unknown finalized baseline and
`review_required`. County remains incomplete.

The frozen replay utility now accepts the original zero-padded checkpoint01–09
filenames without renaming them. All61 packets were successfully replayed using
hash-bound copies; payloads, run IDs, scopes and historical capture identities
remain unchanged. Original blobs were read from the database, hash-verified and
saved to new local paths. No captures or finalized reports were added by replay.
Evidence: `review/frozen-replay-results.json`, `review/older-frozen-replay-cli.json`,
and `draft/checkpoint-<n>-frozen.json`. The former older-binding audit is complete;
source completeness and legal review are separate. Next judge Pascale Achille/33.


## October 16 — Pascale Achille, Division33

Saved judiciary card links profile
`http://www.17th.flcourts.org/2726-2/?smid=21193`; own procedure wrapper
`https://www.17th.flcourts.org/division-33/` embeds published Google document
`2PACX-1vR3ks1-1lN15bFjogwei1zlIuOrlULVIUQuALbJFlnyo-uetnWt2eSOblWJ_FmpoCye_ZhZK9AR18LN`.
Manifest keys `achille-bio`, `achille-wrapper`, `achille-document`, `achille-links`
and `achille-header-image` preserve actual source/derived evidence. Full text read,
including all24numbered sections and RUCD affidavit. Header/contact tables checked
in DOM; embedded image is state seal, visually checked. No browser rendering or
individual PDF export claimed. Updated date is2026-04-17, not universal effective date.

Record `receipts/person-pascale-achille.json`: Dyana Del Ponte,9548311648,
shareddiv33email,WW11129/WW11156,201SE6thStreetFortLauderdale33301,
Zoom562237373. Hours8:30–4,lunch12–1:30. Pro-se case management8532/ufchelp.
Judge name contains mailto pachille, saved with express division-communication
restriction; not permission for direct/exparte contact. Named assistant email/fax
not located after recorded searches. Do not infer them from the judge-name link.

Individual requirements include oral conferral, five-minute UMC restrictions,
JA special-setting details, 24-hour notice service, five-business-day evidentiary
lists, paper binder/highlighted authorities, special trial/cancellation/order routes
and loading-dock use for over5boxes. Preserve literal supporting-upload wording
“at least two business days after the hearing has been set”; do not silently turn
it into before-hearing or within-two-days. Conflicts include unilateral setting
versus all-party confirmation, emailed authorities versus paper-only directions,
pro-se communication routes, order channels, days/business-days, trial memorandum
versus joint stipulation,58-35heading versus58-33body, and old holiday destination.

Division33 expressly declines the shared2019-15status-quo template for the stated
case cohort. Both original order and individual statement remain. Latest facts
include `shared_source_applicability` with `expressly_not_used_for_specified_cases`,
case filing start2025-01-01, individual policy effective2025-03-01 and earlier-case
applicability not determined. Do not reuse the order's asset/records-preservation
requirements as automatic Division33 duties or infer circuit-wide repeal.

The saved UnifiedFamily AdministrativeOrders index actually links
`https://www.17th.flcourts.org/wp-content/uploads/2020/12/2020-91-UFC_amended.pdf`.
All9pages read/visually checked: First Amended order dated2020-12-07,nunc pro tunc
2020-11-19,effective2021-01-01; contested family trials with enumerated exclusions.
Attached template has45day witness/exhibit lists,30day rebuttal,15day discovery,
10day exhibits/log,7day impasse,5day joint stipulation and5calendar-day memoranda,
with stated exceptions/ratification requirements. Do not turn blank template into
an entered case order. Page8 image-only exhibit log is labeled manual transcription
in `review/family-trial-visual.txt`; raw PDF and rendered pages retained. Checklist
says premark1day before; sectionV says before hearing/trial. Preserve both.

Actual holiday link leads to2025memo dated2024-07-31; collected/read/visually
checked, with current2026memo reused separately. Actual2018Local10Alink returned404;
failed original retained without supporting citation. Current official indexed
rule reused, not claimed byte-identical to unavailable historical link. Optional
CMS/Zoom technical-help links retained but not exhaustively reviewed. Shared
family emergency/temporary/mediation/distribution material reused with review
scope intact. Child/family merits screened, not expanded into a separate project.

Initial capture4522 (`51a6cfd8a63dca67fb80786dcd95edd4efe562f665644279b64a37556623aeb3`)
preserved initial reviewed record. Capture4526
(`bab6617d0e1ae390e9a96ffd296e96291e12e679e57eccaf0d4cabfd55b6e550`) adds explicit
shared-source applicability to semantic comparison facts; original retained.
25topics,12discrepancies,121nested citations,783artifacts,418source entries and
13associated shared reviews. Person validation, artifact/fact read-back, replay,
entity-context verification and finalized-report preservation passed. All63packets
frozen/replayed; county remains incomplete. Next Lauren M. Alperstein/35.


## October16 — Lauren M. Alperstein, Division35

Official judiciary card links profile
`http://www.17th.flcourts.org/2726-2/?smid=16299` and wrapper
`https://www.17th.flcourts.org/division-35/`. Wrapper iframe published ID
`2PACX-1vTyrasW-61xc0gdaVZvqs7LLWmPx4BAWgRUcG3iMgqaY5AzCBXocCNIWO1FS0LjLQqIPlLhLifWNOlF`
differs from actual print/edit document ID
`1mSfiyWQBUiYSLxvqP4arT_1sC9kMqqVMWIkyfx6QiwA`; export that actual ID to PDF.
Manifest keys `alperstein-bio`, `alperstein-wrapper`, `alperstein-document`,
`alperstein-print-pdf`, `alperstein-ai-original-linked` preserve originals.
All25HTML sections/embedded affidavit read, all23PDF pages visually inspected;
92HTML/PDF token-difference groups inspected as formatting only. Header images
are two seals. Published HTML external body URLs are printed text; anchors are
internal contents fragments. Do not invent a Court Holidays destination.

Receipt `receipts/person-lauren-m-alperstein.json` records Maria Torres Gutierrez,
9548317779,shareddiv35email,WW11125/WW11168,201SE6thStreetFortLauderdale33301,
weekdays8:30–4/lunch12–1:30. Body says Ms.Morrison repeatedly; preserve discrepancy.
Meeting/link605014865 versus one-tap598494885 is another source discrepancy.
No named assistant email/separate phone/fax or direct judge email located in checked
sources and targeted searches. Search-result testtitan mirror not adopted as current
official contact. Month-only “October2026” is not October1 or an effective date.

Own instructions require CMS support once hearing appears, not Achille33's
two-business-day language; no unilateral two-day setting permission copied.
JA special sets require all-party confirmation and24hour notice; five-business-day
evidence lists, paper binder/authority rules, individual trial/order routes and
scope-specific mode restrictions retained. Division35 expressly does not use
2019-15 status-quo template for cases filed2025-01-01onward under policy effective
2025-03-01. Explicit association saved in semantic facts, no circuit-wide repeal.

Printed original AI URL successfully retrieved:
`https://www.17th.flcourts.org/wp-content/uploads/2026/01/AO2026-03-GEN-Use-of-AI-in-Court-Filings.pdf`.
All3pages read/visually inspected. Signed2026-01-26, no separate effective clause
located. Retain original, prior reviewed Amendments1/2,June vacatur and individual
October disclosure/certification statement. Conflict recorded without controlling
authority conclusion; underlying Supreme Court references not independently
reviewed in this task. Existing shared family trial/mediation/emergency/temporary,
Local10A,ADA and2026holiday evidence reused with original scope/timestamps.

Capture4530 (`bd47da0840f2fc85a57f8a9f63683f9bf45fb7a5e6dd11e0e374cfb3172b56d5`),
packet64:25topics,12discrepancies,181nested citations,423source entries,812artifacts,
16shared reviews. Person/citation validators, exact original/fact read-back,
frozen replay and entity context passed; finalized reports unchanged. County remains
incomplete. Review artifacts `alperstein-discovery.json`, `alperstein-links.json`,
`alperstein-html-pdf-diff.json`, `alperstein-visual-review.json`, search output and
context JSON are under run/review. No browser UI or live CMS/Zoom action claimed.
Next Susan L. Alspector/FV57 individually.

## October 16 — Susan L. Alspector, FV/57

The official judiciary card links profile
`http://www.17th.flcourts.org/2726-2/?smid=8351` and
`https://www.17th.flcourts.org/division-fv/`. The wrapper has no print/edit link.
Its iframe published ID is
`2PACX-1vSrvUsqkUfnhk0lCvWZDU89tGjBaA2LkgC2xRBTQ-Som3QsoziBFQJDBsbpkPRwSXW8R_5jg53uYmXV`.
Manifest keys: `alspector-bio`, `alspector-wrapper`, `alspector-document`,
`alspector-dv-hub`, `alspector-header-image-1/2`, `alspector-links`,
`alspector-qr-decoded`, and `alspector-courtesy-linked`.

The entire 17,302-character procedure was read and screened, three DOM tables
checked, and both images viewed. It states updated August 23, 2026 and identifies
Circuit Criminal FV. Shared access, scheduling, orders and evidence were reviewed;
criminal plea/diversion merits were not expanded. The official domestic-violence
hub's own card links the same FV document. Targeted civil-injunction and Division57
searches located no separate individual civil procedure. Do not infer all hub
civil rules belong to Alspector or apply FV criminal deadlines to commercial cases.

Contacts: Stacy McMenemy, 954-831-7566, shared divfv@17th.flcourts.org, chambers
NW6820, courtroom NW6900, 201 S.E. 6th Street, Fort Lauderdale, FL 33301. Named
in-court clerk Claudette Ryner is not identified as elected Clerk of Court; deputy
is Sal Greco. Interpreter-office phone7290/email/fax7279 remains separate from
chambers contact. Named assistant email, separate phone, chambers fax and hours
were not located in checked sources/searches. Historical2010 roster hits were not
adopted as current contacts.

Profile/visible Zoom ID328337467 differs from actual anchor and QR458523246.
The QR was decoded offline using Apple Vision; original image hash verified,
destination not opened. Seal negative case returned no QR; missing-file exit1,
missing-argument exit2. Original helper compiled without diagnostics. The reusable version
`scripts/decode_source_qr.swift` now decodes the exact bytes it hashes; all four
checks passed again in `review/qr-helper-validation.json`. Original decoder and
output remain in packet65. Decoder output is derived evidence, not corrected
source text. Clerk label reads browardclerk.org but actual anchor points to
browarddefender.org; preserve the discrepancy.

All hearings requested by email to JA, not CMS scheduling. Starting2025-10-01,
agreed orders may use CMS with motion/opponent agreement; other orders by email,
oral-ruling orders in Word/PDF, two-working-day follow-up. These are separate
feature states. Physical default/authorized Zoom requirements, special sets of
15minutes or longer with witness counts, notice/conferral, exhibit premarking and
scoped interpreter instructions recorded. No general civil schedule inferred.
Missing CANCELLATIONS cross-reference recorded; actual email-JA instruction
retained. Individual strict-professionalism wording remains alongside aspirational
shared standards and different four/five-business-day notice versions without
selecting controlling authority.

Actual2017 I-94-o-1 link returned404; failed response retained without supporting
citation. Official indexed1994 order/standards and Version1.4 previously reviewed
and reused, not claimed byte-identical to failed URL. Bar handbook link and criminal
emergency-alternate order reference retained but not exhaustively reviewed.
No PDF export or browser UI check claimed.

Capture4534 (`eb2ed247b83c3cbb555b977c428fd921ca9e26c2ef25cb02970ff29a74adfdb1`),
packet65:12 topics,4 discrepancies,63 nested citations,432 source entries,
800 artifacts,4 shared reviews. Person/citation validators, original/fact read-back,
frozen replay and entity context passed; finalized reports unchanged. County
incomplete; next Arthmann/38. Receipt `receipts/person-susan-l-alspector.json`;
discovery/link/QR/search/check artifacts under `review/alspector-*`. Future agents
should inspect actual targets and reuse originals with their specific scope.

## October 16 — David J. Arthmann, Division38

Official judiciary card links profile
`http://www.17th.flcourts.org/2726-2/?smid=15117` and
`https://www.17th.flcourts.org/division-38/`. Published iframe and actual print/edit
link share document ID `1BhBPZVh8hFifL2bJinB6al5QUhQJQeUloMvyA8hGrWM`.
Manifest keys `arthmann-bio`, `arthmann-wrapper`, `arthmann-document`,
`arthmann-print-pdf`, and `arthmann-links` retain originals and link/table inventory.
Entire61,932-character HTML read in bounded overlapping chunks; all24 physical
PDF pages read and visually checked, including RUCD affidavit and header seal.
Two contact/header tables checked. Contents-page numbering is stale; use physical
PDF page pinpoints. No browser UI or automated textual-equivalence claim.

Profile names Stephanie Lee; individual header names Stephanie A. Lee. Shared
954-831-7708/div38@17th.flcourts.org, chambersWW11139, 201 Southeast6th Street,
Fort Lauderdale, FL33301. Hours8:30–5, lunch12–1:30. Profile/header courtroom11166
conflicts with location sectionWW11-168. One competing-order paragraph and mailto
specify Div40; header and later redline provision specify Div38. Both retained,
without selecting a controlling room/address. Named assistant email, separate
phone, fax and direct judge email not located in checked sources/searches.

Revision July6,2026; separate policies state physical DV proceedings from
March10,2025 and conferral/discovery changes fromOctober31,2025. Division38
expressly adopts2019-15 status-quo procedures. `shared_source_applicability`
preserves adoption and dissolution/paternity scope, with no invented adoption
date. Do not copy Division33/35 non-use into this judge's record.

Twenty-six topics cover communications, conferral, UMC/special sets, appearance,
materials/evidence, emergencies, trial/continuance, orders, counsel changes,
mediation/referrals, reporters/interpreters, rehearing and family-specific forms.
Fifteen `deadline_rules` entries preserve subject, trigger, unit, literal wording
and exceptions. Emergency orders are two business days in one section and two
days in another. Special-set/trial orders are two weeks, DV orders seven days,
GAL orders five days. General courtesy materials differ from exhibit exchange and
CMS courtesy exhibits. Individual stipulation says “within five business days
prior”; shared template uses five days. No due-date arithmetic or harmonization.

Other recorded differences include unilateral setting versus confirmation,
automatic emergency notice versus required email, disputed-order CMS/email routes,
temporary relief duration scope, trial-setting route, CMC continuance wording,
pro-se communication routes and interpreter “certified court reporter” wording.
Financial-affidavit paragraph leaves exactly$50,000 unspecified; no inferred fix.
Repeated withdrawal/referral blocks summarized once with both source locations.
Family merits and referenced cases/statutes screened without exhaustive analysis.

Actual legacy2011-53 electronic-filing URL returned404. Official search found
`https://www.17th.flcourts.org/wp-content/uploads/2017/08/2011-53-UFC.pdf`.
All three pages read/visually checked: signed November12,2013, nunc pro tunc
October28,2011, with immediate-effect wording. Initial family portal scope,
original-document retention,24-hour acceptance/rejection and possible technical
failure relief recorded as historical source statements. No blanket current-law
claim or byte identity to missing legacy URL. Separate date fields survive in
shared-rule comparison facts. Manifest keys `arthmann-efiling-2011` and
`arthmann-efiling-official-copy` distinguish failure and recovery.

Actual2018Local10A link also404; previously reviewed official indexed rule reused.
Linked `court-closures-2/` page actually points to2025memo; retained alongside
reviewed2026memo. Actual links preserved in `arthmann-links.json`; optional videos,
general forms/help pages not all substantively reviewed. Older assignment order
lists a different Division38 occupant; current profile/procedure support Arthmann,
while county roster reconciliation remains pending. No other judge researched
out of sequence.

Capture4538 (`3e4fbc9679d744e3f14e1a0fb7821064ab0a2d0453f0a96d39a217ab7df81af3`),
packet66:26 topics,15 timing entries,14 discrepancies,184 nested citations,
441 acquisition entries,840 artifacts and12 shared reviews. Person/citation
validation, byte/fact read-back, exact frozen replay and entity context verified;
finalized reports unchanged. Receipt `receipts/person-david-j-arthmann.json`;
discovery, visual review, links, search outputs and context under `review/arthmann-*`.
Next Tim Bailey, individually. County remains incomplete.

## October 16 — Tim Bailey, Division FH

Completed current contact and scoped procedure review in capture4542, packet67.
Start at judiciary → Tim Bailey → Biography (`2726-2/?smid=3804`) and
Division Procedures (`division-fh/`). The latter embeds the published Google
document recorded as `bailey-document` in `review/acquisition.json`; preserve
the exact iframe URL. `bailey-criminal-hub` independently identifies FH. Current
JA is Nichole Lunsford, phone954-831-7821, shared divfh@17th.flcourts.org;
chambers NW7910/courtroom NW7900,201S.E.6thStreet,FortLauderdale33301.

Full current text screened;12shared-procedure topics and4timing rules saved.
Case-law/courtesy copies two days before hearing; interpreter requests three
days or seven for languages other than Spanish/Haitian Creole; equipment request
at least24hours before appearance. Days are unspecified, not inferred business
days. All hearings physical absent permission for Zoom. Exhibit-numbering clauses
are inconsistent and retained without choosing a rule. Criminal merits not
expanded, two plea-form links retained without fetching/reviewing their forms.

Search also returns `wp-content/uploads/2017/08/div41procedures.pdf`: all3pages
collected, page1 identity/date/header inspected and page1 visually checked.
It expressly states updated/effective2013-01-14 and names Sheena Bergeron/905B.
Those are historical assignment/contact facts, not current FH values. No present
civil duty inferred. Current document has no author-stated revision/effective
date; automatic Google refresh wording and search age metadata are not dates.

Read `receipts/person-tim-bailey.json`, `review/bailey-discovery.json` and
`review/bailey-links.json`. Exactly822artifact bytes/facts read back;44nested
citations validated; person validator, identical save and frozen replay passed.
Use `draft/checkpoint-67-frozen.json` for replay, never rerun the mutable save body.
`review/bailey-context.json` verifies current/historical separation and timing
units. `review/finish-bailey.py` asserts those facts and updates the handoff.
No final report advanced. Next Bernard I. Bober/FW; county work remains incomplete.

## October 16 — Bernard I. Bober, Division FW

Completed contact/shared procedure review in capture4546, packet68. Navigate
judiciary → Bernard I. Bober → Biography (`2726-2/?smid=2751`) and Division
Procedures (`division-fw/`). Save the exact published Google iframe recorded as
`bober-document` in `review/acquisition.json`. The reused criminal hub and
assignment order also identify FW. Full 11,731-character procedure screened;
12 shared-procedure topics, 3 timing rules and 1 link discrepancy recorded.

Suzanne Tracy's named email `stracy@17th.flcourts.org` is plain visible text beneath
her name, not a mailto anchor. Shared division email `divfw@17th.flcourts.org` and
954-831-0661 remain separately attributed. Chambers NW5910, courtroom NW5900 and
document drop-off reception NW5865 are distinct. Clerk felony telephone is
attorneys-only; in-court clerk is Unassigned. Clerk website label opens the public
defender website; original label and destination preserved without correction.

All hearings physical absent permission. Zoom request48hours in advance, usually
granted for non-evidentiary matters under30minutes; still discretionary. Interpreter
three-day/seven-day clauses retain unspecified-day units, language exceptions and
literal typo “at leave seven (7) days.” No Bailey courtesy-copy or equipment
deadline imported. Cancellation requires JA contact plus notice; agreed order
alone does not cancel the reserved hearing. Criminal merits and both linked plea
forms not expanded. Sole embedded image is a viewed Florida seal.

Read `receipts/person-bernard-i-bober.json`, `review/bober-discovery.json` and
`review/bober-links.json`. Named-email discovery must include visible text as well
as anchors. Original/fact read-back verified 830 artifacts and 46 nested citations;
person validator, identical save, frozen replay and entity-context checks passed.
Use `draft/checkpoint-68-frozen.json` for replay, not the mutable save body.
`review/bober-context.json` and `review/finish-bober.py` verify contact roles,
locations, timing units, typo and source mismatch. No final report advanced.
Next Hope Tieman Bristol; county remains incomplete.

## October 16 — Hope Tieman Bristol, combined Unified Family divisions

Completed contact/individual civil-shared procedure review in capture4550,
packet69. Navigate judiciary → Hope Tieman Bristol → Biography
(`2726-2/?smid=2753`) and Division Procedures (`division-js-29-39/`). Save the
exact Google iframe recorded as `bristol-document` in acquisition.json. Current
profile lists JS/39/JG/JF/29/JE. Assignment order page3 separates dependency,
family29 and delinquency JE/JF/JG, with JE labeled Drug Court. Criminal/diversion
merits not expanded; common official procedure link retained.

Nadine Turner,954-831-7882,plain-text NTurner@17th.flcourts.org in COMMUNICATION
section; chambers WW9135, courtroom WW9155. All9,206characters and five footnotes
read; one contact table, one portal target and one seal image checked. No print
link, PDF export or browser UI claim. Fifteen checklist topics and two timing
rules preserve filing two business days versus email two unspecified days.
Agreed goal-date extension expressly does not require an accompanying motion.
Hearing mode follows notice; magistrate referral names Lucy Miller. No deadline,
calendar or commercial assignment inferred from a generic Circuit Civil header.

Footnotes4/5 cite2008-60-UFC; official-domain exact-number search located original
`wp-content/uploads/2017/08/2008-60-UFC.pdf`. Both pages read and visually checked.
Its Civil Rule1.610/Room880 statements differ from retained2019-9-UFC Family
Rule12.605/Suite20170 directions. Dates and replacements kept separately; no
controlling-authority conclusion. Current individual author date unknown.

Existing2026-33-UFC distribution original reused: all3pages visually checked;
supplemental review covers paragraphs2,3,5,7,11,13,15,16 and dates. Omission from
ordinary new-case tables is not an assignment-termination finding; JS remains in
other allocation clauses. Earlier Franker review preserved separately. Dependency
hub's introduction/card supports related-family transfers; other judges not
researched out of sequence. Search-only2020COVID guidance not adopted as current.

Read `receipts/person-hope-tieman-bristol.json`, `review/bristol-discovery.json`,
`review/bristol-links.json` and shared-source registry. Read-back verified842
artifacts and65nested citations. Person validator, identical save, frozen replay
and entity-context checks passed. Replay `draft/checkpoint-69-frozen.json`; never
rerun mutable save body, which appends shared reviews. `review/bristol-context.json`
and `review/finish-bristol.py` verify source distinctions and order exception.
No final report advanced. Next Elaine A. Carbuccia; county remains incomplete.

## October 16 — Elaine A. Carbuccia, Division40

Completed individual civil/shared review in capture4554, packet70. Judiciary →
Carbuccia → Biography (`2726-2/?smid=17474`) and Division Procedures
(`division-40/`). Save exact iframe in `carbuccia-document`; actual print/edit link
has ID `1ueJ1zO0YBuKknsMnOWT16RHo-4SAmL6G2xjZ705EXh4`, exported as PDF.
Full63,175-character HTML and all22 physical PDF pages read/visually checked,
including RUCD form. Two header tables and one seal image inspected. Contents
references are not physical pinpoints. PDF external destinations match HTML
inventory; Rect/Point JSON errors repaired by numeric coordinate serialization.

Profile Pam Coe/procedure Pamela Coe; shared Div40@17th.flcourts.org,
954-831-0654, chambers WW11135/courtroom WW11164,8:30–5 office hours with
noon–1:30 lunch. Header updated2026-08-19; distinct dated appearance/conferral
changes retained. No named assistant email/fax/separate phone inferred.

SectionVI names Division38 in its status-quo adoption sentence. Store owner40,
stated subject38 and `reference_names_other_division`; neither40adoption nor
40non-use inferred. General courtesy copies accepted at hearing; distinct non-DV
five-business-day exchange and three-business-day CMS instructions retain
physical-copy exception. Emergency orders have two-business-day/two-day clauses.
Joint stipulation literally within five business days before trial, unlike shared
template wording. Friday discovery line versus UMC exclusion, emergency clerk
notification, CMC routes and other discrepancies retained without choosing a rule.

Record contains29 topics,17 structured timing rules and11 ambiguities/discrepancies.
All16 sections and embedded affidavit reviewed; optional forms/help/videos remain
links, not a claim of exhaustive review. Source Dunac/§61.1003 references preserved
without independent validation. Existing relevant shared reviews reused; old
rehearing link returned404 and indexed official copy remains separate. Existing
Local10A/efiling failed URLs and official alternatives preserved. Closures page
links2025memo;2026holiday memo retained separately.

Read `receipts/person-elaine-a-carbuccia.json`, `review/carbuccia-discovery.json`,
`review/carbuccia-links.json` and `review/carbuccia-pdf-pages.json`. Original/fact
read-back verified875 artifacts and164 nested citations. Person validator,
identical save, frozen replay and exact-entity context checks passed.
Replay `draft/checkpoint-70-frozen.json`, not mutable save body.
`review/carbuccia-context.json` and `review/finish-carbuccia.py` verify attribution,
timing and exceptions. No final report advanced. Next Thomas J. Coleman.

## October 16 — Thomas J. Coleman, Division FP

Completed scoped contact/shared review in capture4558, packet71. Judiciary →
Coleman → Biography (`2726-2/?smid=2778`) and direct Division Procedures link:
`https://docs.google.com/document/d/1n5uy6H_rT27qh2iNkUFLZSO3ScEM2VBfp9P-u1MdyBk/edit?usp=sharing`.
Edit response is a JavaScript shell; same-ID `/export?format=pdf` succeeded.
All10 pages read and visually checked. Raw pypdf extraction retained; separate
PyMuPDF text and annotation JSON provide readable pinpoints and actual targets.

Profile Tyrone Kintchen versus procedure Tye Kintchen retained as source variants.
Shared `divfp@17th.flcourts.org`, 954-831-5835, fax954-831-7899; NW7880 chambers,
NW7870 courtroom, seventh-floor reception mailbox. Historical temporary-docket
PDF page4 supplies `tkintchen@17th.flcourts.org`; current validity not asserted.
That8-page document was collected but only pages1/4 reviewed for context/contact.
The2020-07-15 filename date is not an author-stated revision date.

Current profile/procedure FP and March6 assignment-order FK statement preserved;
procedure expressly announces reassignment effectiveAugust17,2026. Revision
August14 and CMS commencementOctober1,2025 are separate. Visible/profile Zoom
883035672 differs from PDF link532000556. Source appearance-permission and
Tuesday–Friday versus Tuesday–Thursday CMS wording differ. Clerk website entry
prints/targets public-defender site. Belinda Mitchell is the in-court clerk, not
the elected Clerk. No live Zoom/CMS interactions performed.

Rule2.530 target is a four-page proposed-amendment notice. Read header and visually
underlined subdivision(f); April1,2025 is comment deadline, not effective date.
Original linked2022-37 and2022-24 orders fully read/visually checked; prior amended
versions retained separately. AI paragraph requires attorney signature/responsibility;
do not invent a disclosure certificate or infer repeal of that individual statement
from circuit AI-order vacatur. Criminal merits/forms remain deprioritized.

Receipt `receipts/person-thomas-j-coleman.json`, discovery `review/coleman-discovery.json`,
annotations `review/coleman-pdf-pages.json`, and entity context `review/coleman-context.json`
retain15 topics,6 timing rules and6 discrepancies. 115 nested citations and870
artifact/fact read-backs verified. `review/finish-coleman.py` checks source distinctions.
Replay `draft/checkpoint-71-frozen.json`; do not rerun mutable save body.
Finalized reports unchanged; next Barbara R. Duffy, county still incomplete.

## October 16 — Barbara R. Duffy, Division FD

Capture4562, packet72: judiciary/criminal hub → Duffy → Biography
`2726-2/?smid=2785`, Division Procedures `division-fd/`, then published Google
iframe saved as `duffy-document`. No wrapper print/edit link located; no PDF
export claimed. Full6,574-character HTML and header table reviewed, all6 anchor
destinations inspected; sole image collected/viewed is Florida seal.

Profile Kamela Rubin/procedure Kami Rubin, shared `DivFD@17th.flcourts.org`,
954-831-5540. Profile chambersNW6880/courtroomNW6840 conflict with procedure
mailingSuite5880; preserve distinct source fields. No named email/fax/office hours
located. Zoom419713883 matches anchors/profile but does not itself establish
remote permission. Additional named-contact/civil searches returned no results;
that is not proof of absence. Three plea links retained without fetching forms.

RevisionOctober7,2025 and CMS-order policy effectiveOctober1,2025 separate.
Five-business-day witness/exhibit-list filing/exchange is a list requirement,
not an inferred exchange deadline for underlying exhibits. Written cancellation
two unspecified days; courtesy copies48hours; email JA for continuance date48hours.
Keep general clerk-filing and CMS supporting-motion/order instructions separate;
do not assert CMS submission satisfies clerk filing. Trial period literal SECOND
AND THIRD WEEK of Calendar Call retained without importing another judge's week.

Read receipt `receipts/person-barbara-r-duffy.json`, `review/duffy-discovery.json`,
`review/duffy-links.json`, and `review/duffy-context.json`. Twelve topics,
four timing rules and two discrepancies saved.48 nested citations and878
artifact/fact read-backs verified; replay/finalized preservation checked.
`review/finish-duffy.py` verifies field, unit and document-type distinctions.
Replay `draft/checkpoint-72-frozen.json`, not mutable body. Next Martin S. Fein.

## October 16 — Martin S. Fein, Division FT

Capture4566, packet73: judiciary/criminal hub → Fein → Biography
`2726-2/?smid=2829`, procedures `ft-division/`. Save published Google iframe and
exact print/edit ID `1KlDH2RB_VF6g5ZH_uKW4Cvqk2UnxMY1zrQ2JdqpIOoA`.
Full3,993-character HTML and3-page PDF read/visually checked; anchor targets agree.
Named assistant Victoria Cruz, `vcruz@17th.flcourts.org`,954-831-7342. Current
NW4760 chambers/NW4780 courtroom; street address from official clerk North
Building entry. Clerk hours are not JA office hours. Older one-page FX source
under2024 upload path retained, including historical Box160; no current routing
or reassignment date inferred. Its OCR email defects do not replace current HTML.

Non-evidentiary Zoom permission expressly applies to attorneys; physical
evidentiary/plea/sentencing/trial attendance retained. CMS motion calendar8:45;
special evidentiary hearings set by judge after filed motion/courtesy email/status
hearing. CMS cancellation limited to motion calendar; no numerical lead time
invented. Proposed orders Word format; bring proposed orders to motion calendar.
Copy opponent on all submissions. Emergencies require call AND email.

Actual proposed-order example link ID `1h38Oo0t-PScmlbXaqDNxZIIpPPaGWkJjdRqmhVPaFKI`
exports a three-page populated criminal case order, not a blank form. All3 pages
read/visually checked for format/scope. June17,2026 order date and2027 case deadlines
stay within `example_scope`, not general deadline rules or current procedure
revision date. Case equipment-access provision also remains case-specific.
Plea form link-only; no criminal-merits expansion or current validity analysis of
the example's historical Supreme Court references.

Read `receipts/person-martin-s-fein.json`, `review/fein-discovery.json`,
`review/fein-links.json`, `review/fein-pdf-pages.json`, and `review/fein-context.json`.
Twelve topics/two source discrepancies;56 nested citations and892artifact/fact
read-backs verified. `review/finish-fein.py` checks scope, contact and conjunctive
instructions. Replay `draft/checkpoint-73-frozen.json`, not mutable save body.
Finalized reports unchanged; next Yael Gamm. County remains incomplete.

## October 16 — Yael Gamm, Divisions JT/46/JL

Capture4570, packet74: judiciary → Gamm → Biography `2726-2/?smid=2796`,
procedure wrapper `division-jt-46-jl/`, published Google iframe saved as
`gamm-document`. Full11,482-character HTML, header table, numbered notes1–6 and
roman-i technology note read. Zero anchors despite printed named email/portal
address. Sole seal collected/viewed. No wrapper print/edit link or PDF claimed.

Lisa Cameron, `lcameron@17th.flcourts.org`,954-831-7758;WW9131 chambers,WW9170
courtroom,Zoom697041821. No author revision/effective date. March assignment
order identifies dependencyJT/46 and delinquencyJL; new-case allocation differs
in purpose from individual assignment. No inferred termination of JL duties.

Individual referral names Vicki Plant;2026-33 paragraph5 maps JT/46 toGMX;
2026-09 names Denise Kistner forGMX. Keep all three `referral_statements` with
their independent dates, not one overwriting identity. This documented conflict
does not block completed source review.2008 emergency reference retained beside
the separately dated2019 source, with rule/office differences unresolved.

Filing2business days versus email2unspecified days preserved. TPR calendar call
literal within10days of trial setting keeps unknown direction/anchor meaning and
party-waiver exception. Footnote4 excepts agreed goal-date extensions from an
accompanying motion; footnote3 requires conferral method/date/time. Premarking
alphabetical then clerk numbers on admission; not another judge's numeric rule.
No dependency online scheduling. Notice controls appearance; hybrid/phone/remote
trial exceptions require source-specific permission. Civil dependency/shared
procedures reviewed; no further delinquency-merits research.

Read `receipts/person-yael-gamm.json`, `review/gamm-discovery.json`,
`review/gamm-links.json`, and `review/gamm-context.json`. Seventeen topics,
three timing rules and four discrepancies;72 nested citations and900artifact/fact
read-backs verified. `review/finish-gamm.py` checks referrals, units and footnotes.
Replay `draft/checkpoint-74-frozen.json`, not mutable body. Finalized reports
unchanged; next James R. Harris. County remains incomplete.

## October 16 — James R. Harris, Division42

Capture4574, packet75: family hub → Harris → Biography `2726-2/?smid=23913`.
The Division Procedures link goes directly to Google document
`1ZMeO_mfEpshcsWbF1DvmieXXtJwuaxZtae3oZHYuXvk/edit?usp=sharing`.
The edit response is an editor/JS shell, not reviewed procedure text. Export the
same document ID with `/export?format=pdf`; retain both original responses.
All24 physical PDF pages visually checked (24blank),48,222characters read.
Read `review/harris-readable.txt` and `review/harris-pdf-pages.json` for text
and actual annotation targets. A truncated image batch was reopened; do not
count images omitted from tool output as reviewed.

Oscaryn Melendez; shared `Div42@17th.flcourts.org`;954-831-0615. ChambersWW11131,
courtroomWW11174. Hours8:30–4:30, lunchnoon–1:30. No named assistant email,
separate phone or chambers fax located; interpreterfax7279 belongs to that office.
Staging testtitan room is not used as current production contact. Header revision
March16,2026 is separately retained; no universal effective date inferred.

Keep actual Zoom target `zoom.us` beside displayed `z-oom.us`. Header Oscaryn
differs from p10 cancellation instruction naming Ms.DelPonte. General morethan30
minutes versus special30minutesormore stays distinct. Motion/noticeCMS24hours
AFTERsetting; response2businessdaysBEFOREhearing. UMCorder48hoursCMS,
specialorder5daysCMS, deferred/requestedhearingorder2days/trialorder5daysemail.
Unilateral setting after2fullbusinessdays nonresponse is distinct from refusal to
agree to the offered date sets. Division42 expressly adopts statusquo; no date
inferred. Later AI circuit sources do not silently erase individual March clause.

Save all nine trial-table rows in `trial_calendar` without correcting2026to2027;
December18,2026call is paired with January19–28,2026. Preserve trailing`*8`.
No case-specific setting or deadline calculation. Individual stipulation literal
within5businessdaysprior differs from shared at least5daysprior. Separate judge
USB is preferred, not mandatory; no other judge's exhibit deadline imported.

The p16 `2018/01/Local_Rule_10A_approved.pdf` works and was fully reviewed,4pages.
Approval stamp January23,2018; blank execution date/signature. Keep separate from
March5final copy and broken2018/03link. The p12 Rule12.200 hyperlink opens
`03-60_rulesandforms.pdf`,128pages: pages1–4 rule/commentary and blank5 reviewed;
remaining123collectedonly. It says30daysafterSERVICE; individual omitsservice.
Do not infer current adopted text or dates from filename. Optional family forms,
videos and secondary authorities remain links, not exhaustive substantive review.

Read `receipts/person-james-r-harris.json`, `review/harris-discovery.json`,
`review/harris-visual-notes.txt` and `review/harris-context.json`.
26topics,15timing rules,12discrepancies;192citations,914artifact/fact read-backs
verified. `review/finish-harris.py` checks literal years, destinations, dates,
statusquo association, timing and review scope. Replay
`draft/checkpoint-75-frozen.json`, not the mutable body. Finalized reports unchanged.
Next Peter Holden; county incomplete.

## October 16 — Peter Holden, Division FC

Capture4578, packet76: judiciary page2 → Holden → Biography
`2726-2/?smid=7594` and procedure wrapper `division-fc/`. Follow its published
Google iframe; saved as `holden-document`. Full16,317-character HTML screened;
contacts and shared procedural sections substantively reviewed. Header table and
sole seal inspected. No print/edit link, individual PDF or browser UI claimed.

Sheila Oldershaw; shared`divfc@17th.flcourts.org`;954-831-7340;NW5880 chambers,
NW5870 courtroom. Fifth-floor North Wing reception drop-off. No namedJAemail,
separatephone,fax orofficehours located. In-court clerk Michelle Dykes is distinct
from elected Clerk of Court; felony-clerk5600 is marked attorneys-only. The visible
clerk URL targets public defender site; preserve both in separate fields.

No author revision/effective date. Motion-calendar heading/schedule excludes
Thursday while narrative includes it; calendar-call heading8:45a.m. differs from
afternoon narrative.5–10minute general motion calendar,5minute CMS clause,
morethan10minute special instruction and15minute special heading remain separate.
No rule inferred for11–14minutes. All physical; court permission for Zoom requested
48hours before, not automatic short-hearing permission. Special-set materials
48hours before; notice within2businessdays AFTER time first offered by JA.
Continuance on/beforeThursday prior to calendar call; later emergency-only
exception preserved. No calendar calculation or invented Word requirement.

CMS access paragraph names`div07@17th.flcourts.org` inside FC; preserve mismatch,
do not silently replace address or send identity documents. Withdrawal clause
uses defendant absent AND no proper notice; keep conjunction. Interpreter3days
and other-language literal“at leave seven”days retained. Header times do not prove
office hours. Eight plea/DNA/probation links saved without collecting/reviewing
contents; no expansion into criminal merits.

Targeted civil-assignment search surfaced2022-33-UFC, naming Holden as DV alternate.
Current saved family-order index links2025-28-UFC with other named judges. Both
one-page originals read/visually checked, datedJuly11,2022 andAugust14,2025.
The2025 order expressly supersedes2023-19, not2022-33 byname; no intervening chain
or replacement date invented.2026 assignment and current profile identify FC.
Separate `assignment_statements` preserve source function/date without treating
historical family search results as present civil assignments.

Read `receipts/person-peter-holden.json`, `review/holden-discovery.json`,
`review/holden-links.json` and `review/holden-context.json`.
15topics,7timing rules,7discrepancies;90citations,925artifact/fact read-backs
verified. `review/finish-holden.py` checks calendars, destinations, role boundaries,
timing triggers, historical statements and form-review scope. Replay
`draft/checkpoint-76-frozen.json`, not mutable save body. Finalized reports unchanged.
Next Jose Izquierdo; county incomplete.

## October 16 — Jose Izquierdo, Divisions JQ/34/JK

Capture4582, packet77: judiciary page2 → Izquierdo → Biography
`2726-2/?smid=2810`; direct procedure Google document
`1UMxDmrM_eRoXYRGNzvpi9V4yhkOLDsOwqIx0ya__jVw/edit?usp=sharing`.
The edit response is an editor shell. Same-ID `/export?format=pdf` yields six pages.
All pages and footnotes1–7 read/visually checked. Initial pypdf extraction breaks
words/lines; retained it and added PyMuPDF readable12,389character extraction.
Original bytes unchanged; no browser rendering claimed.

Laura Gonzalez, shared`divjq@17th.flcourts.org`, named`lgonzale@17th.flcourts.org`,
954-831-3599;WW9133 chambers/WW9150 courtroom. Named email is the PDFpage1 link
behind Laura Gonzalez, with annotation rectangle clipped text verifying name.
It is not guessed from surname. No separatephone,fax orhours located. No author
revision/effective date; retrieval and order dates are separate.

Individual referral names Vicki Plant.2026-33 paragraph5 maps JQ/34 toGMZ;
2026-09 names Denise Kistner forGMZ (corrected in capture4594). Preserve all three dated statements;
Keep GMZ distinct from Gamm's GMX even though both rows name Denise. Profile includes dependency and related
family/ICWA matters; March assignment includesJK. New-case allocation does not
itself endJK assignment. No exhaustive delinquency-merits review.

72hour Zoom motion/notice requirement; physical notice requires court permission.
Interpreter-residence clause and late-unavailability conferral/continuance route
retained without inventing automatic permission. TPR pretrial not less than10days
BEFOREtrial is clear, unlike another judge's setting wording. Filing2businessdays
and emailcopies2unspecifieddays retained separately. Trials/exhibits follow in-court
directions or case-specific pretrial order; no imported alphabetical premarking.

Footnote2 requires conferral method/date/time;4 excepts agreed goal-date extension
from accompanying motion;5 says agreed continuance does not guarantee grant.
No online dependency scheduling. Emergency footnotes cite2008-60, retained beside
separately dated2019source with different rule/office details. Footnote backlinks
are not claimed as independently reviewed separate published document versions.

Indexed2024-9-UFC Hague assignment order fully read/visually checked,2pages.
March8,2024issuance; no stated effective date. Receiving judges immediately notify
Izquierdo for identified Hague/ICARA/statutory matters; family administrative judge
designates temporary substitute if unavailable; related-case notice required.
Review covers state assignment/routing, not federal court expansion or Hague merits.

Read `receipts/person-jose-izquierdo.json`, `review/izquierdo-discovery.json`,
`review/izquierdo-readable.txt`, `review/izquierdo-pdf-pages.json` and
`review/izquierdo-context.json`.15topics,4timing rules,4discrepancies;84citations and
936artifact/fact read-backs verified. `review/finish-izquierdo.py` verifies named-link
association, GMZ mapping, remote conditions, footnotes and timing. Replay
`draft/checkpoint-77-frozen.json`, not mutable save body. Finalized reports unchanged.
Next Kristin R. Kanner; county incomplete.

## October 16 — Kristin R. Kanner, Division 37

Capture4586, packet78: judiciary page2 → Kristin R. Kanner → Biography
`2726-2/?smid=2756` → `/division-37/` → published Google iframe
`2PACX-1vTj_Ma_XHjNE2NatcHbOefvmLUvv5_DYijAS-U5CiF6WaNRVAsGC2Us8BuB0cGq9x97pMmofRblEMM1`.
No edit/print link in collected wrapper or document; do not guess export IDs.
All60,760characters read, XVI sections, embedded RUCD affidavit and finalstar note.
The single image is the Florida seal, visually inspected. HTML tables/anchors
saved; no PDF or browser-layout verification claimed. Header revision July6,2026;
DV physical March10,2025 and conferral/discovery October31,2025 are separate dates.

Patti Buchholz, shared`Div37@17th.flcourts.org`,954-831-5895;WW11127 chambers,
WW11154 courtroom. Full source name Kristin Raybon Kanner. Office8:30–5,lunch12–1:30.
Named assistant email, fax and separate phone not located in checked sources;
historical staff search hits for other judges do not establish current contacts.

Owner37 status-quo paragraph names38. General-order paragraph's actual email
target isDiv40; specific competing-order section/header useDiv37. Preserve these
as source statements, not assistant reassignment or inferred status-quo adoption.
Header UMC9a.m. versus Tue/Wed/Thu8:45–9:30a.m.*; finalstar is only a reminder to
review changing procedures. Special-set temporary relocation3hours versus specific
relocation1hour. Neither discrepancy resolved. Pretrial UMC is expressly PHYSICAL;
do not copy Carbuccia's Zoom instruction or her custody/adoption conditions.

Emergency orders2businessdays versus2days; general/specific competing-order routes;
clerk notification descriptions; CMC cancellation routes; individual/shared temporary
relief and trial-stipulation timing retained. Interpreter wording literally says
possible certified court reporter. §61.1003(10) retained as printed, not repaired.
Individual source Dunac/statutory references not independently analyzed.
Shared sources reused within recorded scope; no exhaustive family-merits expansion.

Read `receipts/person-kristin-r-kanner.json`, `review/kristin-discovery.json`,
`review/kristin-links.json`, and `review/kristin-context.json`.
28topics,16timing rules,13discrepancies;157citations and943artifact/fact read-backs
verified. `review/finish-kristin.py` checks cross-division associations, hearing
times, units, physical pretrial and fullHTML scope. Replay immutable
`draft/checkpoint-78-frozen.json`, not the mutable body/save script.
Finalized reports unchanged. Next Michael G. Kaplan; county incomplete.

## October 16 — Michael G. Kaplan, Divisions 59/57

Capture4590, packet79: saved official family hub → Kaplan → Biography
`2726-2/?smid=2812` → `/division-59/` → published Google iframe
`2PACX-1vRiU4FYcYfQK8etdju54KQvTGkGF4f1fgCIDO_Ky7_ghjhToZ6u35N-40wqkDbQSS0a2A4ONiZbabiW`.
All20,138characters read, sectionsA–I and three embeddedforms; singleFloridaSeal
image inspected. No supplied print/edit link or individual PDF claimed. No stated
revision/effective date. Review is civil/shared procedure, not exhaustive firearms,
criminal or program merits. Program-contact routing retained.

Hope Allan, shared`Div59@17th.flcourts.org`,954-831-1663;WW10138/WW10150.
DVclerk2140/954-831-5570/5520 andcompliancemonitor7278 are separate contact roles.
Search hits for historical Haury procedures mention`hallan@17th.flcourts.org`;
not verified as Kaplan's current named assistant email. Fax, hours and separate
assistantphone not located. PublishedZoom link does not authorize remote appearance.

Court alone schedules/cancels; no online scheduling or motion calendar. Email
motion and clerkacceptance, hearingtime/names/case. Remote appearance requires
filed motion and hearing-request process; JA cannot grant. Agreedorders require
motion; bothPDFandWord by email. Emergency motions/status throughclerk, notJA.
Physical exhibits on hearingday, extraopponentcopy, retainableformat, ownplayback/
HDMIequipment; do not submit inadvance. Authorizedremoteappearance instead requires
CMSsupportingdocuments; no individual leadtime. Ten-day prose follow-up atclerk is
not a court turnaroundpromise and has no expressly specified clockstart.

Missing-evidence register: individualH.5 cites2012-12-UFC without hyperlink for
family/DVtransfer. Officialfamilyorderindex has no entry. Exact-number/subject
searches returned no original. Constructed probes at `/wp-content/uploads/2017/08/`
and `/images/stories/17th_pdf_files/` with`2012-12-UFC.pdf` returned404; these were
not supplied links. Retain gap for any later officialarchive/recoveredlink; do not
assert nonexistent/repealed or substitute2026-33. The individual source's own
transfer-at-next-DVhearing instruction remains preserved with attendanceunlesswaived.

Assignmentorder2026-09page3 visually checked: circuitUnifiedFamily59/57 andchairperson.
Individual59title does not end57assignment.2026-33page1 paragraph4 visuallychecked:
59/57 civilDVallocation37.5%,63 37.5%,45 25%;September14effective,September10issuance.
Supplemental shared scope saved.2019-9emergency reference has different scope,
including paragraph3DVexclusion; preserve without determining controllingprocedure.

Read `receipts/person-michael-g-kaplan.json`, `review/kaplan-discovery.json`,
`review/kaplan-links.json`, foursearch-result files and `review/kaplan-context.json`.
16topics,1timingcue,2discrepancies;61citations and956artifact/fact read-backs verified.
`review/finish-kaplan.py` checks roles, routes, missingoriginal, probeprovenance and
history comparison. Replay `draft/checkpoint-79-frozen.json`, not mutable save script.
Finalized reports unchanged. Next Ernest A. Kollra Jr; county incomplete.

## October 16 — correction to Izquierdo magistrate row association

Capture4594/packet80 corrects an agent error in capture4582/packet77. The original
2026-09-Gen page6 and its saved quote both sayGMZ Denise Kistner. The earlier
semantic record saidLucy Ramos Miller, taken from adjacent rows. This was not a
source conflict. Page6 visually rechecked; GMX andGMZ both nameDenise, while
ZM/GMW/GMY nameLucy. JQ/34→GMZ remains supported by2026-33paragraph5.
Vicki Plant remains the individual procedure's separate statement, without selecting
controlling authority. Original sources and prior capture preserved; correction
is tagged `agent_transcription_correction`, not a source change.

Read `review/izquierdo-referral-correction.json`, corrected person receipt and
`review/izquierdo-corrected-context.json`. Replay`draft/checkpoint-80-frozen.json`.
The old packet77/body/save/finish files are historical; do not regenerate current
state from them. `finish-izquierdo-correction.py` compares the exactGMZrow to the
saved name and rejects the formerLucyvalue. Valid citation substrings alone had
not detected the incorrect semantic association.84citations/951artifact and fact
read-backs passed; prior capture and finalized reports unchanged. No judge count
increment for this correction. Next Ernest A. Kollra Jr.

## October 16 — Ernest A. Kollra, Jr., Division FF

Capture4598/packet81: officialCircuitCriminalhub → Kollra → Biography
`2726-2/?smid=2813` → `/division-ff/` → publishedGoogleiframe
`2PACX-1vR1Szl1rn4ug2Ed2ufXXtftWo8Dcdc8hW2PlHtKdVwC5XjJ_Vy6_QiuLTio2avzSakNr6VomQurFONa`.
All8,369characters screened, shared/contact practice reviewed; singleFloridaSeal
image inspected. No print/edit link or individualPDF claimed. Two externalEnglish/
Spanish pleaformlinks saved, not downloaded/reviewed; noexpandedcriminalmerits.

Teresa Sugar (“T”),954-831-3575,NW5760/NW5750; reception fifthfloorNorthWing.
Headernamedemail actualmailto`tsugar@17th.flcourts.org`; hearingrequest actualmailto
`TSGUAR@17TH.FLCOURTS.ORG`. These differ beyondcase; preservebothcontexts without
guessing which is valid. Source expressly prohibits FFdivisionemail for hearing
requests but supplies no fulladdress; do notconstruct it. Automatedclosure7777
andCMSsupportcalendar email separate fromJA. No fax,separatephone orhours located.

CMScommencementOctober1,2025; no whole-documentrevision/effective date. Actual
`/cms3-manuals/THIS` hyperlink404; clean`/cms3-manuals/` separatelyprinted and existing
officialindex200, reused. Do not call it a redirect. FirstBSOemail-lookingtext points
to`http://csucourtorders.org`; another occurrence has matchingmailto. Prosecutor
AFERRERfragment targetsTSTEIN; secretarySAMATHAfragment targetslbrown. Splitdivision
link partly targetsjudiciaryindex, partlyurts.org. Inventoryretained; nonofficial
targets notvisited and criminalagency contacts notpromoted toverifiedcourt roster.

8:30five-minuteZoom permitted withoutwrittenmotion, notifyASA; mandatoryclientnotice
requiresphysicalappearance. SpecialwitnessZoomallpartyagreement/noticeconditions
separate.11a.m.1hourmandatory,afternoonsgenerally90minutes; specific3–5session2hours,
Arthur1:30or3beside1:30-onlyheading. Keep source-specificdifferences. Motion>10pages
hardcopyreceptionwithattachments; otherreviewmaterialsphysical;3signaturecopies.
Calendar-call agreedsubmissions2daysbefore, no business-unitinference. Continuance
eachcaseuploadedseparately, filedmotion evenagreed. Trialdatesonlysetincourt.
Propertyreturn includesholdingagencynotice/agreement; notgeneralcivilreplevinrule.

Read `receipts/person-ernest-a-kollra-jr.json`, `review/kollra-discovery.json`,
`review/kollra-links.json`, bothsearch-result files and `review/kollra-context.json`.
13topics,1timingrule,5discrepancies;68citations/960artifactandfact read-backs verified.
`finish-kollra.py` checks exactFFrow againstsavedname, negativeadjacent-namecontrol,
emailvariants, thresholds, conditionalappearance andunreviewedforms. Replay
`draft/checkpoint-81-frozen.json`, notmutablesave script. Finalizedreportsunchanged.
Next FrankLedee; countyincomplete. PriorIzquierdo correction remainspreserved.

## October 16 — Frank Ledee, Division FI

Capture4602/packet82. Official criminal hub → biography `2726-2/?smid=8291`
→ `/division-fi-procedures/` → Drive preview
`1RrGb-88MFjd6tsRa1WShsNI4D13NwQIu`. Download by that same ID preserves the
13-page original. Page9 links a separate four-page trial template,
`1VToHrbqp3urWRiUO_bmBJh5f508N76eM`; both originals retained, no text/byte
identity asserted. All17 pages text-screened and visually checked; substantive
review covers contacts and shared procedural logistics. Six external plea/VOP
forms remain links only. Criminal merits not exhaustively analyzed.

Barbara Sierra,954-831-3758,shared `Divfi@17th.flcourts.org`,NW4790 chambers,
NW4750 courtroom; fourth-floor North Wing reception behind elevator bank for
physical dropoff. Explicit no facsimile. No current named JA email,separatephone
or officehours located. Historical foreclosure contact/search hit not promoted.
Zari Fleming is in-court clerk; felony clerk6565 and attorney-only5600 are separate
roles. Jill Holness is probation contact, not JA. FI row on2026-09page2 verified;
old foreclosure/family-chair references do not establish current civil duties.

Printed July1,2024 date not labeled revision/effective. Five BUSINESS days for
courtesy pleadings; complete discovery failure/noextension may get10-day order
measured from signing, defective responses require hearing. Entity replacement
counsel20days fromwithdrawalorder. Interpreter3days,7forotherlanguages. Rule10A
oral OR written communication includesemail/text, with continued effort to speak
if initial attempt fails. No competing proposed orders; disputed language goesMC.
Cancellation requiresJAcontact evenafteragreedorder entered. Generalcalendarcall
less/more365days fromarrest leaves exact365unaddressed; no inclusive inference.

Blank template: discovery proof by5PM30calendar days before PTC if reciprocal
discovery elected; memoranda20calendar beforePTC; inlimine/evidence motions5calendar
beforePTC. Continuance must be SET10calendar beforeTRIAL,withclientconsent,except
trulyunforeseenemergency. No case dates computed. Template8:30trial and physical
PTC defendant instruction retained beside general10:30trial/remotePTC clauses.
Template compliance motions8:30anyday differ in scope fromgeneralMon–WedMC;
specialjuryinstruction submission atPTC differs fromgeneralconferralbeforeclosing.

Literal rehearing cite2022-002-GEN: official
`/wp-content/uploads/2022/01/2022-2-Gen.pdf` page1 is assignments,effective
January10,2022 unlessotherwiseindicated. All6pages collected, onlypage1 reviewed.
Separate2022-5rehearing order is not silently substituted. Individual emergency
cite2014-32 retained alongside2021-50's express supersession statement; no authority
resolution. Sources, original bytes, retrieval times, dates and scope preserved.

Read `receipts/person-frank-ledee.json`, `review/ledee-discovery.json`,
`review/ledee-pdf-pages.json`, readable extracts, search results and
`review/ledee-context.json`.108citation checks,975artifact read-backs and fact
read-back passed. `finish-ledee.py` checks exact FI row, negative name/event-anchor
controls, template conditions, fax state, literal reference and review scopes.
Replay `draft/checkpoint-82-frozen.json`, not mutable save script. All82 packets
verified; no finalized-report advancement. Next Michael Lynch; county incomplete.

## October 16 — Michael Lynch, Division FA

Official criminal hub → biography `2726-2/?smid=2821` → `/division-fa/` → published
Google document `2PACX-1vTyNsrcKxQV_jJEibK2e4jE4XlOn4iI4fbLJ1HYAj860ph53_XTKpZdAI7oi72wng`.
Print link supplies document ID `1V5lFi1-KWPxLYrxqlTmyWiuTNuniPY77`; PDF export200,
four pages. All text and images reviewed for contacts/shared procedure. HTML and
PDF match after whitespace plus two zero-width spaces removed; not byte identity.
Seven DNA/plea/VOP form destinations decoded and retained, not downloaded/reviewed.

Profile Elizabeth Viera versus procedure Susan Moss: preserve both statements,
shared divfa/7831 route and unknown change date. Do not borrow historical roster
email/phone or confuse Michael Lynch with Thomas M. Lynch IV. NW6760 chambers,
NW6780 courtroom; sixth-floor North Wing reception dropoff. Street/ZIP supported
by official clerk North Building location; clerk service hours are not chambers
hours. FA assignment row on2026-09page2 checked against exact name.

Source has general physical language plus an express under30-minute non-evidentiary
Zoom exception; other hearings need permission. Calendar call separately allows
Zoom with in-person attorneys called first. The15-minute-or-less threshold governs
9AM Mon/Tue/Wed/Fri scheduling; longer hearings generallyThu/Fri afternoons.
Both parties must confirm and notice reachJA before hearing set. Agreed orders
require CMS, Agreed Motion attachment AND email chain agreeing to order language.
Continuance with attached order byprecedingTuesday; only emergencywritten motions
thereafter. No invented numeric business-day deadline or time-of-day cutoff.

Read `receipts/person-michael-lynch.json`, `review/lynch-discovery.json`,
`review/lynch-links.json`, search-result files and `review/lynch-context.json`.
Ten topics, one timing rule and one discrepancy;51 citation checks and985 artifacts
read back. `finish-lynch.py` verifies name provenance, exact FA row, negative
same-surname control, duration operators, required attachments and normalized
comparison. Uses `pymupdf` import; initial `fitz` deprecation warning addressed.
Replay `draft/checkpoint-83-frozen.json`; do not rerun mutable writer. All83 packets
replayed without advancing finalized reports. Next Lorena V. Mastrarrigo.

## October 16 — Lorena V. Mastrarrigo, Division FB

Official criminal hub → biography `2726-2/?smid=16300` → `/division-fb/` → published
Google document `2PACX-1vT0XMyzF9uSbxHRDUYsHbGfkZXqKz13ZGoiLS9Nn6_0p9vzUkEhx4tI-YEFBxi9Ryry_dsvcOGr3Hga`.
Print link document ID `1QmxRN3OaEufyPPHnRSzMIZAgDwk8tGBt563CaUW9KoI` exports six-page
PDF200. All13,729 HTML characters and six PDF pages screened/read for shared
process; all images visually checked. Normalized text matches after whitespace,
zero-width spacing and two bullet glyphs removed. Revision January24,2025 explicit.

Angela M. Salomon (procedure omits M.),954-831-7208,shared divfb. NW5790 profile/body
chambers versus letterhead5880; NW5780 courtroom. Preserve both room statements.
Heading saysFD despiteFB title/profile; forms introduction saysFC. These labels do
not establish extra assignments; exact2026-09FB row supports Mastrarrigo. Historical
family41 search result not promoted to current civil assignment. Nina Chandler is
in-court clerk, Latrone Bailey probation; neither is JA. Named email/fax/separate
phone/officehours not located. Printed clerk URL actually targets defender site.

Thirty minutes or longer physical; in-custody counsel physical, noZoom. Other
remote appearances require advance inquiry about the specific matter. Do not copy
Lynch's automatic short-hearing permission. Defendant waiver requires filed writing
AND recent client contact. MC Mon/Tue/Wed/Fri9,5–10minutes; only5minute motions
expressly self-setCMS aftercoordination. Morethan10special versus heading10-or-longer
retained. JA specialsMon–Fri10:30–4:30 need filedmotion,duration,witnesscounts.
Notice within2BUSINESSdays afterFIRSTtimeoffered, orslotmaycancel. Court-review
materials48HOURSbeforehearing. Separate agreedcontinuanceCMSdeadlineTuesday3PM.
ArraignmentnarrativeMon–Wed versus scheduleaddsFriday retained. Agreedmotion
labeltitleANDbody; agreedorderCMS, noLynchagreement-email attachmentrule imported.
Interpreter3days,7forotherlanguages; alwayscopyJA oninterpreterrequestemail.

Six form labels/five unique destinations remain unreviewed: Creole plea andVOP
point to sameDriveID. Preserve duplicate destination without deciding correct label.
Read `receipts/person-lorena-v-mastrarrigo.json`, discovery/link inventory, both
search-result files and `review/mastrarrigo-context.json`. Eleven topics,five timing
rules,six discrepancies;69 citation checks/995 artifacts read back. Finish script
checks exactFB row, negative name control, first-offer trigger, actual targets,
conditional appearance and normalized text. Replay `draft/checkpoint-84-frozen.json`;
all84 verified, finalized reports unchanged. Next George Odom Jr; Merrigan completed.

## October 16 — George Odom, Jr., Division FJ (partial)

Official criminal hub → biography `2726-2/?smid=12287` → `/division-fj/` → published
Google document `2PACX-1vQ-MciDi9gfSzL8mU95slA3sNwUTgswVi-OQwGzLkOWDTVGQNwb00x0Ciww-5rzM9VUbrce-8Jy4OZf`.
No print/edit/PDF link. All12,683characters screened/shared process reviewed;
one embedded FloridaSeal checked. TOC page labels are not verified PDF pinpoints.
Use named proceduresA–L for citations. Vanessa R.Williams,6574,sharedDivFJ,
NW4880/NW4870,revisionOctober9,2025. No namedemail/fax/separatephone/hours located.
Do not use search-discovered private-practice contact as chambers contact.

Five-minute-or-less coordinated CMS setting; >=30minutes specialset throughJA,
no permission inferred for6–29minutes. Notifycourt aftertwoFULLbusinessdays of
nonresponsivecoordination, not unilateralset. Caselaw/responses2businessdaysbefore.
Remote status/calendarcall,15minutes availablebothbeforeANDafter. Wordorders,
CMS/email/inperson routes. ContinuanceTuesday4:59PM; statusrescheduleemailreasons.
Allow24BUSINESShoursforJAresponse;48hourservicefollowup hasunspecifiedtrigger,
notdecisiondeadline. Courtesyhanddeliveryemailreceipt; unrepresentednoemailinperson.
IndividualAIface-disclosure/personalverification requirement kept beside circuit
2026vacatur; no SupremeCourt-original review or controlling-authority decision.

Pending originals and retrieval record:
- `2018-112-Gen_Amendment-2.pdf` under official2024/07 uploads, citedbyjudge.
- `2018-112-Gen_Amendment-3-.pdf` under official2026/04 uploads, listedbygeneralindex.
- Both45secondcurl attempts and30secondIPv4 retries timedout. WebinitialPDFmetadata
  says11pages; subsequentwebfetchalsotimedout. See `odom-retrieval-attempts.json`
  and `odom-duty-web-results.json`. Originalbytes/fullbodyreview notclaimed.
- CitedBar2019–2021handbook returned403XMLAccessDenied. ExactURL andresponse saved
  under `odom-bar-handbook`; webalsoinaccessible. No substitutedhandbook claimed.
- `MOTION TO WITHDRAW ATTORNEY` finalheading isunlinked/noformbody. Exacttitle+Odom
  officialsearchdidnotlocateform. OneEnglishpleaformURLislinked,scope-deprioritized.

Read personreceipt, `review/odom-discovery.json`, linkinventory, searchresults and
`review/odom-context.json`. Capture4614/85 has11topics,7timingrules,2discrepancies;
74citations/1,007artifactreadbacks passed. `finish-odom-partial.py` verifies saved
facts AND incompleteentitycheck/count74/activeOdom. Structuralpersonvalidation
is not completion. Replay `draft/checkpoint-85-frozen.json`, notmutablewriter.
Keep Odom active until remaining source work is addressed; county unfinished.

## October 16 — George Odom, Jr., recovered originals and completed scoped review

This supplements the historical partial review above; do not rerun the old partial
writer over newer state. Capture4618/86 contains12topics,7timingrules,3discrepancies,
121citation validations,566sources and1,015artifacts. All86 frozen replays passed.

Recovery paths for future agents:
- General administrative-order index → `2018-112-Gen_Amendment-3-.pdf` under
  `/wp-content/uploads/2026/04/`. Normal HTTP public entry redirects to HTTPS and
  now returns200. Save both URLs and prior timeout evidence. Eleven-page original
  `odom-duty-a3-recovery`; main1–7 signedJanuary21,2025, attached8–11 datedDecember1,2014.
  Upload-directory date is not issuance date. Review civil/shared routing; criminal
  warrant merits are lower priority. Exact cited Amendment2 under2024/07 returned404.
- Official Bar search found separate `/uploads/2019/08/ADA-2019-2021-Ideals-Goals-Handbook-v2.pdf`.
  `odom-handbook-v2` has174pages; review only1–3,7,17–28. Exact October2019 URL remains403.
  Do not silently replace its source identity or call all174pages reviewed. Letter
  August2019, Guidelines foreword2008, final revision09-08-2011 remain component dates.
  Preserve must/should distinction; next-business-day proposed-order guidance is
  recommendation in that source, not a new binding individual filing deadline.
- Repeated exactfilename/title/author searches did not recover old dutyPDF or the
  advertised unlinked withdrawal form. Save search responses and unavailable status;
  no inference of nonexistent form or source deletion from empty results.

Use `review/odom-completed-discovery.json`, personreceipt, `odom-completed-context.json`
and `history-capture-86.json`. `odom-completed-body.py` loads frozen85 receipt before
enriching it; never mutates historical packet. Replay `draft/checkpoint-86-frozen.json`
for deterministic persistence, rather than rerunning time-sensitive writer.
`finish-odom-completed.py` verifies actual source identity, date components, page
limits, source gaps, literal timing units and preserved history. Exactentity check
is verified; `odom-missing-originals` remains incomplete. County stays incomplete.
Genuine unavailable sources are accurately disclosed, not confused with unresolved
authority conflicts or an instruction to spend indefinitely on low-priority forms.

## October 16 — Michael J. Orlando, Division JC

Official `/04-juvenile-delinquency/` hub → biography `2726-2/?smid=2626` →
`/division-jc/`. Iframe published document
`2PACX-1vTosz_hB4YdHytGtY73b9ovVGX1PNCOBFUQM5u1neRa9N6bHbF_7r_SVv1GHRDgwg`;
print link document ID `1WWcgeQEoAgPBmHQwvInVBSpgrwDmtIeB` exports six-pagePDF.
Read profile for assistant/phone/rooms; procedures for namedJAemail and fulladdress.
Shawnta Mallard,6344,smallard@17th.flcourts.org,NW5850/NW5840. No separateJAphone,
fax or officehours located. Programmanager ybrown email explicit; name not stated.

All9,507HTMLcharacters and sixPDFpages screened/read for sharedprocess; all six
visually checked. Text agrees after whitespace/fourU+200B normalization. Noimages
or linkedforms, only fourmailtoanchors. No individual revision/effective date printed.
Do not treat retrievaldate as issuance. Current assignmentorder page3 exact JC row;
older search-hit JE assignments do not establish current additional assignment.

Save agreedPDF/emailJA route, agreement statement in email AND motion, descriptive
AGREED title, copyall. ThreeBUSINESSdaysdisputedrequestnotice withmotion/allpartytime;
source gives no counting cutoff. No CMSselfsetting or Wordorder route inferred.
Continuanceagreement/newdate/motionANDorder; immediateparticipantnotice onlyafter
signedorderreceived. Noagreement→hearingrequest. CourtPAPERcopies at hearing,
opponentcopies immediatelyuponsetting, not an invented three-daycourtesydeadline.
Keep initialphysical/permission, specifiedremote categories, and opponentobjection
defaultphysical distinct. DivisionalZoom95929742162 differs fromdetention99725122895.
Individualemergency assignedjudge→alternatejuvenilejudge→programmanager; motion,
timeestimate,copyall/assignedJA,andreachablephone. Do not substitute genericcivilchain.

Read `review/orlando-discovery.json`, personreceipt, `orlando-context.json`, and
`history-capture-87.json`. Capture4622/87:9topics,3timingrules,0identifiedconflicts,
54citationvalidations/1,019artifactreadbacks. Reuse twoidentifiedshared reviews with
scope/date limits. Juvenilemerits/diversion remain deprioritized; noexhaustiveforms.
Replay `draft/checkpoint-87-frozen.json`; `finish-orlando.py` checks format/timing,
appearancequalifications,exactassignmentrow,normalizedPDFmatch andpreservedhistory.
County remainsincomplete; finalizedreportsnotadvanced. No live submissiontest.

## October 16 — Ari Abraham Porth, Division FZ

Follow the official criminal hub to biography `2726-2/?smid=2834`. Its actual
procedure link is `http://www.17th.flcourts.org/wp-content/uploads/2026/01/FZ-Division-Procedures-1.pdf`,
which redirects to HTTPS. The first search result instead used the older
`2025/10/FZ-Division-Procedures.pdf` path. Save both originals and inspect the
profile's actual link; search ranking does not establish the linked version.

The profile and linked PDF list Makila Holmes, phone ending 6905, chambers NW7790
and courtroom NW7810. The PDF also supplies named MHolmes, shared DIVFZ and judge
JPorth email addresses. Its prohibition on ex parte communications still applies.
Interpreter fax 7279 is not a chambers fax. The in-court clerk is identified only
as Richie; do not invent a surname. The Lucy Ramos Miller/Elizabeth Ranalli entry
is a reference in this judge's procedures, not a newly refreshed magistrate record.

The linked PDF has eight physical pages despite seven printed page labels. All
physical pages were screened, reviewed for shared procedure, and visually checked.
Use physical-page citations. The older seven-page PDF was collected, but only its
first page was reviewed: letterhead room 1635/phone 7783 conflicts with body
7790/6905. Neither version states a revision or effective date; upload paths are
not legal dates. The linked PDF has no link annotations despite blue underlined
text. Mechanical extraction of nine annotations from the older PDF recovered a
plea-form Google Drive URL. Retain it as an older-source link; no plea-form merits
review or identity with a newer form is claimed.

Record these individual requirements without importing neighboring practices:
- Hearing requests go to DIVFZ with opponent copied and duration stated. Next-day
  add-ons have a 3 PM cutoff; the source does not define holiday adjustments.
- Special sets of 15 minutes or longer require a filed motion, JA copy, time and
  witness estimates, opponent coordination, and served/emailed notice. No notice
  means no setting. The source places these hearings in courtroom NW7810.
- Unopposed motions require a conferral certification, agreement scope and
  “UNOPPOSED Motion” in the title. Post-ruling orders require Word AND PDF.
- Agreed orders accompany agreed motions. Contact the JA to cancel; if the
  resolving order was not submitted or signed, attend. An entered order alone
  does not cancel the hearing.
- Preserve the separate Zoom witness-agreement and plea court-order conditions.
  Other-language interpreter requests require seven DAYS, not business days.
- Substitution without a hearing requires written client consent, stipulation
  and the stated counsel certification. Withdrawal requires proper party notice.

Do not expand mental-health/diversion merits or infer a current FR assignment
from old search results. Rendering emitted `MuPDF error: format error:
cmsOpenProfileFromMem failed`; images were produced and visually checked readable.
Do not report warning-free rendering.

Use the person receipt, `porth-discovery.json`, `porth-pdf-annotations.json`,
`porth-context.json` and `history-capture-88.json`. Capture 4626/88 contains ten
topics, three timing rules and two discrepancies; 52 nested citations and 1,026
artifact readbacks were validated. Replay the frozen packet. `finish-porth.py`
checks the actual profile link, version differences, physical pages, review limits,
formats, contact roles, thresholds and preserved prior records. The county remains
incomplete; finalized reports were not advanced.

## October 16 — Rebollo/Marra source association and historical contact boundary

Do not select the next judge solely from the March assignment order. Its JD row
names Carlos S. Rebollo; the October2026 chart and current structured roster name
Jessica M. Marra. The live juvenile hub links biography `2726-2/?smid=2837`, whose
heading/contact block names Marra while career text references Rebollo's law office.
Follow its `/division-jd/` link and inspect the document title before associating
contacts or procedures. The PDF expressly names Marra and states October13,2026.
Neither the profile ID nor a search match for Rebollo proves current applicability.
Preserve source statements and chronology; no retirement or controlling-authority
decision is needed to record this baseline accurately.

The official historical directory at
`https://www.17th.flcourts.org/wp-content/uploads/2017/10/judges_ja_phone_list.pdf`
states September5,2017 on its pages. Rebollo's row on physicalpage2 lists Elizabeth
Viera,954-831-7708,NW4850/NW4840,JD Juvenile Delinquency. Two pages collected;
only the date/header and Rebollo row on page2 were reviewed and visually checked.
Save those fields as historical, never as verified current contacts. The Marra
contact block (Ashley Beckford/7700) was not reassigned to Rebollo. His current
contact/procedure fields remain null and unverified; absence from a newer list is
not proof of retirement or its date.

Receipt `receipts/rebollo-source-reconciliation.json` uses a source-association
record, not a complete current-person receipt. The existing person validator was
not weakened or claimed passed. Save helper `save-rebollo-reconciliation.py`
validated all seven citations and persisted the record as `county_roster_reconciliation`.
Packet89/capture4630 keeps an incomplete exact-person check and a verified, dated,
hash-backed source-association check. The completed judge count stays77. The helper
initially rejected missing timestamp metadata on the latter check; the writer was
corrected, not the validator. PDF whitespace affected the initial title assertion;
comparison normalizes whitespace while preserving the original citation bytes.

For the next Marra review, reuse the collected iframe
`2PACX-1vTAOr82lvZNx1zSYq42_B8KuSToI0fs0DUOImX9AFE-2_bv0iBqEDOfkor9kIpPZgFHNjSzHdjt12dK`
and print document `1s9c3trJMRRBOrJ6ikbIOBuDPi0f0x9KBfs7EQJtz-UI`.
Acquisition keys start `rebollo-jd-` because of discovery provenance, not authorship.
The HTML has23,119characters; the PDF has12pages. Only PDFpage1 identity/contact
header was reviewed and visually checked here. A long HTML output was truncated;
do not claim the full body reviewed. `rebollo-jd-links.json` inventories seven anchors
and one image; its Google redirect destinations still need decoding for the next
review. Plea-form analysis remains low priority. No Marra person receipt exists yet.

`finish-rebollo-reconciliation.py` checks dated source claims, historical-only fields,
the negative controls against Ashley Beckford/7700, current null fields, page limits,
unchanged judge count, frozen89 hashes/replay and preserved Izquierdo correction.
All89 frozen packets replayed, finalized reports unchanged. Use the frozen packet
for deterministic replay. The county and statewide goal remain incomplete.

## October 16 — Jessica M. Marra, Division JD

Reuse the sources collected during the Rebollo identity review: biography
`2726-2/?smid=2837`, `/division-jd/`, published Google document
`2PACX-1vTAOr82lvZNx1zSYq42_B8KuSToI0fs0DUOImX9AFE-2_bv0iBqEDOfkor9kIpPZgFHNjSzHdjt12dK`
and print document `1s9c3trJMRRBOrJ6ikbIOBuDPi0f0x9KBfs7EQJtz-UI`.
Their acquisition keys start `rebollo-jd-` but their title expressly names Marra,
with an October13,2026 update date. Do not infer ownership from an acquisition key.
Current main DV hub names Tynan45; cached/testtitan Marra45 or old Zoom snippets
do not replace direct current page evidence. Earlier March assignments remain
separate dated statements; no controlling-authority decision is required.

Header identifies Ashley Beckford and named `abeckford@17th.flcourts.org`, shared
`divjd@17th.flcourts.org`, phone7700,NW4850/NW4840. Page2 lists in-court clerk
Aveyanna Lewis,probation officer Alina Hegedus and juvenile clerk phone6492 for
attorneys only. The biography's career narrative is not relied upon for Marra.
Separate JA phone,fax and office hours were not located.

All23,119HTMLcharacters were read in three bounded chunks this review. All12PDF
pages were screened for shared process and visually checked, including the seal.
The earlier partial screening record remains historical. HTML/PDF comparison
normalizes whitespace/U+200B only, retaining originals. Three generated numbered
list markers in the global plea section explain the remaining differences;
page10 visually confirms them. `marra-pdf-comparison.json` records exact differences.
Seven anchors were decoded in `marra-links.json`; one plea-form URL remains link
only. Do not expand juvenile plea/discovery merits beyond the authorized scope.

Capture these individual requirements without importing another division's rules:
- Motion calendar:5–10minutes through JA after opponent coordination, with filed
  motion and notice certifying opponent email notice. Heading says Mon–Thu;
  narrative and schedule say Mon–Fri,09:30. Preserve both.
- Special sets: narrative >10minutes versus heading15minutes or longer. JA requires
  filed motion/proof,service,duration,witness counts,coordination and notice. Notice
  must reach JA within2BUSINESSdays after the FIRST time offered, not confirmation.
- Motion conferral: at least3DAYS before,in person/video/phone; email insufficient.
  Opposition memorandum and courtesy materials use2BUSINESSdays before hearing.
  Page6 says “hard copies” via email; page11 permits emailed courtesy copies.
- Agreed motion/order titles and statements of agreement to proposed language are
  required. No specific Word/PDF format or CMS platform is stated. Opponent may
  object before an order is signed.
- Calendar-call timing differs among everyThursday09:30,Thursdayafternoon and
  everyotherThursday09:30. Continuance deadline is Thursday PRIOR, no hour stated.
  No arraignment/calendar-call add-ons. Cancellation needs JA contact and filed
  notice; order timing says both prior-or-at-hearing and prior, retained separately.
- Attorneys may use Zoom only for non-evidentiary matters. Others need a timely
  written motion and advance ruling; an unruled motion leaves physical appearance
  required. Preserve the standalone-withdrawal motion-calendar juvenile exception.
- Withdrawal filing:10DAYS from awareness or24HOURS if trial/dispositive motion
  already scheduled; proper juvenile notice remains required. Interpreter requests:
  3DAYS generally,7DAYS for other than Spanish/Haitian Creole; copy JA. Emergency
  and urgent requests must first be filed,then emailed with all counsel copied.

Eight discrepancies/ambiguities are recorded, including unspecified lower-priority
trial units/direction; do not invent computed deadlines from those clauses. Use
`person-jessica-m-marra.json`, `marra-discovery.json`, `marra-context.json` and
`history-capture-90.json`. Capture4634/90 has13topics,10timingrules,82validated
citations and1,037artifact readbacks. Replay frozen90. `finish-marra.py` checks
identity,first-offer trigger,units,appearance qualifications,absence of invented
formats,generated-list differences and preservation of Rebollo's separate record.
All90 packets replayed; finalized reports unchanged. County remains incomplete.

## October 16 — Alberto Ribas, Jr., JO/32/JJ

Use the row on the juvenile/dependency hub and biography `2726-2/?smid=2838`.
The actual procedure target is `/Division%20JO32JJ/`; follow its published Google
iframe `2PACX-1vRdDhBnUsgVOeGj_YmcQe01CaW19v3XSy7G5yG805Shm5ADXgph31wJrFmuVcCE92XFgWjUFCuSOVQg`.
No print/edit link was found. Do not invent an export ID or call the separately
located `/wp-content/uploads/2017/10/Div-JO-32-JJ-Procedures.pdf` its print rendition.
March6 assignment order page3 lists both JO/32 and JJ; October chart names Ribas
under dependency. Header/profile/hub agree on Kenndrah Stonom,6907,WW9129/WW9175.
Use full954-831 phone prefix. Named JA email is in HTML header and communications.

Read all14,180HTMLcharacters and use named sections for pinpoints. The HTML footer
has no usable page numbers. Its sole real image is a seal, visually checked; the
second img is empty. One standalone PDF page was read and visually checked. Neither
source states a revision/effective date. Search terms: `site:17th.flcourts.org
"Alberto Ribas" "procedures"`, `"Kenndrah Stonom" email`, and `"Ribas" fax procedures`.
Save search leads, but do not import former JA/2020 closure snippets into contacts.

`ribas-links.json` preserves all12 anchor labels and targets, decoded Google redirects
and the image inventory. One kstonom link targets kstonom, but three later labels
target div32. Save both values; do not silently repair the HTML or infer mailbox
ownership. Clerk exhibit list email is mdulphe@browardclerk.org; evidence division
5537 and Zoom dial-in numbers are not JA contact numbers. Fax5572 appears only in
the undated standalone PDF; keep it source-limited, not current verified contact.
Separate JA phone and office hours were not located.

Individual shared procedure requirements:
- No online scheduling. File motion first, email JA motion/duration and copy all.
- Courtesy filings reach judge at least2BUSINESSdays before hearing. Linked HTML
  permits email; separate PDF requires paper motion/cover letter/materials and
  delivery/mail scheduling. Preserve both without deciding which controls.
- Nonagreed motion certifies conferral or reasonable unsuccessful efforts with
  all affected parties/nonparties, identifying resolved/unresolved issues. No fixed
  interval or email prohibition inferred from another judge.
- Agreed orders require advance circulation/no form objection, motion/agreement/
  petition copy. Footnote2 allows no motion only for an agreed goal-date extension.
- Posthearing orders: circulate, then email PDF after approval or reasonable period
  for objections, copying all and identifying disputes. Signature page includes
  case number/style/title. No invented numeric objection interval.
- Notice governs Zoom/physical/hybrid attendance; permission required to change it.
- Emergency email marks BOTH subject and body, with filed verified motion, good-
  faith certification and duration. Judge/JA decide this court or Shelter docket.
- No add-ons without approval. Cancellation email to JA/all as soon as practicable.
- Exhibit conferral, numerical premarking except impeachment, and LIST to clerk:
  at least2BUSINESSdays before trial/evidentiary hearing. Email conferral allowed.
- After Zoom, file ADMITTED evidence and log within5BUSINESSdays of LOG RECEIPT.
  If original required, moving party coordinates with evidence division within the
  same receipt-based period after hearing. Do not use hearing date as trigger or
  require prehearing filing of all prospective exhibits.
- Termination pretrial ten-day timing stays dependency-specific. Forms statement
  is attributed to source, not independently verified statewide absence. Order
  status goes through clerk online docket; no turnaround guarantee.

Reuse existing shared originals/reviews: `bristol-emergency-2008`, expressly cited
in footnotes; `franker-family-emergency` for dated comparison; `ao-2026-20` for ADA.
2008order cites Civil1.610/Room880. 2019order cites Family12.605/Suite20170 and
family-then-civil-duty assignment, expressly replacing2019-3. Preserve scope and
dates; do not infer a direct repeal or select controlling authority. Literal
magistrate name in Ribas HTML is Lucy Miller; no GM division mapping inferred.

Receipt `receipts/person-alberto-ribas-jr.json`; scripts `ribas-body.py`,
`save-ribas.py`, `finish-ribas.py`; source manifest `review/acquisition.json`.
Capture4638/packet91 stores12topics,5timing rules,3discrepancies,55validated nested
citations and1,047artifact readbacks. Replay `draft/checkpoint-91-frozen.json`, not
the mutable historical writer. `history changes --stream
manual_research:county-baseline-v1:6bf5ac02ab39 --entity
broward-circuit-alberto-ribas-jr` retrieves only this judge's context. Verified source
check does not finalize a report or remove earlier judges' unresolved source gaps.
County remains incomplete; cloud continues with roster verification for Stacy Ross.

## October 16 — Stacy Ross, Division JB

Start with the juvenile roster and biography `2726-2/?smid=2842`. The row links
`/division-jb/`, which explicitly embeds and offers a download of
`https://docs.google.com/document/d/1LDBcCvokRf5mZntaz4kVAlhymLNuvVAp/export?format=pdf`.
This is an actual source href, not an invented Google document ID. Search also
located `/wp-content/uploads/2024/05/JB-Division-Procedures-Ross.pdf`; save separately.
The linked document is four pages; standalone is two. Both lack stated revision
and effective dates. Do not turn2024/05 or PDF metadata into legal currency.

Profile/hub identify Chela Iverson,954-831-7396,NW5820/NW5810,JB andZoom186476648.
PDF text supplies civerson@17th.flcourts.org; visual review confirms extraction's
split domain. The separate letterhead supplies courthouse street/city/postcode.
March6,2026 assignment page3 lists JB Stacy Ross; October chart lists delinquency.
Biography's prior county civil service is not a current civil assignment. The
standalone COUNTY COURT JUDGE heading remains a conflicting source statement.

All six pages visually checked. Full text screened, shared process reviewed;
linked page4 and standalone page2 program merits remain limited. Save originals,
original extracted text, separate whitespace-collapsed readable derivatives and
`ross-links.json`. Linked PDF has no URI annotations; standalone has one matching
civerson mailto. Underlined See Plea Form is not a collected hyperlink: preserve
the unlinked label without guessing a destination or expanding plea review.

Shared-process checklist:
- File motion, copy all, provide JA copy and total hearing time for ALL parties.
  Email preferred. Source says phone calls returned by next business day; record
  as stated service practice, not verified performance or litigant deadline.
- Agreed orders: PDF,email JA/all, descriptive AGREED title and opponent agreement
  in BOTH email and motion. Use agreed language or judge's ruling. Do not infer
  Word,CMS or universal disputed-order format.
- Status requests identify purpose and/or applicable motion. Trials/final VOPs
  are set in courtroom at calendar calls/status. No online scheduling authority
  or numerical conferral interval inferred.
- Continuance: opponent agreement,preferred agreed date,motion/order to JA.
  Petitioning party immediately notifies all participants on signed-order receipt.
  Cancellation email states both agree; disagreement goes to hearing request.
- Prospective Zoom exhibits or motion in limine may prompt requested pretrial
  conference. Give all motion/notice before conference; no numerical deadline or
  automatic remote-evidence permission invented.
- Emergency chain: assigned delinquency judge,then alternate if unavailable,then
  Court Programs Manager at ybrown@17th.flcourts.org for instructions. Written
  motion to all,cover letter with duration,copy assigned JA,reachable phone.
- Courtesy: HARD copies THREE BUSINESS days before hearing are preferred. At
  hearing is minimum. Opponent copies immediately on setting. Preserve all three.
- Advance permission for Zoom,case-management out-of-county/hardship qualification,
  docket-only appearances and separate detention99725122895 at11:00 retained.

Preserve four differences without deciding control: linked North Wing heading
versus West Wing body; standalone county-judge label versus circuit assignment;
detention in-person expectation versus all-party optional Zoom,also evidentiary
should/shall wording; and Girls Court/RISE population descriptions. Program
2019-47-UFC/2021-63-Crim references remain source citations, not claimed new
collections or substantive reviews. No exhaustive diversion/expunction work.

Search terms: `site:17th.flcourts.org "Stacy Ross" "procedures"`, `"Stacy Ross"
"fax"`, `"Chela Iverson" email fax`, and `"Chela Iverson" "civerson"`.
No fax,separate JA phone or office hours located. Other service contacts on page2
remain role-labelled; they do not substitute for JA contact. Reuse shared ADA
`ao-2026-20` with its dates/exceptions, not an invented emergency definition.

Receipt `receipts/person-stacy-ross.json`; `ross-body.py`,`save-ross.py`,
`finish-ross.py`; capture4642/packet92,59 nested citations,1,063 artifact readbacks.
Nine topics,six timing rules,four differences. Replay frozen92,not the historical
writer. Entity context command uses stream
`manual_research:county-baseline-v1:6bf5ac02ab39` and entity
`broward-circuit-stacy-ross`. Preference/minimum,trigger,link inventory,source version
and preservation checks passed; finalized reports unchanged. County incomplete.
The general county workflow now records the extraction and timing lessons above.

## October 16 — Stacey Schulman, JM/30/JH

Official roster/biography `2726-2/?smid=2846` link `/division-30-jm/`.
Follow actual iframe published ID
`2PACX-1vQ0wEYXhf-wahluBe0rbh0gmbehiKRACkwLoROaMAKQVEeJJ8Ao3f78FRn5CgBMwoDF5QRRbCkVq2Qj`.
PRINT link supplies edit ID `13p5OVIQ6jZ8XkogRvjjOmbWEfIBuuoaGVprouka2fTI`;
export that ID to PDF. Header says last modifiedOctober3,2025. Search also finds
`/wp-content/uploads/2017/11/Div30_JM_Procedures.pdf`, expressly datedSeptember28,2017.
Keep separate versions. No separate effective date inferred from URL/revision.

Profile/roster and current header identify Kim Oliva,954-831-7628,
koliva@17th.flcourts.org,WW9137/WW9160,Zoom556448344. March2026 assignment page3
lists JM/30 andJH; Octoberchart/profile name Dependency Chairperson. Current
header says Circuit Civil Judge: retain wording but do not invent another
commercial civil assignment. Fax,separate JA phone and office hours not located.

All11,815HTMLcharacters read, all four linked PDF pages and four historical pages
read/visually checked. CurrentPDF seal checked. HTML/PDF comparison retained in
`schulman-pdf-comparison.json`: header case and footnote extraction placement differ;
no byte identity or automated semantic equivalence claimed. All footnotes manually
checked. Fifteen anchors include matching koliva mailto and fourteen footnote links;
no substantive forms links. Original2017 page1 spells Randi Boven; search snippet
spells Bowen. Use downloaded/visual original, not search text, for the name.

Individual procedure checklist preserves:
- Filed motion/copy all,judge copy with cover letter/email stating duration and
  evidence need. Email subject requires case number,case name,relevant matter.
- Notice determines Zoom/physical; Zoom-noticed hearing not physically heard;
  physical notice requires court permission for Zoom. Test camera AND microphone.
- Current referral names Lucy Miller;2017 names Randi Boven. No GM code inferred.
- Trials/evidence hearings set in court; oral/pretrial-order directions govern
  exhibits. Termination pretrial at least10DAYS before trial,dependency-specific.
- File motion before materials. Current paragraph says courtesy materials FILED
  at least2BUSINESSdays before,emailed copies at least2DAYS before for review.
  Keep exact verbs/units; do not harmonize or substitute another judge's period.
- Conferral certificate: actual inability to resolve OR reasonable unsuccessful
  efforts,with each individual's method,date,time; identify partial agreements.
- All proposed orders Word; posthearing circulate first. Agreed order no-form-
  objection confirmation,agreement indication in title and/or cover letter,
  motion/agreement/petition copy. Footnote4 exceptions are agreed goal-date
  extension AND hearing audio, latter described as grantable ex parte.
- No online scheduling. JA courtesy/cover letter specifies time and evidence need.
- Written continuance/good cause; agreed motion/order may be considered in
  chambers but agreement does not guarantee approval. Otherwise movant sets hearing.
- Emergency copy/cover letter ASAP with duration and emergency marking; verified
  motion/good-faith certification. Judge/JA determine this court or Shelter docket.
- Court approval for double-booking/add-ons; cancellation notice ASAP. Signed-order
  status via clerk online docket instead of JA calls; no invented turnaround.

Historical2017 instructions separately retain paper2businessday copies,original
order plus at least five copies/envelopes,goal-date-only exception,appointment
declination notice/hard copy,discretionary advance-motion telephone appearance,
and pro se Room2140/case-manager8532. Do not promote historical contacts into current.

Current procedure cites2008-60-UFC;2017 cites2015-10-UFC. Reuse saved2008 and2019-9
orders and collect explicitly discovered originals:
`/wp-content/uploads/2017/08/2015-10-ufc.pdf` (two pages,March16,2015),
`/wp-content/uploads/2019/01/2019-3-UFC.pdf` (three pages,January2,2019).
All five new pages read/visually checked; child merits screened, shared emergency
filing/access and non-child provisions reviewed.2015paragraph7 expressly replaces
2008-60;2019-3paragraph7 replaces2015-10;existing2019-9paragraph7 replaces2019-3.
Preserve these exact source statements,Room880/Suite20170 and Civil1.610/Family12.605
differences without selecting controlling authority. New shared review keys
`schulman-emergency-2015` and `schulman-emergency-2019-3` are reusable, not grounds
to rewrite earlier captures. Shared ADA2026-20 review remains associated separately.

Queries: judge full name+procedures,KimOliva+email/fax,judge+fax,and2015-10-UFC,
all restricted to official court host. Search results and actual URLs retained.
Receipt `receipts/person-stacey-schulman.json`; scripts `schulman-body.py`,
`save-schulman.py`,`finish-schulman.py`; manifest `review/acquisition.json`.
Capture4646/packet93:11topics,3timing rules,4discrepancies,72nested citations,
1,086artifact readbacks,five shared sources. `historical_statements` and
`source_sequence` are semantic facts with source citations retained in receipt.
Replay frozen93,not old writer. Use entity `broward-circuit-stacey-schulman`
with stream `manual_research:county-baseline-v1:6bf5ac02ab39` for context.
Literal units,Word format,footnote exceptions,source names/successors and prior
gap preservation checks passed. County remains incomplete; no baseline advanced.

## October 16 — Elijah H. Williams, Division JA

Profile `2726-2/?smid=2853`,roster and `/division-ja/` identify JA/Delinquency
Chairperson. Follow actual published iframe
`2PACX-1vRT-an1d8DHWF6Ookg9WYu2V0b-SveopKwgbKayrdmr9RdQdOG3J80OFEiSoMyj8A`.
Actual PRINT ID `1dQu0XkEapEHmPzszTvr5jN_ABxvpXkd_` exports to three-page PDF.
Search-located separate copy:
`/wp-content/uploads/2024/05/Judicial-Procedures-for-Judge-Elijah-Williams-JHW-1.pdf`
has two pages. Neither states revision/effective date. Do not date it from URL.

Gina Trentacosta,gtrentac@17th.flcourts.org,NW7850 chambers/NW7840 courtroom,
Zoom97660599500. Profile/roster list954-831-6974; current procedure header prints
945-831-6974,visually confirmed. Preserve both,not an unrecorded correction.
Street/city/postcode from retained official clerk North Building address block;
room from profile and North Wing courthouse identified in procedure. Do not copy
clerk phones,fax,hours into chambers record. No separate JA phone,fax or hours found.

All6,402HTMLcharacters read; normalized whitespace/U+200B text equals current PDF.
Both versions read and all five PDF pages visually checked. Six anchors decoded:
Zoom,three matching gtrentac mailtos,ybrown,and one plea-form link. No images.
Plea form remains link-only; do not expand criminal merits review. Search terms
judge+procedures,GinaTrentacosta+email/fax,judge+fax,GinaTrentacosta+gtrentac;
last two searches returned no results,which does not establish absence.

Procedure checklist:
- Zoom non-evidentiary only; physical instruction or either-party objection makes
  physical default unless court decides otherwise. Trials/evidence in person.
  Docket-only participation,proper camera/dress/identification,staff call order.
- Agreed orders emailedJA/all in PDF,descriptive AGREED title; BOTH email and
  motion state opponent agreement,use agreed language or ruling language.
- Disputed hearing request: three BUSINESS days notice,copy motion,total duration
  for ALL parties. Preserve notice wording,do not invent exact trigger/cutoff.
- Status request gives purpose/motion if applicable; trials/finalVOPs set in court.
- Continuance agreement,date,motion/order toJA; upon signed-order receipt movant
  immediately notifies all participants. Cancellation email says both agree;
  disagreement requires hearing request. No fixed lead time invented.
- Email only AFTER opponent communication,copy opponent on ALL communications.
- Current emergency chain: assigned,alternate,then CaseManagement juvenile Programs
  Manager ybrown. Motion/all,cover letter/duration,copyJA,reachablephone. Separate
  PDF goes throughCourtAdministration toCriminalDutyJudge. Preserve both versions.
- Judge hardcopies at hearing are PREFERENCE; opponent copies immediately on setting.
  Separate PDF says opponent first/when possible. No prehearing judge-copy deadline.
- No courtroom photo/video/audio recording,stated juvenile confidentiality scope.
  Family communications route through attorneys and require youth identity/relationship.

Collect `/13-juvenile-drug-court/` original but review only assignment sentence:
Williams currently presides. March6,2026 order page3 lists JA Williams and JE Drug
Court HopeTiemanBristol. Do not infer JE forWilliams or resolve authority; no program
manual/eligibility analysis. SharedADA2026-20 reused with scope/date exceptions.

Receipt `receipts/person-elijah-h-williams.json`; scripts `williams-body.py`,
`save-williams.py`,`finish-williams.py`; capture4650/packet94. Eight topics,four
timing rules,four differences,56nested citations,1,091artifact readbacks. Frozen94
replay,context,source hashes,normalized comparison and prior gap checks passed.
Use stream `manual_research:county-baseline-v1:6bf5ac02ab39` with entity
`broward-circuit-elijah-h-williams`. Source differences do not advance finalized
baseline. County remains incomplete; roster comparison is the next saved task.

## October 16 — Roster reconciliation after 82 individual reviews

Use `review/roster-reconciliation-96.json` and frozenpacket96,capture4658.
This compares the RETAINED October15 public JSON response with82 completed scoped
receipts; it is not a newly fetched roster. `roster-response` acquisition entry
preserves actual200status,retrieval timestamp and POST form. Earlier status-unknown
initial response remains separate. Current raw bytes match both preserved copies.

All96rows accounted for:84matched rows/82people,eight pending named people,three
docket labels and one unnamed62/SB row.92named rows represent90distinct entries.
Duplicate names are Michael Davis and Giuseppina Miranda,not extra people. Exact
multiset of alphabetic name tokens matches every completed receipt uniquely;
no fuzzy aliases were needed. All82receipt hashes/bytes read back from database.

Pending research queue,one person at a time:
1. Stefanie C.Moon,63.
2. Michael I.Rothschild,FG.
3. Andrew L.Siegel,FY.
4. Kevin P.Tynan,45.
5. Michael A.Usan,FX.
6. Francis Viamontes,FO.
7. Marlon J.Weiss,41.
8. Christopher Wigand,44.

Three docket labels:First Appearance Zoom,Division FM In-Custody AM Docket,
Detention Weekday Juvenile. The empty62/SB row requires separate source
reconciliation; do not invent a vacancy/person. Completed identity keys include
50circuit,31county and one senior(Christopher Pole). Octoberchart58circuit/32county
labels do not prove member/classification correspondence. Magistrates/hearing
officers,clerk,material shared procedures and known missing originals remain in
the county worklist. Eight pending names is not all remaining county work.

Capture4654/packet95 accidentally included receipt paths/hashes inside compared
rows. Preserve it. Capture4658/packet96 moves that provenance into receipt matching
evidence; semantic rows retain name,division,classification and stablejudgekey only.
This is an evidence-maintenance correction,not a personnel/legal change. Do not
rerun old writer95 after correction. Replay frozen96. `finish-roster-96.py` verifies
the difference is only those metadata fields,mutates receipt provenance to ensure
the projected semantic rows are unchanged,and checks all82receipt artifacts.

Save scripts `save-roster-progress-95.py` (historical) and
`save-roster-progress-96.py`; verifier `finish-roster-96.py`.
Current entity `broward-roster-progress`,stream
`manual_research:county-baseline-v1:6bf5ac02ab39`; context `roster-96-context.json`.
Corrected capture stores1,174artifacts; readback,duplicate-save,frozen replay and
context checks passed. Sourcecheck verifies this partial accounting,not county
completion or freshness. Finalized reports unchanged. State now includes the
remaining named queue; research resumes with Moon only after roster/profile check.

## October 16 — Stefanie C. Moon, Division 63

Official profile `2726-2/?smid=8349` and Domestic Violence hub agree: Leslie Sparks,
954-831-7710,WW10135 chambers/WW10155 courtroom,Zoom815731156. Follow `/division-63/`
and its actual Google published iframe. No PRINT/edit link found; do not invent
an export ID. Header supplies West Tower,201S.E.6thStreet,FortLauderdaleFL33301;
sectionIV supplies **division** email div63@17th.flcourts.org. Do not label that
as a personal assistant email. Former private-practice search contacts are not
chambers contacts. No current fax,separateJAphone or officehours located.
March6,2026 assignment order page3 footnote4 assigns Moon BSO-petitioner RPOs;
preserve that dated association without expanding firearm merits research.

All10,637HTMLcharacters read; revisionFebruary15,2026, no separate effective date.
Thirteen anchors: six matching division mailtos,one compliance-monitor mailto,
six external links. One downloaded image visually confirmed as Florida seal.
Three English/Spanish/Creole general handouts remain link-only. Firearm/program
sections reviewed for routing, not merits. Clerk emergency numbers5570,5520,5579
and compliance-monitor7278/email belong to those services, not the JA.

Procedure checklist preserves: efile plus **filed AND accepted** motion emailed
with hearing-duration cover letter; body certification of conferral OR attempted
conferral; judge controls hearing setting; no agreed orders without leave and no
attorney cancellation authority. Filing does not alter pending orders/docket.
No-coverage status report must be filed/accepted and emailed by **noon the prior
business day**, with specified preparation subjects. Audio/video to division
**two business days before final hearing**; conditional Zoom attorney Notice of
Filing **two business days before hearing**. Alphabet LETTER exhibit premarks,
case/style/hearing identity,opponent copied. Preserve both statement that clerk
cannot accept multimedia and instruction to deliver ALL evidence on USB to the
in-court clerk at hearing; do not invent an exception. ProfileZoom does not itself
authorize all remote appearances. No order-file format or generalcourtesydeadline
inferred. Withdrawal orders contain clientpostal/email/phone and specified
**five days** counsel/pro-se language; no business-day or separate trigger inferred.

Emergency requests verified/certified,throughclerk,notJA; retained2019-9 source
reused. AIsection citesAmendment1; priorJanuaryURL404 reused,Apriloriginal available.
RetainedAmendment2 expressly replacesA1; 2026-19 vacatesA2 June15,2026at12:01am.
Remote2020reference kept distinct from2022successor statements. No determination
of which individual/shared source controls; no repeatsearch to resolve authority.

New linked `/wp-content/uploads/2022/10/2022-12-UFC_Amended.pdf`: full11pages
collected, only1,6–9read/visuallychecked. October25,2022signature,expressreplacement
of unamended2022-12. CivilDV related-case assignments,transfer coordination and
Rule2.545(d) relatedcasenotice retained. Less/morethan12monthstext not converted
to an invented exactly12months rule. Otherpages remain unreviewed. IndividualXI
says relatedfamilyfile/reopening leads to15dayreturnhearingtransfer,allattend;
specialsethearing requires chambersnotice inadvance. Keep that alongside the
plan's conditional assignments,not a general commercial-case transfer rule.

Receipt `receipts/person-stefanie-c-moon.json`; `moon-body.py`,`save-moon.py`,
`finish-moon.py`; capture4662/packet97. Twelve topics,five timing rules,three
differences,90citations,1,098artifactreadbacks,615sourceentries. Nine shared sources
associated with retained dates/scope. Frozen97 replay and entitycontext verified;
no finalizedbaselineadvanced. Entity `broward-circuit-stefanie-c-moon` in stream
`manual_research:county-baseline-v1:6bf5ac02ab39`. Next RothschildFG; county incomplete.

## October 16 — Michael I. Rothschild, Division FG

Use retained Circuit Criminal hub, profile `2726-2/?smid=2843`, `/division-fg/`,
and its actual Google published iframe. No PRINT/edit link found. Current sources
agree Kim Cox,954-831-7888,NW4820/NW4810,Zoom712673701. Header supplies courthouse,
201S.E.6thStreet,Suite4820,FortLauderdaleFL33301. SectionI publishes **division**
email divFG@17th.flcourts.org; special-set text uses lowercase divfg. No personal
JA email or separate phone inferred. March6,2026 assignment page2 confirms FG.

All19,516HTMLcharacters screened; shared procedure reviewed. Five actual anchors:
two visible Zoom fragments incorrectly target419713883, three criminal forms
(plea,DNA,VOP) retained as links only. Save visible and actual destinations; do not
silently repair or test the Zoom meeting. One downloaded image has the same SHA256
as the Florida seal visually inspected for Moon; no extra instructions in image.
Body says last modifiedMarch9,2026; footer7/14/26MIR/kc has no date-role label.
CMS availabilityOctober1,2025 is another distinct date, not a new observation date.

Shared process checklist:
- Contact JA, not judge; email preferred, copy opponent/necessary parties. Written
  ex parte correspondence goes in court file. SectionIX questions/concerns language
  does not establish permission for private case contact.
- Eligible morning motions throughCMS, five-minute cap, opponent coordination and
  filed notice; JA excluded from coordination unless absolutely necessary.
- Special sets: preferred JA email after coordination, total time for both sides
  and witness availability. Court receives/reviews motion before offering dates.
  Do not include JA on interparty availability discussions. Notice required unless
  opponent waives; overrun can be rescheduled/bifurcated.
- Zoom nonevidentiary; evidence requires BOTH parties' agreement. Presenting party
  handles witness technology; no technical delay unless absolutely necessary.
- Calendar call generally10days before trial. Factual/evidentiary motions heard
  before announcing ready OR between call and trial; not on trial day. Pretrial
  evidence review, objections, stipulations and scheduling preparation retained.
- Agreed motion states agreement; order heading Agreed Order; no hearing unless
  court requests. Party prepares no-findings orders; court prepares findings and
  legal-interpretation orders. Withdrawal motion/notice service and substitution
  authorization are preserved with their defendant-specific scope.
- CMS electronic orders only agreed/prior-hearing matters, Word; motion attached
  OR filed-date referenced, motion prefiledCMS, all parties registered for service.
  Check style/case/judge/jurisdiction/date. Nonmerits rejection repair within24hours;
  Friday rejection byMonday5PM. Traditional submission remains allowed unless
  court orders otherwise; pro se JA assistance/paper. Repeated failure can barCMS.
- Written continuance motion/order byTuesday before calendarcall; afterward only
  emergency written motions. Granted:notifydefendant; denied:attendcall.
- Evidentiary cancellation:notifyJA as early as practicable; agreedorder BEFORE
  cancellation with court. No fixed notice hours invented.
- Pleading/case-law courtesy copies at least **two days**, not business days,
  before hearing; paragraph does not supply delivery medium.

Targeted fax search found `/wp-content/uploads/2017/10/Div-FB-Procedures.pdf`:
four pages collected, onlypage1 read/visuallychecked. Expressly effectiveJanuary1,
2018, DivisionFB, Suite4880, DIVFB email, fax954-831-7899. Preserve historical
contacts; do not fill current FG fax with that number. Pages2–4 not reviewed;
no exhaustive old criminal procedure analysis. Retained sharedADA review reused.

Receipt `receipts/person-michael-i-rothschild.json`; `rothschild-body.py`,
`save-rothschild.py`,`finish-rothschild.py`. Capture4666/packet98, ten topics,
six timing rules,three source differences,55citations,1,104artifact readbacks.
Frozen98 replay and entity context verified, prior corrections/gaps and finalized
reports preserved. Entity `broward-circuit-michael-i-rothschild`, stream
`manual_research:county-baseline-v1:6bf5ac02ab39`. Next SiegelFY; county incomplete.

## October 16 — Andrew L. Siegel, Division FY

Use retained Circuit Criminal hub,profile `2726-2/?smid=2801`,`/division-fy/`,
and actual Google iframe. No PRINT/edit link found. Current profile,hub,individual
procedure and March6,2026 assignment page2 agree FY,Sabrina Albert,954-831-6348,
NW7760/NW7750,Zoom516621248. Individual header publishes division email
divfy@17th.flcourts.org. Street/city/postcode from retained clerk North Building
address block; chambers from profile,North Wing identified by procedure. Do not
copy clerk contact/hours to judge. No current fax or separate assistant phone found.

All8,897HTMLcharacters read/screened,shared process reviewed. Search-located
`/wp-content/uploads/2024/05/Div-FY-Procedues-5-24-24.pdf` has three pages,all read
and visually checked. Neither source states revision/effective date; do not date
it from filename. HTML has one plea-form link,no images; form remains link-only.

Procedure checklist:
- Short5/10minute motions throughJA,usually weekdays8:30. At scheduling motion
  filed,copyJA,previously copyopponent. Coordinate first; notice toopponent/JA.
- Special sets heading says10minutesORMORE,bodyMORETHAN10. Preserve ambiguity,
  not automatic exactly10minute classification. JA,usually weekdays13:30; same
  filed/copy/coordination prerequisites,estimatedtime. No CMS permission inferred.
- Setting emails copyopponent; excludeJA/court from interparty witness/issue emails.
- Status Zoom default; no bond/release/withdrawal or in-custody cases. Evidence
  requires priorcourtapproval. Calendar calls and specified VOP hearings physical.
- Status defendant waiver requires filedwaiver AND counsel communication within
  preceding10days. Friday8:30 status/call schedules remain source-specific.
- Agreed Motion/Agreed Order titles,stateagreement,submitJA,no hearingunlesscourt
  requires. No Word/PDF format invented.
- Continuance motion/order beforestatus; disputedhearing; deniedphysicalattendance.
- Cancel/resetthroughJA,notifyopponent. Agreementorder **before OR at hearing**.
- Interpreter individual JAemail3DAYS general/7DAYSotherthanSpanishCreole,also
  interpreterofficeemail. Shared2026-11 CMSform/2BUSINESSdaysSpanishCreole/7daysother
  and late online-plus-phone requirements remain separately attributed.
- Individual AI tool-identification and attorney-verification text retained with
  separateA2/2026-19vacatur evidence; no finding that individual policy was revoked.
- Questions/concerns/emergencies throughJA with opponent/prose/necessaryparties.

Version comparison: PDF arraignment waiver writtenplea+discovery demand versus
HTMLnoticeofappearance+writtenplea. PDF calendar call has speedywaiver alternative;
HTML first-hearing statement does not. HTML adds10daystatuswaiver and expresses
short-motion filing/copy prerequisites; PDF explicitly gives those forspecialsets.
PDF continuance beforestatusORcalendarcall versus HTMLbeforestatus. HTMLAI/agreed
heading requirements absent from separatePDF. Preserve dates as unknown and do not
choose control. Criminal merits/forms not exhaustively reviewed.

Retain historical Salbert@17th.flcourts.org from already-collected temporaryCOVID
docket physicalpage2,other-jurisdictionparagraph; not currentpersonalemailconfirmed.
Only contact/assignment paragraph reviewed for this judge; no expandedcriminal
analysis. Retained Porth PDF **physicalpage7**, printedPage6of7 mid-paragraph,
names Siegel alternate if Porth absent/docket suspended. That paragraph alone was
reviewed/visuallychecked forSiegel; don't import Porth's broader procedures.

Receipt `receipts/person-andrew-l-siegel.json`; `siegel-body.py`,`save-siegel.py`,
`finish-siegel.py`. Capture4670/packet99,ten topics,six timingrules,four differences,
78citations,1,117artifactreadbacks,626sourceentries. Four shared source reviews
reused with dates/scope. Frozen99 replay/entitycontext and source assertions passed;
prior corrections/gaps and finalized reports unchanged. Entity
`broward-circuit-andrew-l-siegel`,stream
`manual_research:county-baseline-v1:6bf5ac02ab39`. Next Tynan45; county incomplete.

## October 16 — Kevin P. Tynan, Division 45

Use DV and Unified Family hubs, profile `2726-2/?smid=17697`, `/division-45/`,
the actual published iframe and PRINT document ID
`1Ae7vDcC7AtrpC9vb3aesMi-RG5si4rDIPZGQCRfntGQ`. Current sources agree Alicia Ray,
954-831-7704,WW10133/WW10160,Zoom84066218747; procedure supplies division email
Div45@17th.flcourts.org and courthouse address201S.E.6thStreet,FortLauderdale33301.
No separate personal JA email,phone,fax or hours found. Older Alicia Ray contacts
for other judges are not current Tynan contacts.

August3,2026 HTML17,932characters and nine-page print PDF reviewed. Separate
`/wp-content/uploads/2024/03/Judge-Tynan-Div-45-Procedures.pdf` is seven pages,
datedJanuary4,2024. All16 pages visually checked. HTML/PDF normalization leaves
14 list-number/letter insertions only; exactdiff retained. Do not claim complete
normalized equality. One seal image inspected; eight anchors include three
general translation handouts retained as links only. Generic flcourts homepage
is not proof of a downloaded specific form.

Procedure checklist and timing:
- All matters special set; no motion calendar. Court controls setting/cancellation.
  Zoom requires leave. Communications in court or division email copied to all.
- Pro-se motion filedRoom2140 or efile; email filing proof/motion todivision/all.
  Attorney motion body requires conferral/attempt certification, filed/accepted
  copy and duration cover letter. Separate live conferral by arguing attorneys
  at least **five days** before hearing; inperson/Zoom/phone,notemail.
- Without available coverage counsel, filed/accepted status report emailed by
  **noon the preceding business day**, addressing the specified preparation topics.
- Continuance identifies hearing and opponent positions. Original hearing remains
  on unless court rules. Withdrawal requires consent or service and prescribed
  **10-day** counsel/pro-se order language; filing alone does not withdraw counsel.
- Other pre-judgment/discovery motions written,notoretenus. Initial return hearing:
  **72hours before OR24hours after retention,WHICHEVER IS LATER**,absentgoodcause;
  courtesy copies,cover letter and hearing date in email subject.
- Later motion: file **10days after last hearing**; **schedule within30days** of
  last hearing. Hearing need not occur within30days. Response **10days before**;
  memorandum attached and case-law copies CMS **48hours before**. Court may adjust.
- Current emailed orders **Word**; 2024 ordinaryCMS and email **PDF AND Word**.
- Four evidence copies,alphabet premark,own playback equipment and retainable media.
  At-hearing evidence,notadvance/efile. Zoom NoticeofFiling **2BUSINESSdays**;
  2024 approvedremote exhibit/audio CMS **2DAYS**,notemail. Preserve versions.
- Pretrial notice controls mode; pretrial order deadlines cannot change by party
  agreement without leave. Dismissal notice/acceptedreceipt and hearing details
  todivision; pro-se petitioner filing rules distinguish petitioner’s counsel from
  respondent’s counsel. Related-family transfers and required notice retained.
- Emergency verified/certified,clerk route,notJA. Current pro-se inperson versus
  2024 inperson/efile/mail. Header2015-10 and body2019-9 preserved with retained
  express2015→2019-3→2019-9 replacement statements; no control adjudication.
- Conditional RPO process: source14-day final-hearing statement,simultaneous petition
  email,operational laptop for orders,service of allegations rather than only
  setting order,petitioner ensures held respondent attendance,written advance
  extension requests. No independent firearm/imminence merits analysis.
- Historical2024 return-firearm routing includes optional court letter allowing
  15days response plus10days if USmailed; not treated as a current calculated date.

Discrepancies: current header literally KENIN versus profile/oldPDF Kevin; March6
assignment TynanFamily36/Marra45 versus current rosters Tynan45. RPO procedure
does not prove all-RPO assignment or override March Marra/Moon split. Current
monitor email `compliancemonitor@17th.fl.courts.org`,old
`compliancemonitor@17thfl.courts.org`,retainedMoon
`compliancemonitor@17th.flcourts.org`: preserve literal spellings,not auto-correction.
General status clerk5770/5570/5579 differs from emergency5570/5520/5579; distinct
service fields,not chambers phones. Specialized merits/translation handouts not
exhaustively reviewed. Conflicts do not block this completed individual review.

Receipt `receipts/person-kevin-p-tynan.json`; scripts `tynan-body.py`,
`save-tynan.py`,`finish-tynan.py`; capture4674/packet100. Fifteen topics,13timing
rules,eight differences,124citations,1,140artifactreadbacks,633sources,seven shared
reviews. Frozen100 replay,entitycontext and source assertions passed. Prior
corrections/gaps and finalized reports preserved. Entity
`broward-circuit-kevin-p-tynan`,stream
`manual_research:county-baseline-v1:6bf5ac02ab39`. Next UsanFX; county incomplete.

## October 16 — Michael A. Usan, Division FX

Retained Circuit Criminal roster: select exact full name **Michael A. Usan** and
division **FX**. SubstringUSAN incorrectly matchesSUSAN Alspector. Original procedure
href `//www.17th.flcourts.org/division-fx-procedures/` must be resolved withurljoin
against the actual source URL; do not pass protocol-relative href to curl directly.
The initial invalidURL failure and repair are in `review/usan-discovery-errors.json`.
No Alspector source was fetched or attributed as Usan. Biography smid2851; actual
PRINT ID `1WMD6fhsZaQxhIS25Rs_r_euDozYRU12nbSr7pctTvQo` exports three pages.

Current roster/profile: Debra Marshall,954-831-1678,NW7820/NW7780,FX,Zoom96220495954.
Procedure says **Debbie** Marshall and dmarshall@17th.flcourts.org. Preserve both
name spellings. North Building street/city/postcode from official clerk address
block; current profile chambers and procedure NorthWing identify location. No
separate JAphone,fax or hours found. Do not copy clerk hours/contact into chambers.

All7,927HTMLcharacters and three-pagePDF reviewed; normalized whitespace/U+200B
text equality verified,allpagesvisualchecked. No anchors/images or PDFannotations.
Source says pleaform linkedbelow,but none exists in checked HTML/PDF; recorded as
referenced without link,not downloaded/reviewed. No criminal-form search expansion.
Separate `/wp-content/uploads/2024/03/Judge-Usan-Procedures-for-Div-FP-3-20-24.pdf`
is one page,read/visuallychecked; two matchingdmarshall mailtoannotations. Neither
procedure states revision/effectivedate. URL/filename dates not substituted.

Shared procedure checklist:
- JA5–10minute hearings Monday–Thursday9:30,coordinateopponent,notice toJA/opponent.
- Special heading10ORMORE,shortparagraph>10; JAusuallyThursday13:30. Filedmotion,
  JA/previousopponentcopies,estimatedtime,availability and notice required.
- CMSspecific≤5minute matters Monday–Wednesday9:30. CMSparagraph separately says
  >15minutes or earlierdates contactJA; no6–15minute CMS permission inferred.
- Listed motions may be emailed with motionANDorder; no fileformat specified.
- Fridaycalendarcall9:30 Zoom withoutarrangement. Monday–Thursday nonevidentiary
  pretrial≤30minutes only,priorarrangement andwrittenmotion≥48hours. In-custody
  attorney inperson. Identifycounselrole,muteuntilcalled. SeparateFP PDF says
  Fridayonly/no weekdayZoom and number883035672; currentparagraph itself saysFP
  despite FXheader/roster/Marchassignment. Preserveall source statements.
- Continuance motion/order by2PM daybeforecalendarcall,disputedrequireshearing;
  grantednewdate,deniedattend. No business-day modifier supplied.
- Courtesy copies email,USmail,7th-floor reception mailbox; no fixedleadtime.
- Cancel/resetJA/opponent; agreedorder beforeORathearing.
- InterpreterJAemail3DAYSgeneral/7DAYSotherthanSpanish/HaitianCreole,alsooffice;
  shared2026-11CMS/2BUSINESSdaysSpanishCreole retained separately.
- Questions/communications/emergencies viaJA phone,email,writing.

Retained Porth physicalpage7 alternateparagraph lists Usan ifPorthabsent/docket
suspended; reused scopedassociation only. Historical2024 appellatepanel search
lead not treated as currentcivilassignment or independentlyreviewed. Criminal
merits unexpanded. Sourceconflicts do not block completed scopedreview.

Receipt `receipts/person-michael-a-usan.json`; `usan-body.py`,`save-usan.py`,
`finish-usan.py`; capture4678/packet101. Ten topics,six timingrules,five differences,
68citations,1,140artifactreadbacks,638sources,two shared reviews. Frozen101 replay,
entitycontext and source assertions passed; prior corrections/gaps and finalized
reports preserved. New roster helper ten tests passed and was exercised against
retained actual HTML; result `review/usan-roster-helper-validation.json` includes
source/helper hashes and matched destinations. That is local workflow validation,
not a new live roster fetch. Next ViamontesFO; county incomplete.

## October 16 — Francis Viamontes, Division FO

Use the retained Circuit Criminal roster with the full-name/division helper.
Biography smid14573; actual procedure link is directly to Google edit document
`1CmrBNqEJPNpUt83RhjRHu2AmJwgDTSbmsfTQ98V166U`. A mistaken iframe assumption
raised TypeError before fetching the document; exporting that exact linked ID
returned nine pages. Viewer shell title July10,1:22PM is not a legal date.
Procedure expressly effective February23,2026. All nine pages screened and
visually checked; shared procedure reviewed, criminal merits not exhausted.

Profile Gregory Patrick Woods II; procedure Gregory P. Woods II;954-831-7785;
chambers NW6850, courtroom NW6750. Procedure division email divfo@17th.flcourts.org
is the JA contact route. Profile visible/mailto div33@17th.flcourts.org retained
separately. Address201S.E.6thStreet,FortLauderdaleFL33301; Zoom335631889 is not
permission to appear remotely. In-court clerk says TBD. Separate felony clerk
6565 and attorneys-only5600 numbers are not chambers numbers. No separate JA
phone, fax or hours located. Do not map flattened prosecutor/defender columns
or off-page annotations to the JA.

Shared procedure findings:
- Motion calendar Mon/Tue/Wed/Fri9AM, generally5–10minutes; five-minute matters
  through JA after coordination, attorneys may also set directly on CMS.
  Filed motion and notice to JA, notice certifies opponent received email;
  no notice means cancellation. First-come scheduling.
- Special sets through JA weekdays10:30–16:30; heading10minutes or longer,
  earlier paragraph morethan10minutes. File motion first, supply relief,
  service, duration and witness count EACHside. JA reviews and offers time.
  Notice toJA within2BUSINESSdays after time FIRST OFFERED, not after confirmation.
  Movant coordinates/serves; notice date/time/duration and motion required.
- Review documents at least48hours before specialset. Dropoff receptionbehind
  sixth-floorNorthWingelevator. Paragraph calls chambers6750 despiteheader6850;
  specialsetparagraph sayscourtroom5780 despite6750 elsewhere. Preserve all.
- Default physical; specialsetevidentiary physical. Custody excludesZoom and
  requirescounselphysical. Otherhearings MAYZoom byadvanceJArequest,specificmatter.
- Calendarcall bodyThursday9AM; tableThursdayand/orFriday. Arraignmentbody
  Mon/Tue/Wed versus tableincludingFriday. Writtenwaiver ANDrecentclientcontact;
  no numerical recent-contact interval supplied. Trial generallytwo-weekwindow
  followingMonday ifready, orspecialset.
- Agreedcontinuance motion as supportingdocument withorder CMSWorkbench by
  Tuesday3PMbeforecall. Disputedsethearingorcall; grantednewdate,deniedattend.
- AgreedMotion titleANDbody plusagreementstatement; AgreedOrder heading.
  Usuallynohearingunlesscourtrequires. No genericWord/PDFformat inferred.
- Cancel throughJA, agreedorderbeforeORathearing; attendifnonebefore. Entered
  order alone doesnotcancel hearing. InterpreterJA3DAYSgeneral/7DAYSotherlanguages;
  sharedCMS2BUSINESSdaysSpanishCreole remains separate.
- Actualadmittedexhibits, letterbeforeadmission/numberafter; pretrialstipulations,
  notices,challenges andinstructionconferral encouraged withoutfixeddeadline.
  Noexparte; professionalism andpartyresolution expectations retained.

Page9 six plea/VOP/DNA forms: exact links retained, not downloaded or reviewed.
AOI94 old2017link retained404; official2026repost alreadycollected/reviewed.
ExactOctober2019Barhandbook retained403 remains missing-original queue; separate
Augustv2 reused with its limited page review, not deemed the exact document.
Shared source reuse preserves original timestamps and does not claim a fresh probe.

March6,2026 assignment physicalpage2 clearly FO FrancisViamontes, FP Marina
Garcia-Wood. Flattenedtext misleadingly puts FP next toFrancis; visual and PDF
word-coordinate checks confirm alignment. Record extractionissue, not authority
conflict. Screenshot retained as `review/viamontes-assignment-page-2.png`.

Receipt `receipts/person-francis-viamontes.json`; body/save/finish scripts under
`review/viamontes-*` and `review/save-viamontes.py`, `finish-viamontes.py`.
Capture4682/packet102;10topics,6timingrules,6discrepancies,91citations,641sources,
1,151artifactreadbacks,four reused shared reviews. Duplicate-save,frozen102 replay,
entity context and source assertions passed; prior corrections/gaps and finalized
reports unchanged. No CMS/Zoom/contact/browser operations tested. Next Weiss41;
county incomplete, no nextcounty before user review.

## October 16 — Marlon J. Weiss, Division41

Use exact full-name/division against retained family-hub with roster helper.
Biography smid22401; wrapper `/division-41/`; actual published Google document ID
`2PACX-1vQkqQPYijI-hQ1dEZBd9l-bAn99Fn_vjnEtQhTCW3kY3tOeLru0r6eI358zgy0WC4cFkze-Mmy6E6fT`.
Full49,746characters read,includingRUCDaffidavit; updatedJuly7,2025. Wrapper and
document have no PRINT/exportlink. BrowserlocalPDF21pages is derived,notoriginal;
visualpages1,2,13,14,15,19 inspected withtoolbaroverlaplimitation. CiteoriginalHTML
section/offset quotations. Browserclosed; CMS/Zoom/contactoperationsnot tested.

StephanieLee/profile versusStephanieA.Lee/procedure;954-831-7576;
Div41@17th.flcourts.org divisioncontactroute;WW11138/WW11152 versusprocedure
WW11-138/WW11-152. 201Southeast6thStreet,FortLauderdaleFL33301;hours8:30–17,
lunch12–13:30. No separateJAphone/faxfound. ProseCaseManagement8532/ufchelp,
CMSsupportcalendar separatefromchambers. Allcorrespondencewritten,case/style,
allparties,samethread; noarguments,exparte,duplicateemails orschedulingdebates.

Twenty structured topics and16timing rules include:
- UMC5min/no testimony/12slots;MonWedThu9–10,Tue9–9:30,Fri9:30–10Zoom.
  Headernoticed8:45/actual9 retained. Special>15minutesORevidence;6–15gapnotfilled.
- Oralconferral,unilateralafter2FULLBUSINESSdaysnoresponse OR3failedattempts;
  specifiednoticelanguage. Specialrequestfiledmotion/date,totalbothsidetime,
  urgency/conferral/allemails; waitforJAconfirmation, noadd-ons.
- GeneralnoticeANDmotionCMS2DAYSaftersetting versusrepeatednocopylanguage;
  response2BUSINESSdaysbefore. Courtesybeforeorathearing versuscancellation
  sectionCMS2DAYSbefore. Witness/exhibitlistsfileANDexchange5BUSINESSdays,
  premarkedexhibits/liststoCourtCMS2BUSINESSdays. Hardcopies/USB,notscreens.
- HeaderDVreturnZoom versusbodyallDVphysical. 30minute+physicalunlessordered;
  custodyphysicalJune23,2025; GALexceptionwithadvanceJAnotice; otherexceptions
  motionfiled/setUMC. Trialletters versussharednumericmarking preserved.
- UMC/CMCorders2BUSINESSdays;special/trial10DAYS. ONEredlinedWordorderONEemail
  fordisagreement; generalcompetingemailwordingretained,separatefromspecificban.
  Agreedverificationrequired;income-withholdingemail,DVCECMSonlyleave.
- Trialreadinessafterdiscovery/impasse;jointstipulationwithin5BUSINESSdaysprior
  versusshared5days. PTCapproximately2weeksbefore/allZoom;continuanceUMC≥5BUSINESS
  days/clientconsent,exigentwaiver. CMCcancelrequiresorder; disputedroutesdiffer.
- Temporaryreliefmediation5DAYSbefore;general1hourcap versussharedchildsupport
  normally30minutes. Withdrawalclientregistration2DAYSaftersignedorder.
- DVinterpreterJA7days/ownothers versussharedCMSdirections. Rehearingefile,
  emailcopy,literalsubjectREHEARING/RELOCATION,nohearingwithoutauthorization.
- EmbeddedRUCDaffidavit/requestpackage reviewed,includingnotarization,
  requiredID/disclosuresandexactjudgmenttitle; nottreatedascompletedcasefiling.

September8 circuitannouncement saysappointmentSeptember4. OfficialFourthDCA
article expressly effectiveDecember1,2026. Preservefutureassignment,no current
appellatecontacts inferred. OriginalDCAHTML extractor returnednavigationonly;
bodyis`__NEXT_DATA__.props.pageProps.pageData.body.html5`. Newboundedhelper
`scripts/flcourts_article.py` parsesJSONwithoutscript execution. Originalhash/time
unchanged; shellextraction andderivedbodyseparate. Eighthelpertests plus10roster
tests passed; initialfixtureincorrectlyembeddedclosing-scripttag,correctedto
validescapedJSON. Actualretainedsourcecheckmatchedandhashessaved.

AssignmentMarchorderphysicalpage4visually41MarlonWeiss,42JamesHarris;
flattened42nexttoMarlonisextractionartifact,notconflict. OldLocalRule10A,
rehearingandefilinglinked404pathsretained; officialalternatereviewsreusedwith
priorretrievaldates. Bailey'shistoricalDivision41PDFnotattributedtoWeiss.
Eleven sharedreviews; noauthority-resolutionproject orfreshnessclaimfromreuse.

Receipt`receipts/person-marlon-j-weiss.json`,body/save/finishWeissscripts,
capture4686/packet103:137citations,647sources,1,162artifactreadbacks. Save/replay,
entitycontext,source-specificfactchecksandpriorgap/finalizedpreservationpassed.
NextWigand44;countyremainsincomplete.

## October 16 — Christopher Wigand, Division44

Select the exact Christopher Wigand/44 row from retained family-hub with the
roster helper. Biography smid18772; wrapper `/division-44/`; published Google ID
`2PACX-1vSwzqQ2GwHia5cCtjjM7EfFXY4xRxNm8IGNnwAfgv63iwQWbhKhX_uNssBEQnhAnY-FET_LjMk6kECR`.
All47,017 extracted characters were read, including RUCD affidavit, calendar,
AI and digital-evidence sections. Heading says updatedMarch6,2026 to address
electronic evidence. No official PRINT link located. Live element screenshots
visually confirm the contact table, all12 calendar rows, AI certification and
digital-evidence paragraph. This does not claim a full-page layout audit.

Patti Milcent;954-831-7044;Div44@17th.flcourts.org. Profile WW11137/WW11158;
procedure11137/11158, with location specifying West Wing.201Southeast6thStreet,
FortLauderdaleFL33301. Hours8:30–16:30,lunch12–13:30. Interpreter fax7279 and
office7290 are separate service contacts, not chambers. No separateJAphone/fax
located. The current UMC cancellation paragraph still names Ms.DelPonte; record
that discrepancy rather than replacing the verified header/profile name.

Distinct requirements retained:
- Motion/notice CMS within24HOURS after setting; responses2BUSINESSdays before.
- UMC Mon–Thu8:45–9:30,represented litigants,5minutes/no testimony; setting at
  least5DAYS before. Oral OR written conferral includes email/text. UMC orders
  within48HOURS after hearing, not the preceding judge's two-business-day rule.
- Special sets >5minutes or evidence. Accepted stamped motion,time,priority,
  conferral details and evidentiary indicator. Two rounds of three offered dates,
  then Court chooses; separate no-response2FULLBUSINESSday unilateral option.
  JA confirmation before notice; no add-ons. Special orders2DAYS unless ordered.
- Requested deferred-ruling orders by email2DAYS after hearing/5DAYS aftertrial.
  Each party's separate Word.Doc order/cover letter and ONE combined TrackChanges
  document directions both retained. Fallback underline petitioner language,
  italic respondent language. Agreed verification; withholding orders email.
- All evidence hearings/trials physical; >30minute nonevidentiary physical.
  UMC/CMC/calls Zoom; attorney video unless advance telephonic permission.
  Published Zoom930694338 differs from one-tap562237373; no connection tested.
- Trial readiness requires impasse; new trial counsel after prior mediation
  requires mediation again. Joint stipulation5BUSINESSdays prior, with separate
  unilateral-explanation paragraph; shared trial form rejects unilateral.
  Twelve calendar rows retain exact source cells and ISO dates. No case assigned.
- Digital evidence may replace paper on USB; bring a computer to remove
  unadmitted material from the submission copy and rename admitted exhibits.
  Original evidence is not deleted by this task. Separate judge trialUSB is
  preferred, not mandatory. Trial identification letters, clerk admission numbers.
- Withdrawal registration2DAYS after signed order. DV interpreterJA7days;
  sign-language/ADA7days when possible; shared2026CMS provisions separate.
- Rehearing subject literallyREHEARING/RELOCATION. RUCD package and embedded
  notarized affidavit reviewed. DV Wednesday10–17,physical. Individual AI
  on-face disclosure and personal accuracy certification remain published;
  circuit2026-03 amendments and2026-19vacatur are separate dated evidence.

Optional2024procedure search lead returned404; search snippets were not used as
verified historical contacts or procedure. Generic family forms/resource links
are retained, not recursively reviewed. Initial anchor inspection hit a name-only
anchor without href; filtering nonempty external hrefs repaired discovery.
Retain internal fragments as navigation, not guessed download destinations.

Receipt`receipts/person-christopher-wigand.json`; body/save/finishWigand scripts.
Capture4690/packet104:21topics,15timingrules,7discrepancies,12calendarrows,
121citations,651sources,1,164artifactreadbacks,14sharedreviews. Duplicate save,
frozen104 replay, entity context and source assertions passed. Prior corrections,
missing-original queues and finalized reports unchanged. Browser closed normally;
no CMS,Zoom,filing or contact operations tested.

The named-judge queue is now empty at90 reviewed people. This is not complete
county coverage. Next reconcile roster classifications/blank62SB and inventory
magistrates/hearing officers, then finish clerk/material procedures/gaps and the
county review checkpoint. Do not rerun historical roster96 finalizer or overwrite
its then-current counts. Do not begin another county before user review.

## October16 — Roster reconciliation and other-personnel inventory after90 reviews

New packet105/capture4694 supersedes the progress view of96; it does not rewrite
96 or its82-person count. RetainedOctober15 AJAX roster96rows:92 named rows for
90 people,three docket labels,and one unnamed62/SB row. MichaelDavis and
GiuseppinaMiranda each have two rows. All90 completed receipts match exact
alphabetic name-token multisets and are byte-verified against database artifacts.
Receipt paths/hashes remain outside semantic facts; provenance mutation leaves
the semantic projection unchanged.

The October assignment chart was visually checked in full. Its department
sections contain91 name appearances/88 distinct people:57 circuit-group and31
county-group. The separate ChiefJudge box repeats Carol-LisaPhillips. Header
states90judges,58circuit/32county. Roster-only Arthmann andSeniorPole are not
inferred departed. Pole's own profile explicitly saysSeniorJudge; do not count
him as a regular-seat solution. Six explicit name variants map chart spellings
to existing receipt names, including TabithaBlackmonEves/TabithaB.Eves and
KennethGillespie/KennethL.Gillespie. Exact transcription and associations are in
`review/chart-membership-105.json` and `review/roster-reconciliation-105.json`.

The retained county index contains two identical62/SB HTML blocks, no name or
assistant heading, and image altUNASSIGNED. The actual biography link smid2826
was fetched and also has no name/assistant. It retains0473,S216/S220,Zoom98661669177.
Actual linked procedure namesJeremyI.Franker,May4,2026; his current named profile
is36. Preserve all source statements; neither a current occupant nor a formal
vacancy is established. Review of this discrepancy is complete and does not
block baseline delivery; genuine missing originals remain separate.

Follow the actual Judiciary “Magistrates & Hearing Officers” link:
`https://www.17th.flcourts.org/general-magistrates/`. Newly fetched original is
`magistrate-index` in acquisition.json. Twelve h2 rows, not the judge adapter's
h3/Biography layout. Inventory only; complete one officer before the next:

| Person | Source role | Division | Procedure path |
| --- | --- | --- | --- |
| Hilary Creary | General magistrate |98|/division-98/|
| Rebecca Frieden | Hearing officer |DOR95|/division-95/|
| Linda Ivelisse Gonzalez | General magistrate |99|/division-procedures-zm-99/|
| Caleb S.Johnston | General magistrate |69|/division-69/|
| Denise E.Kistner | General magistrate |GMX/GMZ|/division-gmx-gmz/|
| Yves P.Laventure | General magistrate |68|/division-68-2/|
| Stephanie Matalon | General magistrate |93|/division-93/|
| Lucy Ramos Miller | Administrative magistrate perchart |GMW/GMY/ZM|/division-gmw-gmy/|
| Michael Sullivan | Hearing officer |DOR94|/division-94/|
| Annette J.Szorosy | General magistrate |91|/division-91/|
| Matthew Tannenbaum | Hearing officer |DOR96|/division-96-2/|
| Allana Robinson Woods | General magistrate |90|/division-90/|

All paths are onwww.17th.flcourts.org; exact source hrefs/resolvedURLs, published
names and stable person keys are in state.remaining_personnel. Preserve the
AdministrativeAssistant role, not automatically JudicialAssistant. Chart agrees
on12 identities, with Denise's middle initial supplied only by the current index.
No other-person contact or procedure is marked individually reviewed yet.

Save helper initially rejected an absolute derived-text path before saving;
changed the new derived artifact to a repository-relative path and successfully
saved. No validator weakening.1,261artifacts andall90receiptbindings read back;
duplicate-save,frozen105 replay,entitycontext,semanticprovenanceinvariance and
priorcorrection/gap/finalized-history preservation verified. NextHilaryCreary98,
then remaining officers,clerk/admin/materialprocedures/gaps and county review.
No next county before user review.

## October16 — Hilary Creary98 and role-preserving officer validation

First other-officer review, packet106/capture4698. Source chain: Judiciary →
Magistrates & Hearing Officers → exact h2 CREARY, HILARY / Division98 block →
https://www.17th.flcourts.org/division-98/ → actual Google published iframe.
The block has no Biography link. Its Administrative Assistant label is preserved;
do not change it to Judicial Assistant or classify this person as a judge.
David Mar,954-831-5506,divgm98@17th.flcourts.org,WW12131/WW12154;
201 SE6th Street,Fort Lauderdale33301. Zoom894164912. Separate personal contacts,
fax and office hours not located in checked sources; shared division route saved.

Full22,495 extracted characters read, 15 checklist topics/18 timing rules/3
discrepancies. No PRINT/PDF link; original HTML/text retained, no rendered visual
audit claimed. UMC Tuesday8:45≤5min; child support alternating Monday9AM≤30min.
Word recommended and ratifying orders EMAIL, notCMS; findings/testimony,
transmittal and referenced PDF exhibits required. Two weeks afterhearing packet;
five days fromreceipt for pro se objections or opposing attorney version;
30days before status inquiry, separate from aspirational2week review.

Earlier Zoom steps14days versus later5day submissions, and shared2BUSINESSdays
are separately recorded; letter versus shared numerical markings retained.
General email ban versus specific email directions and individual>1hour mediation
threshold versus shared2026 temporary-relief requirements retained without
resolving authority. Shared remote-evidence order exempts magistrates/hearing
officers from in-court clerk requirement; do not import the judge clerk workflow.
CSC notice2weeks, filed/emailed notice10days BEFOREhearing, support2BUSINESSdays;
general notice10days AFTERassistantconfirmation. These are distinct triggers.
April1,2022 referral transition is not the document revision/effective date.

Existing _person nonjudge branch checks office fields but skips procedures.
New scripts/officer_review.py supplements it with explicit officer role, task/key,
assistant role, procedure association/inventory, checklist and shared-evidence
requirements. No legacy validator changes or fake judge identity. Twelve focused
tests plus ten existing roster tests passed; actual receipt validated79citations.
1,167artifact readbacks, duplicate save, frozen106 replay and entitycontext checked;
finalized reports unchanged. Prior gaps/corrections retained. Collection/review
limits and generic external form/video links remain explicit.

Use review/creary-body.py and save-creary.py as this first nonjudge example,
re-read next officer sources rather than copying values. Reuse original manifest
sources; save one officer, freeze only its new packet, check entity context, and
advance completed_other_personnel without touching completed_judges. Historical
roster105 must retain its12pending inventory; do not rerun its state-writing
finalizer. Next Rebecca FriedenDOR95;11otherofficers pending.

## October16 — Rebecca Frieden DOR95: order formats and alternative evidence routes

Second other-officer review, packet107/capture4702. Exact h2 FRIEDEN, REBECCA
(Hearing Officer), DivisionDOR95 block at general-magistrates index links
https://www.17th.flcourts.org/division-95/. Administrative Assistant Erika Melendez
Valles,954-831-7791,WW12135/WW12176; procedure emaildivgm95@17th.flcourts.org.
Address201SE6thStreet,FortLauderdale33301. Shareddivisionroute,notpersonalemail.

Wrapper has both published iframe and actual PRINT Googleedit link, documentID
1SLsdRagpHhXxyGzJ4ILnNlVmbb3aB7f6WKKkGaTebes. Exported that sameID asPDF;
all8057HTMLcharacters and4PDFpages read,all4renderedpages visually inspected.
Whitespace-normalized comparison differs solely by moved identical letterhead.
PDFURIannotations contain clerklink; HTMLlink inventory retained. No stated
revision/effective date. pdftoppm was unavailable (FileNotFoundError); installed
pymupdf rendered successfully. No dependencies installed or originals altered.

No CMS scheduling; filedmotion/petition needed but referral NOTrequired toschedule.
ProseMonTueThuAM/PM,WedPMonly; attorneyTueWedAM. Generalhalf-hourintervals and
specific30/60/15minuteallocations kept distinct. Strictly>120minute granted hearing
gets readinessconference approximately2weeksbefore. AllhearingsZoom; mobileID
993825885 conflicts with roster/general/desktop/phone97301119006. Accommodation
email singularflcourt.org differs fromheader/final/evidenceflcourts.org.
Telephoneparticipant needs presentqualifiedoathadministrator; no device/notary
contactassistantASAPand≥1weekbefore. No neighboring2hourphysicalhearingrule copied.

OAGpreparesproseorders; selectedattorneypartyemails TWOdocuments: recommendedPDF,
ratifyingWord. No inherited CrearyWordrecommendedorder or2weekdeadline. Evidence
clerkfiling≥1week OR explicitly alternativePDFemail≥48HOURS to BOTHdivision/OAG.
This is not an internalcontradiction; shared2022-37CMS/2BUSINESSday instructions
are separately preserved. Paper mail stronglydiscouraged,notabsoluteprohibition.
IndividualDORserviceaddress/hours retained as sourcedstatement,not independently
verifiedcurrentagencyservicepolicy. InterpreterassistantASAP; sharedCMS/ADA rules
retained. No liveCMS/Zoom/email/efileoperations performed.

Eleven checklist topics,six timing requirements,three discrepancies; 56citations,
1180artifacts andsavedfacts checked. Duplicate save,frozen107replay,entitycontext,
priorofficer/gaps/corrections/finalizedreports preserved. Existingofficervalidator
used unchanged; no new appcode or new testclaim. See review/frieden-body.py,
save-frieden.py andfinish-frieden.py; next LindaIvelisseGonzalez99,tenofficersleft.

## October16 — Gonzalez99 and shared court-reporting evidence

Packet108/capture4706. Exact h2 GONZALEZ, LINDA IVELISSE /99 row at magistrate
index links https://www.17th.flcourts.org/division-procedures-zm-99/.
Current roster/procedure99; wrapperZM/99 does not prove currentZMassignment.
OscarlynPires,AdministrativeAssistant,6514,WW12129/WW12174; divisionemaildivgm99,
separateOPires@17th.flcourts.org expressly forZoomtechnicalissues. Both actual
iframe andPRINTdocument collected; PRINTID1-nNtFbZ3k-YKjjkLDJDvzbRXlIFdUsdvsthVRiLoQOo.
Full14,177HTMLcharacters equal whitespace-normalized eightPDFpages; all8visual.
No statedrevision/effectivedate. NoUMC/onlinebooking; final/evidentiaryphysical,
CMCZoom,noticeappearancecontrols. Threephysicalexhibitcopies. BothordersWord
divisionemail14DAYS;proseobjections2DAYSfromreceipt/redline14DAYSfromhearing.
Preserve internalemail/scheduling/continuance/recording/calendar differences.

Follow printed /court-reporting/ URL, then actualFAQ/transcript/multimedia/
dissemination links. AllfourFAQpages andthreeone-pageforms read/visual. Save
CRSphone6260/fax6230/Room19170/CRSTRAN separately from chambers. Court-reporting
index search found current AO2023-32-Gen Amendment2 at /2026/04/ path; signed
May27,2025,effectiveimmediately,supersedesAmendment1. All13textpages read;
criminalstaffing/capital details screened only. Civil/access/fees reviewed;
pages4/5/10–14visual. Page14 is image-only form, ordinaryextraction yielded only
page number; selectedtext manuallytranscribed withsameoriginalhash/timestamp.
CurrentappendixemaildefaultunlessCDrequested,andnopaymentuntilaccessconfirmed.
LinkedolderformCDonly/whole-daysatellite/specifichearing2–3weeks remainsdistinct.

Directofficial AOSC11-22 collected12pages; scoped1–3/9–12read,3/9–12visual;
4–8notfullyreviewed. Signed/effectiveJuly20,2011; attachmentrevisedJuly15 not
issuance. Standardsmandatory,bestpracticessuggested. Audio-releaseacknowledgment
protectsconfidentialinformation,notblanketbanonallpublicinformation. Do not
assert statutory/substantivecriminalreview from collection ofthewholefile.

Separate historyentity broward-court-reporting-procedures storessevenreviews and
fourdiscrepancies:30DAYS/30BUSINESS/30–45BUSINESS/fromdeposit; OVERhour versus
hourORlonger and exceptions; audioformat/turnaround/paymentsequence; payment
methods. Civilpartiesarrangereporter exceptlistedpublicexpensecases; GM/HO
digitalcoverage. AppealsdesignationmustbeservedCRS,clerkfilingaloneinsufficient.
LocalAOoriginal2023-32/A1notindependentlycollected; currentA2andformversions
preserved withoutauthorityresolution. Allseven addedshared-civil-reviewed.json.

155nestedcitations/1229artifacts andbothsemanticrecords readback; duplicate-save,
frozen108replay/bothentitycontexts verified; historicalinventories,priorofficers,
genuinegaps andfinalizedreports preserved. No livecontact/payment/recordrequest.
Next CalebS.Johnston69; nineofficersremain. Use review/gonzalez-body.py and
save-gonzalez.py, separate officerandsharedfindings inexistingcounty stream.

## October16 — Johnston69G: exact time units and linked legacy template

Packet109/capture4710. Exact h2 JOHNSTON, CALEB S. /69 roster block links
https://www.17th.flcourts.org/division-69/. Marilena DiLiddo,AdministrativeAssistant,
7572,divgm69@17th.flcourts.org; chambersWW3123/hearingroomWW3142. Procedure header
addressRoomWW3142 is kept separately. DiLidddo spelling occurs in body; no new
person inferred. Full7630HTMLcharacters/fourPDFpages read and allfour visual.
Actual document revisionDecember26,2024, not Googleautomatic-five-minute banner.

Wrapper iframe contains literal `? embedded=true`; curl rejected malformedinput
before HTTP. Encoding space as%20 returned200 without changing the query name or
documentID14tVa9Tjpc57y4Bud8oQNwX-GVxMA3ylzxex2fYDwMHk. Originalhref andexacterror
saved. SameactualID PDF export available; wrapper has noPRINTlink. Bodymatches
aftercase/whitespace/platformheader/repeatedfooter normalization; rawdiff retained.

Signedreferral/petition andcompliance prerequisites; showcausedocketcondition
andwrittencontinuance≤daybefore separate from incapacity/advocate/APS unanimous
agreedrescheduling withoutmotion. ETGWorddraft≥3HOURS;petition/currentaddress to
appointedcounsel≥24HOURS; restorationdraft≥3DAYS. EvidenceCMSbeforedockethearing,
admittedlist/documents immediatelyemailGM/allparties. No inventedgenericdeadline.
Remoteunlessnoticedphysical; physicalwitnessZoomrequiresfiledmotion. Feesnot
currentlyheard. Bakertransfer paragraph retained/sharedscreenonly, noexpandedmerits.

ActuallylinkedHEREtemplate ID13Spj9ypO_FlffP2ACx8lLDLLmafEXvpmNH2aeyxsn24
exported/read/visualallthreepages. Page3blank confirmed; page2namesClaudetteVanni
and2020year withblankcase/signingfields. Preservelegacytemplate,notcurrentperson
orenteredorder. Its30dayfinalaccounting runsfromemergencyorderEXPIRATION, not
hearing. Individual permits leaving other formsectionsblank beforehearing.

ExactcitedAO2019-100-PRCofficialoriginal3pages fullyreviewed/visual:24hourfiling/
notice rules andnoticeharmexception,objection/same-dayjudgefallback,48hourGM
availabilityfallback,10dayexceptions/waiver,dangeremergencyjudgeroutes; dated
December13,2019/supersedes2016-24. RelevantactualindexlinkedAO2017-43two pages
reviewed/visual:acceptedfilingautomaticshowcausedismissal,subsequentaudit/misuse/
unpaidauditfeeexceptions. DatedAugust14,2017. Individualallplanscompliantcondition
retained separately; no decisionwhichcontrols orclaimunnumberedreferenceproven.

12topics/8timings/3discrepancies;108citations and1226artifacts readback; exactsave,
frozen109replay/entitycontext checked. Seven relevantsharedsources,includingtwo
neworders. Priorofficer/sharedreportingrecords,gaps/history/finalizedreports
preserved. See review/johnston-body.py/save-johnston.py/finish-johnston.py.
Next DeniseE.KistnerGMX/GMZ; eightofficerspending; no nextcountybeforeuserreview.

## October16 — KistnerGMX/GMZ: visible text versus hyperlink target

Packet110/capture4714. Exact h2 KISTNER DENISE E. /GMX/GMZ roster links
https://www.17th.flcourts.org/division-gmx-gmz/. Shamika Thompson,
Administrative Assistant,5331,divgdek@17th.flcourts.org; WW9125/WW12158.
Entire8,351-character published HTML read and actual anchors inspected.
No PRINTlink or separate normal Google documentID found; no PDF export guessed
from2PACX. No PDF/browser visual-review claim or inferred document date.

Printed Zoom703204202 agrees with roster, but actual anchor's Google redirect
q target is894164912. Preserve original href, parsed target and printed number;
never join a meeting to test identity. Raw HTML retained as a second text artifact
for exact href citation because ordinary visible-text extraction omits attributes.
Special-set sentence says Magistrate Plant's assistant but gives divgdek email;
preserve conflict, do not assign Plant current contacts. Two conflicts recorded.

Reports14days AFTER HEARING unless directed otherwise; proposed copies to all
parties with24hour objection opportunity BEFORE SUBMISSION. Portal unspecified,
no Word/PDF format supplied. Suggested dates require conferral/assistant response
within3days of INITIAL REQUEST. Special-set Notice/Motion/Referral packet within
7days FROM SCHEDULING, courtesy copies all parties. Scope and triggers are separate.

Dependency motion/referral/notice; hybrid only approved limited circumstances;
all in person for interpreter or specified transported inmate; only magistrate
directs cancellation, agreement not dispositive. Family referral by magistrate
for pro se/counsel for represented; notice responsibility similarly distinct.
Exhibits CMS Supporting Documents, no individual deadline; pretrial case by case.
Four shared sources reused (remote evidence, ADA, interpreter, UFC plan). Relevant
UFC plan not conclusively identified as the unnamed AO in individual procedure.
No general commercial docket or expanded dependency merits review inferred.

12topics/4timings/2conflicts;77citations/1216artifacts readback and exactsave,
frozen110replay/context verified. Earlier records/gaps/finalized reports unchanged.
See review/kistner-body.py/save-kistner.py/finish-kistner.py and discovery/links files.
Next Yves P. Laventure68; sevenofficers pending; no nextcounty before user review.

## October16 — Laventure68: mailto targets, precise triggers and missing template

Packet111/capture4718. Exact h2 LAVENTURE, YVES P. /68 roster links
https://www.17th.flcourts.org/division-68-2/. Administrative Assistant Janice Todaro
Reres,7695; printeddivgm68@17th.flcourts.org versus six HTML/PDFmailto targetsdiv68.
RosterWW3127/WW3146; procedureRoom12127. Preserve variants without silentcorrection.
Full4386HTMLcharacters and3PDFpages read/visual. Explicit Updated1/9/2023; Google
automaticbanner not revision date. SameiframeID1DmJIyrAYIrPRA5tTSeDUD1L5OPefjpibPXX2JRw5ksM
exportedPDF; noPRINTlink. Literalqueryspace firstcausedcurl3; percentencoded%20
without changingID/queryname. Bodymatches aftercase/whitespace/platformprefix/
repeatedheader normalization. Originalbytes andnormalizationcomparison retained.

Signedreferral+petition/compliance prerequisites. Showcause no telephone, written
continuance request; “within3days of the hearing” filedpleadings phrase retained
literally, no≥3days inference. Compliance-docket paragraph separately preserved.
ETGfullWordreport≥3HOURS before,copyall;petition/currentaddress toappointedattorney
10AMdaybefore. Incapacity/advocate/APS unanimousagreedcontinuanceemail,no motion;
telephoneemail reason/agreement/notary/names/phones,conferencecallifmultiple.
Fees eachpendingpetition andcapacityreport Word≥3DAYS,copyall. No inherited
Johnston fee-unavailability or24hourindividual deadline. RosterZoom305594432 is
not blanket remote-appearance authorization.

HERE advertises blankETGreport but isplain text; no HTMLanchor/PDFannotation.
Official-domain searches found legacy2017/08/div68procedures.pdf: threepages
collected, page1text reviewed only; PriscillaHart/Room1000/phart anddifferent
showcausecontinuance instructions retained aslegacyvariant, notcurrent data.
URLyearnotissuance. LegacyPDFalso has noURIannotations. Checked retainedcourtforms,
probatesmartforms andprobatehub links; noidentifiedDivision68reporttemplate.
Johnston's linked template is distinct, not substituted. Missingtemplate remains
separateincomplete sourcecheck plusnextaction; no claimall evidenceavailable.

10topics/5timings/5discrepancies. ReusedAO2022-37,2026-20,2019-100,2017-43;
shared24hourETGfiling/noticeroutes andshowcauseconditions stay separate from
individualterms.86citations/1232artifacts readback, frozen111/context verified;
priorofficers/sharedrecords/history/gaps/finalizedreports preserved. See
review/laventure-body.py/save-laventure.py/finish-laventure.py, discovery,
transport, formatcomparison andtemplate-discovery files. NextStephanieMatalon93.

## October16 — Matalon93: scoped deadlines and embedded official form downloads

Packet112/capture4722. Exact h2 MATALON, STEPHANIE /93 roster links
https://www.17th.flcourts.org/division-93/. LesleyBurton,AdministrativeAssistant,
7285,divgm93,WW12137/WW12156,Zoom887625587. Full17933HTMLcharactersread;updated
July9,2026. Actualmail/Zoomlinks agree. Published2PACXonly,noPRINT/exportIDinvented.

UMCThursday8:30–9:30/allready8:30; online/conferral/referral,packet5BUSINESSdays
withliteral uploadviaemail phrase. Specialsetsphone/email/referral;courtesyemail
andCMSexhibits3BUSINESSdays. AdditionalZoom14days,conditionalCMS/emailoneperparty;
admittedhardcopiesimmediatelyaftertrial. Prose stipulatedemail3BUSINESSdays.
CSCthirdThursday≤30min,minimum2weeksnotice,10daynoticefile/email,2BUSINESSdaysCMS.
Allnoticesimmediateconfirmation/≥14days. Preserveoverlaps,nouniversaldeadline.

Verifiedcontinuancemotionfile/courtesyemail,opposedUMC,agreednohearingbutorder/
assistantconfirmation. Temporary>1hourmediation14days;shared2026-06beforeSET
separately retained. Triallists14CALENDARdays,exchange14days,letterpremarking/
numbersadmission/threecopies;sharedremoteordernumericpremarkingconflict retained.
Earliercancellationstipulation/agreedordertojudge vs lateragreedrecommendedorder
ANDconfirmation. Finalhearings/trialsmaynotbecanceled. Wordrecommended+ratifying
packet/transmittalletter/allparties;5dayreceiptobjections/competing;2weekshearing
submission;reviewtarget2weeks/statuswait30days. Apr1,2022referraltransitionseparate.

Officialformpages12.915/12.920abc/12.921 returnedHTMLshell,notmissingformcontent.
Parsed `__NEXT_DATA__.props.pageProps.pageData.filePdf.uri` withnew
`scripts.flcourts_article.extract_form`; versionqueries preserved. Official PDFs:
915 /content/download/685859/7661591?version=4 (08/2023),
920 /content/download/685861/7661613?version=3 (04/2022),
921 /content/download/685866/7661656?version=5 (11/2020).
All19pages textread; visual915pages3–4,920pages8–10,921pages3–5. Recordvariants:
2023emailmandatoryunlessexcused vsolderoptionalelection;920instruction/order
objectiontriggers;920noticefooterlabelsOrderofReferral. 921instructionreferences
12.961forRule12.615contempt; alternativenotcollected, noexpandedchildsupportmerits.
Unexecutedformsnotcaseorders. See receipts/family-notice-forms-reviewed.json and
independententity `broward-family-notice-and-address-forms` forfuture reuse.

14topics/20timings/7discrepancies;196citations1264artifactsreadback; frozen112 and
bothcontextsverified. Eightrelevantsharedsources including3newforms. Firstsave
validationrejectedmissinghashlistonsharedcheck; addedactualcitationhashes and
validatedbeforepersisting. Prior records/gaps/finalizedreports unchanged.
28extractortests passed; nofullappbuildclaim. See review/matalon-body.py,
save-matalon.py/finish-matalon.py, form-links/discovery andretainedoriginals.
NextLucyRamosMillerGMW/GMY/ZM;fiveofficersremain.

## October16 — Miller: distinguish unlabeled anchors from displayed links

Packet113/capture4726. Exact h2 MILLER, LUCY RAMOS /GMW/GMY/ZM roster links
https://www.17th.flcourts.org/division-gmw-gmy/. ElizabethRanalli,0697,divglrm,
WW9127/WW12162. RosterAdministrativeAssistant/procedureAdministrativeSecretary,
sameperson; preservebothlabels. OctoberchartAdministrativeMagistrate; no newdate
inferred. HeaderGMW/GMYplusfelonymentalhealthprobation/diversion,rosteraddsZM.

Full7707HTMLchars/fivePDFpages read/allfivevisual. ActualPRINTdocumentID
1Oh4doPzoYFre1plfvLYYLhLdwdiEy8GBiNECII9FknA exported. Rawcomparison differences
areORPHONE/emailPDFextractionpositionandbullets/listnumbers; visualreviewconfirms
wording, no exactnormalizedequalityclaim. No statedrevision/effectivedate.

Displayed/s/595222547linksandrosternumber595222547 agree. ExtraHTMLanchoris
nonbreakingwhitespace targeting/j/894164912;PDFpage1URIrectangle
[150.667969,278.84998,153.667969,293.25]. Preserveoriginalmarkup/targetseparately;
do not falselyclaimthevisiblelinkpointselsewhere. PrintedhelpvideoURLslackhyphens
foundinactualtargets; links retained, videosnotwatched.

Court schedulesallhearings; date/continuance/info phone/emailoffice. Ordersupload
unspecifiedportal,emailifunable,copyallcounsel;no inventedWord/14day/CMSrule.
EmergencyANDurgenttodivision/shelterjudge. Exhibits/pretrial/trialcase-specific,
emailassistance/copyall. DependencyZoom/mentalhealthhybridunlessotherwise;
telephoneONLYnonevidentiary,join≥10minutesearly,technicalassistantimmediately.
CourtSmartrecordingstatement,quiet/nodriving/one device/mute/witnesscontrols saved.
Individualonlycourt/reporterrecordversusquotedAOconsentlanguage preserved.
HistoricalAO2020-42/2022-31similartextnotprovedexactunnumberedversion; replacement
chainkept(2022-31replacesAmendment2;2022-37replaces2022-31). Noexpandeddiversion
manuals/plea/sentencinganalysisorcontact/Zoom/portaloperation.

10topics/2timings/3discrepancies;111citations1255artifactsreadback,frozen113/context
verified. Five sharedsources;priorrecords/sharedforms/reporting/gaps/finalizedreports
preserved. See review/miller-body.py/save-miller.py/finish-miller.py,
discovery/formatcomparison/HTMLandPDFlinkinventories. NextMichaelSullivanDOR94.

## October16 — SullivanDOR94: explicit observer exception and unstated deadline

Packet114/capture4730. Exact h2 SULLIVAN,MICHAEL(HearingOfficer)/DOR94 rosterlinks
https://www.17th.flcourts.org/division-94/. MakaelynSlager,AdministrativeAssistant,
7214,Div94@17th.flcourts.org,WW12121/WW12152,Zoom508258194. Full6707HTMLcharsread;
noPRINTlink,documentanchors,normalGoogleexportID,PDF/visualclaimor revisiondate.

Noonlinescheduling. Filedmotion/petitionrequired; referralpreparedjudge/casemanagement
butNOTnecessarytoschedule. ProseassistantreceivesreferralORmotion,sets/mailsatmotion
address;updatewhenmoving. AttorneysThursdayAM1hourintervals,requestmoretime.
Petition(notmotion)licensedprocessserverDORserviceatstatedTallahasseeaddress,
Mon/Thu13:30–15:30;hearingafterClerkproof. Retainassourcestatement,notcurrentagency
verification. Prosetwostampedcopies/ClerkRoom2140forms; sourceUIinstructionsnotlivechecked.

Videofulllegalname/cameraon,≥10minbefore,technicalassistantimmediately. Telephone
notaryidentityrequirementexplicitlyexceptsNONTESTIFYINGobservers. NoZoom/device/notary:
assistantASAPbut≥1weekbefore. AccommodationemailprintsDiv94@17th.flcourt.org;
elsewhereflcourts.org. AlternativePDFemailOAGprintsmyfloridaleagal.com versus
retainedFriedenmyfloridalegal.com. Preserveboth,no correction/contactattempt.

Continuancemotionfilefirst,thenassistantsetshearing. Evidencefile≥1weekORPDFemail
BOTHdivision/OAG; no separatealternativedeadline stated—do notimportFrieden48hours.
Papermailstronglydiscouraged. RecommendedHOorderPDF/ratifyingorderWord,TWOdocuments
email,renderedeportaldistribution,nodeadlineinvented. SharedremoteCMS2BUSINESSday
rule remainsseparatewithscope. No expandedDORmeritsreview.

9topics/4timings/2emaildiscrepancies;53citations1252artifactsreadback,frozen114/
contextverified. Priorofficers,sharedforms/reporting,knownsourcegaps/finalizedreports
preserved. See review/sullivan-body.py/save-sullivan.py/finish-sullivan.py and
discovery/linkinventories. NextAnnetteJ.Szorosy91;threeofficersremain.

## October16 — Szorosy91: preserve separate notice triggers and source routes

Packet115/capture4734. Exact h2 SZOROSY,ANNETTEJ./91 rosterlinks
https://www.17th.flcourts.org/division-91/. JessicaVillafranca/procedureJessicaM.,
5700,divgm91,rosterWW12133/procedure12139chambers,courtroom12166. Full18768HTMLchars
read; noPRINT/PDF/dateclaim. RosterZoomAfter4/20/2020notdocumentdate.

OnlineFriday8:45UMCbriefCMCnonevidentiary/10–12CSCtemporarysupportenforcement≤45min;
othersspecialemail. Validreferral;specialrequestallparties+referral+pleading+time.
NoticeNEXTbusinessday plus2BUSINESSdaycancellationthreshold retained; CSCnotice
“within10daysinadvance”literal. UMCpacket5BUSINESSdays includingrenotice. Prose
courtsets,3weeksnonoticefromreferralphone;separate10daysafterobjectionexpirystatus.
TrialorderNOTnotice;final/trialmediationbeforeSET,cited2019-15ExhibitA5exceptions
andbeforefinalhearingtriggerseparate. Motionmaysetwithoutmediation.

Generalemailonlyscheduling conflictswithspecificnotice/evidence/orders/delayemails;
phonebothparties/schedulingonly vsprosefollowup/samplecalls. No merits/exparte.
Physical≥3copies;Zoomexchange14days/uploadattorney orproseemail5days,exactEVIDENCE
subject. Publicfileexhibitbanprehearing separatefromsharedpostadmissionfilingand
PDForderattachmentsCMSDocket/filingdatereferences. Issue-specifictrialproposals14days.
ContinuancehearingORwrittenackboth vshearingrequired/noexceptionsCMC clauseskept.
Withdrawalclientnotice/lastcontactfields;court-setCMCpriororderforchanges.

Recommended+ratifyingWordemaildivision14days,NOTjudge. Transmittalletter;recording/
transcriptobtainedbeforeDISPUTED/redlinereview,cooperate,nocourtindisputemails.
Prose5daysreceiptobjections+14dayshearingredline;attorneyredline14days. Lateemail,
fullmail/emailservice,USMailifnodesignatedemail. CRSforms/official920/921reused,
no newrecordingrequest/payment/contact. Final/trialmaynotcanceluponresolution.

Actual/zoom/fragmenttargetservesinterimdependencydirectory; originalretained,no
oldpersoncontactsimported. Exactphraseofficialsearchfoundseparatetipspage
/electronic-hearing-with-zoom/,readandretained,notclaimedredirectoridentical.
Linked2020COVIDPDFnotpursuedaslowpriorityhistoricaldependencycontext. Actual
/2018/07/27/7235/supportlandingread,embedded04elG0CDPJslinkretained,notwatched.
2019-15ExhibitA5physicalpage5targetedreviewpreservesmediationexceptions.

14topics18timings8discrepancies;188citations1263artifactsreadback,frozen115/context
verified;14relevantsharedsources. Priorofficers/sharedrecords/gaps/finalizedreports
unchanged. See review/szorosy-body.py/save-szorosy.py/finish-szorosy.py and
discovery/linkinventories. NextMatthewTannenbaumDOR96;twoofficersremain.

## October16 — Tannenbaum96: hearing allocations and conditional status conference

Packet116/capture4738. Exact h2 TANNENBAUM, MATTHEW (Hearing Officer) /DOR96
roster links https://www.17th.flcourts.org/division-96-2/. Procedure adds middle
initial A.; matching division/phone/actual linked document. Patricia Cantrell,
Administrative Assistant,954-831-6585,DivGM96@17th.flcourts.org; chambersWW12120,
courtroomWW12172,Zoom993825885. No personal email/fax/hours separately located.

Actual published 2PACX iframe: full8,053-character HTML read, no PRINT/normal
GoogleID/PDF/date or visual-review claim. Only anchor is generic Clerk homepage;
Google outbound href and decoded http://www.browardclerk.org retained. No specific
missing form/template advertised. Clerk operational review remains separate.

No CMS scheduling; filed motion/petition required, referral NOT required. DOR
motions OAG schedules/notices; represented hearing assistant/attorney coordinate.
Pro se Mon/Tue/Thu AM+PM,Wed PM; assistant receives referral OR motion, notice to
motion address. Private counsel Tue/Wed AM generally half-hour intervals; reasons
for longer requests. Specific allocations30min enforcement/contempt/license/arrears,
60min guidelines/modification/establishment,15min status/miscellaneous. Unless
otherwise requested/granted. MORE THAN120 minutes triggers mandatory readiness
conference approximately2weeks before. Keep >120 distinct from >=120, and approximate
from exact. Continuance motion filed then hearing coordinated; no invented exception.

Zoom join5–10min before, camera/microphone. Telephone notary OR jurisdiction-qualified
oath administrator present; no express non-testifying observer exception here.
No device/notary: assistant ASAP but no later than1week before. Accommodation email
prints singular flcourt.org versus header/contact/evidence flcourts.org; both retained.
Evidence file≥1week OR PDF email BOTH division and OAG≥48hours. Shared AO2022-37
2BUSINESSday conferral/numerical marking/CMS upload retained separately, including
its family-hearing-officer exception to required in-court clerk presence. No control
determination. Pro se orders OAG prepares; attorney cases Court assigns drafter.
Recommended PDF / ratifying Word, two email documents, no deadline stated.

DOR petition-service address/hours preserved as individual-source statements,
not independently checked agency policy. DOAH superseding-petition route captured
without merits expansion. Emergency motions Division Judge; license contests
generally not emergency, remain HO. Interpreter assistant ASAP alongside shared
CMS/request deadlines. Clerk button colors not live UI test. No calls/emails/Zoom.

11topics/6timings/2discrepancies;55citations/1266artifacts validated/read back;
frozen116/context verified. Three shared sources reused, earlier reviews/gaps and
finalized reports preserved. See review/tannenbaum-body.py, save-tannenbaum.py,
finish-tannenbaum.py and discovery/link inventories. Next Allana Robinson Woods90;
one officer remains, then clerk/admin/material procedures/gaps/county review.

## October16 — Woods90: templates, source variants and folder extraction

Packet117/capture4742. Exact h2 WOODS,ALLANA ROBINSON /90 links
https://www.17th.flcourts.org/division-90/. Keren Vega rosterAdministrativeAssistant /
procedureAdministrativeSecretary,6580,kvega and divgm90,WW12138/12164,Zoom961072109.
Named assistant email separately established; case-manager8532/resourceClerk6565
are not assistant numbers. Resource list remains individual-source-only evidence.

Full27728-character published2PACX procedure read. Header March2026, embedded9/2017
order-type paragraph and April1,2022 referral transition stored distinctly. Valid
referral/expired objection/ordered mediation; related pending matter existingreferral
suffices. Discovery resolved before setting. Timesharing/parenting mediation before
setting; final/trial if required mediation AND report filed. Prose courtsets after
10dayobjection,3weekreferral followup; cannot scheduleonline but may register evidence.

UMCWed/Thu8:45≤5min,5BUSINESSday packet. CSC overview secondTuesday versus detail
secondThursday9–12/13–16≤30min, non-evidentiary label retained. Special packet7days
from scheduling; notice7daysconfirmation; CSC10dayadvance phrase retained literally.
Scheduling no-need-cc-prose exception versus all-partycommunication rules. General
continuances mustbeheard versus agreed exception;5dayreceipt review warning notbar.
AllZoomunlessotherwise versus under2hour general list, no inferred duration ban.
Telephone non-evidentiaryonly; join10min,fulllegalname,CourtSmartaudio.

Zoomsteps14days,CMSifbothrepresented/registered,elseemailalloneperparty. Admitted
list/docshardcopy immediatelyaftertrial. Trialexchange14days,letterpremark,3copies,
redaction;stipulatedemail2days. Shared2BUSINESSday/numericalpremark retained separately.
Specialcancelagreedrecommended+assistantconfirm;finaltrialonlyifFinalJudgmentset
beforeJudge,noticebeforecancel. RecommendedWord/exhibitsPDF,ratifyingformat not
explicitly stated. Emailkvega,no mail/CMSrecommendeduploads;2weekpacket,3BUSINESSday
opponentreview/prose5dayreceiptobjections,redlines/separateversions. Reviewtarget
2weeks but wait30daysstatus. Recording/reporteraddress andreferraldate required.

Actual notice-template link and GM recommended/final-order link both point to
/wp-content/uploads/2022/10/Generic-Template.pdf:2pages recommendedorderonly,
fulltext/visualreview. MissingadvertisedGMfinalcomponent tracked separately;official
920(c)/921noticeforms reused without pretending identical replacements. Actual
/wp-content/uploads/2023/10/Generic-Template-HO.doc is OLEbinary33792bytes; retained
original and textutil extraction,fulltextread,no page/visualclaim. Contains HO
recommended+finalorder but reviewnotice names GM/12.490(e);official921HO12.491(f)
preserved. Templates blank,notcaseorders;URLmonthnotissuancedate.

CMSmanualHTTP/HTTPS404; eBench200shellnotguide. Existing supporting-document training
landing separate,not replacement. Two legacyhelp.flcourts.org URLs curl60hostname
certificatefailure and webopeninaccessible; no insecure retry. Official.gov search
found Helpful-Videos folder and Zoom/Teams childfolder, retained separately. Initial
article extractor correctly rejected different metadata. scripts/flcourts_folder.py
reads name/description.html5 and supported contentblock/rawhtml/separator JSON,
including escaped iframe links; no script/video execution.37focused tests passed;
retained9/4videolinks checked. Descriptions read/videosnotwatched; lowpriority
linkedcriminal/dependencybodiesnotexpanded. Original shell and derivedtext bothsaved.

16topics22timings11conflicts;2missing/unavailable-source nextactions;190citations and
1288artifacts validated/readback. Frozen117/entitycontext/priorrecords/finalizedreports
preserved. All12officers nowreviewed; nextcountyClerk/admin/material/gaps review.
See woods-body.py/save-woods.py/finish-woods.py, discovery and folder verification.

## October16 — Institutional contacts and courthouse access, checkpoint118

Capture4746/packet118 adds separate `broward-clerk`, `broward-court-administration`
and `broward-courthouse-access` findings. `/Home` footer/menu gives actual
`/AboutUs/AboutTheOffice#ContactUs`, `/AboutUs/HoursAndLocations#ClerkDirectory`,
and `/GeneralInformation/Miscellaneous#PublicRecordsCustodian`. Do not treat the
standalone `/aboutus/contactus` shell's confirmation text as a sent message.

AboutTheOffice panelsAboutTheClerk/OverviewOfOffice/ContactUs reviewed;90kpage
news/event bodies not globally reviewed. Clerk BrendaD.Forman sworn thirdterm
Jan6,2025,notpage-revisiondate. General6565 agents08–16:20 weekdays except holidays;
administration5848/7019,Room18150,counter08–15:30. GenericEclerk assistance/accessibility
route,notpersonalemail/filingchannel. All-other-inquiries201SE6thStreet include
division;traffic-onlyPOBox14610 separate. NnamdiJacksonGeneralCounsel/PublicRecords
custodian mailbox;internal-audit6900/internalaudit distinct restrictedpurpose.

Retained Oct15 clerk-locations source: all38directory rows reviewed/extracted,
room leadingzeros/fax/attorney/option/thirdpartyafterhours labels preserved. Circuit
CivilRoom04130,6565option2/5600attorneys/fax6572. CountyCivilCentral03170/5622,
North160/1209,South100/0353,West170/2339. Jurycounter7:15–16:15/phone9–16 distinct.
2026thirteen/2027fourteenholiday rows structured and weekday/date consistency checked.
Counter/agent/location hours not generalized into one schedule or artificial conflict.
No department's criminal/diversion merits expanded. Prior source retrieval not reset.

Court `/welcome/` and `/court-programs/`: JosephM.D’Amico TrialCourtAdministrator,
appointmentSeptember2022,7740,WW20170,201SE6thStreet. Mediarelations published feedback
route,notpersonalemail; nolegaladvice/pendingdecisionresponse. Hurricane7777/ADA7721
separate. Aggregate90judges/11magistrates wording not interchangeable with roster's
12otherofficersincludinghearingofficers. No inferred vacancies or roster deletion.

`/for-attorneys/` actual room-sheet link2024/07: rooms14107/15107/16107/17107,
firstcome,7767 withjudge/dates,dailykey20170/validdriverlicensefrontdesk. Separate
search-found2017/10sheet omits17107,namesLorraineEdewaard/formofID. Both onepage
text+visual,nostatedrevisiondate orreplacement; do not useLorraine ascurrentassistant.

Clerk MiscADA/security/publiccustodian/judicialrecord panels reviewed; unrelated
COVID/traffic/pretrial/disclaimer bodies not globally reviewed. Security actual
`.pdf.` link and2025/10ExhibitA target404. Retained `/general-orders/` actual
2026/04/2025-38-Gen.pdf succeeded. Sevenpages text read,1/6/7visual. SignedOct3,2025,
effectiveimmediately,revokes2017-64Amendment1. Licensedattorney/employee belt exception
inC(4) absent generalClerksummary; notblanket screening exemption. ExhibitA two
columns visually checked. Footnote attached plainclothes sign-inlog not present,
law-enforcement-only gap retained without exhaustive lowpriority pursuit.

Directory extraction helper scripts/broward_clerk_directory.py validates unique
panel/two-column headers/unmerged cells/nonempty unique divisionlinks/rows; no
contact-role inference inside helper.18tests passed (8new+10roster),38retained rows
matched. Scalar normalization and role-qualified display remain in institution
receipt, with exact row citations.74citations/1319artifacts readback,3contexts/frozen118
and earlierofficers/ZIPfinding/gaps/finalizedreports preserved. See institutions-body.py,
save-institutions.py,finish-institutions.py,discovery and helper verification.

Next `review/county-operational-review-queue.json`: actual commercial Clerkdivisions,
records,efiling,fees; selected datednews bodies; accessbadge/securityrecording/closure
orders; officialrecordssearch/propertyappraiser navigation; remaininggaps/countyreview.
Contact completion does not certify those operations reviewed or county complete.

## October16 — Circuit Civil operations, checkpoint119

Capture 4750 (`7897f6291d585d362d6641a6b5786aae57375da15eb1c42b54a471c8220cb1df`), stable entity
`broward-clerk-circuit-civil`; receipt `receipts/clerk-circuit-civil-reviewed.json`.
Reviewed all six `/Divisions/CircuitCivil` bodies: CircuitCivilFiling,CourtRegistry,
ForeclosureSales,IndigentStatus_Civil,FormsandSelfHelp,FilingFees. The source overview
says disputes exceeding$50,000,not an exhaustive jurisdiction conclusion.

Registry requirements retain bond amounts/recorded-judgment filing,interpleader order,
repair-lien transfer$13 and literal registry formula. Auction deposit5%estimatedbid
received3pmEST preceding business day; successful balance/registryfee noonEST next
business day ORjudgmentdeadline. Objections10days from certificate-of-sale filing.
Electronic sale$70eachschedule/reschedule. Documentary stamp nearest$100 wording,
printed FS45.31 and deposit-method typo retained,not silently corrected. Refund
service-charge request served GeneralCounsel mailbox; live sale requires judgment
language or separate order. Auction actual linked landing/instructions403 and web
open Internal Error; inaccessible instructions remain separate gap.

Thirty fee rows (17filing/9misc/4copies) preserve labels,thresholds,per-unit scope.
Page realproperty newcase401/906/1906 versus quiettitle instructions400/905/1905;
counterclaim395/900/1900 separate. No fee calculator or controlling-authority view.
Indigent2019form says otherfees notwaived versus webpage sheriff-service waiver;
Form2.601 request(D)/determination(C); forged instructionsParagraph6 versus actual
form4; LawLibraryRoom1800 versus Woods1881. Five discrepancies retained. Library
public07:30–12:00 versus virtualforms07:30–15:30,MonFri excludingholidays.

Fourteen form originals:12PDF/22pages fully text read,16selectedpages visually
inspected;2DOCX bodies plus header/footer/note XML inspected without rendering.
Affidavit/worksheet retain field/file/oath requirements; AO2014-17 reused from
existing sharedreview,not recollected. Surplus claim representations preserved as
template statements. Quiettitle forged/wild/fraudulent forms retain distinct
allegations without assuming universal suitability. Form1.998footer06/24 and
indigent05/01/2019 are revisions; affidavitJuly1,2013 is case applicability.
Pypdf field dictionaries and images recover prepopulated17th/Broward values absent
from plain extraction. Blank forms not submitted. First rendering used deprecated
fitz alias and warned; subsequent reproducible rendering uses pymupdf directly.

`review/circuit-civil-body.py`, `save-circuit-civil.py`, `finish-circuit-civil.py`
record mapping/save/verification.79citations,1355artifactreadbacks,exact/frozen
replay and entitycontext checked; previous institutions/officers/ZIP/gaps/finalized
reports unchanged. County remains incomplete. Next CountyCivil in explicit queue;
global fee page and other operational sources/news remain pending.

## October16 — County Civil operations, checkpoint120

Capture 4754 (`089523f48f169dad12c17f59f5111af44e47b413e6c0a9fd2aa42c41f59e8052`), stable entity
`broward-clerk-county-civil`; `receipts/clerk-county-civil-reviewed.json`.
Reuse `mchugh-clerk-civil` at its original retrieval timestamp. Read all ten panel
bodies, including plural `ForeclosuresSales`. Sources and exact hrefs are saved in
`review/clerk-county-civil-links.json`. Before fetching orders, check the existing
`county-order-index-benson`, shared receipts and individual operational receipts.

Small claims/filing/eviction panels point to already-reviewed AO2025-40; preserve
ZIP and exception details in the existing independent finding. The2017footer
small-claims handout says file at any office and1courtcopy plus1perdefendant,
whereas the webpage directs the ZIP order and2sets perdefendant. Keep both.
Its8000threshold does not establish a newer revision date than the printed footer.
Residential eviction panel7weekly/15monthly nonpayment wording differs from the
linked2026section83.56's3daynonpayment/7daynonrent statements. Do not convert these
into commercial tenancy advice. The2014eviction sheet's copy counts,5daydefault
exclusions and185/10/40/90fees remain dated source statements,not currentfeequotes.

Garnishment3pages fully read/visual:20dayreceipt deadline,8businessdayhanddelivery
and14businessdaymail plaintiff objections; certificate permits email without a
matching objection deadline. Circuit Court caption despite CountyCivil link.
Shared2.601,1.998,party andindigent forms reused from119. Paidformcatalog is labels
only; SelfService is disclaimer/acceptance landing,not generatedforms. Existing
McHugh summons andauction limitations retained. No purchases or form submissions.

Clerk links2017-79-CO PIPtransfer order. Actual retained county index links2023-35,
which expressly VACATES it, signedAugust31,2023. Save both originals; do not treat
Clerk link as present applicability. Oldorder signedDecember13,2017/effective
January15,2018,2014oroldercases/Division70; original uniformpretrialattachment not
identified,2025forms not assumed identical. Officialdomain search for2021-6-CO
found Amendment3 actual2021/08/2021-6-CO-Amendment_3.pdf, signedAugust2,2021.
OriginalFebruary15order says mandatory immediate referral; Amendment3 says
landlordagreement/mayrefer. Preserve both,including10calendardayreporthold,
registry/rentdetermination rights and differing notices/assistance sheets.

Collected7PDFs64pages;23pages read and visually inspected. Originalmediation
27pages:reviewed1–6,8. Amendment3 26pages:reviewed1–4,6. Remaining41pages are
retained historical tax/assistance appendices,not substantively reviewed. Images
generated for additional pages are not evidence of visual review. Three clerk
forms8pages andPIPtransfer/vacatur3pages fully reviewed. No currentfunding claim.

Feehelper `scripts/broward_clerk_fees.py` preserves37Countyrows (17/10/10) and
30Circuitrows (17/9/4),including repeated charges in different sections. It rejects
changed heading/count/shape/amount rather than silently dropping rows. Exactquotes
matched both originals andCircuitvalues matched119receipt.114focusedtests passed.
143citations/1399artifactreadbacks,replay/context and previous records/gaps/finalized
reports verified. Next Appeals in operationalqueue; county remains incomplete.

## October16 — Appeals operations, checkpoint121

Capture 4758 (`6558b2d69fd15ff2257a43b25868d800ca730b0e55a8720e82040833d5b88762`), stable entity
`broward-clerk-appeals`; receipt `receipts/clerk-appeals-reviewed.json`.
Read retained `clerk-appeals` six panels and contact sidebar. Office West Building,
4th Floor04140,201SE6thStreet,FortLauderdale33301;9548315751;weekdays8–15:30
except holidays. Five fee rows in three tables, not the civil single-table shape:
100Clerk/300DCA under CircuitCivil/Family/Felony/Probate heading;281Traffic;
3.50perinstrument/document and7sign/seal. CountyCivil not inferred into heading.

Overview says county notices directly to District Courts; HowtoFile says Clerk
Appeals Division. FourthDCA trial instructions direct original to trial clerk and
copy to opponent same day. Administrative instructions also direct copy to DCA.
Save distinctions without choosing controlling authority. Notice original signature,
order attachment and mail/hand-delivery choices are undated form statements,not
a determination that electronic filing/service is prohibited. DCA Forms Next.js
page is folder content; original stripped HTML shell was insufficient. Existing
folder helper extracted description/nine links; only notice/two instructions reviewed.

Clerk AppellateGuidelines PDF has broken font mapping in both extraction tools.
Original/garbled text retained; labeled manual transcription from inspected page
shares original hash/URL/retrieval timestamp, with its own text hash. Updated
November3,2020 and refers2020-89; preserve earlier2018guidelines separately.

GeneralOrders actual2026/04link serves2020-89, signedNovember3,2020/effective
January1,2021. Tenphysical pages:8order+2attachments; all text reviewed,4–10visual.
Expressly supersedes2019-6, but attachmentA still cites2019-6 and lists reply briefs
while body limits initial/answer. Keep both. Record2extensions/120initial and
2/60answer, exclusions,50dayrecordnotice threshold,10court-business-day return,
2page emergency request, Word/RTF proposed orders versus PDF copies. Distinguish
courtesy email/service from correspondence and actual Clerk filing. Historical
Bowman appointment not current roster verification. Chapter2020-61 pages4,6
reviewed visually for deletions/additions and effective dates; no deleted rule
converted into current law. Reused12-page AO2020-97 secondamendment,body1–3
reviewed; transfer case lists/attachment not reviewed in this task. Historical
January29,2021 deadline/eDCA instructions not present operational assertions.

Seven PDF sources32pages collected,19text/13visual reviewed;13pages outside
substantive scope. Shared indigence/email-excusal/party forms reused, not refetched.
Five discrepancies saved; all94citations/1386artifact bytes and semantic facts
verified; exact/frozen replay, context, previous records/gaps and finalized reports
preserved.99focused tests passed without warnings. Next Evidence; county incomplete.

## October16 — Evidence and Archives, checkpoint122

Capture4762 (`82f7583b23a23df787ead2130a7289fbb4d586e0d736fbd2a0349030c3ff6791`), separate entities
`broward-clerk-evidence` and `broward-clerk-archives`, receipts under those division
names. Actual Clerk-home links lead to `/Divisions/Evidence` and `/Divisions/Archives`.
Six Evidence panels include `FeesandCosts` (lowercase a); four Archives panels
include `PaymentMethods` and `ArchivesFees`. Expand FAQ bodies and read contact.

Evidence requires appointment for copy/retrieve/view; listed photo ID and signed
delegated-release document. Preserve separate court-order release conditions and
sealed/exempt access. First-day exhibit list uses sequential numbers; pre-marked
identification uses letters/color labels; label also has admitted number. Preserve
six list fields/five label fields and green/pink/gold/blue mapping. Back placement
recommended. No downloadable label in these panels. Reuse2022-37 September2original
and September12Amendment1: numerical remote upload2businessdays before, admitted
evidence/log filing5businessdays after log receipt. Amendment excepts specified
magistrate/hearing-officer proceedings from in-court-clerk requirement. Do not merge
CMS upload with Clerk filing or overwrite judge-specific evidence procedures.
Both Evidence5537/5539 numbers are phones per HTML, email evidencedivision;
WestBuilding,no room listed. Five fees2/1/2/5/6 retain units and oversize dimensions.

Archives: CircuitCivil1915–Present,CountyCivil1989–Present are published service
ranges,not proof all historical records survive or are online. Other ranges retained
without expanding criminal/marital review. Generic search fields and access exclusions
preserved. PaymentMethods permits personal/business/traveler checks, while fee panel
omits those; no inferred ban. Four fees2/1/2/7 with distinct units. EastBuilding03305,
6565option3. Escrow FAQ requests deposit plus letter, use-based amounts, unique
organization number and charges against balance. Linked Finance confirms West18120,
6244phone/6115fax. Invoice email not escrow email; no separate escrow form/minimum
found. No account opened, money sent or individual records requested.

66citations/1381artifact bytes and semantic facts read back; exact/frozen replay,
both contexts and prior records/gaps/finalized reports preserved. Source scopes,
conflicts and original retrieval times retained. Next RecordsRequest; county incomplete.

## October16 — Records Request and access standards, checkpoint123

Capture4766 (`d8d80616eb43261a799d553b2b6e6a021b555fe263d77ed14d76cf02e143ab5a`), stable entity
`broward-clerk-records-request`; receipt `clerk-records-request-reviewed.json`.
Actual `/GeneralInformation/RecordsRequest` has5relevant panels plus duplicated
marriage panel screened only.24directory quotes match prior institution record.
Request PDF lowercase/uppercase URLs byte-identical,onepage,revised2022-08-22,
visually checked. Redactarchives@browardclerk.org/fax9548315550,East03-305;
2week processing estimate,send once,cost notified after processing,no mailed cash.
Seven fee entries preserve channels:8electroniccertified,1/pagecopy,2/document
certification,2/yearsearch for each physical/request channel. Form lists Discover,
request overview omits it. Form property-deed/appraiser referral differs from page
recorded-deed/RecordsTaxesTreasury referral; retain both.

ElectronicCertifiedDocuments4panels/15FAQs reviewed:100-page purchase exclusion,
no wet seal,digital certificate,nonexpiration claim separate from30-day download,
check receiving agency acceptance. eCertify email sender,spam/receipt recovery;
two malformedFAQhrefs preserved with working navigation separately. CaseSearchECA
and web2/eReceipt are guest/empty landings only; no query,checkout,account or upload.
200resultcap,requirednames/datepair/civilcaseformat and missing-image limitations
recorded. Videos/widgets not exercised; cryptography not independently certified.

Access page links old technology-standards.stml returningHTTP200not-found. Official
search found current Services/information-technology/oit-resources/technology-standards;
Next.js folder helper extracted actual links. Downloaded September2024standards14pp,
matrixv15onepage,AOSC24-65eighteenpp. Standardsreview1,2,4,5,6,8,13,14text;
1,2,4,5,6,13,14visual. Matrixlegend,sixcivilrows/roles3,4,5,7,11visual; retain
sealed/expunged overrides. Order1–3text/3visual,signedSeptember16,2024,express
supersession; attachments collected but not double-counted as reviewed. User role,
confidentiality,VOR,replicated records and authorized-index-automation limits saved.
No exhaustive criminal/agency-cell review. Four distinctPDFs34pages,13text/10visual.

98citations1415artifacts verified/read back; exact/frozen replay,entity context,
prior records/gaps/finalized reports preserved.99focusedtests passed,no warnings.
Workflow/test-plan instructions record source paths and pitfalls. Next eFILING.

## October16 — E-filing and Portal source comparison, checkpoint124

Capture4770 (`91896ef18672a91178c4e474da563bf673558103a07d3178bb8a5b65fb79c9f8`), entity
`broward-clerk-efiling`, receipt `clerk-efiling-reviewed.json`. Actual source
`https://www.browardclerk.org/GeneralInformation/eFILING`: General,
AdministrativeOrders,FAQs and26answers read;22 checklist topics saved.
Clerk processing eFiling@browardclerk.org requires case type/reference in subject;
Portal support support@myflcourtaccess.com/8505774609; firm registration mailbox
separate. Preserve proposed orders to judge, filing with Clerk, and issuance versus
service of process. Reuse individual judicial procedures for CMS/email details.

Clerk-linked December2018manual correction pages126–134 and training-index
September2025manual109–113 reviewed. Clerk5days/oldmanual5business days/newmanual
30business days retained without deadline calculation. Replacement timestamp and
payment settlement statements differ. November2021commerce notice describes
submission settlement/correction refund; older Clerk/manual acceptance statements
remain. PDF/A preference/requirement and published8.5x12 typo retained. Portal
training actual href inventory saved.2017service guide body reviewed; screenshots
and modern authenticated behavior not independently tested. Editor comment on
2025manualpage111 visibly present,not adopted as an instruction.

Three-page civil rollout2012-16 fully reviewed. SC11-399 is revised opinion dated
October18,2012,despite ClerkAOSClabel/filename; selected shared-rule appendix
strikeouts visually checked. Deleted follow-up paper/risk clauses not treated as
operative additions. AOSC13-48 criminal rollout body screened only,attachments
collected. Scan-only2013prohacvice letter visually read; selected manual transcript
has own text hash and original provenance,empty extraction retained. Firm form
footer2013-09-12 checked. PDF/A visiblecover2021-08-24 differs fromindex2021-04
and machineheader2019-02-11; software tutorials not reviewed.

Clerk2025/07complex-order link404; previously reviewed2026/04official-index copy
reused with separate provenance. Twelve source differences saved without resolving
which controls. Eleven new PDF originals396pages collected,65text/23visual pages
reviewed within stated scope; reused complexorder not double-counted.
126citations/1456artifacts verified/read back; exact/frozen replay,entity context,
prior records/gaps/finalized reports preserved.90focusedtests passed,no warnings.
No account,casequery,filing,service,message,payment or publication performed.
Next FeesAndCosts; statewide goal active and Broward incomplete.

## October16 — Consolidated fee comparison, checkpoint125

Capture4774 (`6cc064bb4b439e192fea4abc7fcfd57e04f6f2da38a72b8f93b43df3bba43115`), stable entity
`broward-clerk-global-fees`; receipt `clerk-global-fees-reviewed.json`.
Actual GeneralInformation/FeesAndCosts has CourtFilingFees with eight tables.
Scoped existing strict fee extractor to CircuitCivil table3 andCountyCivil table4;
original HTML/text remain citation evidence,temporary wrapper not a source.
81selected rows:30Circuit,37County,2civilappeals,4Archives,1Familysharedthreshold,
7estate/trust entries. All73overlapping label/amount pairs match prior division
receipts exactly. Repeated fees remain in their sections,not summed;payee notes
remain distinct from blank/zero fees. No new PDFs or repeat division acquisition.

Three discrepancies preserved: shared Family row >15,000 vsCircuit >50,000;
global indigence wording vsprior page/form;Archives shortened payment list vs
separate PaymentMethods. No controlling-authority resolution or jurisdiction
inference. No revision/effective date stated in reviewed table bodies/headings.
Other personal-status/traffic rows screened only;marriage/passport panels retained
without substantive expansion. Cross-page matches do not prove no change over time.

260nested citations/1432artifacts verified/read back; exact/frozen replay,entity
context,prior findings/gaps/finalized reports preserved.106focused tests passed,
no warnings. All8scheduled operational sources reviewed within scope; overall
Clerk/county coverage remains incomplete for selected news and other county tasks.
Next selected dated Clerk news; no next county before user review.

## October16 — Dated Clerk announcements, checkpoint126

Dated Clerk news saved capture4778/packet126 (6beed1bdbf757fd09f1172d0737c0cacdcd60b64e639666429790cd667652419);11selected notices,19topics,8discrepancies;114citations/1476artifacts readback/replay/context verified;106focused tests passed without warnings. Six PDFs55collected/50text/18visual pages. All8scheduled Clerk operations plus selected news reviewed within scope.90named judges reconciled/12other officers reviewed with gaps. Next material access orders,navigation,gaps/countyreview. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

See COUNTY_WORKFLOW.md dated-announcement task card and review/news-validation.json. Receipt: receipts/clerk-dated-news-reviewed.json. The archive panel contains44articles;11priority bodies reviewed. The June2025 notice now links an October2025 order: preserve publication label and later body evidence separately. The rule link returns a2014version; preserve it alongside the corrected2025opinion. Keep30days in the opinion separate from30business days in the Portal manual. Historical flood relief and fee increases are not new2026changes.

## October16 — Courthouse access orders, checkpoint127

Courthouse access orders saved capture4782/packet127 (5f35569ee237bb34b4aa17bfd589a1a128dc45e02c686e6cfdc8d8ab7844228f);4orders/6pages read,5pages visually checked,9topics,29citations/1464artifacts verified/readback/replay/context. Exact Temp/Gen vacatur identifiers preserved. Prior findings/gaps/finalized reports unchanged.90named judges reconciled/12other officers reviewed with gaps. Next resource navigation (original agency/Acclaim downloads403; web extraction retained),gaps and county review. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

Discovery: General Orders table, actual2026/04PDF links.2019-91-Gen security recording;2023-26-Gen employee/judge badges;2023-28-Gen closure authority;2023-44-Gen vacates2023-28-Temp, a different suffix. All six PDF pages read; all except recording-order page1 visually inspected. Dates read from signatures, not download folders. No additional effective/revision dates stated. Prior2025-38security,ADA/rooms and2025holiday-label evidence retained.

Navigation drafts: property appraiser https://www.bcpa.net/ and linked RecMenu.asp; separate tax collector https://browardtax.org/. Official Records discovered via county agency to https://officialrecords.broward.org/AcclaimWeb. Three direct agency/Acclaim requests returned403; response bytes retained. Web-tool extraction saved in review/navigation-web-tool-evidence.json, explicitly not original HTML. Playwright wrapper launch permission denied; no bypass or browser-session claim. No personal records queried, disclaimer accepted, login, payment or contact. Finish navigation provenance/coverage review next.

## October16 — Navigation and county audit, checkpoint128

Resource navigation saved capture4786/packet128 (a701bce6bef2c5ce36a28352a91f6aaec1a802eb995502da53f5780ee3122ced);4endpoints,11citations/1458artifacts verified/readback/replay/context. Official Records/agency originals returned403; provider-only extraction retained separately.90named judges reconciled/12other officers reviewed with gaps. County audit identified material civil-order review candidates; check alternate copies then review missing commercial/shared orders before county review. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

Public court-record landing is /Web2/CaseSearchECA. Clerk home navigation names Property Appraiser, Records Division and Tax Collector separately. Property Appraiser homepage links RecMenu.asp; eight actual search-button URLs inventoried without submitting searches. Tax Assessor nav should use the appraiser, not collector. AcclaimWeb destination is supported by separately retained web-provider extraction, not raw original HTML; source HTTP status remains unknown for provider extraction. Three raw403 responses retained as failed attempts. No validator weakened or200status invented.

Gap audit must include evidence_limitations and next_actions inside all findings, not just top-level source checks. Old Rebollo next_action still calls Marra pending despite completed Marra finding; preserve history and record later reconciliation instead of deleting old receipt. Audit all material civil/general/county/local-order index entries, then distinguish reviewed originals, separate alternates, unreviewed collections and scope exclusions. Filename/url mismatch alone does not prove missing content.

## October16 — County completion audit, checkpoint129

Navigation128/capture4786 verified. County audit129/capture4790 (1a6885d620af55130196fa4e978098865095b10879660e0e79108c55df281c21) saved and frozen replay/context verified;158index rows,85material review/reuse candidates,402embedded limitations,340contact field states,11prior actions inventoried. This is discovery, not completed review.90named judges reconciled/12officers reviewed with gaps. Next review/material-orders-next.json: reconcile alternate copies, then nonbinding arbitration/property fraud/property-loss and remaining material shared orders. Disposition embedded limitations before county review. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

Sources: orders-index, civil-orders, general-orders, newly collected county-orders-index and temporary-orders-index. Each index row retains exact text/links and explicit relevance decision. Exact URL/hash citation associations are leads, not whole-document review proof. Current temporary senior-judge/assignment orders remain audit candidates; expired/election/commissioner titles were screened without exhaustive content review.

402limitations and340contact-field states are existing database annotations, not402missing documents. Eleven prior next_actions preserve their original wording. Later Marra observation4634 supersedes the old pending-action premise, while Rebollo current fields remain unknown. Three umbrella check reasons updated to the actual outstanding audit; no source gaps cleared or old findings overwritten. All originals, provider-only discovery and finalized reports retained.

## October16 — Nonbinding arbitration, checkpoint130

Nonbinding arbitration130/capture4794 (f4773d8928747d0b2b0a03f1f1c1173cf4ed9d933ba9c53157eb5bccdfaa0ac2) saved and verified: order plus10unique standalone forms,27pages text/15visual,16topics,6source differences,66citations/1502artifacts readback/replay/context. April2024body and June2026filename exhibit cue separate; attachment inventory, fee/email/service versions preserved. Prior findings/gaps/finalized reports unchanged. Next property-fraud order in review/material-orders-next.json index1, then remaining material review/reuse and embedded limitation audit.90named judges reconciled/12other officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

Civil index links AO2023-10-Civ Amendment1 with filename exhibits-revised-June-2026.pdf. Body signedApril30,2024 expressly allows separate exhibit revisions. Actual9pagePDF containsAapplication, Bsingle referral, Ccounty notice, Dstatistics; body advertises additional forms. Mediation & Arbitration hub supplies11links/10unique PDFs, including general/panel/county versions and shared acceptance link. All27PDFpages read;15selected pages visually checked. Form dates not inferred from2022path.

Preserve revised county1500/750three-hour branches versus standalone750cap/plaintiff default and general/panel1500perday/175advance. Revised application countymed email differs from named standalone email; revised referral adds email/compensation text. Rendered revised statistical question says before or not later; original extraction misreads after; separate transcript retains original provenance. Standalone question visibly differs. Old service certificate choices retained alongside separately dated2025electronic-service opinion. No authority resolution. Arbitrator roster linked only, not judicial roster expansion. Receipt nonbinding-arbitration-reviewed.json; next priority task property-fraud order.

## October16 — Joint property-fraud order, checkpoint131

Property-fraud131/capture4798 (4556e15a7321eecd122ce85cf444c91ea094797271ae0a564f4b46061da6668a) saved and verified: joint circuit/county Amendment2,2pages text/visual,8topics,15citations/1491artifacts. County index404 preserved; complete circuit-index original separately reviewed,not byte-identity to failed URL. Reassignment discretionary/order-based; fee waiver limited to reassignment; remote hearing option retained. Next property-loss order at review/material-orders-next.json index2.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

Civil row25 and county row34 identify AO2023-16-Civ/2023-17-CO Amendment2. Actual county2024/04link404; actual circuit2026/04link200. WorkingPDF header identifies both numbers, signedApril3,2024; no separate effective date. Full2page text/visual review covers qualifying real-property ownership allegations, six action categories, surplus claims with same predicate, discretionary Division03reassignment byorder, original case number/no reassignment fee, attendance consideration with remote option, and unchanged applicability of51.011. Existing Casey and Clerk quiet-title-form records linked, not rewritten. Both priority entries now covered by one joint order; preserve failed response and both discovery paths.

## October16 — First-party property-loss order, checkpoint132

Property-loss132/capture4802 (633ba894cfb17af2997dbad64d7a7dff8f3f3149cac4772419c84c3b5dc461f0) saved and verified: AO2025-25-Civ and both forms,16pages text/14visual,27topics,15table rows,4internal discrepancies,3historical comparisons,95citations/1505artifacts. Express supersession and AI/mediator wording changes retained without overwriting13prior citation-associated records. No case dates or controlling authority inferred. Next county mediation order at review/material-orders-next.json index3.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

Civil index row31 →2025-25-Civ, actual2026/06combined PDF. Body signedJuly24,2025; no stated effective/exhibit revision date. Physical1–2body,3–13CMO,14–16trial form. Entire16pages text reviewed; physical2,3,5–16visually checked. Keep15deadline-table rows, paragraph-specific actions/triggers and four table/prose or sequence issues. Historical Amendment3 reused for AI paragraph and mediator-window comparison; express vacatur of Amendments1–3 recorded, not adjudicated.13old-source citation-associated entities retained unchanged; association is not adoption/assignment. Existing ESI and generic service-notice reviews reused. Save/finish scripts, receipt, frozen packet and validation are under this run; next county mediator/referral order.

## October16 — County mediation, checkpoint133

County-mediation133/capture4806 (971c3ab611a069015129dfd44ddedb4ba24c8e218fd5313b76f38198f5a6b3a3) saved and verified: AO2023-6-CO Amendment1 and AttachmentsA-D,13pages text/12visual,21topics,3case paths,4discrepancies,45citations/1506artifacts. Supporting standalone CMAP statistical/time/invoice templates not located; separate gap retained. Next small-claims credit-card order at review/material-orders-next.json index5.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

County index row32 →2023-6-CO Amendment1, actual2024/10PDF. SignedOctober21,2024; no separate effective/form revision date. Physical1–3body,4–7A county/nonresidential,8–9B small claims,10–12C residential,13D report. Keep10/5day selection,60/15day mediation,private5day eportal versus CMAP30day administrative return/residential10day sheet, hourly350/250caps and CMAP60-per-party/conditional-free paths separate. Body/form may/shall and under15000/15000orless differences, residential extension contradiction and report fields preserved. Four official HTML menus inspected with PDF guard after discarded broad-inspection warnings; bounded searches found references,not current standalone county CMAP statistical/time/invoice templates. Existing family and arbitration forms not substituted.

## October16 — Credit-card shared review, checkpoint134

Credit-card134/capture4810 (adeab935c4cacf7346cd984d294292a3721729a3570f1593209153f734fa6fc8) saved and verified: AO2026-25-CO,4pages text/3visual,11topics,4retained comparisons,28citations/1499artifacts. Three prior person reviews verified; repeat original/text hashes identical. July1effective date, literal130before/150after anomaly, waiver/transfer/default triggers preserved. County-mediation133/capture4806 also verified; supporting CMAP template gap retained. Next ESI panel order at review/material-orders-next.json index6.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

County index row48 already associated with ao-2026-25 and McCarthy/McCaulRicca/Clermont reviews. Full4page review scope verified in each receipt, not inferred from citation presence. Repeat retrieval original/text hashes identical; new timestamp retained,not new legal content. Complete order reread; pages2–4visually checked. Preserve narrow small-claims credit-card47/101/102scope; issuedJune29/effectiveJuly1,2026; literal130before/150after window;120-day proof,5-day extension, noon3business-day waiver/transfer,30calendar-day default package anchored to case default order. Four prior Clermont comparisons retained, person observations unchanged. Workflow adds reuse-before-fetch and bounded semantic receipt inspection to avoid giant citation output.

## October16 — ESI panel history, checkpoint135

ESI-panel135/capture4814 (3eb20743ae7d5dc4cc40505c0666c4668c9a40f18c182dd260834986a66d3947) saved and verified:2020-87-Gen,2pages text/visual,5topics,8citations/1497artifacts. Historical panel120-day period is not litigant deadline;5members not current judicial roster. Related2021-20recitals reused. Next record-newspaper order at review/material-orders-next.json index7.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

General index row19 →2020-87-Gen,actual2026/04PDF. SignedOctober27,2020; no separately stated effective date. Establishes at least5attorney panel to propose best practices;120days from effective date applies to panel,good-cause extension possible. Names retained as historical appointments; no added judges/current panel assertions. Suggestions about special masters/examiners are topics to consider,not mandatory appointments. Existing2021-20recitals state panel provided recommendations; substantive review remains separate.

## October16 — Record newspaper, checkpoint136

Record-newspaper136/capture4818 (ee3bb0def89335c5b3a6d471fa9cdc671ef0f674829b38a489e9d557c5982bdb) saved and verified:2023-43-Gen,1page text/visual,3topics,4citations/1498artifacts. Sun Sentinel designation limited to stated50.0711matters; no universal legal-notice rule or current publisher status inferred. ESI-panel135/capture4814 also verified as administrative history. Next professionalism order at review/material-orders-next.json index8.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

General index row31 →2023-43-Gen,actual2026/04PDF. SignedNovember13,2023; no separate effective date. One page text/visual reviewed. Sun Sentinel designated for section50.0711matters; express2012-21supersession retained. DailyBusinessReview cessation recital is a2023statement,not a fresh business-status assertion. No publication vendor research,universal-notice mandate or case deadline inferred.

## October16 — Professionalism procedure, checkpoint137

Professionalism137/capture4822 (ba9173345540e2b4dbe416c73b286a82306d690feb4d8363f161afb9bfcdc5af) saved and verified:2025-45-Gen,referral form,dated13member list;8pages text/7visual,11topics,38citations/1515artifacts. Two404member paths preserved; hub original recovered. Four judges unchanged; no discipline/compulsory attendance authority inferred. ESI-panel135 and newspaper136 verified. Nine-entry priority batch reviewed; next reconcile remaining county-completion-audit rows/review scopes and evidence-gap dispositions.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

General index row37 links AO,referral and broken member path. Official /broward-professionalism-panel/ supplies working /2026/06/LPPmembersupdated11426.pdf,datedJanuary14,2026; April-index and January-search paths404. Five-page order signedNovember26,2025 vacates2023-29Amendment1; two-page form directs Chair MilesMcGraneIV,mmcgrane@conroysimberg.com,3440HollywoodBlvdSte200,HollywoodFL33021-6923.13member table visually reconciled,4judges not rewritten. Report bodies remain outside scoped procedural review; two date labels share one actual URL. Direct originals override no web-provider availability claim; failed404text/image inspection not counted. Finalizer corrects generic acknowledgment labels:one standalone form,one member list,not attached forms.

## October16 — Index reuse reconciliation, checkpoint138

Index-reconciliation138/capture4826 (2ba88c756dfb737d8d3090ca210fb08504c21dc32b24ced4f8e199834b39e50b) saved and verified:158rows,33rows with page-specific reuse evidence,9priority reviews,73prior scope screens,43remaining original/review-scope followups. One reused appeal-order body retains unreviewed historical attachments4-12.158index citations/1529artifacts;no findings added or history finalized. Original402limitations/340contact states/11actions preserved for disposition. Next review/index-reconciliation.json:general-orders48 current assignment order,then current temporary orders.90named judges reconciled/12officers reviewed with gaps. Broward incomplete;statewide goal active;cloud direct;no next county before user review.

reconcile-index-reviews.py matches exactURL,successful original/hash and page-specific receipt metadata,retaining receipt JSON pointers/hashes. Source presence alone is insufficient. Nine dedicated priority receipts resolve their row-specific alternate/missing-link history. Entire row stays pending when another linked form lacks review evidence;33reused rows retain scope limits and43remain followups. Partial2020-97appeal attachments remain unreviewed,not silently promoted. New audit saved as draft without adding findings;original158row audit and embedded limitations unchanged. Next ordering puts current assignment/senior orders first.

## October16 — Current assignment order, checkpoint139

Assignment checkpoint139/capture4830 (b504245b758ebc2b62350f23322e660194210ebdf9a99589c51646c879cae744) saved and verified: AO2026-37-Gen,135 assignment rows,two explicit vacancies,101 existing person keys;all6pages read and visually checked.169 citations/1515artifacts;dated exceptions and Stephen/Steven discrepancy retained. Individual/contact records unchanged;Rebollo gap retained.42 index followup rows remain plus embedded gap disposition. Next review/index-followup-progress.json:temporary-orders-index18.90named judges reconciled/12officers reviewed with gaps. Broward incomplete and unpublished;statewide goal active;cloud direct;no next county before user review.

Search path: general administrative-orders index row48 → September2026 AO2026-37 PDF. No exact/alternate matching original existed in acquisition inventory; original acquired under assignment-order-2026-37. All135 rows transcribed against rendered cells, preserving two vacancies, role typography and separate effective dates. Source body can garble FO/FP,41/42,47/48,100/102 and community-court pairings; inspect page layout. Only existing person-key associations saved; no new contact observation. Prior index reconciliation138 remains immutable; index-followup-progress.json carries42pending rows. Complete source review does not finalize county or resolve source conflicts.

## October16 — Assignment provenance correction, checkpoint140

Latest capture140/4834 (a9fea4a556e19fb38abf86c0b17954f978ec875b91db6ff77c57484e85c47b02) corrects discovery parent to https://www.17th.flcourts.org/general-orders/;1517artifacts verified,substantive facts unchanged. Initial correction save rejected absolute artifact path; changed to repository-relative path and reran successfully;dependent freeze reran after successful save. Corrected receipt: receipts/assignments-2026-37-provenance-corrected.json. Earlier original and capture remain intact. Next task unchanged.

## October16 — Temporary and county civil assignments, checkpoint141

Assignment followup141/capture4838 (1c5826a6705df974237774540286aae9a911c1a121cac8b8ac2c54bee97e28e4) saved/verified: five orders,11pages read/visually reviewed,199citations,1534artifacts. Reciprocal quarters retain89/88names and distinct periods;senior order9names adds8pending individual reviews. Division50 lists and satellite-jury retention/location rules retained. Two discrepancies preserved.37index rows remain plus gap disposition and eight senior records. Next senior Richard D. Eade;finish each senior before next. Existing90named-person/12officer records unchanged;no county publication. Statewide goal active;cloud direct;county review before next county.

Sources: temporary-administrative-orders-2 rows18,20,16;county-administrative-orders rows45,46. The five originals were absent from retained exact/alternate acquisition URLs. Court-year and fiscal-quarter labels are not reporting-period dates. Source review fully covers11pages and does not supply missing senior contacts. Full pending senior list is in review/index-followup-progress.json;current public roster alone misses8assigned senior judges. Reuse existing Pole receipt rather than restarting his review. Retain the first-quarter Woody D./second-quarter Woody R. difference and paragraph-specific Division50 lists. Signature/effective dates can be reversed;do not normalize them.

## October16 — Richard D. Eade, checkpoint142

Checkpoint142/capture4842 (38ac1081dafb4764ec6784580751718e8580b259ec3e05ffc670e89906c102d0) saved/verified Richard D. Eade senior assignment with current contacts/procedure explicitly unknown.26citations/1542artifacts;official E-filter/site search,Chief Judge and Supreme senior page reviewed. Embedded Supreme folder body recovered with existing helper;historical contact snippets excluded.90previous named-person/12officer records unchanged;Eade not counted fully complete.7senior reviews pending,next Sandy Karlan.37index rows plus existing gap disposition remain. Prior141 reviewed5assignment orders/11pages. Broward incomplete/unpublished;statewide goal active;cloud direct;user county review before next county.

Reproduce bounded paths and search queries from review/eade-search-log.json. Judiciary E-filter lists Evans/Eves,not Eade;site search returns no result,not proof of no procedures. Senior appointment original establishes inclusion. Chief Judge and Supreme public-information contacts remain separately labeled administrative routes,never chambers substitutes. Supreme /Employment/Senior-Judges redirects to /the-court/about-the-court/employment/Senior-Judges and renders only shell text to basic extraction;reuse scripts/flcourts_folder.py for pageData.description.html5/nestedblocks. Derived source senior-supreme-hub-content retains exact original/timestamp and separate text hash. Application phone is excluded from individual contacts. Historical2008directory and old foreclosure-program search leads were not collected or accepted as current. Current fields remain explicit gaps;no request,email or call sent.

## October16 — Sandy Karlan, checkpoint143

Checkpoint143/capture4846 (0050433bfc6fe5a721daed6e73d7d801dc9d9f90fbc9827eb3d0a10df1934947) saved/verified Sandy Karlan senior appointment with current chambers/assistant/procedure gaps.26citations/1541artifacts;March19Miami directory page7 and October16API directory page9 reviewed visually/textually,distinct dated name lists and separately labeled coordinator retained.17PDFpages collected,3reviewed including reused Broward assignment;other Miami pages unreviewed.90previous named-person/12officer records unchanged;Karlan not counted fully complete.6senior reviews pending,next Phyllis Williams Kotey.37index rows plus existing gap disposition remain. Broward incomplete/unpublished;goal active;cloud direct;county review before next county.

Paths/queries:review/karlan-search-log.json. OriginalAPI PDF downloaded today prints October16and omits Karlan on senior page9;search cache returns June23text naming her. Static documents/judicial_directory PDF prints March19and names her on page7. Save both originals;do not substitute cached snippets or infer a Broward appointment termination. Coordinator Odalys Somodevilla/3053497008 is a separate Eleventh Circuit route,not Karlan chambers/JA. Only senior-list pages reviewed;no Miami county baseline initiated.

## October16 — Phyllis Williams Kotey, checkpoint144

Checkpoint144/capture4850 (5295cfe10420816bc20afffbb3e036a6377747914d2b4d8fb6698ca5a3d73727) saved/verified Phyllis Williams Kotey senior appointment with nine current contact/procedure fields unknown.26citations/1543artifacts;retained K-filter/shared hubs reused,official name search and bounded domain searches reviewed. Academic CV/committee contacts not substituted. Prior143retains Karlan's dated Miami directory differences.90previous named-person/12officer records unchanged;three new seniors reviewed with gaps,five pending,next Lester Langer.37index rows and gap disposition remain. Broward incomplete/unpublished;goal active;cloud direct;county review before next county.

Review/search receipt:review/kotey-search-log.json. Current2026-40senior appointment reused;K-filter from Karlan reused without downloading again. No Kotey-specific profile/procedure identified. Historical FIU2019CV and2002JEAC committee search leads are not judicial chamber/assistant sources and were not newly collected or analyzed. Shared Chief Judge/Supreme public-information routes separately labeled. Current contact/procedure gaps persist;bounded review done before next senior.

## October16 — Lester Langer, checkpoint145

Checkpoint145/capture4854 (f0b11c927ff3ba5cbf99a54465f18ced78c86eb4ce8212e6c8a9b39ccb2d82a7) saved/verified Lester Langer Broward senior assignment and separately scoped Eleventh Circuit coordinator route.26citations/1551artifacts;retained October16directory page9 and current senior card identify Langer.Individual Broward chambers/assistant/procedure fields remain unknown. This turn143–145saved Karlan,Kotey,Langer with gaps;Karlan's dated directory difference preserved.90previous named-person/12officer records unchanged;four new senior bounded reviews saved,fourpending,next Susan Lebow.37index rows plus gap disposition remain. Broward incomplete/unpublished;statewide goal active;cloud direct;county review before next county.

Paths/queries:review/langer-search-log.json. Same-day API directory originally collected for Karlan reused,not downloaded again. Its last page names Langer and directs senior contacts to Odalys Somodevilla/3053497008. Current Miami directory card data-judgeid670 is not a profile link;linked public script only filters cards by judgeId. Preserve listed route as Eleventh Circuit senior contact,not individual Broward chamber/JA. Historical family plan not substituted. Other Miami roster pages remain unreviewed;no next county begun.

## October16 — Susan Lebow, checkpoint146

Checkpoint146/capture4858 (bce0387eb33e9dbac251507ef16fb3c29e6af23dab3c16ac7286a2a699214989) saved/verified Susan Lebow: Broward senior assignment supported;individual contact/procedure fields explicitly unknown. 26citations/1553artifacts;exact frozen replay,facts/artifact readback and finalized reports preserved.90previous named-person/12officer records unchanged;5additional senior bounded reviews saved with gaps,3pending. Next Joseph A. Murphy, III.37index rows and gap disposition remain. Broward incomplete/unpublished;statewide goal active;cloud direct;county review before next county.

Person-specific paths/queries and exclusions: review/lebow-search-log.json. Receipt: receipts/senior-susan-lebow-reviewed.json. Broward senior appointment verified October1,2026–September30,2027. Current individual contacts/assistant/procedures not located in bounded official research. Historical directories/news do not supply verified current chambers contacts. Individual gaps remain incomplete;bounded review does not certify contacts complete.

## October16 — Joseph A. Murphy, III, checkpoint147

Checkpoint147/capture4862 (b3e24c56d3e4e661de8bd51afa0446d86a06a3f9caf6c5346e6c7ca408f357ef) saved/verified Joseph A. Murphy, III: Broward senior assignment supported;individual contact/procedure fields explicitly unknown. 26citations/1558artifacts;exact frozen replay,facts/artifact readback and finalized reports preserved.90previous named-person/12officer records unchanged;6additional senior bounded reviews saved with gaps,2pending. Next Louis H. Schiff.37index rows and gap disposition remain. Broward incomplete/unpublished;statewide goal active;cloud direct;county review before next county.

Person-specific paths/queries and exclusions: review/murphy-search-log.json. Receipt: receipts/senior-joseph-a-murphy-iii-reviewed.json. Broward senior appointment verified October1,2026–September30,2027. Current individual contacts/assistant/procedures not located in bounded official research. Historical directories/news do not supply verified current chambers contacts. Individual gaps remain incomplete;bounded review does not certify contacts complete.

## October16 — Louis H. Schiff, checkpoint148

Checkpoint148/capture4866 (96aac0ffefbb94f74fe7352c8d29b8c6756adf42076195d0f6aef3eba5fc9bc9) saved/verified Louis H. Schiff: Broward senior assignment supported;individual contact/procedure fields explicitly unknown. 26citations/1562artifacts;exact frozen replay,facts/artifact readback and finalized reports preserved.90previous named-person/12officer records unchanged;7additional senior bounded reviews saved with gaps,1pending. Next Mark A. Speiser.37index rows and gap disposition remain. Broward incomplete/unpublished;statewide goal active;cloud direct;county review before next county.

Person-specific paths/queries and exclusions: review/schiff-search-log.json. Receipt: receipts/senior-louis-h-schiff-reviewed.json. Broward senior appointment verified October1,2026–September30,2027. Current individual contacts/assistant/procedures not located in bounded official research. Historical directories/news do not supply verified current chambers contacts. Individual gaps remain incomplete;bounded review does not certify contacts complete.

## October16 — Mark A. Speiser, checkpoint149

Checkpoint149/capture4870 (cdc79b0bc6c6112aea21ed7becd991ab2ff03e8d6d7791f3164c0a4ad86b86c5) saved/verified Mark A. Speiser: Broward senior assignment supported;individual contact/procedure fields explicitly unknown. 36citations/1567artifacts;exact frozen replay,facts/artifact readback and finalized reports preserved.90previous named-person/12officer records unchanged;8additional senior bounded reviews saved with gaps,0pending. Next remaining county-index reviews.37index rows and gap disposition remain. Broward incomplete/unpublished;statewide goal active;cloud direct;county review before next county.

Person-specific paths/queries and exclusions: review/speiser-search-log.json. Receipt: receipts/senior-mark-a-speiser-reviewed.json. Current2026-40senior appointment verified. Historical2025-01Amendment3 names Speiser in divisions11/22 effectiveMay19,2025;retrieved foreclosure hub names Pole/Garcia-Wood. Keep dated source associations separate;current individual chambers/assistant/procedure remain unlocated. Individual gaps remain incomplete;bounded review does not certify contacts complete.


### Civil-index followup150: public alternatives and dated requirements

The civil administrative-order index rows2,4,5,6,10,14,19are dispositioned.
See `receipts/foreclosure-index-worksheets-reviewed.json` and
`receipts/civil-index-*-reviewed.json` in the county run for source statements.
Court worksheet DOC is accessible;the linked PDF points to internal `callisto-vm`
and was not requested. Clerk PDF/DOCX are separately reviewed alternatives.
The DOC/DOCX normalized body text matches;court/Clerk2012-16normalized text
also matches. Neither comparison is original-byte or layout identity.

The2011residential form retains its historical ADA/fee language without updating
current contact records. The2012e-filing order is an initial-rollout source.
The2016water-transfer order is signed March11nunc pro tunc March4.
The2018service order is limited to section790.401risk-protection proceedings;
no exhaustive subject review is needed for commercial-civil coverage.
The2020refiling order supplies division-assignment/correction steps.
Next exact row and URLs are in `review/index-followup-progress.json`;
read row21(vehicle ownership) before acquiring anything. Do not rerun save150
after the checkpoint has advanced;use its frozen packet for controlled replay.


### Index followup151: operative language and alternate originals

Twenty remaining index rows are dispositioned through sixteen cited receipts.
Vehicle-title order2021-13Civ/14CO includes both forms and the affidavit Sheriff
letter requirement. Emergency order/form alternates have normalized text equality
with retained copies,not identical original hashes. Civil2024-33was recovered
from the observed2026/04public upload folder after its indexed2024/12URL404;
manifest discovery metadata distinguishes the inferred path from an actual href.
County2020-67and2021-14links404;available circuit originals supply the reviewed
statements. All failed responses remain preserved with separate original gaps.

2012-24is corrected,signedJuly5,2016nunc pro tuncApril12,2012.2012-51is titled
as vacating but immediately reinstates VI-02-D-3. Save these statements without
adjudicating control. Cost schedules are collected and screened for traffic/criminal/
municipal scope,not exhaustively analyzed.2023-37/38signature lines omit the year;
month/day and order-identifier year are separate fields. Ten index rows remain;
next is county row13. Use frozen151for replay,not the mutating save script.


### Index followup152: queue accounted for; gap disposition next

The final ten rows have cited receipts: county relief,older pretrial form,writs,
firm filing-location exception,2013e-filing,2017general vacatur,duty-order reuse,
ADA forms,LocalRule1A,and10Aversion history. The ten receipts distinguish
actual reading from reused review and conditional/historical applicability.
All43followup rows now have unique dispositions;original158-row audit unchanged.
This is not county completion. Next read `review/county-completion-audit.json`
and create a separate gap-disposition ledger using later captures. Preserve
402original limitations,340contact states and11prior actions as audit inputs;
most are evidence boundaries,not automatically unfinished research. Include the
eight newly reviewed senior records and recent failed-link receipts in the current
county review packet. Keep Rebollo current identity/contact uncertainty explicit.


### Gap disposition153 and next delivery step

`review/county-gap-disposition.json` preserves all753original limitation/contact/action
entries with original observation references. Nine progress notes use later findings;
only the stale pending Marra action is completed. Missing templates/originals,
335unpublished/unestablished direct contact fields and specially attributed contact
values are retained. No claims of new acquisition or current contact completeness.
Regular assignment order names89judges+12officers; separate senior order names9.
Eight seniors retain missing individual evidence; Rebollo remains historical/current
uncertain separately. All43index followups are accounted for.

Next inspect existing directory schema/render/import code,then create a county
review/export packet that preserves source-specific contacts,unknowns,procedure
checklists and historical limits. Validate against current records and old-county
preservation before user review. Do not run the bundled-directory import expecting
it to consume these history findings. No publication/next county yet.


### Read-only county review export from capture4886

Broward read-only review export built from capture4886: output/county-review/broward-4886/index.html. 178 exact saved findings (98 judge,12 officer,clerk,administration and shared procedures/reconciliations),1274 original/extraction artifacts. All facts/citations and artifact bytes read back;2398 local links checked;deterministic second export and unchanged database/directory/finalized reports verified. Six exporter tests and24 directory/history regression tests passed. No browser visual check or public release. Next inspect and implement the bounded production-directory integration: preserve all existing counties/history, explicitly add reviewed Broward scope, map source-attributed contacts without substituting historical/ancillary values, preserve conflicting assignment evidence, and review rendered output. Eight senior contact gaps and Rebollo historical/current uncertainty remain explicit. User county review before another county. Statewide goal active; cloud direct.

See `docs/workflow/COUNTY_REVIEW_EXPORT.md` for the reproducible command and
limitations. This export is not a new research observation and did not advance
the comparison baseline. Retain the immutable checkpoint153 and its frozen replay.


### Dated directory integration draft

Broward website integration draft built: output/county-review/broward-site-4886-v4/directory.html; pending supplement draft/county-directory-4886-v3.json derives from capture4886.112personnel records:89ordinary judges,9seniors,9magistrates,3hearing officers,clerk and court administrator. Default view combines them with181existing personnel;explicit issue/date queries retain saved historical contacts. 810projected contact lines and source observations/citations checked against packet;five archived reports/10historical JS selections unchanged;CLI preview deterministic and production gate rejects draft. 74focused/regression tests passed before final circuit-membership display adjustment;final actual-data CLI/Node check and JS syntax passed afterward. Source contact qualifiers retained in expandable notes;8senior gaps and Rebollo historical/current uncertainty preserved. No browser visual check: prior wrapper permission denial,execute bits absent;no workaround. Next complete manual projection audit for112records and omitted field ledger,inspect final rendered directory when browser capability is available,then present concrete county checkpoint for user review. Use docs/workflow/COUNTY_DIRECTORY_INTEGRATION.md. No research capture/finalized report changed,no public release,no next county. Statewide goal active;cloud direct.
