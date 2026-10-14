import json

import pytest

from backend.db import connect
from scripts import seed_demo


def test_demo_api_and_evidence(client, settings):
    seed_demo.seed(settings)
    assert client.get("/summary").json() == {
        "chips": 3,
        "tests": 12,
        "passed": 4,
        "failed": 4,
        "in_progress": 4,
    }
    chips = client.get("/chips").json()
    assert {chip["part_number"] for chip in chips} == {"A0", "A1", "A2"}
    evidence_count = 0
    for thread in client.get("/threads").json():
        base = f"/chips/{thread['chip_id']}/macros/{thread['macro']}/threads/{thread['id']}"
        detail = client.get(base).json()
        assert len(detail["steps"]) == 3
        for step in detail["steps"]:
            for attachment in step["attachments"]:
                response = client.get(
                    f"{base}/steps/{step['id']}/attachments/{attachment['id']}/download"
                )
                assert response.status_code == 200
                assert "DEMO SINTETICA" in response.text
                evidence_count += 1
    assert evidence_count == 9
    with connect(settings.database) as db:
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert (
            db.execute(
                "SELECT COUNT(*) FROM audit WHERE actor=?", (seed_demo.CAMPAIGN,)
            ).fetchone()[0]
            == 60
        )
        assert all(
            json.loads(row[0])["synthetic"] for row in db.execute("SELECT snapshot FROM audit")
        )


def test_demo_preserves_existing_data_and_later_edits(client, chip, settings):
    seed_demo.seed(settings)
    with connect(settings.database) as db:
        original = dict(db.execute("SELECT * FROM chips WHERE id=?", (chip["id"],)).fetchone())
        db.execute("UPDATE steps SET notes='Edición manual' WHERE id=(SELECT MIN(id) FROM steps)")
        db.execute("DELETE FROM chips WHERE part_number='A2'")
        count = db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
    seed_demo.seed(settings)
    with connect(settings.database) as db:
        assert (
            dict(db.execute("SELECT * FROM chips WHERE id=?", (chip["id"],)).fetchone()) == original
        )
        assert (
            db.execute("SELECT notes FROM steps ORDER BY id LIMIT 1").fetchone()[0]
            == "Edición manual"
        )
        assert db.execute("SELECT COUNT(*) FROM chips WHERE part_number='A2'").fetchone()[0] == 0
        assert db.execute("SELECT COUNT(*) FROM audit").fetchone()[0] == count


def test_demo_rolls_back_and_can_retry(settings, monkeypatch):
    audit = seed_demo.audit
    calls = 0

    def failing_audit(*args):
        nonlocal calls
        calls += 1
        if calls == 5:
            raise RuntimeError("Simular fallo de auditoría")
        return audit(*args)

    monkeypatch.setattr(seed_demo, "audit", failing_audit)
    with pytest.raises(RuntimeError, match="auditoría"):
        seed_demo.seed(settings)
    with connect(settings.database) as db:
        for table in ("chips", "threads", "steps", "attachments", "audit"):
            assert db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0
    monkeypatch.setattr(seed_demo, "audit", audit)
    seed_demo.seed(settings)
    with connect(settings.database) as db:
        assert db.execute("SELECT COUNT(*) FROM threads").fetchone()[0] == 12
