# required library imports
import re
from nltk.tokenize import word_tokenize

def pronoun_counter(text):

    '''
    Function designed to take a text input and return a count of the genedered pronouns.
    Output will be a tuple returning the pronoun counts in the following order:
    (female, male, binary neutral, neutral)
    '''

    # establish pronoun lists (can easily be added to if required)
    female = ['she', 'her', 'hers', 'her']
    male = ['he', 'him', 'his']
    neutral = ['they', 'them', 'their']
    binary_neutral = ['he/she', 'she/he', 's/he', '(s)he', 'him/her', 'her/him', 
        'his/hers', 'his/her', 'hers/his' 'her/his']
    binary_neutral_multiword = ['he or she', 'she or he', 'him or her', 
        'her or him', 'his or hers', 'his or her', 'hers or his', 'her or his', 
        'he (or she)', 'she (or he)', 'him (or her)', 'her (or him)', 
        'his (or hers)', 'his (or her)', 'hers (or his)', 'her (or his)']

    # initialise term counts
    female_count = 0
    male_count = 0
    neutral_count = 0
    binary_neutral_count = 0

    # render all text lower case to avoid missing capitalised words
    text = text.lower()

    # remove periods to stop words being counted at the edge of sentences
    # edge case found for this in trials
    text = re.sub("\.", "", text)    

    # count binary neutral multiword terms 
    for term in binary_neutral_multiword:
        term_count = text.count(term)
        binary_neutral_count += term_count

    # remove binary neutral multiword terms to avoid double counting
    for term in binary_neutral_multiword:
        text = re.sub(term, "", text)

    # text is tokenised to avoid counting shorter terms hidden in others
    # e.g. "her" in "there"
    tokens = word_tokenize(text)

    # check through tokens and add to term counts
    for token in tokens:
        if token in female:
            female_count += 1
        if token in male:
            male_count += 1
        if token in neutral:
            neutral_count += 1
        if token in binary_neutral:
            binary_neutral_count += 1

    # return count scores as a immutable tuple
    return (female_count, male_count, binary_neutral_count, neutral_count)