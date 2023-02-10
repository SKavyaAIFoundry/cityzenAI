from nlp_resources.gendered_nouns import gendered_noun_count

def gendered_language_experiment(document_text, gendered_language_objective, gendered_language_imbalance_weight):

    gendered_language_noun_count, gendered_language_noun_list, gender_counts = gendered_noun_count(document_text)

    # get gendered noun counts and source list of nouns for analysis

    # count gendered nouns in the selected text
    female_count = gendered_language_noun_count[0]
    male_count = gendered_language_noun_count[1]
    neutral_count = gendered_language_noun_count[2]
    total_count = female_count + male_count + neutral_count

    # calculate female and male percentages in total noun count
    if female_count > 0:
        female_percentage = round((female_count / total_count) * 100, 2)
    else:
        female_percentage = 0

    if male_count > 0:
        male_percentage = round((male_count / total_count) * 100, 2)
    else:
        male_percentage = 0

    if gendered_language_objective == 'Gender balance':
        # count gendered nouns in the 'gendered_words.json' dataset
        female_gender_count = gender_counts[0]
        male_gender_count = gender_counts[1]
        neutral_gender_count = gender_counts[2]
        total_gender_count = female_gender_count + male_gender_count + neutral_gender_count

        # calculate proportion of gender counts
        female_gender_percentage = round((female_gender_count / total_gender_count) * 100, 2)
        male_gender_percentage = round((male_gender_count / total_gender_count) * 100, 2)
        neutral_gender_percentage = round((neutral_gender_count / total_gender_count) * 100, 2)
        print("Analysis of gendered words dataset:")
        print("Female: " + str(female_gender_count) + "     " + str(female_gender_percentage))
        print("Male: " + str(male_gender_count) + "     " + str(male_gender_percentage))
        print("Neutral: " + str(neutral_gender_count) + "     " + str(neutral_gender_percentage))
    
        # distances between text and data counts
        female_distance = abs(female_gender_percentage - female_percentage)
        male_distance = abs(male_gender_percentage - male_percentage)

        # weighted deduction based on combined distances and selected weight
        imbalance_deduction = round((female_distance + male_distance) * (gendered_language_imbalance_weight / 100), 2)
    else:
        imbalance_deduction = 0

    if neutral_count > 0:
        neutral_percentage = round((neutral_count / total_count) * 100, 2)
    else:
        neutral_percentage = 0

    gendered_language_rating = max(0, (neutral_percentage - (imbalance_deduction)))

    return (female_count, female_percentage, male_count, male_percentage,
        imbalance_deduction, neutral_count, neutral_percentage,
        gendered_language_noun_list, gendered_language_rating)

