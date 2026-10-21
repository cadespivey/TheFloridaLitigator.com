import json
from pathlib import Path
from flwu.county_review import export_review
from flwu.county_directory import make_supplement,validate_supplement
r=Path(__file__).parent;out=Path('output/county-review/martin-7905');m=export_review('/Users/cadespivey/.local/share/flwu/research-history.sqlite','manual_research:county-baseline-v1:82fb054fd539',7905,out);p=json.loads((out/'packet.json').read_text());courts=[dict(group_id='circuit_nineteenth',category='Circuit Courts',label='Nineteenth Judicial Circuit',url='https://www.circuit19.org/'),dict(group_id='county_martin',category='County Courts',label='Martin',url='https://www.circuit19.org/judges/?_location=martin-county')];d,a=make_supplement(p,courts);(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'initial-field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('People',len(d['people']))
for person in d['people']:print(person['name'],a[person['id']]['omitted_contact_fields'])
