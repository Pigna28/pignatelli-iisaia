"""SQLite: una conexión por request, FK activas y auditoría en la misma transacción."""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

SCHEMA = """
BEGIN IMMEDIATE;
CREATE TABLE chips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_number TEXT NOT NULL,
    board TEXT NOT NULL,
    assembled_at TEXT
);
CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chip_id INTEGER NOT NULL REFERENCES chips(id) ON DELETE CASCADE,
    macro TEXT NOT NULL CHECK (macro IN ('Tx','Rx','PLL')),
    metric TEXT NOT NULL,
    measured_value REAL NOT NULL,
    unit TEXT NOT NULL,
    passed INTEGER NOT NULL CHECK (passed IN (0,1)),
    measured_at TEXT
);
CREATE INDEX ix_tests_chip_macro_passed ON tests(chip_id, macro, passed);
CREATE TABLE audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    resource_id INTEGER NOT NULL,
    snapshot TEXT NOT NULL
);
PRAGMA user_version = 1;
COMMIT;
"""


@contextmanager
def connect(path):
    # FastAPI puede ejecutar el dependency y el endpoint en workers diferentes.
    # La conexión sigue siendo exclusiva de este request, nunca global.
    connection = sqlite3.connect(str(path), timeout=10, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.execute("PRAGMA journal_mode = WAL")
        version = db.execute("PRAGMA user_version").fetchone()[0]
        if version == 0:
            db.executescript(SCHEMA)
        elif version != 1:
            raise RuntimeError(f"Versión de base no soportada: {version}")


def get_db(request):
    # Se utiliza mediante wrapper tipado en routes.py.
    with connect(request.app.state.settings.database) as db:
        yield db


def audit(db, actor, action, resource, resource_id, snapshot):
    db.execute(
        "INSERT INTO audit(occurred_at,actor,action,resource,resource_id,snapshot) "
        "VALUES (?,?,?,?,?,?)",
        (
            datetime.now(timezone.utc).isoformat(),
            actor,
            action,
            resource,
            resource_id,
            json.dumps(snapshot, ensure_ascii=False),
        ),
    )


def record(row):
    data = {key: value for key, value in dict(row).items() if value is not None}
    if "passed" in data:
        data["passed"] = bool(data["passed"])
    return data
