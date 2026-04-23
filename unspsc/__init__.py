"""unspsc-python — UNSPSC v26.0801 lookup, hierarchy traversal, and fuzzy matching."""

from unspsc._lookup import hierarchy, lookup, search
from unspsc._match import match
from unspsc._models import Class, Commodity, Family, Hierarchy, MatchResult, Segment

__version__ = "0.1.0"
__all__ = [
    "lookup",
    "hierarchy",
    "search",
    "match",
    "Segment",
    "Family",
    "Class",
    "Commodity",
    "Hierarchy",
    "MatchResult",
]
