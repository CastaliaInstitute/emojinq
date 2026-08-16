#!/usr/bin/env python3
"""Draw a recognizable squirrel as a small sumi-e brush study.

The source squirrel was too fragmented to read at glyph size.  This version
uses a deliberately reduced anatomy: one body wash, one large curled tail,
and a few tapered marks for the head, paws, legs, eye, and tail fold.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets/pua/animals/squirrel.svg"


def main() -> None:
    existing = TARGET.read_text()
    match = re.search(r'data-pua="([^"]+)"', existing)
    if not match:
        raise SystemExit("missing squirrel PUA code point")

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img"
     aria-label="animals / squirrel" {match.group(0)}
     data-castalia-style="sumi-e-brush-art-v2"
     data-ink-stroke-system="filled-brush-mass-v2"
     data-ink-animation="wash-v1" data-ink-path-units="normalized">
  <title>animals / squirrel — naturalist sumi-e brush study</title>
  <!-- The tail is intentionally oversized: it is the primary squirrel cue. -->
  <path class="ink-wash" fill="#4a4943" d="M43 47 C50 43 56 38 58 30 C60 22 57 16 52 14 C48 12 44 14 44 18 C44 22 49 25 52 28 C55 31 53 37 48 40 C44 42 40 45 37 48 C35 51 39 52 43 47Z"/>
  <path class="ink-wash" fill="#6b6961" d="M49 42 C56 38 60 32 60 25 C60 18 56 12 51 11 C47 10 43 12 42 16 C41 20 44 23 48 25 C52 27 55 30 54 34 C53 38 49 40 45 43 C43 45 46 45 49 42Z"/>
  <!-- Compact body and haunch. -->
  <path class="ink-wash" fill="#5a5952" d="M18 40 C18 32 24 27 33 27 C42 27 49 32 50 40 C51 47 47 54 40 57 C33 59 25 57 20 52 C17 49 16 44 18 40Z"/>
  <path class="ink-wash" fill="#3f3e39" d="M28 31 C34 28 43 31 47 37 C49 42 47 49 42 53 C38 56 32 56 28 53 C32 49 34 44 32 39 C31 36 29 34 28 31Z"/>
  <!-- Head, pointed muzzle, and one readable ear. -->
  <path class="ink-wash" fill="#34332f" d="M14 36 C11 34 10 31 12 28 C14 25 18 23 22 24 L25 20 L28 25 C31 26 33 29 32 32 C31 35 27 37 23 38 L18 40 C16 40 15 38 14 36Z"/>
  <path class="ink-dry" fill="#77746a" d="M13 31 C16 29 19 29 22 30 C20 32 17 34 14 34"/>
  <path class="ink-wash" fill="#24231f" d="M24 25 C25 23 26 21 27 20 C28 22 29 24 29 26 C27 26 26 25 24 25Z"/>
  <path class="ink-wash" fill="#24231f" d="M22 28 C22.7 27 23.6 27 24.2 27.8 C24.6 28.6 24 29.5 23.2 29.5 C22.4 29.4 21.7 28.8 22 28Z"/>
  <!-- Forepaws held to the chest and two grounded hind feet. -->
  <path class="ink-wash" fill="#33322e" d="M30 37 C28 39 27 42 28 44 C29 45 31 44 32 42 L34 39 C35 37 33 36 30 37Z"/>
  <path class="ink-wash" fill="#383732" d="M25 49 C23 52 22 55 23 57 C24 59 28 59 30 57 C28 56 27 54 28 51 C28 49 27 48 25 49Z"/>
  <path class="ink-wash" fill="#383732" d="M39 50 C39 53 40 56 43 57 C45 58 48 57 49 55 C46 55 44 53 44 50 C43 48 40 48 39 50Z"/>
  <!-- A single tail-fold mark gives volume without creating a second outline. -->
  <path class="ink-dry" fill="#858178" d="M47 18 C51 19 55 23 56 27 C57 31 55 35 52 38"/>
  <path class="ink-dry" fill="#77746a" d="M18 62 C27 64 39 64 50 61"/>
</svg>
'''
    TARGET.write_text(svg)
    print(f"redrew recognizable brush squirrel at {TARGET}")


if __name__ == "__main__":
    main()
