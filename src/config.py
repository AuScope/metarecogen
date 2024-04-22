from pathlib import Path

"""
Config for creation of ISO19139 or ISO19115-3 XML metadata records from PDF reports or online metadata services
(e.g. CKAN, dSpace, geonetwork)

See "CONFIG.md" in root directory for format details 
"""
CONFIG = {
        ##
        # Victorian Geological Survey has some PDF reports
        'vic': { 'method': 'PDF',
            'params': [   { 'name': 'Otway Basin',
                            'model_endpath': 'otway',
                            'pdf_file': '../data/reports/vic/G107513_OtwayBasin_3D_notes.pdf',
                            'pdf_url': 'https://gsv.vic.gov.au/downloader/Downloader?ID=ERPublications/reports/GSV-3d-Vic/G107513_OtwayBasin_3D.pdf',
                            'organisation': "Geological Survey of Victoria",
                            'title': "Otway 3D model",
                            'cutoff': 1000,
                            'output_file': 'otway_pdf.xml'
                            },
                            { 'name': 'Bendigo',
                              'model_endpath': 'bendigo',
                              'pdf_file': '../data/reports/vic/G35615_3DVIC1_pt1.pdf',
                              'pdf_url': 'https://gsv.vic.gov.au/downloader/Downloader?ID=ERPublications/reports/GSV-3d-Vic/G35615_3DVIC1_pt1.pdf',
                              'organisation': "Geological Survey of Victoria",
                              'title': "Bendigo 3D model",
                              'cutoff': 3000,
                              'output_file': 'bendigo_pdf.xml'
                            },
                       ],
        },
        #
        # Use PDF version of academic paper for Uni of Adelaide Stuart Shelf model
        'nci': { 'method': 'PDF',
            'params': [ { 'name': 'Stuart Shelf',
                          'model_endpath': 'stuartshelf',
                          'pdf_file': '../data/reports/nci/Heinson-StuShelf.pdf',
                          'pdf_url': 'https://www.nature.com/articles/s41598-018-29016-2',
                          'organisation': 'NCI/University of Adelaide',
                          'title': 'Stuart Shelf Model',
                          'cutoff': 3000,
                          'output_file': 'stuartshelf_pdf.xml'
                          },
                     ],
        },
        #
        # Geo Survey of QLD has a CKAN repo
        'qld': { 'method': 'CKAN',
            'params': [ { 'name': 'Quamby',
                          'model_endpath': 'quamby',
                          'ckan_url': 'https://geoscience.data.qld.gov.au',
                          'package_id': 'ds000006',
                          'output_file': 'quamby_ckan.xml'
                        },
                        { 'name': 'Mt Dore',
                          'model_endpath': 'mtdore',
                          'ckan_url': 'https://geoscience.data.qld.gov.au',
                          'package_id': 'ds000002',
                          'output_file': 'mtdore_ckan.xml'
                        }
                 ]
        },
        #
        # SA Geo Survey has a geonetwork with ISO19115-3 records
        'sa': { 'method': 'ISO19115-3',
                'params': [  { 'name': 'Burra Mine',
                               'model_endpath': 'burramine',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/37e0f6f0-b9c7-47f0-bbed-482ce35851a4/formatters/xml',
                               'output_file': 'burra_19115-3.xml'
                             },
                             { 'name': 'Central Flinders',
                               'model_endpath': 'centralflinders',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/2369469b-4906-4352-9100-632974e0ec04/formatters/xml',
                               'output_file': 'centralflinders_19115-3.xml'
                             },
                             { 'name': 'North Flinders',
                               'model_endpath': 'northflinders',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/a86d7379-ca96-4e7d-8e1f-58bfeba9a8f5/formatters/xml',
                               'output_file': 'northflinders_19115-3.xml'
                             },
                             { 'name': 'North Gawler',
                               'model_endpath': 'ngawler',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml',
                               'output_file': 'ngawler_19115-3.xml'
                             },
                             { 'name': 'Curnamona Sedimentary Basins',
                               'model_endpath': 'curnamonased',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/bda114bc-1eb8-4569-94e5-a9fa1a994645/formatters/xml',
                               'output_file': 'curnamonased_19115-3.xml'
                             },
                             { 'name': 'Western Gawler',
                               'model_endpath': 'westgawler',
                               'metadata_url' :'https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/13ed6259-1ceb-4728-848f-35e81b502d12/formatters/xml',
                               'output_file': 'westgawler_19115-3.xml'
                             }
                ]
        },
        #
        # SA also has some reports: Burra.pdf  CurnamonaSed.pdf
        #'sa-test': { 'method': 'PDF',
        #    'params': [ { 'name': 'Burra Mine',
        #                  'model_endpath': 'burramine',
        #                  'pdf_file': '../data/reports/sa/Burra.pdf',
        #                  'organisation': 'South Australia Geological Survey',
        #                  'title': 'Burra Mine Test',
        #                  'cutoff': 3000,
        #                  'output_file': 'burra_pdf.xml'
        #                  },
        #               { 'name': 'Curnamona Sedimentary Basins',
        #                  'model_endpath': 'curnamonased',
        #                  'pdf_file': '../data/reports/sa/CurnamonaSed.pdf',
        #                  'organisation': 'South Australia Geological Survey',
        #                  'title': 'Curnamona Sed Basins Test',
        #                  'cutoff': 3000,
        #                  'output_file': 'curnamonased_pdf.xml'
        #                  },
        #             ],
        #},
        #
        # NT Geo Survey has ISO19139 records
        'nt': { 'method': 'ISO19139',
                'params': [  { 'name': 'McArthur Basin',
                               'model_endpath': 'mcarthur',
                               'metadata_url': 'http://www.ntlis.nt.gov.au/metadata/export_data?type=xml&metadata_id=1080195AEBC6A054E050CD9B214436A1',
                               'output_file': 'mcarthur_19139.xml'
                              }
                 ]
        },
        #
        # NT also has an OAI-PMH interface
        'nt': { 'method': 'OAIPMH',
                'params': [  { 'name': 'McArthur Basin',
                               'model_endpath': 'mcarthur',
                               'oai_id': 'oai:geoscience.nt.gov.au:1/81751',
                               'oai_prefix': 'oai_dc',
                               'service_name': "NTGS GEMIS",
                               'output_file': 'mcarthur_oai.xml'
                             }
                 ]
        },
        #
        # Geo Survey of WA has ISO19139 records 
        'wa': { 'method': 'ISO19139',
                'params': [{ 'name': 'Sandstone',
                             'model_endpath': 'sandstone',
                             'metadata_url': 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Sandstone_2015.xml',
                             'output_file': 'sandstone_19139.xml'
                          },
                          { 'name': 'Windimurra',
                            'model_endpath': 'windimurra',
                            'metadata_url': 'https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Windimurra_2015.xml',
                             'output_file': 'windimurra_19139.xml'
                          }
                ]
        }
}

# Currently set to root dir
OUTPUT_DIR = str(Path(__file__).parent / 'output')
