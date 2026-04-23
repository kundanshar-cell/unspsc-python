from typing import List, Optional, Union

from unspsc._db import get_conn
from unspsc._models import Class, Commodity, Family, Hierarchy, MatchResult, Segment


def lookup(code: int) -> Optional[Union[Segment, Family, Class, Commodity]]:
    """Return the UNSPSC node for *code* at whatever level it belongs to."""
    conn = get_conn()
    row = conn.execute("SELECT code, title, definition FROM segments WHERE code=?", (code,)).fetchone()
    if row:
        return Segment(**row)
    row = conn.execute("SELECT code, title, definition, segment_code FROM families WHERE code=?", (code,)).fetchone()
    if row:
        return Family(**row)
    row = conn.execute("SELECT code, title, definition, family_code FROM classes WHERE code=?", (code,)).fetchone()
    if row:
        return Class(**row)
    row = conn.execute("SELECT code, title, definition, class_code FROM commodities WHERE code=?", (code,)).fetchone()
    if row:
        return Commodity(**row)
    return None


def hierarchy(commodity_code: int) -> Optional[Hierarchy]:
    """Return the full 4-level hierarchy for a commodity code."""
    conn = get_conn()
    com = conn.execute(
        "SELECT code, title, definition, class_code FROM commodities WHERE code=?",
        (commodity_code,),
    ).fetchone()
    if not com:
        return None

    cls = conn.execute(
        "SELECT code, title, definition, family_code FROM classes WHERE code=?",
        (com["class_code"],),
    ).fetchone()
    fam = conn.execute(
        "SELECT code, title, definition, segment_code FROM families WHERE code=?",
        (cls["family_code"],),
    ).fetchone()
    seg = conn.execute(
        "SELECT code, title, definition FROM segments WHERE code=?",
        (fam["segment_code"],),
    ).fetchone()

    return Hierarchy(
        segment=Segment(**seg),
        family=Family(**fam),
        cls=Class(**cls),
        commodity=Commodity(**com),
    )


def search(query: str, limit: int = 10) -> List[MatchResult]:
    """Full-text search across commodity titles and definitions."""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT c.code, c.title, c.definition,
               rank AS score
        FROM commodities_fts
        JOIN commodities c ON c.code = commodities_fts.rowid
        WHERE commodities_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (query, limit),
    ).fetchall()
    return [
        MatchResult(
            code=r["code"],
            title=r["title"],
            definition=r["definition"],
            score=abs(r["score"]),
        )
        for r in rows
    ]
