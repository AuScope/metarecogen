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

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2, MetadataRecord

from extractor import Extractor

class ISO19139Extractor2(Extractor):

    def write_record(self, model_endpath, metadata_url):
        # XML Namespace dict
        ns = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gco': 'http://www.isotc211.org/2005/gco'}

        # Read XML metadata record from given URL
        try:
            metadata = requests.get(metadata_url)
        except Exception as e:
            print(f"Cannot retrieve URL {metadata_url}\n", e)
            return False

        # Parse XML metadata record
        root = etree.fromstring(bytes(metadata.text, 'utf-8'))
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
        result = []
        while len(result) == 0 and len(xpath_list) > 1:
            xpath = '/' + '/'.join(xpath_list)
            #print(xpath)
            result = root.xpath(xpath, namespaces=ns)
            xpath_list.pop()

        # Insert 'online_root' and any other required elements 
        leftovers = master_xpath_list[len(xpath_list):]
        child = result[0]
        for elemtag in leftovers[1:]:
            tagtag = elemtag.split(':')[1] 
            newtag = '{http://www.isotc211.org/2005/gmd}' + tagtag 
            if tagtag != 'BLAH':
                #print(f'Inserting {newtag=} @ {child=}')
                child = etree.SubElement(child, newtag, nsmap=ns)
            else:
                #print(f'Inserting {online_root=} @ {child=}')
                child.append(online_root)
                break
        
        xml_string = etree.tostring(root, pretty_print=True).decode("utf-8")
        #print("\n\n\nROOT:")
        #print(etree.tostring(root, pretty_print=True).decode("utf-8"))
        # write to disk
        with open(f"{model_endpath}.xml", 'w') as ff:
            ff.write(xml_string)

        return True


if __name__ == "__main__":
    metadata_url = "http://www.ntlis.nt.gov.au/metadata/export_data?type=xml&metadata_id=1080195AEBC6A054E050CD9B214436A1"
    #metadata_url = 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Windimurra_2015.xml'
    ce = ISO19139Extractor2()
    ce.write_record('windimurra', metadata_url)
