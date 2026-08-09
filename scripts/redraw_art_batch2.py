#!/usr/bin/env python3
"""Second expressive sumi-e pass for dense conceptual PUA studies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "science/archive": """
<path d="M18 18c9-4 18-3 27 1l10-6v37l-10 6c-9-4-18-4-27 0z" fill="#262522" opacity=".16"/>
<path d="M18 18c9-3 18-2 27 1l10-6v37l-10 6c-9-4-18-4-27 0z" stroke-width="2.0" {i}/>
<path d="M45 19v37M23 27c6-2 12-1 18 2M23 36c6-2 12-1 18 2M23 45c5-2 10-1 16 1" stroke-width="1.15" {i}/>
<path d="M18 18l-6 4c-2 2-1 4 2 4l6-2M55 13l5 2c3 2 2 4-1 5l-5-1" stroke-width="1.3" {i}/>
""",
    "science/border": """
<path d="M12 55V18c12-3 36-3 48 0v37" stroke-width="1.9" {i}/>
<path d="M12 18h48M12 55c12 3 36 3 48 0M22 18v12M34 18v8M46 18v12M22 55V43M34 55v-8M46 55V43" stroke-width="1.2" {i}/>
<path d="M12 35h13M47 35h13" stroke-width="1.55" {i}/>
<path d="M18 22c4 1 7 1 11 0M40 22c4 1 7 1 11 0" stroke-width=".9" {i}/>
""",
    "science/capital": """
<path d="M15 57h42M19 57V37h34v20L36 19z" fill="#262522" opacity=".12"/>
<path d="M14 57h44M19 57V37h34v20M15 37l21-18 21 18z" stroke-width="2.0" {i}/>
<path d="M24 57V44M36 57V42M48 57V44M21 37h30M22 30l14-11 14 11" stroke-width="1.2" {i}/>
<path d="M36 9l3 6 7 1-5 4 1 7-6-3-6 3 1-7-5-4 7-1z" stroke-width="1.15" {i}/>
<path d="M19 57c9-2 19-2 29 0" stroke-width=".9" {i}/>
""",
    "science/conclusion": """
<path d="M9 54c8-14 17-20 26-15 8 5 13 1 27-13-7 16-14 26-24 27-9 1-17-2-29 1z" fill="#262522" opacity=".14"/>
<path d="M9 54c8-14 17-20 26-15 8 5 13 1 27-13" stroke-width="2.05" {i}/>
<path d="M55 27l7-1-4 7M46 40c5-1 9-3 13-7" stroke-width="1.35" {i}/>
<circle cx="62" cy="22" r="3" stroke-width="1.15" {i}/>
<path d="M15 47c4-3 8-3 12-1M22 40c4-2 7-2 10 0" stroke-width=".95" {i}/>
<path d="M11 61c15-3 31-3 49 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "science/diversity": """
<path d="M36 58V28M36 43c-8-9-15-10-21-5 3 9 10 13 21 12M36 39c7-9 14-10 21-5-3 9-10 13-21 12" stroke-width="1.9" {i}/>
<path d="M36 28c-5-8-4-14 1-19 5 6 5 12-1 19zM25 57c-5-6-5-11-1-15 5 4 5 9 1 15zM47 57c5-6 5-11 1-15-5 4-5 9-1 15z" stroke-width="1.3" {i}/>
<path d="M20 38c4 2 7 5 10 9M52 34c-4 2-7 5-10 9M14 61c14-3 30-3 45 0" stroke-width=".95" {i}/>
""",
    "science/era": """
<circle cx="34" cy="34" r="20" stroke-width="2.0" {i}/>
<path d="M34 19v16l10 7M18 17l-5 5M13 22h7" stroke-width="1.4" {i}/>
<path d="M50 48c6 3 9 7 10 12M59 60l-1-5-5 2" stroke-width="1.2" {i}/>
<path d="M22 24c4-4 8-6 13-7M42 19c4 2 7 4 9 8" stroke-width=".9" {i}/>
""",
    "science/harvest": """
<path d="M36 59V23M36 35c-8-7-13-8-18-4 2 8 8 11 18 10M36 41c7-7 13-8 18-4-2 8-8 11-18 10" stroke-width="1.95" {i}/>
<path d="M36 23c-5-7-4-12 1-17 5 6 5 11-1 17zM18 24c-4-6-3-10 1-14 4 5 4 9-1 14zM54 24c4-6 3-10-1-14-4 5-4 9 1 14z" fill="#262522" opacity=".16"/>
<path d="M36 23c-5-7-4-12 1-17 5 6 5 11-1 17zM18 24c-4-6-3-10 1-14 4 5 4 9-1 14zM54 24c4-6 3-10-1-14-4 5-4 9 1 14z" stroke-width="1.3" {i}/>
<path d="M22 38c4 2 8 5 12 10M50 36c-4 2-8 5-12 10M13 61c14-3 30-3 46 0" stroke-width=".95" {i}/>
""",
    "science/hero": """
<path d="M36 12l5 13 14 2-11 8 3 15-11-8-12 8 4-15-11-8 14-2z" stroke-width="1.85" {i}/>
<path d="M36 48v12M29 56l7 5 7-5M23 31l13 4 13-4" stroke-width="1.25" {i}/>
<path d="M15 19l2 4M57 19l-2 4M36 7v4" stroke-width="1.05" {i}/>
""",
    "science/holiday": """
<path d="M36 12l-5 10 4-1-8 12 5-1-11 15h30L40 32l5 1-8-12 4 1z" fill="#262522" opacity=".16"/>
<path d="M36 12l-5 10 4-1-8 12 5-1-11 15h30L40 32l5 1-8-12 4 1z" stroke-width="1.9" {i}/>
<path d="M36 47v13M23 60h26M27 37c6 2 12 2 18 0M21 47c10 3 20 3 30 0" stroke-width="1.2" {i}/>
<circle cx="30" cy="34" r="2" stroke-width="1.05" {i}/><circle cx="43" cy="44" r="2" stroke-width="1.05" {i}/>
<path d="M36 12v-5M32 9l4-4 4 4" stroke-width="1.0" {i}/>
""",
    "science/lie": """
<path d="M36 13c-12 0-21 9-21 21s9 21 21 21 21-9 21-21-9-21-21-21z" stroke-width="2.0" {i}/>
<path d="M23 30c4-3 8-3 12 0M49 30c-4-3-8-3-12 0M25 45c4-4 8-4 12 0 4-4 8-4 12 0" stroke-width="1.5" {i}/>
<path d="M36 34c-2 3-2 6 0 8M28 22c3-2 6-3 9-3M44 19c3 0 6 1 8 3" stroke-width="1.05" {i}/>
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
