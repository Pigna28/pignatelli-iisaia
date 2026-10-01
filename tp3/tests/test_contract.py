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
