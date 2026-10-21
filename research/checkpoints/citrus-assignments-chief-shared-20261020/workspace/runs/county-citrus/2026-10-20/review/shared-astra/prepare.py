import json,hashlib,shutil
from pathlib import Path
from flwu.history import now
root=Path('/Users/cadespivey/florida-litigator-weekly-update');p=Path(__file__).parent;run=p.parent.parent
f=json.loads((root/'runs/county-hernando/2026-10-19/review/shared/findings.json').read_text())[0]
# Reuse only circuit-wide source originals, never Hernando-specific access or assignments.
for c in f['citations']:
 for field,hashkey in [('path','sha256'),('text_path','text_sha256')]:
  src=root/c[field];assert hashlib.sha256(src.read_bytes()).hexdigest()==c[hashkey];dest=p/(c[hashkey]+src.suffix);shutil.copyfile(src,dest)
 assert c['quote'] in (root/c['text_path']).read_text()
x=f['facts'];x['county']='citrus';x['circuit']=5;x['title']='Fifth Circuit shared civil operating sources applicable to Citrus';x['key']='citrus-shared-civil-baseline';x['reviewed_at']=now();x['reviewed_by']='Astra';x['limitations']=[t.replace('Hernando','Citrus') for t in x['limitations']];x['reuse_note']='Original Lake evidence and bounded review reused; selected text directly checked during Citrus review, not new retrieval. Detailed civil deadlines/forms not expanded. Prior manual AI excerpts retain their limited scope.'
f['key']='citrus-shared-civil-baseline'
packet=json.loads((run/'draft/checkpoint-015.json').read_text());packet['payload']['findings'].append(f)
for person in packet['payload']['findings']:
 if person['key']=='citrus-chief-daniel-merritt':person['facts']['reuse']['source_finding']='hernando-daniel-merritt-jr'
 if person['key']=='citrus-edward-spaight':person['facts']['shared_rule_note']='2023 standing order cites A-2021-13; collected A-2024-59 expressly rescinds/supersedes/replaces it. Preserve older individual standing order and newer shared source without deciding control.'
packet['run_id']='citrus-shared-astra-20261020';packet['payload']['contract']['created_at']=now();(p/'reviewed-packet.json').write_text(json.dumps(packet,indent=2)+'\n')
