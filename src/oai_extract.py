#!/usr/bin/env python3
import os
import sys
import datetime

from pygeometa.core import render_j2_template
from sickle import Sickle

from extractor import Extractor
from constants import OUTPUT_DIR


class OaiExtractor(Extractor):

    def __init__(self, oai_url, output_dir):
        self.OAI_URL = oai_url
        self.output_dir = output_dir

    def output_xml(self, oai_dict, oai_id, bbox, model_endpath, service_name, output_file):
        """
        Uses jinja template to write to file OAI-PMH metadata as an ISO 19115-3 XML record

        :param oai_dict: metadata dictionary to be output
        :param oai_id: OAI-PMH identifier e.g. 'oai:eprints.rclis.org:4088'
        :param bbox: bounding box dict, keys are 'north' 'south' 'east' 'west', values are decimals as strings, EPSG:4326 is assumed
        :param model_endpath: path of model in website
        :param service_name: generic name of OAI-PMH service
        :param output_file: name of xml file e.g. 'blah.xml'
        :returns: boolean success indicator
        """
        bbox_list = [str(bbox['west']), str(bbox['east']), str(bbox['south']), str(bbox['north'])]
        mcf_dict = {
            "mcf": {
                "version": 1.0
            },
            "metadata": {
                "identifier": oai_dict['identifier'][0],
                "language": "en",
                "charset": "utf8",
                "parentidentifier": "",
                "hierarchylevel": "dataset",
                "datestamp": oai_dict['relation'][2],
                "dataseturi": oai_dict['identifier'][3],
                "model_endpath": model_endpath
            },
            "spatial": {
                "datatype": "tin",
                "geomtype": "composite"
            },
            "identification": {
                "language": "eng; AUS",
                "charset": "utf8",
                "title": {
                    "en": oai_dict['title'][0],
                },
                "abstract": {
                    "en": oai_dict['description'][0],
                },
                "dates": {
                    "creation": oai_dict['date'][0],
                    "publication": oai_dict['date'][1]
                },
                "keywords": {
                    "default": {
                        "keywords": {
                            "en": oai_dict['subject'][0]
                        }
                    }
                },
                "topiccategory": [
                    "geoscientificInformation"
                ],
                "extents": {
                    "spatial": [
                        {
                            "bbox": bbox_list,
                            "crs": "4326"
                        }
                    ]
                },
                "fees": "None",
                "accessconstraints": "license",
                "rights": {
                    "en": ' '.join(oai_dict['rights']),
                },
                "url": oai_dict['identifier'][3],
                "status": "completed",
                "maintenancefrequency": "continual"
            },
            "contact": {
                "distributor": {
                    "organization": oai_dict['publisher'][0]
                }
            },
            "distribution": [
                {
                    "url": oai_dict['identifier'][3],
                    "type": "WWW:LINK",
                    "rel": "service",
                    "name": {
                        "en": ' '.join(oai_dict['type']),
                    },
                    "description": {
                        "en": ' '.join(oai_dict['type']),
                    },
                    "function": "download"
                },
                {
                    "url": f"http://geomodels.auscope.org.au/model/{model_endpath}",
                    "type": "WWW:LINK",
                    "rel": "service",
                    "name": {
                        "en": "3D Geological model website",
                    },
                    "description": {
                        "en": "3D Geological model website",
                    },
                    "function": "website"
                }
            ],
            "dataquality": {
                "scope": {
                    "level": "dataset"
                },
                "lineage": {
                    "statement": f"This record was created using metadata sourced from the {service_name} OAI-PMH service with URL {self.OAI_URL} and identifier {oai_id} on {datetime.datetime.now():%d %b %Y}. The metadata and dataset can be reached from {oai_dict['identifier'][3]}"
                }
            }
        }

        xml_string = render_j2_template(mcf_dict, template_dir='../data/templates/ISO19115-3')

        # write to disk
        with open(os.path.join(OUTPUT_DIR, output_file), 'w') as ff:
            ff.write(xml_string)
        return True



    def write_record(self, name, bbox, model_endpath, oai_id, oai_prefix, service_name, output_file):
        """
        Write an XML record to file using metadata from OAI-PMH service

        :param bbox: bounding box dict, keys are 'north' 'south' 'east' 'west', values are decimals as strings, EPSG:4326 is assumed
        :param model_endpath: path of model in website
        :param oai_id: OAI-PMH identifier e.g. 'oai:eprints.rclis.org:4088'
        :param oai_prefix: OAI-PMH prefix e.g. 'oai_dc'
        :param service_name: generic name of OAI-PMH service
        :param output_file: name of xml file e.g. 'blah.xml'
        :returns: boolean success indicator
        """
        print(f"Converting: {model_endpath}")
        # Open connection to OAI-PMH
        sickle = Sickle(self.OAI_URL)
        rec = sickle.GetRecord(identifier=oai_id, metadataPrefix=oai_prefix)

        oai_dict = rec.get_metadata()
        #for k, v in oai_dict.items():
        #    print(k, '=>', v);

        self.output_xml(oai_dict, oai_id, bbox, model_endpath, service_name, output_file)

if __name__ == "__main__":
    # Get records from Northern Territory Geological Service
    # OAI-PMH URL
    OAI__URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'
    
    # GEMIS permanent link of McArthur 3D model
    MODEL__URL = 'https://geoscience.nt.gov.au/gemis/ntgsjspui/handle/1/81751'
    oe = OaiExtractor(OAI__URL, 'output')
    # Convert perm link to OAI-PMH ID
    handle_id = '/'.join(MODEL__URL.split('/')[-2:])
    print(handle_id)
    # NB: Some geological fields that are present in GEMIS website are missing from OAI output with 'oai_dc' prefix,
    # i.e. "Stratigraphy" The 'xoai' prefix will allow extraction of these missing fields but the XML output
    # would need to be parsed
    oe.write_record([154.3, 109.1, -43.9, -10.6], 'mcarthur', 'oai:geoscience.nt.gov.au:'+handle_id, 'oai_dc', "NTGS GEMIS", 'test_oai.xml')

