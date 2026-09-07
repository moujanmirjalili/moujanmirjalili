THEMES = {
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
                  prompt="#0969da", green="#1a7f37", gray="#6e7781", accent="#bc4c00",
                  d1="#ff5f57", d2="#febc2e", d3="#28c840"),
    "dark":  dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#c9d1d9",
                  prompt="#58a6ff", green="#3fb950", gray="#8b949e", accent="#ffa657",
                  d1="#ff5f57", d2="#febc2e", d3="#28c840"),
}

# (class, text) — None means blank line
LINES = [
    ("cmd",  "moujan@goettingen:~$ whoami"),
    ("out",  "Moujan Mirjalili"),
    ("dim",  "M.Sc. Applied Data Science, University of Goettingen"),
    (None,   ""),
    ("cmd",  "moujan@goettingen:~$ cat interests.txt"),
    ("acc",  "NLP  ·  Media Bias  ·  AI Interpretability"),
    (None,   ""),
    ("cmd",  "moujan@goettingen:~$ ./thesis --status"),
    ("dim",  "[*] generating 7,680 synthetic news articles"),
    ("dim",  "[*] asking 4 language models what \"bias\" means"),
    ("out",  "[!] they disagree. that's the finding."),
    (None,   ""),
    ("cmd",  "moujan@goettingen:~$ ls projects/"),
    ("acc",  "the-cats-take-over/   dnlp/   backdoors-in-llms/"),
    ("dim",  "# a detective game about a viral video. the cats"),
    ("dim",  "# were not taking over. it was a festival."),
    (None,   ""),
    ("cmd",  "moujan@goettingen:~$ contact --list"),
    ("out",  "moujanmirjalili@gmail.com"),
    ("dim",  "moujanmirjalili.github.io   ·   linkedin.com/in/moujanmirjalili"),
    (None,   ""),
]

W, H = 860, 700
X = 42
Y0 = 108
LH = 25

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build(name, c):
    rows = []
    y = Y0
    delay = 0.0
    for cls, txt in LINES:
        if cls is None:
            y += LH
            continue
        rows.append(
            f'<text x="{X}" y="{y}" class="{cls} line" style="animation-delay:{delay:.2f}s">{esc(txt)}</text>'
        )
        y += LH
        delay += 0.14
    cursor_y = y
    rows.append(f'<text x="{X}" y="{cursor_y}" class="cmd line" style="animation-delay:{delay:.2f}s">moujan@goettingen:~$ <tspan class="cursor">&#9608;</tspan></text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Moujan Mirjalili's GitHub profile">
  <style>
    .win {{ fill: {c["panel"]}; stroke: {c["border"]}; stroke-width: 1; }}
    text {{ font-family: "JetBrains Mono", "Fira Code", "SF Mono", "Cascadia Code", Consolas, "Courier New", monospace; font-size: 15px; dominant-baseline: middle; }}
    .cmd  {{ fill: {c["prompt"]}; }}
    .out  {{ fill: {c["text"]}; }}
    .acc  {{ fill: {c["green"]}; }}
    .dim  {{ fill: {c["gray"]}; }}
    .title {{ fill: {c["gray"]}; font-size: 13px; }}
    .badge {{ fill: {c["accent"]}; font-size: 13px; }}
    .line {{ animation: fadein 0.35s ease both; }}
    @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .cursor {{ animation: blink 1.05s steps(2, start) infinite; }}
    @keyframes blink {{ to {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .line {{ animation: none; }}
      .cursor {{ animation: none; }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  <rect x="12" y="12" width="{W-24}" height="{H-24}" rx="10" class="win"/>

  <circle cx="40"  cy="44" r="6.5" fill="{c["d1"]}"/>
  <circle cx="62"  cy="44" r="6.5" fill="{c["d2"]}"/>
  <circle cx="84"  cy="44" r="6.5" fill="{c["d3"]}"/>
  <text x="{W//2}" y="44" class="title" text-anchor="middle">moujan@goettingen — zsh — 86×26</text>
  <text x="{W-42}" y="44" class="badge" text-anchor="end">🌶️</text>

  <line x1="12" y1="68" x2="{W-12}" y2="68" stroke="{c["border"]}" stroke-width="1"/>

  {chr(10).join("  " + r for r in rows)}
</svg>
'''

for name, c in THEMES.items():
    open(f"{name}_mode.svg", "w").write(build(name, c))
print("built light_mode.svg and dark_mode.svg")
