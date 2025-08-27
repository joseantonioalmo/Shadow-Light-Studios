import duckdb
import sys
import os


DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

if len(sys.argv) == 3:
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    query = f"""
    SELECT SUM(conversions) * 100 AS total_revenue
    FROM ads_spend
    WHERE date BETWEEN '{start_date}' AND '{end_date}';
    """
    label = f"Total Revenue for {start_date} to {end_date}:"
else:
    query = "SELECT SUM(conversions) * 100 AS total_revenue FROM ads_spend;"
    label = "Total Revenue for all dates:"

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print(label)
print(df.to_string(index=False))
db.close()