#!/usr/bin/env python3
"""Paint a small people study in vector sumi-e brush marks.

The shapes are deliberately authored as irregular brush masses rather than
assembled pictogram geometry.  Keep this as the visual prototype for the
larger PUA redraw.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = "#262522"

ART = {
    "people/farmer": r'''
<path class="ink-wash" fill="#403f3a" d="M15 24c5-8 13-12 24-12 9 0 17 3 22 9-7-1-12 0-16 2-7-2-16 0-24 5-3 1-5 0-6-4z"/>
<path class="ink-stroke" d="M15 24c8-7 18-10 30-8 6 1 11 3 16 7" stroke="#262522" stroke-width="2.25" fill="none"/>
<path class="ink-wash" fill="#5a5952" d="M30 23c5-3 11-3 16 0 2 7 1 13-2 18-3 4-4 8-3 13-7 4-14 4-21 0 5-8 7-14 5-20-1-4 0-8 5-11z"/>
<path class="ink-stroke" d="M34 23c-4 4-5 10-4 16 1 5-1 10-5 16M45 24c4 8 3 15-1 21-2 4-2 7 0 10" stroke="#262522" stroke-width="1.65" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#34332f" d="M24 42c-3 5-7 10-13 16 6 2 12 2 18 0l3-11c-3-1-5-3-8-5zM43 42c4 5 8 10 15 15-5 3-11 3-17 1l-3-10c2-2 3-4 5-6z"/>
<path class="ink-stroke" d="M25 42c-2 8-6 14-12 17M45 42c2 7 7 13 13 16M12 59c6 1 11 0 16-2M43 58c5 2 10 2 15 0" stroke="#262522" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M16 39c-4 4-8 7-12 8M52 37c4 2 8 4 12 3" stroke="#262522" stroke-width="2.1" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M59 11c-1 15-3 31-4 48" stroke="#262522" stroke-width="1.15" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M7 63c12-2 25-1 38 1 8 1 15 0 20-2" stroke="#262522" stroke-width=".85" fill="none" opacity=".58"/>
''',
    "people/sage": r'''
<path class="ink-wash" fill="#4a4943" d="M21 23c3-11 11-17 22-17 9 0 15 4 19 11-10-3-18-2-25 2-5 3-10 4-16 4z"/>
<path class="ink-stroke" d="M20 23c5-8 13-12 23-12 7 0 13 2 19 7" stroke="#262522" stroke-width="2.35" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#65645d" d="M34 19c6 1 10 5 11 11 2 8-1 14-5 20-4 4-5 8-3 14-8 3-16 2-23-3 5-5 7-11 7-18 0-8 4-15 13-24z"/>
<path class="ink-stroke" d="M35 21c-5 7-7 14-5 21 1 5 0 12-4 20M45 28c2 8 0 14-5 20-3 4-3 9 0 15" stroke="#262522" stroke-width="1.55" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M18 35c5 3 10 4 16 3M20 44c5 3 10 4 15 3" stroke="#262522" stroke-width="1.05" fill="none" stroke-linecap="round" opacity=".8"/>
<path class="ink-wash" fill="#33322e" d="M19 47c-4 7-8 12-14 16 7 1 14 0 20-4l3-10c-3 0-6-1-9-2zM45 47c5 7 10 11 17 14-6 3-12 3-18 1l-3-10c1-2 2-4 4-5z"/>
<path class="ink-stroke" d="M20 48c-3 7-8 12-14 15M46 48c4 6 9 11 16 13M7 63c7 0 12-2 18-5M45 61c7 2 12 2 18 0" stroke="#262522" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#292824" d="M54 29c3 8 6 18 6 30l-5 2-3-19z"/>
<path class="ink-stroke" d="M56 25c1 14 2 27 2 38M52 31l8 0M52 38l8 0" stroke="#262522" stroke-width="1.05" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M8 18c6-3 12-4 18-3M12 10c5-2 10-2 15 0" stroke="#262522" stroke-width=".9" fill="none" opacity=".55"/>
''',
    "people/healer": r'''
<path class="ink-wash" fill="#494842" d="M22 22c2-8 8-14 17-15 8-1 15 3 18 10-7-2-14 0-19 4-5 4-10 5-16 4z"/>
<path class="ink-stroke" d="M22 22c5-8 12-11 21-10 6 0 11 2 15 6" stroke="#262522" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#73726a" d="M32 21c7 0 12 5 13 12 1 8-3 13-8 18-3 4-3 8-1 14-8 2-16 0-22-5 6-6 8-13 7-20-1-8 3-15 11-19z"/>
<path class="ink-stroke" d="M33 23c-5 7-6 14-4 20 2 6 1 12-3 19M44 29c2 7 0 13-4 18-4 5-4 10-1 16" stroke="#262522" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<path class="ink-wash" fill="#383732" d="M20 43c-5 3-10 7-15 13 6 4 12 5 18 4l7-10c-4-1-7-4-10-7zM45 43c4 3 9 7 14 13-5 3-11 4-17 2l-6-9c3-2 6-4 9-6z"/>
<path class="ink-stroke" d="M20 44c-4 6-9 10-15 12M46 44c4 6 8 10 14 13M6 57c6 3 12 3 18 1M47 58c5 2 9 2 14 0" stroke="#262522" stroke-width="1.75" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M27 40c4 3 8 3 12 0M33 32v9M29 36h8" stroke="#262522" stroke-width="1.1" fill="none" stroke-linecap="round"/>
<path class="ink-stroke" d="M8 27c4-3 8-4 12-4M52 21c5 0 9 2 13 5" stroke="#262522" stroke-width=".85" fill="none" opacity=".55"/>
''',
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
        'data-castalia-style="sumi-e-brush-study-v2" '
        'data-ink-stroke-system="expressive-taper-v2" '
        'data-ink-animation="draw-v1" data-ink-path-units="normalized">\n'
        f'<title>{label} — sumi-e brush study</title>{body}</svg>\n'
    )
    path.write_text(svg)


for key, body in ART.items():
    redraw(key, body)
print(f"redrew {len(ART)} vector brush studies")
