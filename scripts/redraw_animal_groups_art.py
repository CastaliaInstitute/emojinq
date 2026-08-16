#!/usr/bin/env python3
"""Compose animal-group concepts as unified sumi-e brush studies."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/animals" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 42 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="animals / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>animals / {name} — naturalist sumi-e group study</title>{''.join(marks)}</svg>
''')


# A small colony: three distinct bees, each with body, wings, and brush-stripe
# marks. Their shared diagonal flight makes this a composition rather than a
# row of repeated icons.
bee = '''
<g transform="{t}">
  <ellipse class="ink-wash" cx="0" cy="0" rx="7" ry="3.4" fill="#3c3b36"/>
  <path class="ink-wash" fill="#77746a" d="M -2 -2 C -9 -8 -13 -6 -10 -1 C -7 1 -4 1 -2 0 Z M 2 -2 C 7 -8 12 -6 10 -1 C 7 1 4 1 2 0 Z"/>
  <path class="ink-dry" fill="#262522" d="M -2 -3 L -1 3 M 2 -3 L 3 3"/>
  <path class="ink-dry" fill="#262522" d="M 7 -1 L 11 -3 M 7 1 L 11 3"/>
</g>'''
write("colony", [
    bee.format(t="translate(20 34) rotate(-18) scale(.68)"),
    bee.format(t="translate(37 25) rotate(12) scale(.82)"),
    bee.format(t="translate(53 39) rotate(-8) scale(.58)"),
    '<path class="ink-dry" fill="#77746a" d="M 13 49 C 26 45 38 45 52 49"/>',
])

# A flock: varied bird gestures on one rising current, with open contour wings
# so the silhouettes remain recognizable at small sizes.
write("flock", [
    '<path class="ink-wash" fill="#3c3b36" d="M 10 29 C 15 24 20 24 26 29 C 21 29 18 31 15 35 C 14 32 12 30 10 29 Z"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 28 19 C 34 13 41 14 47 20 C 40 19 36 22 32 27 C 31 23 30 21 28 19 Z"/>',
    '<path class="ink-wash" fill="#262522" d="M 47 37 C 52 31 59 31 65 36 C 58 36 55 39 51 44 C 51 41 49 39 47 37 Z"/>',
    '<path class="ink-dry" fill="#77746a" d="M 12 27 C 16 23 20 22 24 24 M 30 18 C 35 13 40 12 45 14 M 49 35 C 54 30 59 30 63 32"/>',
    '<path class="ink-dry" fill="#77746a" d="M 17 42 C 27 38 37 36 47 37"/>',
])

print("redrew colony and flock as unified animal-group studies")
