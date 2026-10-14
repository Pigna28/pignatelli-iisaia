from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate

ROOT = Path(__file__).resolve().parent.parent


def test_openapi_valid_and_served(client):
    spec = yaml.safe_load((ROOT / "openapi.yaml").read_text("utf-8"))
    validate(spec)
    assert client.get("/openapi.json").json() == spec
    original = yaml.safe_load((ROOT / "opeanapi.yaml").read_text("utf-8"))
    for path, methods in original["paths"].items():
        for method, operation in methods.items():
            assert spec["paths"][path][method]["operationId"] == operation["operationId"]
            assert set(operation["responses"]) <= set(spec["paths"][path][method]["responses"])


def test_responses_match_contract(client, chip, measurement):
    spec = client.get("/openapi.json").json()
    base = f"/chips/{chip['id']}/macros/Tx/tests"
    test = client.post(base, json=measurement)
    cases = [
        ("/chips", "get", client.get("/chips")),
        (
            "/chips",
            "post",
            client.post(
                "/chips", json={"part_number": "x", "board": "b", "assembled_at": "2026-09-30"}
            ),
        ),
        ("/chips/{chipId}/macros/{macro}/tests", "post", test),
        ("/chips/{chipId}/macros/{macro}/tests", "get", client.get(base)),
        ("/chips/{chipId}/macros/{macro}/tests", "get", client.get(base + "?passed=bad")),
        ("/summary", "get", client.get("/summary")),
        ("/session", "get", client.get("/session")),
        ("/audit", "get", client.get("/audit")),
        ("/health", "get", client.get("/health")),
    ]
    for path, method, response in cases:
        schema = spec["paths"][path][method]["responses"][str(response.status_code)]["content"][
            "application/json"
        ]["schema"]
        validator = Draft202012Validator(
            {**schema, "components": spec["components"]}, format_checker=FormatChecker()
        )
        validator.validate(response.json())


def test_thread_responses_match_contract(client, chip):
    spec = client.get("/openapi.json").json()
    base = f"/chips/{chip['id']}/macros/Tx/threads"
    created = client.post(base, json={"title": "Contract thread"})
    path = base + "/" + str(created.json()["id"])
    step = client.post(path + "/steps", json={"title": "First step"})
    step_path = path + "/steps/" + str(step.json()["id"])
    link = client.post(
        step_path + "/attachments/links", json={"name": "Reference", "url": "https://example.org"}
    )
    file = client.post(
        step_path + "/attachments/files", content=b"hello", headers={"X-Filename": "data.txt"}
    )
    template = "/chips/{chipId}/macros/{macro}/threads"
    cases = [
        (template, "post", created),
        (template, "get", client.get(base)),
        ("/threads", "get", client.get("/threads")),
        (template + "/{threadId}", "get", client.get(path)),
        (template + "/{threadId}/steps", "post", step),
        (
            template + "/{threadId}/steps/{stepId}",
            "put",
            client.put(step_path, json={"title": "Updated", "status": "passed"}),
        ),
        (template + "/{threadId}/steps/{stepId}/attachments/links", "post", link),
        (template + "/{threadId}/steps/{stepId}/attachments/files", "post", file),
    ]
    for route, method, response in cases:
        schema = spec["paths"][route][method]["responses"][str(response.status_code)]["content"][
            "application/json"
        ]["schema"]
        Draft202012Validator(
            {**schema, "components": spec["components"]}, format_checker=FormatChecker()
        ).validate(response.json())
