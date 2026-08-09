#!/usr/bin/env python3
"""Repair clearly cropped science/concept PUA studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "science"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "storytelling": '''
<path d="M12 20h22v34H12zM34 20h26v34H34z" stroke-width="2.45" {c}/>
<path d="M18 28h10M18 34h9M18 40h11M40 28h13M40 34h9" stroke-width="1.2" opacity=".72" {c}/>
<path d="M43 45c2-7 8-8 12-4 3 3 1 8-4 9l-7 2z" stroke-width="1.7" {c}/>
<path d="M29 47c-4-4-8-3-10 1-2 4 1 7 6 7l6 0z" stroke-width="1.7" {c}/>
<path d="M15 58h42" stroke-width="1" opacity=".62" {c}/>
''',
    "code": '''
<rect x="12" y="16" width="48" height="40" rx="3" stroke-width="2.55" {c}/>
<path d="M12 25h48M20 34l7 5-7 5M38 34l-7 5 7 5M46 33l-4 13" stroke-width="2.0" {c}/>
<path d="M18 20h2M24 20h2M30 20h2" stroke-width="1.1" opacity=".7" {c}/>
<path d="M19 61h34" stroke-width="1" opacity=".62" {c}/>
''',
    "current": '''
<path d="M10 38c8-10 15-10 23 0s15 10 23 0" stroke-width="2.4" {c}/>
<path d="M10 48c8-10 15-10 23 0s15 10 23 0" stroke-width="1.25" opacity=".72" {c}/>
<path d="M16 27l6 0-3-4M56 27l-6 0 3-4" stroke-width="1.7" {c}/>
<path d="M32 18c3-4 7-4 10 0M32 58c3 4 7 4 10 0" stroke-width="1.1" opacity=".68" {c}/>
''',
    "adaptation": '''
<path d="M36 59V26M36 42L23 32M36 49l15-12" stroke-width="2.1" {c}/>
<path d="M23 32c1-8 8-11 14-7-1 7-7 10-14 7zM51 37c-1-8-8-11-14-7 1 7 7 10 14 7z" stroke-width="2.0" {c}/>
<path d="M16 18c5 2 8 6 8 11-5-1-8-5-8-11zM48 16c5 2 8 6 8 11-5-1-8-5-8-11z" stroke-width="1.6" {c}/>
<path d="M14 62h44" stroke-width="1" opacity=".62" {c}/>
''',
    "balance": '''
<path d="M36 14v43M24 19h24M17 59h38" stroke-width="2.35" {c}/>
<path d="M36 19L19 40M36 19l17 21M12 40h14M46 40h14" stroke-width="1.8" {c}/>
<path d="M10 40c2 7 6 10 10 10s8-3 10-10M42 40c2 7 6 10 10 10s8-3 10-10" stroke-width="2.0" {c}/>
<circle cx="36" cy="14" r="3" stroke-width="1.3" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"science / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} reviewed science studies")
