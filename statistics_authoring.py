import utils
import json
file = utils.resolve_path("examples/examples_1st.json")
with open(file, "r", encoding="utf-8") as f:
    rows = json.load(f)

#displaying statistics about the participants.
ages = []
countries = {}
for row in rows:
    age = int(row["payload"]["participant"]["age"])
    country = row["payload"]["participant"]["country"].lower().strip()
    ages.append(age)
    countries[country] = countries.get(country, 0) + 1

average_age = sum(ages) / len(ages) if ages else 0
most_common_country = max(countries, key=countries.get) if countries else None
print(f"Average age of participants: {average_age:.2f}")
#sorting the countries by values
sorted_countries = dict(sorted(countries.items(), key=lambda item: item[1], reverse=True))
for country, count in sorted_countries.items():
    print(f"{country}: {count} participants")

