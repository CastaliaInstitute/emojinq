#!/usr/bin/env python3
"""Strengthen faint pattern/color concept glyphs as monochrome brush symbols."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "patterns"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "blue": '''
<path d="M10 39c7-13 15-13 22 0s15 13 22 0 13-13 18-2" stroke-width="2.6" {c}/>
<path d="M10 48c7-13 15-13 22 0s15 13 22 0" stroke-width="1.35" opacity=".72" {c}/>
<path d="M15 56c7-5 14-5 21 0M42 56c5-4 10-4 15 0" stroke-width="1.1" opacity=".65" {c}/>
''',
    "curve": '''
<path d="M17 58c3-17 11-29 27-39 4-3 8-5 12-5" stroke-width="2.5" {c}/>
<path d="M24 61c4-16 11-27 24-35" stroke-width="1.15" opacity=".7" {c}/>
<path d="M53 14l4 0-3 3" stroke-width="1.3" {c}/>
''',
    "green": '''
<path d="M36 61V22M36 39L22 28M36 47l15-13" stroke-width="2.1" {c}/>
<path d="M22 28c1-8 7-11 14-7-1 7-7 10-14 7zM51 34c-1-8-7-11-14-7 1 7 7 10 14 7z" stroke-width="2.0" {c}/>
<path d="M16 63h40" stroke-width="1" opacity=".6" {c}/>
''',
    "orange": '''
<path d="M20 53c-4-11 1-24 11-30 9-5 21-2 26 7 5 10 0 22-9 28-10 6-24 4-28-5z" stroke-width="2.45" {c}/>
<path d="M27 50c-3-8 1-17 8-21 7-4 15-2 19 5" stroke-width="1.55" {c}/>
<path d="M36 29l2 17M28 38l17 9M47 32l-6 15" stroke-width="1.0" opacity=".68" {c}/>
''',
    "oval": '''
<path d="M13 37c0-11 10-19 24-19s24 8 24 19-10 19-24 19-24-8-24-19z" stroke-width="2.55" {c}/>
<path d="M18 37c2-7 9-12 19-12s17 5 19 12c-2 7-9 12-19 12s-17-5-19-12z" stroke-width="1.2" opacity=".7" {c}/>
''',
    "purple": '''
<path d="M36 58V36M36 36c-8-2-13-7-11-14 7-1 12 3 11 10 2-8 7-12 14-10 1 7-4 12-12 14" stroke-width="2.25" {c}/>
<path d="M36 42c-7 1-12-2-14-8 6-3 12 0 14 6 2-6 8-9 14-6-2 6-7 9-14 8z" stroke-width="1.7" {c}/>
<path d="M27 61h18" stroke-width="1" opacity=".62" {c}/>
''',
    "red": '''
<path d="M36 61c-11-6-13-15-7-23 3-4 7-8 5-16 10 7 15 15 11 23-2 4-5 7-9 8z" stroke-width="2.5" {c}/>
<path d="M36 54c-5-4-5-9-1-14 2-2 3-4 2-7 6 5 7 10 4 15-1 3-3 5-5 6z" stroke-width="1.45" {c}/>
<path d="M24 62h24" stroke-width="1" opacity=".6" {c}/>
''',
    "sphere": '''
<circle cx="36" cy="37" r="22" stroke-width="2.5" {c}/>
<path d="M14 37h44M36 15c-8 7-11 14-11 22s3 15 11 22M36 15c8 7 11 14 11 22s-3 15-11 22" stroke-width="1.2" opacity=".72" {c}/>
<path d="M19 26c10 4 24 4 34 0M19 48c10-4 24-4 34 0" stroke-width="1.0" opacity=".6" {c}/>
''',
    "yellow": '''
<circle cx="36" cy="37" r="12" stroke-width="2.5" {c}/>
<path d="M36 10v9M36 55v9M9 37h9M55 37h9M17 18l6 6M49 50l6 6M55 18l-6 6M23 50l-6 6" stroke-width="1.7" {c}/>
<path d="M31 37c3-4 7-4 10 0-3 4-7 4-10 0z" stroke-width="1.1" opacity=".65" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"patterns / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} reviewed pattern studies")
