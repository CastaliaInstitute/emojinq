#!/usr/bin/env python3
"""Replace selected dense cross-category PUA studies with traceable sumi-e marks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "objects/axle": """
<path d="M12 36h48M20 27v18M52 27v18" stroke-width="2.0" {i}/>
<circle cx="20" cy="36" r="10" stroke-width="1.8" {i}/><circle cx="52" cy="36" r="10" stroke-width="1.8" {i}/>
<path d="M16 31l8 10M48 31l8 10" stroke-width="1.15" {i}/>
""",
    "body/breath": """
<path d="M25 18c-8 4-10 12-5 18 4 5 10 6 15 1M47 18c8 4 10 12 5 18-4 5-10 6-15 1" stroke-width="1.9" {i}/>
<path d="M36 37c-5 6-9 10-9 15 0 5 4 8 9 8s9-3 9-8c0-5-4-9-9-15z" stroke-width="1.8" {i}/>
<path d="M18 26c-4 3-6 7-6 12M54 26c4 3 6 7 6 12" stroke-width="1.15" {i}/>
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
        f'<title>{label} — simplified naturalist study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for key, body in ART.items():
    redraw(key, body)
print(f"redrew {len(ART)} cross-category studies")
