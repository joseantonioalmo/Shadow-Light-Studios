import duckdb
import sys
import os


DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

if len(sys.argv) == 4:
    platform = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    query = f"SELECT * FROM ads_spend WHERE platform = '{platform}' AND date BETWEEN '{start_date}' AND '{end_date}';"
    label = f"Rows for platform {platform} from {start_date} to {end_date}:"
elif len(sys.argv) == 2:
    platform = sys.argv[1]
    query = f"SELECT * FROM ads_spend WHERE platform = '{platform}';"
    label = f"Rows for platform {platform} (all dates):"
else:
    print("Usage: python filter_by_platform.py <platform> [<start_date> <end_date>]")
    sys.exit(1)

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print(label)
print(df.to_string(index=False))
db.close()