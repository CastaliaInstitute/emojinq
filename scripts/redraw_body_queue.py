#!/usr/bin/env python3
"""Replace repeated placeholder body studies with distinct ink gestures."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "body"
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "pulse": '''
<circle cx="36" cy="19" r="8" stroke-width="2.4" {c}/>
<path d="M27 28c-6 4-8 10-8 19l-3 12M45 28c6 4 8 10 8 19l3 12M28 34l-7 9M44 34l7 9M28 62h-8M44 62h8" stroke-width="2.2" {c}/>
<path d="M18 45h8l3-6 4 13 4-17 4 10h11" stroke-width="1.85" {c}/>
<path d="M14 45h5M55 45h4" stroke-width="1" opacity=".6" {c}/>
''',
    "push": '''
<circle cx="24" cy="20" r="7" stroke-width="2.4" {c}/>
<path d="M20 28c-5 5-7 12-7 21l-3 12M31 28c5 4 8 9 9 16M17 38l10 5 10-6M17 62H7M36 62h10" stroke-width="2.35" {c}/>
<path d="M41 35h19M54 29l7 6-7 6" stroke-width="2.3" {c}/>
<path d="M48 27c4 1 8 3 12 7" stroke-width="1" opacity=".65" {c}/>
''',
    "reach": '''
<circle cx="30" cy="18" r="7" stroke-width="2.35" {c}/>
<path d="M26 26c-5 6-6 13-5 21l-2 14M36 27c4 5 5 10 5 17l8 17M24 35l-8 8M38 35l14-15 7-4" stroke-width="2.3" {c}/>
<path d="M57 16l5 0M57 16l3-4M57 16l3 4M18 61h-8M48 61h10" stroke-width="1.7" {c}/>
<path d="M47 22c3-4 6-6 10-7" stroke-width="1" opacity=".65" {c}/>
''',
    "roll": '''
<circle cx="35" cy="36" r="21" stroke-width="2.6" {c}/>
<path d="M25 28c5-7 14-7 20-1M44 43c-5 7-14 7-20 1" stroke-width="2.15" {c}/>
<path d="M20 20l-7-5M52 20l7-5M20 52l-7 5M52 52l7 5" stroke-width="1.65" {c}/>
<path d="M35 9v7M35 56v7" stroke-width="1.15" opacity=".68" {c}/>
''',
    "shake": '''
<circle cx="36" cy="17" r="7" stroke-width="2.35" {c}/>
<path d="M28 25c-5 5-7 12-6 21l-3 16M44 25c5 5 7 12 6 21l3 16M27 35l-9 9M45 35l9 9M25 62h-8M47 62h8" stroke-width="2.2" {c}/>
<path d="M10 22l7 5-7 5M62 22l-7 5 7 5M12 44l6 0M60 44l-6 0" stroke-width="1.8" {c}/>
<path d="M21 29c-3 3-4 6-4 10M51 29c3 3 4 6 4 10" stroke-width="1" opacity=".66" {c}/>
''',
    "skin": '''
<path d="M17 58c0-11 5-18 14-20 8-2 15 1 20 8 3 4 4 8 4 14" stroke-width="2.7" {c}/>
<path d="M24 36c-3-6-1-13 4-17 6-5 15-4 20 2 4 5 4 12 0 17" stroke-width="2.35" {c}/>
<path d="M29 23c3 3 9 4 15 1M31 31c3 2 7 2 10 0" stroke-width="1.2" {c}/>
<path d="M20 51c5-3 10-3 15 0M41 48c4-2 8-1 12 2M22 57c4-2 8-2 12 0" stroke-width="1.35" opacity=".74" {c}/>
<path d="M14 62h45" stroke-width="1" opacity=".58" {c}/>
''',
}

for name, body in ART.items():
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"body / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} reviewed body studies")
