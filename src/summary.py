#!/usr/bin/env python3

import os
import sys

from bedrock_summary import run_claude

from pdf_helper import parse_docling
from config import OUTPUT_DIR, USE_CLAUDE

# Writes out a file of text extracted from PDF file
OUTPUT_PDF_TXT = True

def get_summary(filename: str) -> str:
    """
    Summarise a PDF file

    :param filename: filename of PDF file
    :returns: text string of PDF file
    """
    pdf_text = parse_docling(filename)
    # Option to output to text file
    if OUTPUT_PDF_TXT:
        txt_filename = os.path.basename(filename).split('.')[0] + ".txt"
        with open(os.path.join(OUTPUT_DIR, txt_filename), 'w') as fd:
            fd.write(pdf_text)
    if USE_CLAUDE:
        summary = run_claude(pdf_text)
    else:
        raise NotImplementedError
    return summary
