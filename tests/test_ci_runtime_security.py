"""Exercise the inline pre-checkout guard without installing or invoking Node."""
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest


def guards():
    return [job['steps'][0]['run'] for file in Path('.github/workflows').glob('*.yml')
            for job in json.loads(file.read_text())['jobs'].values()]


def execute_guard(version, *, missing_runner=False, missing_node=False):
    scripts = guards()
    assert len(scripts) == 3 and len(set(scripts)) == 1
    code = scripts[0].split('\n', 1)[1].rsplit('\n', 1)[0]
    class FakePath:
        def __init__(self, value): self.value = str(value)
        def __truediv__(self, other): return FakePath(self.value+'/'+str(other))
        def resolve(self, strict=False):
            return SimpleNamespace(name='python3' if missing_runner else 'Runner.Worker',
                                   parent=SimpleNamespace(parent=FakePath('/runner')))
        def read_text(self): return 'PPid:\t1\n'
        def __str__(self): return self.value
    def version_call(args, **kwargs):
        assert args == ['/runner/externals/node24/bin/node', '--version']
        if missing_node: raise FileNotFoundError('node absent')
        return version+'\n'
    with patch('pathlib.Path', FakePath), patch('os.getpid', return_value=123), \
         patch('subprocess.check_output', side_effect=version_call):
        exec(compile(code, '<runtime guard>', 'exec'), {})


@pytest.mark.parametrize('version', ['v24.22.1', 'v24.23.0'])
def test_patched_bundled_runtime_allowed(version):
    execute_guard(version)


@pytest.mark.parametrize('version', ['v24.22.0', 'v24.0.0', 'v20.20.2', 'v26.12.1', 'v24.22.1-rc.1', 'unknown'])
def test_old_or_unreviewed_runtime_blocked(version):
    with pytest.raises(SystemExit, match='Unsafe or unrecognized'):
        execute_guard(version)


def test_missing_runner_or_binary_blocks_actions():
    with pytest.raises(SystemExit, match='Cannot locate'):
        execute_guard('v24.22.1', missing_runner=True)
    with pytest.raises(FileNotFoundError):
        execute_guard('v24.22.1', missing_node=True)
