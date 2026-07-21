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
    ("Role",     "AI Engineer | Full-Stack Dev"),
    ("Stack",    "Python | FastAPI | React | TS"),
    ("AI",       "LLMs | LangGraph | RAG | CV"),
    ("Infra",    "Docker | K8s | PostgreSQL | Redis"),
    ("Projects", "Enterprise Multi-Agent AI"),
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
    <text x="100" y="{y_spec}" font-family="Consolas, monospace" font-size="12" fill="#f0d6ff">{value}</text>
  </g>"""
    y_spec += 25

# Blueprint nodes
NODES = [
    ("root", "Repositories",               440, 405, 140, 34, "root"),
    ("p1",   "AI Platform",                320, 485, 120, 30, "child"),
    ("p2",   "RAG Platform",               470, 485, 130, 30, "child"),
    ("p3",   "More Projects",              640, 485, 120, 30, "child"),
    ("c1",   "Multi-Agent Orchestration",  285, 565, 175, 30, "child"),
    ("c2",   "Hybrid RAG Retrieval",       475, 565, 145, 30, "child"),
    ("c3",   "Multilingual Chatbot",       640, 565, 140, 30, "child"),
    ("c4",   "Plant Disease AI",           800, 565, 120, 30, "child"),
    ("s1",   "LangGraph + WebSocket",      325, 645, 150, 30, "child"),
    ("s2",   "BM25 + BGE + RRF",           490, 645, 130, 30, "child"),
    ("s3",   "NLP + Context State",        650, 645, 130, 30, "child"),
]

nodes_markup = ""
paths_markup = ""
pulses_markup = ""

# Root -> Level 1  (root bottom = 405+34 = 439)
paths_markup += '<path d="M 510 439 L 510 460 L 380 460 L 380 485" fill="none" stroke="#ff4fa3" stroke-width="1.5" opacity="0.6"/>'
paths_markup += '<path d="M 510 439 L 510 485" fill="none" stroke="#ff9ecd" stroke-width="2" opacity="0.8"/>'
paths_markup += '<path d="M 510 439 L 510 460 L 700 460 L 700 485" fill="none" stroke="#ff4fa3" stroke-width="1.5" opacity="0.6"/>'

pulses_markup += """
<circle r="3" fill="#ffffff">
  <animateMotion path="M 510 439 Q 510 460 380 460 L 380 485" dur="4s" repeatCount="indefinite"/>
</circle>
<circle r="3" fill="#ffffff">
  <animateMotion path="M 510 439 L 510 485" dur="3s" repeatCount="indefinite"/>
</circle>
<circle r="3" fill="#ffffff">
  <animateMotion path="M 510 439 Q 510 460 700 460 L 700 485" dur="5s" repeatCount="indefinite"/>
</circle>
"""

# Level 1 -> Level 2  (level1 bottom = 485+30 = 515)
connections_l1_l2 = [
    (380, 515, 372, 565),
    (380, 515, 547, 565),
    (535, 515, 547, 565),
    (535, 515, 710, 565),
    (700, 515, 710, 565),
    (700, 515, 860, 565),
]
for fx, fy, tx, ty in connections_l1_l2:
    paths_markup += f'<path d="M {fx} {fy} L {fx} {fy+15} L {tx} {fy+15} L {tx} {ty}" fill="none" stroke="#9d2060" stroke-dasharray="3 3" stroke-width="1"/>'

# Level 2 -> Level 3  (level2 bottom = 565+30 = 595)
connections_l2_l3 = [
    (372, 595, 400, 645),
    (547, 595, 555, 645),
    (710, 595, 715, 645),
]
for fx, fy, tx, ty in connections_l2_l3:
    paths_markup += f'<path d="M {fx} {fy} L {tx} {ty}" fill="none" stroke="#ff4fa3" stroke-width="1.2" opacity="0.7"/>'
    pulses_markup += f"""
<circle r="2.5" fill="#ff9ecd">
  <animateMotion path="M {fx} {fy} L {tx} {ty}" dur="{3.5 + (fx%3)}s" repeatCount="indefinite"/>
</circle>"""

# Render node boxes
for n in NODES:
    nx, ny, nw, nh, nt = n[2], n[3], n[4], n[5], n[6]
    label = n[1]
    stroke_col = "#ff9ecd" if nt == "root" else "#ff4fa3"
    glow_col   = "drop-shadow(0px 0px 6px rgba(255,158,205,0.8))" if nt == "root" else "drop-shadow(0px 0px 4px rgba(255,79,163,0.4))"
    b_fill     = "#2a0d1e" if nt == "root" else "#1a0a18"
    t_col      = "#ffffff" if nt == "root" else "#ffd6ee"
    nodes_markup += f"""
  <!-- Node: {label} -->
  <g transform="translate({nx}, {ny})">
    <rect width="{nw}" height="{nh}" rx="6" fill="{b_fill}" stroke="{stroke_col}" stroke-width="1.2" style="filter: {glow_col};" opacity="0.9"/>
    <text x="{nw//2}" y="{nh//2 + 4}" font-family="Outfit, Inter, sans-serif" font-size="10.5" font-weight="bold" fill="{t_col}" text-anchor="middle">{label}</text>
  </g>"""

# Floating tech badges (right of terminal card — terminal at translate(625,15), width=310)
badges_str = """
  <!-- Badge: LangGraph — aligned to AI row (local y=120 → abs y=135) -->
  <g transform="translate(850, 108)">
    <rect x="0" y="0" width="85" height="24" rx="12" fill="#1a0f2e" stroke="#ff9ecd" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(255,158,205,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#ff9ecd">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
    </circle>
    <text x="49" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">LangGraph</text>
    <line x1="0" y1="12" x2="-25" y2="12" stroke="#ff9ecd" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>

  <!-- Badge: RAG — aligned to Stack row (local y=145 → abs y=160) -->
  <g transform="translate(858, 145)">
    <rect x="0" y="0" width="65" height="24" rx="12" fill="#1a0f2e" stroke="#c084fc" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(192,132,252,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#c084fc">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite" />
    </circle>
    <text x="38" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">RAG</text>
    <line x1="0" y1="12" x2="-25" y2="12" stroke="#c084fc" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>

  <!-- Badge: Docker — aligned to Infra row (local y=170 → abs y=185) -->
  <g transform="translate(848, 182)">
    <rect x="0" y="0" width="77" height="24" rx="12" fill="#1a0f2e" stroke="#67e8f9" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(103,232,249,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#67e8f9">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite" />
    </circle>
    <text x="45" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">Docker</text>
    <line x1="0" y1="12" x2="-25" y2="12" stroke="#67e8f9" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>

  <!-- Badge: K8s — at prompt area (local y=280 → abs y=295) -->
  <g transform="translate(780, 278)">
    <rect x="0" y="0" width="65" height="24" rx="12" fill="#1a0f2e" stroke="#ffaa00" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(255,170,0,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#ffaa00">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.2s" repeatCount="indefinite" />
    </circle>
    <text x="38" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">K8s</text>
    <line x1="0" y1="12" x2="-25" y2="12" stroke="#ffaa00" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>
"""

# Motherboard pins (cartridges)
pins_markup = """
  <!-- Motherboard cartridges design at bottom left panel -->
  <g transform="translate(25, 520)">
    <rect width="250" height="330" rx="10" fill="#100818" stroke="#3d1a2e" stroke-width="1.5"/>
    <text x="15" y="27" font-family="Outfit, sans-serif" font-size="14" font-weight="bold" fill="#ff9ecd" style="filter: drop-shadow(0px 0px 3px #ff9ecd);">[ System Modules ]</text>
    <line x1="15" y1="36" x2="235" y2="36" stroke="#3d1a2e" stroke-width="1"/>

    <!-- Cartridge 1 -->
    <g transform="translate(15, 50)">
      <rect width="220" height="50" rx="5" fill="#1a0f2e" stroke="#ff4fa3" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#ff9ecd"/>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">Multi-Agent AI</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#ff9ecd">PORT_01 // ORCHESTRATOR</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#ff9ecd" stroke-width="2"/>
    </g>

    <!-- Cartridge 2 -->
    <g transform="translate(15, 115)">
      <rect width="220" height="50" rx="5" fill="#1a0f2e" stroke="#ff4fa3" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#ff9ecd"/>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">RAG Platform</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#ff9ecd">PORT_02 // RETRIEVAL_ONLINE</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#ff9ecd" stroke-width="2"/>
    </g>

    <!-- Cartridge 3 -->
    <g transform="translate(15, 180)">
      <rect width="220" height="50" rx="5" fill="#1a0f2e" stroke="#ff4fa3" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#c084fc">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">NLP Chatbot</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#c084fc">PORT_03 // INFERENCE_READY</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#c084fc" stroke-width="2"/>
    </g>

    <!-- Cartridge 4 -->
    <g transform="translate(15, 245)">
      <rect width="220" height="50" rx="5" fill="#1a0f2e" stroke="#ff4fa3" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#ff9ecd"/>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">Plant Disease CNN</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#ff9ecd">PORT_04 // CV_DEPLOYED</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#ff9ecd" stroke-width="2"/>
    </g>
  </g>
"""

grid_pattern = """
  <defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e0f2a" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)" />
"""

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="950"
     height="900"
     viewBox="0 0 950 900"
     fill="none">
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&amp;display=swap');
    .glow-card {{
      filter: drop-shadow(0px 0px 10px rgba(255, 79, 163, 0.15));
    }}
    .circle-scan {{
      transform-origin: 140px 140px;
    }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="15" fill="#0d0618" stroke="#3d1a2e" stroke-width="2"/>
  {grid_pattern}

  <!-- ================= LEFT COLUMN ================= -->
  <g class="glow-card" transform="translate(15, 15)">
    <rect width="280" height="870" rx="16" fill="#100820" fill-opacity="0.85" stroke="#3d1a2e" stroke-width="1.5"/>

    <!-- Holographic Scanner rings -->
    <g class="circle-scan">
      <circle cx="140" cy="140" r="72" fill="none" stroke="#ff9ecd" stroke-dasharray="12 8" stroke-width="1.5">
        <animateTransform attributeName="transform" type="rotate" from="0 140 140" to="360 140 140" dur="18s" repeatCount="indefinite"/>
      </circle>
      <circle cx="140" cy="140" r="80" fill="none" stroke="#c084fc" stroke-dasharray="5 15" stroke-width="1">
        <animateTransform attributeName="transform" type="rotate" from="360 140 140" to="0 140 140" dur="24s" repeatCount="indefinite"/>
      </circle>
      <circle cx="140" cy="140" r="62" fill="none" stroke="#ff4fa3" stroke-width="1" stroke-opacity="0.5"/>
      <path d="M 140 50 L 140 65 M 140 215 L 140 230 M 50 140 L 65 140 M 215 140 L 230 140" stroke="#ff9ecd" stroke-width="1" opacity="0.6"/>
    </g>

    <!-- Avatar Image -->
    <defs>
      <clipPath id="avatar-clip">
        <circle cx="140" cy="140" r="58"/>
      </clipPath>
    </defs>
    {"" if not photo_b64 else f'<image href="data:image/jpeg;base64,{photo_b64}" x="75" y="75" width="130" height="130" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>'}

    <!-- Name & handle -->
    <text x="140" y="255" font-family="'Outfit', sans-serif" font-weight="800" font-size="22" fill="#ffffff" text-anchor="middle">Tasmiya A</text>
    <text x="140" y="280" font-family="Consolas, monospace" font-size="11.5" fill="#ff9ecd" text-anchor="middle">tasmiya-a25 • she/her</text>
    <line x1="30" y1="295" x2="250" y2="295" stroke="#3d1a2e" stroke-width="1"/>

    <!-- Profile Classification -->
    <g transform="translate(20, 312)" font-family="'Outfit', sans-serif" font-size="11" fill="#ffd6ee">
      <rect width="240" height="165" rx="8" fill="#100820" stroke="#3d1a2e" stroke-width="1"/>
      <text x="15" y="25" font-weight="700" fill="#ff9ecd" font-size="11">PROFILE CLASSIFICATION</text>
      <text x="15" y="52" font-weight="750" fill="#ffffff">• AI / ML ENGINEER</text>
      <text x="15" y="72" font-weight="750" fill="#ffffff">• FULL STACK DEVELOPER</text>
      <text x="15" y="92" font-weight="750" fill="#ffffff">• RAG &amp; MULTI-AGENT SYSTEMS</text>
      <text x="15" y="112" font-weight="750" fill="#ffffff">• CLOUD-NATIVE &amp; DevOps</text>
      <text x="15" y="132" font-weight="750" fill="#ffffff">• OPEN SOURCE BUILDER</text>
    </g>

    <!-- Pins / Cartridges -->
    {pins_markup}
  </g>

  <!-- ================= RIGHT COLUMN ================= -->

  <!-- Sub-col 1: ASCII Portrait Terminal -->
  <g class="glow-card" transform="translate(310, 15)">
    <rect width="300" height="320" rx="12" fill="#100820" fill-opacity="0.85" stroke="#3d1a2e" stroke-width="1.5"/>
    <g>
      <circle cx="18" cy="18" r="5" fill="#ff5f56" />
      <circle cx="33" cy="18" r="5" fill="#ffbd2e" />
      <circle cx="48" cy="18" r="5" fill="#27c93f" />
      <text x="150" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">tasmiya@portrait:~</text>
      <line x1="0" y1="36" x2="300" y2="36" stroke="#3d1a2e" stroke-width="1"/>
    </g>
    <defs>
      {clips_str}
    </defs>
    {texts_str}
    {cursor_str}
  </g>

  <!-- Sub-col 2: Specs Terminal -->
  <g class="glow-card" transform="translate(625, 15)">
    <rect width="310" height="320" rx="12" fill="#100820" fill-opacity="0.85" stroke="#3d1a2e" stroke-width="1.5"/>
    <g>
      <circle cx="18" cy="18" r="5" fill="#ff5f56" />
      <circle cx="33" cy="18" r="5" fill="#ffbd2e" />
      <circle cx="48" cy="18" r="5" fill="#27c93f" />
      <text x="155" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">tasmiya@terminal:~</text>
      <line x1="0" y1="36" x2="310" y2="36" stroke="#3d1a2e" stroke-width="1"/>
    </g>
    <g transform="translate(0, 0)">
      <text x="20" y="52" font-family="Consolas, monospace" font-size="14" font-weight="bold" fill="#ff9ecd">tasmiya@github</text>
    </g>
    {specs_str}

    <!-- Blinking prompt -->
    <g transform="translate(20, 280)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="12" fill="#8b949e">tasmiya@terminal:~$ </text>
      <rect x="148" y="-11" width="7" height="13" fill="#ff9ecd">
        <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" dur="0.8s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>

  <!-- ================= BLUEPRINT FLOW SECTION ================= -->
  <g transform="translate(310, 350)">
    <rect width="625" height="535" rx="15" fill="#0a0514" fill-opacity="0.95" stroke="#3d1a2e" stroke-width="1.5"/>
    <text x="25" y="27" font-family="'Outfit', sans-serif" font-size="14" font-weight="bold" fill="#ff9ecd" style="filter: drop-shadow(0px 0px 3px #ff9ecd);">[ Holographic System Blueprint ]</text>
    <line x1="25" y1="38" x2="600" y2="38" stroke="#3d1a2e" stroke-width="1"/>
  </g>

  <g>
    {paths_markup}
    {pulses_markup}
    {nodes_markup}
    {badges_str}
  </g>

</svg>
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Tasmiya Profile Dashboard SVG generated at {output_path}!")
