from nlp_resources.flesch_kincaid import readability


def reading_ease_experiment(document_text, reading_ease_target_score):

    # call the NLP resource    
    reading_ease_score, reading_ease_assessment = readability(document_text)

    # calculate simple distance from target score as rating
    accessibility_rating = round(max(0, 100 - abs(reading_ease_score - reading_ease_target_score)), 2)

    return reading_ease_score, reading_ease_assessment, accessibility_rating

