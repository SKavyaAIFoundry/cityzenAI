# import necessary libraries
import streamlit as st

from experiments.neurodiversity_experiment import neurodiversity_experiment
from pages.page_components.cache_file_content import cache_file_content
from pages.page_components.page_feedback import (
    show_neurodiversity_score_feedback,
    show_neurodiversity_rating_feedback
)
from pages.page_components.page_instructions import page_instructions_experiment
from pages.page_components.page_results import (
    get_file_content_analysis,
    show_neurodiversity_results
)


document_path = './example_documents/'

def show():

    # show instructions if file has not been selected in dashboard
    if st.session_state.current_document == None:
        page_instructions_experiment()

    else:
        st.title("Neurodiversity")

        st.write("This experiment involves analysing the proportion of block text, "
            + "bullet-pointed text, and images to determine the mix of textual and "
            + "visual representation in learning materials.  The goal of this experiment "
            + "is to measure the accessibility of the materials based on the diversity "
            + "of content and their suitability for a range of neurodiverse learners."
        )

        st.write("Weights are applied to bullet points and images to reflect the relative impact of each content type.")
        st.write("The weight values can be amended in the sidebar.")

        st.write("--------------------")

        # experiment options
        experiment_option_expander = st.sidebar.expander(label='Neurodiversity options', expanded=False)
        with experiment_option_expander:
            neurodiversity_bullet_weight = st.slider('bullet point weight', 1, 10, st.session_state.neurodiversity_bullet_weight)
            neurodiversity_image_weight = st.slider('image weight', 1, 10, st.session_state.neurodiversity_image_weight)
            neurodiversity_total_weight = neurodiversity_bullet_weight + neurodiversity_image_weight

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
            # show file content analysis
            get_file_content_analysis(current_document, word_count, bullet_count, image_count, document_text)

            # run neurodiversity experiment
            words_per_bullet, bullet_score, words_per_image, image_score, neurodiversity_rating = (
                neurodiversity_experiment(word_count, bullet_count, image_count,
                    neurodiversity_bullet_weight, neurodiversity_image_weight, neurodiversity_total_weight)
            )

            # show neurodiversity results and feedback
            show_neurodiversity_results(words_per_bullet, bullet_score, words_per_image, image_score, neurodiversity_rating)
            show_neurodiversity_score_feedback("bullet point", bullet_score)
            show_neurodiversity_score_feedback("image", image_score)
            show_neurodiversity_rating_feedback(neurodiversity_rating)

            # update session state variables
            st.session_state.neurodiversity_bullet_weight = neurodiversity_bullet_weight
            st.session_state.neurodiversity_image_weight = neurodiversity_image_weight
            st.session_state.neurodiversity_total_weight = neurodiversity_total_weight

