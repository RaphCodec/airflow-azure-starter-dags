from airflow.sdk import dag, task
from datetime import datetime

from structlog import get_logger

log = get_logger()

@dag(
    dag_id='hello_github',
    dag_display_name='Hello GitHub',
    description='A simple DAG to say hello to GitHub',
    start_date=datetime(2025, 8, 25),
    schedule='@hourly',
    catchup=False,
    tags=['example'],
    doc_md="""
    # Description
    This is a basic hello world dag to ensure that Airflow is working properly.
    """
)
def hello_world():
    @task
    def print_message():
        log.info('Hello, from GitHub!')

    print_message()

hello_world()