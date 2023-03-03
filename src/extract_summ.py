#!/usr/bin/env python3

from PyPDF2 import PdfReader
import yake
import spacy
import pytextrank
import glob
import sys

def is_page_text(page):
    total = len(page)
    if total < 3000:
        return False
    alpha = 0
    for char in page:
        if char.isalpha():
            alpha += 1
    return float(alpha)/float(total)*100 > 73 
    

def parse_pdf(filename):
    reader = PdfReader(filename)

    meta = reader.metadata

    print(len(reader.pages))

    # All of the following could be None!
    #print(meta.author)
    #print(meta.creator)
    #print(meta.producer)
    #print(meta.subject)
    #print(meta.title)
    #print(meta)

    text = ""
    number_of_pages = len(reader.pages)
    for idx, page in enumerate(reader.pages):
        page_str = page.extract_text()
        if is_page_text(page_str):
            # print("Including page ", idx, "sz=", len(page_str))
            text += page_str + " "
            # print(page_str)
 
            
        #print(repr(page.extract_text()))

    return text

#with open("MESAJ083011-019.txt", "r") as fd:
#    text = fd.read()

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
    summary = tokenizer.decode(summary_ids[0])
    print("SUMMARY:", summary)

if __name__ == "__main__":
    for file in glob.glob('../data/reports/wa/*.pdf'):
        print(f"\n\nFILE:{file}\n")
        #if 'G161893_VGP_TR35_3D-Geological-framework-Otway_low-res.pdf' in file: # threshold = 80
        #if 'sandstone.pdf' in file:
        text = parse_pdf(file)
        run_t5(text)
        #run_yake(text)
        #run_textrank(text)
