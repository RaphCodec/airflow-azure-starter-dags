ARG AIRFLOW_VERSION=3.1.6
FROM apache/airflow:${AIRFLOW_VERSION}
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt