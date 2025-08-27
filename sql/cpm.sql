SELECT SUM(spend) / NULLIF(SUM(impressions), 0) * 1000 AS CPM
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';