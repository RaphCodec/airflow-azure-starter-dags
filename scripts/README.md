# DAG Generator Implementation Summary

This directory contains a comprehensive DAG generation system for your Airflow project.

## Files Created

### 1. `create_dag.py` (Main Generator)
The primary entry point for DAG generation. Provides a CLI for creating standardized Airflow DAGs.

**Key Features:**
- Generates three types of DAGs: ingestion, processing, orchestration
- Domain-based naming conventions
- Comprehensive argument validation
- File conflict detection
- Step-by-step guidance for next steps

**Usage:**
```bash
python scripts/create_dag.py --domain sales --name orders --type ingestion --schedule "@daily"
```

### 2. `dag_helpers.py` (Helper Utilities)
Provides functions for validating and generating task IDs and DAG IDs.

**Key Functions:**
- `normalize_identifier()` - Normalize domain/name to valid identifiers
- `validate_airflow_id()` - Validate Airflow-compatible IDs
- `generate_task_id()` - Generate domain-based task IDs
- `generate_dag_id()` - Generate domain-based DAG IDs
- `validate_unique_task_ids()` - Ensure no duplicate task IDs

**Naming Conventions:**
- Task IDs: `<domain>_<action>_<object>` or `<domain>_<action>`
- DAG IDs: `<domain>_<name>_<type>`
- All lowercase, underscores for separation

### 3. `dag_templates.py` (Template Definitions)
Contains template strings for each DAG type.

**Template Functions:**
- `get_ingestion_dag_template()` - dlt-based ingestion DAG
- `get_processing_dag_template()` - Data transformation DAG
- `get_orchestration_dag_template()` - DAG coordination DAG
- `get_dlt_pipeline_template()` - dlt pipeline code template
- `get_dlt_sources_template()` - dlt source definitions template

**Features:**
- Comprehensive docstrings
- TODO markers for implementation guidance
- Domain-based naming
- Production-ready structure

### 4. `DAG_GENERATOR.md` (Documentation)
Comprehensive documentation covering:
- Quick start guide
- Naming conventions
- DAG type descriptions
- Configuration and secrets management
- Full command reference
- Best practices
- Troubleshooting guide

## Generated DAG Structures

### Ingestion DAGs

Creates:
```
dags/
  {domain}_{name}_ingestion.py

include/
  {domain}/
    ingestion/
      __init__.py
      pipeline.py        # dlt pipeline code
      sources.py         # dlt source definitions
```

**Task Flow:**
```
{domain}_start → {domain}_run_ingestion → {domain}_validate_ingestion → {domain}_end
```

### Processing DAGs

Creates:
```
dags/
  {domain}_{name}_processing.py
```

**Task Flow:**
```
{domain}_extract_{name} → {domain}_transform_{name} → {domain}_validate_{name} → {domain}_publish_{name}
```

### Orchestration DAGs

Creates:
```
dags/
  {domain}_{name}_orchestration.py
```

**Task Flow:**
```
{domain}_start 
  → {domain}_trigger_{name}_ingestion 
  → {domain}_wait_{name}_ingestion 
  → {domain}_trigger_{name}_processing 
  → {domain}_wait_{name}_processing 
  → {domain}_end
```

## Test DAGs Created

The generator has been tested with three example DAGs:

1. **sales_orders_ingestion**
   - Location: `dags/sales_orders_ingestion.py`
   - Supporting files: `include/sales/ingestion/*`
   - Domain: sales | Name: orders | Type: ingestion

2. **finance_transactions_processing**
   - Location: `dags/finance_transactions_processing.py`
   - Domain: finance | Name: transactions | Type: processing

3. **marketing_campaigns_orchestration**
   - Location: `dags/marketing_campaigns_orchestration.py`
   - Domain: marketing | Name: campaigns | Type: orchestration

All test DAGs have been verified for:
- ✓ Valid Python syntax
- ✓ Valid DAG ID and task ID generation
- ✓ Domain-based naming conventions
- ✓ Appropriate task flows

## Quick Start Examples

### Create an Ingestion DAG

```bash
python scripts/create_dag.py \
  --domain sales \
  --name orders \
  --type ingestion \
  --schedule "@daily" \
  --owner sales_team
```

Creates:
- `dags/sales_orders_ingestion.py`
- `include/sales/ingestion/pipeline.py`
- `include/sales/ingestion/sources.py`

Next steps:
1. Edit sources.py to configure your data source
2. Edit pipeline.py to configure dlt destination
3. Edit the DAG file to import your pipeline

### Create a Processing DAG

```bash
python scripts/create_dag.py \
  --domain finance \
  --name transactions \
  --type processing \
  --schedule "0 2 * * *" \
  --owner finance_team
```

Creates:
- `dags/finance_transactions_processing.py`

Next steps:
1. Implement extract() task
2. Implement transform() task
3. Implement validate() task
4. Implement publish() task

### Create an Orchestration DAG

```bash
python scripts/create_dag.py \
  --domain marketing \
  --name campaigns \
  --type orchestration \
  --schedule "0 9 * * *" \
  --owner marketing_team
```

Creates:
- `dags/marketing_campaigns_orchestration.py`

Next steps:
1. Configure TriggerDagRunOperator for external DAGs
2. Configure ExternalTaskSensor for dependencies
3. Add cross-domain logic as needed

## Key Features

### 1. Domain-Based Naming
All generated DAGs and tasks follow consistent domain-based naming:
- Ensures clarity and consistency
- Makes it easy to identify ownership and purpose
- Follows organization structure

### 2. dlt Integration
Ingestion DAGs are designed to work with dlt (data load tool):
- Separates extraction logic from Airflow orchestration
- Provides reusable pipeline and source code
- Supports multiple dlt destinations (Snowflake, BigQuery, Postgres, DuckDB, etc.)

### 3. Comprehensive Validation
- Prevents invalid DAG/task IDs
- Checks for existing files (use --force to override)
- Validates all arguments before generation
- Clear error messages for troubleshooting

### 4. Production-Ready Templates
- Includes proper error handling
- Documentation with docstrings
- TODO markers for implementation
- Follows Airflow best practices

### 5. No Secrets Hard-Coded
- All templates omit hard-coded credentials
- Guidance on using Airflow Connections/Variables
- Support for Azure Key Vault and Google Cloud Secret Manager
- dlt secrets.toml/config.toml integration

## Command Line Interface

```
usage: create_dag.py [-h] --domain DOMAIN --name NAME
                     --type {ingestion,processing,orchestration}
                     --schedule SCHEDULE [--owner OWNER]
                     [--description DESCRIPTION] [--start-date START_DATE]
                     [--no-catchup] [--force]

Arguments:
  --domain DOMAIN             Domain name (required)
  --name NAME                 DAG name (required)
  --type {ingestion,processing,orchestration}  DAG type (required)
  --schedule SCHEDULE         Cron or Airflow preset (required)
  --owner OWNER               DAG owner (default: airflow)
  --description DESCRIPTION   Custom description
  --start-date START_DATE     Start date YYYY-MM-DD (default: 2025-08-01)
  --no-catchup                Disable catchup
  --force                     Overwrite existing DAGs
  --help                      Show help message
```

## Validation Rules

### Domain and Name
- Must be provided
- Must normalize to valid identifier
- Must contain only alphanumeric characters and underscores after normalization
- Examples: sales, finance, user_events, daily_reconciliation

### Type
- Must be one of: ingestion, processing, orchestration
- Invalid types are rejected

### Generated IDs
- Must be ≤ 250 characters
- Must contain only lowercase letters, digits, hyphens, underscores, dots
- Must start with letter or underscore
- Must be unique within a DAG (for task IDs)

### Files
- DAG files are not overwritten unless --force is used
- Directory structure is automatically created
- Python syntax is validated after generation

## Project Dependencies

The generator uses only built-in Python libraries:
- `argparse` - Command-line argument parsing
- `pathlib` - File path handling
- `re` - Regular expressions for validation

No additional dependencies need to be installed.

## Project Dependencies for Generated DAGs

Generated DAGs depend on packages already installed in your environment:
- `apache-airflow` (3.3.1)
- `pendulum` - For timezone-aware datetime handling
- `structlog` - For structured logging
- `dlt` (dlthub 0.30.0) - For ingestion DAGs
- `pydantic` - For configuration validation (optional)

All required packages are in your `requirements.txt`.

## Environment

- **Airflow Version**: 3.3.1
- **Python Version**: 3.14+
- **dlt Version**: 0.30.0
- **Project Home**: /opt/airflow

## Next Steps

1. **Review the documentation**
   ```bash
   cat scripts/DAG_GENERATOR.md
   ```

2. **Create your first DAG**
   ```bash
   python scripts/create_dag.py --domain sales --name orders --type ingestion --schedule "@daily"
   ```

3. **Implement the generated code**
   - Edit `include/sales/ingestion/sources.py`
   - Edit `include/sales/ingestion/pipeline.py`
   - Update `dags/sales_orders_ingestion.py`

4. **Test locally**
   ```bash
   python include/sales/ingestion/pipeline.py
   ```

5. **Verify in Airflow**
   ```bash
   airflow dags list
   airflow dags details sales_orders_ingestion
   ```

## File Structure

```
/opt/airflow/
├── scripts/
│   ├── __init__.py                 # Package marker
│   ├── create_dag.py               # Main generator script
│   ├── dag_helpers.py              # Helper functions
│   ├── dag_templates.py            # Template definitions
│   └── DAG_GENERATOR.md            # Documentation
│
├── dags/
│   ├── sales_orders_ingestion.py               # Example ingestion DAG
│   ├── finance_transactions_processing.py      # Example processing DAG
│   └── marketing_campaigns_orchestration.py    # Example orchestration DAG
│
└── include/
    └── sales/
        ├── __init__.py
        └── ingestion/
            ├── __init__.py
            ├── pipeline.py                      # dlt pipeline
            └── sources.py                       # dlt sources
```

## Support and Resources

- **Airflow Documentation**: https://airflow.apache.org/docs/
- **dlt Documentation**: https://dlthub.com/docs
- **Project README**: `/opt/airflow/README.md`
- **Generated DAG Documentation**: Each generated DAG includes comprehensive docstrings

---

**Generator Version**: 1.0
**Created**: August 31, 2026
**Status**: Production Ready
