SELECT SUM(spend) / NULLIF(SUM(clicks), 0) AS CPC
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';