#!/usr/bin/env python3
"""Check that the static browser catalog is wired to the current assets."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    page = Path("docs/all.html").read_text()
    pua = json.loads(Path("assets/pua/manifest.json").read_text())
    gray = json.loads(Path("assets/gray-all/manifest.json").read_text())
    divination = json.loads(Path("assets/divination/manifest.json").read_text())

    required = ("puaRoot", "manifest.json", "Emojinq-Regular.ttf", "@font-face")
    missing = [token for token in required if token not in page]
    if missing:
        raise SystemExit(f"catalog wiring missing: {', '.join(missing)}")
    if len(pua) != 751:
        raise SystemExit(f"unexpected PUA manifest count: {len(pua)}")
    if not gray or not divination:
        raise SystemExit("catalog source manifests are unexpectedly empty")
    print(f"catalog checked: {len(gray)} emoji, {len(divination)} divination, {len(pua)} PUA entries")


if __name__ == "__main__":
    main()
