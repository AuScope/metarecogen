#!/usr/bin/env python3

import sys
import os
import requests
import json 
from pathlib import Path
import datetime
import geojson
from lxml import etree
from io import BytesIO
from copy import copy
from lxml.builder import ElementMaker
from add_model_keyw import insert
from constants import OUTPUT_DIR



def add_coords(coords, model_endpath, text, encoding, iso_ver):
    print(f"Adding coords to {model_endpath}")
    if iso_ver.upper() == 'ISO19115-3':
        return __add_coords_iso19115_3(coords, model_endpath, text, encoding)
    return __add_coords_iso19139(coords, model_endpath, text, encoding)

"""
Uses XPATH insert technique to add in BBOX coords to an ISO19139 XML record
"""
def __add_coords_iso19139(coords, model_endpath, text, encoding):
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
    insert_txt = f"""<gmd:extent xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:srv="http://www.isotc211.org/2005/srv" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:gmi="http://www.isotc211.org/2005/gmi" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd">
           <gmd:EX_Extent>
             <gmd:geographicElement>
               <gmd:EX_GeographicBoundingBox>
                 <gmd:westBoundLongitude>
                   <gco:Decimal>{coords['west']}</gco:Decimal>
                 </gmd:westBoundLongitude>
                 <gmd:eastBoundLongitude>
                   <gco:Decimal>{coords['east']}</gco:Decimal>
                 </gmd:eastBoundLongitude>
                 <gmd:southBoundLatitude>
                   <gco:Decimal>{coords['south']}</gco:Decimal>
                 </gmd:southBoundLatitude>
                 <gmd:northBoundLatitude>
                   <gco:Decimal>{coords['north']}</gco:Decimal>
                 </gmd:northBoundLatitude>
               </gmd:EX_GeographicBoundingBox>
             </gmd:geographicElement>
           </gmd:EX_Extent>
         </gmd:extent>
    """
    # Insert 
    root = insert(root, insert_txt, insertpoint_xpath_list, ns)
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    #print(xml_string)
    #print("\n\n\nROOT:")
    #print(etree.tostring(root, pretty_print=True).decode("utf-8"))

    ## write to disk
    #with open(f"{model_endpath}.xml", 'w') as ff:
    #    ff.write(xml_string)

    return xml_string



"""
Uses XPATH insert technique to add in BBOX coords to an ISO19115-3 XML record
"""
def __add_coords_iso19115_3(coords, model_endpath, text, encoding):
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
    insert_txt = f"""<mri:extent xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0" xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0">
                       <gex:EX_Extent>
                         <gex:geographicElement>
                           <gex:EX_GeographicBoundingBox>
                             <gex:westBoundLongitude>
                               <gco:Decimal>{coords['west']}</gco:Decimal>
                             </gex:westBoundLongitude>
                             <gex:eastBoundLongitude>
                               <gco:Decimal>{coords['east']}</gco:Decimal>
                             </gex:eastBoundLongitude>
                             <gex:southBoundLatitude>
                               <gco:Decimal>{coords['south']}</gco:Decimal>
                             </gex:southBoundLatitude>
                             <gex:northBoundLatitude>
                               <gco:Decimal>{coords['north']}</gco:Decimal>
                             </gex:northBoundLatitude>
                           </gex:EX_GeographicBoundingBox>
                         </gex:geographicElement>
                       </gex:EX_Extent>
                     </mri:extent>
    """
    # Insert 
    root = insert(root, insert_txt, insertpoint_xpath_list, ns)
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    #print(xml_string)
    #print("\n\n\nROOT:")
    #print(etree.tostring(root, pretty_print=True).decode("utf-8"))

    # write to disk
    with open(os.path.join(OUTPUT_DIR, f"{model_endpath}.xml"), 'w') as ff:
        ff.write(xml_string)

    return True



if __name__ == "__main__":
    metadata_url = "https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml"

    model_endpath ='ngawler'
    print(f"Converting: {model_endpath}")
    # Read XML from URL
    try:
        metadata = requests.get(metadata_url)
    except Exception as e:
        print(f"Cannot retrieve URL {metadata_url}\n", e)
        sys.exit(1)
    #print(f"{metadata.text=}")
    #print(f"{metadata.encoding=}")
    if metadata.encoding is not None:
        encoding = metadata.encoding
    else:
        encoding = 'utf-8'
    __add_coords_iso19139(coords, model_endpath, metadata.text, encoding)