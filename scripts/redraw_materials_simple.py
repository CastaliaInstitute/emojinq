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
<path d="M21 22h30l-3 33c-1 5-8 8-12 8s-11-3-12-8z" stroke-width="2.3" {i}/>
<path d="M18 22c0-4 5-6 18-6s18 2 18 6-5 6-18 6-18-2-18-6z" stroke-width="2.0" {i}/>
<path d="M24 39c7 3 17 3 25 0M24 49c7 3 17 3 25 0" stroke-width="1.15" {i}/>
""",
    "cloth": """
<path d="M12 25l13-8 36 13-14 27-36-12z" stroke-width="2.2" {i}/>
<path d="M25 17l22 13 14 0M25 17l-1 28M24 45l23 12" stroke-width="1.4" {i}/>
<path d="M18 29c8 3 15 7 22 12M20 38c7 3 13 6 20 11" stroke-width="1.0" opacity=".75" {i}/>
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
<path d="M15 20l39 5 4 32-39-5z" stroke-width="2.1" {i}/>
<path d="M15 20l18 18 25-13M33 38l-14 14M33 38l25 19" stroke-width="1.35" {i}/>
<path d="M23 28l10 2M22 34l9 2" stroke-width="1.0" {i}/>
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
<path d="M21 21h30v33c-2 6-8 9-15 9s-13-3-15-9z" stroke-width="2.2" {i}/>
<path d="M21 21c0-4 7-6 15-6s15 2 15 6-7 6-15 6-15-2-15-6zM28 35c6 4 12 4 18 0M28 44c6 4 12 4 18 0" stroke-width="1.2" {i}/>
<path d="M51 27c8 2 11 6 10 12-1 5-5 8-10 8" stroke-width="1.5" {i}/>
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
