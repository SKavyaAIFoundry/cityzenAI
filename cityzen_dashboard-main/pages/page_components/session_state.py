import pandas as pd
import streamlit as st
import time

from experiments.experiment_defaults import (
    get_neurodiversity_default_values,
    get_reading_ease_default_values,
    get_gendered_language_default_values,
    get_gender_test_default_values,
    get_idioms_default_values
)


# populate default values for all experiment parameters

# neurodiversity default values
(default_neurodiversity_bullet_weight,
    default_neurodiversity_image_weight,
    default_neurodiversity_total_weight) = get_neurodiversity_default_values()

# reading ease default values
default_reading_ease_target_score = get_reading_ease_default_values()

# gendered language default values
(default_gendered_language_objective,
    default_gendered_language_imbalance_weight) = get_gendered_language_default_values()

# gender test default values
default_gender_test_objective = get_gender_test_default_values()

# analogies and idioms default values = 
(default_idioms_non_stem_weight,
    default_idioms_sports_weight,
    default_idioms_english_common_weight,
    default_idioms_english_fairly_common_weight,
    default_idioms_english_uncommon_weight,
    default_idioms_total_weight) = get_idioms_default_values()


def setup_session_state_data():
    # set up streamlit session state data to retain parameter values across experiment pages

    # document to be analysed
    if 'current_document' not in st.session_state:
        st.session_state.current_document = None
    # neurodiversity experiment
    if 'neurodiversity_bullet_weight' not in st.session_state:
        st.session_state.neurodiversity_bullet_weight = default_neurodiversity_bullet_weight
    if 'neurodiversity_image_weight' not in st.session_state:
        st.session_state.neurodiversity_image_weight = default_neurodiversity_image_weight
    if 'neurodiversity_total_weight' not in st.session_state:
        st.session_state.neurodiversity_total_weight = default_neurodiversity_total_weight
    # reading ease experiment
    if 'reading_ease_target_score' not in st.session_state:
        st.session_state.reading_ease_target_score = default_reading_ease_target_score
    # gendered language experiment
    if 'gendered_language_objective' not in st.session_state:
        st.session_state.gendered_language_objective = default_gendered_language_objective
    if 'gendered_language_imbalance_weight' not in st.session_state:
        st.session_state.gendered_language_imbalance_weight = default_gendered_language_imbalance_weight
    # gender test experiment
    if 'gender_test_objective' not in st.session_state:
        st.session_state.gender_test_objective = default_gender_test_objective
    # analogies and idioms experiment
    if 'idioms_non_stem_weight' not in st.session_state:
        st.session_state.idioms_non_stem_weight = default_idioms_non_stem_weight
    if 'idioms_sports_weight' not in st.session_state:
        st.session_state.idioms_sports_weight = default_idioms_sports_weight
    if 'idioms_english_common_weight' not in st.session_state:
        st.session_state.idioms_english_common_weight = default_idioms_english_common_weight
    if 'idioms_english_fairly_common_weight' not in st.session_state:
        st.session_state.idioms_english_fairly_common_weight = default_idioms_english_fairly_common_weight
    if 'idioms_english_uncommon_weight' not in st.session_state:
        st.session_state.idioms_english_uncommon_weight = default_idioms_english_uncommon_weight
    if 'idioms_total_weight' not in st.session_state:
        st.session_state.idioms_total_weight = default_idioms_total_weight


# export default and current parameter values to csv file
def export_experiment_parameter_values():
    message_sleep_time = 5
    export_message = st.empty()      
    try:
        # declare and initialise parameter values table
        parameter_values = [
            [default_neurodiversity_bullet_weight,
            st.session_state.neurodiversity_bullet_weight,
            default_neurodiversity_image_weight,
            st.session_state.neurodiversity_image_weight,
            default_neurodiversity_total_weight,
            st.session_state.neurodiversity_total_weight,
            default_reading_ease_target_score,
            st.session_state.reading_ease_target_score,
            default_gendered_language_objective,
            st.session_state.gendered_language_objective,
            default_gendered_language_imbalance_weight,
            st.session_state.gendered_language_imbalance_weight,
            default_gender_test_objective,
            st.session_state.gender_test_objective,
            default_idioms_non_stem_weight,
            st.session_state.idioms_non_stem_weight,
            default_idioms_sports_weight,
            st.session_state.idioms_sports_weight,
            default_idioms_english_common_weight,
            st.session_state.idioms_english_common_weight,
            default_idioms_english_fairly_common_weight,
            st.session_state.idioms_english_fairly_common_weight,
            default_idioms_english_uncommon_weight,
            st.session_state.idioms_english_uncommon_weight,
            default_idioms_total_weight,
            st.session_state.idioms_total_weight,
            ]
        ]
        print(parameter_values)
        df = pd.DataFrame(parameter_values, columns = [
            'default_neurodiversity_bullet_weight',
            'current_neurodiversity_bullet_weight',
            'default_neurodiversity_image_weight',
            'current_neurodiversity_image_weight',
            'default_neurodiversity_total_weight',
            'current_neurodiversity_total_weight',
            'default_reading_ease_target_score',
            'current_reading_ease_target_score',
            'default_gendered_language_objective',
            'current_gendered_language_objective',
            'default_gendered_language_imbalance_weight',
            'current_gendered_language_imbalance_weight',
            'default_gender_test_objective',
            'current_gender_test_objective',
            'default_idioms_non_stem_weight',
            'current_idioms_non_stem_weight',
            'default_idioms_sports_weight',
            'current_idioms_sports_weight',
            'default_idioms_english_common_weight',
            'current_idioms_english_common_weight',
            'default_idioms_english_fairly_common_weight',
            'current_idioms_english_fairly_common_weight',
            'default_idioms_english_uncommon_weight',
            'current_idioms_english_uncommon_weight',
            'default_idioms_total_weight',
            'current_idioms_total_weight'
        ])
        df.to_csv('./data/parameter_values.csv', index=False)
        export_message.write("Exported!")
        time.sleep(message_sleep_time)
        export_message.empty()
    except:
        export_message.error("Error - file may be open!")
        time.sleep(message_sleep_time)
        export_message.empty()