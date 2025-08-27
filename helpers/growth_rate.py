import duckdb
import sys
import os


DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

if len(sys.argv) == 5:
    current_start = sys.argv[1]
    current_end = sys.argv[2]
    prior_start = sys.argv[3]
    prior_end = sys.argv[4]
    query = f"""
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
    """
    label = "Growth Rate for spend:"
else:
    query = "SELECT SUM(spend) AS total_spend FROM ads_spend;"
    label = "Total spend for all dates:"

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print(label)
print(df.to_string(index=False))
db.close()