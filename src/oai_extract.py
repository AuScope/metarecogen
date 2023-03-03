#!/usr/bin/env python3
import sys
import datetime

from pygeometa.core import render_j2_template
from sickle import Sickle

# Get records from Northern Territory Geological Service

# OAI-PMH URL
OAI_URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'



def output_xml(oai_dict, bbox, model_endpath):
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
            "dataseturi": oai_dict['source.uri'][0]
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
            }
        },
        "dataquality": {
            "scope": {
                "level": "dataset"
            },
            "lineage": {
                "statement": f"{oai_dict['source.volume'][0]}\nThis metadata record was reproduced from NTGS GEMIS metadata retrieved from {oai_dict['source.uri'][0]} on {datetime.datetime.now():%d %b %Y}"
            }
        }
    }


    xml_string = render_j2_template(mcf_dict, template_dir='../data/templates/ISO19115-3')
    print(xml_string)

    # write to disk
    with open('output.xml', 'w') as ff:
        ff.write(xml_string)


if __name__ == "__main__":
    # GEMIS permanent link of McArthur 3D model
    # TODO: Supply this from model config
    PERM_LINK = 'https://geoscience.nt.gov.au/gemis/ntgsjspui/handle/1/81751'

    # Convert perm link to OAI-PMH ID 
    handle_id = '/'.join(PERM_LINK.split('/')[-2:])

    sickle = Sickle(OAI_URL)

    # NB: Some geological fields that are present in GEMIS website are missing from OAI output with 'oai_dc' prefix,
    # i.e. "Stratigraphy" The 'xoai' prefix will allow extraction of these missing fields but the XML output
    # would need to be parsed
    rec = sickle.GetRecord(identifier='oai:geoscience.nt.gov.au:'+handle_id, metadataPrefix='oai_dc')

    oai_dict = rec.get_metadata()
    for k,v in oai_dict.items():
        print(k, ': ', v)

    # TODO: Supply these 2 from the model config
    bbox = [154.3, 109.1, -43.9, -10.6]
    model_endpath = 'mcarthur'

    output_xml(oai_dict, bbox, model_endpath)    

