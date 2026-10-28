#!/usr/bin/env python3
"""Run the current FLWU checkout without relying on an editable install or cwd."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

PROJECT = Path('/Users/cadespivey/florida-litigator-weekly-update')
BUNDLED_CHECKOUT = Path(__file__).resolve().parents[3]
DEFAULT_CHECKOUT = (BUNDLED_CHECKOUT if (BUNDLED_CHECKOUT / 'src/flwu/workflow.py').is_file()
                    else None)
INSTALL_CONFIG = Path(__file__).resolve().parents[1] / 'installation.json'
PYTHON = PROJECT / '.venv/bin/python'
REQUIRED = ('src/flwu/workflow.py', 'src/flwu/update.py', 'src/flwu/source_gate.py',
            'src/flwu/opinion_discovery.py', 'docs/workflow/MODEL_EXECUTION.md')


def main(argv=None):
    installation=json.loads(INSTALL_CONFIG.read_text()) if INSTALL_CONFIG.is_file() else {}
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--checkout', type=Path, default=installation.get('checkout') or DEFAULT_CHECKOUT)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--python',type=Path,default=installation.get('python') or PYTHON)
    args, command = parser.parse_known_args(argv)
    if args.checkout is None:
        print('No FLWU checkout configured. Run the repository skill installer or pass --checkout PATH.',file=sys.stderr)
        return 1
    checkout = args.checkout.expanduser().resolve()
    python=args.python.expanduser().absolute()
    missing = [name for name in REQUIRED if not (checkout / name).is_file()]
    if missing or not python.is_file():
        print('FLWU checkout preflight failed: ' + str(checkout), file=sys.stderr)
        print('Missing: ' + ', '.join(missing or [str(python)]), file=sys.stderr)
        print('Use --checkout PATH for a current checkout; do not reinstall or replace dirty files.', file=sys.stderr)
        return 1
    origin = subprocess.run(['git', '-C', str(checkout), 'remote', 'get-url', 'origin'],
                            capture_output=True, text=True)
    remote = origin.stdout.strip().removesuffix('.git').rstrip('/')
    if origin.returncode or not any(remote.endswith(suffix) for suffix in (
            'cadespivey/TheFloridaLitigator.com', 'cadespivey/Florida-Law-Weekly-Update')):
        print('FLWU checkout has an unexpected or missing origin.', file=sys.stderr)
        return 1
    env = dict(os.environ, PYTHONPATH=str(checkout / 'src'), PYTHONDONTWRITEBYTECODE='1')
    # Verify actual imports, not merely the presence of files or executable name.
    probe = '''import json, pathlib, flwu.cli, flwu.update, flwu.source_gate, flwu.opinion_discovery, flwu.workflow
print(json.dumps({"cli": str(pathlib.Path(flwu.cli.__file__).resolve()), "update": str(pathlib.Path(flwu.update.__file__).resolve()), "workflow": str(pathlib.Path(flwu.workflow.__file__).resolve())}))'''
    result = subprocess.run([str(python), '-c', probe], cwd=checkout, env=env,
                            capture_output=True, text=True)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        return result.returncode
    paths = json.loads(result.stdout)
    if any(not Path(value).is_relative_to(checkout / 'src') for value in paths.values()):
        print('FLWU imports escaped the selected checkout.', file=sys.stderr)
        return 1
    for entry in ('update','workflow','prepare-report','refresh-directory'):
        help_result = subprocess.run([str(python), '-m', 'flwu', entry, '--help'],
                                    cwd=checkout, env=env, capture_output=True, text=True)
        if help_result.returncode:
            print(help_result.stderr, file=sys.stderr)
            return help_result.returncode
    if args.check:
        print(json.dumps({'checkout': str(checkout), 'python': str(python),
                          'imports': paths, 'update_command_verified': True,
                          'workflow_commands_verified': True}, indent=2))
        return 0
    return subprocess.run([str(python), '-c',
        'from flwu.cli import main; raise SystemExit(main())', *(command or ['--help'])],
        cwd=checkout, env=env).returncode


if __name__ == '__main__':
    raise SystemExit(main())
