import subprocess
import sys
import os

HELPERS_DIR = os.path.join(os.path.dirname(__file__), 'helpers')
HELPERS = [
    'aggregation.py',
    'cac.py',
    'conversion_rate.py',
    'cpc.py',
    'cpm.py',
    'ctr.py',
    'filter_by_platform.py',
    'gigachad_query.py',
    'growth_rate.py',
    'kpi_by_date_range.py',
    'metadata.py',
    'metrics_by_group.py',
    'metrics_by_time.py',
    'roas.py',
    'show_kpi_results.py',
    'total_revenue.py',
]

def run_helper(script, args=None):
    path = os.path.join(HELPERS_DIR, script)
    cmd = [sys.executable, path]
    if args:
        cmd += args
    print(f"\nRunning: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e.stderr}")

if __name__ == "__main__":
    start_date = '2025-02-14'
    end_date = '2025-03-25'
    prior_start = '2025-01-01'
    prior_end = '2025-02-13'
    platform = 'facebook'
    group = 'platform'

    print("\n=== Running all helpers WITH date range ===")
    for script in HELPERS:
        if script == 'filter_by_platform.py':
            run_helper(script, [platform, start_date, end_date])
        elif script == 'growth_rate.py':
            run_helper(script, [start_date, end_date, prior_start, prior_end])
        elif script == 'metrics_by_group.py':
            run_helper(script, [group, start_date, end_date])
        elif script == 'metrics_by_time.py':
            run_helper(script, [start_date, end_date])
        elif script == 'gigachad_query.py':
            run_helper(script, ['--start', start_date, '--end', end_date, '--metric', 'cac', '--group-by', 'platform'])
        elif script in [
            'aggregation.py', 'cac.py', 'conversion_rate.py', 'cpc.py', 'cpm.py', 'ctr.py',
            'kpi_by_date_range.py', 'roas.py', 'total_revenue.py'
        ]:
            run_helper(script, [start_date, end_date])
        elif script in ['metadata.py', 'show_kpi_results.py']:
            run_helper(script)
        else:
            run_helper(script)

    print("\n=== Running all helpers WITHOUT date range ===")
    for script in HELPERS:
        if script == 'filter_by_platform.py':
            run_helper(script, [platform])
        elif script == 'growth_rate.py':
            run_helper(script)
        elif script == 'metrics_by_group.py':
            run_helper(script, [group])
        elif script == 'metrics_by_time.py':
            run_helper(script)
        elif script == 'gigachad_query.py':
            run_helper(script, ['--metric', 'cac'])
        elif script in [
            'aggregation.py', 'cac.py', 'conversion_rate.py', 'cpc.py', 'cpm.py', 'ctr.py',
            'kpi_by_date_range.py', 'roas.py', 'total_revenue.py'
        ]:
            run_helper(script)
        elif script in ['metadata.py', 'show_kpi_results.py']:
            run_helper(script)
        else:
            run_helper(script)