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
                            'output_file': 'otway_pdf.xml'
                            },
                            { 'name': 'Bendigo',
                              'model_endpath': 'bendigo',
                              'pdf_file': '../data/reports/vic/G35615_3DVIC1_pt1.pdf',
                              'pdf_url': 'https://gsv.vic.gov.au/downloader/Downloader?ID=ERPublications/reports/GSV-3d-Vic/G35615_3DVIC1_pt1.pdf',
                              'organisation': "Geological Survey of Victoria",
                              'title': "Bendigo 3D model",
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
        # SA Geo Survey has CKAN
        'sa': { 'method': 'CKAN',
                'params': [  { 'name': 'Burra Mine',
                               'model_endpath': 'burramine',
                               'ckan_url' :'https://catalog.sarig.sa.gov.au'
                               'package_id': 'mesac271',
                               'output_file': 'burra_19115-3.xml'
                             },
                             { 'name': 'Central Flinders',
                               'model_endpath': 'centralflinders',
                               'ckan_url' :'https://catalog.sarig.sa.gov.au',
                               'package_id': 'mesac178',
                               'output_file': 'centralflinders_19115-3.xml'
                             },
                             { 'name': 'North Flinders',
                               'model_endpath': 'northflinders',
                               'package_id'; 'mesac776',
                               'output_file': 'northflinders_19115-3.xml'
                             },
                             { 'name': 'North Gawler',
                               'model_endpath': 'ngawler',
                               'package_id': 'mesac25693',
                               'output_file': 'ngawler_19115-3.xml'
                             },
                             { 'name': 'Curnamona Sedimentary Basins',
                               'model_endpath': 'curnamonased',
                               'package_id': 'mesac25808',
                               'output_file': 'curnamonased_19115-3.xml'
                             },
                             { 'name': 'Western Gawler',
                               'model_endpath': 'westgawler',
                               'package_id': 'mesac27247',
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
        #                  'output_file': 'burra_pdf.xml'
        #                  },
        #               { 'name': 'Curnamona Sedimentary Basins',
        #                  'model_endpath': 'curnamonased',
        #                  'pdf_file': '../data/reports/sa/CurnamonaSed.pdf',
        #                  'organisation': 'South Australia Geological Survey',
        #                  'title': 'Curnamona Sed Basins Test',
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

# Runs in cloud using Anthropic Claude LLM via AWS Bedrock
USE_CLAUDE = False

