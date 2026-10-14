from datetime import datetime, timezone

from fastapi import HTTPException

ATTACHMENT_FIELDS = "id,step_id,kind,name,url,size,created_at"


def now():
    return datetime.now(timezone.utc).isoformat()


def thread_record(row):
    data = dict(row)
    data.pop("legacy_test_id", None)
    return data


def require_thread(db, chip_id, macro, thread_id):
    row = db.execute(
        "SELECT * FROM thread_overview WHERE id=? AND chip_id=? AND macro=?",
        (thread_id, chip_id, macro),
    ).fetchone()
    if row is None:
        raise HTTPException(404, "El hilo no existe en esa muestra y macro")
    return thread_record(row)


def require_step(db, chip_id, macro, thread_id, step_id):
    require_thread(db, chip_id, macro, thread_id)
    row = db.execute(
        "SELECT * FROM steps WHERE id=? AND thread_id=?", (step_id, thread_id)
    ).fetchone()
    if row is None:
        raise HTTPException(404, "El paso no existe en ese hilo")
    return dict(row)


def evidence(db, step_id):
    return [
        dict(row)
        for row in db.execute(
            f"SELECT {ATTACHMENT_FIELDS} FROM attachments WHERE step_id=? ORDER BY id", (step_id,)
        )
    ]


def detail(db, thread):
    return {
        **thread,
        "steps": [
            {**dict(row), "attachments": evidence(db, row["id"])}
            for row in db.execute(
                "SELECT * FROM steps WHERE thread_id=? ORDER BY id", (thread["id"],)
            )
        ],
    }


def chip_threads(db, chip_id):
    return [
        detail(db, thread_record(row))
        for row in db.execute(
            "SELECT * FROM thread_overview WHERE chip_id=? ORDER BY id", (chip_id,)
        )
    ]
