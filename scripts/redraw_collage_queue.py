#!/usr/bin/env python3
"""Replace PUA studies that visibly contain accidental source-crop fragments."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "objects/drum": '''
<path d="M18 25c0-6 8-10 18-10s18 4 18 10v25c0 6-8 10-18 10s-18-4-18-10z" stroke-width="2.7" {c}/>
<path d="M18 25c0 6 8 10 18 10s18-4 18-10M18 50c0 6 8 10 18 10s18-4 18-10M22 27v22M28 31v25M44 31v25M50 27v22" stroke-width="1.25" opacity=".78" {c}/>
<path d="M22 23c4-4 24-4 28 0M14 64h44" stroke-width="1.05" opacity=".62" {c}/>
''',
    "people/health": '''
<circle cx="36" cy="22" r="8" stroke-width="2.2" {c}/>
<path d="M25 60c0-14 4-23 11-23s11 9 11 23M22 46c3-6 8-9 14-9s11 3 14 9M36 38v12M31 45h10" stroke-width="2.45" {c}/>
<path d="M20 60c2-6 6-10 11-12M52 60c-2-6-6-10-11-12M31 16c2-3 8-3 10 0" stroke-width="1.15" opacity=".68" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/science": '''
<path d="M30 18h12M34 18v15l-13 22c-2 4 1 7 5 7h20c4 0 7-3 5-7L38 33V18" stroke-width="2.45" {c}/>
<path d="M27 49h18M29 54c5-3 10-3 16 0M48 26h10v17M53 23v20" stroke-width="1.35" opacity=".76" {c}/>
<circle cx="53" cy="17" r="4" stroke-width="1.5" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "science/story": '''
<path d="M13 20c8-4 15-3 23 2v37c-8-5-15-6-23-2zM59 20c-8-4-15-3-23 2v37c8-5 15-6 23-2z" stroke-width="2.35" {c}/>
<path d="M18 29h13M18 35h12M18 41h10M54 29H41M54 35H42M54 41H44" stroke-width="1.2" opacity=".7" {c}/>
<path d="M36 22v37M16 62h40" stroke-width="1.1" opacity=".62" {c}/>
''',
    "science/medicine": '''
<path d="M22 48c0-7 6-12 14-12s14 5 14 12-6 11-14 11-14-4-14-11z" stroke-width="2.4" {c}/>
<path d="M25 45c5 3 17 3 22 0M31 34l5-11 5 11M30 23h12" stroke-width="1.45" {c}/>
<path d="M51 24c4-4 8-3 10 1-2 3-5 5-9 4M52 29c-2 8-5 13-9 16" stroke-width="1.45" opacity=".78" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/safety": '''
<path d="M36 12l22 8v17c0 13-9 22-22 27-13-5-22-14-22-27V20z" stroke-width="2.5" {c}/>
<circle cx="36" cy="31" r="6" stroke-width="1.7" {c}/>
<path d="M24 51c1-9 5-13 12-13s11 4 12 13M31 31c1 2 3 3 5 3s4-1 5-3" stroke-width="1.55" {c}/>
<path d="M36 17v7" stroke-width="1.1" opacity=".65" {c}/>
''',
    "science/ancestor": '''
<path d="M27 56c0-12 4-21 12-27 4-3 7-8 6-13-1-4-5-6-9-5-5 1-9 7-9 13 0 7 4 11 10 12" stroke-width="2.5" {c}/>
<path d="M35 58c2-8 7-13 14-16M28 59c-5-4-9-5-14-4M43 20c5 1 8 4 9 8M18 26c4-3 8-4 12-3" stroke-width="1.35" opacity=".76" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/stewardship": '''
<path d="M36 58V30M36 42c-8-7-15-6-20 0 7 3 13 3 20 0zM36 37c7-9 14-9 20-3-6 5-13 6-20 3z" stroke-width="2.1" {c}/>
<path d="M36 30c-2-6 0-11 6-14 3 6 1 11-6 14zM36 46c-4 2-7 6-8 12M36 46c4 2 7 6 8 12" stroke-width="1.45" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/law": '''
<path d="M36 14v43M22 20h28M16 59h40" stroke-width="2.35" {c}/>
<path d="M22 20L12 39h20zM50 20L40 39h20z" stroke-width="1.7" {c}/>
<path d="M12 39c2 5 5 7 10 7s8-2 10-7M40 39c2 5 5 7 10 7s8-2 10-7" stroke-width="1.45" {c}/>
<circle cx="36" cy="14" r="3" stroke-width="1.25" {c}/>
''',
    "science/century": '''
<path d="M36 59V24M36 24c-7-8-16-7-20 0 7 2 14 2 20 0zM36 35c7-8 16-7 20 0-7 2-14 2-20 0z" stroke-width="2.2" {c}/>
<path d="M21 59c2-8 7-12 15-14 8 2 13 6 15 14M28 45c2-5 5-8 8-10M44 45c-2-5-5-8-8-10" stroke-width="1.35" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "science/culture": '''
<path d="M22 27h28l-3 28c-1 6-5 9-11 9s-10-3-11-9z" stroke-width="2.45" {c}/>
<path d="M22 27c0-5 6-8 14-8s14 3 14 8-6 8-14 8-14-3-14-8zM27 43c6 3 14 3 19 0M29 50c5 2 11 2 16 0" stroke-width="1.35" opacity=".8" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "science/other": '''
<path d="M36 12c12 8 17 19 14 31-2 10-8 17-14 20-6-3-12-10-14-20-3-12 2-23 14-31z" stroke-width="2.45" {c}/>
<path d="M36 15c-2 10-2 22 0 45M28 22c5 4 11 5 17 2M24 33c7 4 15 5 23 2M25 45c7 3 14 4 22 1" stroke-width="1.25" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "science/memory": '''
<path d="M36 59c-2-14 0-27 8-39 4-5 8-7 13-7-1 6-4 10-10 12M36 48c-7-6-13-7-19-4 3 6 8 9 15 9" stroke-width="2.2" {c}/>
<path d="M44 20c-2 7-5 12-9 16M29 39c-4 2-7 5-9 9M36 58c-5-1-10-1-15 1" stroke-width="1.3" opacity=".73" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/memory": '''
<path d="M20 37c0-13 7-22 16-22s16 9 16 22-7 20-16 20-16-7-16-20z" stroke-width="2.35" {c}/>
<path d="M27 29c3-4 6-4 9 0 3-4 6-4 9 0M27 38c3-4 6-4 9 0 3-4 6-4 9 0M28 47c3-3 6-3 8 0 3-3 6-3 8 0" stroke-width="1.45" {c}/>
<path d="M30 15c1-5 4-8 9-9 1 5-2 9-9 9zM36 57v7M28 64h16" stroke-width="1.25" opacity=".74" {c}/>
''',
    "people/promise": '''
<path d="M18 28c4-5 9-6 14-2l4 4 4-4c5-4 10-3 14 2-1 8-7 14-18 22-11-8-17-14-18-22z" stroke-width="2.35" {c}/>
<path d="M22 30c4 2 7 5 10 9M50 30c-4 2-7 5-10 9M36 30v17" stroke-width="1.35" opacity=".75" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "locations/post": '''
<path d="M21 22h30v25H21zM27 22v-7h18v7M29 31h14M29 37h10" stroke-width="2.35" {c}/>
<path d="M36 47v13M28 60h16M16 64h40" stroke-width="1.35" opacity=".75" {c}/>
<path d="M26 16c3-3 6-3 9 0M40 16c3-3 6-3 9 0" stroke-width="1.15" opacity=".64" {c}/>
''',
    "science/demand": '''
<path d="M36 60c-5-9-5-18-1-28 2-5 6-8 10-7 4 1 5 5 3 8-2 3-5 4-8 3M36 42c-5-5-9-6-13-3-3 3-1 7 3 8 4 1 7-1 10-5" stroke-width="2.35" {c}/>
<path d="M45 25c3-4 7-6 12-5-2 5-6 7-12 5zM36 60c-3 2-7 3-11 2M36 60c3 2 7 3 11 2" stroke-width="1.35" opacity=".75" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/ancestor": '''
<path d="M26 58c0-13 4-24 12-30 5-4 8-9 7-14-1-4-5-6-9-5-6 2-9 8-8 14 1 7 5 10 11 11" stroke-width="2.45" {c}/>
<path d="M32 58c2-9 7-14 14-17M27 59c-4-4-8-5-13-3M44 19c5 1 8 4 9 8M19 27c4-3 8-4 12-3" stroke-width="1.35" opacity=".75" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/firefighter": '''
<path d="M36 17c-7 8-11 13-11 22 0 11 5 19 11 23 6-4 11-12 11-23 0-9-4-14-11-22z" stroke-width="2.4" {c}/>
<path d="M28 31c2-4 5-7 8-10 3 3 6 6 8 10M28 44c4-3 12-3 16 0M30 51c4-2 8-2 12 0" stroke-width="1.35" opacity=".76" {c}/>
<path d="M20 60c5-3 11-4 16-4s11 1 16 4M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/ibnsina": '''
<path d="M36 16c-8 0-13 6-13 15 0 13 5 24 13 29 8-5 13-16 13-29 0-9-5-15-13-15z" stroke-width="2.35" {c}/>
<path d="M27 24c5-4 13-4 18 0M28 35c5 3 11 3 16 0M28 44c5 3 11 3 16 0M30 53c4 2 8 2 12 0" stroke-width="1.3" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/mechanic": '''
<circle cx="36" cy="25" r="8" stroke-width="2.2" {c}/>
<path d="M24 60c1-13 5-22 12-22s11 9 12 22M27 20c3-5 15-5 18 0M29 45h14" stroke-width="2.2" {c}/>
<path d="M49 44l7 7M55 43l4 4-8 8-4-4zM18 64h36" stroke-width="1.45" opacity=".76" {c}/>
''',
    "people/nurse": '''
<path d="M24 21c3-7 21-7 24 0v19c0 11-5 18-12 22-7-4-12-11-12-22z" stroke-width="2.4" {c}/>
<path d="M36 15v12M30 21h12M29 36h14M31 45c3-2 7-2 10 0M14 64h44" stroke-width="1.35" opacity=".76" {c}/>
<path d="M27 54c3-3 15-3 18 0" stroke-width="1.1" {c}/>
''',
    "people/alliance": '''
<path d="M21 33c3-7 9-10 15-5 6-5 12-2 15 5-5 5-10 8-15 13-5-5-10-8-15-13z" stroke-width="2.25" {c}/>
<path d="M22 48c4-4 9-4 14 1 5-5 10-5 14-1M27 30c3 4 6 7 9 10M45 30c-3 4-6 7-9 10" stroke-width="1.35" opacity=".76" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/farmer": '''
<path d="M36 17c-8 0-13 7-13 16 0 13 5 22 13 28 8-6 13-15 13-28 0-9-5-16-13-16z" stroke-width="2.35" {c}/>
<path d="M25 23c4-5 18-5 22 0M28 36c5 3 11 3 16 0M29 46c4 2 10 2 14 0" stroke-width="1.3" opacity=".75" {c}/>
<path d="M25 58c-4 2-7 4-10 6M47 58c4 2 7 4 10 6M14 64h44" stroke-width="1.15" opacity=".65" {c}/>
''',
    "people/fool": '''
<path d="M36 14c-7 7-10 15-10 24 0 12 4 20 10 28 6-8 10-16 10-28 0-9-3-17-10-24z" stroke-width="2.4" {c}/>
<path d="M28 30c4-3 12-3 16 0M28 40c5 3 11 3 16 0M30 50c4 2 8 2 12 0" stroke-width="1.35" opacity=".74" {c}/>
<path d="M30 18c2-3 4-5 6-7 2 2 4 4 6 7" stroke-width="1.25" {c}/>
''',
    "people/food": '''
<path d="M18 41c0-8 8-13 18-13s18 5 18 13-8 13-18 13-18-5-18-13z" stroke-width="2.35" {c}/>
<path d="M23 41c4-4 22-4 26 0M26 48c6 3 14 3 20 0M36 28V18M31 18h10" stroke-width="1.35" opacity=".76" {c}/>
<path d="M14 60c7 3 14 4 22 4s15-1 22-4" stroke-width="1.15" {c}/>
''',
    "people/hypatia": '''
<path d="M36 15c-8 0-13 7-13 16 0 13 5 23 13 29 8-6 13-16 13-29 0-9-5-16-13-16z" stroke-width="2.35" {c}/>
<path d="M27 24c5-4 13-4 18 0M28 36c5 3 11 3 16 0M29 47c4 2 10 2 14 0M36 20v37" stroke-width="1.3" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/police": '''
<path d="M36 14l20 7v16c0 12-8 21-20 28-12-7-20-16-20-28V21z" stroke-width="2.4" {c}/>
<path d="M28 35c2-6 5-9 8-9s6 3 8 9M25 51c3-8 7-12 11-12s8 4 11 12M30 22h12" stroke-width="1.45" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/progress": '''
<path d="M16 56c5-13 12-21 20-28 8-7 14-10 20-12-2 7-5 14-12 22-7 8-15 14-28 18z" stroke-width="2.35" {c}/>
<path d="M23 50c5-7 11-13 18-19M30 53c6-3 13-9 18-16M36 28l4 4M44 21l4 4" stroke-width="1.35" opacity=".75" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/spirit": '''
<path d="M36 13c-8 9-13 17-13 27 0 12 5 19 13 24 8-5 13-12 13-24 0-10-5-18-13-27z" stroke-width="2.3" {c}/>
<path d="M36 22c-4 6-6 11-6 17 0 7 2 12 6 17 4-5 6-10 6-17 0-6-2-11-6-17zM27 33c3 2 6 2 9 0M36 33c3 2 6 2 9 0" stroke-width="1.3" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "objects/bowl": '''
<path d="M17 29h38c-1 17-8 27-19 27S18 46 17 29z" stroke-width="2.45" {c}/>
<path d="M17 29c0-6 8-10 19-10s19 4 19 10-8 10-19 10-19-4-19-10zM25 45c6 3 14 3 22 0" stroke-width="1.35" opacity=".76" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "objects/pottery": '''
<path d="M25 19h22l3 11c1 14-3 25-14 31-11-6-15-17-14-31z" stroke-width="2.45" {c}/>
<path d="M25 19c2-4 20-4 22 0M23 30c7 3 19 3 26 0M27 42c5 2 13 2 18 0M30 51c4 2 8 2 12 0" stroke-width="1.35" opacity=".76" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "objects/print": '''
<rect x="20" y="18" width="32" height="38" rx="2" stroke-width="2.35" {c}/>
<path d="M26 27h20M26 34h20M26 41h14M26 49h18" stroke-width="1.35" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "objects/wonder": '''
<path d="M36 13c-6 8-10 15-10 24 0 12 4 20 10 27 6-7 10-15 10-27 0-9-4-16-10-24z" stroke-width="2.4" {c}/>
<path d="M36 20c-3 6-5 11-5 17 0 7 2 13 5 19 3-6 5-12 5-19 0-6-2-11-5-17zM28 31c5 3 11 3 16 0M29 43c4 2 10 2 14 0" stroke-width="1.35" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/aristotle": '''
<path d="M36 14c-8 0-13 7-13 16 0 13 5 23 13 29 8-6 13-16 13-29 0-9-5-16-13-16z" stroke-width="2.35" {c}/>
<path d="M27 23c5-5 13-5 18 0M28 35c5 3 11 3 16 0M29 46c4 2 10 2 14 0M36 19v39" stroke-width="1.3" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/confucius": '''
<path d="M36 15c-8 0-13 7-13 16 0 13 5 23 13 29 8-6 13-16 13-29 0-9-5-16-13-16z" stroke-width="2.35" {c}/>
<path d="M27 24c5-4 13-4 18 0M28 36c5 3 11 3 16 0M29 47c4 2 10 2 14 0M30 18c2-3 10-3 12 0" stroke-width="1.3" opacity=".74" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/cook": '''
<path d="M24 22c3-7 21-7 24 0v20c0 10-5 17-12 22-7-5-12-12-12-22z" stroke-width="2.35" {c}/>
<path d="M28 25c5-4 11-4 16 0M29 37c4 2 10 2 14 0M30 47c4 2 8 2 12 0" stroke-width="1.3" opacity=".74" {c}/>
<path d="M21 58c5-3 10-4 15-4s10 1 15 4M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
    "people/faith": '''
<path d="M36 14c-8 0-13 7-13 16 0 13 5 23 13 29 8-6 13-16 13-29 0-9-5-16-13-16z" stroke-width="2.35" {c}/>
<path d="M36 23v25M28 31h16M29 44c4 2 10 2 14 0" stroke-width="1.45" {c}/>
<path d="M14 64h44" stroke-width="1" opacity=".6" {c}/>
''',
}

for key, body in ART.items():
    category, name = key.split("/", 1)
    path = ROOT / "assets" / "pua" / category / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"{category} / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — reviewed vector study</title>{body.format(c=C)}</svg>\n'
    )
    path.write_text(svg)

print(f"redrew {len(ART)} accidental collage/crop studies")
