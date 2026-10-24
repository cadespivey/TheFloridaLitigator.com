# Publication integrity acceptance contract

Intent: a screening receipt must not imply a reviewed public update. Every relevant
finding must survive into a supported published item/directory record or an explicit
supported exclusion. Fail closed on missing provenance and incomplete mapping.

## Implementation and behavioral checks

- `evidence_binding.py`: exact acquisition URL, raw/extraction hash pair, retrieval
  timestamp and HTTP result. Tests mutate each binding, invent quotes, substitute
  same-host pages and reuse mismatched legacy status metadata; each must fail.
- `research.py`: required task URL, pinned database, actual named roster citation,
  stable identity and matching person receipt. Test same-host substitution, wrong
  database override, placeholder names and different person names.
- `source_gate.py`: acceptance v3, exact current/previous support and changed-line
  coverage for no-change conclusions. Test unreadable extraction, heading-only
  quotes, partial diff coverage, stale receipt reuse and baseline-review bypass.
- `publication_acceptance.py`: latest report, exact report bytes, bound standard
  update queue, all relevant finding versions, included report text, directory
  fact equality, actual people and explicit removals from finalized predecessor.
  Tests cover omitted findings, changed report bytes, wrong candidate mapping,
  wrong roster roles/names, omitted inventory, unsupported retirement and altered
  contact values. A separate acceptance manifest is mandatory for finalize/export.
- `publication_pending.py`: exact denominator of source/opinion/effective-date and
  discovery tasks. Test omissions, unsupported scope exclusions, genuine retrieval
  failures and available evidence mislabeled unavailable. A recorded gap is not a
  no-change conclusion. In-scope reviews are completed before queue refresh.
- `history.py`: SQLite writer reservation covers validation and acceptance/finalize
  persistence. A real second connection must fail to write during validation and
  succeed after release. Failures leave neither approval nor finalized baseline.
- CLI regression invokes review-template, accept and finalize, checking rejection
  of incomplete manifests and report modification after acceptance.

Run tests with the existing root virtualenv, PYTHONPATH=src and
PYTHONDONTWRITEBYTECODE=1. Use disposable databases. No historical-production-report
verification is required or authorized as part of this integration.

## Human/model review boundary

Hash and quotation checks establish identity and coverage, not legal significance.
The invoking reviewer must read the relevant changed passages, determine scope,
check official roster coverage and inspect rendered output. Never use a generic
hostname/keyword classifier to generate completed reviews. Never fabricate an
independent reviewer or claim a test proves semantic legal accuracy.

## Release acceptance still required

Run the full suite, inspect the final diff, scan staged public files for secrets,
and verify current website/database behavior. Preserve unrelated dirty files and
private originals. The erroneous latest issue is a current remediation item; it
must not be silently treated as a trustworthy reporting baseline. Passing fixture
tests alone does not certify that production repair is complete.
