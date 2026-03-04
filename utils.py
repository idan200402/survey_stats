"""
Utility helpers for analyzing Prolific survey submission JSONs.

Your submission files are a list of objects shaped like:
  {"payload": {"meta": {...}, "answers": [...], "participant": {...}, "feedback": {...}}}

Assumptions used by the analysis scripts:
* Each base question appears twice (suffix _a / _b before the "__" separator).
* Each answer has: trialId, shownOrder, chosenOptionId.
* chosenOptionId is one of: AF, AT, BT.
"""

from __future__ import annotations

import json
import os
from collections import Counter
from typing import Dict, List, Tuple


files_pool = [
    "submissions_1st_survey.json",
    "submissions_2nd_survey.json",
    "submissions_3rdA_survey.json",
    "submissions_3rdB_survey.json",
    "submissions_4th_survey.json",
]


def resolve_path(path: str) -> str:
    """Resolve a file path.

    Older scripts hard-coded "data/<file>.json". This helper makes the code work
    whether you run it from the repo root or from inside the data folder.
    """
    if os.path.exists(path):
        return path
    candidate = os.path.join("data", path)
    if os.path.exists(candidate):
        return candidate
    raise FileNotFoundError(f"Could not find '{path}' or '{candidate}'")


def merge_jsons(json_files):
    """
    input: list of json files.
    output: merged list of all the data in the json files.
    """
    merged_data: List[dict] = []
    for file in json_files:
        path = resolve_path(file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"Expected a list in {path}, got {type(data).__name__}")
        merged_data.extend(data)
    return merged_data


def median(lst):
    """
    input: list of numbers.
    return. median of the list:
    """
    lst = sorted(lst)
    n = len(lst)
    if n % 2 == 1:
        return lst[n // 2]
    else:
        return (lst[n // 2 - 1] + lst[n // 2]) / 2


def common_education_level(education_levels):
    """
    :param education_levels:
    :return: common education level among the participants.
    """
    counter = Counter(education_levels)
    most_common = counter.most_common(1)
    return most_common[0][0] if most_common else None


def base_question(trial_id):
    """
    :param post_cutoff_a__AF_vs_AT
    :return: post_cutoff
    """
    left = trial_id.split("__", 1)[0]
    return left.rsplit("_", 1)[0]


def comparison_pair(trial_id: str) -> Tuple[str, str]:
    """Return the pair of option IDs compared in this trial, normalized.

    Examples:
      "...__AF_vs_AT" -> ("AF", "AT")
      "...__BT_vs_AF" -> ("AF", "BT")
    """
    try:
        right = trial_id.split("__", 1)[1]
        a, b = right.split("_vs_", 1)
    except Exception as e:
        raise ValueError(f"Unrecognized trialId format: {trial_id}") from e
    return tuple(sorted((a, b)))  # canonicalize order


def group(chosen_option_id: str) -> str:
    """Map raw choice to a coarse group.

    Consistency treats AT and BT as the same "T" bucket, and AF as "AF".
    """
    return "AF" if chosen_option_id == "AF" else "T"


def consistency_prob_general(row):
    """
    :param row: a participant's responses.
    :return: the probability that the participant is consistent.
    """
    answers = row["payload"]["answers"]

    by_q: Dict[str, List[str]] = {}
    for a in answers:
        q = base_question(a["trialId"])
        g = group(a["chosenOptionId"])
        by_q.setdefault(q, []).append(g)

    consistent = 0
    total = 0
    for _, gs in by_q.items():
        if len(gs) < 2:
            continue
        total += 1
        if gs[0] == gs[1]:
            consistent += 1

    return (consistent / total) if total else 0.0


def consistency_prob_af(row):
    """
    :param row: a participant's responses.
    :return: consistency probability conditioned on AF appearing at least once.
    """
    answers = row["payload"]["answers"]

    by_q: Dict[str, List[str]] = {}
    for a in answers:
        q = base_question(a["trialId"])
        g = group(a["chosenOptionId"])
        by_q.setdefault(q, []).append(g)

    consistent = 0
    total = 0
    for _, gs in by_q.items():
        if len(gs) < 2:
            continue
        if "AF" in gs:
            total += 1
            if gs[0] == gs[1]:
                consistent += 1

    return (consistent / total) if total else 0.0