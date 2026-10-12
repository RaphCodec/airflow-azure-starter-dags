from include.opendata import civil_service


def test_create_resources_uses_all_civil_service_endpoints(monkeypatch):
    calls = []

    def fake_make_resource(**kwargs):
        calls.append(kwargs)
        return lambda: kwargs["name"]

    monkeypatch.setattr(civil_service, "make_resource", fake_make_resource)

    resources = civil_service.create_resources("https://example.test", {"x-api-key": "test"})

    assert resources == [
        "civil_service_list_active",
        "civil_service_list_terminated",
        "civil_service_titles",
    ]
    assert [call["endpoint"] for call in calls] == [
        "vx8i-nprf/query.json",
        "qu8g-sxqf/query.json",
        "nzjr-3966/query.json",
    ]
    assert all(call["url"] == "https://example.test" for call in calls)
    assert all(call["headers"] == {"x-api-key": "test"} for call in calls)


def test_create_source_wraps_all_resources():
    source = civil_service.create_source("https://example.test", {})

    assert source.name == "civil_service"
    assert set(source.selected_resources) == {
        "civil_service_list_active",
        "civil_service_list_terminated",
        "civil_service_titles",
    }


def test_create_source_defers_client_config():
    calls = []

    source = civil_service.create_source(client_config=lambda: calls.append("called"))

    assert calls == []
    assert set(source.selected_resources) == {
        "civil_service_list_active",
        "civil_service_list_terminated",
        "civil_service_titles",
    }


def test_run_pipeline_preserves_destination_and_credentials(monkeypatch):
    run_args = {}

    class FakePipeline:
        def run(self, **kwargs):
            run_args.update(kwargs)
            return "load-info"

    pipeline_args = {}

    def fake_pipeline(**kwargs):
        pipeline_args.update(kwargs)
        return FakePipeline()

    monkeypatch.setattr(civil_service.dlt, "pipeline", fake_pipeline)
    monkeypatch.setattr(civil_service, "create_resources", lambda **kwargs: ["resource"])

    result = civil_service.run_pipeline("https://example.test", {}, "token")

    assert result == "load-info"
    assert pipeline_args == {
        "pipeline_name": "nyc_open_data",
        "destination": "motherduck",
        "dataset_name": "civil_service",
    }
    assert run_args == {
        "data": ["resource"],
        "credentials": "md:OpenData?motherduck_token=token",
    }
