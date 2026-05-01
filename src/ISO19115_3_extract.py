#!/usr/bin/env python3

import os
import requests
from lxml import etree as ET
import lxml

from extractor import Extractor

from add_model_keyw import add_models_keyword
from local_types import Coords

from xmlns import iso19115_3_ns, insert

class ISO19115_3Extractor(Extractor):
    """
    Retrieves ISO 19115-3 XML from a geonetwork server or similar
    Uses an XSLT to insert extra fields
    Outputs ISO 19115-3 XML to file
    Returns True upon success
    """

    def write_record(self, name: str, bbox: Coords, model_endpath: str, metadata_url: str, output_file: str) -> bool:
        """
        Writes out ISO 19115-3 XML from an ISO 19115-3 source

        :param name: name of model
        :param bbox: 2D bounding box. This parameter is not used, we retain the record's coords instead
        :param model_endpath: model path
        :param metadara_url: URL of metadata record or a local filename
        :param output_file: name of output file e.g. 'blah.xml'
        :returns: boolean
        """
        print(f"Converting: {model_endpath}")
        # Is this a URL ?
        if metadata_url[:8] == "https://":
            # Read XML from URL
            try:
                metadata = requests.get(metadata_url)
            except Exception as e:
                print(f"Cannot retrieve URL {metadata_url}\n{e}\n")
                return False
            if metadata.encoding is not None:
                encoding = metadata.encoding
            else:
                encoding = 'utf-8'
            metadata_text = metadata.text
        else:
            # Is this a file ?
            try:
                with open(metadata_url, "r") as fp:
                    lines = fp.readlines()
                    metadata_text = ""
                    for line in lines:
                        metadata_text += line.strip(" \t\n")
            except Exception as e:
                print(f"Cannot read XML file {metadata_url}\n{e}\n")
                return False
            encoding = 'utf-8'


        # XML snippet to be inserted into XML record
        insert_txt = f"""<mrd:onLine xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
                                     xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0"
                                     xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0">
            <cit:CI_OnlineResource>
              <cit:linkage>
                <gco:CharacterString>https://geomodels.auscope.org.au/model/{model_endpath}</gco:CharacterString>
              </cit:linkage>
              <cit:protocol>
                <gco:CharacterString>WWW:LINK-1.0-http--link</gco:CharacterString>
              </cit:protocol>
              <cit:name>
                <gco:CharacterString>3D Geological Model</gco:CharacterString>
              </cit:name>
            </cit:CI_OnlineResource>
          </mrd:onLine>
        """

        # Stylesheet to do the insertion
        # Path is '/mdb:MD_Metadata/mdb:distributionInfo/mrd:MD_Distribution/mrd:transferOptions/mrd:MD_DigitalTransferOptions'
        insert_point_xpath_list = ['mdb:MD_Metadata','mdb:distributionInfo','mrd:MD_Distribution',
                'mrd:transferOptions','mrd:MD_DigitalTransferOptions','mri:BLAH']
        # Parse XML
        parser = ET.XMLParser(recover=False, remove_blank_text=True)
        try:
            root = ET.fromstring(bytes(metadata_text, encoding), parser=parser)
        except lxml.etree.XMLSyntaxError as xse:
            print(f"Error in {metadata_text}: {xse}")
            return False
        result = insert(root, insert_txt, insert_point_xpath_list, iso19115_3_ns)

        byte_result = ET.tostring(result, pretty_print=True)
        if byte_result is not None:
            str_result = byte_result.decode('utf-8')
            # Replace header because geonetwork will not accept old header
            str_result = str_result.replace("""<mdb:MD_Metadata xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0" xmlns:cat="http://standards.iso.org/iso/19115/-3/cat/1.0" xmlns:gfc="http://standards.iso.org/iso/19110/gfc/1.1" xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0" xmlns:gcx="http://standards.iso.org/iso/19115/-3/gcx/1.0" xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0" xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0" xmlns:srv="http://standards.iso.org/iso/19115/-3/srv/2.0" xmlns:mas="http://standards.iso.org/iso/19115/-3/mas/1.0" xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0" xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0" xmlns:mda="http://standards.iso.org/iso/19115/-3/mda/1.0" xmlns:mds="http://standards.iso.org/iso/19115/-3/mds/1.0" xmlns:mdt="http://standards.iso.org/iso/19115/-3/mdt/1.0" xmlns:mex="http://standards.iso.org/iso/19115/-3/mex/1.0" xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0" xmlns:mpc="http://standards.iso.org/iso/19115/-3/mpc/1.0" xmlns:mrc="http://standards.iso.org/iso/19115/-3/mrc/1.0" xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0" xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0" xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0" xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0" xmlns:msr="http://standards.iso.org/iso/19115/-3/msr/1.0" xmlns:mdq="http://standards.iso.org/iso/19157/-2/mdq/1.0" xmlns:mac="http://standards.iso.org/iso/19115/-3/mac/1.0" xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mds/1.0 http://standards.iso.org/iso/19115/-3/mds/1.0/mds.xsd">""",
                   """<mdb:MD_Metadata xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/2.0" xmlns:cat="http://standards.iso.org/iso/19115/-3/cat/1.0" xmlns:gfc="http://standards.iso.org/iso/19110/gfc/1.1" xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/2.0" xmlns:gcx="http://standards.iso.org/iso/19115/-3/gcx/1.0" xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0" xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0" xmlns:srv="http://standards.iso.org/iso/19115/-3/srv/2.1" xmlns:mas="http://standards.iso.org/iso/19115/-3/mas/1.0" xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0" xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0" xmlns:mda="http://standards.iso.org/iso/19115/-3/mda/1.0" xmlns:mds="http://standards.iso.org/iso/19115/-3/mds/2.0" xmlns:mdt="http://standards.iso.org/iso/19115/-3/mdt/2.0" xmlns:mex="http://standards.iso.org/iso/19115/-3/mex/1.0" xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0" xmlns:mpc="http://standards.iso.org/iso/19115/-3/mpc/1.0" xmlns:mrc="http://standards.iso.org/iso/19115/-3/mrc/2.0" xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0" xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0" xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/2.0" xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0" xmlns:msr="http://standards.iso.org/iso/19115/-3/msr/2.0" xmlns:mdq="http://standards.iso.org/iso/19157/-2/mdq/1.0" xmlns:mac="http://standards.iso.org/iso/19115/-3/mac/2.0" xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mds/2.0 http://standards.iso.org/iso/19115/-3/mds/2.0/mds.xsd">""")

            # Add '3D Geomodels' keyword
            xml_string = add_models_keyword(str_result, 'utf-8', 'ISO19115-3')

            # Write to disk
            with open(os.path.join(self.output_dir, output_file), 'w') as ff:
                ff.write(xml_string)

            return True
        return False


