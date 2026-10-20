"""Weekly orchestration (C34)."""
from __future__ import annotations
from typing import Any
from flwu.config import load_config
from flwu.registry import load_sources, validate_sources

class OrchestrationError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

def run_weekly(state_root, output_dir, fixture_path=None, observed_at=None):
    if fixture_path is not None:
        from pathlib import Path
        from flwu.fixture_pipeline import run_fixture
        return run_fixture(Path(fixture_path), Path(state_root), Path(output_dir), observed_at=observed_at)
    raise OrchestrationError("NOT_IMPLEMENTED", "Live orchestration is unavailable. Research evidence tracking does not execute source adapters.")
