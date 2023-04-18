#!/usr/bin/env python3

import glob
import sys
import sqlite3
from contextlib import closing

import yake
import spacy
import pytextrank

from pdf_helper import parse_pdf

def phrase_in_dict(phrase, dict):
    words = phrase.split(' ')
    for word in words:
        if word in dict:
            return True, dict[word]
    return False, ''

def run_yake(kw_lookup, text):
    kw_extractor = yake.KeywordExtractor(top=500)
    keywords = kw_extractor.extract_keywords(text)
    # print(len(keywords))
    kw_set = set()
    for kw in keywords:
        if kw[0] in kw_lookup:
            kw_set.add(kw_lookup[kw[0]])
            continue
        included, kw = phrase_in_dict(kw[0], kw_lookup)
        if included:
            kw_set.add(kw)
    # If no USGS keywords found then just use YAKE's estimates
    if len(kw_set) == 0:
        kw_set = set([kw[0] for kw in keywords])
    return kw_set

def run_textrank(text):

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
This is the format of the USGS Vocab table in the SQLITE DB:

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
    # Connect to USGS Thesaurus DB (https://apps.usgs.gov/thesaurus/)
    with closing(sqlite3.connect("../db/thesauri.db")) as con:
        with closing(con.cursor()) as cur:
            for row in cur.execute("SELECT code, name, parent FROM term"):
                # print(row)
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
                # print("parent of", name_dict[k], "is:  ", name_dict[ggchild]) 
                keyword_lkup[name_dict[k]] = name_dict[ggchild]
        except KeyError:
            pass
    return keyword_lkup

def run_usgs(kw_dict, text):
    kw_set = set()
    text = text.replace('\n',' ')
    # print('#words', len(text.split(' ')))
    for word in text.split(' '):
        if word.isalpha() and word in kw_dict:
            kw_set.add(kw_dict[word])
    return kw_set    

def get_keywords(text):
    kw_dict = extract_db_terms()
 
    yake_kwset = run_yake(kw_dict, text)

    return yake_kwset


if __name__ == "__main__":
    kw_dict = extract_db_terms()
    for file in ['G107513_OtwayBasin_3D_notes.pdf',
                 # 'G161893_VGP_TR35_3D-Geological-framework-Otway_low-res.pdf', 
                 #'G35615_3DVIC1_pt1.pdf'
                 ]:
        text = parse_pdf(f'../data/reports/vic/{file}', False)
 
        yake_kwset = run_yake(kw_dict, text)
        print(f"{file}: usgs+yake: {yake_kwset}")
    
        #run_textrank(text)
        #usgs_kwset = run_usgs(kw_dict, text)
        #print("pure usgs:", usgs_kwset)

