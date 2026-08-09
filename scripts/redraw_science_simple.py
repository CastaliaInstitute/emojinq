#!/usr/bin/env python3
"""Simplify the highest-density science PUA studies into traceable concepts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "science"
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "fossil": """
<path d="M14 45c-2-12 4-24 16-30 12-2 24 3 29 14 4 10 0 23-10 29-12 5-28 1-35-13z" stroke-width="2.2" {i}/>
<path d="M36 20c9 0 15 7 15 16 0 10-6 16-15 16-8 0-13-6-13-14 0-7 5-12 11-12 6 0 9 4 9 9 0 4-2 7-6 7-3 0-5-2-5-5" stroke-width="1.9" {i}/>
<path d="M18 51c5 3 10 5 16 5M47 18c4 2 7 5 9 9" stroke-width="1.0" opacity=".7" {i}/>
""",
    "chaos": """
<path d="M10 38c8-18 20-23 28-14 7 8-1 18-10 15-9-3-8-14 3-20M62 34c-8 18-20 23-28 14-7-8 1-18 10-15 9 3 8 14-3 20" stroke-width="2.25" {i}/>
<path d="M15 17l5 5M57 17l-5 5M15 55l5-5M57 55l-5-5" stroke-width="1.35" {i}/>
""",
    "honesty": """
<path d="M10 36c7-10 16-15 26-15s19 5 26 15c-7 10-16 15-26 15S17 46 10 36z" stroke-width="2.25" {i}/>
<circle cx="36" cy="36" r="7" stroke-width="1.65" {i}/>
<path d="M15 27c4-5 9-8 15-9M57 27c-4-5-9-8-15-9" stroke-width="1.1" {i}/>
""",
    "galaxy": """
<path d="M36 14c13 0 22 7 21 16-1 10-15 18-27 17-11-1-16-8-11-14 4-5 12-7 18-4 7 3 7 9 2 12-4 3-9 2-11-1" stroke-width="2.35" {i}/>
<path d="M12 19l1 3M58 49l1 3M48 13l1 3M18 52l1 2" stroke-width="1.2" {i}/>
""",
    "climate": """
<path d="M36 12v15M25 17l11 10 11-10M17 43c8-8 15-8 22 0 6 6 12 6 19 0" stroke-width="1.65" {i}/>
<path d="M10 51c9-4 18-4 27 0 8 4 16 4 25 0M13 59c9-3 17-3 25 0 8 3 15 3 21 0" stroke-width="1.35" {i}/>
<path d="M36 29c-4 5-5 8-5 11 0 4 3 7 6 7s6-3 6-7c0-3-2-6-7-11z" stroke-width="1.35" {i}/>
""",
    "evidence": """
<circle cx="31" cy="32" r="16" stroke-width="2.25" {i}/>
<path d="M43 44l16 16M24 37c4-8 9-12 16-15M24 38c4 3 9 3 14 0" stroke-width="2.1" {i}/>
<path d="M16 56c4-3 8-3 12 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "extinction": """
<path d="M12 53c8-8 17-11 27-9 9 2 16 2 22-5" stroke-width="2.0" {i}/>
<path d="M37 44V22M37 28l-8-7M37 34l9-7M37 39l-7-5" stroke-width="1.8" {i}/>
<path d="M18 57c10-2 21-2 37 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "frontier": """
<path d="M8 53l17-20 9 11 13-23 17 32" stroke-width="2.25" {i}/>
<path d="M8 58c16-4 37-4 57 0M13 47c8 1 16 1 25-1" stroke-width="1.25" {i}/>
<path d="M48 21l4-4 4 4" stroke-width="1.15" {i}/>
""",
    "awe": """
<circle cx="36" cy="26" r="5" stroke-width="1.75" {i}/>
<path d="M36 32v18M36 37l-10-8M36 37l10-8M36 50l-7 10M36 50l7 10" stroke-width="2.0" {i}/>
<path d="M12 17l2 4M24 9l1 5M58 9l-1 5M62 17l-2 4" stroke-width="1.25" {i}/>
<path d="M20 62c10-3 22-3 32 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "cosmos": """
<circle cx="36" cy="36" r="15" stroke-width="1.8" {i}/>
<path d="M18 36c7-10 20-15 32-10 8 4 8 12 2 16-6 4-15 2-18-3-3-5 2-9 7-8" stroke-width="2.0" {i}/>
<path d="M12 18l1 4M58 17l-1 4M12 54l2-2M60 53l-2-2" stroke-width="1.15" {i}/>
""",
    "freeze": """
<path d="M36 12v48M16 24l40 24M16 48l40-24M23 16l13 20 13-20M23 56l13-20 13 20" stroke-width="1.75" {i}/>
<path d="M36 12l-3 5M36 12l3 5M16 24l6 1M16 24l3 5M16 48l6-1M16 48l3-5M56 24l-6 1M56 24l-3 5M56 48l-6-1M56 48l-3-5" stroke-width="1.05" {i}/>
""",
}


def redraw(name: str, body: str) -> None:
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"science / {name}"
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
print(f"redrew {len(ART)} science studies")
