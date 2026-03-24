import json
import random
import uuid

from source.utils import resolve_path
from utils import resolve_path, merge_jsons
from typing import Any , Dict , List

INPUT_FILE = resolve_path("examples/examples_1st.json")
OUTPUT_FILE = resolve_path("examples/grouped_examples_1st.json")
GROUP_SIZE = 10
SEED = 42

def load_json(file_path: str) ->Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def extract_authorings(record: Dict[str , Any]) -> Dict[str ,str]:
    """Extract authoring json from the record."""
    return record.get("payload", {}).get("authoring", {})


def make_pairwise_instances(records: List[Dict[str , Any]]) -> List[Dict[str , Any]]:
    """Create pairwise instances from each record.
    from question BT, AT, AF we will create 2 instances:
    1. question BT vs AF
    2. question AT vs AF
    """
    expended_records = []

    for i , record in enumerate(records):
        authoring = extract_authorings(record)
        question = authoring.get("question", "").strip()
        af = authoring.get("af", "").strip()
        at = authoring.get("at", "").strip()
        bt = authoring.get("bt", "").strip()
        if not question or not af:
            continue  # skip if any of the fields are missing

        # 1 . question AF vs AT
        if at:
            expended_records.append({
                "instanceId": str(uuid.uuid4()),
                "sourceIndex": i,
                "pairType": "AF_vs_AT",
                "question": question,
                "af": af,
                "at": at,
            })
        # 2. question AF vs BT
        if bt:
            expended_records.append({
                "instanceId": str(uuid.uuid4()),
                "sourceIndex": i,
                "pairType": "AF_vs_BT",
                "question": question,
                "af": af,
                "bt": bt,
            })
    return expended_records



def group_to_batches(instances: List[Dict[str , Any]], group_size: int) -> List[Dict[str , Any]]:
    """Group instances into batches of specified size,
    each with unique groupId.
    """
    groups = []
    for start in range(0, len(instances), group_size):
        chunk = instances[start:start+group_size]
        groups.append({
            "groupId": str(uuid.uuid4()),
            "groupNumber": len(groups) + 1,
            "questions": chunk})
    return groups


def main():
    random.seed(SEED)
    records = load_json(INPUT_FILE)
    instances = make_pairwise_instances(records)
    random.shuffle(instances)
    grouped_data = group_to_batches(instances, GROUP_SIZE)
    save_json(grouped_data, OUTPUT_FILE)
    print(f"Saved {len(grouped_data)} groups to {OUTPUT_FILE}")


if __name__ == "__main__":    main()