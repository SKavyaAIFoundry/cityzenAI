import streamlit as st

from utilities.gauge_chart import gauge_chart


# methods to generate results of all experiments and file analysis

def get_file_content_analysis(selected_document, word_count, bullet_count, image_count, document_text):
    st.subheader("Analysis of document content: ")
    #st.subheader(str(selected_document))
    st.write("Word count: " + str(word_count))
    st.write("Bullet point count: " + str(bullet_count))
    st.write("Unique image count: " + str(image_count))
    st.write("--------------------")
    #st.write(document_text)
    #st.write("--------------------")


# gauge chart used to output all experiment ratings
def results_gauge(rating, title):
    fig = gauge_chart(rating, title)
    fig.update_layout(margin=dict(l=1, r=1, t=1, b=1, pad=0), width=300, height=300)
    st.plotly_chart(fig)   


def show_neurodiversity_results(words_per_bullet, bullet_score, words_per_image, image_score, neurodiversity_rating):
    # show neurodiversity results
    st.subheader("Neurodiversity Rating")
    st.write("Words per bullet: " + str(words_per_bullet))
    st.write("This is the word count divided by the number of bullets, lower is better.")
    st.write("--------------------")
    st.write("Bullet score: " + str(bullet_score) + "%")
    st.write("This gives a weighted percentage reflecting the proportion of bulleted content in the text.")
    st.write("--------------------")
    st.write("Words per image: " + str(words_per_image))
    st.write("This is the word count divided by the number of images, lower is better.")
    st.write("--------------------")
    st.write("Image score: " + str(image_score) + "%")
    st.write("This gives a weighted percentage reflecting the proportion of image content in the text.")
    st.write("--------------------")
    results_gauge(neurodiversity_rating, "Neurodiversity rating")
    st.write("This is a rating based on the contributions of weighted bullet and image scores.")


def show_reading_ease_results(reading_ease_score, reading_ease_assessment, accessibility_rating):
    st.write("Readability score: " + str(reading_ease_score))
    st.write("This is the readability score calculated using the Flesch-Kincaid method")
    st.write("The reading ease test is a weighted average of the number of syllables "
        + "per word and the number of words per sentence within a text.")
    st.write("--------------------")
    st.write("Assessment: " + str(reading_ease_assessment))
    st.write("This is an assessment of the readability of the text based on guidance associated with the score.")
    st.write("--------------------")
    results_gauge(accessibility_rating, "Accessibility rating")
    st.write("This is a simple rating calculated by subtracting the distance between the readability and target scores from 100%.")


def show_gendered_language_results(female_count, female_percentage, male_count, male_percentage,
        imbalance_deduction, neutral_count, neutral_percentage,
        gendered_language_noun_list, gendered_language_rating):
    st.write("Gendered language noun count: ")
    st.write("Female: " + str(female_count) + " (" + str(female_percentage) + "%)")
    st.write("Male: " + str(male_count) + " (" + str(male_percentage) + "%)")
    st.write("These are the numbers and proportions of female and male nouns in the text.")
    st.write("--------------------")
    st.write("Weighted Female/Male imbalance deduction: " + str(imbalance_deduction) + "%")
    st.write("This is a deduction which will be applied if the balanced experiment is selected.")
    st.write("It is calculated as the combined distances of the female and male "
        + "noun proportions in the text from those in the list of all gendered terms.")
    st.write("--------------------")
    st.write("Neutral: " + str(neutral_count) + " (" + str(neutral_percentage) + "%)")
    st.write("This is the number and proportion of neutral nouns in the text.")
    st.write("------------------------")
    #st.write("Gendered language noun list:")
    #st.write(str(gendered_language_noun_list))
    results_gauge(gendered_language_rating, "Gendered language rating")
    st.write("This is the rating of the text based on the level of neutrality (minus "
        + "the imbalance deduction if a balanced experiment is selected).")


def show_gender_test_results(pronoun_female_count, female_percentage, pronoun_male_count,
    male_percentage, pronoun_binary_neutral_count, binary_neutral_percentage,
    pronoun_neutral_count, neutral_percentage, gender_test_rating):
    st.write("Gendered pronoun counts: ")
    st.write("Female: " + str(pronoun_female_count) + " (" + str(female_percentage) + "%)")
    st.write("Male: " + str(pronoun_male_count) + " (" + str(male_percentage) + "%)")
    st.write("Binary Neutral: " + str(pronoun_binary_neutral_count) + " (" + str(binary_neutral_percentage) + "%)")
    st.write("Neutral: " + str(pronoun_neutral_count) + " (" + str(neutral_percentage) + "%)")
    st.write("These are the numbers and proportions of each type of gender pronoun in the text.")
    st.write("------------------------")
    results_gauge(gender_test_rating, "Gender test rating")
    st.write("This is the rating based on the level of neutrality or balance in "
        + "the text depending on which experiment objective is selected.")


def show_analogies_idioms_results(non_stem_unique_frequencies, non_stem_unique_terms, non_stem_score,
    sports_unique_frequencies, sports_unique_terms, sports_score,
    english_common_unique_frequencies, english_common_unique_terms, english_common_score,
    english_fairly_common_unique_frequencies, english_fairly_common_unique_terms, english_fairly_common_score,
    english_uncommon_unique_frequencies, english_uncommon_unique_terms, english_uncommon_score,
    idioms_rating):

    st.subheader("Non-STEM Terms")
    non_stem_occurrences = sum(non_stem_unique_frequencies)
    st.write("Unique terms: " + str(len(non_stem_unique_terms)))
    st.write("Total occurrences: " + str(non_stem_occurrences))
    st.write("Score: " + str(non_stem_score) + "%")
    if len(non_stem_unique_terms) > 0:
        show_non_stem_detail = st.checkbox('Show non-STEM detail')
        if show_non_stem_detail:
            for i in range(len(non_stem_unique_terms)):
                st.write(str(non_stem_unique_frequencies[i]) + " * '" + non_stem_unique_terms[i] + "'")
    st.write("--------------------")

    st.subheader("Sports Idioms")
    sports_occurrences = sum(sports_unique_frequencies)
    st.write("Unique terms: " + str(len(sports_unique_terms)))
    st.write("Total occurrences: " + str(sports_occurrences))
    st.write("Score: " + str(sports_score) + "%")
    if len(sports_unique_terms) > 0:
        show_sports_detail = st.checkbox('Show sports detail')
        if show_sports_detail:
            for i in range(len(sports_unique_terms)):
                st.write(str(sports_unique_frequencies[i]) + " * '" + sports_unique_terms[i] + "'")
    st.write("--------------------")

    st.subheader("English Idioms - Common")
    english_common_occurrences = sum(english_common_unique_frequencies)
    st.write("Unique terms: " + str(len(english_common_unique_terms)))
    st.write("Total occurrences: " + str(english_common_occurrences))
    st.write("Score: " + str(english_common_score) + "%")
    if len(english_common_unique_terms) > 0:
        show_english_common_detail = st.checkbox('Show English common detail')
        if show_english_common_detail:
            for i in range(len(english_common_unique_terms)):
                st.write(str(english_common_unique_frequencies[i]) + " * '" + english_common_unique_terms[i] + "'")
    st.write("--------------------")

    st.subheader("English Idioms - Fairly Common")
    english_fairly_common_occurrences = sum(english_common_unique_frequencies)
    st.write("Unique terms: " + str(len(english_fairly_common_unique_terms)))
    st.write("Total occurrences: " + str(english_fairly_common_occurrences))
    st.write("Score: " + str(english_fairly_common_score) + "%")
    if len(english_fairly_common_unique_terms) > 0:
        show_english_fairly_common_detail = st.checkbox('Show English fairly common detail')
        if show_english_fairly_common_detail:
            for i in range(len(english_fairly_common_unique_terms)):
                st.write(str(english_fairly_common_unique_frequencies[i]) + " * '" + english_fairly_common_unique_terms[i] + "'")
    st.write("--------------------")

    st.subheader("English Idioms - Uncommon")
    english_uncommon_occurrences = sum(english_uncommon_unique_frequencies)
    st.write("Unique terms: " + str(len(english_uncommon_unique_terms)))
    st.write("Total occurrences: " + str(english_uncommon_occurrences))
    st.write("Score: " + str(english_uncommon_score) + "%")
    if len(english_uncommon_unique_terms) > 0:
        show_english_uncommon_detail = st.checkbox('Show English uncommon detail')
        if show_english_uncommon_detail:
            for i in range(len(english_uncommon_unique_terms)):
                st.write(str(english_uncommon_unique_frequencies[i]) + " * '" + english_uncommon_unique_terms[i] + "'")

    st.write("--------------------")

    print(idioms_rating)
    results_gauge(idioms_rating, "Analogies & Idioms rating")
        
