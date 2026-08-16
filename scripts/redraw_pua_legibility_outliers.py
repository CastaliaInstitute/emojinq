#!/usr/bin/env python3
"""Repair small PUA marks that became too thin after centerline recovery."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def mark(d: str, width: float = 1.25, tone: str = "#262421", role: str = "semantic-contour") -> str:
    return (
        f'<path class="ink-stroke" data-ink-stroke="tapered" '
        f'data-ink-role="{role}" data-ink-index="0" pathLength="1" '
        f'd="{d}" fill="none" stroke="{tone}" stroke-width="{width}" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )


ART: dict[str, list[str]] = {
    "blood": [
        mark("M36 9 C30 18 22 27 22 38 C22 49 28 57 36 57 C44 57 50 49 50 38 C50 28 42 17 36 9 Z", 1.45),
        mark("M36 20 C32 27 29 34 30 40 C31 45 34 48 36 50", .78, "#4a4943", "internal-flow"),
    ],
    "bounce": [
        mark("M27 25 C30 20 38 19 43 23 C48 27 49 35 45 40 C41 45 33 46 28 42 C23 38 22 30 27 25 Z", 1.35),
        mark("M14 18 C18 13 23 11 28 11", .72, "#4a4943", "motion-arc"),
        mark("M46 11 C52 12 57 15 60 20", .68, "#77746a", "motion-arc"),
        mark("M29 56 C34 59 40 59 45 56", .72, "#4a4943", "motion-arc"),
    ],
    "stump": [
        mark("M23 27 C25 24 31 22 36 22 C42 22 48 24 50 27 L48 56 C42 59 30 59 24 56 Z", 1.35),
        mark("M23 27 C25 31 31 33 36 33 C42 33 48 31 50 27 C48 23 42 20 36 20 C30 20 25 23 23 27 Z", 1.15),
        mark("M30 25 C32 23 36 23 39 24 M34 29 C38 27 42 27 45 29", .62, "#4a4943", "growth-ring"),
        mark("M29 36 C30 42 30 48 29 54 M43 35 C42 42 42 49 43 55", .62, "#4a4943", "bark-grain"),
    ],
    "cloth": [
        mark("M18 27 C24 23 31 24 36 27 C42 24 49 24 54 28 L49 49 C41 53 29 52 21 48 Z", 1.30),
        mark("M36 27 C34 34 33 41 35 49 M25 31 C29 34 32 35 35 35 M39 35 C44 33 47 31 51 30", .72, "#4a4943", "fold-line"),
    ],
    "leather": [
        mark("M20 24 C27 21 39 22 48 25 C53 28 55 35 52 42 C48 49 37 51 28 48 C21 45 18 37 20 30 Z", 1.30),
        mark("M26 27 C29 33 34 37 41 39 C45 40 49 39 52 37", .68, "#4a4943", "hide-fold"),
        mark("M30 43 C34 42 38 43 42 45", .60, "#77746a", "hide-fold"),
    ],
    "metal": [
        mark("M19 30 L49 24 L55 42 L24 49 Z", 1.35),
        mark("M25 31 L31 45 M34 29 L40 44 M43 27 L49 43", .64, "#4a4943", "hammered-plane"),
    ],
    "stone": [
        mark("M20 43 L23 31 L34 23 L49 27 L54 39 L45 49 L29 51 Z", 1.35),
        mark("M23 31 L35 36 L49 27 M35 36 L45 49 M35 36 L34 23", .65, "#4a4943", "facet-line"),
    ],
    "black": [
        mark("M23 25 C29 22 43 22 49 25 L49 47 C42 50 30 50 23 47 Z", 1.30),
        mark("M28 30 C33 33 39 33 44 30 M28 37 C33 40 39 40 44 37", .66, "#4a4943", "tone-mark"),
    ],
    "brown": [
        mark("M23 25 C29 22 43 22 49 25 L49 47 C42 50 30 50 23 47 Z", 1.30, "#4a4943"),
        mark("M28 31 C33 34 39 34 44 31 M28 39 C33 42 39 42 44 39", .68, "#77746a", "tone-mark"),
    ],
    "cube": [
        mark("M36 18 L52 27 L52 45 L36 54 L20 45 L20 27 Z", 1.30),
        mark("M36 18 L36 36 L52 27 M36 36 L20 27 M36 36 L36 54", .78, "#4a4943", "cube-edge"),
    ],
    "pattern": [
        mark("M22 36 C27 27 32 27 36 36 C40 45 45 45 50 36", 1.05),
        mark("M22 36 C27 45 32 45 36 36 C40 27 45 27 50 36", .76, "#4a4943", "repeat-motif"),
    ],
    "log": [
        mark("M18 28 C24 24 42 24 51 29 L51 45 C42 50 25 49 18 44 Z", 1.30),
        mark("M18 28 C21 32 21 40 18 44 C21 48 26 48 29 46 C31 41 31 32 29 27", .92, "#4a4943", "cut-end"),
        mark("M36 30 C39 35 39 41 36 46 M43 29 C46 34 46 41 44 45", .60, "#77746a", "bark-grain"),
    ],
    "divide": [
        mark("M15 36 C25 35 35 35 44 36 C50 36 56 36 62 36", 1.40),
        mark("M34 25 C34 21 38 20 40 23 C42 26 40 29 37 29 C35 29 34 27 34 25 Z", 1.05, "#4a4943", "division-dot"),
        mark("M34 47 C34 43 38 42 40 45 C42 48 40 51 37 51 C35 51 34 49 34 47 Z", 1.05, "#4a4943", "division-dot"),
    ],
    "one": [
        mark("M25 24 C29 22 32 19 35 16 C36 28 35 43 36 58", 1.65),
        mark("M27 58 C33 60 40 60 46 58", .76, "#4a4943", "terminal"),
    ],
}

CATEGORY_HINTS = {
    "pattern": "patterns",
    "one": "science",
    "log": "plants",
}


def write(name: str, marks: list[str]) -> None:
    matches = list((ROOT / "assets" / "pua").rglob(f"{name}.svg"))
    if name in CATEGORY_HINTS:
        matches = [path for path in matches if path.parent.name == CATEGORY_HINTS[name]]
    if len(matches) != 1:
        raise SystemExit(f"expected one PUA source for {name}, found {len(matches)}")
    source = matches[0]
    text = source.read_text(encoding="utf-8")
    codepoint = re.search(r'data-pua="([^"]+)"', text)
    if not codepoint:
        raise SystemExit(f"missing data-pua in {source}")
    category = source.parent.name
    source.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" '
        f'aria-label="{category} / {name}" {codepoint.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1" '
        'data-ink-animation="draw-v1" data-ink-path-units="normalized" '
        'data-ink-coverage="complete" data-ink-pressure="loaded-middle-v1" '
        'data-pua-filter="manual-legibility-v1">'
        f'<title>{category} / {name} — stroke-only semantic study</title>'
        f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">{"".join(marks)}</g></svg>\n',
        encoding="utf-8",
    )
    print(f"repaired {category}/{name}")


def main() -> None:
    for name, marks in ART.items():
        write(name, marks)


if __name__ == "__main__":
    main()
