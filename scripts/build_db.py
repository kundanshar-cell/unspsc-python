"""
Build the UNSPSC SQLite database from the official UNDP codeset Excel file.

Usage:
    python scripts/build_db.py path/to/unspsc-english-v260801.xlsx

Download the codeset (free) from: https://www.undp.org/unspsc
"""

import argparse
import gzip
import shutil
import sqlite3
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("Missing dependency: pip install openpyxl")
    sys.exit(1)

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "unspsc.db"
DB_GZ_PATH = DATA_DIR / "unspsc.db.gz"


def build(source: Path) -> None:
    DATA_DIR.mkdir(exist_ok=True)

    print(f"Loading {source} ...")
    wb = openpyxl.load_workbook(source, read_only=True)
    ws = wb.active
    all_rows = list(ws.iter_rows(values_only=True))

    # Find header row (contains "Segment")
    header_idx = next(i for i, r in enumerate(all_rows) if r[2] == "Segment")
    data = all_rows[header_idx + 1 :]

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript(
        """
        CREATE TABLE segments (
            code INTEGER PRIMARY KEY, title TEXT NOT NULL, definition TEXT
        );
        CREATE TABLE families (
            code INTEGER PRIMARY KEY, title TEXT NOT NULL, definition TEXT,
            segment_code INTEGER NOT NULL
        );
        CREATE TABLE classes (
            code INTEGER PRIMARY KEY, title TEXT NOT NULL, definition TEXT,
            family_code INTEGER NOT NULL
        );
        CREATE TABLE commodities (
            code INTEGER PRIMARY KEY, title TEXT NOT NULL, definition TEXT,
            class_code INTEGER NOT NULL
        );
        CREATE VIRTUAL TABLE commodities_fts USING fts5(
            title, definition, content=commodities, content_rowid=code
        );
        """
    )

    seen_seg: set = set()
    seen_fam: set = set()
    seen_cls: set = set()
    n = 0

    for r in data:
        seg_code, seg_title, seg_def = r[2], r[3], r[4]
        fam_code, fam_title, fam_def = r[5], r[6], r[7]
        cls_code, cls_title, cls_def = r[8], r[9], r[10]
        com_code, com_title, com_def = r[11], r[12], r[13]

        if seg_code and seg_code not in seen_seg:
            c.execute("INSERT OR IGNORE INTO segments VALUES (?,?,?)", (seg_code, seg_title, seg_def))
            seen_seg.add(seg_code)
        if fam_code and fam_code not in seen_fam:
            c.execute("INSERT OR IGNORE INTO families VALUES (?,?,?,?)", (fam_code, fam_title, fam_def, seg_code))
            seen_fam.add(fam_code)
        if cls_code and cls_code not in seen_cls:
            c.execute("INSERT OR IGNORE INTO classes VALUES (?,?,?,?)", (cls_code, cls_title, cls_def, fam_code))
            seen_cls.add(cls_code)
        if com_code:
            c.execute("INSERT OR IGNORE INTO commodities VALUES (?,?,?,?)", (com_code, com_title, com_def, cls_code))
            n += 1

    c.execute('INSERT INTO commodities_fts(commodities_fts) VALUES ("rebuild")')
    conn.commit()
    conn.close()

    print(f"Inserted: {len(seen_seg)} segments, {len(seen_fam)} families, {len(seen_cls)} classes, {n} commodities")

    print("Compressing ...")
    with open(DB_PATH, "rb") as f_in, gzip.open(DB_GZ_PATH, "wb", compresslevel=9) as f_out:
        shutil.copyfileobj(f_in, f_out)

    print(f"Done — {DB_GZ_PATH} ({DB_GZ_PATH.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build UNSPSC SQLite database")
    parser.add_argument("source", help="Path to UNDP UNSPSC Excel or CSV file")
    args = parser.parse_args()
    build(Path(args.source))
