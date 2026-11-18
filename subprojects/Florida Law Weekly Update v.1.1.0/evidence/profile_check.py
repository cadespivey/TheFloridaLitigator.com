"""Inspect actual Codex skill discovery and issue one harmless local fixture card per profile."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from tests.test_workflow import environment


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discovered(argv, env, checkout):
    messages = [
        dict(id=1, method='initialize', params=dict(clientInfo=dict(name='flwu-check', title='FLWU check', version='1.1.0'),
                                                    capabilities={})),
        dict(method='initialized'),
        dict(id=2, method='skills/list', params=dict(cwds=[str(checkout)], forceReload=True))]
    with TemporaryDirectory() as scratch:
        stderr_path = Path(scratch)/'stderr'
        with stderr_path.open('w') as stderr:
            proc = subprocess.Popen(argv, env=env, cwd=checkout, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=stderr, text=True)
            try:
                for request in messages:
                    proc.stdin.write(json.dumps(request)+'\n')
                    proc.stdin.flush()
                    if 'id' in request:
                        for line in proc.stdout:
                            response = json.loads(line)
                            if response.get('id') == request['id']:
                                if 'error' in response:
                                    raise ValueError(response['error'])
                                break
                        else:
                            raise RuntimeError('app-server closed before its response')
                groups = response['result']['data']
                matches = [skill for group in groups for skill in group['skills'] if skill['name']=='florida-update']
                assert len(matches) == 1
                errors = [entry for group in groups for entry in group.get('errors',[]) if 'florida-update' in str(entry)]
            finally:
                proc.stdin.close()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.terminate()
                    proc.wait(timeout=5)
        warnings = [line for line in stderr_path.read_text().splitlines()
                    if 'deprecat' in line.lower() or ('florida-update' in line and 'error' in line.lower())]
    return matches[0], errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--profiles', type=Path, required=True)
    parser.add_argument('--canonical', type=Path, required=True)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--require-candidate', action='store_true')
    args = parser.parse_args()
    sys.path.insert(0, str(args.profiles))
    from launch import prepare
    source = args.checkout/'skills/florida-update'
    relative = sorted(path.relative_to(source) for path in source.rglob('*') if path.is_file()
                      and '__pycache__' not in path.parts and path.name != 'installation.json')
    results = {}
    for profile in ('cloud','personal','local'):
        argv, env = prepare(profile, ['app-server'], os.environ)
        skill, errors, warnings = discovered(argv, env, args.checkout)
        manifest = Path(skill['path'])
        installed = (args.profiles/profile/'skills/florida-update').resolve(strict=True)
        assert manifest.resolve(strict=True) == args.canonical/'SKILL.md' and installed == args.canonical
        assert skill['enabled'] and not errors
        matches = {str(path): (installed/path).is_file() and sha(source/path)==sha(installed/path) for path in relative}
        script = installed/'scripts/flwu.py'
        check = json.loads(subprocess.check_output([sys.executable, str(script), '--check'], env=env))
        assert check['checkout'] == str(args.checkout) and check['python'] == sys.executable
        with TemporaryDirectory() as temp:
            run, _, _, _ = environment(Path(temp))
            state = json.loads(subprocess.check_output([sys.executable, str(script), 'workflow','model-next','--run-dir',str(run)], env=env))
            assert state['phase'] == 'source_review' and state.get('task_handle') and state.get('scope')
        results[profile] = dict(name=skill['name'], description=skill['description'], enabled=skill['enabled'],
                                discovered=str(manifest), canonical=str(installed), skill_sha256=sha(manifest),
                                candidate_file_matches=matches, launcher=check, fixture_phase=state['phase'],
                                discovery_warnings=warnings)
    args.output.write_text(json.dumps(results, indent=2)+'\n')
    if args.require_candidate:
        assert all(all(profile['candidate_file_matches'].values()) and
                   profile['launcher'].get('workflow_protocol_versions') == [1,2] for profile in results.values())
    print({key:(val['fixture_phase'],all(val['candidate_file_matches'].values())) for key,val in results.items()})


if __name__ == '__main__':
    main()
