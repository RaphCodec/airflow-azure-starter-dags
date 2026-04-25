# duckdb_example

**Short Description:** A simple dag to show the use of a python virtual env with duckdb
**Long Description:** 
    ### Example Virtualenv DAG

    This DAG demonstrates how to use the **`@task.virtualenv`** decorator in Airflow.
    The task installs and runs a library (`duckdb`) **not included in Airflow or your base environment**.
    Using `requirements` ensures the task runs in an isolated virtual environment
    with the specified dependencies.

    **Key points:**
    - The `requirements` parameter pins the package version (`duckdb==1.1.1`).
    - The virtual environment is created only for this task.
    - Great for tasks needing custom dependencies without bloating the global Airflow image.
    
**Schedule:** @daily  
**Tags:** 

## Tasks

- virtualenv_duckdb
