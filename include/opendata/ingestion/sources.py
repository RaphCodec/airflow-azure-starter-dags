"""
dlt source definitions for opendata_payroll data.

This module defines the data source configuration and extraction logic.
"""

import os

import dlt
import requests

SOCRATA_DOMAIN = "data.cityofnewyork.us"
SOCRATA_DATASET_ID = "k397-673e"
SOCRATA_PAGE_SIZE = 10_000
SOCRATA_QUERY_TIMEOUT_SECONDS = 600


def _query_socrata_page(
    endpoint: str,
    page_number: int,
    page_size: int,
    app_token: str | None,
) -> list[dict[str, object]]:
    headers = {"Accept": "application/json"}
    if app_token:
        headers["X-App-Token"] = app_token

    response = requests.post(
        endpoint,
        headers=headers,
        json={
            "query": "SELECT *",
            "page": {"pageNumber": page_number, "pageSize": page_size},
            "includeSystem": False,
            "includeSynthetic": False,
        },
        timeout=SOCRATA_QUERY_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    rows = response.json()
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("Socrata returned an unexpected response; expected a list of row objects")
    return rows


@dlt.source
def opendata_payroll_source(
    domain: str = SOCRATA_DOMAIN,
    dataset_id: str = SOCRATA_DATASET_ID,
    page_size: int = SOCRATA_PAGE_SIZE,
    app_token: str | None = None,
):
    """
    Define the NYC Open Data Citywide Payroll Data source.

    The source uses the SODA3 query API and fetches rows page by page so the
    complete dataset does not need to be held in memory.
    """
    if page_size < 1:
        raise ValueError("page_size must be greater than zero")

    endpoint = f"https://{domain}/api/v3/views/{dataset_id}/query.json"
    token = app_token or os.getenv("NYC_OPEN_DATA_APP_TOKEN")

    @dlt.resource(name="citywide_payroll")
    def citywide_payroll():
        page_number = 1
        while True:
            rows = _query_socrata_page(endpoint, page_number, page_size, token)
            if not rows:
                return

            yield from rows
            if len(rows) < page_size:
                return
            page_number += 1

    return citywide_payroll()
