SELECT
    SUM(spend) / NULLIF(SUM(conversions), 0) AS CAC,
    (SUM(conversions) * 100) / NULLIF(SUM(spend), 0) AS ROAS
FROM ads_spend
WHERE date BETWEEN '{start}' AND '{end}';