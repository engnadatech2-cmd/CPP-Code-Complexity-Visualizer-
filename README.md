# 🔍 C++ Code Complexity Visualizer

> "Point it at any C++ codebase and get an interactive complexity map in seconds."

A static analyzer written in C++17 that reads a folder of `.cpp` and `.h` files,
calculates Cyclomatic Complexity for every function, maps `#include` dependencies,
and produces a self-contained interactive HTML report powered by D3.js.

---

## The Problem

Large C++ codebases hide complexity debt in plain sight. Functions grow, branches
multiply, and nobody notices until a bug appears in the most tangled corner of the
codebase. Code-review tools catch style; linters catch syntax. But **which function
is the single riskiest thing you own?** That question usually has no fast answer.

This tool makes it a one-command operation.

---

## Demo

```bash
# 1. Build
make

# 2. Analyze any folder
./analyzer/analyzer --path ./MyProject --name "My Project" --output output/report.json

# 3. Generate & open the interactive report
python3 visualizer/html_generator.py output/report.json
```

The browser opens a dark-themed dashboard with:

- A **force-directed dependency graph** — nodes sized by complexity, color-coded by risk
- A **hero stats panel** — avg CC, total functions, max CC, riskiest function
- A **per-file function list** — every function with its CC score at a glance
- **Click-to-inspect** — click any graph node to see file details and top risky functions

---

## Features

- **Comment-safe analysis** — a 4-state machine strips `//`, `/* */`, and string literals
  before analysis, so keywords inside strings never inflate complexity scores
- **Cyclomatic Complexity** — per-function CC using branch-keyword counting
  (`if`, `for`, `while`, `do`, `case`, `catch`, `&&`, `||`, `?`)
- **Risk classification** — `low` (CC 1–5), `medium` (CC 6–10), `high` (CC 11+)
- **Deep-nesting detection** — nesting depth ≥ 4 adds a risk reason independently
- **Dependency graph** — maps `#include` relationships; ignores `<system>` headers
- **Circular dependency detection** — DFS across the full graph, highlighted in red
- **Zero C++ dependencies** — no external libraries; JSON is built manually
- **Self-contained HTML report** — one `.html` file, no server needed

---

## Architecture

```
INPUT: A folder of .cpp / .h files
        │
        ▼
┌─────────────────────────────────────┐
│         C++17 ANALYZER              │
│                                     │
│  CommentStripper   (4-state machine)│
│         ↓  clean source             │
│  MetricsCalculator (CC + nesting)   │
│         ↓  FileMetrics              │
│  DependencyGraph   (unordered_map)  │
│         ↓  graph edges              │
│  JsonExporter      (output.json)    │
└─────────────────────────────────────┘
              ↓ output.json
┌─────────────────────────────────────┐
│         PYTHON LAYER                │
│  graph_builder.py  → D3-ready data  │
│  html_generator.py → report.html    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      D3.js VISUALIZATION            │
│  Force-directed graph               │
│  Color-coded risk levels            │
│  Click → file & function details    │
│  Hero stats dashboard               │
└─────────────────────────────────────┘
```

---

## File Structure

```
complexity-visualizer/
├── analyzer/
│   ├── main.cpp
│   ├── comment_stripper.h / .cpp
│   ├── metrics_calculator.h / .cpp
│   ├── dependency_graph.h / .cpp
│   └── json_exporter.h / .cpp
├── visualizer/
│   ├── graph_builder.py
│   └── html_generator.py
├── tests/
│   ├── test_comment_stripper.cpp
│   ├── test_metrics.cpp
│   └── sample_files/
│       ├── simple.cpp
│       ├── with_comments.cpp
│       └── complex.cpp
├── output/            ← generated reports land here
├── Makefile
└── README.md
```

---

## Installation

**Requirements:**

- `g++` with C++17 support (GCC 8+ or Clang 7+)
- Python 3.8+
- No external C++ or Python libraries needed

```bash
git clone https://github.com/nada/complexity-visualizer.git
cd complexity-visualizer
make
```

---

## Usage

```bash
# Analyze a project folder
./analyzer/analyzer --path /path/to/project

# With a custom project name and output path
./analyzer/analyzer \
    --path ./HospitalSystem \
    --name "Hospital System" \
    --output output/hospital.json

# Generate the interactive HTML report
python3 visualizer/html_generator.py output/hospital.json

# Run unit tests
make test

# Quick demo on the included sample files
make demo
```

**CLI options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--path <dir>` | Directory to analyze | *(required)* |
| `--name <name>` | Project display name | directory basename |
| `--output <file>` | JSON output path | `output/output.json` |
| `--help` | Show help message | — |

---

## JSON Contract

The C++ analyzer produces a JSON file that the Python layer reads. Its shape
is fixed — do not change it without updating both sides.

```json
{
  "project": "HospitalSystem",
  "analyzed_at": "2026-04-29T14:30:00",
  "analyzer_version": "1.0.0",
  "summary": {
    "total_files": 5,
    "total_functions": 23,
    "total_lines": 1240,
    "avg_complexity": 4.2,
    "max_complexity": 15,
    "riskiest_file": "hospital.cpp",
    "riskiest_function": "processAdmission",
    "high_risk_count": 3,
    "medium_risk_count": 7,
    "low_risk_count": 13
  },
  "files": [ ... ],
  "dependency_graph": {
    "nodes": [...],
    "edges": [{"from": "...", "to": "..."}],
    "circular_dependencies": []
  }
}
```

---

## Technical Decisions

**Why a state machine for comment stripping?**
A naive regex approach misfires on `//` inside strings, `/*` inside
line comments, and multi-line block comments. The 4-state machine
(`CODE → LINE_COMMENT / BLOCK_COMMENT / STRING`) handles all edge cases
cleanly with O(n) time and O(1) state.

**Why brace counting for function detection instead of a full parser?**
A full C++ parser would require a lexer, preprocessor, and grammar — effectively
a compiler front-end. Brace counting after signature detection gives ~95% accuracy
on well-formatted C++17 code with far less complexity, which is the right trade-off
for a standalone tool.

**Why zero external C++ dependencies?**
Keeping the analyzer dependency-free means it builds with a single `g++` command on
any machine. Tools like `nlohmann/json` or `libclang` are excellent but add friction
to setup and complicate cross-platform builds.

**Why D3.js for the report instead of a charting library?**
Force-directed graphs need full control over physics (link strength, charge, collision).
D3's simulation API exposes exactly that. The result is embedded inline in the HTML so
the report is a single portable file with no CDN dependency at runtime.

---

## CV-Ready Bullets

- Engineered a C++17 static analyzer using a 4-state machine to accurately strip
  comments and string literals before analysis, eliminating false positives in
  complexity calculations.

- Implemented Cyclomatic Complexity analysis across C++ codebases using brace-counting
  and branch-keyword detection, producing per-function risk ratings (low / medium / high).

- Built a dependency graph using `std::unordered_map` to map `#include` relationships
  across files, with DFS-based circular dependency detection.

- Designed a zero-dependency JSON exporter bridging the C++ analyzer to a Python/D3.js
  visualization layer, producing interactive force-directed HTML reports with
  color-coded risk levels.

- Delivered a self-contained HTML report with D3.js force-directed graph — nodes sized
  by complexity score, colored by risk level, with click-to-inspect function details.

---

## About

Built by **Nada** as a portfolio project demonstrating systems programming, static
analysis, data pipeline design, and interactive visualization — all in one tool.

Tested on a real Hospital Management System codebase.
