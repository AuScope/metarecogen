#!/usr/bin/env python3

import os
import requests
from lxml import etree

from extractor import Extractor
from add_model_keyw import add_models_keyword
from local_types import Coords

class ISO19139Extractor(Extractor):
    """ Uses an XSLT to insert elements into ISO 19139 XML
        Outputs ISO 19139 XML to file
        Returns True upon success
    """

    def write_record(self, name: str, bbox: Coords, model_endpath: str, metadata_url: str, output_file: str) -> bool:
        """
        Reads ISO 19139 from a source adds extra fields and outputs XML to file

        :param name: name of model
        :param bbox: 2D bounding box. This parameter is not used, we retain the record's coords instead
        :param model_endpath: model path
        :param metadara_url: URL of metadata record
        :param output_file: name of output file e.g. 'blah.xml'
        :returns: boolean
        """
        print(f"Converting: {model_endpath}")
        # Read XML from URL
        try:
            metadata = requests.get(metadata_url)
        except Exception as e:
            print(f"Cannot retrieve URL {metadata_url}\n", e)
            return False

        # XML Namespaces
        ns = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gco': 'http://www.isotc211.org/2005/gco'}

        # XML snippet to be inserted into XML record
        model_online = f"""<gmd:onLine>
                  <gmd:CI_OnlineResource>
                     <gmd:linkage>
                        <gmd:URL>https://geomodels.auscope.org.au/model/{model_endpath}</gmd:URL>
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

        # Stylesheet to do the insertion
        # Path is '/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions'
        xslt = f"""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco">

<xsl:output method="xml" indent="yes"/>

<!-- Copies everything -->
<xsl:template match="@*|node()">
   <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
   </xsl:copy>
</xsl:template>

<xsl:template match="/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     {model_online} 
  </xsl:copy>
</xsl:template>

<xsl:template match="/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions[not(gmd:MD_DigitalTransferOptions)]">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     <gmd:MD_DigitalTransferOptions>
     {model_online} 
     </gmd:MD_DigitalTransferOptions>
  </xsl:copy>
</xsl:template>

<xsl:template match="/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution[not(gmd:transferOptions)]">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     <gmd:transferOptions>
        <gmd:MD_DigitalTransferOptions>
        {model_online} 
        </gmd:MD_DigitalTransferOptions>
     </gmd:transferOptions>
  </xsl:copy>
</xsl:template>

<xsl:template match="/gmd:MD_Metadata/gmd:distributionInfo[not(gmd:MD_Distribution)]">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     <gmd:MD_Distribution>
        <gmd:transferOptions>
           <gmd:MD_DigitalTransferOptions>
           {model_online} 
           </gmd:MD_DigitalTransferOptions>
        </gmd:transferOptions>
     </gmd:MD_Distribution>
  </xsl:copy>
</xsl:template>

<xsl:template match="/gmd:MD_Metadata[not(gmd:distributionInfo)]">
<xsl:copy>
   <xsl:apply-templates select="@*|node()"/>
   <gmd:distributionInfo>
      <gmd:MD_Distribution>
         <gmd:transferOptions>
            <gmd:MD_DigitalTransferOptions>
            {model_online} 
            </gmd:MD_DigitalTransferOptions>
         </gmd:transferOptions>
      </gmd:MD_Distribution>
   </gmd:distributionInfo>
</xsl:copy>
</xsl:template>

</xsl:stylesheet>""".encode('utf-8')
        # Recovers from minor syntax errors
        parser = etree.XMLParser(recover=True)
        encoding = 'utf-8'
        if metadata.encoding is not None:
            encoding = metadata.encoding
        doc = etree.fromstring(bytes(metadata.text, encoding), parser=parser)
        xslt_tree = etree.XML(xslt)
        transform = etree.XSLT(xslt_tree)
        result = transform(doc)
        byte_result = etree.tostring(result, pretty_print=True)
        if byte_result is not None:
            str_result = byte_result.decode('utf-8')

            # Add '3D Geological Models' keyword and write to disk
            xml_string = add_models_keyword(str_result, 'utf-8', 'ISO19139')

            # Write to disk
            with open(os.path.join(self.output_dir, output_file), 'w') as ff:
                ff.write(xml_string)
            return True
        return False

