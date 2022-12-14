'''
CS375 Project 4
Aidan Tokarski, Cynthia Zafris,
Eda Wright, Xavier Markowitz

Utilities for extracting text from PDF files
'''

import re
import os
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

def get_text(file):

    fp = open(file, 'rb')
    pdfmgr = PDFResourceManager()
    strio = io.StringIO()
    converter = TextConverter(pdfmgr, strio, laparams=LAParams())
    interpreter = PDFPageInterpreter(pdfmgr, converter)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        text =  strio.getvalue()

    text = text.replace("\n", " ")
    text = text.replace("—", " ")
    text = text.replace(".", " ")
    text = text.replace("’", "'")
    text = re.sub(r'[^a-zA-Z\'\- ]', '', text)
    text = text.lower()

    return text

def get_files(dir):
    return os.listdir(dir)

def write_text_file(file, in_dir, out_dir):
    source_file = "{}\{}".format(in_dir, file)
    filename = file.replace(".pdf", "")
    with open("{}\{}.txt".format(out_dir, filename), 'w') as new_file:
        new_file.write(get_text(source_file))

if __name__ == "__main__":
    files = get_files("CS375_documents")
    for file in files:
        write_text_file(file, "CS375_documents", "CS375_extracted")