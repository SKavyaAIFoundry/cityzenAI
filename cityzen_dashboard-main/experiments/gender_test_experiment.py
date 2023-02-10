from nlp_resources.pronoun_counter import pronoun_counter
from utilities.gini_coefficient import calculate_gini_coefficient

def calculateDistance(value):
    #target = 25
    target = 33.333
    distance = round(abs(value - target), 2)
    print(distance)
    return distance


def gender_test_experiment(document_text, gender_test_objective):
    
    # get pronoun counts for all categories
    pronoun_female_count, pronoun_male_count, pronoun_binary_neutral_count, pronoun_neutral_count = pronoun_counter(document_text)

    total_count = pronoun_female_count + pronoun_male_count + pronoun_binary_neutral_count + pronoun_neutral_count

    # calculate proportion of each category
    if pronoun_female_count > 0:
        female_percentage = round((pronoun_female_count / total_count) * 100, 2)
    else:
        female_percentage = 0
    if pronoun_male_count > 0:
        male_percentage = round((pronoun_male_count / total_count) * 100, 2)
    else:
        male_percentage = 0
    if pronoun_binary_neutral_count > 0:
        binary_neutral_percentage = round((pronoun_binary_neutral_count / total_count) * 100, 2)
    else:
        binary_neutral_percentage = 0
    if pronoun_neutral_count > 0:
        neutral_percentage = round((pronoun_neutral_count / total_count) * 100, 2)
    else:
        neutral_percentage = 0

    if gender_test_objective == 'Pronoun neutrality':
        gender_test_rating = neutral_percentage

    else:
        ## method 1 - calculating distance from equal proportion
        #female_distance = calculateDistance(female_percentage)
        #male_distance = calculateDistance(male_percentage)
        #neutral_distance = calculateDistance(neutral_percentage)
        #total_distance = female_distance + male_distance + neutral_distance
        #print("total distance: " + str(total_distance))
        #gender_test_rating = round(max(0, 100 - total_distance), 2)
        #print("Gender Test Rating method 1: " + str(gender_test_rating))

        # method 2 - calculating distribution using gini coefficient
        # calculate distribution of accepted terms
        if (pronoun_female_count + pronoun_male_count + pronoun_neutral_count) > 0:
            gini_coefficient = calculate_gini_coefficient([pronoun_female_count, pronoun_male_count, pronoun_neutral_count]) * 100
            print("gini coefficient: " + str(gini_coefficient))
            # calculate score with non-accepted terms deducted
            gender_test_rating = round(max(0, ((100 - gini_coefficient) - binary_neutral_percentage)), 2)
            print("Gender Test Rating method 2: " + str(gender_test_rating))
        else:
            gender_test_rating = 100

    if total_count == 0:
        gender_test_rating = 100

    return (pronoun_female_count, female_percentage, pronoun_male_count, male_percentage,
        pronoun_binary_neutral_count, binary_neutral_percentage, pronoun_neutral_count,
        neutral_percentage, gender_test_rating
    )

