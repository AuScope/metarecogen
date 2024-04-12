"""
Config for creation of ISO19139 or ISO19115-3 XML metadata records from PDF reports or online metadata services
(e.g. CKAN, dSpace, geonetwork)
"""
CONFIG = {
        #
        # Victoria has some PDF reports
        'vic': { 'method': 'PDF',
            'params': [   { 'name': 'Otway Basin',
                            'model_endpath': 'otway',
                            'pdf_file': '../data/reports/vic/G107513_OtwayBasin_3D_notes.pdf',
                            'organisation': "Geological Survey of Victoria",
                            'title': "Otway 3D model",
                            'cutoff': 1000
                            },
                            { 'name': 'Bendigo',
                              'model_endpath': 'bendigo',
                              'pdf_file': '../data/reports/vic/G35615_3DVIC1_pt1.pdf',
                              'organisation': "Geological Survey of Victoria",
                              'title': "Bendigo 3D model",
                              'cutoff': 3000
                            },
                       ],
            },
        #
        # Use PDF version of academic paper for Stuart Shelf model
        'nci': { 'method': 'PDF',
            'params': [ { 'name': 'Stuart Shelf',
                          'model_endpath': 'stuartshalf',
                          'pdf_file': '../data/reports/nci/Heinson-StuShelf.pdf',
                          'organisation': 'NCI/University of Adelaide',
                          'title': 'Stuart Shelf Model',
                          'cutoff': 3000
                          },
                     ],
            },
        #
        # QLD has a CKAN repo
        'qld': { 'method': 'CKAN',
            'params': [ { 'name': 'Quamby',
                          'model_endpath': 'quamby',
                          'ckan_url': 'https://geoscience.data.qld.gov.au',
                          'package_id': 'ds000006'
                        },
                        { 'name': 'Mt Dore',
                          'model_endpath': 'mtdore',
                          'ckan_url': 'https://geoscience.data.qld.gov.au',
                          'package_id': 'ds000002'
                        }
                 ]
               },
        #
        # SA has a geonetwork with ISO19115-3 records
        'sa': { 'method': 'ISO19115-3',
                'params': [  { 'name': 'Burra Mine',
                               'model_endpath': 'burramine',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/37e0f6f0-b9c7-47f0-bbed-482ce35851a4/formatters/xml'
                             },
                             { 'name': 'Central Flinders',
                               'model_endpath': 'centralflinders',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/2369469b-4906-4352-9100-632974e0ec04/formatters/xml'
                             },
                             { 'name': 'North Flinders',
                               'model_endpath': 'northflinders',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/a86d7379-ca96-4e7d-8e1f-58bfeba9a8f5/formatters/xml'
                             },
                             { 'name': 'North Gawler',
                               'model_endpath': 'ngawler',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml'
                             },
                             { 'name': 'Curnamona Sedimentary Basins',
                               'model_endpath': 'curnamonased',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/bda114bc-1eb8-4569-94e5-a9fa1a994645/formatters/xml'
                             },
                             { 'name': 'Western Gawler',
                               'model_endpath': 'westgawler',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/13ed6259-1ceb-4728-848f-35e81b502d12/formatters/xml'
                             }
                ]
              },
        # Burra.pdf  CurnamonaSed.pdf
        'sa-test': { 'method': 'PDF',
            'params': [ { 'name': 'Burra Mine',
                          'model_endpath': 'burramine',
                          'pdf_file': '../data/reports/sa/Burra.pdf',
                          'organisation': 'South Australia Geological Survey',
                          'title': 'Burra Mine Test',
                          'cutoff': 3000
                          },
                       { 'name': 'Curnamona Sedimentary Basins',
                          'model_endpath': 'curnamonased',
                          'pdf_file': '../data/reports/sa/CurnamonaSed.pdf',
                          'organisation': 'South Australia Geological Survey',
                          'title': 'Curnamona Sed Basins Test',
                          'cutoff': 3000
                          },
                     ],
            },
        #
        # NT has ISO19139 records
        'nt': { 'method': 'ISO19139',
                'params': [  { 'name': 'McArthur Basin',
                               'model_endpath': 'mcarthur',
                               'metadata_url': 'http://www.ntlis.nt.gov.au/metadata/export_data?type=xml&metadata_id=1080195AEBC6A054E050CD9B214436A1'    }
                 ]
               },
        # NT also has an OAI-PMH interface
        #'nt': { 'method': 'OAIPMH',
        #         'params': [  { 'model_endpath': 'mcarthur',
        #                        'oai_id': 'oai:geoscience.nt.gov.au:1/81751',
        #                        'oai_prefix': 'oai_dc',
        #                        'service_name': "NTGS GEMIS"
        #                    }
        #         ]
        #       },

        # WA has ISO19139 records 
        'wa': { 'method': 'ISO19139',
                'params': [{ 'name': 'Sandstone',
                             'model_endpath': 'sandstone',
                            'metadata_url': 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Sandstone_2015.xml'
                          },
                          { 'name': 'Windimurra',
                            'model_endpath': 'windimurra',
                            'metadata_url': 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Windimurra_2015.xml'
                          }
                ]
              }
}
