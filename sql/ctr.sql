SELECT SUM(clicks) / NULLIF(SUM(impressions), 0) AS CTR
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';