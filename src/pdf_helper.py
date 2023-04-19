from PyPDF2 import PdfReader

def is_page_text(page, cutoff):
    """
    Tries to filter out non-alphabetic text

    :param page: a page of text, string
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
    :param pdf_stream: filename or stream object
    :param page_filter: will try to filter out non-alphabetic text
    """
    reader = PdfReader(pdf_stream)

    meta = reader.metadata

    # print(len(reader.pages))

    # All of the following could be None!
    #print(meta.author)
    #print(meta.creator)
    #print(meta.producer)
    #print(meta.subject)
    #print(meta.title)
    #print(meta)

    text = ""
    number_of_pages = len(reader.pages)
    for idx, page in enumerate(reader.pages):
        page_str = page.extract_text()
        if not page_filter or is_page_text(page_str, cutoff):
            # print("Including page ", idx, "sz=", len(page_str))
            text += page_str + " "
            # print(page_str)
 
            
        #print(repr(page.extract_text()))
    #print(f"parse_pdf {pdf_stream=} {len(text)=} {page_filter=}")

    return text
