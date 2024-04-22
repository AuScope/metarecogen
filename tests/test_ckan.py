from ckan_extract import CkanExtractor

def test_ckan():
    SITE__URL = 'https://geoscience.data.qld.gov.au'
    ce = CkanExtractor()
    assert ce.write_record('Mt Dore', { 'north': -10.2, 'south': -45.0, 'east': 145.0, 'west': 90.0}, 'mtdore', SITE__URL, 'ds000002', 'test_ckan.xml')

