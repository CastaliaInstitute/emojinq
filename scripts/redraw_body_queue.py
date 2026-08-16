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
<path d="M18 51c3-12 8-20 16-22 8-2 15 2 20 10 2 4 3 8 3 13" stroke-width="2.55" {c}/>
<path d="M27 30c-3-6-1-12 4-16 5-4 12-3 16 2 4 5 3 11-1 15" stroke-width="2.1" {c}/>
<path d="M21 44c6-3 11-3 16 0 5-3 10-3 15 0M29 52c5-2 10-2 15 0" stroke-width="1.25" opacity=".72" {c}/>
<path d="M16 57c8-4 16-4 24 0M45 54l6-3 5 3" stroke-width="1.2" {c}/>
''',
    "push": '''
<path d="M22 18c-5 3-7 9-5 14 2 5 7 7 12 5 5-2 7-8 5-13-2-5-7-8-12-6z" stroke-width="2.2" {c}/>
<path d="M25 36c-7 5-10 13-9 22l-3 5M34 35c7 4 11 10 13 17l3 10M21 45l13-5 11 8" stroke-width="2.35" {c}/>
<path d="M47 41h17M57 35l7 6-7 6M15 63h-7M47 63h10" stroke-width="1.9" {c}/>
<path d="M26 38c3 3 7 5 12 6" stroke-width="1.15" opacity=".68" {c}/>
''',
    "reach": '''
<path d="M27 13c-5 1-8 5-8 10 0 5 3 9 8 10 4 1 8-1 10-5-3 1-5 0-6-2 3-2 4-5 2-8-1-4-3-6-6-5z" stroke-width="2.0" {c}/>
<path d="M24 32c-4 5-6 12-5 20 1 5 0 10-3 13M35 31c5 5 7 11 7 17l8 14M21 38c-3 4-6 7-10 9M35 37c3 2 5 3 8 4" stroke-width="2.15" {c}/>
<path d="M42 40c4-4 8-8 11-12l6-4M54 28l5-2M55 27l3-4M56 29l5 1" stroke-width="1.8" {c}/>
<path d="M17 64H8M49 64h11M27 32c3 2 6 3 9 2M25 47c3 1 6 1 9-1" stroke-width="1.35" opacity=".74" {c}/>
<path d="M20 15c3-3 7-4 11-2M14 39c-2 4-3 8-2 12" stroke-width="1.05" opacity=".62" {c}/>
''',
    "roll": '''
<circle cx="35" cy="36" r="21" stroke-width="2.6" {c}/>
<path d="M25 28c5-7 14-7 20-1M44 43c-5 7-14 7-20 1" stroke-width="2.15" {c}/>
<path d="M20 20l-7-5M52 20l7-5M20 52l-7 5M52 52l7 5" stroke-width="1.65" {c}/>
<path d="M35 9v7M35 56v7" stroke-width="1.15" opacity=".68" {c}/>
''',
    "shake": '''
<path d="M29 15c-4 4-4 10 0 14 4 4 10 4 14 0 3-4 3-10-1-14-3-3-9-3-13 0z" stroke-width="2.2" {c}/>
<path d="M29 31c-6 5-8 12-7 21l-3 10M42 31c6 5 8 12 7 21l3 10M27 40l-10 7M45 40l10 7M24 62h-8M48 62h8" stroke-width="2.3" {c}/>
<path d="M10 21l7 5-7 5M62 21l-7 5 7 5M11 44l7 0M61 44l-7 0" stroke-width="1.7" {c}/>
<path d="M22 33c-3 3-4 7-4 11M50 33c3 3 4 7 4 11" stroke-width="1.08" opacity=".66" {c}/>
''',
    "skin": '''
<path d="M17 58c0-11 5-18 14-20 8-2 15 1 20 8 3 4 4 8 4 14" stroke-width="2.7" {c}/>
<path d="M24 36c-3-6-1-13 4-17 6-5 15-4 20 2 4 5 4 12 0 17" stroke-width="2.35" {c}/>
<path d="M29 23c3 3 9 4 15 1M31 31c3 2 7 2 10 0" stroke-width="1.2" {c}/>
<path d="M20 51c5-3 10-3 15 0M41 48c4-2 8-1 12 2M22 57c4-2 8-2 12 0" stroke-width="1.35" opacity=".74" {c}/>
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
