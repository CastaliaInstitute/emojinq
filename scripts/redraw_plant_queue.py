#!/usr/bin/env python3
"""Strengthen faint plant PUA studies while keeping their naturalist silhouettes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "plants"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "seed": '''
<path d="M36 59c-8-7-12-16-9-25 3-8 11-13 19-13 3 9 0 19-6 25-3 3-6 6-4 13z" stroke-width="2.6" {c}/>
<path d="M36 57c2-12 5-22 10-34M38 48l-10-8M41 39l12-8" stroke-width="1.35" {c}/>
<path d="M28 62c5-2 13-2 19 0" stroke-width="1" opacity=".62" {c}/>
''',
    "oak": '''
<path d="M36 57V27M36 39l-11-9M36 45l12-10M36 31l6-9" stroke-width="2.1" {c}/>
<path d="M25 31c-7 1-10-4-7-9 1-3 5-4 8-2 0-6 6-8 10-4 4-4 10-1 10 4 5-2 9 2 8 6-1 4-5 6-9 5-2 5-7 6-10 2-3 4-8 3-10-2z" stroke-width="2.25" {c}/>
<path d="M18 62h36M25 57h22" stroke-width="1.05" opacity=".68" {c}/>
''',
    "pine": '''
<path d="M36 11L22 34h8L18 48h12L20 61h32L42 48h12L42 34h8z" stroke-width="2.15" {c}/>
<path d="M36 11v50" stroke-width="1.35" {c}/>
<path d="M30 22l6 4 6-4M27 35l9 5 9-5M25 48l11 6 11-6" stroke-width="1.05" opacity=".74" {c}/>
''',
    "root": '''
<path d="M36 12c-1 11-2 20-2 29 0 7-4 10-10 13M35 41c6 5 11 9 17 12M31 45c-5 5-9 8-15 10M39 45c4 6 8 10 12 13" stroke-width="2.25" {c}/>
<path d="M35 22l-8 7M36 29l9 7M31 50l-8 9M43 52l8 7" stroke-width="1.25" {c}/>
<path d="M10 62c9-3 18-3 27 0 9-3 18-3 25 0" stroke-width="1.1" opacity=".64" {c}/>
''',
    "stream": '''
<path d="M14 18c12 7 15 14 10 21-5 7-3 14 10 18 12 4 19 0 19-8 0-6-5-10-11-11-7-1-12 3-12 8" stroke-width="2.25" {c}/>
<path d="M20 15c10 6 14 12 10 18M47 22c7 5 9 11 6 16M18 57c8 5 17 7 27 5" stroke-width="1.15" opacity=".72" {c}/>
<path d="M13 29l-5 5M57 48l6 3M30 62h13" stroke-width="1.0" opacity=".6" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"plants / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} reviewed plant studies")
