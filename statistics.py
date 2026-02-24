import json
from utils import merge_jsons, median, common_education_level



files_pool = ['submissions_1st_survey.json','submissions_2nd_survey.json','submissions_3rdA_survey.json','submissions_3rdB_survey.json','submissions_4th_survey.json']

flag = True
if flag:
    with open('submissions_4th_survey.json', 'r', encoding='utf-8') as f:
        rows = json.load(f)
else:
    json_files = files_pool
    rows = merge_jsons(json_files)

# for each question , and for each option , how many times it was chosen.
trial_counts = {}
at_af_counts = {}
af_bt_counts = {}
# for each participant
for row in rows:
    # for each question he answered
    for a in row['payload']['answers']:
        # the question.
        trial_id = a['trialId']
        # the option he chose.
        option = a['chosenOptionId']
        # if the question is not in the dictionary yet , add it.
        if trial_id not in trial_counts:
            trial_counts[trial_id] = {}
        # if the option is not in the dictionary yet , add it.
        if option not in trial_counts[trial_id]:
            trial_counts[trial_id][option] = 0  # zero times chosen until now.
        # increment the count for this option in this question.
        trial_counts[trial_id][option] += 1

        # ---AT_vs_AF---
        if trial_id.endswith('AT_vs_AF'):
            if option not in at_af_counts:
                at_af_counts[option] = 0
            at_af_counts[option] += 1

        # ---AF_vs_BT---
        if trial_id.endswith('AF_vs_BT'):
            if option not in af_bt_counts:
                af_bt_counts[option] = 0
            af_bt_counts[option] += 1

# analyzing average age across all participants.
ages = [row['payload']['participant']['age'] for row in rows]
# make the list of ages int instead of string.
ages = [int(age) for age in ages]
average_age = sum(ages) / len(ages)
median_age = median(ages)

# analyzing education levels across all participants.
education_levels = [row['payload']['participant']['education'] for row in rows]
most_common_education = common_education_level(education_levels)

# printing probabilities.
print(
    f"per question (trialID) , summing up to {len(rows[0]['payload']['answers'])} questions across {len(rows)} participants")
for trial_id, options in trial_counts.items():
    # all options answered for this question.
    total = sum(options.values())
    print(trial_id)
    for option, count in options.items():
        print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

print("\n---AT_vs_AF---")
total_at_af = sum(at_af_counts.values())
for option, count in at_af_counts.items():
    print(f"option {option} probability: {count / total_at_af:.3f} ({count}/{total_at_af})")

print("\n---AF_vs_BT---")
total_af_bt = sum(af_bt_counts.values())
for option, count in af_bt_counts.items():
    print(f"option {option} probability: {count / total_af_bt:.3f} ({count}/{total_af_bt})")

print("the ages of the participants:", ages)
print(f"\nAverage age: {average_age:.2f}")
print(f"Median age: {median_age}")

print(f"Most common education level: {most_common_education}")
