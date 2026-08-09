#!/usr/bin/env python3
"""Strengthen low-ink people studies that fail at small glyph sizes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "humility": '''
<circle cx="36" cy="24" r="7" stroke-width="2.35" {c}/>
<path d="M29 30c-6 5-8 12-7 21l-4 11M43 30c6 5 8 12 7 21l4 11M28 40l-9 6M44 40l9 6" stroke-width="2.2" {c}/>
<path d="M31 23c3 2 7 2 10 0M32 28c2 1 5 1 8 0" stroke-width="1.15" opacity=".68" {c}/>
<path d="M15 62h42" stroke-width="1" opacity=".6" {c}/>
''',
    "trade": '''
<path d="M10 34h21l-5-5M31 34l-5 5M62 46H41l5-5M41 46l5 5" stroke-width="2.35" {c}/>
<path d="M20 25c3-6 8-9 14-9s11 3 14 9M24 54c3 6 8 9 14 9s11-3 14-9" stroke-width="1.25" opacity=".7" {c}/>
<path d="M25 40h22v12H25z" stroke-width="2.0" {c}/>
<path d="M29 40c1-5 4-7 7-7s6 2 7 7" stroke-width="1.6" {c}/>
''',
    "trickster": '''
<path d="M17 59c2-10 8-16 17-16s15 6 18 16" stroke-width="2.55" {c}/>
<path d="M27 35c-3-4-2-10 2-13 4-4 11-3 14 1 3 4 2 10-1 13-4 4-12 4-15-1z" stroke-width="2.35" {c}/>
<path d="M22 24l8-8 6 6 8-8 6 10-7 4M30 31c2-2 4-2 6 0 2-2 4-2 6 0" stroke-width="1.85" {c}/>
<path d="M14 63h44" stroke-width="1" opacity=".62" {c}/>
''',
    "hildegard": '''
<path d="M17 61c1-10 7-17 16-17s15 7 16 17" stroke-width="2.45" {c}/>
<path d="M27 35c-3-5-2-11 2-15 5-4 12-2 15 2 3 5 1 10-2 14-4 4-12 4-15-1z" stroke-width="2.2" {c}/>
<path d="M28 28c3 2 7 2 11 0M31 35c2 1 5 1 7 0" stroke-width="1.1" opacity=".68" {c}/>
<path d="M22 48h28v13H22zM28 53h16M28 57h12" stroke-width="1.65" {c}/>
<path d="M52 39c6-7 10-8 12-4-3 2-6 5-8 10" stroke-width="1.4" {c}/>
''',
    "value": '''
<circle cx="36" cy="20" r="7" stroke-width="2.3" {c}/>
<path d="M29 27c-5 5-7 12-6 21l-4 13M43 27c5 5 7 12 6 21l4 13M28 39l-9 7M44 39l9 7" stroke-width="2.2" {c}/>
<path d="M28 48c3-4 7-6 12-6s9 2 12 6" stroke-width="1.35" opacity=".7" {c}/>
<circle cx="36" cy="52" r="6" stroke-width="1.8" {c}/>
<path d="M36 48v8M33 52h6" stroke-width="1.1" {c}/>
''',
    "tribe": '''
<circle cx="24" cy="22" r="6" stroke-width="2.1" {c}/><circle cx="48" cy="22" r="6" stroke-width="2.1" {c}/><circle cx="36" cy="17" r="7" stroke-width="2.3" {c}/>
<path d="M18 29c-4 5-5 11-4 20l-3 12M30 29c4 4 5 10 5 16M42 29c-4 4-5 10-5 16M54 29c4 5 5 11 4 20l3 12M29 25c-4 5-5 10-4 17M43 25c4 5 5 10 4 17" stroke-width="2.0" {c}/>
<path d="M21 40h30M16 62h40" stroke-width="1.65" {c}/>
<path d="M32 18c2 1 5 1 8 0" stroke-width="1.0" opacity=".65" {c}/>
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

print(f"redrew {len(ART)} low-ink people studies")
