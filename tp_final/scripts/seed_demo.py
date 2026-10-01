"""Carga explícita y repetible de datos sintéticos. Nunca se ejecuta al arrancar."""

from backend.config import load_settings
from backend.db import audit, connect, initialize


def seed(settings):
    if settings.auth_mode != "local":
        raise SystemExit("El seed está restringido al modo local")
    initialize(settings.database)
    with connect(settings.database) as db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM chips LIMIT 1").fetchone():
            print("La base ya tiene muestras; no se insertó nada.")
            return
        for index, (part, board) in enumerate(
            [
                ("DEMO-RF2401", "EVK-A / Rev. 2"),
                ("DEMO-RF2401", "EVK-B / Rev. 2"),
                ("DEMO-PLL800", "Socket board / Rev. 1"),
            ]
        ):
            chip_id = db.execute(
                "INSERT INTO chips(part_number,board,assembled_at) VALUES (?,?,?)",
                (part, board, "2026-09-25"),
            ).lastrowid
            audit(
                db,
                "seed-demo",
                "create",
                "chip",
                chip_id,
                {
                    "id": chip_id,
                    "part_number": part,
                    "board": board,
                    "assembled_at": "2026-09-25",
                    "synthetic": True,
                },
            )
            for macro, metric, value, unit, passed in [
                ("Tx", "Ganancia", 18.6 + index, "dB", True),
                ("Tx", "Ancho de banda", 242.1, "MHz", True),
                ("Rx", "Figura de ruido", 4.8, "dB", False),
                ("PLL", "Ruido de fase @ 1 MHz", -112.4, "dBc/Hz", True),
            ]:
                test_id = db.execute(
                    "INSERT INTO tests(chip_id,macro,metric,measured_value,unit,passed,measured_at) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (chip_id, macro, metric, value, unit, passed, "2026-09-30T15:00:00Z"),
                ).lastrowid
                audit(
                    db,
                    "seed-demo",
                    "create",
                    "test",
                    test_id,
                    {
                        "id": test_id,
                        "chip_id": chip_id,
                        "macro": macro,
                        "metric": metric,
                        "measured_value": value,
                        "unit": unit,
                        "passed": passed,
                        "measured_at": "2026-09-30T15:00:00Z",
                        "synthetic": True,
                    },
                )
    print("Demo creada: 3 muestras y 12 ensayos sintéticos.")


if __name__ == "__main__":
    seed(load_settings())
