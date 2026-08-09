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
    "mentor": """
<circle cx="25" cy="24" r="5" stroke-width="1.75" {i}/><circle cx="47" cy="30" r="5" stroke-width="1.75" {i}/>
<path d="M16 53c1-10 6-16 13-16s11 6 12 16M39 55c1-8 5-13 11-13 5 0 8 4 9 11" stroke-width="2.0" {i}/>
<path d="M31 25c5-4 9-4 14 0M34 20l5-5 5 5" stroke-width="1.35" {i}/>
""",
    "legend": """
<path d="M14 20c10-5 21-5 32 0l12-5v34l-12 5c-11-5-22-5-32 0z" stroke-width="2.1" {i}/>
<path d="M46 20v34M26 26c5-2 10-2 15 0M25 34c5-2 10-2 15 0" stroke-width="1.25" {i}/>
<path d="M20 47l4-5 4 5 5-2" stroke-width="1.1" {i}/>
""",
    "flow": """
<path d="M9 28c8-9 17-9 24 0 7 9 15 9 29-1M9 43c8-9 17-9 24 0 7 9 15 9 29-1M17 57c7-5 14-5 21 0" stroke-width="2.15" {i}/>
<path d="M48 18c4-3 8-3 13 0" stroke-width="1.15" {i}/>
""",
    "contradiction": """
<path d="M21 54c-5-8-3-16 3-22 4-4 5-10 3-16 8 6 10 13 6 20-3 6-2 12 3 18" stroke-width="2.15" {i}/>
<path d="M49 15v38M34 23l30 18M34 41l30-18M40 18l9 18 9-18M40 48l9-18 9 18" stroke-width="1.35" {i}/>
""",
    "cause": """
<path d="M36 13c-5 5-7 9-7 13 0 5 3 8 7 8s7-3 7-8c0-4-2-8-7-13z" stroke-width="1.8" {i}/>
<path d="M36 36c-10 4-16 9-16 15M36 36c10 4 16 9 16 15M12 56c8-3 16-3 24 0 8-3 16-3 24 0" stroke-width="1.55" {i}/>
""",
    "divide": """
<path d="M36 12v48" stroke-width="2.0" {i}/>
<path d="M10 23c8 4 16 4 24 0M10 49c8-4 16-4 24 0M62 23c-8 4-16 4-24 0M62 49c-8-4-16-4-24 0" stroke-width="1.4" {i}/>
<path d="M13 59c7-2 14-2 21 0M59 59c-7-2-14-2-21 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "mist": """
<path d="M10 33c7-7 14-7 21 0 6-7 14-7 21 0 5-4 10-4 14 0M10 45c8-4 16-4 24 0 8-4 16-4 28 0M16 56c7-3 14-3 21 0 7-3 14-3 20 0" stroke-width="1.65" {i}/>
""",
    "history": """
<circle cx="30" cy="35" r="18" stroke-width="2.1" {i}/>
<path d="M30 22v14l8 6M14 21l-5 5M9 26h7" stroke-width="1.55" {i}/>
<path d="M47 47c6 2 9 6 10 11M54 52l4 1-1 4" stroke-width="1.35" {i}/>
""",
    "knowledge": """
<path d="M12 22c8-3 16-2 24 4 8-6 16-7 24-4v35c-8-3-16-2-24 4-8-6-16-7-24-4z" stroke-width="2.1" {i}/>
<path d="M36 26v35M19 31c5-2 10-1 15 2M53 31c-5-2-10-1-15 2" stroke-width="1.25" {i}/>
<path d="M54 15l1 4M50 18l4 1M58 18l-3 1" stroke-width="1.15" {i}/>
""",
    "future": """
<path d="M36 59V33M36 42c-7-8-13-9-19-6 2 8 8 12 19 11M36 38c7-8 13-9 19-6-2 8-8 12-19 11" stroke-width="2.0" {i}/>
<path d="M10 59c9-3 18-3 26 0 8-3 17-3 26 0" stroke-width="1.15" {i}/>
<path d="M36 19l1 4M31 22l5-3 5 3" stroke-width="1.1" {i}/>
""",
    "fraction": """
<circle cx="36" cy="36" r="22" stroke-width="2.1" {i}/>
<path d="M36 14v44M14 36h44" stroke-width="1.45" {i}/>
<path d="M22 22l5 5M50 22l-5 5M22 50l5-5M50 50l-5-5" stroke-width="1.05" {i}/>
""",
    "because": """
<circle cx="22" cy="35" r="10" stroke-width="1.9" {i}/><circle cx="50" cy="35" r="10" stroke-width="1.9" {i}/>
<path d="M32 35h16M22 31l4 4-4 4M50 31l-4 4 4 4" stroke-width="1.35" {i}/>
<path d="M15 18c5-3 10-3 15 0M42 18c5-3 10-3 15 0" stroke-width="1.0" opacity=".7" {i}/>
""",
    "hypothesis": """
<path d="M20 55V25c0-6 6-10 16-10s16 4 16 10v30c-10 4-22 4-32 0z" stroke-width="2.0" {i}/>
<path d="M20 25c10 4 22 4 32 0M29 36c2-5 9-7 12-3 4 5-2 7-5 10-2 2-2 4-2 6M35 52v1" stroke-width="1.45" {i}/>
""",
    "idea": """
<path d="M36 16c-10 0-17 8-17 17 0 6 3 10 7 14v7h20v-7c4-4 7-8 7-14 0-9-7-17-17-17z" stroke-width="2.1" {i}/>
<path d="M30 54h12M31 59h10M36 10v-4M20 12l-3-3M52 12l3-3M14 28H9M58 28h5" stroke-width="1.3" {i}/>
""",
    "explanation": """
<path d="M12 20h48v31H33L22 59v-8H12z" stroke-width="2.05" {i}/>
<path d="M23 30h26M23 38h20M23 46h12" stroke-width="1.25" {i}/>
<path d="M51 13l3 4 5-1-3 4 2 4-5-2-3 3 1-5-4-3 5-1z" stroke-width="1.15" {i}/>
""",
    "exploration": """
<circle cx="30" cy="31" r="16" stroke-width="2.0" {i}/>
<path d="M30 18l4 13-10 8 4-13zM46 47c6 3 9 7 10 12M56 59c-5-1-10 0-15 3" stroke-width="1.5" {i}/>
<path d="M30 12v-4M14 31h-4M30 50v4M46 31h4" stroke-width="1.1" {i}/>
""",
    "art": """
<path d="M14 52c3-11 10-21 19-29 7-6 14-5 18 0 4 6-1 13-8 18-9 7-19 10-29 11z" stroke-width="2.0" {i}/>
<path d="M19 45l11 7M25 37l12 8M33 29l10 7" stroke-width="1.15" {i}/>
<circle cx="54" cy="20" r="3" stroke-width="1.15" {i}/>
""",
    "courage": """
<path d="M36 58V32M36 38l-10-8M36 38l10-8M36 51l-7 9M36 51l7 9" stroke-width="2.0" {i}/>
<circle cx="36" cy="25" r="6" stroke-width="1.8" {i}/>
<path d="M10 28c7-5 13-5 19 0M53 28c4-3 8-3 10 0M9 47c8-4 15-4 22 0M48 47c6-3 11-3 16 0" stroke-width="1.35" {i}/>
""",
    "fall": """
<path d="M36 13c-5 7-7 13-4 17 3 4 9 3 11-2 2-4-1-9-7-15z" stroke-width="1.8" {i}/>
<path d="M38 29c-5 8-9 14-13 19M31 43l-6 5M31 43l1 7" stroke-width="1.45" {i}/>
<path d="M11 58c9-3 18-3 26 0 8-3 17-3 25 0" stroke-width="1.15" {i}/>
""",
    "path": """
<path d="M12 56c8-8 16-14 18-22 2-7-2-12-8-15M60 56c-8-8-16-14-18-22-2-7 2-12 8-15" stroke-width="2.15" {i}/>
<path d="M18 56c10-3 26-3 36 0M24 45c7-2 17-2 24 0M30 34c4-1 8-1 12 0" stroke-width="1.25" {i}/>
<path d="M12 60c16-2 32-2 48 0" stroke-width="1.0" opacity=".65" {i}/>
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
