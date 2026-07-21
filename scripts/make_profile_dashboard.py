import os
import base64
from xml.sax.saxutils import escape

# Paths
scripts_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(scripts_dir)
photo_path = os.path.join(scripts_dir, "photo.jpg")
ascii_path = os.path.join(scripts_dir, "ascii.txt")
output_path = os.path.join(root_dir, "profile-dashboard.svg")

# Encode Photo to Base64
if os.path.exists(photo_path):
    with open(photo_path, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode("utf-8")
else:
    photo_b64 = ""

# Read ASCII text
if os.path.exists(ascii_path):
    with open(ascii_path, "r", encoding="utf-8") as f:
        ascii_lines = [line.rstrip("\n") for line in f.readlines()]
else:
    ascii_lines = ["(ASCII Portrait)"]

# Crop/scale ASCII portrait lines
ascii_lines = [line[:80].ljust(80) for line in ascii_lines[:45]]

# Generate SMIL animations for ASCII rows
char_width = 3.125
line_height = 4.5
font_size = 5.2

clips = []
texts = []
cursors = []
total_rows = len(ascii_lines)
duration = 3.0
row_dur = duration / total_rows

for i, row in enumerate(ascii_lines):
    begin_time = round(i * row_dur, 4)
    y = 52 + i * line_height
    width = len(row) * char_width

    clips.append(f"""  <clipPath id="aclip{i}">
    <rect x="15" y="{y - line_height + 1.0}" width="0" height="{line_height}">
        <animate attributeName="width" from="0" to="{width}" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
    </rect>
  </clipPath>""")

    safe_row = escape(row)
    texts.append(f"""  <text x="15" y="{y}" clip-path="url(#aclip{i})" font-family="Consolas, monospace" font-size="{font_size}" xml:space="preserve" fill="#ff9ecd" opacity="0.85">{safe_row}</text>""")

    cursors.append(f"""  <rect x="15" y="{y - line_height + 1.0}" width="4" height="{line_height}" fill="#ff9ecd" opacity="0">
    <animate attributeName="x" from="15" to="{15 + width}" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.99;1" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
  </rect>""")

last_y = 52 + (total_rows - 1) * line_height
last_width = len(ascii_lines[-1]) * char_width
cursors.append(f"""  <rect x="{15 + last_width}" y="{last_y - line_height + 1.0}" width="4" height="{line_height}" fill="#ff9ecd" opacity="0">
    <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" begin="{duration}s" dur="0.8s" repeatCount="indefinite" />
  </rect>""")

clips_str = "\n".join(clips)
texts_str = "\n".join(texts)
cursor_str = "\n".join(cursors)

# Info items
INFO = [
    ("User",     "Tasmiya A"),
    ("Role",     "AI Engineer | Full-Stack"),
    ("Stack",    "Python, React, TS"),
    ("AI",       "LLMs, LangGraph, CV"),
    ("Infra",    "Docker, PostgreSQL"),
    ("Location", "India"),
]

specs_str = ""
y_spec = 70
for i, (key, value) in enumerate(INFO):
    delay = 1.0 + i * 0.15
    specs_str += f"""
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.4s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" begin="{delay}s" dur="0.4s" fill="freeze"/>
    <text x="20" y="{y_spec}" font-family="Consolas, monospace" font-size="12" font-weight="bold" fill="#ff9ecd">{key}:</text>
    <text x="90" y="{y_spec}" font-family="Consolas, monospace" font-size="12" fill="#f0d6ff">{value}</text>
  </g>"""
    y_spec += 25

# Integrated inline badges under specs (fixing alignment issues)
badges_str = f"""
  <g opacity="0" transform="translate(20, {y_spec + 10})">
    <animate attributeName="opacity" from="0" to="1" begin="2.0s" dur="0.5s" fill="freeze"/>
    
    <!-- Badge 1: LangGraph -->
    <rect x="0" y="0" width="75" height="22" rx="11" fill="#1a0f2e" stroke="#ff9ecd" stroke-width="1"/>
    <circle cx="11" cy="11" r="3.5" fill="#ff9ecd">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="40" y="15" font-family="Outfit, sans-serif" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">LangGraph</text>

    <!-- Badge 2: RAG -->
    <rect x="85" y="0" width="55" height="22" rx="11" fill="#1a0f2e" stroke="#c084fc" stroke-width="1"/>
    <circle cx="96" cy="11" r="3.5" fill="#c084fc">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <text x="120" y="15" font-family="Outfit, sans-serif" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">RAG</text>

    <!-- Badge 3: Docker -->
    <rect x="150" y="0" width="65" height="22" rx="11" fill="#1a0f2e" stroke="#67e8f9" stroke-width="1"/>
    <circle cx="161" cy="11" r="3.5" fill="#67e8f9">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="187" y="15" font-family="Outfit, sans-serif" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">Docker</text>
    
    <!-- Badge 4: K8s -->
    <rect x="225" y="0" width="55" height="22" rx="11" fill="#1a0f2e" stroke="#ffaa00" stroke-width="1"/>
    <circle cx="236" cy="11" r="3.5" fill="#ffaa00">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <text x="258" y="15" font-family="Outfit, sans-serif" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">K8s</text>
  </g>
"""

# New Unique Left-Column Skill Modules (Progress bars)
skills_markup = """
  <g transform="translate(25, 520)">
    <rect width="250" height="330" rx="12" fill="#0d0414" stroke="#4a1a36" stroke-width="1.5"/>
    <text x="15" y="27" font-family="Outfit, sans-serif" font-size="14" font-weight="bold" fill="#ff9ecd" style="filter: drop-shadow(0px 0px 3px #ff9ecd);">[ System Analytics ]</text>
    <line x1="15" y1="36" x2="235" y2="36" stroke="#4a1a36" stroke-width="1"/>

    <!-- Progress 1 -->
    <g transform="translate(15, 60)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="11" fill="#ffd6ee">AI &amp; Multi-Agent Systems</text>
      <text x="215" y="0" font-family="Consolas, monospace" font-size="11" fill="#ff9ecd" text-anchor="end">95%</text>
      <rect x="0" y="8" width="215" height="6" rx="3" fill="#1a0a18"/>
      <rect x="0" y="8" width="204" height="6" rx="3" fill="#ff4fa3"/>
      <circle cx="204" cy="11" r="2.5" fill="#ffffff"><animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite"/></circle>
    </g>

    <!-- Progress 2 -->
    <g transform="translate(15, 120)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="11" fill="#ffd6ee">RAG &amp; Vector DBs</text>
      <text x="215" y="0" font-family="Consolas, monospace" font-size="11" fill="#c084fc" text-anchor="end">90%</text>
      <rect x="0" y="8" width="215" height="6" rx="3" fill="#1a0a18"/>
      <rect x="0" y="8" width="193" height="6" rx="3" fill="#c084fc"/>
      <circle cx="193" cy="11" r="2.5" fill="#ffffff"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.2s" repeatCount="indefinite"/></circle>
    </g>

    <!-- Progress 3 -->
    <g transform="translate(15, 180)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="11" fill="#ffd6ee">Backend (Python, FastAPI)</text>
      <text x="215" y="0" font-family="Consolas, monospace" font-size="11" fill="#67e8f9" text-anchor="end">85%</text>
      <rect x="0" y="8" width="215" height="6" rx="3" fill="#1a0a18"/>
      <rect x="0" y="8" width="182" height="6" rx="3" fill="#67e8f9"/>
      <circle cx="182" cy="11" r="2.5" fill="#ffffff"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" repeatCount="indefinite"/></circle>
    </g>

    <!-- Progress 4 -->
    <g transform="translate(15, 240)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="11" fill="#ffd6ee">DevOps (Docker, K8s)</text>
      <text x="215" y="0" font-family="Consolas, monospace" font-size="11" fill="#ffaa00" text-anchor="end">80%</text>
      <rect x="0" y="8" width="215" height="6" rx="3" fill="#1a0a18"/>
      <rect x="0" y="8" width="172" height="6" rx="3" fill="#ffaa00"/>
      <circle cx="172" cy="11" r="2.5" fill="#ffffff"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.8s" repeatCount="indefinite"/></circle>
    </g>
  </g>
"""

# New Unique Horizontal Blueprint Nodes Layout
# Left to right flow instead of top to bottom
NODES = [
    ("root", "Repositories",               350, 565, 110, 30, "root"),
    
    ("p1",   "AI Platform",                550, 435, 110, 26, "child"),
    ("p2",   "RAG Platform",               550, 520, 110, 26, "child"),
    ("p3",   "NLP Chatbot",                550, 605, 110, 26, "child"),
    ("p4",   "Plant Disease",              550, 690, 110, 26, "child"),
    
    ("c1",   "Multi-Agent",                750, 410, 140, 24, "leaf"),
    ("c2",   "WebSocket",                  750, 460, 140, 24, "leaf"),
    
    ("c3",   "Hybrid Retrieval",           750, 500, 140, 24, "leaf"),
    ("c4",   "BM25 + BGE",                 750, 540, 140, 24, "leaf"),
    
    ("c5",   "Context State",              750, 606, 140, 24, "leaf"),
    
    ("c6",   "CNN Model",                  750, 691, 140, 24, "leaf"),
]

nodes_markup = ""
paths_markup = ""
pulses_markup = ""

# Draw paths for horizontal layout
# Root (x=460 right edge, y=580 center) to P1, P2, P3, P4 (left edge 550)
paths_markup += '<path d="M 460 580 L 500 580 L 500 448 L 550 448" fill="none" stroke="#ff4fa3" stroke-width="1.2" opacity="0.6"/>'
paths_markup += '<path d="M 460 580 L 500 580 L 500 533 L 550 533" fill="none" stroke="#ff4fa3" stroke-width="1.2" opacity="0.6"/>'
paths_markup += '<path d="M 460 580 L 500 580 L 500 618 L 550 618" fill="none" stroke="#ff4fa3" stroke-width="1.2" opacity="0.6"/>'
paths_markup += '<path d="M 460 580 L 500 580 L 500 703 L 550 703" fill="none" stroke="#ff4fa3" stroke-width="1.2" opacity="0.6"/>'

# P1 (right edge 660) to leaves (left edge 750)
paths_markup += '<path d="M 660 448 L 705 448 L 705 422 L 750 422" fill="none" stroke="#9d2060" stroke-width="1" stroke-dasharray="2 2"/>'
paths_markup += '<path d="M 660 448 L 705 448 L 705 472 L 750 472" fill="none" stroke="#9d2060" stroke-width="1" stroke-dasharray="2 2"/>'
# P2 to leaves
paths_markup += '<path d="M 660 533 L 705 533 L 705 512 L 750 512" fill="none" stroke="#9d2060" stroke-width="1" stroke-dasharray="2 2"/>'
paths_markup += '<path d="M 660 533 L 705 533 L 705 552 L 750 552" fill="none" stroke="#9d2060" stroke-width="1" stroke-dasharray="2 2"/>'
# P3 to leaves
paths_markup += '<path d="M 660 618 L 750 618" fill="none" stroke="#9d2060" stroke-width="1" stroke-dasharray="2 2"/>'
# P4 to leaves
paths_markup += '<path d="M 660 703 L 750 703" fill="none" stroke="#9d2060" stroke-width="1" stroke-dasharray="2 2"/>'

pulses_markup += """
<circle r="2.5" fill="#ffffff"><animateMotion path="M 460 580 L 500 580 L 500 448 L 550 448" dur="3s" repeatCount="indefinite"/></circle>
<circle r="2.5" fill="#ffffff"><animateMotion path="M 460 580 L 500 580 L 500 533 L 550 533" dur="2.5s" repeatCount="indefinite"/></circle>
<circle r="2.5" fill="#ffffff"><animateMotion path="M 460 580 L 500 580 L 500 618 L 550 618" dur="4s" repeatCount="indefinite"/></circle>
<circle r="2.5" fill="#ffffff"><animateMotion path="M 460 580 L 500 580 L 500 703 L 550 703" dur="3.5s" repeatCount="indefinite"/></circle>
"""

# Render node boxes
for n in NODES:
    nx, ny, nw, nh, nt = n[2], n[3], n[4], n[5], n[6]
    label = n[1]
    if nt == "root":
        stroke_col, b_fill, t_col, glow = "#ff9ecd", "#2a0d1e", "#ffffff", "drop-shadow(0px 0px 6px rgba(255,158,205,0.8))"
    elif nt == "child":
        stroke_col, b_fill, t_col, glow = "#ff4fa3", "#1a0a18", "#ffd6ee", "drop-shadow(0px 0px 4px rgba(255,79,163,0.4))"
    else:
        stroke_col, b_fill, t_col, glow = "#c084fc", "#10061c", "#eaddff", "none"
        
    nodes_markup += f"""
  <g transform="translate({nx}, {ny})">
    <rect width="{nw}" height="{nh}" rx="4" fill="{b_fill}" stroke="{stroke_col}" stroke-width="1" style="filter: {glow};" opacity="0.9"/>
    <text x="{nw//2}" y="{nh//2 + 3.5}" font-family="Outfit, Inter, sans-serif" font-size="10" font-weight="bold" fill="{t_col}" text-anchor="middle">{label}</text>
  </g>"""


grid_pattern = """
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1c0b29" stroke-width="1"/>
      <circle cx="40" cy="40" r="1" fill="#3a1854"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)" />
"""

# Avatar Hexagon Polygon
hex_points = "140,82 190,111 190,169 140,198 90,169 90,111"

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="950"
     height="900"
     viewBox="0 0 950 900"
     fill="none">
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&amp;display=swap');
    .glow-card {{
      filter: drop-shadow(0px 0px 15px rgba(192, 132, 252, 0.1));
    }}
    .circle-scan {{
      transform-origin: 140px 140px;
    }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="15" fill="#090311" stroke="#3d1a2e" stroke-width="2"/>
  {grid_pattern}

  <!-- ================= LEFT COLUMN ================= -->
  <g class="glow-card" transform="translate(15, 15)">
    <rect width="280" height="870" rx="16" fill="#10051a" fill-opacity="0.85" stroke="#4a1a36" stroke-width="1.5"/>

    <!-- Unique Hexagon Scanner rings -->
    <g class="circle-scan">
      <polygon points="140,70 200,105 200,175 140,210 80,175 80,105" fill="none" stroke="#ff9ecd" stroke-dasharray="10 10" stroke-width="1.5">
        <animateTransform attributeName="transform" type="rotate" from="0 140 140" to="360 140 140" dur="20s" repeatCount="indefinite"/>
      </polygon>
      <circle cx="140" cy="140" r="75" fill="none" stroke="#c084fc" stroke-dasharray="4 8" stroke-width="1">
        <animateTransform attributeName="transform" type="rotate" from="360 140 140" to="0 140 140" dur="24s" repeatCount="indefinite"/>
      </circle>
      <circle cx="140" cy="140" r="60" fill="none" stroke="#ff4fa3" stroke-width="1" stroke-opacity="0.4"/>
    </g>

    <!-- Avatar Image -->
    <defs>
      <clipPath id="avatar-clip">
        <polygon points="{hex_points}"/>
      </clipPath>
    </defs>
    {"" if not photo_b64 else f'<image href="data:image/jpeg;base64,{photo_b64}" x="80" y="80" width="120" height="120" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>'}

    <!-- Name & handle -->
    <text x="140" y="255" font-family="'Outfit', sans-serif" font-weight="800" font-size="24" fill="#ffffff" text-anchor="middle">Tasmiya A</text>
    <text x="140" y="280" font-family="Consolas, monospace" font-size="11.5" fill="#ff9ecd" text-anchor="middle">tasmiya-a25 • she/her</text>
    <line x1="30" y1="295" x2="250" y2="295" stroke="#4a1a36" stroke-width="1"/>

    <!-- Profile Classification -->
    <g transform="translate(20, 312)" font-family="'Outfit', sans-serif" font-size="11" fill="#ffd6ee">
      <rect width="240" height="165" rx="8" fill="#0d0414" stroke="#4a1a36" stroke-width="1"/>
      <text x="15" y="25" font-weight="700" fill="#c084fc" font-size="11">PROFILE CLASSIFICATION</text>
      <text x="15" y="52" font-weight="750" fill="#ffffff">• AI / ML ENGINEER</text>
      <text x="15" y="72" font-weight="750" fill="#ffffff">• FULL STACK DEVELOPER</text>
      <text x="15" y="92" font-weight="750" fill="#ffffff">• RAG &amp; MULTI-AGENT SYSTEMS</text>
      <text x="15" y="112" font-weight="750" fill="#ffffff">• CLOUD-NATIVE &amp; DevOps</text>
      <text x="15" y="132" font-weight="750" fill="#ffffff">• OPEN SOURCE BUILDER</text>
    </g>

    <!-- System Analytics (Unique Progress Bars) -->
    {skills_markup}
  </g>

  <!-- ================= RIGHT COLUMN ================= -->

  <!-- Sub-col 1: ASCII Portrait Terminal -->
  <g class="glow-card" transform="translate(310, 15)">
    <rect width="300" height="320" rx="12" fill="#10051a" fill-opacity="0.85" stroke="#4a1a36" stroke-width="1.5"/>
    <g>
      <circle cx="18" cy="18" r="5" fill="#ff5f56" />
      <circle cx="33" cy="18" r="5" fill="#ffbd2e" />
      <circle cx="48" cy="18" r="5" fill="#27c93f" />
      <text x="150" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">tasmiya@matrix:~</text>
      <line x1="0" y1="36" x2="300" y2="36" stroke="#4a1a36" stroke-width="1"/>
    </g>
    <defs>
      {clips_str}
    </defs>
    {texts_str}
    {cursor_str}
  </g>

  <!-- Sub-col 2: Specs Terminal -->
  <g class="glow-card" transform="translate(625, 15)">
    <rect width="310" height="320" rx="12" fill="#10051a" fill-opacity="0.85" stroke="#4a1a36" stroke-width="1.5"/>
    <g>
      <circle cx="18" cy="18" r="5" fill="#ff5f56" />
      <circle cx="33" cy="18" r="5" fill="#ffbd2e" />
      <circle cx="48" cy="18" r="5" fill="#27c93f" />
      <text x="155" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">tasmiya@core:~</text>
      <line x1="0" y1="36" x2="310" y2="36" stroke="#4a1a36" stroke-width="1"/>
    </g>
    <g transform="translate(0, 0)">
      <text x="20" y="52" font-family="Consolas, monospace" font-size="14" font-weight="bold" fill="#ff9ecd">sys_info()</text>
    </g>
    {specs_str}
    {badges_str}

    <!-- Blinking prompt -->
    <g transform="translate(20, 280)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="12" fill="#8b949e">tasmiya@core:~$ </text>
      <rect x="110" y="-11" width="7" height="13" fill="#ff9ecd">
        <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" dur="0.8s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>

  <!-- ================= HORIZONTAL BLUEPRINT FLOW SECTION ================= -->
  <g transform="translate(310, 350)">
    <rect width="625" height="535" rx="15" fill="#090311" fill-opacity="0.95" stroke="#4a1a36" stroke-width="1.5"/>
    <text x="25" y="27" font-family="'Outfit', sans-serif" font-size="14" font-weight="bold" fill="#c084fc" style="filter: drop-shadow(0px 0px 3px #c084fc);">[ Architecture Graph ]</text>
    <line x1="25" y1="38" x2="600" y2="38" stroke="#4a1a36" stroke-width="1"/>
  </g>

  <g>
    {paths_markup}
    {pulses_markup}
    {nodes_markup}
  </g>

</svg>
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Tasmiya Unique Profile Dashboard SVG generated at {output_path}!")
