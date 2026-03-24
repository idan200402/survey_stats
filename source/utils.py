"""
Utility helpers for analyzing Prolific survey submission JSONs.

Submission files are a list of objects shaped like:
  {"payload": {"meta": {...}, "answers": [...], "participant": {...}, "feedback": {...}}}

Assumptions used by the analysis scripts:
* Each base question appears twice (suffix _a / _b before the "__" separator).
* Each answer has: trialId, shownOrder, chosenOptionId.
* chosenOptionId is one of: AF, AT, BT.
"""

import json
import os
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


english_knowing = [
    "united kingdom",
    "ireland",
    "australia",
    "canada",
    "kenya",
    "south africa"
]

non_english_knowing = [
    "germany",
    "italy",
    "brazil",
    "poland",
    "france",
    "portugal",
    "greece",
    "egypt",
    "vietnam"
]
files_pool = [
    "submissions_1st_survey.json",
    "submissions_2nd_survey.json",
    "submissions_3rdA_survey.json",
    "submissions_3rdB_survey.json",
    "submissions_4th_survey.json",
]


def resolve_path(path: str):
    """
    Resolve a file path.
    Works whether you run from repo root (with data/ folder) or from inside data/.
    """
    if os.path.exists(path):
        return path
    candidate = BASE_DIR / "data" / path
    if os.path.exists(candidate):
        return candidate
    raise FileNotFoundError(f"Could not find '{path}' or '{candidate}'")


def merge_jsons(json_files):
    """
    Input: list of json filenames
    Output: merged list of all rows across all files
    """
    merged_data = []
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
    input: list of numbers
    return: median
    """
    lst = sorted(lst)
    n = len(lst)
    if n == 0:
        return None
    if n % 2 == 1:
        return lst[n // 2]
    return (lst[n // 2 - 1] + lst[n // 2]) / 2


def common_education_level(education_levels):
    """
    return: most common education level among participants
    """
    counter = Counter(education_levels)
    most_common = counter.most_common(1)
    return most_common[0][0] if most_common else None


def base_question(trial_id: str) -> str:
    """
    Example:
      "post_cutoff_a__AF_vs_AT" -> "post_cutoff"
      "math_problem_b__BT_vs_AF" -> "math_problem"
    """
    left = trial_id.split("__", 1)[0]  # "post_cutoff_a"
    return left.rsplit("_", 1)[0]  # remove "_a"/"_b" -> "post_cutoff"


def comparison_pair(trial_id: str):
    """
    Return the pair of option IDs compared in this trial, normalized.

    Examples:
      "...__AF_vs_AT" -> ("AF", "AT")
      "...__BT_vs_AF" -> ("AF", "BT")
    """
    right = trial_id.split("__", 1)[1]  # "AF_vs_AT"
    a, b = right.split("_vs_", 1)
    return tuple(sorted((a, b)))  # canonical order


def group(chosen_option_id: str) -> str:
    """
    Consistency treats AT and BT as the same "T" bucket, and AF as "AF".
    """
    return "AF" if chosen_option_id == "AF" else "T"


def consistency_prob_general(row):
    """
    Per participant:
      consistent if group(choice1) == group(choice2) for a base question.
    Returns: consistent_pairs / total_pairs
    """
    answers = row["payload"]["answers"]

    by_q = {}
    for a in answers:
        q = base_question(a["trialId"])
        g = group(a["chosenOptionId"])
        if q not in by_q:
            by_q[q] = []
        by_q[q].append(g)

    consistent = 0
    total = 0
    for gs in by_q.values():
        total += 1
        if gs[0] == gs[1]:
            consistent += 1

    return (consistent / total) if total else 0.0


def consistency_prob_af(row):
    """
    Consistency probability conditioned on AF appearing at least once.
    Returns: consistent_pairs / total_pairs_over_questions_where_AF_appears
    """
    answers = row["payload"]["answers"]

    by_q = {}
    for a in answers:
        q = base_question(a["trialId"])
        g = group(a["chosenOptionId"])
        if q not in by_q:
            by_q[q] = []
        by_q[q].append(g)

    consistent = 0
    total = 0
    for gs in by_q.values():
        if "AF" in gs:
            total += 1
            if gs[0] == gs[1]:
                consistent += 1

    return (consistent / total) if total else 0.0


#for the authoring dataset.
