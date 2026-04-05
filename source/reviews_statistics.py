"""
This file uses methods from util.py that parsing examples_review/reviews_1st.json
and prints statistics about the reviews to the terminal.
"""

from utils import *

JSON_FILE = "examples_review/reviews_1st.json"

def main():
    with open(resolve_path(JSON_FILE), "r", encoding="utf-8") as f:
        rows = json.load(f)

    bt_vs_af = review_stats_bt_vs_af(rows)
    af_vs_at = review_stats_af_vs_at(rows)
    per_chunk = review_stats_per_chunk(rows)

    print("-"*60)
    print("Overall Statistics")
    print("-"*60)
    print(format_stats_block("BT vs AF" , bt_vs_af))
    print()
    print(format_stats_block("AF vs AT" , af_vs_at))
    print()
    print("-"*60)
    print("Per Chunk Statistics")
    print("-"*60)

    for chunk_id , chunk_stats in per_chunk.items():
        print(f"Chunk {chunk_id}")
        print(format_stats_block("BT vs AF" , chunk_stats["bt_vs_af"]))
        print(format_stats_block("AF vs AT" , chunk_stats["af_vs_at"]))
        print("-"*40)

if __name__ == "__main__":
    main()