from docling.document_converter import DocumentConverter

def parse_docling(pdf_file: str) -> str:
    """
    Extracts the text from a PDF file using docling
    NB: Assumes PDF does not contain metadata, if exists should be utilised in future

    :param pdf_stream: filename
    """
    converter = DocumentConverter()
    doc = converter.convert(pdf_file).document
    return doc.export_to_markdown()
