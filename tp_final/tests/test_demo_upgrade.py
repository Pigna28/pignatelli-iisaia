"""Regresión: la entrega debe mostrar hilos pendientes sin perder la demo v1."""

import pytest
from fastapi.testclient import TestClient

from backend.db import SCHEMA, connect
from backend.main import create_app
from scripts import seed_demo, seed_measurements_legacy


def test_v1_demo_migration_and_current_campaign_preserve_all_measurements(settings):
    with connect(settings.database) as db:
        db.executescript(SCHEMA)
        for sample in seed_measurements_legacy.load_dataset().samples:
            chip = sample.chip
            chip_id = db.execute(
                "INSERT INTO chips(part_number,board,assembled_at) VALUES (?,?,?)",
                (
                    chip.part_number,
                    chip.board,
                    str(chip.assembled_at) if chip.assembled_at else None,
                ),
            ).lastrowid
            for macro, measurements in sample.tests.items():
                for measurement in measurements:
                    db.execute(
                        "INSERT INTO tests(chip_id,macro,metric,measured_value,unit,passed,measured_at) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (
                            chip_id,
                            macro,
                            measurement.metric,
                            measurement.measured_value,
                            measurement.unit,
                            measurement.passed,
                            measurement.measured_at.isoformat()
                            if measurement.measured_at
                            else None,
                        ),
                    )
        before = [tuple(row) for row in db.execute("SELECT * FROM tests ORDER BY id")]
    seed_demo.seed(settings)
    seed_demo.seed(settings)
    with TestClient(create_app(settings), base_url=settings.base_url) as client:
        assert client.get("/openapi.json").json()["info"]["version"] == "2.0.0"
        assert client.get("/summary").json() == {
            "chips": 11,
            "tests": 60,
            "passed": 42,
            "failed": 14,
            "in_progress": 4,
        }
        assert len(client.get("/threads?status=in_progress").json()) == 4
    with connect(settings.database) as db:
        assert [tuple(row) for row in db.execute("SELECT * FROM tests ORDER BY id")] == before
        assert (
            db.execute("SELECT COUNT(*) FROM threads WHERE legacy_test_id IS NOT NULL").fetchone()[
                0
            ]
            == 48
        )
        assert db.execute("SELECT COUNT(*) FROM steps").fetchone()[0] == 84
        assert db.execute("SELECT COUNT(*) FROM attachments").fetchone()[0] == 9
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("append", [False, True])
def test_current_demo_cli_can_prepare_a_separate_database(settings, tmp_path, monkeypatch, append):
    destination = tmp_path / "demo-v2.db"
    monkeypatch.setattr(seed_demo, "load_settings", lambda: settings)
    argv = ["seed_demo", "--database", str(destination)]
    if append:
        argv.append("--append")
    monkeypatch.setattr("sys.argv", argv)
    seed_demo.main()
    seed_demo.main()
    assert destination.exists() and not settings.database.exists()
    with connect(destination) as db:
        assert (
            db.execute(
                "SELECT COUNT(*) FROM thread_overview WHERE status='in_progress'"
            ).fetchone()[0]
            == 4
        )
        assert db.execute("SELECT COUNT(*) FROM threads").fetchone()[0] == 12
