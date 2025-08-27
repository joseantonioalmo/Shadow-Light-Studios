SELECT SUM(spend) / NULLIF(SUM(conversions), 0) AS CAC
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';