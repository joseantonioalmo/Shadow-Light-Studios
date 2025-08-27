SELECT SUM(spend) AS total_spend, AVG(spend) AS avg_spend, MIN(spend) AS min_spend, MAX(spend) AS max_spend
FROM ads_spend WHERE date BETWEEN '{start}' AND '{end}';