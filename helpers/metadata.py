import duckdb
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))

query = "SELECT DISTINCT load_date, source_file_name FROM ads_spend ORDER BY load_date DESC;"

db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()
print("Data provenance and ingestion history:")
print(df.to_string(index=False))
db.close()