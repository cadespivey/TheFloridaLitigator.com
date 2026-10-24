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


@pytest.mark.parametrize('version', ['v20.20.2', 'v26.12.1', 'v24.22.1-rc.1', 'unknown'])
def test_old_or_unreviewed_runtime_blocked(version):
    with pytest.raises(SystemExit, match='Unsafe or unrecognized'):
        execute_guard(version)


def test_missing_runner_or_binary_blocks_actions():
    with pytest.raises(SystemExit, match='Cannot locate'):
        execute_guard('v24.22.1', missing_runner=True)
    with pytest.raises(FileNotFoundError):
        execute_guard('v24.22.1', missing_node=True)


@pytest.mark.parametrize('failure', [None, 'checksum', 'download', 'install', 'version', 'architecture'])
def test_old_runtime_patch_is_verified_and_fail_closed(tmp_path, failure):
    import hashlib
    import io
    import subprocess
    import tarfile
    real_path = Path
    runner = tmp_path / 'runner'
    node = runner / 'externals/node24/bin/node'
    node.parent.mkdir(parents=True)
    node.write_text('old')
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode='w:xz') as tf:
        member = tarfile.TarInfo('node-v24.22.1-linux-x64/bin/node')
        member.size = 7
        tf.addfile(member, io.BytesIO(b'patched'))
    content = archive.getvalue()
    expected = hashlib.sha256(content).hexdigest()
    code = guards()[0].split('\n', 1)[1].rsplit('\n', 1)[0]
    code = code.replace('6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6', expected)
    class ProcessPath:
        def __truediv__(self, other): return self
        def resolve(self, strict=False):
            return runner / 'bin/Runner.Worker'
    def path(value):
        return ProcessPath() if str(value) == '/proc' else real_path(value)
    installed = []
    def run(args, **kwargs):
        assert kwargs['check']
        if args[0] == 'curl':
            if failure == 'download': raise subprocess.CalledProcessError(22, args)
            real_path(args[args.index('--output')+1]).write_bytes(b'corrupt' if failure == 'checksum' else content)
        else:
            assert args[:5] == ['sudo', '-n', 'install', '-m', '755']
            assert real_path(args[5]).read_bytes() == b'patched'
            if failure == 'install': raise subprocess.CalledProcessError(1, args)
            node.write_text('patched')
            installed.append(True)
    def version(args, **kwargs):
        if str(args[0]) == str(node):
            return 'v24.22.1' if installed else 'v24.21.0'
        return 'v24.21.0' if failure == 'version' else 'v24.22.1'
    with patch('pathlib.Path', side_effect=path), patch('os.getpid', return_value=123), \
         patch('platform.system', return_value='Linux'), \
         patch('platform.machine', return_value='arm64' if failure == 'architecture' else 'x86_64'), \
         patch('subprocess.run', side_effect=run), patch('subprocess.check_output', side_effect=version):
        if failure:
            with pytest.raises((SystemExit, subprocess.CalledProcessError)):
                exec(compile(code, '<runtime patch>', 'exec'), {})
            assert not installed
        else:
            exec(compile(code, '<runtime patch>', 'exec'), {})
            assert installed == [True]
