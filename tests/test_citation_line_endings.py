"""Citation validation must preserve the acquisition's exact extraction bytes."""
import hashlib

import pytest

from flwu.research import _citation


@pytest.mark.parametrize("ending", [b"\n", b"\r\n", b"\r"])
def test_exact_extraction_bytes_and_quote_are_required(tmp_path, ending):
    raw = b"<html>Original source</html>"
    text = ending.join([b"Judge Jane Example", b"Published contact", b""])
    (tmp_path / "raw.bin").write_bytes(raw)
    path = tmp_path / "extraction.txt"
    path.write_bytes(text)
    ref = {
        "path": "raw.bin", "sha256": hashlib.sha256(raw).hexdigest(),
        "text_path": "extraction.txt", "text_sha256": hashlib.sha256(text).hexdigest(),
        "url": "https://example.invalid/source", "authority": "official",
        "synthetic": False, "http_status": 200,
        "retrieved_at": "2026-10-25T00:00:00+00:00",
        "locator": "Named contact block", "quote": text.decode("utf-8"),
    }
    _citation(tmp_path, ref)

    with pytest.raises(ValueError, match="Claim quote is absent"):
        _citation(tmp_path, dict(ref, quote="Invented contact"))

    # Even a line-ending-only modification is a different acquisition.
    other_ending = b"\n" if ending != b"\n" else b"\r\n"
    path.write_bytes(text.replace(ending, other_ending))
    with pytest.raises(ValueError, match="Extracted text changed"):
        _citation(tmp_path, ref)
