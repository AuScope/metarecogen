#!/usr/bin/env python3

from PyPDF2 import PdfReader
import yake
import spacy
import pytextrank
import glob
import sys

def parse_pdf(filename):
    reader = PdfReader(filename)

    meta = reader.metadata

    print(len(reader.pages))

    # All of the following could be None!
    print(meta.author)
    print(meta.creator)
    print(meta.producer)
    print(meta.subject)
    print(meta.title)
    print(meta)


    text = ""
    number_of_pages = len(reader.pages)
    for page in reader.pages:
        text += page.extract_text() + " "

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

"""
CREATE TABLE term (
  code    integer not NULL,
  name    character varying(128),
  parent  integer,
  scope   character varying(1024)
  );
"""
def extract_db_terms():
    pass

if __name__ == "__main__":
    for file in glob.glob('*.pdf'):
        text = parse_pdf(file)
        run_yake(text)
        run_textrank(text)
