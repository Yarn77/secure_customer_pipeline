import csv
import json
from pathlib import Path

def export_clean_csv(filepath: Path, records: list):
    fields = ["cid", "name", "email", "pin", "spend"]
    with filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

def export_manifest(filepath: Path, count: int, csv_name: str, digest: str):
    payload = {
        "accepted_records": count,
        "output_csv": csv_name,
        "sha256": digest
    }
    filepath.write_text(json.dumps(payload, indent=2), encoding="utf-8")