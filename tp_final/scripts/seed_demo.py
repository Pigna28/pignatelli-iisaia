"""Carga explícita, atómica y repetible de la campaña sintética A0/A1/A2."""

import argparse
import csv
import io
from dataclasses import replace
from pathlib import Path

from backend.config import ROOT, load_settings
from backend.db import audit, connect, initialize
from backend.thread_store import now

CAMPAIGN = "seed-demo:a0-a1-a2-v1"
# Resultado y etapa activa: 0 preparación, 1 medición, 2 revisión, 3 completo.
SAMPLES = {
    "A0": [("passed", 3, 242.1), ("in_progress", 1, None), ("failed", 3, 6.8), ("passed", 3, 82.4)],
    "A1": [
        ("in_progress", 0, None),
        ("passed", 3, 18.9),
        ("in_progress", 2, 3.2),
        ("failed", 3, 142.0),
    ],
    "A2": [("failed", 3, 178.5), ("failed", 3, 11.2), ("passed", 3, 2.9), ("in_progress", 1, None)],
}
MEASUREMENTS = [
    (
        "Tx",
        "Ancho de banda",
        "MHz",
        "Calibrar el barrido de frecuencia",
        "Ejecutar barrido a -3 dB",
    ),
    (
        "Tx",
        "Ganancia",
        "dB",
        "Calibrar niveles de entrada y salida",
        "Medir ganancia de pequeña señal",
    ),
    ("Rx", "Ruido", "dB", "Calibrar la fuente de ruido", "Medir figura de ruido"),
    (
        "PLL",
        "Consumo",
        "mW",
        "Configurar fuente y frecuencia del PLL",
        "Medir potencia en régimen estable",
    ),
]


def insert(db, table, fields, timestamp):
    """Tablas y columnas internas constantes; valores siempre parametrizados."""
    row_id = db.execute(
        f"INSERT INTO {table}({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})",
        tuple(fields.values()),
    ).lastrowid
    snapshot = {key: value for key, value in fields.items() if key != "content"}
    audit(
        db,
        CAMPAIGN,
        "create",
        {"chips": "chip", "threads": "thread", "steps": "step", "attachments": "attachment"}[table],
        row_id,
        {
            **snapshot,
            "id": row_id,
            "synthetic": True,
            "demo_campaign": CAMPAIGN,
            "seeded_at": timestamp,
        },
    )
    return row_id


def seed(settings):
    if settings.auth_mode != "local" or settings.environment != "development":
        raise SystemExit("El seed está restringido al modo local de desarrollo")
    initialize(settings.database)
    timestamp = now()
    with connect(settings.database) as db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM audit WHERE actor=? LIMIT 1", (CAMPAIGN,)).fetchone():
            print("La demo A0/A1/A2 ya fue cargada; se conservan sus cambios sin duplicarla.")
            return
        for part, outcomes in SAMPLES.items():
            chip_id = insert(
                db,
                "chips",
                {
                    "part_number": part,
                    "board": f"DEMO sintética / EVK-{part}",
                    "assembled_at": "2026-10-12",
                },
                timestamp,
            )
            for (macro, metric, unit, preparation, measurement), (result, stage, value) in zip(
                MEASUREMENTS, outcomes, strict=True
            ):
                thread_id = insert(
                    db,
                    "threads",
                    {
                        "chip_id": chip_id,
                        "macro": macro,
                        "title": f"{metric} — {part}",
                        "description": "Campaña DEMO: datos y dictámenes sintéticos para mostrar el flujo; no representan límites eléctricos reales.",
                        "created_at": timestamp,
                    },
                    timestamp,
                )
                for position, title in enumerate(
                    [preparation, measurement, "Revisar resultados y cerrar informe"]
                ):
                    status = "passed" if position < stage else "in_progress"
                    if result == "failed" and position == 1:
                        status = "failed"
                    measured = position == 1 and value is not None
                    notes = "DEMO sintética. "
                    if status == "in_progress":
                        notes += (
                            "Etapa activa."
                            if position == stage
                            else "Pendiente de completar la etapa anterior."
                        )
                    elif status == "failed":
                        notes += "Dictamen de ejemplo: resultado rechazado; investigar y repetir en otro paso."
                    elif position == 2 and result == "failed":
                        notes += "Revisión completada: se documenta el fallo de medición, sin aprobar el hilo."
                    else:
                        notes += "Etapa completada y revisada."
                    step_id = insert(
                        db,
                        "steps",
                        {
                            "thread_id": thread_id,
                            "title": title,
                            "notes": notes,
                            "status": status,
                            "metric": metric if measured else None,
                            "measured_value": value if measured else None,
                            "unit": unit if measured else None,
                            "measured_at": timestamp if measured else None,
                            "created_at": timestamp,
                            "updated_at": timestamp,
                        },
                        timestamp,
                    )
                    if measured:
                        buffer = io.StringIO(newline="")
                        writer = csv.writer(buffer)
                        writer.writerow(
                            ["origen", "chip", "macro", "metrica", "valor", "unidad", "estado"]
                        )
                        writer.writerow(
                            ["DEMO SINTETICA", part, macro, metric, value, unit, status]
                        )
                        content = buffer.getvalue().encode("utf-8-sig")
                        insert(
                            db,
                            "attachments",
                            {
                                "step_id": step_id,
                                "kind": "file",
                                "name": f"demo-{part}-{metric.lower().replace(' ', '-')}.csv",
                                "size": len(content),
                                "content": content,
                                "created_at": timestamp,
                            },
                            timestamp,
                        )
    print(
        "Demo creada: A0, A1, A2; 12 hilos (4 aprobados, 4 fallidos, 4 en progreso), 36 pasos y 9 CSV sintéticos."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, help="Base alternativa; ruta relativa a tp_final")
    parser.add_argument(
        "--append", action="store_true", help="Compatibilidad: siempre conserva datos existentes"
    )
    args = parser.parse_args()
    settings = load_settings()
    if args.database is not None:
        path = args.database if args.database.is_absolute() else ROOT / args.database
        settings = replace(settings, database=path)
    seed(settings)


if __name__ == "__main__":
    main()
