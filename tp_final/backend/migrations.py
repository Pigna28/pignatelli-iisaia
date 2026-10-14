"""Extensión v2: hilos, pasos y evidencias sin perder las mediciones v1."""

V2 = """
CREATE TABLE threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chip_id INTEGER NOT NULL REFERENCES chips(id) ON DELETE CASCADE,
    macro TEXT NOT NULL CHECK(macro IN ('Tx','Rx','PLL')),
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    legacy_test_id INTEGER UNIQUE REFERENCES tests(id) ON DELETE CASCADE
);
CREATE INDEX ix_threads_chip_macro ON threads(chip_id,macro);
CREATE TABLE steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL CHECK(status IN ('in_progress','passed','failed')),
    metric TEXT,
    measured_value REAL,
    unit TEXT,
    measured_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX ix_steps_thread ON steps(thread_id,id);
CREATE TABLE attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_id INTEGER NOT NULL REFERENCES steps(id) ON DELETE CASCADE,
    kind TEXT NOT NULL CHECK(kind IN ('file','link')),
    name TEXT NOT NULL,
    url TEXT,
    size INTEGER NOT NULL DEFAULT 0,
    content BLOB,
    created_at TEXT NOT NULL
);
CREATE INDEX ix_attachments_step ON attachments(step_id);
CREATE VIEW thread_overview AS
SELECT t.*, c.part_number, c.board,
    (SELECT COUNT(*) FROM steps s WHERE s.thread_id=t.id) step_count,
    CASE
      WHEN EXISTS(SELECT 1 FROM steps s WHERE s.thread_id=t.id AND s.status='failed')
        THEN 'failed'
      WHEN NOT EXISTS(SELECT 1 FROM steps s WHERE s.thread_id=t.id)
        OR EXISTS(SELECT 1 FROM steps s WHERE s.thread_id=t.id AND s.status='in_progress')
        THEN 'in_progress'
      ELSE 'passed'
    END status
FROM threads t JOIN chips c ON c.id=t.chip_id;
CREATE TRIGGER legacy_test_thread AFTER INSERT ON tests BEGIN
    INSERT INTO threads(chip_id,macro,title,created_at,legacy_test_id)
    VALUES(NEW.chip_id,NEW.macro,NEW.metric,strftime('%Y-%m-%dT%H:%M:%fZ','now'),NEW.id);
    INSERT INTO steps(thread_id,title,status,metric,measured_value,unit,measured_at,created_at,updated_at)
    SELECT id,NEW.metric,CASE NEW.passed WHEN 1 THEN 'passed' ELSE 'failed' END,
      NEW.metric,NEW.measured_value,NEW.unit,NEW.measured_at,
      strftime('%Y-%m-%dT%H:%M:%fZ','now'),strftime('%Y-%m-%dT%H:%M:%fZ','now')
    FROM threads WHERE legacy_test_id=NEW.id;
END;
INSERT INTO threads(chip_id,macro,title,created_at,legacy_test_id)
SELECT chip_id,macro,metric,COALESCE(measured_at,strftime('%Y-%m-%dT%H:%M:%fZ','now')),id
FROM tests ORDER BY id;
INSERT INTO steps(thread_id,title,status,metric,measured_value,unit,measured_at,created_at,updated_at)
SELECT t.id,v.metric,CASE v.passed WHEN 1 THEN 'passed' ELSE 'failed' END,
    v.metric,v.measured_value,v.unit,v.measured_at,t.created_at,t.created_at
FROM threads t JOIN tests v ON v.id=t.legacy_test_id ORDER BY t.id;
PRAGMA user_version=2;
"""


def migrate_v2(db):
    # executescript confirma una transacción anterior; el BEGIN pertenece al script.
    try:
        db.executescript("BEGIN IMMEDIATE;\n" + V2 + "\nCOMMIT;")
    except Exception:
        db.rollback()
        raise
