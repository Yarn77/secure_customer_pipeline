import hashlib
from pathlib import Path

BASE_OUT = Path("output").resolve()
BASE_OUT.mkdir(parents=True, exist_ok=True)

def get_safe_path(filename: str) -> Path:
    if Path(filename).name != filename:
        raise ValueError("Directory traversal blocked")
    candidate = (BASE_OUT / filename).resolve()
    if candidate.parent != BASE_OUT:
        raise ValueError("Path outside base output directory blocked")
    return candidate

def compute_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with filepath.open("rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()