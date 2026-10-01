"""Migra el contrato histórico a la extensión implementada; salida determinista."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def response(description, schema):
    return {"description": description, "content": {"application/json": {"schema": schema}}}


def ref(name):
    return {"$ref": f"#/components/schemas/{name}"}


def build():
    spec = yaml.safe_load((ROOT / "opeanapi.yaml").read_text("utf-8"))
    spec["info"]["version"] = "1.1.0"
    spec["info"]["description"] += (
        " Laboratorio compartido. Cookie de sesión en modo Auth0; modo local solo en loopback."
        " Antes de escribir, obtener X-CSRF-Token de GET /session."
    )
    spec["servers"] = [{"url": "/"}]
    spec["security"] = [{"SessionCookie": []}]
    components = spec["components"]
    components["securitySchemes"] = {
        "SessionCookie": {"type": "apiKey", "in": "cookie", "name": "lab_session"}
    }
    components["parameters"]["CSRF"] = {
        "name": "X-CSRF-Token",
        "in": "header",
        "required": True,
        "description": "Valor csrf_token de GET /session, usando la misma cookie.",
        "schema": {"type": "string"},
    }
    components["parameters"]["ChipId"]["schema"]["minimum"] = 1
    schemas = components["schemas"]
    for name in ("Chip", "ChipInput", "Test", "TestInput"):
        schemas[name]["additionalProperties"] = False
        for key, prop in schemas[name]["properties"].items():
            if key in {"id", "chip_id"}:
                prop["minimum"] = 1
            if key in {"part_number", "board", "metric", "unit"}:
                prop.update(minLength=1, maxLength=120)
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            operation["responses"]["401"] = response("Sesión requerida.", ref("Error"))
            operation["responses"]["403"] = response("Sin permiso o CSRF inválido.", ref("Error"))
            operation["responses"]["503"] = response(
                "Base temporalmente no disponible.", ref("Error")
            )
            if "{" in path or method == "post":
                operation["responses"]["400"] = response("Entrada inválida.", ref("Error"))
            if method in {"post", "delete"}:
                operation.setdefault("parameters", []).append(
                    {"$ref": "#/components/parameters/CSRF"}
                )
            for param in operation.get("parameters", []):
                if param.get("name") == "testId":
                    param["schema"]["minimum"] = 1
    schemas["Summary"] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["chips", "tests", "passed", "failed"],
        "properties": {
            key: {"type": "integer", "minimum": 0} for key in ["chips", "tests", "passed", "failed"]
        },
    }
    schemas["Session"] = {
        "type": "object",
        "required": ["user", "can_write", "mode", "csrf_token"],
        "properties": {
            "user": {
                "type": "object",
                "required": ["sub", "name"],
                "properties": {"sub": {"type": "string"}, "name": {"type": "string"}},
            },
            "can_write": {"type": "boolean"},
            "mode": {"enum": ["local", "auth0"]},
            "csrf_token": {"type": "string"},
        },
    }
    schemas["AuditEvent"] = {
        "type": "object",
        "required": ["id", "occurred_at", "actor", "action", "resource", "resource_id", "snapshot"],
        "properties": {
            "id": {"type": "integer"},
            "occurred_at": {"type": "string", "format": "date-time"},
            "actor": {"type": "string"},
            "action": {"enum": ["create", "delete"]},
            "resource": {"enum": ["chip", "test"]},
            "resource_id": {"type": "integer"},
            "snapshot": {"type": "object", "additionalProperties": True},
        },
    }
    for path, name, schema in [
        ("/summary", "getSummary", ref("Summary")),
        ("/session", "getSession", ref("Session")),
        ("/audit", "listAudit", {"type": "array", "items": ref("AuditEvent")}),
    ]:
        spec["paths"][path] = {
            "get": {
                "operationId": name,
                "tags": ["Laboratorio"],
                "responses": {
                    "200": response("Operación exitosa.", schema),
                    "401": response("Sesión requerida.", ref("Error")),
                    "403": response("Sin permiso.", ref("Error")),
                    "503": response("Base temporalmente no disponible.", ref("Error")),
                },
            }
        }
    spec["paths"]["/audit"]["get"].update(
        parameters=[
            {
                "name": "limit",
                "in": "query",
                "schema": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
            },
            {"name": "before", "in": "query", "schema": {"type": "integer", "minimum": 1}},
        ]
    )
    spec["paths"]["/audit"]["get"]["responses"]["400"] = response(
        "Paginación inválida.", ref("Error")
    )
    spec["paths"]["/health"] = {
        "get": {
            "operationId": "health",
            "security": [],
            "responses": {
                "200": response(
                    "Base accesible.",
                    {
                        "type": "object",
                        "required": ["status"],
                        "properties": {"status": {"const": "ok"}},
                    },
                ),
                "503": response("Base no disponible.", ref("Error")),
            },
        }
    }
    spec["paths"]["/logout"] = {
        "post": {
            "operationId": "logout",
            "parameters": [{"$ref": "#/components/parameters/CSRF"}],
            "responses": {
                "200": response(
                    "Sesión local cerrada; navegar a redirect para cerrar Auth0.",
                    {
                        "type": "object",
                        "required": ["redirect"],
                        "properties": {"redirect": {"type": "string"}},
                    },
                ),
                "401": response("Sesión requerida.", ref("Error")),
                "403": response("CSRF inválido.", ref("Error")),
            },
        }
    }
    (ROOT / "openapi.yaml").write_text(
        yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), "utf-8"
    )


if __name__ == "__main__":
    build()
