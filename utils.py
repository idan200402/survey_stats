import json

files_pool = ['submissions_1st_survey.json', 'submissions_2nd_survey.json', 'submissions_3rdA_survey.json',
              'submissions_3rdB_survey.json', 'submissions_4th_survey.json']


def merge_jsons(json_files):
    """
    input: list of json files.
    output: merged list of all the data in the json files.
    """
    merged_data = []
    for file in json_files:
        file = "data/" + file
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)
    return merged_data


def median(lst):
    """
    input: list of numbers.
    return. median of the list:
    """
    lst = sorted(lst)
    n = len(lst)
    if n % 2 == 1:
        return lst[n // 2]
    else:
        return (lst[n // 2 - 1] + lst[n // 2]) / 2


def common_education_level(education_levels):
    """
    :param education_levels:
    :return: common education level among the participants.
    """
    from collections import Counter
    counter = Counter(education_levels)
    most_common = counter.most_common(1)
    return most_common[0][0] if most_common else None


def base_question(trial_id):
    """
    :param Math__AT_vs_AF
    :return: Math
    """
    return trial_id.split('__', 1)[0]


def group(chosenOptionId):
    """
    AF stays the same, AT and BT are grouped together as T.
    """
    if chosenOptionId == 'AF':
        return 'AF'
    else:
        return 'T'


def consistency_prob(row):
    """
    :param row: a participant's responses.
    :return: the probability that the participant is consistent.
    """
    answers = row['payload']['answers']
    # group the answers by base question.
    by_q = {}
    for a in answers:
        q = base_question(a['trialId'])
        g = group(a['chosenOptionId'])
        if q not in by_q:
            by_q[q] = []
        by_q[q].append(g)

    consistent = 0
    total = 0
    for q, gs in by_q.items():
        total += 1
        if gs[0] == gs[1]:
            consistent += 1

    return consistent / total
