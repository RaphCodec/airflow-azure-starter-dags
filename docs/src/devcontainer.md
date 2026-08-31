---
title: "Dev Container"
description: "Base image, installed packages, ports, and VS Code extensions for the Airflow dev container."
---

# Dev Container

_This file is auto-generated. Regenerate with `docs/scripts/generate_devcontainer_docs.py`._

## Base Image

```dockerfile
FROM apache/airflow:3.3.1-python3.14

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
```

## uv Tools

These tools are installed globally via `uv tool install`:

| Tool |
|---|
| `prek@latest\` |
| `commitizen@latest\` |
| `ruff@latest` |

## Python Libraries

### Apache Airflow

| Package | Version |
|---|---|
| `apache-airflow-core` | 3.3.1 |
| `apache-airflow-task-sdk` | 1.3.1 |
| `apache-airflow` | 3.3.1 |

### Airflow Providers

| Package | Version |
|---|---|
| `apache-airflow-providers-amazon` | 9.34.0 |
| `apache-airflow-providers-celery` | 3.23.1 |
| `apache-airflow-providers-common-compat` | 1.18.0 |
| `apache-airflow-providers-common-io` | 1.8.0 |
| `apache-airflow-providers-common-sql` | 2.1.0 |
| `apache-airflow-providers-git` | 0.4.2 |
| `apache-airflow-providers-google` | 22.3.0 |
| `apache-airflow-providers-http` | 6.0.4 |
| `apache-airflow-providers-microsoft-azure` | 14.1.0 |
| `apache-airflow-providers-odbc` | 4.12.3 |
| `apache-airflow-providers-openlineage` | 2.20.0 |
| `apache-airflow-providers-postgres` | 7.0.1 |
| `apache-airflow-providers-smtp` | 3.0.3 |
| `apache-airflow-providers-snowflake` | 6.16.0 |
| `apache-airflow-providers-standard` | 1.17.0 |

### Azure

| Package | Version |
|---|---|
| `azure-ai-projects` | 2.4.0 |
| `azure-batch` | 14.2.0 |
| `azure-common` | 1.1.28 |
| `azure-core` | 1.41.0 |
| `azure-cosmos` | 4.16.3 |
| `azure-datalake-store` | 1.0.1 |
| `azure-identity` | 1.25.3 |
| `azure-keyvault-secrets` | 4.11.1 |
| `azure-kusto-data` | 6.0.4 |
| `azure-mgmt-compute` | 38.3.0 |
| `azure-mgmt-containerinstance` | 10.1.0 |
| `azure-mgmt-containerregistry` | 15.0.0 |
| `azure-mgmt-core` | 1.6.0 |
| `azure-mgmt-cosmosdb` | 10.0.0 |
| `azure-mgmt-datafactory` | 10.0.0 |
| `azure-mgmt-datalake-nspkg` | 3.0.1 |
| `azure-mgmt-datalake-store` | 0.5.0 |
| `azure-mgmt-nspkg` | 3.0.2 |
| `azure-mgmt-resource` | 26.0.0 |
| `azure-mgmt-storage` | 25.1.0 |
| `azure-nspkg` | 3.0.2 |
| `azure-servicebus` | 7.14.3 |
| `azure-storage-blob` | 12.30.0 |
| `azure-storage-file-datalake` | 12.25.0 |
| `azure-storage-file-share` | 12.26.0 |
| `azure-synapse-artifacts` | 0.22.0 |
| `azure-synapse-spark` | 0.7.0 |

### Other

| Package | Version |
|---|---|
| `a2wsgi` | 1.10.10 |
| `adal` | 1.2.7 |
| `adlfs` | 2026.8.0 |
| `aenum` | 3.1.17 |
| `agate` | 1.9.1 |
| `aiofiles` | 25.1.0 |
| `aiohappyeyeballs` | 2.7.1 |
| `aiohttp-cors` | 0.8.1 ; python_full_version < '3.15' |
| `aiohttp` | 3.14.3 |
| `aiosignal` | 1.4.0 |
| `aiosmtplib` | 5.1.2 |
| `aiosqlite` | 0.21.0 |
| `alembic` | 1.19.1 |
| `amqp` | 5.3.1 |
| `annotated-doc` | 0.0.5 |
| `annotated-types` | 0.8.0 |
| `anyio` | 4.14.2 |
| `argcomplete` | 3.7.2 |
| `arrow` | 1.4.0 |
| `asgiref` | 3.12.1 |
| `asn1crypto` | 1.5.1 |
| `astronomer-cosmos` | 1.15.1 |
| `asyncpg` | 0.31.0 |
| `attrs` | 26.1.0 |
| `authlib` | 1.7.2 |
| `babel` | 2.18.0 |
| `beautifulsoup4` | 4.15.0 |
| `billiard` | 4.2.4 |
| `boto3` | 1.43.78 |
| `botocore` | 1.43.78 |
| `cachetools` | 7.1.7 |
| `cadwyn` | 7.0.0 |
| `cattrs` | 26.1.0 |
| `celery` | 5.6.3 |
| `certifi` | 2026.7.22 |
| `cffi` | 2.1.1 |
| `chardet` | 7.6.0 |
| `charset-normalizer` | 3.5.1 |
| `click-didyoumean` | 0.3.1 |
| `click-plugins` | 1.1.1.2 |
| `click-repl` | 0.3.0 |
| `click` | 8.4.2 |
| `colorama` | 0.4.6 |
| `colorful` | 0.5.8 ; python_full_version < '3.15' |
| `colorlog` | 6.12.0 |
| `cron-descriptor` | 2.1.0 |
| `croniter` | 6.2.4 |
| `cryptography` | 50.0.0 |
| `daff` | 1.4.2 |
| `dag-factory` | 1.1.0 |
| `db-dtypes` | 1.7.1 |
| `dbt-adapters` | 1.24.5 |
| `dbt-common` | 1.39.0 |
| `dbt-core-experimental-parser` | 2.0.0b2 |
| `dbt-core` | 1.12.3 |
| `dbt-duckdb` | 1.11.0 |
| `dbt-extractor` | 0.6.0 |
| `dbt-protos` | 1.0.565 |
| `decorator` | 5.3.1 |
| `deepdiff` | 8.6.2 |
| `deprecated` | 1.3.1 |
| `deprecation` | 2.1.0 |
| `dill` | 0.4.1 |
| `distlib` | 0.4.3 |
| `distro` | 1.9.0 |
| `dlthub` | 0.30.0 |
| `dnspython` | 2.8.0 |
| `docstring-parser` | 0.18.0 |
| `duckdb` | 1.5.5 |
| `email-validator` | 2.3.0 |
| `fastapi-cli` | 0.0.32 |
| `fastapi` | 0.136.3 |
| `fastuuid` | 0.14.0 |
| `filelock` | 3.32.3 |
| `flower` | 2.1.0 |
| `frozenlist` | 1.8.0 |
| `fsspec` | 2026.7.0 |
| `gcloud-aio-auth` | 5.5.0 |
| `gcloud-aio-bigquery` | 7.1.0 |
| `gcloud-aio-storage` | 9.6.4 |
| `gcsfs` | 2026.8.0 |
| `gitdb` | 4.0.12 |
| `gitpython` | 3.1.59 |
| `google-ads` | 31.4.0 |
| `google-analytics-admin` | 0.30.1 |
| `google-api-core` | 2.34.0 |
| `google-api-python-client` | 2.199.0 |
| `google-auth-httplib2` | 0.4.1 |
| `google-auth-oauthlib` | 1.4.0 |
| `google-auth` | 2.56.3 |
| `google-cloud-aiplatform` | 1.165.1 |
| `google-cloud-alloydb` | 0.11.0 |
| `google-cloud-appengine-logging` | 1.10.0 |
| `google-cloud-audit-log` | 0.6.1 |
| `google-cloud-automl` | 2.20.0 |
| `google-cloud-batch` | 0.22.2 |
| `google-cloud-bigquery-datatransfer` | 3.23.0 |
| `google-cloud-bigquery-storage` | 2.40.0 |
| `google-cloud-bigquery` | 3.43.0 |
| `google-cloud-bigtable` | 2.42.0 |
| `google-cloud-build` | 3.38.1 |
| `google-cloud-compute` | 1.50.0 |
| `google-cloud-container` | 2.65.0 |
| `google-cloud-core` | 2.6.1 |
| `google-cloud-datacatalog` | 3.31.0 |
| `google-cloud-dataflow-client` | 0.14.0 |
| `google-cloud-dataform` | 0.11.2 |
| `google-cloud-dataplex` | 2.20.0 |
| `google-cloud-dataproc-metastore` | 1.23.0 |
| `google-cloud-dataproc` | 5.30.0 |
| `google-cloud-dlp` | 3.38.0 |
| `google-cloud-kms` | 3.16.0 |
| `google-cloud-language` | 2.21.0 |
| `google-cloud-logging` | 3.16.2 |
| `google-cloud-managedkafka` | 0.4.1 |
| `google-cloud-memcache` | 1.16.0 |
| `google-cloud-monitoring` | 2.31.0 |
| `google-cloud-orchestration-airflow` | 1.22.0 |
| `google-cloud-os-login` | 2.22.0 |
| `google-cloud-pubsub` | 2.39.1 |
| `google-cloud-redis` | 2.22.0 |
| `google-cloud-resource-manager` | 1.18.0 |
| `google-cloud-run` | 0.16.1 |
| `google-cloud-secret-manager` | 2.30.0 |
| `google-cloud-spanner` | 3.69.1 |
| `google-cloud-speech` | 2.40.0 |
| `google-cloud-storage-control` | 1.13.0 |
| `google-cloud-storage-transfer` | 1.21.0 |
| `google-cloud-storage` | 3.13.1 |
| `google-cloud-tasks` | 2.24.0 |
| `google-cloud-texttospeech` | 2.37.0 |
| `google-cloud-translate` | 3.27.0 |
| `google-cloud-videointelligence` | 2.20.0 |
| `google-cloud-vision` | 3.15.0 |
| `google-cloud-workflows` | 1.23.0 |
| `google-crc32c` | 1.8.0 |
| `google-genai` | 2.19.0 |
| `google-resumable-media` | 2.10.1 |
| `googleapis-common-protos` | 1.75.1 |
| `greenback` | 1.3.0 |
| `greenlet` | 3.5.5 |
| `grpc-google-iam-v1` | 0.14.5 |
| `grpc-interceptor` | 0.15.4 |
| `grpcio-gcp` | 0.2.2 |
| `grpcio-status` | 1.83.0 |
| `grpcio` | 1.83.0 |
| `h11` | 0.16.0 |
| `h2` | 4.4.1 |
| `hf-xet` | 1.6.0 ; platform_machine  |
| `hpack` | 4.2.0 |
| `httpcore` | 1.0.9 |
| `httplib2` | 0.32.0 |
| `httptools` | 0.8.0 |
| `httpx` | 0.28.1 |
| `huggingface-hub` | 1.28.0 |
| `humanize` | 4.16.0 |
| `hyperframe` | 6.1.0 |
| `idna` | 3.19 |
| `ijson` | 3.4.0.post0 |
| `immutabledict` | 4.3.1 |
| `importlib-metadata` | 8.9.0 |
| `inflection` | 0.5.1 |
| `iniconfig` | 2.3.0 |
| `isodate` | 0.7.2 |
| `isoduration` | 20.11.0 |
| `itsdangerous` | 2.2.0 |
| `jinja2` | 3.1.6 |
| `jiter` | 0.16.0 |
| `jmespath` | 1.1.0 |
| `joblib` | 1.5.3 |
| `joserfc` | 1.7.4 |
| `jsonpath-ng` | 1.8.0 |
| `jsonschema-specifications` | 2025.9.1 |
| `jsonschema` | 4.26.0 |
| `kombu` | 5.6.2 |
| `lazy-object-proxy` | 1.12.0 |
| `leather` | 0.4.1 |
| `libcst` | 1.9.0 |
| `linkify-it-py` | 2.1.0 |
| `litellm` | 1.96.2 |
| `lockfile` | 0.12.2 |
| `looker-sdk` | 26.12.0 |
| `lxml` | 6.1.2 |
| `mako` | 1.4.1 |
| `markdown-it-py` | 4.2.0 |
| `markupsafe` | 3.0.3 |
| `marshmallow` | 4.3.1 |
| `mashumaro` | 3.17 |
| `mdurl` | 0.1.2 |
| `methodtools` | 0.4.7 |
| `metricflow` | 0.212.0 |
| `microsoft-kiota-abstractions` | 1.11.9 |
| `microsoft-kiota-authentication-azure` | 1.11.9 |
| `microsoft-kiota-http` | 1.11.9 |
| `microsoft-kiota-serialization-json` | 1.11.9 |
| `microsoft-kiota-serialization-text` | 1.11.9 |
| `mmh3` | 5.2.1 |
| `more-itertools` | 10.8.0 |
| `msal-extensions` | 1.3.1 |
| `msal` | 1.37.0 |
| `msgpack` | 1.2.1 |
| `msgraph-core` | 1.5.1 |
| `msgraphfs` | 0.5 |
| `msgspec` | 0.21.1 |
| `msrest` | 0.7.1 |
| `msrestazure` | 0.6.4.post1 |
| `multidict` | 6.7.1 |
| `narwhals` | 2.25.0 |
| `natsort` | 8.4.0 |
| `networkx` | 3.6.1 |
| `numpy` | 2.5.2 |
| `oauthlib` | 3.3.1 |
| `openai` | 2.54.0 |
| `opencensus-context` | 0.1.3 ; python_full_version < '3.15' |
| `opencensus` | 0.11.4 ; python_full_version < '3.15' |
| `openlineage-integration-common` | 1.52.0 |
| `openlineage-python` | 1.52.0 |
| `openlineage-sql` | 1.52.0 |
| `opentelemetry-api` | 1.44.0 |
| `opentelemetry-exporter-otlp-proto-common` | 1.44.0 |
| `opentelemetry-exporter-otlp-proto-grpc` | 1.44.0 |
| `opentelemetry-exporter-otlp-proto-http` | 1.44.0 |
| `opentelemetry-exporter-otlp` | 1.44.0 |
| `opentelemetry-exporter-prometheus` | 0.65b0 ; python_full_version < '3.15' |
| `opentelemetry-proto` | 1.44.0 |
| `opentelemetry-resourcedetector-gcp` | 1.14.0 |
| `opentelemetry-sdk` | 1.44.0 |
| `opentelemetry-semantic-conventions` | 0.65b0 |
| `orderly-set` | 5.5.0 |
| `outcome` | 1.3.0.post0 |
| `packaging` | 26.3 |
| `pandas-gbq` | 0.35.1 |
| `pandas` | 3.0.5 |
| `parsedatetime` | 2.6 |
| `pathlib-abc` | 0.5.2 |
| `pathspec` | 1.0.4 |
| `pendulum` | 3.2.0 |
| `platformdirs` | 4.11.3 |
| `pluggy` | 1.6.0 |
| `polars-runtime-32` | 1.43.2 |
| `polars-st` | 0.7.1 |
| `polars` | 1.43.2 |
| `prometheus-client` | 0.26.0 |
| `prompt-toolkit` | 3.0.53 |
| `propcache` | 0.5.2 |
| `proto-plus` | 1.28.3 |
| `protobuf` | 6.33.6 |
| `psutil` | 7.2.2 |
| `psycopg-binary` | 3.3.4 ; implementation_name != 'pypy' |
| `psycopg2-binary` | 2.9.12 |
| `psycopg` | 3.3.4 |
| `py-spy` | 0.4.2 ; python_full_version < '3.15' |
| `pyarrow` | 25.0.1 |
| `pyasn1-modules` | 0.4.2 |
| `pyasn1` | 0.6.4 |
| `pyathena` | 3.35.4 |
| `pycparser` | 3.0 ; implementation_name != 'PyPy' |
| `pydantic-core` | 2.46.4 |
| `pydantic-extra-types` | 2.11.1 |
| `pydantic-settings` | 2.15.0 |
| `pydantic` | 2.13.4 |
| `pydata-google-auth` | 1.9.1 |
| `pygments` | 2.21.0 |
| `pygtrie` | 2.5.0 |
| `pyjwt` | 2.13.0 |
| `pyodbc` | 5.3.0 |
| `pyogrio` | 0.13.0 |
| `pyopenssl` | 26.4.0 |
| `pyparsing` | 3.3.2 |
| `pytest` | 9.1.1 |
| `python-daemon` | 3.1.2 |
| `python-dateutil` | 2.9.0.post0 |
| `python-discovery` | 1.5.2 |
| `python-dotenv` | 1.2.3 |
| `python-multipart` | 0.0.32 |
| `python-slugify` | 8.0.4 |
| `pytimeparse` | 1.1.8 |
| `pytz` | 2026.3.post1 |
| `pyyaml` | 6.0.3 |
| `rapidfuzz` | 3.14.5 |
| `ray` | 2.57.0 ; python_full_version < '3.15' |
| `redis` | 6.4.0 |
| `redshift-connector` | 2.1.16 |
| `referencing` | 0.37.0 |
| `regex` | 2026.7.19 |
| `requests-oauthlib` | 2.0.0 |
| `requests-toolbelt` | 1.0.0 |
| `requests` | 2.34.2 |
| `rich-argparse` | 1.8.0 |
| `rich-toolkit` | 0.20.3 |
| `rich` | 15.0.0 |
| `rpds-py` | 2026.6.3 |
| `rsa` | 4.9.1 |
| `ruamel-yaml` | 0.19.1 |
| `s3transfer` | 0.19.2 |
| `sagemaker-studio` | 1.0.27 |
| `scikit-learn` | 1.9.0 |
| `scipy` | 1.18.1 |
| `scramp` | 1.4.17 |
| `setproctitle` | 1.3.7 |
| `setuptools` | 84.0.0 |
| `shellingham` | 1.5.4 |
| `six` | 1.17.0 |
| `smart-open` | 8.0.1 ; python_full_version < '3.15' |
| `smmap` | 5.0.3 |
| `sniffio` | 1.3.1 |
| `snowflake-connector-python` | 4.7.2 |
| `snowflake-sqlalchemy` | 1.11.0 |
| `snowplow-tracker` | 1.1.0 |
| `sortedcontainers` | 2.4.0 |
| `soupsieve` | 2.9.2 |
| `sqlalchemy-bigquery` | 1.17.2 |
| `sqlalchemy-spanner` | 1.19.0 |
| `sqlalchemy` | 2.0.52 |
| `sqlglot` | 30.17.0 |
| `sqlparse` | 0.6.0 |
| `starlette` | 1.6.0 |
| `std-uritemplate` | 2.0.12 |
| `structlog` | 26.1.0 |
| `svcs` | 26.1.0 |
| `tabulate` | 0.10.0 |
| `tenacity` | 9.1.4 |
| `termcolor` | 3.3.0 |
| `text-unidecode` | 1.3 |
| `threadpoolctl` | 3.6.0 |
| `tiktoken` | 0.14.0 |
| `tokenizers` | 0.23.1 |
| `tomlkit` | 0.15.1 |
| `tornado` | 6.5.8 |
| `tqdm` | 4.70.0 |
| `typer` | 0.27.1 |
| `types-protobuf` | 7.35.1.20260822 |
| `typing-extensions` | 4.16.0 |
| `typing-inspection` | 0.4.4 |
| `tzdata` | 2026.3 |
| `tzlocal` | 5.4.4 |
| `uc-micro-py` | 2.0.0 |
| `universal-pathlib` | 0.3.10 |
| `uritemplate` | 4.2.0 |
| `urllib3` | 2.7.0 |
| `uuid6` | 2025.0.1 |
| `uvicorn` | 0.52.4 |
| `uvloop` | 0.22.1 ; platform_python_implementation != 'PyPy' and sys_platform != 'cygwin' and sys_platform != 'win32' |
| `vine` | 5.1.0 |
| `virtualenv` | 21.7.4 |
| `watchfiles` | 1.2.0 |
| `watchtower` | 3.4.0 |
| `wcwidth` | 0.8.2 |
| `websockets` | 16.1.1 |
| `wirerope` | 1.0.0 |
| `wrapt` | 2.3.0 |
| `yarl` | 1.24.5 |
| `zipp` | 4.1.0 |


## Forwarded Ports

| Port | Description |
|---|---|
| `8080` | Airflow UI & API |
| `5555` | Flower (Celery monitoring) |
| `8000` |  |

## VS Code Extensions

| Extension ID |
|---|
| `ms-python.python` |
| `ms-python.vscode-pylance` |
| `mechatroner.rainbow-csv` |
| `adamviola.parquet-explorer` |
| `charliermarsh.ruff` |
| `redhat.vscode-yaml` |
| `mtxr.sqltools` |
| `koszti.snowflake-driver-for-sqltools` |
| `snowflake.snowflake-vsc` |
| `ms-mssql.mssql` |
| `sqlfluff.vscode-sqlfluff` |
| `necatiarslan.airflow-vscode-extension` |
| `aaron-bond.better-comments` |
| `streetsidesoftware.code-spell-checker` |
| `tamasfe.even-better-toml` |
