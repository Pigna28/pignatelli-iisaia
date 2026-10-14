"""Contrato de hilos: parámetros/inputs derivados de las rutas y salidas explícitas."""

from fastapi import FastAPI

from backend.attachments import router as attachment_router
from backend.threads import router as thread_router


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def obj(properties):
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def extend(spec):
    app = FastAPI()
    app.include_router(thread_router)
    app.include_router(attachment_router)
    generated = app.openapi()
    schemas = spec["components"]["schemas"]
    schemas.update(generated["components"]["schemas"])
    integer = {"type": "integer", "minimum": 1}
    string = {"type": "string"}
    date = {"type": "string", "format": "date-time"}
    status = {"type": "string", "enum": ["in_progress", "passed", "failed"]}
    thread = dict(
        id=integer,
        chip_id=integer,
        macro={"enum": ["Tx", "Rx", "PLL"]},
        title=string,
        description=string,
        created_at=date,
        part_number=string,
        board=string,
        step_count={"type": "integer", "minimum": 0},
        status=status,
    )
    schemas["Thread"] = obj(thread)
    attachment = dict(
        id=integer,
        step_id=integer,
        kind={"enum": ["file", "link"]},
        name=string,
        url={"type": ["string", "null"]},
        size={"type": "integer", "minimum": 0},
        created_at=date,
    )
    schemas["Attachment"] = obj(attachment)
    step = dict(
        id=integer,
        thread_id=integer,
        title=string,
        notes=string,
        status=status,
        metric={"type": ["string", "null"]},
        measured_value={"type": ["number", "null"]},
        unit={"type": ["string", "null"]},
        measured_at={"type": ["string", "null"], "format": "date-time"},
        created_at=date,
        updated_at=date,
    )
    schemas["Step"] = obj(step)
    schemas["StepDetail"] = obj(
        {**step, "attachments": {"type": "array", "items": ref("Attachment")}}
    )
    schemas["ThreadDetail"] = obj(
        {**thread, "steps": {"type": "array", "items": ref("StepDetail")}}
    )
    responses = {
        "listAllThreads": {"type": "array", "items": ref("Thread")},
        "listThreads": {"type": "array", "items": ref("Thread")},
        "createThread": ref("Thread"),
        "getThread": ref("ThreadDetail"),
        "createStep": ref("Step"),
        "updateStep": ref("Step"),
        "addLink": ref("Attachment"),
        "uploadEvidence": ref("Attachment"),
    }
    for path, methods in generated["paths"].items():
        for method, operation in methods.items():
            operation["responses"].pop("422", None)
            for code in [400, 401, 403, 404, 503]:
                operation["responses"][str(code)] = {
                    "description": "Entrada inválida, sesión/permisos, jerarquía o disponibilidad.",
                    "content": {"application/json": {"schema": ref("Error")}},
                }
            if method in {"post", "put", "delete"}:
                operation.setdefault("parameters", []).append(
                    {"$ref": "#/components/parameters/CSRF"}
                )
            operation_id = operation["operationId"]
            success = "201" if method == "post" else "200"
            if operation_id in responses:
                operation["responses"][success] = {
                    "description": "Operación exitosa.",
                    "content": {"application/json": {"schema": responses[operation_id]}},
                }
            if operation_id == "uploadEvidence":
                operation["description"] = (
                    "Cuerpo binario, máximo 10 MiB y 20 evidencias por paso. X-Filename codificado con percent-encoding. Tipos: PDF, PPT/PPTX, DOC/DOCX, XLS/XLSX, TXT/CSV, PNG/JPG/JPEG/WEBP/GIF. Descarga forzada; no se ejecuta ni analiza el contenido."
                )
                operation["parameters"].append(
                    {"name": "X-Filename", "in": "header", "required": True, "schema": string}
                )
                operation["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/octet-stream": {
                            "schema": {"type": "string", "format": "binary"}
                        }
                    },
                }
                operation["responses"]["413"] = {
                    "description": "Archivo mayor a 10 MiB.",
                    "content": {"application/json": {"schema": ref("Error")}},
                }
            if operation_id == "downloadEvidence":
                operation["responses"]["200"] = {
                    "description": "Descarga autenticada.",
                    "content": {
                        "application/octet-stream": {
                            "schema": {"type": "string", "format": "binary"}
                        }
                    },
                }
        spec["paths"][path] = methods
    spec["paths"]["/summary"]["get"]["description"] = (
        "Contadores globales de hilos. tests = passed + failed + in_progress; cada hilo cuenta una vez, sin importar sus pasos."
    )
    for path, methods in spec["paths"].items():
        if "/tests" in path:
            for operation in methods.values():
                operation["deprecated"] = True
                operation["description"] += (
                    " API histórica de mediciones: cada alta crea un hilo de un paso. Para el flujo actual usar /threads. Las filas históricas no reflejan ediciones posteriores de pasos."
                )
