#!/usr/bin/env python3

import sys
import requests
from lxml import etree

from extractor import Extractor

from add_model_keyw import add_models_keyword

class ISO19115_3Extractor(Extractor):
    """
    Retrieves ISO 19115-3 XML from a geonetwork server or similar
    Uses an XSLT to insert extra fields
    Outputs ISO 19115-3 XML to file
    """

    def write_record(self, name, bbox, model_endpath, metadata_url):
        """
        Writes out ISO 19115-3 XML from an ISO 19115-3 source

        :param name: name of model
        :param bbox: 2D bounding box. This parameter is not used, we use records' coords instead
        :param model_endpath: model path
        :param metadara_url: URL of metadata record
        :returns: boolean
        """
        print(f"Converting: {model_endpath}")
        # Read XML from URL
        try:
            metadata = requests.get(metadata_url)
        except Exception as e:
            print(f"Cannot retrieve URL {metadata_url}\n", e)
            return False
        if metadata.encoding is not None:
            encoding = metadata.encoding
        else:
            encoding = 'utf-8'

        # XML Namespaces
        ns = {'cit': 'http://standards.iso.org/iso/19115/-3/cit/2.0',
              'mrd': 'http://standards.iso.org/iso/19115/-3/mrd/1.0',
              'gco': 'http://www.isotc211.org/2005/gco'}

        # XML snippet to be inserted into XML record
        model_online = f"""<mrd:onLine>
            <cit:CI_OnlineResource>
              <cit:linkage>
                <gco:CharacterString>http://geomodels.auscope.org/model/mcarthur</gco:CharacterString>
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
        xslt = f"""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                 xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0"
                 xmlns:cat="http://standards.iso.org/iso/19115/-3/cat/1.0"
                 xmlns:gfc="http://standards.iso.org/iso/19110/gfc/1.1"
                 xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0"
                 xmlns:gcx="http://standards.iso.org/iso/19115/-3/gcx/1.0"
                 xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0"
                 xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0"
                 xmlns:srv="http://standards.iso.org/iso/19115/-3/srv/2.0"
                 xmlns:mas="http://standards.iso.org/iso/19115/-3/mas/1.0"
                 xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0"
                 xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0"
                 xmlns:mda="http://standards.iso.org/iso/19115/-3/mda/1.0"
                 xmlns:mds="http://standards.iso.org/iso/19115/-3/mds/1.0"
                 xmlns:mdt="http://standards.iso.org/iso/19115/-3/mdt/1.0"
                 xmlns:mex="http://standards.iso.org/iso/19115/-3/mex/1.0"
                 xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0"
                 xmlns:mpc="http://standards.iso.org/iso/19115/-3/mpc/1.0"
                 xmlns:mrc="http://standards.iso.org/iso/19115/-3/mrc/1.0"
                 xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0"
                 xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0"
                 xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0"
                 xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0"
                 xmlns:msr="http://standards.iso.org/iso/19115/-3/msr/1.0"
                 xmlns:mdq="http://standards.iso.org/iso/19157/-2/mdq/1.0"
                 xmlns:mac="http://standards.iso.org/iso/19115/-3/mac/1.0"
                 xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0"
                 xmlns:gml="http://www.opengis.net/gml/3.2"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mds/1.0 http://standards.iso.org/iso/19115/-3/mds/1.0/mds.xsd">

<xsl:output method="xml" indent="yes"/>

<!-- Copies everything -->
<xsl:template match="@*|node()">
   <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
   </xsl:copy>
</xsl:template>

<xsl:template match="/mdb:MD_Metadata/mdb:distributionInfo/mrd:MD_Distribution/mrd:transferOptions/mrd:MD_DigitalTransferOptions">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     {model_online} 
  </xsl:copy>
</xsl:template>

<xsl:template match="/mdb:MD_Metadata/mdb:distributionInfo/mrd:MD_Distribution/mrd:transferOptions[not(mrd:MD_DigitalTransferOptions)]">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     <mrd:MD_DigitalTransferOptions>
     {model_online} 
     </mrd:MD_DigitalTransferOptions>
  </xsl:copy>
</xsl:template>

<xsl:template match="/mdb:MD_Metadata/mdb:distributionInfo/mrd:MD_Distribution[not(mrd:transferOptions)]">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     <mrd:transferOptions>
        <mrd:MD_DigitalTransferOptions>
        {model_online} 
        </mrd:MD_DigitalTransferOptions>
     </mrd:transferOptions>
  </xsl:copy>
</xsl:template>

<xsl:template match="/mdb:MD_Metadata/mdb:distributionInfo[not(mrd:MD_Distribution)]">
  <xsl:copy>
     <xsl:apply-templates select="@*|node()"/>
     <mrd:MD_Distribution>
        <mrd:transferOptions>
           <mrd:MD_DigitalTransferOptions>
           {model_online} 
           </mrd:MD_DigitalTransferOptions>
        </mrd:transferOptions>
     </mrd:MD_Distribution>
  </xsl:copy>
</xsl:template>

<xsl:template match="/mdb:MD_Metadata[not(mdb:distributionInfo)]">
<xsl:copy>
   <xsl:apply-templates select="@*|node()"/>
   <mdb:distributionInfo>
      <mrd:MD_Distribution>
         <mrd:transferOptions>
            <mrd:MD_DigitalTransferOptions>
            {model_online} 
            </mrd:MD_DigitalTransferOptions>
         </mrd:transferOptions>
      </mrd:MD_Distribution>
   </mdb:distributionInfo>
</xsl:copy>
</xsl:template>

</xsl:stylesheet>""".encode(encoding)
        #print(f'{xslt=}')
        parser = etree.XMLParser(recover=False)
        doc = etree.fromstring(bytes(metadata.text, encoding), parser=parser)
        #print(f'{doc=}')
        #for child in doc:
        #    print(child)
        xslt_tree = etree.XML(xslt)
        transform = etree.XSLT(xslt_tree)
        result = transform(doc)
        #print(f"{result=}")
        #print(f'{transform.error_log=}')
        byte_result = etree.tostring(result, pretty_print=True)
        #print(f"{byte_result=}")
        if byte_result is not None:
            str_result = byte_result.decode('utf-8')
            # Replace header because geonetwork will not accept old header
            str_result = str_result.replace("""<mdb:MD_Metadata xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/1.0" xmlns:cat="http://standards.iso.org/iso/19115/-3/cat/1.0" xmlns:gfc="http://standards.iso.org/iso/19110/gfc/1.1" xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0" xmlns:gcx="http://standards.iso.org/iso/19115/-3/gcx/1.0" xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0" xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0" xmlns:srv="http://standards.iso.org/iso/19115/-3/srv/2.0" xmlns:mas="http://standards.iso.org/iso/19115/-3/mas/1.0" xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0" xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0" xmlns:mda="http://standards.iso.org/iso/19115/-3/mda/1.0" xmlns:mds="http://standards.iso.org/iso/19115/-3/mds/1.0" xmlns:mdt="http://standards.iso.org/iso/19115/-3/mdt/1.0" xmlns:mex="http://standards.iso.org/iso/19115/-3/mex/1.0" xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0" xmlns:mpc="http://standards.iso.org/iso/19115/-3/mpc/1.0" xmlns:mrc="http://standards.iso.org/iso/19115/-3/mrc/1.0" xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0" xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0" xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0" xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0" xmlns:msr="http://standards.iso.org/iso/19115/-3/msr/1.0" xmlns:mdq="http://standards.iso.org/iso/19157/-2/mdq/1.0" xmlns:mac="http://standards.iso.org/iso/19115/-3/mac/1.0" xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mds/1.0 http://standards.iso.org/iso/19115/-3/mds/1.0/mds.xsd">""",
                   """<mdb:MD_Metadata xmlns:mdb="http://standards.iso.org/iso/19115/-3/mdb/2.0" xmlns:cat="http://standards.iso.org/iso/19115/-3/cat/1.0" xmlns:gfc="http://standards.iso.org/iso/19110/gfc/1.1" xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/2.0" xmlns:gcx="http://standards.iso.org/iso/19115/-3/gcx/1.0" xmlns:gex="http://standards.iso.org/iso/19115/-3/gex/1.0" xmlns:lan="http://standards.iso.org/iso/19115/-3/lan/1.0" xmlns:srv="http://standards.iso.org/iso/19115/-3/srv/2.1" xmlns:mas="http://standards.iso.org/iso/19115/-3/mas/1.0" xmlns:mcc="http://standards.iso.org/iso/19115/-3/mcc/1.0" xmlns:mco="http://standards.iso.org/iso/19115/-3/mco/1.0" xmlns:mda="http://standards.iso.org/iso/19115/-3/mda/1.0" xmlns:mds="http://standards.iso.org/iso/19115/-3/mds/2.0" xmlns:mdt="http://standards.iso.org/iso/19115/-3/mdt/2.0" xmlns:mex="http://standards.iso.org/iso/19115/-3/mex/1.0" xmlns:mmi="http://standards.iso.org/iso/19115/-3/mmi/1.0" xmlns:mpc="http://standards.iso.org/iso/19115/-3/mpc/1.0" xmlns:mrc="http://standards.iso.org/iso/19115/-3/mrc/2.0" xmlns:mrd="http://standards.iso.org/iso/19115/-3/mrd/1.0" xmlns:mri="http://standards.iso.org/iso/19115/-3/mri/1.0" xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/2.0" xmlns:mrs="http://standards.iso.org/iso/19115/-3/mrs/1.0" xmlns:msr="http://standards.iso.org/iso/19115/-3/msr/2.0" xmlns:mdq="http://standards.iso.org/iso/19157/-2/mdq/1.0" xmlns:mac="http://standards.iso.org/iso/19115/-3/mac/2.0" xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mds/2.0 http://standards.iso.org/iso/19115/-3/mds/2.0/mds.xsd">""")

            # Add '3D Geomodels' keyword and write to disk
            add_models_keyword(model_endpath, str_result, 'utf-8', 'ISO19115-3')
            return True
        return False


# Used for testing only
if __name__ == "__main__":
    metadata_url = "https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml"

    ce = ISO19115_3Extractor()
    ce.write_record('ngawler', metadata_url)
