import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE_DIR, "data", "processed"), exist_ok=True)

# Loading business JSON
business = pd.read_json(os.path.join(BASE_DIR, "data", "raw", "yelp_academic_dataset_business.json"), lines=True)
print(business.shape)
print(business.head())

# Filtering to restaurants 
restaurants = business[business["categories"].str.contains("Restaurant", na=False)].copy()
print(restaurants.shape)
# Keep useful business columns
restaurants = restaurants[
    ["business_id", "name", "city", "state", "stars", "review_count", "categories"]
]

# Convert to CSV
restaurants.to_csv(os.path.join(BASE_DIR, "data", "processed", "restaurants.csv"), index=False)

#Create subset of reviews and convert to CSV
restaurant_ids = set(restaurants["business_id"])
chunks = []
chunk_size = 50000

for chunk in pd.read_json(os.path.join(BASE_DIR, "data", "raw", "yelp_academic_dataset_review.json"), lines=True, chunksize=chunk_size):
    filtered = chunk[chunk["business_id"].isin(restaurant_ids)][
        ["review_id", "business_id", "stars", "date", "text"]
    ]
    chunks.append(filtered)

reviews = pd.concat(chunks, ignore_index=True)
print(reviews.shape)
reviews.to_csv(os.path.join(BASE_DIR, "data", "processed", "restaurant_reviews.csv"), index=False)

#Load into SQL
conn = sqlite3.connect(os.path.join(BASE_DIR, "data", "yelp.db"))

restaurants.to_sql("restaurants", conn, if_exists="replace", index=False)
reviews.to_sql("reviews", conn, if_exists="replace", index=False)

conn.commit()
conn.close()