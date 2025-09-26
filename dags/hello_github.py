from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello, from Github!")

with DAG(
    dag_id='hello_github_dag',
    start_date=datetime(2025, 8, 25),
    schedule='@hourly',
    catchup=False,
    tags=['example'],
) as dag:
    hello_task = PythonOperator(
        task_id='hello_github_task',
        python_callable=hello_world,
    )