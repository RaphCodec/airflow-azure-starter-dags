---
title: "DAG Generator"
description: "Create standardized Airflow DAGs with domain-based naming conventions"
---

# DAG Generator

A comprehensive Python script for generating standardized Apache Airflow DAGs with domain-based naming conventions.

Supports three DAG types: **ingestion** (using dlt), **processing** (data transformation), and **orchestration** (DAG coordination).

## Quick Start

Generate an ingestion DAG for sales orders:

```bash
cd /opt/airflow
python scripts/create_dag.py \
  --domain sales \
  --name orders \
  --type ingestion \
  --schedule "@daily"
```

This creates:
- `dags/sales_orders_ingestion.py` — The main DAG file
- `include/sales/ingestion/pipeline.py` — dlt pipeline code
- `include/sales/ingestion/sources.py` — dlt source definitions

## Naming Conventions

All generated DAGs follow strict **domain-based naming** conventions.

### DAG ID Format

```
<domain>_<name>_<type>
```

**Examples:**
- `sales_orders_ingestion`
- `finance_transactions_processing`
- `marketing_campaigns_orchestration`

### Task ID Format

```
<domain>_<action>[_<object>]
```

**Examples:**
- `sales_start` — Start task
- `sales_extract_orders` — Extract action on orders object
- `sales_validate_orders` — Validate action on orders object
- `sales_load_orders` — Load action on orders object
- `sales_end` — End task

### Naming Rules

- **Domain**: Single word, lowercase (e.g., `sales`, `finance`, `marketing`)
- **Name**: Lowercase, hyphens/spaces converted to underscores (e.g., `orders`, `user_events`)
- **Type**: One of `ingestion`, `processing`, or `orchestration`
- **Action**: Lowercase verb (e.g., `extract`, `validate`, `load`, `transform`)
- **Object**: Lowercase noun matching the name (e.g., `orders`, `transactions`)

## DAG Types

### 1. Ingestion DAGs

Extract and load data using **dlt (data load tool)**.

**When to use:**
- Data extraction from external sources (APIs, databases, files)
- Initial data ingestion into data warehouse
- When you want dlt to handle extraction/loading logic

**Generated structure:**
```
dags/
  {domain}_{name}_ingestion.py

include/
  {domain}/
    ingestion/
      pipeline.py          # dlt pipeline code
      sources.py           # dlt source definitions
```

**Generated task flow:**
```
{domain}_start → {domain}_run_ingestion → {domain}_validate_ingestion → {domain}_end
```

**Example:**
```bash
python scripts/create_dag.py \
  --domain sales \
  --name orders \
  --type ingestion \
  --schedule "@daily" \
  --owner sales_team
```

**Next steps:**
1. Edit `include/sales/ingestion/sources.py` — Configure your data source
2. Edit `include/sales/ingestion/pipeline.py` — Configure dlt destination
3. Edit `dags/sales_orders_ingestion.py` — Import your pipeline
4. Test locally: `python include/sales/ingestion/pipeline.py`

### 2. Processing DAGs

Transform and enrich data using Airflow TaskFlow API.

**When to use:**
- Complex data transformations
- Data quality validation
- Aggregations and enrichment
- Multi-step processing logic

**Generated task flow:**
```
{domain}_extract_{name} → {domain}_transform_{name} → {domain}_validate_{name} → {domain}_publish_{name}
```

**Example:**
```bash
python scripts/create_dag.py \
  --domain finance \
  --name transactions \
  --type processing \
  --schedule "0 2 * * *" \
  --owner finance_team
```

**Next steps:**
1. Edit `dags/finance_transactions_processing.py`
2. Implement `extract()` task logic
3. Implement `transform()` task logic
4. Implement `validate()` task logic
5. Implement `publish()` task logic

### 3. Orchestration DAGs

Coordinate other DAGs without containing business logic.

**When to use:**
- Orchestrating multiple ingestion/processing DAGs
- Complex multi-step workflows spanning multiple domains
- Conditional branching based on external events
- Cross-functional data pipelines

**Generated task flow:**
```
{domain}_start 
  → {domain}_trigger_{name}_ingestion 
  → {domain}_wait_{name}_ingestion 
  → {domain}_trigger_{name}_processing 
  → {domain}_wait_{name}_processing 
  → {domain}_end
```

**Example:**
```bash
python scripts/create_dag.py \
  --domain marketing \
  --name campaigns \
  --type orchestration \
  --schedule "0 9 * * *" \
  --owner marketing_team
```

**Next steps:**
1. Edit `dags/marketing_campaigns_orchestration.py`
2. Configure external DAG triggers using `TriggerDagRunOperator`
3. Configure external task sensors using `ExternalTaskSensor`
4. Add cross-DAG dependencies

## Command Reference

### Required Arguments

```bash
python scripts/create_dag.py \
  --domain <domain> \           # Domain name (e.g., sales, finance)
  --name <name> \               # DAG name (e.g., orders, transactions)
  --type <type> \               # ingestion, processing, or orchestration
  --schedule <schedule>         # Cron or Airflow preset (e.g., @daily, "0 2 * * *")
```

### Optional Arguments

```bash
  --owner <owner>               # DAG owner (default: airflow)
  --description <description>   # Custom DAG description
  --start-date <date>           # Start date YYYY-MM-DD (default: 2025-08-01)
  --no-catchup                  # Disable catchup
  --force                       # Overwrite existing DAG files
  --help                        # Show help message
```

### Examples

**Ingestion DAG:**
```bash
python scripts/create_dag.py \
  --domain sales \
  --name orders \
  --type ingestion \
  --schedule "@daily"
```

**Processing DAG with custom owner:**
```bash
python scripts/create_dag.py \
  --domain finance \
  --name transactions \
  --type processing \
  --schedule "0 2 * * *" \
  --owner finance_team
```

**Orchestration DAG with description:**
```bash
python scripts/create_dag.py \
  --domain marketing \
  --name campaigns \
  --type orchestration \
  --schedule "0 9 * * *" \
  --owner marketing_team \
  --description "Master orchestration for campaign processing"
```

**Overwrite existing DAG:**
```bash
python scripts/create_dag.py \
  --domain sales \
  --name orders \
  --type ingestion \
  --schedule "@daily" \
  --force
```

## Configuration and Secrets

### Airflow Connections

Use Airflow Connections for database and API credentials:

```python
from airflow.hooks.base import BaseHook

# In your pipeline code:
conn = BaseHook.get_connection("my_database")
```

### Airflow Variables

Use Airflow Variables for configuration:

```python
from airflow.models import Variable

# In your DAG or task:
api_url = Variable.get("sales_api_url")
```

### Environment Variables

For local development and testing:

```bash
export SALES_API_KEY="your-api-key"
export SALES_API_URL="https://api.example.com"
```

### Azure Key Vault (if using Azure)

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
secret = client.get_secret("sales-api-key")
```

### dlt Configuration

dlt reads from `secrets.toml` or `config.toml`:

```toml
# ~/.dlt/secrets.toml
[sources.my_source]
api_key = "your-api-key"
api_url = "https://api.example.com"

[destination.duckdb]
path = "/opt/airflow/data/warehouse"
```

**Important:** Never hard-code secrets in DAG files or pipeline code!

## dlt Integration

The generator includes built-in support for dlt (data load tool) v0.30.0 in ingestion DAGs.

### dlt Architecture

```
Airflow DAG
    ↓
Orchestrates
    ↓
dlt Pipeline
    ├── Source
    │   └── Extract from API/Database/File
    ├── Resource
    │   └── Define data structure
    ├── Transform
    │   └── Normalize data
    └── Destination
        └── Load to Data Warehouse
```

### Configure dlt Source

Edit `include/{domain}/ingestion/sources.py`:

```python
import dlt

@dlt.source
def sales_orders_source():
    """Define the sales_orders data source."""
    @dlt.resource(name="orders")
    def fetch_orders():
        """Fetch orders from the API."""
        # TODO: Configure API client
        # TODO: Fetch orders
        yield {"id": 1, "amount": 100}
    
    return fetch_orders()
```

### Configure dlt Pipeline

Edit `include/{domain}/ingestion/pipeline.py`:

```python
import dlt
from .sources import sales_orders_source

def run_ingestion():
    """Run the sales_orders ingestion pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name="sales_orders",
        destination="snowflake",  # or postgres, bigquery, duckdb, etc.
        dataset_name="raw_sales_orders"
    )
    
    load_info = pipeline.run(sales_orders_source())
    return load_info
```

### Supported dlt Destinations

- `duckdb` — Local DuckDB database
- `postgres` — PostgreSQL
- `snowflake` — Snowflake Data Warehouse
- `bigquery` — Google BigQuery
- `redshift` — AWS Redshift
- `weaviate` — Weaviate Vector DB
- `qdrant` — Qdrant Vector DB
- `mssql` — Microsoft SQL Server

## Validation

The generator performs strict validation:

✓ **Domain validation**
- Must be provided and normalize to valid identifier
- Must produce valid Airflow ID

✓ **Name validation**
- Must be provided and normalize to valid identifier
- Must produce valid Airflow ID

✓ **Type validation**
- Must be: `ingestion`, `processing`, or `orchestration`
- Invalid types are rejected

✓ **DAG ID validation**
- Must be ≤ 250 characters
- Must contain only lowercase letters, digits, hyphens, underscores, dots
- Must start with letter or underscore

✓ **File validation**
- Prevents overwriting existing DAGs (use `--force` to override)
- Creates necessary directory structure
- Validates Python syntax after generation

## Error Handling

**Error:** `Configuration Error: --domain is required and must be a string`
- **Solution:** Provide a --domain argument: `--domain sales`

**Error:** `Configuration Error: --type must be one of: ingestion, processing, orchestration`
- **Solution:** Use valid type: `--type ingestion`

**Error:** `✗ DAG file already exists: dags/sales_orders_ingestion.py`
- **Solution:** Use `--force` to overwrite or choose different domain/name

## Best Practices

### 1. Use Meaningful Domain Names

✓ Good:
```bash
python scripts/create_dag.py --domain sales --name orders ...
python scripts/create_dag.py --domain finance --name reconciliation ...
```

✗ Poor:
```bash
python scripts/create_dag.py --domain data --name dag ...
python scripts/create_dag.py --domain pipeline --name process ...
```

### 2. Keep Names Concise but Descriptive

✓ Good:
```bash
--name user_events
--name customer_profiles
--name daily_reconciliation
```

✗ Poor:
```bash
--name extract_transform_load_user_events_and_do_validation_and_publish
```

### 3. Use Appropriate DAG Types

- **Ingestion DAGs:** For data extraction and loading
- **Processing DAGs:** For transformation and enrichment
- **Orchestration DAGs:** For coordinating other DAGs

### 4. Never Hard-Code Secrets

✓ Good:
```python
from airflow.models import Variable
api_key = Variable.get("sales_api_key")
```

✗ Poor:
```python
api_key = "sk-1234567890abcdef"  # NEVER do this!
```

### 5. Test Generated DAGs

Before deploying to production:

```bash
# Verify syntax
python -m py_compile dags/sales_orders_ingestion.py

# Test locally (for ingestion DAGs)
python include/sales/ingestion/pipeline.py

# Check Airflow recognizes the DAG
airflow dags details sales_orders_ingestion
```

## Troubleshooting

### DAG Not Appearing in Airflow

1. Check file syntax:
   ```bash
   python -m py_compile dags/sales_orders_ingestion.py
   ```

2. Verify file location:
   ```bash
   ls -la /opt/airflow/dags/sales_orders_ingestion.py
   ```

3. Check Airflow logs:
   ```bash
   airflow dags list-import-errors
   ```

### dlt Pipeline Not Working

1. Verify dlt installation:
   ```bash
   python -c "import dlt; print(dlt.__version__)"
   ```

2. Test locally:
   ```bash
   python include/sales/ingestion/pipeline.py
   ```

3. Check dlt configuration:
   ```bash
   cat ~/.dlt/secrets.toml
   cat ~/.dlt/config.toml
   ```

## Files

**Generator scripts:** `scripts/`
- `create_dag.py` — Main generator CLI
- `dag_helpers.py` — Helper utilities
- `dag_templates.py` — Template definitions
- `DAG_GENERATOR.md` — Full documentation
- `README.md` — Implementation details

**Generated DAGs:** `dags/`
**Pipeline code:** `include/`

---

**Airflow Version:** 3.3.1 | **dlt Version:** 0.30.0 | **Python:** 3.14+
