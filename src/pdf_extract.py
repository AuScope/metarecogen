#!/usr/bin/env python3

import os
import sys
import requests
import json
from pathlib import Path
import datetime
import geojson
from datetime import date

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2, MetadataRecord

from extractor import Extractor
from keywords import get_keywords
from summary import get_summary

class PDFExtractor(Extractor):

    def get_record_config(self, keywords, summary, organisation, title, bbox):
        now = datetime.datetime.now()
        current_date = datetime.date(year=now.year, month=now.month, day=now.day)
        record_config = {
            "hierarchy_level": "dataset",
            "metadata": {
                "language": "eng",
                "character_set": "utf-8",
                "contacts": [{"organisation": {"name": organisation}, "role": ["pointOfContact"]}],
                "date_stamp": current_date,
            },
            "identification": {
                "title": {"value": title},
                "dates": {"creation": {"date": current_date, "date_precision": "year"}},
                "abstract": summary,
                "character_set": "utf-8",
                "language": "eng",
                "topics": ['geoscientificInformation'],
                "extent": {
                    "geographic": {
                        "bounding_box": {
                            "west_longitude": bbox['west'],
                            "east_longitude": bbox['east'],
                            "south_latitude": bbox['south'],
                            "north_latitude": bbox['north'],
                        }
                    }
                },
            },
        }
        return record_config



    def write_record(self, model_endpath, pdf_file, organisation, title, bbox, pdf_url=None):
        print(f"Converting: {model_endpath}")
        if pdf_url is not None:
            print("URL=", pdf_url)
            r = requests.get(pdf_url)
            text = r.text
            encoding = r.encoding
        else:
            if os.path.exists(pdf_file):
                text = pdf_file
                encoding = False
            else:
                print(f"{pdf_file} does not exist")
                sys.exit(1)
        kwset = get_keywords(text)
        summary = get_summary(text, encoding)
        #kwset = set(['kw1','kw2','kw3'])
        #summary = 'summary summary summary'
        record_config = self.get_record_config(list(kwset), summary, organisation, title, bbox)
        configuration = MetadataRecordConfigV2(**record_config)
        record = MetadataRecord(configuration=configuration)
        document = record.generate_xml_document()

        # output document
        fp = open(f"{model_endpath}.xml", 'w')
        fp.write(document.decode())
        fp.close()


if __name__ == "__main__":
    pe = PdfExtractor()
    pe.write_record("test-pdf", "https://blah/blah.pdf")
