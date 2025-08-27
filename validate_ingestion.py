#!/usr/bin/env python3
"""
Ingestion Validation Script
Validates that data was successfully ingested into the DuckDB warehouse.
"""

import duckdb
import os
import sys
from datetime import datetime

def validate_ingestion():
    """Validate the ingestion process and display results."""

    # Database path
    db_path = 'warehouse.duckdb'
    table_name = 'ads_spend'

    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file '{db_path}' not found!")
        return False

    try:
        # Connect to database
        db = duckdb.connect(db_path)

        # Check if table exists
        table_check = db.execute(f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{table_name}'
        """).fetchdf()

        if table_check.empty:
            print(f"❌ Error: Table '{table_name}' does not exist!")
            db.close()
            return False

        # Get row count
        result = db.execute(f'SELECT COUNT(*) as total_rows FROM {table_name}').fetchdf()
        row_count = result.iloc[0, 0]

        print(f"✅ Ingestion Validation Successful!")
        print(f"📊 Total rows ingested: {row_count:,}")

        if row_count > 0:
            # Show recent data sample
            print(f"\n📋 Recent Data Sample (last 3 rows):")
            print("-" * 80)

            sample = db.execute(f"""
                SELECT
                    date,
                    platform,
                    account,
                    campaign,
                    spend,
                    clicks,
                    impressions,
                    conversions,
                    load_date
                FROM {table_name}
                ORDER BY load_date DESC
                LIMIT 3
            """).fetchdf()

            print(sample.to_string(index=False))

            # Show data summary
            print(f"\n📈 Data Summary:")
            print("-" * 40)

            summary = db.execute(f"""
                SELECT
                    COUNT(DISTINCT platform) as platforms,
                    COUNT(DISTINCT account) as accounts,
                    COUNT(DISTINCT campaign) as campaigns,
                    ROUND(SUM(spend), 2) as total_spend,
                    SUM(clicks) as total_clicks,
                    SUM(impressions) as total_impressions,
                    SUM(conversions) as total_conversions
                FROM {table_name}
            """).fetchdf()

            for col in summary.columns:
                if col in ['platforms', 'accounts', 'campaigns']:
                    print(f"{col.capitalize()}: {summary.iloc[0][col]}")
                else:
                    print(f"{col.replace('_', ' ').title()}: {summary.iloc[0][col]:,}")

        db.close()
        return True

    except Exception as e:
        print(f"❌ Error during validation: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Starting ingestion validation...")
    print(f"⏰ Validation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    success = validate_ingestion()

    print()
    if success:
        print("🎉 Validation completed successfully!")
    else:
        print("💥 Validation failed!")
        sys.exit(1)