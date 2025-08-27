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

db.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    date DATE,
    platform VARCHAR,
    account VARCHAR,
    campaign VARCHAR,
    country VARCHAR,
    device VARCHAR,
    spend DOUBLE,
    clicks INTEGER,
    impressions INTEGER,
    conversions INTEGER,
    load_date TIMESTAMP,
    source_file_name VARCHAR
)
""")

db.register('temp_df', df)
db.execute(f"INSERT INTO {table_name} SELECT * FROM temp_df")

db.close()
print('Ingestion complete.')