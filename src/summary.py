#!/usr/bin/env python3

import io
import sys
import glob

import yake
import spacy
import pytextrank

from pdf_helper import parse_pdf


def run_yake(text):

    print("yake:")
    kw_extractor = yake.KeywordExtractor(top=100)
    keywords = kw_extractor.extract_keywords(text)

    for kw in keywords:
        print(kw)

def run_textrank(text):

    print("textrank:")


    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    for phrase in doc._.phrases[:40]:
        print(phrase.text)
        print(phrase.rank, phrase.count)
        print(phrase.chunks)
        print()

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

def get_summary(text, encoding):
    if encoding != False:
        # text
        if encoding is None:
            encoding = 'utf-8'
        stream_or_file = io.BytesIO(bytes(text, encoding))
    else:
        # filename
        stream_or_file = text
    pdf_text = parse_pdf(stream_or_file, True)
    return run_t5(pdf_text)
    

if __name__ == "__main__":
    for file in glob.glob('../data/reports/wa/*.pdf'):
        print(f"\n\nFILE:{file}\n")
        #if 'G161893_VGP_TR35_3D-Geological-framework-Otway_low-res.pdf' in file: # threshold = 80
        #if 'sandstone.pdf' in file:
        text = parse_pdf(file, True)
        summary = run_t5(text)
        print("SUMMARY:", summary)

        #run_yake(text)
        #run_textrank(text)
