import json
from pathlib import Path
from flwu.county_review import export_review
from flwu.county_directory import make_supplement,validate_supplement
r=Path(__file__).parent;out=Path('output/county-review/sumter-7935');m=export_review('/Users/cadespivey/.local/share/flwu/research-history.sqlite','manual_research:county-baseline-v1:3fd9f6b097a8',7935,out);p=json.loads((out/'packet.json').read_text());courts=[dict(group_id='circuit_fifth',category='Circuit Courts',label='Fifth Judicial Circuit',url='https://www.circuit5.org/'),dict(group_id='county_sumter',category='County Courts',label='Sumter',url='https://www.circuit5.org/courts-judges/sumter-county/judiciary/')];d,a=make_supplement(p,courts);(r/'initial-draft.json').write_text(json.dumps(d,indent=2)+'\n');(r/'initial-field-audit.json').write_text(json.dumps(a,indent=2)+'\n');print('People',len(d['people']))
for person in d['people']:print(person['name'],a[person['id']]['omitted_contact_fields'])
