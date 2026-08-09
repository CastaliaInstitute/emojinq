#!/usr/bin/env python3
"""Replace a small, explicitly reviewed PUA queue with complete vector studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"

COMMON = (
    'fill="none" stroke="#262522" stroke-linecap="round" '
    'stroke-linejoin="round"'
)

ART = {
    "astronaut": """
<path d="M24 28c-3-3-3-9 0-13 4-5 12-5 16 0 3 4 3 10 0 13" stroke-width="2.7" {c}/>
<path d="M27 22c3 2 8 2 11 0M29 15c2 2 5 2 7 0" stroke-width="1.25" {c}/>
<path d="M23 29c-3 3-4 7-4 13l-3 8c-1 3 1 5 4 5h32c3 0 5-2 4-5l-3-8c0-6-1-10-4-13-6 4-20 4-26 0z" stroke-width="2.9" {c}/>
<path d="M24 34l-7 8-5 7M48 34l7 8 5 7M28 54l-3 9M44 54l3 9" stroke-width="2.25" {c}/>
<path d="M36 42v12M31 47h10M57 24c7 4 10 9 11 16" stroke-width="1.1" opacity=".72" {c}/>
""",
    "conflict": """
<path d="M31 19c-4-4-10-4-14 0-3 3-3 8 0 11l5 4-5 5c-3 3-3 8 0 11 4 4 10 4 14 0l5-5" stroke-width="2.6" {c}/>
<path d="M41 19c4-4 10-4 14 0 3 3 3 8 0 11l-5 4 5 5c3 3 3 8 0 11-4 4-10 4-14 0l-5-5" stroke-width="2.6" {c}/>
<path d="M34 30l4 4-4 4 4 4-4 4M38 34l4-4M38 42l4 4" stroke-width="2.15" {c}/>
<path d="M27 24c2 1 4 1 6 0M45 24c-2 1-4 1-6 0" stroke-width="1.15" opacity=".75" {c}/>
""",
    "constitution": """
<path d="M22 14c-3 2-4 5-4 9v32c0 3 2 5 5 5h26c3 0 5-2 5-5V23c0-4-1-7-4-9" stroke-width="2.8" {c}/>
<path d="M24 14h24l-4 8H28z" stroke-width="2.2" {c}/>
<path d="M28 31h16M28 38h16M28 45h11" stroke-width="1.6" {c}/>
<path d="M49 43c4-5 8-8 11-7 2 1 1 4-2 7l-11 11-6 2 2-6z" stroke-width="2.1" {c}/>
<path d="M47 55l-4-4" stroke-width="1.1" opacity=".7" {c}/>
""",
    "invite": """
<path d="M18 58c1-10 6-16 14-16s13 6 14 16" stroke-width="2.7" {c}/>
<circle cx="32" cy="27" r="8" stroke-width="2.5" {c}/>
<path d="M28 28c2 2 5 2 8 0M53 20v27M53 20c5 0 8 4 8 9s-3 9-8 9" stroke-width="2.25" {c}/>
<path d="M47 35h-9M41 30l-6 5 6 5" stroke-width="2.0" {c}/>
<path d="M16 63h45" stroke-width="1.0" opacity=".6" {c}/>
""",
    "language": """
<path d="M12 32c0-9 7-15 16-15 5 0 9 2 12 5" stroke-width="2.6" {c}/>
<path d="M60 32c0-9-7-15-16-15-5 0-9 2-12 5" stroke-width="2.6" {c}/>
<path d="M17 32c0 8 5 14 13 15M55 32c0 8-5 14-13 15" stroke-width="2.0" {c}/>
<path d="M21 38c3 1 5 1 8 0M51 38c-3 1-5 1-8 0" stroke-width="1.2" {c}/>
<path d="M20 57c4-4 8-5 12-5s8 1 12 5M35 52v10" stroke-width="2.1" {c}/>
<path d="M38 27c4-2 8-2 12 0M45 23v8" stroke-width="1.15" opacity=".7" {c}/>
""",
    "name": """
<path d="M18 60c1-11 7-18 17-18s16 7 18 18" stroke-width="2.8" {c}/>
<path d="M27 30c-2-4-1-10 3-13 4-4 11-3 14 1 3 4 2 10-1 13-4 4-12 4-16-1z" stroke-width="2.5" {c}/>
<path d="M30 31c2 2 5 3 8 2M29 23c3 1 7 1 11-1" stroke-width="1.25" {c}/>
<path d="M43 49h16l-3 12H40z" stroke-width="2.15" {c}/>
<path d="M44 53h10M43 57h9" stroke-width="1.25" {c}/>
<path d="M15 63h44" stroke-width="1.0" opacity=".6" {c}/>
""",
}


def redraw(name: str, body: str) -> None:
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"people / {name}"
    content = body.format(c=COMMON)
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{content}</svg>\n'
    )
    path.write_text(svg)


for name, body in ART.items():
    redraw(name, body)
print(f"redrew {len(ART)} reviewed PUA studies")
