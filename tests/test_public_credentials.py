"""Exercise the actual index boundary, including ignored/unstaged originals."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_public_credentials.py'


def test_guard_scans_staged_extensionless_blobs_without_leaking_values(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    key = 'AI' + 'za' + 'X' * 35
    evidence = tmp_path / 'capture'
    evidence.write_text('maps URL: ' + key)
    subprocess.run(['git', 'add', 'capture'], cwd=tmp_path, check=True)
    evidence.write_text('sanitized working tree, but unsafe index')
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 1
    assert 'capture' in result.stderr
    assert key not in result.stdout + result.stderr
    subprocess.run(['git', 'add', 'capture'], cwd=tmp_path, check=True)
    evidence.write_text('untracked local edit: ' + key)
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    assert key not in result.stdout + result.stderr


def test_guard_blocks_azure_request_credentials_and_allows_redaction(tmp_path):
    subprocess.run(['git','init','-q',str(tmp_path)],check=True)
    key='fixture-'+'X'*48
    prefix='https://fixture.azurewebsites.us'+'/api/rules?code='
    path=tmp_path/'update.json';path.write_text(prefix+key)
    subprocess.run(['git','add','update.json'],cwd=tmp_path,check=True)
    result=subprocess.run([sys.executable,str(SCRIPT)],cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==1 and key not in result.stdout+result.stderr
    path.write_text(prefix+'%5BREDACTED%5D')
    subprocess.run(['git','add','update.json'],cwd=tmp_path,check=True)
    result=subprocess.run([sys.executable,str(SCRIPT)],cwd=tmp_path,capture_output=True,text=True)
    assert result.returncode==0
