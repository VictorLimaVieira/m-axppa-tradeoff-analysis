from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT / "database" / "m_axppa_synthetic.sqlite"


def format_value(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python src/run_query.py database/queries/02_energia_com_erro_controlado.sql")
        raise SystemExit(1)

    query_path = ROOT / sys.argv[1]
    if not query_path.exists():
        print(f"Query nao encontrada: {query_path}")
        raise SystemExit(1)

    if not DATABASE_PATH.exists():
        print("Banco nao encontrado. Rode primeiro:")
        print("python src/data_generation/generate_synthetic_data.py")
        raise SystemExit(1)

    query = query_path.read_text(encoding="utf-8")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    connection.close()

    print(" | ".join(columns))
    print("-" * 100)
    for row in rows:
        print(" | ".join(format_value(value) for value in row))


if __name__ == "__main__":
    main()

