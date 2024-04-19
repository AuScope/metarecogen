from PyPDF2 import PdfReader


def is_page_text(page, cutoff):
    """
    Tries to filter out non-alphabetic text

    :param page: a page of text, string
    :param cutoff: page with less than 'cutoff' bytes are ignored
    """
    total = len(page)
    if total < cutoff:
        return False
    alpha = 0
    for char in page:
        if char.isalpha():
            alpha += 1
    return float(alpha)/float(total)*100 > 73.0

def parse_pdf(pdf_stream, page_filter, cutoff=3000):
    """
    Extracts the text from a PDF file
    NB: Assumes PDF does not contain metadata, if exists should be utilised in future

    :param pdf_stream: filename or stream object
    :param page_filter: will try to filter out non-alphabetic text
    :param cutoff: page with less than 'cutoff' bytes are ignored
    """
    reader = PdfReader(pdf_stream)

    # All of the following are often None!
    # TODD: Use this if defined
    # meta = reader.metadata
    # print(meta.author)
    # print(meta.creator)
    # print(meta.producer)
    # print(meta.subject)
    # print(meta.title)
    # print(meta)

    text = ""
    for idx, page in enumerate(reader.pages):
        page_str = page.extract_text()
        if not page_filter or is_page_text(page_str, cutoff):
            text += page_str + " "
    return text
