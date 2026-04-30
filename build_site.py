#!/usr/bin/env python3
"""
Generates the complete learning-hub/ static site for the
C++ Code Complexity Visualizer — by Nada.
"""
import os

BASE = "learning-hub"

# ─────────────────────────────────────────────────────────────
# SHARED CSS
# ─────────────────────────────────────────────────────────────
SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg:          #fffcf8;
    --surface:     #ffffff;
    --sidebar-bg:  #f7f5ff;
    --border:      #ebe7ff;
    --accent:      #5b4ef8;
    --accent-2:    #4338ca;
    --accent-light:#edeaff;
    --text:        #1a1523;
    --text-muted:  #6b7280;
    --code-bg:     #f8fafc;
    --code-border: #e2e8f0;
    --high:        #ef4444;
    --high-bg:     #fef2f2;
    --med:         #f59e0b;
    --med-bg:      #fffbeb;
    --low:         #22c55e;
    --low-bg:      #f0fdf4;
    --ph1: #6366f1; --ph1-bg: #eef2ff;
    --ph2: #ec4899; --ph2-bg: #fdf2f8;
    --ph3: #14b8a6; --ph3-bg: #f0fdfa;
    --ph4: #f97316; --ph4-bg: #fff7ed;
    --ph5: #8b5cf6; --ph5-bg: #f5f3ff;
}

*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.75;
    min-height: 100vh;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Layout ─────────────────────────────────────────── */
.layout { display: flex; min-height: 100vh; }

/* ── Sidebar ─────────────────────────────────────────── */
.sidebar {
    width: 270px; min-width: 270px;
    background: var(--sidebar-bg);
    border-right: 1.5px solid var(--border);
    position: sticky; top: 0;
    height: 100vh; overflow-y: auto;
    flex-shrink: 0;
    padding-bottom: 40px;
}

.sidebar-brand {
    padding: 22px 20px 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 10px;
}

.sidebar-brand a {
    display: flex; align-items: center; gap: 10px;
    color: var(--text); text-decoration: none;
}

.brand-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--accent), #818cf8);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 900; color: white;
    flex-shrink: 0;
}

.brand-text { line-height: 1.25; }
.brand-text strong { display: block; font-size: 13px; font-weight: 800; }
.brand-text span { font-size: 11px; color: var(--text-muted); }

.sb-section { margin-bottom: 4px; }

.sb-label {
    padding: 8px 20px 4px;
    font-size: 10px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 1.2px;
    color: var(--text-muted);
}

.sidebar nav a {
    display: flex; align-items: center; gap: 8px;
    padding: 7px 20px;
    font-size: 13px; font-weight: 500;
    color: var(--text-muted);
    border-left: 3px solid transparent;
    transition: all 0.15s;
    text-decoration: none;
}

.sidebar nav a:hover {
    color: var(--accent);
    background: var(--accent-light);
    border-left-color: var(--accent);
    text-decoration: none;
}

.sidebar nav a.active {
    color: var(--accent); font-weight: 700;
    background: var(--accent-light);
    border-left-color: var(--accent);
}

.ph-dot {
    width: 20px; height: 20px; border-radius: 7px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 9px; font-weight: 800; color: white;
    flex-shrink: 0;
}

.sidebar nav a.sub { padding-left: 48px; font-size: 12.5px; }

/* ── Main ───────────────────────────────────────────── */
.main { flex: 1; padding: 52px 60px; max-width: 880px; }

@media (max-width: 900px) {
    .sidebar { display: none; }
    .main { padding: 28px 20px; max-width: 100%; }
    .compare { grid-template-columns: 1fr; }
}

/* ── Page header ────────────────────────────────────── */
.breadcrumb {
    display: flex; align-items: center; gap: 6px;
    font-size: 12px; color: var(--text-muted);
    margin-bottom: 12px;
}
.breadcrumb a { color: var(--accent); }
.breadcrumb span { color: var(--text-muted); }

.phase-tag {
    display: inline-block;
    padding: 4px 12px; border-radius: 20px;
    font-size: 10.5px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.6px;
    margin-bottom: 12px;
}

.page-title {
    font-size: 36px; font-weight: 800; line-height: 1.2;
    margin-bottom: 14px; letter-spacing: -0.5px;
}

.page-subtitle {
    font-size: 16.5px; color: var(--text-muted);
    max-width: 580px; margin-bottom: 40px;
    font-weight: 400; line-height: 1.6;
}

/* ── Sections ───────────────────────────────────────── */
.section { margin-bottom: 48px; }

.section h2 {
    font-size: 21px; font-weight: 800;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border);
}

.section h3 {
    font-size: 16px; font-weight: 700;
    margin: 24px 0 10px; color: var(--text);
}

.section p { font-size: 15px; color: #374151; margin-bottom: 14px; line-height: 1.8; }

ul, ol { padding-left: 22px; margin-bottom: 14px; }
li { font-size: 15px; color: #374151; margin-bottom: 6px; line-height: 1.75; }

/* ── Code ───────────────────────────────────────────── */
pre {
    background: var(--code-bg);
    border: 1.5px solid var(--code-border);
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
    margin: 16px 0 20px;
    font-size: 13px;
    line-height: 1.75;
    position: relative;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.code-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 18px;
    background: #f1f5f9;
    border-bottom: 1px solid var(--code-border);
    font-size: 11.5px; font-weight: 600;
    color: var(--text-muted);
    font-family: 'Fira Code', monospace;
}

.code-header .dots { display: flex; gap: 5px; }
.code-header .dots span { width: 11px; height: 11px; border-radius: 50%; }
.code-header .dots span:nth-child(1) { background: #fc5555; }
.code-header .dots span:nth-child(2) { background: #fcbc40; }
.code-header .dots span:nth-child(3) { background: #28c840; }

.code-body {
    padding: 18px 22px;
    overflow-x: auto;
    font-family: 'Fira Code', monospace;
    color: #334155;
}

code {
    font-family: 'Fira Code', monospace;
    font-size: 13px;
    background: var(--accent-light);
    color: var(--accent-2);
    padding: 2px 7px; border-radius: 5px;
}

pre code { background: none; padding: 0; color: inherit; font-size: inherit; border-radius: 0; }

/* Syntax coloring */
.kw  { color: #7c3aed; font-weight: 600; }
.ty  { color: #0369a1; }
.fn  { color: #0f766e; font-weight: 500; }
.st  { color: #16a34a; }
.cm  { color: #9ca3af; font-style: italic; }
.nm  { color: #ea580c; }
.op  { color: #dc2626; }

/* ── Callouts ───────────────────────────────────────── */
.callout {
    border-radius: 12px; padding: 16px 20px;
    margin: 18px 0; border-left: 4px solid;
    font-size: 14.5px; line-height: 1.7;
}
.callout > strong { display: block; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 5px; }
.callout.info  { background: #eff6ff; border-color: #3b82f6; color: #1e40af; }
.callout.tip   { background: #f0fdf4; border-color: #22c55e; color: #15803d; }
.callout.warn  { background: #fffbeb; border-color: #f59e0b; color: #92400e; }
.callout.key   { background: var(--accent-light); border-color: var(--accent); color: #3730a3; }

/* ── Comparison cards ───────────────────────────────── */
.compare {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 18px; margin: 20px 0;
}

.cmp-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 14px; overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.cmp-card .cmp-head {
    padding: 12px 18px;
    font-size: 12px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.6px;
    display: flex; align-items: center; gap: 8px;
    color: white;
}

.cmp-card.python .cmp-head { background: #2563eb; }
.cmp-card.cpp .cmp-head { background: #7c3aed; }
.cmp-card.good .cmp-head { background: #16a34a; }
.cmp-card.bad  .cmp-head { background: #dc2626; }

.cmp-card .cmp-body { padding: 16px 18px; font-size: 13.5px; }
.cmp-card .cmp-body p { margin-bottom: 8px; font-size: 13.5px; }

/* ── Diagram box ────────────────────────────────────── */
.diagram {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 14px; padding: 28px 32px;
    margin: 20px 0;
    font-family: 'Fira Code', monospace;
    font-size: 13px; line-height: 1.9;
    color: #334155;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    overflow-x: auto;
}

/* ── Metric cards ───────────────────────────────────── */
.metric-row { display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }

.metric {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 14px; padding: 18px 22px;
    min-width: 140px; flex: 1;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

.metric .metric-val {
    font-size: 28px; font-weight: 800;
    line-height: 1.1; margin-bottom: 4px;
}

.metric .metric-lbl { font-size: 12px; color: var(--text-muted); font-weight: 500; }

/* ── Risk badges ────────────────────────────────────── */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 11.5px; font-weight: 700;
}
.badge.high { background: var(--high-bg); color: var(--high); }
.badge.med  { background: var(--med-bg);  color: #d97706; }
.badge.low  { background: var(--low-bg);  color: #16a34a; }

/* ── Step list ──────────────────────────────────────── */
.steps { list-style: none; padding: 0; }
.steps li {
    display: flex; gap: 16px; align-items: flex-start;
    padding: 14px 0; border-bottom: 1px solid var(--border);
    font-size: 14.5px;
}
.steps li:last-child { border-bottom: none; }
.step-num {
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--accent); color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 800; flex-shrink: 0; margin-top: 1px;
}

/* ── Card grid ──────────────────────────────────────── */
.card-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px; margin: 20px 0;
}

.card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 14px; padding: 22px 20px;
    text-decoration: none; color: var(--text);
    transition: all 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    display: block;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(91,78,248,0.14);
    border-color: var(--accent);
    text-decoration: none;
}

.card .card-icon { font-size: 30px; margin-bottom: 12px; }
.card .card-title { font-size: 14px; font-weight: 700; margin-bottom: 5px; }
.card .card-desc  { font-size: 12.5px; color: var(--text-muted); line-height: 1.5; }

/* ── Table ──────────────────────────────────────────── */
.tbl { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; border-radius: 12px; overflow: hidden; border: 1.5px solid var(--border); }
.tbl th { background: var(--sidebar-bg); padding: 11px 16px; text-align: left; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: var(--text-muted); }
.tbl td { padding: 11px 16px; border-bottom: 1px solid var(--border); }
.tbl tr:last-child td { border-bottom: none; }
.tbl tr:hover td { background: var(--sidebar-bg); }

/* ── Q&A (Phase 5) ──────────────────────────────────── */
.qa-item { margin-bottom: 28px; }
.qa-q {
    background: var(--accent); color: white;
    border-radius: 10px 10px 0 0;
    padding: 14px 20px;
    font-size: 15px; font-weight: 700;
    display: flex; align-items: flex-start; gap: 10px;
}
.qa-q::before { content: "Q"; background: rgba(255,255,255,0.25); border-radius: 6px; padding: 1px 8px; font-size: 11px; font-weight: 800; margin-top: 2px; flex-shrink: 0; }
.qa-a {
    background: var(--surface);
    border: 1.5px solid var(--border); border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 18px 20px;
    font-size: 14.5px; line-height: 1.75;
}
.qa-a strong { color: var(--accent); }

/* ── Interview tip ──────────────────────────────────── */
.int-tip {
    background: #fff7ed; border: 1.5px solid #fed7aa;
    border-radius: 10px; padding: 12px 16px;
    font-size: 13px; color: #92400e; margin-top: 10px;
}
.int-tip::before { content: "💡 Interview tip: "; font-weight: 700; }

/* ── Scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

/* ── Footer ─────────────────────────────────────────── */
.page-footer {
    margin-top: 60px; padding-top: 24px;
    border-top: 2px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    font-size: 13px; color: var(--text-muted);
}
"""

# ─────────────────────────────────────────────────────────────
# SIDEBAR NAV
# ─────────────────────────────────────────────────────────────
def sidebar(active=""):
    nav_items = [
        ("home", "🏠", "", "index.html", "Overview", ""),
        # Phase 1
        ("p1",   "1", "ph1", "phase1/index.html", "Phase 1 — C++17 Deep Dive", "ph1"),
        ("p1-str","1","ph1", "phase1/string-vs-python.html", "std::string vs Python str", "sub"),
        ("p1-fio","1","ph1", "phase1/file-io.html", "File I/O in C++", "sub"),
        ("p1-map","1","ph1", "phase1/unordered-map.html", "unordered_map Internals", "sub"),
        ("p1-sc", "1","ph1", "phase1/struct-vs-class.html", "struct vs class", "sub"),
        ("p1-cr", "1","ph1", "phase1/const-references.html", "const & References", "sub"),
        ("p1-raii","1","ph1","phase1/raii.html", "RAII", "sub"),
        ("p1-vd", "1","ph1", "phase1/vector-vs-deque.html", "vector vs deque", "sub"),
        ("p1-rx", "1","ph1", "phase1/regex.html", "std::regex", "sub"),
        ("p1-tpl","1","ph1", "phase1/templates.html", "Templates", "sub"),
        ("p1-js", "1","ph1", "phase1/json-output.html", "JSON Output", "sub"),
        # Phase 2
        ("p2",   "2", "ph2", "phase2/index.html", "Phase 2 — Architecture", "ph2"),
        # Phase 3
        ("p3",   "3", "ph3", "phase3/index.html", "Phase 3 — File Walkthrough", "ph3"),
        ("p3-cs","3","ph3", "phase3/comment-stripper.html", "comment_stripper.cpp", "sub"),
        ("p3-mc","3","ph3", "phase3/metrics-calculator.html", "metrics_calculator.cpp", "sub"),
        ("p3-dg","3","ph3", "phase3/dependency-graph.html", "dependency_graph.cpp", "sub"),
        ("p3-je","3","ph3", "phase3/json-exporter.html", "json_exporter.cpp", "sub"),
        ("p3-m", "3","ph3", "phase3/main-cpp.html", "main.cpp", "sub"),
        ("p3-gb","3","ph3", "phase3/graph-builder-py.html", "graph_builder.py", "sub"),
        ("p3-hg","3","ph3", "phase3/html-generator-py.html", "html_generator.py", "sub"),
        ("p3-vz","3","ph3", "phase3/viz-js.html", "D3.js Visualization", "sub"),
        # Phase 4
        ("p4",   "4", "ph4", "phase4/index.html", "Phase 4 — Algorithms", "ph4"),
        ("p4-cc","4","ph4", "phase4/cyclomatic-complexity.html", "Cyclomatic Complexity", "sub"),
        ("p4-sm","4","ph4", "phase4/state-machine.html", "State Machine", "sub"),
        ("p4-gt","4","ph4", "phase4/graph-traversal.html", "DFS Traversal", "sub"),
        ("p4-d3","4","ph4", "phase4/d3-simulation.html", "D3.js Force Simulation", "sub"),
        # Phase 5
        ("p5",   "5", "ph5", "phase5/index.html", "Phase 5 — Interview Q&A", "ph5"),
    ]

    def prefix_for(page_id, file_path):
        if "phase1" in file_path: return "../"
        if "phase2" in file_path: return "../"
        if "phase3" in file_path: return "../"
        if "phase4" in file_path: return "../"
        if "phase5" in file_path: return "../"
        return ""

    html = '<div class="sidebar">\n'
    html += '''<div class="sidebar-brand">
  <a href="{home}">
    <div class="brand-icon">C<span style="font-size:11px">++</span></div>
    <div class="brand-text">
      <strong>Complexity Visualizer</strong>
      <span>Learning Hub</span>
    </div>
  </a>
</div>\n'''

    current_phase = active.split("-")[0] if "-" in active else active

    # Build items
    html += '<nav>\n'
    for (item_id, num, ph_cls, href, label, kind) in nav_items:
        is_active = "active" if item_id == active else ""
        css_class = f"active " if is_active else ""
        if kind == "sub":
            css_class += "sub"
        if kind in ("ph1","ph2","ph3","ph4","ph5"):
            # Section header style
            color_map = {"ph1":"#6366f1","ph2":"#ec4899","ph3":"#14b8a6","ph4":"#f97316","ph5":"#8b5cf6"}
            c = color_map.get(ph_cls, "#6366f1")
            html += f'<a href="{{prefix}}{href}" class="{css_class.strip()}">'
            html += f'<span class="ph-dot" style="background:{c}">{num}</span> {label}</a>\n'
        elif kind == "sub":
            html += f'<a href="{{prefix}}{href}" class="{css_class.strip()}">{label}</a>\n'
        else:
            html += f'<a href="{{prefix}}{href}" class="{css_class.strip()}">{label}</a>\n'
    html += '</nav>\n</div>\n'
    return html


def make_page(title, subtitle, phase_tag, phase_color, breadcrumb_items, content, active_id="", in_subfolder=False):
    prefix = "../" if in_subfolder else ""
    home_link = f"{prefix}index.html"

    # Build breadcrumb
    bc_parts = []
    for (bc_label, bc_href) in breadcrumb_items:
        if bc_href:
            bc_parts.append(f'<a href="{prefix}{bc_href}">{bc_label}</a>')
        else:
            bc_parts.append(f'<span>{bc_label}</span>')
    breadcrumb_html = ' <span>›</span> '.join(bc_parts) if bc_parts else ''

    # Phase tag style
    phase_styles = {
        "Phase 1": "background:#eef2ff; color:#4338ca;",
        "Phase 2": "background:#fdf2f8; color:#be185d;",
        "Phase 3": "background:#f0fdfa; color:#0f766e;",
        "Phase 4": "background:#fff7ed; color:#c2410c;",
        "Phase 5": "background:#f5f3ff; color:#6d28d9;",
        "Overview": "background:#fafafa; color:#374151;",
    }
    tag_style = phase_styles.get(phase_tag, "background:#eef2ff; color:#4338ca;")

    # Build sidebar nav with correct prefix
    nav_items = [
        ("home", "", "index.html", "🏠 Overview", ""),
        ("p1",   "ph1", "phase1/index.html", "⚙️ Phase 1 — C++17", "ph1"),
        ("p1-str","ph1", "phase1/string-vs-python.html", "std::string vs Python str", "sub"),
        ("p1-fio","ph1", "phase1/file-io.html", "File I/O in C++", "sub"),
        ("p1-map","ph1", "phase1/unordered-map.html", "unordered_map", "sub"),
        ("p1-sc", "ph1", "phase1/struct-vs-class.html", "struct vs class", "sub"),
        ("p1-cr", "ph1", "phase1/const-references.html", "const & References", "sub"),
        ("p1-raii","ph1","phase1/raii.html", "RAII", "sub"),
        ("p1-vd", "ph1", "phase1/vector-vs-deque.html", "vector vs deque", "sub"),
        ("p1-rx", "ph1", "phase1/regex.html", "std::regex", "sub"),
        ("p1-tpl","ph1", "phase1/templates.html", "Templates", "sub"),
        ("p1-js", "ph1", "phase1/json-output.html", "JSON Output", "sub"),
        ("p2",   "ph2", "phase2/index.html", "🏗️ Phase 2 — Architecture", "ph2"),
        ("p3",   "ph3", "phase3/index.html", "📁 Phase 3 — File Walkthrough", "ph3"),
        ("p3-cs","ph3", "phase3/comment-stripper.html", "comment_stripper.cpp", "sub"),
        ("p3-mc","ph3", "phase3/metrics-calculator.html", "metrics_calculator.cpp", "sub"),
        ("p3-dg","ph3", "phase3/dependency-graph.html", "dependency_graph.cpp", "sub"),
        ("p3-je","ph3", "phase3/json-exporter.html", "json_exporter.cpp", "sub"),
        ("p3-m", "ph3", "phase3/main-cpp.html", "main.cpp", "sub"),
        ("p3-gb","ph3", "phase3/graph-builder-py.html", "graph_builder.py", "sub"),
        ("p3-hg","ph3", "phase3/html-generator-py.html", "html_generator.py", "sub"),
        ("p3-vz","ph3", "phase3/viz-js.html", "D3.js Visualization", "sub"),
        ("p4",   "ph4", "phase4/index.html", "🔢 Phase 4 — Algorithms", "ph4"),
        ("p4-cc","ph4", "phase4/cyclomatic-complexity.html", "Cyclomatic Complexity", "sub"),
        ("p4-sm","ph4", "phase4/state-machine.html", "State Machine", "sub"),
        ("p4-gt","ph4", "phase4/graph-traversal.html", "DFS Traversal", "sub"),
        ("p4-d3","ph4", "phase4/d3-simulation.html", "D3.js Force Simulation", "sub"),
        ("p5",   "ph5", "phase5/index.html", "🎤 Phase 5 — Interview Q&A", "ph5"),
    ]
    ph_colors = {"ph1":"#6366f1","ph2":"#ec4899","ph3":"#14b8a6","ph4":"#f97316","ph5":"#8b5cf6"}

    nav_html = ""
    for item in nav_items:
        item_id, ph_cls, href, label, kind = item
        is_active = "active" if item_id == active_id else ""
        css_class = f"{is_active} {kind if kind == 'sub' else ''}".strip()
        c = ph_colors.get(ph_cls, "#6366f1")
        if kind in ("ph1","ph2","ph3","ph4","ph5"):
            num = ph_cls[-1]
            nav_html += f'<a href="{prefix}{href}" class="{css_class}"><span class="ph-dot" style="background:{c}">{num}</span> {label}</a>\n'
        else:
            nav_html += f'<a href="{prefix}{href}" class="{css_class}">{label}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | C++ Complexity Visualizer — Learning Hub</title>
<style>{SHARED_CSS}</style>
</head>
<body>
<div class="layout">

  <!-- Sidebar -->
  <div class="sidebar">
    <div class="sidebar-brand">
      <a href="{home_link}">
        <div class="brand-icon">C<span style="font-size:10px">++</span></div>
        <div class="brand-text">
          <strong>Complexity Viz</strong>
          <span>Learning Hub · by Nada</span>
        </div>
      </a>
    </div>
    <nav>
{nav_html}    </nav>
  </div>

  <!-- Main content -->
  <main class="main">
    <div class="breadcrumb">{breadcrumb_html}</div>
    <div class="phase-tag" style="{tag_style}">{phase_tag}</div>
    <h1 class="page-title">{title}</h1>
    <p class="page-subtitle">{subtitle}</p>

{content}

    <div class="page-footer">
      <span>C++ Code Complexity Visualizer — Learning Hub</span>
      <a href="{home_link}">← Back to Home</a>
    </div>
  </main>

</div>
</body>
</html>"""


def codeblock(filename, code):
    return f"""<div class="code-block-wrap">
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>{filename}</span></div><div class="code-body">{code}</div></pre>
</div>"""


# ═════════════════════════════════════════════════════════════
# PAGE CONTENT
# ═════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────
# index.html — Overview
# ─────────────────────────────────────────────────────────────
INDEX_CONTENT = """
<div class="section">
  <h2>🔍 What does this project do?</h2>
  <p>Imagine you have a big C++ codebase — hundreds of files, thousands of functions. How do you know <em>which function is the most dangerous</em> to modify? Which one is so complicated that a small change could break everything?</p>
  <p>This tool is the answer. You point it at any folder of <code>.cpp</code> and <code>.h</code> files, and it gives you:</p>
  <ul>
    <li>📊 A <strong>complexity score</strong> for every single function</li>
    <li>🚦 A <strong>risk rating</strong> (low / medium / high) for every function and file</li>
    <li>🕸️ An <strong>interactive dependency graph</strong> showing which files include which</li>
    <li>🔄 <strong>Circular dependency detection</strong> (when A includes B which includes A)</li>
    <li>🌐 A beautiful <strong>self-contained HTML report</strong> with D3.js visualizations</li>
  </ul>
</div>

<div class="section">
  <h2>🏗️ The 3-Layer Architecture</h2>
  <p>The project is split into three clear layers that talk to each other through a JSON file:</p>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace">
┌──────────────────────────────────────────────────┐
│   INPUT: A folder of .cpp / .h files             │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│         🔧 LAYER 1: C++17 ANALYZER               │
│                                                  │
│  CommentStripper → strips // and /* */ first     │
│  MetricsCalculator → counts complexity           │
│  DependencyGraph → maps #include links           │
│  JsonExporter → writes output.json               │
└────────────────────┬─────────────────────────────┘
                     │  output.json (the bridge)
                     ▼
┌──────────────────────────────────────────────────┐
│         🐍 LAYER 2: PYTHON TRANSFORMER           │
│                                                  │
│  graph_builder.py → JSON → D3-ready data         │
│  html_generator.py → embeds data into HTML       │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│         🌐 LAYER 3: D3.js VISUALIZATION          │
│                                                  │
│  Force-directed graph of files                   │
│  Nodes sized by complexity, colored by risk      │
│  Click any node to see function details          │
└──────────────────────────────────────────────────┘
</pre>
  </div>
</div>

<div class="section">
  <h2>🛠️ Tech Stack</h2>
  <div class="metric-row">
    <div class="metric"><div class="metric-val" style="color:#6366f1">C++17</div><div class="metric-lbl">Core Analyzer</div></div>
    <div class="metric"><div class="metric-val" style="color:#f59e0b">Python</div><div class="metric-lbl">Data Transformer</div></div>
    <div class="metric"><div class="metric-val" style="color:#f97316">D3.js</div><div class="metric-lbl">Visualization</div></div>
    <div class="metric"><div class="metric-val" style="color:#22c55e">JSON</div><div class="metric-lbl">The Bridge</div></div>
  </div>
  <div class="callout key"><strong>Zero external C++ dependencies</strong> The entire C++ analyzer builds with a single <code>g++ -std=c++17</code> command. No Boost, no libclang, no CMake madness. Just pure C++17 standard library.</div>
</div>

<div class="section">
  <h2>📚 Learning Path</h2>
  <div class="card-grid">
    <a class="card" href="phase1/index.html">
      <div class="card-icon">⚙️</div>
      <div class="card-title">Phase 1 — C++17 Deep Dive</div>
      <div class="card-desc">strings, file I/O, templates, unordered_map, RAII, regex, and more — explained for Python developers</div>
    </a>
    <a class="card" href="phase2/index.html">
      <div class="card-icon">🏗️</div>
      <div class="card-title">Phase 2 — Architecture</div>
      <div class="card-desc">Why 3 layers? Why JSON? How does data flow from C++ to the browser?</div>
    </a>
    <a class="card" href="phase3/index.html">
      <div class="card-icon">📁</div>
      <div class="card-title">Phase 3 — File Walkthrough</div>
      <div class="card-desc">Every file explained line by line, from comment_stripper.cpp to the D3.js visualization</div>
    </a>
    <a class="card" href="phase4/index.html">
      <div class="card-icon">🔢</div>
      <div class="card-title">Phase 4 — Algorithms</div>
      <div class="card-desc">Cyclomatic complexity, the state machine, DFS cycle detection, and D3 physics explained</div>
    </a>
    <a class="card" href="phase5/index.html">
      <div class="card-icon">🎤</div>
      <div class="card-title">Phase 5 — Interview Q&A</div>
      <div class="card-desc">Confident, specific answers to every question an interviewer could ask about this project</div>
    </a>
  </div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/index.html
# ─────────────────────────────────────────────────────────────
P1_INDEX_CONTENT = """
<div class="section">
  <h2>⚙️ Why C++17?</h2>
  <p>C++17 is the version of C++ that added a lot of modern, comfortable features. Before C++17, writing C++ felt very old-fashioned. With C++17, it's still C++, but much more pleasant to write.</p>
  <p>This project uses C++17 for features like <code>std::filesystem</code> (like Python's <code>pathlib</code>) and structured bindings.</p>
  <div class="callout tip"><strong>Good news for Python devs</strong>Many C++ concepts have direct Python equivalents. These pages will always show you both side by side!</div>
</div>

<div class="section">
  <h2>📖 Topics in this phase</h2>
  <div class="card-grid">
    <a class="card" href="string-vs-python.html"><div class="card-icon">📝</div><div class="card-title">std::string vs Python str</div><div class="card-desc">Mutable vs immutable, memory ownership, common operations</div></a>
    <a class="card" href="file-io.html"><div class="card-icon">📂</div><div class="card-title">File I/O in C++</div><div class="card-desc">ifstream, ofstream — the C++ equivalent of Python's open()</div></a>
    <a class="card" href="unordered-map.html"><div class="card-icon">🗺️</div><div class="card-title">unordered_map</div><div class="card-desc">C++'s hash map — like Python dict but with explicit types</div></a>
    <a class="card" href="struct-vs-class.html"><div class="card-icon">📦</div><div class="card-title">struct vs class</div><div class="card-desc">When to use each — from FunctionMetrics and FileMetrics</div></a>
    <a class="card" href="const-references.html"><div class="card-icon">🔒</div><div class="card-title">const &amp; References</div><div class="card-desc">Pass-by-reference without copying — C++'s superpower</div></a>
    <a class="card" href="raii.html"><div class="card-icon">🛡️</div><div class="card-title">RAII</div><div class="card-desc">C++'s version of Python's "with" statement — but automatic</div></a>
    <a class="card" href="vector-vs-deque.html"><div class="card-icon">📋</div><div class="card-title">vector vs deque</div><div class="card-desc">The two most important sequence containers in C++</div></a>
    <a class="card" href="regex.html"><div class="card-icon">🔍</div><div class="card-title">std::regex</div><div class="card-desc">Regular expressions in C++ — used to detect function signatures</div></a>
    <a class="card" href="templates.html"><div class="card-icon">🧩</div><div class="card-title">Templates</div><div class="card-desc">Generic programming — write code that works for any type</div></a>
    <a class="card" href="json-output.html"><div class="card-icon">📄</div><div class="card-title">JSON Output</div><div class="card-desc">Building JSON manually with ostringstream — no libraries needed</div></a>
  </div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/string-vs-python.html
# ─────────────────────────────────────────────────────────────
P1_STRING_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>In Python, a string is simple: <code>name = "hello"</code>. You don't worry about memory, sizes, or copying. Python handles all of that for you behind the scenes.</p>
  <p>In C++, <code>std::string</code> is a <em>class</em> that manages its own memory. It's more powerful but also more explicit. Let's compare them side by side.</p>
</div>

<div class="section">
  <h2>📝 Basic usage — side by side</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python</div>
      <div class="cmp-body">
<pre><div class="code-body"># Create
name = "hello"
path = 'world'

# Concatenate
full = name + ", " + path

# Length
n = len(name)       # 5

# Substring
sub = name[1:3]     # "el"

# Check if empty
if not name:
    print("empty")</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++</div>
      <div class="cmp-body">
<pre><div class="code-body">#include &lt;string&gt;

// Create
std::string name = "hello";
std::string path = "world";

// Concatenate
std::string full = name + ", " + path;

// Length
size_t n = name.size();   // 5

// Substring
std::string sub = name.substr(1, 2); // "el"

// Check if empty
if (name.empty()) {
    std::cout &lt;&lt; "empty";
}</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>🔑 Key difference: Mutability</h2>
  <p>In Python, strings are <strong>immutable</strong>. Every time you "modify" a string, Python creates a brand new one in memory. In C++, <code>std::string</code> is <strong>mutable</strong> — you can change it in place.</p>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python — strings are IMMUTABLE</div>
      <div class="cmp-body">
<pre><div class="code-body">s = "hello"
# You can NOT do s[0] = 'H' — it's an error!
# Python creates a NEW string every time:
s = s.upper()       # new string "HELLO"
s = s + " world"    # another new string</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++ — strings are MUTABLE</div>
      <div class="cmp-body">
<pre><div class="code-body">std::string s = "hello";
// You CAN modify in place:
s[0] = 'H';        // now s = "Hello" ✓
s += " world";     // appends in place ✓
s.push_back('!');  // adds character ✓</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📁 From the project: CommentStripper</h2>
  <p>Look at how <code>CommentStripper::strip()</code> builds its result string. Because C++ strings are mutable, we can build a result character by character very efficiently:</p>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>comment_stripper.cpp</span></div><div class="code-body">std::string CommentStripper::strip(const std::string&amp; source) const {
    std::string result;
    result.reserve(source.size());  // 🔑 pre-allocate memory!

    for (std::size_t i = 0; i &lt; len; ++i) {
        const char c = source[i];   // read one char at a time

        // ... state machine logic ...
        result += c;                // append in place — very fast!
    }

    return result;
}</div></pre>

  <div class="callout key"><strong>Why result.reserve(source.size())?</strong> This is a huge performance trick! It tells the string "I'm going to add about this many characters". Without this, the string would resize itself (and copy all its data) multiple times as it grows. With reserve(), we do it once. In Python, you'd do <code>''.join(chars)</code> for the same reason.</div>
</div>

<div class="section">
  <h2>📁 From the project: readFile()</h2>
  <p>Here's how the project reads an entire file into a single <code>std::string</code>:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp</span></div><div class="code-body">static std::string readFile(const fs::path&amp; path) {
    std::ifstream file(path, std::ios::binary);
    std::ostringstream ss;
    ss &lt;&lt; file.rdbuf();   // read entire file at once
    return ss.str();      // convert to string
}</div></pre>
  <p>The Python equivalent would be:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>equivalent Python</span></div><div class="code-body">def read_file(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')</div></pre>
</div>

<div class="section">
  <h2>🔬 Common string operations — quick reference</h2>
  <table class="tbl">
    <tr><th>Operation</th><th>Python</th><th>C++</th></tr>
    <tr><td>Length</td><td><code>len(s)</code></td><td><code>s.size()</code></td></tr>
    <tr><td>Empty check</td><td><code>not s</code></td><td><code>s.empty()</code></td></tr>
    <tr><td>Concatenate</td><td><code>s + t</code></td><td><code>s + t</code> or <code>s += t</code></td></tr>
    <tr><td>Substring</td><td><code>s[1:4]</code></td><td><code>s.substr(1, 3)</code></td></tr>
    <tr><td>Find</td><td><code>s.find("x")</code></td><td><code>s.find("x")</code> returns <code>npos</code> if not found</td></tr>
    <tr><td>Replace</td><td><code>s.replace("a","b")</code></td><td>Manual — no built-in replace</td></tr>
    <tr><td>Split by lines</td><td><code>s.splitlines()</code></td><td><code>std::getline(stream, line)</code> in a loop</td></tr>
    <tr><td>Starts with</td><td><code>s.startswith("x")</code></td><td><code>s.rfind("x", 0) == 0</code></td></tr>
    <tr><td>To number</td><td><code>int(s)</code></td><td><code>std::stoi(s)</code></td></tr>
  </table>
</div>

<div class="section">
  <h2>🎁 Special: std::string_view (C++17)</h2>
  <p>C++17 added <code>std::string_view</code> — it's a <em>read-only view</em> into a string. No copying, no memory allocation. Think of it like a lightweight reference to a string or a substring.</p>
  <div class="callout info"><strong>When to use it</strong> Use <code>std::string_view</code> for function parameters when you only need to READ the string. The project uses <code>const std::string&amp;</code> (same idea) throughout — like <code>strip(const std::string&amp; source)</code>.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/file-io.html
# ─────────────────────────────────────────────────────────────
P1_FILEIO_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>In Python, you open files with <code>open()</code> and Python cleans up after you automatically (especially with <code>with</code>). In C++, you use <code>std::ifstream</code> to read and <code>std::ofstream</code> to write. The good news: they clean up automatically too, thanks to RAII!</p>
</div>

<div class="section">
  <h2>📖 Reading a file</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python</div>
      <div class="cmp-body">
<pre><div class="code-body">with open("data.txt", "r") as f:
    content = f.read()   # whole file as string

# Line by line:
with open("data.txt") as f:
    for line in f:
        print(line.strip())</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++</div>
      <div class="cmp-body">
<pre><div class="code-body">#include &lt;fstream&gt;
#include &lt;sstream&gt;

// Whole file at once:
std::ifstream file("data.txt");
std::ostringstream ss;
ss &lt;&lt; file.rdbuf();
std::string content = ss.str();

// Line by line:
std::string line;
while (std::getline(file, line)) {
    // process line
}</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>✍️ Writing a file</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python</div>
      <div class="cmp-body">
<pre><div class="code-body">with open("output.json", "w") as f:
    f.write(json_string)</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++</div>
      <div class="cmp-body">
<pre><div class="code-body">std::ofstream out("output.json");
if (!out.is_open()) {
    throw std::runtime_error("Cannot open file!");
}
out &lt;&lt; json_string;</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📁 From the project: readFile() in main.cpp</h2>
  <p>The project reads every C++ source file into memory as a single big string. Here's exactly how it's done:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp</span></div><div class="code-body">static std::string readFile(const fs::path&amp; path) {
    std::ifstream file(path, std::ios::binary);  // open for binary read
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + path.string());
    }
    std::ostringstream ss;
    ss &lt;&lt; file.rdbuf();   // stream entire file buffer into string stream
    return ss.str();      // extract as std::string
}
// file closes automatically when the function ends — that's RAII!</div></pre>

  <div class="callout tip"><strong>std::ios::binary</strong> means "don't do any line-ending translation". On Windows, text mode converts \r\n to \n automatically. Binary mode skips that so we get the raw bytes. Always use binary mode when you want exact byte-for-byte content.</div>
</div>

<div class="section">
  <h2>📁 From the project: JsonExporter::exportToFile()</h2>
  <p>After building the JSON string in memory, the exporter writes it to disk:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp</span></div><div class="code-body">void JsonExporter::exportToFile(const std::vector&lt;FileMetrics&gt;&amp; files,
                                 const DependencyGraph&amp; graph,
                                 const std::string&amp; projectName,
                                 const std::string&amp; outputPath) const {
    // 1. Build the entire JSON string in memory first
    const std::string json = buildJson(files, graph, projectName);

    // 2. Open the output file
    std::ofstream out(outputPath);
    if (!out.is_open()) {
        throw std::runtime_error("Cannot open output file: " + outputPath);
    }

    // 3. Write it all at once
    out &lt;&lt; json;

    // 4. Check it worked
    if (!out.good()) {
        throw std::runtime_error("Write failed for: " + outputPath);
    }
    // out closes automatically here — RAII!
}</div></pre>
</div>

<div class="section">
  <h2>🗺️ ostringstream — building strings with &lt;&lt;</h2>
  <p>The project builds JSON strings using <code>std::ostringstream</code>. Think of it as a writable buffer that you can pour things into with <code>&lt;&lt;</code>, then extract as a <code>std::string</code>.</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>How ostringstream works</span></div><div class="code-body">std::ostringstream ss;
ss &lt;&lt; "{\\"name\\": \\"";  // pour a string
ss &lt;&lt; filename;           // pour a variable
ss &lt;&lt; "\\"}\n";           // pour more

std::string result = ss.str();  // get the built string</div></pre>
  <div class="callout info"><strong>Python equivalent</strong> <code>ostringstream</code> is like Python's <code>io.StringIO</code> or building a list of strings and joining at the end with <code>''.join(parts)</code>.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/unordered-map.html
# ─────────────────────────────────────────────────────────────
P1_MAP_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p><code>std::unordered_map</code> is C++'s hash map. It's almost exactly like Python's <code>dict</code> — you store key-value pairs, and lookup is O(1) average time. The main difference is that you must declare the types explicitly in C++.</p>
</div>

<div class="section">
  <h2>📝 Basic usage</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python dict</div>
      <div class="cmp-body">
<pre><div class="code-body"># Create
graph = {}

# Insert
graph["hospital.cpp"] = ["patient.h"]

# Lookup (KeyError if missing)
deps = graph["hospital.cpp"]

# Safe lookup
deps = graph.get("hospital.cpp", [])

# Check existence
if "hospital.cpp" in graph:
    print("found")

# Iterate
for filename, deps in graph.items():
    print(filename, deps)</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ std::unordered_map</div>
      <div class="cmp-body">
<pre><div class="code-body">#include &lt;unordered_map&gt;
#include &lt;vector&gt;
#include &lt;string&gt;

// Create — must declare types!
std::unordered_map&lt;std::string,
    std::vector&lt;std::string&gt;&gt; graph;

// Insert
graph["hospital.cpp"] = {"patient.h"};

// Lookup (inserts default if missing!)
auto&amp; deps = graph["hospital.cpp"];

// Safe lookup
auto it = graph.find("hospital.cpp");
if (it != graph.end()) {
    auto&amp; deps = it-&gt;second;
}

// Check existence
if (graph.count("hospital.cpp") &gt; 0) { }

// Iterate
for (const auto&amp; kv : graph) {
    std::string filename = kv.first;
    auto deps = kv.second;
}</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>⚠️ Gotcha: operator[] creates entries!</h2>
  <p>In Python, <code>d["missing_key"]</code> raises a <code>KeyError</code>. In C++, <code>map["missing_key"]</code> quietly <em>creates</em> a new entry with a default value. This can be surprising!</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>C++ gotcha</span></div><div class="code-body">std::unordered_map&lt;std::string, int&gt; counts;

// This CREATES "hello" with value 0 if it doesn't exist:
counts["hello"]++;   // OK — the default int is 0

// This is SAFE — doesn't create:
auto it = counts.find("hello");
if (it != counts.end()) {
    int val = it-&gt;second;
}</div></pre>
</div>

<div class="section">
  <h2>📁 From the project: DependencyGraph</h2>
  <p>The heart of the dependency graph is a single <code>unordered_map</code>:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.h</span></div><div class="code-body">class DependencyGraph {
private:
    // filename → list of direct dependencies
    // e.g. "hospital.cpp" → ["patient.h", "utils.h"]
    std::unordered_map&lt;std::string, std::vector&lt;std::string&gt;&gt; graph_;

    // Set of files involved in circular dependencies
    mutable std::unordered_set&lt;std::string&gt; circularFiles_;
};</div></pre>

  <p>And here's how <code>addFile()</code> uses it safely:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.cpp</span></div><div class="code-body">void DependencyGraph::addFile(const std::string&amp; filename,
                               const std::vector&lt;std::string&gt;&amp; dependencies) {
    // Ensure the file appears as a node even if it has no deps
    if (graph_.find(filename) == graph_.end()) {
        graph_[filename] = {};   // safe: we're intentionally inserting
    }

    for (const auto&amp; dep : dependencies) {
        auto&amp; deps = graph_[filename];
        // Avoid duplicate edges
        if (std::find(deps.begin(), deps.end(), dep) == deps.end()) {
            deps.push_back(dep);
        }
    }
}</div></pre>
</div>

<div class="section">
  <h2>⚡ Why unordered_map vs map?</h2>
  <table class="tbl">
    <tr><th>Feature</th><th>unordered_map</th><th>map</th></tr>
    <tr><td>Lookup speed</td><td><span class="badge low">O(1) average</span></td><td><span class="badge med">O(log n)</span></td></tr>
    <tr><td>Internal structure</td><td>Hash table</td><td>Red-black tree</td></tr>
    <tr><td>Keys sorted?</td><td>No</td><td>Yes (always sorted)</td></tr>
    <tr><td>When to use</td><td>Fast lookup, order doesn't matter</td><td>Need sorted keys, small maps</td></tr>
  </table>
  <div class="callout key"><strong>This project uses unordered_map</strong> because files are looked up by name constantly during graph traversal, and order doesn't matter. O(1) is exactly what you want for a graph adjacency list.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/struct-vs-class.html
# ─────────────────────────────────────────────────────────────
P1_STRUCT_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>In C++, <code>struct</code> and <code>class</code> are almost identical — with one difference: <strong>struct members are public by default; class members are private by default</strong>. That's literally the only difference in the language.</p>
  <p>By convention: use <code>struct</code> for plain data containers (like Python dataclasses), use <code>class</code> for objects with behavior and hidden internals.</p>
</div>

<div class="section">
  <h2>📦 Structs in this project: FunctionMetrics &amp; FileMetrics</h2>
  <p>The project uses structs to hold analysis results — they're pure data containers with no complex behavior:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.h</span></div><div class="code-body">// FunctionMetrics — holds results for one function
struct FunctionMetrics {
    std::string name;           // e.g. "processAdmission"
    int line_start      = 0;   // = 0 is the default value
    int line_end        = 0;
    int lines           = 0;
    int complexity      = 1;   // baseline = 1
    int nesting_depth   = 0;
    int parameter_count = 0;
    std::string risk;          // "low" | "medium" | "high"
    std::vector&lt;std::string&gt; risk_reasons;
};

// FileMetrics — holds results for one file
struct FileMetrics {
    std::string name;
    std::string path;
    int total_lines      = 0;
    int code_lines       = 0;
    int comment_lines    = 0;
    int blank_lines      = 0;
    int complexity_score = 0;
    std::string risk;
    std::vector&lt;FunctionMetrics&gt; functions;  // structs inside structs!
};</div></pre>

  <div class="callout info"><strong>Python equivalent</strong> This is identical to a Python <code>@dataclass</code>:<br><br>
<code>@dataclass<br>class FunctionMetrics:<br>&nbsp;&nbsp;&nbsp;&nbsp;name: str = ""<br>&nbsp;&nbsp;&nbsp;&nbsp;line_start: int = 0<br>&nbsp;&nbsp;&nbsp;&nbsp;complexity: int = 1</code></div>
</div>

<div class="section">
  <h2>🏛️ Classes in this project</h2>
  <p>The tool's analyzers are <code>class</code>es because they have private implementation details:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>comment_stripper.h — a class</span></div><div class="code-body">class CommentStripper {
public:
    // Public API — what callers see and use
    std::string strip(const std::string&amp; source) const;
    std::vector&lt;std::string&gt; stripLines(const std::string&amp; source) const;

private:
    // Private implementation detail — hidden from callers
    enum class State {
        CODE,
        LINE_COMMENT,
        BLOCK_COMMENT,
        STRING
    };
};</div></pre>
  <p>The <code>State</code> enum is private because it's an implementation detail. Callers don't need to know HOW the stripping works, just that it does.</p>
</div>

<div class="section">
  <h2>📊 Comparison at a glance</h2>
  <table class="tbl">
    <tr><th>Feature</th><th>struct</th><th>class</th></tr>
    <tr><td>Default visibility</td><td>public</td><td>private</td></tr>
    <tr><td>Use case</td><td>Plain data, POD types, result holders</td><td>Encapsulated behavior, hidden state</td></tr>
    <tr><td>Python equivalent</td><td>@dataclass or namedtuple</td><td>Regular class with __init__</td></tr>
    <tr><td>Can have methods?</td><td>Yes (but usually don't)</td><td>Yes (that's the point)</td></tr>
    <tr><td>In this project</td><td>FunctionMetrics, FileMetrics</td><td>CommentStripper, MetricsCalculator, DependencyGraph, JsonExporter</td></tr>
  </table>
</div>

<div class="section">
  <h2>⚡ Default values in structs (C++11+)</h2>
  <p>Notice how the structs have <code>= 0</code> after each member? That's a default value. Before C++11, you had to write a constructor to initialize everything. Now you can do it inline:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Using FunctionMetrics</span></div><div class="code-body">// Creating a struct in metrics_calculator.cpp:
FunctionMetrics fm;
fm.name        = funcName;       // set the name
fm.line_start  = funcStart;      // set line start
fm.line_end    = funcEnd + 1;
fm.lines       = fm.line_end - fm.line_start + 1;
fm.complexity  = calculateComplexity(body);   // computed
// fm.nesting_depth already = 0 from default
// fm.parameter_count already = 0 from default

functions.push_back(std::move(fm));  // add to vector</div></pre>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/const-references.html
# ─────────────────────────────────────────────────────────────
P1_CONSTREF_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>When you call a function in Python, you're passing a reference to the object — there's no copying of the actual data. In C++, the default behavior is the opposite: <strong>everything is copied by value</strong>. This can be very slow for big objects like strings or vectors.</p>
  <p><code>const std::string&amp;</code> is C++'s way of saying: "pass this without copying, and I promise I won't modify it".</p>
</div>

<div class="section">
  <h2>📝 The problem with copies</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Slow — copies the entire string!</span></div><div class="code-body">// BAD: This copies the ENTIRE source file string on every call
std::string strip(std::string source) {   // source = copy
    // process...
    return result;
}

// The source file might be 50,000 characters long.
// Making a copy every time wastes memory and time.</div></pre>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Fast — no copy!</span></div><div class="code-body">// GOOD: const reference — no copy, no modification allowed
std::string strip(const std::string&amp; source) {  // just a reference
    // process...
    return result;
}

// source is just a pointer to the original data.
// Zero copying. No memory waste.</div></pre>
</div>

<div class="section">
  <h2>📁 From the project: every function signature</h2>
  <p>Look at how <strong>every single function</strong> in this project uses <code>const &amp;</code>:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>comment_stripper.h</span></div><div class="code-body">// const std::string& = "read-only reference to a string"
std::string strip(const std::string&amp; source) const;</div></pre>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.h</span></div><div class="code-body">FileMetrics analyze(const std::string&amp; rawSource,
                    const std::string&amp; strippedSource,
                    const std::string&amp; filePath) const;</div></pre>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.h</span></div><div class="code-body">void exportToFile(const std::vector&lt;FileMetrics&gt;&amp; files,
                  const DependencyGraph&amp; graph,
                  const std::string&amp; projectName,
                  const std::string&amp; outputPath) const;</div></pre>
  <p>All of these take their arguments by const reference. Zero copies.</p>
</div>

<div class="section">
  <h2>🔍 The const keyword — two meanings</h2>
  <p><code>const</code> appears in two places and means two different things:</p>
  <table class="tbl">
    <tr><th>Where</th><th>Syntax</th><th>Meaning</th></tr>
    <tr><td>Parameter</td><td><code>const std::string&amp; s</code></td><td>"I promise not to modify this argument"</td></tr>
    <tr><td>After method</td><td><code>void foo() const;</code></td><td>"This method doesn't modify the object"</td></tr>
  </table>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Both const keywords</span></div><div class="code-body">class CommentStripper {
    // "const source" = won't modify source
    // trailing "const" = won't modify the CommentStripper object
    std::string strip(const std::string&amp; source) const;
    //                ^--- parameter const         ^--- method const
};</div></pre>
</div>

<div class="section">
  <h2>🔄 The range-for with const &amp;</h2>
  <p>The project uses <code>const auto&amp;</code> in every loop. This is the same idea:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp</span></div><div class="code-body">// BAD — copies each FileMetrics on every iteration!
for (FileMetrics fm : allMetrics) { ... }

// GOOD — just a reference, no copy
for (const auto&amp; fm : allMetrics) {
    // fm is a read-only reference to each element
    std::cout &lt;&lt; fm.name &lt;&lt; "\n";
}</div></pre>
  <div class="callout tip"><strong>Rule of thumb</strong> In C++, if you're not modifying a variable, always use <code>const</code>. If it's a big object (string, vector, struct), always use <code>&amp;</code>. Combine them: <code>const auto&amp;</code> in loops, <code>const Type&amp;</code> in parameters.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/raii.html
# ─────────────────────────────────────────────────────────────
P1_RAII_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>RAII stands for <strong>Resource Acquisition Is Initialization</strong>. It's a scary name for a simple idea: <em>when an object is created, it acquires a resource; when it's destroyed, it releases it automatically.</em></p>
  <p>Python has the same concept — it's called the <code>with</code> statement (context managers). C++ does it automatically for ALL objects, not just those used with <code>with</code>.</p>
</div>

<div class="section">
  <h2>🐍 Python context managers vs C++ RAII</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python — explicit with statement</div>
      <div class="cmp-body">
<pre><div class="code-body"># You MUST use "with" or the file might
# not close properly!
with open("file.txt") as f:
    content = f.read()
# file closes HERE (end of with block)

# Without "with" — risky!
f = open("file.txt")
content = f.read()
f.close()  # easy to forget!</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++ — automatic RAII</div>
      <div class="cmp-body">
<pre><div class="code-body">// In C++, EVERY object cleans up automatically
// when it goes out of scope!
{
    std::ifstream file("file.txt");  // OPENS file
    std::string content;
    // use file...
}
// file CLOSES automatically here!
// You can't forget — it's not optional.

// Same for strings, vectors, etc.
{
    std::string s = "hello";  // allocates memory
}   // memory freed automatically!</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📁 RAII in the project: readFile()</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp</span></div><div class="code-body">static std::string readFile(const fs::path&amp; path) {
    std::ifstream file(path, std::ios::binary);
    // ↑ file OPENS here (constructor)

    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file");
    }

    std::ostringstream ss;
    ss &lt;&lt; file.rdbuf();
    return ss.str();

    // ↓ file CLOSES here automatically (destructor)
    // This happens even if an exception is thrown!
    // That's the magic of RAII.
}</div></pre>
</div>

<div class="section">
  <h2>📁 RAII in the project: exportToFile()</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp</span></div><div class="code-body">void JsonExporter::exportToFile(..., const std::string&amp; outputPath) const {
    const std::string json = buildJson(files, graph, projectName);

    std::ofstream out(outputPath);   // OPENS file for writing
    if (!out.is_open()) {
        throw std::runtime_error("Cannot open output file: " + outputPath);
        // ↑ even if we throw here, the ofstream destructor runs!
    }
    out &lt;&lt; json;
    // out CLOSES and FLUSHES automatically when function ends
}</div></pre>
</div>

<div class="section">
  <h2>🏗️ How RAII works under the hood</h2>
  <p>Every C++ class has a <strong>constructor</strong> (runs when created) and a <strong>destructor</strong> (runs when destroyed). RAII uses this guarantee:</p>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace">
Constructor called → object created in memory
        │
        │  (object is alive and usable)
        │
Destructor called → object goes out of scope
        │
        └── cleanup runs AUTOMATICALLY:
              std::ifstream  → closes the file
              std::string    → frees the memory
              std::vector    → frees all elements
              std::mutex     → releases the lock
              Your class     → whatever you write in ~YourClass()
</pre>
  </div>
  <div class="callout key"><strong>Why this matters for interviews</strong> RAII is one of the most important C++ patterns. It means: no memory leaks, no resource leaks, exception-safe code, by default. Python's garbage collector handles memory but not other resources (file handles, network connections, locks).</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/vector-vs-deque.html
# ─────────────────────────────────────────────────────────────
P1_VEC_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p><code>std::vector</code> is C++'s dynamic array — like Python's <code>list</code>. It stores elements in a single continuous block of memory. <code>std::deque</code> is a "double-ended queue" — it's like a list of small arrays. Both are used in this project.</p>
</div>

<div class="section">
  <h2>📋 std::vector — the workhorse</h2>
  <p>The project uses <code>std::vector</code> everywhere. It's the default choice for ordered collections:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>From the project</span></div><div class="code-body">// In MetricsCalculator — collect all functions in a file:
std::vector&lt;FunctionMetrics&gt; functions;

// In main.cpp — collect all file metrics:
std::vector&lt;FileMetrics&gt; allMetrics;
allMetrics.reserve(files.size());  // pre-allocate for speed

// Add elements:
allMetrics.push_back(metrics);  // adds to the end

// Iterate:
for (const auto&amp; fm : allMetrics) { ... }

// In DependencyGraph — each file's list of dependencies:
std::unordered_map&lt;std::string, std::vector&lt;std::string&gt;&gt; graph_;</div></pre>
</div>

<div class="section">
  <h2>⚡ vector vs Python list</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python list</div>
      <div class="cmp-body">
<pre><div class="code-body">items = []            # create
items.append(x)       # add to end
items[0]              # access by index
len(items)            # length
items.clear()         # remove all
for x in items: ...   # iterate</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ std::vector</div>
      <div class="cmp-body">
<pre><div class="code-body">std::vector&lt;int&gt; items;   // create
items.push_back(x);        // add to end
items[0]                   // access by index
items.size()               // length
items.clear()              // remove all
for (const auto&amp; x : items) ... // iterate</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📦 move semantics: push_back vs std::move</h2>
  <p>The project uses <code>std::move</code> when adding to vectors. This is a C++11 optimization:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp</span></div><div class="code-body">FunctionMetrics fm;
fm.name = funcName;
// ... fill in fm ...

// Without move — COPIES the entire struct:
functions.push_back(fm);     // slow for big objects

// With move — TRANSFERS ownership, no copy:
functions.push_back(std::move(fm));  // fast!
// After move, fm is in a "moved-from" state — don't use it</div></pre>
  <div class="callout info"><strong>Python analogy</strong> In Python, appending always just adds a reference to the object — there's no copying. In C++, you have to explicitly say "move this, don't copy" with <code>std::move</code>.</div>
</div>

<div class="section">
  <h2>📊 When to use what</h2>
  <table class="tbl">
    <tr><th>Container</th><th>Best for</th><th>Avoid when</th></tr>
    <tr><td><code>std::vector</code></td><td>Most things. Sequential access, push_back at end</td><td>Frequent inserts/deletes in the middle</td></tr>
    <tr><td><code>std::deque</code></td><td>Need push_front AND push_back efficiently</td><td>Need contiguous memory (vector is better)</td></tr>
    <tr><td><code>std::list</code></td><td>Frequent inserts/deletes anywhere</td><td>Random access (no []operator)</td></tr>
  </table>
  <div class="callout tip"><strong>The rule</strong> Start with <code>std::vector</code>. Switch to something else only when you have a specific reason. This project uses vector everywhere and it's perfect for the job.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/regex.html
# ─────────────────────────────────────────────────────────────
P1_REGEX_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>Regular expressions in C++ work the same as in Python — you write a pattern, and it matches text. The syntax is identical (both use the ECMAScript regex flavor). The main difference is the API: Python uses <code>re.search()</code>, C++ uses <code>std::regex_search()</code>.</p>
</div>

<div class="section">
  <h2>📝 Basic usage comparison</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python re module</div>
      <div class="cmp-body">
<pre><div class="code-body">import re

pattern = re.compile(r'#include\s*"([^"]+)"')
line = '#include "patient.h"'

m = pattern.search(line)
if m:
    print(m.group(1))  # "patient.h"</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++ std::regex</div>
      <div class="cmp-body">
<pre><div class="code-body">#include &lt;regex&gt;

std::regex pattern(R"(#include\s*"([^"]+)")");
std::string line = "#include \"patient.h\"";

std::smatch match;
if (std::regex_search(line, match, pattern)) {
    std::string file = match[1].str(); // "patient.h"
}</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📁 From the project: extractIncludes()</h2>
  <p>The dependency graph uses regex to find <code>#include "file.h"</code> lines:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.cpp</span></div><div class="code-body">std::vector&lt;std::string&gt; DependencyGraph::extractIncludes(
        const std::string&amp; source) const {
    std::vector&lt;std::string&gt; includes;

    // R"(...)" is a raw string literal — no need to escape backslashes!
    // Pattern matches: #include "anything"
    // Captures the filename in group 1
    static const std::regex localInclude(R"re(^\s*#include\s*"([^"]+)")re");

    std::istringstream stream(source);
    std::string line;
    while (std::getline(stream, line)) {
        std::smatch match;
        if (std::regex_search(line, match, localInclude)) {
            std::string includePath = match[1].str();
            // Extract just the filename from a path like "utils/patient.h"
            const auto slashPos = includePath.find_last_of("/\\\\");
            if (slashPos != std::string::npos) {
                includePath = includePath.substr(slashPos + 1);
            }
            includes.push_back(includePath);
        }
    }
    return includes;
}</div></pre>
</div>

<div class="section">
  <h2>📁 From the project: function signature detection</h2>
  <p>This is the most complex regex in the project. It tries to detect lines that look like C++ function signatures:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp — the function detection regex</span></div><div class="code-body">// static = compiled once, reused every call (important for performance!)
static const std::regex funcSignaturePattern(
    // Optional modifiers before the return type:
    R"(^\s*(?:(?:inline|static|virtual|explicit|friend|constexpr|const|override|final|noexcept)\s+)*)"
    // Return type + function name + parameter list:
    R"([\w:~&lt;&gt;\*&amp;\s]+\s+(\w+)\s*\(([^;]*)\)\s*(?:const\s*)?(?:noexcept\s*)?(?:override\s*)?(?:-&gt;\s*[\w:&amp;\*&lt;&gt;\s]+)?\s*\{?\s*$)"
);
// Match group 1 = function name
// Match group 2 = parameter string</div></pre>
  <div class="callout warn"><strong>Why not use regex for everything?</strong> Regex is used here for the <em>first pass</em> — spotting likely function signatures. But C++ syntax is so complex that regex alone can't fully parse it. That's why the code also does brace counting and keyword filtering after the regex match.</div>
</div>

<div class="section">
  <h2>🔑 Raw string literals R"(...)"</h2>
  <p>Notice <code>R"(...)"</code> instead of <code>"..."</code> for the patterns. Raw string literals don't need you to escape backslashes — perfect for regex patterns!</p>
  <div class="compare">
    <div class="cmp-card bad">
      <div class="cmp-head">😤 Without raw strings</div>
      <div class="cmp-body">
<pre><div class="code-body">// Every \\ needs to be doubled — nightmare!
std::regex r("^\\s*#include\\s*\"([^\"]+)\"");</div></pre>
      </div>
    </div>
    <div class="cmp-card good">
      <div class="cmp-head">😊 With raw strings</div>
      <div class="cmp-body">
<pre><div class="code-body">// Clean! Backslashes are literal
std::regex r(R"(^\s*#include\s*"([^"]+)")");</div></pre>
      </div>
    </div>
  </div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/templates.html
# ─────────────────────────────────────────────────────────────
P1_TEMPLATES_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>Templates are C++'s way of writing code that works for <em>any type</em>. In Python, every function automatically works with any type (duck typing). In C++, you have to be explicit — which is where templates come in.</p>
</div>

<div class="section">
  <h2>📝 The problem templates solve</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Without templates — repetitive!</span></div><div class="code-body">int    max(int    a, int    b) { return a > b ? a : b; }
double max(double a, double b) { return a > b ? a : b; }
float  max(float  a, float  b) { return a > b ? a : b; }
// Same code 3 times! What about long, short, char...?</div></pre>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>With templates — one version works for all types!</span></div><div class="code-body">template&lt;typename T&gt;
T myMax(T a, T b) { return a > b ? a : b; }

// The compiler generates the right version automatically:
myMax(3, 5);        // compiler makes int version
myMax(3.14, 2.71);  // compiler makes double version
myMax(3L, 5L);      // compiler makes long version</div></pre>
</div>

<div class="section">
  <h2>📁 Templates in the standard library — used in this project</h2>
  <p>You already use templates every time you write <code>std::vector&lt;FileMetrics&gt;</code> or <code>std::unordered_map&lt;std::string, ...&gt;</code>. The <code>&lt;...&gt;</code> is the template parameter:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Template types used in the project</span></div><div class="code-body">// vector is a template that works with ANY type:
std::vector&lt;FileMetrics&gt; allMetrics;     // vector of FileMetrics
std::vector&lt;std::string&gt; dependencies;  // vector of strings
std::vector&lt;FunctionMetrics&gt; functions; // vector of FunctionMetrics

// unordered_map is a template with 2 type params:
std::unordered_map&lt;std::string, std::vector&lt;std::string&gt;&gt; graph_;
//                 ^key type   ^value type

// pair is a template for a pair of values:
std::vector&lt;std::pair&lt;std::string, std::string&gt;&gt; getEdges() const;
//          edges are (filename, dependency) pairs</div></pre>
</div>

<div class="section">
  <h2>📁 Lambda templates in the project: countOp</h2>
  <p>The project uses a lambda (anonymous function) that acts like a mini-template:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp — lambda for counting operators</span></div><div class="code-body">int MetricsCalculator::calculateComplexity(const std::string&amp; body) const {
    int complexity = 1;

    // Lambda — captures body by reference, works like a reusable mini-function
    auto countOp = [&amp;](const std::string&amp; op) {
        int count = 0;
        std::size_t pos = 0;
        while ((pos = body.find(op, pos)) != std::string::npos) {
            ++count; pos += op.size();
        }
        return count;
    };

    // Reuse the same lambda for different operators:
    complexity += countOp("&amp;&amp;");   // logical AND
    complexity += countOp("||");   // logical OR
    complexity += countOp("?");    // ternary operator

    return complexity;
}</div></pre>
</div>

<div class="section">
  <h2>🐍 Python comparison</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python — duck typing (no templates needed)</div>
      <div class="cmp-body">
<pre><div class="code-body"># Works with any type automatically
def my_max(a, b):
    return a if a > b else b

my_max(3, 5)         # works
my_max(3.14, 2.71)   # works
my_max("cat", "dog") # works!</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++ — explicit templates required</div>
      <div class="cmp-body">
<pre><div class="code-body">template&lt;typename T&gt;
T myMax(T a, T b) {
    return a > b ? a : b;
}
// Must declare T explicitly
// But: compiler catches type errors at compile time!</div></pre>
      </div>
    </div>
  </div>
  <div class="callout key"><strong>Trade-off</strong> Python templates (duck typing) are more flexible. C++ templates are more explicit but catch errors earlier — at compile time instead of runtime. For a tool that analyzes millions of lines of code, compile-time safety is worth it.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase1/json-output.html
# ─────────────────────────────────────────────────────────────
P1_JSON_CONTENT = """
<div class="section">
  <h2>🎯 The big idea</h2>
  <p>This project builds JSON entirely by hand — no external libraries. Instead of <code>json.dumps()</code> like in Python, the <code>JsonExporter</code> class builds JSON strings character by character using <code>std::ostringstream</code>.</p>
  <div class="callout key"><strong>Why no JSON library?</strong> Keeping the C++ analyzer dependency-free means it builds with a single <code>g++</code> command on any machine. No CMake, no downloads, no version conflicts. Zero external dependencies.</div>
</div>

<div class="section">
  <h2>📝 Python vs C++ JSON building</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">🐍 Python — json.dumps()</div>
      <div class="cmp-body">
<pre><div class="code-body">import json

data = {
    "project": project_name,
    "total_files": len(files),
    "risk": "high",
}

json_string = json.dumps(data, indent=2)</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">⚙️ C++ — manual building</div>
      <div class="cmp-body">
<pre><div class="code-body">std::ostringstream j;
j &lt;&lt; "{\n";
j &lt;&lt; "  \"project\": \""
  &lt;&lt; escapeString(projectName) &lt;&lt; "\",\n";
j &lt;&lt; "  \"total_files\": " &lt;&lt; files.size() &lt;&lt; ",\n";
j &lt;&lt; "  \"risk\": \"high\"\n";
j &lt;&lt; "}\n";
std::string result = j.str();</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📁 The buildJson() function</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp — top-level JSON builder</span></div><div class="code-body">std::string JsonExporter::buildJson(const std::vector&lt;FileMetrics&gt;&amp; files,
                                     const DependencyGraph&amp; graph,
                                     const std::string&amp; projectName) const {
    std::ostringstream j;
    j &lt;&lt; "{\n";
    j &lt;&lt; indent(1) &lt;&lt; "\"project\": \""         &lt;&lt; escapeString(projectName) &lt;&lt; "\",\n";
    j &lt;&lt; indent(1) &lt;&lt; "\"analyzed_at\": \""      &lt;&lt; currentTimestamp()        &lt;&lt; "\",\n";
    j &lt;&lt; indent(1) &lt;&lt; "\"analyzer_version\": \"" &lt;&lt; "1.0.0\",\n";
    j &lt;&lt; indent(1) &lt;&lt; "\"summary\": " &lt;&lt; buildSummary(files) &lt;&lt; ",\n";

    j &lt;&lt; indent(1) &lt;&lt; "\"files\": [\n";
    for (std::size_t fi = 0; fi &lt; files.size(); ++fi) {
        j &lt;&lt; buildFileObject(files[fi], graph, 2);
        if (fi + 1 &lt; files.size()) j &lt;&lt; ",";  // no trailing comma!
        j &lt;&lt; "\n";
    }
    j &lt;&lt; indent(1) &lt;&lt; "],\n";

    j &lt;&lt; indent(1) &lt;&lt; "\"dependency_graph\": " &lt;&lt; buildDependencyGraph(graph) &lt;&lt; "\n";
    j &lt;&lt; "}\n";
    return j.str();
}</div></pre>
</div>

<div class="section">
  <h2>🔑 escapeString() — handling special characters</h2>
  <p>JSON strings can't contain raw quotes, backslashes, or newlines. The <code>escapeString()</code> function handles this:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp</span></div><div class="code-body">std::string JsonExporter::escapeString(const std::string&amp; s) const {
    std::string result;
    result.reserve(s.size());
    for (char c : s) {
        switch (c) {
            case '"':  result += "\\\""; break;  // " → \"
            case '\\': result += "\\\\"; break;  // \ → \\
            case '\n': result += "\\n";  break;  // newline → \n
            case '\r': result += "\\r";  break;
            case '\t': result += "\\t";  break;
            default:   result += c;      break;
        }
    }
    return result;
}
// Python equivalent: json.dumps(s)[1:-1]  (the string part without outer quotes)</div></pre>
</div>

<div class="section">
  <h2>📐 indent() — clean indentation</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp</span></div><div class="code-body">std::string JsonExporter::indent(int level) const {
    // level=1 → "  "  (2 spaces)
    // level=2 → "    " (4 spaces)
    // level=3 → "      " (6 spaces)
    return std::string(static_cast&lt;std::size_t&gt;(level) * 2, ' ');
}

// Usage:
j &lt;&lt; indent(1) &lt;&lt; "\"project\": ...\n";   // 2 spaces indent
j &lt;&lt; indent(2) &lt;&lt; "\"name\": ...\n";      // 4 spaces indent</div></pre>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase2/index.html
# ─────────────────────────────────────────────────────────────
P2_INDEX_CONTENT = """
<div class="section">
  <h2>🏗️ The 3 layers explained</h2>
  <p>The project is deliberately split into three separate layers. Each layer has a specific job and talks to the next layer only through well-defined interfaces:</p>

  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace;font-size:12px">
  ┌─────────────────────────────────────────────────────────────────┐
  │                    LAYER 1: C++17 ANALYZER                      │
  │                                                                 │
  │  WHY C++? → Speed. Analyzing thousands of files needs fast I/O  │
  │             and fast string processing. Python would be 10x     │
  │             slower for character-by-character parsing.           │
  │                                                                 │
  │  What it does:                                                  │
  │  ┌──────────────────┐   ┌─────────────────────┐                │
  │  │ CommentStripper  │   │ MetricsCalculator   │                │
  │  │ 4-state machine  │──▶│ Cyclomatic CC       │                │
  │  │ strips // /* */  │   │ Function extraction │                │
  │  └──────────────────┘   └──────────┬──────────┘                │
  │                                    │                            │
  │  ┌──────────────────┐   ┌──────────▼──────────┐                │
  │  │ DependencyGraph  │   │ JsonExporter         │                │
  │  │ unordered_map    │──▶│ builds output.json  │                │
  │  │ DFS cycle detect │   │ zero external deps  │                │
  │  └──────────────────┘   └─────────────────────┘                │
  └─────────────────────────────────────────────────────────────────┘
                               │
                          output.json
                     (the JSON bridge)
                               │
  ┌─────────────────────────────────────────────────────────────────┐
  │                    LAYER 2: PYTHON                              │
  │                                                                 │
  │  WHY PYTHON? → HTML generation with string templates is messy   │
  │               in C++. Python's string formatting is perfect     │
  │               for building HTML. Also, the D3.js data           │
  │               transformation is cleaner in Python.              │
  │                                                                 │
  │  ┌──────────────────┐   ┌─────────────────────┐                │
  │  │ graph_builder.py │   │ html_generator.py   │                │
  │  │ JSON → D3 nodes  │──▶│ embeds data in HTML │                │
  │  │ & edges          │   │ produces report.html│                │
  │  └──────────────────┘   └─────────────────────┘                │
  └─────────────────────────────────────────────────────────────────┘
                               │
                          report.html
                               │
  ┌─────────────────────────────────────────────────────────────────┐
  │                    LAYER 3: D3.js                               │
  │                                                                 │
  │  WHY D3? → Force-directed graphs need full control over         │
  │             physics: charge, link strength, collision. D3's     │
  │             simulation API is the best tool for this.           │
  │             Result: a single self-contained HTML file.          │
  │                                                                 │
  │  Force-directed graph • Risk-colored nodes • Click to inspect  │
  └─────────────────────────────────────────────────────────────────┘
</pre>
  </div>
</div>

<div class="section">
  <h2>🌉 Why a JSON bridge?</h2>
  <p>The JSON file (<code>output.json</code>) is the contract between the C++ world and the Python world. This is a key architectural decision with several benefits:</p>
  <ul>
    <li><strong>Decoupling:</strong> The C++ analyzer doesn't need to know anything about HTML or D3.js. The Python layer doesn't need to know how complexity is calculated.</li>
    <li><strong>Testability:</strong> You can test the C++ analyzer by checking the JSON output. You can test the Python layer by feeding it a sample JSON file (like <code>demo.json</code>).</li>
    <li><strong>Reusability:</strong> The JSON output can be used by other tools — a different visualizer, a CI/CD pipeline, a database import.</li>
    <li><strong>Debuggability:</strong> You can open <code>output.json</code> and read it. If something looks wrong in the visualization, you check the JSON first.</li>
  </ul>
</div>

<div class="section">
  <h2>🔄 Complete data flow — step by step</h2>
  <ol class="steps">
    <li><div class="step-num">1</div><div><strong>User runs the C++ analyzer:</strong> <code>./analyzer --path ./MyProject</code></div></li>
    <li><div class="step-num">2</div><div><strong>collectCppFiles()</strong> scans the directory and returns a list of <code>.cpp</code> and <code>.h</code> files.</div></li>
    <li><div class="step-num">3</div><div><strong>For each file:</strong> <code>readFile()</code> loads it as a raw string. <code>CommentStripper::strip()</code> removes all comments/strings. <code>MetricsCalculator::analyze()</code> computes complexity. <code>DependencyGraph::addFile()</code> records its <code>#include</code> relationships.</div></li>
    <li><div class="step-num">4</div><div><strong>JsonExporter::exportToFile()</strong> takes all metrics + the graph and writes <code>output.json</code>.</div></li>
    <li><div class="step-num">5</div><div><strong>User runs Python:</strong> <code>python html_generator.py output.json</code></div></li>
    <li><div class="step-num">6</div><div><strong>graph_builder.py</strong> transforms the JSON into D3-ready nodes and edges with color, radius, and tooltip data.</div></li>
    <li><div class="step-num">7</div><div><strong>html_generator.py</strong> embeds the D3 data and JavaScript into a single <code>report.html</code> file.</div></li>
    <li><div class="step-num">8</div><div><strong>User opens <code>report.html</code></strong> in any browser. Interactive force-directed graph appears with no server needed.</div></li>
  </ol>
</div>

<div class="section">
  <h2>🧩 The comment stripping challenge</h2>
  <p>One of the trickiest problems: <strong>keywords inside strings and comments should NOT count as complexity</strong>. For example:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>The problem</span></div><div class="code-body">// This is a comment with "if" and "while" keywords.
/* Another block comment with for and case keywords */
std::string msg = "if you see this, report a bug";
                   // ↑ "if" is inside a STRING — not real code!

// A naive complexity counter would count all these "if"/"for"/"while"
// keywords and report a complexity score that's completely wrong!</div></pre>

  <p>The solution: <strong>strip ALL comments and string literals before counting keywords</strong>. The <code>CommentStripper</code> does this with a 4-state machine. After stripping, the above becomes:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>After stripping — safe to count keywords</span></div><div class="code-body">                                                          
                                                            
std::string msg =                                    ;
// Everything outside real code is replaced with spaces.
// Line numbers are PRESERVED (crucial for accurate reporting).</div></pre>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/index.html
# ─────────────────────────────────────────────────────────────
P3_INDEX_CONTENT = """
<div class="section">
  <h2>📁 All the files at a glance</h2>
  <div class="card-grid">
    <a class="card" href="comment-stripper.html">
      <div class="card-icon">🔧</div>
      <div class="card-title">comment_stripper.cpp</div>
      <div class="card-desc">The 4-state machine that safely removes comments and string literals</div>
    </a>
    <a class="card" href="metrics-calculator.html">
      <div class="card-icon">📊</div>
      <div class="card-title">metrics_calculator.cpp</div>
      <div class="card-desc">Extracts functions, counts complexity, classifies risk</div>
    </a>
    <a class="card" href="dependency-graph.html">
      <div class="card-icon">🕸️</div>
      <div class="card-title">dependency_graph.cpp</div>
      <div class="card-desc">Builds the include graph, detects circular dependencies with DFS</div>
    </a>
    <a class="card" href="json-exporter.html">
      <div class="card-icon">📄</div>
      <div class="card-title">json_exporter.cpp</div>
      <div class="card-desc">Manually builds JSON output — zero external dependencies</div>
    </a>
    <a class="card" href="main-cpp.html">
      <div class="card-icon">🚀</div>
      <div class="card-title">main.cpp</div>
      <div class="card-desc">CLI pipeline — orchestrates all components, prints results</div>
    </a>
    <a class="card" href="graph-builder-py.html">
      <div class="card-icon">🐍</div>
      <div class="card-title">graph_builder.py</div>
      <div class="card-desc">Transforms JSON into D3-ready nodes and edges</div>
    </a>
    <a class="card" href="html-generator-py.html">
      <div class="card-icon">🌐</div>
      <div class="card-title">html_generator.py</div>
      <div class="card-desc">Assembles the final self-contained HTML report</div>
    </a>
    <a class="card" href="viz-js.html">
      <div class="card-icon">✨</div>
      <div class="card-title">D3.js Visualization</div>
      <div class="card-desc">Force-directed graph, click interactions, risk coloring</div>
    </a>
  </div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/comment-stripper.html
# ─────────────────────────────────────────────────────────────
P3_CS_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>CommentStripper</code> removes all comments (<code>//</code> and <code>/* */</code>) and string literals from C++ source code. It does this using a <strong>4-state machine</strong> — a loop that reads one character at a time and keeps track of what "mode" it's in.</p>
  <div class="callout warn"><strong>Why not just use regex?</strong> A regex like <code>//.*$</code> would fail on strings containing <code>//</code>, like <code>std::string url = "https://example.com"</code>. The state machine handles all these edge cases correctly.</div>
</div>

<div class="section">
  <h2>🔄 The 4 states</h2>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace;font-size:12px">
                ┌─────────────────────────────────────────────┐
                │                                             │
                ▼                                             │
         ┌────────────┐   // found   ┌──────────────────┐   │
         │            │─────────────▶│  LINE_COMMENT    │   │
         │    CODE    │              │  emit spaces     │   │
         │            │   /* found   └──────┬───────────┘   │
         │  (normal   │─────────────▶┌──────▼───────────┐   │
         │   code)    │              │  BLOCK_COMMENT   │   │
         │            │   " or '     └──────┬───────────┘   │
         │            │─────────────▶┌──────▼───────────┐   │
         └────────────┘              │     STRING       │   │
                ▲                   │  (in quotes)     │───┘
                │                   └──────────────────┘
                │         \n found
                └─────────────────────────────────────────────

KEY: All states preserve \n (newlines) so line numbers stay accurate!
     Non-code content is replaced with SPACES, not deleted.
</pre>
  </div>
</div>

<div class="section">
  <h2>📁 The strip() function — annotated</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>comment_stripper.cpp</span></div><div class="code-body">std::string CommentStripper::strip(const std::string&amp; source) const {
    std::string result;
    result.reserve(source.size());  // same size as input

    State state = State::CODE;      // start in CODE state
    const std::size_t len = source.size();

    for (std::size_t i = 0; i &lt; len; ++i) {
        const char c  = source[i];            // current character
        const char nc = (i + 1 &lt; len) ? source[i + 1] : '\0'; // next char (lookahead)

        switch (state) {

        case State::CODE:
            if (c == '/' &amp;&amp; nc == '/') {      // detected "//"
                result += "  ";               // two chars in, two spaces out
                state = State::LINE_COMMENT;
                ++i;                          // skip the second '/'
            } else if (c == '/' &amp;&amp; nc == '*') { // detected "/*"
                result += "  ";
                state = State::BLOCK_COMMENT;
                ++i;                          // skip '*'
            } else if (c == '"' || c == '\'') { // string start
                result += ' ';
                state = State::STRING;
            } else if (c == '\n') {
                result += '\n';               // ALWAYS preserve newlines!
            } else {
                result += c;                  // normal code — copy as-is
            }
            break;

        case State::LINE_COMMENT:
            if (c == '\n') {
                result += '\n';               // end of line = end of comment
                state = State::CODE;
            } else {
                result += ' ';               // comment content → space
            }
            break;

        case State::BLOCK_COMMENT:
            if (c == '*' &amp;&amp; nc == '/') {     // detected closing "*/"
                result += "  ";
                state = State::CODE;
                ++i;                         // skip '/'
            } else if (c == '\n') {
                result += '\n';              // preserve newline inside block!
            } else {
                result += ' ';
            }
            break;

        case State::STRING:
            if (c == '\\' &amp;&amp; nc == '"') {   // escaped quote: \"
                result += "  ";
                ++i;                         // skip both chars
            } else if (c == '"' || c == '\'') { // end of string
                result += ' ';
                state = State::CODE;
            } else if (c == '\n') {
                result += '\n';              // unterminated string
                state = State::CODE;
            } else {
                result += ' ';              // string content → space
            }
            break;
        }
    }
    return result;
}</div></pre>
</div>

<div class="section">
  <h2>✅ A worked example</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Input to strip()</span></div><div class="code-body">// This counts patients
int countP(/* all of them */ int n) {
    std::string msg = "if you see this, bug!";
    return n; // done
}</div></pre>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Output from strip() — same line count, comments/strings → spaces</span></div><div class="code-body">                     
int countP(              int n) {
    std::string msg =                      ;
    return n;       
}</div></pre>
  <p>Notice: the same number of lines! The function body is still recognizable. Keywords inside the string and comment are gone, so complexity counting will be accurate.</p>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/metrics-calculator.html
# ─────────────────────────────────────────────────────────────
P3_MC_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>MetricsCalculator</code> takes stripped C++ source and extracts every function, computing complexity, nesting depth, parameter count, and risk rating for each one.</p>
</div>

<div class="section">
  <h2>🔍 How function extraction works</h2>
  <ol class="steps">
    <li><div class="step-num">1</div><div>Split the stripped source into lines with <code>splitLines()</code></div></li>
    <li><div class="step-num">2</div><div>For each line, try to match the function signature regex (looking for <code>returnType name(params)</code>)</div></li>
    <li><div class="step-num">3</div><div>Filter out control flow keywords (<code>if</code>, <code>for</code>, <code>while</code>) that look like functions but aren't</div></li>
    <li><div class="step-num">4</div><div>Scan forward to find the opening <code>{</code> brace</div></li>
    <li><div class="step-num">5</div><div>Count braces to find the matching closing <code>}</code> — this gives us the function body</div></li>
    <li><div class="step-num">6</div><div>Compute complexity, nesting depth, and parameter count on the body</div></li>
    <li><div class="step-num">7</div><div>Classify risk and store the result</div></li>
  </ol>
</div>

<div class="section">
  <h2>📊 Complexity calculation</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp</span></div><div class="code-body">int MetricsCalculator::calculateComplexity(const std::string&amp; body) const {
    int complexity = 1;  // baseline: every function has at least 1 path

    // Count whole-word branch keywords:
    static const std::vector&lt;std::string&gt; keywords = {
        "if", "for", "while", "do", "case", "catch"
    };
    for (const auto&amp; kw : keywords) {
        complexity += countWholeWordOccurrences(body, kw);
    }

    // Count logical operators (each adds a decision point):
    complexity += countOp("&amp;&amp;");   // AND
    complexity += countOp("||");   // OR
    complexity += countOp("?");    // ternary

    return complexity;
}</div></pre>

  <div class="callout info"><strong>Example:</strong> A function with 2 <code>if</code>s, 1 <code>for</code>, and 1 <code>&amp;&amp;</code> has complexity = 1 + 2 + 1 + 1 = <strong>5</strong> → low risk.</div>
</div>

<div class="section">
  <h2>🎯 Risk classification</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp</span></div><div class="code-body">std::string MetricsCalculator::classifyRisk(int complexity, int nestingDepth) const {
    if (complexity &gt;= 11 || nestingDepth &gt;= 4) return "high";
    if (complexity &gt;= 6  || nestingDepth &gt;= 4) return "medium";
    return "low";
}</div></pre>

  <table class="tbl">
    <tr><th>Risk</th><th>CC Score</th><th>Nesting Depth</th><th>Meaning</th></tr>
    <tr><td><span class="badge low">LOW</span></td><td>1–5</td><td>0–3</td><td>Simple, easy to test and maintain</td></tr>
    <tr><td><span class="badge med">MEDIUM</span></td><td>6–10</td><td>—</td><td>Somewhat complex, review carefully</td></tr>
    <tr><td><span class="badge high">HIGH</span></td><td>11+</td><td>4+</td><td>Complex! Hard to test, refactor needed</td></tr>
  </table>
</div>

<div class="section">
  <h2>📐 Line counting strategy</h2>
  <p>The line counter compares the raw source with the stripped source to classify each line:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp — countLines()</span></div><div class="code-body">for (int i = 0; i &lt; lineCount; ++i) {
    const std::string rawTrimmed = trim(rawLines[i]);
    const std::string strTrimmed = trim(strippedLines[i]);

    if (rawTrimmed.empty()) {
        ++blank;             // empty in raw → blank line
    } else if (strTrimmed.empty()) {
        ++comment;           // had content in raw but empty in stripped → comment line
    } else {
        ++code;              // has content in both → code line
    }
}</div></pre>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/dependency-graph.html
# ─────────────────────────────────────────────────────────────
P3_DG_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>DependencyGraph</code> builds a directed graph of <code>#include</code> relationships between files. It stores the graph as an adjacency list using <code>unordered_map</code>, and detects circular dependencies using DFS (Depth-First Search).</p>
</div>

<div class="section">
  <h2>🗺️ The graph data structure</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.h</span></div><div class="code-body">// The whole graph is just ONE map:
// filename → list of files it directly includes
std::unordered_map&lt;std::string, std::vector&lt;std::string&gt;&gt; graph_;

// Example state after analyzing a project:
// {
//   "main.cpp"          : ["comment_stripper.h", "metrics_calculator.h", ...],
//   "metrics_calculator.cpp" : ["metrics_calculator.h"],
//   "comment_stripper.h"     : [],
//   ...
// }</div></pre>
</div>

<div class="section">
  <h2>🔍 extractIncludes() — finding #include lines</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.cpp</span></div><div class="code-body">std::vector&lt;std::string&gt; DependencyGraph::extractIncludes(const std::string&amp; source) const {
    std::vector&lt;std::string&gt; includes;

    // Only match LOCAL includes: #include "file.h"
    // IGNORE system includes:   #include &lt;iostream&gt;
    static const std::regex localInclude(R"re(^\s*#include\s*"([^"]+)")re");

    std::istringstream stream(source);
    std::string line;
    while (std::getline(stream, line)) {
        std::smatch match;
        if (std::regex_search(line, match, localInclude)) {
            std::string includePath = match[1].str();
            // Get just the filename: "utils/patient.h" → "patient.h"
            const auto slashPos = includePath.find_last_of("/\\\\");
            if (slashPos != std::string::npos)
                includePath = includePath.substr(slashPos + 1);
            includes.push_back(includePath);
        }
    }
    return includes;
}</div></pre>
</div>

<div class="section">
  <h2>🔄 DFS Circular Dependency Detection</h2>
  <p>The project uses DFS (Depth-First Search) with a "currently in stack" set to detect cycles. This is the classic algorithm for cycle detection in directed graphs:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.cpp — DFS</span></div><div class="code-body">bool DependencyGraph::dfs(const std::string&amp; node,
                           std::unordered_set&lt;std::string&gt;&amp; visited,  // seen nodes
                           std::unordered_set&lt;std::string&gt;&amp; inStack,  // current DFS path
                           std::vector&lt;std::string&gt;&amp; path,            // current path
                           std::vector&lt;std::string&gt;&amp; cycles) const {  // found cycles

    visited.insert(node);   // mark as seen
    inStack.insert(node);   // mark as on current path
    path.push_back(node);

    for (const auto&amp; neighbor : graph_.at(node)) {
        if (visited.find(neighbor) == visited.end()) {
            dfs(neighbor, visited, inStack, path, cycles);  // recurse
        } else if (inStack.find(neighbor) != inStack.end()) {
            // ↑ neighbor is ALREADY on our current path → CYCLE!
            // Build the cycle string: "a.cpp → b.h → a.cpp"
            std::string cycle;
            bool found = false;
            for (const auto&amp; n : path) {
                if (n == neighbor) found = true;
                if (found) cycle += n + " → ";
            }
            cycle += neighbor;
            cycles.push_back(cycle);
        }
    }

    path.pop_back();         // leaving this node
    inStack.erase(node);     // no longer on current path
    return false;
}</div></pre>
</div>

<div class="section">
  <h2>⚡ Lazy caching with mutable</h2>
  <p>Cycle detection is expensive, so it's only computed once and cached. The <code>mutable</code> keyword allows a <code>const</code> method to modify the cache:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.h — mutable cache</span></div><div class="code-body">// mutable = "even const methods can change this"
mutable std::vector&lt;std::string&gt; circularDeps_;
mutable bool circularDepsComputed_ = false;

// In detectCircularDependencies():
if (circularDepsComputed_) {
    return circularDeps_;   // return cached result
}
// ... expensive DFS computation ...
circularDepsComputed_ = true;  // mark as done
return circularDeps_;</div></pre>
  <div class="callout info"><strong>Python equivalent</strong> This is like <code>@functools.lru_cache</code> — compute once, return cached result on subsequent calls.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/json-exporter.html
# ─────────────────────────────────────────────────────────────
P3_JE_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>JsonExporter</code> takes all the computed metrics and dependency graph data and writes them to a JSON file. It builds the JSON entirely by hand using <code>std::ostringstream</code> — no external JSON library is used.</p>
</div>

<div class="section">
  <h2>📄 The JSON contract</h2>
  <p>The output follows a strict schema. Here's the real output from analyzing the sample files:</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>demo.json — real output</span></div><div class="code-body">{
  "project": "Sample Files",
  "analyzed_at": "2026-04-29T17:44:09",
  "analyzer_version": "1.0.0",
  "summary": {
    "total_files": 3,
    "total_functions": 9,
    "total_lines": 145,
    "avg_complexity": 3.8,
    "max_complexity": 14,
    "riskiest_file": "complex.cpp",
    "riskiest_function": "processData",
    "high_risk_count": 1,
    "medium_risk_count": 1,
    "low_risk_count": 7
  },
  "files": [
    {
      "name": "complex.cpp",
      "complexity_score": 25,
      "risk": "high",
      "functions": [
        {
          "name": "processData",
          "complexity": 14,
          "nesting_depth": 5,
          "risk": "high",
          "risk_reasons": ["high_complexity", "deep_nesting"]
        }
      ]
    }
  ]
}</div></pre>
</div>

<div class="section">
  <h2>🏗️ The builder pattern</h2>
  <p>The exporter uses a hierarchical builder pattern — each method builds one section:</p>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace;font-size:12px">
exportToFile()
    └── buildJson()
            ├── buildSummary()
            ├── buildFileObject() × N files
            │       └── buildFunctionObject() × M functions per file
            └── buildDependencyGraph()
</pre>
  </div>
</div>

<div class="section">
  <h2>📏 The indent() helper</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp</span></div><div class="code-body">// Returns N*2 spaces: indent(1)="  ", indent(2)="    ", indent(3)="      "
std::string JsonExporter::indent(int level) const {
    return std::string(static_cast&lt;std::size_t&gt;(level) * 2, ' ');
}

// Used like:
j &lt;&lt; indent(1) &lt;&lt; "\"summary\": {\n";
j &lt;&lt; indent(2) &lt;&lt; "\"total_files\": " &lt;&lt; files.size() &lt;&lt; ",\n";
j &lt;&lt; indent(2) &lt;&lt; "\"avg_complexity\": " &lt;&lt; avgStr.str() &lt;&lt; ",\n";
j &lt;&lt; indent(1) &lt;&lt; "},\n";</div></pre>
</div>

<div class="section">
  <h2>⏰ The timestamp</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>json_exporter.cpp — ISO-8601 timestamp</span></div><div class="code-body">std::string JsonExporter::currentTimestamp() const {
    const std::time_t now = std::time(nullptr);
    std::tm tm_utc = {};
#ifdef _WIN32
    gmtime_s(&amp;tm_utc, &amp;now);   // Windows thread-safe version
#else
    gmtime_r(&amp;now, &amp;tm_utc);   // Linux/macOS thread-safe version
#endif
    std::ostringstream oss;
    oss &lt;&lt; (tm_utc.tm_year + 1900) &lt;&lt; "-"    // years since 1900!
        &lt;&lt; std::setfill('0') &lt;&lt; std::setw(2) &lt;&lt; (tm_utc.tm_mon + 1) &lt;&lt; "-"
        &lt;&lt; std::setfill('0') &lt;&lt; std::setw(2) &lt;&lt; tm_utc.tm_mday;
    // Output: "2026-04-29T17:44:09"
    return oss.str();
}</div></pre>
  <div class="callout info"><strong>Note:</strong> <code>tm_year</code> is years since 1900, and <code>tm_mon</code> is 0-indexed (January = 0). Classic C API quirks! That's why you see <code>tm_year + 1900</code> and <code>tm_mon + 1</code>.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/main-cpp.html
# ─────────────────────────────────────────────────────────────
P3_MAIN_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>main.cpp</code> is the entry point and orchestrator. It handles CLI arguments, collects files, runs each component in sequence, prints a colored summary to the terminal, and triggers the JSON export.</p>
</div>

<div class="section">
  <h2>🚀 The main pipeline</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp — the core pipeline</span></div><div class="code-body">CommentStripper   stripper;
MetricsCalculator calculator;
DependencyGraph   depGraph;
JsonExporter      exporter;

std::vector&lt;FileMetrics&gt; allMetrics;

for (const auto&amp; filePath : files) {
    // Step 1: Read raw source
    const std::string raw      = readFile(filePath);

    // Step 2: Strip comments and strings
    const std::string stripped = stripper.strip(raw);

    // Step 3: Compute complexity metrics
    const FileMetrics metrics  = calculator.analyze(raw, stripped, filePath.string());

    // Step 4: Extract #include dependencies
    const auto includes = depGraph.extractIncludes(raw);  // use RAW source!
    depGraph.addFile(metrics.name, includes);

    allMetrics.push_back(metrics);
}

// Step 5: Export everything to JSON
exporter.exportToFile(allMetrics, depGraph, projectName, outputPath);</div></pre>

  <div class="callout tip"><strong>Why extract includes from raw, not stripped?</strong> <code>#include</code> directives are never inside comments or strings in valid C++ code. But more importantly, we use the raw source to be safe — we don't want stripping to accidentally remove an include line.</div>
</div>

<div class="section">
  <h2>🎨 Terminal colors with ANSI codes</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp — ANSI color namespace</span></div><div class="code-body">namespace Color {
    constexpr const char* RESET  = "\033[0m";  // back to normal
    constexpr const char* RED    = "\033[31m";
    constexpr const char* YELLOW = "\033[33m";
    constexpr const char* GREEN  = "\033[32m";
    constexpr const char* CYAN   = "\033[36m";
    constexpr const char* BOLD   = "\033[1m";
}

// Usage:
std::cout &lt;&lt; Color::RED &lt;&lt; "Error: --path is required.\n" &lt;&lt; Color::RESET;</div></pre>
  <p>These are ANSI escape codes — special byte sequences that terminals interpret as color commands. <code>\033[31m</code> means "switch text color to red". <code>\033[0m</code> resets everything back to default.</p>
</div>

<div class="section">
  <h2>📁 Collecting files with std::filesystem (C++17)</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>main.cpp — file collection</span></div><div class="code-body">namespace fs = std::filesystem;  // alias for convenience

static std::vector&lt;fs::path&gt; collectCppFiles(const fs::path&amp; dir) {
    std::vector&lt;fs::path&gt; files;
    // recursive_directory_iterator walks ALL subdirectories
    for (const auto&amp; entry : fs::recursive_directory_iterator(dir)) {
        if (!entry.is_regular_file()) continue;  // skip dirs, symlinks
        const auto ext = entry.path().extension().string();
        if (ext == ".cpp" || ext == ".h" || ext == ".hpp" || ext == ".cc") {
            files.push_back(entry.path());
        }
    }
    std::sort(files.begin(), files.end());  // alphabetical order
    return files;
}</div></pre>
  <div class="callout info"><strong>Python equivalent</strong> <code>list(Path(dir).rglob("*.cpp")) + list(Path(dir).rglob("*.h"))</code></div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/graph-builder-py.html
# ─────────────────────────────────────────────────────────────
P3_GB_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>graph_builder.py</code> is the bridge between the C++ world and the D3.js world. It reads the JSON produced by the C++ analyzer and transforms it into exactly the format D3.js needs for force-directed graphs.</p>
</div>

<div class="section">
  <h2>🔄 The transformation</h2>
  <div class="compare">
    <div class="cmp-card python">
      <div class="cmp-head">📥 INPUT — from C++ (output.json)</div>
      <div class="cmp-body">
<pre><div class="code-body">{
  "files": [
    {
      "name": "complex.cpp",
      "complexity_score": 25,
      "risk": "high",
      "function_count": 3,
      ...
    }
  ]
}</div></pre>
      </div>
    </div>
    <div class="cmp-card cpp">
      <div class="cmp-head">📤 OUTPUT — D3-ready nodes</div>
      <div class="cmp-body">
<pre><div class="code-body">{
  "nodes": [
    {
      "id": "complex.cpp",
      "complexity": 25,
      "risk": "high",
      "color": "#ef4444",
      "radius": 40.0,
      "label": "HIGH RISK",
      "functions": [...]
    }
  ],
  "edges": [...]
}</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>📐 Node radius calculation</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>graph_builder.py</span></div><div class="code-body">def build_nodes(files, max_complexity):
    nodes = []
    for f in files:
        complexity = f.get("complexity_score", 0)
        risk       = f.get("risk", "low")

        # Radius: 15px (min, lowest complexity) to 40px (max, highest complexity)
        # Formula: 15 + (my_complexity / max_complexity) * 25
        if max_complexity > 0:
            radius = 15 + (complexity / max_complexity) * 25
        else:
            radius = 15.0

        # Top 5 riskiest functions for the tooltip popup
        funcs = sorted(f.get("functions", []),
                       key=lambda fn: fn.get("complexity", 0),
                       reverse=True)[:5]

        node = {
            "id":        f.get("name", ""),
            "color":     RISK_COLORS.get(risk, "#22c55e"),
            "radius":    round(radius, 1),
            "functions": funcs,
            ...
        }
        nodes.append(node)
    return nodes</div></pre>
</div>

<div class="section">
  <h2>🎨 Risk colors</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>graph_builder.py</span></div><div class="code-body">RISK_COLORS = {
    "high":   "#ef4444",   # red
    "medium": "#f59e0b",   # amber
    "low":    "#22c55e",   # green
}

RISK_LABELS = {
    "high":   "HIGH RISK",
    "medium": "MEDIUM RISK",
    "low":    "LOW RISK",
}</div></pre>
</div>

<div class="section">
  <h2>🔗 Edge filtering</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>graph_builder.py</span></div><div class="code-body">def build_edges(dependency_graph, node_ids):
    edges = []
    seen = set()  # deduplicate edges

    for raw_edge in dependency_graph.get("edges", []):
        src = raw_edge.get("from", "")
        tgt = raw_edge.get("to", "")

        # Skip edges where either endpoint isn't an analyzed file
        # (e.g., system headers like &lt;iostream&gt; that we filtered out)
        if src not in node_ids or tgt not in node_ids:
            continue

        if (src, tgt) in seen:
            continue   # skip duplicate edges

        seen.add((src, tgt))
        edges.append({"source": src, "target": tgt, "strength": 1})

    return edges</div></pre>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/html-generator-py.html
# ─────────────────────────────────────────────────────────────
P3_HG_CONTENT = """
<div class="section">
  <h2>🎯 What this file does</h2>
  <p><code>html_generator.py</code> is the final step in the pipeline. It takes the D3-ready data from <code>graph_builder.py</code> and embeds it into a single, self-contained HTML file that contains everything — HTML structure, CSS styles, D3.js library code, and the actual data — all in one file.</p>
</div>

<div class="section">
  <h2>📦 Self-contained HTML — how it works</h2>
  <p>The generated HTML file embeds everything inline so it needs no internet connection or local server to work:</p>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace;font-size:12px">
report.html (single file, ~300KB)
├── &lt;style&gt; ... &lt;/style&gt;          CSS styles inline
├── &lt;script&gt;D3.js source&lt;/script&gt;  D3 library inline (minified)
└── &lt;script&gt;
      // All data embedded as JavaScript variables:
      const graphData = { nodes: [...], edges: [...] };
      const summary   = { total_functions: 9, ... };

      // D3 force simulation code
      const simulation = d3.forceSimulation(graphData.nodes)...
    &lt;/script&gt;
</pre>
  </div>
</div>

<div class="section">
  <h2>🏗️ How html_generator.py works (inferred from output)</h2>
  <p>Based on the generated <code>report.html</code> and <code>demo.html</code>, here's what the generator does:</p>
  <ol class="steps">
    <li><div class="step-num">1</div><div>Load the <code>output.json</code> file using <code>graph_builder.load_json()</code></div></li>
    <li><div class="step-num">2</div><div>Call <code>graph_builder.build_graph_data()</code> to get D3-ready nodes and edges</div></li>
    <li><div class="step-num">3</div><div>Serialize the transformed data as a JavaScript variable: <code>const graphData = JSON.stringify(data)</code></div></li>
    <li><div class="step-num">4</div><div>Build an HTML template string with the data embedded in a <code>&lt;script&gt;</code> tag</div></li>
    <li><div class="step-num">5</div><div>Write the complete HTML to <code>report.html</code></div></li>
    <li><div class="step-num">6</div><div>Open the file in the default browser automatically</div></li>
  </ol>
</div>

<div class="section">
  <h2>📊 The generated dashboard sections</h2>
  <table class="tbl">
    <tr><th>Section</th><th>What it shows</th></tr>
    <tr><td>Hero stats panel</td><td>Total functions, avg complexity, max CC, riskiest function</td></tr>
    <tr><td>Force-directed graph</td><td>Nodes (files) sized by complexity, colored by risk, edges = includes</td></tr>
    <tr><td>Sidebar details</td><td>Click any node → shows file details + top risky functions</td></tr>
    <tr><td>Risk legend</td><td>Color key: green=low, amber=medium, red=high</td></tr>
    <tr><td>Circular deps warning</td><td>Red warning banner if any cycles detected</td></tr>
  </table>
</div>

<div class="section">
  <h2>💡 Key design: data-over-protocol</h2>
  <p>The HTML file uses <code>data:</code> URIs and inline everything — no CDN, no network calls at runtime. This means the report works offline, can be emailed as an attachment, and opens instantly.</p>
  <div class="callout key"><strong>Interview point:</strong> "The report is self-contained. I embed the D3.js library inline (minified) and serialize all the graph data as a JavaScript constant in a &lt;script&gt; tag. This means the report is a single portable file — no server, no internet, no dependencies at runtime."</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase3/viz-js.html
# ─────────────────────────────────────────────────────────────
P3_VIZ_CONTENT = """
<div class="section">
  <h2>🎯 What D3.js does here</h2>
  <p>D3.js (Data-Driven Documents) is used to create the force-directed graph visualization. Each file becomes a circle (node) and each <code>#include</code> relationship becomes a line (edge). The physics simulation makes the graph self-organize into a readable layout.</p>
</div>

<div class="section">
  <h2>⚡ Force-directed graphs — the concept</h2>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace;font-size:12px">
Imagine the nodes as BALLS and the edges as SPRINGS:

  [main.cpp] ←──── spring ────→ [comment_stripper.h]

Forces applied every frame:
  ⊖ Charge force: nodes REPEL each other (like magnets, same pole)
  ⊕ Link force:  edges ATTRACT connected nodes
  ⊕ Center force: everything pulled toward screen center
  ⊕ Collision:   nodes bounce off each other

The simulation runs for ~300 iterations until it reaches equilibrium.
Result: naturally clustered layout where related files end up near each other.
</pre>
  </div>
</div>

<div class="section">
  <h2>📁 D3 force simulation setup</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Inside report.html — D3 simulation code</span></div><div class="code-body">const simulation = d3.forceSimulation(graphData.nodes)
    .force("link", d3.forceLink(graphData.edges)
        .id(d =&gt; d.id)          // match edges to nodes by id
        .distance(120))          // target edge length in pixels
    .force("charge", d3.forceManyBody()
        .strength(-300))         // repulsion force (negative = repel)
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide()
        .radius(d =&gt; d.radius + 10));  // no overlapping nodes</div></pre>
</div>

<div class="section">
  <h2>🎨 Drawing the nodes</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>D3 node rendering</span></div><div class="code-body">// Create circle elements for each node
const node = svg.append("g")
    .selectAll("circle")
    .data(graphData.nodes)
    .enter().append("circle")
    .attr("r", d =&gt; d.radius)      // radius from graph_builder.py
    .attr("fill", d =&gt; d.color)    // color: red/amber/green
    .attr("stroke", "#fff")
    .attr("stroke-width", 2)
    .call(drag(simulation));        // make nodes draggable</div></pre>
</div>

<div class="section">
  <h2>🖱️ Click interaction — file details</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>D3 click handler</span></div><div class="code-body">node.on("click", (event, d) =&gt; {
    // d = the node's data object from graph_builder.py
    // Show the details panel on the right
    detailPanel.style("display", "block");
    detailTitle.text(d.name);
    detailRisk.text(d.label).style("color", d.color);
    detailLines.text(d.total_lines + " total lines");
    detailFunctions.text(d.function_count + " functions");

    // List the top risky functions
    functionList.selectAll("*").remove();
    d.functions.forEach(fn =&gt; {
        functionList.append("div")
            .html(`&lt;strong&gt;${fn.name}()&lt;/strong&gt; — CC: ${fn.complexity}`);
    });
});</div></pre>
</div>

<div class="section">
  <h2>🔄 Animation — tick function</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>D3 animation loop</span></div><div class="code-body">// Called on every frame of the physics simulation:
simulation.on("tick", () =&gt; {
    // Update edge positions:
    link
        .attr("x1", d =&gt; d.source.x)
        .attr("y1", d =&gt; d.source.y)
        .attr("x2", d =&gt; d.target.x)
        .attr("y2", d =&gt; d.target.y);

    // Update node positions:
    node
        .attr("cx", d =&gt; d.x)
        .attr("cy", d =&gt; d.y);

    // Update label positions:
    label
        .attr("x", d =&gt; d.x)
        .attr("y", d =&gt; d.y + d.radius + 14);
});</div></pre>
  <div class="callout info"><strong>How it works:</strong> The simulation updates <code>d.x</code> and <code>d.y</code> on each node every frame. The tick function just reads those values and repositions the SVG elements. D3 handles all the physics math internally.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase4/index.html
# ─────────────────────────────────────────────────────────────
P4_INDEX_CONTENT = """
<div class="section">
  <h2>🔢 Algorithms overview</h2>
  <p>This phase goes deep on the four key algorithms used in the project. Understanding these will let you explain your technical decisions confidently in any interview.</p>
  <div class="card-grid">
    <a class="card" href="cyclomatic-complexity.html">
      <div class="card-icon">📊</div>
      <div class="card-title">Cyclomatic Complexity</div>
      <div class="card-desc">How to measure code complexity — the math behind the scores</div>
    </a>
    <a class="card" href="state-machine.html">
      <div class="card-icon">🔄</div>
      <div class="card-title">Comment Stripping State Machine</div>
      <div class="card-desc">Why a state machine beats regex for this problem</div>
    </a>
    <a class="card" href="graph-traversal.html">
      <div class="card-icon">🕸️</div>
      <div class="card-title">DFS for Cycle Detection</div>
      <div class="card-desc">How we find circular dependencies in the include graph</div>
    </a>
    <a class="card" href="d3-simulation.html">
      <div class="card-icon">✨</div>
      <div class="card-title">D3 Force Simulation</div>
      <div class="card-desc">The physics behind the interactive graph layout</div>
    </a>
  </div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase4/cyclomatic-complexity.html
# ─────────────────────────────────────────────────────────────
P4_CC_CONTENT = """
<div class="section">
  <h2>🎯 What is Cyclomatic Complexity?</h2>
  <p>Cyclomatic Complexity (CC) is a number that measures how many independent paths of execution exist through a function. Invented by Thomas McCabe in 1976, it's the most widely used code complexity metric.</p>
  <p><strong>Simple rule: CC = 1 + number of decision points</strong></p>
  <p>A "decision point" is anything that creates a new branch in the code: <code>if</code>, <code>for</code>, <code>while</code>, <code>case</code>, <code>catch</code>, <code>&amp;&amp;</code>, <code>||</code>, and <code>?</code> (ternary).</p>
</div>

<div class="section">
  <h2>📝 Worked examples</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>CC = 1 (lowest possible — straight-line code)</span></div><div class="code-body">int add(int a, int b) {
    return a + b;    // 1 path: always add and return
}
// CC = 1 (baseline) + 0 decisions = 1</div></pre>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>CC = 3 (simple branching)</span></div><div class="code-body">std::string classifyRisk(int complexity) {
    if (complexity &gt;= 11) return "high";   // +1
    if (complexity &gt;= 6)  return "medium"; // +1
    return "low";
}
// CC = 1 + 2 ifs = 3</div></pre>

<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>CC = 14 (from demo.json — processData — HIGH RISK)</span></div><div class="code-body">// This function has something like:
void processData(vector&lt;T&gt;&amp; data, int max, bool flag) {
    if (data.empty()) return;           // +1 if
    for (auto&amp; item : data) {          // +1 for
        if (item.value &gt; max) {        // +1 if
            if (flag &amp;&amp; item.valid) {  // +1 if, +1 &amp;&amp;
                while (item.value &gt; 0) {  // +1 while
                    switch (item.type) {
                        case TYPE_A:    // +1 case
                        case TYPE_B:    // +1 case
                        case TYPE_C:    // +1 case
                        // ...more cases
                    }
                }
            } else if (item.value &lt; 0 || !item.valid) { // +1 else if, +1 ||
                // handle negative case
            }
        }
    }
}
// CC ≈ 1 + 13 decisions = 14 → HIGH RISK</div></pre>
</div>

<div class="section">
  <h2>⚙️ How this project calculates CC</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>metrics_calculator.cpp</span></div><div class="code-body">int MetricsCalculator::calculateComplexity(const std::string&amp; body) const {
    int complexity = 1;  // baseline

    // Keyword counting (whole-word to avoid false matches):
    // "if", "for", "while", "do", "case", "catch"
    for (const auto&amp; kw : keywords) {
        complexity += countWholeWordOccurrences(body, kw);
    }

    // Operator counting:
    complexity += countOp("&amp;&amp;");  // logical AND
    complexity += countOp("||");  // logical OR
    complexity += countOp("?");   // ternary (e.g. x = a ? b : c)

    return complexity;
}</div></pre>
  <div class="callout key"><strong>Why whole-word counting matters:</strong> Without whole-word checking, a function named <code>for_each</code> or a variable named <code>iffy</code> would incorrectly inflate the complexity score. The <code>countWholeWordOccurrences()</code> function checks that the surrounding characters are not alphanumeric or underscore.</div>
</div>

<div class="section">
  <h2>📊 What the numbers mean</h2>
  <table class="tbl">
    <tr><th>CC Score</th><th>Risk</th><th>What it means</th><th>Action</th></tr>
    <tr><td>1–5</td><td><span class="badge low">LOW</span></td><td>Simple, predictable function</td><td>No action needed</td></tr>
    <tr><td>6–10</td><td><span class="badge med">MEDIUM</span></td><td>Moderate complexity</td><td>Consider refactoring if growing</td></tr>
    <tr><td>11–15</td><td><span class="badge high">HIGH</span></td><td>Complex, hard to test</td><td>Refactor — split into smaller functions</td></tr>
    <tr><td>16+</td><td><span class="badge high">VERY HIGH</span></td><td>Untestable spaghetti</td><td>Urgent: requires major rewrite</td></tr>
  </table>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase4/state-machine.html
# ─────────────────────────────────────────────────────────────
P4_SM_CONTENT = """
<div class="section">
  <h2>🎯 What is a state machine?</h2>
  <p>A state machine (or finite automaton) is a program that can be in exactly one of a finite number of "states" at any time. It reads inputs and transitions between states based on rules.</p>
  <p>In our comment stripper, there are 4 states: <code>CODE</code>, <code>LINE_COMMENT</code>, <code>BLOCK_COMMENT</code>, <code>STRING</code>. The input is one character at a time. The rules are: what to do and where to go when you see each character in each state.</p>
</div>

<div class="section">
  <h2>📊 Complete state transition table</h2>
  <table class="tbl">
    <tr><th>Current State</th><th>Input</th><th>Action</th><th>Next State</th></tr>
    <tr><td rowspan="5"><code>CODE</code></td><td><code>//</code></td><td>emit 2 spaces</td><td><code>LINE_COMMENT</code></td></tr>
    <tr><td><code>/*</code></td><td>emit 2 spaces</td><td><code>BLOCK_COMMENT</code></td></tr>
    <tr><td><code>" or '</code></td><td>emit 1 space</td><td><code>STRING</code></td></tr>
    <tr><td><code>\n</code></td><td>emit \n (preserve!)</td><td><code>CODE</code></td></tr>
    <tr><td>anything else</td><td>emit char as-is</td><td><code>CODE</code></td></tr>
    <tr><td rowspan="2"><code>LINE_COMMENT</code></td><td><code>\n</code></td><td>emit \n</td><td><code>CODE</code></td></tr>
    <tr><td>anything else</td><td>emit space</td><td><code>LINE_COMMENT</code></td></tr>
    <tr><td rowspan="3"><code>BLOCK_COMMENT</code></td><td><code>*/</code></td><td>emit 2 spaces</td><td><code>CODE</code></td></tr>
    <tr><td><code>\n</code></td><td>emit \n (preserve!)</td><td><code>BLOCK_COMMENT</code></td></tr>
    <tr><td>anything else</td><td>emit space</td><td><code>BLOCK_COMMENT</code></td></tr>
    <tr><td rowspan="4"><code>STRING</code></td><td><code>\" or \'</code></td><td>emit 2 spaces</td><td><code>STRING</code></td></tr>
    <tr><td><code>" or '</code></td><td>emit space</td><td><code>CODE</code></td></tr>
    <tr><td><code>\n</code></td><td>emit \n</td><td><code>CODE</code></td></tr>
    <tr><td>anything else</td><td>emit space</td><td><code>STRING</code></td></tr>
  </table>
</div>

<div class="section">
  <h2>⚡ Why not regex?</h2>
  <div class="compare">
    <div class="cmp-card bad">
      <div class="cmp-head">❌ Why regex fails</div>
      <div class="cmp-body">
<pre><div class="code-body">// Regex approach (WRONG):
source = re.sub(r'//.*$', '', source, flags=re.M)
# FAILS on:
std::string url = "https://example.com";
//                         ^^ this "//" is inside a STRING!
# The regex would eat "example.com";</div></pre>
      </div>
    </div>
    <div class="cmp-card good">
      <div class="cmp-head">✅ Why state machine works</div>
      <div class="cmp-body">
<pre><div class="code-body">// State machine approach (CORRECT):
// When we see '"', we enter STRING state.
// In STRING state, we IGNORE everything including "//".
// We only exit STRING state when we see the closing '"'.
// So "https://example.com" is handled perfectly!</div></pre>
      </div>
    </div>
  </div>
</div>

<div class="section">
  <h2>⏱️ Complexity: O(n) time, O(1) space</h2>
  <p>The state machine visits each character exactly once — O(n) time where n is the source length. The state is just a single enum value — O(1) extra space (beyond the output string, which is the same size as input). This is optimal — you can't do better than reading every character once.</p>
  <div class="callout key"><strong>Interview answer</strong> "The state machine is O(n) time and O(1) extra space — optimal for this problem. A regex-based approach would be O(n) too but would give incorrect results for // or /* inside string literals. The state machine correctly handles all C++ comment and string literal edge cases."</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase4/graph-traversal.html
# ─────────────────────────────────────────────────────────────
P4_GT_CONTENT = """
<div class="section">
  <h2>🎯 The problem: detecting circular dependencies</h2>
  <p>A circular dependency is when file A includes B, which includes C, which includes A again. This creates an infinite loop in the compiler and is always a bug. We need to detect these automatically across the entire codebase.</p>
  <div class="diagram">
<pre style="background:transparent;border:none;padding:0;box-shadow:none;font-family:'Fira Code',monospace;font-size:12px">
     hospital.cpp
          │
          ▼
      patient.h ───────────┐
          │                │
          ▼                │
      record.h             │
          │                │
          ▼                │
      hospital.h ──────────┘  ← CYCLE! hospital.h → patient.h → hospital.h
</pre>
  </div>
</div>

<div class="section">
  <h2>🔍 DFS with an "in-stack" set — the algorithm</h2>
  <p>The classic algorithm uses two sets: <code>visited</code> (all nodes we've seen) and <code>inStack</code> (nodes on the current DFS path). A cycle exists when we reach a node that's already <code>inStack</code>.</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>Pseudocode</span></div><div class="code-body">function dfs(node):
    visited.add(node)
    inStack.add(node)
    path.push(node)

    for each neighbor of node:
        if neighbor NOT in visited:
            dfs(neighbor)       // explore unvisited neighbor
        elif neighbor IN inStack:
            // neighbor is on our current path → CYCLE!
            report_cycle(path, neighbor)

    path.pop()
    inStack.remove(node)        // leaving this node</div></pre>
</div>

<div class="section">
  <h2>📁 From the project: the real DFS</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>dependency_graph.cpp</span></div><div class="code-body">bool DependencyGraph::dfs(const std::string&amp; node,
                           std::unordered_set&lt;std::string&gt;&amp; visited,
                           std::unordered_set&lt;std::string&gt;&amp; inStack,
                           std::vector&lt;std::string&gt;&amp; path,
                           std::vector&lt;std::string&gt;&amp; cycles) const {
    visited.insert(node);
    inStack.insert(node);
    path.push_back(node);

    const auto it = graph_.find(node);
    if (it != graph_.end()) {
        for (const auto&amp; neighbor : it-&gt;second) {
            if (visited.find(neighbor) == visited.end()) {
                dfs(neighbor, visited, inStack, path, cycles);
            } else if (inStack.find(neighbor) != inStack.end()) {
                // Build human-readable cycle description:
                // "a.cpp -&gt; b.h -&gt; a.cpp"
                std::string cycle;
                bool found = false;
                for (const auto&amp; n : path) {
                    if (n == neighbor) found = true;
                    if (found) cycle += n + " -&gt; ";
                }
                cycle += neighbor;
                cycles.push_back(cycle);
            }
        }
    }

    path.pop_back();
    inStack.erase(node);
    return false;
}</div></pre>
</div>

<div class="section">
  <h2>⏱️ Complexity: O(V + E)</h2>
  <p>Where V = number of files (vertices) and E = number of include relationships (edges). Each node is visited at most once, and each edge is traversed at most once.</p>

  <div class="callout key"><strong>Interview answer</strong> "I use DFS with two sets: visited (all seen nodes) and inStack (current DFS path). A cycle is detected when we reach a node that's already in inStack — meaning we've looped back to a node we're currently exploring. Time complexity is O(V+E) where V is files and E is include relationships. Results are cached with a mutable flag so repeated queries are O(1)."</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase4/d3-simulation.html
# ─────────────────────────────────────────────────────────────
P4_D3_CONTENT = """
<div class="section">
  <h2>🎯 What is a force simulation?</h2>
  <p>D3's force simulation is a physics engine embedded in JavaScript. It treats graph nodes as physical objects with mass and simulates forces between them every frame until the graph reaches a stable equilibrium.</p>
</div>

<div class="section">
  <h2>⚡ The forces in play</h2>
  <table class="tbl">
    <tr><th>Force</th><th>Effect</th><th>Why we need it</th></tr>
    <tr><td><code>forceLink</code></td><td>Pulls connected nodes toward each other (spring)</td><td>Creates visual edges, keeps related files near each other</td></tr>
    <tr><td><code>forceManyBody</code></td><td>Repels all nodes from each other (negative gravity)</td><td>Prevents all nodes from collapsing to one point</td></tr>
    <tr><td><code>forceCenter</code></td><td>Gently pulls everything toward screen center</td><td>Keeps the graph visible — doesn't drift off screen</td></tr>
    <tr><td><code>forceCollide</code></td><td>Prevents nodes from overlapping (collision detection)</td><td>Nodes don't cover each other — all labels visible</td></tr>
  </table>
</div>

<div class="section">
  <h2>🔄 The simulation loop</h2>
  <p>The simulation runs for a fixed number of "ticks" (iterations). On each tick:</p>
  <ol class="steps">
    <li><div class="step-num">1</div><div>Apply all forces to each node — update velocity</div></li>
    <li><div class="step-num">2</div><div>Update each node's position based on velocity</div></li>
    <li><div class="step-num">3</div><div>Apply "alpha" decay — the system gradually "cools down" (α starts at 1.0, decays toward 0)</div></li>
    <li><div class="step-num">4</div><div>Fire the "tick" event — our code moves SVG elements to new positions</div></li>
    <li><div class="step-num">5</div><div>When alpha falls below threshold, stop simulating</div></li>
  </ol>
</div>

<div class="section">
  <h2>📐 Why radius scales with complexity</h2>
  <p>A key visual design decision: bigger nodes = more complex files. This makes the highest-risk files immediately obvious without reading any numbers.</p>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>graph_builder.py — radius formula</span></div><div class="code-body"># radius ranges from 15px (simplest) to 40px (most complex)
radius = 15 + (complexity / max_complexity) * 25

# Example with demo.json data:
# complex.cpp: complexity=25, max=25 → radius = 15 + 25*1.0 = 40px (biggest)
# simple.cpp:  complexity=3,  max=25 → radius = 15 + 25*0.12 = 18px (small)
# with_comments.cpp: complexity=6, max=25 → radius = 15+25*0.24 = 21px</div></pre>
</div>

<div class="section">
  <h2>🖱️ Drag interaction</h2>
<pre><div class="code-header"><div class="dots"><span></span><span></span><span></span></div><span>D3 drag behavior</span></div><div class="code-body">function drag(simulation) {
    return d3.drag()
        .on("start", (event, d) =&gt; {
            if (!event.active) simulation.alphaTarget(0.3).restart(); // reheat
            d.fx = d.x;   // fix position (don't let simulation move it)
            d.fy = d.y;
        })
        .on("drag", (event, d) =&gt; {
            d.fx = event.x;  // follow mouse
            d.fy = event.y;
        })
        .on("end", (event, d) =&gt; {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;  // unfix: simulation can move it again
            d.fy = null;
        });
}</div></pre>
  <div class="callout key"><strong>Why reheat on drag?</strong> When you drag a node, its neighbors need to rearrange. Setting <code>alphaTarget(0.3)</code> "reheats" the simulation so it reacts to the drag. When drag ends, we set alphaTarget back to 0 so the simulation cools down again.</div>
</div>
"""

# ─────────────────────────────────────────────────────────────
# phase5/index.html
# ─────────────────────────────────────────────────────────────
P5_CONTENT = """
<div class="section">
  <h2>🎤 How to use these answers</h2>
  <p>These are real questions interviewers ask about projects like this. Read the answers, understand them deeply, then close this page and say them in your own words. The goal is confident, specific answers — not memorization.</p>
  <div class="callout tip"><strong>Golden rule</strong> Always refer to specific code. "I used <code>std::unordered_map</code> because..." is infinitely better than "I used a hash map". Specificity signals genuine understanding.</div>
</div>

<div class="section">
  <h2>📦 Project Overview Questions</h2>

  <div class="qa-item">
    <div class="qa-q">Tell me about this project in 60 seconds.</div>
    <div class="qa-a">I built a C++17 static analyzer that measures cyclomatic complexity for every function in a C++ codebase. You point it at a folder, it analyzes all <code>.cpp</code> and <code>.h</code> files, and produces an interactive HTML report with a force-directed dependency graph. Nodes are sized by complexity and colored by risk level — green for safe, amber for medium, red for high risk. I designed it in three layers: a zero-dependency C++ analyzer, a Python data transformer, and a D3.js browser visualization, with a JSON contract between layers. The whole thing runs with a single command and produces a self-contained HTML file that works offline with no server needed.</div>
    <div class="int-tip">End with the user value: "a developer can instantly see which function is their biggest technical debt".</div>
  </div>

  <div class="qa-item">
    <div class="qa-q">What is Cyclomatic Complexity and why does it matter?</div>
    <div class="qa-a">Cyclomatic Complexity is a count of the independent execution paths through a function. The formula is: CC = 1 + number of decision points. A decision point is any branch: <code>if</code>, <code>for</code>, <code>while</code>, <code>case</code>, <code>catch</code>, and logical operators <code>&amp;&amp;</code>, <code>||</code>, and <code>?</code>. It matters because CC directly correlates with testability — a function with CC of 14 needs at least 14 test cases to achieve full branch coverage. Functions above CC 11 are classified as "high risk" in my tool and flagged for refactoring. In the sample files, <code>processData()</code> has CC 14 and nesting depth 5 — it's a textbook example of what to fix first.</div>
  </div>
</div>

<div class="section">
  <h2>🔧 C++ Technical Questions</h2>

  <div class="qa-item">
    <div class="qa-q">Why did you use a state machine for comment stripping instead of regex?</div>
    <div class="qa-a">A regex like <code>//.*$</code> fails on <code>std::string url = "https://example.com"</code> — the <code>//</code> inside the string literal would incorrectly match. C++ has four distinct "modes": normal code, line comment, block comment, and string literal. A 4-state machine handles all transitions correctly with O(n) time and O(1) extra space. The states are <code>CODE</code>, <code>LINE_COMMENT</code>, <code>BLOCK_COMMENT</code>, and <code>STRING</code>, with transitions based on character pairs like <code>//</code>, <code>/*</code>, <code>*/</code>, and escaped quotes. Critically, the machine preserves newlines in all states so line numbers remain accurate after stripping.</div>
    <div class="int-tip">You can draw the state diagram on a whiteboard during this answer — it always impresses.</div>
  </div>

  <div class="qa-item">
    <div class="qa-q">Why did you use unordered_map for the dependency graph?</div>
    <div class="qa-a">The dependency graph stores an adjacency list: filename → list of included filenames. During graph traversal, I need O(1) average-case lookup to check if a node exists and retrieve its neighbors. <code>std::unordered_map</code> provides that — it's a hash table. A sorted <code>std::map</code> would give O(log n) lookup, which is unnecessary overhead when I don't need the keys in any particular order. The graph_ member is <code>unordered_map&lt;string, vector&lt;string&gt;&gt;</code> — straightforward adjacency list representation.</div>
  </div>

  <div class="qa-item">
    <div class="qa-q">Why did you use const references everywhere?</div>
    <div class="qa-a">C++ passes function arguments by value (copy) by default. A <code>std::string</code> representing a full source file can be tens of thousands of characters — copying it on every function call would be wasteful. <code>const std::string&amp;</code> passes a reference (just a pointer) instead of a copy, eliminating memory allocation and copying. The <code>const</code> tells callers "I won't modify your string", which is both a contract and an optimization hint to the compiler. All my function signatures use const references for strings, vectors, and structs for exactly this reason.</div>
  </div>

  <div class="qa-item">
    <div class="qa-q">Explain RAII and how it's used in your project.</div>
    <div class="qa-a">RAII — Resource Acquisition Is Initialization — means a C++ object acquires its resource in the constructor and releases it in the destructor, which runs automatically when the object goes out of scope. In my project, <code>std::ifstream</code> opens a file in its constructor and closes it in its destructor — so <code>readFile()</code> never explicitly calls <code>close()</code>, and the file is guaranteed to close even if an exception is thrown. Same for <code>std::ofstream</code> in <code>exportToFile()</code>. Python's <code>with open()</code> statement provides the same guarantee, but in C++ it's automatic for all objects, not just context managers.</div>
  </div>
</div>

<div class="section">
  <h2>🏗️ Architecture Questions</h2>

  <div class="qa-item">
    <div class="qa-q">Why did you use three separate layers instead of one program?</div>
    <div class="qa-a">Separation of concerns. Each layer does what it's best at: C++ for fast character-by-character parsing and file I/O; Python for HTML generation (much cleaner string templating); D3.js for interactive physics-based visualization in the browser. Layers communicate through a JSON file — which means I can test the C++ analyzer independently by examining <code>output.json</code>, change the visualization without recompiling C++, or swap out the Python layer entirely. The JSON contract is the API between systems. I actually did test this — I have a <code>demo.json</code> that lets me develop the Python/D3 layer without running the C++ analyzer at all.</div>
  </div>

  <div class="qa-item">
    <div class="qa-q">How does the dependency graph detect circular dependencies?</div>
    <div class="qa-a">I use DFS with two data structures: a <code>visited</code> set of all nodes seen so far, and an <code>inStack</code> set of nodes on the current DFS path. When traversing neighbors, if I encounter a node that's already in <code>inStack</code> — meaning it's an ancestor in the current path — I've found a cycle. I reconstruct the cycle description by reading the current <code>path</code> vector from the cycle start to the repeated node. Time complexity is O(V+E) where V is files and E is include relationships. Results are cached using a <code>mutable</code> flag so the expensive DFS only runs once.</div>
  </div>
</div>

<div class="section">
  <h2>💼 CV / Resume Questions</h2>

  <div class="qa-item">
    <div class="qa-q">What was the hardest technical challenge in this project?</div>
    <div class="qa-a">The comment stripping was the subtlest problem. My first attempt used regex and kept getting wrong complexity scores — the issue was <code>//</code> inside string literals, and block comments spanning multiple lines with embedded keywords. The 4-state machine solution was the correct approach: it handles all C++ comment and string literal forms in a single O(n) pass. Preserving newlines inside block comments (so line numbers stay accurate after stripping) was the detail that tripped me up — the block comment state had to emit <code>\n</code> for newlines rather than replacing them with spaces.</div>
    <div class="int-tip">Interviewers love "I tried X, it failed because Y, so I switched to Z". It shows problem-solving process, not just the solution.</div>
  </div>

  <div class="qa-item">
    <div class="qa-q">What would you improve if you had more time?</div>
    <div class="qa-a">Three things: First, I'd replace the regex-based function detection with a proper recursive descent parser for C++ function signatures — the regex approach is good but misses some template function signatures. Second, I'd add a CI/CD integration mode — output a non-zero exit code when any function exceeds a configurable CC threshold, so teams can fail builds on new high-risk functions. Third, I'd add trend tracking — store historical JSON reports and show a chart of how complexity changed over time. Currently it's a snapshot; with history it becomes a monitoring tool.</div>
  </div>
</div>
"""

# ═════════════════════════════════════════════════════════════
# BUILD ALL PAGES
# ═════════════════════════════════════════════════════════════

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path.replace(BASE+'/', '')}")


# index.html
write(f"{BASE}/index.html", make_page(
    "C++ Code Complexity Visualizer — Learning Hub",
    "A beginner-friendly guide to every concept, algorithm, and design decision in this project.",
    "Overview", "#374151",
    [("Home", "")],
    INDEX_CONTENT, "home", False
))

# phase1/index.html
write(f"{BASE}/phase1/index.html", make_page(
    "Phase 1 — C++17 Deep Dive",
    "Modern C++ concepts explained for Python developers — with real examples from the project.",
    "Phase 1", "#4338ca",
    [("Home", "index.html"), ("Phase 1", "")],
    P1_INDEX_CONTENT, "p1", True
))

# phase1 sub-pages
p1_pages = [
    ("string-vs-python.html", "std::string vs Python str",
     "Mutable strings, reserve(), and why C++ string handling is different from Python.",
     "p1-str", P1_STRING_CONTENT),
    ("file-io.html", "File I/O in C++",
     "ifstream, ofstream, and ostringstream — reading and writing files the C++ way.",
     "p1-fio", P1_FILEIO_CONTENT),
    ("unordered-map.html", "unordered_map — C++'s Dictionary",
     "Hash maps in C++ — like Python dict but with explicit types and O(1) lookup guarantees.",
     "p1-map", P1_MAP_CONTENT),
    ("struct-vs-class.html", "struct vs class",
     "The only real difference is default visibility. When to use each in practice.",
     "p1-sc", P1_STRUCT_CONTENT),
    ("const-references.html", "const & References",
     "The most important C++ parameter style — pass by reference without copying.",
     "p1-cr", P1_CONSTREF_CONTENT),
    ("raii.html", "RAII — Automatic Resource Management",
     "C++'s equivalent of Python's 'with' statement — but automatic for ALL objects.",
     "p1-raii", P1_RAII_CONTENT),
    ("vector-vs-deque.html", "std::vector vs std::deque",
     "The two main sequence containers — when to use each, and std::move optimization.",
     "p1-vd", P1_VEC_CONTENT),
    ("regex.html", "std::regex in C++",
     "Regular expressions in C++ — used to detect function signatures and #include lines.",
     "p1-rx", P1_REGEX_CONTENT),
    ("templates.html", "Templates — Generic Programming",
     "Write code that works for any type — the C++ answer to Python's duck typing.",
     "p1-tpl", P1_TEMPLATES_CONTENT),
    ("json-output.html", "Building JSON Manually",
     "How the project builds JSON with ostringstream and no external libraries.",
     "p1-js", P1_JSON_CONTENT),
]

for (fname, title, subtitle, active, content) in p1_pages:
    write(f"{BASE}/phase1/{fname}", make_page(
        title, subtitle, "Phase 1", "#4338ca",
        [("Home", "index.html"), ("Phase 1", "phase1/index.html"), (title, "")],
        content, active, True
    ))

# phase2/index.html
write(f"{BASE}/phase2/index.html", make_page(
    "Phase 2 — Architecture",
    "The 3-layer design, why a JSON bridge, the complete data flow, and the comment stripping challenge.",
    "Phase 2", "#be185d",
    [("Home", "index.html"), ("Phase 2", "")],
    P2_INDEX_CONTENT, "p2", True
))

# phase3/index.html
write(f"{BASE}/phase3/index.html", make_page(
    "Phase 3 — File-by-File Walkthrough",
    "Every source file explained: what it does, how it works, and key code excerpts annotated.",
    "Phase 3", "#0f766e",
    [("Home", "index.html"), ("Phase 3", "")],
    P3_INDEX_CONTENT, "p3", True
))

# phase3 sub-pages
p3_pages = [
    ("comment-stripper.html", "comment_stripper.cpp",
     "The 4-state machine that strips comments and string literals while preserving line numbers.",
     "p3-cs", P3_CS_CONTENT),
    ("metrics-calculator.html", "metrics_calculator.cpp",
     "Function extraction, cyclomatic complexity calculation, and risk classification.",
     "p3-mc", P3_MC_CONTENT),
    ("dependency-graph.html", "dependency_graph.cpp",
     "Building the include graph with unordered_map and detecting cycles with DFS.",
     "p3-dg", P3_DG_CONTENT),
    ("json-exporter.html", "json_exporter.cpp",
     "Manual JSON construction with ostringstream — no external libraries required.",
     "p3-je", P3_JE_CONTENT),
    ("main-cpp.html", "main.cpp",
     "The CLI orchestrator — argument parsing, pipeline assembly, terminal output.",
     "p3-m", P3_MAIN_CONTENT),
    ("graph-builder-py.html", "graph_builder.py",
     "Python transformer: converts C++ JSON output into D3.js-ready nodes and edges.",
     "p3-gb", P3_GB_CONTENT),
    ("html-generator-py.html", "html_generator.py",
     "The final step: assembling a single self-contained HTML report from all data.",
     "p3-hg", P3_HG_CONTENT),
    ("viz-js.html", "D3.js Visualization",
     "Force-directed graph physics, node rendering, click interactions, and the tick loop.",
     "p3-vz", P3_VIZ_CONTENT),
]

for (fname, title, subtitle, active, content) in p3_pages:
    write(f"{BASE}/phase3/{fname}", make_page(
        title, subtitle, "Phase 3", "#0f766e",
        [("Home", "index.html"), ("Phase 3", "phase3/index.html"), (title, "")],
        content, active, True
    ))

# phase4/index.html
write(f"{BASE}/phase4/index.html", make_page(
    "Phase 4 — Algorithms Deep Dive",
    "The four key algorithms powering this project — explained clearly with code.",
    "Phase 4", "#c2410c",
    [("Home", "index.html"), ("Phase 4", "")],
    P4_INDEX_CONTENT, "p4", True
))

# phase4 sub-pages
p4_pages = [
    ("cyclomatic-complexity.html", "Cyclomatic Complexity Calculation",
     "The math behind CC scores — 1 + decision points — with worked examples from the project.",
     "p4-cc", P4_CC_CONTENT),
    ("state-machine.html", "Comment Stripping State Machine",
     "Why regex fails and how the 4-state machine solves all C++ comment edge cases correctly.",
     "p4-sm", P4_SM_CONTENT),
    ("graph-traversal.html", "DFS for Circular Dependency Detection",
     "Depth-first search with visited + inStack sets — detecting cycles in O(V+E).",
     "p4-gt", P4_GT_CONTENT),
    ("d3-simulation.html", "D3.js Force Simulation Explained",
     "The physics forces, the animation loop, drag interaction, and why nodes are sized by complexity.",
     "p4-d3", P4_D3_CONTENT),
]

for (fname, title, subtitle, active, content) in p4_pages:
    write(f"{BASE}/phase4/{fname}", make_page(
        title, subtitle, "Phase 4", "#c2410c",
        [("Home", "index.html"), ("Phase 4", "phase4/index.html"), (title, "")],
        content, active, True
    ))

# phase5/index.html
write(f"{BASE}/phase5/index.html", make_page(
    "Phase 5 — Interview Q&A",
    "Confident, specific answers to every question an interviewer could ask about this project.",
    "Phase 5", "#6d28d9",
    [("Home", "index.html"), ("Interview Q&A", "")],
    P5_CONTENT, "p5", True
))

print(f"\n✅ Done! Generated all pages in {BASE}/")