#!/usr/bin/env python3

import os

# from semantic_text_splitter import TextSplitter

from bedrock_summary import run_claude

from pdf_helper import parse_pdf
from constants import OUTPUT_DIR

# os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

OUTPUT_PDF_TXT = False

#def run_t5(text):
#    """ Runs t5 model
#
#    :param text: text to be summarized
#    :returns summarixzed text
#    """
#    import torch
#    from transformers import AutoTokenizer, AutoModelWithLMHead
#    tokenizer = AutoTokenizer.from_pretrained('t5-base')
#    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)
#
#    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)
#    summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)
#    if len(summary_ids) > 0:
#        return tokenizer.decode(summary_ids[0])
#    return ""

#def run_pegasus(text):
#    """ Runs pegasus model, it can summarize large paragraphs
#
#    :param text: text to be summarized
#    :returns summarixzed text
#    """
#    from transformers import PegasusForConditionalGeneration, AutoTokenizer
#    import torch
#
#    # You can chose models from following list
#    # https://huggingface.co/models?sort=downloads&search=google%2Fpegasus
#    model_name = 'google/pegasus-cnn_dailymail'
#    device = 'cuda' if torch.cuda.is_available() else 'cpu'
#    tokenizer = AutoTokenizer.from_pretrained(model_name)
#    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
#    batch = tokenizer(text, truncation=True, padding='longest', return_tensors="pt").to(device)
##    translated = model.generate(**batch)
#    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
#    return tgt_text

def get_summary(filename, cutoff):
    """
    Summarise a PDF file

    :param filename: filename of PDF file
    :param cutoff: text pages below this threashold are ignored
    :returns: text string of PDF file
    """
    pdf_text = parse_pdf(filename, True, cutoff)
    # Option to output to text file
    if OUTPUT_PDF_TXT:
        txt_filename = os.path.basename(filename).split('.')[0] + ".txt"
        with open(os.path.join(OUTPUT_DIR, txt_filename), 'w') as fd:
            fd.write(pdf_text)
    summary = run_claude(pdf_text)
    return summary
    #summary = run_t5(pdf_text)
    #return(clean_t5_summary(summary))
    
#def clean_t5_summary(s):
#    """
#    Used for t5 Remove tags, empty sections etc. from summary
#
#    :param s: input string
#    :returns: cleaned string
#    """
#    # Get rid of XML tags
#    p = re.compile("<\w+>")
#    s = p.sub("",s)
#    # Remove empty bits
#    s_arr = s.split(" ")
#    clean_s_arr = [ s_item for s_item in s_arr if s_item not in ['','.'] ]
#    # Capitalise after full stop
#    for idx, s_item in enumerate(clean_s_arr):
#        if s_item[-1] == '.' and idx+1 < len(clean_s_arr):
#          clean_s_arr[idx+1] = clean_s_arr[idx+1].capitalize()
#    # First word capitalised
#    clean_s_arr[0] = clean_s_arr[0].capitalize()
#    return " ".join(clean_s_arr)

#def reduce(splitter, text, chunk_sz):
#    """ Uses semantic splitter to split large text into similar chunks
#        and runs pegasus to reduce the size of each one
#    """
#    # Maximum number of characters in a chunk
#    big_summary = ''
#    for chunk in splitter.chunks(text, chunk_sz):
#        print(f"CCHUNK: {chunk}")
#        summary = run_pegasus(chunk)
#        print(f"SUMMARY: {summary}\n\n" )
#        big_summary += f"{summary[0]} "
#
#    return big_summary


#if __name__ == "__main__":
#    splitter = TextSplitter()
#
#    for file in glob.glob('../data/reports/sa/*.pdf'):
#        #if 'G161893_VGP_TR35_3D-Geological-framework-Otway_low-res.pdf' in file:
#        #    continue
#        print(f"\n\nFILE:{file}\n")
#        filename = os.path.basename(file)
#        summary_filename = os.path.splitext(filename)[0] + "_summ.txt"
#
#        print(f"{filename=}\n")
#        print(f"{summary_filename=}\n")
#        text = parse_pdf(file, True)
#        text = text.replace('\n',' ')
#        print(repr(text))
#        depth_cnt = 0
#        big_summary = reduce(splitter, text)
#        print(f"\nBIG SUMMARY: {big_summary}\n\n")
#        with open(summary_filename, 'w') as fd:
#            fd.write(big_summary)

