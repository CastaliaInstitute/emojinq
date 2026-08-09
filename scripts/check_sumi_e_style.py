#!/usr/bin/env python3
"""Check that every shipped SVG uses the Emojinq sumi-e contract."""

from __future__ import annotations

import argparse
from pathlib import Path

from style_contract import SUMI_E_STYLE, SUMI_E_STROKE_SYSTEM, assert_sumi_e


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets"))
    args = parser.parse_args()
    files = sorted(args.root.rglob("*.svg"))
    failures = []
    for path in files:
        try:
            assert_sumi_e(path)
        except ValueError as exc:
            failures.append(str(exc))
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"Sumi-e SVG contract checked: {len(files)} SVGs ({SUMI_E_STYLE}, {SUMI_E_STROKE_SYSTEM})")


if __name__ == "__main__":
    main()
