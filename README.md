# Metadata Record Generator

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html)

This is a basic framework of Python scripts that generate ISO 19115 geospatial metadata records (ISO 19139 and ISO 19115-3 XML). It is used for describing geological models from the AuScope 3D Geological Models website <https://geomodels.auscope.org.au>, but could be adapted for other kinds of metadata

The framework is capable of generating metadata records from these sources:  

1. [CKAN](https://ckan.org/) API 
2. PDF geoscience report files
3. ISO 19115-3 XML (e.g. [geonetwork](https://geonetwork-opensource.org/))
4. ISO 19139 XML (e.g. [geonetwork](https://geonetwork-opensource.org/))
5. OAI-PMH (e.g. [dSpace](https://dspace.lyrasis.org/))

For ISO 19115-3 and ISO 19139 the framework does little more than customisation of the XML records.
For the other sources XML is generated from scratch.

## Initialise

Assumes PDM <https://github.com/pdm-project/pdm> is installed

```
git clone --recurse-submodules https://github.com/AuScope/metarecogen
cd metarecogen
pdm install
```

NB: AuScope 'geomodelportal' repository is included in the git clone as a submodule.
This allows the scripts to copy some model data (i.e. geospatial coordinates) for inclusion in the metadata record

## Input and Output Details

**Table of fields output for each source type**

| Field             | PDF | CKAN | ISO 19115-3 | ISO 19139 | OAI-PMH |
| ------------------| ----|------|-------------|-----------|---------|
| Id                |     | Y    |   Y         |    Y      |     Y   |
| Title             | Y   | Y    |   Y         |    Y      |     Y   |
| Abstract          | Y   | Y    |   Y         |    Y      |     Y   |
| Organisation Name | Y   | Y    |   Y         |    Y      |     Y   |
| Creation Date     | Y   | Y    |   Y         |    Y      |     Y   |
| Publication Date  |     | Y    |   Y         |    Y      |     Y   |
| Spatial Coordinates | Y   | Y    |   Y         |    Y      |    Y   |
| Custom keywords   | Y   |      |     Y     |     Y     |      Y   |
| Fixed Keywords    | Y   | Y    |   Y         |    Y      |     Y   |
| License           | Y   | Y    |   Y         |   Y       |     Y   |
| Maintenance Freq  | Y   | Y    |   Y         |    Y      |     Y   |
| Lineage           | Y   | Y    |    Y        |   Y       |     Y   |

&nbsp;
NB: 'Fixed keywords' do not vary from record to record, 'Custom keywords' are tailored to each record
&nbsp;

**Table of output XML**

| Input source | Output ISO XML standard |
| ------------ | ----------------------- |
| PDF          |  ISO 19115-3            |
| CKAN         |  ISO 19115-3            |
| ISO 19115-3  |  ISO 19115-3            |
| ISO 19139    |  ISO 19139              |
| OAI-PMH      |  ISO 19115-3            |


## Run

This project is written in Python and uses PDM <https://github.com/pdm-project/pdm> for its package management. PDM requires python version 3.7 or higher.

To generate metadata from PDF file, this project uses AWS Bedrock to run a Claude LLM and assumes that the correct AWS credentials have been set up in the user's environment.

```
cd src
eval $(pdm venv activate)
./process.py
```
XML files are written to 'output' directory (defined in [constants.py](src/constants.py))

## Configuration

The framework is configured via the [config.py](src/config.py) file. Its format is described in [CONFIG.md](CONFIG.md)

## Testing

There are very basic tests in [tests](tests), run via using pytest
```
pytest
```

