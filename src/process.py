#!/usr/bin/env python3

from oai_extract import OaiExtractor
from ckan_extract import CkanExtractor
from ISO19139_extract2 import ISO19139Extractor2

"""
Create ISO19139 or ISO19115-3 XML metadata records from PDF reports or online metadata services
(e.g. CKAN, dSpace, geonetwork)
"""
STATES = {
        #
        # Victoria has some PDF reports 
        'vic': { 'method': 'PDF',
                    'params': { 'URLS': [ ] }
                  },
        #
        # Tasmania's metadata is not available yet
        'tas': { 'method': None },
        #
        # NSW has no sources
        'nsw': { 'method': None },
        #
        # GA has no sources
        'ga': { 'method': None },
        #
        # QLD has a CKAN repo
        'qld': { 'method': 'CKAN',
                 'params': [ { 'model_endpath': 'quamby',
                               'ckan_url': 'https://geoscience.data.qld.gov.au',
                               'package_id': 'ds000006'
                             },
                             { 'model_endpath': 'mtdore',
                               'ckan_url': 'https://geoscience.data.qld.gov.au',
                               'package_id': 'ds000002'
                             }
                 ]
               },
        #
        # SA has a geonetwork with ISO19115-3 records
        'sa': { 'method': 'ISO191115-3',
                'params': [  { 'model_endpath': 'burramine',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/37e0f6f0-b9c7-47f0-bbed-482ce35851a4/formatters/xml'
                             },
                             { 'model_endpath': 'centralflinders',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/2369469b-4906-4352-9100-632974e0ec04/formatters/xml'
                             },
                             { 'model_endpath': 'northflinders',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/a86d7379-ca96-4e7d-8e1f-58bfeba9a8f5/formatters/xml'
                             },
                             { 'model_endpath': 'ngawler',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml'
                             },
                             { 'model_endpath': 'curnamonased',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/bda114bc-1eb8-4569-94e5-a9fa1a994645/formatters/xml'
                             },
                             { 'model_endpath': 'westgawler',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/13ed6259-1ceb-4728-848f-35e81b502d12/formatters/xml'
                             }
                ]
              },
        #
        # NT has an OAI-PMH interface and ISO19139 records
        'nt': { 'method': 'ISO19139',
                 'params': [  { 'model_endpath': 'mcarthur',
                                'metadata_url': 'http://www.ntlis.nt.gov.au/metadata/export_data?type=xml&metadata_id=1080195AEBC6A054E050CD9B214436A1'    }
                 ]
               },
        # NT has an OAI-PMH interface and ISO19139 records
        #'nt': { 'method': 'OAIPMH',
        #         'params': [  { 'model_endpath': 'mcarthur',
        #                        'bbox': [154.3, 109.1, -43.9, -10.6],
        #                        'oai_id': 'oai:geoscience.nt.gov.au:1/81751',
        #                        'oai_prefix': 'oai_dc',
        #                        'service_name': "NTGS GEMIS"
        #                    }
        #         ]
        #       },

        # WA has ISO19139 records 
        'wa': { 'method': 'ISO19139',
                'params': [{ 'model_endpath': 'sandstone',
                            'metadata_url': 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Sandstone_2015.xml'
                          },
                          { 'model_endpath': 'windimurra',
                            'metadata_url': 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Windimurra_2015.xml'
                          }
                ]
              }
}

def pdf_convert(param_list):
    pass

def ckan_convert(param_list):
    ce = CkanExtractor()
    for params in param_list:
        ce.write_record(**params)

def ISO19139_convert(param_list):
    ie = ISO19139Extractor2()
    for params in param_list:
        ie.write_record(**params)

def oaipmh_convert(param_list):
    # Get records from Northern Territory Geological Service
    # OAI-PMH URL
    OAI__URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'
    oe = OaiExtractor(OAI__URL, 'output')
    for params in param_list:
        oe.write_record(**params)

if __name__ == "__main__":
    for k,v in STATES.items():
        if v['method'] == 'PDF':
            pdf_convert(v['params'])
        elif v['method'] == 'CKAN':
            ckan_convert(v['params'])
        elif v['method'] == 'ISO19139':
            ISO19139_convert(v['params'])
        elif v['method'] == 'OAIPMH':
            oaipmh_convert(v['params'])
