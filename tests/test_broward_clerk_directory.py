import pytest
from scripts.broward_clerk_directory import extract_directory


ROW = '<tr><td><a href="/Divisions/CircuitCivil">Circuit Civil</a><br>201 Street<br>Room: 04130</td><td>Counter: 8–3:30<br>954-831-6565 (option 2)<br>954-831-6572 (Fax)</td></tr>'


def page(rows=ROW):
    return '<nav>Wrong phone 999</nav><div id="ClerkDirectory"><table><thead><tr><th>Division, Address<br>and Room Number</th><th>Hours of Operation<br>and Phone Numbers</th></tr></thead><tbody>' + rows + '</tbody></table></div>'


def test_preserves_row_identity_leading_zero_room_and_labeled_contacts():
    row, = extract_directory(page())
    assert row['division'] == 'Circuit Civil'
    assert row['original_href'] == '/Divisions/CircuitCivil'
    assert 'Room: 04130' in row['address_text']
    assert row['hours_and_contact_text'] == 'Counter: 8–3:30\n954-831-6565 (option 2)\n954-831-6572 (Fax)'
    assert '999' not in row['quote']
    assert row['quote'].endswith('(Fax)')


@pytest.mark.parametrize('source', [
    '<p>shell</p>', page() + page(), page(''), page(ROW + ROW),
    page(ROW.replace('<td>', '<td colspan="2">', 1)),
    page(ROW.replace('<a href="/Divisions/CircuitCivil">Circuit Civil</a>', 'No division link')),
    page().replace('Hours of Operation', 'Changed schema'),
])
def test_rejects_ambiguous_or_changed_directory(source):
    with pytest.raises(ValueError):
        extract_directory(source)
