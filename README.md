# isometarecgen

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

This is a prototype bundle of Python scripts that generate ISO 19115 geospatial metadata records (ISO19139 and ISO19115-3) describing geological models from the AuScope Geological Models website <http://geomodels.auscope.org.au>.

The metadata records are extracted and compiled from these sources:  

1. CKAN API
2. Geological PDF report files
3. ISO19139 XML
4. OAI-PMH (dSpace)

## Initialise

Assumes PDM <https://github.com/pdm-project/pdm> is installed

```
pdm install
```

## Run

This project is written in Python and uses PDM <https://github.com/pdm-project/pdm> for its package management. PDM requires python version 3.7 or higher.

```
cd src
eval $(pdm venv activate)
./process.py
```
XML files are written to 'src' directory

## Configuration

Not documented yet

## Testing

No tests written yet

