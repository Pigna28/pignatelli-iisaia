import sqlite3
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from backend.db import SCHEMA, connect, initialize
from backend.main import create_app
from scripts.backup import backup
from tests.test_auth import auth_app


@pytest.fixture
def thread(client, chip):
    base = f"/chips/{chip['id']}/macros/Tx/threads"
    response = client.post(base, json={"title": "Caracterización RF", "description": "Campaña 1"})
    assert response.status_code == 201
    return base + "/" + str(response.json()["id"])


@pytest.fixture
def step(client, thread):
    response = client.post(thread + "/steps", json={"title": "Alimentación"})
    assert response.status_code == 201
    return thread + "/steps/" + str(response.json()["id"])


def test_thread_states_and_global_navigation(client, thread, step):
    assert client.get(thread).json()["status"] == "in_progress"
    assert client.get("/summary").json()["in_progress"] == 1
    assert len(client.get("/threads?status=in_progress").json()) == 1
    result = client.put(step, json={"title": "Alimentación", "status": "passed"})
    assert result.status_code == 200
    assert client.get(thread).json()["status"] == "passed"
    assert client.get("/threads?status=in_progress").json() == []
    second = client.post(
        thread + "/steps",
        json={
            "title": "Ganancia",
            "status": "failed",
            "metric": "gain",
            "measured_value": -2,
            "unit": "dB",
        },
    ).json()
    assert client.get(thread).json()["status"] == "failed"
    assert [s["title"] for s in client.get(thread).json()["steps"]] == ["Alimentación", "Ganancia"]
    assert client.get("/summary").json() == {
        "chips": 1,
        "tests": 1,
        "passed": 0,
        "failed": 1,
        "in_progress": 0,
    }
    assert client.delete(thread + "/steps/" + str(second["id"])).status_code == 204
    assert client.get(thread).json()["status"] == "passed"
    assert client.delete(step).status_code == 204
    assert client.get(thread).json()["status"] == "in_progress"
    assert any(e["action"] == "update" for e in client.get("/audit").json())


def test_upload_link_download_restart_and_cascade(client, thread, step, settings):
    base = step + "/attachments"
    content = b"%PDF-1.7\nlab-evidence"
    result = client.post(
        base + "/files", content=content, headers={"X-Filename": quote("medición.pdf")}
    )
    assert result.status_code == 201
    attachment = result.json()
    assert attachment["size"] == len(content) and "content" not in attachment
    download = base + f"/{attachment['id']}/download"
    response = client.get(download)
    assert response.content == content and response.headers["content-disposition"].startswith(
        "attachment;"
    )
    assert response.headers["x-content-type-options"] == "nosniff"
    assert (
        client.post(
            base + "/links", json={"name": "Presentación", "url": "https://example.org/slides"}
        ).status_code
        == 201
    )
    with TestClient(create_app(settings), base_url=settings.base_url) as restarted:
        assert restarted.get(download).content == content
        assert len(restarted.get(thread).json()["steps"][0]["attachments"]) == 2
    with connect(settings.database) as db:
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    assert client.delete(thread).status_code == 204
    with connect(settings.database) as db:
        assert db.execute("SELECT COUNT(*) FROM attachments").fetchone()[0] == 0
    snapshot = client.get("/audit").json()[0]["snapshot"]
    assert len(snapshot["steps"][0]["attachments"]) == 2
    assert "content" not in str(snapshot)


@pytest.mark.parametrize(
    "name", ["../secret.txt", "bad.exe", "x.html", "x.svg", "a\\b.pdf", "bad\n.pdf"]
)
def test_invalid_upload_names(client, step, name):
    assert (
        client.post(
            step + "/attachments/files", content=b"x", headers={"X-Filename": quote(name)}
        ).status_code
        == 400
    )


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,test",
        "file:///a",
        "https://user:pass@example.org",
        "https://example.org/a b",
    ],
)
def test_invalid_links(client, step, url):
    assert (
        client.post(step + "/attachments/links", json={"name": "Bad", "url": url}).status_code
        == 400
    )


def test_file_limits_and_hierarchy(client, thread, step, monkeypatch):
    base = step + "/attachments"
    monkeypatch.setattr("backend.attachments.MAX_BYTES", 10)
    assert (
        client.post(
            base + "/files", content=b"12345678901", headers={"X-Filename": "x.txt"}
        ).status_code
        == 413
    )
    assert (
        client.post(base + "/files", content=b"", headers={"X-Filename": "x.txt"}).status_code
        == 400
    )
    item = client.post(base + "/files", content=b"12345", headers={"X-Filename": "x.txt"}).json()
    wrong = base.replace("/macros/Tx/", "/macros/Rx/")
    assert client.get(wrong + f"/{item['id']}/download").status_code == 404
    assert client.delete(wrong + f"/{item['id']}").status_code == 404
    monkeypatch.setattr("backend.attachments.MAX_ATTACHMENTS", 1)
    assert (
        client.post(
            base + "/links", json={"name": "More", "url": "https://example.org"}
        ).status_code
        == 400
    )
    assert client.delete(base + f"/{item['id']}").status_code == 204
    assert client.get(base + f"/{item['id']}/download").status_code == 404
    assert (
        client.put(step.replace("/threads/", "/threads/999/"), json={"title": "X"}).status_code
        == 404
    )


@pytest.mark.parametrize(
    "body",
    [
        {"title": ""},
        {"title": "X", "status": "other"},
        {"title": "X", "metric": "gain"},
        {"title": "X", "metric": "gain", "measured_value": True, "unit": "dB"},
        {"title": "X", "measured_at": "2026-10-13T12:00:00"},
        {"title": "X", "thread_id": 2},
    ],
)
def test_invalid_steps(client, thread, body):
    assert client.post(thread + "/steps", json=body).status_code == 400


def test_migration_v1_preserves_data_and_is_repeatable(settings):
    with connect(settings.database) as db:
        db.executescript(SCHEMA)
        db.execute("INSERT INTO chips(id,part_number,board) VALUES(7,'LEGACY','EVK')")
        db.execute(
            "INSERT INTO tests(id,chip_id,macro,metric,measured_value,unit,passed,measured_at) "
            "VALUES(11,7,'PLL','noise',-112.5,'dBc/Hz',0,'2026-09-30T12:00:00Z')"
        )
    initialize(settings.database)
    initialize(settings.database)
    with TestClient(create_app(settings), base_url=settings.base_url) as client:
        thread = client.get("/threads").json()[0]
        assert thread["status"] == "failed" and thread["step_count"] == 1
        result = client.get(f"/chips/7/macros/PLL/threads/{thread['id']}").json()
        assert result["steps"][0]["measured_value"] == -112.5
        assert result["steps"][0]["measured_at"] == "2026-09-30T12:00:00Z"
        assert len(client.get("/threads").json()) == 1
        assert client.get("/chips/7/macros/PLL/tests").json()[0]["id"] == 11


def test_new_resources_permission_csrf(client, step, settings):
    app = auth_app(settings, writer=False)
    with TestClient(app, base_url=settings.base_url) as reader:
        assert reader.get("/threads").status_code == 401
        reader.get("/callback")
        reader.headers["X-CSRF-Token"] = reader.get("/session").json()["csrf_token"]
        assert reader.get("/threads").status_code == 200
        assert reader.put(step, json={"title": "bad"}).status_code == 403
        assert (
            reader.post(
                step + "/attachments/files", content=b"a", headers={"X-Filename": "x.txt"}
            ).status_code
            == 403
        )
    client.headers.pop("X-CSRF-Token")
    assert (
        client.post(
            step + "/attachments/links", json={"name": "X", "url": "https://example.org"}
        ).status_code
        == 403
    )


def test_upload_rollback_on_audit_failure(client, step, settings):
    with connect(settings.database) as db:
        db.execute(
            "CREATE TRIGGER fail_attachment_audit BEFORE INSERT ON audit BEGIN SELECT RAISE(ABORT, 'test'); END"
        )
    with pytest.raises(sqlite3.IntegrityError):
        client.post(step + "/attachments/files", content=b"a", headers={"X-Filename": "x.txt"})
    with connect(settings.database) as db:
        assert db.execute("SELECT COUNT(*) FROM attachments").fetchone()[0] == 0


def test_backup_preserves_uploaded_bytes(client, step, settings, tmp_path):
    item = client.post(
        step + "/attachments/files",
        content=b"backup-evidence",
        headers={"X-Filename": "result.txt"},
    ).json()
    target = tmp_path / "copy.db"
    backup(settings.database, target)
    with connect(target) as db:
        assert (
            db.execute("SELECT content FROM attachments WHERE id=?", (item["id"],)).fetchone()[0]
            == b"backup-evidence"
        )
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []


def test_failed_migration_rolls_back(settings, monkeypatch):
    from backend import migrations

    with connect(settings.database) as db:
        db.executescript(SCHEMA)
        db.execute("INSERT INTO chips(part_number,board) VALUES('kept','EVK')")
    monkeypatch.setattr(migrations, "V2", migrations.V2 + "\nINVALID SQL;")
    with pytest.raises(sqlite3.OperationalError):
        initialize(settings.database)
    with connect(settings.database) as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == 1
        assert db.execute("SELECT part_number FROM chips").fetchone()[0] == "kept"
        assert db.execute("SELECT name FROM sqlite_master WHERE name='threads'").fetchone() is None


def test_step_and_attachment_cannot_cross_threads(client, thread, step, settings):
    base = thread.rsplit("/", 1)[0]
    other = client.post(base, json={"title": "Other thread"}).json()
    wrong_step = base + f"/{other['id']}/steps/" + step.rsplit("/", 1)[1]
    assert client.put(wrong_step, json={"title": "Wrong target"}).status_code == 404
    assert client.delete(wrong_step).status_code == 404
    attachment = client.post(
        step + "/attachments/files", content=b"test", headers={"X-Filename": "a.txt"}
    ).json()
    suffix = f"/attachments/{attachment['id']}/download"
    assert client.get(wrong_step + suffix).status_code == 404
    with TestClient(auth_app(settings, writer=False), base_url=settings.base_url) as reader:
        assert reader.get(step + suffix).status_code == 401
        reader.get("/callback")
        assert reader.get(step + suffix).content == b"test"
