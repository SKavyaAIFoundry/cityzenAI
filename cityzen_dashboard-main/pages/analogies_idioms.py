import streamlit as st

from experiments.analogies_idioms_experiment import analogies_idioms_experiment    
from pages.page_components.page_instructions import page_instructions_experiment
from pages.page_components.cache_file_content import cache_file_content
from pages.page_components.page_results import show_analogies_idioms_results
from pages.page_components.page_feedback import show_analogies_idioms_feedback


document_path = './example_documents/'
idiom_path = './example_idioms/'

def show():

    # show instructions if file has not been selected in dashboard
    if st.session_state.current_document == None:
        page_instructions_experiment()

    else:
        st.title("Analogies and Idioms")

        st.write("This experiment involves searching text for analogies and idioms, "
        + "to consider inclusivity by determining how broad the range of topics is "
        + "when explaining concepts in materials.  This involves identifying terms and idioms "
        + "of various categories, most significantly non-STEM related topics in the "
        + "documents which could indicate which topics have been used to provide examples "
        + "and in the text.  The goals of the experiment are to assess the broadness "
        + "of topics used as examples in text (with a broader range indicating greater inclusivity) "
        + "and suitability of idioms in text descriptions."
        )

        st.write("Weights are applied to reflect the relative impact of each category.")
        st.write("The weight values can be amended in the sidebar.")

        st.write("--------------------")

        # experiment options
        experiment_option_expander = st.sidebar.expander(label='Analogies and idioms options', expanded=False)
        with experiment_option_expander:
            idioms_non_stem_weight = st.slider('Non-STEM term weight', 1, 10, st.session_state.idioms_non_stem_weight)
            idioms_sports_weight = st.slider('Sports idiom weight', 0, 10, st.session_state.idioms_sports_weight)
            idioms_english_common_weight = st.slider('English common idiom weight', 0, 10, st.session_state.idioms_english_common_weight)
            idioms_english_fairly_common_weight = st.slider('English fairly common idiom weight', 0, 10, st.session_state.idioms_english_fairly_common_weight)
            idioms_english_uncommon_weight = st.slider('English uncommon idiom weight', 0, 10, st.session_state.idioms_english_uncommon_weight)
            idioms_total_weight = (
                idioms_non_stem_weight
                + idioms_sports_weight
                + idioms_english_common_weight
                + idioms_english_fairly_common_weight
                + idioms_english_uncommon_weight
            )

        # set current document to be analysed - selected in dashboard
        current_document = st.session_state.current_document
        st.sidebar.write("Current document:")
        st.sidebar.write(current_document)

        #######################################################################

        # path of current document
        file_name = document_path + current_document

        # extract file content for experiment (cached on first run)
        return_status, document_text, word_count, paragraph_count, bullet_count, image_count = cache_file_content(file_name)

        if return_status != "OK":
            st.subheader(str(return_status))
        else:
            # run analogies & idioms experiment
            (non_stem_unique_terms, non_stem_unique_frequencies, non_stem_score,
                sports_unique_terms, sports_unique_frequencies, sports_score,
                english_common_unique_terms, english_common_unique_frequencies, english_common_score,
                english_fairly_common_unique_terms, english_fairly_common_unique_frequencies, english_fairly_common_score,
                english_uncommon_unique_terms, english_uncommon_unique_frequencies, english_uncommon_score,
                idioms_rating) = analogies_idioms_experiment (
                document_text, idioms_non_stem_weight, idioms_sports_weight,
                idioms_english_common_weight, idioms_english_fairly_common_weight,
                idioms_english_uncommon_weight, idioms_total_weight
            )
            
            # show analogies and idioms results and feedback
            show_analogies_idioms_results(non_stem_unique_frequencies, non_stem_unique_terms, non_stem_score,
                sports_unique_frequencies, sports_unique_terms, sports_score,
                english_common_unique_frequencies, english_common_unique_terms, english_common_score,
                english_fairly_common_unique_frequencies, english_fairly_common_unique_terms, english_fairly_common_score,
                english_uncommon_unique_frequencies, english_uncommon_unique_terms, english_uncommon_score,
                idioms_rating)
            show_analogies_idioms_feedback(idioms_rating)

            # update session state variables
            st.session_state.idioms_non_stem_weight = idioms_non_stem_weight
            st.session_state.idioms_sports_weight = idioms_sports_weight
            st.session_state.idioms_english_common_weight = idioms_english_common_weight
            st.session_state.idioms_english_fairly_common_weight = idioms_english_fairly_common_weight
            st.session_state.idioms_english_uncommon_weight = idioms_english_uncommon_weight
            st.session_state.idioms_total_weight = idioms_total_weight

