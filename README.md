# unspsc-python

A clean Python library for UNSPSC code lookup, hierarchy traversal, and fuzzy matching.

**UNSPSC v26.0801 · 149,849 commodities · 58 segments · zero dependencies**

---

## Why this exists

Every procurement developer eventually needs to map a product description to a UNSPSC code. The official codeset is a spreadsheet. The public tooling is a broken GitHub repo from 2019.

This library gives you a proper API — lookup by code, traverse the 4-level hierarchy, fuzzy-match a description to a commodity — in a few lines of Python.

```python
from unspsc import match

match("cutting fluid")
# → [MatchResult(code=12191507, title='Cutting oils', score=91.2), ...]
```

---

## Installation

```bash
pip install unspsc-python

# For fuzzy matching (recommended):
pip install "unspsc-python[fuzzy]"
```

---

## Quick start

### Lookup a code at any level

```python
from unspsc import lookup

lookup(10000000)  # Segment
# → Segment(code=10000000, title='Live Plant and Animal Material...', definition='...')

lookup(12191507)  # Commodity
# → Commodity(code=12191507, title='Cutting oils', definition='...', class_code=12191500)
```

### Traverse the full 4-level hierarchy

```python
from unspsc import hierarchy

h = hierarchy(12191507)
print(h)
# → 12000000 Chemicals including Bio Chemicals and Gas Materials →
#   12190000 Lubricants and oils and greases and anti corrosives →
#   12191500 Cutting and lubricating and cooling fluids →
#   12191507 Cutting oils

h.segment.title   # "Chemicals including Bio Chemicals and Gas Materials"
h.family.title    # "Lubricants and oils and greases and anti corrosives"
h.cls.title       # "Cutting and lubricating and cooling fluids"
h.commodity.title # "Cutting oils"
```

### Fuzzy-match a description

```python
from unspsc import match

results = match("industrial lubricant", limit=5)
for r in results:
    print(f"{r.code}  {r.title:<50}  score={r.score}")
```

Requires `rapidfuzz` (`pip install "unspsc-python[fuzzy]"`). Falls back to full-text search if not installed.

### Full-text search

```python
from unspsc import search

results = search("consulting services", limit=10)
for r in results:
    print(r.code, r.title)
```

---

## CLI

```bash
# Lookup any code
unspsc lookup 12191507

# Show full hierarchy
unspsc hierarchy 12191507

# Fuzzy-match a description
unspsc match "cutting fluid" --limit 5

# Full-text search
unspsc search "lubricant" --limit 10
```

All commands output JSON.

---

## UNSPSC hierarchy

UNSPSC organises all products and services into four levels:

| Level | Example code | Example title |
|-------|-------------|---------------|
| Segment | `12000000` | Chemicals including Bio Chemicals |
| Family | `12190000` | Lubricants and oils and greases |
| Class | `12191500` | Cutting and lubricating fluids |
| Commodity | `12191507` | Cutting oils |

---

## Data source

Codeset: **UNSPSC UNv26.0801** (August 2023)  
Publisher: [United Nations Development Programme (UNDP)](https://www.undp.org/unspsc)  
Free download: https://www.undp.org/unspsc  
UNSPSC® is a registered trademark of UNDP.

The bundled database (`data/unspsc.db.gz`) is built from the official UNDP codeset.  
To rebuild from a newer version:

```bash
python scripts/build_db.py path/to/unspsc-english-vXX.xlsx
```

---

## Roadmap

- [ ] Oracle Fusion + Coupa code mapping
- [ ] `hierarchy()` for segment/family/class codes (not just commodity)
- [ ] Batch match via CSV input
- [ ] Confidence threshold filtering in `match()`
- [ ] Parquet export of the full codeset

---

## Contributing

PRs welcome. Open an issue first for anything beyond a small fix.

```bash
git clone https://github.com/kundanshar-cell/unspsc-python
cd unspsc-python
pip install -e ".[dev]"
pytest
```

---

## License

MIT — see [LICENSE](LICENSE)

UNSPSC® is a registered trademark of UNDP. The codeset is published by UNDP under free-access terms at https://www.undp.org/unspsc.

---

*Built by [Kundan Sharma](https://github.com/kundanshar-cell) — IT & Digital Solution Architect with 15 years in enterprise procurement and ERP.*
