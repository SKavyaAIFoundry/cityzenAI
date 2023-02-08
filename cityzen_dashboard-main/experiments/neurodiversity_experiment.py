def neurodiversity_experiment(word_count, bullet_count, image_count, neurodiversity_bullet_weight,
    neurodiversity_image_weight, neurodiversity_total_weight):

    # use weight first to generate individual scores based on impact of each element
    if bullet_count > 0:
        words_per_bullet = round(word_count / bullet_count, 2)
        bullet_score = round(min(1, ((bullet_count * neurodiversity_bullet_weight) / words_per_bullet)), 2) * 100
    else:
        words_per_bullet = "n/a"
        bullet_score = 0
    
    if image_count > 0:
        words_per_image = round(word_count / image_count, 2)
        image_score = round(min(1, ((image_count * neurodiversity_image_weight) / words_per_image)), 2) * 100
    else:
        words_per_image = "n/a"
        image_score = 0

    # use weight again to limit contribution of each score to its maximum contribution
    neurodiversity_rating = round((
        (
            (bullet_score * (neurodiversity_bullet_weight / neurodiversity_total_weight))
            + (image_score * (neurodiversity_image_weight / neurodiversity_total_weight))
        )
    ), 2)

    return words_per_bullet, bullet_score, words_per_image, image_score, neurodiversity_rating