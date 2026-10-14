from pathlib import PurePosixPath
from urllib.parse import quote, unquote

from fastapi import APIRouter, HTTPException, Request, Response

from .db import audit
from .routes import DB, Id, actor
from .schemas import Macro
from .thread_schemas import LinkInput
from .thread_store import ATTACHMENT_FIELDS, now, require_step
from .threads import STEPS

router = APIRouter(tags=["Evidencias"])
BASE = STEPS + "/{stepId}/attachments"
MAX_BYTES = 10 * 1024 * 1024
MAX_ATTACHMENTS = 20
ALLOWED = {
    ".pdf",
    ".ppt",
    ".pptx",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".txt",
    ".csv",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
}


def reserve(db, chip_id, macro, thread_id, step_id):
    db.execute("BEGIN IMMEDIATE")
    require_step(db, chip_id, macro, thread_id, step_id)
    if (
        db.execute("SELECT COUNT(*) FROM attachments WHERE step_id=?", (step_id,)).fetchone()[0]
        >= MAX_ATTACHMENTS
    ):
        raise HTTPException(400, "Máximo 20 evidencias por paso")


def metadata(db, step_id, attachment_id):
    row = db.execute(
        f"SELECT {ATTACHMENT_FIELDS} FROM attachments WHERE id=? AND step_id=?",
        (attachment_id, step_id),
    ).fetchone()
    if row is None:
        raise HTTPException(404, "La evidencia no existe en ese paso")
    return dict(row)


@router.post(BASE + "/links", status_code=201, operation_id="addLink")
def add_link(
    chipId: Id, macro: Macro, threadId: Id, stepId: Id, body: LinkInput, request: Request, db: DB
):
    reserve(db, chipId, macro, threadId, stepId)
    identifier = db.execute(
        "INSERT INTO attachments(step_id,kind,name,url,created_at) VALUES(?,'link',?,?,?)",
        (stepId, body.name, body.url, now()),
    ).lastrowid
    result = metadata(db, stepId, identifier)
    audit(db, actor(request), "create", "attachment", identifier, result)
    db.commit()
    return result


@router.post(BASE + "/files", status_code=201, operation_id="uploadEvidence")
async def upload(chipId: Id, macro: Macro, threadId: Id, stepId: Id, request: Request, db: DB):
    # Leer en streaming y limitar antes de persistir. Nunca usar el nombre como ruta.
    require_step(db, chipId, macro, threadId, stepId)
    name = unquote(request.headers.get("X-Filename", ""))
    if (
        not name
        or len(name) > 240
        or any(ord(c) < 32 for c in name)
        or "/" in name
        or "\\" in name
        or PurePosixPath(name).suffix.lower() not in ALLOWED
    ):
        raise HTTPException(
            400, "Nombre o tipo no admitido. Usar PDF, Office, texto o imágenes comunes"
        )
    content = bytearray()
    async for chunk in request.stream():
        if len(content) + len(chunk) > MAX_BYTES:
            raise HTTPException(413, "El archivo supera el límite de 10 MiB")
        content.extend(chunk)
    if not content:
        raise HTTPException(400, "El archivo está vacío")
    reserve(db, chipId, macro, threadId, stepId)
    identifier = db.execute(
        "INSERT INTO attachments(step_id,kind,name,size,content,created_at) VALUES(?,'file',?,?,?,?)",
        (stepId, name, len(content), bytes(content), now()),
    ).lastrowid
    result = metadata(db, stepId, identifier)
    audit(db, actor(request), "create", "attachment", identifier, result)
    db.commit()
    return result


@router.get(BASE + "/{attachmentId}/download", operation_id="downloadEvidence")
def download(chipId: Id, macro: Macro, threadId: Id, stepId: Id, attachmentId: Id, db: DB):
    require_step(db, chipId, macro, threadId, stepId)
    item = metadata(db, stepId, attachmentId)
    if item["kind"] != "file":
        raise HTTPException(404, "La evidencia es un enlace, no un archivo")
    content = db.execute("SELECT content FROM attachments WHERE id=?", (attachmentId,)).fetchone()[
        0
    ]
    return Response(
        content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": "attachment; filename*=UTF-8''" + quote(item["name"], safe="")
        },
    )


@router.delete(BASE + "/{attachmentId}", status_code=204, operation_id="deleteEvidence")
def delete_attachment(
    chipId: Id, macro: Macro, threadId: Id, stepId: Id, attachmentId: Id, request: Request, db: DB
):
    db.execute("BEGIN IMMEDIATE")
    require_step(db, chipId, macro, threadId, stepId)
    snapshot = metadata(db, stepId, attachmentId)
    db.execute("DELETE FROM attachments WHERE id=?", (attachmentId,))
    audit(db, actor(request), "delete", "attachment", attachmentId, snapshot)
    db.commit()
    return Response(status_code=204)
