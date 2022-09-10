import csv


def score_carer(carer):
    normalized_img_problems = int(carer['img_problems']) / 8
    normalized_num_previous = int(carer['num_previous_clients']) / 100
    normalized_years_experience = int(carer['years_experience']) / 100
    normalized_avg_review = float(carer['avg_review']) / 5
    normalized_type = carer['type'] / 2

    normalized_days_since_logged_in = 0 if int(carer['days_since_login']) \
        < 7 else ( int(carer['days_since_login']) if int(carer['days_since_login']) \
        < 100 else 100) / 100

    weighted_type = normalized_type / 5
    weighted_img_problems = normalized_img_problems * 0.6
    weighted_years_experience = normalized_years_experience * 1.5

    score = (normalized_avg_review * (
        normalized_num_previous
        + weighted_years_experience
        + weighted_type)
        / (1
           + weighted_img_problems
           + normalized_days_since_logged_in)
        * 100)

    return round(score, 4)


def validate_carer(carer):
    if carer['num_reviews'] > carer['num_previous_clients']:
        return False
    elif (int(carer['num_reviews']) == 0 and float(carer['avg_review']) != 0):
        return False
    else:
        return True


if __name__ == "__main__":
    carers = []
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for carer in reader:
            match carer['type']:
                case 'basic':
                    carer['type'] = 0
                case 'advanced':
                    carer['type'] = 1
                case 'expert':
                    carer['type'] = 2
                case other:
                    continue

            if not validate_carer(carer):
                continue
            score = score_carer(carer)
            carer['score'] = score
            carers.append(carer)

    sorted_list = sorted(
        carers, key=lambda carer: carer['score'], reverse=True)

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, sorted_list[0].keys())
        writer.writeheader()
        for carer in sorted_list:
            writer.writerow(carer)

