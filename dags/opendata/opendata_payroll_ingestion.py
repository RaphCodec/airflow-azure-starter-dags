"""
Ingestion DAG for opendata - payroll_ingestion.

This DAG orchestrates data ingestion using dlt (data load tool).
The actual extraction and loading logic is defined in the dlt pipeline
located in include/opendata/ingestion/.
"""

import pendulum
from airflow.sdk import dag, task
from structlog import get_logger

log = get_logger()


@dag(
    dag_id="opendata_payroll_ingestion",
    description="Ingestion DAG for opendata - payroll",
    start_date=pendulum.datetime(2025, 8, 1, tz="EST"),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["opendata", "ingestion"],
    default_args={
        "owner": "airflow",
    },
    doc_md="""
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
    """,
)
def opendata_payroll_ingestion():
    @task
    def start():
        """Start task."""
        log.info("Starting {dag_id} ingestion")

    @task
    def run_ingestion():
        from include.opendata.ingestion.pipeline import run_ingestion as dlt_run

        load_info = dlt_run()
        log.info("Payroll ingestion completed", load_info=str(load_info))

    @task
    def validate():
        """
        Validate the ingestion results.

        Confirm that the replacement load created a non-empty destination table.
        """
        from include.hooks import MsSqlPythonHook

        hook = MsSqlPythonHook()
        result = hook.get_first("SELECT COUNT_BIG(*) FROM [dbo].[citywide_payroll]")
        row_count = result[0] if result else 0
        if not row_count:
            raise ValueError("dbo.citywide_payroll exists but contains no rows")
        log.info("Payroll table validated", row_count=row_count)

    @task
    def end():
        """End task."""
        log.info("Completed {dag_id} ingestion")

    start() >> run_ingestion() >> validate() >> end()


opendata_payroll_ingestion()
