import duckdb
import pandas as pd
from datetime import datetime
import os

csv_path = 'data/ads_spend.csv'
db_path = 'warehouse.duckdb'
table_name = 'ads_spend'

df = pd.read_csv(csv_path)

df['load_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
df['source_file_name'] = os.path.basename(csv_path)

db = duckdb.connect(db_path)

df.to_sql(table_name, db, if_exists='append', index=False)

db = duckdb.connect(db_path)
result = db.execute(f"SELECT * FROM {table_name} ORDER BY load_date DESC LIMIT 10").fetchdf()
print("Latest ingested rows:")
print(result)
db.close()
print('Ingestion complete.')