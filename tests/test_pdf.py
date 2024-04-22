from pdf_extract import PDFExtractor

def test_pdf():
    pe = PDFExtractor()
    # Test missing PDF file
    assert not pe.write_record("Blah Blah", "blah", "blah.pdf", "https://blah.org/blah.pdf", "test org", "test title", {'north': -15.0, 'south': -40.4, 'east': 120.5, 'west': 100.3}, 3000, "pdf_test.xml")
