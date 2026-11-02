"""A checkout move preserves research identity and never launches acquisition."""
import copy
import fcntl
import json
from pathlib import Path

import pytest

from flwu import history as h, workflow as w, source_gate as g
from flwu import workflow_relocation as relocation
from tests.test_workflow import environment, answer


def moved_environment(tmp_path, monkeypatch, *, finish_one=True, machine_supplement=False):
    old = tmp_path/'before'
    old.mkdir()
    monkeypatch.setattr(w, 'ROOT', old)
    # The database remains external to the moved checkout, just as in production.
    original_environment = old/'environment'
    original_environment.mkdir()
    run, database, registry, server = environment(original_environment)
    external = tmp_path/'external.sqlite'
    # No history connection is open; use the SQLite backup API to pin a fixture
    # with an external DB before exercising the actual relocation command.
    import sqlite3
    with sqlite3.connect(database) as source, sqlite3.connect(external) as target:
        source.backup(target)
    config = w.read(run/'workflow/contract.json')
    config['database'] = str(external)
    with h.database(external) as conn:
        w.record(conn, config, dict(kind='initialized', config=config))
    w.write(run/'workflow/contract.json', config)
    if finish_one:
        for _ in range(32):
            task = w.inspect(run, emit=True)
            if task['kind'] != 'source_review':
                break
            answer(run, external, task)
        assert task['kind'] == 'opinion_review'
    if machine_supplement:
        from tests.test_supplemental_coverage import supplement
        supplement(external,registry)
    next_task = w.inspect(run, emit=True)
    before = snapshot(external, config)
    original = (run/'workflow/contract.json').read_bytes()
    accepted = {str(p.relative_to(run)): p.read_bytes()
                for p in (run/'workflow/accepted').glob('*.json')}
    new = tmp_path/'after'
    old.rename(new)
    monkeypatch.setattr(w, 'ROOT', new)
    return new/'environment/run', external, config, original, accepted, before, next_task, server


def snapshot(db, config):
    with h.database(db) as conn:
        return dict(domain=[tuple(r) for r in conn.execute(
            "SELECT capture_id,payload FROM captures WHERE stream NOT LIKE 'workflow:%' ORDER BY seq")
            if json.loads(r['payload']).get('opinion_discovery',{}).get('checkpoint') != 'update-result'],
            baseline=h.latest_finalized(conn, config['registry']['stream']))


def test_move_preserves_accepted_evidence_and_resumes_pending_opinion(tmp_path, monkeypatch):
    run, db, previous, original, accepted, before, task, server = moved_environment(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match='relocated'):
        w.load(run)
    # Prove continuation cannot perform network retrieval even if called in error.
    monkeypatch.setattr(g, 'retrieve', lambda *_: pytest.fail('Relocation fetched a source'))
    monkeypatch.setattr(w.update, 'run', lambda *_args, **_kwargs: pytest.fail('Relocation restarted acquisition'))
    result = relocation.relocate(run, 'User moved checkout')
    assert result['run_id'] == previous['run_id'] and not result['acquisition_repeated']
    current = w.load(run)
    assert {k:v for k,v in current.items() if k not in ('run_dir','checkout','relocated_from')} == {
        k:v for k,v in previous.items() if k not in ('run_dir','checkout')}
    preserved = run/'workflow/relocations'/h.sha(previous)/'contract.json'
    assert preserved.read_bytes() == original
    assert {str(p.relative_to(run)):p.read_bytes() for p in (run/'workflow/accepted').glob('*.json')} == accepted
    next_task = w.inspect(run, emit=True)
    assert next_task['kind'] == task['kind'] == 'opinion_review'
    assert next_task['identity'] == task['identity']
    assert str(run) in next_task['packet']
    assert snapshot(db,current) == before
    assert relocation.relocate(run,'Retry after resumption')['replayed']
    assert snapshot(db,current) == before
    with h.database(db) as conn:
        old_events = w.events(conn,previous)
        assert old_events[-1]['kind'] == 'relocation_committed'
        assert len(w.events(conn,current)) == 1
    # The newly materialized pending task is actually submittable after rebinding.
    answer(run,db,next_task)


@pytest.mark.parametrize('fail_at', ['new_initialization','contract_projection'])
def test_interrupted_relocation_recovers_without_new_run_or_review(tmp_path,monkeypatch,fail_at):
    run,db,previous,original,accepted,before,_,_=moved_environment(tmp_path,monkeypatch)
    real_record=w.record; real_project=relocation._project
    def interrupted_record(conn,config,event):
        if fail_at=='new_initialization' and config.get('relocated_from'):
            raise OSError('fixture interruption')
        return real_record(conn,config,event)
    def interrupted_project(*args):
        raise OSError('fixture interruption')
    monkeypatch.setattr(w,'record',interrupted_record)
    if fail_at=='contract_projection':monkeypatch.setattr(relocation,'_project',interrupted_project)
    with pytest.raises(OSError,match='fixture interruption'):
        relocation.relocate(run,'Initial recovery attempt')
    assert (run/'workflow/contract.json').read_bytes()==original
    monkeypatch.setattr(w,'record',real_record);monkeypatch.setattr(relocation,'_project',real_project)
    result=relocation.relocate(run,'Retry must reuse the original saved reason')
    assert result['replayed']
    current=w.load(run)
    assert current['relocated_from']['reason']=='Initial recovery attempt'
    assert snapshot(db,current)==before
    with h.database(db) as conn:
        assert len([e for e in w.events(conn,previous) if e['kind']=='relocation_committed'])==1
        assert len(w.events(conn,current))==1


@pytest.mark.parametrize('damage', ['contract','pending_submission','downstream','coverage'])
def test_refuses_unsafe_relocation_without_mutation(tmp_path,monkeypatch,damage):
    run,db,config,original,_,before,task,_=moved_environment(tmp_path,monkeypatch,finish_one=False)
    if damage=='contract':
        corrupt=copy.deepcopy(config);corrupt['end']='2026-10-23';w.write(run/'workflow/contract.json',corrupt)
    else:
        with h.database(db) as conn:
            if damage=='pending_submission':
                packet=json.loads((run/Path(task['packet']).relative_to(config['run_dir'])).read_text())
                w.record(conn,config,dict(kind='submission',task=packet,receipt={}))
            elif damage=='downstream':
                w.record(conn,config,dict(kind='report_prepared'))
            else:
                w.record(conn,config,dict(kind='decision',task=dict(kind='coverage_review'),packet_sha256='fixture',receipt=dict(decision='unavailable')))
    raw=(run/'workflow/contract.json').read_bytes()
    with h.database(db) as conn:count=conn.execute('SELECT count(*) FROM captures').fetchone()[0]
    with pytest.raises(ValueError):relocation.relocate(run,'Do not bypass required work')
    assert (run/'workflow/contract.json').read_bytes()==raw
    with h.database(db) as conn:assert conn.execute('SELECT count(*) FROM captures').fetchone()[0]==count
    assert snapshot(db,config)==before


def test_refuses_active_coordinator_or_acquisition(tmp_path,monkeypatch):
    run,db,config,*_=moved_environment(tmp_path,monkeypatch)
    for path in (run/'workflow/coordinator.lock',Path(str(db)+'.acquisition.lock')):
        with path.open('a+') as handle:
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with pytest.raises(ValueError,match='active|already running'):
                relocation.relocate(run,'Wait for the real command')
            fcntl.flock(handle,fcntl.LOCK_UN)
    assert w.read(run/'workflow/contract.json')==config


def test_preserved_contract_tampering_blocks_resumption(tmp_path,monkeypatch):
    run,db,previous,*_=moved_environment(tmp_path,monkeypatch)
    relocation.relocate(run,'Moved checkout')
    (run/'workflow/relocations'/h.sha(previous)/'contract.json').write_text('{}')
    with pytest.raises(ValueError,match='checksum'):w.load(run)


def test_original_binding_is_frozen_after_relocation(tmp_path,monkeypatch):
    run,db,previous,original,*_=moved_environment(tmp_path,monkeypatch)
    relocation.relocate(run,'Moved checkout')
    old=Path(previous['run_dir']);old.mkdir(parents=True)
    (old/'workflow').mkdir();(old/'workflow/contract.json').write_bytes(original)
    monkeypatch.setattr(w,'ROOT',Path(previous['checkout']))
    with pytest.raises(ValueError,match='Workflow relocated; use its new binding'):
        w.load(old)


def test_no_relocation_of_a_copy_or_without_reason(tmp_path,monkeypatch):
    run,db,previous,*_=moved_environment(tmp_path,monkeypatch)
    with pytest.raises(ValueError,match='reason'):relocation.relocate(run,' ')
    old=Path(previous['run_dir']);old.mkdir(parents=True)
    with pytest.raises(ValueError,match='still exists'):relocation.relocate(run,'Copied, not moved')


def test_rebases_only_declared_publication_paths(tmp_path,monkeypatch):
    old=tmp_path/'before';old.mkdir();monkeypatch.setattr(w,'ROOT',old)
    db=tmp_path/'external.sqlite';run=old/'runs/research'
    registry=dict(schema_version=1,stream='weekly',review_protocol=g.PROTOCOL,
                  sources=[dict(id=g.source_id('https://court.gov/profile'),url='https://court.gov/profile')])
    path=old/'registry.json';w.write(path,registry)
    directory=old/'website/county-directories/example.json';w.write(directory,{'unchanged':'fixture'})
    archive=old/'website/updates'
    with h.database(db) as conn:
        h.record(conn,stream='weekly',mode='manual_research',scope={'profile':'test'},run_id='initial',
                 payload=dict(status='incomplete',contract={},checks=[],findings=[],drafts=[]),artifacts={})
    w.initialize(run,db,path,'same-id',start='2026-10-15',end='2026-10-22',mode='publish',directories=[directory],archive=archive)
    from tests.test_opinion_discovery import Server,opinion
    with h.database(db) as conn:
        w.update.run(conn,registry,'same-id',run,start='2026-10-15',end='2026-10-22',fetch=Server([opinion()]))
    previous=w.load(run);new=tmp_path/'after';old.rename(new);monkeypatch.setattr(w,'ROOT',new)
    moved=new/'runs/research';relocation.relocate(moved,'User moved project')
    current=w.load(moved)
    assert current['archive']==str(new/'website/updates')
    assert current['directories']==[str(new/'website/county-directories/example.json')]
    assert current['database']==str(db) and current['registry']==previous['registry']
    assert w.read(current['directories'][0])=={'unchanged':'fixture'}


def test_unchanged_machine_packet_keeps_original_and_new_binding_files(tmp_path,monkeypatch):
    run,db,previous,_,accepted,before,_,_=moved_environment(tmp_path,monkeypatch,machine_supplement=True)
    with h.database(db) as conn:
        old=next(e for e in w.events(conn,previous) if e.get('reuse',{}).get('policy')=='reviewed_supplement')
    old_packet=run/Path(old['task']['packet_path']).relative_to(previous['run_dir'])
    original_bytes=old_packet.read_bytes()
    relocation.relocate(run,'Keep exact prior machine coverage files')
    assert w.inspect(run,emit=True)['kind']=='opinion_review'
    current=w.load(run)
    with h.database(db) as conn:
        new=next(e for e in w.events(conn,current) if e.get('reuse',{}).get('policy')=='reviewed_supplement')
    assert new['packet_sha256']==old['packet_sha256']
    assert new['task']['packet_path']!=old['task']['packet_path']
    assert '/bindings/' in new['task']['packet_path']
    assert Path(new['task']['packet_path']).is_file()
    assert old_packet.read_bytes()==original_bytes
    assert (w.projection_folder(current,'accepted')/(new['packet_sha256']+'.json')).is_file()
    for name,raw in accepted.items():assert (run/name).read_bytes()==raw
    assert snapshot(db,current)==before
