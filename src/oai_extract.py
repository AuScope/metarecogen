#!/usr/bin/env python3
from sickle import Sickle

# Get records from Northern Territory Geological Service

OAI_URL = 'https://geoscience.nt.gov.au/gemis/ntgsoai/request'

PERM_LINK = 'https://geoscience.nt.gov.au/gemis/ntgsjspui/handle/1/81751'
handle_id = '/'.join(PERM_LINK.split('/')[-2:])

sickle = Sickle(OAI_URL)

# Some geological fields that are present in GEMIS website are missing from OAI output with 'oai_dc' prefix,
# i.e. "Stratigraphy" The 'xoai' prefix will allow extraction of these missing fields but the XML output
# would need to be parsed
rec = sickle.GetRecord(identifier='oai:geoscience.nt.gov.au:'+handle_id, metadataPrefix='oai_dc')

m_dict = rec.get_metadata()
for k,v in m_dict.items():
  print(k, ': ', v)

TODO: Use pygeometa to make an ISO record
