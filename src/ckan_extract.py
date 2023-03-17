#!/usr/bin/env python3

import sys
import requests
import json 
from pathlib import Path
import datetime
import geojson

from pygeometa.core import render_j2_template

from extractor import Extractor

class CkanExtractor(Extractor):

    def output_xml(self, ckan_dict, url, model_endpath):
        # print(json.dumps(ckan_dict, indent=4))
        try:
            extent = geojson.loads(ckan_dict['GeoJSONextent'])
            coords = extent.coordinates[0]
            bbox = [coords[0][0], coords[1][1], coords[2][0], coords[3][1]]
        except Exception:
            bbox = [154.3, 109.1, -43.9, -10.6]
        mcf_dict = {
            "mcf": {
                "version": 1.0
            },
            "metadata": {
                "identifier": ckan_dict['id'],
                "language": "en",
                "charset": "utf8",
                "parentidentifier": "",
                "hierarchylevel": "dataset",
                "datestamp": ckan_dict['metadata_modified'],
                "dataseturi": url
            },
            "spatial": {
                "datatype": "tin",
                "geomtype": "composite"
            },
            "identification": {
                "language": "eng; AUS",
                "charset": "utf8",
                "title": {
                    "en": ckan_dict['title'],
                },
                "abstract": {
                    "en": ckan_dict['notes'],
                },
                "dates": {
                    "creation": ckan_dict['metadata_created'],
                    "publication": ckan_dict['metadata_modified']
                },
                "keywords": {
                    "default": {
                        "keywords": {
                            "en": [
                                "geological models"
                            ]
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
                    "en": f"{ckan_dict['license_title']} ({ckan_dict['license_url']})",
                },
                "url": url,
                "status": "completed",
                "maintenancefrequency": "continual"
            },
            "contact": {
                "distributor": {
                    "organization": ckan_dict['organization']['title']
                }
            },
            "distribution": {
                "wms": {
                    "url": ckan_dict['resources'][0]['url'],
                    "type": "WWW:LINK",
                    "rel": "service",
                    "name": {
                        "en": ckan_dict['resources'][0]['name'],
                    },
                    "description": {
                        "en": ckan_dict['resources'][0]['resource:description'],
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
                    "statement": f"This metadata record was reproduced from CKAN metadata retrieved from '{url}' on {datetime.datetime.now():%d %b %Y}"
                }
            }
        }


        xml_string = render_j2_template(mcf_dict, template_dir='../data/templates/ISO19115-3')

        # write to disk
        with open(f"{model_endpath}.xml", 'w') as ff:
            ff.write(xml_string)


    def write_record(self, model_endpath, ckan_url, package_id):
        # Set up CKAN URL
        url_path =  Path('api') / '3' / 'action' / 'package_show'
        url = f'{ckan_url}/{url_path}'
        # print("URL=", url)
        r = requests.get(url, params={'q':'type:report', 'id':package_id})
        try:
            dict = json.loads(r.text)
        except json.JSONDecodeError:
            return False
        if dict['success'] is True:
            self.output_xml(dict['result'], r.url, model_endpath)
            return True
        return False


if __name__ == "__main__":
    SITE__URL = 'https://geoscience.data.qld.gov.au'
    ce = CkanExtractor()
    ce.write_record(SITE__URL, 'ds000002')