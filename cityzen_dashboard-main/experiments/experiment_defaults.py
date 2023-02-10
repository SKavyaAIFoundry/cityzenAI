# define default values for all experiments
# look at using dependency injection instead if time permits

def get_neurodiversity_default_values():
    # neurodiversity default values
    default_neurodiversity_bullet_weight = 3
    default_neurodiversity_image_weight = 5
    default_neurodiversity_total_weight = default_neurodiversity_bullet_weight + default_neurodiversity_image_weight
    return default_neurodiversity_bullet_weight, default_neurodiversity_image_weight, default_neurodiversity_total_weight


def get_reading_ease_default_values():
    # reading ease default values
    default_reading_ease_target_score = 65
    return default_reading_ease_target_score


def get_gendered_language_default_values():
    # gendered language default values
    default_gendered_language_objective = "Gender neutrality"
    default_gendered_language_imbalance_weight = 100
    return default_gendered_language_objective, default_gendered_language_imbalance_weight


def get_gender_test_default_values():
    # gender test default values
    default_gender_test_objective = "Pronoun neutrality"
    return default_gender_test_objective


def get_idioms_default_values():
    # analogies and idioms default values
    default_idioms_non_stem_weight = 5
    default_idioms_sports_weight = 5
    default_idioms_english_common_weight = 5
    default_idioms_english_fairly_common_weight = 5
    default_idioms_english_uncommon_weight = 5
    default_idioms_total_weight = (
        default_idioms_non_stem_weight
        + default_idioms_sports_weight
        + default_idioms_english_common_weight
        + default_idioms_english_fairly_common_weight
        + default_idioms_english_uncommon_weight
    )
    return (
        default_idioms_non_stem_weight,
        default_idioms_sports_weight,
        default_idioms_english_common_weight,
        default_idioms_english_fairly_common_weight,
        default_idioms_english_uncommon_weight,
        default_idioms_total_weight
    )

