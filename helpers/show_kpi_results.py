import duckdb

import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))
SQL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sql', 'kpi_modeling.sql'))

db = duckdb.connect(DB_PATH)

with open(SQL_PATH, 'r') as f:
    query = f.read()

df = db.execute(query).fetchdf()

print("KPI Comparison: Last 30 Days vs Prior 30 Days")
print(df.to_string(index=False))

db.close()