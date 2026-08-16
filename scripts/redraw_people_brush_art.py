#!/usr/bin/env python3
"""Vector-only sumi-e studies with authored brush gestures, not pictograms."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = {
"people/farmer": r'''
<path class="ink-wash" fill="#4a4943" d="M13 22c7-8 18-11 31-8 8 2 14 6 18 12-9-3-17-2-24 1-7 3-15 4-24 2-2-2-2-4-1-7z"/>
<path class="ink-stroke" d="M13 22c7-7 17-10 29-8 8 1 15 5 20 10M17 25c9-3 19-3 28 0" stroke="#262522" stroke-width="2.15" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M28 18c-2 3-2 7 1 10 2 2 5 2 8 1 2-1 4-3 5-5M38 24c3 2 5 4 6 7" stroke="#262522" stroke-width="1.05" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#68675f" d="M28 28c7-3 14-1 18 5 3 5 1 12-3 17-3 4-3 8-1 13-9 3-17 1-24-4 5-7 7-13 6-19-1-5 0-9 4-12z"/>
<path class="ink-stroke" d="M31 29c-4 6-5 12-3 18 2 6 1 11-3 16M43 33c3 6 2 12-2 17-3 4-3 8 0 13" stroke="#262522" stroke-width="1.45" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M29 39c4 2 8 2 12 0M30 46c4 2 8 2 12 0M32 53c3 2 6 2 9 1" stroke="#262522" stroke-width=".8" fill="none" opacity=".72"/>
<path class="ink-wash" fill="#383732" d="M27 44c-5 5-10 10-17 15 5 3 11 4 17 2 5-2 8-6 10-12-4 0-7-2-10-5zM46 44c4 5 9 10 16 14-5 3-11 4-17 2-4-2-7-6-8-11 3-1 6-3 9-5z"/>
<path class="ink-stroke" d="M27 45c-4 7-10 12-17 14M47 45c4 6 9 10 16 13M10 60c6 2 12 1 18-2M48 59c5 2 10 2 15 0" stroke="#262522" stroke-width="1.55" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M27 34c-5 2-9 5-12 9M45 35c4 1 8 3 11 6" stroke="#262522" stroke-width="1.35" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M61 12c-1 14-2 30-2 48" stroke="#262522" stroke-width="1.05" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M6 64c14-3 28-1 41 1 8 1 15 0 21-3" stroke="#262522" stroke-width=".72" fill="none" opacity=".52"/>
''',
"people/sage": r'''
<path class="ink-wash" fill="#4b4a44" d="M18 22c3-9 10-15 20-16 9-1 17 3 21 10-8-2-16-1-22 3-6 4-12 5-19 3z"/>
<path class="ink-stroke" d="M18 22c5-8 12-12 22-12 8 0 14 2 19 7M21 25c8-3 16-4 24-1" stroke="#262522" stroke-width="2.1" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M36 18c-4 1-6 4-6 8 0 3 2 5 5 5l4-2M39 29c3 2 5 4 6 7" stroke="#262522" stroke-width="1.05" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#66655e" d="M31 28c7-3 14-1 18 5 4 7 1 14-3 19-3 4-4 8-2 13-8 3-17 2-24-3 5-7 7-14 6-20-1-6 1-11 5-14z"/>
<path class="ink-stroke" d="M33 29c-4 7-5 13-3 19 2 6 1 11-3 17M45 34c2 6 1 12-3 17-3 4-3 8 0 13" stroke="#262522" stroke-width="1.45" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M31 39c4 2 8 2 12 0M31 47c4 2 8 2 12 0M34 54c3 1 6 1 9 0" stroke="#262522" stroke-width=".78" fill="none" opacity=".7"/>
<path class="ink-wash" fill="#393833" d="M27 45c-5 6-10 11-17 15 5 3 11 3 17 1 5-2 8-6 10-12-4 0-7-2-10-4zM47 45c5 5 10 10 17 13-6 3-12 3-17 1-4-2-7-6-8-11 3-1 5-2 8-3z"/>
<path class="ink-stroke" d="M27 46c-4 6-10 11-17 14M48 46c4 6 9 10 16 12M11 61c6 1 12 0 18-3M49 60c5 1 10 1 15-1" stroke="#262522" stroke-width="1.55" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#302f2b" d="M55 27c3 8 5 20 5 33l-4 2-3-20z"/>
<path class="ink-stroke" d="M56 24c1 14 2 28 2 38M53 33h7M53 41h7" stroke="#262522" stroke-width=".95" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M8 17c5-3 10-4 15-3M12 10c4-2 9-2 13 0" stroke="#262522" stroke-width=".75" fill="none" opacity=".52"/>
''',
"people/healer": r'''
<path class="ink-wash" fill="#4c4b45" d="M20 21c3-8 10-13 19-14 9 0 16 4 19 11-8-2-15 0-21 4-5 3-11 4-17 2z"/>
<path class="ink-stroke" d="M20 21c5-7 12-11 21-11 7 0 12 2 17 6M23 24c7-3 15-3 22 0" stroke="#262522" stroke-width="2.05" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M35 18c-4 2-5 5-4 8 1 3 3 4 6 4l4-3M40 28c3 2 5 4 6 7" stroke="#262522" stroke-width="1.0" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#706f67" d="M32 27c7-2 13 1 16 7 3 6 0 13-4 18-3 4-3 8-1 13-8 2-16 0-23-5 5-6 7-13 6-19-1-6 1-11 6-14z"/>
<path class="ink-stroke" d="M34 28c-4 6-5 12-3 18 2 6 1 12-3 18M46 34c2 7 0 12-4 18-3 4-3 8-1 13" stroke="#262522" stroke-width="1.4" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M32 38c4 2 8 2 12 0M32 46c4 2 8 2 12 0M35 53c3 1 6 1 9 0" stroke="#262522" stroke-width=".78" fill="none" opacity=".68"/>
<path class="ink-wash" fill="#373631" d="M28 43c-5 4-11 9-18 15 6 3 12 3 18 1 4-2 7-6 9-11-3-1-6-3-9-5zM47 43c4 4 9 9 15 14-5 3-11 4-17 2-4-2-7-6-8-10 4-2 7-4 10-6z"/>
<path class="ink-stroke" d="M28 44c-4 6-10 11-17 14M48 44c4 6 9 10 15 13M12 60c6 2 11 1 17-2M49 59c5 2 9 2 14 0" stroke="#262522" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M28 33c4 3 9 3 13 0M35 31v10M31 36h8" stroke="#262522" stroke-width="1.0" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M8 27c4-3 8-4 12-3M53 21c4 0 8 2 12 5" stroke="#262522" stroke-width=".72" fill="none" opacity=".5"/>
''',
}

for key, body in ART.items():
    path = ROOT / "assets/pua" / f"{key}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    category, name = key.split("/", 1)
    label = f"{category} / {name}"
    body = body.replace('class="ink-stroke" d=', 'class="ink-stroke" pathLength="1" d=')
    svg = (f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="{label}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>{label} — naturalist sumi-e study</title><g transform="translate(10.08 10.08) scale(.72)">{body}</g></svg>
''')
    path.write_text(svg)
print(f"redrew {len(ART)} naturalist brush studies")
