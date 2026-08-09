#!/usr/bin/env python3
"""Repair faint material and weather silhouettes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    ("materials", "plastic"): '''
<path d="M28 16h16M30 16v8c0 3-5 5-6 10l-3 22c-1 6 3 9 15 9s16-3 15-9l-3-22c-1-5-6-7-6-10v-8" stroke-width="2.45" {c}/>
<path d="M23 42c8 3 18 3 26 0M22 50c8 3 20 3 28 0M28 23h16" stroke-width="1.25" opacity=".72" {c}/>
<path d="M32 12h8" stroke-width="1.1" opacity=".62" {c}/>
''',
    ("weather_sky", "shade"): '''
<path d="M13 35c7-13 16-19 26-19s19 6 26 19" stroke-width="2.5" {c}/>
<path d="M18 35c6 11 14 17 21 17s15-6 21-17" stroke-width="1.6" opacity=".72" {c}/>
<path d="M22 29c5-4 9-5 14-5M42 24c5 0 9 2 13 5" stroke-width="1.15" {c}/>
<path d="M18 57c8-3 18-3 27 0 4 1 7 1 10 0" stroke-width="1.0" opacity=".62" {c}/>
''',
    ("weather_sky", "sky"): '''
<path d="M10 45c9-7 18-7 27 0s17 7 25 0" stroke-width="2.15" {c}/>
<path d="M14 53c8-5 16-5 24 0s15 5 22 0" stroke-width="1.2" opacity=".7" {c}/>
<path d="M36 15v11M29 21h14M31 18l10 6M41 18l-10 6" stroke-width="1.45" {c}/>
<path d="M18 34c3-5 8-7 13-5 3-6 12-6 15 0 5-2 10 1 11 5" stroke-width="1.55" {c}/>
''',
}

for (category, name), body in ART.items():
    path = ROOT / "assets" / "pua" / category / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"{category} / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} material/weather studies")
