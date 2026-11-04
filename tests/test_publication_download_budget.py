"""Current production archive download is bounded independently of content review."""
import io
import json

import pytest

from flwu import workflow_deployment as deployment


def test_current_sized_archive_over_32_mib_can_be_verified(monkeypatch):
    text='x'*(34*1024*1024)
    raw=json.dumps({'current':text}).encode()
    monkeypatch.setattr(deployment.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(raw))
    assert deployment.fetch_json('https://court.example/current.json')=={'current':text}


def test_download_still_stops_at_budget_plus_one_without_parsing_excess(monkeypatch):
    monkeypatch.setattr(deployment,'MAX_PUBLICATION_BYTES',64,raising=False)
    class Response(io.BytesIO):
        def read(self,size=-1):
            assert size==65
            return super().read(size)
    monkeypatch.setattr(deployment.urllib.request,'urlopen',lambda *a,**k:Response(b'x'*100))
    with pytest.raises(ValueError,match='exceeds verification limit'):
        deployment.fetch_json('https://court.example/current.json')


def test_successful_download_does_not_mask_invalid_json(monkeypatch):
    monkeypatch.setattr(deployment.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(b'not json'))
    with pytest.raises(json.JSONDecodeError):
        deployment.fetch_json('https://court.example/current.json')
