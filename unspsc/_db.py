import gzip
import shutil
import sqlite3
from pathlib import Path
from typing import Optional

_DATA_DIR = Path(__file__).parent.parent / "data"
_DB_GZ = _DATA_DIR / "unspsc.db.gz"
_DB = _DATA_DIR / "unspsc.db"

_conn: Optional[sqlite3.Connection] = None


def _ensure_db() -> None:
    if _DB.exists():
        return
    if not _DB_GZ.exists():
        raise FileNotFoundError(
            f"UNSPSC database not found at {_DB_GZ}. "
            "Run: python -m unspsc.build to generate it from the official UNDP codeset."
        )
    with gzip.open(_DB_GZ, "rb") as f_in, open(_DB, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _ensure_db()
        _conn = sqlite3.connect(_DB, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn
