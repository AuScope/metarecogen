from ISO19139_extract import ISO19139Extractor

def test_ISO19139():
    metadata_urls = [
 ("mcarthur", "http://www.ntlis.nt.gov.au/metadata/export_data?type=xml&metadata_id=1080195AEBC6A054E050CD9B214436A1"),
 ("windimurra", "https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Windimurra_2015.xml"),
 ("sandstone", "https://warsydprdstadasc.blob.core.windows.net/downloads/Metadata_Statements/XML/3D_Sandstone_2015.xml")
    ]
    ce = ISO19139Extractor()
    for name, url in metadata_urls:
        ce.write_record(name, {'north': '0.0', 'south': '-45', 'east': '-145', 'west':'-100'}, name, url, f"test_19139_{name}.xml")

