import json
import utils
flag = False
if flag:
    file = 'submissions_4th_survey.json'
    with open(file, 'r', encoding='utf-8') as f:
        rows = json.load(f)
else:
    json_files = utils.files_pool
    rows = utils.merge_jsons(json_files)

print("      Prolific ID        , Consistency Probability")
probs = []
for row in rows:
    prolific_id = row['payload']['participant']['prolificId']
    prob = utils.consistency_prob(row)
    print(f"{prolific_id} , {prob:.4f}")
    probs.append(prob)

average_prob = sum(probs) / len(probs)
print(f"Average consistency probability across all participants: {average_prob:.4f}")
