"""One person's county-specific evidence context is not a conflicting identity."""
import copy

import pytest

from flwu import county_directory as directory, workflow as w
from tests.test_county_directory import supplement, seal


def county_pair(supplement):
    first = copy.deepcopy(supplement)
    second = copy.deepcopy(supplement)
    second['county'] = 'Clay'
    second['courts'][0].update(group_id='clerk_clay', label='Clay County')
    for person in second['people']:
        person['counties'] = ['Clay']
        person['court_ids'] = ['clerk_clay']
    return first, second


@pytest.mark.parametrize('context', ['dates', 'conflicts', 'both'])
def test_cross_county_evidence_versions_remain_distinct_without_blocking_identity(tmp_path, supplement, context):
    first, second = county_pair(supplement)
    if context in ('dates', 'both'):
        second['people'][0]['dates'] = {'procedure_revision': '2025-06-27'}
    if context in ('conflicts', 'both'):
        second['people'][0]['conflicts'] = [dict(
            topic='Fixture procedure format', statements=['Source A says Word.', 'Source B says PDF.'],
            resolution='Both retained without choosing a controlling source.')]
    seal(first); seal(second)
    paths = [tmp_path / 'first.json', tmp_path / 'second.json']
    w.write(paths[0], first); w.write(paths[1], second)
    before = [path.read_bytes() for path in paths]
    assert directory.load_supplements(paths, preview=True) == [first, second]
    assert [path.read_bytes() for path in paths] == before
    assert first['people'][0]['dates'] != second['people'][0]['dates'] or context == 'conflicts'
    assert first['people'][0]['conflicts'] != second['people'][0]['conflicts'] or context == 'dates'


@pytest.mark.parametrize('field', ['name', 'kind', 'assignment', 'contacts', 'profile_url', 'procedure_url'])
def test_cross_county_actual_personnel_differences_still_require_reconciliation(tmp_path, supplement, field):
    first, second = county_pair(supplement)
    person = second['people'][0]
    if field == 'kind': person[field] = 'Senior judge'
    elif field == 'contacts': person[field]['office'][0]['lines'] = ['Different published contact']
    else: person[field] += '-different'
    seal(first); seal(second)
    paths = [tmp_path / 'first.json', tmp_path / 'second.json']
    w.write(paths[0], first); w.write(paths[1], second)
    before = [path.read_bytes() for path in paths]
    with pytest.raises(ValueError, match='Conflicting identity across county supplements'):
        directory.load_supplements(paths, preview=True)
    assert [path.read_bytes() for path in paths] == before
