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
<path d="M18 43c3-10 13-14 27-13 10 1 16 7 17 14 1 8-4 13-14 13H27c-8 0-12-5-9-14z" stroke-width="2.5" {i}/>
<path d="M19 36c-5 1-9-1-10-5 4-1 7-4 10-5 3-4 7-4 10-1l1 6M12 27l-2-4 5 2" stroke-width="2.35" {i}/>
<path d="M27 57l-1 7M46 57l2 7M18 54l-4 4" stroke-width="1.8" {i}/>
<path d="M23 31c2 2 5 2 7 0M51 39c2 2 3 2 5 0M37 35c2-2 4-2 6 0" stroke-width="1.05" {i}/>
""",
    "colony": """
<path d="M9 47c4-4 9-4 13 0M17 44c-2-4-1-7 2-9M19 44c3-4 6-5 9-3M27 51c4-4 9-4 13 0M35 48c-2-4-1-7 2-9M37 48c3-4 6-5 9-3M45 43c4-4 9-4 14 0M53 40c-2-4-1-7 2-9M55 40c3-4 6-5 9-3" stroke-width="1.8" {i}/>
<path d="M8 56c16 3 34 3 56 0" stroke-width="1.05" {i}/>
""",
    "flock": """
<path d="M9 32c5-5 10-5 15 0-5-1-9 0-13 4M27 25c5-5 10-5 15 0-5-1-9 0-13 4M46 34c5-5 10-5 16 0-5-1-10 0-14 4M20 45c5-5 10-5 15 0-5-1-9 0-13 4" stroke-width="2.2" {i}/>
<path d="M8 55c16-4 36-4 56 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "herd": """
<path d="M7 48c1-8 7-12 15-11 6 1 9 5 10 11M27 48c1-8 7-12 15-11 6 1 9 5 10 11M47 48c1-7 6-10 12-9 4 1 6 4 7 9" stroke-width="2.25" {i}/>
<path d="M10 40c-4-2-6-5-5-8 3 1 5 0 7-2M31 40c-4-2-6-5-5-8 3 1 5 0 7-2M51 40c-3-2-4-4-3-7 2 1 4 0 6-1" stroke-width="1.75" {i}/>
<path d="M13 48v11M25 48v11M34 48v11M46 48v11M54 48v11M63 48v11M7 61c18-2 39-2 59 0" stroke-width="1.4" {i}/>
""",
    "lamb": """
<path d="M17 45c-1-8 2-14 8-16 3-3 7-3 10 0 4-2 8-1 11 2 5 2 8 7 8 14 0 9-8 14-20 14-10 0-16-5-17-14z" stroke-width="2.5" {i}/>
<path d="M18 35c-5-1-9-4-9-8 3-1 6-3 9-1 2-3 6-3 8 0l1 6M28 32c3 2 6 2 9 0M39 31c3 2 6 2 8 0" stroke-width="2.05" {i}/>
<path d="M25 57l-1 7M43 57l1 7M52 52l6 3" stroke-width="1.65" {i}/>
<path d="M20 43c3-2 5-2 8 0M38 34c3-2 6-2 9 0" stroke-width="1.1" {i}/>
""",
    "migration": """
<path d="M8 27c5-5 10-5 15 0-5-1-9 0-13 4M23 37c5-5 10-5 15 0-5-1-9 0-13 4M39 26c5-5 10-5 15 0-5-1-9 0-13 4M52 38c4-4 8-4 12 0-4-1-7 0-10 3" stroke-width="2.15" {i}/>
<path d="M8 55c17-3 35-3 57 0" stroke-width="1.0" opacity=".6" {i}/>
""",
    "pack": """
<path d="M7 48c1-10 8-16 17-16 8 0 14 6 15 16M25 48c1-8 7-13 15-13 7 0 12 5 13 13M43 49c1-7 6-11 12-11 5 0 9 4 10 11" stroke-width="2.2" {i}/>
<path d="M9 35l-2-8 7 4 6-5 4 7M28 38l-1-7 6 4 6-4 3 7M46 41l-1-6 5 3 5-3 2 6" stroke-width="1.8" {i}/>
<path d="M13 49l-2 10M27 49l1 10M48 49l-1 10M61 49l2 10M7 62c18-2 38-2 58 0" stroke-width="1.35" {i}/>
""",
    "predator": """
<path d="M8 47c5-9 15-13 27-12 12 1 22 6 28 13-6 5-15 8-27 8H17c-6 0-10-3-9-9z" stroke-width="2.5" {i}/>
<path d="M10 43c-2-5 0-10 5-12l6 4 7-5 4 6M14 35l-3-6 7 3M12 39l-5 1" stroke-width="2.1" {i}/>
<path d="M35 43c4 4 9 5 15 3M21 55l-2 8M48 55l2 8M59 49c4-2 6-5 6-9" stroke-width="1.65" {i}/>
""",
    "prey": """
<path d="M18 51c-4-7-2-15 5-19 8-4 18 0 22 8 3 7 0 13-7 16-7 3-16 1-20-5z" stroke-width="2.35" {i}/>
<path d="M21 39c-3-6-2-15 1-20 4 2 6 6 6 11 3-7 7-10 12-10 1 6-1 11-6 14M45 45c3 2 5 2 7 1" stroke-width="2.05" {i}/>
<path d="M26 53l-2 8M40 53l3 7M17 48l-7 3M44 50l6 3" stroke-width="1.5" {i}/>
""",
    "squirrel": """
<path d="M27 48c-5-8-2-17 6-20 8-3 15 1 17 8 2 7-2 13-9 16-6 3-11 2-14-4z" stroke-width="2.35" {i}/>
<path d="M45 40c-3-12 2-23 11-25 8 5 9 16 3 24-4 5-8 8-13 10" stroke-width="2.4" {i}/>
<path d="M29 30c-1-5 1-8 5-10l4 5M30 49l-4 10M43 51l3 8M22 44l-9 4" stroke-width="1.65" {i}/>
<path d="M19 35c3-2 5-2 7 0" stroke-width="1.05" {i}/>
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
