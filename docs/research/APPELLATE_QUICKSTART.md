# Appellate baseline: source map and update instructions

This is a bounded, agent-led evidence baseline for the Florida Supreme Court and six DCAs. It is not an unattended crawler, a new-law report, or a requirement to review every administrative order. Use the current goal and AGENTS.md; no local workers.

## Resume from saved evidence

Read the latest captures in `manual_research:appellate-baseline-v1:1998d30845c8` from `~/.local/share/flwu/research-history.sqlite`. The October 22 shared-practice captures are 9257–9281 (odd sequence numbers). Roster acceptance/publication is recorded separately at 9033/9035. The [review inventory](../../research/audits/20261022/appellate-practical-procedures.json) supplies each source URL, retrieval timestamp, original/extraction hash, review scope, conflict and limitation. Do not rerun successful one-shot capture scripts.

For personnel, consult the saved official roster/profile first. Finish identity, assignment, chambers and assistant contacts, clerk routing and official procedures for one person before moving on. Shared court clerk numbers are not personal chambers numbers. Preserve a bounded-search gap when personal contacts are unpublished; see [gap accounting](../../research/audits/20261022/appellate-gap-accounting.json).

## Where to search and what to review

Use these exact saved official sources before further searching. Follow an additional link only to fill a missing required contact or practical filing/appearance requirement. Search the official court domain for that specific missing field; log query, URL, timestamp and result. Do not search individual lawsuits or collect all historical orders.

### Florida Supreme Court

- Capture 9275: Public oral-argument access. [Official source 1](https://supremecourt.flcourts.gov/visit-us/oral-argument)
- Capture 9257: General filing information. [Official source 1](https://supremecourt.flcourts.gov/Practice-Procedures/General-Filing-Information)

### First District Court of Appeal

- Capture 9259: General frequently asked questions. [Official source 1](https://1dca.flcourts.gov/Resources/General-Frequently-Asked-Questions)
- Capture 9273: Material filing, agreed extension and remote argument orders. [Official source 1](https://1dca.flcourts.gov/content/download/869955/file/AO%2023-1.pdf) [Official source 2](https://1dca.flcourts.gov/content/download/429513/file/19-2%20In%20re%20Agreed%20Extensions%20of%20Time%20for%20Briefs.pdf) [Official source 3](https://1dca.flcourts.gov/content/download/746732/file/AO%2021-1.pdf)

### Second District Court of Appeal

- Capture 9277: Electronic filing and argument notice. [Official source 1](https://2dca.flcourts.gov/E-Filing) [Official source 2](https://2dca.flcourts.gov/Oral-Arguments/Oral-Argument-Notice)
- Capture 9261: Shared practice preferences. [Official source 1](https://2dca.flcourts.gov/Practice-and-Procedures/practice-preferences/Oral-Argument) [Official source 2](https://2dca.flcourts.gov/Practice-and-Procedures/practice-preferences/Notices-Motions-and-Records) [Official source 3](https://2dca.flcourts.gov/Practice-and-Procedures/practice-preferences/briefs-and-briefwriting)

### Third District Court of Appeal

- Capture 9279: Material shared submission orders. [Official source 1](https://3dca.flcourts.gov/content/download/430076/file/AO3D13-6.pdf) [Official source 2](https://3dca.flcourts.gov/content/download/430075/file/AO3D13-5.pdf) [Official source 3](https://flcourts-media.flcourts.gov/content/download/2488770/file/AO3D26-01%20Signed%2001.pdf)
- Capture 9263: Clerk notice and shared filing guidance. [Official source 1](https://3dca.flcourts.gov/clerk-s-office/notice-to-attorneys-and-parties) [Official source 2](https://2dca.flcourts.gov/Practice-and-Procedures/practice-preferences/briefs-and-briefwriting) [Official source 3](https://3dca.flcourts.gov/clerk-s-office)

### Fourth District Court of Appeal

- Capture 9269: Notice to attorneys/parties and argument request notice. [Official source 1](https://4dca.flcourts.gov/content/download/301/file/Notice%20to%20Attorneys%20and%20Parties%20-%20September%202023.pdf) [Official source 2](https://4dca.flcourts.gov/content/download/300/file/OA%20Notice.pdf)

### Fifth District Court of Appeal

- Capture 9281: Oral argument preference form. [Official source 1](https://5dca.flcourts.gov/content/download/813936/file/OA%20Preference%20Request%20Form.pdf)
- Capture 9265: Clerk shared practice guidance. [Official source 1](https://5dca.flcourts.gov/Clerk-s-Office)

### Sixth District Court of Appeal

- Capture 9271: Material civil briefing, argument and possession orders. [Official source 1](https://6dca.flcourts.gov/content/download/2435228/file/AO%2024-01%20Signed.pdf) [Official source 2](https://6dca.flcourts.gov/content/download/857361/file/6DCA-AO-23-02-In-Re-Remote-Video-Oral-Argument.pdf) [Official source 3](https://6dca.flcourts.gov/content/download/857364/file/6DCA-AO-23-03-In-Re-Agreed-Extensions-of-Time-for-Briefs.pdf) [Official source 4](https://6dca.flcourts.gov/content/download/2482903/file/Amended%20AO%2025-02.pdf) [Official source 5](https://6dca.flcourts.gov/content/download/2487113/file/AO%200001.pdf)
- Capture 9267: Filings information and electronic filing. [Official source 1](https://6dca.flcourts.gov/clerk-s-office/filings-information) [Official source 2](https://6dca.flcourts.gov/clerk-s-office/e-filing)

## Collection and review contract

1. Preserve the actual HTTP response bytes before parsing. Record requested/resolved URL, actual acquisition timestamp, status, MIME type and SHA-256. Save extraction separately, with its own hash. Failed pages are acquisition evidence, not supporting substantive evidence. Never print or commit embedded credentials; originals belong in the local database.
2. For flcourts pages, inspect structured page content, not just footer text. `scripts/flcourts_article.py` and `scripts/flcourts_folder.py` handle their documented content shapes. FAQ answers may be embedded in `props.pageProps.childrenInfos`; an empty article extraction does not prove no guidance exists. Preserve the original and label the extraction method.
3. For PDFs, read the relevant operating provisions and visually inspect scanned pages or ambiguous dates. Use installed tools only. A selected visual transcription is not full OCR. Record collected, partially reviewed and reviewed scope separately.
4. Write a concise structured checklist for filing/submissions, conferral, scheduling/appearance, communications and access as applicable. Keep original statement, locator and citation alongside the summary. Distinguish public attendance from counsel permission, a preference request from approval, and an old linked order from proof of current legal supremacy. Retain stated issuance/revision/effective dates independently; unknown remains unknown.
5. Preserve conflicts without deciding which controls. Examples retained here include differing Second/Third DCA AI-rule dates and the Third DCA emergency order’s heading date versus “immediately” wording. Do not delay baseline publication for adjudication. Do not convert first observation into a new legal development.

## Save, verify, compare and publish

Use `flwu.history.record` for appellate shared findings; the county-only `flwu.baseline_capture` scope validator is not an appellate packet format. Keep the exact existing stream scope from the database. Supply `mode=manual_research`, a new stable run ID, `status=incomplete`, findings with stable keys and citations, explicit checks and an artifact map of hash to original bytes. Preserve existing findings; do not rewrite captures. The exercised local saver is `runs/statewide-completion-audit/2026-10-22/save-practice-pages.py`; it is a local receipt-driven aid, not a public installed command.

Preflight the payload in a temporary database, then record once in the shared database. Verify capture payload readback and every artifact hash/byte match; identical replay must return the same receipt. Save the acknowledgement and review inventory. Passing structural validation does not replace reading the source.

Use the installed `flwu history changes --database <database> --stream <exact-stream> --start <YYYY-MM-DD> --end <YYYY-MM-DD> --output <new-file>` command for an explicit period. Omit `--start` only when last-finalized-report comparison is intended. If the stream has no finalized report, preserve `baseline_known: false`; never substitute its latest partial run. See [baseline capture](../workflow/BASELINE_CAPTURE.md).

Shared research summaries remain in the database; they are not automatically new weekly updates. Current personnel/profile/procedure links are published through reviewed directory supplements under [directory publication](../workflow/COUNTY_DIRECTORY_PUBLICATION.md). Never finalize a report just to publish contacts or baseline research. Final integration verifies current database/publication consistency and future comparison behavior, without historical-report checks.
