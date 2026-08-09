#!/usr/bin/env python3
"""Repair people studies that remain too fragmentary at display scale."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "protection": '''
<path d="M36 12l22 8v16c0 13-9 22-22 27C23 58 14 49 14 36V20z" stroke-width="2.5" {c}/>
<path d="M36 25c-5-6-14-3-14 4 0 7 8 12 14 18 6-6 14-11 14-18 0-7-9-10-14-4z" stroke-width="2.0" {c}/>
<path d="M27 37c3 3 6 4 9 4s6-1 9-4" stroke-width="1.15" opacity=".68" {c}/>
''',
    "work": '''
<circle cx="26" cy="19" r="7" stroke-width="2.3" {c}/>
<path d="M20 27c-5 5-7 12-6 21l-4 13M32 27c5 4 7 10 7 17l8 10M20 39l-9 7M32 39l14-5" stroke-width="2.25" {c}/>
<path d="M39 44h21v14H39zM42 40h15" stroke-width="1.9" {c}/>
<path d="M43 49h13M43 54h9M10 62h53" stroke-width="1.05" opacity=".65" {c}/>
''',
    "peace": '''
<path d="M36 56c-9-10-19-16-19-26 0-6 6-9 10-5 3 3 5 7 9 12 4-5 6-9 9-12 4-4 10-1 10 5 0 10-10 16-19 26z" stroke-width="2.35" {c}/>
<path d="M36 37c-3 6-3 12 0 19M28 34c-5 0-9-2-12-5M44 34c5 0 9-2 12-5" stroke-width="1.45" {c}/>
<path d="M10 61h52" stroke-width="1" opacity=".6" {c}/>
''',
    "kindness": '''
<path d="M10 54c7-8 14-10 21-5l5 4 5-4c7-5 14-3 21 5" stroke-width="2.45" {c}/>
<path d="M36 53c-7-8-15-7-16-1-1 5 5 8 16 14 11-6 17-9 16-14-1-6-9-7-16 1z" stroke-width="2.0" {c}/>
<path d="M21 34c3-6 8-8 15-6M51 34c-3-6-8-8-15-6" stroke-width="1.25" opacity=".68" {c}/>
<path d="M14 61h44" stroke-width="1" opacity=".6" {c}/>
''',
    "village": '''
<path d="M10 57V35l12-10 12 10v22zM36 57V29l13-12 13 12v28z" stroke-width="2.35" {c}/>
<path d="M14 35h16M40 29h18M18 45h6v12h-6zM45 41h8v16h-8zM48 17v-5" stroke-width="1.7" {c}/>
<path d="M8 61h57M18 61c4-5 8-5 12 0M40 61c4-5 8-5 12 0" stroke-width="1.1" opacity=".68" {c}/>
''',
    "pilgrimage": '''
<circle cx="29" cy="17" r="7" stroke-width="2.3" {c}/>
<path d="M24 25c-5 6-6 13-4 21l-8 13M34 25c4 6 6 12 7 19l7 13M24 36l-10 7M34 36l12-4" stroke-width="2.2" {c}/>
<path d="M51 19v42M51 19l8 5M51 27l7-4" stroke-width="1.8" {c}/>
<path d="M8 62c11-5 20-5 29 0 9-5 18-5 27 0" stroke-width="1.15" opacity=".68" {c}/>
<path d="M17 55l6-6 6 6M47 55l6-6 6 6" stroke-width="1.0" opacity=".6" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"people / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} display-scale people studies")
