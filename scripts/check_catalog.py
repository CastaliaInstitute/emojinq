#!/usr/bin/env python3
"""Check that the static browser catalog is wired to the current assets."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    page = Path("docs/all.html").read_text()
    pua = json.loads(Path("assets/pua/manifest.json").read_text())
    gray = json.loads(Path("assets/gray-all/manifest.json").read_text())
    divination = json.loads(Path("assets/divination/manifest.json").read_text())

    required = (
        "puaRoot",
        "developmental-vocabulary.json",
        "manifest.json",
        "Emojinq-Regular.ttf",
        "@font-face",
        'name="recognition"',
        "needs more defining brush strokes",
        '<select id="coverage">',
        '<option value="all">All sequences</option>',
        "const PAGE_SIZE = 240;",
        "const allItems = [...rankedEmojiItems, ...sharedItems];",
        "location.hostname.endsWith(\"github.io\")",
        "Open review issue on GitHub",
        "Color wash · standard + 12 PUA pigments",
        '<option value="blind">Label-blind test</option>',
        'name="guess"',
        "Label-blind guess:",
    )
    missing = [token for token in required if token not in page]
    if missing:
        raise SystemExit(f"catalog wiring missing: {', '.join(missing)}")
    # The original library had 782 PUA studies; the catalog is intentionally
    # extensible as new naturalist families are added. Never allow an
    # accidental shrink, but do not make the browser test reject a valid
    # expansion.
    if len(pua) < 782:
        raise SystemExit(f"PUA manifest unexpectedly shrank: {len(pua)}")
    if not gray or not divination:
        raise SystemExit("catalog source manifests are unexpectedly empty")
    if sum(entry.get("brushed") is not False for entry in gray) != len(gray):
        raise SystemExit("catalog would hide standard entries marked brushed=false")
    match = re.search(r"<script>(.*?)</script>", page, re.DOTALL)
    if not match:
        raise SystemExit("catalog inline script is missing")
    node = shutil.which("node")
    if node:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as script:
            script.write(match.group(1))
            script.flush()
            subprocess.run([node, "--check", script.name], check=True)
    if "omitted sequences" in page.lower():
        raise SystemExit("catalog still claims sequences are omitted")
    print(f"catalog checked: {len(gray)} emoji, {len(divination)} divination, {len(pua)} PUA entries")


if __name__ == "__main__":
    main()
