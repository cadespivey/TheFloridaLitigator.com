from bs4 import BeautifulSoup
from flwu.site import navigation


def test_nested_counties_restrict_resource_links_and_keep_search():
    court = dict(group_id='county_example', category='County Courts', label='Example', url='https://example.gov/', resources=[dict(label=label,url='https://example.gov/'+str(i)) for i,label in enumerate(['Official Records','Court Records','Tax Assessor','Extra service'])])
    soup = BeautifulSoup(navigation('updates',courts=[court],extra_groups=['county_example']), 'html.parser')
    menu=soup.select_one('.court-menu .county-section')
    assert menu.name=='details'
    assert menu.select_one('ul details > summary').text=='A–F'
    county=menu.select_one('.county-menu')
    assert county.select_one('summary').text=='Example'
    assert [a.text for a in county.select('.county-resources a')]==['Official Records','Court Records','Tax Assessor']
    assert 'Extra service' not in soup.text
    assert soup.select_one('.personnel-menu .county-section [data-court]')['href']=='directory.html?court=county_example'
    assert not soup.select('form')


def test_numbered_courts_sort_numerically_in_both_menus():
    rows = []
    for category, prefix, suffix, words in [
        ('Circuit Courts', 'circuit', 'Judicial Circuit', ['Twentieth', 'Eleventh', 'Second', 'First', 'Nineteenth']),
        ('District Courts of Appeal', 'dca', 'District Court of Appeal', ['Sixth', 'Fourth', 'Second', 'Third', 'First', 'Fifth']),
    ]:
        rows.extend(dict(category=category, group_id=prefix+'_'+word.lower(), label=word+' '+suffix, url='https://example.gov/') for word in words)
    soup = BeautifulSoup(navigation('updates', courts=rows, extra_groups=[r['group_id'] for r in rows]), 'html.parser')
    expected = [['First', 'Second', 'Eleventh', 'Nineteenth', 'Twentieth'], ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth']]
    for menu in ['.court-menu', '.personnel-menu']:
        for section, order in zip(soup.select(menu+' .court-section'), expected):
            assert [a.text.split()[0] for a in section.select('a')] == order
