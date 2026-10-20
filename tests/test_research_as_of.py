"""Partial-day baselines must name a real cutoff without relaxing normal weeks."""
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import pytest
from flwu.research import initialize


def test_explicit_partial_day_cutoff_is_pinned(tmp_path):
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=1)
    day = cutoff.astimezone(ZoneInfo('America/New_York')).date().isoformat()
    initialize(tmp_path, day, day, as_of=cutoff.isoformat())
    contract = json.loads((tmp_path/'contract.json').read_text())
    assert contract['partial_final_day'] is True
    assert contract['cutoff_utc'] == cutoff.isoformat()
    with pytest.raises(ValueError, match='differs'):
        initialize(tmp_path, day, day)


def test_as_of_rejects_future_and_wrong_calendar_day(tmp_path):
    with pytest.raises(ValueError, match='future'):
        initialize(tmp_path, '2026-01-01', '2026-01-01', as_of='2099-01-01T12:00:00Z')
    with pytest.raises(ValueError, match='window-end'):
        initialize(tmp_path, '2026-01-01', '2026-01-01', as_of='2026-01-02T12:00:00Z')
