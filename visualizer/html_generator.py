"""
html_generator.py
~~~~~~~~~~~~~~~~~
Assembles a self-contained, single-file HTML report from output.json.
Embeds D3.js v7, all CSS, and the graph data inline — no internet required
after generation.

Usage:
    python visualizer/html_generator.py output/output.json
    python visualizer/html_generator.py output/output.json --out report.html
"""

from __future__ import annotations

import json
import sys
import webbrowser
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Import our sibling module (handles path resolution gracefully)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))

from graph_builder import build_graph_data, load_json  # noqa: E402


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
def _html_template(graph_data: dict[str, Any]) -> str:
    """Return the complete, self-contained HTML as a string."""

    graph_json = json.dumps(graph_data, separators=(",", ":"))
    project    = graph_data.get("project", "Unknown Project")
    summary    = graph_data.get("summary", {})

    total_files   = summary.get("total_files",     0)
    total_funcs   = summary.get("total_functions", 0)
    avg_cc        = summary.get("avg_complexity",  0)
    max_cc        = summary.get("max_complexity",  0)
    high_count    = summary.get("high_risk_count", 0)
    med_count     = summary.get("medium_risk_count", 0)
    low_count     = summary.get("low_risk_count",  0)
    riskiest_file = summary.get("riskiest_file",   "—")
    riskiest_func = summary.get("riskiest_function","—")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>C++ Complexity Visualizer — {project}</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet"/>
<style>
/* ═══════════════════════════════════════════════════════════════
   DESIGN SYSTEM — dark terminal aesthetic, neon accents
   ═══════════════════════════════════════════════════════════════ */
:root{{
  --bg:          #0a0e17;
  --bg2:         #111827;
  --bg3:         #1a2235;
  --border:      #1e2d45;
  --border2:     #263550;
  --text:        #e2e8f0;
  --text-muted:  #64748b;
  --text-dim:    #94a3b8;
  --accent:      #38bdf8;
  --accent2:     #818cf8;
  --high:        #ef4444;
  --medium:      #f59e0b;
  --low:         #22c55e;
  --font-mono:   'JetBrains Mono', monospace;
  --font-display:'Syne', sans-serif;
  --radius:      8px;
  --shadow:      0 4px 24px rgba(0,0,0,0.4);
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-mono);
  min-height: 100vh;
  overflow-x: hidden;
}}

/* ── HEADER ─────────────────────────────────────────────────── */
header {{
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  padding: 18px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}}
.header-logo {{
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.02em;
  white-space: nowrap;
}}
.header-logo span {{ color: var(--text-muted); font-weight: 400; }}
.header-meta {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}}
.badge {{
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: 20px;
  border: 1px solid var(--border2);
  background: var(--bg3);
  color: var(--text-dim);
  white-space: nowrap;
}}
.badge.high   {{ border-color: var(--high);   color: var(--high);   background: rgba(239,68,68,.08); }}
.badge.medium {{ border-color: var(--medium); color: var(--medium); background: rgba(245,158,11,.08); }}
.badge.low    {{ border-color: var(--low);    color: var(--low);    background: rgba(34,197,94,.08); }}

/* ── LAYOUT ─────────────────────────────────────────────────── */
.layout {{
  display: grid;
  grid-template-columns: 1fr 340px;
  height: calc(100vh - 65px);
  overflow: hidden;
}}

/* ── GRAPH PANEL ────────────────────────────────────────────── */
#graph-panel {{
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(ellipse at 20% 80%, rgba(56,189,248,0.04) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(129,140,248,0.04) 0%, transparent 50%),
    var(--bg);
}}
#graph-svg {{
  width: 100%;
  height: 100%;
  cursor: grab;
}}
#graph-svg:active {{ cursor: grabbing; }}

.graph-hint {{
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.65rem;
  color: var(--text-muted);
  pointer-events: none;
  letter-spacing: 0.05em;
}}

/* Legend */
.legend {{
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(17,24,39,0.9);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  backdrop-filter: blur(8px);
}}
.legend-item {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.68rem;
  color: var(--text-dim);
}}
.legend-dot {{
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}}

/* ── SIDEBAR ────────────────────────────────────────────────── */
#sidebar {{
  background: var(--bg2);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

/* ── HERO STATS ─────────────────────────────────────────────── */
.hero-stats {{
  padding: 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg3);
}}
.hero-title {{
  font-family: var(--font-display);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 14px;
}}
.stats-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-bottom: 14px;
}}
.stat-card {{
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 8px;
  text-align: center;
  transition: border-color 0.2s;
}}
.stat-card:hover {{ border-color: var(--border2); }}
.stat-value {{
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
}}
.stat-label {{
  font-size: 0.58rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 3px;
}}

.risk-bars {{
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 14px;
}}
.risk-row {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.65rem;
}}
.risk-label {{
  width: 42px;
  color: var(--text-muted);
  flex-shrink: 0;
}}
.risk-bar-track {{
  flex: 1;
  height: 5px;
  background: var(--bg);
  border-radius: 3px;
  overflow: hidden;
}}
.risk-bar-fill {{
  height: 100%;
  border-radius: 3px;
  transition: width 1s ease;
}}
.risk-count {{
  width: 20px;
  text-align: right;
  color: var(--text-dim);
}}

.riskiest-box {{
  background: rgba(239,68,68,0.08);
  border: 1px solid rgba(239,68,68,0.25);
  border-radius: var(--radius);
  padding: 10px 12px;
}}
.riskiest-label {{
  font-size: 0.6rem;
  color: var(--high);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 4px;
}}
.riskiest-func {{
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
}}
.riskiest-file {{
  font-size: 0.65rem;
  color: var(--text-muted);
  margin-top: 2px;
}}

/* ── NODE DETAIL PANEL ──────────────────────────────────────── */
#detail-panel {{
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  min-height: 120px;
  background: var(--bg2);
}}
.detail-empty {{
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80px;
  color: var(--text-muted);
  font-size: 0.7rem;
  letter-spacing: 0.05em;
}}
.detail-header {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}}
.detail-filename {{
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  word-break: break-all;
}}
.detail-risk-badge {{
  font-size: 0.6rem;
  padding: 2px 7px;
  border-radius: 20px;
  font-weight: 600;
  flex-shrink: 0;
  margin-left: 8px;
  margin-top: 3px;
}}
.detail-stats {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  margin-bottom: 10px;
}}
.detail-stat {{
  background: var(--bg3);
  border-radius: 5px;
  padding: 6px 8px;
}}
.detail-stat-label {{
  font-size: 0.58rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.07em;
}}
.detail-stat-value {{
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
}}
.detail-funcs-title {{
  font-size: 0.6rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 6px;
}}
.detail-func-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.68rem;
}}
.detail-func-row:last-child {{ border-bottom: none; }}
.detail-func-name {{ color: var(--text); word-break: break-all; }}
.detail-func-cc {{
  font-size: 0.62rem;
  padding: 1px 5px;
  border-radius: 3px;
  flex-shrink: 0;
  margin-left: 4px;
}}

/* ── FUNCTION LIST ──────────────────────────────────────────── */
.func-list-section {{
  flex: 1;
  overflow-y: auto;
  padding: 0;
}}
.func-list-section::-webkit-scrollbar {{ width: 4px; }}
.func-list-section::-webkit-scrollbar-track {{ background: transparent; }}
.func-list-section::-webkit-scrollbar-thumb {{ background: var(--border2); border-radius: 2px; }}

.func-list-header {{
  padding: 12px 20px 8px;
  font-size: 0.6rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  position: sticky;
  top: 0;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  z-index: 10;
}}
.file-group {{ border-bottom: 1px solid var(--border); }}
.file-group-header {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  cursor: pointer;
  background: var(--bg3);
  user-select: none;
  transition: background 0.15s;
}}
.file-group-header:hover {{ background: var(--bg); }}
.file-group-dot {{
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}}
.file-group-name {{
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.file-group-count {{
  font-size: 0.6rem;
  color: var(--text-muted);
}}
.file-group-chevron {{
  font-size: 0.6rem;
  color: var(--text-muted);
  transition: transform 0.2s;
}}
.file-group-chevron.open {{ transform: rotate(90deg); }}
.file-group-funcs {{ display: none; }}
.file-group-funcs.open {{ display: block; }}
.func-item {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 20px 5px 36px;
  font-size: 0.68rem;
  cursor: pointer;
  transition: background 0.1s;
  border-bottom: 1px solid rgba(30,45,69,0.5);
}}
.func-item:hover {{ background: var(--bg3); }}
.func-item-name {{
  flex: 1;
  color: var(--text-dim);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.func-item-cc {{
  font-size: 0.6rem;
  padding: 1px 5px;
  border-radius: 3px;
  flex-shrink: 0;
}}

/* ── D3 NODE STYLES ─────────────────────────────────────────── */
.node-circle {{
  stroke-width: 2;
  transition: filter 0.2s;
  cursor: pointer;
}}
.node-circle:hover {{ filter: brightness(1.3); }}
.node-label {{
  font-family: var(--font-mono);
  font-size: 10px;
  fill: #e2e8f0;
  pointer-events: none;
  text-anchor: middle;
}}
.link-line {{
  stroke: #263550;
  stroke-opacity: 0.6;
  stroke-width: 1.5;
  fill: none;
}}
.link-line.circular {{
  stroke: var(--high);
  stroke-opacity: 0.8;
  stroke-dasharray: 5 3;
}}

/* ── TOOLTIP ────────────────────────────────────────────────── */
#tooltip {{
  position: fixed;
  pointer-events: none;
  background: rgba(17,24,39,0.95);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  padding: 10px 14px;
  font-size: 0.7rem;
  max-width: 220px;
  backdrop-filter: blur(8px);
  box-shadow: var(--shadow);
  z-index: 200;
  opacity: 0;
  transition: opacity 0.15s;
}}
#tooltip.visible {{ opacity: 1; }}

/* ── CIRCULAR DEPS BANNER ───────────────────────────────────── */
.circular-banner {{
  margin: 10px 20px;
  background: rgba(239,68,68,0.08);
  border: 1px solid rgba(239,68,68,0.3);
  border-radius: var(--radius);
  padding: 8px 12px;
  font-size: 0.65rem;
  color: var(--high);
}}
.circular-banner-title {{
  font-weight: 600;
  margin-bottom: 4px;
}}
.circular-banner-item {{
  color: var(--text-dim);
  font-size: 0.62rem;
  padding: 1px 0;
}}

/* ── ANIMATIONS ─────────────────────────────────────────────── */
@keyframes pulse-ring {{
  0%   {{ r: 0; opacity: 0.6; }}
  100% {{ r: 60px; opacity: 0; }}
}}
.pulse-ring {{
  fill: none;
  stroke: var(--high);
  stroke-width: 1;
  animation: pulse-ring 2s ease-out infinite;
}}
</style>
</head>
<body>

<!-- ── HEADER ──────────────────────────────────────────────────── -->
<header>
  <div class="header-logo">🔍 Complexity Visualizer <span>/ {project}</span></div>
  <div class="header-meta">
    <span class="badge">{total_files} files</span>
    <span class="badge">{total_funcs} functions</span>
    <span class="badge">avg CC {avg_cc}</span>
    <span class="badge high">🔴 {high_count} high</span>
    <span class="badge medium">🟡 {med_count} medium</span>
    <span class="badge low">🟢 {low_count} low</span>
  </div>
</header>

<!-- ── LAYOUT ──────────────────────────────────────────────────── -->
<div class="layout">

  <!-- Graph panel -->
  <div id="graph-panel">
    <svg id="graph-svg"></svg>

    <!-- Legend -->
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>High Risk (CC ≥ 11)</div>
      <div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div>Medium Risk (CC 6–10)</div>
      <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>Low Risk (CC 1–5)</div>
      <div class="legend-item" style="margin-top:4px;font-size:0.62rem;color:#475569">Node size ∝ complexity score</div>
    </div>

    <div class="graph-hint">Scroll to zoom · Drag to pan · Click node for details</div>
  </div>

  <!-- Sidebar -->
  <div id="sidebar">

    <!-- Hero stats -->
    <div class="hero-stats">
      <div class="hero-title">📊 Project Overview</div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent)">{avg_cc}</div>
          <div class="stat-label">avg CC</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent2)">{total_funcs}</div>
          <div class="stat-label">functions</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--high)">{max_cc}</div>
          <div class="stat-label">max CC</div>
        </div>
      </div>

      <div class="risk-bars" id="risk-bars">
        <!-- injected by JS -->
      </div>

      <div class="riskiest-box">
        <div class="riskiest-label">🔴 Riskiest Function</div>
        <div class="riskiest-func">{riskiest_func}()</div>
        <div class="riskiest-file">{riskiest_file}</div>
      </div>
    </div>

    <!-- Node detail panel -->
    <div id="detail-panel">
      <div class="detail-empty">← Click a node to inspect</div>
    </div>

    <!-- Function list -->
    <div class="func-list-section">
      <div class="func-list-header">📋 All Functions</div>
      <div id="func-list"><!-- injected by JS --></div>
    </div>

  </div><!-- /sidebar -->
</div><!-- /layout -->

<!-- Tooltip -->
<div id="tooltip"></div>

<!-- ── D3 v7 ──────────────────────────────────────────────────── -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>

<script>
// ═══════════════════════════════════════════════════════════════
// DATA
// ═══════════════════════════════════════════════════════════════
const GRAPH_DATA = {graph_json};

const nodes = GRAPH_DATA.nodes.map(d => ({{...d}}));
const links = GRAPH_DATA.edges.map(d => ({{...d}}));
const circularSet = new Set(
  (GRAPH_DATA.circular || []).flatMap(c => c.split(" -> "))
);

// ═══════════════════════════════════════════════════════════════
// RISK BARS
// ═══════════════════════════════════════════════════════════════
(function buildRiskBars() {{
  const s = GRAPH_DATA.summary;
  const total = (s.high_risk_count||0) + (s.medium_risk_count||0) + (s.low_risk_count||0);
  const bars = [
    {{ label:"High",   count: s.high_risk_count||0,   color:"var(--high)"   }},
    {{ label:"Medium", count: s.medium_risk_count||0, color:"var(--medium)" }},
    {{ label:"Low",    count: s.low_risk_count||0,    color:"var(--low)"    }},
  ];
  const container = document.getElementById("risk-bars");
  bars.forEach(b => {{
    const pct = total > 0 ? (b.count / total * 100).toFixed(0) : 0;
    container.innerHTML += `
      <div class="risk-row">
        <span class="risk-label" style="color:${{b.color}}">${{b.label}}</span>
        <div class="risk-bar-track">
          <div class="risk-bar-fill" style="width:0%;background:${{b.color}}"
               data-pct="${{pct}}%"></div>
        </div>
        <span class="risk-count" style="color:${{b.color}}">${{b.count}}</span>
      </div>`;
  }});
  // Animate bars after paint
  setTimeout(() => {{
    document.querySelectorAll(".risk-bar-fill[data-pct]").forEach(el => {{
      el.style.width = el.dataset.pct;
    }});
  }}, 200);
}})();

// ═══════════════════════════════════════════════════════════════
// FUNCTION LIST
// ═══════════════════════════════════════════════════════════════
function riskColor(r) {{
  return r === "high" ? "var(--high)" : r === "medium" ? "var(--medium)" : "var(--low)";
}}
function riskBg(r) {{
  return r === "high"   ? "rgba(239,68,68,.15)"
       : r === "medium" ? "rgba(245,158,11,.15)"
       :                  "rgba(34,197,94,.15)";
}}

(function buildFuncList() {{
  const container = document.getElementById("func-list");
  // Circular deps banner
  if (GRAPH_DATA.circular && GRAPH_DATA.circular.length) {{
    const div = document.createElement("div");
    div.className = "circular-banner";
    div.innerHTML = `<div class="circular-banner-title">⚠ Circular Dependencies Detected</div>`
      + GRAPH_DATA.circular.map(c => `<div class="circular-banner-item">• ${{c}}</div>`).join("");
    container.appendChild(div);
  }}

  nodes.forEach(node => {{
    const group = document.createElement("div");
    group.className = "file-group";
    group.dataset.nodeId = node.id;

    const header = document.createElement("div");
    header.className = "file-group-header";
    header.innerHTML = `
      <div class="file-group-dot" style="background:${{node.color}}"></div>
      <div class="file-group-name" title="${{node.id}}">${{node.name}}</div>
      <span class="file-group-count">${{node.function_count}} fn</span>
      <span class="file-group-chevron">▶</span>`;

    const funcsDiv = document.createElement("div");
    funcsDiv.className = "file-group-funcs";
    (node.functions || []).forEach(fn => {{
      const row = document.createElement("div");
      row.className = "func-item";
      row.innerHTML = `
        <span class="func-item-name" title="${{fn.name}}">${{fn.name}}()</span>
        <span class="func-item-cc" style="background:${{riskBg(fn.risk)}};color:${{riskColor(fn.risk)}}">
          CC ${{fn.complexity}}
        </span>`;
      row.addEventListener("click", () => focusNode(node.id));
      funcsDiv.appendChild(row);
    }});

    header.addEventListener("click", () => {{
      const chevron = header.querySelector(".file-group-chevron");
      const isOpen  = funcsDiv.classList.toggle("open");
      chevron.classList.toggle("open", isOpen);
      focusNode(node.id);
    }});

    group.appendChild(header);
    group.appendChild(funcsDiv);
    container.appendChild(group);
  }});
}})();

// ═══════════════════════════════════════════════════════════════
// DETAIL PANEL
// ═══════════════════════════════════════════════════════════════
function showDetail(node) {{
  const panel = document.getElementById("detail-panel");
  const allFuncs = (node.functions || [])
    .sort((a, b) => b.complexity - a.complexity);

  const funcsHtml = allFuncs.slice(0, 6).map(fn => `
    <div class="detail-func-row">
      <span class="detail-func-name">${{fn.name}}()</span>
      <span class="detail-func-cc"
            style="background:${{riskBg(fn.risk)}};color:${{riskColor(fn.risk)}}">
        CC ${{fn.complexity}}
      </span>
    </div>`).join("");

  const riskBadgeStyle = `background:${{riskBg(node.risk)}};color:${{riskColor(node.risk)}}`;
  const circularWarn = circularSet.has(node.id)
    ? `<div style="margin-top:8px;font-size:0.62rem;color:var(--high)">⚠ Involved in circular dependency</div>` : "";

  panel.innerHTML = `
    <div class="detail-header">
      <div class="detail-filename">${{node.name}}</div>
      <span class="detail-risk-badge" style="${{riskBadgeStyle}}">${{node.risk.toUpperCase()}}</span>
    </div>
    <div class="detail-stats">
      <div class="detail-stat">
        <div class="detail-stat-label">Total Lines</div>
        <div class="detail-stat-value">${{node.total_lines}}</div>
      </div>
      <div class="detail-stat">
        <div class="detail-stat-label">Code Lines</div>
        <div class="detail-stat-value">${{node.code_lines}}</div>
      </div>
      <div class="detail-stat">
        <div class="detail-stat-label">Functions</div>
        <div class="detail-stat-value">${{node.function_count}}</div>
      </div>
      <div class="detail-stat">
        <div class="detail-stat-label">Complexity</div>
        <div class="detail-stat-value" style="color:${{riskColor(node.risk)}}">${{node.complexity}}</div>
      </div>
    </div>
    ${{funcsHtml ? `<div class="detail-funcs-title">Top Functions by Complexity</div>${{funcsHtml}}` : ""}}
    ${{circularWarn}}`;
}}

// ═══════════════════════════════════════════════════════════════
// D3 FORCE GRAPH
// ═══════════════════════════════════════════════════════════════
const svgEl   = document.getElementById("graph-svg");
const W       = svgEl.clientWidth  || 800;
const H       = svgEl.clientHeight || 600;

const svg = d3.select("#graph-svg");

// Arrow marker for directed edges
svg.append("defs").append("marker")
  .attr("id", "arrow")
  .attr("viewBox", "0 -5 10 10")
  .attr("refX", 18)
  .attr("refY", 0)
  .attr("markerWidth", 6)
  .attr("markerHeight", 6)
  .attr("orient", "auto")
  .append("path")
  .attr("d", "M0,-5L10,0L0,5")
  .attr("fill", "#263550");

// Zoomable container
const container = svg.append("g").attr("class", "zoom-container");

svg.call(
  d3.zoom()
    .scaleExtent([0.2, 4])
    .on("zoom", e => container.attr("transform", e.transform))
);

// Simulation
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links)
    .id(d => d.id)
    .distance(120)
    .strength(0.4))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(W / 2, H / 2))
  .force("collision", d3.forceCollide().radius(d => d.radius + 8));

// Links
const link = container.append("g")
  .selectAll("line")
  .data(links)
  .enter().append("line")
  .attr("class", d => "link-line" + (circularSet.has(d.source.id || d.source) && circularSet.has(d.target.id || d.target) ? " circular" : ""))
  .attr("marker-end", "url(#arrow)");

// Node groups
const node = container.append("g")
  .selectAll("g")
  .data(nodes)
  .enter().append("g")
  .attr("class", "node-group")
  .call(
    d3.drag()
      .on("start", (e, d) => {{ if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }})
      .on("drag",  (e, d) => {{ d.fx = e.x; d.fy = e.y; }})
      .on("end",   (e, d) => {{ if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }})
  );

// Pulse ring for high-risk nodes
node.filter(d => d.risk === "high")
  .append("circle")
  .attr("class", "pulse-ring")
  .attr("r", d => d.radius);

// Main circle
node.append("circle")
  .attr("class", "node-circle")
  .attr("r", d => d.radius)
  .attr("fill", d => d.color)
  .attr("fill-opacity", 0.85)
  .attr("stroke", d => d.color)
  .attr("stroke-opacity", 0.5)
  .on("click", (e, d) => {{ e.stopPropagation(); focusNode(d.id); showDetail(d); }})
  .on("mouseover", (e, d) => showTooltip(e, d))
  .on("mousemove", moveTooltip)
  .on("mouseout", hideTooltip);

// Labels
node.append("text")
  .attr("class", "node-label")
  .attr("dy", d => d.radius + 14)
  .text(d => d.name.length > 18 ? d.name.slice(0, 16) + "…" : d.name);

// Tick
simulation.on("tick", () => {{
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);

  node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
}});

// ── Tooltip ─────────────────────────────────────────────────────
const tooltip = document.getElementById("tooltip");
function showTooltip(e, d) {{
  tooltip.innerHTML = `
    <div style="font-weight:600;margin-bottom:4px;color:${{d.color}}">${{d.name}}</div>
    <div>Complexity: <b>${{d.complexity}}</b></div>
    <div>Functions: <b>${{d.function_count}}</b></div>
    <div>Lines: <b>${{d.total_lines}}</b></div>
    <div style="margin-top:4px;font-size:0.62rem;color:var(--text-muted)">${{d.label}}</div>`;
  tooltip.classList.add("visible");
  moveTooltip(e);
}}
function moveTooltip(e) {{
  const x = e.clientX + 14;
  const y = e.clientY - 10;
  tooltip.style.left = Math.min(x, window.innerWidth - 240) + "px";
  tooltip.style.top  = y + "px";
}}
function hideTooltip() {{ tooltip.classList.remove("visible"); }}

// ── Focus node ──────────────────────────────────────────────────
let selectedId = null;
function focusNode(id) {{
  selectedId = id;

  // Highlight in graph
  d3.selectAll(".node-circle")
    .attr("stroke-opacity", d => d.id === id ? 1.0 : 0.3)
    .attr("fill-opacity",   d => d.id === id ? 1.0 : 0.4)
    .attr("stroke-width",   d => d.id === id ? 3   : 1.5);

  // Highlight in sidebar list
  document.querySelectorAll(".file-group").forEach(el => {{
    el.style.opacity = el.dataset.nodeId === id ? "1" : "0.5";
  }});

  // Show detail
  const nodeData = nodes.find(n => n.id === id);
  if (nodeData) showDetail(nodeData);
}}

// Click background to deselect
svg.on("click", () => {{
  selectedId = null;
  d3.selectAll(".node-circle")
    .attr("stroke-opacity", 0.5)
    .attr("fill-opacity",   0.85)
    .attr("stroke-width",   2);
  document.querySelectorAll(".file-group").forEach(el => el.style.opacity = "1");
  document.getElementById("detail-panel").innerHTML =
    `<div class="detail-empty">← Click a node to inspect</div>`;
}});

// ── Auto-fit after layout stabilizes ────────────────────────────
simulation.on("end", () => {{
  const bounds = container.node().getBBox();
  if (!bounds.width) return;
  const scaleX = W / (bounds.width  + 80);
  const scaleY = H / (bounds.height + 80);
  const scale  = Math.min(scaleX, scaleY, 1);
  const tx = (W - scale * (bounds.x * 2 + bounds.width))  / 2;
  const ty = (H - scale * (bounds.y * 2 + bounds.height)) / 2;
  svg.transition().duration(800)
     .call(d3.zoom().transform,
           d3.zoomIdentity.translate(tx, ty).scale(scale));
}});
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# generate
# ---------------------------------------------------------------------------
def generate(json_path: str, output_path: str = "report.html") -> None:
    """
    Main entry point.

    1. Reads output.json
    2. Builds graph data
    3. Renders HTML
    4. Writes report.html
    5. Opens browser
    """
    print(f"[html_generator] Reading: {json_path}")
    raw        = load_json(json_path)
    graph_data = build_graph_data(raw)
    html       = _html_template(graph_data)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[html_generator] Report written: {out.resolve()}")
    except OSError as exc:
        print(f"[html_generator] ERROR: Cannot write {output_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[html_generator] Opening browser...")
    webbrowser.open(out.resolve().as_uri())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_args() -> tuple[str, str]:
    """Minimal arg parser (no argparse dependency)."""
    args       = sys.argv[1:]
    json_path  = None
    out_path   = "report.html"

    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        elif not args[i].startswith("--"):
            json_path = args[i]
            i += 1
        else:
            print(f"Unknown argument: {args[i]}", file=sys.stderr)
            i += 1

    if not json_path:
        print("Usage: python html_generator.py <output.json> [--out report.html]")
        sys.exit(1)

    return json_path, out_path


if __name__ == "__main__":
    jp, op = _parse_args()
    generate(jp, op)
