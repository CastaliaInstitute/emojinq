#!/usr/bin/env python3
"""Third expressive sumi-e pass for science and concept PUA plates."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "science/calm": """
<path d="M9 49c9-7 18-7 27 0 8-7 17-7 27 0M10 57c16-3 34-3 52 0" stroke-width="1.65" {i}/>
<circle cx="38" cy="25" r="9" stroke-width="1.35" {i}/>
<path d="M38 11v5M23 16l4 4M53 16l-4 4M17 28h6M59 28h-6" stroke-width="1.0" {i}/>
<path d="M13 61c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "science/conservation": """
<path d="M36 58V31M36 45c-8-8-15-9-21-4 3 9 10 12 21 11M36 41c7-8 14-9 21-4-3 9-10 12-21 11" stroke-width="1.9" {i}/>
<path d="M16 58c-7-3-10-9-8-15 7 0 12 5 13 11M56 58c7-3 10-9 8-15-7 0-12 5-13 11" stroke-width="1.45" {i}/>
<path d="M36 31c-5-7-4-12 1-17 5 6 5 11-1 17z" fill="#262522" opacity=".16"/>
<path d="M36 31c-5-7-4-12 1-17 5 6 5 11-1 17z" stroke-width="1.2" {i}/>
""",
    "science/engineering": """
<path d="M10 53h52M16 53V27l20-13 20 13v26" stroke-width="1.9" {i}/>
<path d="M16 27h40M24 53V31M36 53V25M48 53V31M16 41h40" stroke-width="1.2" {i}/>
<path d="M21 26l15-12 15 12M10 59c17-3 35-3 52 0" stroke-width="1.0" {i}/>
""",
    "science/less": """
<path d="M13 24c9 2 16 6 22 12 6 6 14 10 24 12" stroke-width="1.8" {i}/>
<path d="M13 44c9-2 16-6 22-12 6-6 14-10 24-12" stroke-width="1.35" {i}/>
<path d="M18 58c12-3 25-3 39 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "science/many": """
<path d="M12 48c7-8 14-10 21-5 6-7 13-8 20-3 5-5 10-5 15 0" stroke-width="1.9" {i}/>
<path d="M19 46c2-6 6-9 11-8 3 1 5 4 4 8M37 43c2-6 6-9 11-8 3 1 5 4 4 8M53 45c2-5 5-7 9-6 3 1 4 3 4 6" stroke-width="1.25" {i}/>
<path d="M36 57c-6-6-6-11 0-16 6 5 6 10 0 16z" stroke-width="1.3" {i}/>
""",
    "science/nature": """
<path d="M36 59V27M36 43c-8-9-15-10-21-5 3 9 10 13 21 12M36 39c7-9 14-10 21-5-3 9-10 13-21 12" stroke-width="1.9" {i}/>
<path d="M36 27c-5-8-4-14 1-19 5 6 5 12-1 19zM21 57c-5-6-5-11-1-15 5 4 5 9 1 15zM51 57c5-6 5-11 1-15-5 4-5 9-1 15z" stroke-width="1.25" {i}/>
<path d="M16 61c13-3 28-3 42 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "science/music": """
<path d="M25 19v29c0 6-7 9-11 5-4-4 0-9 6-9 3 0 5 1 5 4M25 20l27-8v27c0 6-7 9-11 5-4-4 0-9 6-9 3 0 5 1 5 4" stroke-width="1.9" {i}/>
<path d="M12 57c8-5 15-5 22 0 7 5 14 5 26-1M40 47c4-4 8-5 13-2" stroke-width="1.15" {i}/>
<path d="M29 25l22-7" stroke-width="1.0" {i}/>
""",
    "science/north": """
<path d="M36 10l5 25-5 27-5-27z" stroke-width="1.5" {i}/>
<path d="M10 36l26-5 26 5-26 5z" stroke-width="1.25" {i}/>
<circle cx="36" cy="36" r="4" stroke-width="1.15" {i}/>
<path d="M36 10v-4M36 66v-4M10 36H6M66 36h-4" stroke-width="1.0" {i}/>
""",
    "science/imagination": """
<path d="M12 47c5-9 12-12 19-8 5-9 14-11 20-4 8-1 13 4 12 11-1 7-8 11-16 9-7 5-17 4-21-2-6 2-12 0-14-6z" stroke-width="1.8" {i}/>
<path d="M26 39c4-3 8-3 12 0M43 34c3-2 6-2 9 0" stroke-width="1.15" {i}/>
<path d="M36 15l2 5M31 18l5-3 5 3M17 20l1 4M55 18l-1 4" stroke-width="1.0" {i}/>
""",
    "science/paradox": """
<path d="M18 25c7-10 18-11 26-3 8 8 5 19-4 24-8 4-17 1-18-7-1-7 6-12 12-9 6 2 7 9 2 13" stroke-width="2.0" {i}/>
<path d="M54 47c-7 10-18 11-26 3-8-8-5-19 4-24 8-4 17-1 18 7 1 7-6 12-12 9-6-2-7-9-2-13" stroke-width="1.45" {i}/>
<path d="M12 58c16-3 32-3 48 0" stroke-width="1.0" opacity=".65" {i}/>
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
