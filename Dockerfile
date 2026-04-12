ARG AIRFLOW_VERSION=3.1.6
FROM apache/airflow:${AIRFLOW_VERSION}
USER root
# Install Azure CLI
RUN apt-get update \
	&& apt-get install -y --no-install-recommends curl ca-certificates apt-transport-https lsb-release gnupg \
	&& curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
USER airflow
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt