#!/usr/bin/env python3
"""Repair four remaining cropped historical/professional people studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "baker": '''
<path d="M16 61V39h40v22z" stroke-width="2.5" {c}/>
<path d="M21 39c2-8 7-12 15-12s13 4 15 12M23 48h26M23 54h26" stroke-width="1.55" {c}/>
<path d="M29 34c2-5 5-7 7-7s5 2 7 7" stroke-width="1.2" opacity=".68" {c}/>
<circle cx="36" cy="51" r="4" stroke-width="1.4" {c}/>
<path d="M12 64h48" stroke-width="1" opacity=".62" {c}/>
''',
    "maimonides": '''
<circle cx="36" cy="20" r="7" stroke-width="2.3" {c}/>
<path d="M29 27c-5 5-7 12-6 21l-4 13M43 27c5 5 7 12 6 21l4 13M28 39l-9 7M44 39l9 7" stroke-width="2.2" {c}/>
<path d="M23 47h26v13H23zM27 51h18M27 56h13" stroke-width="1.7" {c}/>
<path d="M30 25c3 2 7 2 11 0M32 31c2 1 5 1 8 0" stroke-width="1.05" opacity=".66" {c}/>
''',
    "laozi": '''
<path d="M17 61c2-12 8-18 19-18s17 6 19 18" stroke-width="2.5" {c}/>
<path d="M28 36c-3-5-2-11 2-15 5-4 12-2 15 2 3 5 1 10-2 14-4 4-12 4-15-1z" stroke-width="2.25" {c}/>
<path d="M29 28c3 2 7 2 11 0M32 35c2 1 5 1 8 0" stroke-width="1.1" opacity=".68" {c}/>
<path d="M23 47c7 4 19 4 26 0M27 53c5 3 13 3 18 0" stroke-width="1.25" {c}/>
<path d="M11 61h50" stroke-width="1" opacity=".62" {c}/>
''',
    "orphan": '''
<circle cx="36" cy="22" r="8" stroke-width="2.4" {c}/>
<path d="M28 31c-6 6-8 14-7 23l-4 8M44 31c6 6 8 14 7 23l4 8M28 42l-9 7M44 42l9 7" stroke-width="2.3" {c}/>
<path d="M31 21c3 2 7 2 10 0M32 27c2 1 5 1 8 0" stroke-width="1.1" opacity=".68" {c}/>
<path d="M12 62V45h16v17M12 45l8-7 8 7M17 62V52h6v10" stroke-width="1.8" {c}/>
<path d="M8 64h56" stroke-width="1" opacity=".62" {c}/>
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

print(f"redrew {len(ART)} cropped people studies")
