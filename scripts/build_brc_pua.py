#!/usr/bin/env python3
"""Generate the Black Rock City PUA glyph set (F1460+) as tapered-ink SVGs.

The Man himself, the Temple, an art car and a shade structure — the four
things a city in the dust is made of. Drawn with the same brush as the cosmos
block, whose helpers this borrows outright rather than copying: one stroke
synthesiser, one style, one set of checks.

Usage: python3 scripts/build_brc_pua.py            # writes assets/pua/brc/
       python3 scripts/build_brc_pua.py --manifest # also updates the manifest
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cosmos_pua as base  # noqa: E402  (the shared brush)

from build_cosmos_pua import S, L, D, Pat, circ, earc, panel  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATEGORY = "brc"
BLOCK_START = 0xF14B0   # F1460 was taken by the dinosaurs block; this sits clear of everything in use
OUT_DIR = ROOT / "assets" / "pua" / CATEGORY

# ── the glyphs ────────────────────────────────────────────────────────
#
# The Man is the whole point of the set: two limbs that sweep out at the
# shoulders, cross close at the waist and open again at the feet — the
# ")(" that reads as a figure with its arms up — under a diamond head.

GLYPHS = {
    "man": [
        # left limb: arm tip, in to the waist, out to the foot
        S([(15, 9), (24, 22), (31, 36), (24, 51), (17, 64)], [1.5, 3.4, 3.8, 3.4, 1.6]),
        # right limb, its mirror
        S([(57, 9), (48, 22), (41, 36), (48, 51), (55, 64)], [1.5, 3.4, 3.8, 3.4, 1.6]),
        # the diamond head
        L([(36, 5), (44, 14), (36, 23), (28, 14)], 2.6),
    ],
    "temple": [
        # a spire in tiers, the way the real one stacks
        S([(20, 62), (28, 40), (36, 12)], [3.0, 2.4, 1.4]),
        S([(52, 62), (44, 40), (36, 12)], [3.0, 2.4, 1.4]),
        S([(24, 50), (36, 46), (48, 50)], [1.4, 2.2, 1.4]),
        S([(27, 38), (36, 35), (45, 38)], [1.2, 1.9, 1.2]),
        S([(16, 63), (36, 60), (56, 63)], [1.4, 2.6, 1.4]),
        D(36, 9, 2.2),
    ],
    "art-car": [
        # a bus that someone welded a shape onto
        L([(12, 46), (16, 33), (52, 31), (60, 46)], 2.6),
        S([(20, 31), (26, 20), (40, 18), (44, 29)], [1.3, 2.2, 2.2, 1.3]),
        S([(30, 20), (32, 10)], [1.4, 0.7]),
        L(circ(22, 50, 5.0, 12), 2.0),
        L(circ(50, 50, 5.0, 12), 2.0),
        S([(14, 40), (58, 38)], [1.0, 1.0]),
    ],
    "shade": [
        # four poles and a stretched roof: the commonest building in the city
        S([(10, 26), (36, 18), (62, 26)], [1.8, 3.0, 1.8]),
        S([(14, 26), (14, 56)], [2.2, 1.4]),
        S([(58, 26), (58, 56)], [2.2, 1.4]),
        S([(28, 22), (28, 50)], [1.4, 0.9]),
        S([(44, 22), (44, 50)], [1.4, 0.9]),
        S([(12, 56), (60, 56)], [1.2, 1.2]),
    ],
}
ORDER = ["man", "temple", "art-car", "shade"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", action="store_true", help="update assets/pua/manifest.json")
    args = parser.parse_args()

    # point the shared builder at this block
    base.CATEGORY = CATEGORY
    base.BLOCK_START = BLOCK_START
    base.OUT_DIR = OUT_DIR
    base.GLYPHS = GLYPHS
    base.ORDER = ORDER

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in ORDER:
        (OUT_DIR / f"{name}.svg").write_text(base.build_svg(name))
    print(f"wrote {len(ORDER)} glyphs → {OUT_DIR}")

    if args.manifest:
        entries = json.loads(base.MANIFEST.read_text())
        entries = [e for e in entries if not e.get("label", "").startswith(CATEGORY + "/")]
        for i, name in enumerate(ORDER):
            cp = BLOCK_START + i
            entries.append({
                "name": f"{cp:05X}",
                "source": f"{CATEGORY}/{name}.svg",
                "codepoints": [cp],
                "label": f"{CATEGORY}/{name}",
            })
        base.MANIFEST.write_text(json.dumps(entries, indent=2) + "\n")
        print(f"manifest updated: {len(entries)} entries")


if __name__ == "__main__":
    main()
