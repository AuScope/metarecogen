import os
import datetime

from pygeometa.core import render_j2_template
from pdf_helper import parse_pdf

from extractor import Extractor
from keywords import get_keywords
from summary import get_summary

class PDFExtractor(Extractor):
    """ Creates an ISO 19115 XML file by reading a PDF file
    """

    def write_record(self, name, model_endpath, pdf_file, pdf_url, organisation, title, bbox, cutoff, output_file):
        """
        Write XML record

        :param name: model name used in download links in record
        :param model_endpath: path of model in website, used to create a link to website URL
        :param pdf_file: path to PDF file
        :param pdf_url: URL for PDF file
        :param organisation: name of organisation
        :param title: title
        :param bbox: bounding box coords, dict, keys are 'north', 'south' etc.
        :param cutoff: skip pages that have less than this amount of text, set to between 1000 and 3000, used to filter out pages with no useful text
        :param output_file: output filename e.g. 'blah.xml'
        :returns: boolean
        """
        print(f"Converting: {model_endpath}")
        if not os.path.exists(pdf_file):
            print(f"{pdf_file} does not exist")
            return False
        # Extract keywords from PDF text
        pdf_text = parse_pdf(pdf_file, False)
        kwset = get_keywords(pdf_text)
        summary = get_summary(pdf_file, cutoff)
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        keywords = list(kwset)
        bbox_list = [str(bbox['west']), str(bbox['east']), str(bbox['south']), str(bbox['north'])]

        # Remove encodings that can upset XML
        summary = summary.replace('<', '&lt;')
        summary = summary.replace('>', '&gt;')

        # Assemble dict for jinja template
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
                "datestamp": date_str,
                "dataseturi": "",
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
                    "en": title,
                },
                "abstract": {
                    "en": summary,
                },
                "dates": {
                    "creation": date_str,
                    "publication": date_str
                },
                "keywords": {
                    "default": {
                        "keywords": {
                            "en": keywords
                        }
                    }
                },
                "topiccategory": [
                    "geoscientificInformation"
                ],
                "extents": {
                    "spatial": [
                        {
                            "bbox": bbox_list,
                            "crs": "4326"
                        }
                    ]
                },
                "fees": "None",
                "accessconstraints": "license",
                "rights": {
                    "en": "CC BY 4.0",
                },
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "status": "completed",
                "maintenancefrequency": "continual"
            },
            "contact": {
                "distributor": {
                    "organization": organisation
                }
            },
            "distribution": [
                {
                    "url": pdf_url,
                    "type": "WWW:LINK",
                    "rel": "service",
                    "name": {
                        "en": name,
                    },
                    "description": {
                        "en": "3D Model Report",
                    },
                    "function": "download"
                },
                {
                    "url": f"https://geomodels.auscope.org.au/model/{model_endpath}",
                    "type": "WWW:LINK",
                    "rel": "service",
                    "name": {
                        "en": "AuScope 3D Geoscience model website",
                    },
                    "description": {
                        "en": "AuScope 3D Geoscience model website",
                    },
                    "function": "website"
                }
            ],
            "dataquality": {
                "scope": {
                    "level": "dataset"
                },
                "lineage": {
                    "statement": f"This metadata record was reproduced from the PDF report retrieved from {pdf_url} on {datetime.datetime.now():%d %b %Y}. The abstract was generated by Anthropic Claude V2.0 (https://www.anthropic.com/). Keywords were taken from USGS Thesaurus (https://apps.usgs.gov/thesaurus/) and extracted by yake (https://pypi.org/project/yake)"
                }
            }
        }

        # Create ISO 19115-3 XML with a modified version pygeometa's jinja template
        template_dir = os.path.join(os.path.dirname(__file__), '../data/templates/ISO19115-3')
        xml_string = render_j2_template(mcf_dict, template_dir=template_dir)

        # write to disk
        with open(os.path.join(self.output_dir, output_file), 'w') as ff:
            ff.write(xml_string)
        return True
