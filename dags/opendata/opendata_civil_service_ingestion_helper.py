import os

from airflow.sdk import BaseHook, dag
from dlt.helpers.airflow_helper import PipelineTasksGroup

from include.opendata.civil_service import create_pipeline, create_source

PIPELINE_NAME = "nyc_open_data_airflow_helper"


@dag(
    dag_id="opendata_civil_service_ingestion_helper",
    dag_display_name="OpenData Civil Service Ingestion (dlt Airflow Helper)",
    tags=["dlt", "OpenData", "ingestion", "helper"],
    catchup=False,
    schedule=None,
)
def civil_service_pipeline_with_helper():
    tasks = PipelineTasksGroup(pipeline_name=PIPELINE_NAME, wipe_local_data=True)
    pipeline = create_pipeline(pipeline_name=PIPELINE_NAME)

    def load_api_config():
        conn = BaseHook.get_connection("opendata-v3")
        return conn.host, conn.extra_dejson.get("headers", {})

    source = create_source(client_config=load_api_config)

    def configure_credentials():
        md_conn = BaseHook.get_connection("motherduck_default")
        if not md_conn.password:
            raise ValueError("The motherduck_default connection must provide a password")
        os.environ["DESTINATION__MOTHERDUCK__CREDENTIALS"] = f"md:OpenData?motherduck_token={md_conn.password}"

    tasks.add_run(
        pipeline,
        data=source,
        decompose="parallel-isolated",
        serialize_first_task=False,
        on_before_run=configure_credentials,
    )


civil_service_pipeline_with_helper()
