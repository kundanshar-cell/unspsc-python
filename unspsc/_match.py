from unspsc._db import get_conn
from unspsc._models import MatchResult

try:
    from rapidfuzz import process, fuzz
    _HAS_RAPIDFUZZ = True
except ImportError:
    _HAS_RAPIDFUZZ = False

from typing import List, Optional, Tuple
_cache: Optional[List[Tuple[int, str]]] = None


def _get_titles() -> List[Tuple[int, str]]:
    global _cache
    if _cache is None:
        conn = get_conn()
        rows = conn.execute("SELECT code, title FROM commodities").fetchall()
        _cache = [(r["code"], r["title"]) for r in rows]
    return _cache


def match(description: str, limit: int = 5, threshold: float = 0.0) -> List[MatchResult]:
    """Fuzzy-match *description* against all commodity titles.

    Returns up to *limit* results with confidence score 0–100.
    Requires ``rapidfuzz`` for best performance (``pip install rapidfuzz``).
    Falls back to SQLite FTS if rapidfuzz is not installed.
    """
    if not _HAS_RAPIDFUZZ:
        from unspsc._lookup import search
        results = search(description, limit=limit)
        return results

    titles = _get_titles()
    choices = {code: title for code, title in titles}

    hits = process.extract(
        description,
        choices,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=threshold,
    )

    conn = get_conn()
    results = []
    for title, score, code in hits:
        row = conn.execute(
            "SELECT code, title, definition, class_code FROM commodities WHERE code=?", (code,)
        ).fetchone()
        if row:
            results.append(
                MatchResult(
                    code=row["code"],
                    title=row["title"],
                    definition=row["definition"],
                    score=round(score, 2),
                )
            )
    return results
