#!/usr/bin/env python3
"""Expressive sumi-e redraws for people, places, and narrative objects."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "people/hero": """
<circle cx="36" cy="16" r="5" stroke-width="1.7" {i}/>
<path d="M36 22c-6 6-8 14-6 23l-9 13c5-2 10-2 15 0 5-2 10-2 15 0l-9-13c2-9 0-17-6-23z" stroke-width="1.9" {i}/>
<path d="M36 27l3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1z" stroke-width="1.15" {i}/>
<path d="M13 61c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "people/mentor": """
<circle cx="25" cy="19" r="4" stroke-width="1.45" {i}/><circle cx="47" cy="25" r="4" stroke-width="1.45" {i}/>
<path d="M25 24c-6 5-8 12-7 20M47 30c-5 4-6 10-5 16M19 44c5-3 10-3 15 0M42 46c5-3 10-3 15 0" stroke-width="1.7" {i}/>
<path d="M31 30c5-2 9-2 14 1M33 27l4-5 5 4" stroke-width="1.2" {i}/>
<path d="M14 60c14-3 30-3 45 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "people/leader": """
<circle cx="36" cy="15" r="5" stroke-width="1.65" {i}/>
<path d="M36 21c-6 7-8 17-5 29l-9 8h28l-9-8c3-12 1-22-5-29z" stroke-width="1.9" {i}/>
<path d="M25 31c7 3 15 3 22 0M36 50v8M17 18v31M13 22h8" stroke-width="1.25" {i}/>
<path d="M14 61c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "people/care": """
<circle cx="27" cy="20" r="4" stroke-width="1.5" {i}/><circle cx="45" cy="33" r="3.5" stroke-width="1.4" {i}/>
<path d="M27 25c-7 5-9 14-7 23M45 37c-3 5-3 10-1 16M21 48c7-4 13-4 19 0 4 3 8 4 13 2" stroke-width="1.8" {i}/>
<path d="M25 31c7 5 13 8 20 8M39 38c-5 4-8 8-9 14" stroke-width="1.25" {i}/>
<path d="M13 61c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "people/builder": """
<circle cx="29" cy="17" r="4.5" stroke-width="1.55" {i}/>
<path d="M29 22c-6 7-7 15-4 25l-9 11h27l-8-11c3-10 1-18-6-25z" stroke-width="1.85" {i}/>
<path d="M23 31c6 2 11 2 17 0M43 38l12-11M52 25l5 2M52 25l-2 5" stroke-width="1.3" {i}/>
<path d="M12 61c15-3 31-3 48 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "people/babysitter": """
<circle cx="28" cy="18" r="4" stroke-width="1.5" {i}/><circle cx="46" cy="34" r="3" stroke-width="1.35" {i}/>
<path d="M28 23c-7 7-8 16-5 27l-8 9h26l-8-9c3-9 2-18-5-27zM46 38c-4 4-5 9-3 15" stroke-width="1.8" {i}/>
<path d="M25 34c6 4 12 6 18 7M42 48c4 4 8 5 13 4" stroke-width="1.25" {i}/>
<path d="M12 61c15-3 31-3 48 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "locations/academy": """
<path d="M12 55h48M17 55V30h38v25M12 30l24-17 24 17z" stroke-width="1.95" {i}/>
<path d="M24 55V39M36 55V39M48 55V39M20 30h32M27 22l9-7 9 7" stroke-width="1.2" {i}/>
<path d="M36 13v-5M31 10l5-4 5 4M14 61c14-3 30-3 45 0" stroke-width="1.0" {i}/>
""",
    "locations/bakery": """
<path d="M15 57V31h42v26M12 31h48M18 31c1-8 8-13 18-13s17 5 18 13" stroke-width="1.95" {i}/>
<path d="M24 57V43c0-5 4-8 8-8s8 3 8 8v14M46 43c5-2 8 0 9 4" stroke-width="1.3" {i}/>
<path d="M20 22c4-3 8-4 12-4M42 18c4 1 7 3 10 6" stroke-width="1.0" {i}/>
""",
    "objects/writing": """
<path d="M14 54c14-3 29-3 44 0V20c-15-3-30-3-44 0z" stroke-width="1.8" {i}/>
<path d="M23 31c7-2 15-2 24 0M23 39c7-2 15-2 24 0M23 47c5-2 10-2 15 0" stroke-width="1.15" {i}/>
<path d="M42 15l16-9c3-2 5 2 2 4L45 20z" stroke-width="1.45" {i}/>
<path d="M12 60c16-3 32-3 48 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "objects/robot": """
<path d="M23 25c0-6 5-10 13-10s13 4 13 10v22c0 7-6 11-13 11s-13-4-13-11z" stroke-width="1.9" {i}/>
<circle cx="31" cy="32" r="2" stroke-width="1.2" {i}/><circle cx="41" cy="32" r="2" stroke-width="1.2" {i}/>
<path d="M30 42c4 3 8 3 12 0M23 32h-8v14M49 32h8v14M30 58v5M42 58v5M27 63h7M39 63h7M36 15V8M32 8h8" stroke-width="1.35" {i}/>
<path d="M16 55c14-3 28-3 41 0" stroke-width="1.0" opacity=".65" {i}/>
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
print(f"redrew {len(ART)} narrative studies")
