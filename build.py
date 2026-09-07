# -*- coding: utf-8 -*-
import json, os
from chili import CHILI_WIDE as CHILI, PALETTE, OUTLINE, glyph

S = json.load(open(os.path.join(os.path.dirname(__file__), "stats.json")))

HEADER = "moujan@mirjalili"

ROWS = [
    ("Uptime",                "25 years, 9 months"),
    ("Host",                  "Georg-August-Universitaet Goettingen"),
    ("Kernel",                "M.Sc. Applied Data Science"),
    ("Shell",                 "SUB Goettingen, R&D"),
    (None, ""),
    ("Languages.Programming", "Python, Java, C, C++, JavaScript"),
    ("Languages.Computer",    "HTML, CSS, JSON, LaTeX, YAML"),
    ("Languages.Real",        "Persian, English, German"),
    ("Frameworks",            "PyTorch, TensorFlow, Keras, Hugging Face Transformers"),
    ("Libraries",             "scikit-learn, pandas, NumPy, Matplotlib, Phaser"),
    ("AI.Tooling",            "Prompt engineering, RAG, fine-tuning and evaluation"),
    ("AI.APIs",               "Claude, OpenAI, Claude Code, Copilot"),
    ("Databases",             "MySQL"),
    ("Tools",                 "Git, LaTeX, Linux"),
    (None, ""),
    ("Research.Focus",        "NLP, Media Bias, Interpretability"),
    ("Research.Thesis",       "Definitional sensitivity in LLM data"),
    ("Research.Also",         "LRM perception under refusal steering"),
    ("Research.Also",         "Book classification"),
    (None, ""),
    ("§", "Contact"),
    ("Email.Personal",        "moujanmirjalili@gmail.com"),
    ("Email.Uni",             "moujan.mirjalili@stud.uni-goettingen.de"),
    ("Email.Work",            "moujan.mirjalili@sub.uni-goettingen.de"),
    ("Website",               "moujanmirjalili.github.io"),
    ("LinkedIn",              "linkedin.com/in/moujanmirjalili"),
    (None, ""),
    ("§", "GitHub"),
    ("Member since",          S["member_since"]),
    ("Repos",                 S["repos"]),
    ("Followers",             S["followers"]),
    ("Following",             S["following"]),
]

if S.get("stars") is not None:
    ROWS.append(("Stars", S["stars"]))
if S.get("commits") is not None:
    ROWS.append(("Commits", S["commits"]))

RW = 74
CH = 8.4
FS = 14
LH = 22
ART_FS = 13
ART_CH = ART_FS * 0.60
ART_LH = 14

THEMES = {
    "dark":  dict(bg="#0d1117", panel="#161b22", border="#30363d",
                  label="#39ff6a", value="#79c0ff", dots="#484f58",
                  head="#c9d1d9", rule="#484f58"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de",
                  label="#0f7b2e", value="#0550ae", dots="#afb8c1",
                  head="#1f2328", rule="#afb8c1"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

ART_COLS = max(len(r) for r in CHILI)
X_ART = 40
X_RIGHT = X_ART + ART_COLS * ART_CH + 40

def art_svg(y0, outline):
    """Emit one <text> per coloured run, positioned explicitly, so the art does not
    depend on leading whitespace surviving the renderer."""
    out = []
    for r, row in enumerate(CHILI):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            col = outline if ch == "K" else PALETTE.get(ch)
            start_c, buf = c, ""
            while c < len(row):
                ch2 = row[c]
                col2 = outline if ch2 == "K" else PALETTE.get(ch2)
                if ch2 == "." or col2 != col:
                    break
                buf += glyph(ch2, r, c)
                c += 1
            xs = " ".join(f"{X_ART + (start_c + i) * ART_CH:.1f}" for i in range(len(buf)))
            out.append(f'<text x="{xs}" y="{y0 + r*ART_LH}" font-size="{ART_FS}" '
                       f'fill="{col}" xml:space="preserve">{esc(buf)}</text>')
    return out

def build(c):
    out, y = [], 74
    dashes = "-" * max(0, RW - len(HEADER) - 1)
    out.append(f'<text x="{X_RIGHT:.0f}" y="{y}" xml:space="preserve">'
               f'<tspan fill="{c["head"]}" font-weight="bold">{esc(HEADER)}</tspan>'
               f'<tspan fill="{c["rule"]}"> {dashes}</tspan></text>')
    y += LH * 2

    for label, value in ROWS:
        if label is None:
            y += LH; continue
        if label == "§":
            d = "-" * max(0, RW - len(value) - 4)
            out.append(f'<text x="{X_RIGHT:.0f}" y="{y}" xml:space="preserve">'
                       f'<tspan fill="{c["rule"]}">- </tspan>'
                       f'<tspan fill="{c["head"]}" font-weight="bold">{esc(value)}</tspan>'
                       f'<tspan fill="{c["rule"]}"> {d}</tspan></text>')
            y += LH; continue
        head = f"  {label}: "
        ndots = max(1, RW - len(head) - len(value) - 1)
        out.append(f'<text x="{X_RIGHT:.0f}" y="{y}" xml:space="preserve">'
                   f'<tspan fill="{c["label"]}">{esc(head)}</tspan>'
                   f'<tspan fill="{c["dots"]}">{"." * ndots}</tspan>'
                   f'<tspan fill="{c["value"]}"> {esc(value)}</tspan></text>')
        y += LH

    art_h = len(CHILI) * ART_LH
    art_y = max(78, int((y - art_h) / 2))
    out = art_svg(art_y, c["outline"]) + out

    W = int(X_RIGHT + RW * CH + 36)
    H = int(max(y + 16, art_y + art_h + 40))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Moujan Mirjalili's GitHub profile">
  <style>
    text {{ font-family: "JetBrains Mono", "Fira Code", "SF Mono", "Cascadia Code", Consolas, "DejaVu Sans Mono", monospace; font-size: {FS}px; white-space: pre; }}
    .art {{ font-size: {ART_FS}px; letter-spacing: 0; }}
  </style>
  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}"/>
  {chr(10).join("  " + o for o in out)}
</svg>
'''

for t, col in THEMES.items():
    open(f"{t}_mode.svg", "w").write(build(dict(col, outline=OUTLINE[t])))
print("built")
