import json
from pathlib import Path
from flwu.county_directory import make_supplement
p=Path(__file__).parent
packet=json.loads(Path('output/county-review/indian-river-7815-a/packet.json').read_text())
courts=[dict(group_id='circuit_nineteenth',category='Circuit Courts',label='Nineteenth Judicial Circuit',url='https://www.circuit19.org/'),dict(group_id='county_indian_river',category='County Courts',label='Indian River',url='https://www.circuit19.org/judges/?_location=indian-river-county')]
draft,audit=make_supplement(packet,courts)
assert len(draft['people'])==17
(p/'initial-draft.json').write_text(json.dumps(draft,indent=2)+'\n');(p/'initial-field-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Initial pending draft:',len(draft['people']),'people')
for key,v in audit.items():
 if v['omitted_contact_fields']:print(key,v)
