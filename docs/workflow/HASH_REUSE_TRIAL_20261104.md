# Hash reuse trial — November 4, 2026

The user authorized a fresh, bounded Qwen3.8-27B-8bit trial of 20 source checks,
with file-only results and no production database or website updates. The sample
contained 14 Fifth DCA personnel/index pages and six Circuit 7 administration/search
pages selected from the slow run. It was intentionally weighted toward the noise
that had caused unnecessary reviews, rather than a randomized full-workflow sample.

## Observed results

| Measure | Result |
| --- | --- |
| Fresh official-source retrievals | 20 successful; zero blocked |
| Retrieval/baseline preparation | 14.982 seconds |
| Worker elapsed time, monotonic timer | 1,837.388 seconds (30 min 37 sec) |
| Machine-reused source checks | 16 (80%) |
| Model reviews | Four: three no-change conclusions, one personnel change |
| Pending checks at exit | Zero; worker exited successfully |
| Production database writes / publication | None |

The code required one review of each newly changed shared court component before
reusing other sources' own completed content reviews. The clerk change survived
the hash gate. Qwen identified the replacement of Sandra Williams by Kristopher
Warburton on the [Fifth DCA clerk page](https://5dca.flcourts.gov/Clerk-s-Office)
and retained the heading/body surname discrepancy. It also reviewed the distinct
search-query metadata on [Circuit 7's senior search](https://circuit7.org/?s=senior).

The production database was opened only with SQLite `mode=ro` and
`PRAGMA query_only=ON` for baseline reads. Its maximum capture sequence remained
376435 before acquisition, after acquisition and after worker exit; the
acquisition connection reported zero changes. The model used cached trial files.
Provisional file receipts exercised the production fingerprint/ReviewIndex code;
they were never accepted production reviews or published findings.

## Independent evaluation

**Completeness and boundary adherence: A. Interpretation accuracy: B−.**
Qwen finished the returned tasks, avoided reopening machine-reused pages, detected
the material personnel change and preserved the official spelling discrepancy.
However, it described Cloudflare changes as request/session data without explaining
the added origin/URL-construction logic, called URL capitalization changes cosmetic
routing without verifying target equivalence, inferred a timestamp's meaning, and
called the clerk's stated selection date an effective date in its summary. Its
finding quotation correctly said *selected*. The model's final claim of no
unresolved issues does not erase these review-quality defects.

After grading, the skill directions were tightened to distinguish token changes
from script logic, observed links from verified routing, and selection/publication/
revision/retrieval/effective dates. Those additional directions were not tested by
a second Qwen run. Original trial receipts remain unchanged.

The comparison with the earlier approximately nine-hour/32-task run is directional,
not a controlled speed ratio: task mix, context age and receipt requirements differ.
This trial conservatively annotated every raw-content difference even for changed
text, where production sometimes uses that comparison only as a reading aid. It
did not test local-model opinion/statute summaries, full production acceptance,
database finding reconciliation, report assembly or deployment. New/unreviewed
documents, status changes and unsupported differences still require their normal
review. A source hash cannot repair an inaccurate prior interpretation.

## Implementation verification

The complete automated suite passed **1,119 tests** with no reported warnings.
New coverage includes known metadata reuse, real/unknown changes staying queued,
new navigation requiring one review, retained original bytes, the standard update
and coordinator paths (including all 14 opinion-listing channels), decoded script
fields, failure-preserving step execution, overwrite protection and real-launcher
next-task behavior. This used synthetic fixture databases; historical reports were
not audited. Skill installation/launcher tests passed. The optional skill metadata
validator could not run because PyYAML was unavailable; no packages were installed.

Private artifacts, including original source captures and worker logs, remain in
`runs/hashing-improvement-20261104/`; they are intentionally excluded from public Git.
