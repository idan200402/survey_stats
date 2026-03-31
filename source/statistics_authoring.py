import utils
import json
good_examples = utils.resolve_path("examples/examples_1st.json")
bad_examples = utils.resolve_path("examples/examples_1st_bad.json")
with open(good_examples, "r", encoding="utf-8") as f:
    rows_good = json.load(f)

with open(bad_examples, "r", encoding="utf-8") as f:
    rows_bad = json.load(f)

#displaying statistics about the participants.
instances_per_file = [0, 0]
ages = []
countries = {}
for row in rows_good:
    age = int(row["payload"]["participant"]["age"])
    country = row["payload"]["participant"]["country"].lower().strip()
    ages.append(age)
    countries[country] = countries.get(country, 0) + 1
    instances_per_file[0] += 1

for row in rows_bad:
    instances_per_file[1] += 1



average_age = sum(ages) / len(ages) if ages else 0
most_common_country = max(countries, key=countries.get) if countries else None
print(f"Average age of participants: {average_age:.2f}")
#sorting the countries by values
# sorted_countries = dict(sorted(countries.items(), key=lambda item: item[1], reverse=True))
# for country, count in sorted_countries.items():
#     print(f"{country}: {count} participants")

#display number of instances for each file

print(f"Number of instances in good examples: {instances_per_file[0]}")
print(f"Number of instances in bad examples: {instances_per_file[1]}")

print(f"Number of pair of questions in good examples: {instances_per_file[0]*2}")