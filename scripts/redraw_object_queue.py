#!/usr/bin/env python3
"""Replace the next explicitly reviewed object PUA studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "objects"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "computer": '''
<rect x="14" y="14" width="44" height="31" rx="3" stroke-width="2.8" {c}/>
<path d="M18 19h36v21H18zM29 55h14M36 45v10M24 60h24" stroke-width="2.15" {c}/>
<path d="M23 51h26l-2 4H25z" stroke-width="1.15" opacity=".72" {c}/>
<path d="M22 24c5-3 10-3 15 0M22 30h12M22 35h8" stroke-width="1.1" opacity=".65" {c}/>
''',
    "earn": '''
<path d="M12 53c5-7 10-10 17-10 4 0 7 2 10 4l8-9c2-2 5-2 7 0 2 2 2 5 0 7l-9 11H24" stroke-width="2.8" {c}/>
<path d="M39 47l6 5M25 44l-6-7c-2-2-2-5 0-7 2-2 5-2 7 0l7 7" stroke-width="2.1" {c}/>
<circle cx="51" cy="20" r="9" stroke-width="2.4" {c}/>
<path d="M51 15v10M47 19h8M47 23h8" stroke-width="1.35" {c}/>
<path d="M15 59h42" stroke-width="1" opacity=".6" {c}/>
''',
    "recipe": '''
<path d="M15 18h38v27H15z" stroke-width="2.5" {c}/>
<path d="M20 25h27M20 31h25M20 37h18" stroke-width="1.25" opacity=".72" {c}/>
<path d="M30 51c-6-2-10 0-10 4s5 6 14 6h14c4 0 7-2 7-5 0-4-4-6-10-5" stroke-width="2.3" {c}/>
<path d="M43 48c-2 4-1 8 2 10M44 43c4 3 7 7 8 13" stroke-width="2.0" {c}/>
<path d="M17 15h34" stroke-width="1" opacity=".6" {c}/>
''',
    "trade": '''
<path d="M12 30h22l-5-5M34 30l-5 5M60 42H38l5-5M38 42l5 5" stroke-width="2.45" {c}/>
<path d="M22 24c3-5 7-7 12-7s9 2 12 7M50 48c-3 5-7 7-12 7s-9-2-12-7" stroke-width="1.2" opacity=".7" {c}/>
<path d="M20 40c3-4 7-6 12-6s9 2 12 6c-3 4-7 6-12 6s-9-2-12-6z" stroke-width="2.0" {c}/>
<path d="M27 40h10" stroke-width="1.1" {c}/>
''',
    "traveler": '''
<path d="M31 20c-3-4-2-8 2-10 4-1 7 2 7 6 0 4-3 6-7 6" stroke-width="2.4" {c}/>
<path d="M30 23l-5 14 5 10-6 13M36 24l6 12 7 7M30 33l10 2 7-5" stroke-width="2.5" {c}/>
<path d="M25 27c-4 2-7 5-8 10M39 25l9-5 6 3-7 5" stroke-width="2.1" {c}/>
<path d="M14 63c9-5 18-5 27-2 7 2 13 1 19-2M48 22l5 7" stroke-width="1.15" opacity=".68" {c}/>
<path d="M12 59l8-8 7 8M51 51l7-7 5 7" stroke-width="1.4" opacity=".72" {c}/>
''',
    "wagon": '''
<path d="M17 27h35l5 24H15z" stroke-width="2.7" {c}/>
<path d="M21 27c2-7 7-11 14-11s12 4 14 11M24 34h26M25 41h25" stroke-width="1.45" {c}/>
<circle cx="25" cy="55" r="5" stroke-width="2.2" {c}/><circle cx="49" cy="55" r="5" stroke-width="2.2" {c}/>
<path d="M15 51l-6 7h10M55 51l7 7h-8" stroke-width="2.0" {c}/>
<path d="M11 63h52" stroke-width="1" opacity=".6" {c}/>
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

print(f"redrew {len(ART)} reviewed object studies")
