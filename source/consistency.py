import json
import utils

flag = False
if flag:
    file = utils.resolve_path("options/submissions_1st_survey_20_mock.json")
    with open(file, "r", encoding="utf-8") as f:
        rows = json.load(f)
else:
    rows = utils.merge_jsons(["options/submissions_1st_survey_20_mock.json"])

print("      Prolific ID        , Consistency Probability")
probs = []
for row in rows:
    prolific_id = row["payload"]["participant"]["prolificId"]
    prob = utils.consistency_prob_general(row)
    print(f"{prolific_id} , {prob:.4f}")
    probs.append(prob)

average_prob = sum(probs) / len(probs) if probs else 0.0
print(f"Average consistency probability across all participants: {average_prob:.4f}\n\n")

print("      Prolific ID        , Consistency Probability (given AF)")
probs_af = []
for row in rows:
    prolific_id = row["payload"]["participant"]["prolificId"]
    prob = utils.consistency_prob_af(row)
    print(f"{prolific_id} , {prob:.4f}")
    probs_af.append(prob)

non_zero = [p for p in probs_af if p != 0]
average_prob_af = (sum(non_zero) / len(non_zero)) if non_zero else 0.0
print(f"Average consistency probability across all participants: {average_prob_af:.4f}")