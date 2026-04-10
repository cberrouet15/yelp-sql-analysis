import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "processed", "restaurants.csv")

restaurants = pd.read_csv(data_path)

visuals_path = os.path.join(BASE_DIR, "visuals")
os.makedirs(visuals_path, exist_ok=True)

# Ratings Distribution Histogram
plt.figure(figsize=(8, 5))
plt.hist(restaurants["stars"].dropna(), bins=10, edgecolor="black")
plt.title("Distribution of Restaurant Ratings")
plt.xlabel("Rating")
plt.ylabel("Number of Restaurants")
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "ratings_distribution.png"))
plt.show()

# Top Cities by Average Rating
city_avg = (
    restaurants.groupby("city")
    .agg(
        avg_rating=("stars", "mean"),
        total_restaurants=("city", "size")
    )
    .reset_index()
)

city_avg = city_avg[city_avg["total_restaurants"] > 50]
city_avg = city_avg.sort_values("avg_rating", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(city_avg["city"], city_avg["avg_rating"])
plt.title("Top 10 Cities by Average Restaurant Rating")
plt.xlabel("Average Rating")
plt.ylabel("City")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "top_cities_avg_rating.png"))
plt.show()

# Review Count vs Rating Scatter Plot
plt.figure(figsize=(8, 5))
plt.scatter(
    restaurants["review_count"],
    restaurants["stars"],
    alpha=0.5
)
plt.title("Review Count vs Restaurant Rating")
plt.xlabel("Review Count")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "review_count_vs_rating.png"))
plt.show()

# Most Reviewed Restaurants
top_reviewed = (
    restaurants[["name", "review_count"]]
    .dropna()
    .sort_values("review_count", ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
plt.barh(top_reviewed["name"], top_reviewed["review_count"])
plt.title("Top 10 Most Reviewed Restaurants")
plt.xlabel("Review Count")
plt.ylabel("Restaurant")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "most_reviewed_restaurants.png"))
plt.show()