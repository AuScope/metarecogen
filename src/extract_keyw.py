#!/usr/bin/env python3

from PyPDF2 import PdfReader
import yake
import spacy
import pytextrank
import glob
import sys
import sqlite3
from contextlib import closing

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
    """ Function to create a lookup table that translates geological terms into keywords
    """
    keyword_lkup = {}
    name_dict = {}
    link_dict = {}
    with closing(sqlite3.connect("../db/thesauri.db")) as con:
        with closing(con.cursor()) as cur:
            for row in cur.execute("SELECT code, name, parent FROM term"):
                print(row)
                link_dict[row[0]] = row[2]
                name_dict[row[0]] = row[1]
    for k,v in link_dict.items():
        parent = v
        child = -1
        gchild = -1
        ggchild = -1
        while parent != 1 and parent != None:
            ggchild = gchild
            gchild = child
            child = parent
            parent = link_dict[parent]
        try:
            if name_dict[ggchild] not in ['chemical elements', 'chemical element groups']:
                print("parent of", name_dict[k], "is:  ", name_dict[ggchild]) 
                keyword_lkup[k] = name_dict[ggchild]
        except KeyError:
            pass
    return keyword_lkup

if __name__ == "__main__":
    #for file in glob.glob('*.pdf'):
    #    text = parse_pdf(file)
    #    run_yake(text)
    #    run_textrank(text)
    extract_db_terms()
