# 7. Find reviews most similar to “The disposal worked and was installed in less time than expected.”
from pymilvus import Collection
import numpy as np

collection = Collection("reviews")
query_vector = embed("The disposal worked and was installed in less time than expected.")

search_params = {"metric_type": "IP", "params": {"nprobe": 10}}

results = collection.search(
    data=[query_vector],
    anns_field="review_embedding",
    param=search_params,
    limit=10,
    output_fields=["review_text"]
)

for result in results[0]:
    print(result.entity.get("review_text"))

# 8. Identify reviews that are similar to “After a couple of years, the unit started freezing up,”
#    but only for products with more than 50 reviews.
query_vector = embed("After a couple of years, the unit started freezing up.")

search_results = collection.search(
    data=[query_vector],
    anns_field="review_embedding",
    param={"metric_type": "IP", "params": {"nprobe": 10}},
    limit=10,
    output_fields=["review_text", "product_id"]
)

filtered_results = []
for result in search_results[0]:
    product_id = result.entity.get("product_id")

    # Check if the product has more than 50 reviews
    review_count = collection.query(
        expr=f"product_id == '{product_id}'",
        output_fields=["count(*)"]
    )[0]["count(*)"]

    if review_count > 50:
        filtered_results.append(result.entity.get("review_text"))

print(filtered_results)

# 9. Retrieve reviews that are semantically related to “The oven heats unevenly”
#    and were written in 2020 or later.
query_vector = embed("The oven heats unevenly.")

search_results = collection.search(
    data=[query_vector],
    anns_field="review_embedding",
    param={"metric_type": "IP", "params": {"nprobe": 10}},
    limit=10,
    output_fields=["review_text", "review_date"]
)

filtered_reviews = [
    result.entity.get("review_text")
    for result in search_results[0]
    if result.entity.get("review_date") >= "2020-01-01"
]

print(filtered_reviews)
