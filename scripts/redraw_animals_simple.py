#!/usr/bin/env python3
"""Replace the dense animal studies with traceable sumi-e silhouettes.

These are deliberately built from a small shared vocabulary: one outer body
gesture, a head gesture, and only the anatomical marks needed for recognition.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "animals"

INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "calf": """
<path d="M19 43c3-11 13-16 27-13 11 2 18 8 19 16 0 7-6 12-15 13l-18 0c-9-1-15-7-13-16z" stroke-width="2.35" {i}/>
<path d="M22 37c-6 1-11-2-12-6 4-1 8-3 10-6 4-3 8-3 11 0l2 5M17 27l-3-5M27 26l4-5" stroke-width="2.15" {i}/>
<path d="M29 57l-2 7M48 57l2 7M19 53l-5 4M59 47c4-1 6-4 7-8M39 33c-1 7 0 12 4 17M45 51c3-2 6-2 9 0" stroke-width="1.55" {i}/>
<path d="M14 34c2 1 4 1 6 0M28 36c4 3 8 3 12 1M48 38c3 2 6 2 8 0" stroke-width="1.05" {i}/>
""",
    "colony": """
<path d="M12 48c1-6 6-10 11-8 4 1 6 5 5 9-1 5-6 7-11 5-4-1-6-3-5-6zM32 44c1-6 6-10 11-8 4 1 6 5 5 9-1 5-6 7-11 5-4-1-6-3-5-6zM51 50c1-5 5-8 9-7 4 1 5 4 4 7-1 4-5 6-9 5-3-1-5-3-4-5z" stroke-width="1.65" {i}/>
<path d="M18 40l-2-6M22 40l3-6M38 36l-2-6M43 36l4-5M56 43l-1-6M60 44l4-4M11 55c16 4 35 4 54 0" stroke-width="1.15" {i}/>
""",
    "flock": """
<path d="M9 34c6-8 14-9 22-3-7-1-12 1-16 6M28 24c7-7 15-6 21 1-7-2-12 0-16 5M47 38c6-7 13-7 19-1-6-1-11 1-15 5M20 48c5-6 11-6 17-1-6-1-10 1-13 5" stroke-width="1.85" {i}/>
<path d="M14 32c4 0 8 2 11 6M34 23c4 1 8 4 11 8M53 37c4 0 7 2 10 5" stroke-width="1.1" {i}/>
<path d="M8 58c17-3 36-3 56 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "herd": """
<path d="M7 48c2-9 9-14 18-12 6 1 10 6 10 12M29 48c2-8 8-12 16-11 7 1 10 5 11 11M49 49c2-7 7-10 13-8 4 1 6 4 7 8" stroke-width="2.15" {i}/>
<path d="M10 38c-4-2-6-5-5-9 3 2 6 1 8-2 3 2 4 5 2 8M33 38c-4-2-6-5-5-8 3 1 5 0 7-2 2 3 2 6-2 10" stroke-width="1.65" {i}/>
<path d="M13 48l-1 11M25 48l1 11M36 48v11M47 48l1 11M55 49v10M64 49l1 10M7 61c18-2 39-2 59 0" stroke-width="1.3" {i}/>
<path d="M17 43c3-2 6-2 9 0M39 42c3-2 6-2 9 0M58 43c2-1 4-1 6 0" stroke-width="1.0" {i}/>
""",
    "lamb": """
<path d="M17 45c-1-9 3-15 9-17 4-3 8-2 11 1 4-2 8-1 11 3 5 2 8 8 7 15-1 9-9 14-21 14-10 0-16-5-17-16z" stroke-width="2.3" {i}/>
<path d="M19 36c-5-1-9-4-9-8 3-1 6-3 9-1 2-3 6-3 8 0l1 6M29 31c3 3 6 3 9 0M40 32c3 2 6 2 8 0" stroke-width="1.95" {i}/>
<path d="M22 40c3-3 6-3 9 0M35 36c3-3 7-3 10 0M47 39c3-2 6-2 8 1M25 57l-1 7M43 57l1 7M52 52l6 3" stroke-width="1.15" {i}/>
""",
    "migration": """
<path d="M8 32c8-9 17-9 27-2-9-1-16 1-22 7M29 24c8-8 17-7 26 0-9-2-16 0-22 6M43 40c7-7 15-7 22-1-8-1-14 1-19 6" stroke-width="1.95" {i}/>
<path d="M14 31c5 0 10 2 15 6M35 24c5 1 10 4 14 8M49 39c4 0 8 2 11 5" stroke-width="1.1" {i}/>
<path d="M8 58c17-3 35-3 57 0" stroke-width="1.0" opacity=".6" {i}/>
""",
    "pack": """
<path d="M8 44c1-8 8-13 16-11 5 1 8 4 10 8M28 47c1-8 7-12 15-10 5 1 8 4 10 8M48 49c1-7 6-10 12-8 4 1 6 4 7 8" stroke-width="2.1" {i}/>
<path d="M10 34l-1-8 7 5 5-6 3 8M31 37l-1-8 7 4 5-5 3 8M51 40l-1-7 6 4 5-4 2 7" stroke-width="1.7" {i}/>
<path d="M13 45l-2 10M25 45l1 10M35 48l-1 9M46 48l1 9M55 50l-1 7M64 50l2 7M7 61c18-2 38-2 58 0" stroke-width="1.25" {i}/>
""",
    "predator": """
<path d="M9 48c5-10 15-15 28-13 12 1 22 6 27 13-7 6-16 8-28 8H17c-6 0-10-3-8-8z" stroke-width="2.35" {i}/>
<path d="M10 43c-2-6 0-11 5-14l6 5 7-6 5 7M15 35l-4-7 8 3M13 40l-6 1" stroke-width="2.0" {i}/>
<path d="M37 43c4 4 10 5 16 2M22 55l-3 8M49 55l2 8M59 49c5-2 7-6 6-11M19 49c4-3 7-3 11-1M34 52c4-2 8-2 12 0" stroke-width="1.45" {i}/>
<path d="M27 38c3-2 6-2 9 0M44 37c3-2 6-2 9 0" stroke-width="1.0" {i}/>
""",
    "prey": """
<path d="M22 50c-5-8-2-17 7-20 9-3 18 1 22 9 3 7 0 14-7 17-9 3-18 1-22-6z" stroke-width="2.25" {i}/>
<path d="M25 39c-4-7-4-16-1-22 5 2 8 8 8 14 3-7 8-11 13-10 0 7-3 13-8 16M48 45c3 2 5 2 8 1" stroke-width="1.95" {i}/>
<path d="M29 53l-2 8M43 53l3 7M20 48l-7 3M46 51l6 3M31 43c3-2 6-2 9 0M29 47c3 2 6 2 9 0" stroke-width="1.3" {i}/>
""",
    "squirrel": """
<path d="M27 49c-5-8-2-17 6-21 8-3 16 1 18 8 2 7-2 14-9 17-7 3-12 1-15-4z" stroke-width="2.25" {i}/>
<path d="M45 41c-3-13 2-25 11-27 8 5 10 17 4 26-4 6-9 9-14 11" stroke-width="2.25" {i}/>
<path d="M29 31c-1-5 1-9 5-11l4 5M30 50l-4 10M44 52l3 8M22 45l-9 4M35 37c3-2 6-2 9 0" stroke-width="1.5" {i}/>
""",
}


def redraw(name: str, body: str) -> None:
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"animals / {name}"
    content = body.format(i=INK)
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — simplified naturalist study</title>{content}</svg>\n'
    )
    path.write_text(svg)


for name, body in ART.items():
    redraw(name, body)
print(f"redrew {len(ART)} animal studies")
