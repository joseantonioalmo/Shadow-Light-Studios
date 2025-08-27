WITH
recent AS (
    SELECT
        SUM(spend) AS spend,
        SUM(conversions) AS conversions
    FROM ads_spend
    WHERE date >= CURRENT_DATE - INTERVAL 30 DAY
),
prior AS (
    SELECT
        SUM(spend) AS spend,
        SUM(conversions) AS conversions
    FROM ads_spend
    WHERE date >= CURRENT_DATE - INTERVAL 60 DAY
      AND date < CURRENT_DATE - INTERVAL 30 DAY
),
metrics AS (
    SELECT
        'CAC' AS kpi,
        recent.spend / NULLIF(recent.conversions, 0) AS recent_value,
        prior.spend / NULLIF(prior.conversions, 0) AS prior_value
    FROM recent, prior
    UNION ALL
    SELECT
        'ROAS' AS kpi,
        (recent.conversions * 100) / NULLIF(recent.spend, 0) AS recent_value,
        (prior.conversions * 100) / NULLIF(prior.spend, 0) AS prior_value
    FROM recent, prior
)
SELECT
    kpi,
    ROUND(recent_value, 2) AS last_30_days,
    ROUND(prior_value, 2) AS prior_30_days,
    ROUND((recent_value - prior_value) / NULLIF(prior_value, 0) * 100, 2) AS delta_percent
FROM metrics;