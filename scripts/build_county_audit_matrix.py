"""Summarize saved county audits without treating inventory as final acceptance."""
import argparse
import hashlib
import json
from pathlib import Path


def build(root, audit_dir):
    supplements = {p.stem: p for p in (root / 'website/county-directories').glob('*.json')}
    audits = {p.name.removesuffix('-coverage-audit.json'): p
              for p in audit_dir.glob('*-coverage-audit.json')}
    if len(supplements) != 67 or set(supplements) != set(audits):
        raise ValueError(f'County inventory mismatch: missing={set(supplements)-set(audits)}, '
                         f'extra={set(audits)-set(supplements)}; supplements={len(supplements)}')
    rows = []
    for slug, path in sorted(audits.items()):
        audit = json.loads(path.read_text())
        supplement = json.loads(supplements[slug].read_text())
        people = audit['people']
        # Audit schemas evolved. Preserve all gap/qualification fields rather than
        # silently dropping unfamiliar fields or interpreting an absent key as no gap.
        qualifiers = {k: v for k, v in audit.items() if any(
            word in k for word in ('gap', 'limitation', 'remaining', 'qualification', 'note'))}
        limitations = []
        for person in people:
            details = {k: v for k, v in person.items() if any(
                word in k for word in ('gap', 'limitation', 'next_action', 'procedure_search')) and v}
            if details:
                limitations.append({'id': person['id'], 'name': person['name'], **details})
        rows.append({'county': slug, 'audit_path': str(path.relative_to(root)),
                     'audit_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'audited_people': len(people), 'supplement_people': len(supplement['people']),
                     'people_with_checklist': sum(p.get('checklist_present') is True for p in people),
                     'people_without_checklist': [p['id'] for p in people if not p.get('checklist_present')],
                     'qualifications': qualifiers, 'person_limitations': limitations,
                     'integration_status': 'pending_final_integration'})
    return {'scope': 'Saved evidence audits; not fresh retrieval or final acceptance. Counts are county-scoped, not unique statewide people. Missing checklists may be bounded gaps or intentional noncivil scope.',
            'counties': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit-dir', default='research/audits/20261022')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    directory = root / args.audit_dir
    result = build(root, directory)
    (directory / 'county-coverage-matrix.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# County coverage audit matrix', '', result['scope'], '',
             'All rows await final current database/website integration. Audit files contain source-specific gaps and qualifications.', '',
             '| County | Audited records | Supplement records | With checklist | Evidence |',
             '| --- | ---: | ---: | ---: | --- |']
    for row in result['counties']:
        lines.append(f"| {row['county']} | {row['audited_people']} | {row['supplement_people']} | {row['people_with_checklist']} | [Audit]({Path(row['audit_path']).name}) |")
    (directory / 'county-coverage-matrix.md').write_text('\n'.join(lines) + '\n')
    print(f"Wrote {len(result['counties'])} county rows; final integration remains pending.")
