import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json(file_name: str) -> list[dict[str, Any]]:
    with (DATA_DIR / file_name).open(encoding="utf-8") as file:
        return json.load(file)


def save_json(file_name: str, rows: list[dict[str, Any]]) -> None:
    with (DATA_DIR / file_name).open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)
        file.write("\n")
