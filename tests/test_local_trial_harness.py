"""Offline tests of trial preparation and evidence tooling; no model calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('local_model_replay',REPO/'trials/local_model_replay.py')
trial=importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


def test_trial_preserves_synthetic_boundary_and_retry_sequence(tmp_path):
    root=tmp_path/'trial'
    trial.prepare(root)
    workspace=root/'workspace'
    def fetch(endpoint):
        result=subprocess.run([sys.executable,str(workspace/'trial.py'),'fetch',endpoint],capture_output=True,text=True,check=True)
        return json.loads(result.stdout)
    first=fetch('opinions/C-START');second=fetch('opinions/C-START')
    assert first['status']==429 and first['retry_after']==0
    assert second['status']==200 and second['synthetic'] is True
    assert 'SYNTHETIC REPLAY' in (workspace/second['path']).read_text()
    assert fetch('procedures/casey-morgan')['status']==503
    (workspace/'state/control.json').write_text('{"restored":true}')
    assert fetch('procedures/casey-morgan')['status']==200
    assert (root/'answer-key.json').is_file()
    assert not (workspace/'answer-key.json').exists()
    assert json.loads((root/'plan.json').read_text())['native_auto_compaction_tested'] is False


def test_trial_rejects_false_citation_and_synthetic_relabeling(tmp_path):
    root=tmp_path/'trial'
    trial.prepare(root)
    workspace=root/'workspace'
    path=workspace/'work/answers/test.json'
    for value in ({'synthetic':False},{'synthetic':True,'citations':[{'evidence_id':'nonexistent','quote':'invented'}]}):
        path.write_text(json.dumps(value))
        result=subprocess.run([sys.executable,str(workspace/'trial.py'),'verify','work/answers/test.json'],capture_output=True,text=True)
        assert result.returncode==1
        assert 'error' in json.loads(result.stdout)
