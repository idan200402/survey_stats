import json

from utils import (
    comparison_pair,
    base_question,
    merge_jsons,
    median,
    common_education_level,
    resolve_path,
    english_knowing,
    non_english_knowing
)

# -----------------------------
# Choose input
# -----------------------------
USE_SINGLE_FILE = False

if USE_SINGLE_FILE:
    file_path = resolve_path("options/submissions_2nd_survey_20_english.json")
    with open(file_path, "r", encoding="utf-8") as f:
        rows = json.load(f)
else:
    rows = merge_jsons(["options/submissions_2nd_survey_20_english.json" , "options/submissions_3rd_survey_20.json"])

# -----------------------------
# Counters
# -----------------------------

# trialId -> option -> count
trial_counts = {}

# global aggregates by comparison type
af_at_counts = {}
af_bt_counts = {}

# theme -> pair -> option -> count
theme_pair_counts = {}

# gender -> pair -> option -> count
gender_pair_counts = {}

# education -> pair -> option -> count
education_pair_counts = {}

# age groups -> pair -> option -> count
age_group_pair_counts = {}

# aducation_academic -> pair -> option -> count
education_academic_pair_counts = {}

# english knowing -> pair -> option -> count
english_knowing_pair_counts = {}


for row in rows:
    for a in row["payload"]["answers"]:
        trial_id = a["trialId"]
        option = a["chosenOptionId"]

        # --- per trialId ---
        if trial_id not in trial_counts:
            trial_counts[trial_id] = {}
        trial_counts[trial_id][option] = trial_counts[trial_id].get(option, 0) + 1

        # --- normalized pair ---
        pair = comparison_pair(trial_id)

        # --- global pair aggregates ---
        if pair == ("AF", "AT"):
            af_at_counts[option] = af_at_counts.get(option, 0) + 1
        elif pair == ("AF", "BT"):
            af_bt_counts[option] = af_bt_counts.get(option, 0) + 1

        # --- per-theme merged aggregates ---
        theme = base_question(trial_id)

        if theme not in theme_pair_counts:
            theme_pair_counts[theme] = {}
        if pair not in theme_pair_counts[theme]:
            theme_pair_counts[theme][pair] = {}
        theme_pair_counts[theme][pair][option] = theme_pair_counts[theme][pair].get(option, 0) + 1

        # --- per-gender merged aggregates ---
        gender = row["payload"]["participant"]["gender"]
        if gender not in gender_pair_counts:
            gender_pair_counts[gender] = {}
        if pair not in gender_pair_counts[gender]:
            gender_pair_counts[gender][pair] = {}
        gender_pair_counts[gender][pair][option] = gender_pair_counts[gender][pair].get(option, 0) + 1

        # --- per-education merged aggregates ---
        education = row["payload"]["participant"]["education"]
        if education not in education_pair_counts:
            education_pair_counts[education] = {}
        if pair not in education_pair_counts[education]:
            education_pair_counts[education][pair] = {}
        education_pair_counts[education][pair][option] = education_pair_counts[education][pair].get(option, 0) + 1

        # --- per-age-group merged aggregates ---
        age = int(row["payload"]["participant"]["age"])
        # if age < 28.5 group 1, else group 2
        age_group = "Young" if age < 28.5 else "Old"
        if age_group not in age_group_pair_counts:
            age_group_pair_counts[age_group] = {}
        if pair not in age_group_pair_counts[age_group]:
            age_group_pair_counts[age_group][pair] = {}
        age_group_pair_counts[age_group][pair][option] = age_group_pair_counts[age_group][pair].get(option, 0) + 1

        # --- per-education-academic merged aggregates ---
        education_ = row["payload"]["participant"]["education"]
        education_level = "Academic" if education_ in ["bachelor", "grad"] else "Non-Academic"
        if education_level not in education_academic_pair_counts:
            education_academic_pair_counts[education_level] = {}
        if pair not in education_academic_pair_counts[education_level]:
            education_academic_pair_counts[education_level][pair] = {}
        education_academic_pair_counts[education_level][pair][option] = education_academic_pair_counts[education_level][
                                                                            pair].get(option, 0) + 1

        # --- per-English-knowing merged aggregates ---
        country_ = row["payload"]["participant"]["country"].lower().strip()
        english_knowing_ = "English-knowing" if country_ in english_knowing else "Non-English-knowing"
        if english_knowing_ not in english_knowing_pair_counts:
            english_knowing_pair_counts[english_knowing_] = {}
        if pair not in english_knowing_pair_counts[english_knowing_]:
            english_knowing_pair_counts[english_knowing_][pair] = {}
        english_knowing_pair_counts[english_knowing_][pair][option] = english_knowing_pair_counts[english_knowing_][
                                                                          pair].get(option, 0) + 1

# -----------------------------
# Demographics stats
# -----------------------------
ages = [int(row["payload"]["participant"]["age"]) for row in rows]
average_age = sum(ages) / len(ages) if ages else 0.0
median_age = median(ages)

education_levels = [row["payload"]["participant"]["education"] for row in rows]
most_common_education = common_education_level(education_levels)

# dictionary of country counts
country_counts = {}
for row in rows:
    country = row["payload"]["participant"]["country"].lower().strip()
    country_counts[country] = country_counts.get(country, 0) + 1

# comments iterate through all rows and populate the above counters
comments = [row["payload"]["feedback"]["comments"] for row in rows]

# -----------------------------
# Prints (existing)
# -----------------------------
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

# demographics
print("\nthe ages of the participants:", ages)
print(f"Average age: {average_age:.2f}")
print(f"Median age: {median_age}")
print(f"Most common education level: {most_common_education}")
print("\nCountry counts:")
for country, count in country_counts.items():
    print(f"  {country}: {count}")

#show the comments
print("\nParticipant comments:")
for i, comment in enumerate(comments, 1):
    if comment.strip():  # only print non-empty comments
        print(f"{i}. {comment}")

# -----------------------------
# NEW: per-theme merged stats (all themes)
# -----------------------------
print("\n=== Per-theme merged statistics ===")

for theme in sorted(theme_pair_counts.keys()):
    print(f"\n--- Theme: {theme} ---")
    for pair in sorted(theme_pair_counts[theme].keys()):
        counts = theme_pair_counts[theme][pair]
        total = sum(counts.values())
        print(f"Pair {pair[0]}_vs_{pair[1]} (n={total})")
        for option, count in counts.items():
            print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

# -----------------------------
# stats for gender
# -----------------------------
print("\n=== Per-gender merged statistics ===")
for gender in sorted(gender_pair_counts.keys()):
    print(f"\n--- Gender: {gender} ---")
    for pair in sorted(gender_pair_counts[gender].keys()):
        counts = gender_pair_counts[gender][pair]
        total = sum(counts.values())
        print(f"Pair {pair[0]}_vs_{pair[1]} (n={total})")
        for option, count in counts.items():
            print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

# -----------------------------
# stats for education
# -----------------------------
print("\n=== Per-education merged statistics ===")
for education in sorted(education_pair_counts.keys()):
    print(f"\n--- Education: {education} ---")
    for pair in sorted(education_pair_counts[education].keys()):
        counts = education_pair_counts[education][pair]
        total = sum(counts.values())
        print(f"Pair {pair[0]}_vs_{pair[1]} (n={total})")
        for option, count in counts.items():
            print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

# -----------------------------
# stats for age groups
# -----------------------------
print("\n=== Per-age-group merged statistics ===")
for age_group in sorted(age_group_pair_counts.keys()):
    print(f"\n--- Age Group: {age_group} ---")
    for pair in sorted(age_group_pair_counts[age_group].keys()):
        counts = age_group_pair_counts[age_group][pair]
        total = sum(counts.values())
        print(f"Pair {pair[0]}_vs_{pair[1]} (n={total})")
        for option, count in counts.items():
            print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

# -----------------------------
# stats for education academic vs non-academic
# -----------------------------
print("\n=== Per-education-academic merged statistics ===")
for education_level in sorted(education_academic_pair_counts.keys()):
    print(f"\n--- Education Level: {education_level} ---")
    for pair in sorted(education_academic_pair_counts[education_level].keys()):
        counts = education_academic_pair_counts[education_level][pair]
        total = sum(counts.values())
        print(f"Pair {pair[0]}_vs_{pair[1]} (n={total})")
        for option, count in counts.items():
            print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")

# -----------------------------
# stats for English-knowing vs non-English-knowing
# -----------------------------
print("\n=== Per-English-knowing merged statistics ===")
for english_knowing_ in sorted(english_knowing_pair_counts.keys()):
    print(f"\n--- English-knowing: {english_knowing_} ---")
    for pair in sorted(english_knowing_pair_counts[english_knowing_].keys()):
        counts = english_knowing_pair_counts[english_knowing_][pair]
        total = sum(counts.values())
        print(f"Pair {pair[0]}_vs_{pair[1]} (n={total})")
        for option, count in counts.items():
            print(f"  option {option} probability: {count / total:.3f} ({count}/{total})")



print(af_at_counts)
print(af_bt_counts)
print(theme_pair_counts)

#subtract the votes from the theme 'user_personal_information' from the global counts to see the effect of that theme
precise_location_counts = theme_pair_counts.get("user_personal_information", {})
if precise_location_counts:
    for pair in precise_location_counts.keys():
        counts = precise_location_counts[pair]
        for option, count in counts.items():
            if pair == ("AF", "AT"):
                af_at_counts[option] = af_at_counts.get(option, 0) - count
            elif pair == ("AF", "BT"):
                af_bt_counts[option] = af_bt_counts.get(option, 0) - count


print("\n---AF_vs_AT (after removing user_personal_information)---")
total_af_at = sum(af_at_counts.values())
for option, count in af_at_counts.items():
    print(f"option {option} probability: {count / total_af_at:.3f} ({count}/{total_af_at})")


print("\n---AF_vs_BT (after removing user_personal_information)---")
total_af_bt = sum(af_bt_counts.values())
for option, count in af_bt_counts.items():
    print(f"option {option} probability: {count / total_af_bt:.3f} ({count}/{total_af_bt})")