import json,hashlib
from pathlib import Path
from flwu.history import now
p=Path(__file__).parent;run=p.parent.parent
packet=json.loads((run/'draft/checkpoint-013.json').read_text());meta=json.loads((p/'order-meta.json').read_text());text=(p/'manual-excerpts.txt').read_text();meta['text_sha256']=hashlib.sha256(text.encode()).hexdigest();c=dict(meta,authority='official',synthetic=False,quote='AMENDED ADMINISTRATIVE ORDER NO. C-2025-45-D',locator='Astra visual review of rendered pages 1–6; manually transcribed selected assignment excerpts, pages 1 and 3–5')
assignments={
'Carol Falvey':'AO C-2025-45-D, effective June 22, 2026: 75% general civil, including all civil jury trials and eminent domain; 10% family; county administrative duties. Profile allocation differs; both preserved.',
'Kristie M. Healis':'AO C-2025-45-D: juvenile delinquency, non-death-penalty criminal felony, Jimmy Ryce and risk protection cases. Noncivil basic review.',
'Robert Kyle Lambert':'AO C-2025-45-D: 25% general civil, nonjury only; all mortgage foreclosure; 40% family; adult protective, Baker Act and Marchman Act matters.',
'George L. Singeltary II':'AO C-2025-45-D: dependency, 50% family and unified family court/support matters. Noncivil basic review; retain already collected practical instructions.',
'Bruce E. Carney':'AO C-2025-45-D: county criminal, including criminal traffic, plus rotating first appearances. Noncivil basic review; retain already collected general submission instructions.',
'Edward C. Spaight':'AO C-2025-45-D: county general civil except civil infractions, evictions, small claims, traffic, unlawful detainer and prohibited practices; probate/guardianship, specified injunction matters and rotating first appearances.',
'Amber Thomas':'AO C-2025-45-D: civil infractions, evictions, small claims, traffic, unlawful detainer and prohibited practices; extraordinary writs except habeas corpus and appeals from final administrative orders; also specified noncivil dockets and rotating first appearances.',
'Keith Schenck':'AO C-2025-45-D: referred pro se domestic relations and nonemergency dependency; civil matters referred under Rule 1.490, probate and other authorized magistrate referrals. May also serve as assigned child support hearing officer.'}
for f in packet['payload']['findings']:
 name=f['facts'].get('name')
 if name not in assignments:continue
 x=f['facts'];x['prior_profile_assignment']=x.get('assignment');x['assignment']=assignments[name];x['assignment_source_effective']='2026-06-22';x['assignment_source_signed']='2026-06-11';x['assignment_reviewed_at']=now();x.setdefault('procedure_links',[]).append(dict(text='Citrus 2026 assignment order C-2025-45-D',url=meta['url']));f['citations'].append(c)
 # Keep historical gap text but label it resolved rather than erasing evidence.
 gaps=x.get('gaps',[]);resolved=[g for g in gaps if ('assignment' in g.lower() or 'allocation' in g.lower()) and 'email' not in g.lower()]
 x['gaps']=[g for g in gaps if g not in resolved]
 if resolved:x['resolved_assignment_gaps']=dict(prior_statements=resolved,resolution='Assignment order visually reviewed; scope/effective date recorded.')
 if name=='Carol Falvey':x.setdefault('conflicts',[]).append(dict(subject='Assignment allocations',statements=['Profile states all general civil and contains differing family allocation wording.','C-2025-45-D effective June22,2026 states75% general civil and10% family.'],disposition='Preserve both source statements and dates; no controlling-source determination.'))
packet['payload']['findings'].append(dict(key='citrus-assignments-2026',kind='source_review',facts=dict(county='citrus',circuit=5,title='Citrus 2026 assignments',reviewed_by='Astra',reviewed_at=now(),review_status='reviewed',effective_date='2026-06-22',signed_date='2026-06-11',review_scope='Complete six-page original collected; all pages visually inspected for current assignment identities, scope, effective/signature dates and basic duty coverage. Selected excerpts manually transcribed. No specialty practice analysis.',summary='Seven roster judges and Schenck matched current indexed assignment order. General civil allocation: Falvey75% including all jury trials, Lambert25% nonjury and all mortgage foreclosure. Spaight county general civil with stated exceptions; Thomas small claims/evictions and other listed matters. County judge duty coverage does not establish permanent circuit appointment.',limitations=['June duty table names Fritton; dated monthly duty listing does not establish current roster membership.','Simmons appointment reviewed separately; chief/senior applicability remains pending.','Falvey profile allocation differs and is preserved without resolution.']),citations=[c]))
packet['run_id']='citrus-assignments-astra-20261020';packet['payload']['contract']['created_at']=now()
(p/'reviewed-packet.json').write_text(json.dumps(packet,indent=2)+'\n')
