from airflow.sdk import DAG, task
import pendulum
import pathlib

with DAG(
    dag_id="duckdb_example",
    description="A simple dag to show the use of a python virtual env with duckdb",
    start_date=pendulum.datetime(2025, 8, 1, tz="EST"),
    schedule="@daily",
    catchup=False,
    doc_md="""
    ### Example Virtualenv DAG

    This DAG demonstrates how to use the **`@task.virtualenv`** decorator in Airflow.
    The task installs and runs a library (`duckdb`) **not included in Airflow or your base environment**.
    Using `requirements` ensures the task runs in an isolated virtual environment
    with the specified dependencies.

    **Key points:**
    - The `requirements` parameter pins the package version (`duckdb==1.1.1`).
    - The virtual environment is created only for this task.
    - Great for tasks needing custom dependencies without bloating the global Airflow image.
    """
):
    @task.virtualenv(
        task_id="virtualenv_duckdb", requirements=["duckdb==1.1.1", "numpy==2.3.0", "pandas==2.3.2"], system_site_packages=False,
        pip_install_options=""
    )
    def run_query():
        import duckdb
        result = duckdb.query("SELECT 42 AS answer").to_df()
        print("Query result:\n", result)

    run_query()