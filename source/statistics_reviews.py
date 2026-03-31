import json
from utils import *

#for each chunk_id , count how many participants review it.
reviews_per_chunk = {}
comments_per_chunk = {}
with open(resolve_path("examples_review/reviews_1st.json"), "r", encoding="utf-8") as f:
    rows = json.load(f)
    for row in rows:
        chunk_id = row["chunk_id"]
        comments = row["feedback"]["comments"]
        if chunk_id not in reviews_per_chunk:
            reviews_per_chunk[chunk_id] = 0
        reviews_per_chunk[chunk_id] += 1
        if comments.strip() != "" and comments != "N/A":
            if chunk_id not in comments_per_chunk:
                comments_per_chunk[chunk_id] = []
            comments_per_chunk[chunk_id].append(comments.strip())




#display the statistics
for chunk_id, count in reviews_per_chunk.items():
    print(f"Chunk ID: {chunk_id}, Number of reviews: {count}")
print()
for chunk_id in comments_per_chunk:
    print("Chunk ID: ", chunk_id)
    for comment in comments_per_chunk[chunk_id]:
        print("Comment: ", comment)

print()
print("number of chunks reviewed: ", len(reviews_per_chunk))