---
title: "duckdb_example"
description: "A simple dag to show the use of a python virtual env with duckdb"
tags: []
---

# duckdb_example

- **DAG ID:** `duckdb_example`
- **Description:** A simple dag to show the use of a python virtual env with duckdb
- **Schedule:** @daily
- **Catchup:** False
- **Start date:** 2025-08-01T05:00:00+00:00
- **Tags:** 

## Details
 

    ### Example Virtualenv DAG

    This DAG demonstrates how to use the **`@task.virtualenv`** decorator in Airflow.
    The task installs and runs a library (`duckdb`) **not included in Airflow or your base environment**.
    Using `requirements` ensures the task runs in an isolated virtual environment
    with the specified dependencies.

    **Key points:**
    - The `requirements` parameter pins the package version (`duckdb==1.1.1`).
    - The virtual environment is created only for this task.
    - Great for tasks needing custom dependencies without bloating the global Airflow image.
    

## Tasks (1)

| Task ID | Operator | Retries | Doc |
|---|---:|---:|---|
| `virtualenv_duckdb` | _PythonVirtualenvDecoratedOperator | 0 |  |

---
_This file is auto-generated. Regenerate with the project's `generate_dag_docs.py` script._