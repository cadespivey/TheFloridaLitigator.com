import fcntl
import json
import subprocess

import pytest
from scripts import resume_hermes as handoff


@pytest.fixture
def saved_run(tmp_path):
    root = tmp_path / 'checkout with spaces'
    run = root / 'runs/updates/example'
    (run / 'workflow').mkdir(parents=True)
    (root / 'docs/workflow').mkdir(parents=True)
    (root / 'docs/workflow/HERMES_HANDOFF.md').write_text('Preserve the saved evidence.\n')
    (run / 'RESUME.md').write_text('Next task is pending.\n')
    (run / 'agent-next-task.json').write_text('{}')
    db = tmp_path / 'existing.sqlite'
    db.write_bytes(b'existing database sentinel')
    contract = dict(checkout=str(root), run_dir=str(run), database=str(db), end='2026-11-08')
    (run / 'workflow/contract.json').write_text(json.dumps(contract))
    return root, run, db


def test_prepare_preserves_inputs_and_rejects_wrong_checkout_or_missing_database(saved_run):
    root, run, db = saved_run
    before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
    resolved, prompt = handoff.prepare(run, root)
    assert resolved == run and str(run) in prompt and str(db) in prompt
    assert before == {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
    contract_path = run / 'workflow/contract.json'
    contract = json.loads(contract_path.read_text())
    contract['checkout'] = str(root.parent / 'wrong')
    contract_path.write_text(json.dumps(contract))
    with pytest.raises(ValueError, match='different checkout'):
        handoff.prepare(run, root)
    contract['checkout'] = str(root)
    contract['database'] = str(root / 'missing.sqlite')
    contract_path.write_text(json.dumps(contract))
    with pytest.raises(ValueError, match='database is missing'):
        handoff.prepare(run, root)
    assert not (root / 'missing.sqlite').exists()


def test_active_lock_refuses_handoff_but_stale_lock_file_is_allowed(saved_run):
    root, run, _ = saved_run
    for name in ('coordinator.lock', 'inline-reply.lock'):
        with (run / 'workflow' / name).open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with pytest.raises(ValueError, match='command is active'):
                handoff.prepare(run, root)
        handoff.prepare(run, root)


def test_check_is_nonmutating_and_interactive_launch_uses_only_selected_profile(saved_run, monkeypatch):
    root, run, db = saved_run
    monkeypatch.setattr(handoff, 'ROOT', root)
    monkeypatch.setattr(handoff.shutil, 'which', lambda _: '/tools/hermes')
    calls = []

    def execute(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, '--query-file PATH --in DIR', '')

    monkeypatch.setattr(handoff.subprocess, 'run', execute)
    assert handoff.main(['--run-dir', str(run), '--check']) == 0
    assert not (run / 'hermes-resume-prompt.md').exists()
    assert len(calls) == 2 and calls[0][:3] == ['/tools/hermes', '-p', 'personal-code']
    assert '--help' in calls[0] and '--check' in calls[1]
    monkeypatch.setattr(handoff.sys.stdin, 'isatty', lambda: False)
    assert handoff.main(['--run-dir', str(run)]) == 1
    assert not (run / 'hermes-resume-prompt.md').exists()
    monkeypatch.setattr(handoff.sys.stdin, 'isatty', lambda: True)
    monkeypatch.setattr(handoff.sys.stdout, 'isatty', lambda: True)
    assert handoff.main(['--run-dir', str(run)]) == 0
    assert calls[-1] == ['/tools/hermes', '-p', 'personal-code', 'chat', '--in', str(root),
                         '--query-file', str(run / 'hermes-resume-prompt.md')]
    assert 'Preserve the saved evidence.' in (run / 'hermes-resume-prompt.md').read_text()
    assert db.read_bytes() == b'existing database sentinel'
