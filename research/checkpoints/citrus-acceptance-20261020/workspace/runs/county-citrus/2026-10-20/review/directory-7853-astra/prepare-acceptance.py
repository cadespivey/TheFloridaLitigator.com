import json,copy
from pathlib import Path
from flwu.county_directory import public_metadata,validate_supplement
from flwu.publication import digest
from flwu.history import now
p=Path(__file__).parent;run=p.parent.parent;d=json.loads((p/'draft.json').read_text());validate_supplement(d,preview=True)
m=json.loads((p/'browser-matrix.txt').read_text().splitlines()[1]);assert len(m)==9
for x in m[:8]:assert not x['overflow'] and x['rows']==(0 if '&from=' in x['query'] else 62 if 'circuit_fifth' in x['query'] else 4)
l=json.loads((p/'browser-links.txt').read_text().splitlines()[1]);expected=set()
for person in d['people']:
 if 'county_citrus' in person['court_ids']:
  expected.update(u for u in [person['profile_url'],person['procedure_url']] if u);expected.update(r['href'] for rows in person['contacts'].values() for r in rows if r.get('href'))
assert expected==set(l['links']);assert l['focus']=='Skip to content' and l['skip']==dict(hash='#report',focus='report')
stamp=now();d=public_metadata(d);d['review_status']='reviewed';d['review']=dict(reviewed_by='Astra',reviewed_at=stamp,attestation='Pinned source/contact and explicit court-membership review, original artifact/export validation, desktop/mobile filter and overflow checks, rendered county links, keyboard skip-link and historical exclusion. Current senior-service and contact gaps remain explicit; source conflicts not resolved.')
d['content_sha256']=digest({k:v for k,v in d.items() if k!='content_sha256'});validate_supplement(d);(p/'reviewed-supplement.json').write_text(json.dumps(d,indent=2)+'\n')
(p/'review-validation.json').write_text(json.dumps(dict(people=11,county_rows=4,circuit_rows=62,historical_rows=0,prior_hernando_rows=4,viewports=[390,1280],visual_review='Desktop full-page and mobile viewport row inspected; aligned desktop table and readable stacked mobile record. Full-page mobile capture repeated header tiles; discarded as visual evidence, retained for diagnosis.',source_review='Pinned7853; reviewed phone/email/address values and source labels against person facts. Schenck dualphones, staffroles, unknown emails/address, clerk civil/admin fax, branch and inquiry routes preserved.',remaining='Production build/tests and deployed site validation.'),indent=2)+'\n')
packet=json.loads((run/'draft/checkpoint-017.json').read_text());packet['run_id']='citrus-acceptance-astra-20261020';packet['payload']['contract']['created_at']=stamp
packet['payload']['findings'].append(dict(key='citrus-county-review',kind='county_review',facts=dict(basis_capture=7853,reviewed_by='Astra',reviewed_at=stamp,research_review_status='bounded_accepted_with_documented_gaps',publication_status='reviewed_supplement_not_published',counts=dict(resident_judges=7,officers=2,clerk=1,circuit_chief=1,people=11),validation=dict(county_rows=4,circuit_rows=62,historical_rows=0,viewports=[390,1280],overflow=False,reviewed_supplement_digest=d['content_sha256']),gaps='Senior current-service not established; officer emails/addresses, Thomas assistant email, Lambert fax remain documented. No exhaustive noncivil analysis.',next_action='Integrate and test production supplement, publish and verify actual site; then Martin County.'),citations=copy.deepcopy(packet['payload']['findings'][0]['citations'])))
(p/'reviewed-packet.json').write_text(json.dumps(packet,indent=2)+'\n')
