# import necessary libraries
import streamlit as st

from experiments.gendered_language_experiment import gendered_language_experiment
from pages.page_components.cache_file_content import cache_file_content
from pages.page_components.page_feedback import show_gendered_language_feedback
from pages.page_components.page_instructions import page_instructions_experiment
from pages.page_components.page_results import show_gendered_language_results


document_path = './example_documents/'

def show():

    # show instructions if file has not been selected in dashboard
    if st.session_state.current_document == None:
        page_instructions_experiment()
    
    else:
        st.title("Gendered Language")

        st.write("This experiment will be performed to search for gendered and/or "
            + "gender-neutral nouns in text when referring to subjects.  A list of "
            + "gendered nouns, such as 'freshman', 'actress', etc is searched for "
            + "within text resources, the results indicating the proportion of "
            + "gendered and/or gender-neutral nouns when describing subjects. ")

        st.write("Resources will be scored with one of two selectable objectives: "
            + "maximising gender neutrality or balancing the use of all gendered terms "
            + "by comparing with the proportions of terms in the list of gendered nouns. "
        )

        st.write("The objective can be changed in the sidebar.")

        st.write("--------------------")

        # experiment options
        gendered_language_experiment_options = ['Gender neutrality', 'Gender balance']
        experiment_option_expander = st.sidebar.expander(label='Gendered language options', expanded=True)
        with experiment_option_expander:
            gendered_language_objective = st.radio('Experiment objective', gendered_language_experiment_options,
                index=gendered_language_experiment_options.index(st.session_state.gendered_language_objective))
            if gendered_language_objective == 'Gender balance':
                gendered_language_imbalance_weight = st.slider(
                    'Female/Male imbalance weight (%)', 0, 100, st.session_state.gendered_language_imbalance_weight, step=5
                )
            else:
                gendered_language_imbalance_weight = st.session_state.gendered_language_imbalance_weight

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
            # run gendered language experiment
            (female_count, female_percentage, male_count, male_percentage,
            imbalance_deduction, neutral_count, neutral_percentage,
            gendered_language_noun_list, gendered_language_rating) = (
                gendered_language_experiment(document_text, gendered_language_objective, gendered_language_imbalance_weight)
            )

            # show gendered language results and feedback
            show_gendered_language_results(female_count, female_percentage, male_count, male_percentage,
                imbalance_deduction, neutral_count, neutral_percentage, gendered_language_noun_list, gendered_language_rating)
            show_gendered_language_feedback(gendered_language_rating)

            # update session state variables
            st.session_state.gendered_language_objective = gendered_language_objective
            st.session_state.gendered_language_imbalance_weight = gendered_language_imbalance_weight

