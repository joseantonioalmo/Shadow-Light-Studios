import duckdb
import sys


import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

if len(sys.argv) == 3:
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    query = f'''
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
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY date
    ORDER BY date;
    '''
    label = f"Metrics by day for {start_date} to {end_date}:"
else:
    query = '''
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
    GROUP BY date
    ORDER BY date;
    '''
    label = "Metrics by day for all dates:"

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print(label)
print(df.to_string(index=False))
db.close()