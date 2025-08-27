import duckdb
import sys


import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

if len(sys.argv) == 3:
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    query = f'''
    SELECT
        SUM(spend) / NULLIF(SUM(conversions), 0) AS CAC,
        (SUM(conversions) * 100) / NULLIF(SUM(spend), 0) AS ROAS
    FROM ads_spend
    WHERE date BETWEEN '{start_date}' AND '{end_date}';
    '''
    label = f"KPI for {start_date} to {end_date}:"
else:
    query = '''
    SELECT
        SUM(spend) / NULLIF(SUM(conversions), 0) AS CAC,
        (SUM(conversions) * 100) / NULLIF(SUM(spend), 0) AS ROAS
    FROM ads_spend;
    '''
    label = "KPI for all dates:"

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print(label)
print(df.to_string(index=False))
db.close()