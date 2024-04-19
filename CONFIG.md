# Configuring the framework

The 'config.py' file tells the framework how and where it can get the resources needed to create XML records

The 'config.py' file contains a python dict which has this format:
```
CONFIG = {
     '<provider label>': {
              'method': '<method>',
              'params': '<params>' 
        },

      ...
}
```
where:

**'\<provider label>'** is a label for representing the resource provider e.g. 'vic'

**'\<method>'** is one of: 'PDF' 'CKAN' 'ISO19115-3' 'ISO19139' 'OAIPMH'

**'\<params>'** are detailed in the sections below

NB: These parameters are reflected in the 'write_record' function for each kind of 'Extractor' class

### Parameters for 'PDF' method

This method uses a PDF report file as a source of metadata, all parameters are mandatory

**name** - model name

**model_endpath** - part of the URL of this model in geomodels website, used to output path to model in metadata

**pdf_file** - path to PDF file

**pdf_url**  - URL to PDF file

**organisation** - name of organisation

**title** - title of metadata record

**cutoff** - tolerance for non-text in the PDF file, used to exclude pages with a small amount of valid text, set to between 1000 and 3000


### Parameters for 'CKAN' method

This method uses a record in a CKAN repository as a source of metadata

**name** - model name

**model_endpath** - part of the URL of this model in geomodels website, used to output path to model in metadata

**ckan_url** - URL of CKAN website e.g. 'https://demo.ckan.org'

**package_id** - package id of record in CKAN repository


### Parameters for 'ISO19115-3' method

This method uses an ISO19115-3 XML record as a source of metadata fetched from a web service e.g. geonetwork

**name** - model name

**model_endpath** - part of the URL of this model in geomodels website, used to output path to model in metadata

**metadata_url** - URL of ISO19115-3 XML metadata record

### Parameters for 'ISO19139' method

This method uses an ISO19139 XML record as a source of metadata fetched from a web service e.g. geonetwork

**name** - model name

**model_endpath** - part of the URL of this model in geomodels website, used to output path to model in metadata

**metadata_url** - URL of ISO19139 XML metadata record

### Parameters for 'OAIPMH' method

This method queries a method from an OAI-PMH web service as a source of metadata

**name** - model name

**model_endpath** - part of the URL of this model in geomodels website, used to output path to model in metadata

**oai_id** - OAI-PMH id string e.g. 'oai:eprints.rclis.org:4088'

**oai_prefix** - OAI-PMH prefix string e.g. 'oai_dc'

**service_name** - A general name for this OAI-PMH service


