import json,copy
from pathlib import Path
from collections import Counter
from flwu.county_directory import make_supplement,validate_supplement
from flwu.publication import digest
p=Path(__file__).parent
packet=json.loads(Path('output/county-review/bay-7763-a/packet.json').read_text());before=copy.deepcopy(packet)
courts=[dict(group_id='circuit_fourteenth',category='Circuit Courts',label='Fourteenth Judicial Circuit',url='https://jud14.flcourts.org/'),dict(group_id='county_bay',category='County Courts',label='Bay',url='https://jud14.flcourts.org/court-locations/bay-county')]
draft,audit=make_supplement(packet,courts);facts={e['entity_key']:e['facts'] for e in packet['entities'] if e['kind']=='person'}
assert len(draft['people'])==22 and set(facts)=={x['id'] for x in draft['people']}
for person in draft['people']:
 role=facts[person['id']]['role']
 person['court_ids']=['county_bay'] if role=='County Judge' else ['circuit_fourteenth']
 if role=='Clerk of Circuit Court and Comptroller':person['court_ids']=['circuit_fourteenth','county_bay']
draft['coverage_note']='Reviewed personnel baseline with explicit source-specific gaps and conflicts; dated assignments and contact qualifications remain in supporting research. Publication review pending.'
draft['content_sha256']=digest({k:v for k,v in draft.items() if k!='content_sha256'});validate_supplement(draft,preview=True);assert packet==before
(p/'draft.json').write_text(json.dumps(draft,indent=2)+'\n');(p/'field-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
counts=Counter(g for person in draft['people'] for g in person['court_ids']);assert counts=={'county_bay':6,'circuit_fourteenth':17}
(p/'projection-check.json').write_text(json.dumps(dict(capture=7763,people=22,memberships=dict(counts),source_packet_unchanged=True,review_status='pending',remaining=['Review contact-field omissions/qualifiers and dated assignment integration','Add verified county records/tax-appraiser resources','Browser validation, release integration and historical isolation']),indent=2)+'\n')
print(dict(people=22,memberships=dict(counts),roles=dict(Counter(x['kind'] for x in draft['people']))))
print(json.dumps({k:v for k,v in audit.items() if v['omitted_contact_fields']},indent=2))
