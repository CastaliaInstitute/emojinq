#!/usr/bin/env python3
"""Repair the next visibly incomplete people PUA studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "art": '''
<path d="M17 56c5-11 12-16 22-16s17 5 21 16" stroke-width="2.6" {c}/>
<circle cx="36" cy="25" r="8" stroke-width="2.4" {c}/>
<path d="M29 48l-5-14 4-2 8 12 14-18 3 2-13 22z" stroke-width="2.1" {c}/>
<path d="M15 60h43M48 29l7-5M52 20l5 0M55 17v6" stroke-width="1.2" opacity=".7" {c}/>
''',
    "artist": '''
<path d="M14 61V20h28v41" stroke-width="2.5" {c}/>
<path d="M19 53l8-12 7 7 5-8M19 25h18M19 31h14" stroke-width="1.4" {c}/>
<circle cx="53" cy="21" r="7" stroke-width="2.2" {c}/>
<path d="M48 29c-4 5-5 11-4 18l-3 14M57 29c4 5 5 11 4 18l3 14M46 40l-8 7M59 40l8-4" stroke-width="2.1" {c}/>
<path d="M40 61h27M10 64h57" stroke-width="1" opacity=".62" {c}/>
''',
    "choice": '''
<circle cx="36" cy="17" r="7" stroke-width="2.35" {c}/>
<path d="M29 25c-6 6-8 14-7 23l-4 13M43 25c6 6 8 14 7 23l4 13M29 36l-9 9M43 36l9 9" stroke-width="2.3" {c}/>
<path d="M36 31v15M36 46L20 57M36 46l16 11" stroke-width="1.8" {c}/>
<path d="M13 57h14M45 57h14" stroke-width="1.0" opacity=".64" {c}/>
''',
    "cooperation": '''
<circle cx="24" cy="22" r="6" stroke-width="2.2" {c}/><circle cx="48" cy="22" r="6" stroke-width="2.2" {c}/>
<path d="M18 29c-5 5-7 12-6 23l-3 10M30 29c4 5 6 11 6 18M42 29c-4 5-6 11-6 18M54 29c5 5 7 12 6 23l3 10" stroke-width="2.15" {c}/>
<path d="M16 41h40M25 41l11 10 11-10M17 62h38" stroke-width="2.0" {c}/>
<path d="M31 20c3-3 7-3 10 0" stroke-width="1.1" opacity=".68" {c}/>
''',
    "temple": '''
<path d="M12 25h48L36 12zM17 29h38M20 29v27M30 29v27M42 29v27M52 29v27M12 56h48M9 62h54" stroke-width="2.35" {c}/>
<path d="M28 56V43c0-7 16-7 16 0v13" stroke-width="1.8" {c}/>
<path d="M24 20h24M18 35h36" stroke-width="1.05" opacity=".68" {c}/>
''',
    "treaty": '''
<path d="M12 24c7-7 14-7 21 0v24c-7-7-14-7-21 0zM60 24c-7-7-14-7-21 0v24c7-7 14-7 21 0z" stroke-width="2.35" {c}/>
<path d="M20 30h10M42 30h10M20 37h10M42 37h10" stroke-width="1.2" opacity=".7" {c}/>
<path d="M36 24v25M30 56c3 3 9 3 12 0" stroke-width="1.45" {c}/>
<path d="M15 53c5 6 12 7 21 3 9 4 16 3 21-3" stroke-width="1.1" opacity=".64" {c}/>
''',
    "trust": '''
<path d="M12 49c7-8 14-11 21-7l7 5c3 2 3 5 1 7-2 2-5 2-8 0l-7-4M60 49c-7-8-14-11-21-7l-7 5c-3 2-3 5-1 7 2 2 5 2 8 0l7-4" stroke-width="2.45" {c}/>
<path d="M36 43c-3-4-8-5-11-1-3 3-2 7 2 9l9 6 9-6c4-2 5-6 2-9-3-4-8-3-11 1z" stroke-width="1.75" {c}/>
<path d="M14 58h18M40 58h18" stroke-width="1.1" opacity=".62" {c}/>
''',
    "vote": '''
<circle cx="23" cy="20" r="7" stroke-width="2.3" {c}/>
<path d="M17 28c-5 5-7 12-6 22l-3 12M29 28c5 5 7 12 6 22l3 12M18 39l-9 7M28 39l9 7" stroke-width="2.2" {c}/>
<path d="M44 31h18v27H44zM47 35h12M47 40h9" stroke-width="2.0" {c}/>
<path d="M36 26l9 8M39 25l6 9" stroke-width="1.7" {c}/>
<path d="M42 62h23" stroke-width="1" opacity=".62" {c}/>
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

print(f"redrew {len(ART)} reviewed people studies")
