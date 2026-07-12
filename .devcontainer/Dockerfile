FROM apache/airflow:3.1.8-python3.12

USER root
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends unixodbc-dev gcc g++ curl apt-transport-https gnupg2 ca-certificates lsb-release iputils-ping net-tools ripgrep fish \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/microsoft-prod.gpg] https://packages.microsoft.com/repos/azure-cli/ bookworm main" > /etc/apt/sources.list.d/azure-cli.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 azure-cli \
    && rm -rf /var/lib/apt/lists/* \
    && usermod --shell /usr/bin/fish airflow


USER airflow

COPY requirements.txt .
RUN uv pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
RUN uv tool install prek@latest\
    && uv tool install commitizen@latest\
    && uv tool install ruff@latest