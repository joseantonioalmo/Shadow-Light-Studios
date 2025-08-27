
SELECT
    date,
    SUM(spend) AS total_spend,
    SUM(clicks) AS total_clicks,
    SUM(impressions) AS total_impressions,
    SUM(conversions) AS total_conversions,
    SUM(spend) / NULLIF(SUM(conversions), 0) AS CAC,
    (SUM(conversions) * 100) / NULLIF(SUM(spend), 0) AS ROAS,
    SUM(conversions) / NULLIF(SUM(clicks), 0) AS conversion_rate,
    SUM(spend) / NULLIF(SUM(clicks), 0) AS CPC,
    SUM(spend) / NULLIF(SUM(impressions), 0) * 1000 AS CPM
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}'
GROUP BY date
ORDER BY date;