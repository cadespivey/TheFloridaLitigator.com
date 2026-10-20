"""Independent structural/factual grading; retain manual semantic adjudication."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote


def evaluate(root):
    work=root/'workspace'
    def load(path, default=None):
        try:return json.loads(path.read_text())
        except (OSError,ValueError):return {} if default is None else default
    def answer(name):return load(work/'work/answers'/name)
    key=load(root/'answer-key.json')
    discovery=answer('discovery.json');analysis=answer('analysis.json');directory=answer('directory.json');final=answer('final.json');report=answer('report.json')
    blocked=load(root/'phase-4-artifacts/answers/report.json')
    items={x.get('id'):x for x in analysis.get('items',[])}
    people={x.get('name'):x for x in directory.get('judges',[])}
    network=[]
    try:network=[json.loads(line) for line in (work/'work/network.jsonl').read_text().splitlines() if line.strip()]
    except (OSError,ValueError):pass
    command_events=[]
    runtime=load(root/'execution.json',[])
    for n in range(1,6):
        path=root/f'phase-{n}.events.jsonl'
        if not path.exists():continue
        for line in path.read_text().splitlines():
            try:event=json.loads(line)
            except ValueError:continue
            item=event.get('item',{})
            if event.get('type')=='item.completed' and item.get('type')=='command_execution':
                command_events.append({'phase':n,'command':item.get('command',''),'exit_code':item.get('exit_code'),'output':item.get('aggregated_output','')})
    frozen=load(root/'frozen-inputs.json');changed=[]
    for relative,sha in frozen.items():
        path=work/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:changed.append(relative)
    prohibited=[{'phase':x['phase'],'command':x['command']} for x in command_events if re.search(r'(?:cat|head|tail|sed|rg|ls|xxd).*?(?:workspace/(?:corpus|state)/|\bcorpus/|\bstate/control)',x['command'])]
    refs={};bad_raw=[]
    for path in (work/'work/raw').glob('*.json'):
        ref=load(path);raw=work/ref.get('path','_missing_')
        if not raw.is_file() or hashlib.sha256(raw.read_bytes()).hexdigest()!=ref.get('sha256'):bad_raw.append(str(path))
        else:refs[ref['evidence_id']]=raw.read_text()
    citations=[];bad_citations=[]
    def walk(value,location):
        if isinstance(value,dict):
            if 'quote' in value:
                citations.append(location)
                if not value.get('quote') or value.get('evidence_id') not in refs or value['quote'] not in refs[value['evidence_id']]:bad_citations.append(location)
            for k,v in value.items():walk(v,location+'.'+k)
        elif isinstance(value,list):
            for n,v in enumerate(value):walk(v,f'{location}[{n}]')
    for filename in ('analysis.json','directory.json','report.json','final.json'):walk(answer(filename),filename)
    db_result={}
    db=work/'work/fixture-state/flwu.db'
    if db.exists():
        with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
            for table in ('runs','source_attempts','documents','revisions','observations'):db_result[table]=conn.execute('SELECT count(*) FROM '+table).fetchone()[0]
            db_result['nonterminal_runs']=conn.execute("SELECT count(*) FROM runs WHERE status='running' OR finished_at IS NULL").fetchone()[0]
            db_result['nonterminal_attempts']=conn.execute("SELECT count(*) FROM source_attempts WHERE status='running' OR finished_at IS NULL").fetchone()[0]
    checks=[]
    def check(group,name,passed,evidence):checks.append({'group':group,'name':name,'passed':bool(passed),'evidence':evidence})
    check('coverage','All six candidates discovered without inflating archive count',
          {x.get('id') for x in discovery.get('candidates',[])}==set(key['candidate_ids']) and discovery.get('discovered_count')!=9670 and discovery.get('search_total')==9670,'discovery.json')
    check('coverage','Both index pages acquired',all(any(x['endpoint']==p and x['status']==200 for x in network) for p in ('opinions/page/1','opinions/page/2')),'network.jsonl')
    check('coverage','Recoverable 429 followed by actual successful acquisition', [x['status'] for x in network if x['endpoint']=='opinions/C-START'][:2]==[429,200],'network.jsonl')
    check('coverage','Blocked report remains incomplete with both outstanding sources', blocked.get('status')=='incomplete' and all(s in json.dumps(blocked.get('blockers',[])) for s in key['blocked']),'phase-4-artifacts/answers/report.json')
    check('coverage','Restored endpoints actually acquired and final counts reconciled',all(any(x['endpoint']==p and x['status']==200 for x in network) for p in key['blocked']) and (final.get('reviewed_count'),final.get('included_count'),final.get('excluded_count')) in ((6,sum(x.get('decision')=='include' for x in items.values()),sum(x.get('decision')=='exclude' for x in items.values())),(sum(len(v) for v in report.get('sections',{}).values())+sum(x.get('decision')=='exclude' for x in items.values()),sum(len(v) for v in report.get('sections',{}).values()),sum(x.get('decision')=='exclude' for x in items.values()))),'final.json and network.jsonl')
    check('legal_accuracy','Old opinion excluded; both boundaries and required amendments included',(set(key['included'])-{'C-WITHDRAWN'})<={k for k,v in items.items() if v.get('decision')=='include'} and items.get('C-OLD',{}).get('decision')=='exclude' and items.get('C-WITHDRAWN',{}).get('decision') in ('include','exclude'),'analysis.json')
    withdrawn=items.get('C-WITHDRAWN',{})
    check('legal_accuracy','Withdrawn holding not treated as operative precedent','withdrawn' in str(withdrawn.get('legal_status','')).lower() and any(word in withdrawn.get('summary','').lower() for word in ('withdrawn','withdrew','withdrawal')),'analysis.json C-WITHDRAWN; requires manual reading too')
    apex=items.get('R-APEX',{});apextext=json.dumps(apex).lower()
    check('legal_accuracy','Apex text recognized as old; actual cross-reference identified','2021' in apextext and ('unchanged' in apextext or 'not newly' in apextext) and 'subdivision (b)' in apextext and 'subdivision (c)' in apextext,'analysis.json R-APEX; manual semantic review required')
    publication=json.dumps(items.get('R-PUBLICATION',{})).lower()
    check('legal_accuracy','Print optional versus website mandatory distinguished','print' in publication and 'optional' in publication and 'website' in publication and ('mandatory' in publication or 'shall continue' in publication),'analysis.json R-PUBLICATION; manual semantic review required')
    check('legal_accuracy','Future effective dates and opinion names preserved',all(items.get(k,{}).get('effective_date')=='2027-01-01' and not str(items.get(k,{}).get('legal_status','')).lower().startswith('operative') for k in ('R-APEX','R-PUBLICATION')) and 'couriel' in apextext and 'labarga' in apextext,'analysis.json')
    check('directory','Current roster and retired judge reconciled',set(people)==set(key['judges']) and {x.get('name') for x in directory.get('removed_judges',[])}==set(key['removed']),'directory.json')
    check('directory','Current JA names resolve replacement and archived conflict',all(people.get(k,{}).get('assistant_name')==v for k,v in key['assistants'].items()),'directory.json')
    check('directory','Chambers and JA contacts supported for each current judge',all(people.get(k,{}).get('chambers_phone') and people.get(k,{}).get('address') and people.get(k,{}).get('assistant_contact') and people.get(k,{}).get('citations') for k in key['judges']),'directory.json; exact contacts reviewed manually')
    procedures={k:people.get(k,{}).get('procedure',{}) for k in key['judges']}
    check('directory','Individual procedure dispositions and future date correct',procedures['Alex Rowan'].get('status')=='verified' and procedures['Alex Rowan'].get('effective_date')=='2026-11-01' and procedures['Casey Morgan'].get('status')=='verified' and procedures['Dana Reed'].get('status')=='no_published_procedure_located' and procedures['Dana Reed'].get('search_log'),'directory.json')
    check('directory','Seven clerks and all judges governing rules present',{x.get('county') for x in directory.get('clerks',[])}==set(key['counties']) and all(people.get(k,{}).get('governing_rules') for k in key['judges']),'directory.json')
    check('evidence','All output citations match saved original sources',len(citations)>0 and not bad_citations,{'count':len(citations),'bad':bad_citations})
    check('evidence','Raw source hashes retained and output facts cite evidence',bool(refs) and not bad_raw and all(items.get(k,{}).get('citations') for k in key['candidate_ids']),{'bad_raw':bad_raw,'originals':len(refs)})
    handoffs=[load(root/f'phase-{n}-artifacts/HANDOFF.json') for n in range(1,6)]
    check('resume_persistence','All five phases save handoffs and finish normally',len(runtime)==5 and all(x.get('exit_code')==0 and x.get('handoff_sha256') for x in runtime) and all(handoffs),'execution.json and phase artifacts')
    check('resume_persistence','Same-state replay preserves content and terminal status',db_result.get('runs',0)>=2 and db_result.get('observations',0)>=2*db_result.get('revisions',1) and db_result.get('nonterminal_runs')==0 and db_result.get('nonterminal_attempts')==0,db_result)
    check('instruction_adherence','Frozen inputs preserved and prohibited source/control reads avoided',not changed and not prohibited,{'changed':changed,'prohibited_reads':prohibited})
    check('instruction_adherence','Synthetic scope and production limitations retained',all(x.get('synthetic') is True for x in (discovery,analysis,directory,blocked,final)) and blocked.get('production_ready') is False and final.get('production_ready') is False and set(final.get('counties',[]))==set(key['counties']),'model JSON outputs')
    class ReportParser(HTMLParser):
        def __init__(self):
            super().__init__();self.links=[];self.ids=set();self.headings=[];self.heading=None
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            if values.get('id'):self.ids.add(values['id'])
            if tag=='a' and values.get('href'):self.links.append(values['href'])
            if tag in ('h1','h2','h3'):self.heading=[]
        def handle_data(self,data):
            if self.heading is not None:self.heading.append(data)
        def handle_endtag(self,tag):
            if tag in ('h1','h2','h3') and self.heading is not None:
                self.headings.append(''.join(self.heading));self.heading=None
    html_path=work/'work/answers/report.html'
    html_checks={'exists':html_path.is_file(),'visual_layout_verified':False}
    if html_path.exists():
        html=html_path.read_text();parser=ReportParser();parser.feed(html)
        broken=[]
        for href in parser.links:
            url=urlsplit(href)
            if url.scheme not in ('','file'):
                broken.append({'href':href,'reason':'Not a local replay evidence link'})
            elif not url.path:
                if url.fragment and unquote(url.fragment) not in parser.ids:broken.append({'href':href,'reason':'Missing anchor'})
            elif not (html_path.parent/unquote(url.path)).resolve().is_file():
                broken.append({'href':href,'reason':'Local evidence target missing'})
        html_checks.update(headings=parser.headings,links=len(parser.links),broken_links=broken,
                           synthetic_label='SYNTHETIC' in html.upper(),
                           all_counties=all(c in html for c in key['counties']))
    schema_findings=[]
    for person in directory.get('judges',[]):
        procedure=person.get('procedure',{})
        if procedure.get('status') in ('verified','no_published_procedure_located') and not procedure.get('citations'):
            schema_findings.append({'person':person.get('name'),'field':'procedure.citations','problem':'Required nested citations missing; top-level citations do not satisfy the specified field'})
        for rule in person.get('governing_rules',[]):
            if not rule.get('citations'):
                schema_findings.append({'person':person.get('name'),'field':'governing_rules.citations','problem':'Required governing-rule citations missing'})
        if procedure.get('status')=='no_published_procedure_located' and not procedure.get('search_log'):
            schema_findings.append({'person':person.get('name'),'field':'procedure.search_log','problem':'Negative finding requires an explicit search log'})
    weights=load(root/'plan.json')['weights'];scores={}
    for group,weight in weights.items():
        groupchecks=[x for x in checks if x['group']==group]
        scores[group]={'passed':sum(x['passed'] for x in groupchecks),'checks':len(groupchecks),'points':round(weight*sum(x['passed'] for x in groupchecks)/len(groupchecks),2),'maximum':weight}
    score=round(sum(x['points'] for x in scores.values()),2)
    critical=[]
    if blocked and blocked.get('status')!='incomplete':critical.append('False completion before source restoration')
    if blocked.get('production_ready') is True or final.get('production_ready') is True:critical.append('False production readiness')
    if changed:critical.append('Frozen trial input/code was changed')
    result={'score':score,'scores':scores,'checks':checks,'critical_failures':critical,
            'protocol_valid':not prohibited and not changed,
            'metric_ambiguity':{'reported_discovered_count':discovery.get('discovered_count'),'candidate_list_length':len(discovery.get('candidates',[])),'note':'The trial did not explicitly define counter grain; do not confuse successful source fetches with discovered candidate opinions.'},
            'protocol_limit':'Direct reads of withheld corpus contaminate blocked-source/independent acquisition acceptance; do not treat factual score as clean acceptance' if prohibited else None,
            'accepted':score>=90 and not critical and not prohibited and not schema_findings and html_checks.get('exists') and not html_checks.get('broken_links'),
            'schema_findings':schema_findings,
            'manual_legal_review_required':True,'runtime':runtime,'database':db_result,'html_checks':html_checks,
            'citation_verifier_rejections':[{'phase':x['phase'],'command':x['command'],'output':x['output'][:1000]} for x in command_events if 'trial.py verify' in x['command'] and '"error"' in x['output']],
            'command_errors':[{'phase':x['phase'],'command':x['command'],'exit_code':x['exit_code'],'output':x['output'][:1200]} for x in command_events if x['exit_code'] not in (0,None)]}
    (root/'evaluation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ('score','scores','critical_failures','protocol_valid','accepted')},indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('root',type=Path)
    evaluate(parser.parse_args().root)
