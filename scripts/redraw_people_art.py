#!/usr/bin/env python3
"""Replace weak symbolic people glyphs with small sumi-e figure studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "people/astronaut": """
<path d="M36 12c-10 0-16 7-16 17s6 17 16 17 16-7 16-17-6-17-16-17z" stroke-width="1.9" {i}/>
<path d="M25 28c6-4 16-4 22 0M28 34c5 3 11 3 16 0M30 46c-5 5-7 10-6 15M42 46c5 5 7 10 6 15" stroke-width="1.35" {i}/>
<path d="M24 58h24M20 18l-5-4M52 18l5-4M36 12V7" stroke-width="1.1" {i}/>
""",
    "people/farmer": """
<circle cx="34" cy="19" r="5" stroke-width="1.6" {i}/>
<path d="M27 19c2-6 12-8 16-1M34 24c-7 7-8 16-5 26l-9 10h29l-9-10c3-10 1-19-6-26z" stroke-width="1.85" {i}/>
<path d="M28 34c5 2 10 2 15 0M44 39l14-13M54 24l6 2M54 24l-2 6" stroke-width="1.25" {i}/>
<path d="M12 61c15-3 31-3 48 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "people/healer": """
<circle cx="35" cy="17" r="5" stroke-width="1.6" {i}/>
<path d="M35 23c-8 7-10 16-7 26l-9 10h31l-9-10c3-10 1-19-6-26z" stroke-width="1.85" {i}/>
<path d="M27 34c6 3 12 3 18 0M35 40v12M29 46h12" stroke-width="1.25" {i}/>
<path d="M17 56c4-6 9-8 14-5 4 2 6 6 5 10M53 56c-4-6-9-8-14-5" stroke-width="1.2" {i}/>
""",
    "people/nurse": """
<circle cx="35" cy="17" r="5" stroke-width="1.6" {i}/>
<path d="M35 23c-7 7-8 16-5 26l-8 10h27l-8-10c3-10 2-19-6-26z" stroke-width="1.85" {i}/>
<path d="M35 29v10M30 34h10M27 44c5 2 11 2 16 0" stroke-width="1.2" {i}/>
<path d="M15 54c7-5 14-5 20 1 6-6 13-6 21-1" stroke-width="1.25" {i}/>
""",
    "people/prayer": """
<circle cx="36" cy="16" r="5" stroke-width="1.6" {i}/>
<path d="M36 22c-7 6-9 14-6 22 3 7 9 11 16 13-4 2-10 3-16 2-8-1-13-5-16-10 8 1 13-1 16-7 3-6 4-13 6-20z" stroke-width="1.9" {i}/>
<path d="M31 31l5 8 5-8M29 43c5 2 10 2 15 0" stroke-width="1.2" {i}/>
<path d="M36 7V3M30 8l-3-4M42 8l3-4" stroke-width="1.0" {i}/>
""",
    "people/sage": """
<circle cx="36" cy="16" r="5" stroke-width="1.6" {i}/>
<path d="M36 22c-9 7-12 17-9 29l-8 9h34l-8-9c3-12 0-22-9-29z" stroke-width="1.9" {i}/>
<path d="M27 34c6 3 12 3 18 0M28 43c5 2 11 2 16 0M36 51v9M17 22v38M13 26h8" stroke-width="1.25" {i}/>
<path d="M30 11c3-3 8-3 11 0" stroke-width="1.0" {i}/>
""",
    "people/seeker": """
<circle cx="29" cy="18" r="4.5" stroke-width="1.55" {i}/>
<path d="M29 23c-7 7-8 16-5 25l-8 11h29l-8-11c3-9 2-18-8-25z" stroke-width="1.8" {i}/>
<path d="M43 58V27c0-5 3-8 7-8s7 3 7 8v31M46 27h8M49 17V8M45 12h8" stroke-width="1.25" {i}/>
<path d="M24 35c5 2 10 2 15 0M12 61c15-3 31-3 48 0" stroke-width="1.0" {i}/>
""",
}


def redraw(key: str, body: str) -> None:
    path = ROOT / "assets" / "pua" / f"{key}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    category, name = key.split("/", 1)
    label = f"{category} / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — expressive figure study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for key, body in ART.items():
    redraw(key, body)
print(f"redrew {len(ART)} figure studies")
