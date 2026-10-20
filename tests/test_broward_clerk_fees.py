import pytest

from scripts.broward_clerk_fees import extract_fees


HTML = b'''<div id="FilingFees"><table><tbody>
<tr><td colspan="2">Valid Forms of Payment -- no personal checks.</td></tr>
<tr><td colspan="2">Filing</td></tr>
<tr><td>More than $500, not more than $2,500; per defendant</td><td>$1,750.00</td></tr>
<tr><td>Writ fee</td><td>$85.00</td></tr>
<tr><td colspan="2">Additional</td></tr>
<tr><td>Writ fee</td><td>$85.00</td></tr>
</tbody></table></div>'''
COUNTS = {'Filing': 2, 'Additional': 1}


def test_preserves_tiers_units_and_repeated_fees_without_total():
    rows = extract_fees(HTML, COUNTS)
    assert rows[0] == {
        'section': 'Filing',
        'label': 'More than $500, not more than $2,500; per defendant',
        'amount_usd': '1750.00', 'row_index': 2,
        'quote': 'More than $500, not more than $2,500; per defendant\n$1,750.00',
    }
    assert [(r['section'], r['amount_usd']) for r in rows[1:]] == [('Filing', '85.00'), ('Additional', '85.00')]


@pytest.mark.parametrize('old,new', [
    (b'id="FilingFees"', b'id="Other"'),
    (b'Additional', b'Unknown section'),
    (b'Additional', b'Filing'),
    (b'<td>Writ fee</td>', b'<td rowspan="2">Writ fee</td>'),
    (b'<td>Writ fee</td>', b'<td colspan="2">Writ fee</td>'),
    (b'<td>Writ fee</td>', b'<td></td>'),
    (b'$85.00', b'$85.00 per item'),
    (b'$85.00', b'$1234,567.00'),
    (b'Valid Forms of Payment', b'Changed introduction'),
    (b'<td>Writ fee</td>', b'<th>Writ fee</th>'),
])
def test_changed_structure_or_values_require_review(old, new):
    with pytest.raises(ValueError):
        extract_fees(HTML.replace(old, new), COUNTS)


def test_rejects_multiple_panels_or_tables():
    for html in [HTML + HTML, HTML.replace(b'</tbody></table>', b'</tbody></table><table></table>')]:
        with pytest.raises(ValueError):
            extract_fees(html, COUNTS)


def test_missing_row_and_changed_count_fail():
    with pytest.raises(ValueError):
        extract_fees(HTML.replace(b'<tr><td>Writ fee</td><td>$85.00</td></tr>', b'', 1), COUNTS)
    with pytest.raises(ValueError):
        extract_fees(HTML, {'Filing': 3, 'Additional': 1})


@pytest.mark.parametrize('counts', [{}, {'Filing': 0}, {'Filing': True}])
def test_requires_reviewed_expectations(counts):
    with pytest.raises(ValueError):
        extract_fees(HTML, counts)
