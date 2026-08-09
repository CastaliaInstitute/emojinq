#!/usr/bin/env python3
"""Simplify material studies into clear, traceable sumi-e forms."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "materials"
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "clay": """
<path d="M25 22h22l-2 8c8 5 10 13 8 22-2 8-9 12-17 12s-15-4-17-12c-2-9 1-17 8-22z" stroke-width="2.3" {i}/>
<path d="M23 22c0-4 4-6 13-6s13 2 13 6-4 5-13 5-13-1-13-5z" stroke-width="2.0" {i}/>
<path d="M21 45c9 4 21 4 30 0M23 55c8 3 18 3 26 0" stroke-width="1.15" {i}/>
""",
    "cloth": """
<path d="M13 23c8-4 16-4 23 0 8 4 15 4 23 0l1 28c-10 6-20 6-29 0-7-4-12-4-19 0z" stroke-width="2.2" {i}/>
<path d="M13 23c8 5 16 5 23 0 8 5 15 5 23 0M14 38c7 4 14 4 22 0 8 4 15 4 24 0" stroke-width="1.3" {i}/>
<path d="M19 29c2 2 4 3 7 3M43 31c3 1 5 1 8-1" stroke-width="1.0" opacity=".7" {i}/>
""",
    "fiber": """
<path d="M17 57c8-11 12-22 18-39M25 58c8-12 14-22 24-35M34 59c8-12 16-20 24-28" stroke-width="2.0" {i}/>
<path d="M17 57c4 2 8 2 12 0M25 58c4 2 9 2 13-1M34 59c4 2 9 1 13-2" stroke-width="1.0" {i}/>
""",
    "glass": """
<path d="M20 17h32l-3 36c-1 7-6 11-13 11s-12-4-13-11z" stroke-width="2.15" {i}/>
<path d="M20 17c0 4 7 6 16 6s16-2 16-6M24 45c7 3 17 3 25 0" stroke-width="1.2" {i}/>
<path d="M26 29c2 1 4 1 6 1" stroke-width="1.0" opacity=".7" {i}/>
""",
    "leather": """
<path d="M16 22c8-4 20-5 38-2l7 17-10 19c-14 4-26 3-38-2l-3-16z" stroke-width="2.25" {i}/>
<path d="M21 27c10-2 20-2 30 0M19 48c10 3 19 3 29 0" stroke-width="1.2" {i}/>
<path d="M25 34l17 8M28 31l17 8" stroke-width="1.0" opacity=".65" {i}/>
""",
    "metal": """
<path d="M14 26l39-10 7 30-39 10z" stroke-width="2.2" {i}/>
<path d="M20 29l34-8M23 39l29-7M28 49l22-6" stroke-width="1.15" {i}/>
<path d="M17 25l8 27" stroke-width="1.0" opacity=".65" {i}/>
""",
    "paper": """
<path d="M15 18l43 6v35l-43-6z" stroke-width="2.1" {i}/>
<path d="M15 18l20 19 23-13M35 37l-16 13M35 37l23 22" stroke-width="1.35" {i}/>
<path d="M23 29l9 2M22 35l9 2M21 42l8 2" stroke-width="1.0" {i}/>
""",
    "plastic": """
<path d="M28 18h16v7l5 6v25c0 4-5 7-13 7s-13-3-13-7V31l5-6z" stroke-width="2.2" {i}/>
<path d="M28 18h16M24 39c7 3 17 3 25 0" stroke-width="1.25" {i}/>
<path d="M31 13h10v5H31z" stroke-width="1.5" {i}/>
""",
    "sand": """
<path d="M9 51c10-11 20-15 31-11 8 3 14 3 23-5M10 59c13-5 25-5 36-1 8 3 15 2 21-1" stroke-width="2.0" {i}/>
<path d="M18 43c7-3 14-3 20 0M46 50c5-2 9-2 14 0" stroke-width="1.0" opacity=".7" {i}/>
""",
    "stone": """
<path d="M13 47c3-11 10-19 22-22 11 0 19 5 25 14l-4 17c-12 5-25 5-38 0z" stroke-width="2.3" {i}/>
<path d="M23 38c7-3 15-3 24 0M21 48c9-2 17-2 27 1" stroke-width="1.15" {i}/>
""",
    "thread": """
<path d="M24 22c3-5 8-7 12-7s9 2 12 7v30c-3 5-7 8-12 8s-9-3-12-8z" stroke-width="2.2" {i}/>
<path d="M24 22c0 5 5 8 12 8s12-3 12-8M24 52c0-5 5-8 12-8s12 3 12 8M29 30v14M43 30v14" stroke-width="1.2" {i}/>
<path d="M48 27c8 2 11 6 10 12-1 5-5 8-10 8" stroke-width="1.5" {i}/>
""",
}


def redraw(name: str, body: str) -> None:
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"materials / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — simplified naturalist study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for name, body in ART.items():
    redraw(name, body)
print(f"redrew {len(ART)} material studies")
