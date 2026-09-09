---
title: "opendata_payroll_ingestion"
description: "Ingestion DAG for opendata - payroll"
tags: ["ingestion", "opendata"]
---

# opendata_payroll_ingestion

- **DAG ID:** `opendata_payroll_ingestion`
- **Description:** Ingestion DAG for opendata - payroll
- **Schedule:** None
- **Catchup:** False
- **Start date:** 2025-08-01T05:00:00+00:00
- **Max active runs:** 1
- **Max active tasks:** 16
- **Tags:** ingestion, opendata

## Default Args

| Key | Value |
|---|---|
| `owner` | `airflow` |


## Details


    # {dag_id} DAG

    ## Overview
    This DAG manages the ingestion of payroll data into the data warehouse.

    It uses **dlt (data load tool)** to orchestrate the extraction, transformation,
    and loading of data from source systems.

    ## Task Flow
    1. `opendata_start` - Start marker
    2. `opendata_run_ingestion` - Run the dlt ingestion pipeline
    3. `opendata_validate_ingestion` - Validate the ingestion results
    4. `opendata_end` - End marker

    ## Configuration
    - **Domain**: opendata
    - **Data Source**: payroll_ingestion
    - **Schedule**: manual trigger only
    - **Owner**: airflow

    ## Pipeline Code
    The dlt pipeline and source definitions are located in:
    - `include/opendata/ingestion/pipeline.py`
    - `include/opendata/ingestion/sources.py`

    ## Secrets and Configuration
    All sensitive configuration (API keys, credentials, connection strings)
    should be managed via:
    - Airflow Connections
    - Airflow Variables
    - Environment variables
    - Azure Key Vault (if using Azure)
    - Google Cloud Secret Manager (if using GCP)

    Do NOT hard-code secrets in the DAG or pipeline code.
    

## Task Flow

```mermaid
flowchart LR
  start --> run_ingestion
  run_ingestion --> validate
  validate --> end
```

## Tasks (4)

| Task ID | Operator | Retries | Doc |
|---|---:|---:|---|
| `start` | _PythonDecoratedOperator | 0 | Start task. |
| `run_ingestion` | _PythonDecoratedOperator | 0 |  |
| `validate` | _PythonDecoratedOperator | 0 | Validate the ingestion results.  Confirm that the replacement load created a non-empty destination table. |
| `end` | _PythonDecoratedOperator | 0 | End task. |

---
_This file is auto-generated. Regenerate with the project's `generate_dag_docs.py` script._