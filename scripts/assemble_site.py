#!/usr/bin/env python3
"""Assemble the exact static artifact used by GitHub Pages."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def copy_tree(source: Path, target: Path) -> None:
    if not source.exists():
        raise SystemExit(f"required site input is missing: {source.relative_to(ROOT)}")
    shutil.copytree(source, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "pages")
    args = parser.parse_args()
    output = args.output.resolve()
    allowed_root = (ROOT / "dist").resolve()
    if output == allowed_root or allowed_root not in output.parents:
        raise SystemExit(f"refusing to replace site outside {allowed_root}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copy_tree(ROOT / "docs", output / "docs")
    for family in ("gray-all", "divination", "pua", "pua-color"):
        copy_tree(ROOT / "assets" / family, output / "assets" / family)
    for data_file in ("developmental-vocabulary.json", "pua-recognition-review.json"):
        shutil.copy2(ROOT / "assets" / data_file, output / "assets")
    (output / "fonts").mkdir()
    for font in ("Emojinq-Regular.ttf", "Emojinq-Color.ttf"):
        shutil.copy2(ROOT / "fonts" / font, output / "fonts" / font)
    shutil.copy2(ROOT / "docs" / "all.html", output / "index.html")
    shutil.copy2(ROOT / "NOTICE", output / "NOTICE")
    print(f"assembled GitHub Pages artifact at {output}")


if __name__ == "__main__":
    main()
