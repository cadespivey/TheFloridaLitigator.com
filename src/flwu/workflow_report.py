"""Source-bound report assembly. Editorial decisions remain explicit receipts."""
from __future__ import annotations
import copy
import html
import json
from pathlib import Path

from flwu import history as h, publication as pub, publication_acceptance as pa, publication_pending as pp
from flwu.evidence_binding import AcquisitionIndex
from flwu.research import validate_person_identity
from flwu import workflow as w


def requirements(conn, config):
    seq = conn.execute('SELECT coalesce(max(seq),0) FROM captures').fetchone()[0]
    row = {'stream':config['registry']['stream'], 'seq':seq}
    required = pa.requirements(conn, row)
    for identity, requirement in required.items():
        payload = json.loads(conn.execute('SELECT payload FROM captures WHERE seq=?', (requirement['capture_seq'],)).fetchone()[0])
        finding = next(f for f in payload['findings'] if
                       ('opinion:'+f['key'] if f['kind']=='opinion' else 'source:'+f['key'])==identity)
        requirement['finding'] = finding
    return required


def mapping_template(identity, requirement):
    f = requirement['finding']; facts = f['facts']
    candidate = None
    if f['kind']=='opinion':
        candidate = dict(id=f['key'], title=facts.get('title') or facts.get('case_number') or '',
                         section='case_law', summary=facts['summary'], holding=facts['holding'],
                         disposition=facts['disposition'], authors=facts['authors'],
                         publication_date=facts.get('published_date'), effective_date=None,
                         legal_status=facts.get('status','unknown'))
    elif f['kind']=='candidate':
        candidate = {k:v for k,v in facts.items() if k not in ('citations','citation','decision')}
    return dict(finding_id=identity, version=requirement['version'], decision='', reason='',
                citations=copy.deepcopy(f['citations']), candidate=candidate,
                inventories=[], personnel=[], removals=[])


def tasks(conn, config, queue):
    # Available unread sources are handled by the source/opinion stages, never
    # offered an easy failure/exclusion receipt here.
    pending = pp.pending(queue)
    for identity, item in sorted(pending.items()):
        if identity.startswith(('source:','opinion:')) and not item['unavailable']:
            continue
        yield w.packet(config, 'coverage_review', identity,
                       dict(task=item['task'],unavailable=item['unavailable']),
                       dict(task_id=identity, decision='',reason='',citations=[]),
                       'Describe this exact failure or supported scope exclusion. A missing source cannot '
                       'be called no-change. Available evidence requires quoted support. Resolve material '
                       'effective-date questions rather than excluding them to clear the queue.',
                       checks=('Every pending acquisition task reconciled against saved queue',))
    for identity, requirement in sorted(requirements(conn, config).items()):
        requirement['reporting_window']=queue['bounds']
        yield w.packet(config, 'publication_mapping', identity, requirement,
                       mapping_template(identity, requirement),
                       'Choose include, include_directory, or exclude for this finding and reporting period. '
                       'Preserve the accepted opinion summary. Include needs an explicit section and candidate; '
                       'include_directory retains the exact personnel facts. Exclude needs a substantive cited '
                       'reason. Optional inventories/personnel are complete source-bound roster projections; '
                       'never infer removals or create a person from a role heading.',
                       checks=('Exact finding version and acquired citations', 'Named roster/person reconciliation before acceptance'))


def validate_pending_one(conn, config, queue, receipt):
    expected = pp.pending(queue)
    key = receipt.get('task_id')
    if key not in expected:
        raise ValueError('Unknown pending task')
    # Reuse the same validator with an exact one-task view; no other disposition
    # is auto-filled or treated as reviewed.
    pp.validate_disposition(expected, receipt, AcquisitionIndex(conn, config['registry']['stream']))


def validate_records(conn, config, records):
    index = AcquisitionIndex(conn, config['registry']['stream'])
    for record in records:
        if set(record) != {'key','kind','facts','citations'} or not record['citations']:
            raise ValueError('Projection requires key, kind, complete facts and citations')
        if record['kind'] not in ('judge','clerk','source_inventory'):
            raise ValueError('Unsupported directory projection kind')
        for ref in record['citations']:
            index.validate(ref)
            if not ref.get('quote'):
                raise ValueError('Projection requires quoted evidence')
        facts = record['facts']
        index.validate_tree(facts)
        if record['kind']=='source_inventory':
            if not isinstance(facts.get('entities'),list):
                raise ValueError('Inventory requires explicit named entities')
            for entity in facts['entities']:
                validate_person_identity(entity);index.validate(entity['citation'])
                if entity.get('type') not in ('judge','clerk') or not isinstance(entity.get('counties'),list):
                    raise ValueError('Roster requires explicit role and county membership')
        else:
            if not record['key'].startswith('person-') or not facts.get('name'):
                raise ValueError('Person requires stable person- ID and name')
            if not any(facts['name'] in c['quote'] for c in record['citations']):
                raise ValueError('Person name is not supported by cited identity evidence')
            validate_person_identity(dict(name=facts['name'],citation=next(c for c in record['citations'] if facts['name'] in c['quote'])))


def validate_decision(conn, config, task, receipt):
    if task['kind']=='coverage_review':
        validate_pending_one(conn,config,w.latest_queue(conn,config),receipt)
        return {'validated':'pending_disposition'}
    if task['kind']!='publication_mapping':
        raise ValueError('Unknown workflow decision kind')
    if set(receipt)!=set(task['receipt_template']):
        raise ValueError('Use the exact publication mapping template')
    req = task['inputs']; f = req['finding']
    if receipt['finding_id']!=task['identity'] or receipt['version']!=req['version']:
        raise ValueError('Stale publication finding/version')
    if not isinstance(receipt['reason'],str) or not receipt['reason'].strip():
        raise ValueError('Publication decision needs a substantive reason')
    ix=AcquisitionIndex(conn,config['registry']['stream'])
    if not isinstance(receipt['citations'],list) or not receipt['citations']:
        raise ValueError('Publication decision needs acquired quoted evidence')
    for cite in receipt['citations']:
        ix.validate(cite)
        if not cite.get('quote'):
            raise ValueError('Publication decision requires quotations')
    if not any(c['sha256']==req['sha256'] for c in receipt['citations']):
        raise ValueError('Decision must cite this finding source')
    if receipt['decision']=='include':
        candidate=receipt['candidate']
        if not isinstance(candidate,dict) or candidate.get('section') not in pub.KEYS or not candidate.get('title') or not candidate.get('summary'):
            raise ValueError('Included candidate needs title, summary and section')
        if req['summary'] and req['summary'] not in candidate['summary']:
            raise ValueError('Retain the accepted opinion summary')
        if f['kind']=='opinion' and any(candidate.get(k)!=f['facts'][k] for k in ('holding','disposition','authors')):
            raise ValueError('Opinion fields must match the accepted review; use opinion-revise for corrections')
        pub.candidate_summary(candidate,candidate['section'])
    elif receipt['decision']=='include_directory':
        if f['kind'] not in ('judge','clerk') or receipt['candidate'] is not None:
            raise ValueError('Directory inclusion requires an existing personnel finding and no news candidate')
    elif receipt['decision']=='exclude':
        if receipt['candidate'] is not None:
            raise ValueError('Excluded finding cannot contain a news candidate')
    else:
        raise ValueError('Choose include, include_directory or exclude')
    if not isinstance(receipt['inventories'],list) or not isinstance(receipt['personnel'],list):
        raise ValueError('Inventories and personnel must be explicit lists')
    validate_records(conn,config,receipt['inventories']+receipt['personnel'])
    if any(r['kind']!='source_inventory' for r in receipt['inventories']) or any(r['kind'] not in ('judge','clerk') for r in receipt['personnel']):
        raise ValueError('Projection records are in the wrong collection')
    if not isinstance(receipt['removals'],list):raise ValueError('Removals must be explicit cited decisions')
    for removal in receipt['removals']:
        if set(removal)!={'person_id','reason','citations'} or not removal['reason'].strip() or not removal['citations']:
            raise ValueError('Person removal requires stable ID, reason and citations')
        for cite in removal['citations']:
            ix.validate(cite)
            if not cite.get('quote'):raise ValueError('Removal needs quoted evidence')
    return {'validated':'publication_mapping','version':req['version']}


def decisions(conn, config, queue):
    done=w.accepted(conn,config);mapped=[];pending=[]
    for task in tasks(conn,config,queue):
        event=done.get(task['packet_sha256'])
        if event is None:
            raise ValueError('Unfinished workflow task: '+task['kind']+' '+task['identity'])
        validate_decision(conn,config,task,event['receipt'])
        (pending if task['kind']=='coverage_review' else mapped).append(event['receipt'])
    pp.validate(queue,pending,AcquisitionIndex(conn,config['registry']['stream']))
    return mapped,pending


def reuse_mappings(conn,config,queue):
    """Reuse only decisions that contributed to the pinned finalized baseline."""
    baseline=config.get('baseline_capture')
    if not baseline:return 0
    if h.invalidation(conn,baseline):return 0
    row=conn.execute('SELECT c.seq,c.payload FROM captures c JOIN finalized_reports f ON f.capture_seq=c.seq WHERE c.capture_id=?',
                     (baseline,)).fetchone()
    if row is None:return 0
    payload=json.loads(row['payload'])
    contract=payload.get('workflow_report',{}).get('contract_sha256')
    if not contract:return 0
    old={}
    for saved in conn.execute('SELECT payload FROM captures WHERE stream=? AND seq<? ORDER BY seq',('workflow:'+contract,row['seq'])):
        event=json.loads(saved['payload']).get('workflow',{})
        if event.get('kind')=='decision' and event['task']['kind']=='publication_mapping':
            old[event['task']['identity']]=event
    done=w.accepted(conn,config);count=0
    for task in tasks(conn,config,queue):
        if task['kind']!='publication_mapping' or task['packet_sha256'] in done:continue
        prior=old.get(task['identity'])
        if not prior:continue
        before=prior['task']['inputs'];after=task['inputs']
        if {k:v for k,v in before.items() if k!='reporting_window'}!={k:v for k,v in after.items() if k!='reporting_window'}:continue
        receipt=copy.deepcopy(prior['receipt'])
        if receipt['removals']:continue  # Departure decisions are never silently replayed.
        same_window=all(before['reporting_window'][k]==queue['bounds'][k] for k in ('start','end'))
        policy='identical_reporting_period'
        if not same_window:
            if receipt['decision']=='include_directory':policy='unchanged_directory_finding'
            elif after['finding']['kind']=='opinion' and (receipt['decision']=='include' or
                    prior.get('reuse',{}).get('policy')=='previously_published_unchanged_opinion'):
                published=after['finding']['facts'].get('published_date')
                if not published or published>=queue['bounds']['start']:continue
                receipt.update(decision='exclude',candidate=None,
                               reason='Unchanged opinion already included in the last finalized report; its publication date precedes this reporting period.')
                policy='previously_published_unchanged_opinion'
            else:continue
        validate_decision(conn,config,task,receipt)
        event=dict(kind='decision',packet_sha256=task['packet_sha256'],task=task,receipt=receipt,
                   validation={'validated':'publication_mapping_reuse'},
                   reuse=dict(baseline_capture=baseline,decision_sha256=h.sha(prior),policy=policy))
        w.record(conn,config,event)
        w.materialize(config,task)
        w.write(Path(config['run_dir'])/'workflow'/'accepted'/(task['packet_sha256']+'.json'),event,immutable=True)
        count+=1
    return count


def assemble(conn, config, queue):
    mapped,pending=decisions(conn,config,queue)
    latest=(conn.execute('SELECT * FROM captures WHERE capture_id=?',(config['baseline_capture'],)).fetchone()
            if config['baseline_capture'] else None)
    base=json.loads(latest['payload']) if latest else {'findings':[]}
    records={f['key']:copy.deepcopy(f) for f in base['findings'] if f['kind'] in ('judge','clerk','source_inventory')}
    if latest:
        saved=conn.execute('SELECT manifest,manifest_sha256 FROM publication_acceptances WHERE capture_id=? ORDER BY accepted_at DESC LIMIT 1',(latest['capture_id'],)).fetchone()
        if saved:
            manifest=json.loads(saved['manifest'])
            if h.sha(manifest)!=saved['manifest_sha256']:raise ValueError('Baseline acceptance checksum mismatch')
            for roster in manifest['rosters']:
                if roster['inventory_key'] in records:
                    records[roster['inventory_key']]['facts']['entities']=copy.deepcopy(roster['people'])
    req=requirements(conn,config);dispositions=[];new={}
    for receipt in mapped:
        f=req[receipt['finding_id']]['finding'];key=None
        if receipt['decision']=='include':
            key='candidate-'+h.sha(receipt['finding_id'])[:24]
            facts=dict(receipt['candidate'],decision='include')
            records[key]=dict(key=key,kind='candidate',facts=facts,citations=receipt['citations'])
        elif receipt['decision']=='include_directory':
            key=f['key'] if f['key'].startswith('person-') else 'person-'+f['key']
            new[key]=dict(f,key=key)
        for r in receipt['inventories']+receipt['personnel']:
            if r['key'] in new and new[r['key']]!=r:
                raise ValueError('Conflicting projections for stable identity: '+r['key'])
            new[r['key']]=r
        dispositions.append(dict(finding_id=receipt['finding_id'],version=receipt['version'],decision=receipt['decision'],
                                 candidate_key=key,reason=receipt['reason'],citations=receipt['citations']))
    records.update(new)
    for receipt in mapped:
        for removal in receipt['removals']:
            old=records.get(removal['person_id'])
            if old is None or old['kind'] not in ('judge','clerk'):
                raise ValueError('Removal must identify an existing person')
            if old['facts']['name'] not in ' '.join(c['quote'] for c in removal['citations']):
                raise ValueError('Removal evidence must identify the actual person')
            del records[removal['person_id']]
    validate_records(conn,config,[r for r in records.values() if r['kind']!='candidate'])
    # Reconcile people immediately, not only at the final acceptance boundary.
    roster={}
    for r in records.values():
        if r['kind']=='source_inventory':
            for e in r['facts'].get('entities',[]):
                key='person-'+e['id'];identity=(e['name'],e['type'])
                if key in roster and roster[key]!=identity:
                    raise ValueError('Conflicting named roster identity')
                roster[key]=identity
    people={r['key']:(r['facts'].get('name'),r['kind']) for r in records.values() if r['kind'] in ('judge','clerk')}
    if people!=roster:
        raise ValueError('Complete the explicit roster/person projections; no inferred removals or unrostered people')
    fingerprint=h.sha(dict(queue=queue,mappings=mapped,pending=pending,baseline=latest['capture_id'] if latest else None))
    return records,dispositions,pending,fingerprint


def render(records, queue):
    esc=lambda value:html.escape(str(value),quote=True)
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Florida Litigator review</title><style>body{font:16px system-ui;max-width:76ch;margin:2rem auto;padding:0 1rem;overflow-wrap:anywhere}article{margin:2rem 0}a{color:#245984}</style><main><h1>The Florida Litigator</h1>',
           '<p>'+esc(queue['bounds']['start'])+' – '+esc(queue['bounds']['end'])+'</p>']
    if not queue['acquisition_complete']:
        parts.append('<p>Source coverage is incomplete. Missing findings do not establish no changes.</p>')
    for section,label in pub.SECTIONS:
        parts.append('<section><h2>'+esc(label)+'</h2>')
        items=[r for r in records.values() if r['kind']=='candidate' and r['facts']['section']==section]
        for r in sorted(items,key=lambda r:r['key']):
            f=r['facts'];parts.append('<article><h3>'+esc(f['title'])+'</h3>')
            for line in pub.candidate_summary(f,section).split('\n'):
                if line:parts.append('<p>'+esc(line)+'</p>')
            parts.append('<p><strong>Source:</strong> '+'; '.join('<a href="'+esc(pub.safe_url(c['url']))+'">Official source</a>' for c in r['citations'])+'</p></article>')
        if not items:parts.append('<p>No included items. See recorded review scope and limitations.</p>')
        parts.append('</section>')
    parts.append('<section><h2>Personnel review</h2>')
    for r in sorted(records.values(),key=lambda r:r['key']):
        if r['kind'] in ('judge','clerk'):
            parts.append('<article><h3>'+esc(r['facts']['name'])+'</h3><pre>'+esc(json.dumps(r['facts'],ensure_ascii=False,indent=2))+'</pre></article>')
    parts.append('</section></main></html>')
    return ''.join(parts).encode()


def prepare(run_dir, *, repair=False):
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        queue=w.latest_queue(conn,config,refresh=True)
        if queue is None:raise ValueError('Finish acquisition first')
        records,dispositions,pending,fingerprint=assemble(conn,config,queue)
        folder=Path(config['run_dir'])/'workflow'/'reports'/fingerprint
        previous=next((e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared' and e['fingerprint']==fingerprint),None)
        if repair:w.preserve_attempt(conn,config,folder)
        report=render(records,queue)
        contract=dict(window_start=queue['bounds']['start'],window_end=queue['bounds']['end'],tasks=[])
        # A verified assembly check is not a claim that every source was retrieved.
        payload=dict(status='ready_for_review',contract=contract,drafts=[],findings=sorted(records.values(),key=lambda r:r['key']),
                     checks=[dict(id='validated-workflow-assembly',status='verified',checked_at=queue_timestamp(conn,config),hashes=[h.sha(report)])],
                     workflow_report=dict(contract_sha256=h.sha(config),fingerprint=fingerprint,acquisition_complete=queue['acquisition_complete'],coverage_dispositions=pending))
        cap=h.record(conn,stream=config['registry']['stream'],mode='manual_research',scope=gate_scope(conn,config),
                     run_id='workflow-report:'+h.sha(config)+':'+fingerprint,payload=payload,artifacts={h.sha(report):report})
        folder.mkdir(parents=True,exist_ok=True)
        path=folder/'report.html'
        if path.exists() and path.read_bytes()!=report:raise ValueError('Saved report bytes changed')
        path.write_bytes(report)
        manifest=pa.template(conn,cap['capture_id'],path);manifest['dispositions']=dispositions;manifest['pending']=pending
        # Restore exact roster citations, not metadata invented from names.
        inventories={r['key']:r for r in records.values() if r['kind']=='source_inventory'}
        for roster in manifest['rosters']:
            roster['people']=copy.deepcopy(inventories.get(roster['inventory_key'],{}).get('facts',{}).get('entities',[]))
        w.write(folder/'acceptance-template.json',manifest,immutable=True)
        output=pub.export_capture(config['database'],cap['capture_id'],folder/'archive',preview=True)
        result=dict(kind='report_prepared',fingerprint=fingerprint,capture_id=cap['capture_id'],capture_seq=cap['seq'],
                    report=str(path),report_sha256=h.sha(report),acceptance_template=str(folder/'acceptance-template.json'),
                    acceptance_template_sha256=h.sha((folder/'acceptance-template.json').read_bytes()),
                    public_preview=str(output),public_preview_sha256=h.sha(Path(output).read_bytes()))
        result['projection_hashes']=w.projection_hashes([path,folder/'acceptance-template.json',output])
        if previous and any(result[k]!=previous[k] for k in ('report_sha256','acceptance_template_sha256','public_preview_sha256')):
            raise ValueError('Regenerated report differs from the recorded hashes; review required before continuing')
        w.record(conn,config,result);w.write(Path(config['run_dir'])/'workflow'/'report.json',result)
        return result


def gate_scope(conn,config):
    return json.loads(conn.execute('SELECT scope FROM streams WHERE stream=?',(config['registry']['stream'],)).fetchone()[0])


def queue_timestamp(conn,config):
    # Stable actual acquisition checkpoint time, not the wall clock of each replay.
    target=__import__('flwu.opinion_discovery',fromlist=['stream_for']).stream_for(config['registry']['stream'])[0]
    for r in conn.execute('SELECT recorded_at,payload FROM captures WHERE stream=? ORDER BY seq DESC',(target,)):
        e=json.loads(r['payload']).get('opinion_discovery',{})
        if e.get('run_id')==config['run_id'] and e.get('checkpoint')=='update-result':return r['recorded_at']
    raise ValueError('Missing acquisition checkpoint')


def state(conn,config,queue,*,emit=False):
    records,dispositions,pending,fingerprint=assemble(conn,config,queue)
    prepared=next((e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared' and e['fingerprint']==fingerprint),None)
    if prepared is None:
        return dict(phase='prepare_report',complete=False,command=w.command(config,'prepare-report','--run-dir',config['run_dir']))
    from flwu.workflow_directory import state as directory_state
    return directory_state(conn,config,queue,prepared,emit=emit)
