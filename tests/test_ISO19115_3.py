from ISO19115_3_extract import ISO19115_3Extractor

def test_ISO19115_3():
    url = "https://catalog.sarig.sa.gov.au/geonetwork/srv/api/records/9c6ae754-291d-4100-afd9-478c3a9ddf42/formatters/xml"
    name = 'ngawler'
    ce = ISO19115_3Extractor()
    assert ce.write_record(name, {'north': '0.0', 'south': '-45', 'east': '-145', 'west':'-100'}, name, url, f"test_19115_3_{name}.xml")

