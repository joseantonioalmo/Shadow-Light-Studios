import duckdb
import sys


import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

if len(sys.argv) == 4:
    group = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    query = f'''
    SELECT
        {group},
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
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY {group}
    ORDER BY {group};
    '''
    label = f"Metrics by {group} for {start_date} to {end_date}:"
elif len(sys.argv) == 2:
    group = sys.argv[1]
    query = f'''
    SELECT
        {group},
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
    GROUP BY {group}
    ORDER BY {group};
    '''
    label = f"Metrics by {group} for all dates:"
else:
    print("Usage: python metrics_by_group.py <group> [<start_date> <end_date>]")
    sys.exit(1)

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print(label)
print(df.to_string(index=False))
db.close()