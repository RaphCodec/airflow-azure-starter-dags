"""
dlt pipeline for opendata_payroll ingestion.

This module defines the data extraction, transformation, and loading logic
for the opendata_payroll dataset using dlt (data load tool).

Configuration (API keys, credentials, etc.) should be provided via:
- Environment variables
- Airflow Connections
- Airflow Variables
- dlt secrets.toml or config.toml
- Azure Key Vault
- Google Cloud Secret Manager
"""

from urllib.parse import quote

import dlt
from airflow.hooks.base import BaseHook

from .sources import opendata_payroll_source

MSSQL_CONNECTION_ID = "mssql_python_default"
MSSQL_SCHEMA = "dbo"
MSSQL_TABLE = "citywide_payroll"


def _get_mssql_credentials(connection_id: str = MSSQL_CONNECTION_ID) -> str:
    connection = BaseHook.get_connection(connection_id)
    extras = connection.extra_dejson or {}
    database = connection.schema or extras.get("database")
    if not connection.host or not database:
        raise ValueError(f"Airflow connection {connection_id!r} must define host and database")

    authentication = extras.get("authentication", "SqlPassword")
    if authentication != "SqlPassword":
        raise ValueError(
            "The dlt MSSQL destination currently requires SqlPassword authentication; "
            f"connection {connection_id!r} uses {authentication!r}"
        )
    if not connection.login or connection.password is None:
        raise ValueError(f"Airflow connection {connection_id!r} must define login and password")

    port = connection.port or 1433
    encrypt = extras.get("encrypt", "yes")
    trust_server_certificate = extras.get(
        "trustservercertificate",
        extras.get("trust_server_certificate", "no"),
    )
    if isinstance(encrypt, bool):
        encrypt = "yes" if encrypt else "no"
    if isinstance(trust_server_certificate, bool):
        trust_server_certificate = "yes" if trust_server_certificate else "no"

    return (
        f"mssql://{quote(connection.login, safe='')}:{quote(connection.password, safe='')}"
        f"@{connection.host}:{port}/{quote(database, safe='')}"
        f"?driver=ODBC+Driver+18+for+SQL+Server"
        f"&Encrypt={encrypt}"
        f"&TrustServerCertificate={trust_server_certificate}"
    )


def run_ingestion(
    connection_id: str = MSSQL_CONNECTION_ID,
    schema: str = MSSQL_SCHEMA,
    table: str = MSSQL_TABLE,
):
    """
    Run the opendata_payroll ingestion pipeline.

    This function:
    1. Creates a dlt pipeline instance
    2. Configures the data source
    3. Loads data into the destination (data warehouse)
    4. Returns load information

    Returns:
        LoadInfo: dlt load information object
    """
    pipeline = dlt.pipeline(
        pipeline_name="opendata_payroll",
        destination="mssql",
        credentials=_get_mssql_credentials(connection_id),
        dataset_name=schema,
    )

    return pipeline.run(
        opendata_payroll_source(),
        table_name=table,
        write_disposition="replace",
    )
