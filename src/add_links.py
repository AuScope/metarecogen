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


def add_model_link(model_endpath, text):
    """
    Uses XPATH insert technique to add in models URL to an ISO 19139 record
    Saves XML text to file

    :param model_endpath: model path
    :param text: XML text
    :returns: boolean
    """
    print(f"Adding model download link to: {model_endpath}")
    # XML Namespace dict
    ns = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gco': 'http://www.isotc211.org/2005/gco'}

    # Parse XML metadata record
    root = etree.fromstring(bytes(text, 'utf-8'))
    insert_point_xpath_list = [ 'gmd:MD_Metadata', 'gmd:distributionInfo', 'gmd:MD_Distribution', 'gmd:transferOptions',
            'gmd:MD_DigitalTransferOptions', 'gmd:BLAH']

    # XML snippet to be inserted into XML record
    insert_txt = f"""<gmd:onLine xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco">
              <gmd:CI_OnlineResource>
                 <gmd:linkage>
                    <gmd:URL>http://geomodels.auscope.org/model/{model_endpath}</gmd:URL>
                 </gmd:linkage>
                 <gmd:protocol>
                    <gco:CharacterString>WWW:LINK-1.0-http--link</gco:CharacterString>
                 </gmd:protocol>
                 <gmd:name>
                    <gco:CharacterString>3D Geological Model</gco:CharacterString>
                 </gmd:name>
              </gmd:CI_OnlineResource>
           </gmd:onLine>
    """

    # Insert 
    root = insert(root, insert_txt, insert_point_xpath_list, ns)

    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")

    # write to disk
    print(f"Writing {model_endpath}.xml")
    with open(os.path.join(OUTPUT_DIR, f"{model_endpath}.xml"), 'w') as ff:
        ff.write(xml_string)

    return True
