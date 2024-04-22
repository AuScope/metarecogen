#!/usr/bin/env python3
import os
import sys
import glob
import json

from pyproj import CRS, Transformer

from oai_extract import OaiExtractor
from ckan_extract import CkanExtractor
from ISO19139_extract import ISO19139Extractor
from ISO19115_3_extract import ISO19115_3Extractor
from pdf_extract import PDFExtractor

from config import CONFIG, OUTPUT_DIR

"""
Create ISO19139 or ISO19115-3 XML metadata records from PDF reports or online metadata services
(e.g. CKAN, dSpace, geonetwork)
"""

def convert(extractor, param_list):
    """
    Runs conversion process

    :param extractor: 'Extractor' class instance
    :param param_list: parameters for extraction process
    """
    e = extractor()
    for params in param_list:
        try:
            e.write_record(**params)
        except TypeError as te:
            print(f"Python Error in {params}\n{te}\n\nPlease check config.py file")
            sys.exit(1)


def get_model_info():
    """
    Extracts a little info from model files

    :returns: a dict: key is model name, val is (south, west, north, east) tuple in EPSG:4326 coords in degrees
    """
    SRC_DIR = os.path.join("geomodelportal", "ui", "src", "assets", "geomodels")
    r_dict = {}
    for jfile in glob.glob(os.path.join(SRC_DIR, "*.json")):
        with open(jfile) as fd:
            # Skip 'ProviderModelInfo.json' it is not a model file
            if jfile[-22:] == 'ProviderModelInfo.json':
                continue
            jobj = json.load(fd)
            props = jobj['properties']
            to_crs = CRS.from_epsg(4326)
            from_crs = CRS.from_string(props['crs'])
            transformer = Transformer.from_crs(from_crs, to_crs)
            west, east, south, north = props['extent']
            name = props['name']
            southLat, westLong = transformer.transform(west, south)
            northLat, eastLong = transformer.transform(east, north)
            
            r_dict[name] = {'south': southLat, 'west': westLong, 'north': northLat, 'east': eastLong}
    return r_dict

def oaipmh_convert(param_list):
    """
    Get records from Northern Territory Geological Service
    """
    OAI__URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'
    oe = OaiExtractor(OAI__URL, 'output')
    for params in param_list:
        oe.write_record(**params)

if __name__ == "__main__":
    # Get cooordinates from geomodels JSON config
    coord_dict = get_model_info()

    # Create output dir
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.mkdir(OUTPUT_DIR)
        except OSError as oe:
            print(f"ERROR: Cannot create output dir {OUTPUT_DIR}: {oe}")
            sys.exit(1)

    # Loop over datasets and process each one
    for k, v in CONFIG.items():
        if v['method'] is None:
            continue
        param_list = v['params']
        for params in param_list:
            name = params['name']
            params['bbox'] = coord_dict[name]

        if v['method'] == 'PDF':
            convert(PDFExtractor, param_list)

        elif v['method'] == 'CKAN':
            convert(CkanExtractor, param_list)

        elif v['method'] == 'ISO19115-3':
            convert(ISO19115_3Extractor, param_list)

        elif v['method'] == 'ISO19139':
            convert(ISO19139Extractor, param_list)

        elif v['method'] == 'OAIPMH':
            oaipmh_convert(param_list)
