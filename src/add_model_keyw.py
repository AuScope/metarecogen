from lxml import etree
from copy import copy


""" Adds keywords to ISO 19139 and ISO 19115-3 XML using XPATH insertion
"""


def insert(root, insert_txt, master_xpath_list, ns):
    """ Generic routine to insert text into XML document

    :param root: XML doc root 
    :param insert_txt: XML text to be inserted
    :param master_xpath_list: XML path list of insertion point
    :param ns: namespace dictionary
    """
    # Parse XML snippet into doc object
    insert_root = etree.fromstring(bytes(insert_txt, 'utf-8'))

    # Look for a place to insert 'insert_root'
    xpath_list = copy(master_xpath_list)
    result = []
    while len(result) == 0 and len(xpath_list) > 1:
        xpath = '/' + '/'.join(xpath_list)
        result = root.xpath(xpath, namespaces=ns)
        xpath_list.pop()

    # Insert 'online_root' and any other required elements 

    # If not found then insert at root
    if result==[]:
        leftovers = master_xpath_list[len(xpath_list):]
        child = root
    else:
        leftovers = master_xpath_list[len(xpath_list)+1:]
        child = result[0]
    if len(leftovers) == 1:
        child.append(insert_root)
    else:
        for elemtag in leftovers:
            nsname, tagname = elemtag.split(':')
            newtag = '{' + ns[nsname] + '}' + tagname 
            # If not at the end
            if tagname != 'BLAH':
                # IF we need to insert a new tag in path
                child = etree.SubElement(child, newtag, nsmap=ns)
            else:
                # If at end - insert inline objects here
                child.append(insert_root)
                break
    return root
    

def add_models_keyword(text, encoding, iso_ver):
    """
    Uses XPATH insert technique to add in "3D Geological Models" keyword to an XML record

    :param text: XML text to be inserted
    :param encoding: character encoding of text, e.g. 'utf-8'
    :param iso_ver: ISO XML version string, either 'ISO19139' or 'ISO19115-3'
    :returns: XML string
    """
    if iso_ver == 'ISO19115-3':
        return __add_models_keyword_iso19115_3(text, encoding)
    return __add_models_keyword_iso19139(text, encoding)



def __add_models_keyword_iso19139(text, encoding):
    """
    Uses XPATH insert technique to add in "3D Geological Models" keyword to an ISO19139 XML record

    :param text: XML text to be inserted
    :param encoding: character encoding of text, e.g. 'utf-8'
    :returns: XML string
    """
    # ISO19139 XML Namespace dict
    ns = { 'gmd':"http://www.isotc211.org/2005/gmd",
           'gco':"http://www.isotc211.org/2005/gco",
           'xsi':"http://www.w3.org/2001/XMLSchema-instance",
           'gml':"http://www.opengis.net/gml",
           'gts':"http://www.isotc211.org/2005/gts",
           'xlink':"http://www.w3.org/1999/xlink" }


    # Parse XML metadata record
    root = etree.fromstring(bytes(text, encoding))

    # Point in XML where insertion takes place
    insertpoint_xpath_list = ['gmd:MD_Metadata', 'gmd:identificationInfo', 'gmd:MD_DataIdentification', 'gmd:BLAH'] 

    # XML snippet to be inserted into XML record
    # This uses a direct insert, results in messier XML.
    insert_txt = """
         <gmd:descriptiveKeywords xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:srv="http://www.isotc211.org/2005/srv" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:gmi="http://www.isotc211.org/2005/gmi" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd">
            <gmd:MD_Keywords>
               <gmd:keyword>
                  <gco:CharacterString>AuScope 3D Geological Models</gco:CharacterString>
               </gmd:keyword>
               <gmd:type>
                  <gmd:MD_KeywordTypeCode codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_KeywordTypeCode" codeListValue="theme"/>
               </gmd:type>
            </gmd:MD_Keywords>
         </gmd:descriptiveKeywords>
    """
    # Insert 
    root = insert(root, insert_txt, insertpoint_xpath_list, ns)
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    return xml_string



def __add_models_keyword_iso19115_3(text, encoding):
    """
    Uses XPATH insert technique to add in "3D Geological Models" keyword to an ISO19115-3 XML record

    :param text: XML text to be inserted
    :param encoding: character encoding of text, e.g. 'utf-8'
    :returns: XML string
    """
    # ISO19115-3 XML Namespace dict
    ns = {'mdb': "http://standards.iso.org/iso/19115/-3/mdb/1.0",
            'cat': "http://standards.iso.org/iso/19115/-3/cat/1.0",
            'gfc': "http://standards.iso.org/iso/19110/gfc/1.1",
            'cit': "http://standards.iso.org/iso/19115/-3/cit/1.0",
            'gcx': "http://standards.iso.org/iso/19115/-3/gcx/1.0",
            'gex': "http://standards.iso.org/iso/19115/-3/gex/1.0",
            'lan': "http://standards.iso.org/iso/19115/-3/lan/1.0",
            'srv': "http://standards.iso.org/iso/19115/-3/srv/2.0",
            'mas': "http://standards.iso.org/iso/19115/-3/mas/1.0",
            'mcc': "http://standards.iso.org/iso/19115/-3/mcc/1.0",
            'mco': "http://standards.iso.org/iso/19115/-3/mco/1.0",
            'mda': "http://standards.iso.org/iso/19115/-3/mda/1.0",
            'mds': "http://standards.iso.org/iso/19115/-3/mds/1.0",
            'mdt': "http://standards.iso.org/iso/19115/-3/mdt/1.0",
            'mex': "http://standards.iso.org/iso/19115/-3/mex/1.0",
            'mmi': "http://standards.iso.org/iso/19115/-3/mmi/1.0",
            'mpc': "http://standards.iso.org/iso/19115/-3/mpc/1.0",
            'mrc': "http://standards.iso.org/iso/19115/-3/mrc/1.0",
            'mrd': "http://standards.iso.org/iso/19115/-3/mrd/1.0",
            'mri': "http://standards.iso.org/iso/19115/-3/mri/1.0",
            'mrl': "http://standards.iso.org/iso/19115/-3/mrl/1.0",
            'mrs': "http://standards.iso.org/iso/19115/-3/mrs/1.0",
            'msr': "http://standards.iso.org/iso/19115/-3/msr/1.0",
            'mdq': "http://standards.iso.org/iso/19157/-2/mdq/1.0",
            'mac': "http://standards.iso.org/iso/19115/-3/mac/1.0",
            'gco': "http://standards.iso.org/iso/19115/-3/gco/1.0",
            'gml': "http://www.opengis.net/gml/3.2",
            'xlink': "http://www.w3.org/1999/xlink",
            'xsi': "http://www.w3.org/2001/XMLSchema-instance" }


    # Parse XML metadata record
    root = etree.fromstring(bytes(text, encoding))

    # Point in XML where insertion takes place
    insertpoint_xpath_list = ['mdb:MD_Metadata', 'mdb:identificationInfo', 'mri:MD_DataIdentification', 'mri:BLAH'] 

    # XML snippet to be inserted into XML record
    insert_txt = """<mri:descriptiveKeywords xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0" xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0">
<mri:MD_Keywords>
<mri:keyword>
<gco:CharacterString>AuScope 3D Geological Models</gco:CharacterString>
</mri:keyword>
<mri:type>
<mri:MD_KeywordTypeCode codeList="http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_KeywordTypeCode" codeListValue="theme"/>
</mri:type>
</mri:MD_Keywords>
</mri:descriptiveKeywords>
    """
    # Insert 
    root = insert(root, insert_txt, insertpoint_xpath_list, ns)
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    return xml_string
