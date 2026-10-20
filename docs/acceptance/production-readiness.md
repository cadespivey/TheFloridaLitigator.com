# Production readiness — not yet accepted

## Current website release checks

Build from reviewed reports and explicitly selected county supplements. Check:
- Numerical DCA/circuit ordering in both menus and alphabetical county groups.
- County resource allowlist; keyboard/touch nested menus and Escape behavior.
- Search matches/no matches, report-section and personnel-row destinations,
  About-page search, and no search-query leakage into court filters.
- Current supplements excluded from explicit historical issue/date views.
- Intro/search alignment, matching About prose/creator margins, footer width,
  and no clipping at desktop and mobile widths.
- Actual Actions completion and live-site behavior after release.

## Historical pipeline integration checklist

The checklist below records original pipeline acceptance targets. Unchecked items
are not a statement that the static publication site is unimplemented, nor does a
successful site build establish completion of live research adapters or scheduling.

## Integration review
Executable acceptance plan: [workflow tests](../workflow/TEST_PLAN.md).
Operating procedure: [runbook](../workflow/RUNBOOK.md).
Module intent/specification: [contracts](../workflow/MODULE_CONTRACTS.md).

- [ ] New live adapters actually acquire complete source inventories; registered
      legacy adapters still raise NotImplementedError.
- [ ] Independent replay trial passes coverage, legal accuracy, compaction/resume,
      negative-source, changed-person and amendment-redline cases.
- [ ] Limited live pilot verifies official authority, pagination and freshness.
- [ ] All required source IDs and all roster-derived people have evidence;
      blocked items cannot be removed from the denominator.
- [ ] Production normalization/import and weekly assembly implemented without
      fixture relabeling; actual raw source bytes and pinpoints retained.
- [ ] Production analysis/queue source filtering, concurrent claims, leases,
      recovery and terminal state tested against the accepted workflow.
- [ ] Export binds accepted snapshots, receipts, directory and final artifact hashes.
- [ ] Independent legal review verifies claims and dates against original documents.
- [ ] Final PDF visually reviewed, all county judges included, procedures/rules and
      clerk/contact links readable; complete electronic appellate directory linked.
- [ ] Explicit user approval of concrete final artifacts; publication integration
      implemented and tested before enabling it or a schedule.

Fixture tests, a reference import, `research status: ready_for_review`, generated
site files and historical “accepted” task entries satisfy none of these live
acceptance gates by themselves. The structural evidence checker is available;
automated live orchestration and the legacy release-manifest API fail closed.
The separate reviewed-history website exporter and Pages deployment workflow are
implemented; see [web publication](../workflow/WEB_PUBLICATION.md). Synthetic
preview validation does not satisfy the live research/publication gates above.
