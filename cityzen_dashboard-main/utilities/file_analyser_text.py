# method for extracting content from text files

def analyseTextFile(fileName):
    word_count = 0
    paragraph_count = 0
    bullet_count = 0

    document = open(fileName)
    document_text = document.read()
    document_words = document_text.split()

    for word in document_words:
        if word == "*":
            bullet_count += 1

    word_count = len(document_words) - bullet_count
    paragraph_count = document_text.count('\n\n')
    paragraph_count += bullet_count

    return document_text, word_count, paragraph_count, bullet_count


