#!/usr/bin/env python3
"""Check that every shipped SVG uses the Emojinq sumi-e contract."""

from __future__ import annotations

import argparse
from pathlib import Path

from style_contract import VALID_CONTRACTS, assert_sumi_e


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets"))
    args = parser.parse_args()
    # Familiar-color derivatives have their own semantic color-wash contract;
    # the base sumi-e contract intentionally enforces neutral ink only.
    files = sorted(path for path in args.root.rglob("*.svg") if "pua-color" not in path.parts)
    failures = []
    for path in files:
        try:
            assert_sumi_e(path)
        except ValueError as exc:
            failures.append(str(exc))
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    contracts = ", ".join(f"{style}/{stroke}" for style, stroke in sorted(VALID_CONTRACTS))
    print(f"Sumi-e SVG contract checked: {len(files)} SVGs ({contracts})")


if __name__ == "__main__":
    main()
