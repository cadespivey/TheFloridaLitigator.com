"""Real launcher preflight without relying on cwd or an editable install."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import importlib.util
from types import SimpleNamespace

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
    assert info['inline_review_api_verified']
    assert info['deterministic_publication_api_verified']
    assert {'publication_driver','publication_executor'}<=set(info['imports'])
    assert all(Path(p).is_relative_to(ROOT/'src') for p in info['imports'].values())


def test_unconfigured_installed_skill_does_not_guess_a_development_checkout(tmp_path):
    destination=tmp_path/'installed/scripts';destination.mkdir(parents=True)
    script=destination/'flwu.py';shutil.copy2(ROOT/'skills/florida-update/scripts/flwu.py',script)
    result=subprocess.run([sys.executable,str(script),'--check'],cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==1
    assert 'No FLWU checkout configured' in result.stderr
    assert 'flwu-orchestration' not in result.stderr


def test_ordinary_launcher_uses_one_verified_interpreter_without_help_probes(monkeypatch):
    script=ROOT/'skills/florida-update/scripts/flwu.py'
    spec=importlib.util.spec_from_file_location('checked_launcher',script)
    launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)
    calls=[]
    def run(argv,**kwargs):
        calls.append(argv)
        return SimpleNamespace(returncode=0,stdout='https://github.com/cadespivey/TheFloridaLitigator.com.git',stderr='')
    monkeypatch.setattr(launcher.subprocess,'run',run)
    assert launcher.main(['--checkout',str(ROOT),'--python',sys.executable,
                          'workflow','status','--run-dir','fixture-run'])==0
    assert len(calls)==2  # Git origin and one checked Python command.
    assert calls[1][1]=='-c' and 'imports escaped' in calls[1][2]
    assert '--help' not in calls[1]
    assert calls[1][-4:]==['workflow','status','--run-dir','fixture-run']
