# unspsc-python

> *UNSPSC v26.0801 · 149,849 commodities · lookup, hierarchy traversal, fuzzy matching · zero dependencies*

---

## The Friday Afternoon Problem

Sarah is a developer at a mid-sized manufacturing company. Her manager just asked her to build a tool that automatically tags every purchase order line with a spend category.

Simple enough, she thinks.

She opens Google. Searches **"UNSPSC Python library"**.

Nothing. A broken GitHub repo from 2019 with 3 stars. A CSV someone uploaded to Kaggle. A StackOverflow answer with a dead link.

She spends two hours just trying to understand the UNSPSC hierarchy. Segment → Family → Class → Commodity. Four levels. 55,000 codes. No clean API. No lookup function. No fuzzy match.

She gives up and hard-codes 40 categories manually.

It breaks the first week when a PO comes in for **"cutting fluid"** and the system doesn't know where to put it.

Then someone points her to `unspsc-python`.

```python
from unspsc import match

match("cutting fluid")
# → [MatchResult(code=12191507, title='Cutting oils', score=91.2), ...]
```

Twenty minutes. Done. She goes home on time.

---

## Installation

```bash
pip install unspsc-python

# With fuzzy matching (recommended — powers match()):
pip install "unspsc-python[fuzzy]"
```

---

## What you can do

### Look up any UNSPSC code

```python
from unspsc import lookup

lookup(12191507)
# → Commodity(code=12191507, title='Cutting oils', definition='...', class_code=12191500)

lookup(12000000)
# → Segment(code=12000000, title='Chemicals including Bio Chemicals and Gas Materials', ...)
```

Works at all four levels — segment, family, class, or commodity.

---

### Traverse the full hierarchy

Sarah's manager then asks: *"Can you also show me where each category sits in the tree?"*

```python
from unspsc import hierarchy

h = hierarchy(12191507)
print(h)
# 12000000 Chemicals including Bio Chemicals and Gas Materials →
# 12190000 Lubricants and oils and greases and anti corrosives →
# 12191500 Cutting and lubricating and cooling fluids →
# 12191507 Cutting oils

h.segment.title    # "Chemicals including Bio Chemicals and Gas Materials"
h.family.title     # "Lubricants and oils and greases and anti corrosives"
h.cls.title        # "Cutting and lubricating and cooling fluids"
h.commodity.title  # "Cutting oils"
```

---

### Fuzzy-match a description to a commodity

This is the piece that saves Sarah's Friday afternoon. She feeds raw PO line descriptions directly — no pre-cleaning required.

```python
from unspsc import match

results = match("industrial lubricant", limit=5)
for r in results:
    print(f"{r.code}  {r.title:<50}  score={r.score}")
```

Powered by [rapidfuzz](https://github.com/rapidfuzz/RapidFuzz). Falls back to SQLite full-text search if not installed.

---

### Full-text search

```python
from unspsc import search

results = search("consulting services", limit=10)
for r in results:
    print(r.code, r.title)
```

---

## CLI — for the command line and shell scripts

```bash
# Look up a code
unspsc lookup 12191507

# Show full 4-level hierarchy
unspsc hierarchy 12191507

# Fuzzy-match a description
unspsc match "cutting fluid" --limit 5

# Full-text search
unspsc search "lubricant" --limit 10
```

All commands output clean JSON — pipe them into anything.

---

## The UNSPSC hierarchy

Every product and service in the world fits into four levels:

| Level | Digits | Example code | Example title |
|-------|--------|-------------|---------------|
| Segment | 1–2 | `12000000` | Chemicals including Bio Chemicals |
| Family | 3–4 | `12190000` | Lubricants and oils and greases |
| Class | 5–6 | `12191500` | Cutting and lubricating fluids |
| Commodity | 7–8 | `12191507` | Cutting oils |

---

## The researcher who couldn't evaluate anything

James is writing his PhD on LLMs for enterprise document understanding. He needs to benchmark GPT-4, Claude, and Llama on procurement tasks.

Does the model correctly interpret a purchase order? Can it spot a pricing anomaly? Does it know what a blanket order is?

He has no dataset. None exists publicly. He has to build one himself — which means needing domain knowledge he doesn't have.

He posts on Reddit: *"Does anyone have a procurement Q&A dataset for LLM evaluation?"*

Nothing.

He ends up writing 200 generic questions that don't actually test real procurement understanding. His paper is weaker for it.

If James had found this library first, he would have had the full UNSPSC taxonomy at his fingertips — 149,849 commodities, definitions, hierarchy — to build his dataset from.

The companion project **[procurement-benchmarks](https://github.com/kundanshar-cell/procurement-benchmarks)** is being built for James. 500 real-world Q&A pairs for benchmarking LLMs on procurement domain accuracy.

---

## Data source

**UNSPSC UNv26.0801** — released August 2023  
Publisher: [United Nations Development Programme (UNDP)](https://www.undp.org/unspsc)  
Free download: https://www.undp.org/unspsc  

> UNSPSC® is a registered trademark of UNDP.

The bundled database (`data/unspsc.db.gz`, 11 MB compressed) is built from the official UNDP codeset. To rebuild from a newer version:

```bash
python scripts/build_db.py path/to/unspsc-english-vXX.xlsx
```

---

## Roadmap

- [ ] `hierarchy()` support for segment / family / class codes (not just commodity)
- [ ] Batch match from CSV — tag an entire PO extract in one command
- [ ] Oracle Fusion and Coupa code mapping
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
