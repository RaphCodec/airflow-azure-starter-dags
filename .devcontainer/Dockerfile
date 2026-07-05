FROM apache/airflow:3.1.6-python3.12
USER root
# Install Azure CLI
RUN apt-get update \
	&& apt-get install -y --no-install-recommends curl ca-certificates apt-transport-https lsb-release gnupg \
	&& curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
USER airflow
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt
RUN uv tool install pre-commit@latest \
 && uv tool install commitizen@latest \
 && uv tool install ruff@latest