# import necessary libraries
import streamlit as st

from experiments.gender_test_experiment import gender_test_experiment
from pages.page_components.cache_file_content import cache_file_content
from pages.page_components.page_feedback import show_gender_test_feedback
from pages.page_components.page_instructions import page_instructions_experiment
from pages.page_components.page_results import show_gender_test_results


document_path = './example_documents/'

def show():

    # show instructions if file has not been selected in dashboard
    if st.session_state.current_document == None:
        page_instructions_experiment()
    
    else:
        st.title("Test for Actual Gender")

        st.write("This experiment has an additional gender-based approach, to be "
            + "performed to search for gendered and/or gender-neutral pronouns in "
            + "text when referring to people.  Similar to the experiment on gendered "
            + "language, a list of gendered pronouns ('he', 'her', etc) is searched "
            + "for within text resources utilising a pronoun counter method.")

        st.write("Resources will be scored with one of two selectable objectives: "
            + "maximising gender neutrality or balance by aiming for equally "
            + "proportionate inclusion of gender pronouns. "
        )

        st.write("The objective can be changed in the sidebar.")

        st.write("--------------------")

        # experiment options
        gender_test_experiment_options = ['Pronoun neutrality', 'Pronoun balance']
        experiment_option_expander = st.sidebar.expander(label='Gender test options', expanded=True)
        with experiment_option_expander:
            gender_test_objective = st.radio('Experiment objective', gender_test_experiment_options,
                index=gender_test_experiment_options.index(st.session_state.gender_test_objective))

        # set current document to be analysed - selected in dashboard
        current_document = st.session_state.current_document
        st.sidebar.write("Current document:")
        st.sidebar.write(current_document)

        ###########################################################################

        # path of current document
        file_name = document_path + current_document

        # extract file content for experiment (cached on first run)
        return_status, document_text, word_count, paragraph_count, bullet_count, image_count = cache_file_content(file_name)

        if return_status != "OK":
            st.subheader(str(return_status))
        else:
            # run gender test experiment
            (pronoun_female_count, female_percentage, pronoun_male_count, male_percentage,
                pronoun_binary_neutral_count, binary_neutral_percentage, pronoun_neutral_count,
                neutral_percentage, gender_test_rating) = gender_test_experiment(document_text, gender_test_objective)

            # show gender test results and feedback
            show_gender_test_results(pronoun_female_count, female_percentage, pronoun_male_count,
                male_percentage, pronoun_binary_neutral_count, binary_neutral_percentage,
                pronoun_neutral_count, neutral_percentage, gender_test_rating)
            show_gender_test_feedback(gender_test_rating)

            # update session state variables
            st.session_state.gender_test_objective = gender_test_objective


