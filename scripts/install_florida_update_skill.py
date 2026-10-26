#!/usr/bin/env python3
"""Install the repository skill with an explicit checkout/interpreter binding."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--python',type=Path,required=True)
    parser.add_argument('--destination',type=Path,default=Path.home()/'.codex/skills/florida-update')
    args=parser.parse_args()
    root=args.checkout.resolve();destination=args.destination.expanduser().resolve()
    source=root/'skills/florida-update'
    if source==destination:raise SystemExit('Install destination must be separate from repository skill source')
    probe=subprocess.run([sys.executable,str(source/'scripts/flwu.py'),'--checkout',str(root),'--python',str(args.python),'--check'],capture_output=True,text=True)
    if probe.returncode:raise SystemExit(probe.stderr)
    if not args.python.is_file():raise SystemExit('Specified interpreter does not exist')
    # Preserve unrelated installed metadata; replace only repository-owned files.
    for item in source.rglob('*'):
        if item.is_file() and '__pycache__' not in item.parts and item.name!='installation.json':
            target=destination/item.relative_to(source)
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(item,target)
    (destination/'installation.json').write_text(json.dumps({'checkout':str(root),'python':str(args.python.expanduser().absolute())},indent=2)+'\n')
    result=subprocess.run([sys.executable,str(destination/'scripts/flwu.py'),'--check'],cwd=Path.home())
    return result.returncode


if __name__=='__main__':raise SystemExit(main())
