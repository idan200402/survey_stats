import json

from utils import (
    comparison_pair,
    merge_jsons,
    median,
    common_education_level,
    resolve_path,
)

files_pool = [
    "submissions_1st_survey.json",
    "submissions_2nd_survey.json",
    "submissions_3rdA_survey.json",
    "submissions_3rdB_survey.json",
    "submissions_4th_survey.json",
]

flag = True
if flag:
    file = resolve_path("submissions_2nd_survey_20.json")
    with open(file, "r", encoding="utf-8") as f:
        rows = json.load(f)
else:
    rows = merge_jsons(["submissions_1st_survey_20.json" , "submissions_1st_survey_20_mock.json"])

# For each question (trialId), count options chosen.
trial_counts = {}

# Across all trials, aggregate by comparison type (AF vs AT) and (AF vs BT)
af_at_counts = {}
af_bt_counts = {}

for row in rows:
    for a in row["payload"]["answers"]:
        trial_id = a["trialId"]
        option = a["chosenOptionId"]

        if trial_id not in trial_counts:
            trial_counts[trial_id] = {}
        if option not in trial_counts[trial_id]:
            trial_counts[trial_id][option] = 0
        trial_counts[trial_id][option] += 1

        pair = comparison_pair(trial_id)

        if pair == ("AF", "AT"):
            af_at_counts[option] = af_at_counts.get(option, 0) + 1

        if pair == ("AF", "BT"):
            af_bt_counts[option] = af_bt_counts.get(option, 0) + 1

# Age stats
ages = [int(row["payload"]["participant"]["age"]) for row in rows]
average_age = sum(ages) / len(ages)
median_age = median(ages)

# Education stats
education_levels = [row["payload"]["participant"]["education"] for row in rows]
most_common_education = common_education_level(education_levels)

print(
    f"per question (trialID), summing up to {len(rows[0]['payload']['answers'])} questions across {len(rows)} participants"
)
for trial_id, options in trial_counts.items():
    total = sum(options.values())
    print(trial_id)
    for option, count in options.items():
        print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

print("\n---AF_vs_AT---")
total_af_at = sum(af_at_counts.values())
for option, count in af_at_counts.items():
    print(f"option {option} probability: {count / total_af_at:.3f} ({count}/{total_af_at})")

print("\n---AF_vs_BT---")
total_af_bt = sum(af_bt_counts.values())
for option, count in af_bt_counts.items():
    print(f"option {option} probability: {count / total_af_bt:.3f} ({count}/{total_af_bt})")

print("\nthe ages of the participants:", ages)
print(f"Average age: {average_age:.2f}")
print(f"Median age: {median_age}")
print(f"Most common education level: {most_common_education}")