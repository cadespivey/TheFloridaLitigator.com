> Current authority: Qwen3.8-27B-8bit continues under [LOCAL_AGENT_HANDOFF.md](LOCAL_AGENT_HANDOFF.md). Its current scope and execution instructions supersede historical cloud-only or exhaustive-review directions below.

# County review export

Use this after the county roster, individual reviews, shared procedure review,
and gap disposition have been saved. This is a read-only review deliverable,
not a public website release or a finalized research report. It does not import
into the legacy directory, whose current validator supports seven counties.

Run from the repository root, using the exact database, stream and capture in
the county's `state.json`. Choose a new output directory; existing output is
never overwritten. For Broward's reconciled checkpoint:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m flwu.county_review \
  --database /Users/cadespivey/.local/share/flwu/research-history.sqlite \
  --stream manual_research:county-baseline-v1:6bf5ac02ab39 \
  --through-capture 4886 \
  --output output/county-review/broward-4886
```

The exporter opens the database read-only, pins a consistent transaction, and
selects each entity's latest observation in that stream at or before the explicit
capture. It rejects a capture from another stream. It preserves facts, nested
qualifiers, citation metadata, retrieval dates, revision/effective dates, nulls,
and historical association records unchanged in `packet.json`. It verifies every
referenced original/extraction hash against database bytes before writing output.
Originals and extractions are copied under `artifacts/`; original download links
are available on each detail page. Saved quotes remain in JSON, not page prose.

`index.html` provides a personnel table and links to individual checklists,
clerk/administration records, and shared procedure findings. Each detail page
retains all remaining saved facts in expandable sections. Contact labels retain
the recorded role: division, assistant, clerk and interpreter routes must not be
collapsed into an invented personal chambers contact. Address arrays render one
line per stored component. `historical_contact` never supplies current contacts.
Incomplete senior records and historical identity reconciliations stay visible
without being renamed verified current contacts. Later assignment/order findings
remain separate records; the exporter does not silently override earlier sources.

Before accepting the county packet:

1. Compare every JSON entity, fact and citation with the pinned DB observation.
2. Check artifact hashes and local links; inspect the rendered roster, individual
   contacts, procedure checklists and historical/missing-contact cases.
3. Reconcile roster counts using the latest county gap disposition, not an older
   progress record. An entity count alone is not a current personnel count.
4. Confirm repeated export produces identical bytes and the database, existing
   directories and finalized reports are unchanged.
5. Record actual checks and remaining integration work. This exporter does not
   establish live freshness, resolve conflicts, certify accessibility, normalize
   production display values, or complete public navigation integration.

Under the active statewide goal's October 17/18 override, cloud review and
acceptance replace a new user checkpoint between counties. Complete that review
before proceeding to the next county in the authorized order. Future production
integration must preserve old county entries and historical snapshots, carry the
reviewed county scope explicitly, and retain these source associations. Do not
relax the seven-county validator and import a partial replacement as a shortcut.
