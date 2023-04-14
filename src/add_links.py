#!/usr/bin/env python3

import sys
import requests
import json 
from pathlib import Path
import datetime
import geojson
from lxml import etree
from io import BytesIO
from copy import copy
from lxml.builder import ElementMaker


"""
Uses XPATH insert technique to add in models URL to an iso19139 record
"""
def add_model_link(model_endpath, text):
    #
    # TODO: Call the XPATH insert code in add_model_keyw in place of this
    #
    print(f"Converting: {model_endpath}")
    # XML Namespace dict
    ns = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gco': 'http://www.isotc211.org/2005/gco'}

    # Parse XML metadata record
    root = etree.fromstring(bytes(text, 'utf-8'))
    master_xpath_list = [ 'gmd:MD_Metadata', 'gmd:distributionInfo', 'gmd:MD_Distribution', 'gmd:transferOptions',
            'gmd:MD_DigitalTransferOptions', 'gmd:BLAH']

    # XML snippet to be inserted into XML record
    model_online = f"""<gmd:onLine xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco">
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
    # Parse XML snippet into doc object
    online_root = etree.fromstring(bytes(model_online, 'utf-8'))

    # Look for a place to insert 'online_root'
    xpath_list = copy(master_xpath_list)
    # print(f'{xpath_list=}')
    result = []
    while len(result) == 0 and len(xpath_list) > 1:
        xpath = '/' + '/'.join(xpath_list)
        # print("Searching for ", xpath)
        result = root.xpath(xpath, namespaces=ns)
        # print(f"{result=}")
        xpath_list.pop()

    # Insert 'online_root' and any other required elements 
    leftovers = master_xpath_list[len(xpath_list):]
    # print(f'{leftovers=}')
    # print(f'{result=}')
    # If not found then insert at root
    if result==[]:
        child = root
    else:
        child = result[0]
    for elemtag in leftovers[1:]:
        tagname = elemtag.split(':')[1] 
        newtag = '{http://www.isotc211.org/2005/gmd}' + tagname 
        # If not at the end
        if tagname != 'BLAH':
            # IF we need to insert a new tag in path
            print(f'Inserting {newtag=} @ {child=}')
            child = etree.SubElement(child, newtag, nsmap=ns)
        else:
            # If at end - insert inline objects here
            print(f'Inserting {online_root=} @ {child=}')
            child.append(online_root)
            break
    
    xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
    #print(xml_string)
    #print("\n\n\nROOT:")
    #print(etree.tostring(root, pretty_print=True).decode("utf-8"))
    # write to disk
    with open(f"{model_endpath}.xml", 'w') as ff:
        ff.write(xml_string)

    return True
