# Broward: bounded research and update handoff

Start here, then read `runs/county-broward/2026-10-15/RESUME.txt` and the relevant
fields of `state.json`. The long [research log](broward.md) preserves earlier
observations; its older pending-task statements are not the current task list.
The cloud agent owns baseline/workflow development. Local retrieval/analysis
workers remain deferred until workflow validation is complete.

## Current deliverables and limits

- Evidence checkpoint: capture **4886**, stream
  `manual_research:county-baseline-v1:6bf5ac02ab39`.
- Shared database: `/Users/cadespivey/.local/share/flwu/research-history.sqlite`.
  Scope: `{"profile":"county-baseline-v1","county":"broward","circuit":17}`.
- Read-only full review packet: `output/county-review/broward-4886/index.html`.
- Website preview: `output/county-review/broward-site-4886-v6/directory.html`.
- Pending directory supplement: run-relative `draft/county-directory-4886-v5.json`.
- Contact presentation audit: `review/directory-manual-presentation-review.json`.
- Remaining: browser layout/keyboard review and user county checkpoint. No public
  release, no finalized county report, and no authorization to start another county.

The roster accounts for 89 ordinary judges, nine senior judges, nine magistrates,
three hearing officers, the clerk and the court administrator. Eight senior judges
have unavailable individual contact evidence. Rebollo is a separate historical/
current-identity reconciliation, not a verified current directory entry. Preserve
these distinctions. Documented conflicts do not require deciding which source
controls before delivery; missing facts must not be replaced with guesses.

## Where to look and what to collect

| Task | Saved official starting point | Required distinctions |
| --- | --- | --- |
| Judge identity, JA, phone, room, division, procedure link | `https://www.17th.flcourts.org/judiciary-list-and-category/` and `https://www.17th.flcourts.org/judiciary/` | Reconcile roster, profile heading and dated assignments. A reused profile URL is not proof of the old judge's current identity. |
| Magistrates/hearing officers | `https://www.17th.flcourts.org/general-magistrates/` | Preserve the published Administrative Assistant role. These entries use a different heading structure from judge cards. |
| Individual procedures | Exact `profile_url` and `procedure_url` in the saved person's facts | Follow the actual document/iframe/print link; record the wrapper and original separately. Check header contacts, communications, hearings, motions, orders, copies, remote appearances and civil duties. |
| Civil/shared/local procedure | `/civil-administrative-orders/`, `/county-administrative-orders/`, `/general-orders/`, `/administrative-orders/` on the circuit site | Review material procedure/access items. Keep dated originals and explicit modification/vacatur statements; do not turn this into a conflict-resolution project. |
| Clerk and civil filing operations | `https://www.browardclerk.org/` and saved `broward-clerk`, `broward-clerk-circuit-civil`, `broward-clerk-county-civil` findings | Separate general, division, public-records and personal contacts. Retain action-specific instructions and source dates. |
| Court records search | `https://www.browardclerk.org/Web2/CaseSearchECA/Index/?AccessLevel=ANONYMOUS` | Public navigation only; no private case lookup is necessary for this baseline. |
| Official records | `https://officialrecords.broward.org/AcclaimWeb` | Landing/provider evidence exists; original HTML returned 403. Do not claim an original or completed search interaction. |
| Property appraiser | `https://www.bcpa.net/` | Separate from tax collector. Menu provides property-search destinations. |

These are observed source paths, not a guarantee of future freshness. Inspect
the current source before reusing page selectors or claiming a new check.

## Retrieve one saved person, not the whole corpus

Run from the repository root. Replace only the selected `key` below. This command
is read-only and prints the person's compact starting context, not all citations
or the county's 48 MB review packet:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python - <<'PY'
import json, sqlite3
from pathlib import Path
state = json.loads(Path('runs/county-broward/2026-10-15/state.json').read_text())
saved = state['database_save']
key = 'broward-circuit-shari-africk-olefson'
with sqlite3.connect(Path(saved['database']).as_uri()+'?mode=ro', uri=True) as conn:
    row = conn.execute('''SELECT v.facts,o.capture_seq FROM finding_observations o
      JOIN finding_versions v USING(version_id) JOIN captures c ON c.seq=o.capture_seq
      WHERE c.stream=? AND o.entity_key=? AND c.seq<=? ORDER BY c.seq DESC LIMIT 1''',
      (saved['stream'], key, saved['seq'])).fetchone()
if row is None:
    raise SystemExit('No saved observation for that identity; do not infer deletion.')
facts = json.loads(row[0])
fields = ['name','assignment','profile_url','procedure_url','contact','contacts',
          'current_contact','current_contact_verified','dates','summary']
print(json.dumps({'entity_key':key,'capture_seq':row[1],
                  'facts':{k:facts[k] for k in fields if k in facts}},indent=2))
PY
```

For the next bounded step, select `checklist`, `conflicts`, or the needed shared
source field from that same saved record. Do not dump every person's context.
Source original/text paths, hashes and timestamps are in the run's
`review/acquisition.json`, keyed by acquisition ID. Search for the exact URL and
read only the matching entry. Reuse shared originals already collected; an old
retrieval time does not establish a current recheck.

## Acquisition, review and save

1. Finish the selected person's related sources before another person. For an
   absent field, follow official navigation, then search the official domain for
   the exact name plus the field or division. Log the query, result and remaining
   gap. Do not repeatedly retry the same failed source without a new lead.
2. If roster extraction has only headers, inspect the saved public AJAX response.
   Broward's observed request used `/wp-admin/admin-ajax.php` with
   `action=sls_body_tbl_c`, `searchCatSlug=all`, `tplateID=2611`, `staffTplateID=407`
   and the other fields recorded in the long log. Verify current page code first.
   Do not call an empty extraction an empty roster. Distinguish source rows,
   duplicate assignments, named people, unnamed rows and non-person docket labels.
3. Use `scripts/broward_roster_links.py` to match the exact normalized name and
   division in saved grid HTML. Do not select the first surname substring match.
   Preserve Google document IDs and actual PDF URI annotations; visible link text
   can differ from the target. Use the existing FL Courts article/folder helpers
   for supported `__NEXT_DATA__` shells. Render PDFs when table placement, crossed
   out text or link rectangles affect the meaning.
4. Record contacts/roles, addresses, assignments, official procedure links, a
   structured checklist and concise summary. Preserve original/transcribed values
   separately from display formatting. Distinguish collected documents, reviewed
   pages/topics, conflicts and missing evidence. Criminal/diversion merits are
   low priority unless shared/civil procedure is affected.
5. Follow [BASELINE_CAPTURE.md](../../workflow/BASELINE_CAPTURE.md) for exact packet
   keys, recursive citation validation and the save command. Save a **new** packet,
   verify bytes/facts in the database, verify replay, and preserve finalized
   reports. Update the receipt, state and resume instructions before compaction.
   Do not rerun old mutating checkpoint scripts. Use frozen packets for replay.
6. Compare later research using the existing `flwu history changes` command with
   the same database/stream and `--entity KEY`. Default baseline is the last
   finalized report; `--start YYYY-MM-DD` supplies an explicit comparison start.
   A missing county finalized baseline stays unknown. Partial saves never advance
   it; first observations and source-byte changes are not necessarily legal changes.

For public presentation, follow
[COUNTY_DIRECTORY_INTEGRATION.md](../../workflow/COUNTY_DIRECTORY_INTEGRATION.md).
The dated supplement appears only in the default directory; explicit issue/date
queries keep their original saved contacts. Do not run the legacy bundled
seven-county directory import expecting it to include Broward.
