#!/usr/bin/env python3
"""Expressive sumi-e redraws for dense body, object, and plant PUA studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "body/bounce": """
<circle cx="36" cy="17" r="5" stroke-width="1.65" {i}/>
<path d="M36 23c-4 6-5 12-2 17 3 4 8 4 11 0 3-5 1-11-4-17M34 29l-11-8M39 30l12-10M35 40l-9 10M43 40l9 8" stroke-width="1.9" {i}/>
<path d="M24 21l-4-5M51 20l4-5M18 52c9-4 19-4 29 0M51 48l7-4" stroke-width="1.1" {i}/>
<path d="M13 59c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "body/clap": """
<path d="M14 52c5-7 11-14 18-21 2-2 5-1 6 1 1 2 0 4-2 6l-8 8M58 52c-5-7-11-14-18-21-2-2-5-1-6 1-1 2 0 4 2 6l8 8" stroke-width="1.85" {i}/>
<path d="M23 47l7-8M49 47l-7-8M36 18v-7M25 20l-4-6M47 20l4-6M18 31l-7-2M54 31l7-2" stroke-width="1.15" {i}/>
""",
    "body/crawl": """
<path d="M13 48c7-10 16-15 25-13 7 2 10 7 15 10 5 3 9 3 11 0" stroke-width="2.0" {i}/>
<path d="M29 35c-5-5-5-11-1-15 5 0 8 4 8 9 0 4-2 7-7 8M28 39l-10 12M43 43l-3 13M53 47l8 9M20 51l-8 6" stroke-width="1.7" {i}/>
<path d="M14 59c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "body/grab": """
<path d="M13 28c8 2 15 6 21 12l8 8c3 3 7 3 10 0 3-3 2-7-1-10l-9-8c-2-2-2-5 0-6 2-1 4 0 6 2l8 7c2 2 5 2 7 0 1-2 1-4-1-6l-9-9" stroke-width="1.9" {i}/>
<path d="M22 24l11 8M27 20l11 8M32 17l11 8" stroke-width="1.25" {i}/>
<circle cx="52" cy="48" r="5" stroke-width="1.2" {i}/>
""",
    "body/kick": """
<path d="M27 17c-4 8-4 16 1 22 5 5 11 4 15-1 3-4 2-9-1-13" stroke-width="1.9" {i}/>
<path d="M32 39l-8 12M39 38c5 6 10 8 17 7l10-2M24 51l-8 8M55 45l7 5" stroke-width="1.7" {i}/>
<path d="M58 36l8-4M60 41l9 0M58 46l8 4" stroke-width="1.0" {i}/>
""",
    "body/pull": """
<path d="M19 51c7-8 12-16 14-24 2-7 7-11 12-10 4 1 6 5 5 9-1 5-5 9-10 12M28 36l-11 5M38 37l13 5" stroke-width="1.9" {i}/>
<path d="M47 42c8 0 14 3 18 8M61 46l5 4-6 3" stroke-width="1.45" {i}/>
<path d="M12 59c15-3 31-3 48 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "objects/audience": """
<path d="M14 57c1-9 6-14 13-14s12 5 13 14M35 57c1-9 6-14 13-14s12 5 13 14" stroke-width="1.65" {i}/>
<circle cx="27" cy="35" r="4" stroke-width="1.35" {i}/><circle cx="48" cy="35" r="4" stroke-width="1.35" {i}/>
<path d="M24 20h24v12H24zM28 20l8-8 8 8M36 32v7M32 39h8" stroke-width="1.3" {i}/>
<path d="M10 61c17-3 35-3 52 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "objects/bill": """
<path d="M15 14c13-3 27-3 42 0v39c-14-3-28-3-42 0z" stroke-width="1.9" {i}/>
<path d="M23 25c8-2 16-2 25 0M23 33c8-2 16-2 25 0M23 41c6-2 12-2 18 0" stroke-width="1.2" {i}/>
<circle cx="48" cy="47" r="5" stroke-width="1.15" {i}/>
<path d="M15 14l-4 3M57 14l4 3" stroke-width="1.0" {i}/>
""",
    "objects/brush": """
<path d="M15 55c7-8 14-17 20-27l14-16c3-3 8 1 5 5L40 34c-7 8-14 15-22 21z" stroke-width="1.85" {i}/>
<path d="M31 35l10 9M25 42l9 8M20 49l7 6" stroke-width="1.15" {i}/>
<path d="M49 12c4-2 7-1 9 2M53 10l4-4M57 14l5-1" stroke-width="1.0" {i}/>
""",
    "plants/bud": """
<path d="M36 59V31c0-8 4-15 11-20-1 9-4 16-11 20z" stroke-width="1.8" {i}/>
<path d="M36 43c-7-7-13-8-18-4 3 8 9 11 18 10M36 48c7-7 13-8 18-4-3 8-9 11-18 10" stroke-width="1.45" {i}/>
<path d="M36 31c-6-8-5-14 1-20 6 7 5 13-1 20z" fill="#262522" opacity=".16"/>
<path d="M36 31c-6-8-5-14 1-20 6 7 5 13-1 20z" stroke-width="1.35" {i}/>
<path d="M15 61c14-3 29-3 44 0" stroke-width="1.0" opacity=".65" {i}/>
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
print(f"redrew {len(ART)} expressive cross-category studies")
