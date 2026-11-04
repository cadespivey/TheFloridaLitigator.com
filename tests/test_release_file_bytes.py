"""Large current exports must retain exact commit-byte verification."""
import base64
from types import SimpleNamespace

import pytest

from flwu import workflow_deployment as deployment


ENDPOINT = 'repos/example/repo/contents/website/updates/current.json?ref=' + 'a' * 40


def test_small_file_reuses_inline_bytes_without_a_second_request(monkeypatch):
    raw = b'Exact public bytes\n'
    def metadata(config, *args):
        assert args == ('api', '-H', 'Accept: application/vnd.github.object+json', ENDPOINT)
        return dict(encoding='base64', content=base64.b64encode(raw).decode())
    monkeypatch.setattr(deployment, 'github', metadata)
    monkeypatch.setattr(deployment.subprocess, 'run', lambda *a, **k: pytest.fail('Unexpected raw request'))
    assert deployment.github_file({'checkout': '/fixture'}, ENDPOINT) == raw


@pytest.mark.parametrize('damage', [None, 'truncated', 'failed'])
def test_large_file_uses_pinned_raw_endpoint_and_rejects_failed_or_truncated_bytes(monkeypatch, damage):
    raw = b'\xff\x00' + b'x' * (1024 * 1024 + 1)
    monkeypatch.setattr(deployment, 'github', lambda *a: dict(encoding='none', content='', size=len(raw)))
    def request(args, **kwargs):
        assert args == ['gh', 'api', '-H', 'Accept: application/vnd.github.raw+json', ENDPOINT]
        assert kwargs == dict(cwd='/fixture', capture_output=True, timeout=90)
        return SimpleNamespace(returncode=1 if damage == 'failed' else 0,
                               stdout=raw[:-1] if damage == 'truncated' else raw,
                               stderr=b'Fixture request failure')
    monkeypatch.setattr(deployment.subprocess, 'run', request)
    if damage:
        with pytest.raises(ValueError, match='GitHub verification failed|size differs'):
            deployment.github_file({'checkout': '/fixture'}, ENDPOINT)
    else:
        assert deployment.github_file({'checkout': '/fixture'}, ENDPOINT) == raw


@pytest.mark.parametrize('metadata', [
    dict(encoding='none', content='', size=32 * 1024 * 1024 + 1),
    dict(encoding='none', content='', size=True),
    dict(encoding='none', content='unexpected', size=12),
    dict(encoding='unknown', content=''),
    dict(encoding='base64', content='%%%'),
])
def test_unsupported_or_malformed_metadata_stops_without_a_raw_request(monkeypatch, metadata):
    monkeypatch.setattr(deployment, 'github', lambda *a: metadata)
    monkeypatch.setattr(deployment.subprocess, 'run', lambda *a, **k: pytest.fail('Unexpected raw request'))
    with pytest.raises(ValueError, match='Unsupported|Invalid'):
        deployment.github_file({'checkout': '/fixture'}, ENDPOINT)
