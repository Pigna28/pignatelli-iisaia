import json
import sqlite3
from dataclasses import replace

import pytest
from pydantic import ValidationError

from backend.db import connect, initialize
from scripts import seed_measurements_legacy as seed_demo


def demo_chip(client, board):
    return next(chip for chip in client.get("/chips").json() if board in chip["board"])


def test_demo_scenarios_through_api(client, settings):
    seed_demo.seed(settings)
    assert client.get("/summary").json() == {
        "chips": 8,
        "tests": 48,
        "passed": 38,
        "failed": 10,
        "in_progress": 0,
    }
    chips = client.get("/chips").json()
    assert chips[0]["board"] == "01 / EVK-A / Referencia"
    assert sum(chip["part_number"] == "DEMO-RF2401" for chip in chips) == 6

    for board, failed_macro in [("Falla Tx", "Tx"), ("Falla Rx", "Rx"), ("Falla PLL", "PLL")]:
        chip = demo_chip(client, board)
        for macro in ("Tx", "Rx", "PLL"):
            url = f"/chips/{chip['id']}/macros/{macro}/tests"
            assert len(client.get(url).json()) == 3
            assert len(client.get(url + "?passed=false").json()) == (
                3 if macro == failed_macro else 0
            )
            assert len(client.get(url + "?passed=true").json()) == (
                0 if macro == failed_macro else 3
            )

    repeat = demo_chip(client, "Reensayo")
    history = client.get(f"/chips/{repeat['id']}/macros/Tx/tests").json()
    assert [test["passed"] for test in history] == [True, False]
    assert history[0]["metric"] == history[1]["metric"] == "Ganancia"
    assert history[0]["measured_at"] > history[1]["measured_at"]

    for board, counts in [("Pendiente", [0, 0, 0]), ("Parcial", [3, 0, 0])]:
        chip = demo_chip(client, board)
        for macro, count in zip(("Tx", "Rx", "PLL"), counts):
            response = client.get(f"/chips/{chip['id']}/macros/{macro}/tests")
            assert response.status_code == 200 and len(response.json()) == count

    unknown = demo_chip(client, "Sin fechas")
    assert "assembled_at" not in unknown
    for macro in ("Tx", "Rx", "PLL"):
        test = client.get(f"/chips/{unknown['id']}/macros/{macro}/tests").json()[0]
        assert "measured_at" not in test
    reference = demo_chip(client, "Referencia")
    tests = client.get(f"/chips/{reference['id']}/macros/Tx/tests").json()
    assert tests[-1]["measured_at"] == "2026-10-08T12:00:00Z"

    events = client.get("/audit?limit=100").json()
    assert len(events) == 56
    assert all(event["snapshot"]["synthetic"] is True for event in events)
    assert all(event["snapshot"]["dataset_id"] == "exposicion-v1" for event in events)
    with connect(settings.database) as db:
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []


def test_append_preserves_existing_data_and_does_not_repeat(client, chip, measurement, settings):
    original = client.post(f"/chips/{chip['id']}/macros/Tx/tests", json=measurement).json()
    seed_demo.seed(settings)
    assert client.get("/chips").json() == [chip]
    seed_demo.seed(settings, append=True)
    summary = client.get("/summary").json()
    assert summary == {"chips": 9, "tests": 49, "passed": 39, "failed": 10, "in_progress": 0}
    # Incluso después de borrar un elemento, repetir la carga no repone ni duplica datos.
    pending = demo_chip(client, "Pendiente")
    assert client.delete(f"/chips/{pending['id']}").status_code == 204
    seed_demo.seed(settings, append=True)
    assert client.get("/summary").json() == {**summary, "chips": 8}
    assert chip in client.get("/chips").json()
    assert client.get(f"/chips/{chip['id']}/macros/Tx/tests").json() == [original]


def test_demo_audit_failure_rolls_back_whole_dataset(settings):
    initialize(settings.database)
    with connect(settings.database) as db:
        db.execute(
            "CREATE TRIGGER fail_seed BEFORE INSERT ON audit WHEN NEW.resource='test' "
            "BEGIN SELECT RAISE(ABORT, 'audit unavailable'); END"
        )
    with pytest.raises(sqlite3.IntegrityError):
        seed_demo.seed(settings)
    with connect(settings.database) as db:
        for table in ("chips", "tests", "audit"):
            assert db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0
        db.execute("DROP TRIGGER fail_seed")
    seed_demo.seed(settings)
    with connect(settings.database) as db:
        assert db.execute("SELECT COUNT(*) FROM chips").fetchone()[0] == 8


def test_invalid_dataset_is_rejected_before_database_changes(settings, tmp_path, monkeypatch):
    payload = json.loads(seed_demo.DATASET_PATH.read_text(encoding="utf-8"))
    payload["samples"][-1]["tests"]["Tx"][0]["passed"] = "true"
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(seed_demo, "DATASET_PATH", invalid)
    with pytest.raises(ValidationError):
        seed_demo.seed(settings)
    assert not settings.database.exists()


def test_seed_rejects_production(settings):
    with pytest.raises(SystemExit):
        seed_demo.seed(replace(settings, environment="production"))
    assert not settings.database.exists()


def test_demo_cli_uses_alternative_database(settings, tmp_path, monkeypatch):
    destination = tmp_path / "exposicion.db"
    monkeypatch.setattr(seed_demo, "load_settings", lambda: settings)
    monkeypatch.setattr("sys.argv", ["seed_demo", "--database", str(destination)])
    seed_demo.main()
    assert destination.exists() and not settings.database.exists()
