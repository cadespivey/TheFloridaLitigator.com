"""Pytest configuration for Florida Litigator Weekly Update tests."""

import pytest


@pytest.fixture(autouse=True)
def isolated_research_history(tmp_path, monkeypatch):
    """Tests must never write synthetic or malformed fixtures to personal memory."""
    monkeypatch.setenv("FLWU_HISTORY_DB", str(tmp_path / "history.sqlite"))


@pytest.fixture
def temporary_directory(tmp_path):
    """Provide a temporary directory for tests."""
    return tmp_path
