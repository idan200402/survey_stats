import json
from utils import english_knowing
#takes as input the json file and returns a json file of participance from english speaking countries
file = "data/options/submissions_2nd_survey_20.json"
with open(file, "r", encoding="utf-8") as f:
    rows = json.load(f)

new_file = "data/options/submissions_2nd_survey_20_english.json"
english_speakers = []
for row in rows:
    country = row["payload"]["participant"]["country"].lower().strip()
    if country in english_knowing:
        english_speakers.append(row)

with open(new_file, "w", encoding="utf-8") as f:
    json.dump(english_speakers, f, indent=4)


