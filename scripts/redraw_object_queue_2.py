#!/usr/bin/env python3
"""Repair two remaining cropped object/concept studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "objects"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "pot": '''
<path d="M20 23h32l-3 30c-1 7-6 10-13 10s-12-3-13-10z" stroke-width="2.6" {c}/>
<path d="M20 23c0-5 7-8 16-8s16 3 16 8-7 8-16 8-16-3-16-8zM24 37c7 3 17 3 24 0M25 46c6 2 16 2 22 0" stroke-width="1.55" {c}/>
<path d="M27 15c2-4 5-6 9-6s7 2 9 6" stroke-width="1.25" opacity=".68" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "voice": '''
<path d="M18 51c-4-5-5-12-2-18 3-7 9-11 16-11 9 0 16 7 16 16 0 8-6 14-14 16l-6 8-1-9c-4 0-7-1-9-2z" stroke-width="2.45" {c}/>
<path d="M29 31c4 3 8 3 12 0M30 39c3 2 7 2 10 0" stroke-width="1.25" opacity=".7" {c}/>
<path d="M52 30c5 4 5 10 0 14M58 25c8 7 8 17 0 24M64 20c10 10 10 25 0 35" stroke-width="1.75" {c}/>
<path d="M14 64h49" stroke-width="1" opacity=".6" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"objects / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} cropped object studies")
