#!/usr/bin/env python3

import sys
import os
import requests
import json 
from pathlib import Path
import datetime
import geojson
from urllib.parse import urlparse

from pygeometa.core import render_j2_template

from extractor import Extractor

from constants import OUTPUT_DIR

class CkanExtractor(Extractor):
    """ Connects to CKAN repository
        Uses Jinja templates to create ISO 19115-3 XML
        Writes XML to disk
    """

    def output_xml(self, ckan_dict, url, model_endpath, output_file):
        """
        Outputs XML

        :param ckan_dict: information gathered from CKAN
        :param url: CKAN API record URL
        :param model_endpath: models path name
        :param output_file: output filename e.g. 'blah.xml'
        """
        try:
            extent = geojson.loads(ckan_dict['GeoJSONextent'])
            coords = extent.coordinates[0]
            bbox = [coords[0][0], coords[1][1], coords[2][0], coords[3][1]]
        except Exception:
            bbox = [154.3, 109.1, -43.9, -10.6]

        # CKAN URL for purposes of showing in lineage
        up = urlparse(url)
        lineage_url = f"{up.scheme}://{up.netloc}{up.path}"

        # Assemble dict for jinja template
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
                "dataseturi": url,
                "model_endpath": model_endpath,
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
            "distribution": [
                {
                    "url": ckan_dict['resources'][0]['url'],
                    "type": "WWW:LINK",
                    "rel": "service",
                    "name": {
                        "en": ckan_dict['resources'][0]['name'],
                    },
                    "description": {
                        "en": "3D Model Download",
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
                    "statement": f"This metadata record was reproduced from CKAN metadata retrieved from {lineage_url} with package_id {ckan_dict['id']} on {datetime.datetime.now():%d %b %Y}"
                }
            }
        }

        xml_string = render_j2_template(mcf_dict, template_dir='../data/templates/ISO19115-3')

        # write to disk
        with open(os.path.join(OUTPUT_DIR, output_file), 'w') as ff:
            ff.write(xml_string)


    def write_record(self, name, bbox, model_endpath, ckan_url, package_id, output_file):
        """
        Write out XML for a CKAN record

        :param name: name of model
        :param bbox: bounding box NB: We don't use the 'bbox' parameter, we use the metadata record's coords instead
        :param model_endpath: end of model's URL path 
        :param ckan_url: URL to CKAN website
        :param package_id: CKAN package id of record
        :param output_file: output filename e.g. 'blah.xml'
        """
        print(f"Converting: {model_endpath}")
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
            self.output_xml(dict['result'], r.url, model_endpath, output_file)
            return True
        return False


# Used for testing only
if __name__ == "__main__":
    SITE__URL = 'https://geoscience.data.qld.gov.au'
    ce = CkanExtractor()
    ce.write_record('Mt Dore', 'mtdore', SITE__URL, 'ds000002', 'test_ckan.xml')
