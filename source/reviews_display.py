import json
from utils import *

#for each chunk_id , count how many participants review it.
reviews_per_chunk = {}
#for each chunk , aggregate it's comments
comments_per_chunk = {}
#for each chunk , count number of options showed
options_per_chunk = {}
with open(resolve_path("examples_review/reviews_1st.json"), "r", encoding="utf-8") as f:
    rows = json.load(f)
    for row in rows:
        chunk_id = row["chunk_id"]
        comments = row["feedback"]["comments"]
        answers_per_chunk = row.get("answers" , {})
        if chunk_id not in reviews_per_chunk:
            reviews_per_chunk[chunk_id] = 0
        reviews_per_chunk[chunk_id] += 1
        if comments.strip() != "" and comments != "N/A" and comments != "  None":
            if chunk_id not in comments_per_chunk:
                comments_per_chunk[chunk_id] = []
            comments_per_chunk[chunk_id].append(comments.strip())

        if chunk_id not in options_per_chunk:
            options_per_chunk[chunk_id] = 0
        options_per_chunk[chunk_id] += len(answers_per_chunk)




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
print()

for chunk_id, count in options_per_chunk.items():
    print(f"Chunk ID: {chunk_id}, Number of options : {count}")

total_options = sum(options_per_chunk.values())
print(total_options)