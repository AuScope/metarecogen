import os

from helpers import keyword_check, onlineres_check
from ISO19115_3_extract import ISO19115_3Extractor

def test_ISO19115_3():
    URL = "https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml"
    name = 'ngawler'
    XML_FILE = f"test_19115_3_{name}.xml"
    coords = {'north': '0.0', 'south': '-45', 'east': '-145', 'west':'-100'}
    ce = ISO19115_3Extractor()
    assert ce.write_record(name, coords, name, URL, XML_FILE)

    with open(os.path.join(ce.output_dir, XML_FILE), 'r') as fd:
        lines = fd.readlines()
        xml_str = ''.join(lines)
        # Check that keywords were inserted
        keyword_check(xml_str, ["AuScope 3D Geological Models", "Gawler Craton"], skip_first=True)
        # Check that online resources were inserted
        onlineres_check(xml_str, f"https://geomodels.auscope.org.au/model/{name}", "3D Geological Model", None)


