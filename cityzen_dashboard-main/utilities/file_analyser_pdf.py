import fitz                                                             # BSD (3-clause) Licence # pip install pymupdf
import numpy as np
import os
import PyPDF2                                                           # BSD-3-Clause Licence
import re

from io import StringIO
from pdfreader import PDFDocument, SimplePDFViewer                      # MIT License
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter   # MIT License # pip install pdfminer.six
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from utilities.general_utilities import resetDirectory


# methods for extracting content from PDF files

def analysePdfFilePdfreader(fileName):
    # https://pypi.org/project/pdfreader/
    # https://pdfreader.readthedocs.io/en/latest/tutorial.html#
    page_count = 0
    document_text = ''
    word_count = 0
    paragraph_count = 0
    bullet_count = 0
    image_count = 0

    document = open(fileName, "rb")
    viewer = SimplePDFViewer(document)
    #print(viewer.metadata)

    # count number of pages in the document
    for canvas in viewer:
        print("Page found")
        print(viewer.current_page_number)
        page_count += 1
    print(str(page_count) + " pages in document")

    # navigate back to first page to reset the viewer
    viewer.navigate(1)

    # examine individual pages (example)
    #viewer.navigate(1)
    #viewer.render()
    #page1 = viewer.canvas
    #print(len(viewer.canvas.inline_images))
    #print(len(page1.images))
    #print(page1.images)   

    # save page images as image files (example)
    #image0 = page1.images['Im0']
    #print(image0.Filter)
    #print(image0.Width)
    #print(image0.Height)
    #pil_image0 = image0.to_Pillow()
    #pil_image0.save('Im0.png')

    image_list = []
    inline_image_list = []

    # review all pages in document
    for canvas in viewer:
        page_images = canvas.images
        #page_forms = canvas.forms
        #page_text = canvas.text_content
        page_inline_images = canvas.inline_images
        page_strings = canvas.strings

        document_text += ''.join(page_strings)

        for image in page_images:
            print(image)
            #image_count += 1
            if not image in image_list:
                image_list.append(image)

        for image in page_inline_images:
            print(image)
            #image_count += 1
            if not image in inline_image_list:
                inline_image_list.append(image)

    # count unique images to avoid including multiple header/footer images, etc
    image_count = len(image_list) + len(inline_image_list)
    print(image_list)

    document_words = document_text.split()
    print(len(document_words))
    word_count += len(document_words)

    return document_text, word_count, paragraph_count, bullet_count, image_count


def analysePdfFilePypdf2(fileName):
    # https://pypi.org/project/PyPDF2/
    word_count = 0
    paragraph_count = 0
    bullet_count = 0
    image_count = 0

    pdfReader = PyPDF2.PdfFileReader(fileName)
    document_text = ''

    for page in np.arange(0, pdfReader.numPages):
        #string = pdfReader.getPage(page).extractText().replace('\n','').lower()
        string = pdfReader.getPage(page).extractText()
        document_text += string
    document_words = document_text.split()
    word_count = len(document_words)

    return document_text, word_count, paragraph_count, bullet_count, image_count


def analysePdfFilePdfminer(fileName):
    # https://stackoverflow.com/questions/25665/python-module-for-converting-pdf-to-text
    # https://pdfminersix.readthedocs.io/en/latest/
    # https://pypi.org/project/pdfminer/
    word_count = 0
    paragraph_count = 0
    bullet_count = 0
    image_count = 0

    document_text = convert_pdf_to_txt(fileName)

    ###########################################################################

    # bullet points
    bullet_list = [
        '\u2022', '\u25E6', '\u2023', '\u29BF', '\u2219', '\u2043',
        '\u204D', '\u29BE', '\u25D8', '\u204C', '\u25AA', '\u25C9'
    ]

    for bullet in bullet_list:
        bullet_count += document_text.count(bullet)

    # https://unicode-table.com/en/006F/
    # o this is a latin 'o' which is mistaken for a bullet when converting pdf to text
    # hence the '\n' prefix and ' ' suffix to represent newline -> bullet -> space
    bullet_count += document_text.count('\n\u006F ')

    # remove the latin 'o' bullet points from the text extract
    document_text = document_text.replace('\n\u006F ', '')

    # look for numbered bullets/tabbed sections e.g., '\n1. '
    matches = re.finditer(r'(?=(\n\d+[.]\s))', document_text)
    results = [(match.group(1)) for match in matches]
    print(len(results))
    print(results)
    bullet_count += len(results)

    ###########################################################################

    paragraph_count = document_text.count('\n \n')

    document_words = document_text.split()
    word_count = len(document_words) - bullet_count

    return document_text, word_count, paragraph_count, bullet_count, image_count


def convert_pdf_to_txt(fileName):
    # sourced from https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(fileName, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def analysePdfFilePymupdf(fileName):

    # adapted from method at https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python

    # delete everything in the temporary image directory
    image_path = './temp_image_files/'
    resetDirectory(image_path)

    image_count = 0
    document = fitz.open(fileName)
    for i in range(len(document)):
        for image in document.get_page_images(i):
            # extract raw image
            xref = image[0]
            # create pixel map using raw image
            pix = fitz.Pixmap(document, xref)
            # save gray or rgb pixel map as png file
            if pix.n < 5:
                pix.save(image_path + "%s.png" % (xref))
            # convert cmyk pixel map to rgb then save as png file
            else:
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.save(image_path + "%s.png" % (xref))
                pix1 = None
            pix = None

    # path joining version for other paths
    image_count = len([name for name in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, name))])

    # reset temp image folder for next use (comment out if further inspection of files needed)
    resetDirectory(image_path)

    return image_count
