"""Backup consistente de SQLite, incluyendo transacciones del WAL."""

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

from backend.config import load_settings


def backup(source, destination):
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise ValueError("No existe la base de origen")
    if destination.exists():
        raise ValueError("El destino ya existe; elegir otro nombre")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Reserva exclusiva: nunca sobrescribir accidentalmente un backup.
    with destination.open("xb"):
        pass
    with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(destination)) as dst:
        src.backup(dst)
        if dst.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise RuntimeError("El backup no pasó integrity_check")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    backup(load_settings().database, args.destination)
    print(f"Backup verificado: {args.destination}")
