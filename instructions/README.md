# Eight Figure - Data Engineering Test Project Setup Guide

This guide will walk you through setting up data ingestion from CSV files into a DuckDB warehouse using n8n workflow orchestration.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Data Ingestion Setup](#data-ingestion-setup)
6. [Troubleshooting](#troubleshooting)

## Project Overview

This project demonstrates data ingestion from CSV files into a DuckDB warehouse using n8n for workflow orchestration.

## Prerequisites

### Required Software
- **Python**: 3.8 or higher (for running ingestion scripts)
- **n8n**: Workflow automation tool (for data ingestion orchestration)
- **Git**: Version control system

### Dependencies
The project requires the following Python packages:
- `duckdb==1.3.2` - Analytical database
- `pandas==2.3.2` - Data manipulation and analysis
- `python-dateutil==2.9.0` - Date parsing utilities

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd eight-figure-project
```

### 2. Set Up Python Environment

#### Option A: Using venv (Recommended)
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install duckdb==1.3.2 pandas==2.3.2 python-dateutil==2.9.0
```

### 3. Install n8n

#### Using npm (Recommended)
```bash
# Install n8n globally
npm install -g n8n

# Or install locally in project
npm init -y
npm install n8n
```

### 4. Verify Installation
```bash
# Check Python environment
python --version
pip list | grep -E "(duckdb|pandas|dateutil)"

# Check n8n installation
n8n --version
```

## Project Structure

```
eight-figure-project/
├── data/
│   └── ads_spend.csv          # Sample advertising spend data
├── ingest_ads_spend.py        # Main data ingestion script
├── validate_ingestion.py      # Ingestion validation script
├── warehouse.duckdb          # DuckDB database file
├── sql/
│   └── kpi_modeling.sql       # 30-day KPI comparison SQL
├── helpers/
│   ├── cac.py                 # Customer Acquisition Cost calculations
│   ├── roas.py                # Return on Ad Spend calculations
│   ├── kpi_by_date_range.py   # Date range KPI queries
│   └── show_kpi_results.py    # KPI results display script
├── workflow.json             # Alternative n8n workflow configuration
├── readme.md                 # Main project README
└── .venv/                    # Python virtual environment
```

## Data Ingestion Setup

### 1. Prepare Data Source
The project includes sample data in `data/ads_spend.csv` with the following structure:
```csv
date,platform,account,campaign,country,device,spend,clicks,impressions,conversions
2025-01-01,Meta,AcctA,Prospecting,MX,Desktop,1115.94,360,15840,29
```

### 2. Configure n8n Workflow

#### Prerequisites for Code Node Execution
Before setting up the n8n workflow, ensure your host system has the required Python environment:

1. **Activate Virtual Environment on Host**:
   ```bash
   cd "/Users/juliaalvarez/Eight Figure"
   source .venv/bin/activate
   pip install duckdb==1.3.2 pandas==2.3.2 python-dateutil==2.9.0
   ```

2. **Verify Python Command**:
   ```bash
   which python
   # Should point to: /Users/juliaalvarez/Eight Figure/.venv/bin/python
   ```

#### n8n Workflow Setup

1. Start n8n:
   ```bash
   n8n start
   ```

2. Open n8n in your browser (http://localhost:5678)

3. Create a new workflow or open an existing one

4. Add an **Execute Command** node:
   - Go to **Add node** → **Actions** → **Execute Command**
   - In the **Command** field, paste:
     ```bash
     cd "/Users/juliaalvarez/Eight Figure" && source .venv/bin/activate && python ingest_ads_spend.py
     ```
   - Leave other settings as default

5. Connect a **Manual Trigger** node to the Execute Command node to execute the script on demand

#### Execute Command Node Configuration
For each Execute Command node, ensure these settings:
- **Show Output**: Enabled (to see script results)
- **Show Error Output**: Enabled (to see any errors - you'll see "stderr: empty" when successful)
- **Continue on Error**: Disabled (workflow stops if command fails)
- **Working Directory**: Leave default (n8n handles this via the `cd` command)

The "stderr: empty" message is **normal and expected** when your commands run successfully - it confirms no errors occurred.

6. **Optional: Add Validation Node**
   - Add another **Execute Command** node after the ingestion node
   - Connect the ingestion node to the validation node
   - In the validation command field, paste:
     ```bash
     cd "/Users/juliaalvarez/Eight Figure" && source .venv/bin/activate && python validate_ingestion.py
     ```
   - This node will run the validation script and display comprehensive results

#### Important Notes
- **Host Execution**: The Code node executes the Python script on your host system (not within n8n), so ensure your host has the correct Python environment and dependencies installed
- **Working Directory**: The script will execute from the specified working directory, so relative paths in `ingest_ads_spend.py` will resolve correctly
- **Environment**: The script runs with the same environment variables and Python path as your host system

#### Workflow Configuration
The n8n workflow follows this sequence:

1. **Manual Trigger** → Click "Execute workflow" button to start
2. **Execute Command** (Ingestion) → Runs:
   ```bash
   cd "/Users/juliaalvarez/Eight Figure" && source .venv/bin/activate && python ingest_ads_spend.py
   ```
3. **Execute Command** (Validation) → Automatically runs after ingestion completes:
   ```bash
   cd "/Users/juliaalvarez/Eight Figure" && source .venv/bin/activate && python validate_ingestion.py
   ```

**Node Connections:**
- Manual Trigger connects to Ingestion Execute Command
- Ingestion Execute Command connects to Validation Execute Command
- Each node executes sequentially, providing comprehensive ingestion and validation results

**Workflow Flow:**
```
┌─────────────────┐
│  Manual Trigger │
│  (Click to run) │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Execute Command │
│ (Ingestion)     │
│ ingest_ads_spend│
│ .py             │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Execute Command │
│ (Validation)    │
│ validate_ingest │
│ ion.py          │
└─────────────────┘
```

### 3. Run Data Ingestion

#### Method A: Via n8n Workflow (Recommended)
Execute the complete workflow through the n8n web interface:

1. Open your n8n workflow
2. Click the **"Execute workflow"** button on the Manual Trigger node
3. The workflow will:
   - **Step 1**: Run the ingestion script (`ingest_ads_spend.py`)
   - **Step 2**: Automatically validate the results (`validate_ingestion.py`)
   - **Result**: Display comprehensive ingestion and validation results
   
   #### What You'll See:
   When you execute the workflow, you'll get output like:
   ```
   🔍 Starting ingestion validation...
   ⏰ Validation time: 2025-08-27 16:42:43
   
   ✅ Ingestion Validation Successful!
   📊 Total rows ingested: 2,000
   
   📋 Recent Data Sample (last 3 rows):
   date        platform account     campaign      spend  clicks  impressions  conversions
   2025-01-01     Meta   AcctA  Prospecting    1115.94     360        15840           29
   2025-01-01   Google   AcctA Brand_Search     789.43     566        22640           28
   2025-01-01   Google   AcctA  Prospecting     381.40     133        10241           12
   
   📈 Data Summary:
   Platforms: 2.0
   Accounts: 3.0
   Campaigns: 4.0
   Total Spend: 1,690,764.32
   Total Clicks: 931,552.0
   Total Impressions: 51,379,827.0
   Total Conversions: 54,917.0
   
   🎉 Validation completed successfully!
   ```

#### Method B: Direct Script Execution
Execute the Python script directly:
```bash
python ingest_ads_spend.py
```

### 4. Verify Ingestion
```bash
python -c "
import duckdb
db = duckdb.connect('warehouse.duckdb')
result = db.execute('SELECT COUNT(*) as total_rows FROM ads_spend').fetchdf()
print(f'Total rows ingested: {result.iloc[0,0]}')
db.close()
"
```