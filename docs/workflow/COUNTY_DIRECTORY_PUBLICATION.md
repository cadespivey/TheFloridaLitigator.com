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
