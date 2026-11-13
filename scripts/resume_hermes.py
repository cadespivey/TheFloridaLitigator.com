#!/usr/bin/env python3
"""Resume a saved FLWU run in Hermes; never initialize or acquire a run."""
import argparse
from contextlib import ExitStack
import fcntl
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def prepare(run, root=ROOT):
    run = run.expanduser().resolve()
    for path in (run / 'workflow/contract.json', run / 'RESUME.md',
                 run / 'agent-next-task.json', root / 'docs/workflow/HERMES_HANDOFF.md'):
        if not path.is_file():
            raise ValueError(f'Missing saved handoff input: {path}')
    contract = json.loads((run / 'workflow/contract.json').read_text())
    if Path(contract['checkout']).resolve() != root.resolve():
        raise ValueError('Saved run belongs to a different checkout; do not reinitialize it.')
    if Path(contract['run_dir']).resolve() != run:
        raise ValueError('Saved run directory differs from its contract.')
    if not Path(contract['database']).is_file():
        raise ValueError('The existing research database is missing; do not create a replacement.')
    # These are existing workflow locks. Their mere presence does not mean busy.
    with ExitStack() as stack:
        for name in ('coordinator.lock', 'inline-reply.lock'):
            path = run / 'workflow' / name
            if path.exists():
                handle = stack.enter_context(path.open('r'))
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as error:
                    raise ValueError('A workflow command is active. Wait for it; do not restart.') from error
    prompt = (
        'Resume the existing Florida Litigator weekly update under this Hermes profile.\n'
        f'Checkout: {root}\nRun directory: {run}\n'
        f'Database: {contract["database"]}\nCutoff: {contract["end"]}\n\n'
        + (root / 'docs/workflow/HERMES_HANDOFF.md').read_text()
        + '\n\nRead this current checkpoint before acting:\n' + str(run / 'RESUME.md') + '\n'
    )
    return run, prompt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, default=ROOT / 'runs/updates/weekly-2026-11-08')
    parser.add_argument('--profile', default='personal-code')
    parser.add_argument('--check', action='store_true', help='Validate paths and CLI only; do not launch an agent.')
    args = parser.parse_args(argv)
    try:
        run, prompt = prepare(args.run_dir, ROOT)
        hermes = shutil.which('hermes')
        if not hermes:
            raise ValueError('Hermes is not on PATH.')
        # Profile resolution and supported flags are checked without starting inference.
        result = subprocess.run([hermes, '-p', args.profile, 'chat', '--help'],
                                capture_output=True, text=True, timeout=30)
        if result.returncode or '--query-file' not in result.stdout or '--in DIR' not in result.stdout:
            raise ValueError('Hermes profile/chat preflight failed; inspect hermes -p PROFILE chat --help.')
        launcher = ROOT / 'skills/florida-update/scripts/flwu.py'
        subprocess.run([sys.executable, str(launcher), '--checkout', str(ROOT), '--check'],
                       cwd=ROOT, check=True, timeout=60, stdout=subprocess.DEVNULL)
        path = run / 'hermes-resume-prompt.md'
        command = [hermes, '-p', args.profile, 'chat', '--in', str(ROOT), '--query-file', str(path)]
        if args.check:
            print('Preflight passed. No agent launched; no research or database writes.')
            print(shlex.join(command))
            return 0
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            raise ValueError('Launch from an interactive terminal; use --check for noninteractive validation.')
        path.write_text(prompt)
        return subprocess.run(command, cwd=ROOT).returncode
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f'Handoff stopped: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
