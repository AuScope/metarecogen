from lxml import etree

from xmlns import iso19115_3_ns, iso19139_ns, insert

""" Adds keywords to ISO 19139 or ISO 19115-3 XML using XPATH insertion
"""

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
    root = insert(root, insert_txt, insertpoint_xpath_list, iso19139_ns)
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    return xml_string



def __add_models_keyword_iso19115_3(text, encoding):
    """
    Uses XPATH insert technique to add in "3D Geological Models" keyword to an ISO19115-3 XML record

    :param text: XML text to be inserted
    :param encoding: character encoding of text, e.g. 'utf-8'
    :returns: XML string
    """

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
    root = insert(root, insert_txt, insertpoint_xpath_list, iso19115_3_ns)
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    return xml_string
