#!/usr/bin/env python3
"""Replace two overly solid flora silhouettes with readable ink studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "flora"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "apple": '''
<path d="M36 56c-8-8-13-16-11-24 2-8 10-12 17-8 7-4 15 0 17 8 2 8-3 16-11 24-4 4-8 4-12 0z" stroke-width="2.45" {c}/>
<path d="M37 24c-1-7 2-11 8-14M44 13c5-2 9 0 11 4-5 2-9 0-11-4z" stroke-width="1.8" {c}/>
<path d="M29 37c4-3 8-3 12 0M43 48c3-2 5-4 7-7" stroke-width="1.1" opacity=".68" {c}/>
<path d="M18 62h36" stroke-width="1" opacity=".6" {c}/>
''',
    "maple": '''
<path d="M36 61V30M36 43l-15-9M36 49l15-12M36 37l-7-13M36 37l8-13" stroke-width="2.15" {c}/>
<path d="M29 24l-5-5 8 1 4-9 4 9 8-1-5 5 4 7-9-3-6 3z" stroke-width="2.2" {c}/>
<path d="M21 34l-6-5M51 37l7-5M28 50l-8 6M44 52l8 5" stroke-width="1.2" opacity=".7" {c}/>
<path d="M16 63h40" stroke-width="1" opacity=".6" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"flora / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} reviewed flora studies")
