"""Real launcher preflight without relying on cwd or an editable install."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def test_installed_skill_resolves_explicit_checkout_from_another_directory(tmp_path):
    destination=tmp_path/'installed'
    result=subprocess.run([sys.executable,str(ROOT/'scripts/install_florida_update_skill.py'),
                           '--checkout',str(ROOT),'--python',sys.executable,
                           '--destination',str(destination)],cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    configured=json.loads((destination/'installation.json').read_text())
    assert configured['checkout']==str(ROOT)
    result=subprocess.run([sys.executable,str(destination/'scripts/flwu.py'),'--check'],
                          cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    info=json.loads(result.stdout)
    assert info['checkout']==str(ROOT)
    assert info['workflow_commands_verified'] and info['update_command_verified']
    assert all(Path(p).is_relative_to(ROOT/'src') for p in info['imports'].values())


def test_unconfigured_installed_skill_does_not_guess_a_development_checkout(tmp_path):
    destination=tmp_path/'installed/scripts';destination.mkdir(parents=True)
    script=destination/'flwu.py';shutil.copy2(ROOT/'skills/florida-update/scripts/flwu.py',script)
    result=subprocess.run([sys.executable,str(script),'--check'],cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==1
    assert 'No FLWU checkout configured' in result.stderr
    assert 'flwu-orchestration' not in result.stderr
