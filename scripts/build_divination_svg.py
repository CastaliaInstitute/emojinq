#!/usr/bin/env python3
"""Build the small, reusable Emojinq divination symbol set.

These are intentionally simple single-glyph studies: clear silhouettes, one
brush contour, and no double-line depth marks. The SVGs can be previewed
directly and can later be added to the font manifest with PUA code points.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from style_contract import SUMI_E_STYLE, SUMI_E_STROKE_SYSTEM


INK = "#262421"
PUA_START = 0xF1300  # follows the existing Supplementary PUA corpus (U+F0000–U+F120A)


def svg(name: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" aria-label="{name}" data-castalia-style="{SUMI_E_STYLE}" data-ink-stroke-system="{SUMI_E_STROKE_SYSTEM}">
  <title>{name} — Emojinq brush glyph</title>
  <g fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">
    {body}
  </g>
</svg>
'''


def p(d: str, width: float = 4.2, fill: str = "none") -> str:
    return f'<path d="{d}" stroke-width="{width}" fill="{fill}" data-ink-stroke="tapered" />'


ICONS = {
    # Zodiac: standard Unicode aliases, redrawn in the Emojinq brush hand.
    "zodiac-aries": p("M22 49 C30 20 47 23 58 48 C66 19 84 21 96 49") ,
    "zodiac-taurus": p("M32 34 C39 18 54 18 64 29 C74 18 89 19 96 34 M64 29 C47 29 39 42 40 61 C41 82 54 92 64 92 C75 92 87 81 88 61 C89 42 81 29 64 29") ,
    "zodiac-gemini": p("M39 25 C49 30 49 98 39 104 M89 25 C79 30 79 98 89 104 M38 34 C54 40 74 40 90 34 M38 91 C54 85 74 85 90 91"),
    "zodiac-cancer": p("M28 55 C38 42 54 43 61 53 C67 63 55 72 44 65 C34 59 41 48 53 47 M100 73 C90 86 74 85 67 75 C61 65 73 56 84 63 C94 69 87 80 75 81"),
    "zodiac-leo": p("M37 42 C47 27 68 29 74 44 C80 58 70 71 58 68 C48 65 50 51 61 51 M74 44 C98 34 104 53 91 67 C84 74 86 86 101 88"),
    "zodiac-virgo": p("M28 36 L28 79 C28 94 39 98 46 87 L46 36 M46 38 C48 70 55 77 63 68 C71 59 66 43 58 39 M64 42 C76 52 78 69 72 81 C68 90 74 97 91 91"),
    "zodiac-libra": p("M29 82 C44 76 84 76 99 82 M37 69 C49 61 78 61 91 69 M64 33 C48 33 40 46 40 58 C40 67 50 71 64 71 C78 71 88 67 88 58 C88 46 80 33 64 33"),
    "zodiac-scorpio": p("M27 38 L27 72 C27 86 39 90 47 79 L47 38 M47 39 C50 68 57 76 65 68 C72 61 67 44 59 40 M67 42 C78 51 80 68 75 79 C71 88 80 96 96 88 C101 85 102 79 98 75"),
    "zodiac-sagittarius": p("M29 91 L94 28 M54 28 H94 V67 M38 47 L83 92"),
    "zodiac-capricorn": p("M29 37 C37 29 45 31 48 44 L53 78 C56 93 69 96 76 84 C81 75 76 64 68 64 C59 64 57 77 65 83 C73 89 88 83 94 74 C101 64 96 53 88 53"),
    "zodiac-aquarius": p("M25 48 C34 38 42 39 50 48 C58 57 66 57 74 48 C82 39 90 39 100 48 M25 75 C34 65 42 66 50 75 C58 84 66 84 74 75 C82 66 90 66 100 75"),
    "zodiac-pisces": p("M39 28 C53 43 53 84 39 100 M89 28 C75 43 75 84 89 100 M38 64 H90"),

    # Celestial and planetary symbols.
    "planet-sun": p("M64 20 C86 20 101 38 101 63 C101 87 85 104 64 104 C42 104 27 87 27 63 C27 39 42 20 64 20 M64 8 V18 M64 109 V120 M9 63 H20 M108 63 H119 M25 25 L34 34 M94 94 L103 103 M103 25 L94 34 M34 94 L25 103", 3.8) + p("M64 47 C73 47 80 54 80 63 C80 72 73 79 64 79 C55 79 48 72 48 63 C48 54 55 47 64 47 M64 57 V69 M58 63 H70", 3.0),
    "planet-moon": p("M82 23 C61 30 51 48 53 68 C55 87 69 101 89 104 C78 113 60 112 45 102 C28 91 20 72 25 54 C31 32 49 19 70 20 C75 20 79 21 82 23", 4.0, INK),
    "planet-mercury": p("M64 39 C53 39 46 47 46 57 C46 68 54 75 64 75 C74 75 82 68 82 57 C82 47 75 39 64 39 M64 75 V105 M49 91 H79 M55 26 C55 18 61 14 64 14 C67 14 73 18 73 26"),
    "planet-venus": p("M64 38 C51 38 43 47 43 59 C43 71 52 80 64 80 C76 80 85 71 85 59 C85 47 77 38 64 38 M64 80 V108 M47 94 H81"),
    "planet-mars": p("M62 70 C49 70 41 61 41 50 C41 39 49 31 60 31 C71 31 80 40 80 51 C80 62 72 70 62 70 M76 36 L99 13 M82 13 H99 V30"),
    "planet-jupiter": p("M47 25 C59 22 67 30 65 42 L59 92 M35 61 H76 M76 25 C89 24 97 35 91 46 C87 54 78 57 68 56"),
    "planet-saturn": p("M78 28 C69 28 61 37 61 48 V86 C61 101 76 106 86 96 C92 90 91 80 84 76 C76 71 66 78 66 88 M45 21 V102 M32 52 H73"),
    "planet-uranus": p("M47 24 L64 39 L81 24 M64 39 V89 M46 89 H82 M55 89 C55 105 73 105 73 89"),
    "planet-neptune": p("M64 18 V91 M43 36 C49 49 58 53 64 53 C70 53 79 49 85 36 M40 92 C49 84 57 84 64 92 C71 100 79 100 88 92 M48 108 H80"),
    "planet-pluto": p("M64 24 C48 24 38 35 38 48 C38 61 49 71 64 71 C79 71 90 61 90 48 C90 35 80 24 64 24 M64 71 V105 M46 91 H82"),

    # Major Arcana: symbolic silhouettes, intentionally sparse at glyph size.
    "tarot-the-fool": p("M35 102 C42 85 48 61 53 35 M49 39 C60 33 70 35 79 42 M47 24 C55 18 65 20 68 25 L55 35 M53 35 L44 27 M44 27 L36 31"),
    "tarot-the-magician": p("M64 17 V86 M48 29 H80 M44 91 H84 M35 101 H49 M79 101 H93 M34 101 L27 91 M94 101 L101 91"),
    "tarot-the-high-priestess": p("M37 102 C46 88 48 65 48 42 C48 31 56 24 64 24 C72 24 80 31 80 42 C80 65 82 88 91 102 M48 42 C55 48 73 48 80 42 M54 19 C59 14 69 14 74 19"),
    "tarot-the-empress": p("M39 36 L47 25 L55 35 L64 21 L73 35 L81 25 L89 36 L82 45 H46 Z M45 47 C50 68 52 87 64 102 C76 87 78 68 83 47 M45 47 H83"),
    "tarot-the-emperor": p("M35 94 V44 H93 V94 M28 100 H100 M43 44 V30 H55 V44 M73 44 V30 H85 V44 M47 67 H81"),
    "tarot-the-hierophant": p("M64 21 V91 M48 36 H80 M43 92 H85 M36 103 H92 M38 53 L22 69 L38 85 M90 53 L106 69 L90 85"),
    "tarot-the-lovers": p("M42 94 C32 79 33 57 47 51 C56 47 62 56 64 65 C66 56 72 47 81 51 C95 57 96 79 86 94 M49 34 C55 28 61 31 64 37 C67 31 73 28 79 34 C82 41 75 47 64 54 C53 47 46 41 49 34"),
    "tarot-the-chariot": p("M31 90 H97 M39 90 V54 H89 V90 M32 54 H96 M47 38 H81 M64 54 V75 M53 75 H75"),
    "tarot-strength": p("M34 83 C39 62 49 54 62 59 C73 63 80 75 77 89 C74 101 59 106 47 98 M54 69 C50 61 55 51 64 50 C74 49 81 57 78 65 C76 72 68 75 61 71"),
    "tarot-the-hermit": p("M64 21 V92 M49 40 C54 31 73 31 79 40 L79 71 C73 79 55 79 49 71 Z M64 48 V66 M56 57 H72 M43 94 H85"),
    "tarot-wheel-of-fortune": p("M64 18 C89 18 107 37 107 63 C107 88 89 108 64 108 C39 108 21 88 21 63 C21 37 39 18 64 18 M64 34 V92 M35 63 H93 M44 43 L84 83 M84 43 L44 83"),
    "tarot-justice": p("M64 25 V97 M42 41 H86 M31 48 L43 72 L55 48 M73 48 L85 72 L97 48 M35 75 H51 M77 75 H93 M45 100 H83"),
    "tarot-the-hanged-man": p("M28 32 H100 M64 32 V91 M47 58 C51 48 60 47 64 58 C68 47 77 48 81 58 M48 91 H80"),
    "tarot-death": p("M64 19 C44 19 32 35 35 55 C38 77 48 98 64 108 C80 98 90 77 93 55 C96 35 84 19 64 19 M49 50 H57 M71 50 H79 M52 69 C60 74 68 74 76 69 M57 87 H71"),
    "tarot-temperance": p("M64 28 V92 M48 92 H80 M45 37 C53 31 59 36 64 45 C69 36 75 31 83 37 M52 57 C58 65 64 68 70 57 M64 45 V73"),
    "tarot-the-devil": p("M64 42 C52 28 35 34 35 48 C35 58 45 64 54 59 M64 42 C76 28 93 34 93 48 C93 58 83 64 74 59 M64 42 V81 M50 81 H78 M43 101 C50 88 57 88 64 101 C71 88 78 88 85 101"),
    "tarot-the-tower": p("M42 104 L48 35 L80 35 L86 104 M48 35 L58 45 L70 35 L80 45 M52 69 H76 M64 45 V104 M31 18 L45 31 M97 18 L83 31"),
    "tarot-the-star": p("M64 17 L69 48 L102 48 L75 66 L84 101 L64 80 L44 101 L53 66 L26 48 L59 48 Z M64 80 C56 89 50 95 44 101"),
    "tarot-the-moon": p("M84 23 C65 30 55 47 57 65 C59 84 72 97 91 101 C77 111 57 110 42 100 C27 90 20 72 25 54 C30 35 47 22 66 21 C73 21 79 22 84 23 M42 84 C49 83 55 87 60 94"),
    "tarot-the-sun": p("M64 35 C82 35 94 47 94 64 C94 81 82 94 64 94 C46 94 34 81 34 64 C34 47 46 35 64 35 M64 13 V25 M64 103 V115 M13 64 H25 M103 64 H115 M27 27 L36 36 M92 92 L101 101 M101 27 L92 36 M36 92 L27 101"),
    "tarot-judgement": p("M64 24 C55 24 49 31 49 39 C49 49 56 56 64 56 C72 56 79 49 79 39 C79 31 73 24 64 24 M64 56 V91 M48 91 H80 M35 61 C36 78 45 91 64 91 C83 91 92 78 93 61"),
    "tarot-the-world": p("M64 17 C88 17 106 37 106 63 C106 89 88 109 64 109 C40 109 22 89 22 63 C22 37 40 17 64 17 M46 43 C53 34 64 32 73 38 C82 44 82 56 74 63 C66 70 55 67 50 59 C45 51 49 42 58 39 M64 70 C71 80 77 88 84 98 M44 96 C51 86 57 78 64 70"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("assets/divination"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    entries = []
    for offset, (key, body) in enumerate(ICONS.items()):
        path = args.output / f"{key}.svg"
        path.write_text(svg(key.replace("-", " ").title(), body), encoding="utf-8")
        family, label = key.split("-", 1)
        group = "PUA · Tarot" if family == "tarot" else "PUA · Astrology"
        entries.append({
            "name": key,
            "label": label.replace("-", " ").title(),
            "group": group,
            "source": path.name,
            "codepoints": [PUA_START + offset],
            "private_use": True,
        })
    (args.output / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} divination SVGs to {args.output}")


if __name__ == "__main__":
    main()
