# Hillsborough baseline and research handoff

User selected Hillsborough on October 16, 2026, after accepting the Broward
research checkpoint. October 18: allow the existing Qwen3.8 shared-access
code-repair assignment to finish, then use cloud agents for research, development,
tests, repairs and checkpoint acceptance. Launch no further local workers.
After county acceptance, continue to Miami-Dade and Palm Beach without another
user-approval gate; see the current goal for subsequent population order.

## Pinned state

- Workspace: `runs/county-hillsborough/2026-10-16`.
- Scope: `{"profile":"county-baseline-v1","county":"hillsborough","circuit":13}`.
- Stream: `manual_research:county-baseline-v1:3b85d38b5acd`.
- Shared database: `/Users/cadespivey/.local/share/flwu/research-history.sqlite`.
- Opening capture: **4890**, `55a43ece379afc6e3342149f908e6e194ff393d323b2ee696f975beef52dff86`.
- County-stream prior finalized baseline: none. This is a first observation,
  not a report of newly adopted law. Weekly reporting remains Monday–Sunday.
- Latest capture: **5083**, `24753806f1721b7d7932d2199848b6a10fb5dd86235f7e7b9c8862f0ac6e57dc`.
- Latest immutable packet: `draft/checkpoint-97.json`.
- Research accepted with documented source limitations:69 named judges,8 magistrates,
  7 hearing officers and clerk. Receipt: `review/cloud-material-followups/county-research-acceptance.json`.
-461 findings/2418 artifacts readback; exact replay and five finalized reports unchanged.
- Final directory visual review/publication remains pending, separately from research
  acceptance, consistent with Broward's roadmap status. Native UI currently unavailable.
- Draft `draft/county-directory-5081-v1.json` remains pending; preview server8879.
- Next research county: Miami-Dade. No further local workers.
- After acceptance: Miami-Dade, Palm Beach, then descending population; no additional
  user-approval gate between counties.

Read the run's `state.json` and `RESUME.txt` before continuing. Finish the active
judge's contacts, assignments and applicable civil/shared procedures before
opening another judge's profile. Inventorying the roster is not a contact review.
The checkpoint narratives below are historical. After each save, update this pinned
summary and the goal's latest-checkpoint line as well as the run state and resume
file; appending a narrative alone leaves conflicting instructions for later agents.

## Official source map and extraction

Start at [Judicial Directory](https://www.fljud13.org/Directory/Judges).
Its three labeled download cards link to `directory-alpha.pdf`,
`directory-divisions.pdf` and `judges/judgesflowchart.pdf` under the official
`/Portals/0/Forms/pdfs/` path. Follow actual links, not assumed paths.

The saved HTML contains 69 `article.isotope-item` judge cards, each with an
`h3.title` and `a.full-link[href]`. Anchor text is empty; use the associated
heading, preserve the href, and resolve it against the source URL. Category
classes such as `c-circuit-civil` and `c--circuit-criminal` coexist. Preserve
original classes rather than silently dropping the doubled hyphen. No browser
pagination was needed to inventory these 69 saved cards. This does not establish
the completeness of magistrate, hearing-officer or named senior-judge coverage.

The alphabetical PDF has 68 distinct named body entries plus Chief Judge Sabella
in its header. Repeated assignments are not extra people. `MOODY III, James`
matches the Moody card only after explicit identity review; Sabella needs the
header. The separate unnamed Senior Judge/Circuit Civil M row is not a person.
All three PDFs state October 1, 2026 revision dates.

The pypdf extractor emitted invalid object-offset warnings. Originals remain
unchanged; all five PDF pages were rendered and visually checked. Table extraction
used `pymupdf` and was compared with those images. Do not treat linear extraction
of the assignment chart as reliable column pairing. Keep header and table roles
separate. Use `import pymupdf`, not its deprecated `fitz` alias, for later work.

Source differences include name initials/order, assignment labels and phone
values. They are recorded in `receipts/roster-reviewed.json`. Check the relevant
row again during that person's review; do not choose a globally preferred directory.

## One-judge source traversal

The first profile is [Darren D. Farfante](https://www.fljud13.org/Directory/Judges/Judge-Farfante).
It includes contacts, biography, forms, schedule and a long combined L/Z procedure
in the same original HTML. Read all relevant tabs/sections from that retained
original; do not treat the short biography as the procedure. Preserve different
schedule sections, conditional instructions and conflicting email/submission
routes. A law-firm asbestos calendar coordinator is not a judicial assistant.

Follow the profile's actual local-rule, administrative-order and sample-form
links. Material shared originals are acquired once and reused with their actual
retrieval time and review scope. Personal case records, login, JAWS booking and
emailing chambers are unnecessary for this public baseline.

## Acquisition and database save

`review/acquire.py` accepts a JSON list of `{key,url,parent}` from a saved request
file. It uses one bounded HTTP client, preserves original response bytes and
timestamps before extraction, saves hash-named originals/text and rejects an
existing acquisition key. Inspect its output and HTTP status. An extraction error
does not mean the original was lost; inspect `review/acquisition.json` before retry.

Checkpoint 1 was prepared by `review/save-roster.py` and saved through the existing
`flwu.baseline_capture` validator. Do not rerun this state-mutating script: it guards
against overwriting the checkpoint. New research needs a new immutable packet.
The JSON packet can be replayed through the checkpoint helper without creating a
second observation. Source bytes, semantic facts, replay and preservation of all
finalized reports were verified in `review/checkpoint-1-validation.json`.

For each judge, use the existing person receipt validation and structured checklist
from [COUNTY_WORKFLOW.md](../../workflow/COUNTY_WORKFLOW.md), then the explicit save
contract in [BASELINE_CAPTURE.md](../../workflow/BASELINE_CAPTURE.md). Do not import
this work into the frozen seven-county directory database or finalize an incomplete
county merely to expose it to later research. After the county review, use the
separately dated directory supplement path exercised with Broward.

## Historical Farfante progress — capture 4892

The complete profile/procedure text has been read and 17 checklist topics saved
in `draft/farfante-review-progress.json`. This is an unfinished person receipt,
not a completed judge finding. Local Rule3 (seven text pages; visual pages1,2,3,5,6)
and Business Court AO S-2013-021 (four text pages; signature page4 visual) have
separate reviewed findings. The three-page fee sample text has been read; its form
rendering remains to be checked. The31-page circuit-civil AO S-2024-046 is collected
but not yet substantively reviewed. Do that and applicable linked forms next.

Preserve the profile's June10,2017 approval statement alongside the rule's visually
read June29,2017 stamp. The separate approval-letter HTTP link timed out; its HTTPS
counterpart returned404. Both attempts are recorded. Conferral modes, emergency
copy routes, paper-request room505 versus profile520, and different schedule
sections also remain separate. Do not resolve those differences by inference.

The acquisition helper now records transport failures without inventing response
bytes, HTTP status or retrieval time, then continues with independent requested
sources. A temporary MockTransport check verified that behavior, exact successful
source preservation and duplicate rejection before networking; see
`review/acquisition-helper-validation.json`. The retry used only unfinished
requests; already collected shared originals were reused.

Packet2 retains the current acquisition inventory and unfinished judge receipt as
immutable artifacts, along with all original/text sources. Facts, all supplied
artifact bytes, exact replay and finalized-report preservation were read back in
`review/checkpoint-2-validation.json`. Do not rerun `save-farfante-progress.py`;
prepare a new checkpoint for later changes.

## Farfante completed review — capture 4894

Receipt: `receipts/person-hillsborough-circuit-darren-d-farfante.json`. Packet:
`draft/checkpoint-3.json`. Review includes27 checklist topics,84 source timing
clauses,48 source-specific calendar rows and14 additional full-text source
reviews. Person and226 nested citations validated;98 artifact bytes and18
findings read back; exact replay and unchanged finalized reports checked in
`review/checkpoint-3-validation.json`. These are review/storage checks, not county
completion or a ruling about controlling authority. Do not rerun the assembly or
save scripts after subsequent research; replay the immutable packet if needed.

The shared civil order S-2024-046, DCM order S-2024-085, Trial Division3 order
S-2026-034 and arbitration order S-2018-040 now have scoped reviewed findings.
Farfante's fee sample and applicable business/circuit trial/DCM forms are read.
Visual page checks and manually transcribed signature dates are enumerated in the
receipt. Reuse those originals and reviews for later applicable judges; inspect
the next judge's adoption, exceptions and current page rather than refetching.

Important extraction and review rules learned from this judge:

- `/Resources/Forms-Page/civil` contains **all** form categories. The same jury
  and nonjury link titles occur under `/genciv/` and `/countyciv/`. Require the
  verified section/URL association, not first matching label. Retain link metadata
  in `review/civil-forms-links.json`.
- Case Management Orders1–5 belong to the **Tobacco Cases** heading. Farfante's
  biography identifies tobacco as a past assignment. Do not attach those as his
  current business/asbestos orders merely because they share the forms page.
- DCM AO section3 excepts **Business L** from streamlined/general designation;
  the type table places Asbestos in general. Preserve both assignments. The
  amended DCM filename says Streamlined, but its title covers **both** tracks.
- Save each dated form separately. The current links include2008/2014/2015/2021
  forms,2025 references, superseded-order references, blank case dates and
  differing deadline triggers. Do not invent a latest-form revision or combine
  those defaults into one case deadline. Table14days/body10days meeting language
  is an actual source difference, not an extraction correction.
- Profile UMC15minutes,48hour binders and opposed Portal/Word-email instructions
  differ from shared AO10minutes,3businessdays and opposed paper delivery. Record
  the source, scope, units and dates separately; no reconciliation required.
- The current Forms tab works through the shared page. The procedure's legacy
  `JudicialDirectory/DarrenDFarfante/Forms.aspx` returned404; retain that response.
  Do not re-request it or the unavailable approval letter without a new lead.
- Keep collection, substantive review and visual checks distinct. A rendered
  page is not necessarily visually inspected. Shared registry-funds/foreclosure
  forms and HCBA/Bar standards remain explicit county tasks; their references
  were read, but the separate originals are not yet claimed reviewed.

Next source is the roster's `/Directory/Judges/Judge-Thomas`, not the different
`Judge-Twine-Thomas` identity. Reconcile name/assignment/contact rows first.

## Thomas completed review — capture 4896

`receipts/person-hillsborough-circuit-cheryl-k-thomas.json` and
`draft/checkpoint-4.json` preserve17 checklist topics,15 timing clauses and6 unique
trial/pretrial pairs. Seven new source reviews include the clerk's exhibit
memorandum/list and shared upload guide; twelve prior shared reviews were reused.
Person validation,106 nested citations,137 artifact read-backs,26 saved findings,
exact replay and unchanged finalized reports were checked.

Thomas-specific traps for the next update:

- Profile name Cheryl K. Thomas, DivisionA, JA Dorothy Gross,813-272-6993.
  Her residential trial sample names her/DivisionA but page2 directs questions
  to DivisionK813-272-6360. Keep that as a form discrepancy, not a contact update.
- The page's “Steps to Upload” anchor points to a **DCM explanation** PDF under
  `jdghuey`. Its separate actual upload-guide links point to
  `UploadingProposedOrdertoFloridaEPortal.pdf`. Inspect actual href/content,
  not anchor label or another judge's directory name alone.
- The linked General & Extended amended DCM form retains2021 wording plus a
  2024AO reference. Its query parameter is2021, which is not a verified revision
  date. Preserve its fact-discovery-based months/days separately from the
  complaint-based streamlined/general form.
- Schedule tables are repeated twice in original HTML. Pair the two cells in
  each trial/pretrial row, retain published weeks/day-count wording, and dedupe
  exact repeated rows. Do not compute an end date from “two weeks (14days).”
  `review/thomas-table-rows.json` preserves the actual table pairing.
- Personal Word motion, legacy Preferences.aspx and Forms.aspx links returned404.
  The separately published shared PDF motion is reviewed; no claim the missing
  Word file was collected, rendered or is byte-identical to it.
- Clerk exhibits source: `/Court-Services/Circuit-Civil`, then **related
  documents** → Trial Exhibit Memorandum / Exhibit List. The memo is5physical
  pages despite its first-page “Page1of1”; four list pages are attached. Preserve
  footer2021 and body2024-021 reference; shared2024-046 states supersession.
  Clerk-hosted2024-046 PDF is byte-identical to the court original; reuse review.
- County clerk/service/contact review remains pending. Reading the exhibit
  subsection and collecting the whole clerk page does not complete those tasks.

The run acquisition helper now retains ZIP/Office bytes without parsing them as
HTML or claiming extracted text. This guard was exercised with a temporary
MockTransport fixture alongside failure/404/next-success/duplicate checks; see
`review/acquisition-binary-guard-validation.json`. No fixture was saved to the
live database. Unsupported binary formats require a separate extractor/review.

Next: `/Directory/Judges/Judge-Polo`, matched against saved roster before review.

## Polo completed review — captures 4898 and 4900

Latest receipt: `receipts/person-hillsborough-circuit-melissa-m-polo-v2.json`.
Latest packet: `draft/checkpoint-6.json`; capture4900 improves narrative readability
while retaining capture4898 and all original evidence. Twenty checklist topics,
42 timing clauses,21 calendar rows,17 new source reviews and15 reused reviews are
saved. Initial person review validated200 nested citations; latest packet validated
all nested citations and read back201 artifacts/44 findings. Exact replay and
unchanged finalized reports were checked. County review remains incomplete.

Polo's full18-section profile has more material requirements after the “Top Ten”:
AI disclosure, trial/pretrial, discovery, rehearing, mediation, conferral,
professionalism, briefing/page limits and reporter arrangements. Do not stop at
section10. The two “Good-Faith Conference” headings cover different content.

Her Forms tab links templates under `jdgwolfe`, `jdghuey` and `Isom` paths.
Inspect internal labels: several actually say DivisionB, the jury/fee templates
name Mark R. Wolfe, and the residential form gives a DivisionI question line.
Record **linked by Polo** separately from **named author/division**. Do not
replace her current C/room523/courtroom504/JA Patricia DePagter contacts with
template fields. This does not complete Wolfe or Huey's individual reviews.

The2026/2027 schedules are separate one-page PDFs linked from Schedule, with
multiline trial ranges. Both were visually checked. Preserve all ranges in a row,
not one selected week. The2027 jury-selection column has a blank July cell and
January4/November15 dates that differ from the profile's Friday-before wording.
Keep the blank unknown and the exact dates; do not infer a missing date.

AI comparison sources now preserved directly:

- AOSC26-12, issued May28,2026 and effective June15 at12:01a.m. Official original:
  `https://flcourts-media.flcourts.gov/content/download/2489379/29182858`.
  All3text pages read; pages2–3 visually checked. It expressly addresses local
  orders, policies and judicial practices requiring AI-use/accuracy disclosures
  or certifications. Preserve its statement alongside Polo's profile section11.
- SC2026-0673, same stated issuance/effective dates, Rule2.515 amendment:
  `https://flcourts-media.flcourts.gov/content/download/2489374/opinion/Opinion_SC2026-0673.pdf`.
  Reused the original from the October12 baseline with that actual retrieval
  timestamp; all6text pages read,3/5/6 visual. Distinguish underlined additions
  from unchanged signature representations. No new retrieval or authority
  resolution is claimed.
- Search results located the official original after the Supreme Court index
  opened as a subscription/footer shell. Search snippets alone were not used as
  saved substantive evidence. No other county was researched from search leads.

The old cancellation links to S-2024-021 returned404; current S-2024-046 was
already reviewed. The query-free upload guide was byte-identical to the prior
query-string original. Word-form404 was reused rather than requested again.
The online ADA request was read without submitting data. Separate county ADA,
clerk, courthouse-access and other material-order review remain pending.

For continuation, read only the active judge receipt and needed shared-source
reviews, not all prior county packets into model context. Use acquisition keys
and exact hashes to reuse originals. Full immutable packets are for validated
save/replay; `state.json`, `RESUME.txt` and this handoff identify the next task.

Next: `/Directory/Judges/Judge-Murphy`; reconcile J. Logan Murphy versus the
assignment chart's Logan J. Murphy wording before assigning contacts/procedures.

## Murphy completed review — capture 4902

Receipt `receipts/person-hillsborough-circuit-j-logan-murphy.json`, packet
`draft/checkpoint-7.json`. Fifteen checklist topics, 24 calendar rows (including
November 2026's explicit no-trial row), 13 timing clauses and 17 reused source
reviews are saved. Validation checked the person and 111 nested citations,
read back 208 artifacts and 45 findings, confirmed exact replay, and left finalized
reports unchanged. Four named judges are complete; 65 remain pending.

The alphabetical PDF uses mixed-case `Murphy, J. Logan`; an uppercase-only search
misses it. The division PDF and profile agree on Division D, room 522, courtroom
504, JA Jaclyn Dingwerth, 813-307-4751 and gencivdivd@fljud13.org. Preserve the
chart's `Logan J. Murphy` and biography heading's `Murphy J. Logan` as source
variants. Historical assignments in the biography do not establish current duties.

All three Forms-tab URLs and the upload-guide URL exactly match already preserved
shared originals. Reuse their original retrieval timestamps. The collection key
`thomas-amended-dcm-2021` denotes first discovery, not exclusive Thomas applicability.
Do not repeat its download merely because Murphy links it too. The legacy
`Forms.aspx` 404 also remains recorded without another request.

Read all 15 numbered procedure sections, not only “Top Ten.” Murphy's JAWS
15/30/60-minute scheduling and 5-minute UMC differ from Thomas's schedule. Preserve
the Wednesday-before-DCM upload/excusal, competing Word-email, remote-pretrial and
courtesy-copy differences from shared orders. Calendar cells were checked against
original HTML tables and saved in `review/murphy-table-rows.json`. Keep both trial
ranges in two-week rows, blank week counts as unknown, November 2026 as expressly
no trial week, and June 2027's printed June 26 end date without correction.

Next source: `/Directory/Judges/Judge-Oster`, Circuit Civil E. No other judge was
reviewed by associating these shared forms. County clerk/access/officer tasks remain
open; this checkpoint neither publishes nor advances a finalized report baseline.

## Oster completed review — capture 4904

Receipt `receipts/person-hillsborough-circuit-cynthia-s-oster.json`, packet
`draft/checkpoint-8.json`. Sixteen checklist topics, 13 calendar rows, 30 timing
clauses, four new scoped source reviews and 14 reused shared reviews are saved.
Validation checked the person and 120 nested citations, read back 235 artifacts
and 50 findings, confirmed exact replay, and left finalized reports unchanged.
Five named judges are complete; 64 remain pending.

Oster's profile has a **link to an eight-page procedure PDF**, not embedded
procedure text. Follow “Judicial Practices and Procedures” to
`/Portals/0/Forms/pdfs/judges/JudicialPracticesAndProcedures/JudgeCynthiaOster.pdf`.
Its first page states May 4, 2026 modification, mailing room 524, physical
courtroom 508, and fax 813-307-3408. Do not mark fax absent after checking only the
HTML contact card. All eight text pages were reviewed; visual checks cover pages
1, 3, 4, 6 and 7. Clerk exhibit and ADA contacts are service contacts, not the JA.

This division requires in-person pretrials/discovery and ordinarily hearings over
30 minutes; shorter hearings generally use Zoom. No hybrid hearings. Hard-copy
hearing materials and court exhibits are due three business days ahead. All
proposed orders are Portal PDFs, with competing Word copies additionally emailed;
ten days after hearing and five-day opponent-response language remains distinct
from the shared AO's deadlines. Preserve the paper/alphanumeric exhibit instructions
alongside electronic/numerical shared instructions without choosing authority.

The linked five-page fee-hearing form actually names Oster, Division E and room
508. Do not reuse another judge's fee form on title similarity alone. All text was
reviewed; visual pages 1, 4 and 5 checked. Its blank dates, 90-day mediation,
30/20/20-day fee exchanges, business-day discovery/expert conditions and erroneous
paragraph-5 cross-reference to the paragraph-4 affidavit list remain explicit.

The “Main Forms Page for Circuit Civil” link actually targets `/Resources/Forms`.
Its saved extraction is identical to the earlier `/Resources/Forms-Page/civil`
extraction; raw bytes and retrieval records remain separate. Review of its Circuit
Civil/DCM link section does not complete every linked form or other category.

The standalone `CircuitCivilDCMOrderStreamlined.pdf` had not previously been
collected. Its six text pages are now reviewed; visual pages 1, 5 and 6 checked.
Title covers cases filed after January 1, 2025. It combines fact/expert discovery
at 240 days and puts other pretrial-motion filing at 300 days after complaint,
unlike fields/defaults in the separately saved amended form. It references a
January 1, 2025 revised trial/pretrial order while the forms index links the
April 30, 2021 original. Preserve the reference and actual linked document separately.

Calendar rows run July–December 2026 and January–July 2027; no other months are
asserted absent. January 2027 pretrial is December 9, 2026. The profile biography
has contradictory historical assignment dates (January 2023–January 2018, plus
Circuit Civil January 2018–present); preserve them without converting them into
a verified assignment start date. Current Division E association is supported by
the profile, directories and named procedure PDF.

Next: `/Directory/Judges/Judge-Gabbard`. Finish her record before another judge.

## Gabbard completed review — capture 4908

Receipt `receipts/person-hillsborough-circuit-jennifer-x-gabbard.json`, packet
`draft/checkpoint-9.json`. Twenty-three checklist topics, 11 calendar rows,
54 timing clauses, 21 new scoped source reviews and 19 reused reviews are saved.
Person and 192 nested citations validated; 326 artifact bytes and 72 findings
read back; exact replay and unchanged finalized reports checked. Six named judges
complete, 63 pending. No other judge was researched during this review.

Current identity: Circuit Civil F, room 514, courtroom 500, JA Brandi Paine,
813-272-5774, circivdivf@fljud13.org. Profile and both directory PDFs agree.
The procedure PDF is under
`/Portals/0/Forms/pdfs/judges/JudicialPracticesAndProcedures/JudgeJenniferGabbard.pdf`.
All 13 text pages were reviewed; actual visual checks are pages 1, 2, 5, 6, 8, 9,
10 and 12. No stated PDF revision date was located. The HTML separately dates the
discovery docket September 1, 2026, in-person pretrials October 1, 2024, and Portal
order submission October 1, 2020. These dates describe different instructions.

Preserve the HTML/PDF distinction: HTML says evidentiary hearings **longer than
30 minutes** are in person; PDF says **60 minutes or longer**, with highlighted
60-minute figures. The PDF nonjury exception is **less than 30 minutes**, while
HTML uses **longer than 30 minutes** for in-person nonjury trials. Do not normalize
these boundaries or decide which version controls. Also preserve emergency
paragraph-19 heading/12(B) body mismatch and ordinary-day versus shared
business-day order deadlines. Competing orders use emailed Word files.

Calendar extraction must skip the first one-cell **scheduling notice table**.
The next two tables contain three 2026 and eight 2027 rows, each with **two
pretrial dates**. Retain both dates and both trial-week starts in two-week rows;
do not infer trial ends or choose a pretrial date. HTML says only opened weeks
are published and inquiries about unlisted dates receive no response.

The Forms tab embeds broad shared civil forms, plus Business/Tobacco sections.
Gabbard's F assignment does not establish Business L or Tobacco Y applicability.
No tobacco form body was reviewed for her. `review/gabbard-related-request.json`
maps actual anchor labels/URLs to these newly collected shared-source keys:

| Key suffix (`gabbard-shared-`) | Source |
| --- | --- |
| 1–5 | Indigence; diligent search; arbitration referral; civil mediation referral; mediation party information |
| 6 | Private arbitrator directory: full collection, page-1 header/instructions review only |
| 7–10 | Military-status memorandum; military affidavit; medical-examination order; retained-expert fees |
| 11–16 | Foreclosure compliance; status change; residential trial; final judgment; sale cancellation; possession motion |
| 17–19 | Foreclosure mediation referral; 19-page forms bundle; sale-reset order |

All text in sources 1–5 and 7–19 was reviewed. Visual pages are listed in each
receipt, not inferred from the presence of rendered files. The private arbitrator
directory's July 24, 2026 run date and instruction header are reviewed; its body
contacts are not individually verified or imported as current judicial personnel.
The residential trial PDF extraction misreads relay **711** as `7JJ`; page 2 was
visually checked. Sale-cancellation form preprints **2 p.m.**, whereas the final
judgment form says **10 a.m.** Keep those source defaults separate.

Retain dated forms as dated evidence: medical exam September 18, 2009; expert fees
September 5, 2024; possession September 1, 2015; final judgment effective July 22,
2019; foreclosure mediation effective August 1, 2022. Old order/statute references,
HAMP wording, printed fees and source deadlines are not independently certified
current law. The mediation bundle's postal alternative differs from the referral
order's electronic-platform mandate. No original or historical statement was
rewritten to resolve those differences.

The procedure's professionalism URL returned 404. Current route:
**Resources → Legal Community → Legal Community For Attorneys** at
`/Resources/Legal-Community/Legal-Community-For-Attorneys`. Standards are embedded
in the HTML accordion, not a separate document anchor. Read the saved text under
“Hillsborough County Standards of Professional Courtesy” through the Creed.
Sections A–M and Creed are reviewed; criminal appointment registry links are not.
Section K, headed Settlement/ADR, repeats section J's ex parte content. Preserve
that discrepancy. Its next-business-day proposed-order **preparation** standard
is separate from individual **submission** deadlines. Acquisition key:
`attorney-resources`; reuse this official original for subsequent judges.

Next: `/Directory/Judges/Judge-Nash`. County clerk/access/officer work and other
material-order screening remain pending. Shared forms collected during this
judge improve the county baseline but do not silently complete those tasks.


## Seventh judge completed: Christopher C. Nash

Saved at capture **4911**, packet `draft/checkpoint-10.json`, receipt
`receipts/person-hillsborough-circuit-christopher-c-nash.json`. Fourteen checklist
topics, 22 calendar rows, five individual timing clauses, two new scoped reviews
and 31 shared reviews reused. Person and 145 nested citations validated; 345
artifact originals/derived files and 75 finding records read back from SQLite.
Exact replay and unchanged finalized reports checked. Seven complete, 62 pending.

Profile: `/Directory/Judges/Judge-Nash`. Individual procedures are inline under
**Procedures & Preferences**, not a standalone comprehensive procedure PDF.
Compare the earlier **Schedule** tables separately: they are not duplicates of
the detailed tables. Keep source-specific contact variants: profile **Hilda Lopez,
room 519** versus October 1 directory PDFs **Hilda Aguilar, room 513**. Both list
813-272-6995 and courtroom 503. Calendar headings instead say courtroom 513;
2027 jury-pick column says courtroom 503. Header/calendar/general email is
`divisiong@fljud13.org`; DCM/continuance clauses say `DIVG@FLJUD13.ORG`. Do not
infer a name change or silently normalize the email addresses.

The six HTML tables are schedule, preferences, 2026 calendar, 2027 calendar,
detailed schedule, detailed preferences. Row counts including headers are
**2, 2, 11, 13, 2, 2**. Calendar data has ten 2026 and twelve 2027 rows; retain
multiweek trial and multiple jury-selection dates as printed. DCM/pretrial Zoom
is explicit; opening, section 9 and legacy COVID text differ on other appearances.
Courtesy copies: early table **3 days**, detailed table **2 business days**, shared
AO **3 business days**. Preserve call/email and agreed-order route differences.
Cases filed 2023 or earlier use UMC/CMC continuance hearing; 2024 or later may
email the motion for guidance. No new trial order before court authorization.

Several DCM bullets literally end mid-sentence in the original `<li>` elements.
The source was checked, not merely the extractor. Save incomplete text verbatim
and avoid reconstructing words. The Forms tab links an amended DCMO although the
individual trial-setting instructions say to use the trial order instead.

Nash's five-page exhibit-label PDF is `nash-exhibits`: all text reviewed, visual
pages **1–3**. It specifies white labels on the back of the last exhibit page,
bottom left, numbered tabs/binder, trial-morning clerk copy and two exhibit lists.
Illustrative Marlette/Carullo Division I is not Nash's current division G.
Shared electronic-exhibit instructions remain separately attributed. The link's
2022 query value is not a stated revision/effective date.

`nash-portal-guide` returned HTTP 404. Generic `shared-portal-upload-guide` is
available, but do not claim identical content or that the missing Nash attachment
was reviewed. Nash's legacy indigence link returned **HTTP 200 with a not-found
message**, not a form. Always inspect response content/type before accepting a
200 as successful collection. `nash-indigence-official`, from the official Courts
media host, is byte-identical to already reviewed `gabbard-shared-1`. Preserve both
URLs and retrieval timestamps. Reused Word motion failure has available PDF
counterpart. All unavailable attachment statements remain explicit in the receipt.
Foreclosure-mediation anchor says September 18, 2017; linked PDF says effective
August 1, 2022. These are distinct source statements, not a resolved chronology.

Next: `/Directory/Judges/Judge-Daniel`. Do not rerun completed assembly scripts;
replay saved immutable packets only. County clerk/access/officer/material-order
work remains pending; this judge checkpoint does not finalize the county.


## Eighth judge completed: Helene L. Daniel

Saved at capture **4913**, packet `draft/checkpoint-11.json`, receipt
`receipts/person-hillsborough-circuit-helene-l-daniel.json`. Seventeen checklist
topics, 18 calendar rows, seven numeric timing clauses plus a before-PTC direction,
three new scoped reviews and 23 shared reviews reused. Person and 120 nested
citations validated; 362 artifacts and 79 findings read back. Exact replay and
unchanged finalized reports checked. Eight complete, 61 pending.

Profile `/Directory/Judges/Judge-Daniel` and both October 1 directories agree:
**Tammy Farina**, 813-272-6972, `gencivdivh@fljud13.org`, Edgecomb room 521,
courtroom 502. Undated biography lists earlier/additional Plant City R and East
Circuit administrative assignments; do not infer simultaneous current assignments.
Current roster/header support Circuit Civil H.

Individual procedures are inline: the “Top Ten” heading actually contains **16
numbered sections**, including Additional Procedures. Read through section 16;
do not stop at 10. In particular, the AI disclosure/certification paragraph differs
from the already saved AOSC26-12 and Rule 2.515 materials issued May 28/effective
June 15, 2026. Preserve each statement with its dates without deciding authority.

Two HTML tables contain six 2026 and twelve 2027 rows. The first cell of each row
includes **trial dates, jury-pick dates and motions-in-limine hearing dates**; save
all three, not just the first date. Other cells are week count and PTC date/time.
All listed PTCs are 9:30 a.m. in person. March 26, 2027 holiday note is retained as
a calendar statement. JA confirms availability; nonjury date-certain trials via JA.

Short hearings (30 minutes or less): **no binders/paper to chambers**, file materials
at least three business days before, or applicable earlier rule deadline. Hearings
45 minutes or longer: binders may be mailed/delivered at least three business days
before; no email. The 31–44-minute category is unstated, not inferred. Pretrials,
jury trials and hearings of at least one hour are in person. Agreed orders use
Portal PDF; competing orders go in one email with cover letter and Word copies.
Agreed PTC order has its own Word-email-before-PTC instruction. Preserve individual
and shared-AO copy/order differences without merging them into a synthetic rule.

The query-free trial, amended DCM, final-foreclosure and sale-reset links were
collected and confirmed **byte-identical** to existing originals. See
`review/daniel-related-request.json`, `review/daniel-source-reuse.json` and receipt
`source_aliases`; keep each observation URL/time while reusing content review.
Rule 1.360 form (`polo-linked-4`) and nonjury form (`polo-linked-13`) are exact shared
links. The latter URL is under `jdghuey` but has blank judge/division fields; it
is not an assignment record or a completed review of Huey.

Two Daniel-linked foreclosure forms name **Emmett Lamar Battles**, despite their
current placement in Daniel's Forms tab. `daniel-linked-4` is a two-page residential
trial form, courtroom 502 confirmed visually, printed 2021 order reference,
mandatory mediation/appearance conditions, 20-day PTC request, 10-day exchange and
service periods. `daniel-linked-5` is a one-page surplus distribution/hearing
alternative with **room 519**. All three pages were read and visually checked.
Keep source-named judge/location separate from Daniel's current contacts. The
residential form's no-telephone mediation direction differs from the linked 2022
referral form's conditional corporate-representative phone provision.

The legacy ADA link returns 404; reuse current official request page `polo-linked-1`.
Daniel's minor-settlement DOCX and a bounded query-free check both return 404.
Exact-title searches and saved shared forms pages did not yield a replacement.
The profile's mandatory-hearing instruction is reviewed, while the unavailable
form contents remain unreviewed. The shared Word DCM and legacy Forms.aspx failures
also remain explicit with available PDF/current Forms alternatives. Missing source
content is not renamed reviewed merely because the judge receipt is complete.

Next: `/Directory/Judges/Judge-Huey`. Complete that judge before another profile.
County clerk/access/officer/material-order tasks remain open; no county report was
finalized or published.


## Active ninth judge: Paul L. Huey — draft checkpoint

Capture **4915**, immutable packet `draft/checkpoint-13.json`; draft receipt
`draft/person-hillsborough-circuit-paul-l-huey-v2.json`. **Not complete**: retain
Huey as active. Eight complete, 61 pending (including Huey). Original attempted
packet 12 failed URL validation before save; do not replay it or rerun either
assembly script. Packet 13 passed the unchanged saver, exact replay, 440 artifact
read-backs, 92 finding comparisons and unchanged finalized-report checks. Additional
path-based checks validated 524 citation instances; the saver validates hash-based
packet citations separately. No completed-person validation is claimed for Huey.

Contacts: `/Directory/Judges/Judge-Huey` gives **Sandy Duncan**, directory PDFs
**Sandra Duncan**; preserve source names without assuming alias. Phone813-272-5414,
`circivdivi@fljud13.org`, Edgecomb room527/courtroom506. Profile and roster confirm
Civil I and Tobacco Y. Biography's other assignments are not treated as current.

All **14 inline numbered sections** were read (section11 repeats5), organized into
13 checklist topics. JAWS materials3businessdays ahead; no case-law upload/email;
10-page memos excluding photos/charts/diagrams. Trials/PTC and evidentiary hearings
longer than30minutes in person. Longer-than30minute bookings need JA email with
five specified fields. Agreed orders PortalPDF, opposed Word-email. Limine hearings
only for judge-selected number1 trial case absent approval. Preserve shared-AO and
linked Daubert copy/routing differences. Schedule has no separate discovery docket.

`review/huey-related-request.json` maps twelve newly collected links. Full text of
all linked PDFs (2–12) reviewed. Source1 is the public initial JAWS order-generator
form: case-number textbox and submit button only; **no case submitted or generated
order/calculation tested**. Shared sources reused include the exact DCM guide,
nonjury form, limine/Daubert forms, Rule1.360 form and applicable AOs. Twelve source
reviews, fifteen reused reviews,31numeric and7relative timing clauses are saved.
New sources: stipulatedDCM motion2p; adlitem3p; CMC2p; garnishment1p; juryprocedure4p;
mediation3p; arbitration3p; feehearing5p; residentialtrial2p; calendars1p each.
Actual visual pages are explicitly listed, not inferred from rendered-file count.

The 2026 calendar emitted pypdf wrong-object-offset warnings. Both calendars were
rendered and visually checked; PyMuPDF extracted one13-row table each (header+12).
Twenty-four rows retain all week starts and PTC cells, without inferred enddates.
June3,2026 is printed Thursday, but date arithmetic yields Wednesday. Preserve
both the source and discrepancy. 2027 DecemberPTC is WednesdayNovember10.
The jury form retains CD-R Word delivery; the fee form has a5a–m cross-reference
that points to actual4a–m. Source-specific dates, fees and rule references remain
statements, not certified current law.

Four court anchors contain literal spaces (CMC, garnishment, arbitration,
residentialtrial). HTTP client successfully encoded them; citation URL validator
correctly rejected raw spaces. **Use saved HTTP `resolved_url` for those citations,
while preserving original anchor/request URL in acquisition/source metadata.**
Do not weaken URL validation or refetch successful evidence just to encode its URL.
`review/repair-huey-citation-urls.py` corrected28 citation instances using observed
responses. Its first local check tried the person-citation API on older minimal
packet citations without paths; that API mismatch was corrected before save. The
baseline saver validates those minimal citations against artifact bytes/hashes.

Tobacco source map: current **Resources → Forms → Civil → Tobacco Cases**;
`review/huey-tobacco-request.json` captures exact official links and labels.
All ten originals collected, **243 pages**, with only these reviews so far:

- 1: CMO1,32p; page1scope/header read; page-head inventory only for otherpages.
- 2: CMO2,6p; page1scope/header read.
- 3: CMO3,9p; page1scope/activation discussion read.
- 4: CMO4,6p; page1scope/replacement-order discussion read.
- 5: CMO5,25p image-only; native extraction contains page labels, no content.
  Physical1–4 visually read: body1–3, Exhibit1cover4. Need verifiable OCR or manual
  transcription tied to original/pages before structured deadline findings. Page3
  signatureJuly9/year handwritten alteration; do not guess normalized year.
- 6: active discovery/scheduling,3p; firstpage table text seen, remainder pending.
- 7: Engle PhaseI effect,5p; firstpage scope read; specializedmerits body notreviewed.
- 8: motion to settrial>60days,2p; page1 read, dispositionpage2 pending.
- 9: proposedlimineorders,80p; collected only.
- 10: tobaccojuryinstructions,75p; collected only.

Keep commercial-civil/shared-procedure priority. Next review filing/caption/service,
case activation, trial scheduling and shared discovery requirements in dated CMOs;
CMO1 begins filing/procedure pp1–10 and scheduling pp29–32. Inspect CMO5 scheduling
exhibit following page4; distinguish exhibits/questionnaires from body. Preserve
specialized merits/instructions without exhaustive tobacco-merits analysis. These
historical DivisionD/JamesBarton materials do not override current I/Y identity.
The shared civilAO's Yassignment/disqualification/multiweekdocket provisions were
read and saved. No adjudication of intervening supersession is required.

Continue Huey, then complete personvalidation and a new immutable checkpoint
before Judge Alissa Ellison. County clerk/access/officer/material-order tasks remain.


## Ninth judge completed: Paul L. Huey — scoped final review

The earlier draft section above is historical; **4917 supersedes 4915 for current
progress** without deleting evidence. Packet `draft/checkpoint-14.json`, receipt
`receipts/person-hillsborough-circuit-paul-l-huey.json`. Nine complete,60pending.
Person validation,248nested citations,461artifact read-backs,99finding comparisons,
exact replay and unchanged finalized reports passed. Twenty checklist topics,
24calendar rows,44numeric and7relative timing clauses,20separate CMO5 event rows,
19source reviews and15reused reviews retained. County/goal remain incomplete.

The following tobacco procedural review is finished under the commercial-civil
priority; it is **not** a full substantive review of all243collected pages:

| Source key suffix | Reviewed scope | Remaining collection-only material |
| --- | --- | --- |
| `huey-tobacco-1` | Physical1–10 and28–32: filing, service, liaison, conferences, scheduling, privilege | 11–27 detailed medical/records/expert discovery |
| `-2` | All6pages | Referenced authorization ExhibitA absent from six-page PDF; not asserted obtained |
| `-3` | All9pages, including activation/trial scheduling exhibits | None in downloaded PDF |
| `-4` | All6pages, including replacement trial schedule | None in downloaded PDF |
| `-5` | Physical1–7: body, exhibit1cover and20-row trial schedule | 8–25 specialized worksheet exhibits |
| `-6` | All3pages, earlier active-discovery schedule | None in downloaded PDF |
| `-7` | Page1 scope only, previously read | Remaining specialized Engle merits analysis |
| `-8` | Bothpages, trial preselection order | None in downloaded PDF |
| `-9`, `-10` | Collected only | 80-page proposedlimine and75-page juryinstruction compilations |

CMO1's master/individual caption model differs from CMO2's specific instruction
that individual filings omit the master number. CMO2 p2 literally prints
`08-CV-80000`, whereas header/body use`08-CA-80000`; visual checks confirmed this.
Its signature date isJune6,2008. CMO3 signatureJanuary9,2009; CMO4June26,2009;
trial-preselection orderJune30,2008. Original extraction misreads several signatures
and stamps, so source images and explicit visual observations are retained.

Preserve source chronology and express amendment language without adjudicating
current controlling authority: CMO1 monthlyactivation,2008monthlytrialpreselection,
CMO3quarterlyactivation/designation,CMO4/5replacementtrialexhibits. Plaintiffexpert
trigger changes45daysafterdesignation to150daysbeforeclose; finaldefensewitness
35days to38days, with separateplaintiffrebuttal35days. CMO5worksheetbody says
105–90days“from”close, while table says“prior”; retain both. HistoricalDivisionD,
private liaison counsel and namedjudges are not currentI/Ycontacts.

CMO5 image-only original/native empty extraction is retained under`huey-tobacco-5`.
A separate acquisition-manifest entry`huey-tobacco-5-ocr-scoped` references the same
original bytes/URL/retrieval timestamp plus a derived text hash and extraction time.
Its text covers **physical1–7 only**, though the original remains25pages. Page helpers
must use`text_coverage_physical_pages` to avoid looking for an unextractedPAGE8.
Native text is not overwritten, and OCR is not a fresh source observation.

The bounded helper`review/ocr-pages.swift` compiled with the installed Swift/Vision
SDK and ran successfully on seven rendered PNGs. It uses accurate English OCR,
language correction disabled, and emits per-image text/confidences in
`review/huey-cmo5-ocr.json`. Reproduction from repo root:

```sh
mkdir -p .build/module-cache
swiftc -module-cache-path .build/module-cache runs/county-hillsborough/2026-10-16/review/ocr-pages.swift -o .build/flwu-ocr-pages
```

Invoke the binary with explicit PNG paths; it writes JSON to stdout. Original PDF
pages were rendered at2x withPyMuPDF. OCR is evidence extraction, not a local-agent
research delegation. Source table columns were separated by OCR reading order;
physicalpages5–7 were visually paired into20event/deadline rows. Bodypages1–4 were
visually read in the prior checkpoint; all1–7 now reviewed against OCR. Handwritten
July9/year correction onpage3 remains unnormalized; do not use garbled OCR date.
The binary itself is a local build artifact; source,JSON,derivedtext andimages are
saved and hash-bound in the research database.

Reviewable sources retain actual dates, conditions and historical amounts; no
current case deadline or controlling-authority determination was generated.
Next `/Directory/Judges/Judge-Ellison`; no profile acquired yet. Finish her before
moving to another judge. County clerk/access/officer/material-order work remains.

## Tenth judge completed: Alissa M. Ellison

Capture **4919**, packet `draft/checkpoint-15.json`, receipt
`receipts/person-hillsborough-circuit-alissa-m-ellison.json`. Ten complete,
59 pending. Person validation and 157 nested citations passed; all 475 artifacts
and 103 findings were read back, identical replay passed, and finalized reports
were unchanged. No county publication or finalization occurred.

The profile and both October 1 directories agree: Circuit Civil J, JA Jennifer
Gonzalez, 813-272-6991, gencivdivj@fljud13.org, Edgecomb room 512/courtroom 503.
The complete individual procedure text is represented by 21 checklist topics,
10 numeric and seven relative timing requirements. Both HTML calendar tables
retain 24 rows with trial weeks paired to their pretrial dates. Email the office
for the time; none is inferred. July 15, 2026 is labeled Monday but falls on
Wednesday. Preserve both statements. May 2027 trial weeks 10/24 and October
2027 weeks 4/18/25 are nonconsecutive and must not become continuous ranges.

Distinct individual directions include JAWS hearing materials at least two
business days beforehand, no paper/binders or ShareFile links, emailed briefs
with embedded cases, competing Word orders by email, and unilateral notices
only after lack of cooperation with at least 60 days' notice. All evidence,
pretrials, trials and hearings exceeding 30 minutes are in person; UMC, 15/30
minute hearings and DCM conferences use Zoom. UMC under-five-minute preference
and possible cancellation above seven are distinct from the shared AO's
10-minute cap. Preserve the AO's "unless otherwise directed" qualifications.
Profile order deadlines use days where the AO uses business days; record each
unit and trigger without selecting a controlling source. The older DCM plan
reference is retained alongside the later plan and its express supersession.

Source navigation lessons for later agents:

- The link labeled portal-upload steps actually downloads `huey-dcm-guide`, a
  historical DCM guide. The link labeled DCM process targets a Nash portal guide
  and returns 404 (`ellison-linked-7`). Preserve label, target and actual content
  separately. The saved generic portal guide is an alternative, not proof of
  the unavailable attachment's contents.
- Four linked Word forms return 404: party information, medical examination,
  expert fees and foreclosure cancellation (`ellison-linked-1/2/3/6`). Their
  explicitly linked PDF counterparts are already saved as
  `gabbard-shared-5/9/10/15`. Reuse those; do not claim byte identity or recover
  unavailable Word content from the PDFs.
- The legacy indigence URL is the previously saved HTTP-200 missing-page body.
  The available official PDF is preserved separately. Status 200 is insufficient
  evidence of successful document acquisition.
- `ellison-linked-4` and `ellison-linked-5` are county civil streamlined/general
  templates for cases filed after January 1, 2025, citing S-2024-086. All four/five
  pages are collected; only page-one scope was reviewed here. Finish substantive
  review during the first county civil judge, not as an Ellison assignment.
- Generic business, eminent-domain and tobacco headings do not assign those
  matters to this judge. The eminent-domain list repeats foreclosure links.
  Ten tobacco originals are reused from Huey, with his exact collection/review
  boundaries intact; no repeated merits analysis was performed.

The receipt reuses 35 shared reviews and adds three scoped reviews. Originals,
retrieval timestamps and prior review limits remain intact. No messages or filings
were sent, and no Portal/JAWS/Zoom participation or browser UI check is claimed.
Next: Christine A. Marlewski, `/Directory/Judges/Judge-Marlewski`. Finish her
individual review before another judge. County clerk, access, officer and material
administrative-order work remains pending.

## Eleventh judge completed: Christine A. Marlewski

Capture **4921**, packet `draft/checkpoint-16.json`, receipt
`receipts/person-hillsborough-circuit-christine-a-marlewski.json`. Eleven complete,
58 pending. Validation: 106 nested citations, 487 artifact read-backs, 105 finding
comparisons, identical replay and unchanged finalized reports. Fifteen checklist
subjects, 24 calendar pairs, 12 numeric and four relative timing requirements,
one individual source review and 14 reused reviews.

Profile and October 1 directories agree: Civil K, JA Paula Philips,
813-272-6360, circivdivk@fljud13.org, Edgecomb room 519/courtroom 502. Biography
expressly dates Civil K to 2025–present; Criminal C (2021–2025) and Family J
(2017–2021) are historical assignments, not present extra procedure workloads.

All evidentiary hearings require JA scheduling; non-evidentiary UMC/15/30-minute
hearings use JAWS. In-person evidence may use Zoom with parties' and court's
agreement, including a submitted agreed order. Pretrials and trials are in person.
JAWS materials and emailed embedded-case briefs have two-business-day timing;
no paper/binders, and briefs normally cannot exceed ten pages. Within 24 hours,
cancellation requires both emailed filed notice and a phone call. Settlement
notice alone does not cancel trial/pretrial; the page requires dismissal.

Preserve these source differences:

- Competing-order paragraphs say three days; the specific posthearing paragraph
  says five days unless otherwise directed. Keep both, with their own triggers.
- Profile days versus AO business-day units, individual delivery routes versus
  shared AO routes, and individual AI disclosure versus AOSC26-12/amended
  Rule2.515 remain distinct. The AI sources retain May28/June15,2026 dates.
- The portal-upload anchor points to the historical Huey DCM guide. The DCM
  anchor points to the previously unavailable Nash portal guide. Actual contents
  and missing evidence are recorded independently of link labels.
- Three upload/cancellation anchors point to `S-2024-021.pdf` with different
  fragments, while the headline names 2024-046. The prior `polo-linked-17`
  response is 404; it was reused, not refetched or reconstructed. The preserved
  2024-046 original states supersession of the older order.
- June 2027 jury trial is printed June19–23, beginning Saturday. Keep that
  literal range. Original `0ctober` spellings and November-pretrial/December-trial
  pairings remain intact; do not infer times or silently correct dates.
- The exhibits sentence literally says "approved by or rejected by" the Court.
  Preserve its awkward wording without inferring an exception.

Workflow refinement: compare `urllib.parse.urldefrag(url)[0]` for HTTP response
reuse, while preserving each full anchor URL, label and fragment as discovery
metadata. Fragments do not identify different fetched bodies. Do not discard
query strings or assume query variants are identical without bytes/evidence.
`review/marlewski-fragment-reuse.json` exercises this on the three anchors;
no redundant requests were made. Reused failures retain their original dates.

The assembly saved/validated the database, then a guessed `Judge-Ward` next-URL
assertion failed before writing local state. `review/advance-after-marlewski.py`
completed only that state transition using the actual roster path
`/Directory/Judges/Judge-Laura-Ward`; the repair receipt is
`review/checkpoint-16-state-repair.json`. Do not rerun the immutable one-shot
assembly. Always choose next-profile URLs from `review/roster-cards.json` and
validate them before advancing. No publication, case filing or browserUI check.
Next Laura E. Ward; county clerk/access/officer/material-order work remains.

## Twelfth judge completed: Laura E. Ward

Capture **4923**, packet `draft/checkpoint-17.json`, receipt
`receipts/person-hillsborough-circuit-laura-e-ward.json`. Twelve complete,
57 pending. Validation passed for the person and 109 nested citations; 500 artifact
bytes and 108 finding records were read back, identical replay passed, and
finalized reports were unchanged. Eighteen checklist topics, 15 calendar rows,
11 separately paired glance-table entries, ten numeric and four relative timing
requirements are retained, with two new scoped and 14 reused source reviews.

Profile and October 1 directories agree: Civil O, Monica Ortiz, 813-272-5365,
circivdivo@fljud13.org, Edgecomb room526/courtroom510. All discovery hearings
use the monthly in-person discovery docket, with good-faith conferral before
setting. No discovery on UMC or ordinary 15/30-minute dockets. Withdrawal motions
may use UMC but not those ordinary slots. Pretrials, trials, evidence and all
matters over30minutes are in person. Submit an amended DCMO before asking the
JA to prepare a trial order. Clerk exhibit-assistance phone813-276-8100 is kept
separate from chambers; the full county clerk review remains pending.

The two date tables contain only July–December2026 and January–September2027.
June2027 has three trial weeks, including June28–July2. Preserve these pairings
and missing-month boundaries; do not invent additional dates or hearing times.
The bottom two tables contain additional procedural details, including three
business days for larger/longer-hearing hard copies. Do not stop reading at the
last numbered preference. Pair every table heading with its corresponding cell.

Contact-link verification exposed three mismatches: the visible Division O email
in longer-hearing scheduling, evidence-hearing scheduling and office communication
has `mailto:circivdivc@fljud13.org` as its actual target. The main contact anchor
and courtesy-copy anchor correctly display and target O. Preserve both; do not
silently replace the original or use the mismatched target as a new verified
chambers address. No email was sent.

Reproduce this bounded extraction from the saved raw HTML with BeautifulSoup:
select `a[href]`, retain anchors whose href starts with `mailto:`, and save visible
text, exact href and serialized anchor in document order. The six-anchor listing
is `review/ward-email-anchors.json`. Acquisition key
`ward-profile-email-anchors` points to the **same raw HTML hash, URL and retrieval
time** as `ward-profile`, but its text hash/path and extraction time are separate.
This derivative is not a fresh source observation. Its citation verifies the
actual targets, which ordinary page-text extraction omits. `AGENTS.md` now directs
future agents to compare mailto/tel destinations with their visible labels.

Preserved procedural differences include competing orders three days generally
versus five days after hearing; body binder timing three days versus table three
business days; body email AND phone within24hours versus abbreviated email-only
table; body dismissal needed to cancel trial versus settlement-only table summary;
body emergency flagging versus table omission; and body no-response Portal route
versus table AGREED-only wording. Shared AO units, routes and qualifications are
retained separately. No controlling-authority decision was made.

The Ward assembly preflighted current state and the next profile against the
saved roster before writing the database, preventing the previous guessed-URL
failure. The Marlewski state-repair script/receipt are now hash-bound in packet17.
No production code changes, browserUI verification, messages, filings or county
publication. Next Mark R. Wolfe, `/Directory/Judges/Judge-Wolfe`; complete his
individual review before advancing. County clerk/access/officer/material-order
work and the remaining people are still pending.

## Thirteenth judge reviewed: Mark R. Wolfe

Capture **4925**, packet `draft/checkpoint-18.json`, receipt
`receipts/person-hillsborough-circuit-mark-r-wolfe.json`. Thirteen individual
reviews complete,56pending. The review has an explicit unavailable-source limit
below; it does not assert every mentioned document was obtained. Person and
86 nested citations validated; 513 artifact bytes and110 findings read back,
exact replay and unchanged finalized reports verified. Nineteen checklist topics,
12 numeric/seven relative timing clauses, one new individual and12 reused reviews.

CivilB, Christina Novia, divisionb@fljud13.org, office511/courtroom501. Phone
813-272-6990 comes from both October1 directories; it is absent from the profile
header. Do not substitute the general administration footer number. All18 mailto
label/target pairs agree ignoring capitalization (17division links and one footer).
The biography's past criminal assignments and roster's criminal filter tag do not
establish a current extra criminal division against the dated CivilB assignment.

The profile repeats its entire12-section procedure block. The full extracted
blocks are exactly identical, 13,447characters each; comparison metadata is in
`review/wolfe-procedure-block-comparison.json`. Preserve the raw page, but review
and store one semantic checklist. Do not assume duplicated headings imply identical
content without comparison. The two identical four-column tables are blank hearing
request templates, not calendars. No dated trial/PTC calendar is present, and none
was imported from another page that happens to say DivisionB.

Distinct directions: mediation before summary-judgment hearings;10-minute UMC;
JAWS15/30-minute scheduling with a four-column email fallback; simultaneous
competing Word orders by email; per-case/per-person JAWS email registration;
three-ring binders received72hours before hearing,50pages including cases;
memos72hours and responses24hours before hearing,10-page memo cap excluding
photos/charts/diagrams. Jury attorney conference10days beforePTC versus nonjury
seven days; signedPTC order three days before; nonjury proposed findings/conclusions
in Word ten days before trial. Case closure directs dismissal notices to JAWS and
orders to Portal. These are source statements, not legal-effect determinations.

Preserve the no-password Zoom statement alongside the telephone password; in-person
nonjury listing alongside invitation to request in-person proceedings;72hours and
three days versus sharedAO business-day units; hearing-relative memo deadlines
inside an in-lieu-of-hearing paragraph; and the jury-pretrial list's three-day
introduction versus its final jury-instructions/verdict-form item due byPTC.
Cancellation says within24hours when no longer needed, without a clearer trigger.
Do not invent timing anchors or resolve controlling authority.

**Unlinked document gap:** the pretrial list names “Order on Procedures Applicable
to Jury Trials” without an anchor. Exact-title/Wolfe searches and current saved
forms indexes did not establish a Wolfe original. Similar documents name Isom,
Sisco, Barton or Huey; none was substituted. A search-indexed historical DivisionB
PDF (`ProceduresDIV_B.pdf`) returned404 with its version query and without it;
keys `wolfe-search-division-b-pdf` and `wolfe-search-division-b-queryfree` retain
responses. Its indexed contact/name cannot be used to replace current Wolfe
identity. Search leads involving Palermo/DivisionB are reserved for Palermo's own
review. This limitation does not erase the completed current profile review.

Assembly initially referenced a calendar variable copied from another receipt.
It failed before writing packet18 or the database. The repair omitted the absent
calendar citation, reused the already validated receipt only after exact equality
(including its original review time), and then completed save/read-back/replay.
`review/complete-wolfe.py` is now a completed one-shot script; do not rerun it.
For future assemblies, omit nonexistent optional records rather than creating
empty evidence to satisfy copied code. Preflight the next exact roster link.

No messages, filings, JAWS/Portal/Zoom interaction or browserUI check. Next
Michelle D. Sisco, `/Directory/Judges/Judge-Sisco`; cover civil/shared trial
procedures and record criminal assignments/links with the agreed limited scope.
County clerk/access/officer/material-order work and remaining people are pending.

## Fourteenth judge reviewed: Michelle D. Sisco

Capture **4927**, packet `draft/checkpoint-19.json`, receipt
`receipts/person-hillsborough-circuit-michelle-d-sisco.json`. Fourteen individual
reviews complete,55pending. Person/102 nested citations validated;540 artifact
bytes/116 findings read back, exact replay and unchanged finalized reports passed.
Twenty checklist topics,16 numeric/18 relative timing requirements, five new
scoped reviews and ten reused reviews. No dated calendar; contactJA for trial dates.

Trial Division1 handles civil/criminal matters; profile also identifies
PostconvictionJ and CircuitCriminalK, and biography AdministrativeJudgeCircuitCriminal.
Connie Maldonado,813-272-8551,diazcra@fljud13.org; the November4,2025 procedurePDF
also gives felonydiv1@fljud13.org and fax813-301-3842. Actual profile tel/mailto
links match their labels. **Address conflict:** profile says Edgecomb800Twiggs,
room102; PDF mailing/physical address401NJeffersonroom102, and October1directories
say Annex. Both statements and sources are retained; no controlling address chosen.

Collected and read all13pages of three PDFs: `sisco-linked-6` five-page practices
(lastmodifiedNovember4,2025), `sisco-linked-1` four-page TD1 jury-setting form
(revisedJanuary26,2015), and `sisco-linked-2` four-page jury-procedure form naming
Sisco but printedDivisionD. Only page1 of each was visually checked; images are
saved/hash-bound. DivisionD is not imported as a current assignment. Existing
exact Rule1.360 form `polo-linked-4` and shared sources are reused.

Important individual requirements include JA scheduling, immediate hearing notice,
two-business-day hearing materials, five-day continuance requests, five-business-day
remote requests with a DivisionJ monthly-status exception, and orders within10days.
All pretrial motions in transferredTrial1 cases must be heard by the original judge;
the PDF states waiver for failure timelyfile/set. Preserve that alongside older
form motion schedules. General materials two business days versus evidentiary
courtesy copies two days, hybridTrial1/J status versus J-only request exception,
paper exhibits versus shared clerk electronic directions, and jury-instruction
PTC versus last-business-day timing remain separate source statements.
The PDF's “E-Filing Portal via the JAWS system” wording is retained, not claimed
as tested interface behavior. The2015 form's empty physical-attendance checkbox
is not treated as a checked or entered case order.

Three linked civil originals return404: Sisco ad-litem, mediation and residential
foreclosure trial forms (`sisco-linked-3/4/5`). A search-discovered encoded-comma
ad-litem URL also404 (`sisco-adlitem-encoded`). Search-index text for historical
ad-litem/mediation documents is not a downloaded original. Generic shared mediation
and residential forms are alternatives, not identical replacements. Legacy Sisco
forms, ADA and interpreter paths also404; prior professionalism404 reused. These
are explicit unavailable-source limits, not inferred repeals or empty procedures.

Current official alternatives and review boundaries:

- `sisco-interpreter-current`: Court Services → Court Operations → Court Interpreter
  Center. Contacts, FAQ, observer guidance and request fields read; linked training
  and private-resource destinations not substantively reviewed. No form submitted.
 419NPierceSuite107,8132725947,interpreterrequest@fljud13.org. Preserve due-process
  coverage qualifications and self-arrangement/cost instructions; do not promise
  a commercial litigant court-funded interpreting from the general “trials” list.
- `florida-bar-trial-guidelines`: official Bar page updated2024. Header/foreword
  and fullSectionM reviewed; A–L collected only. The foreword says the guidelines
  do not have force of law and2024 supersedes earlier editions. Current text is
  not assumed identical to the edition referenced by the undated Sisco form.
  SectionM citation uses the actual body occurrence, not its table-of-contents
  heading. The county's separate court-posted standards remain `attorney-resources`.
- Current ADA request page `polo-linked-1` and current Sisco profile Forms tab
  replace navigation to broken legacy paths, without asserting identical contents.

Criminal assignments, links and shared procedures are covered; specialized
criminal merits were not exhaustively analyzed. No filings/messages, authenticated
system use, browserUI check or publication. Next Lyann Goudie,
`/Directory/Judges/Judge-Goudie`; complete her civil/shared review before advancing.
County clerk/access/officer/material-order work and remaining people are pending.

## Fifteenth judge reviewed: Lyann Goudie

Capture **4929**, packet `draft/checkpoint-20.json`, receipt
`receipts/person-hillsborough-circuit-lyann-goudie.json`. Fifteen individual
reviews complete,54pending. Person/55 nested citations validated;552 artifact
bytes/119 findings read back, identical replay and unchanged finalized reports
passed. Fourteen checklist topics, three numeric and nine relative timing clauses,
two scoped new reviews and four reused reviews. No dated calendar inferred.

Civil/criminal TrialDivision2, Deborah Sabella,813-272-6845,
FELONYDIV2@fljud13.org, Criminal Courthouse Annex401NJefferson, office516A and
courtroom51A. Dated directories omit the office suffixA (516); preserve this
rather than silently normalizing. Profile biography's FelonyB January2021 entry
is historical against the current header/datedTrial2 assignments. Actual contact
hrefs match their displayed phone/email; no contact action occurred.

All nine individual sections were read. Trials transfer after notification by
the original lettered division; parties must not independently ask trial divisions
for dates. Pretrial motions, including limine, are heard by the original judge
beforeTD2 jury selection. No continuances after transfer; seek them before the
original judge under that division's preferences. Jury instructions/verdict forms
are emailed to court/opponent in Word, TimesNewRoman12: Thursday before Friday
selection, Friday before Monday selection. Do not invent other-weekday deadlines.
Witness/exhibit lists and evidence review requirements are retained separately.

Remote evidence must be efiled at least four business days before hearing, with
emailed copies; specific written objections and witness exhibit copies at least
two business days before. One premarked PDF per exhibit, sequential pages,
photographs of physical objects, and an index recording stipulation/admission
status. The displayed bank/photo index rows are examples, not actual evidence.
Prefiled items remain public even if not admitted. Witness ID, room scan, no
virtual background/other devices and advance preparation are preserved. The
profile's historical AOSC20-16/AOSC20-23 amendments references are recorded without
claiming those originals were newly collected or determining their current force.

The only linked PDF, `goudie-linked-1`, is a two-page criminal plea/sentencing
physical-presence waiver. Whole original collected; page1 header/scope read;
page2 and specialized criminal merits not reviewed. It is not a civil remote-
appearance form. This scope implements the user's criminal-law priority limit.
Civil/criminal AO index fragments are both recorded and reuse the same saved
index body. The index itself is not evidence that every listed order was reviewed.

No separate general proposed-order/binder/response-time directions were found
in the complete individual profile. Record that absence explicitly; do not turn
remote-hearing evidence instructions about orders/judgments into a general
proposed-order submission route or copy another judge's policy. The shared civil
order and clerk exhibit sources retain their own scope and dates.

No messages, calls, filings, private calendars, Portal/JAWS/Zoom use, browserUI
check or publication. Next Thomas N. Palermo, `/Directory/Judges/Judge-Palermo`.
Earlier search results showed DivisionB content there; compare the current header,
procedure/form titles and October1 directory before attributing any of it. Do
not copy that calendar to Wolfe merely because it saysDivisionB. County clerk,
access, officer and material-order tasks remain pending.

### Palermo checkpoint — October 16, 2026

Capture4931 (`eb514550bd064f15df365e139eb570b836a50f0d7dbd1d454af3808154245ee2`),
immutable `draft/checkpoint-21.json`:16 complete,53 pending. Current profile and
October1 directories agree: Thomas N. Palermo, civil/criminal Trial Division3,
Ann Mynatt,813-307-1940,felonydiv3@fljud13.org,Annex401NJefferson room615,
courtroom62. Biography dates TD3 to September2026 and CivilB June–September2026.
AO2026-034 establishes the division's operation June29; it does not itself date
Palermo's personal assignment. Preserve those different propositions.

The profile retains CivilB procedures and calendar: two identical trimmed15,666-
character procedure blocks;2026 September/October and ten2027 rows. No May/December
rows invented. Body uses DivisionB emails and courtroom501, and a motions paragraph
names Judge Ellison. Do not treat that text/calendar as verified currentTD3 rules
or copy it into Wolfe's record. All17 topics reviewed as source statements with
current applicability unresolved. This is a completed source review with a documented
conflict, not a resolved current-procedure association.

All six new Palermo-filename PDFs were collected and fully text-reviewed. Jury and
fee-hearing forms expressly name PaulL.Huey; foreclosure form names DivisionI and
courtroom506. Page1 of each was also visually checked. Other forms are blank general
adlitem,garnishment and mediation forms. Keep their own attribution, dates, historical
rates/references and scope; filename/link is not adoption. Twenty-one existing shared
reviews reused with original scope and retrieval dates, including the JAWS generator's
initial public page only (no case input),ADA request,DCM,clerk exhibits and BarSectionM.

ActualHTMLcontact inspection found visible/tel8133071940 but aria-label8132725450.
Two empty email anchors targetgencivdivd. Do not import either latent value into the
current contact fields. `review/palermo-derivation-provenance.json` binds anchor/table/
link extracts to originalURL/hash/retrieval time and extractiontime/filehashes.

Validation:145 nested citations,17topics,12calendar rows,32numeric timing clauses,
9relative clauses;579 artifacts and127 cumulative findings read back; identical replay
and unchanged finalized reports. No communications,filings,browserUI check or public
release. Source-level review does not determine which conflicting requirement controls.
Next is county-civil Judge Allen from saved roster `/Directory/Judges/Judge-Allen`;
verify his current name/assignment before receipt. Finish substantive countyDCM review
of `ellison-linked-4/5` with the first county-civil review (previously page1 scope only).
County clerk/access/officer/material-order tasks remain pending.

### Allen and county-civil shared sources — October 16, 2026

Capture4933 (`7223c147518f850ec34c43a5df7c555dec5407730a92b87b0ce9ea3da705b55e`),
immutable `draft/checkpoint-22.json`:17 complete,52 pending. Lisa A. Allen,
County CivilO, Donna O'Dell,813-272-0240,civdivo@fljud13.org,Edgecomb room312,
courtroom301. Current profile and dated roster agree; biography dates assignment
February2026. The earlier pending-state name JamesS.Allen was an unverified
placeholder and was corrected before any person record was created. Future task
names must use the roster label until the full name is verified from evidence.
All visible contact targets/accessibility labels agree on this page.

All six individual procedure sections reviewed,10 checklist topics: JAWS hearings
through60 minutes,JA for longer hearings; inperson default with narrow approved
remote exceptions; PDF proposed orders within1 week; hardcopy authorities3business
days before hearing. Unilateral scheduling requires at least72hours/3documented
attempts and hearing at least30days after third attempt. No individual attachment
or dated calendar. General Zoom header does not grant remote-appearance permission.

Separate county-civil governing sources now saved and fully reviewed:
- `county-civil-2026-039`,16pages,issuedJuly16/effectiveAugust24,2026,
  supersedes2026-024. All30sections, including geographic assignment, registry
  disbursement, multicount jurisdiction, PIP/windshield, hearing/trial scheduling,
  emergency routing, orders, postjudgment contempt and professional requirements.
- `county-dcm-2024-086`,9pages,issuedDecember12,2024/effectiveJanuary1,2025,
  supersedes2022-033. General/streamlined assignments, service, conferral,
  modification and trial setting reviewed. Table and signature pages visually checked.
- `county-mediation-2008-164`,3pages,issuedDecember3,2008/effectiveJanuary1,2009,
  supersedes1999-006. Private selection/deferment/rescheduling, payment and billing.

Previously saved `ellison-linked-4/5` (county streamlined/general DCM forms) now
fully reviewed, including all29 structured filing-relative offsets. General
projects18months, streamlined12months; firm dates require separate orders.
Original retrieval times and old header-only review captures remain intact; this
checkpoint creates new reviewed versions rather than rewriting history. Blank
case dates remain blank. Form titles say afterJanuary1 versus order on/after;
forms still refer to2024-071 and successors. Preserve those statements and the
current2026-039 source without inventing the entire intervening successor chain.

Four additional generic county forms from saved Resources/Forms were fully read:
PIP mediation request(1page), mediation referral excluding smallclaims(2pages,
revisedMay22,2023), jury pretrial(5pages,September22,2014), nonjury pretrial with
technology attachment(4pages,May1,2008). No other division's PIP form substituted
for Allen. Older equipment options/contact details remain source statements,
not verified current availability. Mediation form says$60/party/session and48
business-hour cancellation; older AO has48hour rescheduling and24hour billing
threshold. Individual orders1week versus shared10days and hearing-wait wording
also remain separate; no resolution of controlling authority.

Validation:133 nested citations,10topics,33timing clauses,29DCM offsets,
4relative requirements,10source reviews plus3reused reviews;615 artifacts and136
facts read back, exact replay and unchanged finalized reports. Eleven rendered
pages checked for signatures/tables; no browserUI, filings, calls or emails.
Referenced Eastboundary/reporter/other professional materials remain county-level
followups; prior Bar review is still header/SectionM-only, not full guidelines.
Next `/Directory/Judges/Judge-Baggé-Hernández`, exactly as saved roster. Verify
full name before receipt. County clerk/access/officer/material-order work pending.

### Baggé-Hernández checkpoint — October 16, 2026

Capture4935 (`5edbec06ea8c607fe5e28bab93e0cc5780a982fc29d5e4294cc6a34979965dc0`),
immutable `draft/checkpoint-23.json`:18 complete,51 pending. Michael C.
Baggé-Hernández, County CivilJ, Yolanda DeVesta,813-272-0243,civdivj@fljud13.org,
Annex401NorthJefferson room231/court11. Header, procedure body and October1 roster
agree. Undated biography says CountyCivilL and tab says UnifiedFamilyL; preserve
those labels without inventing historical assignment dates. Visible/tel phone agree,
but HTMLaria-label says8132762014. The latter is not a verified contact.

All13 individual sections fully read,17 topics. Paperless chambers: no mailed,
hand-delivered or couriered submissions unless ordered. Authorized courtesy copies
searchable PDF/emailall; voluminous filings use concise index/docket references,
not unapproved cloud links. Working copies/physical exhibits may still be brought
to inperson proceedings as specified; paperless chambers does not prohibit that.
Inperson default with Rule2.530 motion/authorization; Zoom link alone insufficient.
Unilateral45days; hearing materials/exhibits5days; posthearing orders14days and
consultation5days. Competing Word orders only when requested, agreed/unopposedPDF
Portal, no signature-only page. Emergency, smallclaims, eviction, trial preparation,
access, reporters/interpreters and corporate representation qualifications retained.

Sole linked PDF is existing `circuit-setting-jury`:2015 Circuit Court form,
not automatically a CountyJ rule. Shared Forms also expressly lists DivisionI/J
PIP form (`county-pip-ij-form`),3pages now fully reviewed. It measures response20days
from PTC, discovery30days fromorder and scheduling mediation90days fromPTC, with
2005 statute/rule references. Current shared countyAO uses complaint-service
20/45day triggers and no automaticPIPPTC. Keep both attributed, no silent repair.

Profile cites S-2025-014 for compels without hearing. Official search located its
URL, but direct HTTP and web-open both returned404. Original404response saved as
`county-civil-2025-014`; indexed excerpts are not a collected/reviewed original.
Current2026-039 separately reviewed; full intervening successor chain not asserted.
No published datedcalendar; conditional reference to Schedule tab is not evidence
of available dates. No communications/submissions/privatecalendar or browserUIcheck.

Validation:131 nested citations,17topics,15numeric/8relative timing clauses,
2new reviews and13reused reviews;629 artifacts/139 facts read back, identicalreplay
and unchanged finalizedreports. Shared source dates and prior review depth retained.
Next exact roster `/Directory/Judges/Judge-Bantner`; verify full name before receipt.
County clerk/access/officer/material-order followups remain pending.

### Bantner checkpoint — October 16, 2026

Capture4937 (`89cfbe603fb0079ea40a367eaf118d25993df377cc42629490e145a173c4cb01`),
immutable `draft/checkpoint-24.json`:19 complete,50 pending. Adam L. Bantner,
County CivilM, Suzanne Flowers,813-272-5353,civdivm@fljud13.org,Pat Frank
Courthouse419N.Pierce Street,courtroomB. Division directory adds assistant middle
initialM; no separate office room published, so courtroomB is not an office room.
Contact targets/phone accessibility label agree. Two email anchor labels contain
sentence-ending periods; originals retained, periods excluded from contact value.

All11 individual sections fully reviewed,13topics. JAWS59minutes or less versus
JAover60 leaves exactly60 undefined; do not silently fill that interval. Orders
PDFPortal within1week, prescribed electronic Done/Ordered clause, no signature
line/name. Hardcopy authority3businessdays. Remote short nonevidentiary consent-
notice procedure retained separately from14day motion/10day objection for inperson
hearing exceptions; silence permits proposed-order upload, not automaticapproval.
FinalPTC one monthbeforetrial,trialcall firstday9am,oldestcasefirst,45minute standby
return. No datedcalendar published; dates requested fromJA withallpartiescopied.

AI section expressly removes prior requirements following May28,2026 Rule2.515
amendment. Existing state originals AOSC26-12/SC2026-0673 reused:issuedMay28,
effectiveJune15. Record present removalstatement, not a newly observed legalchange
or reconstructed prior text. No need to resolve conflicting authorities here.

SharedForms DivisionM PIPform(`county-pip-m-form`)3pages fully reviewed, including
requestform. Unlike I/J form, discovery30days runs fromPTC and mediation must be
completed90daysafterPTC. Response20daysPTC;historical2005references. Preserve these
triggers separately from currentcountyAO20/45dayscomplaintservice/noautomaticPIPPTC.
Bantner's text calls S-2021-057 governing; official search found the citation but
no original. Bounded repository-pattern URL returned404,webopen unavailable;
response preserved, original not claimed collected/reviewed. Current2026-039 is
separate evidence, not a substituted historicalcopy or asserted successorchain.

Validation:126nestedcitations,13topics,13numeric/3relative clauses,2newreviews,
14sharedreviews;641artifacts/142factsreadback,identicalreplay,finalizedunchanged.
No calls,emails,filings,privatecalendar,JAWS/Portal/Zoomuse orbrowserUIcheck.
Next `/Directory/Judges/Judge-Black`, roster lists countycivil/family; verify
currentassignment and scope civil/shared review. County-level followups remain.

### Black checkpoint — October 16, 2026

Capture4939 (`26348b3e97a7d68efcbc2edd018bb1a4caa7fc2189e700d74b2660a612ef8124`),
immutable `draft/checkpoint-25.json`:20 complete,49 pending. Melissa C. Black,
County CivilS/UFC Protective InjunctionsK,Robyn R. D'Agresta,8133017033,
civdivs@fljud13.org/famlawdivk@fljud13.org,Edgecomb316/court306. Currentheader,
biography and datedroster agree; divisiondirectory omits assistant middleinitial.
Actualcontacttargets andphoneaccessibilitylabel agree.

Allthree profileproceduresections reviewed,12topics includingfeeform. KeepK
inperson/speciallyauthorizedZoom instructions distinct fromCountyS. CountySJAWS
<=30minutes,JAforlonger;crossnoticeonlycleared;writtenemailedcancellation.
Claims of exemption expressly scheduled throughclerk,courtsupportmanagers@hillsclerk.com,
not generalJAWS. PDForders/coverletter;paperconformingcopies/postagewhenneither
partyrepresented orPortalunavailable. AgreedOrder requiresdocketentrybasis.
DamagesjudgmentForm1.977attachmentrequirementpreserved; separateformtextnotreviewed.
Authoritynotebook5businessdaysbeforehearing. No datedcalendarpublished.

`black-linked-1`,3pages/all17paragraphs reviewed: namedBlack CountyDivisionSfee-
hearingprerequisites,exchange/timesheets/objectionsandreplybeforeJAsetting,
limiteddiscoveryandwrittenobjectionhearinglimits. Expertmeeting literally "not more
than two business days immediately preceding" hearing, not at leasttwo daysbefore.
Timelyentitlementstaymotion within30daysoforder automaticallystaysdeadlines and
requiresseparateentitlementhearing. Paragraph6notice referencesparagraph5; retain
thatcrossreference. Filenamequery2023date is metadata,notstatedeffectivedate.

Profile retains localAIface-disclosure/personalaccuracycertification requirement.
StateAOSC26-12/Rule2.515 originals separatelyretained:May28issuance/June15effect.
Conflict explicitlyrecorded withoutdecidingcontrollingauthority orblockingreview.
`bar-ethics-24-1` collected/all7pagesreviewed,January19,2024,expresslynonbinding:
confidentiality,oversight/verification,fees/costs,advertising/chatbotdisclosure.
Not conflated with a courtfilingdisclosureorder. Existingstateoriginals reused.

LinkedS2026-024(`black-linked-2`)404responsepreserved;notclaimedoriginalreview.
Current2026-039expresslysupersedes024effectiveAugust24,2026. This directstatement
supports supersessionfinding despite unavailableoldcopy; no fullchaininvented.
Validation:119citations,12topics,8numeric/3relativeclauses,3new/14reusedreviews,
656artifacts/146factsreadback,exactreplay,finalizedreportsunchanged. No calls,
emails,filings,privatecalendar,PortalJAWSZoom participationorbrowserUIcheck.
Next exactroster `/Directory/Judges/Judge-Costello`, verifycurrentassignments.
County clerk/access/officer/material-order followups remain pending.

### Costello checkpoint — October 16, 2026

Capture4941 (`fa3446788ed1295b91c1b8e8491c74f39b7abc367237d282cf82c43bf8f3fbf5`),
immutable `draft/checkpoint-26.json`:21 complete,48 pending. Jessica G. Costello,
County Civil K/UFC protective injunction H; Tawanda Streater,813-272-7138,
civdivk@fljud13.org/famlawdivh@fljud13.org, Edgecomb room313/court303.
Current profile, dated directory and actual email/phone targets agree.

All four profile sections and six PDFs (17 pages) text reviewed; six selected
trial/waiver pages visually checked. No dated calendar. County hearings <=15minutes
use JAWS UMC, longer hearings use JA; this differs from Zoom coordination threshold
of <=60minutes. Unilateral notice at least60days only if opponent nonresponsive.
Orders10days after hearing/ruling, circulation7calendar days, authority2business
days; any self-represented party triggers paper order/copies/envelopes. Final PTC
one month before trial, trial call first day9am, standby45minutes. Keep months
literal and do not copy another judge's notebook or paper-submission exception.

`costello-linked-1` fee form: all17paragraphs read, same conditional automatic
entitlement stay and not-more-than2business-day expert meeting as Black's form,
but independently attributed to Costello/CountyK. `costello-linked-2/3` jury/nonjury
trial orders each5pages, named Costello. Preserve historical2022-033 references
and current2024-086 express supersession separately. Both tables literally say
“close of fact expert discovery in DCM order”; visually confirmed, not repaired.
Jury instructions14days before PTC, Word email and hardcopies; nonjury trial
briefing requires approval/request, then filing7days before trial. Both forms
refer to historical Circuit-Civil pretrial forms; do not infer wholesale circuit
procedure adoption. Nonjury intro November7,2022 is underlying DCM issuance,
not a claimed form revision date. Duplicate paragraph5 retained.

`costello-linked-4/5`: Auto Glass and Small Claims waiver forms each1page,
not identical. Auto Glass version includes jury demand; other version omits it.
Both require mediation before trial scheduling and an order excusing PTC;
submitting a stipulation alone is not automatic waiver. Their Small Claims Rules
statement is preserved alongside current countyAO's full Civil Rules provision
for windshield cases filed on/afterMay1,2021. No controlling-authority decision.
Shared index `county-pip-k-form`,2pages, response20days afterPTC, discovery30days
PTC, mediation30days Notice of Trial; telephone mediation consent/good cause5days
before, ADA2working days receipt. Do not replace these with M/IJ form triggers.

Profile section2 AI disclosure/certification and section4 Rule2.515 representations
both retained, with state AOSC26-12 conflict recorded. Same S2026-024 URL reuses
Black's404 original; current039 expressly supersedes024. Form1.977 attachment
requirement retained, separate form content not reviewed. No communications,
filings, private-calendar access or browser UI validation.

Validation:188 nested citations,18topics,40 numeric/8 relative timing clauses,
7 new and18 reused reviews;684 artifacts/154 facts read back, identical replay
and unchanged finalized reports. Next exact roster URL has lowercase slug:
`https://www.fljud13.org/Directory/Judges/Judge-cuellar-stilo`.
Verify all assignments and scope review to civil/shared procedures. County-level
clerk/access/officer/material-order tasks remain pending.

### Cuellar-Stilo checkpoint — October 16, 2026

Capture4943 (`3aa4ec9aba2112e00a5b39d82a755e7f0326c8cff7c32c443a66275ac027c632`),
immutable `draft/checkpoint-27.json`:22 complete,47 pending. Mary Lou Cuellar-Stilo,
Emily McGregor,813-272-7266, Criminal Courthouse Annex401N.Jefferson,room235,
court21. Assignments are civil trafficM, noncriminal/nontraffic infractionsT and
TitleIV-D child-supportY. Do not merge trafficM with Bantner's ordinary civilM.

Header/dated roster room235 differs from all three procedure notice-mailing
addresses room225. Family header `famlawdivy2@fljud13.org` differs from procedure
body `familylawdivy2@fljud13.org`; both labels match their own mailto targets.
Traffic `trafficdivm@fljud13.org` and infractions `civdivt@fljud13.org` agree
throughout. Preserve these source statements without choosing a correct address
or sending test communications. Footer publicinfo is not a JA address.

All three profile sections read and shared procedures recorded: in person unless
ordered otherwise; JAWS<=15minutes, longer through division email; motion first,
file/copy notices, prompt written cancellation. Unscheduled motions pending60days
presumed denied without prejudice unless good cause; filing alone does not suspend
deadlines. Orders3weeks hearing/ruling, circulation10calendar days; counsel mails
signed order to self-represented opponent5calendar days receipt. If neither party
represented or no Portal access, paper/copies/envelopes. Authority3business days,
opponent prehearing exhibit inspection, emergency immediate availability even
nights/weekends. No expanded traffic/family merits research; case-type qualifiers
remain attached to each procedure. No dated calendar or remote credentials.

Three linked PDFs,7pages fully text reviewed;4selected pages visually checked:
`cuellar-linked-1` generic motion2pages, revisedJanuary5,2022; actual PDF title
and content differ from its misleading address-designation aria-label.
`cuellar-linked-2` recording standing order3pages expressly **County Criminal D**,
no shown date/signature/named judge. Shared courtroom-access contents reviewed;
current M/T/Y applicability unresolved. Prior authorization for recording/media,
juror/attorney-client protections, device controls/sanctions and nonrecording
note-taking exception retained. Its S2024-078 reference remains separate county
courthouse-access followup, not a claimed original review or reason to expand
criminal merits research. `cuellar-linked-3` address designation2pages revised
March18,2021: instructions and service/signature fields reviewed; dated e-service
statements not represented as current statewide rule text.

Shared countyAO, ADA, attorney standards and interpreter center reused within
original review scopes. Form1.977 requirement remains qualified “if applicable”;
separate form text not reviewed. Clerk/service/equipment links are discovery leads
for county tasks, not implied content review. No contacts/filings/private calendar,
Portal/JAWS use or browser UI check.
Validation:74citations,15topics,5numeric/5relative timing,4new/4reused reviews;
704artifacts/159facts read back, identical replay, finalizedreports unchanged.
Next exact roster `/Directory/Judges/Judge-Edwards`; verify current identity first.
County clerk/access/officer/material-order tasks remain pending.

### Edwards checkpoint — October 16, 2026

Capture4945 (`ad8d90a1cee9c2b65786de06928533947062d56e69df7a08f2fe23273e25ed2a`),
immutable `draft/checkpoint-28.json`:23 complete,46 pending. Christine D. Edwards,
County Civil I, Beth Schatzberg,813-272-6562,civdivi@fljud13.org,Edgecomb318/court305.
Profile, guide contact block and dated roster agree. All visible profile contact
labels/targets/phone accessibility label agree.

Official profile has12 PTC/jury-pick/trial rows, including January2026 PTC marked
PM and February/December “pick and go” periods with two nonconsecutive dates.
Store those as separate dates, not a continuous interval. Calendar weekdays were
checked. These are posted trial dates, not live available slots. Procedure guide
`edwards-linked-16`,24pages, establishedOctober20,2025, fully read A–M. Twelve
individual forms (`edwards-linked-1` through12),44pages, fully read. Eleven
selected table/link pages visually checked. Three statewide compilations13–15,
661pages, collected with front-page version/scope review only: CivilJanuary1,2025;
SmallClaimsOctober24,2022; GeneralPracticeOctober31,2024. They do not replace
current statewide evidence or count as661pages of substantive review.

Guide preserves a detailed scheduling/remote matrix. UMC says5minutes total or
3minutes per side and Zoom only; do not make that6minutes or general hybrid.
Daily15/30slots; final/ordinaryPTC require orders; >=1hour through court. No party
unilateral setting: court-date request after2written unanswered attempts, court
selects >=30days out. Within24hours, expiredDCM hearing cannot be cancelled and
converts to CMC. ActiveDCM cancellation differs. Nonevidence<=1hour, clerk-default
evidence<=1hour and CMC may be remote without permission. OrdinaryPTC, contested
fees, dismissal, finalhearings/trials and >1hour are listed mandatory in person;
smallclaimsPTC/evidence<=1hour/showcause require waiver order. End-of-guide
permission to attend any hearing in person remains distinct from UMC Zoom-only.

PDF link extraction found the printed full Zoom address/credentials correctly,
but actual hyperlink points to `https://fljud13/`. ADA target also truncates at
`adaaccom`. Keep visible text, actual PDF URI and original bytes separately;
do not substitute the malformed link for meeting contact information. Shared
current ADA source reused. No actual meeting, Portal/JAWS or browser UI use.

Orders10days oral hearing/ruling; competing orders only requested, Word email,
not queue. Authority <=5cases PDF email, >5paper,3businessdays before proceeding.
Evidence specifically identified and contemporaneously filed; refile old exhibits
for intended hearing; no screen sharing/smartphone review. DCM extensions require
actual proposed categories, hearing for stated >90day extension threshold, CMC
set10days filing, older-than3year cases CMC. Mediation before MSJ/final/PTC except
clerkdefault/excusal. Default still requires proof of damages and supported motion;
finaljudgment checklist includes contract/assignment and specified affidavits.

Fee form differs from Black/Costello: cost support10days written request, and
schedule hearing no later120days entry, not a computed actual hearing date.
Timesheets30days order, response30days movantNotice, reply10days objections;
expert narrowing not morethan2businessdays immediately before, timely entitlement
stay30days automatically stays deadlines. Retain literal trigger distinctions.

AmendedDCM form has28 two-track offsets; notably no General535day resolution row.
Mergedtrial form separately has12 printed General defaults and blank case dates.
Trialforms use10days beforePTC for jointstatement/limine/instructions,3days before
trial for approved/requested authority, and CBC7days beforetrial. Guide/finalhearing
form use3businessdays for authorities; jointstatement CBC7days beforePTC.
Do not homogenize those units or events. Guide says trialorder supersedes DCM,
while templates retain unmodified active/expired deadlines. Mergedform prints
“120 dates” for plaintiff witnesses; preserved, not silently corrected. Extracted
jointstatement item8 preceding6 was an extraction-order artifact; image shows
correct5–12 sequence. Template weekend/holiday rule retained without calendaring.

Jointstatement references AttachmentA technology checklist, absent from its5pages.
Bounded official searches returned the already saved historical Circuit nonjury
form, not an Edwards attachment. Missing attachment remains explicit; historical
attachment not substituted. Finalnonjury form includes its own exhibitlist,14day
exhibit/specialdamage deadline,10day jury/time/PTC objections,3businessday materials,
and no stipulation waiver. Current sources are not a claim of newly changed law.

Guide localAI disclosure/certification conflicts with preserved state AOSC26-12;
no control determination. Guide cites2025-014 and once2025-04 as printed; profile
and amendedDCM cite2026-024. Saved404 originals reused; current039 expressly
supersedes024, no full intervening chain asserted. Shared I/J PIP historical form,
county/DCM/mediation/access/stateAI sources retain original review boundaries.

Validation:296nested citations,24topics,12calendar rows,61numeric rules plus28DCM
and12merged-default offsets,10relative clauses;17new/16reused source reviews.
759artifacts/177facts read back, exact replay and unchanged finalizedreports.
Next exact roster `/Directory/Judges/Judge-Giardina`; identity verification first.
County clerk/access/officer/material-order followups remain pending.

### Giardina: checkpoint29 / capture4947

James S. Giardina, County Civil H, completed as the24th current-person review.
Official profile `/Directory/Judges/Judge-Giardina` agrees with the dated directories:
Desiree Wilson,813-272-5778,civdivh@fljud13.org,Edgecomb room315/court304.
Named forms expand his middle name to Salvatore. All12 profile procedure sections,
52PDFpages and shared-source associations reviewed;16 selected PDFpages visually
checked. Receipt `receipts/person-hillsborough-county-james-s-giardina.json` and
immutable `draft/checkpoint-29.json` are in the county workspace. Capture4947:
`006658d05449d858fb10c008172e2f8bfdebf8bbda09afb25fee0b7a72fa0d22`.

Important extraction lesson: inspect original HTML table cells. The approval text
is in the30–60 minute booking cell, not the cancellation cell. A flattened-text
reading would misattribute it. Section1 says more than30 minutes through JA;
table includes exactly30;16–29 minute gap remains unresolved. Cancellation24hours
and less-than1-business-day discretionary ruling clauses retain their own units.
No actual calendar published; sample ZoomAugust20,2023 is an example only.

Header says Zoom password unnecessary; body/example says031612. Profile court304
versus named trial forms PTC303. AmendedDCM has County caption but Circuit Civil
subtitle/2021 references; old jury template has Circuit caption and Jan26,2015
revision, identical bytes to `circuit-setting-jury`. Garnishment form mixes Circuit
caption/CA label with County Judge signature. Current applicability unresolved.
Do not substitute these for current county039/DCM086 or decide controlling law.

Proposed orders1week, consult parties, three-day no-response exception; PDFPortal,
optional paper after hearing if any self-represented party with3conforming copies.
Competing Word email, no further argument. Optional authority3businessdays before
hearing; nonjury approved/requested briefing7days beforetrial. FinalPTC1month
before trial. Trial forms preserve ambiguous “close of fact expert discovery,”
120/90witnesses,30dispositivehearing,21exhibits,14meeting/jointstatement/limine,
3pretrialorder days beforePTC; CBC/reporter7beforetrial and Fridaylimine hearing.
Profile jury materials7beforetrial distinct from template14beforePTC.

Postjudgment forms reviewed with actual predicates and exceptions: compel30days
order unless satisfied/stayed; contempt recites45day judgment duty and20day purge,
personal service, affidavit and ability findings; writ firstappearance24hours,
presiding-court/4pm sheriff notice qualifications, alternative$500purge. No case
identifiers populated or actual enforcement action. DivisionH PIP form found on
shared forms index:20/30days afterPTC and mediation beforetrial, distinct from
current039 service-based PIP timing. Undated form retains old ADA contact/timing.

Residential clerk parent page reviewed; child forms/process links remain county
clerk tasks in `review/giardina-eviction-links.json`. Parent15day monthly notice
versus official2026 §83.57 thirtydays retained as conflict. Printed86.56 anchor
actually targets83.56. Pandemic notice not treated as verified program availability.

Bar2024 Guidelines now fully reviewed (foreword/preamble/A–M); existing finding
version upgraded, prior partial review retained in history. Linked LegalFuel page
has Download href#; actual public endpoint is HTML `data-downloadurl`. Landing
create/updateFebruary16,2026 versus PDFUpdatedJuly2022 recorded separately.
13physicalpages including cover/AppendixA reviewed, recommendations qualified by
rules/orders/judicial directions. Preserve “within5calendar days in advance”
literally, not “at least5.” BarExpectations6pages distinguishes must/should,
committee2014/Board2015 from2017 upload metadata. HCBA403, courtroom-help primary
and sandbox shells, and YouTube title-only response remain substantive-review gaps.
Court-linked video is external hosting, not official video-content evidence.

Browser validation unavailable: chrome executable missing; Firefox temporary and
repo-persistent profiles both failed “Could not find profile folder.” No browser
page verified. Zoom example PDF warned wrong object offsets6/8/10/12; extraction
completed and PyMuPDF image inspected without changing original bytes. These
limitations are in the receipt, not hidden by successful database validation.

Validation:223 nested citations,26topics,41numeric rules,11DCM offsets,8Bar-remote
rules,7relative clauses,18source reviews/17reuse.826artifacts/195facts read back;
exact replay and finalized-report preservation verified.24complete/45pending.
Next exact roster `/Directory/Judges/Judge-Gutman`. No publication/finalization.

### Gutman: checkpoint30 / capture4949

Jack N. Gutman is the25th completed current-person review. Profile uses Jack
Gutman; named guide/form supplies N. County CivilV,JudyFields,813-272-5809,
civdivv@fljud13.org,Edgecomb430/court412 match current profile,September2026guide
andOctober1directory. Official duty-page November16–22,2026 row instead gives
813-272-5228/231Annex with sameJA. Retain dated duty context, no replacement of
current chambers or inferred transfer date. Duty page is collected; only Gutman
row reviewed for this checkpoint, other rows require later reconciliation.

Originals: exact roster `/Directory/Judges/Judge-Gutman`; profile links9page
`JudicialPracticesAndProcedures/JudgeJackGutman.pdf` and8page ThemePluginPro form
in2026/7/16. Profile label says Non-Jury; actual PDF title includes Jury Trial
Procedures. All17pages and20checklist topics reviewed;10selected pages visual.
Prefilled PTC April14,2027,2pm/court412 and trialweekMay17,2027,8:30am retained
as template statements. Parties/case/signature blank; not confirmed available
calendar or actual booked matter. Guide's Schedule tab absent from current
profile. Bounded official searches found duty schedule and older2020criminal
dockets; those older criminal procedures were not imported for currentCountyV.

Scheduling:UMC<=5minutes,JAWS<=30,email>30. JA reserves inJAWS only after receiving
eFiled notice; immediate file/service, motion filing date/index,Zoom/ADA details.
Unilateral30days plus detailed efforts, no fixed attemptcount stated. Crossnotice
prohibited; agreed additions requireJA clearance/amendednotice and enough time.
Continuance5days/goodcause/party signature; cancellation and dismissal/settlement
promptJA notice, same-day file/service. Hybrid has in-person evidence/trial/PTC
(except clerk smallclaims)/eviction/>30minute categories; remote goodcause motion
and actual objectionstatus, no silence shortcut. Zoom9359973308,no password,
phone17866351003,*6; attorneys video absent permission, full names.

OrdersPDFPortal agreed/unopposed5days; consult5dayshearing,submit14dayshearing.
CompetingWordemail, no extra argument. HistoricalS2025-014 discovery citation
original remains404; current039 is separate source. Materials sectionB5days and
case law **5pages**, not5cases. SectionE optional PDF, less-than50page hand/mail/email
wording,5days evidentiary proceeding; no invented route for50+pages. Exhibits
mail7/hand3days and receipt3days; paperclerk except audio/video disc/thumbdrive,
proponent arranges display. Preserve different source units/conditions.

Trialform adds60day discovery/dispositivefiling,30daymotionhearing,21exhibits,
14meeting/jointstatement/limine/instructions beforePTC; voir dire5,pretrialorder3,
mediation20beforePTC. CBC/reporter/approvedauthority7beforetrial; Fridaylimine.
Profile no-motions-afterPTC wording retained alongside limine exception/template.
No unilateral stipulations; immediate motion for delayed joint preparation or
late-discovered item, strict disclosure limits with goodcause/manifestinjustice.
Court continuance order required; discovery afterPTC needs goodcause/no delay,
separate from60day discovery exceptional-circumstances requirement.

PDFp9 printed ownjudgeForms.aspx main annotation actuallyForms.asp; final-x
annotations point to JenniferPJohnson/Forms.aspx. Both ownjudge URL variants404;
wrong-judge link not followed/imported. ActualZoom link matches. Guide broad
interpreter-unavailable statement retained alongside shared official qualified
exceptions. CountyForms index listsPIP H,I/J,K,L,M,U, noV-specificPIP located.
Shared countyPretrial forms reused with dates/scope; no otherdivisionPIP substituted.

Capture4949 `cc46635f0345da2dcbc0d47e1b87b2494af06598e15e05ec1710461427025fab`;
receipt `receipts/person-hillsborough-county-jack-n-gutman.json`, immutable packet30.
144citations,20topics,26numeric/8relative/5otherthresholds,4source/14reusedreviews;
855artifacts/200facts read back, exact replay and finalizedreports unchanged.
No browser UI/JAWS/Portal/Zoom use. Webtool profile open failed InternalError;
directHTTP200 original collected/read. Next exact roster JudgeHenderson,
`/Directory/Judges/Judge-Henderson`;25complete/44pending plus county followups.

### Henderson: checkpoint31 / capture4951

Branden M.Henderson,CountyCivilN,26th reviewed person. Currentprofile andOctober1
directory ZuleimaTavarez,8132725887,civdivN,CriminalCourthouseAnnex401NJefferson,
room232/court22. September2026guide instead Zuleina(Suly)Tavarez and800ETwiggs
forbothmailing/physical; preserveconflict. ActualPDFp2 uppercaseNemaillabel points
toCIVDIVJ, whileprofiletargets/otherPDFmailtoN agree. NeverimportJascontact.

All9guidepages/A–K and13profilecalendarpairs reviewed;5pagesvisual. EveryPTC
1:30pm,inperson,court22;November2026–December2027schedule preserved aspublished,
notliveavailability. UMC<=5Zoomwithoutmotion;JAWS<=15,email>15. SectionAall-dates
email remainsalongsideJAWSdirections. Allotherhearingsinperson;allpartiesmustagree
forremote,nohybrid. SmallclaimsPTC expresslyinperson. Orders7days,consult5,
silence5;binderspickup3daysorrecycled. Same-daycancel requirescall plus email/file/
service. Generalmaterials5days vs exhibitmail7/hand3/receipt3;courtesy<50pagewording
retained. MediationbeforeMSJ/disposition/final/PTC exceptdefault/uncontested/excused.

Formssection contains literalinsert-linkplaceholder;profilehasnoindividualforms.
Boundedofficialsearches foundDivisionNProcedures.pdf andA2025-023 indexedcontent,
butbothdirectoriginals404. Savedresponsebytes;nooriginalreview/currentapplicability
orassignmentdateinferredfromcachedsearch. OldS2025-014404 reused;currentcounty039
andDCM086/othercountyformsretainactualscope. NoN-specificPIPfoundonsharedindex.

Duty-pageHendersonrows agreeprofilephone/Annex/name:Dec29,2025–Jan3,2026 and
Mar15–21,2027 twiceindifferenttablecontexts. SaveHTMLtableindices0,1,4 andheaders;
lastoccurrenceprecededbyCriminalDivisionOSchedule. Do notdeduplicateawaycontext
orassignnewdivisionfromtabplacement. Remainingdutytable stillnotcomprehensively
reconciled. GenericForm2.603copyreusedwithitsactualdate,notadoptedHendersonversion.

Capture4951 `1d9fc299172ea6b273242b24934a28264f7c0a9bb17ad71063aed8ace09299a8`,
receipt `receipts/person-hillsborough-county-branden-m-henderson.json`,packet31.
131citations,16topics,13calendarpairs,12numeric/7relativeclauses,3source/14reuse;
876artifacts/204facts readback,replay/finalizedpreservationverified. NextJohnson,
exact `/Directory/Judges/Judge-Johnson`;26complete/43pending. No publication.

### Johnson: checkpoint32 / capture4953

Jennifer P.Johnson,27th current-person review: profile CountyCivilU/Protective
InjunctionsM fromJune2026,formerCountyJ2024–June2026. TaraMcCaleb,Edgecomb425/
court409,civdivu/famlawdivm. Julyguide assigns8133073536 toProtectiveM andadds
CountyU8132725258;profile/directorysinglephone8133073536 retained withscope.
Profilephonearia8132720243 differsvisible/tel. Dateddirectorysecondassignment
CircuitCriminalM conflictswithprofile/guideProtectiveM; preserveboth,noresolution.

Guide9pagesA–K,sharedUPIP3pages andProtectiveMcreation1page fullyreviewed;
9selectedpagesvisual. Twoidenticalprofileguideanchorsdeduplicated. Circuitjury
pretrialformoriginalalreadyreviewed2014-09-22 reused, retainingCircuitcaption/
signatureandunresolvedCountyUapplicability. Sixcalendarpairs2pm,inperson,court409;
CurrentlyAvailablelabelincludespastSeptember2026row,notindependentavailability.

Individualdifferences:unilateral45days (not30),JAWS<=15/email>15,UMC<=5;
SectionAalldatesemail separatelyretained. Bookingthresholdnot30minutein-person
threshold. Hybridgenerally, butProtectiveMfinal/otherhearingsexceptstatusinperson
andexplicitnoZoomunlesscourtdirects. Do nottreatstatusexceptionasautomaticZoom.
Phone13052241968,*6;meeting86234264771,noPW. Remote motioncourtesytoCountyUemail
asprinted. Interpreter-unavailablestatement specificallyCountyU,notProtectiveM.

Same-daycancelcallplusemail/file/service;orders14days,consult5,silence5;competing
Wordemail,nofurtherargument. Material5days,exhibitmail7/hand3/receipt3;binders
pickup3orrecycled. Mediationallcasesbeforetrial;smallclaimsnonjurysetafterimpasse.
GuideS2026-24numberasprinted;2026-024404 savedprior,current039supersessionseparate.

UPIPundatedformcites2013law/rules:20/30daysPTC,complete mediation90daysPTC,
telephoneconsent/goodcauseorcontestedmotion10daysORDER,notifyprogramhearing/result,
ADA2workingdaysreceipt. Keepcurrent039service-based20/45 PIPtimingdistinct.

AmendedS2026-016 originalfromofficialAOindex:setupimmediately,operationJune29,2026,
allocationbyadministrativejudgetoclerk. EntryMarch27,2026 visiblehandwrittenline,
omittedbyoriginalpypdftext. Supplementalmanualtranscriptionhasowntexthash/
extractiontimestamp andsameoriginalsourceassociation;originalextractionunchanged.
Footnotesaysamendedsolelytocorrectentrydate. OrderdoesnotnameJohnson;operation
dateisnotherexactassignmentdate. Noexhaustiveprotectiveinjunctionmeritsreview.

Guidepypdfwrongobjectoffsetwarnings6/24/27/30/51 recorded;extractioncompleted,
PyMuPDFrendered/selectedpageschecked,originalnotmodified. NoactualcourtUI/meeting.
Capture4953 `eab06e8300422069b0a001e6f574842dd36d3b5331cb2d394ec16af0533f69d3`;
receipt `receipts/person-hillsborough-county-jennifer-p-johnson.json`,packet32.
144citations,18topics,6calendarpairs,19numeric/8relative,4source/15reuse;
905artifacts/209facts readback,replay/finalizedpreservationverified.
NextMakholm `/Directory/Judges/Judge-Makholm`;27complete/42pending pluscountyfollowups.

### Makholm: checkpoint33 / capture4955

Marc S. Makholm, County Civil P: Naysha Massey, 813-272-6873,
CIVDIVP@FLJUD13.ORG, Edgecomb Room308, courtroom300. Profile, guide and dated
roster agree. Phone label/target/aria and email targets agree; footer publicinfo
is not chambers. July1,2026 guide has17 physical pages (16 substantive, number-only
page17); named nonjury template has5 pages. All text reviewed, ten selected pages
visually checked. Template cites underlying November7,2022 DCM, not its revision.

Individual requirements: JAWS<=30minutes, longer via JA; self-represented written
request to clerk. Notice Doc# and e-file within24hours booking. Materials,
memoranda, opposition and binders five BUSINESS days, not another judge's five
calendar days. Unilateral30days with >=3 coordination attempts. Orders PDF within
10days hearing/ruling; disagreement requires available transcript and clarification
motion, not routine competing Word drafts. Reserved-ruling30/60days is a court
target, not a party deadline. SET motion hearing within60days and amendment CMC
within10days filing; do not convert to hearing-held deadlines. Rule2.515 authority
accuracy applies; no additional AI-use disclosure requirement found in this guide.

Preserve conflicts without deciding: >30minute hearing in person without exceptions
inC versus agreed proposed remote order for non-evidentiary matters inM; courtroom
300 vs template PTC303; UMC5total/3per side; CMC Daily15/30 vs UMC/Daily15; monthly
first Monday vs every30days; literal Rule1.980(a)(2); DCM beyond90days unspecified
baseline and truncated next sentence. The template's 'fact expert discovery'
trigger was visually confirmed, not corrected. Joint STATEMENT14daysPTC and
signed pretrial ORDER3daysPTC remain separate. Old014/sectionI04 and2022-033
references stay distinct from current039/086. LegacyForms.aspx unavailable;
current Circuit nonjury form reused with its actual scope.

Profile exposes two PDFs, no calendar; guide's colored form references link back
to that profile. Shared PIP index hasH,I/J,K,L,M,U, noP. Bounded official searches
for final-hearing form/trial schedule located no additional named template/calendar;
this is a search limitation, not proof none exists. Duty rowSep28–Oct4,2026 agrees
contacts; only that row newly reviewed, not entire schedule. Shared originals reused.

Receipt `receipts/person-hillsborough-county-marc-s-makholm.json`, capture4955
`de56dea097d14b4727b73a5e843d274768c02149848befd487920404a89b0b75`.
180citations,23topics,28numeric/10relative timing clauses,4source/16reuse;
928artifacts/214facts read back, exact replay and finalized preservation verified.
Next exact roster `/Directory/Judges/Judge-Manning`;28complete/41pending plus
county-level tasks. Statewide goal active, no publication/finalization.

### Manning: checkpoint34 / capture4957

Daryl Manning, County Civil X: Andi Ford,813-272-0248,countycivildivx@fljud13.org,
Edgecomb320A/court309. Header and October1 directories agree. Scheduling body
sends mailed notices toSuite313. Phone aria8132762478 differs visible/tel0248;
Dec14–20,2026 duty row also gives2762478 and nameDarylM.Manning, sameJA/320A.
Preserve duty context separately. Both trial forms specify PTCcourt303.

All three HTML procedure sections and five individual forms (15PDFpages) reviewed;
ten selected pages visually checked. Portal upload guide and024response reused
by exact URL. Individual PDF links point to current Resources/Forms, matching
visible URL. Profile no dated trial calendar; shared PIP index noX-specific form.
Form1.977 attachment requirement recorded, not represented as a separately
reviewed individual template. Legacy fitz import emitted deprecation warning while
rendering succeeded; subsequent pymupdf page-count check succeeded without it.

Scheduling: <=30minutes JAWS5/15/30, >30JAphone. Opening paragraph allowsZoom<=60,
laterALL>30inperson. Preserve both. Notice prescribed Zoom/video/phone language;
Zoom2146562263,noPW,phone17866351003. Unilateral minimum60days only nonresponsive
opposing counsel; no invented attempt count. Crossnotice clears opponent AND JA.
Written cancellation email ASAP. OrdersPDF10days hearing/ruling,circulate7CALENDAR
days hearing; any self-represented party requires paper/conformingcopies/envelopes.
Contested both upload orders/cover; stipulated motion/order workflow retained.
Authority2BUSINESSdays before hearing. Earlier local AI disclosure/certification
paragraph remains alongside laterRule2.515 and AOSC26-12 prohibition/effective date;
record conflict without deciding control.024unavailable,current039replacement;
trial2022-033 references,current086 separate.

Trialcoordination email desiredmonth/allparties,JA dates/agreement; mandatory
firstday09:00trialcall on all paperwork, oldest case first. Standby parties provide
cells/returnwithin45minutes; witnesses need not attend call but ready when called.
Untried cases nexttrialperiod. Templates have120/90witness,30dispositive,21exhibits,
14jointstatement/limine/deposition,7CBC/reporter,Fridaylimine; jointpretrialORDER3
is separate. Jury adds14dayinstruction/verdict,Wordemail and juror hardcopy rules.
Nonjury authority7daysbeforetrial. Literal 'fact expert discovery' retained.
UnderlyingNov7,2022DCM date is not formrevision. Circuit pretrial forms reused
with stated scope, not converted into County rules.

Fee form: timesheets30daysORDER; costdocuments15daysspecificrequest; objections
30daysSERVICEofcompliancenotice; reply10daysRECEIPT; billedhoursstatement10days
request. Experts confer NOTMORETHAN2businessdays immediately preceding hearing.
Paragraphs2–9 before booking, limited discovery/objections, goodfaith/sanctions.
Entitlement staymotion30daysORDER AUTOMATICALLYstays deadlines iftimely; separate
entitlementhearing. Paragraph6's incorrect paragraph5cross-reference preserved.
AutoGlass-labeled waiver demands jury unless later agreed court-approved waiver;
general waiver does not. Both mediate BEFORE SCHEDULINGtrial, deny allegations,
smallclaims rules absent granted invocation, orderedPTCexcusal. General signature
'Daryl Mannning' retained as source typo, not separate identity.

Receipt `receipts/person-hillsborough-county-daryl-manning.json`, capture4957
`fc4c5b94b2e2804a9058ae710d3df9be378bf799fa11da46680c86c713d8d383`.
184citations,17topics,34numeric/8relative clauses,7source/15reuse;
959artifacts/222facts read back, exact replay/finalized preservation verified.
Next exact roster `/Directory/Judges/Judge-OBrien`;29complete/40pending pluscounty
followups. No publication/finalization; statewide goal active.

### O’Brien: checkpoint35 / capture4959

Colleen O’Brien, CountyCivilR: JobelDenney,8132725156,civdivr@fljud13.org,
Annex401N.JeffersonRoom225/court23. Header/directory agree; actualtel/mailto/aria
agree. Guide explicitly MAILING800E.TwiggsSuite225Annex; trialformPTCvenueAnnex23/
800E.Twiggs. Keep mailing/physical distinct and template venue difference explicit.
Biography2025appointment,CountyRCurrent;Y/M/Totherassignmentsundated,notassumedcurrent.
Guide9pagesA–K/fulljuryform5pages reviewed,tenvisual. HeaderNov2025 but024reference
onpage6; retain chronology, no invented revision. Current039supersedes024; old024
unavailable. Guidepage8legacyFormsURL404saved; trialformcurrentResources/Formscorrect.
Countyjury/sharedforms reused; noR-PIPonindex.

JAWS<=15,largeremail;all-datesemailsectionA retained. Unilateral45days, nofixed
attemptcount; crossnoticeonlyagreedaddition/JAclearance/amendednoticewithinallotted
slot. Materials5days,binderspickup3;courtesy<50pages,exhibitsmail7/hand3/receipt3.
Orders14days,consult5,silence5;competingWordemailnotPortal,briefreason/noadditional
argument,transcriptsallowed. Same-daycancelcallplusimmediateemail/file/service.
Hybrid generally; evidence/PTC/trial/eviction/>30inperson. SmallclaimsPTCexception
not automatic remote permission. Remote motion must state actual opponent position;
attorneysvideounlessphonepermission. Zoom8336038373,noPW,17866351003,*6.

24calendarpairs,firstsix2026rowsnotime,remaining13:45. WeekofApril16,2026 isThursday;
preserve anchor, no correctedMonday/enddate. TUESAYtypo retained. Notliveavailability.
Namedjuryform2025executionyearnotrevision;meetingtable21vsbody14visuallyconfirmed;
literal 'fact expert discovery' retained. CountyCiviljointORDER3days distinctfrom
statement14;juryWordemail/hardcopiesandcourtesyrequirementsseparate. Settlement
EACHPARTYemailsjudge,immediatelywrittennoticeCLERK800E.TwiggsRoom101;notchambers.
Two duty rows samecontacts/nameColleenE.O’Brien:Mar29–Apr4,2027mainTable1 versus
Mar8–14,2027Table4underCriminalDivisionOSchedule. Preservecontexts,nodate/assignment
resolution. Otherdutyrowsremainunreconciled.

Capture4959 `b17bbf83b572210be646d3f7f827cca1fc8f53fa76f568784b0e82f879d78083`;
receipt `receipts/person-hillsborough-county-colleen-obrien.json`,packet35.
184citations,17topics,24calendarpairs,24numeric/9relative,4source/14reuse;
987artifacts/227facts read back,exactreplay/finalizedpreservationverified.
Nextexactroster `/Directory/Judges/Judge-Saba`;30complete/39pending pluscountywork.

### Saba: checkpoint36 / capture4961

Christopher J. Saba, County Civil L: Julia D. Forgas (guide: Julia Forgas),
813-272-6806, civdivl@fljud13.org, Pat Frank Courthouse,419N.PierceSuite130H,
courtA. January2026 guide and October1 directories agree with current profile.
Phone labels/targets/aria agree. Duty Feb1–7,2027 instead names ChristopherC.Saba
and253Annex, same phone/JA, repeated in Tables1/4 with different headings; retain
both contexts without replacing current contacts or inferring a transfer date.

Guide9pages and shared DivisionL PIP3pages fully reviewed, nine visual checks.
Profile contains guide/calendar only. Guide Forms hyperlink goes to legacy
ChristopherJSaba.aspx,404 saved; shared CountyCivil forms index supplies PIPL.
Bounded official search returned guide; cached CMC-on-UMC wording differs from
current original, so it was not imported or represented as an older reviewed PDF.
Twelve PTC/trial-range pairs January–December2027, first PTCDecember17,2026;
no times published and no live-availability claim.

JAWS<=30/email>30, UMC<=5. CMCs NOT onUMC; service-extension motions ONLYUMC.
Unilateral45days with detailed efforts, no fixed attempt count. Notice immediately,
JA dates docketed only after eFiled copy. General materials5days, binderspickup3.
Courtesy PDF/Word,email<25pages,>25hardcopytabbed/indexedbinder; exactly25 unstated.
Orders10days, consultation5/silence5; competingWordemail, notPortal. Same-daycancel
callplusimmediateemail/file/service. Remote default with listed in-person exceptions,
including SMALLCLAIMSPTC and landlord/tenant FINAL eviction hearing; hybrid requires
party agreement, not categorical prohibition. Motion/goodcause/opponentposition,
copyJA AND proposedorder for remote in-person-noticed hearing. Zoom4205308406,
noPW,phone17866351003,*6;lawyersvideoabsentphonepermission. Exhibits7mail/3hand/3receipt.
Stipulated trial date must first be confirmed withJA; no date-certain JURY trial.
Allcasesmediate, smallclaims trial afterimpasse, motion/limine wording preserved.

PIPL undated, no judge named, cites2005law/rule: complaint20daysPTC, complaint-served
discovery30daysPTC, mediation COMPLETE<=90daysPTC. Telephone consent/goodcause or
contestedmotion10daysORDER; program notified hearing/result. ADA2WORKINGdaysreceipt,
old program contacts retained as form content. Request requires order-signingdate
and program availability/opponent coordination beforefax. Current039service-based
20/45timing remains separate. Page1/3 PDF annotations are only form-filling/printing
hints;2011annotation metadata is not a revision/effective date. No embedded action
executed. Old014 unavailable, current039/086 and generic county forms reused with
scope; no invented individual trialform.

Capture4961 `7e219ad8ddb09e5f6cee2456f9a9ace54498c556ed2da4dec602356066b17de3`;
receipt `receipts/person-hillsborough-county-christopher-j-saba.json`,packet36.
156citations,15topics,12calendarpairs,18numeric/9relative timing clauses,
4source/14reuse,1016artifacts/232facts read back. Exact replay and unchanged
finalized reports verified. Next `/Directory/Judges/Judge-Griner`, East County
Civil/Criminal: full civil/shared review, criminal contacts/links without exhaustive
merits.31complete/38pending pluscountyfollowups; goal remains active.

### Griner: checkpoint37 / capture4963

Jeremy R. Griner, East County CivilY, Civil TrafficW, CriminalX. AdyColon,
8132726187,ady.colon@fljud13.org,PlantCity301N.MichiganRoom2021/court1.
Published division emails eastcivdivy/w/x@fljud13.org retained literally, including
civil-looking X criminal address. Header/directory contacts and Nov23–29,2026duty
row agree; alphabetical name R.Jeremy vs other sources JeremyR preserved.
FullY14sections/Wremote/sharedXcommunications reviewed. Criminal pleaEN/ES PDFs
collected8pages,title/scopeonly,notmeritsreviewed. Their Gutman filenames do not
establish current named author. Two Scottdecorum links404 despite indexedsearch;
legacyGrinerForms404, currentprofileformsreviewed. Sharedclerkresidentialparent
reused with pendingchildreviews retained; generic address/Circuittrial forms reused.

Civil/shared PDFs34pages across11URLs,33unique (two professionalism URLs byte-identical),
20selectedpages visual. Source/URLs/retrievals remain separate despite contentreuse.
The current East order2024-0797pages fullyreviewed,enteredNov25,2024/effectiveJan1,2025
exceptearlyX2consolidation. Exactroad/countyboundarytext preserved,notzipinference.
Circuit/county civilEastfiling ifdefendant/respondentresidence,claimaccrualorproperty;
notplaintiffaddress. Wtraffic/Ycivil/Xcriminal clarified. Transfergoodcause/hearing/
convenience;disqualificationroutes,countywideemergency/reciprocalactingcoverage
retained. Supersedes2024-027,rescinds2024-009. No geocoding/legalvenue determination.

Ybooking text<=15JAWS/>30JA,table5–10UMC/15Daily/30–60JAwithapproval.16–29gap
and30boundary retained. Approval belongs30–60cell,not24hourcancellationcell.
Unilateral30days/>=3attempts/cover. CancelexceptPTC24hoursfile/email;less1BUSINESSday
mayrulepapers. Ysections5/6inperson(effectiveFeb14,2022) versussection8Zoomdefault;
WZoomdistinct. YtextmislabelsR. Remote motion10days,goodcause/opponentposition,
allpartyorder/date/time/motion/Zoom/callnumber. SampleAug20,2023notcalendar,allows
physicalalternative,omitsrequiredcallnumber. Meeting6519848351,noPW;one-tap
13052241968/19292056099. Profile hasno actualtrialcalendar.

PTCconflict fileANDemail5BUSINESSdays(exceptionunforeseeableemergency/goodcause).
OrdersONEWEEK,consultbefore,silence3days;PDFPortal/prosepaperpermittedwithTHREE
conformingcopies/envelopes/cover;competingWordemail. Authority3BUSINESSdaysmail/hand.
FinalPTCONE MONTHbeforetrial;allrequireddocsbeforetrialdate;JAmonthcoordination,
settingpartypreparesorder. HTMLjuryvoir-dire/instructions/jointstatement7beforetrial
versusnamedjuryinstructions/verdict14beforePTC,distinctsource requirements.

AutoGlasssmallclaimswaiverunderX/captionX despitecurrentcriminalX:denycomplaint,
smallclaimsrules,jurydemandunlesslateragreedapprovedwaiver,mediateBEFORESCHEDULING
trial,PTCexcusal. Do notrenameY. AmendedDCM8pagesCountycaption/titleCircuitGeneral&
Extended,2021-060/014references;projectednotfirmtrial,plaintiffsettingresponsibility,
conferral,expert>=5depositiondates,11defaultnumeric/monthperiods andblankselected
factcutoff. TrialYjury/nonjury5each references2022-033;nonjuryunderlyingNov7,2022
notrevision. BothPTCEdgecomb303/TampavsPlantCity1. Literal 'fact expert discovery'
retained;jointstatement14/order3distinct. Othertrialchecklist/timingfullysaved.

Civilcontempt2pages:judgmentFactInformationSheet45days,presentability/noncompliance,
purge20daysORDER,affidavitafterfailure,personalservice,confinement<=5daysunlesspurge/
costs,48hourhearingwarning. Separatewrit2pages:firstappearance24hoursdetention,
thenfollowingbusinessdayproduction;notifyGriner<=16:00dayafterdetentionwithinitial
weekend/holidayexception. Distinctactors/triggersretained. Garnishment1pageCircuitCA
caption/CountyJudgesignature,exemption/immediatedissolution/refund. Theseareblank
publictemplates,notcaseactions. BackslashoriginalURLsreturnedactualPDF200;preserved.

Capture4963 `e6f3c8a154d27d3081f9b6bc1d7515560ca9818a4d1320db3e120fedb58a8ed7`;
receipt `receipts/person-hillsborough-county-jeremy-r-griner.json`,packet37.
240citations,22topics,38numeric/11DCMdefaults/9relative,13source/18reuse;
1068artifacts/246facts read back, exactreplay/finalizedpreservationverified.
32complete/37pending, nextChandler `/Directory/Judges/Judge-Chandler`.
Pinnedhandoff/goalcurrent summary repaired to matchstate; older narrative stayshistorical.

### Chandler: checkpoint 38 / capture 4965

Cory L. Chandler, East Circuit R civil/family, S protective injunctions, U
probate/trust. Andrea Paxton, 813-272-6137, paxtonaw@fljud13.org (S/U guides).
Profile/R: eastcirdivr@fljud13.org. Plant City Courthouse, 301 N. Michigan Avenue,
Room 2016, Plant City FL 33563, courtroom 2. S guide instead states courtroom 4;
retain the scoped discrepancy. October 1 roster and November 2–8, 2026 duty row
agree on name, office, JA and phone. HTML phone/email/aria and PDF mailto targets
agree; profile mailto has trailing whitespace. Footer publicinfo is not chambers.
Probate AO additionally publishes eastcirdivu@fljud13.org, visually transcribed
from page 4 because native extraction splits the address.

Exact profile `/Directory/Judges/Judge-Chandler` links three undated PDFs under
`/Portals/0/Forms/pdfs/judges/JudgeChandler/`: `ChandlerDivR.pdf` (3 pages),
`ChandlerDivS.pdf` (1), `ChandlerDivU.pdf` (2). All six pages read and visually
checked. R/U JAWS <=30 minutes (UMC 7–10, Open Docket 5, dedicated 15/30);
longer hearings email JA. R offered dates are not reserved until confirmation
and receipt of e-filed notice. U hearings use R calendar, but proposed probate
orders route to U. Notices include motion filing date/index and duration.
Contested evidentiary >=30 minutes in person; CMC/uncontested <=15 may be Zoom;
R adoptions either. Other routes remain unspecified. S in person unless court
specifically authorizes Zoom; phone participation may prompt rescheduling.
Zoom93507356436/no password, four dial-ins preserved in receipt; photo ID for oath.

R/U mandatory contested-hearing authority >=3 days, exhibits >=3 days in indexed,
tabbed binder. R binders pickup within7 days/recycle; no imported U pickup period.
R cancellation requires all-party notice/agreement, immediate e-filing AND email.
Administrative email copies all, includes case number/name/matter/duration;
substantive litigation by email prohibited. R family financial affidavits5 days
before relevant trial; one agreed/disputed-color Excel ED worksheet, no invented
ED deadline. R first-CMC continuance email >=2 BUSINESS days, reasons/joint signed
agreement/order, family-specific prerequisites; JA supplies agreed date within60
days original. These conditions are not asserted universally commercial. Same
scope caution for R's broadly worded ALL postjudgment magistrate referral with
motion. Agreed orders PDF Portal; competing/nonagreed Word email, wait both drafts;
attorney serves pro se/mails if no email. Preserve literal Incoming Withholding.

U paperless: death certificate and PR/resident-agent papers may be e-filed;
ALL proposed orders Portal U, no hardcopies. File prerequisites, WAIT3 BUSINESS
days for docketing before upload. Hearing-result orders state hearing date and
must not upload MORE THAN2 days BEFORE hearing: earliest-upload restriction,
not a two-day advance deadline. Show-cause response >=5 BUSINESS days including
extension papers; late filings do not cancel hearing. Mediation before >=2-hour
hearing. Formal/summary petitions: death <2 years before filing requires paid
funeral bill/proof; intestate affidavit heirs; pro se signatures notarized.

Material shared originals from the AO index now fully reviewed:

- `probate-ao-s-2024-013`: 11 pages, entered January22,2024/effective March1,2024,
  supersedes2021-078. Probate domicile/East assignment, independent torts to Civil,
  transfer/consolidation and jury rights, property descriptions/confidentiality,
  counsel/resident-agent substitution. Hearing notices particularity/time/copy JA;
  cross-notice court capacity AND agreement; cancellation/JAWS; party reporter;
  papers5 days before, authority AT hearing. Emergency48 hours ACTUAL notice unless
  all agree; physical absence and fallback chain. Order consult5 DAYS/submission10
  DAYS decision, silence5 BUSINESS days, cover/copies; represented Portal versus
  selfrepresented/excused-service hardcopies. Adversary CMC60 days commencement;
  military forms; discovery no-response/no-extension/no-goodcause-opposition plus
  conferral, compliance10 days SIGNING if court orders; trial-setting certificate.
- `trust-ao-s-2024-017`: 5 pages, same entry/effective dates, supersedes2021-076.
  Ch736 and trustee business/residence routing; nonCh736 trustee actions to Civil;
  transfer/consolidation/jury-right conditions, disqualification/emergency chain.
  Does NOT state probate order's48-hour emergency threshold; do not import it.
- `probate-ao-s-2022-020`: 5 physical pages, three order plus two oaths. Entered
  September23,2022/effectiveOctober3,2022, supersedes2010-014. Dated Cadigan/Neaves
  appointments, no current roster conclusion. Written referral objection10 days
  SERVICE; inventory/account/plan review on judge request without referral; other
  matters referral, party may schedule; reports and recording/custody. Oaths
  July28,2003 and February4,2010 visually read, distinct from order dates.

Retain conflicts: U ALL-Portal versus probate AO hardcopies; individual authority
3-days-before versus AO at-hearing; probate/trust all-East-disqualified routes
Tampa A OR B versus East2024-079 A. Preserve all statements without resolution.
Manual visual transcriptions have separate hashes and source linkage; native
extraction retained. No inferred amendment or current appointment from old text.

The shared Forms index's Probate section links two distinct four-page forms,
fully read/visually checked: `probate-uniform-setting` revisedMay1,2008 and
`probate-uniform-pretrial` revisedNovember21,2008. Both captionA/Tampa; not relabeled
as current individualized U orders. Setting form: witness90/70 daysPTC, expert
reports/answers/summary, counselmeeting7, signedjointorder3, motionsfile/hearPTC
exceptlimine, discovery15 beforetrial, mediation/arbitrationbeforePTCunlesswaived,
settlementauthority/wholetrialavailability, immediate settlement notice/dismissal
stipulation/finaldisposition, CBC/reporter7 beforePTC, pro se/sanctions. Pretrial
form: required issues/witnesses/damages/evidence/stipulations/motions/ADA/interpreter,
exhibitattachments regardless prior filing, confer/initial agreedexhibits, CBC
contact AND technologychecklist7 beforePTC. Stray2/omitted21 numbering confirmed
on original pages; blankdates and outdated equipment examples not availability.
Shared military forms and civil/East/DCM/Portal/access sources reused at recorded
review depth. Bar guidelines reuse is explicitly partial in this receipt.

One acquisition-inspection serialization failed on PyMuPDF Rect, after rendering;
fixed by saving coordinates as lists. No original acquisition failed. No browser,
JAWS, Portal, phone/email or Zoom interaction performed.

Capture4965 `0fc21ac1dce2f3f95e305262d60be3cf5da3dff3cd3a5ac4fc8a3daa47e34a28`;
receipt `receipts/person-hillsborough-circuit-cory-l-chandler.json`, packet38.
178 nested citations,22 checklist topics,29 numeric/10 relative timing rules,
10 new source reviews/13 reused;35 PDF pages reviewed,25 visually checked.
1129 artifacts/257 findings read back, exact replay and finalized-report preservation
verified. Independent counts/state/visual consistency check passed.33complete,
36pending, next exact roster `/Directory/Judges/Judge-Moody` (not acquired yet).
County clerk/access/officers/material orders including current court reporting,
duty reconciliation and unavailable-source followups remain; no publication.

### Moody: checkpoint 39 / capture 4967

James S. Moody, III (profile omits middle initial), Tracie Wingate,8132726432,
wingattm@fljud13.org in V/W guides; profile/T eastdivt@fljud13.org. Plant City
301 N.MichiganRoom2011/court4. All HTML/PDF contact and Zoom targets agree.
Profile W says probate/guardianship/mentalhealth; dated directory and East079
say probate/trust. Retain source descriptions without deciding assignments.
Division roster marks administrative judge. DutyApril5–11,2027 appears in tables1
and4 under different page contexts; both retained, not inferred2026 duty.

Exact profile links `ProceduresDivT_Moody.pdf`(2pages), `ProceduresDivV_Moody.pdf`
(1), `ProceduresDivW_Moody.pdf`(2) under `/Portals/0/Forms/pdfs/judges/`.
All5pages fullyread/visual. No stated revisions, actualtrialcalendar or separate
namedforms located. Do not treat search-engine age as document revision.
T/W JAWS<=30(UMC7–10/Open5/15/30),>30emailJA. WchecksTcalendarfirst,then emails
JA to REQUESTbooking after agreement; emailnotice/copyopponents. OrdersPortalW.
Evidence>=30inperson,CMC/uncontested<=15mayZoom,Tadoptions either; gapsretained.
Vcourt4inperson unlessspecificZoomdirection; phone mayreschedule. Zoom2575039244,
noPW,fourdial-ins/photoID/loginnonotice saved. Woriginalpage1 has visualoverlap
atphotoIDsentence; nativeextraction retained separately, original not repaired.

Tmaterials SHOULD5daysbeforehearing (paragraph includestrial); Wauthoritymandatory3,
exhibits3withindexedtabbedbinder. Neitherpublishesbinderpickupdeadline. Do not
copyChandler3dayT-equivalent or7daypickup. Tfamilyaffidavits5days,EDoneExcel/colors/
conferral,noEDnumericdeadline. Tcancelallpartyagreement/notice,immediateefileAND
email. CMCcontinuance2BUSINESSdays withfamilyconditions,jointagreement/order,
JAdateagreed/within60original. Do notimposefamilyprerequisitescommercially.
TALLpostjudgmentreferralwithmotion scopeambiguity retained. AgreedPDFPortal,
nonagreed/competingWORDemail,forwardwhenboth;attorneyservesprose/mailsnoemail.

WpaperlessALLordersPortalW,prerequisitesfirst/WAIT3BUSINESSdaysfordocketing;
showcause5BUSINESSdays includingextensionpapers,latefilingdoesnotcancel.
Mediationbefore>=2hourhearing. Hearingorderdateopeningparagraph,notMOREthan2days
BEFORE=earliestuploadrestriction. Funeralproofifdeath<2years,heirsifintestate,
prosenotarization. Sharedprobate013/trust017/magistrates020/probateforms and
Civil/East/DCM/Portal/access/military/professional sources reused at actualdepth.
Samehardcopy/Portal,authoritytiming,disqualification,oldA/Tampaformconflictsretained.
Shared checklist references only Chandler's shared-source topics, not hisR/S/U rules.

Reuse selection improved: choose latest saved finding for identical raw/text hashes,
notfirst receiptmatch. ThisuseslaterfullBartrialguidelinesreview, preservingolder
partialreviewreceipts. `review/moody-reuse-selection.json` records18 selections.
Capture4967 `137a0c6e49651c1b7d485e0495a8d4b203902ec8a6dc2f9f675134f111b063d4`;
receipt `receipts/person-hillsborough-circuit-james-s-moody-iii.json`,packet39.
157citations,18topics,10numeric6relative,5newsource18reuse;1152artifacts263facts
readback,exactreplay/finalizedpreservationpassed.34complete/35pending.
Next exact saved roster `/Directory/Judges/Judge-Williams`.

### Williams: checkpoint 40 / capture 4969

Michael S. Williams, East O probate/trust, P civil/unifiedfamily, Q protective.
JanellBrown,8132721003,snelljd@fljud13.org; PlantCity301N.MichiganRoom2006/court3.
PvisibleemailEastCirDivP@fljud13.org. Profile/October1directories/April19–25,2027
duty agree. Preserve discrepancies: profilephone/tel1003 butaria5105; Ppage2
cancellationvisibleEastCirDivP butembeddedmailtoEastDivP; QvisibleJanell/`snelljd@fljud13.org` butembeddedmailto `wingattm@fljud13.org`
(MoodyJA). Independentprofile/Oguide support snelljd. Do notreplacevisiblecontact
withmismatchedtarget orsendtestmessage. Ppage1alsohasmisalignedduplicateemail
annotation; derivedrectangles/text retained. Qguidecourt4 versusprofile/O/Pcourt3.

Exact profile links `/Portals/0/Forms/pdfs/judges/ProceduresDivO_Williams.pdf`(2),
`ProceduresDivP_Williams.pdf`(2), `ProceduresDivQ_Williams.pdf`(1). All5pagesread/
visual; no statedrevisions/actualcalendar/additionalnamedforms located. Webopen
reported inaccessible, but directofficialHTTPprofile/allPDFs200; sourceoriginals
saved. This was a web-tool limitation, not missing original evidence.

P/O booking<=30JAWS(UMC7–10/Open5/15/30),>30JA. O usesPcalendar,checkfirst,agree/
emailJA/copyopponents, emailnotice. OrdersPortalO. Remote thresholdsDIFFERfrom
Moody/Chandler: contestedevidence>=45inperson,matters<=30mayZoomunlessotherwise;
emergenciesgenerallyinperson,P adoptions either.31–44andotherunaddressedroutes
notinvented. Zoom81062935489,noPW,fourdialins/noticelogin/photoID saved. Qonly
court-specificZoompermission,phonecanreschedule,otherwisecourt4inperson.

Pmaterials SHOULD5daysbeforehearing (paragraphalsoincludestrial); Oauthority
mandatory3before,exhibits3/indexedtabbedbinder. Noindividualbinderpickupperiod.
Pfamilyaffidavits5daysbeforetrial;singleExcelED/agreed-disputedcolors,conferfirst,
noEDnumericperiod. Cancellationallpartyagreement/notice,immediateefileANDemail.
PfirstCMCcontinuance2BUSINESSdays,emailJA,reasons/jointsignedagreement/order,
family-specificprerequisites; JAdatebothclear/within60original. BroadALLpostjudgment
referralwithmotion scopeambiguity retained,notimposedcommercially. Pordersagreed
PDFPortal,nonagreed/competingWORDemail,forwardonceboth;prosecopies/mailifnoemail.
WilliamsactuallysaysIncome Withholding (notMoodyIncoming).

OALLPortal/nohardcopies,deathcertificate/PRpapersmaye-file. Prerequisitesfirst,
WAIT3BUSINESSdocketing;showcause5BUSINESSincltimeextension,latepapersdonotcancel;
mediationbefore>=2hourhearing. Hearingorderdateopeningparagraph/notMOREthan2days
BEFORE=earliestuploadrestriction,notdeadline. Funeralproofdeath<2years,intestate
heirs/prosenotarization.18sharedsources reused atlatestmatchingraw/texthashes;
sharedprobate/Civil/East conflicts and2008A/Tampaforms preserved. Sharedchecklist
references exclude Chandler's individualR/S/U requirements.

Duty surname candidate search also found JA KathyWilliams underJudgeRice. Saved
candidate rows and exclusions; only exactjudgecolumnMichaelS.Williams selected,
tables1/4April19–25,2027. Do notturnJA-surname match intojudgeduty. PDFcontacttarget
extractions haveindependenttexthashes/sourceURL/retrieval/derivationtimes; originals
andnativeextractionsretained. Noactualcommunication/filing/JAWS/Portal/Zoom/UIcheck.

Capture4969 `35819dc18e874a67cb38bf7952730b02a75664c0ddf386e0d42ba5364d55c2cc`;
receipt `receipts/person-hillsborough-circuit-michael-s-williams.json`,packet40.
162citations,17topics,10numeric6relative,5newsource18reuse;1177artifacts269facts
readback,exactreplay/finalizedpreservationpassed.35complete/34pending.
Next exact roster `/Directory/Judges/Judge-Catlin`, not acquired yet.

## Catlin checkpoint — capture4971 / packet41

Catherine M. Catlin is complete: Division A probate, guardianship, mental health
and trust; Jackie Morgan,813-272-5211,probatedivisiona@fljud13.org; Edgecomb,
800 Twiggs Street,Room445,Tampa33602,courtroom415. The directory address header
adds E.Twiggs. Profile visible/tel/aria and mailto contacts agree. Preserve the
historical January12–18,2026 duty row and biography dates separately.

The complete individual procedure is in two HTML sections. Required papers must
be docketed before orders, with a3-business-day wait. Show-cause responses and
hearing authority/exhibits use5 BUSINESS days; indexed/tabbed exhibit binders,
authority hand-delivered or mailed. Incapacity reporter notice is3 BUSINESS days;
the cancellation condition says failure to notify AND failure to provide, not
one or the other. Formal-administration notarization is limited to pro se
petitions; summary-administration text covers all signatures. Settlement papers
attach closing documents, with requested confidentiality routed to JA for in-camera
review. Minor-settlement approval without a hearing has express/nonexclusive
conditions. Mediation is required before hearings of2 hours or more. Orders all
PDF/Portal ProbateA; earliest upload is not more than2 days before the hearing,
not a two-day advance filing deadline. No public actual calendar dates were
available; JAWS requires login and was not accessed.

New substantive shared reviews: guardianship S-2026-008,17pages; court-reporting
S-2024-043,11pages; probate constructive-service affidavit,4pages. All32 pages of
text reviewed;19 selected original pages visually checked. Catlin's five-page
Portal guide URL without query is byte-identical to the previously reviewed
shared URL; reused review is distinguished from newly read pages. Guardianship
order entry February12,2026 was visually transcribed, effective March2. Reporting
order effectiveMay13,2024; handwritten entry day remains uncertain after page/crop
review. Do not invent that day.

Conflicts retained: reporter coverage, conditional settlement hearings, all-Portal
versus selfrepresented/excused-service paper orders, authority before versus at
hearing, initial report period versus60-day/no-early-filing clauses. No authority
resolution was attempted. The guardianship order separately preserves60-day CMC,
48-hour emergency/GAL-report conditions,5-day order consultation,10-day submission,
5-business-day silence certification,fee/report/death requirements and exceptions.

The court-reporting operational page was fully read and its routing table/anchors
saved. Displayed office8133073597 differs from header tel8132725368; FAQ tel agrees
with3597. Header splits digital appellate/writ requests to eScribers from RTI;
FAQ blanket routing differs. RTI Suite170 versus1230 also differs. None is silently
corrected or imported as a judge's contact. Old service division labels do not
update the roster. Audio request page is a separate remaining access review.

The official Guardianship Case Management page is under Court Services → Court
Programs → Guardianship Case Management. Full page and anchor inventory saved in
`review/catlin-gcm-extraction.json`; section Forms supplies reporting forms and four
simplified-plan variants absent from the generic Forms index. Court authorization
for simplified plans is distinct from automatic simplified-accounting eligibility.
Child URLs are only inventoried, not marked collected/reviewed. Later agents should
follow the exact Guide to Filing Reports and accounting-form links for the county
followup, without importing private guardian/attorney lists as court personnel.
Past class dates labelled Friday conflict with their numeric2026 weekdays; preserve
both, do not shift dates or advertise them as current availability.

One-shot assembly `review/complete-catlin.py` must not be rerun. An initial assembly
index error occurred before receipt/packet writes; source-to-topic assertions were
added and the successful save independently validated. Receipt contains24 topics,
30 numeric and12 relative requirements,8 source reviews and11 latest same-byte
shared reviews.168 citations validated;1,230 artifacts and278 facts read back;
exact replay and unchanged finalized reports confirmed. County remains incomplete,
unpublished. Next exact saved roster URL is
`https://www.fljud13.org/Directory/Judges/Judge-Tesche-Arkin`.

## Tesche Arkin checkpoint — capture4973 / packet42

Caroline Tesche Arkin is complete, probate/guardianship/mental health/trust B and
risk protection N. Susan DiLoreto,813-272-8550,probatedivisionb@fljud13.org;
N rpodivn@fljud13.org;Edgecomb800E.Twiggs Room442,Tampa33602,court417. Visible,
tel,aria and mailto agree. Four individual HTML procedure sections fully reviewed.
No stated revision or public calendar dates; saved duty page has no Tesche/Arkin
match. Current Forms index supplies no additional named form.

Do not copy Catlin's requirements. B authority and indexed/tabbed exhibit binders
use3 DAYS; email authority permitted with case number,name,hearingdate. Hearing-result
orders must not be uploaded BEFORE hearing. Hearings>=onehour are JA-set/inperson;
JAWS lists15/30/45 and named UMC/settlement slots. File notice then email courtesy
copy; notice identifies appearance method. General emergency hearings inperson;
Zoom login at least5minutes early,photoID/actualname,last-resort telephone only
after failed connection attempts. Mediation before>=2hour hearings.

B show-cause responses due5 BUSINESS days before, then source explicitly says late
filings WILL result in cancellation. Original HTML markup was checked and saved;
there is no NOT. Preserve that wording/apparent tension; do not silently repair it
from Catlin or advertise late filing as a reliable way to obtain cancellation.
B ALLPortal wording also coexists with ONEemail of competing Word orders; section3
expressly references Civil046 paragraph13. Preserve actual scope, not inferred
wholesale CivilDCM application. Formal and summary sections both limit notarization
to pro se petitions (summary source spells prose). No Catlin all-signature rule.

Official AO index supplies risk-protection S-2026-007,2pages fully read and visually
checked. Entered/effective immediately February12,2026,handwritten date separately
transcribed;supersedes2020-048. N assignment/designated probate alternate,law
enforcement service,temporaryexparte hearing filingday or nextBUSINESSday inperson
ORtelephone,final hearing HELD<=14days after setting order ENTERED. Generalprofile
emergency-inperson vsN telephone option preserved. No substantive firearms-law
expansion. Printed section numbers skip6; no invented requirement.

Search also returned an old DivisionI temporaryreliefPDF naming a different JA;
directofficial request returned404. Original404response retained,document content
not collected/reviewed,not imported into current B/N. This is a historical lower
priority lead, not a missing current individual procedure. Shared008/043 and other
latest packet41 facts reused; GCM child forms still only inventoried.

Receipt has12 topics,8numeric/7relative requirements,2source reviews and17shared
reviews.128 citations validated;1,250 artifacts/281facts read back,exact replay and
unchanged finalized reports confirmed. No browserUI claim or publication.
Next exact roster `https://www.fljud13.org/Directory/Judges/Judge-Scionti`.
Check civil mental-health/shared responsibilities while retaining full contacts,
assignments and links; do not expand into exhaustive drug/criminal manuals.

## Scionti checkpoint — capture4975 / packet43

Michael J. Scionti is complete. Erin Potter (guide Erin M. Potter),Annex401N.Jefferson
Room515,Tampa33602. Main/M/W8133013825;V8133074475. EmailsMentalHealthDivM,
FelonyDivV,FelonyDivW @fljud13.org match actual targets. Profile/guidecourt52 versus
dateddirectories52A. Profile phone/tel3825 versus aria8132725105;March30–Apr5,2026
duty3825 versusJuly26–Aug1,2027duty5105 (tables1/4 kept separately). Do not collapse
that dated/scoped contact evidence into one unqualified value.

Civil Mental Health M under probate is distinct from criminalM treatmentcourt.
The June1,2025 individual guide describes criminalM/V/W,not automatic civilM
requirements. All5pages read/visuallychecked for office/sharedprocedure,including
3BUSINESSday generalmaterials versus2BUSINESSday authority,5BUSINESSday continuance
and posthearingorders,3BUSINESSday Zoomrequest withapproval-onlycredentials. Exhibits
Portal and paper/at-hearing directions coexist. Emaildivision/copyall exceptlawful
exparte,notice/cancellation immediate,ADA/interpretercontacts retained. Program
manuals,handbooks and2026calendars are linked but notcollected/reviewed. Vprofile
AdministrativeOrder is plain text without href;officialindex supplies2016-032URL,
retained without merits review. W2026-002 link retained. No militarybio download.

Civil/shared S-2021-0746pages fullyread (4visual),enteredDecember10,2021,effective
January1,2022. All393 assignedM versus newer008393.12advocacyA/B is recorded without
resolution. Counselroutes,disqualification and emergency-substitution chains saved;
physicallyabsent differs frombusyhearing. Its oldcopylist SciontiDrugZ is historical.
Bakerhearing S-2021-0274pages fullyread (2visual),entered/effectiveMay10,2021;90day
facilityclassification notice,host/transport/location andcourthouse-relocation
requirements retained.2021facilitycorporatenames are notassertedcurrent identities.
CriminalM S-2023-0465pages collected,onlypages1/5scope/dates readandvisuallychecked;
enteredSeptember19,2023,effectiveOctober1. Pages2–4 intentionallyunreviewed under
commercial-civilpriority. Allthree handwrittenentrydates have separatelyhashed
visualtranscriptions;nativeextracts retained.

Receipt14topics,6numeric/5relative,5sources and6latestsharedreviews.123citations,
1291artifacts and287facts validated/readback;exactreplay andunchangedfinalizedreports
confirmed.15pages in fullyrevieweddocuments plus2selectedpages inpartialdocument;
13uniqueoriginalpages visuallychecked. The first link-inspection JSON serialization
failed on a PyMuPDF Rect; extraction was repaired with explicit coordinate arrays.
A citation-end-marker error was corrected before receipt/packetwrites. No source
lost or review scope broadened to mask either error. County remains unpublished.
Next exactroster `https://www.fljud13.org/Directory/Judges/Judge-Fernandez`;roster
categories include bothcivil/criminal,so verify actualcurrentresponsibilities.

## Fernandez checkpoint — capture4977 / packet44

Kimberly K. Fernandez: Susan Tellefsen,813-272-6879,felonydivb@fljud13.org;
South Annex,401 N.Jefferson,Room540,Tampa33602,court55S. Profile visible/tel/aria
and mailto agree; dated directories and February16–22,2026 duty row agree.
Criminal B and specialty civil Jimmy Ryce T are confirmed. Civil046 page2 assigns
394.914 commitment petitions toT and references specialized civil rules. Do not
infer an ordinary commercial docket or universal CivilDCM application.

Both profile procedure links were followed. First contains backslashes: preserve
that original href and explicitly normalize separators for HTTP. Second contains
spaces: preserve original and percent-encode. Both returned8-page PDFs stating
June24,2026 revision, despite a search excerpt displaying February27. Full text
of the first was read; all8 pages of the second have identical whitespace-normalized
PyMuPDF text. Raw hashes differ. Rendered pages2–8 match exactly; page1 of the
second has missing/overlapping glyphs. pypdf reported invalid object-offset warnings
for7,13,17,30,33,36,72; retain that evidence. The first guide's legible page1 and
both originals supply review evidence, not a claim of zero warnings. ADA annotation
in first ends#ADA,second does not; remaining external destinations agree. Full
annotation dictionaries also differ in internal IDs. Comparison and renders saved.

Shared office checklist preserves all materials5 BUSINESS days, courtesy copies
3 BUSINESS days, exhibits3 DAYS; continuance5 DAYS; orders24 HOURS after hearing
or emailed court request. Portal only agreed orders; no competing-order route
invented. Emergency motion filed AND emailed. Notice/cancellation immediate.
Motions Zoom only all-party agreement; no numeric appearance threshold supplied.
Paper exhibits and emailed copies coexist. Criminal trial/substitution/access
language is scoped; plea/competency/bond paragraphs remain in originals without
expanded criminal or commitment merits research. No additional named form/current
actual calendar located. Current ADA/interpreter/shared rules reused.

Receipt10 topics,5 numeric/5 relative,3 source reviews and7 reused reviews.
86 citations validated;1321 artifacts and291 facts read back; exact replay and
unchanged finalized reports verified.16 physical pages across URLs,8 distinct
normalized-content pages;7 images directly visually checked (guide1 pages1–6,
guide2 page1). Next exact roster: `/Directory/Judges/Judge-Alvarez`.

## Alvarez checkpoint — capture4979 / packet45

Lindsay M. Alvarez, criminal F: Tracy Lugo,813-272-0242,tracy.lugo@fljud13.org;
procedures use felonydivf@fljud13.org. South Annex,401 North Jefferson Street,
Room506,Tampa33602,court54S. Current header and October1 directories agree;
visible phone,tel,aria and email targets agree. The profile's biography instead
explicitly names Lisa A. Allen. Exclude that entire biography from Alvarez fields;
preserve its original and attribution discrepancy. Current Alvarez contact and
F procedure association is independently supported, not inferred from that biography.

Duty candidates were filtered by exact given name. February2–8,2026 lists Alicia
Webb,813-307-3432; May31–June6,2027 lists Tracy Lugo,813-272-0242 in tables1/4.
Preserve the older contacts and duplicate contexts without inventing a transfer
date. Nina M. Alvarez's November2027/TBD row is another person, excluded. Search
also surfaced magistrate/hearing-officer pages with generic Judge Alvarez titles
but different named body content. Those are separate officer-review leads, not
Lindsay Alvarez sources; later officer reviews must verify body identity.

The20-section individual HTML procedure was read; structured review is limited to
shared office/hearing/access matters. Zoom link/display3777074721 differs from
trailing meeting85650928941 in the dial-in text. No call or correction attempted.
Non-evidentiary motions<=10minutes/no witnesses:Tuesday/Thursday8:30AM non-trial
weeks,8AM trial weeks,Zoom unless in-person requested. File motion before date
request; email motion/case details,obtain JA options,confer/agree,confirm JA; notice
to court/opponents includes Zoom. Nonmovant contested response/authority>=7DAYS.
Exhibit notice and sequentially numbered exhibits filed when motion filed. Counsel
substitution/withdrawal FILED AND HEARD>=7DAYS before pretrial,not merely set.
Broad Zoom direction coexists with in-person pretrial requirements. No general
proposed-order deadline or independent courtesy-copy period invented from specific
criminal motion paragraphs. Plea/waiver/DNA/fingerprint links inventoried only;
no child-form downloads or exhaustive criminal merits analysis.

Receipt8 topics,2 numeric/4 relative,1 new source review and4 reused reviews.
72 citations validated;1334 artifacts and293 facts read back,exact replay and
unchanged finalized reports verified. No PDF or browser UI review claimed for this
judge. Next exact roster `/Directory/Judges/Judge-Green`. Current county remains
incomplete and unpublished. This turn completed Scionti4975,Fernandez4977 and
Alvarez4979 sequentially while preserving prior evidence and finalized reports.

## Green checkpoint — capture4981 / packet46

G. Gregory Green,criminal D: Jackie Scott,813-272-6875,FelonyDivD@fljud13.org;
Annex401N.Jefferson,Room228,Tampa33602,court16. Header,November17,2025 guide,
October1 directories and May11–17,2026/October11–17,2027 duty rows agree.
HTML visible/tel/aria/email and PDF email/Zoom targets agree. Biography reverses
name to Gregory G. Green and states family E January2021; preserve those statements
separately without treating the old family assignment as current civil duties.

All6 guide pages read and visually checked,structured analysis limited to shared
office/access. Email hearing coordination; immediate notice with ADA language;
immediate JA cancellation and filed/served notice. Short motions strictly less
than10minutes generally second docket week8:30AM; exactly10 unspecified. No actual
calendar dates found. All materials3BUSINESSdays before vs courtesy materials2DAYS;
retain both. Continuance5DAYS before,remote filed AND emailed3DAYS before,orders
5DAYS after. PDF/Portal with cover agreement/disagreement and disputed marked-up
Word/email both retained. Remote requires good cause despite hybrid wording;
pretrial defendant personal presence separately stated. Emergency detailed motion,
court determination/unilateral setting; no extra timing requirement invented.

Probation decision2–3WEEKS is a court estimate,not party deadline. No status call/
email before3WEEKS after filing is separately scoped; no generic response deadline.
Probation forms homepage remains link-only. Exact legacy interpreter URL reuses
prior404 observation; current interpreter page reused. Criminal merits are not
exhaustively analyzed. PDF link extraction and original source hashes retained.

Receipt10 topics,6 numeric/3 relative requirements,2 new sources,4 reused reviews.
73 citations validated;1357 artifacts/296 facts read back; exact replay and unchanged
finalized reports verified. Next exact roster `/Directory/Judges/Judge-Kiser`.
County incomplete and unpublished. Supporting one-shot scripts are not to be rerun.

## Kiser checkpoint — capture4983 / packet47

Mark D. Kiser,criminal E: Yarimar Ayala,813-272-6851,FelonyDivE@fljud13.org;
Annex401N.Jefferson,Room616,Tampa33602,court61. Profile,August25,2026 guide and
October1 directories agree;alphabetical label Criminal Justice & Trial E retained.
April27–May3,2026 duty instead lists8132762099/428Edgecomb;August23–29,2027
rows in tables1/4 match current contacts. No inferred move/transfer date.

Six-page guide text and images checked. For2026:three docket weeks then two
consecutive one-week jury dockets;Tuesday8:30AM pretrial second docket week,
Monday8:30AM trial starts,short motions<10minutes generally second docket week9AM.
January2027 onward:two docket weeks/two-week trial period,ready either week;
trial order set pretrial or subsequent scheduling hearing. Monthprecision stays
monthprecision:do not invent January1 or concrete trial dates. Preserve2026 details
without assuming every sub-detail explicitly applies after the cycle change.

Email coordination;notice includes motion,date,duration,appearance andADA,immediate
file/service;immediate cancellation JA/file/service. All materials3BUSINESSdays
before vs courtesy case law/reference2DAYS;continuance3DAYS before (not Green5),
remote filedANDemailed3DAYS before,orders5DAYS after. PDF/Portal coveragreement/
disagreement plus disputed marked-upWord/email both retained. Goodcause for remote
and personal pretrial participation preserved. Criminal emergency/trial/limited
statuscontact directions reviewed;no exhaustive criminal merits analysis. Probation
2–3weekdecision estimate separate from no-status-call3weeksafterfiling.

HTMLphone/tel/aria agree,emailcase-only,Zoom6676413743sameID asguide;leadinghref
whitespace and fljud13-org.zoom.us versus printedzoom.us preserved. PDF blue
underlined external URLs have no external annotations;onlyTOC internal targets.
Do not equate visual styling with a verified clickable destination. Profile's four
criminal forms andPublicDefenderprobationhomepage link-only. Legacyinterpreter404
reused,currentalternative reviewed. No browserUI or actual remoteaccess tested.

Receipt10topics,6numeric/3relative,2new sources/4reused;76citations validated.
1380artifacts/299facts readback,exactreplay,finalizedreportsunchanged verified.
Next exact `/Directory/Judges/Judge-Lefler`. County incomplete/unpublished.

## Lefler checkpoint — capture4985 / packet48

Lawrence M. Lefler, criminal C: Maya DelConte,813-272-5450,
maya.delconte@fljud13.org; Annex401N.Jefferson,Room226,Tampa33602,court14.
Guide directs visitors to enter at Edgecomb800E.Twiggs,Tampa33602. Keep entry,
mailing and courtroom distinct. Profile visible/tel5450 versus aria6855; March2–8,
2026 duty6855; June28–July4,2027 table1/4 duty5450. Currentguide/roster5450.
Page4 repeats Maya.delconte@fljud13.org@fljud13.org twice: preserve literal defect,
exclude from contact field; single-domain contact independently verified.

Directly downloaded guide is4pages,August21,2026. Search excerpt at sameURL
instead describesJune23,2025/7139/olderremote-sectioncontents. It is a discovery
lead, not an archived original or verified historical version. Do not import those
old contacts or remote procedures. All4 currentpages text and images checked.
Current guide has no remote/Zoom protocol or specific continuance deadline.

Two docketweeks then two-weekjury docket;all8:30AM,pretrialTue/Wed firstdocketweek,
trialsMonday,arraignmentsMondaydocketweeks. Shortmotions strictly<15minutes;
emailJA beforebooking,copyparties;immediateADA notice/cancellation. Motions FILED
AND HEARD beforepretrial unlesscourtgoodcause;criminal sanctions language scoped.
Allmaterials/exhibits3BUSINESSdays versus courtesycaseauthority3DAYS;orders
5BUSINESSdays afterhearing. Stipulation in title/body; disputedcoverletter plus
marked-upWord emailed;PDFPortal. Exhibits single-sidedpaperclerk,advancechambers
receipt andcopiesathearing. Emergency motion/courtfinding/unilateralsetting.

Short probationcalendar retained:Sep30,Oct28,Nov19,Dec17,2026 at9AM. If filing
<10BUSINESSdays fromhearing choosefollowingmonth;courtmaystrikehearing after
responses if grantingwithouthearing. Not booked slots or a recurringweekday rule.
Profile probationform andPDhomepage remain links only. ADA/interpreter sources
reused;legacyinterpreter404 observation retained. No exhaustivecriminalmerits review.

10topics,5numeric/4relative,4calendarrows,2new/4reusedsources;82citations validated.
1401artifacts/302facts readback,exactreplay,finalizedreports unchanged verified.
Next `/Directory/Judges/Judge-Nazaretian`. County incomplete and unpublished.

## Nazaretian checkpoint — capture4987 / packet49

Nick Nazaretian,criminal G: Kortina Jones,813-272-7139,FelonyDivG@fljud13.org;
Annex401N.Jefferson,Room132,Tampa33602,court19. Guide entrance is Edgecomb800E.Twiggs,
separate from chambers/mailing. Profile,guide,dateddirectories agree. June1–7,2026
duty132Annex;September27–October3,2027 table1/4 Nicholas “Nick” Nazaretian*/132Edgecomb,
samephone/JA. Preserve explicit alias and buildingdifference without inferred move.

Direct guide6pages January23,2026;text andall6images checked. Searchexcerpt says
January5,2026;not a retainedhistoricaloriginal. Communications emailcase/name/matter,
copyall exceptlawful exparte;immediateADA notice,cancellation. Docket phrase literally
“back to back two week jury trial dockets” after two docketweeks;retain rather than
computetotalcycle. Tuesday9AM pretrials firsttwo weeks,Monday8:30AMtrials generally
followpretrialTuesdayorder. No actualcalendar dates orshortmotionthreshold found.

Allmaterials3BUSINESSdays,courtesy2DAYS,exhibits3DAYS before. Exhibits viaPortal AND
single-sidedpaperclerk/copiesathearing;party-specificnumeric/alphabeticlabels retained.
Continuance5DAYSbefore;orders5DAYSafter,PDFPortal plusALLcoveragreement/disagreement,
stipulationtitle/body anddisputedmarked-upWordemail. Remotegoodcause/Zoom2669029219
but no numericrequestdeadline;personalpretrialparticipation separately stated.
Emergency detailedmotion/courtfinding/unilateralsetting. Probation2–3weekcourt
estimate separate from no-statuscall/email3weeksafterfiling. Criminalmerits notexpanded.

COVEauthorizationPDF andPDprobationhomepage remain links only. ADA/interpreter
reviews reused,priorlegacyinterpreter404/currentalternative retained. OriginalHTML
phone/mailto/Zoom agree;phoneariaabsent,not fabricated. PDFtargetchecks retained.
10topics,6numeric/3relative,2new/4reusedsources;79citations validated.1424artifacts/
305facts readback,exactreplay andunchangedfinalizedreports verified. NextRice exact
roster URL. County incomplete/unpublished;thisturn completedLefler4985,Nazaretian4987.

## Rice checkpoint — capture4989 / packet50

Elizabeth G. Rice, criminal I: profile Kathy Williams versus directory Katherine
Williams;813-272-7225,FelonyDivI@fljud13.org,Annex401NorthJeffersonRoom227,
Tampa33602,court15. April12–18,2027 duty tables1/4 Kathy/currentcontacts.
Phone visible/tel/aria,email andZoom9880123461 agree. Biography still says Y/W/E
2020/2021-present; preserve alongside currentI,not as currentassignment proof.
CivilC January2015–January2020 is historical;no currentcivil duty established.

All7HTML proceduresections read atsharedoffice/access scope. Conferbeforebooking,
stateopponentobjects;inpersonunless priorcase-by-caseZoomapproval. Short<=5minutes,
no witnesses,outofcustody→DeputyClerk/status-or-arraignmentdocket. Long heading
10minutesORMORE versusbodyEXCEEDING10 ORwitnesses→JA,notDeputyClerk. Preserve
5–10gap/exact10ambiguity. Filedmotion first;JArequestcase/name/motiontitle/filingdate/
duration/pretrialdate;confer/select;3BUSINESSdaysreplyorofferedslotsreleased.
Notice includesduration/evidentiarylabel,serveopponent/emailJA. Authority3BUSINESS
before;optionaladvancereviewevidence2BUSINESS;allexhibits48HOURS inshort/Zoom
paragraphs. Do not normalizehours tobusinessdays or fill in missing thresholds.

Ordinarymotions FILEDANDHEARD beforepretrial;inlimine FILEDonly. Criminalwaiver
language retained. JuryinstructionsMonday8AMtrialweek;witnesslist sametime;
exhibitlist atORbeforejuryselection,email/Portal,sequential/Bates. Duplicateexhibit
paragraphs retained inoriginal,one checklist rule. Firstdegree/higher two-week
subpoenaperiod versusallcasesfollowingMonday clause preserved. SpecializedPTI/
competency/probationorderchannels notmadeuniversalorderdeadline. No actualtrialdates.

FourPTI andtwo waiverlabels found onsharedFormsindex,link-only. Bothwaiverlabels
share WaiverofPhysicalPresenceinCourt.pdf;no inferredchildcontents/applicability.
No diversionmanual expansion.10topics,4numeric/6relative,1newsource/4reuse;
81citations validated,1438artifacts/307facts readback,exactreplay/finalizedunchanged.
NoPDF/browserUIreviewclaimed. NextSabella;countyincomplete/unpublished.

## Sabella checkpoint — capture4991 / packet51

Christopher C. Sabella, Chief Judge: Christina Novia,813-272-5022,
cornelcm@fljud13.org; Edgecomb800E.Twiggs,Room602,Tampa33602. Directory header
adds ZIP33602-3549. No courtroom number/division letter stated. Phone visible/tel/
aria and email target agree. August17–23,2026 and December13–19,2027 duty rows
agree. Four candidate rows containing assistant Deborah Sabella were excluded by
the judge column; they belong to other judges, not the chief.

April30,2025 guide is4pages,all text and images checked. Contact block instead
prints8132725002 and corncelcm@fljud13.org. Body and embedded targets repeatedly
use cornelcm; retain both original spellings and phone statements. Profile says
Zoom password not required; guide says ask JA for ID/password. No actual ID given.

Chief office instructions: email/copy parties unless lawful ex parte; Portal
service notice does not register JAWS contacts. Register each case and each
attorney/party entitled to service separately. JA strives for response within
1BUSINESSday,otherwise acknowledgment/expected response/alternate contact: a
service target, not a party deadline. Chief-role limitations on another judge's
case remain explicit. Booking through JA; immediate notice with ADA/remote
credentials. Remote appearance requires motion, no numeric lead time supplied.

Proposed orders PDF through Portal's proposed-order portion. Cover says shown to
opponent AND agreed, no response after5DAYS, or objects/will compete. Five days is
an opponent-response condition, not a post-hearing submission deadline or deemed
consent. Competing PDFs/disagreement cover viaPortal plus simultaneous Word email,
subject CompetingOrder and case number. Excused pro se may mail/hand-deliver.
Emergency detailed motion, court determination and unilateral setting retained.
No generic courtesy-copy, exhibit, continuance or cancellation deadline invented.

CHIEF JUDGE navigation `/About/About-the-Court/About-the-Court-3#meetchiefjudge`
redirects to `/About/About-the-Court#meetchiefjudge`. Original URL, resolved URL,
bytes and retrieval saved as sabella-chief-page. Chief/admin sections say70 judges;
opening official directory has69 named profile identities. County reconciliation
must inspect fresh roster/assignment evidence, retain unresolved source count
without inventing an extra person. About spells administrator Rob Snyder, while
PDF header says Rob Synder; county officer followup. Holiday tables collected but
not validated for the access baseline. General history is not substantive review.

Guide's printed ADA URL reuses prior404; exact interpreter landing URL newly
returned404, original saved as sabella-legacy-interpreter. Current ADA/interpreter
sources reused. Shared civil046,county039,Portal upload and reporting reviews reused
at actual scope; chief person review does not finish county order/access inventory.

8topics,1numeric condition/2relative requirements,3new source reviews/7reused.
88citations validated;1463artifacts/311facts readback,exactreplay andunchanged
finalized reports verified. NextTwine-Thomas exact roster path. County incomplete
and unpublished. This turn completed Rice4989 and Sabella4991 sequentially.

## Twine Thomas checkpoint and requested pause — capture4993

Barbara Twine Thomas's contacts, assignment and seven-page individual guide are
saved in packet52. All seven pages were read and visually inspected. The profile
publishes `felonydiva@fljud13.org`; the guide publishes
`felonydivisiona@fljud13.org`. Both statements and original sources remain, without
an alias assumption or controlling-authority decision. Mailing/chambers at401
North Jefferson,Room230 are distinct from the800E.Twiggs entrance instruction.

The guide is revised April7,2026 and expressly dates its new schedule January1,2026.
The HTML calendar is marked September8,2025. Fourteen original calendar data rows
retain their header/cell associations and ambiguous years/weekday labels; they
are not represented as current availability. Three official duty entries retain
one week range and two single dates. Four profile criminal forms and the Public
Defender forms link are inventoried only; no criminal child-form review was added.

Twelve checklist topics, three numeric timing clauses and eight relative timing
requirements preserve the distinct five-business-day materials rule, five-day
courtesy rule and exhibit-at-hearing instruction. A disputed order requires a
hearing to be SET before queue submission; that is not rewritten as HEARD.
Cancellation remains conditional on permission and both parties' agreement.
Shared ADA/interpreter/reporting/Bar evidence reuses the latest same-byte reviews.

Validation: person contract and88 nested citations checked;1488 artifact byte
read-backs and314 finding read-backs; exact replay verified; finalized reports
unchanged. Packet51's entire findings prefix and artifact mapping are preserved.
County remains incomplete/unpublished. User requested pause after this judge;
do not start another profile until resumed. Remaining county followups above
remain pending. No commit, push or publication was performed at this checkpoint.

## Brown checkpoint — capture4995

After the user resumed, Christopher E. Brown's profile, fourteen HTML procedure
sections, two-page February23,2026 remote order and three-page undated recording
order were reviewed. Header/dated directories agree on JA Paulina Skerrett,
813-307-3681,Room334Annex/courtroom32; profile email iscrimdivd@fljud13.org.
The two2027 duty rows are preserved by table/row; Janell Brown assistant rows
were excluded rather than attributed to this judge.

The record contains12 checklist topics,9 numeric timing clauses and10 relative
requirements. Keep the24-hour notice,3-business-day material/response rules,
14-day order period and conditional criminal-specific deadlines separate. Remote
HTML motion/order wording differs from the linked order's written-or-on-record
request. Limine timing clauses retain their evidentiary qualifiers and exceptions.
No independent current civil assignment was established. The profile's two plea
form names are plain list items without anchors; neither was downloaded. The New
Court Date form is described as available through the JA email list.

The cited S-2024-078 was found through the saved official administrative-order
index. It rescinds S-2007-038 immediately onNovember6,2024. Its operative paragraph
and date are absent from extracted text but visible on physical page1; the labeled
`brown-device-visual-transcription` supplements rather than replaces the original.
Preserve Brown's own recording restrictions and authority characterization
separately. No controlling-authority determination was made. Both pages reviewed.

AOSC23-2 is a nineteen-page linked original datedJanuary25,2023 withSeptember2022
standards. Only physical pages1–5 were read and visually checked here; remaining
standards/matrix and later versions belong to the pending county clerk/access
review. Collection is not full content review or proof of current2026 authority.
Shared Portal, ADA/interpreter/reporting/Bar and statewide AI/signature evidence
reuse the latest same-byte reviews from packet52 with their original scope.

Validation: person contract and91 nested citations,1528 artifact bytes and320
finding read-backs, exact replay and unchanged finalized reports. All packet52
findings and artifact mappings remain. County incomplete/unpublished; no commit,
push or publication. Next exact roster label: Judge Scott.

## Scott checkpoint — capture4997

Monique M. Scott's current CriminalE contacts/assignment and all ten HTML procedure
sections are reviewed. JA Niulka Martinez,813-276-2781,crimdive@fljud13.org,
Room344Annex/courtroom33 agree across current profile and dated directories.
Her prior CountyCivilJ and PlantCity civil/probate/guardianship assignments retain
the biography's month precision; do not treat those as current civil assignments.
The one-page linked AutoGlass-labeled form says SmallClaimsJ, carries Scott's
printed name and blank signature/date, demands jury trial unless later waived,
and requires mediation before scheduling trial. Current applicability unconfirmed.

Four individual recording/remote/decorum PDF links return404. Two decorum URLs
were already observed404 under Griner; fresh checks also404. Web cache reports
older copies, which were not saved as current originals or claimed substantively
reviewed. The old Bar link also404; current previously reviewed Bar source reused.
Criminal plea forms remain link-only. Available HTML reviewed; unavailable child
PDFs remain explicit evidence gaps, not resolved by borrowing Brown's orders.

The profile cites S-2012-008. The official administrative index linksS-2025-012.
Both originals retained with their own scope and statements. Legacy order entered
and effectiveFebruary1,2012. New order enteredMarch3,2025/effectiveMarch31,2025,
with earlier operational-transfer exception; handwritten dates visually transcribed.
New order explicitly supersedes2024-080; no invented full supersession chain.
Profile14-day motion filing,2012five-day materials and2025noon-prior-business-day
motion/notice filing remain separate. Two-business-day authority rules preserve
recipient differences. Pretrial attendance and stipulation exceptions preserved.
The2025order's forfeiture provision routes initial probable-cause applications to
CountyCriminalC, but complaints/adversarial preliminary hearings to CircuitCivil;
this is not an assignment to ScottE. Shared office/forfeiture sections reviewed;
no exhaustive criminal merits/assignment analysis. All13pages text read;10visual.

The shared virtual-professionalism sheet was reused without reacquisition, then
reviewed with a source-only summary (`scott-virtual-review`), because an earlier
Griner summary mixed division-specific Zoom information with that shared sheet.
Do not copy those credentials into Scott's record. Previous history remains intact.
Scott's own Zoom is95687943345,no password stated required. DutyAugust10–11,2026
is a two-day interval, not a week; November9–15 retains the source asterisk.
Jackie Scott assistant rows are excluded from this judge's duty evidence.

Validation:11 topics,11 numeric and9 relative timing requirements;105 nested
citations;1575 artifact bytes and326 finding read-backs; exact replay and unchanged
finalized reports. All packet53 findings/artifact mappings preserved. Twenty PDF
pages text-reviewed,seventeen visually checked, with scope explicit. County still
incomplete/unpublished. Next exact roster label Judge Smith. Brown's partial
AOSC23-2 and all earlier county followups remain pending.

## Smith checkpoint — captures4999 and5001

Matthew A. Smith's September25,2026 fifteen-page CountyCriminalA guide is read
and visually checked. Header/directories/duty agree onRoom213Annex/courtroom24,
813-272-5228,Cathy Sanchez; guide saysCatherine Sanchez. Profile visible email
has `.org.org`, while its actual mailto/aria and guide sayCrimDivA@fljud13.org.
Preserve all variants; contact email uses the independently supported guide text.
Biography still labels CountyCivilV current, without dates. No transfer date or
additional current civil assignment inferred. Linked four-page2015 template is
CircuitCivil, with blank CIRCUITJUDGE signature, not CountyCivilV/CriminalA.
The existing original was reused and all four pages read/visually checked.

Twelve checklist topics,14 numeric and12 relative timing clauses preserve
3DAYS versus3BUSINESS DAYS,10business-day remote motion,5business-day orders,
conditional cancellation andTuesday8:30jury selection. Jury instructionsMonday3PM
and witness-list timing remain separate from Monday-noon new-date forms.
The latter condition spans guidepages3–4, while the pretrial disposition-sheet
exclusion is onpage12. Capture5001 refines these specific citations;4999 remains.

Pypdf emitted seven object-offset warnings; originals retained and all15guide
pages verified throughpymupdf images. PDF annotations include Jeske/Gutman plea
forms; these remain link-only, not attributed as Smith-authored forms. The generic
Forms link and interpreter legacy link were previously404; HCBA source previously403.
Current ADA/interpreter/Bar/Portal and county-criminal reviews reused at actualscope.
SharedAOSC23-2 still onlypages1–5reviewed; countyaccessfollowup unchanged.

Actual linkedS-2025-013 returned404 and webopenfailed. Cached searchtitle identifies
FamilyLawProceedings but is only a lead, not a retained current original. The guide
also citesS-2024-015. Its14pageoriginal is collected; onlypages1,10,11,13 reviewed/
visually checked for scope,pretrial,professionalism and dates. EnteredFebruary5,2024
(handwritten date transcribed),effectiveMarch1,2024;remainingcriminalcontentnot
claimed reviewed. Preserve its written-waiver exception beside Smith's current
court-permission language and the already reviewed2025indexorder without resolving
control. Cached nine-month-oldSmith guide wording was not imported into current data.

Validation at5001:127 nested citations,1625 artifact-byte and330finding read-backs,
exact replay and unchanged finalized reports.23PDFpages read/visuallychecked in
this judge review with collection/review scopes explicit. Packet54findings/artifacts
preserved;packet55 remains and onlySmithfinding refined in56. Latest receipt:
`receipts/person-hillsborough-county-matthew-a-smith-v2.json`.
Next exact roster labelJudge Taylor; county incomplete/unpublished. No commit/push.


## Taylor completion and requested pause — capture 5003

Margaret R. Taylor's profile and October 1, 2026 directories agree: County
Criminal B; JA Anita Salario; 813-272-6530; Anita.Salario@fljud13.org; Criminal
Courthouse Annex, Room 330, 401 N. Jefferson Street, Tampa FL 33602; courtroom 31.
Actual email, phone and accessibility labels agree apart from email capitalization.
The HTML contains all seven individual procedure sections and states entry on
January 5, 2022. Preserve that entry date separately from retrieval and any unknown
later revision/effective date. Her prior commercial legal practice is biography,
not evidence of a current civil judicial assignment.

The checklist preserves scheduling through the JA, pretrial motions heard before
pretrial conference, the ten-day specified-motion requirement, two different
ten-day discovery triggers, five-day trial continuance and forty-eight-hour
in-custody transport condition. Proposed-order and general remote instructions
were not found in the individual page; do not borrow another judge's requirements.
Shared S-2025-012 motion/notice and case-law timing remains separately attributed;
the differing scopes do not establish a conflict or require an authority decision.
Existing ADA, interpreter and reporting reviews were reused with their actual
scope and original timestamps. No new PDF visual review is claimed.

Two criminal form links are inventoried, not collected or analyzed. The saved
main/civil forms indexes contain no Taylor entry. Duty January 11–17, 2027 appears
in tables 1 and 4; both contexts are retained without counting two assignments.
Original profile bytes, derived anchors and duty rows are preserved with hashes
and timestamps. Receipt: `receipts/person-hillsborough-county-margaret-r-taylor.json`.

`review/checkpoint-57-validation.json` records 67 nested citations, 1,637 artifact
byte readbacks, 332 finding readbacks, exact replay, unchanged prior findings and
unchanged finalized reports. County-level followups remain unchanged, including
Brown's partially reviewed records-access standards, roster70-versus69,
clerk/access, other officers, material orders, GCM child forms, audio, holidays and
administrator spelling. No partial county publication, finalization, commit or push.
Research is paused after this completed judge as explicitly requested.


## Valkenburg scoped review — capture 5005

Miriam Valkenburg's header and October 1 directories identify County Criminal C,
JA Tamiea Echenique, 813-272-6749, crimdivc@fljud13.org, Criminal Courthouse Annex,
Room 617, 401 N. Jefferson Street, Tampa FL 33602, courtroom 12. Contacts and their
actual destinations agree. The duty table names Miriam V. Valkenburg for November
30–December 6, 2026; retain that source name variant. Biography lists Civil M and
Criminal A without dates or current/past qualifiers; retain without inferring
current civil duties or transfer dates.

The actual standing-order link returns404 by retained HTTP response and independent
web open. Official-domain searches locate a cached excerpt at the same URL but no
available replacement. Do not use that excerpt as the original or current individual
procedure. The criminal pretrial waiver remains link-only. The one-page virtual
professionalism PDF was collected, read and visually checked; its bytes match the
shared sheet collected previously. Its asset query is not a legal revision date.
Profile directs users to JA for Zoom ID, with no password required.

S-2025-012 sections4A–D were reread for the material property procedure: initial
forfeiture probable-cause application goes ex parte to Criminal C via its JA;
JA obtains Clerk's Administrative File number, notifies counsel after decision,
and requests appropriate Portal order. A separate confidentiality motion accompanies
the application if sealing is requested. Complaint and all adversarial preliminary
hearings go to Circuit Civil. Shared scheduling, electronic materials, ADA,
interpreter, reporting and Circuit Civil references retain their documented scope.
Do not treat criminal assignment as excluding this property-related responsibility.

Receipt: `receipts/person-hillsborough-county-miriam-valkenburg.json`.
Validation: `review/checkpoint-58-validation.json`:63 nested citations,1,654 artifact
byte readbacks,335 finding readbacks, exact replay, prior findings and finalized
reports unchanged. County remains incomplete/unpublished; prior followups remain.
The individual standing-order original has a separate `incomplete` check; scoped
person/link completion is not full original recovery.

Implementation evidence: duty extraction initially failed because it expected no
middle initial; inspected actual judge-column row before correcting exact match.
The first save was rejected before persistence for an unsupported custom check
status. Retained rejected packet; `save-valkenburg-repaired-check.py` used existing
`verified`/`incomplete` enums and a separate unavailable-source check, without
weakening validation or changing findings. Use semantic detail in fields/reasons,
not invented status values. Do not rerun either one-shot mutation script.


## Martin completion — capture 5007

Richard H. Martin's profile/directories/August26,2026 guide agree on current dual
Circuit/County Criminal O: JA Hillary Keene;813-272-6841;ppcourt@fljud13.org;
Criminal Courthouse Annex Room229,401N.Jefferson Street,TampaFL33602;courtroom17.
Actual phone/email destinations agree, but HTML accessibility labels still publish
813-272-5103 and juvdepdivb@fljud13.org. Biography dates currentO fromAugust2026,
DependencyB2025–August2026,CircuitCivilJuly2025,CountyCivilL2023–2025; preserve
source precision without inventing dates or importing historical contacts.

All11 guide pages read/visually checked. Saved14 checklist topics,6 quantitative
rules,12 relative timing conditions and14 ordinary-calendar rows. Property return:
confer StateAttorney before filing; email motion to chambers,StateAttorney and
holding agency before scheduling; await court review/hearing determination.
Orders PDF/a viaPortal with required cover letter; signed stipulation filed first.
Cancellation requires filed notice and prompt phone/email, with no stated deadline.
No routine Zoom; unusual leave and participant-specific CCTV rules retained.

S-2024-030:all3pages reviewed, enteredFebruary8/effectiveFebruary9,2024.
S-2024-062:22pages collected; only1,11,13,14,15,21read/visual, entered/effective
August15,2024. Shared motion/order/professionalism provisions reviewed; remaining
16pages not substantively reviewed. A-2025-036:10pages collected/textread,6operative
pages and attachment8/10visual; enteredJuly22,2025,effectiveJanuary1,2026,
attachment separatelyJuly21. Shared emergency relief and protective-injunction
courthouse intake hours retained at their exact case scope; not general civil hours.
Original Martin dutyJuly13–19 differs postedJuly20–26; original expressly excludes
later changes. Posted July contact8132725103/320CEdgecomb is separately dated.

Guide11:59AM motion/notice cutoff, after-noon striking language and shared noon
cutoff remain separate. Guide readily available database authority needs no copies;
sharedorder requires authority3days ahead. PublicPPtable has weekday detention
9–noon/bond2:30, whileguide usesMon/Tue9,Thu9:30detention andMon–Wed3PMmotions.
Keep exact source tables and dates without choosing controlling requirement.
Two legacy duty/PPaspx links404; currentcombinedpage retained. Bondorder2025-063
link inventoried only. Audiovisual-recording order does not establish remote
participation rights for all attendees.

Receipt `receipts/person-hillsborough-circuit-richard-h-martin.json`.
Validation `review/checkpoint-59-validation.json`:126nestedcitations,1,715artifact
readbacks,341findingreadbacks, exactreplay, earlierfindings and finalizedreports
unchanged. Source originals, actual PDFannotations, HTMLlabels, dutytablecontexts
and image-checked date transcriptions saved. County still incomplete/unpublished;
all earlier followups and missing-source observations remain.


## Scope correction and Perrone checkpoint — capture 5009

The user again directed focus on civil litigation, especially commercial litigation.
Prior research went too deeply into criminal procedure. The goal, AGENTS.md and
COUNTY_WORKFLOW.md now require a relevance reason before following another document.
Full personnel/contact/assignment/link coverage remains; noncommercial merits and
criminal calendars/deadlines are not required. Preserve existing evidence, distinguish
intentional nonreview from unavailable sources, and stop recursive authority review.

Perrone: JA Janet Ritchie,8132725122;G famlawdivg@fljud13.org;F dvdivf@fljud13.org;
Edgecomb800EastTwiggsSuite309,Tampa33602;Gcourtroom302,Fcourtroom30. Contacts and
actual destinations agree; guide faxN/A. Biography's CountyCivilU July2013 entry
is not evidence of a current ordinary commercial assignment. GuideSeptember1,2026
collected6pages; review limited to general communication, selectednotice/material
handling, remote access, orders, courtesy/exhibits, emergencyaccess and ADA/interpreter
contacts. Case-specific scheduling, pretrial/trial/merits excluded. NewCourtDateform
and linked rules compilations inventoried only; no new criminal/protective orders
fetched. General office rules remain attributed toG/F, not commercial divisions.

The two order clauses use5/10businessdays for directed drafts versus10days afterany
hearing; both preserved. Guide response target2businessdays belongs toJA, not party.
Existing shared access reviews reused. Structured materiality decisions saved in
`receipts/person-hillsborough-county-frances-m-perrone.json`.

Validation `review/checkpoint-60-validation.json`:58citations,1,734artifactreadbacks,
344findingreadbacks,exactreplay,priorfindings/finalizedreports unchanged. Four selected
PDFpages visually checked. County remains incomplete/unpublished, and all previous
gaps/followups retained. NextAyers must use the renewed commercial-civil screen.


## Ayers scoped checkpoint — capture 5011

Kelly A. Ayers,FamilyD;JA Dwauna Heyward;famlawdivd@fljud13.org;EdgecombRoom422,
800E.Twiggs,Tampa33602;courtroom401. Profile and October1divisiondirectory give
8132762059; same-datealphabeticaldirectory gives8132726913. Preserve both without
selecting a controlling source or inventing a change date. January2026duty entries
use latter; May2027entries use former. Actualprofilephone/tel/aria/email agree.
BiographystatesJanuary2021FamilyD; no ordinarycommercialassignment established.

ProfileHTML saved; review limited to personnel and general correspondence,
reservation/cancellation, access, orders and documentdelivery. Familyfinaltrial,
mediation and family-specificdocket practice excluded. Familyquickreferencechart
and familyadministrativeindex inventoriedaslinks; no extraPDFs fetched. Competing
orders: JAemailorJAWS withtrackedchanges; ordinaryPortalorders withcoverletter,
agreementstatement andprosecopydirections. ConditionalZoom/telephonepermission
retained. Inpersonfinal/trialmaterialparagraph containsboth at-time andthree-business-
days-prior wording; source preserved withoutinterpretation. Schedulingparagraph
says emailJA butsuppliesphonenumber; retainactualwording andseparatesupportedemail.

Receipt `receipts/person-hillsborough-circuit-kelly-a-ayers.json` includesmateriality
screen,6scopedchecklisttopics and3discrepancyrecords. Five dutyrowcontexts represent
fourdistinctintervals; May2027 repeatedintwotables. Validation
`review/checkpoint-61-validation.json`:68citations,1,745artifactreadbacks,
346findingreadbacks,exactreplay,andpriorfindings/finalizedreports unchanged.
No publication/finalization. NextBauman; retaincommercialfocus andallcountyfollowups.

## Bauman scoped completion — capture5013 / packet62

Robert A. Bauman, Family J: JA Debra Stante; famlawdivj@fljud13.org;
Edgecomb Courthouse, Room423, 800EastTwiggs, TampaFL33602; courtroom402.
Profile/division directory phone813-276-8675 differs from the October1
alphabetical directory813-272-5816. Dated duty rows retain both numbers.
Undated biography still describes juvenile assignments as present; header and
current directories say FamilyJ. Preserve statements without resolving them.
Basic scheduling, correspondence, appearance, cancellation, order submission and
courtesy-document directions saved with source quotations and HTML table mapping.
No family merits research or new linked PDF acquisition. Official forms/procedure
links are inventory only in this review. Raw profile and extracted text retained.
Receipt: `receipts/person-hillsborough-circuit-robert-a-bauman.json`.
Validation:90 nested citations;1757 artifact byte readbacks;348 findings; exact
checkpoint replay; prior findings and finalized reports unchanged. Paused before
Brennan; no partial-county publication, finalization, commit or push.

## Brennan scoped completion — capture5015 / packet63

Kim Brennan, Juvenile Delinquency F and Juvenile Mental Health B. Header, biography
and October1 directories agree on current identity/assignments. JA Tracy King-Mills;
8132762338; JuvDelDivF and JuvDelDivB at fljud13.org; Room462 Annex, courtroom43.
Basic HTML procedure paragraphs repeatedly name Judge Vance; current Brennan
applicability remains unresolved. Header and procedure-body division email routes
differ. Two displayed email links point to internal-looking HTTPS paths rather than
mailto targets; those paths were retained as markup evidence and not accessed.
The section8 tracy.king link is a proper mailto. Do not silently substitute the
body's CirJuvdivS route for independently supported current F/B header contacts.
All basic instructions are attributed to the published page, not asserted as
confirmed Brennan requirements. No linked-document or juvenile merits expansion.
Duty row variants Kim Brennan*/Kim H.Brennan retain table contexts: ordinary duty
and Criminal Division O schedule are separate. Do not merge dates across them.
Receipt `receipts/person-hillsborough-circuit-kim-brennan.json`;72 nested citations,
1769 artifact byte readbacks,350 finding readbacks, exact replay and preserved
prior findings/finalized reports. Next Campbell; county incomplete/unpublished.

## Campbell scoped completion — capture5017 / packet64

Lisa D. Campbell, Juvenile Dependency D: JA Jackeline Bermudez-Rodriguez,
8133074750, jackeline.bermudez-rodriguez@fljud13.org; Edgecomb Room320B,
800E.Twiggs,TampaFL33602; courtroom310. Current directories abbreviate JA name as
Jackeline Bermúdez. Earlier duty rows say Room320; current profile/directories and
later rows say320B. Source variants preserved, no inferred personnel change.
Header mailto has trailing whitespace; two body email anchors use relative plain
addresses. Correct email independently repeated in proper mailto anchors; retain
raw malformed destinations without following them. Basic communications,
cancellation, hearing requests, Zoom/physical access and order submission reviewed.
ZoomRoomsA/B may be requested from JA at least3days before hearing; physical room
location and live-appearance exceptions preserved. Two dependency/TPR consent forms
remain links only. Section3's general ORDERS paragraphs reviewed separately from
its excluded trial, witness, exhibit, consent and surrender requirements.
Receipt `receipts/person-hillsborough-circuit-lisa-d-campbell.json`;60 citations,
1781 artifact byte readbacks,352 findings, exact replay and unchanged prior findings
and finalized reports. County remains incomplete/unpublished; DePaul next.

## DePaul scoped completion — capture5019 / packet65

Wendy J. DePaul, FamilyC: JA PattyCoone,8132725777,famlawdivc@fljud13.org;
Edgecomb Room426,800E.Twiggs,TampaFL33602;courtroom408. Header/directories and
contact links agree. June2026 duty rowRoom421 retained separately;December2027
rowsRoom426. Biography says current FamilyC sinceJanuary2021.
Basic communications, scheduling/cancellation, Zoom/courthouse access, document
and order submission saved. Section1 uses >30minutes/evidentiary for live hearings;
section4 dated4/15/25 says <=30minutes non-evidentiary Zoom and >15minutes live.
No controlling choice made. Section7's competing-order email/5day direction and
separate docket/Portal direction retained individually. Family merits, trials,
temporary relief, forms and administrative-order contents intentionally excluded;
S2026023 and family preferencechart saved as official links only in this review.
Receipt `receipts/person-hillsborough-circuit-wendy-j-depaul.json`;93 citations,
1793 artifact byte readbacks,354 findings, exact replay and unchanged prior findings
and finalized reports. NextEssrig;county incomplete/unpublished.

## Essrig scoped completion — capture5021 / packet66

Katherine G. Essrig, IndependentLivingTransitionI and DependencySpecialtyV;
JA ShambraPatrick,8132725080,EdgecombRoom320D,800E.Twiggs,TampaFL33602,
courtroom307. Header/directories/duty agree. Profile/actual anchors, directories,
duty rows, linked guide and bounded official-domain search did not supply a
current assistant email. Keep phone contact; do not infer email or substitute
publicinfo/program inboxes. Scheduling/order/courtesy-copy directions not published
in checked person sources; do not borrow them from another judge.
IndividualZoom8158596094 and phone7866351003 retained. The separate zoom.us/join
anchor is a relative href; proper directmeetingURL is independently present.
Linked onepage Dependency Court Hybrid Procedures retained/read/rendered, stated
effectiveDecember1,2022; URL2023versiontoken not a legal revision date. Basicaccess
only: appearanceexceptions,camera/sound,stationaryattire,onehearingatatime,
24hourclientappearanceconference andcourtabilitytorequireliveattendance.
Source statements about phoneappearance versus camera/video retained, no conflict
resolution or recursiveSC22-1review. PDF has no embeddedlinks; printedZoomtestURL
not called an inspected hyperlink. Two split2026dutyintervals preserved.
Receipt `receipts/person-hillsborough-circuit-katherine-g-essrig.json`;61 citations,
1809 artifact byte readbacks,357 findings, exact replay and unchanged prior findings
and finalized reports. NextFelix;county incomplete/unpublished.

## Felix scoped completion — capture5023 / packet67

Matthew L. Felix, Acting Circuit Family A since January 2025 per biography;
earlier County Civil N assignment is explicitly April 2024–January 2025.
JA Ellen Courtemanche, famlawdiva@fljud13.org; Edgecomb Room427, courtroom411.
Profile/division directory phone813-272-6992 differs from same-date October1
alphabetical directory813-276-2061. January2027 duty rows use profile phone.
Cancellation text and its mailto use misspelled fliud13.org; a later correctly
printed fljud13.org email also targets fliud13.org. Header address independently
supported; preserve wrong targets without contacting them.
Basic communications, booking/cancellation, remote/ADA/interpreter access, order
and document delivery reviewed. Section2 says three business days for courtesy
material; section5 says three days. General remote-motion instruction coexists
with categorical Zoom exceptions. Preserve each statement and scope.
AI disclosure/certification paragraph retained alongside existing AOSC26-12 bytes,
issued May28/effective June15,2026, without deciding authority. No new downloads,
family merits or linked family-form/order analysis. Receipt:
`receipts/person-hillsborough-circuit-matthew-l-felix.json`.
Validation:94 citations;1821 artifact byte readbacks;359 findings; exact replay,
prior findings and finalized reports unchanged. Next Fuson; county incomplete.

## Fuson scoped completion — capture5025 / packet68

Robin F. Fuson, FamilyL per header/directories/June25,2026 guide. Biography still
says Criminal Trial3 current sinceMarch2025; prior Civil/FamilyT dated2019–2021.
JA Meagann Jones, famlawdivl@fljud13.org, Room421 Edgecomb, courtroom416.
Header/directories phone8132762014; guide/HTML aria-label8133071940.
June2026 duty row gives older phone/540S.Annex; September2027 rows give current
header values. Preserve each dated source; no inferred transfer or controlling choice.
Twelve-page PDF collected; review limited to contact/contents, A, general B,
C, general D, E, and K. Selected physical pages1,2,3,4,7,8,9,11,12; visual checks
1,3,4,7,8,9,11. Family merits, emergency authority, evidentiary/trial requirements,
linked family forms/orders intentionally not substantively reviewed.
Basic remote-motion timing is ten BUSINESS days. Directed order preparer has ten
business days after decision; opponent may submit within five business days after
that period if omitted. Page4 courtesy timing five business days differs from
sectionE five days and separate responses/caselaw three days. Preserve each.
PDF links inventoried without downloading them. Rect objects explicitly converted
to coordinate lists after serialization failed; original bytes unchanged.
Receipt `receipts/person-hillsborough-circuit-robin-f-fuson.json`;97 citations,
1844 artifact byte readbacks,362 findings, exact replay and prior findings/finalized
reports unchanged. NextHooi; county remains incomplete and unpublished.

## Hooi scoped completion — capture5027 / packet69

Michael J. Hooi, Family E. Header JA Denisse Meireles versus October1 directories
Denise Meireles; profile/division phone8132726997 versus alpha8132762060.
Room429 Edgecomb,800E.Twiggs,TampaFL33602;courtroom413;famlawdive@fljud13.org.
Header email anchor is relative; later body mailto anchors support the address.
Interpreter declaration visible565Declarations@flcourts.org differs actual mailto
Rule2.565Declarations@flcourts.org. Preserve both, no routing decision or messages.
Five duty rows retain dated phone/name variants and separate schedule contexts;
September2026 row spells judge Micheal. Other matching fields support association,
not creation of another person. No change date inferred.
Basic communication, booking/notice/amendment/cross-notice/cancellation, remote
access, order/courtesy handling and interpreter/reporter access reviewed. Remote
non-evidentiary eligibility retains all three conditions; phone audio supplements
camera. Permission required to amend/cross-notice. No numerical courtesy deadline
invented. Family emergency merits, trials and linked forms/orders not reviewed.
Receipt `receipts/person-hillsborough-circuit-michael-j-hooi.json`;98 citations,
1856 artifact byte readbacks,364 findings, exact replay and unchanged prior findings
and finalized reports. Peacock next; county incomplete/unpublished.

## Peacock scoped completion — capture5029 / packet70

Emily A. Peacock, DependencyB/J and FamilyN. JA JessicaMothershed; Room320C
Edgecomb,800E.Twiggs,TampaFL33602;courtroom308. Both October1 directories give
B/J8132725103 and N8132725355. B juvdepdivb@fljud13.org; J juvdivj@fljud13.org.
N email and separate basic procedures not found in checked page/official search;
retain supported N phone and do not transfer B/J procedure rules to N.
Header phone/tel B/J5103; aria3074751 matches September2026 duty row with Room522.
Biography still claims GeneralCivilD sinceJanuary2019. Indexed old directory
excerpts are not fresh evidence; retained October1 originals supply current entries.
Basic B/J remote/booking/orders/communication/courtesy/cancellation/notice handling
saved. B Zoom82949766513/dial3052241968; J Zoom7836215837/dial7866351003, no passwords.
Portal orders PDF versus competing drafts Word by email remain separate directions.
Published trial calendar and juvenile merits/pretrial/linked forms intentionally
not reviewed. Page's S2026023 all-CircuitCivil characterization retained without
adopting its scope or treating it as assignment proof.
Future duty row SaraK.Peacock* excluded by given-name mismatch, not merged into
Emily. Keep as county reconciliation lead with date/TBD contact qualifiers.
Receipt `receipts/person-hillsborough-circuit-emily-a-peacock.json`;84 citations,
1868 artifact byte readbacks,366 findings, exact replay, prior findings/finalized
reports unchanged. NextPomponio; county incomplete/unpublished.

## Pomponio scoped completion — capture5031 / packet71

Denise A. Pomponio, Juvenile Delinquency A, Juvenile Drug Court E and Marchman Z.
Profile and October1 directories name Deborah Sabella,8132762433; profile email
Deborah.sabella@fljud13.org. Profile Room426 Edgecomb vs directories426Annex;
November3,2025 guide names Clyana Wint but uses Deborah email and mailing427Annex,
401N.Jefferson,TampaFL33602. Preserve separate statements and visitor entrance800Twiggs.
Directory courtrooms A40/E32/Z30 are scoped values; guide gives A40/Z30.
Six-page guide collected, basic sections only reviewed; pages1/3 visually checked.
Communications, booking/cancellation, courtesy materials, PDF Portal orders versus
Word competing drafts, A/Z remote rules and ADA/interpreter contacts saved. E-specific
routing not inferred. CriminalG calendar attribution inconsistent with A/E/Z retained;
literal five(3)business-day deadline and three-business-day versus three-day materials
language retained without selecting a rule. PDF contact annotations with punctuation
retained separately from independently supported contact text. No merits/probation/
treatment/trial-calendar expansion or linked specialized form acquisition.
Receipt `receipts/person-hillsborough-circuit-denise-a-pomponio.json`.
Validation:82 nested citations,1886 artifact byte readbacks,369 findings; exact replay,
prior findings and finalized reports unchanged. County incomplete/unpublished.
Paused at user-requested judge boundary; next Rich only on explicit resume.

## Rich scoped completion — capture5033 / packet72

Jeffrey M. Rich, FamilyI. JA Merissa Clark;8132762968;famlawdivi@fljud13.org;
Room/Suite424 Edgecomb,800E.Twiggs,TampaFL33602;courtroom403. Profile, dated guide
and October1 directories agree. Current profile acquired October17; prior source
retrieval dates retained. Guide states modified December2,2025; eleven pages
collected, only basic sections reviewed, pages1/7/8/9 visually checked.
Basic communications, booking/cancellation, orders, courtesy handling, remote
appearance and ADA/interpreter directions saved. Remote motion ten BUSINESS days;
separate docket-specific Zoom/in-person modes retained. Agreed orders PDF Portal,
competing Word email; drafter ten business days after decision, opponent five
business days after that initial period if drafter fails. SectionB materials five
business days vs SectionE five days/three days retained without choosing control.
Family merits, specialized temporary/postjudgment/pretrial/trial requirements and
linked forms not substantively reviewed. PDF references forms named for other
judges; inventory only, no assumption of their content/current applicability.
Roster label is Judge Schultz Kin, while its URL includes Schultz-Kin. A failed
exact-label precondition was corrected from the saved roster before any persistence;
an exact citation selector was also corrected for the source's double space.
Receipt `receipts/person-hillsborough-circuit-jeffrey-m-rich.json`.
Validation:75 nested citations,1906 artifact byte readbacks,372 findings; identical
replay, prior findings and finalized reports unchanged. County incomplete/unpublished.
Next Judge Schultz Kin; goal active. All county-level followups retained.

## Schultz-Kin scoped completion — capture5035 / packet73

Leslie K. Schultz-Kin, Acting Circuit Judge DependencyS sinceJanuary2023 per
profile; CountyCivilI October2021–December2022 is historical. JA Leah Faulk;
8132727137;337AEdgecomb,800E.Twiggs,TampaFL33602;courtroom312. Profile and October1
directories agree. Actual phone/tel/aria and Zoom84572956762/no-password target
agree. No assistant email published in checked profile, guide, saved directories
or targeted official searches. General publicinfo mailto is not JA contact.
Individual booking/order/courtesy directions likewise not found; do not borrow
another judge's rules. Search terms and limits saved in receipt.
One-page Dependency Court Hybrid Procedures fully read/visually checked; effective
December1,2022,revision unstated. Remote permitted except trials/lengthy evidentiary
hearings unless court specifies otherwise; court may require in-person. Camera,
sound, stable connection, stationary/private setting, no moving vehicle or
simultaneous hearing and counsel24hour preparation retained. No substantive
juvenile/dependency expansion or underlying SC22-1 analysis.
Exact linked URL lacks the version query on Essrig's earlier copy; original and
text hashes match. Both retrieval observations preserved, no new unique PDF bytes;
source-only review kept separate from individual contacts/Zoom.
Receipt `receipts/person-hillsborough-circuit-leslie-k-schultz-kin.json`.
Validation:44 nested citations,1920 artifact byte readbacks,375 findings; exact
replay, prior findings and finalized reports unchanged. County incomplete.
Next Tibbals; remaining county-level followups retained; goal active/unpublished.

## Tibbals scoped completion — capture5037 / packet74

Wesley D. Tibbals, UnifiedFamilyF. JA Jacqueline C. Watkins (profile,guide,alpha);
Jackie Watkins (division directory). Room428Edgecomb,800E.Twiggs,TampaFL33602;
courtroom410. Profile/October1 directories8132762099 versus July28,2026 guide
8132722099, visually confirmed. FamilyF emailFAMLAWDIVF@fljud13.org. ActualHTML
phone/tel/aria and email/mailto match, but cross-source phone difference retained.
Five-page guide collected, basic A–E and I reviewed; pages1/3 visual. JAWS15/30minute
and5minuteUMC/emailJA routing, notice, remote motion at least3days unless notice
alreadyZoom, PDFPortal orders5daysafterhearing, courtesy5BUSINESSdaysbefore saved.
Disputed-order Word email explicitly FelonyDivE@fljud13.org, no mailto annotation;
source discrepancy retained without promoting it to verifiedFamilyF contact or
silently substitutingFamilyF email. Guide ADA/interpreter contact routing saved.
No family merits/emergency/exhibit/trial/temporaryrelief/postjudgment/mediation
expansion. No specific cancellation procedure found in checked guide. Biography
business-litigation experience is not a current civil assignment.
Receipt `receipts/person-hillsborough-circuit-wesley-d-tibbals.json`.
Validation:62 nested citations,1938 artifact byte readbacks,378 findings; exact
replay, prior findings and finalized reports unchanged. NextTompkins; county-level
followups remain, goal active/unpublished.

## Tompkins scoped completion — capture5039 / packet75

Joseph M. Tompkins,FamilyB. JA CarmenJones;8132725496;famlawdivb@fljud13.org;
Room420Edgecomb,800E.Twiggs,TampaFL33602;courtroom400. Profile/directories agree,
actualtel/mailto/Zoom6066682029 targets match. JudicialHistoryCountyCivil/Traffic
is undated, not treated as concurrent civilassignment proof.
BasicHTML communications,cancellation,booking,appearance,materials and orders saved.
JAWS<=60minutes versus JAemail>90 leaves >60 through90 unstated; preserve gap.
Contested evidentiary>=30inperson;CMC/uncontested<=15mayZoom,omitted modes uninferred.
Materials5daysbefore; agreedPDFPortal versus competingWordemail; no Section8 order
submissiondeadline. Specialized familyfinancial/CMC/postjudgment/emergency contents
and linked forms/chart intentionally not reviewed; no additionalPDF acquisition.
Receipt `receipts/person-hillsborough-circuit-joseph-m-tompkins.json`.
Validation:70 nested citations,1950 artifact byte readbacks,380 findings; exact
replay, prior findings/finalizedreports unchanged. All69openingprofiles reviewed,
but county incomplete. Countyfollowup plan identifies exact retained evidence,
remaining tasks and scope screen; current focus is roster reconciliation then
clerk/officers/shared civilaccess. No next county or publication/finalization yet.

## County roster reconciliation — capture5041 / packet76

Fresh October17 roster has69unique cards identical to October16; all69profileURLs
map to complete scopedperson records. Alphabetical/division/chart PDFs returned
identical original and text hashes to previously visually reviewed October1versions.
Repeated pypdf object-offset warnings acknowledged; prior five-page visual/table
review reused, no new render claimed. Alphabetical68body names pluschiefheader
reconcile69. About chief/admin paragraphs continue70judges, revision unstated.
Preserve that nonblocking conflict without selecting source or inventingperson.
Unnamed seniorCircuitCivilM remains a separate missingcoverage lead. Searches for
current senior identities yielded historical assignments/annualreports, not current
identity proof. FuturedutyTBD names preserved by table/row/date, not newcurrentjudges;
old flgov nominee/applicant results likewise not appointments. No claim ofcomplete
statutoryseat or temporarysenior inventory.
Officer officialrosters collected and cardlinks inventoried:8general magistrates,
7hearing officers. Receipt `receipts/roster-reconciliation-20261017.json` and
`review/county-officer-inventory.json`. Individual officer reviews pending; follow
actual profile links sequentially, with family/traffic basic-only and probate/trust
commercially relevant scope. Clerk verification next.
Validation:1965artifactbytes/383findings readback, exactreplay, priorfindings and
finalizedreports unchanged. County incomplete; goalactive.

## Clerk core review — capture5043 / packet77

Victor D. Crist is the Clerk of the Circuit Court and Comptroller. Official
biography says duties assumed January2025. Civil customer service:8132768100;
Clerk of Court,POBox3360,TampaFL33601-3360. Electronic contact is the official
Email/ContactUs form, not a published direct civil email. Form HTML inspected;
no question submitted or delivery/UI test claimed.
Locations: Edgecomb800E.Twiggs Room101,Tampa33602; PlantCity301N.Michigan Room1071,
PlantCity33563; Brandon311PaulsDrive Suite110,Brandon33511. Edgecomb/PlantCity
weekdays8–5,Brandon8–4. PatCollierFrank419Pierce Room140,Tampa33602 is also listed,
with recording/property routing kept separate. Location page includes Brandon
underCivilCourt while individual civil FAQs listTampa/PlantCity; statements retained.
Circuit-civil original reused with expanded landing-page review beyond prior
exhibits-only receipt. Records may need4businessdays forredaction; registry-funds
statement service target10businessdays fromreceipt, not a party filingdeadline.
County civil landing FAQs reviewed: jurisdiction wording, reassignment notices,
records,registry/lien release,judgment/service routes. S2026039 heading with
S2024039 DivisionX body and S2026015 DivisionU list preserved; threshold phrases
up to50000 versus less50000 and less8000 boundaries remain source ambiguities.
Annual judgment-interest descriptions preserved as clerk statements, not current
rate/statutory conclusions. No conflict resolution or personal case search.
Linked forms/registry/UIDDA/service/foreclosure/eFiling/fees/records/holidays require
materiality and prior-review screening before followup. Exact URLs and source
anchors saved; case/fragment variants are candidates for comparison, not assumed
identical. Reassignment lists contain personal case data and were not downloaded.
Receipt `receipts/clerk-core-reviewed.json`; routes in
`review/clerk-civil-followup-routes.json`. Validation1982artifactbytes/386findings,
exact replay, prior findings/finalized reports unchanged. County incomplete.

## Clerk civil services — capture5045 / packet78

The six pages acquired through saved core-page navigation are now reviewed:
Court Registry, E-Filing, Foreclosure Sales, Serving Summons/Subpoenas/Documents,
UIDDA and Court Boundary Lookup. Original HTML, extracted text, URLs and retrieval
times remain in the acquisition manifest and database. Source-bound actual anchors
are in `review/clerk-services-links.json`; do not infer destinations from labels.
Three required forms followed from those anchors: division assignment revised
August 27, 2026; summons request revised April 28, 2021; foreclosure cancellation
revised February 19, 2021. All four PDF pages were read and visually checked.
Checkbox hierarchy and embedded links were verified; no case form was submitted.

Preserve the separate clerk estimates: registry release approximately 10 calendar
days after certified release order; optional eviction mailing within 3 business
days after filing; summons availability within 2 business days after request.
These are not interchangeable with the earlier registry-statement 10-business-day
estimate. Foreclosure objection uses filing of the sale certificate; title timing
uses issuance. Separate both $70 sale charges and retain the plaintiff exception
to the 5% bidder deposit. The 4 PM prior-day deposit instruction does not say
business day; final payment is noon the next business day. No deadlines calculated.

Recorded source differences: foreclosure packet Portal FAQ versus dated 2023
foreclosure changes; general registry order/tender instruction versus specific
county lien remedies; fee-expression wording; email versus HOVER summons delivery;
November 2016 standards description versus August 2017 PDF href; malformed UIDDA
civil-rules link. These do not block completed source review. An actual service
cost anchor points to a 2006 Senate report; do not present it as current sheriff
fees. The correct Bar rules index is independently linked on the UIDDA page.

The boundary form requires acknowledgment of the map and offers defendant
residence, cause location or property location; no filer-address assumption.
Reuse `hillsborough-east-division-2024-079` for the reviewed original order.
Static map instructions were reviewed; interactive map operation was not tested.
Existing Circuit Civil order and uniform foreclosure judgment reviews remain
separately attributable; no recursive authority-resolution project was started.

Receipt: `receipts/clerk-services-reviewed.json`. Save command:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python runs/county-hillsborough/2026-10-16/review/save-clerk-services.py`
was executed once successfully after a pre-save JSON repair. Do not rerun the
one-shot assembler: replay the immutable packet through the documented helper.
A PyMuPDF Rect in annotation metadata initially prevented receipt serialization;
converted to a numeric list before retry. Packet/receipt absence and unchanged
state were checked before retry; no database write had begun. Repair evidence is
`review/clerk-services-save-repair.json`. Final validation read back 2,011 artifacts
and 396 findings; 19 new source citations validated, identical replay, prior facts
and finalized reports preserved. Remaining clerk routes and officers are pending.

## Remaining clerk services — capture5047 / packet79

Thirteen additional source reviews cover paper files, confidentiality, visitor
preparation, clerk holidays, eviction landing/process/rights pages, civil/shared
fees, copy requests, confidentiality notice, security list, recordings route and
current CFO judgment-interest table. Eighty-eight label/value rows retain seven
actual HTML table indices and row indices; original inequalities, tax units and
amounts are not repaired. Seven source discrepancies are separately recorded.
Confidentiality notice (July1,2023) two pages and security list (May9,2017) one page
were read and visually checked. Current link does not make the 2017 list newly
revised. PDF service-certificate fax/email options are not clerk submission routes.

Paper-file viewer guidance uses images whose labels plain text extraction loses.
Actual alt text and mailto:filesordered@hillsclerk.com are in the source-bound link
inventory. Files held10businessdays after receipt; nonparties allow4businessdays
for redaction. Copy-request form HTML inspected only; no submission or UI test.
June19 holiday table has a specific exception opening court-service/official-record
locations while BOCC areas close. PlantCity closesMarch2 for the parade; do not
convert generic closure heading into a universal closure assertion.

Eviction chart expressly describes simple RESIDENTIAL proceedings; its timelines
must not become commercial eviction rules. Shared mail-copy page says$1.01 while
E-Filing says$1.00; both retained. Residential amenities/quiet-hours examples remain
attributed clerk statements, not verified statutory or commercial lease rules.
Fee table has$10 and$4 summons rows, unclear foreclosure boundaries/cross-claim
operators, differently scoped subpoena fees and two-mills versus .002-mills text.
County-to-circuit appeal wording is retained as source text, not current routing
advice. No fees or case deadlines calculated.

Legacy CFO link timed out; official-domain search found
https://www.myfloridacfo.com/division/aa/audits-reports/judgment-interest-rates.
Direct original retained, current-rate table and historical notes reviewed. Quarterly
CFO setting description differs from civil FAQ annual-December1 description; no
controlling-authority resolution or rate selection for an individual judgment.

HOVER returned ReadError and web Internal Error. Official records returned only
an HTTP200 application shell and web zero-content page. CUA reported iab unavailable
and an empty browser inventory. No interactive review claimed. These are separate
shared-access followups, along with current records standards, actual court-reporting
detail and official-record privacy route. Clerk recordings page expressly says it
is not custodian and points to the previously collected court-reporting page.

Receipt `receipts/clerk-remaining-reviewed.json`; source links and image labels in
`review/clerk-remaining-links.json`; browser evidence in
`review/clerk-browser-attempts.json`. `review/save-clerk-remaining.py` assembled
immutable packet79 once; use helper replay for verification, not rerunning the
assembler.26 citations validated,2051 artifacts/411 findings read back, exact replay,
prior findings and finalized reports unchanged. Next saved-roster officer is
MichelleBlume; review contacts/basic family operating procedures before any next
person. County remains incomplete and unpublished.

## General Magistrate Michelle Blume — capture5049 / packet80

First of15 other officers reviewed under the basic noncommercial scope. Saved
roster URL GM-Michelle-Blume redirects to Michelle-Blume; both URLs preserved.
Substantive header/biography and roster identify MichelleBlume, General Magistrate,
Unified Family Court domestic relations/family and juvenile dependency; biography
states January2024 assignment. Administrative Assistant NatalieGuerra,
813-276-2337, family gmfam3@fljud13.org; dependency GMJUV3@fljud13.org. Contact
anchors/phone accessibility label agree with displayed contacts. Edgecomb Courthouse,
Room406,800E.TwiggsStreet,Tampa33602. Fax813-301-3737 is specifically published for
courtesy notices/cancellations, not independently established as a general fax.

Email scheduling; no JAWS hearing times or magistrate-order processing. Proposed
orders, when requested, go by email in Word with cover letter. Basic scheduling,
cancellation, physical materials, appearance, interpreters/ADA and recording
summarized. Family merits/temporary-relief/parenting/support forms deliberately not
exhaustively reviewed; links retained. No call/email/fax/Zoom join or live portal use.

Five discrepancies retained: generic JudgeAlvarez H1; exhibitSuite405 versus
header/evidentiarySuite406; legacy Skype paragraph naming MagistrateJohnson;
May1,2022 dependency appearance permissions versus linked December1,2022 shared
hybrid guidance; greater-than2-hour cancellation heading versus2-or-more body.
Source review complete without resolving these. Family and dependency Zoom routes
and email addresses are distinct, not erroneous duplicates.

Official roster's GM/HO referral-table link acquired once. One-page PDF revised
2026-10 visually checked for Blume GM-3 column/contact row. Case suffixes01,02,05,06,
10,13,14,18,21,22,26,29 retained. Other names on the shared page remain inventory;
individual profile review required before any completion. Same-byte shared hybrid
guide reused from latest Schultz-Kin review; no other judge's contacts inherited.

Receipt `receipts/person-hillsborough-general-magistrate-michelle-blume.json`;
links `review/blume-links.json`; one-shot saver `review/complete-blume.py`;
immutable `draft/checkpoint-80.json`. Existing officer validator exercised without
changing role to judge:50 nested citations,8 checklist topics,5 conflicts,2062
artifact bytes and413 facts validated/read back; identical replay and prior/finalized
history preserved. Next SeanCadigan, whose civil/trust responsibilities should be
screened for commercial relevance before choosing review depth. County incomplete.

## General Magistrate Sean O. Cadigan — capture5051 / packet81

Second of15 other officers reviewed. Current profile identifies Sean O. Cadigan,
Probate/Guardianship/MentalHealth/Trust; assistant Vivianie Marteli;813-276-8517;
fax813-301-3746;gmpgt1@fljud13.org. Edgecomb Courthouse,Room418,800E.TwiggsStreet,
Tampa33602. Phone/mailto match; unlabeled second number is identified by original
HTML fal-fax icon, saved in `review/cadigan-links.json`. Generic JudgeAlvarez H1
retained as defect without changing person identity. Biography2003 Thirteenth
Circuit appointment distinguished from2000 Sixth Circuit appointment/past family.

Eight scoped topics cover identity/assignment, basic hearing prerequisites,
property-report submission, appearances, Word orders/JAWS delivery, interpreter/ADA,
civil/trust referral/report recording and linked constructive-service form. Most
hearings use unique office-supplied Zoom credentials; no standing ID invented.
Preferred Word email; JAWS alternative also Word in Probate/Guardianship&Trust
DivGM1 magistrate queue, not judge queue. Register both MH/CP when required. This
GM1 context is separate from Wartenberg's familyGM1; Blume's no-JAWS instructions
are not inherited. Nonprofessional guardian property-report recency is12months,
not365days; mail/hand-deliver to clerk rather than file. No private report collected.

Previously reviewed S-2022-020 source reused for civil/trust referral: written
objection10DAYS after SERVICE, report rules and recording custody. Prior full
four-page probate diligent-search form review reused, no fresh download or private
investigation. S-2024-016 and specialized guardian/advocacy/physician forms remain
official links; no exhaustive noncommercial merits/authority expansion. Sample
caption division list is not current roster evidence.

Receipt `receipts/person-hillsborough-general-magistrate-sean-o-cadigan.json`;
immutable packet81; one-shot saver `review/complete-cadigan.py`. Officer validator
and36 nested citations checked;2069 artifacts/414 facts read back; exact replay,
prior findings and finalized reports unchanged. No new PDF or browser UI check.
Next TracyEllis, basic family scope. County/statewide work incomplete and active.

## General Magistrate Tracy Ellis — capture5053 / packet82

Basic family/dependency review completed, third of15 officers. Profile: Unified
Family Court (Independent Living Court); Case Manager Carly Kowalski, shared
email gmfam1@fljud13.org; Edgecomb Courthouse,Room313,800E.TwiggsStreet,Tampa33602.
No individual office phone located in profile, magistrate roster, remote directory
or bounded official-domain searches. Generic circuit footer number is not imported
as her office number. Case Manager is not relabeled as Judicial Assistant.
Original mailto matches email. Zoom913-0534-7270/passcode35547 and link agree.

Five basic topics retain identity/contact, assignment, virtual appearance,
shared access and referral/instruction availability. Existing shared hybrid guide
review reused from Schultz-Kin; same original hash as exact Essrig versioned link.
No individual booking/cancellation/exhibit/order instructions located; do not
inherit another officer's rules. No detailed dependency merits review.

S-2025-007 collected as9physical pages, but reviewed only for assignment/basic
referral, supersession and dates. Section6 disqualification and oath attachments
are outside substantive review. Page6 rendered and visually checked: effective
and entered February6,2025. No visual table verification claimed. Profile biography
odd01–49 differs from order dependencyGM1 table; retain both without resolving.
General Magistrate Tracy Ellis/TracyL.Ellis identity is distinct from generic
JudgeAlvarez H1. DependencyGM1 is not familyGM1 or probateGM1.

Search index returned GMJUV1@fljud13.org, while saved direct HTML and current
web open show gmfam1@fljud13.org. `review/ellis-index-search.json` retains the search
response and observation time, expressly as an indexed lead, not an original of
the alternate webpage or proof of a dated email change. Three discrepancies saved.

Receipt `receipts/person-hillsborough-general-magistrate-tracy-ellis.json`;
immutable packet82; one-shot saver `review/complete-ellis.py`. Officer validator
and32 nested citations passed;2083 artifacts/415 facts read back; identical replay,
prior facts and finalized reports unchanged. Next Cheryl Mason. No publication,
finalization, commit or push. County and statewide goal remain incomplete.

## General Magistrate Cheryl Mason — capture5055 / packet83

Fourth of15 officers reviewed. Janice Hernandez, Administrative Assistant;
813-276-2335;gmfam5@fljud13.org;Edgecomb Courthouse,Room407,800E.TwiggsStreet,
Tampa33602. Original phone/tel/accessibility label and email/mailto agree. Zoom
977-1995-1726/passcode473583 matches link. FamilyGM5 contact/assignment legend and
column visually checked in existing October2026 referral PDF; no new download.

Six basic topics cover identity/assignment, communications/scheduling, ordinary
notice/exhibit delivery, remote access, cancellation/pretrial and orders/access.
Email scheduling, no JAWS booking; ordinary <=30minute hearings remote except
pretrial; >30minute evidentiary hearings inperson unless approved. Notice/relief
service uses5BUSINESSdays; ordinary exhibit delivery uses5DAYS, hard copy to407
and opponent, not filed. Word orders plus cover letter emailed, not JAWS. Family
merits and temporary-relief requirements not extracted as general civil rules;
specialist forms retained as links. GenericJudgeAlvarez H1 and greater-than2hours
versus2hours-or-more wording retained without selecting control.

Receipt `receipts/person-hillsborough-general-magistrate-cheryl-mason.json`;
packet83; one-shot saver `review/complete-mason.py`. Officer validator and34 nested
citations passed;2090artifact bytes/416facts read back; exact replay, prior facts
and finalized reports preserved. No publication/finalization/commit/push. Next
Nancy Neaves, probate/trust relevance review with other subjects basic only.

## General Magistrate Nancy Neaves — capture5057 / packet84

Fifth of15 officers reviewed. Administrative Assistant Torey Blount;813-272-8565;
gmpgt2@fljud13.org;Edgecomb Courthouse,Room414,800E.TwiggsStreet,Tampa33602.
Phone/tel and email/mailto agree. Profile identifies probate/guardianship/trust
(Baker Act); dated sharedS-2022-020 identifies NancyJ.Neaves. GenericJudgeAlvarez
H1 recorded as defect. No fax, biography date or standing Zoom ID invented.

Eight scoped topics retain contacts/assignment, basic case routing, scheduling
and property-report delivery, appearance, Word orders/JAWS delivery registration,
access, civil/trust referral and constructive service. Shared order and four-page
probate diligent-search form reuse prior full reviews, without inheriting another
person's procedure. Neaves prefers Word email; her JAWS section is for report/order
E-delivery registration, with BOTH MH/CP registration in involuntary guardianship.
It does not give Cadigan's alternate magistrate upload queue; neither permission
nor prohibition is inferred. Office provides unique Zoom ID for each hearing.

Property-report12MONTH age and delivery to clerk rather than public filing
preserved. Mental-health/guardianship specialties basic only; underlyingS2024016
and specialist forms remain official links. SampleA/B/U/W caption is not current
assignment proof. Shared10DAY referral objection after SERVICE and recording
custody retain dated-source scope, without deciding current controlling authority.

Receipt `receipts/person-hillsborough-general-magistrate-nancy-neaves.json`;
packet84; one-shot saver `review/complete-neaves.py`. Officer validator and33 nested
citations passed;2097artifact bytes/417facts read back; identical replay, previous
facts and finalized reports preserved. No new PDF, browser UI check, publication,
finalization, commit or push. Next Lisa Phillips, basic family/dependency scope.

## General Magistrate Lisa Phillips — capture5059 / packet85

Sixth of15 officers reviewed. Administrative Assistant Judith Lovelace;
813-272-5525;Edgecomb Courthouse,Room311,800E.TwiggsStreet,Tampa33602. Phone/tel
and accessibility label agree. No individual email found in original profile,
magistrate roster or bounded official searches for LisaPhillips email/JudithLovelace.
Only profile mailto is circuit-wide publicinfo; do not use as office email or
infer one from a division label. Zoom837-2582-5836/passcode849881 agrees with link.

Five basic topics save contacts, assignment, appearance, shared access and basic
referral/instruction availability. Profile header JuvenileDependency and biography
DomesticRelations/2022 appointment are retained separately. ExistingS2025007
appointment row visually checked on physicalpage2: dependencyGM4LisaPhillips;
familyGM4MaxineWilliams is a different context. GenericJudgeAlvarez heading also
recorded. No decision about controlling assignment or unsupported change date.

Exact shared hybrid PDF already collected for Essrig, samebytes as Schultz-Kin;
prior one-page basic access review reused. SharedS2025007 basic referral section
reused; no disqualification/dependency merits or oath review. Individual profile
has no booking/cancellation/order/exhibit instructions; no other officer's rules
inherited. No new PDF acquisition.

Receipt `receipts/person-hillsborough-general-magistrate-lisa-phillips.json`;
packet85; one-shot saver `review/complete-lisa-phillips.py`. Officer validator and
36 nested citations passed;2105artifact bytes/418facts read back; identical replay,
prior findings and finalized reports preserved. No publication/finalization/commit
or push. Next Philip S.Wartenberg, basic family scope; county remains incomplete.

## General Magistrate Philip S. Wartenberg — capture5061 / packet86

Seventhof15 officers reviewed. AdministrativeAssistantRebeccaSullins;
813-272-5351;fax813-301-3737 in notice/cancellation text;EdgecombCourthouseRoom404,
800E.TwiggsStreet,Tampa33602. Headergmfam1@fljud13.org versus procedure/table
famlawgm1@fljud13.org preserved with source location; each HTMLmailto matches its
own displayed address. FamilyGM1 table legend/contact checked visually; separate
from probate/dependencyGM1. Zoom916-8038-2965/passcode753981 agrees with link.

Six basic topics retain contacts/assignment, communications/scheduling, appearance,
notice/cancellation, order preparation/submission and access. No JAWS booking or
magistrate-order uploads; Word email with coverletter. Remote<=30minutes except
pretrial; longer evidentiary hearings inperson subject to7DAY request/motion paths.
Separate telephone paragraph preserved. Notice/service5BUSINESSdays versus
cancellation24HOURS and >2hours versus >=2hours wording retained by source. Family
merits and temporary-relief/time-sharing/fee requirements not expanded.

Individual recommended-order PDF2pages read/rendered. TNR12pt/1.5spacing and
case/division/caption/confirmation/service-address requirements saved at basic
submission scope. Separate judicial orders prepared for judge; assistant uploads.
PDF asserts April1,2022 exceptions-period change; preserved as source statement,
not freshly verified rule change. URLver2022 is not document revision, especially
where body referencesS2024019. Underlying family authority chain not followed.

PDFpage2 paragraph11 visibly displays FamLawGM1@fljud13.org but annotationxref62
opens ana.vazquez@fljud13.org; paragraph12 target matches displayed mailbox.
`review/wartenberg-pdf-links.json` retains original source metadata/hash, extraction
time, page/rectangles/visible text/targets. Alternative target not imported as
current assistant/contact and no unrelated-person search or message sent. This
PDF check is now explicit inAGENTS.md. Four recorded discrepancies: genericH1,
email variants,PDFmailto defect,two-hour thresholds.

Receipt `receipts/person-hillsborough-general-magistrate-philip-s-wartenberg.json`;
packet86; one-shot saver `review/complete-wartenberg.py`. Officer validator and65
nested citations passed;2118artifact bytes/419facts read back; identical replay,
prior findings and finalized reports preserved. No publication/finalization/commit
or push. NextMaxineWilliams,basicfamily scope; county remains incomplete.

## General Magistrate Maxine Williams — capture5063 / packet87

LocalQwen3.8 completed review/local-maxine with exit0; cloud source review accepted
with bounded fidelity corrections. Shared office813-272-6435,gmfam4@fljud13.org,
Room405. Assistantname remainsnull/not_published with actualpublishedTBD,reason,
citation and3URL negative-search log. Shared office contact/role verified separately.
Validator supports this documented absence and rejects verified placeholders;
28focused tests passed and all7previous real officer receipts remained valid.

Six basic topics and12unique form links saved. Source defects: displayedphone
272-6435 versus tel/aria276-2337; genericAlvarez heading; >2hours versus >=2hours;
Sarmiento exhibit addressee versus Williams; Skype section names Johnson. No
unrelated person's contacts imported. Cloud corrected conditionalIfInstructedZoom,
OVER100miles wording, separate telephone route, exactindexanchor and fax evidence.
Worker visual check not independently evidenced; table legend observation credited
to previous cloud image review instead. Worker originals retained separately from
corrected accepted receipt. No exhaustive family merits/form review.

Acceptedreceipt receipts/person-hillsborough-general-magistrate-maxine-williams.json;
immutablepacket87;one-shotreview/save script review/accept-maxine-worker.py.
45nestedcitations,2130artifactbytes/420facts readback,identicalreplay,priorfacts and
finalizedreports preserved. No publication/finalization/commit/push. NextCharlesDenton.
The firstlegalprofileworker launch failed beforeinference with expiredCourtListener
OAuth; saved-source codeprofile succeeded. Existing CourtListener credentials were
not modified; official publicsource work can proceed without that dependency.

## Hearing Officer Charles Denton — capture5065 / packet88

LocalQwen3.8 completed review/local-denton with exit0. Cloud verified profile,
contacts,scope and save script. DianelysAleagaTamayo,AdministrativeAssistant;
813-272-5458;CS1@fljud13.org;EdgecombRoom490,800E.TwiggsStreet,Tampa33602.
Phone/tel/aria and email/mailto agree. Zoom882-0646-5216,no password required.
October2026 tableCSEHO1(00–16),CharlesA.Denton matched by contacts; cloud visually
checked table row. Worker attempted image input but capability unsupported; it
correctly declared no visual inspection and used two extraction engines.

Four basic topics save identity/contact/assignment,communications,documents and
appearance/access. ProfileDORIV-D hearings remote Zoom/telephone; telephone oath
requires notary or authorized oath administrator at start; Zoomvideo exempt.
Documents filed withclerk at least3DAYS before. Digitalrecording,private reporter
at ownexpense,minor attendance needs priorcourtorder. Appointment2021 remains
biography statement; no independent appointment source claimed. Four unique
specialist form links inventory only. GenericAlvarez H1 and middleinitial source
variant recorded; no legalmerits or enforcement-form analysis expanded.

Cloud tightened savedresolvedURL validation (actualURL compared,not rederived)
and verified negative tampered-target rejection, and corrected acceptedreceipt
filename to established person-prefix. No substantive receipt correction required.
Cloudreview JSON and workeroriginals retained. Receipt:
receipts/person-hillsborough-hearing-officer-charles-denton.json. Saver:
review/local-denton/prepare-save.py --save (one-shot,do notrerunafteradvance).
42citations,2141artifactbytes/421facts readback,identicalreplay,priorfacts and
finalizedreports preserved. NextJosephFrank. County/statewide remain incomplete.

## Hearing Officer Joseph Frank — capture5067 / packet89

First localpacket rejected: all7roster cards mislabeledCivilInfractions and empty
contactprofile labeledverifiedprocedure. Localrevision corrected originalHTML
per-card attribution (FrankonlyCivilInfractions,sixUnifiedFamilyCourt), documented
boundedabsence, and implementedtested no_published_procedure_located path.
Contacts BetsyChesser,AdministrativeAssistant,813-272-5297;AnnexRoom100,
419PierceStreet,Tampa33602. Noindividualemail/procedure located afterboundedchecks;
phone andassistant verified separately. Missing evidence islimitation,notconflict;
genericAlvarezH1 remainsone sourceconflict. SharedS2025057CivilTrafficDivision
Z2 context separately recorded; no namedofficer in order,division-level association.
Cloud visuallyreadpage4:enteredOctober31,2025,ChristopherC.Sabella,ChiefJudge;
effectiveimmediately. OriginalOCR/scanmetadata retained. Newvisualtranscription
has originalPDFhash/retrievaltime,derivedtexthash/extractiontime and renderedimage.
Childrestraintprogram deadline removedfromindividual basicchecklist; priorworker
receipt/readwork retained. No exhaustive noncommercialmerits work continued.

Negativeprocedure requires exactperson,sourcecitation,reason,structuredURL/search/
result log,andemptydocuments; sharedsources separate. Positiveguards intact.
Cloud added realhostname/no-whitespace checks and rejection of contradictory
positiveinventory.51tests passed;all9previous realreceipts unchanged andvalid.
Receipt receipts/person-hillsborough-hearing-officer-joseph-frank.json;
review/local-frank/prepare-save.py --save alreadyexecuted (do notrerun).
31nestedcitations,2161artifactbytes/422facts readback,replay,priorfacts/finalized
reports preserved. Localoutputs and correctionhistory retained. NextSabrinaFrey.

## Hearing Officer Sabrina Frey — capture5069 / packet90

LocalQwen3.8 completed review/local-frey with exit0. Cloud verified profile,
contacts, scope and save script. Daniel Aponte, Administrative Assistant;
813-272-0241; CS3@fljud13.org; Edgecomb Room 480, 800 E. Twiggs Street, Tampa 33602.
Phone/tel/aria and email/mailto agree. Zoom 821-3565-2986, no password required.
October 2026 table CSEHO-3 (34-50), Sabrina M. Frey matched by contacts.

Four basic topics save identity/contact/assignment, communications, documents and
appearance/access. Profile DOR IV-D hearings remote Zoom/telephone; telephone oath
requires notary or authorized oath administrator at start; Zoom video exempt.
Documents filed with clerk at least 3 days before. Digital recording, private
reporter at own expense, minor attendance needs prior court order (Rule 12.407).
Two unique form links inventoried (Financial Affidavit Short Form external,
Job Search Log internal). Generic Alvarez H1 and middle initial source variant
recorded; no legal merits or enforcement-form analysis expanded.

Cloud checked saved resolved URL validation against the original HTML. No substantive receipt correction required. Receipt:
receipts/person-hillsborough-hearing-officer-sabrina-frey.json. Saver:
review/local-frey/prepare-save.py --save (one-shot, do not re-run after advance).
38 citations, artifact bytes/findings readback, identical replay, prior facts and
finalized reports preserved. Next Chardean Hill. County/statewide remain incomplete.

## Hearing Officer Chardean Hill — capture5071 / packet91

LocalQwen3.8 completed review/local-hill with exit0. Cloud verified profile,
contacts, scope and save script. Hana Newberry, Administrative Assistant;
813-272-5176; CS4@fljud13.org; Edgecomb Room 480, 800 E. Twiggs Street, Tampa 33602.
Phone/tel/aria agree; visible email matches referral table but saved mailto
target 'mailto: CS4@fljud13.org' carries a leading space - discrepancy preserved,
not imported. Zoom 819-7386-0002, no password required; telephonic appearance
(929) 205-6099 with notary/oath at start; Zoom video exempt from notary.
October 2026 table CSEHO-4 (51-67), Chardean M. Hill matched by contacts
(middle initial preserved, not expanded).

Four basic topics save identity/contact/assignment, communications, documents
and appearance/access. Profile DOR Title IV-D hearings remote Zoom/telephone;
documents filed with clerk at least 3 days before (only published time
condition); failure-to-appear may result in orders; electronic recording,
reporter at own expense, minor attendance needs prior court order (Rule
12.407). Three unique form links inventoried (Financial Affidavit Short Form
flcourts.org, Long Form flcourts.gov - domain variants preserved; Job Search
Log internal). Generic Alvarez H1, name variant and mailto space recorded;
affidavit domains retained as link metadata rather than a conflict. No legal
merits or enforcement-form analysis expanded.

Cloud checked saved resolved URL validation against the original HTML. Receipt:
receipts/person-hillsborough-hearing-officer-chardean-hill.json. Saver:
review/local-hill/prepare-save.py --save (one-shot, do not re-run after advance).
42 citations, artifact bytes/findings readback, identical replay, prior facts and
finalized reports preserved. Next Nancy Lawler. County/statewide remain incomplete.

## Hearing Officer Nancy Lawler — capture5073 / packet92

LocalQwen3.8 completed review/local-lawler with exit0. Cloud verified profile,
contacts, scope and save script. Gianna Levy, Administrative Assistant;
813-272-5363; CS5@fljud13.org; Edgecomb Room 480, 800 E. Twiggs Street, Tampa 33602.
Phone/tel/aria agree and match the referral table; visible email matches mailto
target and referral table (no mismatched contacts on this profile). Zoom
857-0834-7715, no password required; telephonic appearance requires notary/oath
at start; Zoom video exempt from notary. October 2026 table CSEHO-5 (68-83),
Nancy W. Lawler matched by contacts (middle initial W preserved, not expanded;
roster label remains 'Nancy Lawler').

Four basic topics save identity/contact/assignment, communications, documents
and appearance/access. Profile DOR Title IV-D hearings remote Zoom/telephone;
documents filed with clerk at least 3 days before (only published time
condition); failure-to-appear may result in orders; electronic recording,
reporter at own expense, minor attendance needs prior court order (Rule
12.407). Two unique form links inventoried (Financial Affidavit Short Form
flcourts.org, Job Search Log internal). Generic Alvarez H1 and the
Lawler / W. Lawler name variant recorded. No legal merits or enforcement-form
analysis expanded.

Cloud checked saved resolved URL validation against the original HTML. Receipt:
receipts/person-hillsborough-hearing-officer-nancy-lawler.json. Saver:
review/local-lawler/prepare-save.py --save (one-shot, do not re-run after advance).
39 citations, artifact bytes/findings readback, identical replay, prior facts and
finalized reports preserved. Next Chris Phillips. County/statewide remain
incomplete.

## Hearing Officer Chris Phillips — capture5075 / packet93

LocalQwen3.8 completed review/local-phillips with exit0. Cloud verified profile,
contacts, scope and save script. Zachariah Fontenot, Administrative Assistant;
(813) 272-5859; visible email CS6@fljud13.org; Edgecomb Room 490, 800 E. Twiggs
Street, Tampa 33602. Phone/tel/aria agree and match the referral table. Visible
email matches the referral table CSEHO-6 row, but the saved-HTML mailto target
is CS1@fljud13.org (CSEHO-1 address); mismatch preserved, not imported, no
message sent. Zoom https://fljud13-org.zoom.us/j/9372638539, Meeting ID 937 263
8539; telephonic appearance (929) 205-6099 same Meeting ID. October 2026 table
CSEHO-6 (84-99), referral table 'Christopher Phillips' matched by contacts
(source name variant preserved; roster label remains 'Chris Phillips').

Four basic topics save identity/contact/assignment, communications, documents
and appearance/access. Profile DOR Title IV-D hearings remote Zoom/telephone;
documents filed with clerk at least 3 days prior (only published time
condition, preserved literally); failure-to-appear may result in orders;
electronic recording, reporter at own expense; Zoom camera-on and no-notary
conditions; telephonic notary condition; Rule 12.407 notice. Forms tab 'TBD'
(no form links). Generic DNN container H1 'Hearing Officer Phillips' recorded.
No legal merits or enforcement-form analysis expanded.

Cloud checked saved resolved URL validation against the original HTML. Receipt:
receipts/person-hillsborough-hearing-officer-chris-phillips.json. Saver:
review/local-phillips/prepare-save.py --save (one-shot, do not re-run after
advance). Citations, artifact bytes/findings readback, identical replay, prior
facts and finalized reports preserved. Next Lila Stello. County/statewide
remain incomplete.

## Hearing Officer Lila Stello — capture5077 / packet94 (final officer)

LocalQwen3.8 completed review/local-stello with exit0. Cloud verified profile,
contacts, scope and save script. Brenda Parrish, Administrative Assistant;
(813) 272-5267; visible email CS2@fljud13.org (mailto target cs2@fljud13.org,
same address modulo case - recorded, not a material mismatch); Edgecomb Room
490, 800 E. Twiggs Street, Tampa 33602 (source street line publishes
street+room with a non-breaking space). Phone/tel/aria agree and match the
referral table. October 2026 table CSEHO-2 (17-33). All sources publish 'Lila
Stello' (no name variant).

Four basic topics save identity/contact/assignment, communications, documents
and appearance/access. Profile DOR IV-D hearings remote Zoom/telephone;
documents filed with clerk at least 3 days prior (only published time
condition, preserved literally); failure-to-appear may result in orders;
electronic recording, reporter at own expense; Zoom no-notary condition
(emphasized 'not'); telephonic notary-at-hearing-start condition; Rule 12.407
notice. Zoom https://fljud13-org.zoom.us/j/4111036983, Meeting ID 411 103 6983
(contact block dashed form 411-103-6983 preserved); Password: Not Required.
Forms tab: Financial Affidavit - Short Form + Job Search Log (link inventory
only, contents not reviewed). Biography button targets '#modalboxcsvNWVC' with
no matching element in the saved HTML (no biography content). Source's own
'remotelyby' missing space preserved verbatim; DNN container H1 'Judge Alvarez'
recorded. No legal merits or form-content analysis expanded.

Cloud checked saved resolved URL validation against the original HTML. Receipt:
receipts/person-hillsborough-hearing-officer-lila-stello.json. Saver:
review/local-stello/prepare-save.py --save (one-shot, do not re-run after
advance). Citations, artifact bytes/findings readback, identical replay, prior
facts and finalized reports preserved. Next shared county followups (no
officers remaining). County/statewide remain incomplete.

## October 18 cloud followup bundle — not yet saved

The execution override is cloud work after the existing Qwen shared-access
code-repair assignment finishes. Do not launch another local assignment. Its
completion still requires source/code/test review; do not accept a placeholder
`code-test-results.txt` or a worker success label without actual test results.

Cloud evidence is staged independently in
`runs/county-hillsborough/2026-10-16/review/cloud-material-followups/`.
`prepare-bundle.py` validates original/extraction hashes and all finding citations,
then writes `cloud-followups-bundle.json`: 24 findings, 109 artifact hashes,
87 citation occurrences. It does not write the database or advance run state.
Resolve and accept the shared-access checkpoint first; then merge this bundle
into a new immutable packet, preserving all predecessor findings. Use the actual
new predecessor ID, never assume a sequence number. Validate through
`flwu.baseline_capture` in a temporary database before the reviewed real save.

Source traversal for later refreshes:

- The official Administrative Orders page has separate General, Civil, Criminal,
  Probate/Guardianship, Family, Juvenile and Local Rules tables. Read row labels
  with actual anchors. Do not construct filenames: older links omit `S-`, while
  Local Rules 1 and 2 use `rule1.pdf` and `rule2.pdf`. Follow the saved index links.
- Material order reviews cover civil/access subjects, not every indexed order.
  Acquisition manifests and review batches preserve collection versus actual
  content-review scope. `remaining-material-scope-plan.json` records the last
  four selections and exclusions. Do not expand criminal/diversion manuals merely
  because an administrative table lists them.
- A-2026-046 defaults to January 1, 2027 except stated clauses; many transitions
  are January 5. A-2026-052 separately states September/October 2026 changes.
  A-2026-048 states a 2027 acting-judge term; A-2025-040 supplies the 2026 term.
  Preserve these statements without promoting future assignees into the October
  roster or deciding authority conflicts.
- The original PDF text sometimes omits handwritten entry dates. Render the
  signed page; retain a separate hashed visual transcription with an extraction
  timestamp. Do not alter the original extracted text. Jury-management
  S-2025-028 has a sixth physical page containing the panel-guideline attachment;
  its vertical exempt-case column requires visual inspection. Preserve its
  wording separately from the body’s discretion language.
- `valkenburg-bounded-recheck.json` retains the current official profile and its
  actual standing-pretrial link returning 404. This is missing evidence, not a
  reviewed criminal order. Existing basic procedures and civil-forfeiture review
  remain available. Do not pursue exhaustive criminal alternatives.
- The official county parcel-information page links the Property Appraiser.
  `property-appraiser-navigation-reviewed.json` supports the requested Tax
  Assessor navigation label and verified homepage. No property search was run.

`person-receipt-audit.json` records exact profile-URL reconciliation: 69 saved
judge identities and 15 officers. Eighty-six receipt files include earlier Polo
and Smith versions; those do not add two current judges. Structural person/officer
validators and recursive evidence checks passed 9,251 citation occurrences. This
is not a new substantive review or proof of named rotating senior coverage.

`comparison-freshness-validation.json` records the bounded read-time comparison
repair: 116 history/checkpoint tests passed; refreshing acquisition metadata in
718 nested evidence objects across 427 existing findings left comparison facts
unchanged. No production history was rewritten. See BASELINE_CAPTURE.md for the
precise ignored fields and limits. County acceptance, directory projection,
visual review and publication remain distinct outstanding steps.
