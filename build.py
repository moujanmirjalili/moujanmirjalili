# -*- coding: utf-8 -*-
from chili import CHILI, PALETTE, OUTLINE

HEADER = "moujan@mirjalili"

ROWS = [
    ("Uptime",                "24 years, 3 months"),
    ("Host",                  "Georg-August-Universitaet Goettingen"),
    ("Kernel",                "M.Sc. Applied Data Science"),
    ("Shell",                 "SUB Goettingen, R&D"),
    (None, ""),
    ("Languages.Programming", "Python, Java, C, C++, JavaScript"),
    ("Languages.Computer",    "HTML, CSS, JSON, LaTeX, YAML"),
    ("Languages.Real",        "Persian, English, German"),
    (None, ""),
    ("Research.Focus",        "NLP, Media Bias, Interpretability"),
    ("Research.Now",          "Definitional sensitivity in LLM data"),
    (None, ""),
    ("§", "Contact"),
    ("Email.Personal",        "moujanmirjalili@gmail.com"),
    ("Email.Uni",             "moujan.mirjalili@stud.uni-goettingen.de"),
    ("Website",               "moujanmirjalili.github.io"),
    ("LinkedIn",              "moujanmirjalili"),
    ("Discord",               "TODO"),
    (None, ""),
    ("§", "GitHub Stats"),
    ("Repos",                 "TODO"),
    ("Commits",               "TODO"),
    ("Stars",                 "TODO"),
    ("Followers",             "TODO"),
]

RW = 66     # right panel width, characters
CH = 8.4    # monospace advance at 14px
FS = 14
LH = 22
PX = 14     # pixel size of the chili

THEMES = {
    "dark":  dict(bg="#0d1117", panel="#161b22", border="#30363d",
                  label="#ffa657", value="#79c0ff", dots="#484f58",
                  head="#c9d1d9", rule="#484f58"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de",
                  label="#bc4c00", value="#0550ae", dots="#afb8c1",
                  head="#1f2328", rule="#afb8c1"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

ART_W = max(len(r) for r in CHILI) * PX
ART_H = len(CHILI) * PX
X_ART = 40
X_RIGHT = X_ART + ART_W + 46

def art_svg(y0, outline):
    out = []
    for r, row in enumerate(CHILI):
        run_start, run_col = None, None
        for c in range(len(row) + 1):
            ch = row[c] if c < len(row) else "."
            col = outline if ch == "K" else PALETTE.get(ch)
            if col != run_col:
                if run_col is not None:
                    w = (c - run_start) * PX
                    out.append(f'<rect x="{X_ART + run_start*PX}" y="{y0 + r*PX}" '
                               f'width="{w}" height="{PX}" fill="{run_col}"/>')
                run_start, run_col = c, col
        # flush handled by sentinel above
    return out

def build(c):
    out = []
    y = 74

    # right column
    dashes = "-" * max(0, RW - len(HEADER) - 1)
    out.append(f'<text x="{X_RIGHT}" y="{y}" xml:space="preserve">'
               f'<tspan fill="{c["head"]}" font-weight="bold">{esc(HEADER)}</tspan>'
               f'<tspan fill="{c["rule"]}"> {dashes}</tspan></text>')
    y += LH * 2

    for label, value in ROWS:
        if label is None:
            y += LH
            continue
        if label == "§":
            d = "-" * max(0, RW - len(value) - 4)
            out.append(f'<text x="{X_RIGHT}" y="{y}" xml:space="preserve">'
                       f'<tspan fill="{c["rule"]}">- </tspan>'
                       f'<tspan fill="{c["head"]}" font-weight="bold">{esc(value)}</tspan>'
                       f'<tspan fill="{c["rule"]}"> {d}</tspan></text>')
            y += LH
            continue
        head = f"  {label}: "
        ndots = max(1, RW - len(head) - len(value) - 1)
        out.append(f'<text x="{X_RIGHT}" y="{y}" xml:space="preserve">'
                   f'<tspan fill="{c["label"]}">{esc(head)}</tspan>'
                   f'<tspan fill="{c["dots"]}">{"." * ndots}</tspan>'
                   f'<tspan fill="{c["value"]}"> {esc(value)}</tspan></text>')
        y += LH

    text_bottom = y
    art_y = max(64, int((text_bottom - ART_H) / 2) + 10)
    out = art_svg(art_y, c["outline"]) + out

    W = int(X_RIGHT + RW * CH + 36)
    H = int(max(text_bottom + 16, art_y + ART_H + 40))
    body = "\n  ".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Moujan Mirjalili's GitHub profile">
  <style>
    text {{ font-family: "JetBrains Mono", "Fira Code", "SF Mono", "Cascadia Code", Consolas, "DejaVu Sans Mono", monospace; font-size: {FS}px; white-space: pre; }}
  </style>
  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}"/>
  {body}
</svg>
'''

for t, col in THEMES.items():
    col = dict(col, outline=OUTLINE[t])
    open(f"{t}_mode.svg", "w").write(build(col))
print("built")
