import os.path as path

from utilities.file_analyser_text import analyseTextFile
from utilities.file_analyser_word import analyseDocxFileDocx, analyseDocxFileDocx2txt, analyseDocxFilePypandoc
from utilities.file_analyser_powerpoint import analysePptxFile
from utilities.file_analyser_pdf import analysePdfFilePdfreader, analysePdfFilePdfminer, analysePdfFilePypdf2, analysePdfFilePymupdf
from utilities.file_analyser_xlsx import analyseXlsxFile, xlsxRowsToTextFile


# method to call appropriate file content extraction method
def get_file_content(fileName):
    document_full_name, document_extension = path.splitext(fileName)
    document_text = None
    word_count = 0
    paragraph_count = 0
    bullet_count = 0
    image_count = 0
    return_status = "OK"

    # call appropriate extraction function for file extension
    # comment / uncomment method calls to use different extraction libraries
    if document_extension == ".txt":
        document_text, word_count, paragraph_count, bullet_count = analyseTextFile(fileName)
    elif document_extension == ".docx":
        #document_text, word_count, paragraph_count, bullet_count, image_count = analyseDocxFileDocx(fileName)
        document_text, word_count, paragraph_count, bullet_count, image_count = analyseDocxFileDocx2txt(fileName)
        #document_text, word_count, paragraph_count, bullet_count, image_count = analyseDocxFilePypandoc(fileName)
    elif document_extension == ".pdf":
        #document_text, word_count, paragraph_count, bullet_count, image_count = analysePdfFilePdfreader(fileName)
        document_text, word_count, paragraph_count, bullet_count, image_count = analysePdfFilePdfminer(fileName)
        #document_text, word_count, paragraph_count, bullet_count, image_count = analysePdfFilePypdf2(fileName)
        image_count = analysePdfFilePymupdf(fileName)
    elif document_extension == ".pptx":
        document_text, word_count, paragraph_count, bullet_count, image_count = analysePptxFile(fileName)
    elif document_extension == ".xlsx":
        document_text, word_count, paragraph_count, bullet_count, image_count = analyseXlsxFile(fileName)
    else:
        return_status = "File format '" + str(document_extension) + "' not supported"

    return return_status, document_text, word_count, paragraph_count, bullet_count, image_count