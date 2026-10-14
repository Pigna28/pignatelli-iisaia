import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.db import connect
from backend.main import create_app


def path(chip, macro="Tx"):
    return f"/chips/{chip['id']}/macros/{macro}/tests"


def test_complete_flow_and_cascade(client, chip, measurement, settings):
    assert client.get("/chips").json() == [chip]
    for macro in ("Tx", "Rx", "PLL"):
        result = client.post(path(chip, macro), json=measurement)
        assert result.status_code == 201
        assert result.json()["macro"] == macro
    assert client.get("/summary").json() == {
        "chips": 1,
        "tests": 3,
        "passed": 3,
        "failed": 0,
        "in_progress": 0,
    }
    assert client.delete(f"/chips/{chip['id']}").status_code == 204
    assert client.get("/chips").json() == []
    assert client.get(path(chip)).status_code == 404
    with connect(settings.database) as db:
        assert db.execute("SELECT COUNT(*) FROM tests").fetchone()[0] == 0
    log = client.get("/audit").json()
    assert len(log) == 5
    assert len(log[0]["snapshot"]["tests"]) == 3
    assert client.delete(f"/chips/{chip['id']}").status_code == 404


def test_filter_and_hierarchy(client, chip, measurement):
    created = client.post(path(chip), json=measurement).json()
    client.post(path(chip), json={**measurement, "passed": False})
    assert len(client.get(path(chip)).json()) == 2
    assert len(client.get(path(chip) + "?passed=true").json()) == 1
    assert client.get(path(chip) + "?passed=false").json()[0]["passed"] is False
    other = client.post("/chips", json={"part_number": "IC-001", "board": "EVK-B"}).json()
    for wrong in [path(chip, "Rx"), path(other)]:
        assert client.delete(f"{wrong}/{created['id']}").status_code == 404
    result = client.delete(f"{path(chip)}/{created['id']}")
    assert result.status_code == 204 and result.content == b""
    assert client.delete(f"{path(chip)}/{created['id']}").status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"part_number": "x"},
        {"part_number": " ", "board": "b"},
        {"part_number": 1, "board": "b"},
        {"part_number": "a", "board": "b", "id": 1},
        {"part_number": "a", "board": "b", "assembled_at": "2026-02-30"},
        {"part_number": "a", "board": "b", "assembled_at": None},
        {"part_number": "a", "board": "b", "assembled_at": 0},
        {"part_number": "a" * 121, "board": "b"},
    ],
)
def test_invalid_chips(client, payload):
    result = client.post("/chips", json=payload)
    assert result.status_code == 400 and "error" in result.json()
    assert client.get("/chips").json() == []


@pytest.mark.parametrize(
    "change",
    [
        {"passed": "false"},
        {"passed": 1},
        {"measured_value": "12"},
        {"measured_value": True},
        {"metric": " "},
        {"unit": None},
        {"chip_id": 1},
        {"macro": "Rx"},
        {"measured_at": "2026-09-30T10:00:00"},
        {"measured_at": None},
        {"measured_at": 1234},
    ],
)
def test_invalid_measurements(client, chip, measurement, change):
    assert client.post(path(chip), json={**measurement, **change}).status_code == 400
    assert client.get(path(chip)).json() == []


@pytest.mark.parametrize("suffix", ["?passed=1", "?passed=yes", "?passed=False"])
def test_strict_query(client, chip, suffix):
    assert client.get(path(chip) + suffix).status_code == 400


def test_invalid_paths_and_json(client, chip):
    for url in ["/chips/0/macros/Tx/tests", "/chips/abc/macros/Tx/tests", path(chip, "tx")]:
        assert client.get(url).status_code == 400
    assert client.get("/chips/999/macros/PLL/tests").status_code == 404
    assert (
        client.post(
            "/chips", content="{broken", headers={"Content-Type": "application/json"}
        ).status_code
        == 400
    )
    assert (
        client.post(
            path(chip),
            content='{"metric":"x","unit":"V","passed":true,"measured_value":NaN}',
            headers={"Content-Type": "application/json"},
        ).status_code
        == 400
    )


def test_dates_and_persistence(client, chip, measurement, settings):
    created = client.post(
        path(chip), json={**measurement, "measured_at": "2026-09-30T10:00:00-03:00"}
    ).json()
    assert created["measured_at"] == "2026-09-30T13:00:00Z"
    with TestClient(create_app(settings), base_url=settings.base_url) as restarted:
        assert restarted.get(path(chip)).json() == [created]


def test_transaction_rollback(client, chip, measurement, settings):
    with connect(settings.database) as db:
        db.execute(
            "CREATE TRIGGER fail_audit BEFORE INSERT ON audit BEGIN SELECT RAISE(ABORT, 'test'); END"
        )
    with pytest.raises(sqlite3.IntegrityError):
        client.post(path(chip), json=measurement)
    assert client.get(path(chip)).json() == []


def test_audit_pagination(client, chip, measurement):
    for _ in range(3):
        client.post(path(chip), json=measurement)
    first = client.get("/audit?limit=2").json()
    second = client.get(f"/audit?limit=2&before={first[-1]['id']}").json()
    assert len({x["id"] for x in first + second}) == 4
    assert client.get("/audit?limit=101").status_code == 400
