"""Behavioral short-answer checks against acquired bytes and existing validators."""
import copy
import json
from pathlib import Path
import pytest
from flwu import history as h, source_gate as g, workflow as w, compact_review as short
from flwu import workflow_short as runner, workflow_report
from tests.test_source_gate import env, acquire, receipt
from tests.test_workflow import environment


def changed_task(env, before='Sandra Williams was Clerk.\nPhone: 555-0100\n',
                 after='Kristopher Warburton was selected as Clerk on October 30, 2026.\nPhone: (386) 947-1530\nExact\u00a0spacing and, punctuation.\n'):
    c,r,root=env
    first,_=acquire(env,'before',page=before.encode())
    for t in first['tasks']:g.accept(c,r,receipt(t,r,c))
    acquire(env,'after',page=after.encode())
    q=g.write_queue(c,r,root/'sources')
    task=next(w.tasks(c,{'run_dir':str(root/'run')},{'source_reviews':q,'opinion_reviews':{'tasks':[]}}))
    return task,short.prepare(c,task)


def person_answer(bundle):
    ref=next(e['id'] for e in bundle['card']['evidence'] if e['side']=='current')
    return dict(decision='material_change',summary='Kristopher Warburton was selected as Clerk on October 30, 2026; the source gives the office telephone.',
                evidence=[ref],people=[dict(person='new',name='Kristopher Warburton',kind='clerk',evidence=[ref],
                    fields={'office_phone':dict(value='(386) 947-1530',evidence=ref)})])


def test_new_clerk_exact_quotes_citations_and_real_directory_projection(env):
    c,r,root=env;t,b=changed_task(env);original=copy.deepcopy(t)
    answer=person_answer(b);draft=short.compile_answer(t,b,answer)
    person=draft['findings'][0];field=person['facts']['fields']['office_phone']
    assert person['kind']=='clerk' and person['key'].startswith('person-kristopher-warburton-')
    assert field['value']=='(386) 947-1530' and field['status']=='verified'
    assert field['citation'] in person['citations'] and len(person['citations'])==1
    assert 'Exact\u00a0spacing and, punctuation.' in field['citation']['quote']
    assert field['citation']['quote'] in g.blob(c,field['citation']['text_sha256']).decode()
    saved=g.accept(c,r,draft)
    records=[{k:person[k] for k in ('key','kind','facts','citations')}]
    workflow_report.validate_records(c,{'registry':r},records)
    assert g.accept(c,r,draft)['capture_id']==saved['capture_id']
    assert t==original and 'citations' not in answer


def test_nonperson_material_change_preserves_semantics(env):
    c,r,_=env;t,b=changed_task(env,before='Civil motions: five days notice.\n',after='Civil motions: ten days notice.\n')
    draft=short.compile_answer(t,b,dict(decision='material_change',summary='Civil motions now require ten days notice rather than five.',evidence=['C1'],people=[]))
    assert draft['findings'][0]['facts']['summary']=='Civil motions now require ten days notice rather than five.'
    assert draft['findings'][0]['kind']=='source_change'
    g.accept(c,r,draft)


def test_no_material_decision_covers_all_changed_lines_without_quote_retyping(env):
    c,r,_=env;t,b=changed_task(env,before='Opinions widget: Nov 1\n',after='Opinions widget: Nov 4\n')
    draft=short.compile_answer(t,b,dict(decision='no_material_change',summary='Only an opinions-navigation date changed; this profile states no personnel or procedural change.',evidence=['C1'],people=[]))
    assert draft['outcome']=='no_relevant_change' and not draft['findings']
    assert draft['support']==dict(t['receipt_template']['support'],reason=draft['summary'])
    g.accept(c,r,draft)


def test_new_navigation_source_is_explicit_baseline_and_accepts_only_model_decision(env):
    c,r,root=env
    acquire(env,'initial-navigation',page=b'Opinions\nJudges\nClerk office\n')
    q=g.write_queue(c,r,root/'sources')
    t=next(w.tasks(c,{'run_dir':str(root/'run')},{'source_reviews':q,'opinion_reviews':{'tasks':[]}}))
    b=short.prepare(c,t)
    assert b['card']['source_context']['purpose']=='baseline'
    assert b['card']['source_context']['previous_text_available'] is False
    assert len(g.reviews(c,r['stream']))==0  # Context is not an automatic verdict.
    a=dict(decision='no_material_change',summary='The captured baseline contains navigation, without substantive information.',evidence=['C1'],people=[])
    rec=short.compile_answer(t,b,a)
    assert rec['outcome']=='baseline_reviewed' and not rec['findings']
    g.accept(c,r,rec)
    assert len(g.reviews(c,r['stream']))==1
    assert h.latest_finalized(c,r['stream']) is None


def test_changed_source_context_keeps_prior_evidence_and_comparison_outcome(env):
    c,r,_=env;t,b=changed_task(env)
    assert b['card']['source_context']['purpose']=='comparison'
    assert b['card']['source_context']['previous_text_available'] is True
    assert {'current','previous'}=={e['side'] for e in b['card']['evidence']}
    rec=short.compile_answer(t,b,dict(decision='no_material_change',summary='Source difference reviewed; no material finding.',evidence=['C1','P1'],people=[]))
    assert rec['outcome']=='no_relevant_change'


def test_notice_role_is_exact_configuration_not_hostname_or_completeness_inference(env):
    c,_,_=env;t,_=changed_task(env)
    from flwu.opinion_discovery import COURTS
    court=next(court for court in COURTS if court.get('notice_urls'))
    t['inputs']['observation']['url']=court['notice_urls'][0]
    b=short.prepare(c,t)
    assert b['card']['source_context']['role']=='configured_opinion_notice_page'
    assert b['card']['source_context']['court']==court['id']
    assert not b['exception'] and b['card']['evidence']
    assert short.compile_answer(t,b,dict(decision='insufficient_evidence',summary='Expected notice body is unavailable.',evidence=[],people=[])) is None
    t['inputs']['observation']['url'] += '/unconfigured-page'
    assert 'role' not in short.prepare(c,t)['card']['source_context']
    t['inputs']['observation'].pop('text_sha256')
    b=short.prepare(c,t)
    assert b['exception'] and 'evidence' not in b['card']


@pytest.mark.parametrize('mutation,match',[
    (lambda a:a.update(evidence=['fake']), 'supplied'),
    (lambda a:a.update(sha256='made-up'), 'template fields'),
    (lambda a:a.update(decision='baseline_reviewed'), 'Invalid source decision'),
    (lambda a:a['people'][0]['fields']['office_phone'].update(value='(999) 999-9999'), 'Field value'),
    (lambda a:a['people'][0].update(name='Unsupported Person'), 'identity evidence'),
])
def test_unsupported_answers_fail_closed(env,mutation,match):
    c,_,_=env;t,b=changed_task(env);a=person_answer(b);mutation(a)
    with pytest.raises(ValueError,match=match):short.compile_answer(t,b,a)


def test_existing_person_preserves_nested_facts_and_successor_is_distinct(env):
    c,r,_=env;t,b=changed_task(env)
    old_cite=b['bindings']['C1']
    old=dict(key='person-warburton',kind='clerk',expected_version=None,
             facts=dict(name='Kristopher Warburton',fields={'office_address':dict(value='Prior address',status='verified',citation=old_cite)},
                        procedure={'documents':[{'url':'https://court.gov/civil','detail':{'untouched':True}}]}),citations=[old_cite])
    t['inputs']['prior_findings']=[old];b=short.prepare(c,t);a=person_answer(b);a['people'][0]['person']='person1'
    draft=short.compile_answer(t,b,a);f=draft['findings'][0]
    assert f['key']==old['key'] and f['expected_version']==old['expected_version']
    assert f['facts']['procedure']==old['facts']['procedure']
    assert f['facts']['fields']['office_address']==old['facts']['fields']['office_address']
    # Changing an existing identity is not a personnel update to the same person.
    b['prior_people']['person1']['facts']['name']='Sandra Williams'
    with pytest.raises(ValueError,match='successor'):short.compile_answer(t,b,a)


def test_raw_uncertainty_has_no_legal_verdict_or_group_narratives(env):
    c,_,_=env;t,b=changed_task(env)
    t['receipt_template']['raw_change_review']={'comparison_sha256':'code-owned'}
    b=short.prepare(c,t)
    assert b['exception'] and 'technical' in b['card']['question'].lower()
    assert 'evidence' not in b['card'] and 'raw_change_review' not in b['card']
    with pytest.raises(ValueError,match='Changed originals'):short.compile_answer(t,b,person_answer(short.prepare(c,{**t,'receipt_template':{k:v for k,v in t['receipt_template'].items() if k!='raw_change_review'}})))


def test_oversized_card_is_explicit_exception_not_silent_truncation(env,monkeypatch):
    c,_,_=env;t,b=changed_task(env);monkeypatch.setattr(short,'MAX_EVIDENCE_CHARACTERS',20)
    b=short.prepare(c,t)
    assert b['exception'] and 'limit' in b['card']['reason']
    assert 'evidence' not in b['card']


def test_standard_cli_produces_short_card_and_accepts_short_answer(tmp_path,capsys):
    from flwu.cli import main
    run,db,_,_=environment(tmp_path)
    assert main(['workflow','next-task','--run-dir',str(run)])==0
    state=json.loads(capsys.readouterr().out)
    assert state['review_mode']=='short_answer' and 'review_card' in state
    assert not set(state)&{'review_guide','full_review_guide','receipt_template','save_receipt','answer_binding'}
    card=w.read(state['review_card']);assert 'receipt_schema' not in json.dumps(card)
    answer=dict(decision='no_material_change',summary='The acquired profile contains operating information; no material change is established.',evidence=['C1'],people=[])
    w.write(state['save_answer'],answer)
    assert main(['workflow','answer','--run-dir',str(run),'--packet',state['packet'],'--answer',state['save_answer'],'--advance'])==0
    nxt=json.loads(capsys.readouterr().out);assert nxt['phase'] in ('source_review','opinion_review')
    with h.database(db) as c:assert len(g.reviews(c,'weekly'))==1


def test_uncertainty_persists_and_other_reviews_continue_without_finalizing(tmp_path):
    run,db,_,_=environment(tmp_path)
    first=w.inspect(run,emit=True);w.write(first['save_answer'],dict(decision='insufficient_evidence',summary='Cannot establish the profile assignment from the acquired text.',evidence=[],people=[]))
    current=runner.answer(run,first['packet'],first['save_answer'],advance=True)
    assert current['phase'] in ('source_review','opinion_review') and current['packet']!=first['packet'] and not current['complete']
    for _ in range(24):
        if current['phase'] not in ('source_review','opinion_review'):break
        value=(dict(decision='no_material_change',summary='No material change established in this fixture baseline.',evidence=['C1'],people=[]) if current['phase']=='source_review' else
               dict(relevance='relevant',summary='Fixture commercial holding.',holding='Commercial holding.',disposition='Affirmed.',authors=['Example'],evidence=['C1']))
        w.write(current['save_answer'],value)
        current=runner.answer(run,current['packet'],current['save_answer'],advance=True)
    assert current['phase']=='review_exceptions' and not current['complete']
    assert len(current['exceptions'])==1 and current['exceptions'][0]['category']=='model_uncertainty'
    with h.database(db) as c:
        pending_source=w.read(first['packet'])['identity']
        assert not any(r['source_id']==pending_source for r in g.reviews(c,'weekly'))
        assert h.latest_finalized(c,'weekly') is None
        n=c.execute('SELECT count(*) FROM captures').fetchone()[0]
    w.inspect(run);w.inspect(run)
    with h.database(db) as c:assert c.execute('SELECT count(*) FROM captures').fetchone()[0]==n
    with pytest.raises(ValueError):workflow_report.prepare(run)


def test_invalid_answer_checkpoint_then_real_repair_is_accepted(tmp_path):
    run,db,_,_=environment(tmp_path);state=w.inspect(run,emit=True)
    bad=dict(decision='no_material_change',summary='Incorrect supplied evidence reference.',evidence=['not-on-card'],people=[])
    w.write(state['save_answer'],bad)
    with pytest.raises(ValueError,match='Short answer rejected'):runner.answer(run,state['packet'],state['save_answer'],advance=True)
    nxt=runner.answer(run,state['packet'],state['save_answer'],advance=True)
    assert nxt['phase'] in ('source_review','opinion_review') and nxt['unresolved_checkpoint']
    assert nxt['review_progress']['checkpointed_reviews']==1
    assert nxt['review_progress']['failed_short_answers']==2
    assert nxt['answer_failure']['attempt']==2
    assert not set(nxt['answer_failure'])&{'answer','packet_sha256','projection_hashes'}
    assert 'Continue this returned task' in nxt['answer_failure']['next_action']
    with h.database(db) as c:
        assert not g.reviews(c,'weekly')
        assert len(runner.unresolved(c,w.load(run)))==1
    w.write(state['save_answer'],dict(decision='no_material_change',summary='Profile content screened; no supported material change.',evidence=['C1'],people=[]))
    runner.answer(run,state['packet'],state['save_answer'],advance=True)
    with h.database(db) as c:
        assert len(g.reviews(c,'weekly'))==1
        assert not runner.unresolved(c,w.load(run))
        assert sum(e['kind']=='answer_rejected' for e in w.events(c,w.load(run)))==2


def test_tampered_card_and_stale_packet_cannot_supply_evidence(tmp_path):
    run,db,_,_=environment(tmp_path);s=w.inspect(run,emit=True)
    w.write(s['save_answer'],dict(decision='no_material_change',summary='Reviewed.',evidence=['C1'],people=[]))
    Path(s['review_card']).write_text('{"fake":"evidence"}')
    with pytest.raises(ValueError,match='Immutable workflow artifact'):runner.answer(run,s['packet'],s['save_answer'])
    packet=w.read(s['packet']);packet['instructions']='changed';bad=Path(run)/'bad-packet.json';w.write(bad,packet)
    with pytest.raises(ValueError,match='stale or modified'):runner.answer(run,bad,s['save_answer'])
    with h.database(db) as c:assert not g.reviews(c,'weekly')


def test_committed_short_answer_replays_after_advance_failure(tmp_path,monkeypatch):
    run,db,_,_=environment(tmp_path);s=w.inspect(run,emit=True)
    w.write(s['save_answer'],dict(decision='no_material_change',summary='Screened current profile.',evidence=['C1'],people=[]))
    actual=w.inspect
    monkeypatch.setattr(w,'inspect',lambda *a,**k:(_ for _ in ()).throw(ValueError('projection interruption')))
    with pytest.raises(ValueError,match='submission is saved'):runner.answer(run,s['packet'],s['save_answer'],advance=True)
    monkeypatch.setattr(w,'inspect',actual)
    nxt=runner.answer(run,s['packet'],s['save_answer'],advance=True)
    assert nxt['phase'] in ('source_review','opinion_review')
    with h.database(db) as c:assert len(g.reviews(c,'weekly'))==1


@pytest.mark.parametrize('old,new', [('Civil rule.\nObsolete banner.\n','Civil rule.\n'), ('Civil rule.\n','Civil rule.\nNavigation banner.\n')])
def test_addition_or_deletion_keeps_both_acquired_contexts(env,old,new):
    c,r,_=env;t,b=changed_task(env,before=old,after=new)
    assert not b['exception']
    assert {'current','previous'} <= {e['side'] for e in b['card']['evidence']}
    draft=short.compile_answer(t,b,dict(decision='no_material_change',summary='A navigation banner changed; the civil rule text is unchanged.',evidence=['C1','P1'],people=[]))
    assert b['bindings']['P1']['retrieved_at'] != b['bindings']['C1']['retrieved_at']
    g.accept(c,r,draft)


def test_real_raw_change_is_durable_exception_and_not_an_automatic_review(tmp_path):
    from flwu import update
    before=b'<html><h1>Clerk office</h1><script>window.token="old";</script></html>'
    after=before.replace(b'"old"',b'"new"')
    run,db,registry,server=environment(tmp_path,profile=before)
    def fetch(raw):
        def call(url):
            meta,body=server(url)
            return dict(meta,content_type='text/html'),raw if url=='https://court.gov/profile' else body
        return call
    with h.database(db) as c:
        g.run(c,registry,'html-baseline',fetch=fetch(before))
        update.refresh(c,registry,'trial',run)
    first=w.inspect(run,emit=True)
    w.write(first['save_answer'],dict(decision='no_material_change',summary='The baseline states an office heading.',evidence=['C1'],people=[]))
    runner.answer(run,first['packet'],first['save_answer'])
    with h.database(db) as c:
        g.run(c,registry,'changed-script',fetch=fetch(after))
        update.refresh(c,registry,'trial',run)
    current=w.inspect(run,emit=True)
    assert current['identity']!=g.source_id('https://court.gov/profile')
    assert current['review_progress']['checkpointed_reviews']==1
    assert current['review_progress']['remaining_source_reviews']>1
    with h.database(db) as c:
        pending=runner.unresolved(c,w.load(run))
        assert len(pending)==1
        assert next(iter(pending.values()))['category']=='technical_or_extended_evidence'
        observations=g.observations(c,'weekly');latest=next(o for o in reversed(observations) if o['url']=='https://court.gov/profile')
        assert not any(r['observation_capture_id']==latest['capture_id'] for r in g.reviews(c,'weekly'))
        assert h.latest_finalized(c,'weekly') is None
    for _ in range(24):
        if current['phase'] not in ('source_review','opinion_review'):break
        value=(dict(decision='no_material_change',summary='Fixture source baseline reviewed.',evidence=['C1'],people=[]) if current['phase']=='source_review' else
               dict(relevance='not_relevant',summary='Fixture screening decision.',holding='',disposition='',authors=[],evidence=['C1']))
        w.write(current['save_answer'],value)
        current=runner.answer(run,current['packet'],current['save_answer'],advance=True)
    assert current['phase']=='review_exceptions' and not current['complete']
    exc=current['exceptions'][0];assert 'maintenance-task' in exc['maintenance_command']
    legacy=runner.maintenance(run,exc['packet'])
    assert legacy['review_mode']=='explicit_maintenance'
    assert 'raw_change_review' in w.read(legacy['receipt_template'])
    with pytest.raises(ValueError):workflow_report.prepare(run)


def test_source_compilation_never_uses_previous_phone_as_current(env):
    c,_,_=env;t,b=changed_task(env)
    a=person_answer(b);a['people'][0]['fields']['office_phone']=dict(value='555-0100',evidence='P1')
    with pytest.raises(ValueError,match='Current personnel fields'):short.compile_answer(t,b,a)


def test_malformed_json_is_counted_and_checkpointed_without_reset(tmp_path):
    run,db,_,_=environment(tmp_path);state=w.inspect(run,emit=True)
    Path(state['save_answer']).write_text('{broken json')
    with pytest.raises(ValueError,match='Short answer rejected'):runner.answer(run,state['packet'],state['save_answer'],advance=True)
    result=runner.answer(run,state['packet'],state['save_answer'],advance=True)
    assert result['unresolved_checkpoint'] and result['answer_failure']['attempt']==2
    assert result['packet']!=state['packet']
    with h.database(db) as c:
        failures=[e for e in w.events(c,w.load(run)) if e['kind']=='answer_rejected']
        assert len(failures)==2 and all('Expecting property name' in e['error'] for e in failures)
        digest=next(iter(failures[0]['projection_hashes'].values()))
        assert g.blob(c,digest)==b'{broken json'
        assert not g.reviews(c,'weekly')


def test_checked_helper_real_cli_from_outside_checkout(tmp_path, monkeypatch):
    import os,subprocess,sys
    # CI imports a normal wheel installation, whose __file__ is not a checkout.
    # The skill's contract pins an explicit checkout before launching its CLI.
    checkout = Path(__file__).resolve().parents[1]
    monkeypatch.setattr(w, 'ROOT', checkout)
    run,db,_,_=environment(tmp_path)
    helper=checkout/'skills/florida-update/scripts/review_step.py'
    prefix=[sys.executable,str(helper),'--checkout',str(checkout),'--python',sys.executable]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    w.write(run/'agent-next-task.json',dict(phase='source_review',complete=False,review_guide='obsolete-v7-pointer'))
    result=subprocess.run(prefix+['next','--run-dir',str(run)],cwd=tmp_path,capture_output=True,text=True,env=env)
    assert result.returncode==0,result.stderr
    state=json.loads(result.stdout)
    assert state['review_mode']=='inline_answer' and isinstance(state['review_card'],dict)
    assert 'receipt_template' not in state and 'review_guide' not in state
    value=dict(decision='no_material_change',summary='Fixture profile screened\u00a0for material changes.',evidence=['C1'],people=[])
    import shlex
    raw=(json.dumps(value,ensure_ascii=False)+'\n').encode()
    result=subprocess.run(shlex.split(state['command']),input=raw,cwd=tmp_path,capture_output=True,env=env)
    assert result.returncode==0,result.stderr
    next_state=json.loads(result.stdout)
    assert next_state['task_handle']!=state['task_handle'] and next_state['review_mode']=='inline_answer'
    attempts=[p for p in (run/'agent-steps').iterdir() if (p/'answer.json').exists()]
    assert len(attempts)==1 and (attempts[0]/'answer.json').read_bytes()==raw
    with h.database(db) as c:
        saved=g.reviews(c,'weekly');assert len(saved)==1
        assert saved[0]['summary']==value['summary']


def test_previous_bindings_are_pinned_before_current_observation_not_future_fetches(env):
    c,_,_=env;t,b=changed_task(env,before='Previous source.\n',after='Current source.\n')
    previous=b['bindings']['P1']['retrieved_at']
    acquire(env,'future-return-to-old-bytes',page=b'Previous source.\n')
    rebuilt=short.prepare(c,t)
    assert rebuilt==b
    assert rebuilt['bindings']['P1']['retrieved_at']==previous


def test_existing_person_patch_passes_real_version_guard_and_retains_other_contacts(env):
    c,r,root=env
    old='Judge Elise Grant\nPhone: (813) 555-0100\nAssistant: Dana Ellis\n'
    first,_=acquire(env,'initial-person',page=old.encode())
    for t in first['tasks']:
        rec=receipt(t,r,c)
        if t['source_id']==r['sources'][0]['id']:
            o=t['observation'];ci={k:o[k] for k in ('url','sha256','text_sha256','retrieved_at','http_status')};ci.update(quote=old,locator='Initial complete source')
            facts=dict(name='Elise Grant',fields={'chambers_phone':dict(value='(813) 555-0100',status='verified',citation=ci),'assistant_name':dict(value='Dana Ellis',status='verified',citation=ci)},procedure={'nested':{'unchanged':True}})
            rec.update(outcome='updated_findings',findings=[dict(key='person-elise-grant',kind='judge',facts=facts,citations=[ci],expected_version=None)])
        g.accept(c,r,rec)
    acquire(env,'phone-update',page=old.replace('555-0100','555-0142').encode())
    q=g.write_queue(c,r,root/'source-exports');t=next(w.tasks(c,{'run_dir':str(root/'run')},{'source_reviews':q,'opinion_reviews':{'tasks':[]}}));b=short.prepare(c,t)
    a=dict(decision='material_change',summary='Judge Grant now lists chambers phone (813) 555-0142.',evidence=['C1'],people=[dict(person='person1',name='Elise Grant',kind='judge',evidence=['C1'],fields={'chambers_phone':dict(value='(813) 555-0142',evidence='C1')})])
    compiled=short.compile_answer(t,b,a);person=compiled['findings'][0]
    assert person['facts']['fields']['assistant_name']['value']=='Dana Ellis'
    assert person['facts']['procedure']=={'nested':{'unchanged':True}}
    assert person['expected_version']
    g.accept(c,r,compiled)
    workflow_report.validate_records(c,{'registry':r},[{k:person[k] for k in ('key','kind','facts','citations')}])
    conflicting=copy.deepcopy(compiled);conflicting['summary']='Another stale change';conflicting['findings'][0]['expected_version']='stale'
    with pytest.raises(ValueError,match='changed since review'):g.accept(c,r,conflicting)


def test_new_person_identity_is_stable_across_whitespace_and_case(env):
    _,_,_=env;t,b=changed_task(env);a=person_answer(b)
    first=short.compile_answer(t,b,a)['findings'][0]
    a['people'][0]['name']='  KRISTOPHER\u00a0  WARBURTON  '
    second=short.compile_answer(t,b,a)['findings'][0]
    assert second['key']==first['key']
    assert second['facts']['name']=='KRISTOPHER WARBURTON'


def test_changed_visible_text_also_exposes_hidden_href_delta_and_verifies_url(env):
    c,r,root=env
    before=b'<h1>Judge Avery Stone</h1><p>Calendar Monday</p><a href="/old-guide.pdf">Civil procedures</a>'
    after=before.replace(b'Monday',b'Tuesday').replace(b'/old-guide.pdf',b'/new-guide.pdf')
    def fetch(body):
        return lambda url:(dict(url=url,resolved_url=url,retrieved_at=h.now(),success=True,http_status=200,content_type='text/html'),body)
    first=g.run(c,r,'links-before',fetch=fetch(before))
    for t in first['tasks']:g.accept(c,r,receipt(t,r,c))
    g.run(c,r,'links-after',fetch=fetch(after));q=g.write_queue(c,r,root/'exports')
    t=next(w.tasks(c,{'run_dir':str(root/'run')},{'source_reviews':q,'opinion_reviews':{'tasks':[]}}));b=short.prepare(c,t)
    assert not b['exception'] and 'raw_change_review' not in t['receipt_template']
    assert b['card']['link_changes']['current_only']==['https://court.gov/new-guide.pdf']
    assert b['card']['link_changes']['previous_only']==['https://court.gov/old-guide.pdf']
    assert b['card']['link_changes']['previous_inventory_known'] is True
    a=dict(decision='material_change',summary='The profile now links a different civil procedure guide; target content has not been reviewed.',evidence=['C1'],people=[dict(person='new',name='Avery Stone',kind='judge',evidence=['C1'],fields={'procedure_url':dict(value='https://court.gov/new-guide.pdf',evidence='C1')})])
    compiled=short.compile_answer(t,b,a);g.accept(c,r,compiled)
    assert compiled['findings'][0]['facts']['fields']['procedure_url']['value']=='https://court.gov/new-guide.pdf'
    a['people'][0]['fields']['procedure_url']['value']='https://court.gov/invented-guide.pdf'
    with pytest.raises(ValueError,match='Field value'):short.compile_answer(t,b,a)


def test_field_repair_names_bad_address_and_preserves_supported_phone(env):
    c,r,_=env
    address='300 South Beach Street\nDaytona Beach, FL 32114'
    t,b=changed_task(env,after='Kristopher Warburton is Clerk.\nPhone: (386) 947-1530\n'+address+'\n')
    a=person_answer(b)
    a['people'][0]['fields']['office_address']=dict(value=address.replace('\n',', '),evidence='C1')
    original=copy.deepcopy(a)
    with pytest.raises(ValueError) as error:short.compile_answer(t,b,a)
    assert 'Kristopher Warburton: fields.office_address:' in str(error.value)
    assert 'Field value must occur exactly' in str(error.value)
    assert 'retain other supported fields' in str(error.value)
    assert 'office_phone' not in str(error.value) and a==original
    a['people'][0]['fields']['office_address']['value']=address
    corrected=copy.deepcopy(a)
    compiled=short.compile_answer(t,b,a);g.accept(c,r,compiled)
    stored=next(review for review in g.reviews(c,r['stream']) if review['sha256']==compiled['sha256'])
    fields=stored['findings'][0]['facts']['fields']
    assert fields['office_phone']['value']=='(386) 947-1530'
    assert fields['office_address']['value']==address and a==corrected
    workflow_report.validate_records(c,{'registry':r},[{k:f[k] for k in ('key','kind','facts','citations')} for f in compiled['findings']])


@pytest.mark.parametrize('update,reason',[
    ({'value':'(386) 947-1530','evidence':'missing'},'supplied'),
    ({'value':'','evidence':'C1'},'nonempty'),
    ({'value':'(386) 947-1530'},'value and evidence'),
])
def test_all_personnel_field_errors_identify_the_person_and_field(env,update,reason):
    _,_,_=env;t,b=changed_task(env);a=person_answer(b)
    a['people'][0]['fields']['office_phone']=update
    with pytest.raises(ValueError) as error:short.compile_answer(t,b,a)
    assert 'Kristopher Warburton: fields.office_phone:' in str(error.value)
    assert reason in str(error.value)


def test_new_person_without_published_contacts_does_not_require_invention(env):
    c,r,_=env;t,b=changed_task(env,after='Kristopher Warburton was selected as Clerk on October 30, 2026.\n')
    a=person_answer(b);a['people'][0]['fields']={}
    compiled=short.compile_answer(t,b,a);g.accept(c,r,compiled)
    assert compiled['findings'][0]['facts']['fields']=={}
    assert 'even if unchanged' in b['card']['answer_help']['contacts']
    assert 'Never invent missing contacts' in b['card']['answer_help']['contacts']


def test_source_counts_partition_current_work_without_double_counting(monkeypatch):
    queue=dict(source_reviews=dict(tasks=[dict(source_id='pending',observation={'capture_id':'capture'})],
        reused_reviews=[dict(source_id='reviewed',sha256='current'),dict(source_id='reviewed',sha256='current'),
                        dict(source_id='machine',sha256='now'),dict(source_id='pending',sha256='old')]),
        opinion_reviews=dict(tasks=[]))
    def decision(kind,identity,digest):
        return dict(task=dict(kind=kind,identity=identity,inputs=dict(observation={'sha256':digest})))
    decisions={'a':decision('source_review','reviewed','current'),
               'duplicate':decision('source_review','reviewed','current'),
               'obsolete':decision('source_review','machine','old'),
               'opinion':decision('opinion_review','machine','now'),
               'unregistered':decision('source_review','not-in-current-queue','other')}
    monkeypatch.setattr(runner,'unresolved',lambda *_:{'packet':dict(task_kind='source_review',identity='pending',observation_capture_id='capture')})
    monkeypatch.setattr(w,'events',lambda *_:[])
    result=runner.progress(None,{},queue,decisions)
    assert {k:result[k] for k in ('total_sources','reviewed_sources','machine_reused_sources','pending_sources')}==dict(
        total_sources=3,reviewed_sources=1,machine_reused_sources=1,pending_sources=1)
    assert result['checkpointed_reviews']==1 and result['remaining_opinion_reviews']==0
