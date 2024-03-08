#!/usr/bin/env python3

import io
import sys
import os
import glob
import re

import yake
import spacy
import pytextrank

from pdf_helper import parse_pdf
from constants import OUTPUT_DIR

OUTPUT_PDF_TXT = True

def run_t5(text):
    import torch
    from transformers import AutoTokenizer, AutoModelWithLMHead
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)
    if len(summary_ids) > 0:
        return tokenizer.decode(summary_ids[0])
    return ""

def get_summary(filename, cutoff):
    """
    Summarise a PDF file

    :param filename: filename of PDF file
    :param cutoff: text pages below this threashold are ignored
    :returns: text string of PDF file
    """
    pdf_text = parse_pdf(filename, True, cutoff)
    if OUTPUT_PDF_TXT:
        txt_filename = os.path.basename(filename).split('.')[0] + ".txt"
        with open(os.path.join(OUTPUT_DIR, txt_filename), 'w') as fd:
            fd.write(pdf_text)
    #print(f"get_summary(): {filename=}")
    #print(f"{len(pdf_text)=}")
    summary =  run_t5(pdf_text)
    return(clean_summary(summary))
    
def clean_summary(s):
    """
    Remove tags, empty sections etc. from summary

    :param s: input string
    :returns: cleaned string
    """
    # Get rid of XML tags
    p = re.compile("<\w+>")
    s = p.sub("",s)
    # Remove empty bits
    s_arr = s.split(" ")
    clean_s_arr = [ s_item for s_item in s_arr if s_item not in ['','.'] ]
    # Capitalise after full stop
    for idx, s_item in enumerate(clean_s_arr):
        if s_item[-1] == '.' and idx+1 < len(clean_s_arr):
          clean_s_arr[idx+1] = clean_s_arr[idx+1].capitalize()
    # First word capitalised
    clean_s_arr[0] = clean_s_arr[0].capitalize()
    return " ".join(clean_s_arr)

if __name__ == "__main__":
    for file in glob.glob('../data/reports/vic/*.pdf'):
        if 'G161893_VGP_TR35_3D-Geological-framework-Otway_low-res.pdf' in file:
            continue
        print(f"\n\nFILE:{file}\n")
        text = parse_pdf(file, True)
        summary = run_t5(text)
        print("SUMMARY:", summary)
