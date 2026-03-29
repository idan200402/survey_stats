import json

from utils import resolve_path


# given an instance_id , find the corresponding authoring json in the original records.

def find_authoring_by_instance_id(instance_id , original_records , grouped_records):
    with open(grouped_records, "r", encoding="utf-8") as f:
        records = json.load(f)
    source_index = -1
    for record in records:
        for question in record["questions"]:
            if question["instanceId"] == instance_id:
                source_index = question["sourceIndex"]
                break

    if source_index == -1:
        raise ValueError(f"Instance ID {instance_id} not found in grouped records.")
    with open(original_records, "r", encoding="utf-8") as f:
        original_data = json.load(f)

    res = original_data[source_index]["payload"]["authoring"]
    return res


def main():
    instance_id = "92650ae2-0160-4ef7-ad92-66dfd848fae6"
    original_records = resolve_path("examples/examples_1st.json")
    grouped_records = resolve_path("examples/grouped_examples_1st.json")
    print(find_authoring_by_instance_id(instance_id , original_records , grouped_records))


if __name__ == "__main__":    main()