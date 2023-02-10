# import necessary libraries
import streamlit as st

from experiments.reading_ease_experiment import reading_ease_experiment
from pages.page_components.cache_file_content import cache_file_content
from pages.page_components.page_feedback import show_reading_ease_feedback
from pages.page_components.page_instructions import page_instructions_experiment
from pages.page_components.page_results import (
    get_file_content_analysis, show_reading_ease_results
)


document_path = './example_documents/'

def show():

    # show instructions if file has not been selected in dashboard
    if st.session_state.current_document == None:
        page_instructions_experiment()
    
    else:
        st.title("Reading Ease")

        st.write("This activity involves determining reading ease of text resources, "
            + "measured using the Flesch-Kincaid grade level; a reading age of around "
            + "13 being the default target to be inclusive for a diverse range of "
            + "learners including those to whom English is not their primary language, "
            + "equating to a score of approximately 65."
        )

        st.write("The target value can be amended in the sidebar to experiment with "
            + "a range of different audiences.")

        st.write("--------------------")

        # experiment options
        experiment_option_expander = st.sidebar.expander(label='Reading ease options', expanded=True)
        with experiment_option_expander:
            reading_ease_target_score = st.slider('Target reading ease score', 1, 100, st.session_state.reading_ease_target_score)

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
            # run reading ease experiment
            reading_ease_score, reading_ease_assessment, accessibility_rating = (
                reading_ease_experiment(document_text, reading_ease_target_score)
            )

            # show reading ease results and feedback
            show_reading_ease_results(reading_ease_score, reading_ease_assessment, accessibility_rating)
            show_reading_ease_feedback(accessibility_rating)

            # update session state variables
            st.session_state.reading_ease_target_score = reading_ease_target_score

