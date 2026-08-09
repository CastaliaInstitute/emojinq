#!/usr/bin/env python3
"""Redraw selected dense PUA concepts as expressive, traceable brush studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "body/blood": """
<path d="M36 10c-4 10-5 18-2 25 3 7 1 15-6 24" stroke-width="2.05" {i}/>
<path d="M35 31c-8-5-15-5-22 1M34 39c9-5 17-4 24 2M30 51c-6-3-11-2-16 3" stroke-width="1.55" {i}/>
<path d="M13 33c-3 4-3 8 0 11 3-3 3-7 0-11zM56 40c-3 4-3 8 0 11 3-3 3-7 0-11zM15 54c-2 3-2 6 0 8 2-2 2-5 0-8z" stroke-width="1.25" {i}/>
""",
    "body/digestion": """
<path d="M26 13c-3 8 0 12 7 14 7 2 8 7 2 12-8 5-12 11-9 18 2 5 8 6 13 2 5-4 4-10-1-14-5-4-4-8 2-11 7-4 7-11 2-17-3-4-7-6-9-4" stroke-width="2.0" {i}/>
<path d="M20 27c-5 5-7 11-4 17 2 4 2 8-1 12M50 26c5 5 7 11 4 17-2 4-2 8 1 12" stroke-width="1.45" {i}/>
<path d="M18 59c12 3 25 3 37 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "body/muscles": """
<path d="M17 52c4-8 7-15 8-22 1-6 5-11 10-12 4 2 5 7 3 12-2 5-1 10 4 13 5 3 8 8 7 13-1 5-6 7-12 5-7-2-12-7-15-14" stroke-width="2.05" {i}/>
<path d="M31 20c5 4 8 8 8 13M26 31c5 1 9 4 12 8M24 42c5 0 10 2 14 6" stroke-width="1.25" {i}/>
<path d="M13 58c13-4 27-4 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "body/nerves": """
<path d="M36 10c-3 11-3 20 0 28 3 8 2 16-1 24" stroke-width="2.05" {i}/>
<path d="M35 23c-7-5-12-5-18-1M36 30c8-5 14-5 20-1M36 40c-8-5-14-4-20 1M35 49c7-4 13-3 18 2" stroke-width="1.5" {i}/>
<path d="M17 22l-5 4M56 29l5 4M16 42l-5 4M53 52l5 4" stroke-width="1.05" {i}/>
""",
    "objects/beam": """
<path d="M13 24c14 2 29 2 47 0v17c-16 2-31 2-47 0z" stroke-width="2.0" {i}/>
<path d="M18 25v16M27 26v15M43 26v15M52 25v16M13 51c16-3 31-3 47 0" stroke-width="1.25" {i}/>
<path d="M20 30c5-2 9-2 14 0M39 35c4-2 8-2 13 0" stroke-width="1.0" {i}/>
""",
    "objects/brewing": """
<path d="M19 29h31l-3 25c-1 6-6 9-13 9s-12-3-13-9z" stroke-width="2.0" {i}/>
<path d="M50 36h7c7 0 8 11 1 14l-7 2M19 29c5-5 10-7 16-7s11 2 15 7" stroke-width="1.45" {i}/>
<path d="M27 20c-4-5 3-7 0-13M39 20c-4-5 3-7 0-13" stroke-width="1.35" {i}/>
<path d="M16 61c14-3 29-3 43 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "science/design": """
<path d="M16 53c7-11 15-20 25-27 5-4 10-3 14 1-5 8-12 15-22 21-6 4-12 6-17 5z" stroke-width="2.0" {i}/>
<path d="M21 47l25-17M27 51l25-17M51 18l3 4 5-1-3 4" stroke-width="1.2" {i}/>
<path d="M13 59c15-3 31-3 47 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "science/disaster": """
<path d="M9 52c8-8 16-10 25-4 8-6 17-5 29 3" stroke-width="2.0" {i}/>
<path d="M36 12l-5 14h8l-5 14 8-11h-8z" stroke-width="1.7" {i}/>
<path d="M15 42c4-5 8-5 12 0M47 42c4-5 8-5 12 0M13 59c15-3 31-3 47 0" stroke-width="1.15" {i}/>
""",
    "science/feedback": """
<path d="M17 31c3-9 12-14 21-12 9 2 15 10 14 19-1 9-9 15-18 14-7-1-12-5-15-11" stroke-width="2.0" {i}/>
<path d="M17 31l-5 6 8 1M52 38l5-6-8-1" stroke-width="1.45" {i}/>
<path d="M26 34c4-3 8-3 12 0M27 42c5 3 10 3 15 0" stroke-width="1.1" {i}/>
""",
    "science/invention": """
<path d="M36 12c-9 0-15 7-15 15 0 6 3 10 7 13v9h16v-9c4-3 7-7 7-13 0-8-6-15-15-15z" stroke-width="2.0" {i}/>
<path d="M30 49h12M31 54h10M36 17v8M30 29c3-3 8-3 11 0" stroke-width="1.25" {i}/>
<path d="M36 8v-4M19 13l-3-3M53 13l3-3" stroke-width="1.05" {i}/>
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
        f'<title>{label} — expressive brush study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for key, body in ART.items():
    redraw(key, body)
print(f"redrew {len(ART)} expressive art studies")
