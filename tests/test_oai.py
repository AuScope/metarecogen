import os
from oai_extract import OaiExtractor

def test_oai():
    # Get records from Northern Territory Geological Service
    # OAI-PMH URL
    OAI__URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'
    XML_FILE = 'test_oai.xml'
    
    # GEMIS permanent link of McArthur 3D model
    MODEL__URL = 'https://geoscience.nt.gov.au/gemis/ntgsjspui/handle/1/81751'
    oe = OaiExtractor(OAI__URL)
    # Convert perm link to OAI-PMH ID
    handle_id = '/'.join(MODEL__URL.split('/')[-2:])
    # NB: Some geological fields that are present in GEMIS website are missing from OAI output with 'oai_dc' prefix,
    # i.e. "Stratigraphy" The 'xoai' prefix will allow extraction of these missing fields but the XML output
    # would need to be parsed
    assert oe.write_record('test', {'east': 154.3, 'west': 109.1, 'south': -43.9, 'north': -10.6}, 'mcarthur', 'oai:geoscience.nt.gov.au:'+handle_id, 'oai_dc', "NTGS GEMIS", XML_FILE)

    with open(os.path.join(oe.output_dir, XML_FILE), 'r') as fd:
        lines = fd.readlines()
        assert '154.3' in ''.join(lines)
