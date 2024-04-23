import requests
import xml.etree.ElementTree as etree

"""
XML namespaces for ISO 19115-3 XML (2018)
"""
ns_19115_3 =  { 'mdb':"http://standards.iso.org/iso/19115/-3/mdb/2.0",
                'cat': "http://standards.iso.org/iso/19115/-3/cat/1.0",
                'gfc': "http://standards.iso.org/iso/19110/gfc/1.1",
                'cit': "http://standards.iso.org/iso/19115/-3/cit/2.0",
                'gcx': "http://standards.iso.org/iso/19115/-3/gcx/1.0",
                'gex': "http://standards.iso.org/iso/19115/-3/gex/1.0",
                'lan': "http://standards.iso.org/iso/19115/-3/lan/1.0",
                'srv': "http://standards.iso.org/iso/19115/-3/srv/2.1",
                'mas': "http://standards.iso.org/iso/19115/-3/mas/1.0",
                'mcc': "http://standards.iso.org/iso/19115/-3/mcc/1.0",
                'mco': "http://standards.iso.org/iso/19115/-3/mco/1.0",
                'mda': "http://standards.iso.org/iso/19115/-3/mda/1.0",
                'mds': "http://standards.iso.org/iso/19115/-3/mds/2.0",
                'mdt': "http://standards.iso.org/iso/19115/-3/mdt/2.0",
                'mex': "http://standards.iso.org/iso/19115/-3/mex/1.0",
                'mmi': "http://standards.iso.org/iso/19115/-3/mmi/1.0",
                'mpc': "http://standards.iso.org/iso/19115/-3/mpc/1.0",
                'mrc': "http://standards.iso.org/iso/19115/-3/mrc/2.0",
                'mrd': "http://standards.iso.org/iso/19115/-3/mrd/1.0",
                'mri': "http://standards.iso.org/iso/19115/-3/mri/1.0",
                'mrl': "http://standards.iso.org/iso/19115/-3/mrl/2.0",
                'mrs': "http://standards.iso.org/iso/19115/-3/mrs/1.0",
                'msr': "http://standards.iso.org/iso/19115/-3/msr/2.0",
                'mdq': "http://standards.iso.org/iso/19157/-2/mdq/1.0",
                'mac': "http://standards.iso.org/iso/19115/-3/mac/2.0",
                'gco': "http://standards.iso.org/iso/19115/-3/gco/1.0",
                'gml': "http://www.opengis.net/gml/3.2",
                'xlink': "http://www.w3.org/1999/xlink",
                'xsi': "http://www.w3.org/2001/XMLSchema-instance"
}

"""
XML namespaces for ISO 19139 XML (2007)
"""
ns_19139 = { 'gmd':"http://www.isotc211.org/2005/gmd",
           'gco':"http://www.isotc211.org/2005/gco",
           'xsi':"http://www.w3.org/2001/XMLSchema-instance",
           'gml':"http://www.opengis.net/gml",
           'gts':"http://www.isotc211.org/2005/gts",
           'xlink':"http://www.w3.org/1999/xlink" }


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
    """
    Fethes metadata from a URL

    :param metadata_url: metadata URL
    :returns: metadata, encoding
    """
    meta = requests.get(metadata_url)
    if meta.encoding is not None:
        encoding = meta.encoding
    else:
        encoding = 'utf-8'

    # Read XML from URL
    return encoding, meta

def coords_check(xml, coords, encoding='utf-8'):
    """
    Look for the coords in ISO 19115-3 XML

    :param xml: XML string
    :param coords: coordinates dict,  keys are 'north' 'south' etc. Values can be string or float
    :param encoding: encoding string

    """
    root = etree.fromstring(bytes(xml, encoding))

    westpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:westBoundLongitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, westpath_list)
    xp += f"[.='" + str(coords['west']) + "']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

    eastpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:eastBoundLongitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, eastpath_list)
    xp += f"[.='" + str(coords['east']) + "']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

    southpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:southBoundLatitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, southpath_list)
    xp += f"[.='" + str(coords['south']) + "']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

    northpath_list = ['mri:MD_DataIdentification', 'mri:extent', 'gex:EX_Extent', 'gex:geographicElement', 'gex:EX_GeographicBoundingBox', 'gex:northBoundLatitude', 'gco:Decimal']
    xp = make_xpath(ns_19115_3, northpath_list)
    xp += f"[.='" + str(coords['north']) + "']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

def __xpath_check(xml, path_list, val, encoding):
    """
    Check for presence of XML

    :param xml: XML string
    :param path_list: list of XML elements
    :param val: string value to check
    :param encoding: encoding string e.g. 'utf-8'
    """
    root = etree.fromstring(bytes(xml, encoding))
    xp = make_xpath(ns_19115_3, path_list)
    xp += f"[.='" + val + "']"
    assert root.findall(xp, namespaces=ns_19115_3) != []

def title_check(xml, title, encoding='utf-8'):
    """
    Look for title in ISO 19115-3 XML

    :param xml: XML string
    :param title: title string to check
    :param encoding: encoding string
    """
    titlepath_list = ['mdb:identificationInfo', 'mri:MD_DataIdentification', 'mri:citation', 'cit:CI_Citation', 'cit:title', 'gco:CharacterString']
    __xpath_check(xml, titlepath_list, title, encoding)

def orgname_check(xml, orgname, encoding='utf-8'):
    """
    Look for title in ISO 19115-3 XML

    :param xml: XML string
    :param title: title string to check
    :param encoding: encoding string
    """
    orgname_path_list = ['mdb:contact', 'cit:CI_Responsibility', 'cit:party', 'cit:CI_Organisation', 'cit:name', 'gco:CharacterString']
    __xpath_check(xml, orgname_path_list, orgname, encoding)

def keyword_check(xml, keyw_list, skip_first=False, encoding='utf-8'):
    """
    Look for keywords in ISO 19115-3 XML

    :param xml: XML string
    :param keyw_list: list of keywords to look for
    :param skip_first: skip first element of path (when there are namespaces defined)
    :param encoding: encoding string
    """
    if skip_first:
        keyword_path_list = ['mri:MD_DataIdentification', 'mri:descriptiveKeywords', 'mri:MD_Keywords', 'mri:keyword', 'gco:CharacterString']
    else:
        keyword_path_list = ['mdb:identificationInfo', 'mri:MD_DataIdentification', 'mri:descriptiveKeywords', 'mri:MD_Keywords', 'mri:keyword', 'gco:CharacterString']
    for keyw in keyw_list:
        __xpath_check(xml, keyword_path_list, keyw, encoding)

def id_check(xml, id_str, encoding='utf-8'):
    """
    Look for keywords in ISO 19115-3 XML

    :param xml: XML string
    :param id_str: identity string to look for
    :param encoding: encoding string
    """
    id_path_list = ['mdb:metadataIdentifier', 'mcc:MD_Identifier', 'mcc:code', 'gco:CharacterString']
    __xpath_check(xml, id_path_list, id_str, encoding)

def onlineres_check(xml, link, name, desc, encoding='utf-8'):
    """
    Check the online resources in ISO 19115-3 XML

    :param xml: XML string
    :param link: online resource URL to check for
    :param name: name to check for
    :param desc: description to check for
    :param encoding: encoding string
    """
    onlineres_path = ['mdb:distributionInfo', 'mrd:MD_Distribution', 'mrd:transferOptions', 'mrd:MD_DigitalTransferOptions', 'mrd:onLine', 'cit:CI_OnlineResource']
    # Check resource URL
    link_pathlist = onlineres_path + ['cit:linkage', 'gco:CharacterString']
    __xpath_check(xml, link_pathlist, link, encoding)

    # Check resource name
    name_pathlist = onlineres_path + ['cit:name', 'gco:CharacterString']
    __xpath_check(xml, name_pathlist, name, encoding)

    # Optionally check resource description
    if desc is not None:
        desc_pathlist = onlineres_path + ['cit:description', 'gco:CharacterString']
        __xpath_check(xml, desc_pathlist, desc, encoding)



