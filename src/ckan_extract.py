#!/usr/bin/env python3

import sys
import requests
import json 
from pathlib import Path
import datetime
import geojson
from geojson import Polygon

from pygeometa.core import read_mcf, render_j2_template



def output_xml(ckan_dict, url):
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
    print(xml_string)

    # write to disk
    with open('output.xml', 'w') as ff:
        ff.write(xml_string)


def get_ckan_dict(ckan_url, package_id):
    url_path =  Path('api') / '3' / 'action' / 'package_show'
    url = f'{ckan_url}/{url_path}'
    # print("URL=", url)
    r = requests.get(url, params={'q':'type:report', 'id':package_id})
    try:
        dict = json.loads(r.text)
    except json.JSONDecodeError:
        return {}, r.url
    if dict['success'] is True:
        return dict['result'], r.url
    return {}, r.url

if __name__ == "__main__":
    site_url = 'https://geoscience.data.qld.gov.au'
    ckan_dict, url = get_ckan_dict(site_url,'ds000002')
    output_xml(ckan_dict, url)    

