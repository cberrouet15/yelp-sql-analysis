-- 1. Top-rated restaurants

-- 1a. High Rating ≠ Popularity
SELECT name, stars, review_count
FROM restaurants
ORDER BY stars DESC
LIMIT 10;

-- 1b. Ratings Stabilize with More Reviews
SELECT stars, AVG(review_count)
FROM restaurants
GROUP BY stars
ORDER BY stars DESC;

-- 1c. Location Matters
SELECT city, AVG(stars) AS avg_rating, COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY city
HAVING COUNT(*) > 50
ORDER BY avg_rating DESC;

-- 1d. Category/Cuisine Patterns
SELECT categories, AVG(stars)
FROM restaurants
GROUP BY categories
ORDER BY AVG(stars) DESC;

-- 1e. The “Trust Signal”
SELECT name, stars, review_count
FROM restaurants
WHERE review_count > 100
ORDER BY stars DESC
LIMIT 10;

-- 2. Best cities by average rating

-- 2a. Review Volume (Engagement)
SELECT city, AVG(stars) AS avg_rating, COUNT(*) AS total_restaurants, AVG(review_count) AS avg_reviews
FROM restaurants
GROUP BY city
HAVING COUNT(*) > 50
ORDER BY avg_rating DESC;

-- 2b. Trustworthy Top Cities
SELECT city, AVG(stars) AS avg_rating, COUNT(*) AS total_restaurants, SUM(review_count) AS total_reviews
FROM restaurants
GROUP BY city
HAVING COUNT(*) > 50
ORDER BY avg_rating DESC, total_reviews DESC;

-- 2c. Distribution Check (Are ratings inflated?)
SELECT city, SUM(CASE WHEN stars >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_rating_ratio, COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY city
HAVING COUNT(*) > 50
ORDER BY high_rating_ratio DESC;

-- 3. Most reviewed restaurants 

-- 3a. Popularity
SELECT r.name, COUNT(rv.review_id) AS total_reviews
FROM restaurants r
JOIN reviews rv
ON r.business_id = rv.business_id
GROUP BY r.name
ORDER BY total_reviews DESC
LIMIT 10;

-- 3b. Popularity vs. Quality
SELECT r.name, AVG(r.stars) AS rating, COUNT(rv.review_id) AS total_reviews
FROM restaurants r
JOIN reviews rv
ON r.business_id = rv.business_id
GROUP BY r.name
ORDER BY total_reviews DESC
LIMIT 10;

-- 3c. Best Overall
SELECT r.name, r.stars, COUNT(rv.review_id) AS total_reviews
FROM restaurants r
JOIN reviews rv
ON r.business_id = rv.business_id
GROUP BY r.name, r.stars
HAVING COUNT(rv.review_id) > 100
ORDER BY r.stars DESC, total_reviews DESC
LIMIT 10;
