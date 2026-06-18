-- ==========================================
-- AI Logistics Analytics Platform
-- Business SQL Queries
-- ==========================================

USE logistics_db;

-- ==========================================
-- BASIC BUSINESS METRICS
-- ==========================================

-- 1. Total Orders
SELECT COUNT(*) AS total_orders
FROM logistics_data;

-- 2. Total Revenue
SELECT ROUND(SUM(line_item_value),2) AS total_revenue
FROM logistics_data;

-- 3. Average Freight Cost
SELECT ROUND(AVG(freight_cost_usd),2) AS avg_freight_cost
FROM logistics_data;

-- 4. Average Order Value
SELECT ROUND(AVG(line_item_value),2) AS avg_order_value
FROM logistics_data;

-- 5. Total Delayed Orders
SELECT COUNT(*) AS delayed_orders
FROM logistics_data
WHERE delayed = 1;

-- ==========================================
-- COUNTRY ANALYSIS
-- ==========================================

-- 6. Top 10 Countries by Orders
SELECT country,
COUNT(*) AS total_orders
FROM logistics_data
GROUP BY country
ORDER BY total_orders DESC
LIMIT 10;

-- 7. Country Wise Revenue
SELECT country,
ROUND(SUM(line_item_value),2) AS revenue
FROM logistics_data
GROUP BY country
ORDER BY revenue DESC;

-- 8. Average Freight Cost by Country
SELECT country,
ROUND(AVG(freight_cost_usd),2) AS avg_freight_cost
FROM logistics_data
GROUP BY country
ORDER BY avg_freight_cost DESC;

-- 9. Average Weight by Country
SELECT country,
ROUND(AVG(weight_kg),2) AS avg_weight
FROM logistics_data
GROUP BY country
ORDER BY avg_weight DESC;

-- ==========================================
-- SHIPMENT ANALYSIS
-- ==========================================

-- 10. Shipment Mode Distribution
SELECT shipment_mode,
COUNT(*) AS shipment_count
FROM logistics_data
GROUP BY shipment_mode
ORDER BY shipment_count DESC;

-- 11. Revenue by Shipment Mode
SELECT shipment_mode,
ROUND(SUM(line_item_value),2) AS revenue
FROM logistics_data
GROUP BY shipment_mode
ORDER BY revenue DESC;

-- 12. Average Delay by Shipment Mode
SELECT shipment_mode,
ROUND(AVG(delay_days),2) AS avg_delay_days
FROM logistics_data
GROUP BY shipment_mode;

-- ==========================================
-- PRODUCT ANALYSIS
-- ==========================================

-- 13. Product Group Distribution
SELECT product_group,
COUNT(*) AS total_orders
FROM logistics_data
GROUP BY product_group
ORDER BY total_orders DESC;

-- 14. Product Group Revenue
SELECT product_group,
ROUND(SUM(line_item_value),2) AS revenue
FROM logistics_data
GROUP BY product_group
ORDER BY revenue DESC;

-- ==========================================
-- VENDOR ANALYSIS
-- ==========================================

-- 15. Top 10 Vendors by Orders
SELECT vendor,
COUNT(*) AS total_orders
FROM logistics_data
GROUP BY vendor
ORDER BY total_orders DESC
LIMIT 10;

-- 16. Top Vendors by Revenue
SELECT vendor,
ROUND(SUM(line_item_value),2) AS revenue
FROM logistics_data
GROUP BY vendor
ORDER BY revenue DESC;

-- 17. Vendor Average Freight Cost
SELECT vendor,
ROUND(AVG(freight_cost_usd),2) AS avg_freight_cost
FROM logistics_data
GROUP BY vendor
ORDER BY avg_freight_cost DESC;

-- ==========================================
-- DELAY ANALYSIS
-- ==========================================

-- 18. Delay Percentage
SELECT ROUND(
(COUNT(CASE WHEN delayed = 1 THEN 1 END) * 100.0)
/
COUNT(*),2
) AS delay_percentage
FROM logistics_data;

-- 19. Countries with Highest Delays
SELECT country,
COUNT(*) AS delayed_orders
FROM logistics_data
WHERE delayed = 1
GROUP BY country
ORDER BY delayed_orders DESC;

-- 20. Vendors with Highest Delays
SELECT vendor,
COUNT(*) AS delayed_orders
FROM logistics_data
WHERE delayed = 1
GROUP BY vendor
ORDER BY delayed_orders DESC;

-- ==========================================
-- RISK ANALYSIS
-- ==========================================

-- 21. High Risk Shipments
SELECT *
FROM logistics_data
WHERE risk_score > 7;

-- 22. Average Risk Score
SELECT ROUND(AVG(risk_score),2) AS avg_risk_score
FROM logistics_data;

-- 23. Country Wise Risk Score
SELECT country,
ROUND(AVG(risk_score),2) AS avg_risk_score
FROM logistics_data
GROUP BY country
ORDER BY avg_risk_score DESC;

-- ==========================================
-- WINDOW FUNCTIONS
-- ==========================================

-- 24. Vendor Revenue Ranking
SELECT vendor,
SUM(line_item_value) AS revenue,
RANK() OVER(
ORDER BY SUM(line_item_value) DESC
) AS vendor_rank
FROM logistics_data
GROUP BY vendor;

-- 25. Country Revenue Ranking
SELECT country,
SUM(line_item_value) AS revenue,
DENSE_RANK() OVER(
ORDER BY SUM(line_item_value) DESC
) AS country_rank
FROM logistics_data
GROUP BY country;

-- ==========================================
-- CTE QUERIES
-- ==========================================

-- 26. Top Revenue Countries
WITH country_revenue AS
(
SELECT country,
SUM(line_item_value) AS revenue
FROM logistics_data
GROUP BY country
)
SELECT *
FROM country_revenue
ORDER BY revenue DESC;

-- 27. High Performing Vendors
WITH vendor_revenue AS
(
SELECT vendor,
SUM(line_item_value) AS revenue
FROM logistics_data
GROUP BY vendor
)
SELECT *
FROM vendor_revenue
WHERE revenue > 1000000;

-- ==========================================
-- ADVANCED ANALYSIS
-- ==========================================

-- 28. Top 5 Highest Revenue Shipments
SELECT *
FROM logistics_data
ORDER BY line_item_value DESC
LIMIT 5;

-- 29. Top 5 Highest Freight Cost Shipments
SELECT *
FROM logistics_data
ORDER BY freight_cost_usd DESC
LIMIT 5;

-- 30. Top 5 Heaviest Shipments
SELECT *
FROM logistics_data
ORDER BY weight_kg DESC
LIMIT 5;
