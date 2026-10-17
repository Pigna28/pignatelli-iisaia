"""Carga explícita de datos sintéticos de exposición. Nunca se ejecuta al arrancar."""

import argparse
from dataclasses import replace
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator

from backend.config import ROOT, load_settings
from backend.db import audit, connect, initialize
from backend.schemas import ChipInput, Input, Macro, TestInput, Text

DATASET_PATH = ROOT / "fixtures/demo_lab.json"


class DemoSample(Input):
    scenario: Text
    chip: ChipInput
    tests: dict[Macro, list[TestInput]]

    @field_validator("tests")
    @classmethod
    def fixed_macros(cls, value):
        if set(value) != {"Tx", "Rx", "PLL"}:
            raise ValueError("Cada muestra debe incluir Tx, Rx y PLL, aunque estén vacías")
        return value


class DemoDataset(Input):
    dataset_id: Text
    synthetic: Literal[True]
    description: str
    samples: list[DemoSample] = Field(min_length=1)


def load_dataset():
    return DemoDataset.model_validate_json(DATASET_PATH.read_text(encoding="utf-8"))


def seed(settings, *, append=False):
    if settings.auth_mode != "local" or settings.environment != "development":
        raise SystemExit("El seed está restringido al modo local de desarrollo")
    dataset = load_dataset()
    seed_actor = f"seed-demo:{dataset.dataset_id}"
    initialize(settings.database)
    total_tests = 0
    with connect(settings.database) as db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM audit WHERE actor=? LIMIT 1", (seed_actor,)).fetchone():
            print("Este conjunto ya fue cargado; no se insertó nada.")
            return
        if not append and db.execute("SELECT 1 FROM chips LIMIT 1").fetchone():
            print("La base ya tiene muestras; usar --append para agregar la demo sin borrarlas.")
            return
        for sample in dataset.samples:
            chip = sample.chip.model_dump(mode="json", exclude_none=True)
            chip_id = db.execute(
                "INSERT INTO chips(part_number,board,assembled_at) VALUES (?,?,?)",
                (chip["part_number"], chip["board"], chip.get("assembled_at")),
            ).lastrowid
            metadata = {
                "synthetic": True,
                "dataset_id": dataset.dataset_id,
                "scenario": sample.scenario,
            }
            audit(db, seed_actor, "create", "chip", chip_id, {"id": chip_id, **chip, **metadata})
            for macro, tests in sample.tests.items():
                for measurement in tests:
                    data = measurement.model_dump(mode="json", exclude_none=True)
                    test_id = db.execute(
                        "INSERT INTO tests(chip_id,macro,metric,measured_value,unit,passed,measured_at) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (
                            chip_id,
                            macro,
                            data["metric"],
                            data["measured_value"],
                            data["unit"],
                            data["passed"],
                            data.get("measured_at"),
                        ),
                    ).lastrowid
                    audit(
                        db,
                        seed_actor,
                        "create",
                        "test",
                        test_id,
                        {"id": test_id, "chip_id": chip_id, "macro": macro, **data, **metadata},
                    )
                    total_tests += 1
    print(f"Demo creada: {len(dataset.samples)} muestras y {total_tests} ensayos sintéticos.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--append", action="store_true", help="Agregar sin borrar muestras existentes"
    )
    parser.add_argument("--database", type=Path, help="Base alternativa; ruta relativa a tp_final")
    args = parser.parse_args()
    settings = load_settings()
    if args.database is not None:
        path = args.database if args.database.is_absolute() else ROOT / args.database
        settings = replace(settings, database=path)
    seed(settings, append=args.append)


if __name__ == "__main__":
    main()
