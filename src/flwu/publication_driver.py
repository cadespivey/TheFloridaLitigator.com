"""Deterministic transfer of reviewed content; small cards only for real decisions.

Legacy validators/receipts stay authoritative. This module never interprets a
legal change, invents a departure, certifies missing evidence, or claims review.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
from datetime import date

from flwu import history as h, workflow as w

KINDS = frozenset({'publication_mapping','coverage_review','directory_review',
                   'directory_removal','roster_review','publication_acceptance'})


def scope_choices():
    courts=w.read(Path(__file__).parent/'data/web/courts.json')
    return dict(court_ids=[c['group_id'] for c in courts],
                counties=[c['label'].removesuffix(' County') for c in courts if c['category']=='County Courts'])


def _base_records(conn, config):
    if not config.get('baseline_capture'):return {}
    row=conn.execute('SELECT payload FROM captures WHERE capture_id=?',(config['baseline_capture'],)).fetchone()
    if row is None:raise ValueError('Pinned publication baseline is missing')
    return {f['key']:copy.deepcopy(f) for f in json.loads(row[0])['findings']
            if f['kind'] in ('judge','clerk','source_inventory')}


def _scope(finding):
    facts=finding['facts']
    counties=facts.get('counties');courts=facts.get('court_ids')
    if not isinstance(counties,list) or any(not isinstance(v,str) for v in counties):return None
    if courts is not None and (not isinstance(courts,list) or any(not isinstance(v,str) for v in courts)):return None
    if not counties and not courts:return None
    return dict(counties=counties,court_ids=courts or [])


def _inventory(person, scope, records):
    """Preserve known membership; construct new membership only from explicit scope."""
    identity=person['key'].removeprefix('person-')
    existing=[f for f in records.values() if f['kind']=='source_inventory' and
              any(e['id']==identity for e in f['facts'].get('entities',[]))]
    if existing:
        if any(any(e['id']==identity and (e['name']!=person['facts']['name'] or e['type']!=person['kind'])
                   for e in f['facts']['entities']) for f in existing):
            raise ValueError('Reviewed identity conflicts with existing named roster')
        return []
    if scope is None:return None
    cite=next(c for c in person['citations'] if person['facts']['name'].casefold() in c.get('quote','').casefold())
    # Explicit scope is recorded once. Appellate exporter recognizes its existing
    # roster IDs; county inventories retain explicit counties on each entity.
    court_ids=scope['court_ids']
    # A delta inventory names this reviewed identity. Do not replace a whole
    # court roster, or let separately reviewed additions overwrite one another.
    key='roster-person-'+identity
    old=records.get(key)
    result=copy.deepcopy(old) if old else dict(key=key,kind='source_inventory',facts=dict(entities=[],court_ids=court_ids),citations=[])
    entity=dict(id=identity,name=person['facts']['name'],type=person['kind'],counties=scope['counties'],citation=copy.deepcopy(cite))
    if any(e['id']==identity for e in result['facts']['entities']):raise ValueError('Duplicate roster identity')
    result['facts']['entities'].append(entity)
    result['citations']=list({h.sha(c):c for c in result['citations']+person['citations']}.values())
    return [result]


def baseline_candidate(conn,config,task,row):
    """Reuse approved text in an explicit interval; dates never imply new law."""
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='publication_acceptances'").fetchone():return None
    saved=conn.execute('SELECT manifest,manifest_sha256 FROM publication_acceptances WHERE capture_id=? ORDER BY accepted_at DESC LIMIT 1',(config['baseline_capture'],)).fetchone()
    if not saved:return None
    manifest=json.loads(saved['manifest'])
    if h.sha(manifest)!=saved['manifest_sha256']:raise ValueError('Baseline acceptance checksum mismatch')
    decision=next((d for d in manifest['dispositions'] if d['finding_id']==task['identity'] and d['version']==task['inputs']['version'] and d['decision']=='include'),None)
    if not decision:return None
    payload=json.loads(row['payload'])
    record=next((f for f in payload['findings'] if f['key']==decision['candidate_key'] and f['kind']=='candidate'),None)
    if record is None:raise ValueError('Approved baseline candidate is missing')
    facts=record['facts'];bounds=task['inputs']['reporting_window']
    dates=[facts.get(k) for k in ('publication_date','effective_date') if facts.get(k)]
    for value in dates:date.fromisoformat(value)
    inside=any(bounds['start']<=value<=bounds['end'] for value in dates)
    # Undated findings keep their previously approved reporting-period meaning.
    # Do not manufacture a publication/effective date from that period.
    contract=payload.get('contract',{})
    overlap=(config.get('start') is not None and not dates and contract.get('window_start') and contract.get('window_end')
             and contract['window_start']<=bounds['end'] and contract['window_end']>=bounds['start'])
    if not inside and not overlap:return None
    return {k:copy.deepcopy(v) for k,v in facts.items() if k!='decision'}


def mapping(conn, config, task, *, supplied=None):
    """Return a receipt only when meaning is already explicitly recorded."""
    from flwu import workflow_report as report
    req=task['inputs'];finding=req['finding'];kind=finding['kind'];facts=finding['facts']
    receipt=copy.deepcopy(task['receipt_template'])
    receipt['reason']='Code transferred this exact reviewed finding/version without rewriting its meaning.'
    if kind not in ('opinion','judge','clerk','source_inventory','source_conflict') and config.get('baseline_capture'):
        baseline=conn.execute('SELECT seq,payload FROM captures WHERE capture_id=?',(config['baseline_capture'],)).fetchone()
        if baseline is None:raise ValueError('Pinned finalized baseline is missing')
        if req['capture_seq']<=baseline[0]:
            candidate=baseline_candidate(conn,config,task,baseline)
            receipt.update(decision='include' if candidate else 'exclude',candidate=candidate,
                           reason='Code reused the exact approved baseline text within the requested interval.' if candidate else
                                  'This exact reviewed finding predates the finalized baseline and is outside the requested interval; no new reviewed change is recorded.')
            report.validate_decision(conn,config,task,receipt)
            return receipt
    if kind=='opinion':
        published=facts.get('published_date')
        if not published:return None
        date.fromisoformat(published)
        bounds=req['reporting_window'];changed=False
        for e in w.accepted(conn,config).values():
            if e['task']['kind']=='opinion_review' and e['task']['identity']==finding['key']:
                reasons=e['task']['inputs'].get('reasons',[])
                changed=('official_status_metadata_changed' in reasons or
                         ('new_or_changed_pdf' in reasons and 'new_or_unreviewed_opinion' not in reasons))
        if bounds['start']<=published<=bounds['end'] or changed:
            receipt['decision']='include'
        else:
            receipt.update(decision='exclude',candidate=None,
                           reason='The recorded issuance date is outside this reporting window; no reviewed revision/status trigger is recorded for this run.')
    elif kind=='candidate':
        candidate=receipt['candidate']
        try:
            from flwu.editorial import validate_change
            validate_change(candidate,receipt['citations'])
            if not candidate.get('title') or candidate.get('section') not in ('case_law','statutes','procedural_rules','local_rules'):return None
        except (ValueError,TypeError,KeyError):return None
        receipt['decision']='include'
    elif kind in ('judge','clerk'):
        receipt.update(decision='include_directory',candidate=None)
        records=_base_records(conn,config)
        for requirement in report.requirements(conn,config).values():
            record=requirement['finding']
            if record['kind']=='source_inventory':records[record['key']]=record
        # Include prior derived projections from this run, not only the baseline.
        for done in w.accepted(conn,config).values():
            if done['task']['kind']=='publication_mapping':
                for record in done['receipt']['inventories']+done['receipt']['personnel']:records[record['key']]=record
        scope=(supplied or {}).get('scope') or _scope(finding)
        if scope is not None:
            if set(scope)!={'counties','court_ids'} or any(not isinstance(scope[k],list) or any(not isinstance(x,str) or not x for x in scope[k]) for k in scope):
                raise ValueError('Scope needs explicit counties and court_ids lists')
            if not scope['counties'] and not scope['court_ids']:raise ValueError('Personnel scope cannot be empty')
            choices=scope_choices()
            if set(scope['counties'])-set(choices['counties']) or set(scope['court_ids'])-set(choices['court_ids']):
                raise ValueError('Choose only the supported county and court IDs supplied on the card')
        inventories=_inventory(finding,scope,records)
        if inventories is None:return None
        receipt['inventories']=inventories
    elif kind=='source_inventory':
        receipt.update(decision='exclude',candidate=None,inventories=[copy.deepcopy(finding)],
                       reason='Reviewed named membership is a directory projection, not a legal news item.')
    elif kind=='source_conflict':
        receipt.update(decision='exclude',candidate=None,
                       reason='This typed source-conflict record remains in research evidence; it is not a separately reviewed legal-change candidate.')
    else:return None
    report.validate_decision(conn,config,task,receipt)
    return receipt


def directory(task):
    """Exact IDs and already reviewed departures need no new identity decision."""
    data=task['inputs'];receipt=copy.deepcopy(task['receipt_template'])
    receipt.update(reviewer='Code projection of reviewed personnel facts',
                   reason='Transferred reviewed facts to exact stable identities; untouched fields and county assignments are preserved.')
    if task['kind']=='directory_removal':return receipt
    if data['possible_matches']:return None
    targets=list(data['exact_matches']);covered={t['path'] for t in targets}
    for path in data['scopes']:
        if path not in covered:targets.append(dict(path=path,id=None))
    receipt['targets']=targets
    assignment=data.get('source_assignment')
    if assignment is not None:
        changed=[r for r in data['current_records'] if r['person'].get('assignment')!=assignment]
        if changed:return None  # County-specific reassignment is a semantic decision.
    return receipt


def _accept(run_dir, task, receipt, policy):
    """Use existing submission validation and durable idempotency, not a new gate."""
    path=Path(task['packet_path']).with_name('derived-'+h.sha(receipt)+'.json')
    w.write(task['packet_path'],task,immutable=True);w.write(path,receipt,immutable=True)
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        intent=dict(kind='publication_derivation_intent',packet_sha256=task['packet_sha256'],receipt_sha256=h.sha(receipt),policy=policy)
        if intent not in w.events(conn,config):w.record(conn,config,intent)
    result=w.submit(run_dir,task['packet_path'],path)
    with w.locked(config),h.database(config['database']) as conn:
        event=dict(kind='publication_derivation',packet_sha256=task['packet_sha256'],
                   receipt_sha256=h.sha(receipt),policy=policy)
        if event not in w.events(conn,config):w.record(conn,config,event)
    return result


def recover_derivations(run_dir):
    config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        events=w.events(conn,config);accepted=w.accepted(conn,config)
        for intent in events:
            if intent['kind']!='publication_derivation_intent':continue
            decision=accepted.get(intent['packet_sha256'])
            if not decision or h.sha(decision['receipt'])!=intent['receipt_sha256']:continue
            completed=dict(intent,kind='publication_derivation')
            if completed not in events:w.record(conn,config,completed);events.append(completed)


def _project(run_dir,state):
    from flwu import compact_review as compact
    config=w.load(run_dir);task=w.read(state['packet'])
    with w.locked(config),h.database(config['database']) as conn:
        return dict(state,**compact.project(conn,config,task),review_mode='short_answer')


def advance(run_dir):
    """Run local mechanical stages; never fetch/research or infer approvals."""
    from flwu import workflow_report as report,workflow_directory as dirs,workflow_release as release
    recover_derivations(run_dir)
    for _ in range(10000):
        state=w.inspect(run_dir,emit=True);kind=state['phase']
        if kind in KINDS:
            config=w.load(run_dir);task=w.read(state['packet']);receipt=None
            with h.database(config['database']) as conn:
                from flwu.workflow_short import unresolved
                checkpoint=unresolved(conn,config).get(task['packet_sha256'])
                if checkpoint:
                    from flwu.workflow_short import present,checked_command
                    return present(conn,config,w.latest_queue(conn,config),w.accepted(conn,config),dict(phase='publication_exceptions',complete=False,exceptions=[checkpoint],
                                explanation='A substantive publication decision remains unresolved; no finalization or release was performed.',
                                retry_command=checked_command(config,'retry',packet=task['packet_path']),
                                next_instruction='Use retry only when a substantively corrected answer is available. Do not poll or repeat an unresolved answer.'))
                if kind=='publication_mapping':receipt=mapping(conn,config,task)
                elif kind in ('directory_review','directory_removal'):receipt=directory(task)
                elif kind=='roster_review':
                    receipt=copy.deepcopy(task['receipt_template'])
                    receipt['reason']='Code reconciled the exact named inventory with reviewed personnel projections and explicitly cited removals; unchanged members are retained.'
                    removals={r['person_id']:r for e in w.accepted(conn,config).values()
                              if e['task']['kind']=='publication_mapping' for r in e['receipt']['removals']}
                    for removal in receipt.get('removals',[]):
                        reviewed=removals.get('person-'+removal['id'])
                        if reviewed is None:raise ValueError('Roster departure lacks an explicit reviewed removal decision')
                        removal.update(reason=reviewed['reason'],citations=copy.deepcopy(reviewed['citations']))
            if receipt is None:return _project(run_dir,state)
            _accept(run_dir,task,receipt,'reviewed-data-projection-v1');continue
        if kind=='prepare_report':report.prepare(run_dir);continue
        if kind=='refresh_directory':dirs.refresh(run_dir);continue
        if kind=='build_review_site':release.build(run_dir);continue
        if kind=='ready_for_publication':
            config=w.load(run_dir)
            with h.database(config['database']) as conn:
                prepared=next(e for e in reversed(w.events(conn,config)) if e['kind']=='report_prepared' and e['capture_id']==state['capture_id'])
                h.finalize(conn,prepared['capture_id'],Path(prepared['report']),'Content approved through the bound compact publication review; deterministic transfer checks retained.')
            continue
        if kind=='export_publication':release.export(run_dir);continue
        if kind=='publication_handoff':release.integrate(run_dir);continue
        if kind in ('release_required','merge_required','deployment_verification'):
            config=w.load(run_dir)
            state['command']=w.command(config,'workflow','release','--run-dir',str(Path(run_dir).resolve()),'--execute','--merge','--wait')
            with h.database(config['database']) as conn:
                checkpoint=next((e for e in reversed(w.events(conn,config)) if e['kind']=='release_execution_checkpoint'),None)
            if checkpoint:
                state['release_checkpoint']=checkpoint['result']
                if checkpoint['result']['phase']=='release_failed' or checkpoint['result'].get('wait_expired'):
                    state['next_instruction']='Preserve this recorded release. Correct the reported condition before re-executing its command; do not poll an unchanged failure or restart research.'
        return state
    raise ValueError('Deterministic publication transition limit reached; preserved state requires inspection')


def _citations(task):
    if task['kind']=='publication_mapping':return task['inputs']['finding']['citations']
    if task['kind']=='coverage_review':return task['inputs']['task'].get('citations',[])
    if task['kind']=='directory_review':
        return [c for person in task['inputs'].get('current_records',[]) for c in person['person'].get('sources',[]) if c.get('quote')]
    return []


def prepare_card(conn,task):
    """Only small semantic fields are model-authored; exact receipts stay hidden."""
    evidence=[];bindings={}
    for ci in _citations(task):
        if not ci.get('quote'):continue
        ident='E'+str(len(evidence)+1);evidence.append(dict(id=ident,passage=ci['quote']));bindings[ident]=ci
    kind=task['kind'];template=dict(decision='',reason='')
    card=dict(question='',evidence=evidence,answer=template,
              instructions='Use reviewed data and the supplied evidence only. Do not copy citations, hashes, versions or receipt schemas. Missing meaning/evidence remains unresolved; do not restart research or invent facts.')
    if kind=='publication_mapping':
        finding=task['inputs']['finding']
        card['finding']={k:finding[k] for k in ('key','kind','facts')}
        card['reporting_window']=task['inputs']['reporting_window']
        if finding['kind'] in ('judge','clerk'):
            template['scope']=dict(counties=[],court_ids=[])
            card['scope_choices']=scope_choices()
            card['question']='This new reviewed person lacks explicit roster scope. State supported counties/court_ids once, or choose unresolved. Include_directory is not legal news and does not remove a predecessor.'
            card['choices']=['include_directory','unresolved']
        else:
            template['candidate']=None
            card['question']='Supply missing publication meaning/metadata for this reviewed finding, or exclude it with a supported reason. Code will copy the evidence and create the mapping.'
            card['choices']=['include','exclude','unresolved']
            card['candidate_fields']='For include: section (statutes/procedural_rules/local_rules), title, summary, publication_date/effective_date (actual stated dates or null), legal_status. change_analysis: material=true, previous_requirement, current_requirement, practical_effect, basis_quote (exact supplied passage substring). A baseline or source discrepancy alone is not an amendment. Do not invent dates or a prior requirement.'
    elif kind=='directory_review':
        data=task['inputs'];template.update(targets=[],assignment_updates=[])
        card.update(question='Resolve only this personnel identity/scope or county-specific assignment. Code already owns contacts and preservation of untouched values.',
                    person=data['person']['name'],possible_matches=data['possible_matches'],exact_matches=data['exact_matches'],
                    scopes=data['scopes'],current_records=data['current_records'],source_assignment=data.get('source_assignment'),choices=['approve','unresolved'])
        card['answer_help']='targets: supplied path plus existing id or null for new. assignment_updates: path, value, reason, evidence IDs; only expressly supported assignments. No copied citation objects.'
        # Use already reviewed person citations from this report for assignments.
        cap=conn.execute('SELECT payload FROM captures WHERE capture_id=?',(data['capture_id'],)).fetchone()
        finding=next(f for f in json.loads(cap[0])['findings'] if f['key']==task['identity'])
        for ci in finding['citations']:
            ident='E'+str(len(evidence)+1);evidence.append(dict(id=ident,passage=ci['quote']));bindings[ident]=ci
    elif kind=='coverage_review':
        card.update(question='Resolve this recorded acquisition exception only. A failure cannot become no-change.',failure=task['inputs'],choices=['unavailable','scope_excluded','unresolved'])
        template['evidence']=[]
    elif kind=='publication_acceptance':
        template['corrections']=[]
        manifest=task['receipt_template'];row=conn.execute('SELECT payload FROM captures WHERE capture_id=?',(manifest['capture_id'],)).fetchone()
        findings=json.loads(row[0])['findings'];entries=[]
        for f in findings:
            if f['kind']=='candidate':entries.append(dict(ref='N'+str(len(entries)+1),**f['facts']))
        audit=w.read(task['inputs']['directory_audit'])
        card.update(question='Approve publication of these reviewed current entries and directory changes, or correct a substantive opinion error. Do not repeat research or re-review unchanged rosters. Approval is bound to this exact report/build.',
                    entries=entries,directory_changes=[dict(before=x.get('before'),after=x.get('after')) for x in audit],
                    report=task['inputs']['report'],site=task['inputs']['site'],choices=['approve','correct','unresolved'])
        card['answer_help']='Approve: reason describes actual content approval; corrections empty. Correct: corrections [{entry:N-reference, summary and/or holding/disposition/authors, reason}], using the reviewed opinion evidence. Code appends a bound revision and rebuilds; never edit generated files. Unresolved blocks finalization. Reviewer is your actual model identity if available, not an independent human. Mechanical artifact checks are code-owned, not a claim of browser/human visual review.'
        # Hidden original mapping allows exact, version-bound corrections.
    return dict(version=1,packet_sha256=task['packet_sha256'],card=card,bindings=bindings,
                answer_template=template,prior_people={},exception=None)


def retry(run_dir,packet):
    """Explicitly reopen one current checkpoint without acquisition or data reset."""
    from flwu.workflow_short import unresolved
    config=w.load(run_dir);state=w.inspect(run_dir,emit=True)
    if state.get('phase') not in KINDS or Path(state['packet']).resolve()!=Path(packet).resolve():
        raise ValueError('Retry must name the current preserved publication task')
    with h.database(config['database']) as conn:
        if w.read(state['packet'])['packet_sha256'] not in unresolved(conn,config):
            raise ValueError('Publication task has no unresolved checkpoint')
    from flwu.review_transport import model_state
    return model_state(run_dir,_project(run_dir,state))


def compile_card(task,bundle,answer):
    """Copy reviewed proof into legacy receipts; no model-authored plumbing."""
    from flwu import compact_review as compact
    if set(answer) not in (set(bundle['answer_template']),set(bundle['answer_template'])|{'reviewer'}):
        raise ValueError('Use only the compact publication answer fields')
    if not isinstance(answer['reason'],str) or not answer['reason'].strip():raise ValueError('A substantive decision reason is required')
    if answer['decision']=='unresolved':return None
    receipt=copy.deepcopy(task['receipt_template']);kind=task['kind']
    receipt['reason']=answer['reason']
    reviewer=answer.get('reviewer','Model identity unavailable')
    if kind=='publication_mapping':
        if task['inputs']['finding']['kind'] in ('judge','clerk'):
            if answer['decision']!='include_directory':raise ValueError('Choose include_directory or unresolved')
            # Compiled in the caller with its database-bound baseline context.
            return dict(_person_scope=answer['scope'],_reason=answer['reason'])
        if answer['decision'] not in ('include','exclude'):raise ValueError('Choose include, exclude or unresolved')
        receipt.update(decision=answer['decision'],candidate=copy.deepcopy(answer['candidate']))
    elif kind=='directory_review':
        if answer['decision']!='approve':raise ValueError('Choose approve or unresolved')
        receipt.update(reviewer=reviewer,targets=answer['targets'],assignment_updates=[])
        for change in answer['assignment_updates']:
            if set(change)!={'path','value','reason','evidence'}:raise ValueError('Use the supplied assignment update fields')
            receipt['assignment_updates'].append(dict(path=change['path'],value=change['value'],reason=change['reason'],citations=compact._refs(change['evidence'],bundle,full=True)))
        # Alias choices bind both names to acquired person evidence.
        receipt['identity_citations']=[copy.deepcopy(c) for c in bundle['bindings'].values()]
    elif kind=='coverage_review':
        receipt.update(decision=answer['decision'],citations=compact._refs(answer['evidence'],bundle,full=True) if answer['evidence'] else [])
    elif kind=='publication_acceptance':
        if answer['decision']=='correct':return dict(_opinion_corrections=answer['corrections'],_reason=answer['reason'],_reviewer=reviewer)
        if answer['decision']!='approve' or answer['corrections']:raise ValueError('Approve without corrections, or choose correct/unresolved')
        receipt.pop('reason',None)
        receipt.update(reviewer=reviewer,legal_review=answer['reason'],
                       visual_review='Code verified exact build bytes, current-data serialization and renderer contracts. This is automated artifact validation, not independent human or browser visual review.')
    else:raise ValueError('This task has a code-owned projection, not another semantic answer')
    return receipt


def artifact_checks(conn,task):
    """Verify the current build/data contract, without asserting visual inspection."""
    import re
    from bs4 import BeautifulSoup
    from flwu.workflow_release import verify_build
    data=task['inputs']
    config_events=[json.loads(r[0]).get('workflow',{}) for r in conn.execute(
        "SELECT payload FROM captures WHERE stream LIKE 'workflow:%' ORDER BY seq")]
    build=next(e for e in reversed(config_events) if e.get('kind')=='site_built' and e['identity']==data['build_identity'] and e['capture_id']==data['capture_id'])
    verify_build(build)
    site=Path(data['site']);pointer=w.read(site/'assets/current-archive.json');name=pointer.get('archive','')
    if not re.fullmatch(r'archive-[0-9a-f]{16}\.json',name):raise ValueError('Invalid review-site archive pointer')
    raw=(site/'assets'/name).read_bytes()
    if name!='archive-'+h.sha(raw)[:16]+'.json':raise ValueError('Review-site archive content hash differs')
    archive=json.loads(raw)
    prepared=next(e for e in reversed(config_events) if e.get('kind')=='report_prepared' and e['capture_id']==data['capture_id'])
    expected=w.read(prepared['public_preview'])
    if archive['issues']!=[expected] or archive['preview'] is not True:raise ValueError('Review site differs from the prepared current report')
    directories=next(e for e in reversed(config_events) if e.get('kind')=='directories_prepared' and e['capture_id']==data['capture_id'] and e['audit']==data['directory_audit'])
    if archive['county_directories']!=[w.read(p) for p in directories['directory_paths']]:raise ValueError('Review site directory data differs from the reviewed projections')
    page=BeautifulSoup((site/'index.html').read_bytes(),'html.parser')
    if not page.select_one('body[data-page="updates"]') or not page.select_one('main#report'):
        raise ValueError('Review site lacks current-report rendering targets')
    for ident in ('from','to','latest'):
        if not page.find(id=ident):raise ValueError('Review site lacks date controls: '+ident)
    if page.select_one('#archive-data').get('href')!='assets/'+name:raise ValueError('Review page does not reference its verified archive')
    return dict(build_identity=data['build_identity'],capture_id=data['capture_id'],
                report_sha256=h.sha(Path(data['report']).read_bytes()),archive_sha256=h.sha(raw),
                checks=['build-bytes','current-report-data','directory-data','date-control-targets','archive-reference'],
                browser_visual_review=False)


def correct_opinions(run_dir,task,bundle,receipt,answer):
    """Explicit semantic edits use existing append-only, source-bound revisions."""
    from flwu import opinion_discovery as opinions,source_gate as gate
    corrections=receipt['_opinion_corrections']
    if not isinstance(corrections,list) or not corrections:raise ValueError('Correct requires a nonempty corrections list')
    entries={x['ref']:x for x in bundle['card']['entries']};seen=set();config=w.load(run_dir)
    with w.locked(config),h.database(config['database']) as conn:
        row=conn.execute('SELECT seq FROM captures WHERE capture_id=?',(task['identity'],)).fetchone()
        if conn.execute('SELECT 1 FROM finalized_reports WHERE capture_seq=?',(row[0],)).fetchone():raise ValueError('Cannot correct a finalized publication in place')
        # Freeze all original versions from the reviewed report, not the moving head.
        originals={}
        for saved in conn.execute('SELECT payload FROM captures WHERE stream=? AND seq<=? ORDER BY seq',(config['registry']['stream'],row[0])):
            review=json.loads(saved[0]).get('opinion_review')
            if review:originals[review['id']]=review
        planned=[]
        for correction in corrections:
            if not isinstance(correction,dict) or not {'entry','reason'}<=set(correction) or set(correction)-{'entry','reason','summary','holding','disposition','authors'}:
                raise ValueError('Opinion correction needs an entry, reason and only reader-facing changed fields')
            ref=correction['entry']
            if ref not in entries or ref in seen:raise ValueError('Correction references a missing or duplicate current entry')
            seen.add(ref);original=originals.get(entries[ref]['id'])
            if original is None:raise ValueError('Only current opinion entries use this editorial correction path')
            if not isinstance(correction['reason'],str) or not correction['reason'].strip():raise ValueError('Correction needs a substantive reason')
            base={k:copy.deepcopy(original[k]) for k in ('id','signature','reviewer','relevance','summary','holding','disposition','authors','citations')}
            for key in ('summary','holding','disposition','authors'):
                if key in correction:base[key]=copy.deepcopy(correction[key])
            if any(not isinstance(base[k],str) or not base[k].strip() for k in ('summary','holding','disposition')) or not isinstance(base['authors'],list):raise ValueError('Correction must retain complete opinion text and author list')
            if all(base[k]==original[k] for k in ('summary','holding','disposition','authors')):raise ValueError('Correction must change reader-facing content')
            base['reviewer']=receipt['_reviewer']
            revision=dict(predecessor_version=original['receipt_sha256'],reason=correction['reason'],review_protocol=config['registry']['review_protocol'],
                          pdf_sha256=original['pdf_sha256'],state_sha256=original['state_sha256'])
            planned.append((dict(base,**revision),h.sha(dict(base,editorial_revision=revision))))
        frozen=Path(task['packet_path']).with_name('correction-'+h.sha(receipt)+'.json')
        w.write(frozen,receipt,immutable=True)
        w.record(conn,config,dict(kind='answer_compiled',packet_sha256=task['packet_sha256'],answer=answer,receipt_path=str(frozen),receipt_sha256=h.sha(receipt),projection_hashes=w.projection_hashes([frozen])))
        # Each intent is durable before a domain mutation; exact restart skips
        # the already committed version and refuses an unrelated newer review.
        w.record(conn,config,dict(kind='submission',task=task,receipt=receipt))
        for revised,digest in planned:
            latest=next(json.loads(r['payload'])['opinion_review'] for r in reversed(gate.rows(conn,config['registry']['stream'])) if json.loads(r['payload']).get('opinion_review',{}).get('id')==revised['id'])
            if latest['receipt_sha256']==digest:continue
            if latest['receipt_sha256']!=revised['predecessor_version']:raise ValueError('Opinion changed since the correction card; refresh current publication')
            opinions.revise_review(conn,config['registry'],revised)
        w.record(conn,config,dict(kind='publication_content_corrected',packet_sha256=task['packet_sha256'],receipt_sha256=h.sha(receipt),opinion_versions=[digest for _,digest in planned]))
