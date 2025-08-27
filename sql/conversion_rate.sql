SELECT SUM(conversions) / NULLIF(SUM(clicks), 0) AS conversion_rate
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';