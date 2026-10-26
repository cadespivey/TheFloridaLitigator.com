"""Reviewable current-directory deltas; never write public files during preview."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import re

from flwu import history as h, workflow as w, county_directory as cd, publication as pub
from flwu.directory_display import format_contacts, load_formats
from flwu.evidence_binding import AcquisitionIndex


def inputs(config, prepared):
    for key in ('report','public_preview','acceptance_template'):
        if h.sha(Path(prepared[key]).read_bytes())!=prepared[key+'_sha256']:
            raise ValueError('Prepared artifact changed: '+key)
    issue=w.read(prepared['public_preview'])
    supplements={path:w.read(path) for path in config['directories']}
    for value in supplements.values():cd.validate_supplement(value)
    return issue,supplements


def scope_matches(person, supplement):
    if supplement['schema_version']==2:
        return supplement['court_scope'] in person.get('court_ids',[])
    return supplement['county'] in person['counties']


def contacts(person):
    result=format_contacts(person,load_formats())
    for side in result.values():
        for row in side:
            row['lines']=[line for value in row['lines'] for line in value.splitlines() if line.strip()]
            row['fact_path']='reviewed_person_details'
            row['label']=re.sub(r'^(?:Chambers|Office|Guide|Profile)\s+','',row['label']).capitalize()
            if row['label']=='Assignment':row['type']='note'
    return result


def merge_contacts(old, proposed):
    """Replace reviewed data categories; preserve fields absent from this source.

    A partial current profile is not evidence that an older address or assistant
    disappeared. Explicit contradictions stay in evidence and in the review packet.
    """
    result=copy.deepcopy(old)
    for side, rows in proposed.items():
        def label(row):
            return re.sub(r'^(?:judicial )?assistant\s+', '', row['label'].casefold()).strip()
        labels={label(row) for row in rows}
        result[side]=[row for row in result[side] if label(row) not in labels]+copy.deepcopy(rows)
    return result


def current(conn, config, prepared):
    _, supplements = inputs(config, prepared)
    return next((e for e in reversed(w.events(conn, config)) if e['kind']=='directories_prepared'
                 and e['capture_id']==prepared['capture_id'] and e['input_sha256']==h.sha(supplements)), None)


def tasks(conn,config,prepared):
    issue,supplements=inputs(config,prepared)
    captured=json.loads(conn.execute('SELECT payload FROM captures WHERE capture_id=?',(prepared['capture_id'],)).fetchone()[0])
    findings={f['key']:f for f in captured['findings']}
    # Only explicit, source-bound removal decisions can remove existing rows.
    from flwu.workflow_report import decisions
    mappings,_=decisions(conn,config,w.latest_queue(conn,config))
    removals={r['person_id']:r for mapping in mappings for r in mapping['removals']}
    for person_id, removal in removals.items():
        targets=[dict(path=path,id=p['id']) for path,s in supplements.items() for p in s['people']
                 if p['id']==person_id or p.get('legacy_person_id')==person_id]
        if targets:
            yield w.packet(config,'directory_removal',person_id,
                           dict(removal=removal,targets=targets,scopes={t['path']:h.sha(supplements[t['path']]) for t in targets}),
                           dict(person_id=person_id,targets=targets,reviewer='',reason=''),
                           'Confirm the cited departure applies to these exact current directory identities. '
                           'Omission from a partial page is not a departure; all other people remain unchanged.',
                           checks=('Explicit source-bound removal and exact current IDs',))
    for person in issue['directory']:
        scoped={path:s for path,s in supplements.items() if scope_matches(person,s)}
        matches=[];choices=[]
        for path,s in scoped.items():
            for old in s['people']:
                if old['id']==person['id'] or old.get('legacy_person_id')==person['id']:
                    matches.append(dict(path=path,id=old['id']))
                elif old['name']==person['name']:
                    choices.append(dict(path=path,id=old['id'],name=old['name'],profile_url=old['profile_url']))
        # Only existing covered scopes are projected. Weekly-only appellate
        # records remain in the report directory; no new coverage is invented.
        if not scoped:continue
        proposal=contacts(person)
        source_facts=findings[person['id']]['facts']
        assignment=source_facts.get('assignment') or person['details'].get('Assignment')
        assignment_changed=assignment is not None and any(
            next(p for p in supplements[m['path']]['people'] if p['id']==m['id'])['assignment']!=assignment for m in matches)
        if not assignment_changed and len(matches)==len(scoped) and not choices and all(
            (lambda old:old==merge_contacts(old,proposal))(next(p for p in supplements[m['path']]['people'] if p['id']==m['id'])['contacts'])
            for m in matches):
            continue
        template=dict(person_id=person['id'],targets=matches,reviewer='',reason='',identity_citations=[],assignment_updates=[])
        facts=dict(capture_id=prepared['capture_id'],person=person,proposed_contacts=proposal,
                   source_assignment=assignment,
                   scopes={path:dict(sha256=h.sha(s),county=s.get('county'),court_scope=s.get('court_scope')) for path,s in scoped.items()},
                   exact_matches=matches,possible_matches=choices,
                   current_records=[dict(path=path,person=p) for path,s in scoped.items() for p in s['people']
                                    if p['id'] in {m['id'] for m in matches+choices}])
        yield w.packet(config,'directory_review',person['id'],facts,template,
                       'Review this person only. Exact stable-ID matches are prefilled. For a new person choose '
                       'a covered scope path and id:null; for an existing alias choose its actual ID. '
                       'Preserve distinct county records. Ambiguous matches require cited identity evidence. '
                       'Contact values are projected from validated facts; do not edit the generated proposal. '
                       'Matching contact labels are replaced; absent fields and county assignments are preserved. '
                       'For a supported reassignment, add assignment_updates with path, value, reason and citations; '
                       'each quotation must identify this judge and the new assignment.',
                       checks=('Source-bound contacts, stable identities and scope', 'Unchanged people preserved'))


def validate_decision(conn,config,task,receipt):
    if set(receipt)!=set(task['receipt_template']) or receipt['person_id']!=task['identity']:
        raise ValueError('Use the exact directory-review receipt')
    if not receipt['reviewer'].strip() or not receipt['reason'].strip():
        raise ValueError('Directory projection requires actual review and reason')
    if task['kind']=='directory_removal':
        if receipt['targets']!=task['inputs']['targets']:raise ValueError('Do not change explicit removal targets')
        index=AcquisitionIndex(conn,config['registry']['stream'])
        for cite in task['inputs']['removal']['citations']:index.validate(cite)
        for path,digest in task['inputs']['scopes'].items():
            if h.sha(w.read(path))!=digest:raise ValueError('Directory changed since removal review')
        return {'validated':'directory_removal'}
    data=task['inputs'];person=data['person'];targets=receipt['targets']
    if not isinstance(targets,list) or not targets:
        raise ValueError('Choose explicit covered directory targets')
    if len({t['path'] for t in targets})!=len(targets) or set(t['path'] for t in targets)!=set(data['scopes']):
        raise ValueError('Each covered county/court scope needs exactly one target')
    index=AcquisitionIndex(conn,config['registry']['stream'])
    for cite in receipt['identity_citations']:index.validate(cite)
    changes=receipt['assignment_updates']
    if not isinstance(changes,list) or len({change['path'] for change in changes})!=len(changes):
        raise ValueError('Assignment changes require unique explicit scope paths')
    for change in changes:
        if (set(change)!={'path','value','reason','citations'} or change['path'] not in data['scopes']
            or not isinstance(change['value'],str) or not change['value'].strip() or not change['reason'].strip()
            or not change['citations']):raise ValueError('Assignment update needs scope, value, reason and acquired evidence')
        for cite in change['citations']:index.validate(cite)
        quoted=' '.join(c.get('quote','') for c in change['citations'])
        if person['name'] not in quoted or change['value'] not in quoted:
            raise ValueError('Assignment evidence must quote the named person and assignment')
    for target in targets:
        if set(target)!={'path','id'}:raise ValueError('Directory target needs path and existing ID or null')
        current=w.read(target['path'])
        if h.sha(current)!=data['scopes'][target['path']]['sha256']:
            raise ValueError('Directory changed since review packet; regenerate')
        old=next((p for p in current['people'] if p['id']==target['id']),None)
        if target['id'] is not None and old is None:raise ValueError('Unknown directory identity')
        exact=target in data['exact_matches']
        if old and not exact:
            quoted=' '.join(c.get('quote','') for c in receipt['identity_citations'])
            if old['name'] not in quoted or person['name'] not in quoted:
                raise ValueError('Alias mapping requires quoted identity support for both source names')
        if old is None and any(p['id']==person['id'] or p.get('legacy_person_id')==person['id'] or p['name']==person['name'] for p in current['people']):
            raise ValueError('New entry would duplicate an existing identity; reconcile it explicitly')
    return {'validated':'directory_projection','capture_id':data['capture_id']}


def refresh(run_dir):
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        from flwu.workflow_report import assemble
        queue=w.latest_queue(conn,config,refresh=True)
        _,_,_,fingerprint=assemble(conn,config,queue)
        prepared=next((e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared' and e['fingerprint']==fingerprint),None)
        if prepared is None:raise ValueError('Prepare the current report first')
        issue,supplements=inputs(config,prepared);done=w.accepted(conn,config)
        pending=list(tasks(conn,config,prepared))
        missing=[t for t in pending if t['packet_sha256'] not in done]
        if missing:return dict(phase='directory_review',complete=False,**w.materialize(config,missing[0]))
        cap=conn.execute('SELECT * FROM captures WHERE capture_id=?',(prepared['capture_id'],)).fetchone()
        payload=json.loads(cap['payload']);findings={f['key']:f for f in payload['findings']}
        observation=dict(capture_seq=cap['seq'],capture_id=cap['capture_id'],recorded_at=cap['recorded_at'])
        through=dict(seq=cap['seq'],capture_id=cap['capture_id'],recorded_at=cap['recorded_at'],research_status='ready_for_review')
        changed={};audit=[]
        for task in pending:
            receipt=done[task['packet_sha256']]['receipt'];validate_decision(conn,config,task,receipt)
            if task['kind']=='directory_removal':
                for target in receipt['targets']:
                    draft=changed.setdefault(target['path'],copy.deepcopy(supplements[target['path']]))
                    old=next(p for p in draft['people'] if p['id']==target['id'])
                    draft['people'].remove(old)
                    audit.append(dict(path=target['path'],before=old,after=None,decision_sha256=h.sha(receipt)))
                    draft.update(stream=config['registry']['stream'],through_capture=through,review_status='reviewed',
                                 review=dict(reviewed_by=receipt['reviewer'],reviewed_at=decision_time(conn,config,task),attestation=receipt['reason']))
                continue
            person=task['inputs']['person'];finding=findings[person['id']]
            sources=[{k:c[k] for k in ('url','sha256','retrieved_at')} for c in finding['citations']]
            for target in receipt['targets']:
                original=supplements[target['path']];draft=changed.setdefault(target['path'],copy.deepcopy(original))
                old=next((p for p in draft['people'] if p['id']==target['id']),None)
                if old:
                    new=copy.deepcopy(old)
                    if new['id']!=person['id']:new['legacy_person_id']=person['id']
                else:
                    new=dict(id=person['id'],name=person['name'],kind='Clerk' if person['kind']=='clerk' else 'Judge',
                             counties=[] if draft['schema_version']==2 else [draft['county']],
                             court_ids=[c['group_id'] for c in draft['courts']],assignment=None,
                             profile_url=None,procedure_url=None,dates=None,conflicts=[],contact_notes=[],sources=[])
                new.update(contacts=merge_contacts(old['contacts'],task['inputs']['proposed_contacts']) if old else copy.deepcopy(task['inputs']['proposed_contacts']),source_observation=observation,contact_status='source_recorded')
                new['sources']=list({(c['url'],c['sha256'],c['retrieved_at']):c for c in new['sources']+sources}.values())
                for field in ('profile_url','procedure_url'):
                    if person.get(field):new[field]=person[field]
                # A cross-county person finding does not override independently
                # reviewed county assignments. New entries use the source finding.
                if old is None:new['assignment']=person['details'].get('Assignment')
                assignment=next((item for item in receipt['assignment_updates'] if item['path']==target['path']),None)
                if assignment:
                    new['assignment']=assignment['value']
                    for cite in assignment['citations']:
                        source={k:cite[k] for k in ('url','sha256','retrieved_at')}
                        if source not in new['sources']:new['sources'].append(source)
                if old:draft['people'][draft['people'].index(old)]=new
                else:draft['people'].append(new)
                audit.append(dict(path=target['path'],before=old,after=new,decision_sha256=h.sha(receipt)))
                draft.update(stream=config['registry']['stream'],through_capture=through,review_status='reviewed',
                             review=dict(reviewed_by=receipt['reviewer'],reviewed_at=decision_time(conn,config,task),
                                         attestation='Explicit person-by-person review receipts and source-bound projections retained in workflow audit. '+receipt['reason']))
        version=h.sha(dict(capture=cap['capture_id'],audit=audit,inputs={k:h.sha(v) for k,v in supplements.items()}))
        folder=Path(config['run_dir'])/'workflow'/'directories'/version;paths=[]
        for source,value in supplements.items():
            if source in changed:
                value=changed[source];value['content_sha256']=cd.digest({k:v for k,v in value.items() if k!='content_sha256'})
                cd.validate_supplement(value)
            path=folder/(Path(source).parent.name+'-'+Path(source).name)
            w.write(path,value,immutable=True);paths.append(str(path))
        cd.load_supplements(paths)
        w.write(folder/'field-audit.json',audit,immutable=True)
        result=dict(kind='directories_prepared',capture_id=cap['capture_id'],input_sha256=h.sha(supplements),
                    directory_paths=paths,audit=str(folder/'field-audit.json'),changed_files=len(changed),changed_people=len(audit))
        w.record(conn,config,result);w.write(Path(config['run_dir'])/'workflow'/'directories.json',result)
        return result


def decision_time(conn, config, task):
    for row in conn.execute('SELECT recorded_at,payload FROM captures WHERE stream=? ORDER BY seq DESC', (w.stream(config),)):
        event=json.loads(row['payload'])['workflow']
        if event['kind']=='decision' and event['packet_sha256']==task['packet_sha256']:
            return row['recorded_at']
    raise ValueError('Missing accepted directory review timestamp')


def state(conn,config,queue,prepared,*,emit=False):
    saved=current(conn,config,prepared)
    if saved is None:
        return dict(phase='refresh_directory',complete=False,command=w.command(config,'refresh-directory','--run-dir',config['run_dir']))
    from flwu.workflow_release import state as release_state
    return release_state(conn,config,prepared,saved,emit=emit)
