import os

from ckan_extract import CkanExtractor
from helpers import coords_check, title_check, orgname_check, id_check, keyword_check, onlineres_check

def test_ckan():
    SITE__URL = 'https://geoscience.data.qld.gov.au'
    XML_FILE = 'test_ckan.xml'
    ce = CkanExtractor()
    name = 'mtdore'
    # These are coords in the CKAN package
    coords = {'west': 140.079224, 'east': -22.29506, 'south': 140.803657, 'north': -20.669165}
    assert ce.write_record('Mt Dore', coords, name, SITE__URL, 'ds000002', XML_FILE)

    with open(os.path.join(ce.output_dir, XML_FILE), 'r') as fd:
        lines = fd.readlines()
        xml_str = ''.join(lines)
        # Check that coords were output with correct XML path & values
        coords_check(xml_str, coords)
        # Check title
        title_check(xml_str, "Mt Dore 3D Model")
        # Check organisation name
        orgname_check(xml_str, "Geological Survey of Queensland")
        # Check identifier
        id_check(xml_str, "9f2e2907-f0a2-4675-871a-51d34a709b43")
        # Check keywords
        keyword_check(xml_str, ["3D Geological Models", "geological models"])
        # Check that online resources were inserted
        onlineres_check(xml_str, f"https://geomodels.auscope.org.au/model/{name}", "3D Geological Model", "3D Geological Model in AuScope 3D Geomodels Portal")



