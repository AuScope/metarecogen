#!/usr/bin/env python3
import sys
import datetime

from pygeometa.core import render_j2_template
from sickle import Sickle

from extractor import Extractor

class OaiExtractor(Extractor):

    def __init__(self, oai_url, output_dir):
        self.OAI_URL = oai_url
        self.output_dir = output_dir

    def output_xml(self, oai_dict, bbox, model_endpath, service_name):
        mcf_dict = {
            "mcf": {
                "version": 1.0
            },
            "metadata": {
                "identifier": "",
                "language": "en",
                "charset": "utf8",
                "parentidentifier": "",
                "hierarchylevel": "dataset",
                "datestamp": oai_dict['relation'][2],
                "dataseturi": oai_dict['source.uri'][0],
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
                    "en": oai_dict['description.abstract'][0],
                },
                "dates": {
                    "creation": oai_dict['date.issued'][0],
                    "publication": oai_dict['date.issued'][0]
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
                            "bbox": bbox,
                            "crs": 4326
                        }
                    ]
                },
                "fees": "None",
                "accessconstraints": "license",
                "rights": {
                    "en": ' '.join(oai_dict['rights']),
                },
                "url": oai_dict['source.uri'][0],
                "status": "completed",
                "maintenancefrequency": "continual"
            },
            "contact": {
                "distributor": {
                    "organization": oai_dict['contributor.issuingbody'][0]
                }
            },
            "distribution": {
                "wms": {
                    "url": oai_dict['source.uri'][0],
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
                "www": {
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
            },
            "dataquality": {
                "scope": {
                    "level": "dataset"
                },
                "lineage": {
                    "statement": f"{oai_dict['source.volume'][0]}\nThis metadata record was reproduced from {service_name} metadata retrieved from {oai_dict['source.uri'][0]} on {datetime.datetime.now():%d %b %Y}"
                }
            }
        }

        xml_string = render_j2_template(mcf_dict, template_dir='../data/templates/ISO19115-3')

        # write to disk
        with open(f"{model_endpath}.xml", 'w') as ff:
            ff.write(xml_string)



    def write_record(self, bbox, model_endpath, oai_id, oai_prefix, service_name):
        print("Converting: {model_endpath}")
        # Open connection to OAI-PMH
        sickle = Sickle(self.OAI_URL)
        rec = sickle.GetRecord(identifier=oai_id, metadataPrefix=oai_prefix)

        oai_dict = rec.get_metadata()
        #for k,v in oai_dict.items():
        #    print(k, ': ', v)

        self.output_xml(oai_dict, bbox, model_endpath, service_name)

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
    oe.write_record([154.3, 109.1, -43.9, -10.6], 'mcarthur', 'oai:geoscience.nt.gov.au:'+handle_id, 'oai_dc', "NTGS GEMIS")

