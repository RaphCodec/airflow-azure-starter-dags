from airflow.sdk import BaseHook, dag, task
from structlog import get_logger

from include.opendata.civil_service import run_pipeline

log = get_logger()


@dag(
    dag_id="opendata_civil_service_ingestion",
    dag_display_name="OpenData Civil Service Ingestion",
    tags=["dlt", "OpenData", "ingestion"],
    catchup=False,
    schedule=None,
)
def civil_service_pipeline():
    @task()
    def run_civil_service_pipeline():
        conn = BaseHook.get_connection("opendata-v3")
        md_conn = BaseHook.get_connection("motherduck_default")

        headers = conn.extra_dejson.get("headers", {})
        run_info = run_pipeline(url=conn.host, headers=headers, md_token=md_conn.password)
        log.info(run_info)

    run_civil_service_pipeline()


civil_service_pipeline()
