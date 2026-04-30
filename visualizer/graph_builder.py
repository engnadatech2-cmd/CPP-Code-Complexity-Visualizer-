"""
graph_builder.py
~~~~~~~~~~~~~~~~
Transforms the output.json produced by the C++ analyzer into
D3.js-ready node/edge structures for the force-directed graph.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Risk colour palette (matches SPEC exactly)
# ---------------------------------------------------------------------------
RISK_COLORS: dict[str, str] = {
    "high":   "#ef4444",
    "medium": "#f59e0b",
    "low":    "#22c55e",
}

RISK_LABELS: dict[str, str] = {
    "high":   "HIGH RISK",
    "medium": "MEDIUM RISK",
    "low":    "LOW RISK",
}


# ---------------------------------------------------------------------------
# build_nodes
# ---------------------------------------------------------------------------
def build_nodes(files: list[dict[str, Any]], max_complexity: int) -> list[dict[str, Any]]:
    """
    Convert each FileMetrics object into a D3 node.

    Node schema:
    {
        "id":          "hospital.cpp",
        "name":        "hospital.cpp",
        "complexity":  87,
        "risk":        "high",
        "color":       "#ef4444",
        "radius":      35,
        "total_lines": 450,
        "code_lines":  312,
        "function_count": 8,
        "has_circular_dep": false,
        "functions":   [...],   # top risky functions (up to 5)
        "label":       "HIGH RISK"
    }
    """
    nodes: list[dict[str, Any]] = []

    for f in files:
        complexity = f.get("complexity_score", 0)
        risk       = f.get("risk", "low")

        # Node radius: 15 (min) to 40 (max), proportional to complexity
        if max_complexity > 0:
            radius = 15 + (complexity / max_complexity) * 25
        else:
            radius = 15.0

        # Sort functions by complexity descending; keep top 5 for tooltip
        funcs = sorted(
            f.get("functions", []),
            key=lambda fn: fn.get("complexity", 0),
            reverse=True,
        )[:5]

        node: dict[str, Any] = {
            "id":              f.get("name", ""),
            "name":            f.get("name", ""),
            "path":            f.get("path", ""),
            "complexity":      complexity,
            "risk":            risk,
            "color":           RISK_COLORS.get(risk, RISK_COLORS["low"]),
            "radius":          round(radius, 1),
            "total_lines":     f.get("total_lines", 0),
            "code_lines":      f.get("code_lines", 0),
            "comment_lines":   f.get("comment_lines", 0),
            "blank_lines":     f.get("blank_lines", 0),
            "function_count":  f.get("function_count", 0),
            "has_circular_dep": f.get("has_circular_dep", False),
            "functions":       funcs,
            "label":           RISK_LABELS.get(risk, "LOW RISK"),
        }
        nodes.append(node)

    return nodes


# ---------------------------------------------------------------------------
# build_edges
# ---------------------------------------------------------------------------
def build_edges(
    dependency_graph: dict[str, Any],
    node_ids: set[str],
) -> list[dict[str, Any]]:
    """
    Convert dependency-graph edges into D3 link objects.

    Only includes edges where both source AND target are known nodes
    (avoids dangling links to system headers that were filtered out).

    Link schema:
    {
        "source":   "hospital.cpp",
        "target":   "patient.h",
        "strength": 1
    }
    """
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for raw_edge in dependency_graph.get("edges", []):
        src = raw_edge.get("from", "")
        tgt = raw_edge.get("to", "")

        if not src or not tgt:
            continue
        if src not in node_ids or tgt not in node_ids:
            continue  # skip edges to nodes not in the analysed files
        if (src, tgt) in seen:
            continue  # deduplicate

        seen.add((src, tgt))
        edges.append({"source": src, "target": tgt, "strength": 1})

    return edges


# ---------------------------------------------------------------------------
# build_graph_data  (main public entry)
# ---------------------------------------------------------------------------
def build_graph_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Top-level transformer.  Returns everything the HTML template needs.

    Returns:
    {
        "project":   "...",
        "summary":   {...},
        "nodes":     [...],
        "edges":     [...],
        "circular":  [...],    # list of cycle description strings
    }
    """
    files   = data.get("files", [])
    dep_graph = data.get("dependency_graph", {})
    summary = data.get("summary", {})

    # Compute max complexity for radius scaling
    max_complexity = max((f.get("complexity_score", 0) for f in files), default=1)
    if max_complexity == 0:
        max_complexity = 1

    nodes     = build_nodes(files, max_complexity)
    node_ids  = {n["id"] for n in nodes}
    edges     = build_edges(dep_graph, node_ids)
    circular  = dep_graph.get("circular_dependencies", [])

    return {
        "project":  data.get("project", "Unknown"),
        "analyzed_at": data.get("analyzed_at", ""),
        "analyzer_version": data.get("analyzer_version", "1.0.0"),
        "summary":  summary,
        "nodes":    nodes,
        "edges":    edges,
        "circular": circular,
    }


# ---------------------------------------------------------------------------
# load_json
# ---------------------------------------------------------------------------
def load_json(json_path: str | Path) -> dict[str, Any]:
    """Load and validate the analyzer output JSON."""
    path = Path(json_path)
    if not path.exists():
        print(f"[graph_builder] ERROR: File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        print(f"[graph_builder] ERROR: Invalid JSON in {json_path}: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI helper (for quick inspection)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python graph_builder.py <output.json>")
        sys.exit(1)

    raw = load_json(sys.argv[1])
    graph_data = build_graph_data(raw)

    print(json.dumps(graph_data, indent=2))
