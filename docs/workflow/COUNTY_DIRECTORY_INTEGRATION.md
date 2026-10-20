# Dated county directory integration

County expansion adds a separately dated directory supplement. It does not edit
finalized weekly reports, fabricate a new weekly update, or import a partial county
into the legacy seven-county directory database. The original research capture
remains incomplete until its actual completion criteria are met.

## Implemented draft path

1. Use the pinned, validated packet from `COUNTY_REVIEW_EXPORT.md`.
2. Project personnel with `flwu.county_directory.make_supplement(packet, courts)`.
   Provide navigation URLs supported by the saved county sources. Preserve the
   three county resources: Official Records, Court Records, Tax Assessor.
   Where a contact difference is recorded outside the contact block, supply an
   explicitly reviewed `contact_notes` selection. Each selection pins the complete
   source-conflict hash and the selected conflict index; changed source facts must
   be reviewed before reusing old editorial wording. Broward's exercised example
   is run-relative `review/directory-contact-notes.json` (19 notes for18people).
   Review `court_ids` for each person before acceptance. The generic projector
   initially includes every supplied group; this is a draft convenience, not
   evidence of assignment to every court. Use the saved assignment to distinguish
   circuit, county and shared responsibilities; preserve cross-assigned personnel
   in each supported group. Record each selection with its source facts digest,
   then recompute the supplement digest and validate. Hillsborough's worked
   example is `review/cloud-material-followups/prepare-directory-5081.py` and its
   `court-membership-review-5081.json`. Do not infer elected office from assignments
   or treat preliminary HTML discovery categories as dispositive.
3. Save the returned supplement and field audit to new files in the county run.
   Generation always sets `review_status=pending`; it never grants approval.
4. Inspect every field omitted by the projection. Ancillary interpreter, clerk,
   Zoom and program contacts are not chambers contacts. Keep them in the research
   packet. Preserve different source statements, source-purpose restrictions,
   historical limitations and address qualifications in the projected contact
   notes. No guessing personal email addresses or replacing missing senior
   contacts with a court coordinator's contact information.
5. Build a new local preview directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/flwu site build \
  --archive website/updates --preview \
  --county-directory runs/county-broward/2026-10-15/draft/county-directory-4886-v5.json \
  --output output/county-review/broward-preview-next
```

`--county-directory` may repeat for multiple reviewed counties later. Duplicate
county supplements, duplicate personnel identities, conflicting navigation groups
and replacement of another county's personnel are rejected. Do not infer removals
from absent records. Explicit retirements/deletions will need separately supported
review before introducing a removal mechanism.

## Temporal and display behavior

- Only the default directory view (including a court-only filter) combines the
  newest issue's saved directory with supplements. It labels each supplement's
  recorded observation date. This date is not a claimed legal effective date.
- Every explicit `issue`, `from`, or `to` query uses the issue's saved contacts,
  including invalid/empty date parameters. Current contacts are never inserted
  into historical date-range results. Archived issue JSON remains byte-for-byte
  unchanged. A county absent from an old snapshot shows the existing empty state.
- The four existing personnel columns and responsive layout remain. Names link
  to official profiles when recorded; a compact Procedures link uses the saved
  individual URL. No Evidence Coverage section or additional source columns.
- Address arrays render one line per component. Source qualifications are in
  expandable Contact notes within the relevant cell. Explicit uncertain source
  phone/email variants are retained as text rather than recommended action links.
  Names come before assistant contact lines; office phones come before email and
  addresses. Remove a repeated chamber code only when that same fully qualified
  code is already in the address; never infer a wing from an unqualified room.
  Empty values and exact duplicate lines may be omitted from presentation with
  recorded reasons, while their original facts remain in the research packet.
  Historical/unlabeled email targets stay in notes without contact-action links.
- Senior judges with unavailable individual contacts remain labeled unverified.
  Historical identity reconciliations, such as Rebollo/Marra, are retained in the
  review packet rather than projected as verified current personnel.

## Acceptance and release

The public builder rejects pending supplements without `--preview`. After actual
county legal/data and visual review and the applicable county acceptance checkpoint, a new
reviewed copy must name `reviewed_by`, timezone-aware `reviewed_at`, and a specific
`attestation`, then recompute `content_sha256`. Do not fabricate that review or
change the original draft. The same file can then be supplied explicitly to
`flwu publish --county-directory PATH`; deployment still requires authorization.
No supplement is auto-discovered from the research database or silently deployed
by CI. Wire an approved county file into the deployment command only at release.

For the active statewide project, the October 17/18 user override assigns county
acceptance to cloud review and authorizes proceeding between counties without
another user approval. Historical notes below describe earlier checkpoints; they
do not reinstate that superseded gate. Publication authorization remains separate.

Test requirements: default versus explicit historical selection in actual JS;
preservation of issue data and old county contacts; pending-publication rejection;
source-field role/qualifier mapping; duplicate/cross-county guards; navigation on
all pages; responsive rendering, keyboard operation and directory filters in a
browser. Unit/static checks do not certify browser appearance or source accuracy.

Broward's current local preview is `output/county-review/broward-site-4886-v6/`.
Its snapshot remains pending. Manual contact presentation/field-disposition review
is recorded for all112people in `review/directory-manual-presentation-review.json`;
this is not a new source retrieval or current-law certification. This paragraph
describes that historical preview, not the current research acceptance state.
The October 17–18 instructions authorize cloud county acceptance and progression
without another user checkpoint. Preview generation does not authorize publication.

### Hillsborough compatibility and preflight

The projection and review exporter recognize the existing `judge` and `clerk`
finding kinds as well as the original `county_*_baseline` kinds. Do not rewrite
historical findings merely to match Broward's naming convention. Hillsborough's
flat clerk fields are projected explicitly: office phone, mailing address, public
contact form and its limitation, each named location's address/hours, and service
qualifications. A repeated common phone is omitted with an audit reason; a distinct
location phone remains. Null direct email does not become an invented mailbox.

A literal backslash in a saved source URL's path is percent-encoded as `%5C` in
the public source reference, not replaced with `/`. Original URL/hash and public
URL are recorded in the projection audit, with original citations unchanged in
the research packet. Unsafe authorities, control characters, credentials and
schemes remain rejected by the unchanged URL policy. Hillsborough's four affected
Giardina/Griner PDF URLs returned identical bytes via the encoded path; see
`review/cloud-material-followups/url-path-encoding-check.json` in its run.

`check-directory-compatibility.py` in that folder checks the actual saved Hillsborough
capture read-only: 69 judges, 8 magistrates, 7 hearing officers and 1 clerk project
and pass pending-supplement validation without altering source facts. This is a
compatibility preflight, not accepted county data, a completed contact presentation
review, a visual check, or publication. Use the later accepted checkpoint for the
actual directory review. Twenty-six focused directory/export tests passed.

The Hillsborough field audit also covers office_phone/email/fax/address fields,
division-specific routes, source-qualified alternatives, and the legacy
`mailing_address`/`physical_address` objects containing `lines`. These are contact
data, not ancillary fields to discard. Alternative or uncertain source values
remain labeled notes; their qualifiers must accompany the values. Unpublished fax
objects display only their recorded absence status, with research search logs
retained in the packet and summarization recorded in the audit. Citation objects
and Zoom meeting/password/dial-in metadata stay in the procedure/research record.

`check-directory-fields.py` verifies the actual draft's 495 contact rows against
original fact paths for all85people and requires an explicit disposition for every
omitted contact field. It is not a substitute for visual review. After this field
mapping correction, 28 focused directory/export tests passed.

### Contact presentation and source differences

Address display may insert whitespace after commas, between `FL` and a five-digit
ZIP, and between `Room`/`Suite` and a number. It must not change address tokens,
choose a conflicting room, or edit saved source facts. The projection audit records
original and display lines for each changed address. The field audit independently
compares line counts and non-whitespace characters rather than calling the formatter
as its own correctness check.

Use `make_supplement(..., contact_notes=...)` for concise editorial explanations of
contact differences. Each person's selection must pin `expected_conflicts_sha256`
to the saved conflict list and identify each selected `conflict_index`. Describe
each source's statement and its relevant date or purpose without selecting which
controls. These notes appear in an expandable Contact differences section; retain
all original conflicts in the database. Do not copy procedural deadline disputes
into the contact table. A changed conflict list invalidates the selection and
requires review before reuse.

Hillsborough's current selection is
`runs/county-hillsborough/2026-10-16/review/cloud-material-followups/directory-contact-notes.json`
(33 notes for 26 people). This is editorial work on already-saved evidence, not a
new source review. Preview v3 passed schema/source-pin validation and a partial
Safari desktop check of corrected addresses and the Nash disclosure. It remains
pending final capture integration, complete presentation review and narrow-layout
verification; do not infer publication approval from this record.

Known alternate/guide assistant-name fields and absence status belong in expandable contact notes. A verified fax object with exactly source_label/status/value displays the original label and number, retaining qualifications such as “if applicable”; internal verification status remains in the research record and summarization audit. Unknown object shapes remain intact rather than being silently reduced.

## Seminole release integration — October 19, 2026

`website/county-directories/seminole.json` is the reviewed copy of the capture6909 directory, accepted at research checkpoint6911. Its23people retain documented missing contacts and source differences. The Pages workflow and its generator explicitly supply this file and watch the county-directory folder. The production build passed all519tests; browser checks showed8county rows by default and0for an explicit historical range. These are local validation results, not a deployed-site claim. Preserve the original draft and immutable report files. Other counties still require their own reviewed supplement integration.

Volusia release integration also uses the reviewed `website/county-directories/volusia.json`, based on accepted checkpoint6855. The original draft hash was verified against the database artifact before promotion. Combined production build `output/county-review/combined-production-6911` passed519tests and eight browser default/historical court-filter checks: Volusia14/0, Seminole8/0, Seventh Circuit54/19, Eighteenth Circuit23/0 rows. Existing Seventh Circuit historical personnel remain; current supplements do not enter historical results. Both supplements are wired explicitly in the workflow generator and checked-in workflow. Neither is deployed yet.

Brevard release integration uses `website/county-directories/brevard.json`, verified against the draft artifact retained at checkpoint6777. The three-county production build includes90supplement personnel (Brevard32, Volusia35, Seminole23). All519tests pass. Browser checks show Brevard12county rows and55Eighteenth Circuit rows, including Melanie Chase; explicit historical ranges show0for both. Recorded gaps remain; no new senior-roster completeness claim. This is local integration, not deployment.

Osceola bounded acceptance6965: website/county-directories/osceola.json explicitly added to Pages workflow and generator alongside the three prior supplements.22personnel,92contact fields; magistrates labeled accurately and repeated clerk phone omitted in display only. Build output/county-review/four-county-production-6965 passes519tests; current county6/circuit22 and historical0 checked in browser; six archive files unchanged. Senior roster403 and unpublished Ferrer assistant name remain. No commit/deployment. Cross-county Orange identities must be reconciled when that supplement is added.

Sarasota reviewed supplement accepted7033 is explicitly wired into Pages/generator. Five-county production build passes519tests; browser Sarasota7/Twelfth26, historical0, prior counties retained. Six archive files unchanged. No deployment. Manatee integration must reconcile shared Twelfth Circuit identities rather than duplicate them.

St. Lucie bounded acceptance7337: reviewed18-entry supplement explicitly added to Pages workflow/generator. Production ten-county build passes521tests; browser1280/390 county4/circuit18/historicalJuly0, no overflow/draft label. Five finalized archive JSON hashes unchanged. Current assignment qualifications and unconfirmed traffic-officer county scopes remain documented. Official appraiser homepage used after legacy deep link403; homepage200 with browser console warnings/errors retained. No deployment claimed.

Escambia bounded acceptance7399: reviewed22person/108contact-field supplement integrated alongside ten existing supplements. Eleven-county production build passes521tests; browser circuit22/county6/historicalJuly0 and existing StLucie4, no overflow/draft label. Five archiveJSON hashes unchanged. Senior county/contact gaps retained; no deployment.

### Generic personnel observations

Generic `person` findings require an explicit recognized role. The projector supports circuit/county/chief/senior judges, general magistrates, child-support hearing officers and circuit-court clerks. Unknown roles raise an error rather than silently dropping a person or guessing a role. Research facts remain unchanged. Empty contact arrays display a missing-source note. Review court memberships separately; generic projection is not publication acceptance. Bay checkpoint7763 preflight projects22people; contact qualifications, assignments, navigation and browser validation remain pending.
