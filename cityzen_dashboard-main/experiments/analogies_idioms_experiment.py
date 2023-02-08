import csv
import nltk
import numpy as np


def analogies_idioms_experiment(document_text, idioms_non_stem_weight, idioms_sports_weight,
    idioms_english_common_weight, idioms_english_fairly_common_weight,
    idioms_english_uncommon_weight, idioms_total_weight):

    # directory of idiom CSV files
    idiom_path = './example_idioms/'

    # convert input text to lower case to match with lower case idiom file content
    document_text_lower_case = document_text.lower()
    sentence_list = nltk.tokenize.sent_tokenize(document_text_lower_case)
    #print(sentence_list)

    def match_idioms(sentence_list, file_name):
        # open given idiom CSV file
        with open(idiom_path + file_name, newline='') as file:
            reader = csv.reader(file)
            idioms_list = list(reader)
        #print(idioms_list)

        # declare list for matched idioms
        match_list = []

        # search each input text sentence for idioms in CSV file
        for sentence in sentence_list:
            #print("*" + sentence + "*")
            for idiom in idioms_list:
                #print(str(idiom[0]))
                if idiom[0] in sentence:
                    #print(idiom[0])
                    match_list.append(idiom[0])
        print(match_list)
        return match_list

    # find idioms in each category and sort results alphabetically
    non_stem_list = sorted(match_idioms(sentence_list, 'example_non_stem_terms.csv'))
    sports_list = sorted(match_idioms(sentence_list, 'list_of_sports_idioms.csv'))
    english_common_list = sorted(match_idioms(sentence_list, 'english_idioms_common.csv'))
    english_fairly_common_list = sorted(match_idioms(sentence_list, 'english_idioms_fairly_common.csv'))
    english_uncommon_list = sorted(match_idioms(sentence_list, 'english_idioms_uncommon.csv'))

    ###################################################################

    # get unique terms and occurrences for each category

    # non-STEM terms
    non_stem_total_terms = len(non_stem_list)
    non_stem_unique_terms, non_stem_unique_frequencies = np.unique(non_stem_list, return_counts=True)
    non_stem_occurrences = sum(non_stem_unique_frequencies)

    # sports idioms
    sports_total_terms = len(sports_list)
    sports_unique_terms, sports_unique_frequencies = np.unique(sports_list, return_counts=True)
    sports_occurrences = sum(sports_unique_frequencies)

    # english idioms - common
    english_common_total_terms = len(english_common_list)
    english_common_unique_terms, english_common_unique_frequencies = np.unique(english_common_list, return_counts=True)
    english_common_occurrences = sum(english_common_unique_frequencies)

    # english idioms - fairly common
    english_fairly_common_total_terms = len(english_fairly_common_list)
    english_fairly_common_unique_terms, english_fairly_common_unique_frequencies = np.unique(english_fairly_common_list, return_counts=True)
    english_fairly_common_occurrences = sum(english_common_unique_frequencies)

    # english idioms - uncommon
    english_uncommon_total_terms = len(english_uncommon_list)
    english_uncommon_unique_terms, english_uncommon_unique_frequencies = np.unique(english_uncommon_list, return_counts=True)
    english_uncommon_occurrences = sum(english_uncommon_unique_frequencies)

    ###################################################################

    # calculate score

    # method 1 - calculate distance from weighted proportion
    total_occurrences = (
        non_stem_occurrences
        + sports_occurrences
        + english_common_occurrences
        + english_fairly_common_occurrences
        + english_uncommon_occurrences
    )

    # default rating before deductions
    idioms_rating = 100
    
    non_stem_score = 0
    sports_score = 0
    english_common_score = 0
    english_fairly_common_score = 0
    english_uncommon_score = 0

    # calculate individual score based on distance from target occurrences
    def calculate_idiom_score(occurrences, weight):
        percentage = (occurrences / total_occurrences) * 100
        #print("percentage: " + str(percentage))
        target = (weight / idioms_total_weight) * 100
        #print("target: " + str(target))
        distance = abs(percentage - target)
        #print("distance: " + str(distance))
        score = 100 - distance
        return score

    if total_occurrences > 0:
        non_stem_score = round(calculate_idiom_score(non_stem_occurrences, idioms_non_stem_weight), 2)
        print(non_stem_score)

        sports_score = round(calculate_idiom_score(sports_occurrences, idioms_sports_weight), 2)
        print(sports_score)

        english_common_score = round(calculate_idiom_score(english_common_occurrences, idioms_english_common_weight), 2)
        print(english_common_score)

        english_fairly_common_score = round(calculate_idiom_score(english_fairly_common_occurrences, idioms_english_fairly_common_weight), 2)
        print(english_fairly_common_score)

        english_uncommon_score = round(calculate_idiom_score(english_uncommon_occurrences, idioms_english_uncommon_weight), 2)
        print(english_uncommon_score)

        # calculate combined rating based on all weighted individual scores
        idioms_rating = round((
            non_stem_score * (idioms_non_stem_weight / idioms_total_weight)
            + sports_score * (idioms_sports_weight / idioms_total_weight)
            + english_common_score * (idioms_english_common_weight / idioms_total_weight)
            + english_fairly_common_score * (idioms_english_fairly_common_weight / idioms_total_weight)
            + english_uncommon_score * (idioms_english_uncommon_weight / idioms_total_weight)
        ), 2)

    print(idioms_rating)

    # method 2 - calculate distribution using gini coefficient

    #gini_coefficient = calculate_gini_coefficient([
    #    (non_stem_occurrences * idioms_non_stem_weight),
    #    (sports_occurrences * idioms_sports_weight),
    #    (english_common_occurrences * idioms_english_common_weight),
    #    (english_fairly_common_occurrences * idioms_english_fairly_common_weight),
    #    (english_uncommon_occurrences * idioms_english_uncommon_weight)
    #]) * 100
    #print(gini_coefficient)

    #idioms_rating = round(max(0, (100 - gini_coefficient)), 2)
    #print(idioms_rating)

    return (
        non_stem_unique_terms, non_stem_unique_frequencies, non_stem_score,
        sports_unique_terms, sports_unique_frequencies, sports_score,
        english_common_unique_terms, english_common_unique_frequencies, english_common_score,
        english_fairly_common_unique_terms, english_fairly_common_unique_frequencies, english_fairly_common_score,
        english_uncommon_unique_terms, english_uncommon_unique_frequencies, english_uncommon_score,
        idioms_rating
    )