> Execution policy: [use the invoking model](../../workflow/MODEL_EXECUTION.md) in Codex or codex-local. This supersedes all named-model and mandatory-delegation directions below. Dated progress notes are historical, not current assignments.

# Miami-Dade research handoff

Active October18,2026. Cloud-only research; Hillsborough research accepted5083
with source limitations; its final directory UI/publication remains pending.

## Pinned state

Run: `runs/county-miami-dade/2026-10-18`.
Stream: `manual_research:county-baseline-v1:595a1bb41e68`.
Latest **5599 / packet261**, `931b9aa1e2021299083ea044fc16c056fde6abd3b8acc5466a69fe9335ea95f0`.
Research accepted with documented source limitations:123 judges,19 magistrates,11 senior judges and clerk. All28 person/source gaps retain explicit dispositions; unavailable content remains unreviewed. County remains unpublished; database checkpoint incomplete/nonfinalized denotes the separate publication gate, not unfinished accepted research.
Acceptance: review/county-final/county-research-acceptance.json. Current structural audit matches all153 roster IDs and clerk with no errors; coverage matrix links civil/shared, clerk, access, AI/professionalism and public resource reviews. Historical partial review notes are reconciled against final receipts. Original extraction retained when citation required an LF-normalized derivative.
3654 artifacts/587 findings read back; exact replay verified; five finalized reports unchanged.35 directory/checkpoint tests passed. Directory preview5591/site-v2 remains pending final refresh and visual/keyboard/responsive QA.
Next county: Palm Beach. Maintain the separate Miami-Dade directory publication gate.

## Official source discovery and extraction

Start https://www.jud11.flcourts.org/About-the-Court/Judges/Judicial-Directory .
Follow its actual Judicial Directory PDF anchor:
https://api.jud11.flcourts.org/api/judicialdirectory . Both returned200 onOctober18.
Originals/text/URL/retrieval timestamps/hashes: run `review/acquisition.json`.
The PDF endpoint returns PDF bytes despite having no filename extension. Detect
PDF by signature, not URL suffix. Preserve extraction and original separately.

HTML renders `.jd-division` within `section.jd-section`; court-group heading is
`h2.group-header` in the ancestor section, not the immediate parent `.jd-grid`.
Each division has `.jd-division-heading`; each `.jd-card` has `.jd-header`,
`.jd-footer` role and section links. Group and division are necessary because
both circuit and county groups have a Civil Division. The same person can have
many division cards and many section-specific URLs. Review all relevant section
pages for one person before advancing; do not split one person into multiple judges.

Seven problem-solving cards omit `data-judgeid`. Parse the actual `judgeid` query
in each section link and require consistency with any card attribute. Those seven
cards repeat IDs elsewhere. Eleven senior cards have attributes but no section
links; preserve that missing-link limitation and obtain contacts from official
senior/PDF sources without inventing detail URLs. Three leadership cards outside
`.jd-division` lack attributes; chief1006 and deputies1100/1054 also occur in the
division inventory. Preserve their labels and roles. Initial raw extraction
`review/roster-card-inventory.json` counted `None` as an ID (154); authoritative
corrected `receipts/roster-opening.json` and capture5085 contain153 actual IDs.
The failed extract is retained as audit evidence, not used for the work queue.

## Next steps

1. Roster reconciled5087 and corrected5089; latest facts in `review/walsh/source-review-partial.json` supersede the old receipt’s false CG01 discrepancy. Names EllenSue/EllenS and JulieHarris/JulieH retained; chiefJAroom header24.238 vsrow24.230 recorded. PDFfooter generationtime is not an effective date.
2. Walsh5093, Simon5095, Areces5097 and Arzola5103 complete. Review Beovides1100 CA03/CA35 and reconcile material additional-assignment evidence before moving on.
3. Inventory only material civil/shared orders and court/clerk operational pages.
   For criminal/family/diversion assignments basic contacts, links and operating
   procedures suffice. Do not expand merits review.
4. Save immutable additive checkpoints using the tested opening helper pattern:
   exact predecessor guard, temporaryDB validation, production save, exact replay,
   allfact/artifact readback and unchanged finalized reports. Update pinned notes.

Acquisition helper: `review/acquire-opening.py`; corrected persisted inventory:
`review/save-opening.py`. Do not rerun either to overwrite this capture. New source
observations use a new manifest/version and checkpoint. No local worker.

## Administrative-order discovery and citation integrity

The official `/General-Information/Administrative-Orders` page is a dynamic shell.
Its actual script `/js/administrative-orders.rim31pwp33.js` exposes the public
`https://api.jud11.flcourts.org/api/adminorders` index (2056 rows observed).
Use each returned `fileId` with `/api/adminorders/view/{fileId}`; do not substitute
SharePoint login URLs for the public document. Save the HTML, script, JSON index
and selected row. Match title, `caseNumber`, `aoNumber` and `fileId` together:
26-15/26-2 is a judicial appointment, not the AI order in case26-1. An index date
is a separate statement from a document's explicit effective date.

CBL PDF embedded links are in `review/walsh/cbl-embedded-links.json`. Four legacy
order URLs returned404 via HTTPS; raw failure bodies are retained. The extractor
warned about replacement characters in those failure bodies and yielded empty
text; this is not evidence of the unavailable orders' contents. Public index
alternatives are being reviewed for relevant civil assignment/discovery/arbitration
orders. Do not expand into unrelated same-number orders or resolve authority
conflicts as a prerequisite to completing the baseline.

Normalize newly extracted text to LF before computing and saving its hash. Keep
raw original bytes unchanged. Existing CRLF extraction must remain preserved;
if the citation validator normalizes it through `read_text()`, create a separately
hashed normalized derivative and point the new citation to that derivative.
Never change old extraction bytes beneath an existing artifact hash. Walsh's
`save-source-review.py` records the bounded correction pattern and validates
quotes through `research._citation` before persistence.

Packet04: AO13-08 arbitration,06-09 discovery and Revised79-2 transfer originals fully read; selected4pages visually checked. ICA exception to general CBL procedures retained. June2006 discovery copy has blank execution day/signature; no exact effective day inferred. CBL label79-1 differs from actual Revised79-2/Case79-1. Amended16-12 and sealing10-10 originals remain unavailable through linked URLs/index. These are source gaps, not resolved conflicts. Judge remains active. Temporary validation rejected a new status enum and a citationless gap finding; both corrected before production save; rejected drafts retained as audit files.

## Simon checkpoint lessons

Inspect all current email anchors: her header displays and links to
`earagon@jud11.flcourts.org`, but the special-set paragraph displays that address
while targeting `mperezmercado@jud11.flcourts.org`. Save the mismatch; do not
import the latter as a verified current assistant. Cached browser text can expose
a target parenthetically; compare the retained current HTML before interpreting it.

Detect image-only PDFs when extraction yields only page markers. Render and read
every relevant page, retain the empty extraction, then save a separately identified
visual transcription with source hash and review timestamp. Simon's AO06-09 scan
matches the previously read textual original, including the blank execution day.
Different bytes remain separate originals. The content comparison does not justify
silently copying a date or signature from another version.

DOCX footer extraction matters: the pandemic evidence memo states May5,2020 in
its footer, omitted from initial paragraph extraction. Preserve table cell structure
for blank case-management forms; blank cells are not deadlines. Judge-specific
fee templates differ: Simon uses10/10/10 with distinct entry/compliance/receipt
triggers. Do not reuse Walsh's timings or ordinary-calendar cancellation steps
for Simon's court-only special-set cancellation.

## Areces checkpoint lessons

Record permitted exceptions to a communication ban. Her no-unsolicited-email
instruction coexists with required settlement/dismissal notices and special-set
cancellation requests by email. The division mailbox is not a general-purpose
personal assistant email. Telephone inquiries remain the ordinary route.

Do not inherit Simon's approval requirement for unilateral settings or her
withdrawal-form stay: Areces publishes different conditions. Keep ordinary motion
and special-set cancellations separate. Her header's Zoom calendar-call statement
and later January2026 cancellation direction are both preserved, as are the
HTML/form descriptions of hearings near the trial-period boundary. Compare
same-titled withdrawal forms by actual bytes and contents before reuse; preserve
two URLs even when their bytes match. A printed portal-address anomaly is not
authorization to rewrite the source or recommend the malformed address.

## Arzola checkpoint lessons

Case-management headings can cite a later amendment than the linked PDF. Verify
the actual PDF caption and superscript footnotes: Amendment10 plus footnote1 is
not Amendment101. Preserve dated local filing-cohort tables as historical evidence;
do not reissue their2021 deadlines as current requirements. Save actual cell
associations and the signature-date image when extraction moves the day number.

The two fee forms have different disclosure triggers. Preserve the entitlement
form's later-of clause and the literal deposition-of-moving-party prerequisite;
do not substitute an expert-deposition requirement based on another judge's form.
Likewise, a greater-than-one-hour scheduling instruction that tells users to book
one hour is an ambiguity to retain, not permission to invent extra slots.

Same-titled disqualification PDFs differ in their final duration clause and page
break. Retain the scanned original and a labeled visual transcription; never copy
an entire textual version into a different original without checking all wording.
Generic case-management downloads can match extracted text while differing in
bytes; preserve each original and separate judge-specific additions.

## Beovides checkpoint lessons

A search result can still describe FC26 while its live URL serves CA03. Preserve
requested URL, resolved URL and actual heading; never infer a section from the URL
parameter alone. Compare assignment orders' operative dates with index dates and
execution dates. Temporary assignments can specify an end date omitted by a later
order's recital; record all statements without deciding their legal interaction.
A current ND02 roster/profile naming Moore does not authorize copying her staff
into Beovides's record. Reuse the collected Moore source when her own turn arrives.

Read the actual rescission clause:24-1 expressly rescinds Revised79-2, which remains
in Walsh's historical linked evidence. Fee prerequisites vary: Beovides's form
requires compliance certification but lacks Arzola's moving-party deposition clause.

## Cynamon checkpoint lessons

An automatically generated notice does not establish special-set approval: wait
for the specific Approved status required by this profile. Ordinary cancellations
and special-set cancellations have different routes. Record an explicit no-stay
withdrawal clause rather than borrowing another judge's thirty-day stay.

A failed direct order link stays a failed source even when another official copy
is already in the corpus. Store the404 body separately from successful citations;
reuse the other copy with its own URL, timestamp, hash and reviewed scope. The
A10 match permits scoped prior review reuse, not a claim of full criminal review.

## Del Rio checkpoint lessons

Public profile review completion is distinct from obtaining referenced originals.
Carry missing named forms into state.open_evidence_gaps and county acceptance;
never turn a completed contact/profile receipt into a claim that those forms were
reviewed. Check actual anchors, alternate official section links and site scripts
before guessing a hidden document endpoint. Search results for another judge's
similarly named template do not establish applicability.

Special-set slots shown open in CourtMAP are expressly reserved for other cases
on this profile; email the court for dates. Ordinary unilateral settings have a
separate qualified permission. Do not import another judge's booking workflow.

## Diaz checkpoint lessons

Separate general civil CA30 from asbestos-only CA42 even though the contact block
and document menu match. Their notice units, calendar caps, required responses and
cancellation routes differ. A shared menu can retain a prior judge's signature;
record that form's attribution without silently replacing it. Match shared orders
by original hash before reusing their reviewed scope. An image-only exhibit worksheet
requires image review; blank extracted text does not mean a blank form.

## Dimitris checkpoint lessons

Distinguish a courtesy-copy duty for documents filed within72hours of a hearing
from an advance filing deadline. Keep the action of scheduling a Daubert/MSJ
hearing before calendar call separate from holding it before the trial period.
A one-hour-or-more form threshold differs from a more-than-one-hour HTML threshold.

Compare withdrawal and fee forms individually. These withdrawal forms use15days,
not30, and differ on mailing versus mailing plus email. The fee order requires
expert depositions or affirmative waivers, completed discovery and post-discovery
conferral; its list preparation and delivery periods are separate. Preserve a
legacy e-Courtesy route rather than silently substituting CourtMAP.

### Jean checkpoint64
Both profiles and shared DOCX collected; contact anchors and Word relationships checked. Basic operating sections reviewed; criminal merits deliberately excluded. Guide Division15 caption versus F061 link association retained. Citation excerpts are bounded to relevant passages. Production readback, exact replay and five finalized reports verified.

### Ramiro Areces checkpoint65
All matching roster cards examined: AP01 plus F070. Local rule R-3-1 and official order-index API17-02 A1 (case25-1) plus original17-02 (case17-1) retained; original and amendment reviewed, with source dates and differences. Avoid similarly numbered criminal reassignment rows. Directory original reused for address. Contact anchors agree; three PDFs have no URI annotations. All984artifacts/205facts readback, exact replay, fivefinalized unchanged. Next de la O has two cards/sections311and125; aggregate both.

### De la O checkpoint66
AP03/F012 both reviewed; Division12 fivepage guide preserved, contacts/basic sections1–8 and11(a),(c) reviewed. Direct judge/JA emails and F012 no-duplicate-copy instruction retained. Hearing confirmation email vs phone discrepancy preserved. PDF targets match printed text. Shared appellate reviews reused from Areces5211 without another fetch; personal material not inherited. 1003artifacts/208findings readback and exact replay; fivefinalized unchanged.

### Butchko Sanchez partial checkpoint67
Profile/linkedformbodies reviewed;PDFwithdrawal visuallyconfirms Hanzman2018/stay;do notinfercurrentapplicabilityfromlink. Wordstructurefollowups remain. Separate specialsetformversions and profile contradictions preserved. Rawcaptures/visualtranscription/screenimages saved,1031artifacts217findingsreadback,exactreplay/fivefinalizedunchanged.

### Butchko Sanchez completed checkpoint68
Wordextra parts reviewed;CMOprefilledfooter retained separately fromblankcaption. SharedGreenAO24-20/06-09 reviews reused. 19topics,13numeric/11relative requirements,95citations validated;1041artifacts/218facts readback/exactreplay/fivefinalized unchanged. Conflicts preserved,unavailablegenericprotocol remains evidenced gap.

### Hernandez checkpoint69
CriminalF009 only:profile contacts/basic sections1–3,agreedorder,5(a),(c)reviewed;fulloriginal retained,criminalmeritsnotreviewed. Directoryaddress/identity reused. Mailto matches.1050artifacts220findingsreadback,exactreplay/fivefinalizedunchanged.

### James checkpoint70
F019basicproceduresandsharedservicememorandumreviewed;criminalformslinkinventoryonly.29citations,1065artifacts222findingsreadback;exactreplay/fivefinalizedunchanged.

### Altfield checkpoint71
F020basicreviewcomplete;PDFpage2contacttarget mismatch visuallyverified,biographyassignmentconflictretained.34citations1081artifacts224factsreadback,exactreplay/fivefinalizedunchanged.

### Bloch checkpoint72
F001profile basicreviewcomplete;directoryaddress/identity and sharedservicepolicyreused.1090artifacts226findingsreadback/exactreplay/fivefinalizedunchanged.

### Brinkley checkpoint73
F004basicreviewcomplete;room201/200andremotepermissiondifferencespreserved. AO21-11collectiondistinctfromlimitedreview.40citations1106artifacts228findingsreadback/exactreplay/fivefinalizedunchanged.

### Cabarga checkpoint74
F017basicreviewcomplete;JAidentityandpublishedhearingmailboxnotconflated.1115artifacts230findingsreadback/exactreplay/fivefinalizedunchanged.

### Delancy checkpoint75
F005basicreviewcompleted;datedroom/bailiffconflictandmisleadingfilenamepreserved.1130artifacts232findingsreadback/exactreplay/fivefinalizedunchanged.

### Clerk civil services review — October 18

From the clerk civil hub, follow `e-filing.page`, `judgments.page`,
`mortgage-foreclosures.page`, `official-records.page`, and
`civil-certified-copies.page`. Saved originals, resolved URLs, HTTP statuses,
retrieval timestamps and text hashes are in
`runs/county-miami-dade/2026-10-18/review/clerk-services/acquisition.json`.
All five main-page bodies were reviewed; their links alone do not establish
review of the linked documents or operation of interactive services.
`source-review-final.json` contains separately attributed findings;
`contact-links.json` preserves actual contact targets (reviewed targets agree
with visible contacts, allowing the telephone country-code prefix).
`followup-queue.json` identifies material civil forms/evidence instructions for
reuse checks and review before county acceptance. Continue the prior clerk-core
queue for district-location and jurisdictional-transfer documents.

Keep the foreign-judgment page's $30,000 thresholds separate from the civil
hub's $50,000 / literal “exceeds $50,001” wording. Record the discrepancy without
choosing a controlling threshold. The e-filing page both excludes five-day
summons in its opening paragraph and permits residential five-day eSummons
later; retain both and the latter's posting-related copy/envelope conditions.
The eCourtesy sentence belongs to the criminal subsection. Do not import it
into civil order-routing rules. Fees and operational statements are observed
source assertions, not proof of their legal currency or a new effective date.

For persistence, the bounded `review/clerk-services/save.py` copies packet213,
validates quotations against saved text, freezes source/review artifacts,
dry-runs the checkpoint in a temporary database, checks the production
predecessor, and saves packet214. It verifies exact replay, all artifact bytes,
all finding facts and preservation of finalized reports. It is a one-shot
checkpoint helper, not a reusable command to rerun after the state advances.

### Linked clerk documents and interactive PDF fields

`review/clerk-documents/acquisition.json` retains six linked PDFs: refund514,
April20,2020 evidence filing instructions, Portal Document Submission Standards,
garnishment726 (Crt.08/24), surplus933 (Rev.07/24), and return-note694 (Rev.04/26).
All seven pages were read and visually inspected, with annotations retained.
Six reviews entered packet215; `followup-disposition.json` separates those from
remaining summons/auction links. Portal standards' 8.5x12 letter-size statement
conflicts internally with its 8.5x11 statement; preserve the literal source.
The note-return form's Civil@miamidade.gov targets match visible text; Room7.209
and9am–4pm pickup are service-specific. Five-to-ten business days is an estimate
from receipt, not a party deadline. No document action or message was sent.

A later widget inspection corrected packet215's refund-mailbox statement.
`review/clerk-refund-widget/source-review-final.json` preserves widget143's
raw PDF object, choices, current/default values and source hash. The displayed
blank selection conceals location mailboxes; two raw option pairs have different
values (SouthDade:none/address; traffic:Caleb/address). Do not infer a routing
address from a blank/default/export value. Inspect widgets with PyMuPDF as well
as rendering, normal text and annotations. Packet216 preserves the correction
without rewriting packet215. The acquisition script's deprecated fitz import
was changed to pymupdf; subsequent extraction/render/field checks completed
without that warning.

### District locations and February2020 transfer instructions

`review/clerk-locations/acquisition.json` contains seven HTTP200 source pages:
Soto, district index, South/North Dade, Hialeah, Coral Gables and Caleb. Full main
content reviewed in packet217. Ordinary civil hours are weekdays9am–4pm;
North/South Dade and Caleb extended hours have express service restrictions,
not generalcivil access. Soto lists Recorder5.243 and civiljury3053497775,
which differ from other clerk pages; preserve both. MiamiBeach closure redirects
pretrial/specialsets toSoto14A and traffic/misdemeanor toGerstein1-1.

`review/clerk-transfers/acquisition.json` preserves the two-page February2020
jurisdictional-transfer instructions, fully read/visualchecked, and five503
Render responses for04-05,06-41,14-13,16-05,16-05A1. These are failed routes,
not proof the orders do not exist. Check prior captures by normalized fileid
and official orders index/API before fetching replacements. Relatedcase,
jurisdictionalamount,samedivisionconsolidation and crosslocation/crossjudge
transfers have distinct routes; preserve all. The2020 Bailey/Abreu/Janowitz
references and3056362260/rchavez contact are dated source assertions, not new
current-person verification. The document's first-person author is not named.
CourtMAP templates are referenced, not included or newly reviewed.

### Recovery of clerk-linked orders

`review/clerk-district-orders/index-source.json` records the fresh official
adminorders index. Match the five failed Render GUIDs case-insensitively to its
fileId rows, then fetch `/api/adminorders/view/{fileId}`. All five returned PDFs;
old503responses remain preserved.04-05(4pages),06-41(5pages),16-05(2pages),
16-05A1(2pages) fullyread;14-13(7pages) collected withpage1family-scope-onlyreview.
Do not expand14-13merits review merely because clerk civilhub links it.

04-05 has historicalZIPdistricts/15000limits/oldvenues; indexcase04-02 differs
fromPDF04-1. EffectiveJuly6,2004; executionJunedayblank.06-41effectiveJanuary8,
2007; November2006dayblank. Its AttachmentA pages3–4 are images omitted by normal
extraction; renderedpage review and a labeled selected-field transcription are
saved. CBLaddendum greater75000 versus anyamount categories remain historical.
16-05April28,2016 andA1May18,2016 retain their distinct May/July versusJune/August
migration dates and all-pending-case notice requirements. No authoritycontrol
resolution or presentcalendar/deadline calculation was performed.

### Summons versions and auction access

`review/clerk-summons/acquisition.json` retains all seven actual summons URLs.
Both314corporate routes return identicalJuly2026PDFbytes; keep retrievalpaths.
Combined070multilingual isDecember2025; separateEnglish/Spanish/French/Creole
forms areJune2026. Englishrequirements read; separate languageforms scoped to
revision,fields,contacts,response/ADAnotice,notcertifiedtranslationequivalence.
Six renderedpage checks preserve locationtable mappings; NorthMiamiBeach label
and dated namedADAcoordinator differ from other currentpages/role-onlyforms.
AllPDFannotations/widgets inspected; oldcombinedformclerkfooter targets
miami-dadeclerk.com despite printedclerk.gov. No messages/forms submitted.

The officialclerk-linked auctionhomepage returnedHTTP403,originalresponse retained
in `auction-acquisition.json`; its proceduralcontent is NOT reviewed. Follow up
with browser/publicalternativeinstructions withoutregistration,bidding/payment.
`followup-disposition.json` supersedes the earlier linkqueue status for these
summons URLs without overwriting historical queues.

### County gap reconciliation

`review/gap-reconciliation/gap-reconciliation.json` preserves all35prior entries
and their dispositions. Two baseAO21-10 collection gaps (947,2184) are resolved
by the later Ihekwaba receipt governing_rules[0], original3fdf9c96… PDF and full
three-page review. State retains33entries; priorcheckpoint retains all35.
Triage:21civil/sharedfollowups,2unpublished/unverifiedcontactentries,3failedroutes
withindependentsubstantivesources,7lower-prioritybasic-scopefollowups. Triage is
not a final acceptance determination; missingcivilforms/truncatedinstructions
remain distinct from conflicts and failedURLs with alreadyreviewedalternates.
Do not reopen base21-10collection or allfiveclerkRenderorder collections.

Auction HTTP403 independently confirmed by web.open. CUA inventory had noenabled
browsers and createBrowserTab(iab) returned Browser is not available: iab; this
is a browser-capability limitation, NOT a successfulbrowsercheck or evidenceof
auctioninstructioncontent. Seek officialclerk/court publicalternatives next.

### Working division routes and historical foreclosure memoranda

The old `/About-the-Court/Court-Divisions/Civil` still503s, but its actual
navigation anchors reveal `Circuit-Civil` and `County-Civil`, bothHTTP200.
`review/shared-followup/division-acquisition.json` retains originals; mainbodies
reviewed and actual links queued in `material-link-queue.json`. Reconcile those
links against existing orders before collecting again. Newhub is an alternate
information source, notproof of identicaloldcontent. Courtdivision8–5hours differ
fromclerk9–4; countyhubMiamiBeachlisting doesnotestablishreopening. Countyhub
stilllinks26-04AI despite laterrescissionalreadyretained; preserve chronology.

Officialdomainsearch found `/docs/CIV10-B.pdf` and `/docs/201506220938.pdf`.
CIV10-B3pagesread/visualchecked; handwrittenJuly19,2010entry/July26effectiveness
transcribed, originalOCRretained. Old9am/9:45calendar ishistorical,notcurrentadvice.
2015memo15-A24CA01 is13scannedpages; ordinaryextractionblank. Onlypages1–2reviewed
sofar; pages3–13includingExhibitA remainqueued(renderedPNGsready). Do not mark
thisdocumentfullyreviewed or substituteitforunidentifiedjudge/auctioninstructions.
Quotevalidation initiallycaught CRnormalizationdifference inHTML; normalized
reviewquote tosavedtext, thenvalidationpassed; nooriginalbytesrewritten.

### Completion of scanned2015foreclosurememo

`review/foreclosure-2015-complete/source-review-final.json` replaces the partial
review with a new immutable version after all13physicalpages were visuallyread.
Originalblankextraction and priorpartialreview remain. Page-keyed manualnotes
are labeledparaphrases,notOCR/verbatimtext. Physicalattachments order isB,A,C:
14-10originalnoteorder/form, cancellationprocedure, FJUDtemplate. Memoentry
June20,2015/effectiveJuly1,2015;14-10May14,2014;formrevisionJune17,2015.
Historical8:15walk-in/8:30cutoff,48hpresumedemergencynotice/5dayemergencywindow,
originalnotehandling,residentialformexceptions andoldsurplus/retentionstatements
remain attributed; do notpresentascurrentdeadlines orcontacts. TheFJUDreferences
AO09-18electronicauctions, a materialofficialalternativelead for the403vendor.
NoPDFlinks/widgets found; allrenderedpagehashes retained inannotations-visuals.

### Shared-link coverage audit and auction authorization

`review/shared-coverage/link-audit.json` enumerates16distinctdocumentURLs from
bothdivisionhubs. NormalizedURLmatchingfoundone(AO24-20); absenceofURLmatchdoes
NOTprovemissingoriginal. Nextcomparetitle/casenumber/fileId/hashagainstretained
receipts beforefetching/reviewingagain. Reviewscope mustalso match; collection
orfirstpartialreviewisnotcompletion. Existing22-02,26-04/26-15,23-31A1,etc. have
alternate-sourcecandidates inearlierreceipts. Theauditremainsintermediate.

AO09-18case09-1,fileIdd70a8ab3-d53a-4504-ba0b-7568cdc40600,wascollectedfromthe
publicAPIandfullyread/visuallychecked2pages. Sameordernumbercase09-2isjudicial
assignmentandwasexcluded. December10,2009immediateeffect; onlineauction/mailnotice,
9amnoticewording/unchangedsaledate,courtorderrequiredtocancelpublicationnotices,
noplaintiffpresencerequired. Historicalauthorizationdoesnotestablishcurrentvendor
deposit/paymentinstructions; vendor403remainsalimit. Original,indexrow,annotations
andreviewstoredinshared-coverage; noauctiontransactionwasperformed.

### Hub-document collection and first review pass

`review/hub-documents/acquisition.json` nowretainsall16PDFsHTTP200. Fourexacthash
matches:0(AO24-20),1(AO24-01),5(AO22-02),14(AO26-04); reviewscopeverification
pending,notautomaticcompletion. `review-disposition.json` pinsstatusbyindex.
Newfullreviews6,7,8,15:hearingtechnologytable,AM23-Ctimeguidelines,23-31base,
23-31A1consumerdebt. Tableimageordinaryextractionomitscontent;visualparaphrase
saved. Exactly30minutesnotcoveredbyunder/longerthresholds. Hearingwaitranges
arejudicialgoals,notpartydeadlines. Consumerdebtoperativefilingrequiresresidence
branch,whereaspreambleFDCPAmentionssigningorresidence; preservebothwithout
rewriting. 23-31entryJune2/effectiveJune5,2023;A1July10,2024immediate;AMNov8,2023.
Eightothernewdocumentsremaincollected-only; reviewcommercial/sharedportions,
notexhaustivecriminal/familyprovisionsofstatewidecompilations.

### Hub reuse verification and related-case/emergency evidence review

`review/hub-followup` verifiesfullpriorreviewsbyhashandactualfacts forindices0
(Green24-20),1(Beovides24-01),5(GonzalezPaulson22-02),14(Cannava26-04withlater
26-15/SC2026-0673). Do not select earlierAIpartialreviewthatstillcalled26-15
uncollected. ReusefullPDFreviewdoesnotcomplete independentlylinkedforms.
Newfulltext/visualreviews2(21-2A1,3pages)and11(24-CL01/24AF01,2pages) complete.
Relatedcaseattachmentimagepages2–3manuallyreviewed/labeledparaphrasespreserved.
January8,2024immediateeffect;separateportalnoticewithininitialfiling,continuing
relatedcase disclosure. January22,2024emergencyevidencememoappliesofficialclosure
byChiefJudge,naturaldisaster/catastrophe;5BUSINESSdaysfiling/service,index,
conferral/correctedadmittedindex. Notordinaryallhearingrule.
Remaininghubdocs3,4,9,10,12,13needcivil/sharedscopereview; allalreadycollected.

### Listed-case reassignment orders

`review/hub-reassignments` saves scopedoperative reviews forhub12/13. AO26-07
February19,2026immediateone-timetransferselectedexistingCC/SPcasesfromND02toother
sections;full21pagescollected,operativepage1read andattachmentstructure sampled.
AO26-06A1February23,2026correctsbase26-06spreadsheet,selectedcasestoND04priority
docket;full23scannedpagesretained,operativepage1visuallyread andattachmentsampled.
Titleline saysAMENDING26-01 whilecaption/body26-06;preserveinternaldifference.
Lastspreadsheetpagecontains#N/A cells,notcaseIDs. Noindividualdocketstatus/actual
transferexecutionasserted. Theseordersdo notassignallfuturefilings. Case-list
preservation/operativeprocedurereview isdistinctfromunrequestedcase-by-caseaudit.
Remaininghubdocuments3,4,9,10:statewidecompilations/minors scopedto commercial/
sharedneeds,countyDCM fullreview. No additionalcase-listmeritsresearchneeded.
