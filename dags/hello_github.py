from airflow.sdk import dag, task
from datetime import datetime

from structlog import get_logger

log = get_logger()

@dag(
    start_date=datetime(2025, 8, 25),
    schedule='@hourly',
    catchup=False,
    tags=['example'],
)
def hello_world():
    @task
    def print_message():
        log.info('Hello, from GitHub!')

    print_message()

hello_world()