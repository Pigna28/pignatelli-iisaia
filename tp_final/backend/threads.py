from typing import Annotated

from fastapi import APIRouter, Query, Request, Response

from .db import audit
from .routes import DB, Id, actor, chip_or_404
from .schemas import Macro
from .thread_schemas import Status, StepInput, ThreadInput
from .thread_store import detail, now, require_step, require_thread, thread_record

router = APIRouter(tags=["Hilos"])
BASE = "/chips/{chipId}/macros/{macro}/threads"
THREAD = BASE + "/{threadId}"
STEPS = THREAD + "/steps"


@router.get("/threads", operation_id="listAllThreads")
def all_threads(db: DB, status: Annotated[Status | None, Query()] = None):
    return [
        thread_record(row)
        for row in db.execute(
            "SELECT * FROM thread_overview WHERE (? IS NULL OR status=?) ORDER BY id DESC",
            (status, status),
        )
    ]


@router.get(BASE, operation_id="listThreads")
def list_threads(
    chipId: Id, macro: Macro, db: DB, status: Annotated[Status | None, Query()] = None
):
    chip_or_404(db, chipId)
    return [
        thread_record(row)
        for row in db.execute(
            "SELECT * FROM thread_overview WHERE chip_id=? AND macro=? "
            "AND (? IS NULL OR status=?) ORDER BY id DESC",
            (chipId, macro, status, status),
        )
    ]


@router.post(BASE, status_code=201, operation_id="createThread")
def create_thread(chipId: Id, macro: Macro, body: ThreadInput, request: Request, db: DB):
    db.execute("BEGIN IMMEDIATE")
    chip_or_404(db, chipId)
    identifier = db.execute(
        "INSERT INTO threads(chip_id,macro,title,description,created_at) VALUES(?,?,?,?,?)",
        (chipId, macro, body.title, body.description, now()),
    ).lastrowid
    result = require_thread(db, chipId, macro, identifier)
    audit(db, actor(request), "create", "thread", identifier, result)
    db.commit()
    return result


@router.get(THREAD, operation_id="getThread")
def get_thread(chipId: Id, macro: Macro, threadId: Id, db: DB):
    return detail(db, require_thread(db, chipId, macro, threadId))


@router.delete(THREAD, status_code=204, operation_id="deleteThread")
def delete_thread(chipId: Id, macro: Macro, threadId: Id, db: DB, request: Request):
    db.execute("BEGIN IMMEDIATE")
    snapshot = detail(db, require_thread(db, chipId, macro, threadId))
    legacy = db.execute("SELECT legacy_test_id FROM threads WHERE id=?", (threadId,)).fetchone()[0]
    db.execute("DELETE FROM threads WHERE id=?", (threadId,))
    if legacy is not None:
        db.execute("DELETE FROM tests WHERE id=?", (legacy,))
    audit(db, actor(request), "delete", "thread", threadId, snapshot)
    db.commit()
    return Response(status_code=204)


@router.post(STEPS, status_code=201, operation_id="createStep")
def create_step(chipId: Id, macro: Macro, threadId: Id, body: StepInput, request: Request, db: DB):
    db.execute("BEGIN IMMEDIATE")
    require_thread(db, chipId, macro, threadId)
    data = body.model_dump(mode="json")
    stamp = now()
    identifier = db.execute(
        "INSERT INTO steps(thread_id,title,notes,status,metric,measured_value,unit,measured_at,"
        "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
        (
            threadId,
            data["title"],
            data["notes"],
            data["status"],
            data["metric"],
            data["measured_value"],
            data["unit"],
            data["measured_at"],
            stamp,
            stamp,
        ),
    ).lastrowid
    result = require_step(db, chipId, macro, threadId, identifier)
    audit(db, actor(request), "create", "step", identifier, result)
    db.commit()
    return result


@router.put(STEPS + "/{stepId}", operation_id="updateStep")
def update_step(
    chipId: Id, macro: Macro, threadId: Id, stepId: Id, body: StepInput, request: Request, db: DB
):
    db.execute("BEGIN IMMEDIATE")
    before = require_step(db, chipId, macro, threadId, stepId)
    data = body.model_dump(mode="json")
    db.execute(
        "UPDATE steps SET title=?,notes=?,status=?,metric=?,measured_value=?,unit=?,"
        "measured_at=?,updated_at=? WHERE id=?",
        (
            data["title"],
            data["notes"],
            data["status"],
            data["metric"],
            data["measured_value"],
            data["unit"],
            data["measured_at"],
            now(),
            stepId,
        ),
    )
    result = require_step(db, chipId, macro, threadId, stepId)
    audit(db, actor(request), "update", "step", stepId, {"before": before, "after": result})
    db.commit()
    return result


@router.delete(STEPS + "/{stepId}", status_code=204, operation_id="deleteStep")
def delete_step(chipId: Id, macro: Macro, threadId: Id, stepId: Id, request: Request, db: DB):
    from .thread_store import evidence

    db.execute("BEGIN IMMEDIATE")
    snapshot = require_step(db, chipId, macro, threadId, stepId)
    snapshot["attachments"] = evidence(db, stepId)
    db.execute("DELETE FROM steps WHERE id=?", (stepId,))
    audit(db, actor(request), "delete", "step", stepId, snapshot)
    db.commit()
    return Response(status_code=204)
