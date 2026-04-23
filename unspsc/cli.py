"""CLI entry point: unspsc <command> [args]"""

import argparse
import json
import sys

from unspsc._lookup import hierarchy, lookup, search
from unspsc._match import match
from unspsc._models import Class, Commodity, Family, Hierarchy, MatchResult, Segment


def _node_dict(node) -> dict:
    if isinstance(node, Segment):
        return {"level": "segment", "code": node.code, "title": node.title, "definition": node.definition}
    if isinstance(node, Family):
        return {"level": "family", "code": node.code, "title": node.title, "definition": node.definition}
    if isinstance(node, Class):
        return {"level": "class", "code": node.code, "title": node.title, "definition": node.definition}
    if isinstance(node, Commodity):
        return {"level": "commodity", "code": node.code, "title": node.title, "definition": node.definition}
    return {}


def _hierarchy_dict(h: Hierarchy) -> dict:
    return {
        "segment": {"code": h.segment.code, "title": h.segment.title},
        "family": {"code": h.family.code, "title": h.family.title},
        "class": {"code": h.cls.code, "title": h.cls.title},
        "commodity": {"code": h.commodity.code, "title": h.commodity.title},
    }


def cmd_lookup(args):
    node = lookup(args.code)
    if node is None:
        print(json.dumps({"error": f"Code {args.code} not found"}))
        sys.exit(1)
    print(json.dumps(_node_dict(node), indent=2))


def cmd_hierarchy(args):
    h = hierarchy(args.code)
    if h is None:
        print(json.dumps({"error": f"Commodity code {args.code} not found"}))
        sys.exit(1)
    print(json.dumps(_hierarchy_dict(h), indent=2))


def cmd_match(args):
    results = match(args.description, limit=args.limit)
    out = [
        {"code": r.code, "title": r.title, "confidence": r.score}
        for r in results
    ]
    print(json.dumps(out, indent=2))


def cmd_search(args):
    results = search(args.query, limit=args.limit)
    out = [
        {"code": r.code, "title": r.title, "score": r.score}
        for r in results
    ]
    print(json.dumps(out, indent=2))


def main():
    parser = argparse.ArgumentParser(prog="unspsc", description="UNSPSC v26.0801 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_lookup = sub.add_parser("lookup", help="Look up a UNSPSC code at any level")
    p_lookup.add_argument("code", type=int, help="UNSPSC code (any level)")

    p_hier = sub.add_parser("hierarchy", help="Show full 4-level path for a commodity code")
    p_hier.add_argument("code", type=int, help="Commodity code")

    p_match = sub.add_parser("match", help="Fuzzy-match a description to a commodity")
    p_match.add_argument("description", help="Product or service description")
    p_match.add_argument("--limit", type=int, default=5, help="Max results (default 5)")

    p_search = sub.add_parser("search", help="Full-text search across titles and definitions")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--limit", type=int, default=10, help="Max results (default 10)")

    args = parser.parse_args()
    {"lookup": cmd_lookup, "hierarchy": cmd_hierarchy, "match": cmd_match, "search": cmd_search}[
        args.command
    ](args)


if __name__ == "__main__":
    main()
