from collections.abc import Callable

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from structlog import get_logger

log = get_logger(__name__)


def create_client(
    url: str,
    headers: dict,
    base_page: int = 1,
    max_page: int = 100_000,
) -> RESTClient:
    log.info("Creating REST Client")
    return RESTClient(
        base_url=url,
        headers=headers,
        paginator=PageNumberPaginator(
            base_page=base_page,
            page_body_path="page.pageNumber",
            total_path=None,
            stop_after_empty_page=True,
            maximum_page=max_page,
        ),
    )


def make_resource(
    name: str,
    url: str | None,
    endpoint: str,
    headers: dict | None,
    query: str = "SELECT *",
    page_size: int = 10_000,
    client_config: Callable[[], tuple[str, dict]] | None = None,
):
    @dlt.resource(name=name, write_disposition="replace", parallelized=True)
    def resource():
        resource_url, resource_headers = client_config() if client_config else (url, headers)
        client = create_client(
            url=resource_url,
            headers=resource_headers,
        )

        page_num = 1

        for page in client.paginate(
            endpoint,
            method="POST",
            json={
                "query": query,
                "page": {
                    "pageNumber": 1,
                    "pageSize": page_size,
                },
            },
        ):
            log.info("Yeilding page for:", name=name, endpoint=endpoint, page_num=page_num)
            yield page
            page_num += 1

    return resource


def create_pipeline(pipeline_name: str = "nyc_open_data"):
    return dlt.pipeline(
        pipeline_name=pipeline_name,
        destination="motherduck",
        dataset_name="civil_service",
    )


def create_resources(
    url: str | None = None,
    headers: dict | None = None,
    client_config: Callable[[], tuple[str, dict]] | None = None,
):
    active_list = make_resource(
        url=url,
        name="civil_service_list_active",
        endpoint="vx8i-nprf/query.json",
        headers=headers,
        client_config=client_config,
    )
    terminated_list = make_resource(
        url=url,
        name="civil_service_list_terminated",
        endpoint="qu8g-sxqf/query.json",
        headers=headers,
        client_config=client_config,
    )

    titles = make_resource(
        url=url,
        name="civil_service_titles",
        endpoint="nzjr-3966/query.json",
        headers=headers,
        client_config=client_config,
    )

    return [active_list(), terminated_list(), titles()]


def create_source(
    url: str | None = None,
    headers: dict | None = None,
    client_config: Callable[[], tuple[str, dict]] | None = None,
):
    @dlt.source(name="civil_service")
    def civil_service_source():
        return create_resources(url=url, headers=headers, client_config=client_config)

    return civil_service_source()


def run_pipeline(url: str, headers: dict, md_token: str):
    pipeline = create_pipeline()

    return pipeline.run(
        data=create_resources(url=url, headers=headers),
        credentials=f"md:OpenData?motherduck_token={md_token}",
    )
