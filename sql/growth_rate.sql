WITH
current AS (
    SELECT SUM(spend) AS spend FROM ads_spend WHERE date BETWEEN '{current_start}' AND '{current_end}'
),
prior AS (
    SELECT SUM(spend) AS spend FROM ads_spend WHERE date BETWEEN '{prior_start}' AND '{prior_end}'
)
SELECT
    current.spend AS current_spend,
    prior.spend AS prior_spend,
    ROUND((current.spend - prior.spend) / NULLIF(prior.spend, 0) * 100, 2) AS growth_rate_percent
FROM current, prior;