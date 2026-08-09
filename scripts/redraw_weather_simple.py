#!/usr/bin/env python3
"""Simplify weather and sky PUA studies into traceable sumi-e gestures."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "weather_sky"
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "breeze": """
<path d="M8 28c10-8 19-8 28 0 6 5 13 5 21-1M11 41c8-6 16-6 23 0 6 5 13 5 22 0M22 53c7-4 14-3 21 2" stroke-width="2.2" {i}/>
<path d="M50 19c3-4 7-5 11-4-1 4-4 7-8 8" stroke-width="1.3" {i}/>
""",
    "drizzle": """
<path d="M13 36c-2-7 4-12 11-12 3-7 12-9 17-3 8-3 16 2 16 9 6 1 8 7 5 11H20c-4 0-7-2-7-5z" stroke-width="2.3" {i}/>
<path d="M23 47l-3 7M34 46l-3 8M45 47l-3 7M55 46l-3 8" stroke-width="1.35" {i}/>
""",
    "frost": """
<path d="M36 12v48M15 24l42 24M15 48l42-24M25 15l11 13 11-13M25 57l11-13 11 13M16 36h40" stroke-width="1.65" {i}/>
<path d="M36 12l-3 5M36 12l3 5M15 24l6 1M15 24l3 5M15 48l6-1M15 48l3-5M57 24l-6 1M57 24l-3 5M57 48l-6-1M57 48l-3-5" stroke-width="1.05" {i}/>
""",
    "heat": """
<path d="M17 55c8-4 16-4 24 0 6 3 11 3 16 0" stroke-width="1.45" {i}/>
<path d="M22 43c-4-5 4-7 0-13-3-5 4-7 1-13M36 43c-4-5 4-7 0-13-3-5 4-7 1-13M50 43c-4-5 4-7 0-13-3-5 4-7 1-13" stroke-width="2.15" {i}/>
""",
    "ice": """
<path d="M18 27l14-13 21 7 1 23-18 14-20-8z" stroke-width="2.15" {i}/>
<path d="M18 27l19 7 16-13M37 34v24M27 23l10 11" stroke-width="1.35" {i}/>
<path d="M11 59c8-3 17-3 25 0M45 59c6-2 11-2 16 0" stroke-width="1.05" opacity=".65" {i}/>
""",
    "lightning": """
<path d="M12 35c-2-7 4-12 11-12 3-7 12-9 17-3 8-3 16 2 16 9 6 1 8 7 5 11H18" stroke-width="2.3" {i}/>
<path d="M39 35l-8 13h7l-4 13 13-18h-7l5-8" stroke-width="2.1" {i}/>
""",
    "puddle": """
<path d="M9 48c7-7 18-8 27-5 8 3 17 2 27-3" stroke-width="2.0" {i}/>
<path d="M16 55c8-4 18-4 27-1 8 2 16 1 22-2" stroke-width="1.25" {i}/>
<path d="M40 22c0 5-4 8-4 12 0 3 2 5 5 5s5-2 5-5c0-4-6-7-6-12z" stroke-width="1.45" {i}/>
""",
    "shade": """
<path d="M12 31c7-10 17-15 28-15 10 0 19 5 25 15H12z" stroke-width="2.2" {i}/>
<path d="M18 31v20M29 31v20M40 31v20M51 31v20M12 53h53" stroke-width="1.35" {i}/>
<path d="M36 8v7M21 12l4 5M51 12l-4 5" stroke-width="1.15" {i}/>
""",
    "sky": """
<path d="M9 42c7-7 16-8 24-3 5-9 17-9 22-1 7 0 11 4 11 9H9" stroke-width="2.15" {i}/>
<path d="M20 21c0-5 4-9 9-9s9 4 9 9M29 12v-4M17 12l-3-3M41 12l3-3" stroke-width="1.35" {i}/>
<path d="M15 55c14 3 29 3 43 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "storm": """
<path d="M10 36c-2-7 4-12 11-12 3-7 12-9 17-3 8-3 16 2 16 9 6 1 8 7 5 11H17c-4 0-7-2-7-5z" stroke-width="2.35" {i}/>
<path d="M20 48l-3 8M31 47l-3 9M43 48l-3 8M54 47l-3 9" stroke-width="1.45" {i}/>
<path d="M12 20c8-5 15-5 22 0M42 19c6-4 11-4 17-1" stroke-width="1.55" {i}/>
""",
    "thunder": """
<path d="M10 35c-2-7 4-12 11-12 3-7 12-9 17-3 8-3 16 2 16 9 6 1 8 7 5 11H17c-4 0-7-2-7-5z" stroke-width="2.35" {i}/>
<path d="M39 34l-8 13h7l-4 13 13-18h-7l5-8" stroke-width="2.15" {i}/>
<path d="M14 18l5-4M55 16l5 3" stroke-width="1.25" {i}/>
""",
}


def redraw(name: str, body: str) -> None:
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"weather sky / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — simplified naturalist study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for name, body in ART.items():
    redraw(name, body)
print(f"redrew {len(ART)} weather studies")
