import duckdb
import argparse
import os

METRIC_SQL = {
    'cac': 'SUM(spend) / NULLIF(SUM(conversions), 0) AS CAC',
    'roas': '(SUM(conversions) * {revenue_per_conversion}) / NULLIF(SUM(spend), 0) AS ROAS',
    'ctr': 'SUM(clicks) / NULLIF(SUM(impressions), 0) AS CTR',
    'conversion_rate': 'SUM(conversions) / NULLIF(SUM(clicks), 0) AS conversion_rate',
    'cpc': 'SUM(spend) / NULLIF(SUM(clicks), 0) AS CPC',
    'cpm': 'SUM(spend) / NULLIF(SUM(impressions), 0) * 1000 AS CPM',
    'total_revenue': 'SUM(conversions) * {revenue_per_conversion} AS total_revenue',
    'spend': 'SUM(spend) AS total_spend',
    'clicks': 'SUM(clicks) AS total_clicks',
    'impressions': 'SUM(impressions) AS total_impressions',
    'conversions': 'SUM(conversions) AS total_conversions'
}

parser = argparse.ArgumentParser(description='Gigachad Query Helper for DuckDB Ads Analytics')
parser.add_argument('--start', required=False, help='Start date (YYYY-MM-DD)')
parser.add_argument('--end', required=False, help='End date (YYYY-MM-DD)')
parser.add_argument('--metric', choices=METRIC_SQL.keys(), default='cac', help='Metric to calculate')
parser.add_argument('--group-by', nargs='*', help='Group by one or more dimensions')
parser.add_argument('--filter-platform', help='Filter by platform')
parser.add_argument('--filter-country', help='Filter by country')
parser.add_argument('--filter-device', help='Filter by device')
parser.add_argument('--filter-campaign', help='Filter by campaign')
parser.add_argument('--filter-account', help='Filter by account')
parser.add_argument('--spend-threshold', type=float, help='Filter by minimum spend')
parser.add_argument('--conversion-threshold', type=int, help='Filter by minimum conversions')
parser.add_argument('--revenue-per-conversion', type=float, default=100, help='Custom revenue per conversion')
parser.add_argument('--show-metadata', action='store_true', help='Show load_date and source_file_name')
args = parser.parse_args()


filters = []
if args.start and args.end:
    filters.append(f"date BETWEEN '{args.start}' AND '{args.end}'")
if args.filter_platform:
    filters.append(f"platform = '{args.filter_platform}'")
if args.filter_country:
    filters.append(f"country = '{args.filter_country}'")
if args.filter_device:
    filters.append(f"device = '{args.filter_device}'")
if args.filter_campaign:
    filters.append(f"campaign = '{args.filter_campaign}'")
if args.filter_account:
    filters.append(f"account = '{args.filter_account}'")
if args.spend_threshold is not None:
    filters.append(f"spend > {args.spend_threshold}")
if args.conversion_threshold is not None:
    filters.append(f"conversions > {args.conversion_threshold}")

where_clause = ' AND '.join(filters) if filters else ''

metric_sql = METRIC_SQL[args.metric].replace('{revenue_per_conversion}', str(args.revenue_per_conversion))
select_fields = metric_sql
if args.group_by:
    select_fields = ', '.join(args.group_by) + ', ' + metric_sql

if args.show_metadata:
    select_fields += ', load_date, source_file_name'
    if args.group_by:
        group_by_fields = args.group_by + ['load_date', 'source_file_name']
        group_by_clause = f"GROUP BY {', '.join(group_by_fields)}"
    else:
        group_by_clause = ''
else:
    group_by_clause = f"GROUP BY {', '.join(args.group_by)}" if args.group_by else ''


if where_clause:
    query = f"SELECT {select_fields} FROM ads_spend WHERE {where_clause} {group_by_clause};"
else:
    query = f"SELECT {select_fields} FROM ads_spend {group_by_clause};"

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warehouse.duckdb'))
db = duckdb.connect(DB_PATH)
df = db.execute(query).fetchdf()

if args.start and args.end:
    print(f"Gigachad Query Result for metric '{args.metric}' from {args.start} to {args.end}:")
else:
    print(f"Gigachad Query Result for metric '{args.metric}' for all dates:")
print(df.to_string(index=False))
db.close()