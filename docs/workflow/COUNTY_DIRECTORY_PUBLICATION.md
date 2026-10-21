# Publishing current court directories

The current directory combines the latest finalized report snapshot with explicitly
reviewed, separately dated files in `website/county-directories/`. These files
publish contacts, assignments, profile links and individual procedure links from
saved county research. They are not new weekly reports or assertions that every
county research task is complete. Raw originals, detailed review findings and
working drafts remain in the research database.

An explicit issue or date range uses its original report snapshot and excludes
current supplements. Preserve archived report JSON bytes. Publishing a directory
must not advance the last-finalized-report comparison baseline.

For each release:

1. Pin the county stream and saved capture. Compare the selected directory draft
   against later personnel observations; reconcile any changed or missing person.
2. Check contact field dispositions and court memberships against saved facts.
   Retain source conflicts and missing contacts. Circuit views include personnel
   serving the circuit's covered counties; county-court views honor explicit
   reviewed membership. Records from different county assignments can retain
   separate scoped observations, even when the same person serves both counties.
3. Verify original source artifact hashes against the database. Public metadata
   keeps source URLs, hashes, dates and statements, but excludes private file paths.
4. Review the combined desktop and mobile directory, all court filters, links,
   historical exclusion, and retained earlier entries. Label partial county
   coverage with `coverage_note`; never imply that a partial set of reviewed people are a
   complete county roster.
5. Set review status, actual reviewer/timestamp/attestation and recompute the
   content checksum. Production builds reject pending files. Explicitly add each
   reviewed filename to both `publish_workflow_config()` and the checked-in Pages
   workflow. No database stream is automatically published.
6. Test and build against current remote main, retaining newer site design work.
   Publish only website data and required code; exclude private databases, raw
   workspaces and caches. Check the actual deployed page after Actions succeeds.

The initial October 19 release included 23 supplements (1,000 county-scoped
personnel observations), adding to the original seven-county and appellate snapshot.
At that release Alachua contained 17 judge reviews. That partial supplement was
replaced by the reviewed Alachua refresh below. Duval's supplement adds reviewed officers to its earlier
snapshot. Missing contacts and documented source differences remain qualified.
The five finalized reports retain their original dates and contents. Collected
legal research is not automatically presented as a newly finalized law-change
report merely because directory publication occurs.

The October 19 Alachua refresh uses evidence checkpoint 7531, accepted at 7533:
25 people (19 judges, five officers and the clerk), preserving the earlier 17 entries. Contact gaps and source qualifications remain explicit. Special-master and magistrate/hearing-officer roles are preserved. Current supplements remain excluded from historical selections.

The October 19 Okaloosa addition uses evidence checkpoint 7563, accepted at 7565:
12 people (nine judges, two judicial officers and the clerk), with 59 contact fields
checked. County and circuit views, mobile layout and historical exclusion were
reviewed. Recorded gaps remain explicit; the property-appraiser destination is
verified through the clerk referral but returned 403. No historical issue is changed.

The October 19 Hernando addition uses evidence checkpoint7603, accepted at7605:
12 people (nine judges,two officers and the clerk), with61 contact fields checked.
Desktop/mobile county views, circuit membership and historical exclusion were
reviewed. Shared office numbers, qualified addresses and source gaps remain
explicit. The five finalized reports are unchanged.

The October 20 Santa Rosa addition uses evidence checkpoint7709, accepted at7711:
ten people (eight active judges, one circuit-wide senior and the clerk). Its
reviewed supplement is wired alongside the existing26files in the Pages workflow
and generator. Combined preview showed4county rows,44First Circuit rows and0Santa
Rosa rows in an explicit historical range, with no overflow at390/1280pixels.
Senior personal contacts/procedures and filing-channel/window-hour gaps remain
explicit; a historical officer reference does not establish current service.
Release validation passed530tests, workflow/generator parity and a production build.
Production browser checks confirmed county4/circuit44/historical0, no draft label
and no overflow at390/1280. The first build attempt rejected a pre-created empty
output directory; retry with a fresh output succeeded. This is not deployment.

Bay acceptance7767 uses evidence7765:22people (17active judges,one senior,three officers,clerk). Production integration passes542tests and workflow parity; browser county6/circuit22/SantaRosa4/historicalBay0 at390/1280 without overflow. Keyboard skip-link and contact targets checked; Roberts office qualifiers preserved. Five historical reports unchanged. Live deployment remains pending.

October20 live verification: PR29 merged287bcbed8d2cc7c707d028c9c706cb4096f2867a, Pages39517117982 succeeded. Bay and Santa Rosa now published. Actual domain browser returned200 with Bay6/FourteenthCircuit22/SantaRosa4 and historicalBay0; no overflow at390/1280. Publication receipt7771 preserves573artifacts/29findings, replay verified, five reports unchanged.

Indian River accepted7817 from evidence7815:17entries with gaps/conflicts qualified.29supplement production build and542tests passed; county7/circuit35/priorStLucie4/historical0 at390/1280 without overflow. Five historical reports unchanged. Live publication pending.

Indian River live publication verified7821: PR30/05cb0ef, Pages39522863691 success. Actual domain HTTP200,county7/circuit35/priorStLucie4/historical0 at390/1280, no overflow/draft.318artifacts/30findings read back/replayed; five reports unchanged. Upstream Actions Node20/24 and library deprecation notices retained in release log.

Citrus accepted7855 from evidence7853:11entries, source gaps/conflicts qualified.30supplement production build and542tests pass; county4/circuit62/priorHernando4/historical0 at390/1280 without overflow or draft label. Five historical reports unchanged. Merge/Pages/live verification pending.

Citrus live verified7857: PR32/4a01f20b, Pages39527265624 success;30supplements published. Actual historical July1 snapshot excludes Citrus. **Browser checks must use `from` and `to` (not `through`), await the hashed archive JSON and rendered content, and prove a saved issue was selected.** An empty/no-matching-updates result does not prove historical isolation. Earlier Citrus preview checks used the wrong parameter; final live validation corrected this.

Highlands accepted8015 from8013:19entries,82contact rows.544tests/workflow parity/production build pass; county5,circuit65,priorFlagler3,historical0 at390/1280 without overflow/draft. Vacancy and November2 appointee distinct; traffic personal contacts and senior assignments qualified. Five finalized reports unchanged. Live publication pending.

Highlands live verified8017: PR40/dbc18d3, Pages39540743395 succeeded. Actual domain county5/circuit65/priorFlagler3/historical0 at390/1280 without overflow/draft;34supplements published.315artifacts/26findings read back/replayed, five historical reports unchanged. Nassau next.

Nassau accepted8041 from8039: eight entries,37contact rows, seven stable snapshot identity replacements and Wallace added. Existing Duval chief remains without duplication.546tests/workflow parity/35supplement production build pass; county3,circuit77,priorHighlands5,historicalNassau7 at390/1280 without overflow/draft. Five finalized reports unchanged. Merge/Pages/live verification pending.

Astra-only. Nassau live verified8043: PR42/34cceb3a2cb56ad3af747ebf9a99916191ebc326, Pages39543384088 success. Eight current entries,37contact rows; seven stable snapshot replacements and Wallace added; chief not duplicated.160artifacts/12findings readback/replay, five finalized reports unchanged.546tests and35supplement production build passed. Actual domain1280/390 county3,circuit77,priorHighlands5,historicalNassau7; no overflow/draft.35supplements published. Next Walton, then Monroe and Putnam; reuse First Circuit sources, one person before next. No local workers or inference changes.

Walton accepted8067 from8063: five new entries,28contact rows; existing FirstCircuit chief/senior retained without duplicate rows.546tests/workflow parity/36supplement production build pass. Preview and production1280/390 county2,circuit49,priorSantaRosa4,historicalWalton0 on actualJuly1issue; no overflow or production draft. Desktop/mobile screenshots, contact links and keyboard skip reviewed.135artifacts/12findings readback/replay verified; five historical reports unchanged. Historical magistrate current service and indexed senior-order body remain documented gaps; property-appraiser destination403 has official referral. Merge/Pages/live verification pending.

Astra-only. Walton live verified8069: PR44/99d9e78924154fe7a633fc1b4da28f373f33a771, Pages39546209924 success. Five new entries,28contact rows; existing FirstCircuit chief/senior retained.137artifacts/12findings readback/replay, five finalized reports unchanged.546tests and36supplement production build passed. Actual domain1280/390 county2,circuit49,priorSantaRosa4,historicalWalton0 on actualJuly1issue; no overflow/draft.36supplements published. Next Monroe, then Putnam, one person before next; retain practical scope and documented gaps. No local workers or inference changes.

Astra-only. Levy accepted8221 from evidence8219: eight personnel,52contact rows, three existing circuit-wide judge records reused without duplicate publication.143 source artifacts verified;547tests and41supplement production build pass. Preview/production1280/390 county2/circuit46/priorJackson2/historicalLevy0 on actualJuly1issue, nooverflow or production draft. Original acquisition dates/conflicts/gaps retained; five finalized reports unchanged. Merge/deploy/live verification pending. USER INSTRUCTION: pause goal after Levy publication; do not begin another county.

STOP — user-directed pause after completed Levy County. Astra-only execution remains the authority when resumed. Levy published and live verified8223/packet016: eight personnel,52contact data points; three existing circuit-wide judge records reused. PR54 merged d4f8dd4b68c887beb709d742019af76a3230cd75; Pages39599444311 succeeded. Live1280/390 county2/circuit46/priorJackson2/historicalLevy0, HTTP200/nooverflow/nodraft; actualJuly1issue selected.547tests passed;41reviewed supplements published; five finalized reports unchanged. Source conflicts and bounded gaps retained. Do not begin another county until user resumes.

Pages emitted upstream Node20/24 and Ubuntu runner-migration notices; deployment succeeded. Evidence receipt retains full output.


### County-specific refresh of a shared historical identity

When the same historical person serves multiple counties with different offices or assignments, retain the county-specific personnel ID and add `legacy_person_id` with the reviewed historical ID. Verify the exact name and county against the finalized directory; the builder rejects unknown or mismatched mappings. Do not alter historical reports or force distinct county contacts into identical records. The current view removes only that county from the older shared membership and renders the separately reviewed county observation. Other counties and historical/date-filtered views retain their original membership. Identical shared records can continue to use their common ID.

Union uses this mapping for Walker, Bullard and Davis. Validate both supplement ordering, county-specific contacts, preserved other-county membership, and unchanged historical contacts.
