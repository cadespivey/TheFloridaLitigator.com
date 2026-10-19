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
    assert soup.select_one('form[role=search] input')['name']=='q'
