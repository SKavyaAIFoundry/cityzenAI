import pandas as pd
import streamlit as st


# feedback generation method for all experiments
def generate_feedback(table, result):
    # create dataframe
    df = pd.DataFrame(table, columns = ['Lower Threshold', 'Feedback'])
    #print(df)
    feedback = ""

    # select appropriate feedback comment
    for threshold in df['Lower Threshold']:
        #print(threshold)
        if threshold < result:
            feedback = df['Feedback'][df['Lower Threshold'].to_list().index(threshold)]
            break
    print(feedback)
    return feedback


def show_neurodiversity_score_feedback(material, score):
    # declare and initialise feedback table
    table = [
        [90, 'The document contains lots of ' + material + 's, increasing its accessibility.'],
        [70, 'The number of ' + material + 's in the document increase its accessibility but could be improved.'],
        [50, 'The accessibility needs to be increased by adding a lot more ' + material + 's to the document.'],
        [30, 'A significant number of additional ' + material + 's is needed to improve accessibility.'],
        [-1, 'The ' + material + ' count is far too low for the document.'],
    ]
    feedback = generate_feedback(table, score)
    st.write(feedback)


def show_neurodiversity_rating_feedback(neurodiversity_rating):
    # declare and initialise feedback table
    table = [
        [90, 'The document has a high level of accessibility.'],
        [70, 'The document has a fairly high level of accessibility but could be improved.'],
        [50, 'The document needs significant improvement to be accessible for all learners.'],
        [30, 'Learners will find it difficult to engage with the document content.'],
        [-1, 'The document is unsuitable for the target audience.'],
    ]
    feedback = generate_feedback(table, neurodiversity_rating)
    st.write(feedback)


def show_reading_ease_feedback(accessibility_rating):
    # declare and initialise feedback table
    table = [
        [90, 'The target audience will easily read and understand the text.'],
        [70, 'The text is fairly well suited to the target audience but could be improved.'],
        [50, 'The text needs improving to be fully readable for the target audience.'],
        [30, 'The target audience will find the text hard to read and understand.'],
        [-1, 'The text is unsuitable for the target audience.'],
    ]
    feedback = generate_feedback(table, accessibility_rating)
    st.write(feedback)


def show_gendered_language_feedback(gendered_language_rating):
    # declare and initialise feedback table
    table = [
        [90, 'The use of gendered language in the text is very appropriate.'],
        [70, 'Gendered language is fairly appropriate but could be improved.'],
        [50, 'The use of gendered langauge in the text needs significant improvement to be fully appropriate.'],
        [30, 'Learners may find the use of gendered language in the text inappropriate.'],
        [-1, 'The text does not use gendered language appropriately.'],
    ]
    feedback = generate_feedback(table, gendered_language_rating)
    st.write(feedback)


def show_gender_test_feedback(gender_test_rating):
    # declare and initialise feedback table
    table = [
        [90, 'The use of gender pronouns in the text is very appropriate.'],
        [70, 'Gender pronouns are used fairly appropriately but could be improved.'],
        [50, 'The use of gender pronouns in the text needs significant improvement to be fully appropriate.'],
        [30, 'Learners may find the use of gender pronouns in the text inappropriate.'],
        [-1, 'The text does not use gender pronouns appropriately.'],
    ]
    feedback = generate_feedback(table, gender_test_rating)
    st.write(feedback)


def show_analogies_idioms_feedback(idioms_rating):
    # declare and initialise feedback table
    table = [
        [90, 'The range of idioms in the text is very appropriate.'],
        [70, 'Idioms are used fairly appropriately but could be improved.'],
        [50, 'The range of idioms in the text needs significant improvement to be fully appropriate.'],
        [30, 'Learners may find the range of idioms in the text inappropriate.'],
        [-1, 'The text does not use an appropriate range of idioms.'],
    ]
    feedback = generate_feedback(table, idioms_rating)
    st.write(feedback)