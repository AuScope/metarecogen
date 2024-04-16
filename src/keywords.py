#!/usr/bin/env python3

import glob
import sys
import sqlite3
from contextlib import closing

import yake

from pdf_helper import parse_pdf

"""
Uses yake and USGS vocabulary to create geoscience keywords
    USGS Thesaurus:   https://apps.usgs.gov/thesaurus/
    yake:   https://pypi.org/project/yake/
"""

def phrase_in_dict(phrase, in_dict):
    """
    Returns true if phrase is in in_dict
    """
    words = phrase.split(' ')
    for word in words:
        if word in in_dict:
            return True, in_dict[word]
    return False, ''

def run_yake(kw_lookup, text):
    """
    Runs yake on some text and returns the top keywords

    :param bw_lookup: lookup table mapping used to categorise geoscience terms into keywords
    :param text: text to search for keywords
    :returns: set() of yake's keywords
    """
    kw_extractor = yake.KeywordExtractor(top=500)
    # Extracts yakes top keywords
    keywords = kw_extractor.extract_keywords(text)
    # Map yakes keywords to USGS keywords
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
    """ Function to create a lookup table that translates geological terms into keywords using USGS vocab
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
    """
    Looks for keywords using USGS vocabulary

    :param kw_dict: keyword dict extracted from USGS vocab - maps a variety of geoscience words to keywords
    :param text: text in which to look for keywords
    :returns: set() of keywords
    """
    kw_set = set()
    text = text.replace('\n',' ')
    for word in text.split(' '):
        if word.isalpha() and word in kw_dict:
            kw_set.add(kw_dict[word])
    return kw_set    

def get_keywords(text):
    """
    Extracts keywords from text

    :param text: text
    :returns: 
    """
    kw_dict = extract_db_terms()
 
    yake_kwset = run_yake(kw_dict, text)

    return yake_kwset


# Used for testing only
if __name__ == "__main__":
    kw_dict = extract_db_terms()
    for file in ['G107513_OtwayBasin_3D_notes.pdf',
                 # 'G161893_VGP_TR35_3D-Geological-framework-Otway_low-res.pdf', 
                 #'G35615_3DVIC1_pt1.pdf'
                 ]:
        text = parse_pdf(f'../data/reports/vic/{file}', False)
 
        yake_kwset = run_yake(kw_dict, text)
        print(f"{file}: usgs+yake: {yake_kwset}")
    
        #usgs_kwset = run_usgs(kw_dict, text)
        #print("pure usgs:", usgs_kwset)

