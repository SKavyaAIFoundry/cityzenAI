import nltk
import numpy as np
import pandas as pd
import string
import syllables

from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')


def readability(text):

    # sentence count is performed with a prebuilt sentence tokenizer
    sent_count = len(sent_tokenize(text))

    # word count is done with a prebuilt word tokenizer
    # punctuation is removed after tokenization as word_tokenizer treats these as tokens
    token_list = word_tokenize(text)
    token_list = [token for token in token_list if token not in string.punctuation]
    word_count = len(token_list)

    # syllables are counted using a prebuilt function
    # function works by looking up each word token in the Carnegie Mellon University’s pronunciation dictionary
    # and counting the number of stressed vowels, before summing for the entire text
    syllable_count = syllables.estimate(text)

    # calculate Flesch reading score and round to 1 d.p.
    score = 206.835 - 1.015*(word_count/sent_count) - 84.6*(syllable_count/word_count)
    score = np.round(score, 1)

    # find note in the Flesch reading table to explain score
    # import csv copy of the Flesch table (with lower threshold column added)
    table = pd.read_csv('./data/flesch_reading_ease.csv')
    # reference score in table and find corresponding note message
    for threshold in table['Lower Threshold']:
        if threshold < score:
            message = table['Notes'][table['Lower Threshold'].to_list().index(threshold)]
            # break loop after correct note is found
            if threshold < score:
                break

    return score, message