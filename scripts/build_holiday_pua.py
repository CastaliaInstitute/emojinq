#!/usr/bin/env python3
"""Build one stable PUA glyph for every holiday in the MSS catalog."""

from __future__ import annotations

import argparse
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "holiday"
MANIFEST = ROOT / "assets" / "pua" / "manifest.json"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

SYMBOLS = {
    "sun": "M36 13 V23 M23 26 H13 M49 26 H59 M26 16 L20 10 M46 16 L52 10 M36 27 A9 9 0 1 1 36 9 A9 9 0 0 1 36 27",
    "flame": "M36 10 C29 18 29 22 34 26 C28 29 26 35 30 40 C34 45 42 43 44 37 C46 31 41 27 39 24 C39 19 38 15 36 10 M32 39 C34 34 38 34 39 39",
    "mask": "M18 20 Q36 12 54 20 L50 39 Q36 52 22 39 Z M27 29 A3 4 0 1 0 27 28 M45 29 A3 4 0 1 0 45 28 M29 40 Q36 44 43 40",
    "bread": "M17 36 C17 24 25 18 36 19 C47 18 55 24 55 36 C47 43 25 43 17 36 Z M25 29 L28 25 M36 30 L39 25 M45 30 L48 26",
    "star": "M36 10 L40 27 L57 27 L43 37 L48 54 L36 44 L24 54 L29 37 L15 27 L32 27 Z",
    "leaf": "M52 12 C29 13 17 24 19 42 C35 45 49 35 52 12 Z M20 42 C29 33 37 25 48 17",
    "heart": "M36 51 L17 32 C8 22 22 12 30 22 L36 29 L42 22 C50 12 64 22 55 32 Z",
    "moon": "M48 12 C31 14 24 29 31 43 C35 51 44 54 53 50 C40 48 34 39 35 29 C36 21 41 16 48 12 Z",
    "lantern": "M25 20 H47 M29 15 H43 M27 20 L24 47 H48 L45 20 M29 29 H43 M29 38 H43 M36 10 V15",
    "crown": "M17 22 L24 39 H48 L55 22 L45 29 L36 18 L27 29 Z M24 44 H48",
    "cross": "M31 11 H41 V28 H53 V38 H41 V53 H31 V38 H19 V28 H31 Z",
    "gift": "M17 25 H55 V52 H17 Z M14 25 H58 V32 H14 Z M36 25 V52 M36 25 C26 23 22 18 25 14 C29 10 34 17 36 25 M36 25 C46 23 50 18 47 14 C43 10 38 17 36 25",
    "drum": "M20 22 Q36 14 52 22 V45 Q36 53 20 45 Z M20 22 Q36 30 52 22 M28 34 H44 M36 29 V47",
    "orb": "M36 11 A19 19 0 1 1 35.9 11 M17 36 H55 M36 17 V55 M24 18 C30 30 30 42 24 54 M48 18 C42 30 42 42 48 54",
    "radish": "M36 30 C24 28 18 36 21 45 C24 54 48 54 51 45 C54 36 48 28 36 30 Z M36 30 C30 23 27 16 29 10 M36 30 C42 23 45 16 43 10 M29 14 L21 11 M43 14 L51 11",
    "ship": "M15 39 H57 L49 49 H23 Z M22 39 V24 H43 V39 M43 24 L52 32 H43 M18 53 Q27 58 36 53 Q45 58 54 53",
    "book": "M16 17 Q26 14 36 21 V52 Q26 45 16 48 Z M56 17 Q46 14 36 21 V52 Q46 45 56 48 Z",
}


def slug(title: str) -> str:
    value = title.lower().replace("’", "'")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "holiday"


def symbol_for(title: str) -> str:
    t = title.lower()
    for needles, symbol in [
        (("new year", "equinox", "solstice", "yalda", "nowruz"), "sun"),
        (("candle", "advent", "lucia", "hanukkah", "light"), "lantern"),
        (("christmas", "st nicholas", "sinterklaas", "gift"), "gift"),
        (("halloween", "perchta", "krampus", "ghost", "muertos", "angelitos", "lupilor"), "mask"),
        (("epiphany", "kings", "crown", "immaculada", "guadalupe"), "crown"),
        (("valentine",), "heart"),
        (("patrick", "imbolc", "palm", "rabanos"), "leaf"),
        (("passover", "maundy", "bread", "brunch", "thanksgiving", "burns"), "bread"),
        (("good friday",), "cross"),
        (("lunar", "losar", "vodoun", "tiki", "magic flute"), "drum"),
        (("earth", "saturnalia", "meteor", "ufo"), "orb"),
        (("ass",), "radish"),
        (("andrews", "scotland", "pearl harbor"), "ship"),
        (("gita", "sunday", "stephen", "martin", "catherine"), "book"),
        (("winter", "night",), "moon"),
    ]:
        if any(needle in t for needle in needles):
            return symbol
    return "star"


def svg_for(title: str, codepoint: int, index: int) -> str:
    symbol = SYMBOLS[symbol_for(title)]
    angle = (index * 137) % 360
    # The variable halo makes each catalog entry a distinct, recognizable plate
    # while the central mark carries the holiday family semantics.
    halo = 20 + (index % 5)
    label = html.escape(f"holiday / {title}", quote=True)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="{SVG_NS}" viewBox="0 0 72 72" role="img" aria-label="{label}" data-pua="U+{codepoint:X}" data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>{label} — naturalist holiday study</title>
<g transform="rotate({angle} 36 36)" fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round">
<circle cx="36" cy="36" r="{halo}" stroke-width="1.25" stroke-dasharray="{3 + index % 4} {2 + index % 3}" />
<path d="{symbol}" stroke-width="{1.35 + (index % 3) * 0.15:.2f}" />
</g>
</svg>
'''


def titles_from_ics(path: Path) -> list[str]:
    titles = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("SUMMARY:"):
            title = line.removeprefix("SUMMARY:").strip()
            if title and title not in titles:
                titles.append(title)
    if not titles:
        raise SystemExit(f"no SUMMARY entries found in {path}")
    return titles


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ics", type=Path, required=True)
    args = parser.parse_args()
    titles = titles_from_ics(args.ics)
    OUT.mkdir(parents=True, exist_ok=True)
    entries = [entry for entry in json.loads(MANIFEST.read_text()) if not entry["source"].startswith("holiday/")]
    for index, title in enumerate(titles):
        codepoint = 0xF1600 + index
        filename = f"{slug(title)}.svg"
        (OUT / filename).write_text(svg_for(title, codepoint, index), encoding="utf-8")
        entries.append({"name": f"{codepoint:X}", "source": f"holiday/{filename}", "codepoints": [codepoint], "label": f"holiday/{title}"})
    MANIFEST.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"built {len(titles)} holiday PUA glyphs in {OUT}")


if __name__ == "__main__":
    main()
