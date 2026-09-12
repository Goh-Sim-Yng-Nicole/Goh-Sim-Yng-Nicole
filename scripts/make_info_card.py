#!/usr/bin/env python3
"""
Render info-card.svg -- the neofetch-style "who am I" card that sits to the
RIGHT of the ASCII portrait in the profile README.

Static, like the portrait: run it by hand whenever the CARD contents below
change. Only the contribution heatmap regenerates daily.

    python scripts/make_info_card.py

Everything you'd want to edit lives in CARD. Keep values under ~54 characters
or they'll run past the right edge of the card.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from identity import DISPLAY_NAME, HANDLE, USERNAME

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

# ---- EDIT ME -------------------------------------------------------------
# (label, value) pairs, rendered in order. Labels are padded to the width of
# the longest one automatically, so you can add/remove rows freely.
CARD = [
    ("Host",       f"github.com/{USERNAME}"),
    ("Kernel",     "Python 3.11 · Node 20"),
    ("Editor",     "VS Code · Jupyter"),
    ("Languages",  "Python, JavaScript, TypeScript, SQL"),
    ("Data/ML",    "pandas, NumPy, scikit-learn"),
    ("Cloud",      "Docker, GitHub Actions"),
    ("Learning",   "systems design, LLM tooling, Agentic AI"),
    ("Currently",  "studying in Singapore Management University"),
    ("Pronouns",   "she/her"),
]
# --------------------------------------------------------------------------

# ---- geometry ------------------------------------------------------------
# Authored at 1100px wide; the README renders it at 490px (the ASCII portrait
# takes the other 370 of the heatmap's 860). Everything scales with it.
CANVAS_W = 1100
PAD = 36
TITLEBAR_H = 44

HEADER_FS = 34
ROW_FS = 25
ROW_H = 46
ADV = 0.6            # monospace advance width, in em

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
LABEL = "#39d353"    # same green as the heatmap's top end
ACCENT = "#22d3ee"

# ---- reveal timing (one-shot, matches the portrait's cadence) -------------
ROW_DUR = 0.34
STAGGER = 0.10

# ANSI-ish swatch strip, the way real neofetch signs off
SWATCHES = [
    "#161b22", "#f85149", "#39d353", "#f2cc60",
    "#58a6ff", "#bc8cff", "#22d3ee", "#c9d1d9",
    "#484f58", "#ff7b72", "#56d364", "#e3b341",
    "#79c0ff", "#d2a8ff", "#76e3ea", "#f0f6fc",
]

header = f"{HANDLE}@github"
label_w = max(len(lbl) for lbl, _ in CARD)

header_y = TITLEBAR_H + 54
rule_y = header_y + 16
rows_top = rule_y + 44
last_row_y = rows_top + (len(CARD) - 1) * ROW_H

sw_y = last_row_y + 40
sw_w = (CANVAS_W - PAD * 2) / len(SWATCHES)
sw_h = 30

prompt_y = sw_y + sw_h + 44
CANVAS_H = int(prompt_y + PAD)

esc = html.escape

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">',
    '<defs><linearGradient id="cbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#cbg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
    f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*22}" cy="{TITLEBAR_H/2}" r="7" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 5}" fill="{MUTED}" font-size="17" '
             f'text-anchor="middle">{esc(HANDLE)}@github: ~$ neofetch</text>')

# header: handle@github, underlined the way neofetch does it
parts.append(
    f'<text x="{PAD}" y="{header_y}" font-size="{HEADER_FS}" font-weight="700">'
    f'<tspan fill="{LABEL}">{esc(HANDLE)}</tspan>'
    f'<tspan fill="{MUTED}">@</tspan>'
    f'<tspan fill="{ACCENT}">github</tspan></text>'
)
rule_w = len(header) * HEADER_FS * ADV
parts.append(f'<line x1="{PAD}" y1="{rule_y}" x2="{PAD + rule_w:.1f}" y2="{rule_y}" '
             f'stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 4"/>')

# rows, each wiped in left-to-right so the card "types" itself
value_x = PAD + (label_w + 2) * ROW_FS * ADV
for i, (lbl, val) in enumerate(CARD):
    y = rows_top + i * ROW_H
    delay = i * STAGGER
    row = (
        f'<text x="{PAD}" y="{y}" font-size="{ROW_FS}" fill="{LABEL}" font-weight="700">'
        f'{esc(lbl)}<tspan fill="{MUTED}">:</tspan></text>'
        f'<text x="{value_x:.1f}" y="{y}" font-size="{ROW_FS}" fill="{INK}" '
        f'xml:space="preserve">{esc(val)}</text>'
    )
    parts.append(
        f'<clipPath id="row{i}"><rect x="{PAD}" y="{y - ROW_FS}" height="{ROW_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{CANVAS_W}" begin="{delay:.2f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#row{i})">{row}</g>')

# swatch strip
strip_delay = len(CARD) * STAGGER
for i, col in enumerate(SWATCHES):
    x = PAD + i * sw_w
    parts.append(
        f'<rect x="{x:.1f}" y="{sw_y}" width="{sw_w:.1f}" height="{sw_h}" fill="{col}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{strip_delay + i*0.03:.2f}s" dur="0.3s" fill="freeze"/></rect>'
    )

# trailing prompt with a cursor that blinks forever
prompt = f"{HANDLE}@github:~$ "
parts.append(f'<text x="{PAD}" y="{prompt_y}" font-size="{ROW_FS}" fill="{MUTED}" '
             f'xml:space="preserve">{esc(prompt)}<tspan fill="{INK}">{esc(DISPLAY_NAME)}</tspan></text>')
cursor_x = PAD + (len(prompt) + len(DISPLAY_NAME)) * ROW_FS * ADV + 6
parts.append(
    f'<rect x="{cursor_x:.1f}" y="{prompt_y - ROW_FS + 4}" width="{ROW_FS*ADV:.1f}" '
    f'height="{ROW_FS}" fill="{INK}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", CANVAS_W, "x", CANVAS_H)
