#!/usr/bin/env python3
"""Repair the two visibly cropped location studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "locations"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "barn": '''
<path d="M12 60V29l24-17 24 17v31z" stroke-width="2.7" {c}/>
<path d="M36 12v17M12 29h48M24 60V43h24v17" stroke-width="2.0" {c}/>
<path d="M17 34h8M47 34h8M17 40h8M47 40h8M18 52h5M49 52h5" stroke-width="1.15" opacity=".72" {c}/>
<path d="M9 62h54M15 24l21-15 21 15" stroke-width="1.1" opacity=".62" {c}/>
''',
    "tower": '''
<path d="M27 57l4-32h10l4 32z" stroke-width="2.6" {c}/>
<path d="M28 25h16M30 20h12M32 15h8v5M34 15v-4h4v4" stroke-width="2.0" {c}/>
<path d="M31 32h10M30 39h12M29 47h14" stroke-width="1.1" opacity=".72" {c}/>
<path d="M8 61c8-5 15-5 22 0s14 5 21 0 13-5 20 0M10 66c10-4 18-4 26 0 8-4 16-4 26 0" stroke-width="1.35" {c}/>
<path d="M21 56c-3-4-6-5-9-4M51 56c3-4 6-5 9-4" stroke-width="1.05" opacity=".64" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"locations / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} reviewed location studies")
