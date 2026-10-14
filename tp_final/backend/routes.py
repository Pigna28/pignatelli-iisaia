import json
import sqlite3
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, Response

from .db import audit, get_db, record
from .schemas import ChipInput, Macro, TestInput
from .thread_store import chip_threads, detail, thread_record

router = APIRouter()
Id = Annotated[int, Path(gt=0)]


def database(request: Request):
    yield from get_db(request)


DB = Annotated[sqlite3.Connection, Depends(database)]


def chip_or_404(db, chip_id):
    row = db.execute("SELECT * FROM chips WHERE id=?", (chip_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "El chip indicado no existe")
    return record(row)


def actor(request):
    return request.state.user["sub"]


@router.get("/chips", operation_id="listChips", tags=["Chips"])
def list_chips(db: DB):
    return [record(row) for row in db.execute("SELECT * FROM chips ORDER BY id DESC")]


@router.post("/chips", status_code=201, operation_id="createChip", tags=["Chips"])
def create_chip(body: ChipInput, request: Request, db: DB):
    data = body.model_dump(mode="json", exclude_none=True)
    cursor = db.execute(
        "INSERT INTO chips(part_number,board,assembled_at) VALUES (?,?,?)",
        (data["part_number"], data["board"], data.get("assembled_at")),
    )
    result = {"id": cursor.lastrowid, **data}
    audit(db, actor(request), "create", "chip", result["id"], result)
    db.commit()
    return result


@router.delete("/chips/{chipId}", status_code=204, operation_id="deleteChip", tags=["Chips"])
def delete_chip(chipId: Id, request: Request, db: DB):
    db.execute("BEGIN IMMEDIATE")
    snapshot = chip_or_404(db, chipId)
    snapshot["tests"] = [
        record(row)
        for row in db.execute("SELECT * FROM tests WHERE chip_id=? ORDER BY id", (chipId,))
    ]
    snapshot["threads"] = chip_threads(db, chipId)
    db.execute("DELETE FROM chips WHERE id=?", (chipId,))
    audit(db, actor(request), "delete", "chip", chipId, snapshot)
    db.commit()
    return Response(status_code=204)


@router.get("/chips/{chipId}/macros/{macro}/tests", operation_id="listTests", tags=["Tests"])
def list_tests(
    chipId: Id,
    macro: Macro,
    db: DB,
    passed: Annotated[Literal["true", "false"] | None, Query()] = None,
):
    chip_or_404(db, chipId)
    sql = "SELECT * FROM tests WHERE chip_id=? AND macro=?"
    args = [chipId, macro]
    if passed is not None:
        sql += " AND passed=?"
        args.append(int(passed == "true"))
    return [record(row) for row in db.execute(sql + " ORDER BY id DESC", args)]


@router.post(
    "/chips/{chipId}/macros/{macro}/tests",
    status_code=201,
    operation_id="createTest",
    tags=["Tests"],
)
def create_test(chipId: Id, macro: Macro, body: TestInput, request: Request, db: DB):
    db.execute("BEGIN IMMEDIATE")
    chip_or_404(db, chipId)
    data = body.model_dump(mode="json", exclude_none=True)
    cursor = db.execute(
        "INSERT INTO tests(chip_id,macro,metric,measured_value,unit,passed,measured_at) "
        "VALUES (?,?,?,?,?,?,?)",
        (
            chipId,
            macro,
            data["metric"],
            data["measured_value"],
            data["unit"],
            data["passed"],
            data.get("measured_at"),
        ),
    )
    result = {"id": cursor.lastrowid, "chip_id": chipId, "macro": macro, **data}
    audit(db, actor(request), "create", "test", result["id"], result)
    db.commit()
    return result


@router.delete(
    "/chips/{chipId}/macros/{macro}/tests/{testId}",
    status_code=204,
    operation_id="deleteTest",
    tags=["Tests"],
)
def delete_test(chipId: Id, macro: Macro, testId: Id, request: Request, db: DB):
    db.execute("BEGIN IMMEDIATE")
    chip_or_404(db, chipId)
    row = db.execute(
        "SELECT * FROM tests WHERE id=? AND chip_id=? AND macro=?", (testId, chipId, macro)
    ).fetchone()
    if row is None:
        raise HTTPException(404, "El ensayo no existe en esa macro y chip")
    snapshot = record(row)
    migrated = db.execute(
        "SELECT * FROM thread_overview WHERE legacy_test_id=?", (testId,)
    ).fetchone()
    if migrated is not None:
        snapshot["thread"] = detail(db, thread_record(migrated))
    db.execute("DELETE FROM tests WHERE id=?", (testId,))
    audit(db, actor(request), "delete", "test", testId, snapshot)
    db.commit()
    return Response(status_code=204)


@router.get("/summary", operation_id="getSummary", tags=["Laboratorio"])
def summary(db: DB):
    counts = {
        row["status"]: row["total"]
        for row in db.execute("SELECT status,COUNT(*) total FROM thread_overview GROUP BY status")
    }
    return {
        "chips": db.execute("SELECT COUNT(*) FROM chips").fetchone()[0],
        "tests": sum(counts.values()),
        "passed": counts.get("passed", 0),
        "failed": counts.get("failed", 0),
        "in_progress": counts.get("in_progress", 0),
    }


@router.get("/audit", operation_id="listAudit", tags=["Laboratorio"])
def list_audit(
    db: DB,
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    before: Annotated[int | None, Query(gt=0)] = None,
):
    if not request.state.can_write:
        raise HTTPException(403, "Solo operadores pueden consultar la auditoría")
    rows = db.execute(
        "SELECT * FROM audit WHERE (? IS NULL OR id < ?) ORDER BY id DESC LIMIT ?",
        (before, before, limit),
    )
    return [{**dict(row), "snapshot": json.loads(row["snapshot"])} for row in rows]
