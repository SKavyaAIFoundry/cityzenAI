# import of required functions
import nltk
import pandas as pd

from nltk import pos_tag, word_tokenize

nltk.download('averaged_perceptron_tagger')


def gendered_noun_count(text):

    '''
    Functions to count the number of gendered nouns within a text.
    Returns a result tuple containing the number of female, male and gender
    neutral nouns respectively.
    '''

    # import master list of nouns and genders
    df = pd.read_json('data/gendered_words.json')
    # separate nouns into a list
    nouns = df['word'].to_list()    

    # count number of each gender in list for weights
    female_gender_count = len(df[df['gender'] == 'f'])
    male_gender_count = len(df[df['gender'] == 'm'])
    neutral_gender_count = len(df[df['gender'] == 'n'])
    gender_counts = (female_gender_count, male_gender_count, neutral_gender_count)

    # text is tokenized and tokens tagged for part of speech
    tags = pos_tag(word_tokenize(text.lower()))

    # empty lists established as data storage
    found_nouns = []
    found_genders = []

    for tag in tags:
        # nouns are extracted from the tokens and saved to a list
        if tag[1] in ['NN', 'NNS']:
            found_nouns.append(tag[0])

            # nouns contained in the master list are identified and the gender recorded
            if tag[0] in nouns:
                found_genders.append(df['gender'][nouns.index(tag[0])])

            # nouns not on the master list are identified as so
            else:
                found_genders.append('not on master list')

    # results sorted into various dataframes for use if required for development purposes
    master_results = pd.DataFrame({'noun': found_nouns, 'gender': found_genders})
    # separated identified nouns into gendered lists for inspection if required
    female_nouns = master_results[master_results['gender'] == 'f'].reset_index(drop=True)
    male_nouns = master_results[master_results['gender'] == 'm'].reset_index(drop=True)
    neutral_nouns = master_results[master_results['gender'] == 'n'].reset_index(drop=True)
    noun_list = master_results[master_results['gender'] != 'not on master list'].reset_index(drop=True)
    # returns nouns not found on masterlist for inspection if required
    outside_masterlist = master_results[master_results['gender'] == 'not on master list'].reset_index(drop=True)

    # nouns counts are generated to return as a result to the user
    female_count = len(female_nouns)
    male_count = len(male_nouns)
    neutral_count = len(neutral_nouns)
    count_result = (female_count, male_count, neutral_count)

    return count_result, noun_list, gender_counts
            