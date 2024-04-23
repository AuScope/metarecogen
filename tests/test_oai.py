import os

from oai_extract import OaiExtractor
from helpers import coords_check, title_check, orgname_check, id_check, keyword_check, onlineres_check



def test_oai():
    # Get records from Northern Territory Geological Service
    # OAI-PMH URL
    OAI__URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'
    XML_FILE = 'test_oai.xml'
    coords = {'east': 154.3, 'west': 109.1, 'south': -43.9, 'north': -10.6}
    name = 'mcarthur'
    
    # GEMIS permanent link of McArthur 3D model
    MODEL__URL = 'https://geoscience.nt.gov.au/gemis/ntgsjspui/handle/1/81751'
    oe = OaiExtractor(OAI__URL)
    # Convert perm link to OAI-PMH ID
    handle_id = '/'.join(MODEL__URL.split('/')[-2:])
    # NB: Some geological fields that are present in GEMIS website are missing from OAI output with standard 'oai_dc' prefix,
    # i.e. "Stratigraphy" The 'xoai' prefix will allow extraction of these missing fields but the XML output would need parsing
    assert oe.write_record('test', coords, name, 'oai:geoscience.nt.gov.au:'+handle_id, 'oai_dc', "NTGS GEMIS", XML_FILE)

    with open(os.path.join(oe.output_dir, XML_FILE), 'r') as fd:
        lines = fd.readlines()
        xml_str = ''.join(lines)
        # Check that coords were output with correct XML path & values
        coords_check(xml_str, coords)
        # Check title
        title_check(xml_str, "3D model of the greater McArthur Basin")
        # Check organisation name
        orgname_check(xml_str, "Northern Territory Geological Survey")
        # Check identifier
        id_check(xml_str, "DIP012")
        # Check keywords
        keyword_check(xml_str, ["3D Geological Models", "Geology"])
        # Check that online resources were inserted
        onlineres_check(xml_str, f"https://geomodels.auscope.org.au/model/{name}", "3D Geological Model", "3D Geological Model in AuScope 3D Geomodels Portal")

