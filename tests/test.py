import requests
import xml.etree.ElementTree as etree

from add_coords import add_coords
from add_links import add_model_link
from add_model_keyw import add_models_keyword
from namespaces import ns_19115_3, ns_19139

ISO19139_URL = "http://52.65.91.200/geonetwork/srv/api/records/97ed8560c193e0c1855445cec4e812d4c59654ff/formatters/xml"
ISO19115_3_URL = "https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml"

def make_xpath(ns_dict, path_elems):
    """
    Makes an xpath with namespaces  given a list of tags

    :param ns_dict: namespace dictionary e.g. { 'cit': 'http://cit.org/1.0', 'dif': 'http://dif.org/2.0' }
    :param path_elems: list of tags e.g. ['cit:citation', 'dif:differential']
    :returns: xpath string
    """
    path = './/'
    for ele in path_elems:
        ns, dot, tag = ele.partition(':')
        path += f"{{{ns_dict[ns]}}}{tag}/"
    return path.rstrip('/')

def get_metadata(metadata_url):
    meta = requests.get(metadata_url)
    if meta.encoding is not None:
        encoding = meta.encoding
    else:
        encoding = 'utf-8'

    # Read XML from URL
    return encoding, meta

def test_add_coords():
    """
    Tests 'add_coords()'
    """
    coords = {'north': '-10.0', 'south': '-20.0', 'east': '-30.0', 'west': '-40.0'}
        
    # Get XML string
    encoding, metadata = get_metadata(ISO19115_3_URL)

    # Add the coords
    xml = add_coords(coords, metadata.text, encoding, "ISO19115-3")

    # Look for the coords in XML
    root = etree.fromstring(bytes(xml, encoding))

    westpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:westBoundLongitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, westpath_list)
    xp += "[.='-40.0']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

    eastpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:eastBoundLongitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, eastpath_list)
    xp += "[.='-30.0']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

    southpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:southBoundLatitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, southpath_list)
    xp += "[.='-20.0']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

    northpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:northBoundLatitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, northpath_list)
    xp += "[.='-10.0']"
    assert root.findall(xp, namespaces=ns_19115_3) != []


def test_add_links():
    """
    Tests 'add_links()'
    """
    # Get XML string
    encoding, metadata = get_metadata(ISO19139_URL)

    # Add model link
    model_endpath = 'mymodel'
    xml_string = add_model_link(model_endpath, metadata.text)

    # Check output
    root = etree.fromstring(bytes(xml_string, encoding))

    modelpath_list = ['gmd:distributionInfo', 'gmd:MD_Distribution', 'gmd:transferOptions',
                   'gmd:MD_DigitalTransferOptions', 'gmd:onLine', 'gmd:CI_OnlineResource', 'gmd:linkage', 'gmd:URL']
    xp = make_xpath(ns_19139, modelpath_list)
    xp += f"[.='https://geomodels.auscope.org/model/{model_endpath}']"
    assert root.findall(xp, namespaces=ns_19139) != []



def test_add_keyw():
    """
    Tests 'add_models_keyword()"
    """
    # Get XML string
    encoding, metadata = get_metadata(ISO19115_3_URL)
    xml_string = add_models_keyword(metadata.text, encoding, 'ISO19115-3')

    # Check output
    root = etree.fromstring(bytes(xml_string, encoding))

    keywpath_list = [ 'mri:MD_DataIdentification', 'mri:descriptiveKeywords', 'mri:MD_Keywords', 'mri:keyword', 'gco:CharacterString']
    xp = make_xpath(ns_19115_3, keywpath_list)
    xp += f"[.='AuScope 3D Geological Models']"
    assert root.findall(xp, namespaces=ns_19115_3) != []
