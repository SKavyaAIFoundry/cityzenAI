import os.path as path
import streamlit as st

from os import listdir
from statistics import mean

from experiments.analogies_idioms_experiment import analogies_idioms_experiment
from experiments.experiment_defaults import (
    get_neurodiversity_default_values,
    get_reading_ease_default_values,
    get_gendered_language_default_values,
    get_gender_test_default_values,
    get_idioms_default_values
)
from experiments.gender_test_experiment import gender_test_experiment
from experiments.gendered_language_experiment import gendered_language_experiment
from experiments.neurodiversity_experiment import neurodiversity_experiment
from experiments.reading_ease_experiment import reading_ease_experiment

from pages.page_components.cache_file_content import cache_file_content
from pages.page_components.page_feedback import (
    show_analogies_idioms_feedback,
    show_neurodiversity_score_feedback,
    show_neurodiversity_rating_feedback,
    show_reading_ease_feedback,
    show_gendered_language_feedback,
    show_gender_test_feedback
)
from pages.page_components.page_instructions import page_instructions_dashboard
from pages.page_components.session_state import (
    setup_session_state_data,
    export_experiment_parameter_values
)

from utilities.gauge_chart import gauge_chart


document_path = './example_documents/'

def show():
    # set up session state data...
    setup_session_state_data()

    # list files in the documents directory
    file_list = [file for file in listdir(document_path) if path.isfile(path.join(document_path, file))]

    # document options
    document_option_expander = st.sidebar.expander(label='Document selection')
    with document_option_expander:
        selected_document = st.selectbox("Select document", file_list)
        st.write("Selected document:")
        st.write(selected_document)
        if document_option_expander.button("Run experiments"):
            st.session_state.current_document = selected_document

    # experiment options
    experiment_option_expander = st.sidebar.expander(label='Experiment options')
    with experiment_option_expander:
        experiment_reset_button = st.button('Reset to default experiment options')
        if experiment_reset_button:
            (st.session_state.neurodiversity_bullet_weight,
                st.session_state.neurodiversity_image_weight,
                st.session_state.neurodiversity_total_weight) = get_neurodiversity_default_values()
            st.session_state.reading_ease_target_score = get_reading_ease_default_values()
            (st.session_state.gendered_language_objective,
                st.session_state.gendered_language_imbalance_weight) = get_gendered_language_default_values()
            st.session_state.gender_test_objective = get_gender_test_default_values()
            (st.session_state.idioms_non_stem_weight,
                st.session_state.idioms_sports_weight,
                st.session_state.idioms_english_common_weight,
                st.session_state.idioms_english_fairly_common_weight,
                st.session_state.idioms_english_uncommon_weight,
                st.session_state.idioms_total_weight) = get_idioms_default_values()
            #st.experimental_rerun()

        parameter_export_button = st.button('Export parameter values to CSV')
        if parameter_export_button:
            export_experiment_parameter_values()

    # show instructions if file has not been selected in dashboard
    if st.session_state.current_document == None:
        page_instructions_dashboard()

    else:
        col1, col2 = st.columns([1, 2.3])
        col2.title("Overall Rating")
        
        # set current document to be analysed
        current_document = st.session_state.current_document
        st.sidebar.write("Current document:")
        st.sidebar.write(current_document)

        # declare list for ratings of all experiments
        overall_ratings = []

        ###########################################################################

        # path of current document
        file_name = document_path + current_document

        # extract file content for experiment (cached on first run)
        return_status, document_text, word_count, paragraph_count, bullet_count, image_count = cache_file_content(file_name)

        if return_status != "OK":
            st.subheader(str(return_status))
        else:
            # run neurodiversity experiment
            words_per_bullet, bullet_score, words_per_image, image_score, neurodiversity_rating = (
                neurodiversity_experiment(word_count, bullet_count, image_count,
                    st.session_state.neurodiversity_bullet_weight, st.session_state.neurodiversity_image_weight,
                    st.session_state.neurodiversity_total_weight)
            )

            # add result to overall results list
            overall_ratings.append(neurodiversity_rating)

            ###########################################################################

            # run reading ease experiment
            reading_ease_score, reading_ease_assessment, accessibility_rating = (
                reading_ease_experiment(document_text, st.session_state.reading_ease_target_score)
            )

            # add result to overall results list
            overall_ratings.append(accessibility_rating)

            ###########################################################################

            # run gendered language experiment
            (female_count, female_percentage, male_count, male_percentage,
                imbalance_deduction, neutral_count, neutral_percentage,
                gendered_language_noun_list, gendered_language_rating) = (
                gendered_language_experiment(
                    document_text, st.session_state.gendered_language_objective,
                    st.session_state.gendered_language_imbalance_weight
                )
            )

            # add result to overall results list
            overall_ratings.append(gendered_language_rating)

            ###########################################################################

            # run gender test experiment
            (pronoun_female_count, female_percentage, pronoun_male_count, male_percentage,
                pronoun_binary_neutral_count, binary_neutral_percentage, pronoun_neutral_count,
                neutral_percentage, gender_test_rating) = gender_test_experiment(document_text, st.session_state.gender_test_objective)

            # add result to overall results list
            overall_ratings.append(gender_test_rating)

            ###########################################################################

            # run analogies & idioms experiment
            (non_stem_unique_terms, non_stem_unique_frequencies, non_stem_score,
                sports_unique_terms, sports_unique_frequencies, sports_score,
                english_common_unique_terms, english_common_unique_frequencies, english_common_score,
                english_fairly_common_unique_terms, english_fairly_common_unique_frequencies, english_fairly_common_score,
                english_uncommon_unique_terms, english_uncommon_unique_frequencies, english_uncommon_score,
                idioms_rating) = analogies_idioms_experiment (
                document_text, st.session_state.idioms_non_stem_weight, st.session_state.idioms_sports_weight,
                st.session_state.idioms_english_common_weight, st.session_state.idioms_english_fairly_common_weight,
                st.session_state.idioms_english_uncommon_weight, st.session_state.idioms_total_weight
            )
            
            # add result to overall results list
            overall_ratings.append(idioms_rating)

            ###########################################################################

            # summarise results as a dashboard
            overall_rating = mean(overall_ratings)

            # gauge chart for experiment ratings
            def results_gauge(rating, title, width, height):
                fig = gauge_chart(rating, title)
                fig.update_layout(margin=dict(l=1, r=1, t=1, b=1, pad=0), width=width, height=height)
                #st.plotly_chart(fig)
                return fig

            # output overall rating
            col1, col2, col3 = st.columns([1,2.5,1])
            width = 400
            height = 200
            col2.plotly_chart(results_gauge(overall_rating, "Overall Rating", width, height))

            # output individual ratings
            col1, col2 = st.columns([1, 2])
            col2.subheader("Experiment Ratings")

            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
            width = 200
            height = 175
            col1.plotly_chart(results_gauge(neurodiversity_rating, "Neurodiversity", width, height))
            col3.plotly_chart(results_gauge(accessibility_rating, "Accessibility", width, height))
            col5.plotly_chart(results_gauge(gendered_language_rating, "Gendered Language", width, height))

            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
            col2.plotly_chart(results_gauge(gender_test_rating, "Test for Gender", width, height))
            col4.plotly_chart(results_gauge(idioms_rating, "Analogies and Idioms", width, height))

            # show feedback comments for all experiments
            st.subheader("Feedback")
            show_neurodiversity_score_feedback("bullet point", bullet_score)
            show_neurodiversity_score_feedback("image", image_score)
            show_neurodiversity_rating_feedback(neurodiversity_rating)
            show_reading_ease_feedback(accessibility_rating)
            show_gendered_language_feedback(gendered_language_rating)
            show_gender_test_feedback(gender_test_rating)
            show_analogies_idioms_feedback(idioms_rating)

            st.write("--------------------")
            
            ###################################################################

            # option to show text content for reference
            show_content_option = st.checkbox('Show document text')
            if show_content_option:
                st.subheader("Document text")
                st.write(document_text)

            