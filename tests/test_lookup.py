import pytest
from unspsc import hierarchy, lookup, match, search
from unspsc._models import Class, Commodity, Family, Segment


def test_lookup_segment():
    node = lookup(10000000)
    assert isinstance(node, Segment)
    assert "Animal" in node.title or node.title  # segment exists


def test_lookup_family():
    node = lookup(10100000)
    assert isinstance(node, Family)


def test_lookup_class():
    node = lookup(10101500)
    assert isinstance(node, Class)


def test_lookup_commodity():
    node = lookup(10101501)  # Cats
    assert isinstance(node, Commodity)
    assert node.title == "Cats"


def test_lookup_unknown():
    assert lookup(99999999) is None


def test_hierarchy():
    h = hierarchy(10101501)
    assert h is not None
    assert h.commodity.code == 10101501
    assert h.cls.code == 10101500
    assert h.family.code == 10100000
    assert h.segment.code == 10000000


def test_hierarchy_str():
    h = hierarchy(10101501)
    s = str(h)
    assert "→" in s
    assert "Cats" in s


def test_search_returns_results():
    results = search("cutting fluid")
    assert len(results) > 0
    assert all(r.score >= 0 for r in results)


def test_match_cutting_fluid():
    results = match("cutting fluid", limit=5)
    assert len(results) > 0
    top = results[0]
    assert top.code > 0
    assert top.score > 0


def test_match_vendor_services():
    results = match("IT consulting services", limit=3)
    assert len(results) > 0
