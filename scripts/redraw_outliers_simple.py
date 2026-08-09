#!/usr/bin/env python3
"""Replace a few dense illustrative outliers with traceable silhouettes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "locations/archive": """
<path d="M12 57V25c0-9 9-15 24-15s24 6 24 15v32" stroke-width="2.25" {i}/>
<path d="M8 57h56M17 29h38M17 40h38M17 51h38" stroke-width="1.55" {i}/>
<path d="M22 29v10M31 29v10M40 29v10M49 29v10M22 40v11M31 40v11M40 40v11M49 40v11" stroke-width="1.0" opacity=".72" {i}/>
""",
    "objects/baking": """
<path d="M18 42c3-10 11-15 18-15s15 5 18 15c-9 7-27 7-36 0z" stroke-width="2.2" {i}/>
<path d="M27 28c-1-8 2-12 6-15M36 28c0-8 3-12 7-15M45 28c1-7 5-10 8-12" stroke-width="1.7" {i}/>
<path d="M11 56h25M44 56h18M47 52l11-5M47 52l11 5" stroke-width="1.8" {i}/>
""",
    "objects/board": """
<path d="M10 29l43-10 9 25-43 11z" stroke-width="2.2" {i}/>
<path d="M16 31l39-9M19 39l38-9M22 47l35-9" stroke-width="1.15" {i}/>
<ellipse cx="42" cy="33" rx="4" ry="2" stroke-width="1.0" {i}/>
""",
    "plants/bloom": """
<path d="M36 38c-8-4-15-11-12-18 6-2 11 1 12 8 1-7 6-10 12-8 3 7-4 14-12 18 8-1 15 2 15 8-5 4-11 3-15-2 2 7-1 13-7 14-5-5-4-11 1-15-6 4-13 4-17-1 1-6 8-8 14-4z" stroke-width="1.8" {i}/>
<circle cx="36" cy="38" r="4" stroke-width="1.35" {i}/>
<path d="M36 42v19M36 54c-5-4-9-4-13-2M36 50c5-4 9-4 13-2" stroke-width="1.55" {i}/>
""",
}


def redraw(key: str, body: str) -> None:
    path = ROOT / "assets" / "pua" / f"{key}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    category, name = key.split("/")
    label = f"{category} / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — simplified naturalist study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for key, body in ART.items():
    redraw(key, body)
print(f"redrew {len(ART)} outlier studies")
