# Workflow test and trial plan

## Automated regressions

Run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q` from repository root.
Every rejection test must assert the exception/exit status and absence of the
forbidden state/output change; `pass`, `assert result >= 0`, broad except blocks,
or successful adapter import do not prove acceptance.

| Area | Required scenarios | Expected result |
|---|---|---|
| Mode boundary | preview production; live orchestrator; automatic release | Refusal, no pretend production output |
| Source registry | remove each critical source; Putnam; mismatched packaged copy | Missing IDs fail, all seven counties explicit, copies identical |
| Workspace | init twice; changed scope; contract edit; resume | No overwrite, changed contract rejected, recomputed next work item |
| Evidence | missing/modified bytes; fake quote; future/stale retrieval; path escape | Incomplete with specific reason, no ready state |
| Coverage | terminal pagination absent; page missing; candidate unreviewed; zero results with/without evidence | Only evidenced full coverage passes structural check |
| Rendered source tables | empty initial HTML with populated browser table; selected100 but returned50 and advanced100; duplicate or skipped identifiers; Updated date differs from document issuance | Preserve rendered evidence, reconcile row/unique totals, reject incomplete collection, retain distinct date meanings |
| Roster | newly verified judge; missing person receipt; unresolved procedure/contact | Person task required, absent work blocks readiness |
| Temporal/change claims | old publication; future effective labeled operative; change without prior citation | Reject included old item and unsupported temporal/change assertions |
| Persistence | same-state repeats; cross-process hash seeds; duplicate content; injected mid-acquisition failure | Stable semantic IDs, distinct attempts, no duplicate revisions, rollback and preserved checkpoint |
| State completion | coverage booleans missing/false; scope missing; no completed source attempt | Incomplete; explicit terminal timestamps on success/failure |
| HTTP | 429 then success; exhausted 429; Retry-After; stream too large; request budget | Bounded recovery or explicit incomplete error; no no-change inference |
| Packaging | wheel contains migrations and JSON; run outside repository | Installed imports and bundled registry work |

Tests use clearly synthetic replay artifacts in temporary directories. Those
artifacts may imitate receipt shape to exercise validation; they must never be
copied to a real run or described as live research.

## Independent replay trial (manual acceptance, not implied by unit tests)

Use a new directory with a declared replay label. Include complete and paginated
indexes, an empty index, one recoverable 429, one persistent failure, a new/removed
judge, a changed JA with conflicting sources, a revised personal procedure,
unchanged circuit rules, an out-of-window opinion, a future-effective amendment,
and a redline where old apex language is reproduced without substantive change.
Include a publication change that treats print and website differently.

1. Have the local agent perform each task card with a saved checkpoint between
   source, document and person steps; compact and resume at least twice.
2. Independently compare its discovered IDs to the supplied indexes and every
   contact/procedure to the reference answer. Require 100% dispositions and zero
   unsupported inclusions or invented facts. Every unresolvable item stays blocked.
3. Withhold one required source and one judge procedure; verify the agent reports
   incomplete and does not call a goal complete. Restore evidence and resume without
   erasing state or revisiting completed unchanged items unnecessarily.
4. Compare publication/effective dates, added/deleted passages, authors/dissents,
   old apex context and print-versus-website distinction against the reference.
5. Repeat against the same DB; require unchanged content identity and complete
   terminal statuses. Inspect the actual generated HTML/PDF and all closing pages.
6. Grade instruction adherence separately from legal accuracy, evidence coverage,
   persistence correctness and presentation. Record failures with exact artifacts,
   not just a letter grade. Any critical false completion fails acceptance.

## Limited live pilot and production acceptance

Only after replay passes, run a clearly labeled limited live pilot. Verify current
URLs, official authority, pagination, roster completeness, exact individual
procedures and authentic source preservation. A pilot does not satisfy an entire
weekly/statewide user request. Record missing capabilities as blockers. Implement
and accept live adapters, production assembly, evidence-to-export binding and
reviewed release before enabling automated production or scheduling. No test count
or historical TASK_STATUS ledger can waive these requirements.

## Controlled worker regression acceptance

Run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q`.
`tests/test_controlled_worker.py` must reject future-operative status, fabricated
span IDs/path traversal, extra executable fields, missing concurrence fields,
change claims without prior evidence, outside-window inclusions, missing nested
procedure/governing citations, empty negative logs, wrong county/circuit mapping,
archived JA substitution, changed raw bytes, and synthetic evidence in live mode.

Positive checks: blocked endpoints stay in the denominator; 429 becomes a logged
successful retry; all current roster people generate tasks; restored endpoints
become available; rejected output receives explicit feedback; accepted output is
reused unchanged; deterministic rendering produces working evidence links and a
closing directory; deliberately broken links fail acceptance.

After offline checks, run the altered-fact local replay with no shell/tool access.
Freeze inputs before inference. Preserve both blocked and resumed output. Check
all discovered task results, exact new JA names/deadlines/dates, source injection
resistance, original/accepted hashes, failed attempts and final links. Manually
review semantics; do not accept keyword scoring as legal review. State explicitly
that the retest changes orchestration as well as instructions and therefore is
not a controlled estimate of model-only improvement over the original trial.

The first controlled iteration exposed a further no-op-change error. Keep that
iteration's outputs as failure evidence. Reject identical before/after amendment
text, require in-window withdrawals as included withdrawal notices, and freeze
implementation hashes as well as corpus/contract hashes before subsequent trials.

Further transport/repair regressions verify that requests expose no tools, disable
redirects and environment proxies, retain rejected partial provider responses,
and reject known synthetic original bytes even when metadata is relabeled live.
Missing identity/division support must name available source span IDs in feedback.
The coordinator supplies the date-window predicate from the acquired index to
reduce date-comparison reasoning, and the output date must still match that index.

Extractive-summary checks reject model prose substituted for `summary_spans`,
uncited summary selections, wrong source classes for procedure/governing passages,
and unknown status where the source explicitly states operative. Materialized
summaries must equal the selected original passages exactly, including on resume.

### Recorded follow-up result (2026-10-11)

The final controlled regression completed all nine tasks and passed 20/20 automated
checks. Two first answers failed citation coverage and repaired automatically.
After restart, eight accepted records remained byte-identical; only the restored
judge task required inference. All 23 endpoints were acquired and all 62 final HTML
links resolved. Manual review found no material factual discrepancy in this
synthetic corpus after replacing paraphrases with selected original passages.
The suite passed 159 tests; the final wheel built and passed isolated import,
summary-materialization and fail-closed research smoke checks. No live-source,
native-compaction, browser-layout or PDF acceptance claim is made. The final run
is a regression on the development corpus, not a statistically independent holdout.
Audit: `/Users/cadespivey/outputs/flwu-controlled-retest-v5-20261011/report.txt`.

## Longitudinal research memory acceptance

Run the full suite plus the history/controlled-worker tests. Required cases:

- Repeating identical capture is idempotent; fresh same-fact checks add
  observations without duplicate fact versions or raw artifacts.
- A→B→A yields both transitions. Byte changes are separate from finding changes;
  restoring a source after a blocked check compares against its last good bytes.
  Importing older retrieved evidence after newer evidence preserves historical
  observations without rolling back the latest supported facts/source checks.
- Blocked/absent sources and window-limited candidate lists preserve last known
  findings; missing records never create a withdrawal/removal claim.
- A finalized report remains the baseline across subsequent partial/research
  runs. Incomplete and superseded captures cannot be finalized. Report bytes and
  reviewer attestation persist; no finalize command means unknown baseline.
- Explicit starts/ends honor inclusive New York dates, DST and timestamp
  awareness. New observations of old publication dates are `first_observed`.
  Known effective dates trigger review even without a new source version.
- Old downloaded bytes reexamined later are not fresh source checks. Successful
  fetches with unfinished model analysis cannot produce no-observed-change.
- Manual status automatically captures incomplete denominators. Controlled
  acceptance persists revalidated facts/raw bytes; later tasks receive only
  frozen history for their own identity. Context tampering fails packet creation.
- Injected transactional failure leaves no partial artifacts/captures. Wrong
  schema/mode/scope fails. Tests use isolated temporary history databases.
- Artifact CLI can recover stored raw bytes without consulting workspace files;
  malformed/unknown stream and incomplete finalization requests fail closed.

Integration evidence: import the completed synthetic regression with the capture
CLI, inspect saved source/finding/observation counts and coverage, compare using
both baseline modes, and export a raw artifact with matching checksum. Do not
silently mark it finalized. Build the wheel and smoke-test the installed history
CLI outside the repository. This is storage/context validation, not a new legal
review, live-source trial or production approval.

### Recorded two-run local-model verification (2026-10-11)

The actual paired local-model run passed 21/21 history acceptance checks. A
reviewed synthetic baseline was finalized, then a second run received frozen
per-entity history and changed current sources. It detected exactly three changed
entities and preserved the other thirteen findings. Both blocked sources remained
gaps; prior Casey data survived; incomplete finalization was rejected. Restart
reused eight accepted files byte-for-byte and inferred only the restored task.
Explicit timestamp and finalized-baseline comparisons agreed. The database held
23 captures, 277 observations, 19 fact versions, 28 artifacts and one finalized
report. All 68 final links resolved. Baseline, blocked and final HTML were viewed
in a browser; no PDF pagination or live-source acceptance is claimed.

The baseline used ten model calls (one automatic citation repair); the followup
used twelve (three citation repairs). No accepted answers were edited. Maximum
reported followup input was 3,022 tokens. Citation omissions remain a model
adherence weakness, despite successful validation/repair. The test held the
publication window fixed and used one isolated database for both runs; it does
not establish multiweek, changing-window or native-compaction reliability.
The full suite passed 177 tests, with no reported warnings. Audit and the retained
fixture-preparation correction are under
`/Users/cadespivey/outputs/flwu-history-model-verification-20261011/report.txt`.
Re-evaluate saved evidence with `trials/evaluate_history_trial.py ROOT`.

## Static website and archive acceptance

Governing intent/spec: [WEB_PUBLICATION.md](WEB_PUBLICATION.md).
`tests/test_publication.py` covers finalized capture export, county roster joins,
private-state exclusion, checksums, citation integrity, unsafe URLs, invalid dates,
immutable IDs, preservation of prior builds, archive ordering, script escaping,
synthetic/public isolation, empty public builds, and the real Pages workflow.

Browser checks must exercise actual controls, not merely inspect generated strings:
latest default; older and overlapping periods; inclusive boundaries; invalid,
reversed and empty selection; reset; reload/Back/Forward; individual issue links;
source-link navigation and absence of quoted-source panels; historical directory preservation. Verify all
four headers and the original computed fonts. Resize through 320, 375, 390, 540,
740, 768, 1024 and 1440px; check both page overflow AND full date-field readability.
A no-overflow assertion alone missed clipped input contents during the first pass.
Inspect screenshots and restore native viewport sizing after automated checks.

Use only clearly labeled fixtures for archival UI scenarios absent from real run
history. Keep preview artifacts outside the public archive. Wheel smoke tests
must find the bundled HTML/CSS/JS while running outside the source checkout.
Record deployment separately: a built workflow is not a verified GitHub deployment.

2026-10-11 website pass: 196 Python tests passed; wheel built and its packaged
assets built a site in an isolated process outside the checkout. Browser checks
passed for latest/range/permalink/history controls, 17 distinct local source links,
original font metrics, and responsive layouts at the eight widths above. The
initial nonisolated wheel attempt lacked poetry-core; the normal isolated build
installed its declared build dependency and passed without reported warnings.

Two visual defects were exposed and corrected: shrinking date inputs now use a
responsive grid; the shared automated browser had a fixed 1200px emulated viewport
inside an 861px native window. Clearing metrics alone did not persist across CLI
calls. The review browser now starts with `browser.contextOptions.viewport: null`;
actual native resizing at 600/860/1200px verified inner width equals window width,
body stays inside it, and no horizontal overflow occurs. Keep viewport-emulated
regression sessions separate from the user's native preview window.

Evidence remains local in `output/playwright/web-verification.txt`,
`web-desktop-final.png`, `web-mobile-final.png`, and `web-native-final.png`.
The preview contains the actual latest synthetic capture plus one clearly labeled
older-period UI fixture. No historical live run was invented. GitHub deployment
has not been performed or validated in this pass; no finalized live public issue
is currently present in `website/updates`.

Native-window follow-up: page screenshots still missed OS-level clipping when the
browser window extended beyond the physical display. Observed screenX=771 plus
outerWidth=1297 on a 1728px-wide screen: 340px were off-screen despite zero DOM
overflow. Repositioned to x=80 with width=1100 and verified the entire OS window
visually using a native screenshot. Future headed preview checks must verify the
window bounds fit the available screen as well as viewport/layout bounds; do not
leave test windows partly off-screen. No website CSS change was needed for this
specific remaining symptom.

Directory-navigation revision: assert the update page has four research sections
and no directory; the separate directory page has the saved personnel snapshot
and no research sections. Verify bidirectional navigation preserves issue/range
queries, latest defaults, same-folder evidence URLs, current-page indication,
CourtListener destination, and 17 court links grouped into four levels. Exercise
menu open/Escape and narrow-window bounds. The 196-test suite, isolated wheel
build of both pages, and browser checks passed for this revision. Court menu scope
comes from registry membership, not a claim of newly completed live research.

Masthead/table revision: 197 tests passed. Browser checks verified navigation
beside the title in Updates/Courts/Personnel Directory order; 17 personnel menu
choices; county and circuit-area filtering; court retention on reset; empty
appellate states without unsupported assignments; six table headings; mobile
labels and no horizontal clipping. Court association export has a roster-identity
regression test. Visual evidence: masthead-final.png, personnel-table-desktop.png,
and personnel-rows-narrow.png under output/playwright. The directory's court
parameter must survive date changes and modified-click individual issue links.


## Active evidence-baseline acceptance clarification

Follow [EVIDENCE_BASELINE.md](EVIDENCE_BASELINE.md). Verify separately: collected originals, scoped content review, recorded source conflicts, and unavailable evidence. Two faithfully cited conflicting official statements pass source-review acceptance without selecting a winner. Missing or misattributed evidence does not pass. Criminal/diversion links plus contacts/assignments satisfy that scoped requirement; civil/shared responsibilities still require substantive review. Verify all five supported reports disclose historical gaps and do not equate a collected document with reviewed substance. Preserve existing provenance, identity, persistence and publication tests.


### Multiple-division source association acceptance

For a judge with two official division profiles, verify one person record retains
both assignment/profile/procedure mappings and each division's published email.
Follow both iframes and both print targets. If the print URLs coincide, check the
actual print document heading/email before reusing it; do not overwrite the other
published division. Read all text differences, inspect table/image content and
retain conflicting internal division labels without inferring reassignment.
The live Miranda checkpoint4334 exercises this manual acceptance: profiles52/53,
different published emails, one Division52 print document, one person finding and
an entity-keyed verified check. Artifact/fact read-back and replay were checked;
this is not an automated guarantee for future websites or county completeness.

## County-baseline evidence checks demonstrated October 16

- Multi-judge source attribution: Pole's profile and separately linked procedure
  retain his senior assignment, phone, rooms and Zoom. Garcia-Wood's assistant
  and phone are not copied from the shared header or adjacent hub block. Inspect
  the receipt and original PDF header; schema validation alone cannot prove this.
- Different document IDs in one division: retain both originals and the distinct
  trial, appearance, schedule and surplus-funds statements. Do not overwrite a
  colleague's record or infer supersession from retrieval order.
- Missing assistant: keep an unlocated state with checked URLs and search terms,
  while recording supported shared-unit contacts. Passing a legacy `not_published`
  enum is not evidence that no assistant exists.
- Historical artifact replay: packets1–61 retain their original payloads/capture
  identities. Recover changed local bindings only from exact saved bytes, verify
  hashes, replay, and check capture count and finalized-report rows remain stable.
  The live audit passed; it does not validate every historical legal conclusion.
- Bounded comparison inspection: redirect full CLI JSON and inspect selected
  entity fields rather than feeding repeated source quotations into a task.
  This is an execution instruction; no model long-context test is claimed.

October16 applicability acceptance evidence: Achille packet63 contains an explicit
shared-source non-use association in both receipt and compared semantic facts.
The entity-filtered context returned the same case cohort/policy date and an
unknown earlier-case scope. Packet62 remains independently replayable; no finalized
report changed. This is a checked data contract, not a claim that a generic engine
infers legal applicability correctly. Later automated tests for source reuse must
include an individually excluded shared template and fail if the exclusion is
lost during receipt-to-fact serialization. A date-wording test must retain “after”
and business-day units without replacing them with an assumed before-hearing rule.

October16 Alperstein acceptance evidence and future regression requirements:

- Keep revision month `2026-10` and null exact revision date; reject invented
  `2026-10-01`. The original AI order's signature date must not become an unstated
  effective date.
- Alperstein35 upload wording and scheduling rules must remain independent from
  Achille33. Fail a later extraction trial that imports the latter's unilateral
  setting permission, two-business-day language or2025holiday link.
- Preserve assistant-header/body and Zoom-link/one-tap discrepancies as separate
  supported statements. Do not infer a personnel change or replace the primary
  profile field with a number from an inconsistent dial-in string.
- Keep the January AI original alongside amendments, vacatur and the individual
  October statement, with retrieval/stated dates. A conflict is a completed source
  review with a discrepancy, not missing evidence or a controlling-law conclusion.
- Packet64 passed person/citation validation, artifact/fact read-back and exact
  frozen replay. This is live evidence validation, not a newly implemented generic
  extractor test or proof of county completeness. All23individual PDF pages and
  three original AI pages were visually reviewed after reopening truncated output.

October16 Alspector link/image acceptance evidence:

- Actual HTML targets, visible labels and QR payloads are separate facts. The
  visible/profile Zoom ID328337467 must not silently overwrite the actual458523246
  anchor/QR, and a clerk label pointing to the defender site must not become the
  verified clerk website. Original HTML/images and derived inventory/decoder output
  are retained in packet65.
- `scripts/decode_source_qr.swift` compiled without diagnostics using installed
  Xcode/Vision. On the saved QR it returned one payload matching the independently
  inspected anchor; on the seal it returned none. Missing file returned1 and
  missing argument returned2. No destination was opened. This exercises macOS
  extraction, not cross-platform availability or arbitrary-image reliability.
  The reusable helper was then strengthened to decode the exact in-memory bytes
  it hashes instead of reopening the path; all four cases passed again against
  that build (`review/qr-helper-validation.json`). The original decoder/output
  in packet65 remains unchanged.
- Separate feature states: CMS agreed-order submission enabled from stated date,
  online hearing scheduling not used. Distinguish named in-court clerk from elected
  clerk and interpreter fax from chambers fax. No civil assignment inferred merely
  from membership in a combined domestic-violence directory.
- Person/citation validation, original/fact read-back and frozen replay passed for
  packet65. Criminal merits remain screened rather than exhaustively researched;
  this is the user-authorized scope, not evidence that every criminal authority or
  every linked handbook was substantively reviewed.

October16 Arthmann acceptance evidence and future extraction cases:

- Packet66 preserves26 topics,15 structured timing rules and14 discrepancies.
  Entity context must retain emergency two-business-day and two-day clauses as
  separate entries, exceptions for DV exhibit exchange and physical courtesy
  copies, and literal “within” wording for the joint stipulation. Do not infer
  deadline arithmetic or a general materials deadline.
- Division38's `expressly_adopted` status-quo association must survive semantic
  serialization, with no invented adoption date. A later extraction trial must
  fail if it copies Division33/35 non-use into Division38.
- Recovered electronic-filing order: issuance2013-11-12, nunc-pro-tunc2011-10-28,
  literal immediate-effect wording and null separately determined effective date
  remain distinct in shared-rule facts. Failed original link and alternate
  official copy are both retained, without byte-equivalence claims.
- Header/profile courtroom11166 versus location-sectionWW11-168 and Div40 versus
  Div38 order-email clauses remain separate statements. Do not repair originals.
  Repeated withdrawal blocks produce one summary with both source locations.
- Full24-page individual PDF and three-page recovered order were visually
  reviewed. Person/citation validation, artifact/fact read-back and frozen replay
  passed. This is a checked live data contract, not an implemented general deadline
  parser or proof of county completion.

October16 Bailey acceptance evidence and future extraction case:

- Packet67 preserves current FH contacts (Nichole Lunsford, NW7910) separately
  from historical Family41 contacts (Sheena Bergeron, 905B), with the historical
  document's explicit revision/effective date of January14,2013. Exact-entity
  history context must retain both entries without overwriting current fields.
- Current FH revision/effective dates stay null. Neither the Google automatic
  refresh banner nor search-engine age metadata supplies an author revision date.
- Four timing rules preserve two/three/seven unspecified days versus24hours,
  separate subjects and triggers, and interpreter language exceptions. No deadline
  arithmetic or general civil interpreter entitlement is inferred.
- Criminal plea-form URLs remain link-only; the historical PDF's three pages are
  collected but only its page1 identity/date/header is substantively inspected.
  Future extraction trials must reject claims of exhaustive form/history review.
- Person/citation validation, artifact/fact read-back and frozen replay passed;
  the entity-context checks above passed against capture4542. This is a live
  record check, not proof of a general extractor or completed county baseline.

October16 Bober acceptance evidence and future extraction case:

- Packet68 retains named assistant email `stracy@17th.flcourts.org` from visible
  text and shared `divfw@17th.flcourts.org` separately. A link-only extractor would
  miss the named address. Chambers NW5910, courtroom NW5900 and reception/drop-off
  NW5865 must remain distinct in the saved facts and comparison context.
- The clerk website's visible label and actual public-defender destination remain
  a documented mismatch. In-court clerk “Unassigned” is not a person identity;
  the felony clerk's attorneys-only telephone is not the assistant's telephone.
- Zoom permission requires48hours advance request, with discretionary language
  and a non-evidentiary/under30minute condition retained. Do not import Bailey's
  two-day courtesy-copy or24hour equipment deadline into Bober's record.
- Interpreter source typo “at leave seven (7) days” remains literal, with an
  interpretation note. Preserve the unspecified-day unit and language exception;
  do not silently correct the original or compute a case deadline from it.
- Person/citation validation, artifact/fact read-back and frozen replay passed
  for capture4546. Exact-entity context checks passed. This live record check
  does not establish a general extractor or county completion.

October16 Bristol acceptance evidence and future extraction case:

- Packet69 preserves all six published division labels and the official order's
  dependency/family/delinquency classifications. The new-case distribution table's
  omission of JS/39 and29 does not become a finding of assignment termination.
- Two-business-day filing and two-unspecified-day email submission remain distinct
  timing entries with different actions. The full agreed-order summary retains
  footnote3's exception for an agreed goal-date extension without a motion.
- Current individual procedure cites2008-60-UFC; the original2008 and retained
  2019-9 emergency statements keep their own dates, rule references and alternate
  office locations. No selected controlling authority or invented supersession
  chain is needed for acceptance of accurately recorded source review.
- The new distribution review is supplemental to the earlier Franker review,
  with explicit paragraphs and visual scope; no historical receipt overwritten.
  Individual author date remains unknown. Current shared-source observations are
  not backdated to their issuance/effective dates.
- Person/citation validation,842artifact/fact read-back, frozen replay and exact
  entity-context checks passed for capture4550. Fifteen checklist topics and two
  discrepancies retained. This does not prove county completion or production
  extraction of every similar source.

October16 Carbuccia acceptance evidence and future extraction case:

- Packet70 stores document owner40 separately from the status-quo statement's
  subject38. Exact-entity context must retain `reference_names_other_division`,
  not affirmative adoption or non-use for40. Do not overwrite Arthmann's separately
  supported Division38 adoption record with a statement attributed to Carbuccia.
- Seventeen timing rules retain subjects, actions, triggers, units and exceptions.
  Emergency two-business-day and two-unspecified-day clauses remain separate;
  general courtesy copies may arrive at hearing, while non-DV exhibit exchange
  and CMS preparation have distinct five/three-business-day requirements.
- Preserve the physical-hearing hardcopy exception, DV scope exception, and literal
  “within” joint-stipulation wording. Do not replace it with the shared template's
  “at least” wording or infer deadline arithmetic.
- All22 individual PDF pages and full HTML were read; RUCD affidavit is present.
  Contents references are not physical pinpoints. Rect/Point annotation geometry
  serialized successfully after initial type errors; PDF external destinations
  are all represented in the HTML inventory. This is not a browser/CMS action.
- Person/citation validation,875artifact/fact read-back, frozen replay and
  exact-entity context checks passed for capture4554. Twenty-nine topics and
  eleven documented ambiguities/discrepancies retained. County remains incomplete.

October16 Coleman acceptance evidence and future extraction case:

- Packet71 retains current shared division email separately from named email
  found only in historical temporary-docket evidence. Filename2020-07-15 is not
  an author-stated revision date; unreviewed historical pages remain explicit.
- An HTTP200 Google editor shell does not count as readable procedures. Exact
  court-linked document ID was exported successfully, with all10 PDF pages read
  and visually checked. Displayed/profile Zoom883035672 and annotation532000556
  survive entity-context read-back as different fields; no meeting was opened.
- Rule2.530 link target is a proposed-amendment notice. Preserve proposal status,
  April1,2025 comment deadline and unknown adoption/effective dates. Underlined
  subdivision(f) was visually checked. Do not promote proposal text to an operative
  deadline merely because a judge links it as a rule.
- RevisionAugust14, reassignmentAugust17 and CMS commencementOctober1,2025 remain
  distinct. March FK assignment and later FP statements retain their source dates.
  CMS weekdays and remote-permission wording remain discrepancies, not silently
  reconciled. The clerk-site entry remains an incorrectly attributed defender URL.
- Six timing rules preserve weekday-relative, hours and unspecified-day units.
  Next-business-day order review after4p.m. is not a filing deadline. Individual
  AI signature/responsibility paragraph does not create a disclosure certificate.
- Capture4558 passed person/citation validation,115 nested citation checks,
  870artifact/fact read-backs, frozen replay and entity-context assertions in
  `review/finish-coleman.py`. All71 packet replays preserve finalized reports.
  These checks validate this manually reviewed record; they do not demonstrate
  a production extractor or completed county roster.

October16 Duffy acceptance evidence and future extraction case:

- Packet72 preserves profile chambersNW6880/courtroomNW6840 and procedure
  mailingSuite5880 separately. Kamela/Kami remains a name variant, not two people.
- Five-business-day filing/exchange concerns witness/exhibit lists, not an
  inferred exchange deadline for every exhibit. Cancellation2unspecified days,
  courtesy copies48hours and continuance-date request48hours retain units/actions.
- General clerk filing, court courtesy delivery and CMS supporting-motion/order
  submission remain separate. No claim that CMS submission fulfills clerk filing.
  Consistent Zoom URL supplies no inferred remote entitlement.
- RevisionOctober7,2025 is distinct from CMS policy effectiveOctober1,2025; a2026
  retrieval is not a new rule. Criminal forms remain link-only. No PDF/browser
  review claimed; published HTML, table, anchors and seal were inspected.
- Capture4562 passed person/citation validation,48 nested citations,878artifact
  and fact read-backs, frozen replay and entity-context assertions. Twelve topics,
  four timing rules and two discrepancies retained. All72 packets replay without
  new captures or finalized-report changes; county remains incomplete.

October16 Fein acceptance evidence and future extraction case:

- Packet73 retains current FT and older FX sources separately. Historical Box160
  does not enter current address lines; clerk building hours do not become JA hours.
- Named Victoria Cruz email verified in current HTML/PDF; historical scanned OCR
  defects do not replace it. Current procedure date remains unknown.
- Court-linked format example is a populated case order. Its June17,2026 date,
  January31,2027 discovery/motion deadline and March24,2027 trial date persist only
  as case-specific facts. General `deadline_rules` remains empty;8:45 a.m. is a
  calendar time. Example is not a blank template or proof of general rule adoption.
- Preserve attorney-only non-evidentiary Zoom permission, motion-calendar-only CMS
  cancellation, Word-format orders and emergency call AND email. Do not import
  neighboring judges' permission requirements, five-minute caps or notice periods.
- Current3-page procedure,3-page example and1-page older source visually reviewed;
  current3993-character HTML also read. Plea form link-only. Capture4566 passed
  person/citation validation,56 nested citations,892artifact/fact read-backs,
  frozen replay and exact entity-context assertions. All73 frozen packets replay
  without new captures or changed finalized reports. County remains incomplete.



October16 Gamm acceptance evidence and future extraction case:

- Packet74 retains individual Vicki Plant statement, September2026 JT/46→GMX
  distribution and March2026 GMX→Denise Kistner assignment separately in semantic
  `referral_statements`. Unknown individual date stays unknown; no controlling
  referral chosen. A documented discrepancy is not a missing source review.
- Filing2business days and email2unspecified days retain their distinct acts.
  Literal within10days of trial setting has unknown direction/anchor meaning and
  waiver exception; no computed deadline or silently inferred before/after.
- Numbered footnote4's agreed goal-date exception and footnote3's conferral
  method/date/time persist. Roman-i technology note is retained in addition to
  six numbered footnotes. No PDF or browser review claimed.
- Named email is visible text with no mailto anchor; zero anchors do not mean
  no contact address. Premarking alphabetically and clerk numerical admission
  remain distinct from other judges' procedures. JL assignment does not disappear
  merely because a later new-case allocation table focuses on other divisions.
- Capture4570 passed person/citation validation,72 nested citations,900artifact
  and fact read-backs, frozen replay and exact entity-context assertions. Seventeen
  topics,three timing rules,four discrepancies saved. All74 frozen packets replay
  without new captures or changed finalized reports. County remains incomplete.

## Broward roster link extraction regression — Usan

Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/pytest -q tests/test_broward_roster_links.py`.
The ten cases cover the observed USAN/SUSAN collision, punctuation/case normalization,
wrong division, duplicate matching rows, surname-only input, changed markup,
protocol-relative and path-relative hrefs, unusable URLs, and missing required links.
Acceptance requires one exact normalized full-name/division match, preservation of
each original href, and resolution against the actual source page URL. No fetching
or inference of a replacement person is permitted by this helper.

The live-evidence exercise uses retained `bailey-criminal-hub` HTML from the Broward
acquisition manifest, with name `Michael A. Usan` and division `FX`. Its profile,
procedure and Zoom destinations must match the sources actually acquired for Usan.
The observed result is saved in `review/usan-roster-helper-validation.json` with
source/helper hashes. Ten fixture tests passed and this retained-source check passed
on October16. This is not a fresh roster retrieval, a browser test, or evidence of
compatibility with other county layouts.
# FL Courts hydrated article extraction — Weiss checkpoint103

`tests/test_flcourts_article.py` checks that the supported Next.js body is extracted
without navigation dates or script/style text, with entities decoded and original
text retained. Missing/duplicate JSON scripts, malformed JSON, changed structure,
non-string fields and empty bodies must fail explicitly. A failing first fixture
embedded an unescaped closing script tag; the fixture was corrected to encode
`<` as `\u003c`, matching valid embedded JSON. No production fallback was added
to accept malformed pages.

Eight article tests and ten roster-link tests passed. The actual retained Fourth
DCA announcement also matched the earlier independently inspected JSON extraction;
source/helper hashes are in `review/weiss-article-helper-check.json` within the
Broward run. This proves the encountered article structure, not all FL Courts
pages or live browser operations. The save retains both the shell extraction and
the derived article under the same original source hash and retrieval timestamp.

## Embedded Florida Courts form metadata — exercised October16

Bounded helper: `scripts.flcourts_article.extract_form`. Acceptance requires
extracting the actual form record from a retained HTML shell without executing
scripts, preserving the exact versioned PDF URI and month/year date, and rejecting
missing/duplicated/malformed metadata, non-form records, non-PDF metadata and
unexpected source/download origins. Navigation text cannot supply form fields.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/pytest -q tests/test_flcourts_article.py tests/test_flcourts_form.py
```

Observed28passed; the article behavior remains covered. Live validation used
official12.915/12.920abc/12.921 form pages, independently downloaded their original
PDFs, reviewed19textpages and8specific rendered form pages, and saved/read back
both the individual and shared-form findings in packet112. Unit tests alone do
not prove PDF contents, current legal effect, full application behavior or county
completion. No full application build was run for this helper addition.

## DOR96 retained-source checkpoint assertions — packet116

For Tannenbaum's retained source, manually inspect the full individual text and
match the roster's exact name/division/link before accepting the receipt. The
post-save `review/finish-tannenbaum.py` then checks database context for:

- Separate 30-minute calendar interval and matter-specific 15/30/60-minute limits.
- Strict `>120` trigger and approximate two-week status-conference timing.
- Five-to-ten-minute arrival range, 48-hour alternative evidence-email route,
  recommended PDF and ratifying Word, and unstated order deadline.
- No imported Sullivan observer exception; Sullivan's prior exception and unstated
  alternative deadline remain unchanged in their own earlier record.
- Exact contacts, source-attributed email discrepancy, no invented document date
  or PDF review, preserved earlier gaps, and unchanged finalized reports.

Observed packet116 receipt/citation validation, artifact/fact database readback,
same-packet save idempotence, frozen replay, and the entity-context assertions
passed. These are live-evidence checkpoint checks, not new unit tests or proof of
completed county research. Do not rerun its state-writing finalizer after advancing
to another officer; use the frozen packet for later replay.

## Folder description extraction — Woods117

Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/pytest -q tests/test_flcourts_folder.py tests/test_flcourts_article.py tests/test_flcourts_form.py`.
Observed37passed (9folder,8article,20form). The new tests require text/links from
embedded supported blocks, recovery of an escaped iframe URL, suppression of
navigation/script text, and explicit failure on missing/duplicate JSON scripts,
wrong content type, empty body, unknown/malformed blocks, non-string content and
nested custom tags. No link is fetched or script executed by the helper.

Live retained-source checks independently match the two `.gov` folder extractions
and their9/4video URLs, original hashes and derived-text hashes in
`review/woods-folder-helper-verification.json`. Videos were not watched. The earlier
article helper correctly rejected these folder pages; a separate helper handles
their distinct metadata. No full application build or universal FL Courts layout
compatibility is claimed.

Packet117 also exercises receipt/citation validation, database fact/artifact
readback, frozen replay and preservation of earlier records/gaps/finalized reports.
Its finalizer checks both CSC weekdays, exact date precision, absence of an inferred
ratifying-order format, distinct three-business-day/five-day review periods, and
both missing-template/manual gaps. The first finalizer attempt failed on importing
`scripts` with `PYTHONPATH=src`; loading the helper by its explicit path repaired
that execution issue. The successful rerun is the verification evidence. Do not
rerun its state-writing finalizer after the project advances.

## Clerk directory extraction and institutional checkpoint118

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/pytest -q tests/test_broward_clerk_directory.py tests/test_broward_roster_links.py`
passed18tests (8directory and10existing roster-link tests). New assertions preserve
division identity/href, leading-zero room and distinct phone-option/fax text, exclude
navigation noise, and reject absent/duplicate panels, empty/duplicate rows, merged
cells, missing division link and changed headers. These tests do not validate every
county layout or infer the legal meaning of contact labels.

The actual retained Broward directory yielded38rows, matched against the saved
extraction. Contact normalization was separately checked against exact originals,
including CircuitCivil's public/attorney/fax lines, regional addresses and jury
telephone versus counter hours. The evidence is
`review/clerk-directory-helper-verification.json`.2026/2027 holiday date/weekday
consistency was checked without inventing additional holidays.

Packet118 verifies three separate entity contexts, original/fact readback,
same-packet save idempotence, frozen replay, unchanged previous roster/officer/ZIP
findings, retained gaps and unchanged finalized reports. The courthouse-access
review includes seven security-order text pages and visual checks on1/6/7, plus
two one-page trial-room sheets. No full application build, telephone test, contact
submission or courthouse visit was performed. Operational Clerk research remains
explicitly incomplete despite the verified contact records.

## Circuit Civil operational baseline acceptance (Broward119)

- Review evidence must identify all six actual panel bodies, not just tab titles.
  Verify 30 fee rows retain their source labels and units; new-case real-property
  tiers 401/906/1906 must remain distinct from counterclaim tiers395/900/1900 and
  quiet-title PDF instructions400/905/1905. No invented rounding/calculator output.
- Preserve auction deposit receipt at3pm EST preceding business day, balance at
  noon EST next business day **or judgment deadline**, and objections measured
  from certificate-of-sale filing. Do not infer calendar-day meaning where the
  source merely says days. Inaccessible linked instructions remain a source gap.
- Confirm 12PDF/2DOCX files;22PDFtextpages and only16visually inspected pages.
  DOCX header/footer review is not rendered pagination. Check prefilled form values
  absent from plain PDF extraction against field dictionaries and rendered images.
- Preserve five documented discrepancies: fee amounts, indigence waiver wording,
  2.601 subsection references, forged-deed paragraph numbers and Law Library room.
  Source disagreement does not invalidate completed review or authorize correction
  of original evidence. Existing officer records must remain unchanged.
- Save/read back the new stable operational entity and original artifacts; exact
  replay must add no capture. Finalized reports remain unchanged. Check prior
  personnel gaps and institutional records are still available in history context.
  A source review does not establish county completeness or website publication.

## County Civil acceptance and fee extractor (Broward120)

- `tests/test_broward_clerk_fees.py` must preserve tier text, per-unit qualifiers,
  decimal amounts and repeated fees under separate headings. Changed counts,
  missing rows, unknown/repeated headings, merged cells, blank labels, malformed
  amounts, duplicate panels and multiple tables must fail visibly.
- Check actual retained County37/Circuit30 rows and exact source quotes. Compare
  Circuit values against the already saved119receipt; tests alone do not prove
  those real-source values. Do not sum duplicate fee labels.
- Preserve all ten CountyCivil panel IDs, including plural `ForeclosuresSales`.
  Confirm small-claims paperwork and venue statements retain their own scope;
  old any-office/copy-count instructions must not silently replace the ZIP order.
- Preserve garnishment20days after receipt,8business days for hand delivery and
  14business days for mail. Email in the certificate supplies no inferred objection
  period. Preserve the Circuit caption on the County-linked form.
- Verify original/later order sources and stated dates:2017PIP transfer,
  2023express vacatur,February2021mediation andAugust2021Amendment3. Preserve
  mandatory-referral versus landlord-agreement language and historical program
  limits. This is evidence comparison, not a current-funding certification.
- Confirm7PDFs/64collected pages,23text and visual pages,41unreviewed appendix
  pages. Do not count rendered but uninspected pages as reviewed. Keep paid-form
  catalogs and interactive preparation screens distinct from actual forms.
- Verify saved facts/artifacts, exact and frozen replay, entity context, previous
  contacts/ZIP/CircuitCivil findings, source gaps and unchanged finalized reports.
  CountyCivil completion leaves Appeals and the remaining operational queue open.


## Appeals source-review acceptance (Broward121)

- Six panel bodies and contact sidebar must be reviewed. Preserve five fees under
  three distinct headings, separate payees and $3.50 per-document/$7 sign-seal units.
  Do not apply a single-table parser or infer a County Civil filing-fee category.
- Keep Clerk overview, HowtoFile and Fourth DCA trial instructions as independent
  filing-destination statements. Administrative instructions add a court copy;
  do not merge them into trial instructions. Do not resolve authority by selection.
- Preserve broken original text and separately labeled, visually verified manual
  transcription. Verify both text hashes and original source association. Extract
  DCA folder description via the proper content type; list-only forms stay unreviewed.
- Preserve AO2020-89's November3,2020 issuance/January1,2021 effectiveness and
  express supersession, without overwriting prior2019/2018 receipts. Record attached
  template's older reference and reply wording. Preserve two initial extensions/120
  total days, two answer extensions/60 total days, exclusions, record-return court
  business days, Word/RTF proposed orders versus PDF copies and2-page emergency cap.
- Confirm32collected PDF pages in seven source-review entries,19text pages and
  13visual pages. This includes reused12-page transfer order reviewed only on1–3;
  session-law review limited to4,6. Prior review history is not reset by these limits.
- Validate exact quote/hash checks, all saved artifact bytes, semantic fact readback,
  identical-packet idempotence, frozen replay, prior personnel/institution/civil
  records and gaps, entity context, and unchanged finalized-report table. Review
  actual findings against originals; unit tests cannot establish legal accuracy.

## Evidence and Archives acceptance (Broward122)

- Evidence: six panels/two FAQ answers/contact; Archives: four panels/three FAQ
  answers/contact. Exact panel names and actual attachment/navigation hrefs retained.
- Five Evidence fees:2/year search,1/page copy,2/document certification,5/page
  oversized copy with source dimensions,6/item CD/DVD/USB duplication. Four Archives
  fees:2/year,1/page,2/document certification,7/document exemplification. Verify
  exact labels/amounts/quotes; no quantity-free or summed fee inference.
- Keep numerical list/admitted numbers distinct from alphabetic identification
  labels; preserve green/pink/gold/blue mappings and all six list/five label fields.
  Remote deadlines remain2business days before hearing and5business days after log
  receipt, with CMS upload versus Clerk filing separate. Compare original/amended
  in-court-clerk exception without overwriting earlier source records.
- Evidence phones5537/5539 both phone; email evidencedivision, no room invented.
  Archives East03305/6565option3; escrow Finance West18120/6244phone/6115fax.
  No invoice-email reassignment. Date ranges are published descriptions, not
  continuous-record verification. Payment-list difference retained, no inferred ban.
- Separate two stable findings/receipts. Verify citation hashes/quotes, artifacts and
  facts read back, identical packet/frozen replay, entity context and earlier records,
  gaps and finalized reports unchanged. Remaining operations stay incomplete.

## Records-request acceptance (Broward123)

- Five relevant RecordsRequest panels and four electronic-certification panels;
  marriage duplicate panels retained/screened only.24directory quotes must match
  existing institution rows before marking reused contacts consistent.
- Request-form case-variant URLs must be byte-compared, not assumed equivalent.
  Count one physical form; visually verify revision,email,fax,choice fields,fees.
- Preserve seven channel-specific fee entries, not a summed payable total;
 100-page exclusion is strictly exceeding100,30-day download window distinct from
  claimed document nonexpiration,2week processing an estimate after receipt.
- Preserve malformed FAQ hrefs and working navigation independently. HTTP200
  not-found body and Next.js shell must not count as substantive source review.
  Current folder-derived text must retain original URL/time/hash and actual links.
- Review matrix cell association visually; six selected rows, five selected roles,
  legend and confidentiality overrides. Differentiate attorney/party/registered/
  anonymous/bulk access. No access claim from category row alone.
- Four distinct PDF originals34pages collected,13text pages and10visual pages with
  explicit partial-page scopes; order attachments not double-counted as review.
  September2024 standards and September16,2024 adoption order retain their dates.
- Verify98nested citations, saved facts/artifacts, packet idempotence/frozen replay,
  single-entity context, prior contacts/procedures/gaps and finalized reports.
  No case-record query, purchase, upload, access agreement or verification result
  may be claimed from public instructional/empty landing pages. eFILING and global
  FeesAndCosts remain incomplete after this checkpoint.

## E-filing acceptance (Broward124)

- Three Clerk panels/26FAQ bodies; actual Clerk and training-index links retained.
  Scoped review counts:11newPDF originals,396collected pages,65text/23visual pages.
  These counts do not mean full manual or criminal-appendix review.
- Preserve three correction-period statements (5unspecified days,5business days,
  30business days), two timestamp-operation descriptions and payment-settlement
  versions with exact citations. No computed deadline or controlling-source choice.
- Keep filing/proposed-order/service routing, confidentiality notice, original
  retention, case-number fields, size/attachment grouping and fee channels separate.
  A UI sample fee is not a verified current payable fee.
- Empty scan extraction is not evidence of absent content. Verify manually
  transcribed excerpts against rendered pages and preserve original retrieval/hash.
  Distinguish visible dates from index dates and hidden/machine-extracted headers.
- Verify amendment strikeouts visually. SC11-399 is a2012revised opinion, not a
  newly effective2026rule or an AOSC merely because the Clerk's label says so.
  Deleted clauses must not become operative findings. Criminal rollout screening
  does not imply exhaustive criminal procedure review.
- Preserve twelve source differences, including broken complex-order link with
  independently sourced working alternate. Do not convert a documented conflict
  into a missing-evidence gap or silently overwrite earlier source statements.
- Verify126nested citations, artifact/fact readback, packet idempotence/frozen replay,
  entity context, prior judge/officer/institution/civil/records findings and gaps,
  and unchanged finalized reports. Unit tests establish storage/validation behavior,
  not legal accuracy or current Portal transaction behavior. FeesAndCosts remains.

## Consolidated fee schedule acceptance (Broward125)

- Confirm one CourtFilingFees panel and eight expected table headings. Parse only
  explicitly scoped civil tables through the existing strict fee helper. Source
  citations must point to original bytes, not the temporary parser wrapper.
- Verify81selected rows:30CircuitCivil,37CountyCivil,2civil appeal fees,4Archives,
 1shared Family row and7estate/trust entries.73prior label/amount pairs must match
  exactly before reporting consistency. A mismatch requires recording evidence,
  not weakening the assertion or assuming the more recent retrieval controls.
- Preserve separate appeal payees and empty-amount payee notes; per-page/year/item
  units and strict/inclusive claim thresholds remain in labels. No automatic
  summation of repeated charges or inference of jurisdiction/eligibility.
- Keep >15,000 Family versus >50,000 Circuit Civil descriptions, indigence scope
  statements and Archives payment-list difference as3documented discrepancies.
  Reviewed schedule has no stated revision/effective date; store null, not today.
- Validate260nested citations, row/semantic fact/artifact readback, identical and
  frozen replay, prior findings/gaps/finalized reports, and entity context.
  All eight scheduled operations sources may be reviewed while overall county and
  selected-news work remain incomplete. No payment or publication is established.

## Dated announcement acceptance (Broward126)

- Scope repeated IDs to the archive panel; verify44headlines and11selected bodies
  against retained HTML/text. Hidden older entries must not disappear from discovery.
- Preserve multiline exception10's actual AO link and all10local entries, separately
  from seven grounds in the corrected opinion. Record30days versus30business days
  as a source difference, without calculating a filing deadline.
- Keep June2025 article label, October2025 linked order, unknown revision date and
  retrieval time distinct. Older linked rule text must not be labeled the2025rule.
- Verify literal href, browser-resolved URL and actual response separately. An
  inventoried malformed statute link is not a fetched failure or reviewed statute.
- Separate six PDFs/55collected pages from50text-reviewed and18visually reviewed
  pages; generated images alone do not count as visual inspection. Preserve original
  scan bytes and provenance for manually transcribed excerpts.
- Validate114nested citations, facts/artifacts, exact/frozen replay and entity
  context. The overall Clerk check is verified with nine supporting receipt hashes;
  genuine missing-source gaps and the incomplete county check remain. Prior people,
  source differences and finalized reports must survive unchanged.
- `review/finish-news.py` records the live checkpoint assertions and validation;
  focused storage/history tests are separate evidence, not proof of legal accuracy.
  No Portal transaction, present emergency relief, county completion or publication
  may be inferred from this checkpoint.

## Access-order acceptance (Broward127)

- Four actual index links; four originals/six text-reviewed pages/five visually
  reviewed pages. Preserve recording-order page1 as text reviewed only.
- Exact targets:2023-26-Gen→2016-15-Gen;2023-28-Gen→2010-40-Gen;
  2023-44-Gen→2023-28-Temp. Reject collapsing Temp into Gen.
- Badge scope is employees/elected judges; recording order preserves separate
  courtroom/media rules and qualified ADA language. Closure policy is not evidence
  of a current closure or deadline relief. Record signature dates and null separate
  effective/revision dates; do not use upload-path dates as legal events.
- Verify29nested citations, saved facts/artifacts, frozen replay, context and prior
  personnel/source gaps/finalized reports. `review/finish-access.py` exercises these
  live assertions. Existing test results remain dated evidence, not a fresh run.
- Preserve raw403 responses separately from web-tool extraction; a denied browser
  wrapper launch does not establish a browser visit. No terms acceptance or search
  transaction is part of this checkpoint. County navigation/review remains pending.

## Navigation and completion-audit acceptance (Broward128–129)

- Verify four distinct navigation destinations/roles from their stated evidence;
  preserve the eight appraiser search-button hrefs without claiming target searches.
  Provider-only Official Records discovery keeps unknown source HTTP status and
  three failed original attempts; do not coerce it into an original200citation.
- Validate11navigation citations, semantic facts/artifacts, replay and unchanged
  history. Read acquisition HTTP status from the provenance receipt: it is excluded
  from semantic comparison facts by design.
- Audit158actual index rows with85material review/reuse candidates and explicit
  exclusion reasons. Counts are discovery inventory, not completed source reviews.
- Preserve402embedded limitations,340contact-field states and11prior actions as
  annotations requiring disposition, not inferred missing-document counts. Later
  Marra capture4634 resolves the old pending-action premise; Rebollo unknown current
  fields remain unknown. Do not clear genuine original-source gaps.
- Audit-only packet129 must add no findings or finding observations, leave finalized
  reports unchanged and replay without a new capture. Update only umbrella reasons
  to reflect actual outstanding work. Validate158index citations and saved artifact
  bytes. `review/finish-navigation.py` and `review/finish-county-audit.py` record live
  assertions; no broad legal-completeness inference from passing checks.

## Arbitration source comparison acceptance (Broward130)

- Verify11hub links/10uniquePDFs and their shared acceptance URL; exclude neighboring
  parenting-form links. One order plus ten standalone forms:27text-reviewed pages,
 15visually reviewed pages. Rendered images alone do not establish review.
- Keep April2024signature, June2026filename revision cue and unknown exact exhibit
  day/effective date distinct. Verify actual exhibit inventory against body claims.
- Preserve COINX OR damages>30000 branch, three-hour versus per-day units,
 100/175advances, equal versus plaintiff-default allocation, caps and agreement
  exceptions. No automatic rate selection, summation or authority resolution.
- Keep15/30/60day order-based events,10day advance and20day post-motion-period
  statistical trigger distinct. Statistical form wording is not a case deadline.
- Check original revised extraction against visual transcript, retaining identical
  original hash/retrieval and different text hash. Keep standalone form's different
  visible wording and application email; do not overwrite either original.
- Validate66nested citations, saved facts/artifacts, exact/frozen replay, entity
  context, prior gaps/finalized reports and queue advancement to property fraud.
  `review/finish-arbitration.py` records these scoped assertions. Passing checks do
  not certify current consolidated rules, actual payments or county completion.

## Joint-order and property-form acceptance (Broward131–132)

- Joint fraud order: verify both identifiers and Amendment2 in the successful
  original, separate404/200retrievals,2text/visual pages, and both queue entries.
  Assert discretionary order-based Division03reassignment, retained case number,
  zero reassignment fee with no initial-fee waiver, and no categorical remote ban.
- Property loss: verify16text pages,14actually viewed rendered pages, body plus
 11-pageCMO and3-page trial form; rendering alone is insufficient. Keep unknown
  effective/exhibit revision dates unknown and form case dates blank.
- Assert15table rows; plaintiff/adjuster/corporate deposition75/90/120days after
  answer, discovery initiation90/completion30before Calendar Call, expert reports
 72hours before deposition, and distinct40-day SJ response after motion service.
  Keep mediation60/arbitration45conditions and later-of-two30-day mediator choice.
- Verify four internal wording/sequence records with both pinpoints; no inferred
  resolution or computed case dates. Preserve old AI paragraph and changed mediator
  window with old/new citations; omission is not absence of all legal obligations.
- Verify express2023amendment supersession without changing prior person versions.
  Thirteen old-source citation associations are provenance, not adoption/assignment.
- Check exact citations, artifact/fact readback, exact/frozen replay, entity context,
  historical records/gaps and unchanged finalized reports. Relevant live assertions
  are in `review/finish-property-fraud.py` and `review/finish-property-loss.py` in
  the Broward run. No unit-test or legal-completeness claim follows from this list.

## County mediation acceptance (Broward133)

- Verify 13 text-reviewed pages and 12 viewed rendered pages, three referral paths
  and report D; preserve blank appointments, dates and checkboxes.
- Verify selection 10/5 days and mediation 60/15 days by applicable path; reporting
  [upon completion, 5, 30, 10] retains distinct actors, recipients and acts.
- Preserve $350/$250 hourly caps, COINX OR >$30,000, $60 per-party CMAP sessions,
  indigence, conditional free small-claims/residential paths and payment anchors.
- Assert four source discrepancies and both supporting pinpoints; no resolution.
  Report D scheduled time is not asserted actual start, and case-type field absence
  remains recorded. Read ADA and interpreter statements separately.
- Supporting template search must not parse PDF exports as HTML or substitute
  family/arbitration forms. Preserve the actual warning and corrected search scope.
- Validate exact citations/artifacts/facts, exact/frozen replay, entity context,
  distinct supporting-template gap and earlier records/finalized history.
  `review/finish-county-mediation.py` records the scoped live assertions; no broad
  unit-test or county-completion inference is authorized by these checks.

## Credit-card reuse acceptance (Broward134)

- Verify exact original/text hash identity, original and repeat retrieval times,
  and full four-page review scope in all three prior person receipts.
- Verify4text/3visual pages; preserve scope47/101/102, issuedJune29 versus effective
  July1,2026, express2025-41supersession and literal130before/150after anomaly.
- Assert noon3business days separately for represented waiver and jury transfer;
  preserve their different entered-order/submission conditions. Assert120-day proof,
  five-day extension and30calendar-day default-package anchored to the case order.
- Retain four prior Clermont comparisons with original citations and unknown
  resolution; do not refresh judge-procedure dates or calculate case deadlines.
- Verify exact/frozen replay, all nested citations/artifacts/facts, entity context,
  prior person observation IDs and genuine gaps/finalized history preservation.
  Scoped assertions live in `review/finish-credit-card.py`; no broader completion
  or unit-test claim is implied.

## Administrative-history and panel acceptance (Broward135–137)

- ESI: verify2text/visual pages, five historical names, unknown separate effective
  date and120-day panel actor. Assert no new judicial roster entries or automatic
  case-special-master requirement; retain the2021guideline relationship citation.
- Newspaper: verify1text/visual page, Sun Sentinel, explicit50.0711scope, signature
  November13,2023,2012-21supersession and no universal-notice/current-publisher claim.
- Professionalism: verify8text/7visual PDF pages across order/form/list, chair email
  and address,13members/four existing judges, datedJanuary14,2026 membership and
  term-year associations. Keep unknown separate effective date and no automatic
  overwrite of judge contact records. Receipt and stored facts must agree.
- Assert no panel disciplinary/compulsory-attendance power, possible Bar referral
  after nonappearance, panel June/December reporting and omitted personal identifiers.
- Preserve two404original attempts and successful hub-member original, with no
  byte-equivalence claim. Check actual status/text_path before read/render and
  retain failed inspection attempts as errors, not content review. Four report links
  are inventory only; two labels share a URL, not proof of report-body identity.
- Verify source receipts/facts/artifacts, exact/frozen replay, unchanged old personnel,
  unresolved genuine gaps and finalized reports. Scope-specific live assertions are
  in `finish-esi-panel.py`, `finish-record-newspaper.py`, `finish-professionalism.py`.
  Correct generic save acknowledgment labels to zero attached forms, one standalone
  referral form and one member list; source body remains unchanged.
- All nine priority entries may be reviewed while the county remains incomplete.
  Next action must reconcile the larger index audit and evidence gaps; no new county
  or county publication follows automatically from these scoped checks.

### Assignment and index-reuse acceptance evidence (Broward 138–140)

- Reuse must identify successful original bytes, matching URL/hash and a receipt's
  explicit page scope. Separately linked unreviewed forms keep the row pending.
  Partial body review must not silently cover attachments.
- Assignment table checks cover split/misaligned cells, repeated people, express
  vacancies, default and delayed effective dates, footnotes and role typography.
  Compare row pairings against rendered originals, not extraction alone.
- Checkpoint139 verified 135 rows, two vacancies, 101 existing person-key mappings,
  all six pages, separate September28/October1 effective dates, and the literal
  Stephen/Steven discrepancy. Person/contact records were not overwritten.
- Checkpoint140 corrected the referring index URL without changing semantic facts;
  original capture139 remains. Artifact readback, exact frozen replay and unchanged
  finalized reports passed. Its first attempt rejected an absolute artifact path;
  repair used a repository-relative path, then reran save and dependent freeze.
- These live assertions establish scoped evidence handling, not county completion
  or a fresh run of the whole test suite. Validation receipts are in the run's
  `review/assignments-validation.json` and `assignment-correction-validation.json`.

### Senior/quarter assignment evidence (Broward 141–142)

Checkpoint141 verified five originals and11pages,89second-quarter versus88first-
quarter names,explicit authority periods,and the printed Woody D./R. difference.
Comparison checked the two circuit-list additions and Franker's county-list
removal without inferring permanent office changes. Division50 assertions keep
paragraph1's Division53 and paragraph2's omission separate;the stated effective
date preceding signature is retained. Satellite jury rules preserve assigned
judge,Central Courthouse default,approval exception and out-of-period notice.

Checkpoint142 verifies Eade's explicit appointment but rejects contact-completion
claims:all nine unavailable fields stay null,six individual-procedure topics stay
unknown,the source check remains incomplete,and completed-person count stays90.
The Supreme folder extraction must preserve original hash and produce a distinct
text hash containing the actual public-records paragraph. Replay,artifact/fact
readback and finalized-report preservation passed for both packets;these are
scoped live checks,not a fresh full-suite run or county-completion proof.

### Cross-circuit senior review checks (143–145)

- Karlan:preserve Broward appointment plus March19 static directory page7 and
  October16 API directory page9. Check named presence/absence against both
  rendered originals,not cached search text. Retain17collected PDF pages versus
  three reviewed pages including reused appointment;remaining Miami pages are
  not a county-wide roster review.
- Kotey:reuse same-day K-filter/shared hubs;do not populate current chambers from
  historic academic CV or ethics-committee contact results.
- Langer:current directory senior card and retained October16PDF page9 support
  a separately scoped Eleventh Circuit coordinator route. Assert that scope and
  its phone3053497008;Broward contact-assignment verification remains false.
- For all three:current individual chamber/assistant/procedure fields remain
  unknown,source checks incomplete,previous completed-person count unchanged.
  Artifact/fact readback,exact frozen replay and finalized-report preservation
  passed. These live checks do not establish full contact completeness or a fresh
  full-suite test run. See corresponding karlan/kotey/langer-validation.json.

### Final additional senior batch (146–149)

Lebow,Murphy,Schiff and Speiser saved one at a time. Exact frozen replay and
artifact/fact readback passed;all eight additional senior entities exist with
incomplete individual-evidence checks. Earlier90named-person/12officer records
and finalized reports remain unchanged. Speiser's historical signatureMay30,2025
and individual effectiveMay19,2025are distinct;only pages1,2,6of6reviewed. A
historical division does not authorize copying another judge's current contacts.

The run-local basic-senior finalizer checks null current contacts,nine unresolved
fields,six unresolved checklist topics,appointment dates,incomplete source checks,
current capture identity and queue progression. Before acceptance,exercise both
current-packet idempotence and rejection of an older packet with byte-identical
handoff files afterward. These checks cover saved-record mechanics,not substantive
completeness of missing contacts or a production-ready statewide workflow.

### Civil-index checkpoint150

Verify seven row dispositions (civil2,4,5,6,10,14,19) against their source receipts;
30 original index rows remain. Check all seven new originals and exact source dates.
The16new PDF pages were text-read;9were visually inspected. DOC text extraction
does not establish layout/pagination review. The internal-host PDF was not fetched;
its missing-original check remains incomplete despite the reviewed public alternate.

Check normalized text equality only for the stated pairs: court DOC versus Clerk
DOCX worksheet, and court versus Clerk2012-16copies. Their original hashes differ.
Do not treat that normalization as byte/layout identity. Keep residential scope,
the water-transfer order's March11signature/March4nunc-pro-tunc dates, and the
risk-protection-only service scope in saved facts. Require artifact/fact readback,
identical frozen replay, unchanged finalized reports and unchanged person lists.
These are live evidence/persistence checks; no full-suite or county-completion claim.

### Index checkpoint151

Assert20dispositioned rows and10remaining;16saved findings. Preserve18successful
new originals and3HTTP404responses,40new PDF pages collected and12visually
reviewed. Collection does not imply substantive review of all cost-schedule pages.
Assert2012-51action is reinstatement;2012-24signature is2016-07-05with
nunc-pro-tunc2012-04-12. For2023-37/38,the full signature date and signature year
remain null while month/day and order-identifier year remain separate.

Vehicle-title review must include both attachments and the Sheriff letter's30-day
statement. Emergency order/form text comparisons must preserve distinct original
hashes. Three failed indexed sources retain incomplete original-source checks
despite reviewed public alternatives. Inspect receipts and source text before
accepting mechanical validation; confirm saved facts/artifacts, exact frozen
replay, unchanged finalized reports and unchanged person lists. No broad unit-suite
or county-completion claim follows from these checks.

### Index checkpoint152

Verify all43original followup rows have unique dispositions and none remain;
the original158-row audit is preserved. Ten new findings account for the last
ten rows. Thirteen new originals contain42PDF pages, all text-read;17pages have
visual checks. Existing duty-order,ADA and current10Areviews retain their original
scope rather than being counted as new full reviews.

Assert pretrial-form filing cutoff2021-04-30and use cutoff2021-12-03;
mediation/arbitration remain checkbox-dependent. Writ60-day period ends when
the30-day period begins2021-03-01at00:01Eastern; measure issuance from judgment.
Firm exception effective2023-06-15is distinct from signature2023-06-02.
ADAold/new coordinator names remain separately attributed; no inferred appointment
date. Old/new10Aboundary remainsMarch4/5,2018. Verify facts/artifact readback,
frozen replay, unchanged finalized reports/person lists and remaining gap phase.

### Gap-disposition checkpoint153

Verify402original limitations,340contact states and11prior actions are preserved
exactly under753unique ledger IDs, with valid saved observation references. Nine
progress notes may cite later findings; only the old Marra-review action is marked
completed. Rebollo and8senior individual-evidence gaps remain unresolved. Preserve
335unpublished/unestablished fields and the five specially attributed contact states;
do not turn absent direct email/fax/hours into absent shared office contact.

Check the101unique ordinary-assignment names against90existing judge and12officer
reviews: Pole is the sole extra existing senior. Ordinary judge intersection89,
officer intersection12; separate senior list9. These are source-name accounting
checks,not complete-current-contact certification. Verify receipt artifacts,original
audit hash,exact frozen replay,fact/artifact readback and unchanged finalized reports.
Record the initial missing-receipt validation rejection and successful repaired save.


### County review export — verified October16,2026

`tests/test_county_review.py`: six tests passed for pinned stream/capture selection,
lossless facts and citations, read-only persistence, deterministic re-export,
overwrite rejection, missing/corrupt artifacts, HTML escaping/labels/addresses,
and exclusion of historical contacts from current directory cells. Existing
directory/display/history regression:24tests passed.

Live-data validation: `runs/county-broward/2026-10-15/review/validate-review-export.py`
compared178entities against an independently selected latest-observation map,
verified1274artifact hashes and bytes, checked2398local links, repeated the export
byte-for-byte, and verified research database/old directory files and finalized
reports unchanged. Result:`review/county-review-export-validation.json`.
Static semantic structure was checked; browser layout/accessibility and production
directory integration remain unverified. No new legal research or freshness claim.


### County directory supplements — October16 draft validation

74 tests passed across county-directory, county-review, publication and directory
display suites. Tests cover source-role projection, qualifiers, missing and historical
contacts, pending publication rejection, malformed/cross-county/duplicate records,
immutable archive preservation, and default versus historical JS selection.
After the circuit-membership display addition, actual CLI/Node validation rechecked
all five archived reports and10historical queries,112added personnel,181existing
personnel,810source-mapped contact lines,preview reproducibility and production
rejection. See `runs/county-broward/2026-10-15/review/county-directory-v4-validation.json`.
JS syntax and git whitespace checks passed. No browser visual check or complete
manual112person projection audit is claimed. Prior previews/drafts are preserved.


### Manual county contact display audit — October16

All112Broward projected people reviewed in five bounded batches. The presentation
audit accounts for every source contact field:729display rows,72exact fully
qualified chamber duplicates removed,9null-value display rows omitted,and402
ancillary/source-format fields retained in the research packet. Nineteen selected
contact-difference summaries are pinned to exact source-conflict hashes.

78tests passed across county-directory, county-review, publication and directory
display suites,including ordering,qualified code deduplication,historical/unlabeled
email notes,duplicate field accounting and stale editorial-note rejection. Actual
CLI/Node validation confirms5unchanged archived issues,10historical selections,
181preserved plus112new personnel,and pending-publication rejection. No browser
layout/accessibility check claimed. See `review/county-directory-v6-validation.json`
and `review/directory-manual-presentation-review.json` in the Broward run.

The quickstart's exact one-person read command executed successfully and returned
1602bytes; the roadmap contains67distinct counties. The initial roadmap check
counted its Markdown separator as a county; excluding header/separator rows fixed
the checker without changing the county inventory.

### Full project validation — October 16

Default pytest initially collected preserved run/worktree tests and failed with
four import-path mismatches. `pyproject.toml` now sets `testpaths = ["tests"]`;
archived work is unchanged. The default command then passed all 430 active tests
in 2.95 seconds, with no warnings reported. A wheel built successfully; county
modules and all seven source web assets match source bytes. The first asset
checker incorrectly expected generated directory.html in the source inventory;
correcting that expectation required no package change. Evidence: Broward
`review/project-validation-20261016.json` and its test/build logs. These checks
do not establish browser layout, source freshness, or publication approval.

## Officer assistant-name and negative-procedure regressions

Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_officer_review.py`.
Check that a source-supported `TBD` is retained separately from a null unpublished
name; verified placeholders are rejected; absent/malformed search logs, missing
reasons, contradictory non-null names and uncited placeholder text are rejected.
The absence branch must still call citation validation and must not mutate the
receipt. Role/contact/procedure association checks continue to apply. Unit tests
mock binding checks to isolate these branches; validate the real Williams receipt
and previous completed officer receipts against retained originals separately.

Negative procedure contract (Hillsborough Frank revision 1): a supported
`no_published_procedure_located` procedure is accepted only with the exact person
association, a real citation, a nonempty absence reason, a nonempty structured
search log of `{url, search, result}` rows with real http(s) URLs, and an empty
document inventory; unknown statuses, empty/malformed/non-URL logs, borrowed
person associations, missing reasons or citations are rejected. The negative
branch must still call citation validation and must not mutate the receipt or
convert statuses. Verified procedures still require a nonempty document
inventory with applicability, review scope and citations. Unit tests mock binding
checks to isolate the branches; validate the real Frank receipt and all
previously accepted officer receipts against retained originals separately
(worker48/cloud51 unit tests;9/9previous receipts unchanged with recursive citations).

## Hash gate and seven-court opinion discovery

Run `pytest tests/test_source_gate.py tests/test_opinion_discovery.py
 tests/test_research_history.py tests/test_baseline_capture.py` (one shell line).
Use disposable databases and fixture HTTP transports; never mutate production
history to simulate a finalized baseline.

Required behaviors: unchanged parent/changed linked PDF; unchanged unreviewed;
raw HTML changes despite identical extracted text; blocked/oversized responses;
stale review and unsupported/mismatched citations; partial-run resume; registry
removal warning; protocol invalidation; effective-date tasks; all seven courts in
the actual update CLI; server-capped pagination; duplicate IDs; late postings;
revised PDFs; withdrawal/status change without PDF change; incomplete listing;
explicit/default baseline and partial-run nonadvancement. Preserve a regression
for Supreme consolidated-case filenames containing spaces.

Live acceptance: run the actual standard command in a separate database, retain
original listing/detail/document bytes and actual timestamps, and inspect all
fourteen channel coverage records and source failures. Reuse successful captured
responses transparently when repairing a parser; do not claim a replay is a fresh
retrieval. No historical production report verification belongs in final integration.

## Deterministic coordinator acceptance

Run `tests/test_workflow.py` plus opinion-discovery, publication-evidence, source-gate and directory suites. Verify exact-packet/receipt replay; interruption after a committed domain review; no acquisitions from status; unchanged review reuse; failed/duplicate listings retained as gaps; partial-page resume; source-bound report mapping and separate editorial acceptance; alias decisions; preservation of county assignments, absent contact fields and unrelated people; stale directory/build rejection. Run the supported `workflow trial-init` scenarios through actual CLI commands in an isolated root. Complete one real model-reviewed preview, inspect its rendered output, and retain its capture IDs and status. No live deployment or historical-report audit is required by this trial.
