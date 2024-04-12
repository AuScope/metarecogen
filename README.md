# isometarecgen

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

This is a basic framework of Python scripts that generate ISO 19115 geospatial metadata records (ISO19139 and ISO19115-3 XML). It is used for describing geological models from the AuScope 3D Geological Models website <https://geomodels.auscope.org.au>, but could easily be adapted for other kinds of metadata

The framework is capable of generating metadata records from these sources:  

1. [CKAN](https://ckan.org/) API 
2. PDF report files
3. ISO19115-3 XML (e.g. [geonetwork](https://geonetwork-opensource.org/))
4. ISO19139 XML (e.g. [geonetwork](https://geonetwork-opensource.org/))
5. OAI-PMH (e.g. [dSpace](https://dspace.lyrasis.org/))

## Initialise

Assumes PDM <https://github.com/pdm-project/pdm> is installed

```
git clone --recurse-submodules https://github.com/vjf/isometarecgen
cd isorecmetagen
pdm install
```

## Run

This project is written in Python and uses PDM <https://github.com/pdm-project/pdm> for its package management. PDM requires python version 3.7 or higher.

```
cd src
eval $(pdm venv activate)
./process.py
```
XML files are written to 'ouput' directory

## Configuration

The framework is configured via the [config.py](src/config.py) file. Its format is described in [CONFIG.md](CONFIG.md)

## Testing

No tests written yet

