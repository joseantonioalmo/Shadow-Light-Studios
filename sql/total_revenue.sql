SELECT SUM(conversions) * 100 AS total_revenue
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';