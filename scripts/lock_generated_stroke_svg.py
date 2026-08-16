#!/usr/bin/env python3
"""Convert legacy authored specimens to the canonical stroke-only contract.

Upstream files in ``assets/source`` are intentionally excluded; they remain
the attribution-preserving OpenMoji inputs.  Every authored/generated SVG is
normalized so the repository cannot contain a second, filled treatment.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import taper

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = [
    ROOT / "assets" / "generated",
    ROOT / "assets" / "canonical",
    ROOT / "assets" / "ink",
    ROOT / "assets" / "line",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, action="append", help="directory to normalize (repeatable)")
    args = parser.parse_args()
    roots = args.root or DEFAULT_ROOTS
    for root_dir in roots:
        for path in sorted(root_dir.glob("*.svg")):
            tree = ET.parse(path)
            root = tree.getroot()
            taper(root)
            # Clear inherited paint on groups as well as explicit shape paint;
            # child strokes already carry their own fill="none" contract.
            for element in root.iter():
                fill = element.get("fill", "").strip().lower()
                if fill and fill not in {"none", "transparent"}:
                    element.set("fill", "none")
            root.set("data-castalia-style", "sumi-e-ink-wash-v1")
            root.set("data-ink-stroke-system", "tapered-v1")
            root.set("data-ink-coverage", "complete")
            root.set("data-ink-pressure", "loaded-middle-v1")
            tree.write(path, encoding="utf-8", xml_declaration=True)
            print(f"locked stroke contract: {path}")


if __name__ == "__main__":
    main()
