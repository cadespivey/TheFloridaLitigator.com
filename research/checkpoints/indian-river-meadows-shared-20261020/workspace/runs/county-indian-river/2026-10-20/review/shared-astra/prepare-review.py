import json,hashlib,shutil,copy
from pathlib import Path
from flwu.history import now
p=Path(__file__).parent;root=Path('/Users/cadespivey/florida-litigator-weekly-update');old=json.loads((root/'runs/county-st-lucie/2026-10-19/draft/checkpoint-025.json').read_text())
items=[]
for key,summary,scope in [
('st-lucie-ada-access','Circuit-wide ADA route applies to Indian River: Kate Bradford, General Counsel, bradfordk@circuit19.org,7728074370,250NW Country Club Drive Suite217 Port St.Lucie34986. Requests by webform, other writing or orally, preferably seven days ahead. Indian River lactation room on third floor; check with security.','Access contact, request channels, case-procedure motion distinction and Indian River lactation location; not individual accommodation advice.'),
('st-lucie-case-management-route','Circuit overview directs parties to case-management templates on the presiding judge’s page. It retains2021 framing and links AO2021-05; not represented as a newly issued rule or independently current statewide deadlines. Current judge-specific instructions remain separately preserved.','General submission/template route; historical framing preserved. No case-specific deadlines or merits analysis.'),
('circuit19-officer-appendix-20260803','August3appendix lists general magistrates Stroke,Baillie,Fleming,Hill; child-support TBD/Presley; traffic officers Battista,Goldman,Grazi,Sebag. It gives no county assignments or contacts. Indian River reviewed profiles separately support Hill,Fleming,Presley and vacant office. Remaining applicability requires bounded screening, not inferred from circuit listing.','Names/roles/revision only. No traffic merits or procedure expansion.')]:
 prior=next(f for f in old['payload']['findings'] if f['key']==key);c=copy.deepcopy(prior['citations'][0])
 for field,hfield in [('path','sha256'),('text_path','text_sha256')]:
  src=root/c[field];assert hashlib.sha256(src.read_bytes()).hexdigest()==c[hfield];dest=p/(key+src.suffix);shutil.copy2(src,dest);c.pop(field)
 facts=dict(county='indian_river',circuit=19,title=prior['facts']['title'],summary=summary,reviewed_at=now(),reviewed_by='Astra',review_status='reviewed',review_scope=scope,stated_revision_date=prior['facts'].get('stated_revision_date'),stated_effective_date=prior['facts'].get('stated_effective_date'),official_links=prior['facts'].get('official_links',[]),reuse=dict(prior_entity=key,prior_checkpoint=7337,original_retrieval=c['retrieved_at'],hashes_verified=True,limitation='Original source reused; no fresh capture claimed.'))
 if key.endswith('20260803'):facts['pending_applicability_screen']=['Lindsay Stroke','Bruce Baillie','Jeffrey Battista','Robert Goldman','Ryan Grazi','Jessica Sebag']
 items.append(dict(key=key.replace('st-lucie','indian-river').replace('circuit19-officer','indian-river-officer'),kind='source_review',facts=facts,citations=[c]))
(p/'reviewed-shared.json').write_text(json.dumps(items,indent=2)+'\n')
