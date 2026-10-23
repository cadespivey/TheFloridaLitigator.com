import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest
from flwu.acquisition import acquisition, progress
from flwu.cli import main


def test_cli_both_acquisitions_reject_busy_before_database_write(tmp_path, capsys):
    db = tmp_path/'research.sqlite'
    registry = tmp_path/'registry.json'
    registry.write_text(json.dumps({'schema_version': 1, 'stream': 'manual_research:test',
                                    'review_protocol': 'v1', 'sources': []}))
    with acquisition(db, 'owner', 'update'):
        for command in (['update'], ['source-gate', 'run']):
            result = main(command + ['--database', str(db), '--registry', str(registry),
                         '--run-id', 'contender', '--output', str(tmp_path/'out')])
            assert result == 1
            assert not db.exists()
            assert not (tmp_path/'out').exists()
    assert 'Acquisition already running' in capsys.readouterr().err


def test_lock_real_process_crash_and_symlink_alias(tmp_path):
    db = tmp_path/'research.sqlite'
    db.touch()
    alias = tmp_path/'alias.sqlite'
    alias.symlink_to(db)
    script = '''import sys,time
from flwu.acquisition import acquisition
with acquisition(sys.argv[1], 'child', 'update'):
 print('ready', flush=True)
 time.sleep(120)
'''
    proc = subprocess.Popen([sys.executable, '-c', script, str(db)],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    try:
        assert proc.stdout.readline().strip() == 'ready'
        with pytest.raises(ValueError, match='Acquisition already running'):
            with acquisition(alias, 'other', 'source-gate run'):
                pass
        proc.kill()  # disposable test child only: OS must release without cleanup
        proc.wait(timeout=5)
        with acquisition(alias, 'resumed', 'update'):
            pass
        assert Path(str(db)+'.acquisition.lock').exists()
    finally:
        if proc.poll() is None:
            proc.kill(); proc.wait(timeout=5)
        proc.stdout.close()


def test_progress_heartbeat_exception_release_and_distinct_databases(tmp_path, capsys):
    db = tmp_path/'a.sqlite'
    with pytest.raises(RuntimeError):
        with acquisition(db, 'first', 'update', heartbeat_seconds=.01):
            progress('opinion_listing', court='supreme', offset=0)
            time.sleep(.04)
            with acquisition(tmp_path/'b.sqlite', 'second', 'update'):
                pass
            raise RuntimeError('interrupted')
    with acquisition(db, 'resumed', 'update'):
        progress('source', index=1, total=2)
    captured = capsys.readouterr()
    assert captured.out == ''
    events = [json.loads(line) for line in captured.err.splitlines()]
    assert any(e['event'] == 'acquisition_heartbeat' and e['phase'] == 'opinion_listing' for e in events)
    assert any(e['phase'] == 'interrupted_or_failed' for e in events)
    assert events[-1]['phase'] == 'completed'
